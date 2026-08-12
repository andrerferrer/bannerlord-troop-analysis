#!/usr/bin/env python3
"""Join compatible normalized context batches without mutating their evidence."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import random
import re
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

try:
    from scripts.analysis import analyze_normalized_combat_batch as base
    from scripts.combat_observations.bundle import safe_extract_tar
except ModuleNotFoundError:  # Direct execution sets sys.path to scripts/analysis.
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.analysis import analyze_normalized_combat_batch as base
    from scripts.combat_observations.bundle import safe_extract_tar


COMMON_FIELD_PROJECTION = (
    "battle_id",
    "battle_context",
    "display_name_normalized",
    "display_names_raw",
    *base.COUNT_FIELDS,
    "needs_review",
)

COMPARISON_FIELDS = (
    "cohort",
    "source_batch_ids",
    "independent_battles",
    *base.COUNT_FIELDS,
    "kills_per_deployed",
    "death_rate",
    "casualty_rate",
    "ci95_low",
    "ci95_high",
    "reliability_status",
)

FOCUS_BATTLE_FIELDS = (
    "cohort",
    "source_batch_id",
    "battle_id",
    "deployed",
    "kills",
    "deaths",
    "wounded",
    "kills_per_deployed",
    "casualty_rate",
)


@dataclass(frozen=True)
class SourceSpec:
    batch_id: str
    cohort: str
    batch_path: str
    normalization_commit: str
    archive_name: str
    expected_archive_sha256: str
    manifest_path: str
    manifest_base_path: str
    summary_path: str
    validation_path: str
    battles_path: str
    consolidated_path: str
    schema_version: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> SourceSpec:
        fields = {field.name for field in cls.__dataclass_fields__.values()}
        missing = sorted(fields - value.keys())
        if missing:
            raise ValueError(f"compatible source is missing: {', '.join(missing)}")
        source = cls(**{field: str(value[field]) for field in fields})
        source.validate()
        return source

    def validate(self) -> None:
        identifier = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
        for label, value in (
            ("batch_id", self.batch_id),
            ("archive_name", self.archive_name),
        ):
            if not identifier.fullmatch(value):
                raise ValueError(f"invalid compatible source {label}: {value}")
        if not re.fullmatch(r"[0-9a-f]{40}", self.normalization_commit):
            raise ValueError(
                f"invalid normalization commit: {self.normalization_commit}"
            )
        if not re.fullmatch(r"[0-9a-f]{64}", self.expected_archive_sha256):
            raise ValueError(f"invalid normalized archive SHA-256: {self.batch_id}")
        if self.schema_version not in base.SUPPORTED_NORMALIZED_SCHEMA_VERSIONS:
            raise ValueError(f"unsupported normalized schema: {self.schema_version}")


@dataclass
class LoadedSource:
    spec: SourceSpec
    summary: dict[str, Any]
    field_battles: list[dict[str, Any]]
    field_rows: list[dict[str, Any]]
    verification: dict[str, Any]


@dataclass
class CombinedAnalysis:
    sources: list[LoadedSource]
    identities: list[dict[str, str]]
    rankings: list[dict[str, Any]]
    reliable: list[dict[str, Any]]
    insufficient: list[dict[str, Any]]
    comparisons: list[dict[str, Any]]
    delta: dict[str, Any]
    coverage: dict[str, Any]


def safe_relative_path(value: str, label: str) -> Path:
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts or pure.as_posix() in {"", "."}:
        if pure.as_posix() == "." and label == "manifest_base_path":
            return Path(".")
        raise ValueError(f"unsafe {label}: {value}")
    return Path(*pure.parts)


def path_below(root: Path, relative: str, label: str) -> Path:
    candidate = (root / safe_relative_path(relative, label)).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(f"{label} escapes its root: {relative}") from error
    return candidate


def safe_output_stem(value: str, label: str = "output stem") -> str:
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", value):
        raise ValueError(f"invalid {label}: {value}")
    return value


def contextual_output_name(stem: str, context: str, suffix: str) -> str:
    """Keep legacy field names while isolating additional context outputs."""
    safe_context = safe_output_stem(context, "context")
    return f"{stem}{'' if safe_context == 'field' else '_' + safe_context}{suffix}"


def decode_ordered_archive(parts: list[Path], destination: Path) -> None:
    if not parts:
        raise ValueError(f"normalized archive parts are missing for {destination.name}")
    encoded = b"".join(part.read_bytes() for part in parts)
    try:
        decoded = base64.b64decode(b"".join(encoded.split()), validate=True)
    except ValueError as error:
        raise ValueError(
            f"invalid Base64 archive parts for {destination.name}"
        ) from error
    destination.write_bytes(decoded)


def verify_manifest(manifest_path: Path, manifest_base: Path) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    for row in base.read_csv(manifest_path):
        relative = row.get("file", "")
        artifact = path_below(manifest_base, relative, "manifest artifact")
        if not artifact.is_file() or artifact.is_symlink():
            raise ValueError(f"manifest artifact is missing or unsafe: {relative}")
        actual_hash = base.sha256_file(artifact)
        actual_size = artifact.stat().st_size
        expected_hash = row.get("sha256", "")
        try:
            expected_size = int(row.get("size_bytes", ""))
        except ValueError as error:
            raise ValueError(f"invalid manifest size for {relative}") from error
        if actual_hash != expected_hash or actual_size != expected_size:
            raise ValueError(f"manifest mismatch: {relative}")
        checks.append(
            {
                "file": relative,
                "sha256": actual_hash,
                "size_bytes": actual_size,
                "passed": True,
            }
        )
    if not checks:
        raise ValueError(f"artifact manifest is empty: {manifest_path}")
    return checks


def validate_summary(
    summary: dict[str, Any], spec: SourceSpec, track: str, game_version: str
) -> None:
    expected = {
        "batch_id": spec.batch_id,
        "schema_version": spec.schema_version,
        "game_track": track,
        "game_version": game_version,
    }
    for field, expected_value in expected.items():
        if str(summary.get(field, "")) != expected_value:
            raise ValueError(
                f"{spec.batch_id}: {field} mismatch: "
                f"{summary.get(field)!r} != {expected_value!r}"
            )


def validate_normalization_report(
    report: dict[str, Any], spec: SourceSpec
) -> dict[str, Any]:
    if report.get("status") not in {"pass", "passed"}:
        raise ValueError(f"{spec.batch_id}: normalization validation did not pass")
    if str(report.get("schema_version", "")) != spec.schema_version:
        raise ValueError(f"{spec.batch_id}: validation schema version mismatch")
    error_lists: list[list[Any]] = []
    for field in ("validation_errors", "errors"):
        values = report.get(field, [])
        if not isinstance(values, list):
            raise TypeError(f"{spec.batch_id}: invalid normalization {field}")
        error_lists.append(values)
    errors = [error for values in error_lists for error in values]
    if errors:
        raise ValueError(f"{spec.batch_id}: normalization validation has errors")
    expected_flags = {
        "sides_pooled": (("sides_pooled",), False),
        "offscreen_rows_inferred": (("offscreen_rows_inferred",), False),
        "heroes_in_primary": (("heroes_in_primary",), False),
        "context_boundaries_preserved": (
            ("context_boundaries_preserved", "contexts_pooled"),
            True,
        ),
    }
    evidence: dict[str, Any] = {}
    unverified: list[str] = []
    for boundary, (source_fields, expected) in expected_flags.items():
        reported_fields = [field for field in source_fields if field in report]
        if not reported_fields:
            evidence[boundary] = {"status": "not_reported"}
            unverified.append(boundary)
            continue
        reported_evidence = []
        for source_field in reported_fields:
            actual = report[source_field]
            effective_expected = (
                False if source_field == "contexts_pooled" else expected
            )
            if actual is not effective_expected:
                raise ValueError(
                    f"{spec.batch_id}: normalization boundary violated: {source_field}"
                )
            reported_evidence.append(
                {
                    "source_field": source_field,
                    "reported_value": actual,
                    "expected_reported_value": effective_expected,
                }
            )
        if len(reported_evidence) == 1:
            evidence[boundary] = {
                "status": "verified",
                **reported_evidence[0],
                "canonical_value": expected,
            }
        else:
            evidence[boundary] = {
                "status": "verified",
                "reported_fields": reported_evidence,
                "canonical_value": expected,
            }
    return {"flags": evidence, "unverified_flags": unverified}


def validate_field_projection(
    spec: SourceSpec,
    battles: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    track: str,
    game_version: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    field_battles = [row for row in battles if row.get("battle_context") == "field"]
    if not field_battles:
        raise ValueError(f"{spec.batch_id}: no field battles")
    field_ids = {str(row.get("battle_id", "")) for row in field_battles}
    if "" in field_ids or len(field_ids) != len(field_battles):
        raise ValueError(f"{spec.batch_id}: field battle IDs are blank or duplicated")
    for battle in field_battles:
        if (
            battle.get("game_track") != track
            or battle.get("game_version") != game_version
        ):
            raise ValueError(f"{spec.batch_id}: field track/version boundary mismatch")
        if battle.get("player_side") not in {"attacker", "defender"}:
            raise ValueError(f"{spec.batch_id}: unresolved player side")

    field_rows = [row for row in rows if row.get("battle_context") == "field"]
    row_keys: set[tuple[str, str]] = set()
    for row in field_rows:
        missing = [field for field in COMMON_FIELD_PROJECTION if field not in row]
        if missing:
            raise ValueError(f"{spec.batch_id}: projection fields missing: {missing}")
        battle_id = str(row["battle_id"])
        slug = str(row["display_name_normalized"])
        key = (battle_id, slug)
        if battle_id not in field_ids or not slug or key in row_keys:
            raise ValueError(f"{spec.batch_id}: invalid field row key: {key}")
        row_keys.add(key)
        if row["needs_review"]:
            raise ValueError(
                f"{spec.batch_id}: review-needed row entered projection: {key}"
            )
        if row.get("game_track", track) != track:
            raise ValueError(f"{spec.batch_id}: row track boundary mismatch: {key}")
        counts = [row.get(field) for field in base.COUNT_FIELDS]
        if not all(isinstance(value, int) and value >= 0 for value in counts):
            raise ValueError(f"{spec.batch_id}: invalid counts: {key}")
        if row["deployed"] <= 0:
            raise ValueError(f"{spec.batch_id}: non-positive deployed count: {key}")
        accounted = sum(
            row[field] for field in ("survivors", "deaths", "wounded", "routed")
        )
        if accounted != row["deployed"]:
            raise ValueError(f"{spec.batch_id}: casualty arithmetic mismatch: {key}")
    return field_battles, field_rows


def validate_context_projection(
    spec: SourceSpec,
    battles: list[dict[str, Any]],
    rows: list[dict[str, Any]],
    track: str,
    game_version: str,
    context: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Validate one configured context; keep the field wrapper for compatibility."""
    if context == "field":
        return validate_field_projection(spec, battles, rows, track, game_version)
    if context not in base.CONTEXTS:
        raise ValueError(f"unsupported battle context: {context}")

    context_battles = [row for row in battles if row.get("battle_context") == context]
    if not context_battles:
        raise ValueError(f"{spec.batch_id}: no {context} battles")
    battle_ids = {str(row.get("battle_id", "")) for row in context_battles}
    if "" in battle_ids or len(battle_ids) != len(context_battles):
        raise ValueError(
            f"{spec.batch_id}: {context} battle IDs are blank or duplicated"
        )
    for battle in context_battles:
        if (
            battle.get("game_track") != track
            or battle.get("game_version") != game_version
        ):
            raise ValueError(
                f"{spec.batch_id}: {context} track/version boundary mismatch"
            )
        if battle.get("player_side") not in {"attacker", "defender"}:
            raise ValueError(f"{spec.batch_id}: unresolved player side")

    context_rows = [row for row in rows if row.get("battle_context") == context]
    row_keys: set[tuple[str, str]] = set()
    for row in context_rows:
        missing = [field for field in COMMON_FIELD_PROJECTION if field not in row]
        if missing:
            raise ValueError(f"{spec.batch_id}: projection fields missing: {missing}")
        battle_id = str(row["battle_id"])
        slug = str(row["display_name_normalized"])
        key = (battle_id, slug)
        if battle_id not in battle_ids or not slug or key in row_keys:
            raise ValueError(f"{spec.batch_id}: invalid {context} row key: {key}")
        row_keys.add(key)
        if row["needs_review"]:
            raise ValueError(
                f"{spec.batch_id}: review-needed row entered projection: {key}"
            )
        if row.get("game_track", track) != track:
            raise ValueError(f"{spec.batch_id}: row track boundary mismatch: {key}")
        counts = [row.get(field) for field in base.COUNT_FIELDS]
        if not all(isinstance(value, int) and value >= 0 for value in counts):
            raise ValueError(f"{spec.batch_id}: invalid counts: {key}")
        if row["deployed"] <= 0:
            raise ValueError(f"{spec.batch_id}: non-positive deployed count: {key}")
        accounted = sum(
            row[field] for field in ("survivors", "deaths", "wounded", "routed")
        )
        if accounted != row["deployed"]:
            raise ValueError(f"{spec.batch_id}: casualty arithmetic mismatch: {key}")
    return context_battles, context_rows


