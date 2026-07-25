from __future__ import annotations

import copy
import json
import statistics
import subprocess
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
from typing import Iterable, Mapping

from . import PIPELINE_VERSION
from .bundle import atomic_write_json, sha256_file
from .domain import (
    BATTLE_CONTEXTS,
    NUMERIC_FIELDS,
    RANKING_CRITICAL_FIELDS,
    REVIEW_STATUSES,
    DomainError,
    TroopMatcher,
    derived_metrics,
    evidence_grade,
    load_aliases,
    load_troop_registry,
    read_jsonl,
    stable_id,
    validate_occurrence,
    write_csv,
    write_jsonl,
)
from .schema_validation import validate_jsonl_file


DUPLICATE_KEY_FIELDS = (
    "battle_id",
    "side",
    "parent_group",
    "row_type",
    "display_name_raw",
    "survivors",
    "kills",
    "upgrade_ready",
    "deaths",
    "wounded",
    "routed",
)


def _parse_jsonish(value: object) -> object:
    if not isinstance(value, str):
        return value
    if value == "":
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _field_value(record: Mapping[str, object], field_path: str) -> object:
    current: object = record
    for part in field_path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


def _set_field(record: dict[str, object], field_path: str, value: object) -> None:
    parts = field_path.split(".")
    current = record
    for part in parts[:-1]:
        child = current.get(part)
        if not isinstance(child, dict):
            child = {}
            current[part] = child
        current = child
    current[parts[-1]] = value


