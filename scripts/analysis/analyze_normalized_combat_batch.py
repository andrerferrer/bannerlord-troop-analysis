#!/usr/bin/env python3
"""Build a conservative Phase 2 analysis from a normalized combat batch."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import shlex
import subprocess
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    from scripts.analysis.build_canonical_identity_audit import (
        HISTORICAL_REPORTED_EXACT,
        normalize_display_name,
    )
    from scripts.combat_observations.bundle import inspect_tar
except ModuleNotFoundError:  # Direct script execution sets sys.path to scripts/analysis.
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from build_canonical_identity_audit import (
        HISTORICAL_REPORTED_EXACT,
        normalize_display_name,
    )
    from combat_observations.bundle import inspect_tar

CONTEXTS = ("field", "siege_attack", "siege_defense")
SUPPORTED_NORMALIZED_SCHEMA_VERSIONS = frozenset(("1.1.0", "2.0.0"))
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
    "evidence_kind",
    "evidence_paths",
    "candidate_count",
    "candidate_troop_ids",
    "blocking_reason",
)
REVIEW_FIELDS = (
    "observation_id",
    "battle_id",
    "source_image_file",
    "source_image_sha256",
    "field",
    "original_value",
    "reviewed_value",
    "decision_status",
    "reason",
    "reviewer",
    "evidence_reference",
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


def read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: invalid JSON: {error}") from error
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected an object")
    return value


def write_csv(path: Path, fields: Iterable[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        writer.writerows(
            {
                field: escape_spreadsheet_formula(value)
                for field, value in row.items()
            }
            for row in rows
        )


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


def escape_spreadsheet_formula(value: Any) -> Any:
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def safe_tar_preflight(archive_path: Path) -> dict[str, int]:
    members = inspect_tar(archive_path)
    regular_files = [member for member in members if member["type"] == "file"]
    return {
        "members": len(members),
        "regular_files": len(regular_files),
        "total_uncompressed_bytes": sum(int(member["size"]) for member in regular_files),
    }


def inspect_optional_source(
    source_path: Path,
    repo_root: Path,
    expected_sha256: str,
    expected_size_bytes: int,
    source_manifest: list[dict[str, str]] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    source_exists = source_path.is_file() or source_path.is_dir()
    source_is_symlink = source_path.is_symlink()
    errors: list[str] = []
    actual_sha256 = ""
    actual_size_bytes: int | None = None
    verification_method = "not_available"
    source_matches = False
    if source_path.is_file():
        actual_sha256 = sha256_file(source_path)
        actual_size_bytes = source_path.stat().st_size
        verification_method = "source_file_sha256_and_size"
        source_matches = (
            actual_sha256 == expected_sha256
            and actual_size_bytes == expected_size_bytes
        )
    elif source_path.is_dir() and not source_is_symlink:
        verification_method = "manifest_files_sha256_and_total_size"
        expected_files: dict[str, str] = {}
        manifest_safe = bool(source_manifest)
        for row in source_manifest or []:
            relative = str(row.get("image_file", ""))
            pure = PurePosixPath(relative)
            if (
                pure.is_absolute()
                or ".." in pure.parts
                or pure.as_posix() in {"", "."}
                or relative in expected_files
            ):
                manifest_safe = False
                break
            expected_files[relative] = str(row.get("image_sha256", ""))
        actual_files = {
            path.relative_to(source_path).as_posix(): path
            for path in source_path.rglob("*")
            if path.is_file() and not path.is_symlink()
        }
        contains_symlink = any(path.is_symlink() for path in source_path.rglob("*"))
        actual_size_bytes = sum(path.stat().st_size for path in actual_files.values())
        files_match = (
            manifest_safe
            and not contains_symlink
            and set(actual_files) == set(expected_files)
            and all(
                sha256_file(actual_files[relative]) == expected_hash
                for relative, expected_hash in expected_files.items()
            )
        )
        source_matches = files_match and actual_size_bytes == expected_size_bytes
    if source_exists and not source_matches:
        errors.append("retained raw source does not match its recorded hash and size")
    try:
        repository_path = str(source_path.relative_to(repo_root))
    except ValueError:
        repository_path = ""
    resolves_inside_repo = False
    if source_exists and not source_is_symlink:
        try:
            source_path.resolve(strict=True).relative_to(repo_root.resolve(strict=True))
            resolves_inside_repo = True
        except (FileNotFoundError, ValueError):
            pass
    tracked = False
    if repository_path and resolves_inside_repo:
        tracked = (
            subprocess.run(
                ["git", "ls-files", "--error-unmatch", "--", repository_path],
                cwd=repo_root,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            ).returncode
            == 0
        )
    repository_addressable = source_matches and resolves_inside_repo and tracked
    return (
        {
            "repository_path": repository_path,
            "retention_policy": "optional_after_verified_normalization",
            "retention_status": (
                "repository_verified"
                if repository_addressable
                else "locally_verified"
                if source_matches
                else "mismatch"
                if source_exists
                else "not_retained"
            ),
            "expected_sha256": expected_sha256,
            "actual_sha256": actual_sha256,
            "expected_size_bytes": expected_size_bytes,
            "actual_size_bytes": actual_size_bytes,
            "verification_method": verification_method,
            "locally_verified": source_matches,
            "repository_addressable": repository_addressable,
            "limits_visual_rereview": not source_matches,
        },
        errors,
    )


def verify_recorded_source_identity(
    expected_sha256: str,
    expected_size_bytes: int,
    normalization_summary: dict[str, Any],
    normalization_validation: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    def recorded_value(
        document: str,
        record: dict[str, Any],
        field_names: tuple[str, ...],
    ) -> tuple[str, Any]:
        for field_name in field_names:
            if field_name in record:
                return f"{document}:{field_name}", record[field_name]
        return f"{document}:{'|'.join(field_names)}", None

    recorded_values = (
        (*recorded_value(
            "normalization_summary.json",
            normalization_summary,
            ("source_sha256", "source_zip_sha256"),
        ), expected_sha256),
        (*recorded_value(
            "validation_report.json",
            normalization_validation,
            ("source_sha256", "source_zip_sha256"),
        ), expected_sha256),
        (*recorded_value(
            "validation_report.json",
            normalization_validation,
            ("source_size_bytes", "source_zip_size_bytes"),
        ), expected_size_bytes),
    )
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    for field, recorded, expected in recorded_values:
        passed = recorded == expected
        checks.append(
            {
                "field": field,
                "recorded": recorded,
                "expected": expected,
                "passed": passed,
            }
        )
        if not passed:
            errors.append(f"recorded source identity mismatch: {field}")
    return checks, errors


def verify_normalized_schema_version(
    normalization_summary: dict[str, Any],
    normalization_validation: dict[str, Any],
) -> tuple[str, list[str]]:
    summary_version = str(normalization_summary.get("schema_version", "")).strip()
    validation_version = str(normalization_validation.get("schema_version", "")).strip()
    if not summary_version or not validation_version:
        return "", ["normalized schema version missing"]
    if summary_version != validation_version:
        return "", ["normalized schema version mismatch"]
    if summary_version not in SUPPORTED_NORMALIZED_SCHEMA_VERSIONS:
        return "", [f"unsupported normalized schema version: {summary_version}"]
    return summary_version, []


def format_reproduction_path(path: Path, repo_root: Path) -> str:
    try:
        value = path.relative_to(repo_root).as_posix()
    except ValueError:
        value = str(path)
    return shlex.quote(value)


def verify_manifest(input_dir: Path, manifest_path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    base = input_dir.resolve(strict=True)
    rows = read_csv(manifest_path)
    manifest_files: set[str] = set()
    for row in rows:
        relative = row["file"]
        if relative in manifest_files:
            errors.append(f"duplicate artifact manifest path: {relative}")
        manifest_files.add(relative)
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or pure.as_posix() in {"", "."}:
            errors.append(f"unsafe artifact manifest path: {relative}")
            continue
        path = input_dir.joinpath(*pure.parts)
        lexical = input_dir
        traverses_symlink = False
        for part in pure.parts:
            lexical /= part
            if lexical.is_symlink():
                errors.append(f"artifact manifest path traverses symlink: {relative}")
                traverses_symlink = True
                break
        if traverses_symlink:
            continue
        try:
            resolved = path.resolve(strict=True)
            resolved.relative_to(base)
        except (FileNotFoundError, ValueError):
            errors.append(f"artifact manifest path escapes input directory: {relative}")
            continue
        path = resolved
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
    actual_files = {
        path.relative_to(input_dir).as_posix()
        for path in input_dir.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and path.relative_to(input_dir).as_posix() != "artifact_hashes.csv"
    }
    for relative in sorted(actual_files - manifest_files):
        errors.append(f"unlisted artifact file: {relative}")
    for relative in sorted(manifest_files - actual_files):
        if not any(error.endswith(relative) for error in errors):
            errors.append(f"manifest artifact file missing: {relative}")
    return checks, errors


def git_changed_paths(repo_root: Path, commit: str, paths: list[str]) -> list[str]:
    if not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
        raise ValueError("normalization commit must be a full 40-character hexadecimal SHA")
    commit_check = subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if commit_check.returncode:
        raise ValueError(f"normalization commit does not resolve to a commit: {commit}")
    result = subprocess.run(
        ["git", "diff", "--no-ext-diff", "--name-only", commit, "--", *paths],
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
    primary_groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in primary:
        observation_id = str(row.get("observation_id"))
        if observation_id in primary_ids:
            errors.append(f"duplicate primary observation: {observation_id}")
        primary_ids.add(observation_id)
        primary_key = (
            str(row.get("battle_id")),
            str(row.get("battle_context")),
            str(row.get("display_name_normalized")),
        )
        primary_groups[primary_key].append(row)
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
            if int(row["deployed"]) <= 0:
                errors.append(f"non-positive deployed count: {observation_id}")
            accounted = sum(int(row[field]) for field in ("survivors", "deaths", "wounded", "routed"))
            if accounted != int(row["deployed"]):
                errors.append(f"troop arithmetic mismatch: {observation_id}")

    consolidated_keys: set[tuple[str, str, str]] = set()
    consolidated_observation_ids: set[str] = set()
    consolidation_matches_primary = True
    for row in consolidated:
        key = (
            str(row.get("battle_id")),
            str(row.get("battle_context")),
            str(row.get("display_name_normalized")),
        )
        if key in consolidated_keys:
            errors.append(f"duplicate consolidated key: {'|'.join(key)}")
            consolidation_matches_primary = False
        consolidated_keys.add(key)
        primary_group = primary_groups.get(key)
        if primary_group is None:
            errors.append(f"consolidated key missing from primary rows: {'|'.join(key)}")
            consolidation_matches_primary = False
        else:
            expected_observation_ids = [
                str(item.get("observation_id")) for item in primary_group
            ]
            expected_raw_names = list(
                dict.fromkeys(str(item.get("display_name_raw")) for item in primary_group)
            )
            expected_tracks = {str(item.get("game_track")) for item in primary_group}
            if row.get("observation_ids") != expected_observation_ids:
                errors.append(
                    f"consolidated observation_ids mismatch: {'|'.join(key)}"
                )
                consolidation_matches_primary = False
            if row.get("display_names_raw") != expected_raw_names:
                errors.append(f"consolidated raw names mismatch: {'|'.join(key)}")
                consolidation_matches_primary = False
            if len(expected_tracks) != 1 or str(row.get("game_track")) not in expected_tracks:
                errors.append(f"consolidated track mismatch: {'|'.join(key)}")
                consolidation_matches_primary = False
            for field in COUNT_FIELDS:
                values = [item.get(field) for item in primary_group]
                if not all(isinstance(value, int) for value in values):
                    consolidation_matches_primary = False
                    continue
                expected_count = sum(int(value) for value in values)
                if row.get(field) != expected_count:
                    errors.append(f"consolidated {field} mismatch: {'|'.join(key)}")
                    consolidation_matches_primary = False
        if row.get("battle_context") not in CONTEXTS:
            errors.append(f"unknown consolidated context: {'|'.join(key)}")
        if row.get("needs_review"):
            errors.append(f"review-needed row entered consolidated input: {'|'.join(key)}")
        observation_ids = row.get("observation_ids")
        if not isinstance(observation_ids, list) or not observation_ids:
            errors.append(f"consolidated row has no observation_ids: {'|'.join(key)}")
        else:
            for raw_observation_id in observation_ids:
                observation_id = str(raw_observation_id)
                if observation_id in consolidated_observation_ids:
                    errors.append(
                        f"observation entered multiple consolidated rows: {observation_id}"
                    )
                consolidated_observation_ids.add(observation_id)
        for field in COUNT_FIELDS:
            if not isinstance(row.get(field), int) or int(row[field]) < 0:
                errors.append(f"invalid consolidated {field}: {'|'.join(key)}")
        if all(isinstance(row.get(field), int) for field in COUNT_FIELDS):
            if int(row["deployed"]) <= 0:
                errors.append(f"non-positive consolidated deployed count: {'|'.join(key)}")
            accounted = sum(int(row[field]) for field in ("survivors", "deaths", "wounded", "routed"))
            if accounted != int(row["deployed"]):
                errors.append(f"consolidated arithmetic mismatch: {'|'.join(key)}")

    for key in sorted(set(primary_groups) - consolidated_keys):
        errors.append(f"primary group missing from consolidated rows: {'|'.join(key)}")
        consolidation_matches_primary = False

    queued_ids = {str(row.get("observation_id", "")) for row in review_queue}
    for observation_id in sorted(consolidated_observation_ids - primary_ids):
        errors.append(f"non-primary observation entered consolidated rows: {observation_id}")
    for observation_id in sorted(primary_ids - consolidated_observation_ids):
        errors.append(f"primary observation missing from consolidated rows: {observation_id}")
    for observation_id in sorted(queued_ids & consolidated_observation_ids):
        errors.append(f"review item leaked into consolidated rows: {observation_id}")

    for queued in review_queue:
        observation_id = queued.get("observation_id", "")
        source = occurrence_by_id.get(observation_id)
        if not source:
            errors.append(f"review item missing source observation: {observation_id}")
            continue
        if not source.get("needs_review"):
            errors.append(f"review item source is not marked needs_review: {observation_id}")
        uncertain_fields = [
            field.strip()
            for field in queued.get("uncertain_fields", "").split("|")
            if field.strip()
        ]
        if not uncertain_fields:
            errors.append(f"review item has no uncertain fields: {observation_id}")
        for field in uncertain_fields:
            if field not in source:
                errors.append(f"review item names unknown field {field}: {observation_id}")
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
        "primary_rows_fully_consolidated": (
            consolidation_matches_primary
            and consolidated_observation_ids == primary_ids
        ),
        "queued_rows_excluded_from_rankings": not bool(
            queued_ids & consolidated_observation_ids
        ),
        "rankings_only_include_primary_troops": all(
            occurrence_by_id.get(observation_id, {}).get("row_type") == "troop"
            and observation_id in primary_ids
            for observation_id in consolidated_observation_ids
        ),
        "ordinary_troop_labels": len(
            {str(row.get("display_name_normalized")) for row in consolidated}
        ),
    }
    return errors, summary


def collect_identity_candidates(
    identity_root: Path,
    existing_audit: Path | None,
    repo_root: Path | None = None,
) -> dict[str, list[tuple[str, str, str]]]:
    def evidence_path(path: Path) -> str:
        if repo_root:
            try:
                return path.resolve().relative_to(repo_root.resolve()).as_posix()
            except ValueError:
                pass
        return str(path)

    candidates: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
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
                evidence_kind = (row.get("evidence_kind") or "versioned_track_reference").strip()
                candidate = (troop_id, evidence_path(path), evidence_kind)
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
                resolution_method = row.get("resolution_method") or ""
                evidence_kind = (
                    (row.get("evidence_kind") or "").strip()
                    or (
                        HISTORICAL_REPORTED_EXACT
                        if resolution_method.startswith("historical_pr_reported_exact")
                        else "versioned_track_reference"
                    )
                )
                candidate = (
                    row["canonical_troop_id"],
                    evidence_path(existing_audit),
                    evidence_kind,
                )
                key = normalize_display_name(name)
                if candidate not in candidates[key]:
                    candidates[key].append(candidate)
    return candidates


def build_identity_audit(
    consolidated: list[dict[str, Any]],
    candidates: dict[str, list[tuple[str, str] | tuple[str, str, str]]],
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
        ids = sorted({match[0] for match in matches})
        paths = sorted({match[1] for match in matches})
        evidence_kinds = {
            match[2] if len(match) > 2 else "versioned_track_reference"
            for match in matches
        }
        confirmed = len(ids) == 1
        historical_only = evidence_kinds == {HISTORICAL_REPORTED_EXACT}
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
                    (
                        "historical_pr_reported_exact_name_in_versioned_source"
                        if historical_only
                        else "exact_normalized_display_name_in_versioned_track_reference"
                    )
                    if confirmed
                    else ""
                ),
                "evidence_kind": (
                    HISTORICAL_REPORTED_EXACT
                    if confirmed and historical_only
                    else "versioned_track_reference"
                    if confirmed
                    else "|".join(sorted(evidence_kinds))
                    if len(ids) > 1
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
    for context in CONTEXTS:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in consolidated:
            if row["battle_context"] == context:
                groups[str(row["display_name_normalized"])].append(row)
        context_rows: list[dict[str, Any]] = []
        for slug, rows in groups.items():
            counts = {field: sum(int(row[field]) for row in rows) for field in COUNT_FIELDS}
            battles = len({str(row["battle_id"]) for row in rows})
            if counts["deployed"] <= 0:
                raise ValueError(f"non-positive deployed total for {context}|{slug}")
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


def build_focus_context_rows(
    rankings: list[dict[str, Any]],
    identities: list[dict[str, str]],
    focus_slugs: list[str],
    contexts: list[str],
) -> list[dict[str, Any]]:
    ranking_by_key = {
        (str(row["context"]), str(row["provisional_slug"])): row
        for row in rankings
    }
    identity_by_slug = {row["provisional_slug"]: row for row in identities}
    known_slugs = set(identity_by_slug) | {
        str(row["provisional_slug"]) for row in rankings
    }
    unknown_slugs = sorted(set(focus_slugs) - known_slugs)
    if unknown_slugs:
        raise ValueError(f"unknown focus slug: {', '.join(unknown_slugs)}")
    output: list[dict[str, Any]] = []
    for context in contexts:
        for slug in focus_slugs:
            observed = ranking_by_key.get((context, slug))
            if observed:
                output.append(dict(observed))
                continue
            identity = identity_by_slug.get(slug, {})
            output.append(
                {
                    "context": context,
                    "rank": "",
                    "display_name": identity.get("display_name", slug),
                    "provisional_slug": slug,
                    "canonical_troop_id": identity.get("canonical_troop_id", ""),
                    "identity_status": identity.get("match_status", "unresolved"),
                    "independent_battles": 0,
                    **{field: 0 for field in COUNT_FIELDS},
                    "kills_per_deployed": "",
                    "death_rate": "",
                    "casualty_rate": "",
                    "ci95_low": "",
                    "ci95_high": "",
                    "reliability_status": "not_observed",
                }
            )
    return output


def format_focus_rate(
    row: dict[str, Any],
    field: str,
    minimum_battles: int,
    minimum_deployed: int,
) -> str:
    if (
        int(row["independent_battles"]) < minimum_battles
        or int(row["deployed"]) < minimum_deployed
        or row[field] == ""
    ):
        return "—"
    return f"{float(row[field]):.3f}"


def build_review_decisions(
    review_queue: list[dict[str, str]],
    occurrences: list[dict[str, Any]],
    reviewer: str,
    raw_visual_review_available: bool,
) -> list[dict[str, str]]:
    occurrences_by_id = {str(row["observation_id"]): row for row in occurrences}
    output: list[dict[str, str]] = []
    for queued in review_queue:
        source = occurrences_by_id[queued["observation_id"]]
        for field in queued["uncertain_fields"].split("|"):
            field = field.strip()
            queue_note = queued.get("notes", "").strip()
            evidence_limit = (
                "The raw screenshot is locally verified, but no direct visual review "
                "decision is recorded; the normalized value remains unresolved and no "
                "replacement is inferred."
                if raw_visual_review_available
                else "The raw screenshot is not retained for visual re-review; the normalized "
                "value remains unresolved and no replacement is inferred."
            )
            output.append(
                {
                    "observation_id": queued["observation_id"],
                    "battle_id": queued["battle_id"],
                    "source_image_file": queued["source_image_file"],
                    "source_image_sha256": str(source["source_image_sha256"]),
                    "field": field,
                    "original_value": "" if source.get(field) is None else str(source[field]),
                    "reviewed_value": "",
                    "decision_status": (
                        "unresolved_pending_raw_image_review"
                        if raw_visual_review_available
                        else "unresolved_no_raw_image_review"
                    ),
                    "reason": f"{evidence_limit} Queue note: {queue_note}",
                    "reviewer": reviewer,
                    "evidence_reference": (
                        f"normalized occurrence {queued['observation_id']}; review_queue.csv; "
                        f"source SHA-256 {source['source_image_sha256']}"
                    ),
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
    parser.add_argument("--expected-source-size-bytes", type=int, required=True)
    parser.add_argument("--source-path", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--track", default="realm_of_thrones")
    parser.add_argument("--minimum-battles", type=int, default=5)
    parser.add_argument("--minimum-deployed", type=int, default=20)
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    parser.add_argument("--reviewer", default="Codex local analysis agent (GPT-5)")
    parser.add_argument("--focus-slug", action="append", default=[])
    args = parser.parse_args()

    args.repo_root = args.repo_root.resolve()
    args.input_dir = args.input_dir.resolve()
    args.batch_dir = args.batch_dir.resolve()
    args.identity_root = args.identity_root.resolve()
    args.archive_path = args.archive_path.resolve()
    args.source_path = args.source_path.resolve()
    if args.existing_identity_audit:
        args.existing_identity_audit = args.existing_identity_audit.resolve()
    analysis_dir = args.batch_dir / "analysis"
    review_dir = args.batch_dir / "review"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)

    archive_hash = sha256_file(args.archive_path)
    archive_ok = archive_hash == args.expected_archive_sha256
    if not archive_ok:
        raise ValueError("normalized archive hash mismatch")
    archive_preflight = safe_tar_preflight(args.archive_path)
    manifest_checks, manifest_errors = verify_manifest(
        args.input_dir, args.batch_dir / "artifact_hashes.csv"
    )
    if manifest_errors:
        raise ValueError("\n".join(manifest_errors))

    battles = read_jsonl(args.input_dir / "battles.jsonl")
    occurrences = read_jsonl(args.input_dir / "troop_occurrences.jsonl")
    primary = read_jsonl(args.input_dir / "primary_troop_occurrences.jsonl")
    consolidated = read_jsonl(args.input_dir / "troop_battle_consolidated.jsonl")
    screenshot_manifest = read_csv(args.input_dir / "screenshots_manifest.csv")
    review_queue = read_csv(args.input_dir / "review_queue.csv")
    recorded_normalization_summary = read_json_object(
        args.input_dir / "normalization_summary.json"
    )
    recorded_normalization_validation = read_json_object(
        args.input_dir / "validation_report.json"
    )
    normalized_schema_version, schema_version_errors = verify_normalized_schema_version(
        recorded_normalization_summary,
        recorded_normalization_validation,
    )
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
            "README.md",
            "review_queue.csv",
            "bundle",
            "source/README.md",
            "handoff/ANALYSIS_PROMPT.md",
        )
    ]
    immutable_changes = git_changed_paths(
        args.repo_root, args.normalization_commit, immutable_paths
    )
    frozen_model_changes = git_changed_paths(
        args.repo_root, args.normalization_commit, ["analysis/model_versions"]
    )

    source_archive, source_errors = inspect_optional_source(
        args.source_path,
        args.repo_root,
        args.expected_source_sha256,
        args.expected_source_size_bytes,
        screenshot_manifest,
    )
    source_provenance_checks, source_provenance_errors = verify_recorded_source_identity(
        args.expected_source_sha256,
        args.expected_source_size_bytes,
        recorded_normalization_summary,
        recorded_normalization_validation,
    )
    external_blockers: list[dict[str, Any]] = []

    validation_errors = [
        *manifest_errors,
        *structural_errors,
        *source_errors,
        *source_provenance_errors,
        *schema_version_errors,
        *[f"immutable normalized input changed: {path}" for path in immutable_changes],
        *[f"frozen model changed: {path}" for path in frozen_model_changes],
    ]
    if validation_errors:
        raise ValueError("\n".join(validation_errors))

    candidates = collect_identity_candidates(
        args.identity_root,
        args.existing_identity_audit,
        args.repo_root,
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
    raw_visual_review_available = bool(source_archive["locally_verified"])
    review_decisions = build_review_decisions(
        review_queue,
        occurrences,
        args.reviewer,
        raw_visual_review_available,
    )
    observed_contexts = [
        context
        for context in CONTEXTS
        if any(row["battle_context"] == context for row in battles)
    ]
    focus_rows = build_focus_context_rows(
        rankings,
        identities,
        args.focus_slug,
        observed_contexts,
    )
    reproduction_identity_root = format_reproduction_path(
        args.identity_root, args.repo_root
    )
    reproduction_existing_audit = (
        format_reproduction_path(args.existing_identity_audit, args.repo_root)
        if args.existing_identity_audit
        else ""
    )
    reproduction_source_path = format_reproduction_path(
        args.source_path, args.repo_root
    )

    write_csv(review_dir / "review_decisions.csv", REVIEW_FIELDS, review_decisions)
    raw_review_sentence = (
        "Raw screenshots are locally verified but no direct visual review decision is "
        "recorded, so the reviewed layer preserves null values."
        if raw_visual_review_available
        else "Raw screenshots are not retained for visual re-review, so the reviewed layer "
        "preserves null values."
    )
    (review_dir / "README.md").write_text(
        "# Phase 2 review decisions\n\n"
        f"The {len(review_queue)} queued rows expand to {len(review_decisions)} field-level "
        f"decisions, and all remain unresolved. {raw_review_sentence} The analysis does not "
        "infer numeric counts. Every queued row remains outside the ordinary-troop primary "
        "input, so this is a documented limitation rather than a merge blocker.\n",
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

    if focus_rows:
        write_csv(
            analysis_dir / "focus_troop_contexts.csv",
            RANKING_FIELDS,
            format_ranking_rows(focus_rows),
        )
    else:
        (analysis_dir / "focus_troop_contexts.csv").unlink(missing_ok=True)

    coverage_rows: list[dict[str, Any]] = []
    for context in CONTEXTS:
        context_rankings = [row for row in rankings if row["context"] == context]
        context_battles = [row for row in battles if row["battle_context"] == context]
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
        "status": "passed",
        "batch_id": args.batch_id,
        "schema_version": normalized_schema_version,
        "pipeline_mode": "offline-existing",
        "normalized_archive": {
            "name": args.archive_path.name,
            "expected_sha256": args.expected_archive_sha256,
            "actual_sha256": archive_hash,
            "passed": archive_ok,
            "safe_preflight": archive_preflight,
        },
        "source_archive": source_archive,
        "source_provenance_checks": source_provenance_checks,
        "manifest_checks": manifest_checks,
        "immutable_normalized_changes": immutable_changes,
        "frozen_model_changes": frozen_model_changes,
        "normalized_summary": normalized_summary,
        "external_blockers": external_blockers,
    }
    write_json(analysis_dir / "input_verification.json", input_verification)

    identity_counts = Counter(row["match_status"] for row in identities)
    unresolved_identity_names = [
        row["display_name"]
        for row in identities
        if row["match_status"] != "confirmed_id"
    ]
    coverage_by_context = {row["context"]: row for row in coverage_rows}
    validation = {
        "status": "passed",
        "validation_errors": [],
        "external_blockers": external_blockers,
        "structural_validation": normalized_summary,
        "review": {
            "queued": len(review_queue),
            "decisions": len(review_decisions),
            "unresolved": sum(
                row["decision_status"].startswith("unresolved") for row in review_decisions
            ),
            "heroes_excluded_from_rankings": normalized_summary[
                "rankings_only_include_primary_troops"
            ],
            "queued_rows_excluded_from_rankings": normalized_summary[
                "queued_rows_excluded_from_rankings"
            ],
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
        f"No earlier batch was joined to `{args.batch_id}`. The repository does not version "
        f"an explicit same-track/schema compatibility decision for this {args.track} batch. "
        "Forcing a comparison would risk mixing extraction schemas or campaign conditions. "
        "The current outputs therefore remain a standalone descriptive batch.\n",
        encoding="utf-8",
    )

    report_lines = [
        f"# Phase 2 analysis — {args.batch_id}",
        "",
        "## Result",
        "",
        "The deterministic local analysis passed all structural, boundary, ranking, and "
        "hash checks. The repository-reconstructible normalized archive is the authoritative "
        "downstream input; raw screenshot retention is optional.",
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
        "- Unresolved canonical labels: "
        + (", ".join(unresolved_identity_names) if unresolved_identity_names else "none")
        + ".",
        f"- All {len(review_decisions)} queued fields remain unresolved; their source rows "
        "remain excluded from ordinary-troop rankings.",
        "",
        "## Reliable descriptive rates",
        "",
    ]
    if reliable:
        report_lines.extend(
            [
                "| Context | Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle bootstrap interval | Casualty rate |",
                "|---|---:|---|---:|---:|---:|---:|---:|",
            ]
        )
        for context in observed_contexts:
            for rank, row in enumerate(
                [item for item in reliable if item["context"] == context][:5],
                start=1,
            ):
                report_lines.append(
                    f"| {context} | {rank} | `{row['provisional_slug']}` | "
                    f"{row['independent_battles']} | {row['deployed']} | "
                    f"{row['kills_per_deployed']:.3f} | "
                    f"{row['ci95_low']:.3f}–{row['ci95_high']:.3f} | "
                    f"{row['casualty_rate']:.3f} |"
                )
    else:
        report_lines.append(
            "No troop/context row reaches the 5-independent-battle / 20-deployed display "
            "gate, so no reliable ranking or bootstrap interval is displayed."
        )
    if focus_rows:
        report_lines.extend(
            [
                "",
                "## Requested Sarnori family by context",
                "",
                "| Context | Troop | Canonical ID | Battles | Deployed | Kills/deployed | Casualty rate | Evidence gate |",
                "|---|---|---|---:|---:|---:|---:|---|",
            ]
        )
        for row in focus_rows:
            kills_per_deployed = format_focus_rate(
                row,
                "kills_per_deployed",
                args.minimum_battles,
                args.minimum_deployed,
            )
            casualty_rate = format_focus_rate(
                row,
                "casualty_rate",
                args.minimum_battles,
                args.minimum_deployed,
            )
            report_lines.append(
                f"| {row['context']} | {row['display_name']} | "
                f"`{row['canonical_troop_id'] or 'unresolved'}` | "
                f"{row['independent_battles']} | {row['deployed']} | "
                f"{kills_per_deployed} | {casualty_rate} | "
                f"{row['reliability_status']} |"
            )
    report_lines.extend(
        [
            "",
            "Each observed context has at most "
            f"{max(row['independent_battles'] for row in coverage_rows)} independent battles. "
            "Contexts are never pooled to manufacture an overall display gate. Complete rates "
            "remain diagnostics only and do not support the provisional S-tier conclusion.",
            "",
            "## Limitations",
            "",
            "- Victory-only, observational campaign data are confounded by army composition, "
            "difficulty, map, siege state, enemy composition, and player choices.",
            "- Only visible scoreboard rows are represented; off-screen rows are not inferred.",
            "- Canonical identity coverage is incomplete, so unresolved labels remain provisional.",
            (
                f"- The original screenshots are locally verified but {len(review_decisions)} "
                "queued fields have no direct review decision and remain unresolved; queued "
                "rows are excluded from rankings."
                if raw_visual_review_available
                else f"- The original screenshots are not retained, so {len(review_decisions)} "
                "queued fields cannot be re-reviewed and remain unresolved; queued rows are "
                "excluded from rankings."
            ),
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
        "The batch-level `../README.md` is git-frozen at the normalization commit as Phase 1 "
        "metadata. This directory records Phase 2 outputs; authoritative workflow state lives "
        "in append-only protocol comments.\n\n"
        + (
            "`focus_troop_contexts.csv` records each requested focus troop separately for "
            "every observed context, including explicit `not_observed` rows. Machine-readable "
            "diagnostic rates remain available with their evidence status; the report masks "
            "rates unless the full display gate passes.\n\n"
            if focus_rows
            else ""
        )
        + "Reproduce from the repository root:\n\n"
        "```bash\n"
        f"batch='{args.batch_dir.relative_to(args.repo_root)}'\n"
        "work_dir=$(mktemp -d /tmp/bannerlord-analysis.XXXXXX)\n"
        f"archive=\"$work_dir/{args.archive_path.name}\"\n"
        f"cat \"$batch\"/bundle/{args.archive_path.name}.base64.part-* \\\n"
        "  | base64 --decode > \"$archive\"\n"
        "python3 - \"$archive\" \"$work_dir/input\" <<'PY'\n"
        "import hashlib\n"
        "import sys\n"
        "from pathlib import Path\n"
        "from scripts.combat_observations.bundle import inspect_tar, safe_extract_tar\n"
        "archive = Path(sys.argv[1])\n"
        f"expected = '{args.expected_archive_sha256}'\n"
        "actual = hashlib.sha256(archive.read_bytes()).hexdigest()\n"
        "if actual != expected:\n"
        "    raise SystemExit(f'archive SHA-256 mismatch: {actual} != {expected}')\n"
        "print(inspect_tar(archive))\n"
        "safe_extract_tar(archive, Path(sys.argv[2]))\n"
        "PY\n"
        "python3 scripts/analysis/analyze_normalized_combat_batch.py \\\n"
        f"  --input-dir \"$work_dir/input/{args.input_dir.name}\" \\\n"
        f"  --batch-dir \"$batch\" --repo-root . --identity-root {reproduction_identity_root} \\\n"
        + (
            f"  --existing-identity-audit {reproduction_existing_audit} \\\n"
            if args.existing_identity_audit
            else ""
        )
        + f"  --normalization-commit {args.normalization_commit} \\\n"
        f"  --expected-archive-sha256 {args.expected_archive_sha256} \\\n"
        "  --archive-path \"$archive\" \\\n"
        f"  --expected-source-sha256 {args.expected_source_sha256} \\\n"
        f"  --expected-source-size-bytes {args.expected_source_size_bytes} \\\n"
        f"  --source-path {reproduction_source_path} \\\n"
        f"  --batch-id {args.batch_id} --track {args.track} \\\n"
        f"  --minimum-battles {args.minimum_battles} --minimum-deployed {args.minimum_deployed} \\\n"
        f"  --bootstrap-repetitions {args.bootstrap_repetitions} \\\n"
        f"  --reviewer {shlex.quote(args.reviewer)}"
        + "".join(
            f" \\\n  --focus-slug {shlex.quote(slug)}" for slug in args.focus_slug
        )
        + "\n"
        + "```\n",
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
