#!/usr/bin/env python3
"""Build a conservative Phase 2 analysis from a normalized combat batch."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import subprocess
import tarfile
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

CONTEXTS = ("field", "siege_attack", "siege_defense")
COUNT_FIELDS = ("deployed", "survivors", "kills", "deaths", "wounded", "routed")
RANKING_FIELDS = (
    "context",
    "rank",
    "display_name",
    "provisional_slug",
    "canonical_troop_id",
    "identity_status",
    "independent_battles",
    *COUNT_FIELDS,
    "kills_per_deployed",
    "death_rate",
    "casualty_rate",
    "ci95_low",
    "ci95_high",
    "reliability_status",
)
IDENTITY_FIELDS = (
    "provisional_slug",
    "display_name",
    "observed_track",
    "canonical_troop_id",
    "match_status",
    "resolution_method",
    "evidence_paths",
    "candidate_count",
    "candidate_troop_ids",
    "blocking_reason",
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{line_number}: expected an object")
            rows.append(value)
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: Iterable[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_tar_preflight(archive_path: Path) -> dict[str, int]:
    names: set[str] = set()
    regular_files = 0
    total_uncompressed_bytes = 0
    with tarfile.open(archive_path, "r:xz") as archive:
        for member in archive.getmembers():
            name = member.name
            pure = PurePosixPath(name)
            if not name or pure.is_absolute() or ".." in pure.parts:
                raise ValueError(f"unsafe archive member path: {name!r}")
            if name in names:
                raise ValueError(f"duplicate archive member: {name}")
            names.add(name)
            if member.issym() or member.islnk() or member.isdev() or member.isfifo():
                raise ValueError(f"unsupported archive member type: {name}")
            if not (member.isfile() or member.isdir()):
                raise ValueError(f"unsupported archive member type: {name}")
            if member.isfile():
                regular_files += 1
                total_uncompressed_bytes += member.size
    if len(names) > 10_000:
        raise ValueError("archive member limit exceeded")
    if total_uncompressed_bytes > 1_000_000_000:
        raise ValueError("archive uncompressed-size limit exceeded")
    return {
        "members": len(names),
        "regular_files": regular_files,
        "total_uncompressed_bytes": total_uncompressed_bytes,
    }


def normalize_display_name(value: str) -> str:
    text = unicodedata.normalize("NFKC", value or "")
    text = text.replace("’", "'").replace("‘", "'").replace("`", "'")
    text = re.sub(r"\s*\[(?:\s*(?:t|tier)?\s*\d{1,2})\s*\]\s*$", "", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip(" .").casefold()


def verify_manifest(input_dir: Path, manifest_path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    for row in read_csv(manifest_path):
        relative = row["file"]
        path = input_dir / relative
        exists = path.is_file()
        actual_hash = sha256_file(path) if exists else ""
        actual_size = path.stat().st_size if exists else None
        passed = (
            exists
            and actual_hash == row["sha256"]
            and actual_size == int(row["size_bytes"])
        )
        checks.append(
            {
                "file": relative,
                "expected_sha256": row["sha256"],
                "actual_sha256": actual_hash,
                "expected_size_bytes": int(row["size_bytes"]),
                "actual_size_bytes": actual_size,
                "passed": passed,
            }
        )
        if not passed:
            errors.append(f"artifact manifest mismatch: {relative}")
    return checks, errors


def git_changed_paths(repo_root: Path, commit: str, paths: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", commit, "--", *paths],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def validate_normalized(
    battles: list[dict[str, Any]],
    occurrences: list[dict[str, Any]],
    primary: list[dict[str, Any]],
    consolidated: list[dict[str, Any]],
    screenshot_manifest: list[dict[str, str]],
    review_queue: list[dict[str, str]],
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    battle_by_id = {str(row.get("battle_id")): row for row in battles}
    if len(battle_by_id) != len(battles):
        errors.append("duplicate battle_id")

    image_hashes = {row.get("image_sha256") for row in screenshot_manifest}
    occurrence_by_id = {str(row.get("observation_id")): row for row in occurrences}
    if len(occurrence_by_id) != len(occurrences):
        errors.append("duplicate observation_id")

    primary_ids: set[str] = set()
    for row in primary:
        observation_id = str(row.get("observation_id"))
        if observation_id in primary_ids:
            errors.append(f"duplicate primary observation: {observation_id}")
        primary_ids.add(observation_id)
        battle = battle_by_id.get(str(row.get("battle_id")))
        if not battle:
            errors.append(f"primary row has unknown battle: {observation_id}")
            continue
        if row.get("row_type") != "troop" or row.get("analysis_status") != "included_primary":
            errors.append(f"non-primary troop in primary input: {observation_id}")
        if row.get("needs_review"):
            errors.append(f"review-needed row entered primary input: {observation_id}")
        if row.get("side") != battle.get("player_side"):
            errors.append(f"player/enemy side boundary violation: {observation_id}")
        if row.get("battle_context") != battle.get("battle_context"):
            errors.append(f"battle context mismatch: {observation_id}")
        if row.get("source_image_sha256") not in image_hashes:
            errors.append(f"unknown source image hash: {observation_id}")
        for field in COUNT_FIELDS:
            if not isinstance(row.get(field), int) or int(row[field]) < 0:
                errors.append(f"invalid {field}: {observation_id}")
        if all(isinstance(row.get(field), int) for field in COUNT_FIELDS):
            accounted = sum(int(row[field]) for field in ("survivors", "deaths", "wounded", "routed"))
            if accounted != int(row["deployed"]):
                errors.append(f"troop arithmetic mismatch: {observation_id}")

    consolidated_keys: set[tuple[str, str, str]] = set()
    for row in consolidated:
        key = (
            str(row.get("battle_id")),
            str(row.get("battle_context")),
            str(row.get("display_name_normalized")),
        )
        if key in consolidated_keys:
            errors.append(f"duplicate consolidated key: {'|'.join(key)}")
        consolidated_keys.add(key)
        if row.get("battle_context") not in CONTEXTS:
            errors.append(f"unknown consolidated context: {'|'.join(key)}")
        if row.get("needs_review"):
            errors.append(f"review-needed row entered consolidated input: {'|'.join(key)}")
        for field in COUNT_FIELDS:
            if not isinstance(row.get(field), int) or int(row[field]) < 0:
                errors.append(f"invalid consolidated {field}: {'|'.join(key)}")
        if all(isinstance(row.get(field), int) for field in COUNT_FIELDS):
            accounted = sum(int(row[field]) for field in ("survivors", "deaths", "wounded", "routed"))
            if accounted != int(row["deployed"]):
                errors.append(f"consolidated arithmetic mismatch: {'|'.join(key)}")

    for queued in review_queue:
        observation_id = queued.get("observation_id", "")
        source = occurrence_by_id.get(observation_id)
        if not source:
            errors.append(f"review item missing source observation: {observation_id}")
        elif source.get("row_type") != "hero" or source.get("analysis_status") != "excluded_hero":
            errors.append(f"review item is not an excluded hero: {observation_id}")
        if observation_id in primary_ids:
            errors.append(f"review item leaked into primary rows: {observation_id}")

    context_counts = Counter(str(row.get("battle_context")) for row in battles)
    summary = {
        "battles": len(battles),
        "battle_context_counts": dict(sorted(context_counts.items())),
        "occurrences": len(occurrences),
        "primary_occurrences": len(primary),
        "consolidated_rows": len(consolidated),
        "review_items": len(review_queue),
        "ordinary_troop_labels": len(
            {str(row.get("display_name_normalized")) for row in consolidated}
        ),
    }
    return errors, summary


def collect_identity_candidates(
    identity_root: Path,
    existing_audit: Path | None,
) -> dict[str, list[tuple[str, str]]]:
    candidates: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for path in sorted(identity_root.rglob("*.csv")):
        try:
            rows = read_csv(path)
        except (OSError, UnicodeError, csv.Error):
            continue
        if not rows or "troop_id" not in rows[0]:
            continue
        for row in rows:
            troop_id = (row.get("troop_id") or "").strip()
            name = next(
                (
                    (row.get(field) or "").strip()
                    for field in ("name", "troop_name", "display_name")
                    if (row.get(field) or "").strip()
                ),
                "",
            )
            if troop_id and name:
                candidate = (troop_id, str(path))
                key = normalize_display_name(name)
                if candidate not in candidates[key]:
                    candidates[key].append(candidate)

    if existing_audit and existing_audit.is_file():
        for row in read_csv(existing_audit):
            if (
                row.get("observed_track") == "realm_of_thrones"
                and row.get("match_status") == "confirmed_id"
                and row.get("canonical_troop_id")
            ):
                name = row.get("display_name", "")
                candidate = (row["canonical_troop_id"], str(existing_audit))
                key = normalize_display_name(name)
                if candidate not in candidates[key]:
                    candidates[key].append(candidate)
    return candidates


def build_identity_audit(
    consolidated: list[dict[str, Any]],
    candidates: dict[str, list[tuple[str, str]]],
    track: str,
) -> list[dict[str, str]]:
    labels: dict[str, str] = {}
    for row in consolidated:
        slug = str(row["display_name_normalized"])
        raw_names = row.get("display_names_raw") or []
        labels.setdefault(slug, str(raw_names[0] if raw_names else slug))

    output: list[dict[str, str]] = []
    for slug, display_name in sorted(labels.items()):
        matches = candidates.get(normalize_display_name(display_name), [])
        ids = sorted({troop_id for troop_id, _ in matches})
        paths = sorted({path for _, path in matches})
        confirmed = len(ids) == 1
        output.append(
            {
                "provisional_slug": slug,
                "display_name": display_name,
                "observed_track": track,
                "canonical_troop_id": ids[0] if confirmed else "",
                "match_status": "confirmed_id" if confirmed else (
                    "ambiguous_exact_name" if len(ids) > 1 else "unresolved"
                ),
                "resolution_method": (
                    "exact_normalized_display_name_in_versioned_track_reference"
                    if confirmed
                    else ""
                ),
                "evidence_paths": "|".join(paths),
                "candidate_count": str(len(ids)),
                "candidate_troop_ids": "|".join(ids),
                "blocking_reason": "" if confirmed else (
                    "Multiple exact name-to-ID candidates in versioned Realm of Thrones references"
                    if len(ids) > 1
                    else "No exact name-to-ID match in versioned Realm of Thrones references"
                ),
            }
        )
    return output


def bootstrap_interval(
    rows: list[dict[str, Any]],
    batch_id: str,
    context: str,
    slug: str,
    repetitions: int,
) -> tuple[float, float]:
    seed_text = f"{batch_id}|{context}|{slug}|{repetitions}"
    seed = int(hashlib.sha256(seed_text.encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    samples: list[float] = []
    for _ in range(repetitions):
        sample = [rows[rng.randrange(len(rows))] for _ in rows]
        deployed = sum(int(row["deployed"]) for row in sample)
        kills = sum(int(row["kills"]) for row in sample)
        samples.append(kills / deployed if deployed else 0.0)
    samples.sort()
    low_index = int(0.025 * (repetitions - 1))
    high_index = int(0.975 * (repetitions - 1))
    return samples[low_index], samples[high_index]


def build_rankings(
    consolidated: list[dict[str, Any]],
    identities: list[dict[str, str]],
    batch_id: str,
    minimum_battles: int,
    minimum_deployed: int,
    repetitions: int,
) -> list[dict[str, Any]]:
    identity_by_slug = {row["provisional_slug"]: row for row in identities}
    output: list[dict[str, Any]] = []
    for context in ("overall", *CONTEXTS):
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in consolidated:
            if context == "overall" or row["battle_context"] == context:
                groups[str(row["display_name_normalized"])].append(row)
        context_rows: list[dict[str, Any]] = []
        for slug, rows in groups.items():
            counts = {field: sum(int(row[field]) for row in rows) for field in COUNT_FIELDS}
            battles = len({str(row["battle_id"]) for row in rows})
            reliable = battles >= minimum_battles and counts["deployed"] >= minimum_deployed
            ci_low: float | str = ""
            ci_high: float | str = ""
            if reliable:
                ci_low, ci_high = bootstrap_interval(
                    rows, batch_id, context, slug, repetitions
                )
            raw_names = Counter(
                str((row.get("display_names_raw") or [slug])[0]) for row in rows
            )
            identity = identity_by_slug[slug]
            deployed = counts["deployed"]
            context_rows.append(
                {
                    "context": context,
                    "rank": 0,
                    "display_name": raw_names.most_common(1)[0][0],
                    "provisional_slug": slug,
                    "canonical_troop_id": identity["canonical_troop_id"],
                    "identity_status": identity["match_status"],
                    "independent_battles": battles,
                    **counts,
                    "kills_per_deployed": counts["kills"] / deployed,
                    "death_rate": counts["deaths"] / deployed,
                    "casualty_rate": (counts["deaths"] + counts["wounded"]) / deployed,
                    "ci95_low": ci_low,
                    "ci95_high": ci_high,
                    "reliability_status": "reliable" if reliable else "insufficient_evidence",
                }
            )
        context_rows.sort(
            key=lambda row: (
                -float(row["kills_per_deployed"]),
                -int(row["deployed"]),
                str(row["provisional_slug"]),
            )
        )
        for rank, row in enumerate(context_rows, start=1):
            row["rank"] = rank
            output.append(row)
    return output


def format_ranking_rows(rows: list[dict[str, Any]], rerank: bool = False) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    ranks: Counter[str] = Counter()
    for row in rows:
        value = dict(row)
        if rerank:
            ranks[str(value["context"])] += 1
            value["rank"] = ranks[str(value["context"])]
        for field in ("kills_per_deployed", "death_rate", "casualty_rate", "ci95_low", "ci95_high"):
            if value[field] != "":
                value[field] = f"{float(value[field]):.6f}"
        output.append(value)
    return output


def build_review_decisions(
    review_queue: list[dict[str, str]],
    occurrences: list[dict[str, Any]],
    reviewer: str,
) -> list[dict[str, str]]:
    occurrences_by_id = {str(row["observation_id"]): row for row in occurrences}
    output: list[dict[str, str]] = []
    for queued in review_queue:
        source = occurrences_by_id[queued["observation_id"]]
        for field in queued["uncertain_fields"].split("|"):
            field = field.strip()
            output.append(
                {
                    "observation_id": queued["observation_id"],
                    "battle_id": queued["battle_id"],
                    "source_image_file": queued["source_image_file"],
                    "source_image_sha256": str(source["source_image_sha256"]),
                    "field": field,
                    "original_value": "" if source.get(field) is None else str(source[field]),
                    "reviewed_value": "",
                    "decision_status": "unresolved_source_unavailable",
                    "reason": (
                        "The normalized evidence records a visual level-up icon, but the "
                        "repository-addressable source image is unavailable; no numeric value "
                        "is inferred."
                    ),
                    "reviewer": reviewer,
                    "evidence_reference": "normalized occurrence and review_queue.csv",
                }
            )
    return output


def artifact_rows(batch_dir: Path, paths: list[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(paths):
        rows.append(
            {
                "file": str(path.relative_to(batch_dir)),
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--batch-dir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--identity-root", type=Path, required=True)
    parser.add_argument("--existing-identity-audit", type=Path)
    parser.add_argument("--normalization-commit", required=True)
    parser.add_argument("--expected-archive-sha256", required=True)
    parser.add_argument("--archive-path", type=Path, required=True)
    parser.add_argument("--expected-source-sha256", required=True)
    parser.add_argument("--source-path", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--track", default="realm_of_thrones")
    parser.add_argument("--minimum-battles", type=int, default=5)
    parser.add_argument("--minimum-deployed", type=int, default=20)
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    parser.add_argument("--reviewer", default="Codex local analysis agent (GPT-5)")
    args = parser.parse_args()

    args.repo_root = args.repo_root.resolve()
    args.input_dir = args.input_dir.resolve()
    args.batch_dir = args.batch_dir.resolve()
    analysis_dir = args.batch_dir / "analysis"
    review_dir = args.batch_dir / "review"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    manifest_checks, manifest_errors = verify_manifest(
        args.input_dir, args.batch_dir / "artifact_hashes.csv"
    )
    archive_hash = sha256_file(args.archive_path)
    archive_ok = archive_hash == args.expected_archive_sha256
    if not archive_ok:
        manifest_errors.append("normalized archive hash mismatch")
    archive_preflight = safe_tar_preflight(args.archive_path)

    battles = read_jsonl(args.input_dir / "battles.jsonl")
    occurrences = read_jsonl(args.input_dir / "troop_occurrences.jsonl")
    primary = read_jsonl(args.input_dir / "primary_troop_occurrences.jsonl")
    consolidated = read_jsonl(args.input_dir / "troop_battle_consolidated.jsonl")
    screenshot_manifest = read_csv(args.input_dir / "screenshots_manifest.csv")
    review_queue = read_csv(args.input_dir / "review_queue.csv")
    structural_errors, normalized_summary = validate_normalized(
        battles,
        occurrences,
        primary,
        consolidated,
        screenshot_manifest,
        review_queue,
    )

    immutable_paths = [
        str((args.batch_dir / name).relative_to(args.repo_root))
        for name in (
            "screenshots_manifest.csv",
            "normalization_summary.json",
            "validation_report.json",
            "artifact_hashes.csv",
            "bundle",
        )
    ]
    immutable_changes = git_changed_paths(
        args.repo_root, args.normalization_commit, immutable_paths
    )
    frozen_model_changes = git_changed_paths(
        args.repo_root, args.normalization_commit, ["analysis/model_versions"]
    )

    source_exists = args.source_path.is_file()
    source_hash = sha256_file(args.source_path) if source_exists else ""
    source_ok = source_exists and source_hash == args.expected_source_sha256
    external_blockers = [] if source_ok else [
        {
            "code": "original_source_archive_unavailable",
            "expected_path": str(args.source_path.relative_to(args.repo_root)),
            "expected_sha256": args.expected_source_sha256,
            "expected_size_bytes": 18596761,
        }
    ]

    validation_errors = [
        *manifest_errors,
        *structural_errors,
        *[f"immutable normalized input changed: {path}" for path in immutable_changes],
        *[f"frozen model changed: {path}" for path in frozen_model_changes],
    ]
    if validation_errors:
        raise ValueError("\n".join(validation_errors))

    candidates = collect_identity_candidates(
        args.identity_root, args.existing_identity_audit
    )
    identities = build_identity_audit(consolidated, candidates, args.track)
    rankings = build_rankings(
        consolidated,
        identities,
        args.batch_id,
        args.minimum_battles,
        args.minimum_deployed,
        args.bootstrap_repetitions,
    )
    reliable = [row for row in rankings if row["reliability_status"] == "reliable"]
    insufficient = [
        row for row in rankings if row["reliability_status"] == "insufficient_evidence"
    ]
    review_decisions = build_review_decisions(review_queue, occurrences, args.reviewer)

    write_csv(review_dir / "review_decisions.csv", review_decisions[0].keys(), review_decisions)
    (review_dir / "README.md").write_text(
        "# Phase 2 review decisions\n\n"
        "All five queued values remain unresolved. Each is a hero `upgrade_ready` field "
        "derived from a visual icon. The original screenshots are not repository-addressable, "
        "so the reviewed layer preserves null values and does not infer numeric counts. Heroes "
        "remain excluded from ordinary troop rankings.\n",
        encoding="utf-8",
    )

    write_csv(analysis_dir / "canonical_identity_audit.csv", IDENTITY_FIELDS, identities)
    write_csv(analysis_dir / "ranking_complete.csv", RANKING_FIELDS, format_ranking_rows(rankings))
    write_csv(
        analysis_dir / "ranking_reliable.csv",
        RANKING_FIELDS,
        format_ranking_rows(reliable, rerank=True),
    )
    write_csv(
        analysis_dir / "insufficient_evidence.csv",
        RANKING_FIELDS,
        format_ranking_rows(insufficient),
    )

    coverage_rows: list[dict[str, Any]] = []
    for context in ("overall", *CONTEXTS):
        context_rankings = [row for row in rankings if row["context"] == context]
        context_battles = (
            battles
            if context == "overall"
            else [row for row in battles if row["battle_context"] == context]
        )
        coverage_rows.append(
            {
                "context": context,
                "independent_battles": len(context_battles),
                "observed_labels": len(context_rankings),
                "deployed": sum(int(row["deployed"]) for row in context_rankings),
                "reliable_labels": sum(
                    row["reliability_status"] == "reliable" for row in context_rankings
                ),
                "insufficient_labels": sum(
                    row["reliability_status"] == "insufficient_evidence"
                    for row in context_rankings
                ),
                "minimum_battles": args.minimum_battles,
                "minimum_deployed": args.minimum_deployed,
            }
        )
    write_csv(
        analysis_dir / "context_coverage.csv",
        coverage_rows[0].keys(),
        coverage_rows,
    )

    input_verification = {
        "status": "passed_with_external_source_blocker" if external_blockers else "passed",
        "batch_id": args.batch_id,
        "schema_version": "1.1.0",
        "pipeline_mode": "offline-existing",
        "normalized_archive": {
            "name": args.archive_path.name,
            "expected_sha256": args.expected_archive_sha256,
            "actual_sha256": archive_hash,
            "passed": archive_ok,
            "safe_preflight": archive_preflight,
        },
        "source_archive": {
            "repository_path": str(args.source_path.relative_to(args.repo_root)),
            "expected_sha256": args.expected_source_sha256,
            "actual_sha256": source_hash,
            "repository_addressable": source_ok,
        },
        "manifest_checks": manifest_checks,
        "immutable_normalized_changes": immutable_changes,
        "frozen_model_changes": frozen_model_changes,
        "normalized_summary": normalized_summary,
        "external_blockers": external_blockers,
    }
    write_json(analysis_dir / "input_verification.json", input_verification)

    identity_counts = Counter(row["match_status"] for row in identities)
    coverage_by_context = {row["context"]: row for row in coverage_rows}
    validation = {
        "status": "passed_with_external_blocker" if external_blockers else "passed",
        "validation_errors": [],
        "external_blockers": external_blockers,
        "structural_validation": normalized_summary,
        "review": {
            "queued": len(review_queue),
            "decisions": len(review_decisions),
            "unresolved": sum(
                row["decision_status"].startswith("unresolved") for row in review_decisions
            ),
            "heroes_excluded_from_rankings": True,
        },
        "identity": {
            "labels": len(identities),
            "status_counts": dict(sorted(identity_counts.items())),
            "provisional_slugs_are_not_canonical_ids": True,
        },
        "ranking": {
            "minimum_battles": args.minimum_battles,
            "minimum_deployed": args.minimum_deployed,
            "bootstrap_repetitions": args.bootstrap_repetitions,
            "bootstrap_seed": "sha256(batch_id|context|provisional_slug|repetitions)",
            "complete_rows": len(rankings),
            "reliable_rows": len(reliable),
            "insufficient_rows": len(insufficient),
            "coverage_by_context": coverage_by_context,
        },
        "boundaries": {
            "track": args.track,
            "player_enemy_pooled": False,
            "contexts_pooled": False,
            "battle_is_independent_unit": True,
            "off_screen_rows_inferred": False,
            "frozen_models_changed": False,
        },
    }
    write_json(analysis_dir / "validation_report.json", validation)

    (analysis_dir / "COMPARISON_BLOCKED.md").write_text(
        "# Earlier-baseline comparison blocked\n\n"
        "No earlier batch was joined. The repository does not version an explicit "
        "same-track/schema compatibility decision for this 2026-07-27 normalized batch. "
        "Forcing a comparison would risk mixing extraction schemas or campaign conditions. "
        "The current outputs therefore remain a standalone descriptive batch.\n",
        encoding="utf-8",
    )

    top_overall = [
        row for row in reliable if row["context"] == "overall"
    ][:5]
    report_lines = [
        "# Phase 2 analysis — 2026-07-27 Realm of Thrones batch",
        "",
        "## Result",
        "",
        "The deterministic local analysis passed all structural, boundary, ranking, and "
        "hash checks. Merge remains blocked only because the exact original source ZIP is "
        "not repository-addressable.",
        "",
        "These rankings describe visible player-side campaign contribution. They are not a "
        "universal tier list, intrinsic-strength estimate, or causal equipment analysis.",
        "",
        "## Coverage",
        "",
        f"- {len(battles)} independent battles: "
        f"{normalized_summary['battle_context_counts'].get('field', 0)} field, "
        f"{normalized_summary['battle_context_counts'].get('siege_attack', 0)} siege attack, "
        f"{normalized_summary['battle_context_counts'].get('siege_defense', 0)} siege defense.",
        f"- {len(consolidated)} consolidated player-side ordinary-troop rows.",
        f"- {len(reliable)} reliable troop/context rows and {len(insufficient)} "
        "insufficient-evidence rows under the 5-battle / 20-deployed gate.",
        f"- {identity_counts.get('confirmed_id', 0)} of {len(identities)} display labels have "
        "a conservative exact canonical ID match.",
        f"- All {len(review_decisions)} queued hero icon fields remain unresolved and excluded.",
        "",
        "## Highest reliable overall descriptive rates",
        "",
        "| Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle bootstrap interval | Casualty rate |",
        "|---:|---|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(top_overall, start=1):
        report_lines.append(
            f"| {rank} | `{row['provisional_slug']}` | {row['independent_battles']} | "
            f"{row['deployed']} | {row['kills_per_deployed']:.3f} | "
            f"{row['ci95_low']:.3f}–{row['ci95_high']:.3f} | "
            f"{row['casualty_rate']:.3f} |"
        )
    report_lines.extend(
        [
            "",
            "Field has only four independent battles and siege defense only one, so neither "
            "context produces a reliable row. Siege attack reaches five battles and has "
            f"{coverage_by_context['siege_attack']['reliable_labels']} reliable rows.",
            "",
            "## Limitations",
            "",
            "- Victory-only, observational campaign data are confounded by army composition, "
            "difficulty, map, siege state, enemy composition, and player choices.",
            "- Only visible scoreboard rows are represented; off-screen rows are not inferred.",
            "- Canonical identity coverage is incomplete, so unresolved labels remain provisional.",
            "- The original screenshots cannot be re-reviewed until the exact source ZIP is restored.",
            "- No earlier baseline comparison or model recalibration was performed.",
        ]
    )
    (analysis_dir / "ANALYSIS_REPORT.md").write_text(
        "\n".join(report_lines) + "\n", encoding="utf-8"
    )
    (analysis_dir / "README.md").write_text(
        "# Phase 2 analytical outputs\n\n"
        "`ranking_complete.csv` contains every observed troop/context estimate. "
        "`ranking_reliable.csv` applies the 5-battle / 20-deployed gate. "
        "`insufficient_evidence.csv` retains all rows that fail the gate. "
        "`canonical_identity_audit.csv` never treats provisional slugs as XML IDs.\n\n"
        "Reproduce from the repository root:\n\n"
        "```bash\n"
        "batch='data/combat_observations/2026-07-27-normalized-only'\n"
        "work_dir=$(mktemp -d /tmp/bannerlord-analysis-20260727.XXXXXX)\n"
        "archive=\"$work_dir/bannerlord_combat_normalized_only_2026-07-27.tar.xz\"\n"
        "cat \"$batch\"/bundle/bannerlord_combat_normalized_only_2026-07-27.tar.xz.base64.part-* \\\n"
        "  | base64 --decode > \"$archive\"\n"
        "python3 - \"$archive\" <<'PY'\n"
        "import sys\n"
        "from pathlib import Path\n"
        "from scripts.analysis.analyze_normalized_combat_batch import safe_tar_preflight\n"
        "print(safe_tar_preflight(Path(sys.argv[1])))\n"
        "PY\n"
        "mkdir -p \"$work_dir/input\"\n"
        "tar -xJf \"$archive\" -C \"$work_dir/input\"\n"
        "python3 scripts/analysis/analyze_normalized_combat_batch.py \\\n"
        "  --input-dir \"$work_dir/input/bannerlord_combat_normalized_2026-07-27\" \\\n"
        "  --batch-dir \"$batch\" --repo-root . --identity-root data/rot_reference \\\n"
        "  --existing-identity-audit analysis/empirical/2026-07-23/canonical_identity_audit.csv \\\n"
        "  --normalization-commit 4e0749b84f5efc297ebcb026fa6dfbdaaed7fdf1 \\\n"
        "  --expected-archive-sha256 031a7c60d4ed239a2fcb70a81bb6edf047711c3a422ee3ba4420c4a4af534855 \\\n"
        "  --archive-path \"$archive\" \\\n"
        "  --expected-source-sha256 42d4adf2e8d9f9bce0dc90945832c673aeddf81d06044cb0e6f08a2ddb852617 \\\n"
        "  --source-path \"$PWD/$batch/source/original_screenshots.zip\" \\\n"
        "  --batch-id combat_2026-07-27_222843_010541 --track realm_of_thrones \\\n"
        "  --minimum-battles 5 --minimum-deployed 20 --bootstrap-repetitions 5000\n"
        "```\n",
        encoding="utf-8",
    )

    hashed_paths = [
        path
        for path in [*review_dir.iterdir(), *analysis_dir.iterdir()]
        if path.is_file() and path.name != "artifact_hashes.csv"
    ]
    write_csv(
        analysis_dir / "artifact_hashes.csv",
        ("file", "sha256", "size_bytes"),
        artifact_rows(args.batch_dir, hashed_paths),
    )

    print(
        json.dumps(
            {
                "status": validation["status"],
                "complete_rows": len(rankings),
                "reliable_rows": len(reliable),
                "insufficient_rows": len(insufficient),
                "identity_status_counts": dict(sorted(identity_counts.items())),
                "review_unresolved": len(review_decisions),
                "external_blockers": external_blockers,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