def apply_corrections(
    raw_records: list[dict[str, object]],
    corrections: Iterable[Mapping[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    records: dict[str, dict[str, object]] = {}
    for raw_record in raw_records:
        observation_id = str(raw_record.get("observation_id") or "")
        if not observation_id:
            raise DomainError("raw occurrence is missing observation_id")
        if observation_id in records:
            raise DomainError(f"duplicate raw observation_id: {observation_id}")
        records[observation_id] = copy.deepcopy(raw_record)
    resolutions: list[dict[str, object]] = []
    unresolved: list[dict[str, object]] = []
    corrected_fields: set[tuple[str, str]] = set()
    for decision in sorted(
        corrections,
        key=lambda row: (str(row.get("observation_id")), str(row.get("field_path")), str(row.get("review_id"))),
    ):
        status = str(decision.get("resolution_status"))
        if status not in REVIEW_STATUSES:
            raise DomainError(f"invalid review resolution status: {status}")
        observation_id = str(decision.get("observation_id"))
        record = records.get(observation_id)
        if record is None:
            raise DomainError(f"review decision references missing observation: {observation_id}")
        field_path = str(decision.get("field_path") or "")
        if not field_path:
            raise DomainError(f"{observation_id}: correction field_path is required")
        correction_key = (observation_id, field_path)
        if correction_key in corrected_fields:
            raise DomainError(
                f"duplicate review decision for {observation_id}:{field_path}"
            )
        corrected_fields.add(correction_key)
        actual_original = _field_value(record, field_path)
        declared_original = _parse_jsonish(decision.get("original_value"))
        if actual_original != declared_original:
            raise DomainError(
                f"{observation_id}:{field_path}: original value mismatch; "
                f"record={actual_original!r}, decision={declared_original!r}"
            )
        review_id = str(decision.get("review_id") or stable_id("review", observation_id, field_path))
        if status in {"canonical", "reviewed"}:
            _set_field(record, field_path, _parse_jsonish(decision.get("corrected_value")))
        elif status == "excluded":
            record["analysis_status"] = "excluded"
        elif status == "unresolved":
            unresolved.append(
                {
                    "review_id": review_id,
                    "observation_id": observation_id,
                    "field_path": field_path,
                    "reason": decision.get("reason") or "unresolved",
                    "ranking_critical": field_path.rsplit(".", 1)[-1] in RANKING_CRITICAL_FIELDS,
                }
            )
        record.setdefault("review_correction_ids", [])
        correction_ids = record["review_correction_ids"]
        if isinstance(correction_ids, list):
            correction_ids.append(review_id)
        resolutions.append(
            {
                "review_id": review_id,
                "observation_id": observation_id,
                "field_path": field_path,
                "resolution_status": status,
                "original_value": actual_original,
                "corrected_value": _parse_jsonish(decision.get("corrected_value")),
                "correction_source": decision.get("correction_source"),
                "reviewer": decision.get("reviewer"),
                "reviewed_at": decision.get("reviewed_at"),
                "reason": decision.get("reason"),
                "source_image_sha256": decision.get("source_image_sha256"),
            }
        )
    return list(records.values()), resolutions, unresolved


def match_troop_identities(
    records: list[dict[str, object]],
    matcher: TroopMatcher,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    reports = []
    for record in records:
        if record.get("row_type") != "troop":
            continue
        existing = record.get("canonical_troop_id")
        if existing:
            if existing not in matcher.by_id:
                reports.append(
                    {
                        "observation_id": record.get("observation_id"),
                        "display_name_raw": record.get("display_name_raw"),
                        "status": "invalid_existing_id",
                        "canonical_troop_id": existing,
                        "method": "existing",
                        "candidates": [],
                    }
                )
                record["canonical_troop_id"] = None
                record["troop_match_method"] = "invalid_existing_id"
            else:
                record["troop_match_method"] = "existing"
            continue
        result = matcher.match(str(record.get("display_name_raw") or ""))
        if result["status"] == "accepted":
            record["canonical_troop_id"] = result["troop_id"]
            record["troop_match_method"] = result["method"]
        reports.append(
            {
                "observation_id": record.get("observation_id"),
                "display_name_raw": record.get("display_name_raw"),
                "status": result["status"],
                "canonical_troop_id": result.get("troop_id"),
                "method": result["method"],
                "candidates": result.get("candidates", []),
            }
        )
    return records, reports


def _duplicate_key(record: Mapping[str, object]) -> tuple[object, ...]:
    return tuple(record.get(field) for field in DUPLICATE_KEY_FIELDS)


def deduplicate_occurrences(
    records: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    groups: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for record in records:
        groups[_duplicate_key(record)].append(record)
    retained: list[dict[str, object]] = []
    report: list[dict[str, object]] = []
    for key in sorted(groups, key=lambda value: tuple("" if item is None else str(item) for item in value)):
        group = sorted(groups[key], key=lambda record: str(record.get("observation_id")))
        if len(group) == 1:
            retained.extend(group)
            continue
        overlap_groups = {str(record.get("overlap_group_id") or "") for record in group}
        screenshot_groups = {str(record.get("screenshot_group_id") or "") for record in group}
        proven = (
            len(overlap_groups) == 1
            and "" not in overlap_groups
            and len(screenshot_groups) == 1
            and "" not in screenshot_groups
        )
        kept = group[0]
        retained.append(kept)
        report.append(
            {
                "duplicate_group_id": stable_id("duplicate", key),
                "observation_ids": [record.get("observation_id") for record in group],
                "kept_observation_id": kept.get("observation_id") if proven else "",
                "status": "deduplicated_proven_overlap" if proven else "candidate_preserved",
                "reason": (
                    "same visible row within one explicit overlap/screenshot group"
                    if proven
                    else "same-valued occurrences lack sufficient overlap identity evidence"
                ),
            }
        )
        if not proven:
            retained.extend(group[1:])
    return sorted(retained, key=lambda record: str(record.get("observation_id"))), report


def _ranking_usable(record: Mapping[str, object], unresolved_ids: set[str]) -> bool:
    if record.get("row_type") != "troop":
        return False
    if record.get("analysis_status") in {"excluded", "unresolved", "non_ranking"}:
        return False
    if str(record.get("observation_id")) in unresolved_ids:
        return False
    if not record.get("canonical_troop_id"):
        return False
    if record.get("battle_context") not in {"field", "siege_attack", "siege_defense"}:
        return False
    try:
        metrics = derived_metrics(record)
    except DomainError:
        return False
    return all(metrics[field] is not None for field in ("survivors", "kills", "deaths", "wounded"))


def consolidate_occurrences(records: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str], list[Mapping[str, object]]] = defaultdict(list)
    for record in records:
        groups[
            (
                str(record["battle_id"]),
                str(record["canonical_troop_id"]),
                str(record["battle_context"]),
            )
        ].append(record)
    result = []
    for (battle_id, troop_id, context), group in sorted(groups.items()):
        totals = {field: sum(int(record.get(field) or 0) for record in group) for field in NUMERIC_FIELDS}
        sources = [
            record.get("source")
            for record in group
            if isinstance(record.get("source"), Mapping)
        ]
        games = [
            record.get("game")
            for record in group
            if isinstance(record.get("game"), Mapping)
        ]
        provenances = [
            record.get("provenance")
            for record in group
            if isinstance(record.get("provenance"), Mapping)
        ]
        base = {
            "schema_version": "2.0.0",
            "consolidated_id": stable_id("battle_troop", battle_id, troop_id, context),
            "battle_id": battle_id,
            "canonical_troop_id": troop_id,
            "battle_context": context,
            "observation_ids": sorted(str(record["observation_id"]) for record in group),
            "source_filenames": sorted(
                {
                    str(source["image_file"])
                    for source in sources
                    if source.get("image_file")
                }
            ),
            "source_image_sha256s": sorted(
                {
                    str(source["image_sha256"])
                    for source in sources
                    if source.get("image_sha256")
                }
            ),
            "review_correction_ids": sorted(
                {
                    str(review_id)
                    for record in group
                    for review_id in (
                        record.get("review_correction_ids")
                        if isinstance(record.get("review_correction_ids"), list)
                        else []
                    )
                }
            ),
            "game_versions": sorted(
                {str(game["version"]) for game in games if game.get("version")}
            ),
            "game_tracks": sorted(
                {str(game["track"]) for game in games if game.get("track")}
            ),
            "active_modules": sorted(
                {
                    str(module)
                    for game in games
                    for module in (
                        game.get("active_modules")
                        if isinstance(game.get("active_modules"), list)
                        else []
                    )
                }
            ),
            "pipeline_versions": sorted(
                {
                    str(provenance["pipeline_version"])
                    for provenance in provenances
                    if provenance.get("pipeline_version")
                }
            ),
            "code_commit_shas": sorted(
                {
                    str(provenance["code_commit_sha"])
                    for provenance in provenances
                    if provenance.get("code_commit_sha")
                }
            ),
            **totals,
        }
        result.append({**base, **derived_metrics(base)})
    return result


def historical_aggregates(consolidated: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    rows = list(consolidated)
    for row in rows:
        grouped[(str(row["canonical_troop_id"]), str(row["battle_context"]))].append(row)
        grouped[(str(row["canonical_troop_id"]), "overall")].append(row)
    result = []
    for (troop_id, context), group in sorted(grouped.items()):
        total_deployed = sum(int(row["deployed"]) for row in group)
        total_kills = sum(int(row["kills"]) for row in group)
        total_survivors = sum(int(row["survivors"]) for row in group)
        total_deaths = sum(int(row["deaths"]) for row in group)
        total_wounded = sum(int(row["wounded"]) for row in group)
        total_routed = sum(int(row["routed"]) for row in group)
        rows_with_rates = sorted(
            (
                (Decimal(str(row["kills_per_deployed"])), str(row["battle_id"]))
                for row in group
                if row["kills_per_deployed"] is not None
            ),
            key=lambda item: (item[0], item[1]),
        )
        battle_rates = [rate for rate, _ in rows_with_rates]
        mean_rate = (
            sum(battle_rates, Decimal(0)) / Decimal(len(battle_rates))
            if battle_rates
            else None
        )
        variation = (
            (
                sum((rate - mean_rate) ** 2 for rate in battle_rates)
                / Decimal(len(battle_rates))
            ).sqrt()
            if mean_rate is not None
            else None
        )
        context_distribution = dict(
            sorted(Counter(str(row["battle_context"]) for row in group).items())
        )
        aggregate = {
            "schema_version": "2.0.0",
            "aggregate_id": stable_id("aggregate", troop_id, context),
            "canonical_troop_id": troop_id,
            "battle_context": context,
            "mixed_contexts": context == "overall",
            "battle_count": len({str(row["battle_id"]) for row in group}),
            "consolidated_ids": sorted(str(row["consolidated_id"]) for row in group),
            "battle_ids": sorted({str(row["battle_id"]) for row in group}),
            "observation_ids": sorted(
                {
                    str(observation_id)
                    for row in group
                    for observation_id in row["observation_ids"]
                }
            ),
            "source_filenames": sorted(
                {
                    str(filename)
                    for row in group
                    for filename in row["source_filenames"]
                }
            ),
            "source_image_sha256s": sorted(
                {
                    str(digest)
                    for row in group
                    for digest in row["source_image_sha256s"]
                }
            ),
            "review_correction_ids": sorted(
                {
                    str(review_id)
                    for row in group
                    for review_id in row["review_correction_ids"]
                }
            ),
            "game_versions": sorted(
                {
                    str(version)
                    for row in group
                    for version in row["game_versions"]
                }
            ),
            "game_tracks": sorted(
                {
                    str(track)
                    for row in group
                    for track in row["game_tracks"]
                }
            ),
            "active_modules": sorted(
                {
                    str(module)
                    for row in group
                    for module in row["active_modules"]
                }
            ),
            "pipeline_versions": sorted(
                {
                    str(version)
                    for row in group
                    for version in row["pipeline_versions"]
                }
            ),
            "code_commit_shas": sorted(
                {
                    str(commit)
                    for row in group
                    for commit in row["code_commit_shas"]
                }
            ),
            "total_deployed": total_deployed,
            "total_kills": total_kills,
            "total_survivors": total_survivors,
            "total_deaths": total_deaths,
            "total_wounded": total_wounded,
            "total_routed": total_routed,
            "historical_kills_per_deployed": f"{total_kills / total_deployed:.6f}" if total_deployed else None,
            "survival_rate": f"{total_survivors / total_deployed:.6f}" if total_deployed else None,
            "death_rate": f"{total_deaths / total_deployed:.6f}" if total_deployed else None,
            "wounded_rate": f"{total_wounded / total_deployed:.6f}" if total_deployed else None,
            "casualty_rate": f"{(total_deaths + total_wounded) / total_deployed:.6f}" if total_deployed else None,
            "routed_rate": f"{total_routed / total_deployed:.6f}" if total_deployed else None,
            "median_battle_kills_per_deployed": f"{statistics.median(battle_rates):.6f}" if battle_rates else None,
            "best_battle_kills_per_deployed": f"{rows_with_rates[-1][0]:.6f}" if rows_with_rates else None,
            "worst_battle_kills_per_deployed": f"{rows_with_rates[0][0]:.6f}" if rows_with_rates else None,
            "best_battle_id": rows_with_rates[-1][1] if rows_with_rates else None,
            "worst_battle_id": rows_with_rates[0][1] if rows_with_rates else None,
            "variation_by_battle": f"{variation:.6f}" if variation is not None else None,
            "context_distribution": context_distribution,
        }
        aggregate["evidence_grade"] = evidence_grade(total_deployed, int(aggregate["battle_count"]))
        result.append(aggregate)
    return result


def build_rankings(aggregates: list[dict[str, object]], output_dir: Path) -> list[Path]:
    fields = (
        "rank",
        "canonical_troop_id",
        "battle_context",
        "mixed_contexts",
        "evidence_grade",
        "battle_count",
        "total_deployed",
        "total_kills",
        "historical_kills_per_deployed",
        "survival_rate",
        "death_rate",
        "wounded_rate",
        "casualty_rate",
        "routed_rate",
        "median_battle_kills_per_deployed",
        "best_battle_kills_per_deployed",
        "worst_battle_kills_per_deployed",
        "best_battle_id",
        "worst_battle_id",
        "variation_by_battle",
        "context_distribution",
    )
    written = []
    for context in ("field", "siege_attack", "siege_defense", "overall"):
        context_rows = [row.copy() for row in aggregates if row["battle_context"] == context]
        context_rows.sort(
            key=lambda row: (
                -float(row["historical_kills_per_deployed"] or 0),
                -int(row["total_deployed"]),
                str(row["canonical_troop_id"]),
            )
        )
        for rank, row in enumerate(context_rows, 1):
            row["rank"] = rank
        complete = output_dir / f"ranking_{context}_complete.csv"
        reliable = output_dir / f"ranking_{context}_reliable.csv"
        write_csv(complete, context_rows, fields)
        write_csv(reliable, [row for row in context_rows if row["evidence_grade"] in {"medium", "high"}], fields)
        written.extend([complete, reliable])
    return written


def hierarchy_validation(records: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    by_battle_side: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for record in records:
        by_battle_side[(str(record.get("battle_id")), str(record.get("side")))].append(record)
    result = []
    for (battle_id, side), group in sorted(by_battle_side.items()):
        totals = [record for record in group if record.get("row_type") == "side_total"]
        troops = [record for record in group if record.get("row_type") == "troop"]
        for field in ("survivors", "kills", "deaths", "wounded", "routed"):
            troop_values = [record.get(field) for record in troops if record.get(field) is not None]
            invalid_numeric = False
            try:
                visible_sum = sum(int(value) for value in troop_values)
            except (TypeError, ValueError):
                visible_sum = 0
                invalid_numeric = True
            total_value = totals[0].get(field) if len(totals) == 1 else None
            if invalid_numeric:
                status = "invalid"
                difference = None
                explanation = "at least one visible troop value is not numeric"
            elif total_value is None:
                status = "partial" if troop_values else "not_applicable"
                difference = None
                explanation = "side total unavailable; visible troop rows retained as partial evidence"
            else:
                try:
                    difference = int(total_value) - visible_sum
                    status = "consistent" if difference == 0 else "inconsistent"
                    explanation = "visible troop sum matches side total" if difference == 0 else "difference may reflect hidden/hero rows or extraction error"
                except (TypeError, ValueError):
                    status = "invalid"
                    difference = None
                    explanation = "side total is not numeric"
            result.append(
                {
                    "battle_id": battle_id,
                    "side": side,
                    "field": field,
                    "aggregation_status": status,
                    "aggregation_difference": difference,
                    "aggregation_explanation": explanation,
                }
            )
    return result


def outlier_report(records: Iterable[Mapping[str, object]]) -> list[dict[str, object]]:
    usable = [record for record in records if record.get("row_type") == "troop"]
    rates = [
        float(metrics["kills_per_deployed"])
        for record in usable
        if (metrics := derived_metrics(record))["kills_per_deployed"] is not None
    ]
    median = statistics.median(rates) if rates else 0.0
    deviations = [abs(rate - median) for rate in rates]
    mad = statistics.median(deviations) if deviations else 0.0
    result = []
    for record in usable:
        try:
            metrics = derived_metrics(record)
        except DomainError:
            continue
        rate = float(metrics["kills_per_deployed"]) if metrics["kills_per_deployed"] is not None else None
        robust_z = 0.6745 * (rate - median) / mad if rate is not None and mad else None
        explicit = bool(record.get("suspected_siege_engine_outlier"))
        review_only = bool(
            record.get("battle_context") == "siege_defense"
            and metrics["deployed"] is not None
            and metrics["deployed"] <= 5
            and robust_z is not None
            and robust_z >= 5
        )
        if explicit or review_only:
            result.append(
                {
                    "observation_id": record.get("observation_id"),
                    "canonical_troop_id": record.get("canonical_troop_id"),
                    "battle_id": record.get("battle_id"),
                    "battle_context": record.get("battle_context"),
                    "deployed": metrics["deployed"],
                    "kills": metrics["kills"],
                    "kills_per_deployed": metrics["kills_per_deployed"],
                    "robust_z": f"{robust_z:.6f}" if robust_z is not None else None,
                    "status": "explicit_occurrence_exclusion" if explicit else "review_only",
                    "primary_excluded": explicit,
                }
            )
    return result


def build_canonical_dataset(
    raw_occurrences_path: Path,
    output_dir: Path,
    troop_registry_path: Path,
    *,
    corrections_path: Path | None = None,
    aliases_path: Path | None = None,
    schemas_dir: Path | None = None,
    fuzzy_threshold: float = 0.94,
    fuzzy_margin: float = 0.05,
) -> dict[str, object]:
    raw_hash_before = sha256_file(raw_occurrences_path)
    raw_records = read_jsonl(raw_occurrences_path)
    corrections = read_jsonl(corrections_path) if corrections_path and corrections_path.exists() else []
    if schemas_dir is None:
        schemas_dir = Path(__file__).resolve().parents[2] / "data/combat_observations/schemas/v2"
    if corrections_path and corrections:
        correction_schema_errors = validate_jsonl_file(
            corrections_path,
            schemas_dir / "review-correction.schema.json",
        )
        if correction_schema_errors:
            raise DomainError(
                f"review corrections failed schema validation: {correction_schema_errors}"
            )
    reviewed, resolutions, unresolved = apply_corrections(raw_records, corrections)
    matcher = TroopMatcher(
        load_troop_registry(troop_registry_path),
        load_aliases(aliases_path),
        fuzzy_threshold=fuzzy_threshold,
        fuzzy_margin=fuzzy_margin,
    )
    reviewed, identity_report = match_troop_identities(reviewed, matcher)
    reviewed, duplicate_report = deduplicate_occurrences(reviewed)
    try:
        code_commit_sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=Path(__file__).resolve().parents[2],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        code_commit_sha = "unknown"

    unresolved_critical = {
        str(row["observation_id"])
        for row in unresolved
        if bool(row["ranking_critical"])
    }
    validation_errors = [error for record in reviewed for error in validate_occurrence(record)]
    contexts_by_battle: dict[str, set[str]] = defaultdict(set)
    for record in reviewed:
        contexts_by_battle[str(record.get("battle_id") or "")].add(
            str(record.get("battle_context") or "")
        )
    conflicting_battles = {
        battle_id: sorted(contexts)
        for battle_id, contexts in contexts_by_battle.items()
        if len(contexts) > 1
    }
    for record in reviewed:
        battle_id = str(record.get("battle_id") or "")
        if battle_id in conflicting_battles:
            validation_errors.append(
                {
                    "record_id": str(record.get("observation_id") or "unknown"),
                    "field": "battle_context",
                    "error": (
                        "inconsistent_battle_context:"
                        + ",".join(conflicting_battles[battle_id])
                    ),
                }
            )
    invalid_ids = {str(error["record_id"]) for error in validation_errors}
    canonical_occurrences: list[dict[str, object]] = []
    quarantine: list[dict[str, object]] = []
    for record in reviewed:
        record = copy.deepcopy(record)
        observation_id = str(record.get("observation_id"))
        provenance = record.get("provenance")
        if not isinstance(provenance, dict):
            provenance = {}
            record["provenance"] = provenance
        provenance.setdefault("pipeline_version", PIPELINE_VERSION)
        provenance.setdefault("code_commit_sha", code_commit_sha)
        try:
            metrics = derived_metrics(record)
        except DomainError:
            metrics = {
                "deployed": None,
                "casualties": None,
                "kills_per_deployed": None,
                "survival_rate": None,
                "death_rate": None,
                "wounded_rate": None,
                "casualty_rate": None,
                "routed_rate": None,
            }
        for key, value in metrics.items():
            record[key] = value
        record["schema_version"] = "2.0.0"
        if _ranking_usable(record, unresolved_critical) and observation_id not in invalid_ids:
            record["analysis_status"] = "canonical"
        elif record.get("row_type") in {"hero", "player", "party", "side_total", "artifact"}:
            record["analysis_status"] = "non_ranking"
        elif record.get("analysis_status") != "excluded":
            record["analysis_status"] = "unresolved"
            quarantine.append(
                {
                    "observation_id": observation_id,
                    "reason": "ranking-critical uncertainty, invalid canonical identity, or semantic validation failure",
                }
            )
        canonical_occurrences.append(record)

    primary = [record for record in canonical_occurrences if record.get("analysis_status") == "canonical"]
    explicit_outliers = {str(row["observation_id"]) for row in primary if row.get("suspected_siege_engine_outlier")}
    primary_without_outliers = [record for record in primary if str(record["observation_id"]) not in explicit_outliers]
    consolidated = consolidate_occurrences(primary_without_outliers)
    aggregates = historical_aggregates(consolidated)

    screenshots_by_hash: dict[str, dict[str, object]] = {}
    battles: dict[str, dict[str, object]] = {}
    for record in canonical_occurrences:
        source = record.get("source") if isinstance(record.get("source"), dict) else {}
        image_hash = str(source.get("image_sha256") or "")
        if image_hash:
            screenshot = screenshots_by_hash.setdefault(
                image_hash,
                {
                    "schema_version": "2.0.0",
                    "screenshot_id": stable_id("screenshot", image_hash),
                    "source_filename": source.get("image_file"),
                    "source_sha256": image_hash,
                    "analysis_status": "canonical_source",
                    "observation_ids": [],
                    "game_versions": [],
                    "game_tracks": [],
                    "code_commit_shas": [],
                },
            )
            screenshot["observation_ids"] = sorted(
                {
                    *screenshot["observation_ids"],
                    str(record.get("observation_id")),
                }
            )
            game = record.get("game") if isinstance(record.get("game"), dict) else {}
            provenance = (
                record.get("provenance")
                if isinstance(record.get("provenance"), dict)
                else {}
            )
            for target, value in (
                ("game_versions", game.get("version")),
                ("game_tracks", game.get("track")),
                ("code_commit_shas", provenance.get("code_commit_sha")),
            ):
                if value:
                    screenshot[target] = sorted({*screenshot[target], str(value)})
        battle_id = str(record.get("battle_id"))
        battle = battles.setdefault(
            battle_id,
            {
                "schema_version": "2.0.0",
                "battle_id": battle_id,
                "battle_context": record.get("battle_context"),
                "classification_source": record.get("classification_source", "raw_extraction"),
                "source_image_sha256s": [],
                "observation_ids": [],
                "review_correction_ids": [],
                "game_versions": [],
                "game_tracks": [],
                "code_commit_shas": [],
            },
        )
        if image_hash and image_hash not in battle["source_image_sha256s"]:
            battle["source_image_sha256s"].append(image_hash)
        battle["observation_ids"].append(str(record.get("observation_id")))
        if isinstance(record.get("review_correction_ids"), list):
            battle["review_correction_ids"].extend(record["review_correction_ids"])
        game = record.get("game") if isinstance(record.get("game"), dict) else {}
        provenance = (
            record.get("provenance")
            if isinstance(record.get("provenance"), dict)
            else {}
        )
        for target, value in (
            ("game_versions", game.get("version")),
            ("game_tracks", game.get("track")),
            ("code_commit_shas", provenance.get("code_commit_sha")),
        ):
            if value:
                battle[target].append(str(value))
    for battle in battles.values():
        for field in (
            "source_image_sha256s",
            "observation_ids",
            "review_correction_ids",
            "game_versions",
            "game_tracks",
            "code_commit_shas",
        ):
            battle[field] = sorted(set(battle[field]))

    canonical_dir = output_dir / "canonical"
    reports_dir = output_dir / "reports"
    reviewed_dir = output_dir / "reviewed"
    write_jsonl(canonical_dir / "canonical_screenshots.jsonl", sorted(screenshots_by_hash.values(), key=lambda row: str(row["screenshot_id"])))
    write_jsonl(canonical_dir / "canonical_battles.jsonl", sorted(battles.values(), key=lambda row: str(row["battle_id"])))
    write_jsonl(canonical_dir / "canonical_occurrences.jsonl", canonical_occurrences)
    write_jsonl(canonical_dir / "canonical_troop_battle_consolidated.jsonl", consolidated)
    write_jsonl(canonical_dir / "canonical_historical_aggregates.jsonl", aggregates)
    write_jsonl(reviewed_dir / "review_corrections.jsonl", corrections)

    resolution_fields = (
        "review_id", "observation_id", "field_path", "resolution_status", "original_value",
        "corrected_value", "correction_source", "reviewer", "reviewed_at", "reason", "source_image_sha256",
    )
    write_csv(reports_dir / "review_resolutions.csv", resolutions, resolution_fields)
    write_csv(reports_dir / "unresolved_rows.csv", [*unresolved, *quarantine], ("review_id", "observation_id", "field_path", "reason", "ranking_critical"))
    write_csv(
        reports_dir / "duplicate_report.csv",
        duplicate_report,
        ("duplicate_group_id", "observation_ids", "kept_observation_id", "status", "reason"),
    )
    write_csv(
        reports_dir / "grouping_validation.csv",
        [
            {
                "duplicate_group_id": row["duplicate_group_id"],
                "observation_ids": row["observation_ids"],
                "grouping_status": (
                    "validated_overlap"
                    if row["status"] == "deduplicated_proven_overlap"
                    else "requires_review"
                ),
                "grouping_explanation": row["reason"],
            }
            for row in duplicate_report
        ],
        (
            "duplicate_group_id",
            "observation_ids",
            "grouping_status",
            "grouping_explanation",
        ),
    )
    write_csv(
        reports_dir / "troop_identity_review.csv",
        identity_report,
        ("observation_id", "display_name_raw", "status", "canonical_troop_id", "method", "candidates"),
    )
    unmatched = [row for row in identity_report if row["status"] == "unmatched"]
    ambiguous = [row for row in identity_report if row["status"] in {"ambiguous", "invalid_existing_id"}]
    write_csv(reports_dir / "unmatched_troops.csv", unmatched, ("observation_id", "display_name_raw", "status", "candidates"))
    write_csv(reports_dir / "ambiguous_troop_matches.csv", ambiguous, ("observation_id", "display_name_raw", "status", "canonical_troop_id", "candidates"))

    hierarchy = hierarchy_validation(canonical_occurrences)
    write_csv(
        reports_dir / "aggregation_validation.csv",
        hierarchy,
        ("battle_id", "side", "field", "aggregation_status", "aggregation_difference", "aggregation_explanation"),
    )
    outliers = outlier_report(canonical_occurrences)
    write_csv(
        reports_dir / "outlier_report.csv",
        outliers,
        ("observation_id", "canonical_troop_id", "battle_id", "battle_context", "deployed", "kills", "kills_per_deployed", "robust_z", "status", "primary_excluded"),
    )
    write_csv(
        reports_dir / "siege_engine_assisted_occurrences.csv",
        [row for row in outliers if row["primary_excluded"]],
        ("observation_id", "canonical_troop_id", "battle_id", "battle_context", "deployed", "kills", "kills_per_deployed", "status"),
    )
    context_rows = [
        {
            "battle_id": battle["battle_id"],
            "original_context": battle["battle_context"],
            "canonical_context": battle["battle_context"],
            "classification_source": battle["classification_source"],
            "review_status": "unresolved" if battle["battle_context"] == "undefined" else "retained",
            "review_reason": "insufficient stored evidence" if battle["battle_context"] == "undefined" else "no conflicting correction",
        }
        for battle in sorted(battles.values(), key=lambda row: str(row["battle_id"]))
    ]
    write_csv(
        reports_dir / "battle_context_review.csv",
        context_rows,
        ("battle_id", "original_context", "canonical_context", "classification_source", "review_status", "review_reason"),
    )
    ranking_paths = build_rankings(aggregates, canonical_dir)
    schema_pairs = (
        ("canonical_screenshots.jsonl", "screenshot.schema.json"),
        ("canonical_battles.jsonl", "battle.schema.json"),
        ("canonical_occurrences.jsonl", "troop-occurrence.schema.json"),
        ("canonical_troop_battle_consolidated.jsonl", "battle-troop-consolidation.schema.json"),
        ("canonical_historical_aggregates.jsonl", "historical-aggregate.schema.json"),
    )
    schema_errors = [
        error
        for data_name, schema_name in schema_pairs
        for error in validate_jsonl_file(canonical_dir / data_name, schemas_dir / schema_name)
    ]
    validation = {
        "schema_version": "2.0.0",
        "status": (
            "failed"
            if schema_errors
            else "passed" if not validation_errors and not quarantine else "passed_with_warnings"
        ),
        "raw_occurrences_sha256": raw_hash_before,
        "raw_input_unchanged": sha256_file(raw_occurrences_path) == raw_hash_before,
        "counts": {
            "raw_occurrences": len(raw_records),
            "canonical_occurrences": len(canonical_occurrences),
            "primary_occurrences": len(primary_without_outliers),
            "quarantined_occurrences": len(quarantine),
            "unresolved_decisions": len(unresolved),
            "consolidated_rows": len(consolidated),
            "historical_aggregates": len(aggregates),
            "explicit_outlier_occurrences": len(explicit_outliers),
        },
        "semantic_errors": validation_errors,
        "schema_errors": schema_errors,
        "generated_rankings": [path.name for path in ranking_paths],
    }
    atomic_write_json(reports_dir / "canonical_validation_report.json", validation)
    return validation