def load_source(
    repo_root: Path,
    temporary_root: Path,
    spec: SourceSpec,
    track: str,
    game_version: str,
    context: str = "field",
) -> LoadedSource:
    batch_path = path_below(repo_root, spec.batch_path, "batch_path")
    archive_parts = sorted(
        (batch_path / "bundle").glob(f"{spec.archive_name}.base64.part-*")
    )
    archive_path = temporary_root / f"{spec.batch_id}.tar.xz"
    decode_ordered_archive(archive_parts, archive_path)
    actual_archive_hash = base.sha256_file(archive_path)
    if actual_archive_hash != spec.expected_archive_sha256:
        raise ValueError(f"{spec.batch_id}: normalized archive SHA-256 mismatch")

    extraction_root = temporary_root / f"extract-{spec.batch_id}"
    preflight = base.safe_tar_preflight(archive_path)
    safe_extract_tar(archive_path, extraction_root)
    manifest_path = path_below(extraction_root, spec.manifest_path, "manifest_path")
    manifest_base = path_below(
        extraction_root, spec.manifest_base_path, "manifest_base_path"
    )
    manifest_checks = verify_manifest(manifest_path, manifest_base)

    summary = base.read_json_object(
        path_below(extraction_root, spec.summary_path, "summary_path")
    )
    validate_summary(summary, spec, track, game_version)
    normalization_validation = base.read_json_object(
        path_below(extraction_root, spec.validation_path, "validation_path")
    )
    boundary_evidence = validate_normalization_report(normalization_validation, spec)
    battles = base.read_jsonl(
        path_below(extraction_root, spec.battles_path, "battles_path")
    )
    rows = base.read_jsonl(
        path_below(extraction_root, spec.consolidated_path, "consolidated_path")
    )
    field_battles, field_rows = validate_context_projection(
        spec, battles, rows, track, game_version, context
    )
    verification = {
        "batch_id": spec.batch_id,
        "cohort": spec.cohort,
        "normalization_commit": spec.normalization_commit,
        "normalization_commit_verification": (
            "identifier_format_only_not_compared_to_worktree"
        ),
        "schema_version": spec.schema_version,
        "archive_name": spec.archive_name,
        "expected_archive_sha256": spec.expected_archive_sha256,
        "actual_archive_sha256": actual_archive_hash,
        "archive_hash_passed": True,
        "archive_preflight": preflight,
        "manifest_entries": len(manifest_checks),
        "manifest_passed": True,
        "normalization_validation_status": normalization_validation["status"],
        "normalization_boundary_evidence": boundary_evidence["flags"],
        "unverified_normalization_boundary_flags": boundary_evidence[
            "unverified_flags"
        ],
        "field_battle_ids": sorted(str(row["battle_id"]) for row in field_battles),
        "field_rows": len(field_rows),
    }
    return LoadedSource(spec, summary, field_battles, field_rows, verification)


def reject_cross_source_battle_collisions(sources: list[LoadedSource]) -> None:
    owners: dict[str, str] = {}
    for source in sources:
        for battle in source.field_battles:
            battle_id = str(battle["battle_id"])
            if battle_id in owners:
                raise ValueError(
                    f"battle ID collision across sources: {battle_id} "
                    f"({owners[battle_id]} and {source.spec.batch_id})"
                )
            owners[battle_id] = source.spec.batch_id


def comparison_row(
    cohort: str,
    sources: list[LoadedSource],
    rows: list[dict[str, Any]],
    analysis_id: str,
    focus_slug: str,
    minimum_battles: int,
    minimum_deployed: int,
    repetitions: int,
    context: str = "field",
) -> dict[str, Any]:
    counts = {
        field: sum(int(row[field]) for row in rows) for field in base.COUNT_FIELDS
    }
    battles = len({str(row["battle_id"]) for row in rows})
    reliable = battles >= minimum_battles and counts["deployed"] >= minimum_deployed
    low: float | str = ""
    high: float | str = ""
    if reliable:
        bootstrap_batch_id = analysis_id
        if cohort != "combined":
            bootstrap_batch_id = (
                sources[0].spec.batch_id
                if len(sources) == 1
                else f"{analysis_id}|{cohort}"
            )
        low, high = base.bootstrap_interval(
            rows, bootstrap_batch_id, context, focus_slug, repetitions
        )
    deployed = counts["deployed"]
    return {
        "cohort": cohort,
        "source_batch_ids": "|".join(
            sorted(source.spec.batch_id for source in sources)
        ),
        "independent_battles": battles,
        **counts,
        "kills_per_deployed": counts["kills"] / deployed,
        "death_rate": counts["deaths"] / deployed,
        "casualty_rate": (counts["deaths"] + counts["wounded"]) / deployed,
        "ci95_low": low,
        "ci95_high": high,
        "reliability_status": "reliable" if reliable else "insufficient_evidence",
    }


def bootstrap_delta(
    baseline_rows: list[dict[str, Any]],
    current_rows: list[dict[str, Any]],
    seed_text: str,
    repetitions: int,
) -> tuple[float, float]:
    seed = int(hashlib.sha256(seed_text.encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    samples: list[float] = []
    for _ in range(repetitions):
        baseline = [
            baseline_rows[rng.randrange(len(baseline_rows))] for _ in baseline_rows
        ]
        current = [current_rows[rng.randrange(len(current_rows))] for _ in current_rows]
        baseline_rate = sum(row["kills"] for row in baseline) / sum(
            row["deployed"] for row in baseline
        )
        current_rate = sum(row["kills"] for row in current) / sum(
            row["deployed"] for row in current
        )
        samples.append(current_rate - baseline_rate)
    samples.sort()
    return (
        samples[int(0.025 * (repetitions - 1))],
        samples[int(0.975 * (repetitions - 1))],
    )


def canonical_row_order(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        rows,
        key=lambda row: (
            str(row["battle_context"]),
            str(row["display_name_normalized"]),
            str(row["battle_id"]),
        ),
    )


def formatted_comparison_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        value = dict(row)
        for field in (
            "kills_per_deployed",
            "death_rate",
            "casualty_rate",
            "ci95_low",
            "ci95_high",
        ):
            if value[field] != "":
                value[field] = f"{float(value[field]):.6f}"
        output.append(value)
    return output


def focus_battle_rows(
    sources: list[LoadedSource], focus_slug: str
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for source in sources:
        for row in source.field_rows:
            if row["display_name_normalized"] != focus_slug:
                continue
            deployed = int(row["deployed"])
            output.append(
                {
                    "cohort": source.spec.cohort,
                    "source_batch_id": source.spec.batch_id,
                    "battle_id": row["battle_id"],
                    "deployed": deployed,
                    "kills": row["kills"],
                    "deaths": row["deaths"],
                    "wounded": row["wounded"],
                    "kills_per_deployed": f"{row['kills'] / deployed:.6f}",
                    "casualty_rate": f"{(row['deaths'] + row['wounded']) / deployed:.6f}",
                }
            )
    return sorted(output, key=lambda row: (row["cohort"], row["battle_id"]))


def comparison_report_line(label: str, row: dict[str, Any]) -> str:
    prefix = (
        f"- {label}: {row['independent_battles']} battles, {row['deployed']} deployed"
    )
    if row["reliability_status"] != "reliable":
        return prefix + "; rate withheld because this cohort is below the display gate."
    return (
        prefix
        + f", {row['kills_per_deployed']:.3f} kills/deployed "
        + f"(95% battle bootstrap {row['ci95_low']:.3f}–{row['ci95_high']:.3f}); "
        + f"casualty rate {row['casualty_rate']:.3f}."
    )


def delta_report_line(delta: dict[str, Any]) -> str:
    if delta["evidence_status"] != "reliable":
        below_gate = ", ".join(delta["below_display_gate"])
        return (
            f"- The machine-readable delta remains `{delta['evidence_status']}`; "
            f"below-gate cohorts: {below_gate}. No increase or decline is claimed."
        )

    if delta["ci95_low"] <= 0 <= delta["ci95_high"]:
        direction = (
            "The interval crosses zero, so no increase or decline is established."
        )
    elif delta["ci95_low"] > 0:
        direction = "The interval excludes zero on the increase side."
    else:
        direction = "The interval excludes zero on the decline side."
    return (
        f"- Current minus baseline: {delta['point_estimate']:.3f} kills/deployed "
        f"(95% battle bootstrap {delta['ci95_low']:.3f}–{delta['ci95_high']:.3f}). "
        f"{direction} This is a descriptive cohort difference, not a causal estimate."
    )


def current_field_gate_line(
    focus_label: str,
    current: dict[str, Any],
    minimum_battles: int,
    minimum_deployed: int,
) -> str:
    evidence = (
        f"{current['independent_battles']} battles and {current['deployed']} deployed"
    )
    if current["reliability_status"] == "reliable":
        return (
            f"- {focus_label} has enough current-batch field evidence to close the "
            f"{minimum_battles}-battle / {minimum_deployed}-deployed display gate "
            f"({evidence})."
        )
    return (
        f"- {focus_label} remains below the current-batch field display gate "
        f"({evidence})."
    )


def current_context_report_lines(
    context_rows: list[dict[str, str]],
    focus_rows: list[dict[str, str]],
    focus_label: str,
) -> list[str]:
    if not context_rows:
        return []

    lines = [
        "",
        "## Current batch context coverage",
        "",
        (
            "| Context | Battles | Visible labels | Deployed | Reliable labels | "
            "Insufficient labels |"
        ),
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in context_rows:
        lines.append(
            f"| `{row['context']}` | {row['independent_battles']} | "
            f"{row['observed_labels']} | {row['deployed']} | "
            f"{row['reliable_labels']} | {row['insufficient_labels']} |"
        )
    lines.append("")
    for row in focus_rows:
        if row["context"] == "field":
            continue
        battles = int(row["independent_battles"])
        battle_word = "battle" if battles == 1 else "battles"
        if row["reliability_status"] == "not_observed":
            lines.append(
                f"- {focus_label} was not observed in `{row['context']}`; no rate "
                "from another context is substituted."
            )
            continue
        if row["reliability_status"] == "reliable":
            status = "passes the display gate"
        else:
            status = "remains below the display gate"
        lines.append(
            f"- {focus_label} in `{row['context']}` {status} with {battles} "
            f"{battle_word} and {row['deployed']} deployed; no rate from another context "
            "is substituted."
        )
    lines.append(
        "- No field and siege observations are pooled; each context must pass its own gate."
    )
    return lines


def validate_standalone_context_gates(
    context_rows: list[dict[str, str]],
    minimum_battles: int,
    minimum_deployed: int,
) -> None:
    for row in context_rows:
        context = row.get("context", "")
        try:
            row_minimum_battles = int(row["minimum_battles"])
            row_minimum_deployed = int(row["minimum_deployed"])
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError(
                f"standalone context gate is invalid for {context or 'unknown context'}"
            ) from error
        if (
            row_minimum_battles != minimum_battles
            or row_minimum_deployed != minimum_deployed
        ):
            raise ValueError(
                f"standalone context gate mismatch for {context or 'unknown context'}: "
                f"{row_minimum_battles}/{row_minimum_deployed} != "
                f"{minimum_battles}/{minimum_deployed}"
            )


def focus_outcome_counts(
    sources: list[LoadedSource], focus_slug: str
) -> dict[str, Counter[str]]:
    counts = {"baseline": Counter(), "current": Counter(), "combined": Counter()}
    for source in sources:
        focus_battle_ids = {
            str(row["battle_id"])
            for row in source.field_rows
            if row["display_name_normalized"] == focus_slug
        }
        for battle in source.field_battles:
            if str(battle["battle_id"]) not in focus_battle_ids:
                continue
            result = str(battle.get("result", "")).strip().casefold() or "not_reported"
            counts[source.spec.cohort][result] += 1
            counts["combined"][result] += 1
    return counts


def format_outcome_counts(counts: Counter[str]) -> str:
    if not counts:
        return "no focus-troop battles"
    order = {"victory": 0, "defeat": 1, "retreat": 2, "not_reported": 3}
    return ", ".join(
        f"{count} {result.replace('_', ' ').title()}"
        for result, count in sorted(
            counts.items(), key=lambda item: (order.get(item[0], 99), item[0])
        )
    )


def build_report(
    config: dict[str, Any],
    sources: list[LoadedSource],
    rankings: list[dict[str, Any]],
    reliable: list[dict[str, Any]],
    identities: list[dict[str, str]],
    comparisons: list[dict[str, Any]],
    delta: dict[str, Any],
    current_review_decisions: int | None,
    standalone_context_rows: list[dict[str, str]],
    standalone_focus_rows: list[dict[str, str]],
) -> str:
    context = str(config.get("context", "field"))
    context_label = context.replace("_", " ")
    contextual = lambda stem, suffix: contextual_output_name(stem, context, suffix)
    minimum_battles = int(config["minimum_battles"])
    minimum_deployed = int(config["minimum_deployed"])
    baseline, current, combined = comparisons
    current_sources = [source for source in sources if source.spec.cohort == "current"]
    current_rows = [row for source in current_sources for row in source.field_rows]
    current_labels = {str(row["display_name_normalized"]) for row in current_rows}
    current_battles = sum(len(source.field_battles) for source in current_sources)
    focus_slug = safe_output_stem(str(config["focus_slug"]), "focus_slug")
    track = str(config["track"])
    focus_label = str(
        config.get("focus_label", focus_slug.replace("_", " ").title())
    ).strip()
    if not focus_label:
        raise ValueError("focus_label cannot be blank")
    schema_versions = sorted({source.spec.schema_version for source in sources})
    schema_versions_text = ", ".join(schema_versions)
    current_gate_statement = (
        f"Because this is below the {minimum_battles}-battle gate, none can clear "
        "the standalone battle-count requirement."
        if current_battles < minimum_battles
        else (
            "Per-label standalone eligibility is evaluated against the configured "
            "battle and deployment gates."
        )
    )
    identity_counts = Counter(row["match_status"] for row in identities)
    unresolved_slugs = [
        row["provisional_slug"]
        for row in identities
        if row["match_status"] != "confirmed_id"
    ]
    unresolved_identity_line = (
        "- Unresolved canonical labels remain provisional: "
        + ", ".join(f"`{slug}`" for slug in unresolved_slugs)
        + "."
        if unresolved_slugs
        else "- Every observed label resolves to exactly one canonical ID."
    )
    delta_line = delta_report_line(delta)
    field_gate_line = current_field_gate_line(
        focus_label, current, minimum_battles, minimum_deployed
    )
    context_lines = current_context_report_lines(
        standalone_context_rows, standalone_focus_rows, focus_label
    )
    outcome_counts = focus_outcome_counts(sources, focus_slug)
    outcome_line = (
        "- Focus-cohort battle results: baseline "
        f"{format_outcome_counts(outcome_counts['baseline'])}; current "
        f"{format_outcome_counts(outcome_counts['current'])}; combined "
        f"{format_outcome_counts(outcome_counts['combined'])}. The cohort contrast "
        "is outcome-confounded when these compositions differ."
    )
    lines = [
        f"# Phase 2 analysis — {config['analysis_id']}",
        "",
        "## Result",
        "",
        (
            f"All {len(sources)} normalized archive hashes and internal manifests passed, as did "
            f"the common {context_label} projection's track, version, context, and row-arithmetic checks. "
            f"The {schema_versions_text} "
            "normalized schemas are joined "
            "only through their shared player-side ordinary-troop count fields; upgrade icons and "
            "whole-army contribution are outside this projection."
        ),
        "",
        (
            "Boundary flags absent from historical normalization reports are recorded as "
            "unverified, not inferred. The compatibility decision is an explicit analytical "
            "judgment over the verified common fields, not a claim of full schema equivalence."
        ),
        "",
        (
            f"The current cohort alone has {current_battles} "
            f"independent {context_label} battles "
            f"and {len(current_labels)} visible ordinary-troop labels. {current_gate_statement} "
            "Across the compatible evidence there "
            f"are {sum(len(source.field_battles) for source in sources)} distinct {context_label} battles, "
            f"{len(reliable)} reliable rows, and {len(rankings) - len(reliable)} insufficient rows "
            f"under the {minimum_battles}-battle / {minimum_deployed}-deployed rule."
        ),
        "",
        (
            "These are descriptive rates for visible player-side campaign rows. They are not an "
            "intrinsic-strength tier list, universal score, or causal estimate."
        ),
        "",
        f"## Reliable combined {context_label} ranking",
        "",
    ]
    if reliable:
        lines.extend(
            [
                (
                    "| Rank | Troop | Battles | Deployed | Kills/deployed | "
                    "95% battle bootstrap interval | Casualty rate |"
                ),
                "|---:|---|---:|---:|---:|---:|---:|",
            ]
        )
        for displayed_rank, row in enumerate(reliable[:10], start=1):
            troop_identity = (
                f"`{row['canonical_troop_id']}`"
                if row["canonical_troop_id"]
                else f"`{row['provisional_slug']}` (provisional)"
            )
            lines.append(
                f"| {displayed_rank} | {troop_identity} | "
                f"{row['independent_battles']} | {row['deployed']} | "
                f"{row['kills_per_deployed']:.3f} | {row['ci95_low']:.3f}–"
                f"{row['ci95_high']:.3f} | {row['casualty_rate']:.3f} |"
            )
    else:
        lines.append("No combined troop row reaches the display gate.")
    lines.extend(
        [
            "",
            f"## {focus_label} focus",
            "",
            comparison_report_line("Baseline cohort", baseline),
            comparison_report_line("Current cohort", current),
            comparison_report_line("Compatible combined estimate", combined),
            field_gate_line,
            delta_line,
            outcome_line,
            *context_lines,
            "",
            "## Identity and completeness",
            "",
            (
                f"- {identity_counts.get('confirmed_id', 0)} of {len(identities)} observed labels "
                f"have one exact canonical ID in the versioned audit for track `{track}`."
            ),
            unresolved_identity_line,
            (
                f"- `{contextual('combined_ranking_complete', '.csv')}` retains every observed {context_label} label; "
                f"`{contextual('combined_ranking_reliable', '.csv')}` and "
                f"`{contextual('combined_insufficient_evidence', '.csv')}` split it "
                "without dropping low-sample rows."
            ),
            (
                f"- Rows marked for review and non-{context_label} battles are rejected from the projection. "
                "Where historical validation reports omit explicit side, hero, or off-screen flags, "
                "that missing verification is preserved in "
                f"`{contextual('compatibility_decision', '.json')}`."
            ),
            "",
            "## Limitations",
            "",
            (
                "- These are observational campaign results, confounded by battle outcome, army "
                "composition, enemy composition, map, difficulty, and player choices. Battle-result "
                "composition is preserved in `combined_battle_provenance.csv` rather than assumed."
            ),
            (
                "- Row visibility is partial, so total-army contribution, deployment share, and "
                "off-screen performance cannot be calculated."
            ),
            (
                "- Raw PNGs for the current batch are not retained; "
                + (
                    f"its {current_review_decisions} field-level review decisions remain unresolved "
                    if current_review_decisions is not None
                    else "its field-level review decisions remain unresolved "
                )
                + "in the separate review layer."
            ),
            (
                f"- The schema join across {schema_versions_text} is deliberately narrow. It does "
                "not imply that every field is interchangeable."
            ),
            "- No frozen model was changed or recalibrated.",
        ]
    )
    return "\n".join(lines) + "\n"


def update_readme(path: Path, config_path: Path, repo_root: Path) -> None:
    config = base.read_json_object(config_path)
    context = str(config.get("context", "field"))
    context_label = context.replace("_", " ")
    marker = f"## Compatible combined {context_label} evidence"
    existing = path.read_text(encoding="utf-8")
    prefix = existing.split(marker, maxsplit=1)[0].rstrip()
    relative_config = config_path.relative_to(repo_root)
    addition = (
        f"{marker}\n\n"
        "After reproducing the standalone analysis above, regenerate the compatible source-batch "
        f"{context_label} projection with:\n\n"
        "```bash\n"
        "python3 scripts/analysis/analyze_compatible_field_evidence.py \\\n"
        f"  --config {relative_config} \\\n"
        "  --repo-root . \\\n"
        f"  --batch-dir {path.parent.parent.relative_to(repo_root)} \\\n"
        "  --identity-root data/realm_of_thrones/audit\n"
        "```\n"
    )
    path.write_text(prefix + "\n\n" + addition, encoding="utf-8")


def load_all_sources(
    repo_root: Path,
    specs: list[SourceSpec],
    track: str,
    game_version: str,
    context: str = "field",
) -> list[LoadedSource]:
    with tempfile.TemporaryDirectory(prefix="bannerlord-compatible-field-") as raw_temp:
        temporary_root = Path(raw_temp)
        return [
            load_source(repo_root, temporary_root, spec, track, game_version, context)
            for spec in specs
        ]


def build_focus_results(
    config: dict[str, Any], sources: list[LoadedSource]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    context = str(config.get("context", "field"))
    focus_slug = str(config["focus_slug"])
    minimum_battles = int(config["minimum_battles"])
    minimum_deployed = int(config["minimum_deployed"])
    repetitions = int(config["bootstrap_repetitions"])
    analysis_id = str(config["analysis_id"])
    cohort_sources = {
        cohort: [source for source in sources if source.spec.cohort == cohort]
        for cohort in ("baseline", "current")
    }
    cohort_rows = {
        cohort: [
            row
            for source in selected
            for row in source.field_rows
            if row["display_name_normalized"] == focus_slug
        ]
        for cohort, selected in cohort_sources.items()
    }
    cohort_rows = {
        cohort: canonical_row_order(rows) for cohort, rows in cohort_rows.items()
    }
    if not cohort_rows["baseline"] or not cohort_rows["current"]:
        raise ValueError(
            f"focus slug is missing from a comparison cohort: {focus_slug}"
        )

    comparisons = [
        comparison_row(
            cohort,
            cohort_sources[cohort],
            cohort_rows[cohort],
            analysis_id,
            focus_slug,
            minimum_battles,
            minimum_deployed,
            repetitions,
            context,
        )
        for cohort in ("baseline", "current")
    ]
    comparisons.append(
        comparison_row(
            "combined",
            sources,
            canonical_row_order(cohort_rows["baseline"] + cohort_rows["current"]),
            analysis_id,
            focus_slug,
            minimum_battles,
            minimum_deployed,
            repetitions,
            context,
        )
    )
    baseline, current, _combined = comparisons
    delta_low, delta_high = bootstrap_delta(
        cohort_rows["baseline"],
        cohort_rows["current"],
        f"{analysis_id}|current-minus-baseline|{focus_slug}|{repetitions}",
        repetitions,
    )
    below_display_gate = [
        row["cohort"]
        for row in (baseline, current)
        if row["reliability_status"] != "reliable"
    ]
    evidence_status = (
        "reliable" if not below_display_gate else "diagnostic_only_below_display_gate"
    )
    delta = {
        "metric": "current_minus_baseline_kills_per_deployed",
        "point_estimate": current["kills_per_deployed"]
        - baseline["kills_per_deployed"],
        "ci95_low": delta_low,
        "ci95_high": delta_high,
        "bootstrap_unit": "independent_battle_within_cohort",
        "bootstrap_repetitions": repetitions,
        "seed": f"sha256(analysis_id|current-minus-baseline|focus_slug|{repetitions})",
        "evidence_status": evidence_status,
        "below_display_gate": below_display_gate,
        "report_displayed": evidence_status == "reliable",
    }
    return comparisons, delta


def build_combined_analysis(
    config: dict[str, Any],
    sources: list[LoadedSource],
    repo_root: Path,
    identity_root: Path,
) -> CombinedAnalysis:
    context = str(config.get("context", "field"))
    combined_rows = canonical_row_order(
        [row for source in sources for row in source.field_rows]
    )
    candidates = base.collect_identity_candidates(identity_root, None, repo_root)
    identities = base.build_identity_audit(
        combined_rows, candidates, str(config["track"])
    )
    rankings = [
        row
        for row in base.build_rankings(
            combined_rows,
            identities,
            str(config["analysis_id"]),
            int(config["minimum_battles"]),
            int(config["minimum_deployed"]),
            int(config["bootstrap_repetitions"]),
        )
        if row["context"] == context
    ]
    reliable = [row for row in rankings if row["reliability_status"] == "reliable"]
    insufficient = [
        row for row in rankings if row["reliability_status"] == "insufficient_evidence"
    ]
    comparisons, delta = build_focus_results(config, sources)
    coverage = {
        "context": context,
        "independent_battles": sum(len(source.field_battles) for source in sources),
        "observed_labels": len(rankings),
        "deployed": sum(int(row["deployed"]) for row in rankings),
        "reliable_labels": len(reliable),
        "insufficient_labels": len(insufficient),
        "minimum_battles": int(config["minimum_battles"]),
        "minimum_deployed": int(config["minimum_deployed"]),
    }
    return CombinedAnalysis(
        sources,
        identities,
        rankings,
        reliable,
        insufficient,
        comparisons,
        delta,
        coverage,
    )


def build_provenance_rows(sources: list[LoadedSource]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for source in sources:
        for battle in source.field_battles:
            output.append(
                {
                    "cohort": source.spec.cohort,
                    "source_batch_id": source.spec.batch_id,
                    "schema_version": source.spec.schema_version,
                    "normalization_commit": source.spec.normalization_commit,
                    "normalization_commit_verification": source.verification[
                        "normalization_commit_verification"
                    ],
                    "archive_sha256": source.spec.expected_archive_sha256,
                    "battle_id": battle["battle_id"],
                    "captured_at": battle.get("captured_at", ""),
                    "player_side": battle["player_side"],
                    "result": str(battle.get("result", "")).strip() or "not_reported",
                }
            )
    return output


def build_compatibility_decision(
    config: dict[str, Any], sources: list[LoadedSource]
) -> dict[str, Any]:
    context = str(config.get("context", "field"))
    return {
        "status": "passed",
        "decision": f"compatible_on_common_player_{context}_count_projection",
        "analysis_id": config["analysis_id"],
        "track": config["track"],
        "game_version": config["game_version"],
        "context": context,
        "projection_fields": list(COMMON_FIELD_PROJECTION),
        "schema_versions": sorted({source.spec.schema_version for source in sources}),
        "sources": [source.verification for source in sources],
        "compatibility_basis": {
            "status": "analysis_decision",
            "rationale": (
                f"Same track, game version, and {context.replace('_', ' ')} context; joined only on common "
                "count fields whose presence, non-negativity, and casualty arithmetic "
                "were machine-validated. This does not establish full semantic "
                "equivalence between normalized schema versions."
            ),
        },
        "checks": {
            "archive_hashes_verified": True,
            "artifact_manifests_verified": True,
            "normalization_validations_passed": True,
            "battle_ids_distinct_across_sources": True,
            "review_needed_rows_excluded_from_projection": True,
            "track_matches": True,
            "game_version_matches": True,
            "context_matches": True,
            "common_count_projection_fields_and_arithmetic_validated": True,
        },
        "excluded_metrics": [
            "whole_army_contribution_index",
            "whole_army_share",
            "off_screen_rows",
            "upgrade_ready",
        ],
        "limitations": [
            "Schema compatibility is limited to the listed common projection.",
            "All source screenshots expose partial troop rows.",
            "Campaign conditions differ and remain observational confounders.",
            (
                "Normalization commit identifiers are provenance labels and were "
                "format-validated, not compared with the current worktree."
            ),
            (
                "Some historical normalization reports omit explicit boundary flags; "
                "those flags remain unverified in the per-source records."
            ),
        ],
    }


def write_tabular_outputs(
    batch_dir: Path, analysis: CombinedAnalysis, focus_slug: str, context: str
) -> None:
    analysis_dir = batch_dir / "analysis"
    focus_stem = safe_output_stem(focus_slug, "focus_slug")
    base.write_csv(
        analysis_dir
        / contextual_output_name("combined_canonical_identity_audit", context, ".csv"),
        base.IDENTITY_FIELDS,
        analysis.identities,
    )
    base.write_csv(
        analysis_dir
        / contextual_output_name("combined_ranking_complete", context, ".csv"),
        base.RANKING_FIELDS,
        base.format_ranking_rows(analysis.rankings),
    )
    base.write_csv(
        analysis_dir
        / contextual_output_name("combined_ranking_reliable", context, ".csv"),
        base.RANKING_FIELDS,
        base.format_ranking_rows(analysis.reliable, rerank=True),
    )
    base.write_csv(
        analysis_dir
        / contextual_output_name("combined_insufficient_evidence", context, ".csv"),
        base.RANKING_FIELDS,
        base.format_ranking_rows(analysis.insufficient),
    )
    base.write_csv(
        analysis_dir
        / contextual_output_name("combined_context_coverage", context, ".csv"),
        analysis.coverage.keys(),
        [analysis.coverage],
    )
    provenance_rows = build_provenance_rows(analysis.sources)
    base.write_csv(
        analysis_dir
        / contextual_output_name("combined_battle_provenance", context, ".csv"),
        provenance_rows[0].keys(),
        provenance_rows,
    )
    base.write_csv(
        analysis_dir
        / contextual_output_name(f"{focus_stem}_comparison", context, ".csv"),
        COMPARISON_FIELDS,
        formatted_comparison_rows(analysis.comparisons),
    )
    base.write_csv(
        analysis_dir
        / contextual_output_name(f"{focus_stem}_battle_rates", context, ".csv"),
        FOCUS_BATTLE_FIELDS,
        focus_battle_rows(analysis.sources, focus_slug),
    )


def update_validation_report(
    path: Path,
    compatibility: dict[str, Any],
    analysis: CombinedAnalysis,
    focus_slug: str,
    context: str,
) -> None:
    validation = base.read_json_object(path)
    validation[f"compatible_{context}_evidence"] = {
        "status": "passed",
        "source_batches": len(analysis.sources),
        "schema_versions": compatibility["schema_versions"],
        "independent_battles": analysis.coverage["independent_battles"],
        "complete_rows": len(analysis.rankings),
        "reliable_rows": len(analysis.reliable),
        "insufficient_rows": len(analysis.insufficient),
        "focus_slug": focus_slug,
        "focus_combined_status": analysis.comparisons[-1]["reliability_status"],
        "delta_evidence_status": analysis.delta["evidence_status"],
        "archive_hashes_verified": True,
        "artifact_manifests_verified": True,
        "normalization_validations_passed": True,
    }
    base.write_json(path, validation)


def write_metadata_outputs(
    config: dict[str, Any],
    config_path: Path,
    repo_root: Path,
    batch_dir: Path,
    analysis: CombinedAnalysis,
) -> None:
    analysis_dir = batch_dir / "analysis"
    standalone_validation = base.read_json_object(
        analysis_dir / "validation_report.json"
    )
    current_review_decisions = standalone_validation.get("review", {}).get("decisions")
    if not isinstance(current_review_decisions, int):
        current_review_decisions = None
    context_coverage_path = analysis_dir / "context_coverage.csv"
    focus_contexts_path = analysis_dir / "focus_troop_contexts.csv"
    standalone_context_rows = (
        base.read_csv(context_coverage_path) if context_coverage_path.is_file() else []
    )
    standalone_focus_rows = (
        base.read_csv(focus_contexts_path) if focus_contexts_path.is_file() else []
    )
    validate_standalone_context_gates(
        standalone_context_rows,
        int(config["minimum_battles"]),
        int(config["minimum_deployed"]),
    )
    compatibility = build_compatibility_decision(config, analysis.sources)
    context = str(config.get("context", "field"))
    focus_stem = safe_output_stem(str(config["focus_slug"]), "focus_slug")
    base.write_json(
        analysis_dir
        / contextual_output_name("compatibility_decision", context, ".json"),
        compatibility,
    )
    base.write_json(
        analysis_dir
        / contextual_output_name(f"{focus_stem}_delta_uncertainty", context, ".json"),
        analysis.delta,
    )
    update_validation_report(
        analysis_dir / "validation_report.json",
        compatibility,
        analysis,
        str(config["focus_slug"]),
        context,
    )
    (
        analysis_dir / contextual_output_name("ANALYSIS_REPORT", context, ".md")
    ).write_text(
        build_report(
            config,
            analysis.sources,
            analysis.rankings,
            analysis.reliable,
            analysis.identities,
            analysis.comparisons,
            analysis.delta,
            current_review_decisions,
            standalone_context_rows,
            standalone_focus_rows,
        ),
        encoding="utf-8",
    )
    (
        analysis_dir / contextual_output_name("COMPARISON_BLOCKED", context, ".md")
    ).unlink(missing_ok=True)
    update_readme(analysis_dir / "README.md", config_path, repo_root)


def write_artifact_manifest(batch_dir: Path) -> None:
    analysis_dir = batch_dir / "analysis"
    review_dir = batch_dir / "review"
    hashed_paths = [
        path
        for path in [*review_dir.iterdir(), *analysis_dir.iterdir()]
        if path.is_file() and path.name != "artifact_hashes.csv"
    ]
    base.write_csv(
        analysis_dir / "artifact_hashes.csv",
        ("file", "sha256", "size_bytes"),
        base.artifact_rows(batch_dir, hashed_paths),
    )


def run_analysis(
    config_path: Path, repo_root: Path, batch_dir: Path, identity_root: Path
) -> dict[str, Any]:
    config = base.read_json_object(config_path)
    track = str(config["track"])
    game_version = str(config["game_version"])
    context = str(config.get("context", "field"))
    if context not in base.CONTEXTS:
        raise ValueError(f"unsupported battle context: {context}")
    focus_slug = safe_output_stem(str(config["focus_slug"]), "focus_slug")
    specs = sorted(
        (SourceSpec.from_dict(value) for value in config["sources"]),
        key=lambda spec: (spec.cohort, spec.batch_id),
    )
    if {spec.cohort for spec in specs} != {"baseline", "current"}:
        raise ValueError("compatible sources must contain baseline and current cohorts")

    sources = load_all_sources(repo_root, specs, track, game_version, context)
    reject_cross_source_battle_collisions(sources)
    analysis = build_combined_analysis(config, sources, repo_root, identity_root)
    (batch_dir / "analysis").mkdir(parents=True, exist_ok=True)
    (batch_dir / "review").mkdir(parents=True, exist_ok=True)
    write_tabular_outputs(batch_dir, analysis, focus_slug, context)
    write_metadata_outputs(config, config_path, repo_root, batch_dir, analysis)
    write_artifact_manifest(batch_dir)
    return {
        "status": "passed",
        "independent_battles": analysis.coverage["independent_battles"],
        "complete_rows": len(analysis.rankings),
        "reliable_rows": len(analysis.reliable),
        "insufficient_rows": len(analysis.insufficient),
        "focus_combined_status": analysis.comparisons[-1]["reliability_status"],
        "delta_evidence_status": analysis.delta["evidence_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--batch-dir", type=Path, required=True)
    parser.add_argument("--identity-root", type=Path, required=True)
    args = parser.parse_args()
    result = run_analysis(
        args.config.resolve(),
        args.repo_root.resolve(),
        args.batch_dir.resolve(),
        args.identity_root.resolve(),
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
