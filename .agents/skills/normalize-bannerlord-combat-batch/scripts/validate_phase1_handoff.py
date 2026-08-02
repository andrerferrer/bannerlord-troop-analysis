#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import binascii
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
import unicodedata
from pathlib import Path, PurePosixPath


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
MAX_BUNDLE_PARTS = 10_000
MAX_BASE64_BYTES = 512 * 1024 * 1024
MAX_TAR_MEMBERS = 10_000
MAX_TAR_UNCOMPRESSED_BYTES = 1_000_000_000
REQUIRED_BATCH_FILES = (
    "README.md",
    "screenshots_manifest.csv",
    "normalization_summary.json",
    "review_queue.csv",
    "validation_report.json",
    "artifact_hashes.csv",
    "source/README.md",
    "bundle/README.md",
    "handoff/ANALYSIS_PROMPT.md",
    "handoff/ANALYSIS_TASK_V1.json",
)
REQUIRED_ARCHIVE_FILES = (
    "README.md",
    "screenshots_manifest.csv",
    "battles.jsonl",
    "troop_occurrences.jsonl",
    "primary_troop_occurrences.jsonl",
    "troop_battle_consolidated.jsonl",
    "review_queue.csv",
    "normalization_summary.json",
    "validation_report.json",
    "artifact_hashes.csv",
)
REQUIRED_ACTIONS = {
    "verify_handoff_hashes",
    "preserve_normalized_inputs",
    "complete_review_layer",
    "resolve_canonical_identities",
    "confirm_frozen_models_unchanged",
    "validate_and_merge",
}
ANALYSIS_ACTION_ALIASES = {
    "generate_analysis_outputs",
    "generate_reliable_and_complete_rankings",
}
FORBIDDEN_ARCHIVE_NAMES = {
    "canonical_identity_audit.csv",
    "historical_troop_aggregates.jsonl",
    "model_comparison.csv",
    "ranking_complete.csv",
    "ranking_reliable.csv",
}
OPTIONAL_ARCHIVE_FILES = {
    "screenshots.jsonl",
    "combat_troop_occurrence.schema.json",
}
PHASE1_ARCHIVE_DIRECTORIES = {"extraction", "provenance", "schemas"}
SOURCE_SUFFIXES = {".zip", ".7z", ".tar", ".xz", ".gz", ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff", ".sha256"}
CONTEXTS = {"field", "siege_attack", "siege_defense"}
SIDES = {"attacker", "defender"}
COUNT_FIELDS = ("deployed", "survivors", "kills", "deaths", "wounded", "routed")
MIRRORED_ARCHIVE_FILES = (
    "screenshots_manifest.csv",
    "normalization_summary.json",
    "review_queue.csv",
    "validation_report.json",
    "artifact_hashes.csv",
)


class HandoffError(RuntimeError):
    pass


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise HandoffError(message)


def load_json(path: Path) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise HandoffError(f"invalid JSON {path}: {error}") from error
    require(isinstance(value, dict), f"JSON root must be an object: {path}")
    return value


def git(repo: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    if check and completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise HandoffError(f"git {' '.join(arguments)} failed: {detail}")
    return completed


def ordered_bundle_parts(bundle_dir: Path) -> list[Path]:
    parts = sorted(bundle_dir.glob("*.base64.part-*"))
    require(parts, f"no Base64 bundle parts found in {bundle_dir}")
    require(len(parts) <= MAX_BUNDLE_PARTS, f"bundle part count exceeds limit: {len(parts)}")
    prefixes: set[str] = set()
    indexes: list[int] = []
    for part in parts:
        match = re.fullmatch(r"(.+\.base64\.part-)(\d+)", part.name)
        require(match is not None, f"invalid bundle part name: {part.name}")
        prefixes.add(match.group(1))
        indexes.append(int(match.group(2)))
    require(len(prefixes) == 1, "bundle parts use more than one filename prefix")
    require(indexes == list(range(len(parts))), f"bundle part indexes are not contiguous: {indexes}")
    return parts


def decode_archive(parts: list[Path]) -> bytes:
    encoded_size = sum(part.stat().st_size for part in parts)
    require(encoded_size <= MAX_BASE64_BYTES, f"Base64 bundle exceeds size limit: {encoded_size}")
    encoded = b"".join(b"".join(part.read_bytes().split()) for part in parts)
    try:
        return base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as error:
        raise HandoffError(f"invalid Base64 bundle: {error}") from error


def archive_files(archive: bytes) -> dict[str, bytes]:
    result: dict[str, bytes] = {}
    roots: set[str] = set()
    collision_names: set[str] = set()
    total_uncompressed = 0
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as handle:
            for member_count, member in enumerate(handle, start=1):
                require(member_count <= MAX_TAR_MEMBERS, f"archive member count exceeds limit: {member_count}")
                path = PurePosixPath(member.name)
                require(not path.is_absolute() and ".." not in path.parts, f"unsafe archive path: {member.name}")
                require(not (member.issym() or member.islnk() or member.isdev()), f"unsafe archive member: {member.name}")
                collision_name = unicodedata.normalize("NFC", path.as_posix()).casefold()
                require(collision_name not in collision_names, f"canonical archive path collision: {member.name}")
                collision_names.add(collision_name)
                if not path.parts:
                    continue
                roots.add(path.parts[0])
                if member.isdir():
                    continue
                require(member.isfile(), f"unsupported archive member: {member.name}")
                total_uncompressed += member.size
                require(
                    total_uncompressed <= MAX_TAR_UNCOMPRESSED_BYTES,
                    f"archive uncompressed size exceeds limit: {total_uncompressed}",
                )
                relative = PurePosixPath(*path.parts[1:]).as_posix()
                require(relative and relative not in result, f"duplicate archive member: {relative}")
                extracted = handle.extractfile(member)
                require(extracted is not None, f"cannot read archive member: {member.name}")
                result[relative] = extracted.read()
    except (tarfile.TarError, OSError) as error:
        raise HandoffError(f"invalid normalized tar.xz archive: {error}") from error
    require(len(roots) == 1, f"archive must contain one top-level directory, found {sorted(roots)}")
    allowed_exact = set(REQUIRED_ARCHIVE_FILES).union(OPTIONAL_ARCHIVE_FILES)
    phase2_named = sorted(
        path for path in result
        if PurePosixPath(path).name in FORBIDDEN_ARCHIVE_NAMES
        or PurePosixPath(path).name.startswith("ranking_")
    )
    require(not phase2_named, f"Phase 2 artifacts are forbidden in the normalized archive: {phase2_named}")
    forbidden = sorted(
        path for path in result
        if path not in allowed_exact
        and PurePosixPath(path).parts[0] not in PHASE1_ARCHIVE_DIRECTORIES
        and not is_allowed_source_path(PurePosixPath(path))
    )
    require(not forbidden, f"non-Phase-1 artifacts are forbidden in the normalized archive: {forbidden}")
    return result


def is_allowed_source_path(path: PurePosixPath) -> bool:
    return (
        bool(path.parts)
        and path.parts[0] == "source"
        and (
            path.suffix.casefold() in SOURCE_SUFFIXES
            or re.fullmatch(r".+\.base64\.part-\d+", path.name) is not None
        )
    )


def validate_manifest(manifest_bytes: bytes, files: dict[str, bytes]) -> int:
    try:
        rows = list(csv.DictReader(io.StringIO(manifest_bytes.decode("utf-8"))))
    except (UnicodeDecodeError, csv.Error) as error:
        raise HandoffError(f"invalid artifact_hashes.csv: {error}") from error
    require(rows, "artifact_hashes.csv is empty")
    seen: set[str] = set()
    for row in rows:
        path = row.get("file", "")
        expected_hash = row.get("sha256", "")
        expected_size = row.get("size_bytes", "")
        require(path in files, f"artifact manifest entry is absent from archive: {path}")
        require(path != "artifact_hashes.csv", "artifact manifest must not hash itself")
        require(path not in seen, f"duplicate artifact manifest entry: {path}")
        seen.add(path)
        require(SHA256_RE.fullmatch(expected_hash) is not None, f"invalid SHA-256 for {path}")
        try:
            size = int(expected_size)
        except ValueError as error:
            raise HandoffError(f"invalid size for {path}: {expected_size}") from error
        require(size == len(files[path]), f"artifact size mismatch for {path}")
        require(expected_hash == sha256_bytes(files[path]), f"artifact SHA-256 mismatch for {path}")
    expected = set(files).difference({"artifact_hashes.csv"})
    require(seen == expected, f"artifact manifest coverage mismatch: missing={sorted(expected - seen)}, extra={sorted(seen - expected)}")
    return len(rows)


def load_archive_json(files: dict[str, bytes], path: str) -> dict[str, object]:
    try:
        value = json.loads(files[path].decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise HandoffError(f"invalid archive JSON {path}: {error}") from error
    require(isinstance(value, dict), f"archive JSON root must be an object: {path}")
    return value


def load_archive_jsonl(
    files: dict[str, bytes],
    path: str,
    identity_key: str | None,
) -> list[dict[str, object]]:
    try:
        text = files[path].decode("utf-8")
    except UnicodeDecodeError as error:
        raise HandoffError(f"invalid archive JSONL encoding {path}: {error}") from error
    records: list[dict[str, object]] = []
    identities: set[str] = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        require(bool(line.strip()), f"blank JSONL line in {path}:{line_number}")
        try:
            record = json.loads(line)
        except ValueError as error:
            raise HandoffError(f"invalid archive JSONL {path}:{line_number}: {error}") from error
        require(isinstance(record, dict), f"JSONL record must be an object: {path}:{line_number}")
        if identity_key is not None:
            identity = record.get(identity_key)
            require(isinstance(identity, str) and bool(identity), f"{path}:{line_number} lacks {identity_key}")
            require(identity not in identities, f"duplicate {identity_key} in {path}: {identity}")
            identities.add(identity)
        records.append(record)
    return records


def load_archive_csv(files: dict[str, bytes], path: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        reader = csv.DictReader(io.StringIO(files[path].decode("utf-8")))
        rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as error:
        raise HandoffError(f"invalid archive CSV {path}: {error}") from error
    fields = reader.fieldnames or []
    require(bool(fields), f"archive CSV lacks a header: {path}")
    return fields, rows


def validate_source_identity(summary: dict[str, object], report: dict[str, object], task: dict[str, object]) -> None:
    summary_hashes = {
        value for key in ("source_sha256", "source_zip_sha256")
        if isinstance((value := summary.get(key)), str)
    }
    require(len(summary_hashes) == 1, "normalization_summary.json lacks one unambiguous source SHA-256")
    source_hash = summary_hashes.pop()
    require(SHA256_RE.fullmatch(source_hash) is not None, "normalization_summary.json source SHA-256 is invalid")
    report_hashes = {
        value for key in ("source_sha256", "source_zip_sha256")
        if isinstance((value := report.get(key)), str)
    }
    require(report_hashes == {source_hash}, "validation_report.json source hash differs from normalization summary")
    source_sizes = {
        value for key in ("source_size_bytes", "source_zip_size_bytes")
        if isinstance((value := report.get(key)), int) and not isinstance(value, bool)
    }
    require(len(source_sizes) == 1 and next(iter(source_sizes)) > 0, "validation_report.json lacks one positive source size")
    require(task.get("source_sha256") == source_hash, "analysis task source_sha256 differs from normalized evidence")
    require(report.get("status") == "passed", "Phase 1 validation_report.json status is not passed")
    errors = report.get("validation_errors")
    require(isinstance(errors, list) and not errors, "Phase 1 validation_report.json contains errors")


def validate_counts(files: dict[str, bytes], summary: dict[str, object], report: dict[str, object]) -> None:
    screenshot_fields, screenshots = load_archive_csv(files, "screenshots_manifest.csv")
    require({"image_file", "image_sha256"}.issubset(screenshot_fields), "screenshots_manifest.csv lacks identity/hash columns")
    screenshot_names: set[str] = set()
    for row in screenshots:
        name = row.get("image_file", "")
        digest = row.get("image_sha256", "")
        require(bool(name) and name not in screenshot_names, f"invalid or duplicate screenshot manifest row: {name!r}")
        require(SHA256_RE.fullmatch(digest) is not None, f"invalid screenshot SHA-256: {name}")
        screenshot_names.add(name)

    battles = load_archive_jsonl(files, "battles.jsonl", "battle_id")
    observations = load_archive_jsonl(files, "troop_occurrences.jsonl", "observation_id")
    primary = load_archive_jsonl(files, "primary_troop_occurrences.jsonl", "observation_id")
    consolidated = load_archive_jsonl(files, "troop_battle_consolidated.jsonl", None)
    _, review_queue = load_archive_csv(files, "review_queue.csv")
    battle_by_id = {str(row["battle_id"]): row for row in battles}
    occurrence_by_id = {str(row["observation_id"]): row for row in observations}
    image_hashes = {row["image_sha256"] for row in screenshots}
    game_track = summary.get("game_track")
    game_version = summary.get("game_version")
    require(isinstance(game_track, str) and bool(game_track), "normalization_summary.json lacks game_track")
    require(isinstance(game_version, str) and bool(game_version), "normalization_summary.json lacks game_version")
    for battle_id, battle in battle_by_id.items():
        require(battle.get("battle_context") in CONTEXTS, f"unknown battle context: {battle_id}")
        require(battle.get("player_side") in SIDES, f"invalid player side: {battle_id}")
        require(battle.get("game_track") == game_track, f"mixed or missing game track: {battle_id}")
        require(battle.get("game_version") == game_version, f"mixed or missing game version: {battle_id}")
    for observation_id, row in occurrence_by_id.items():
        battle = battle_by_id.get(str(row.get("battle_id")))
        require(battle is not None, f"occurrence has unknown battle: {observation_id}")
        require(row.get("battle_context") == battle.get("battle_context"), f"occurrence context mismatch: {observation_id}")
        require(row.get("side") in SIDES, f"invalid occurrence side: {observation_id}")
        require(row.get("source_image_sha256") in image_hashes, f"unknown source image hash: {observation_id}")
    primary_ids: set[str] = set()
    for row in primary:
        observation_id = str(row["observation_id"])
        primary_ids.add(observation_id)
        source = occurrence_by_id.get(observation_id)
        require(source is not None, f"primary row is absent from troop_occurrences.jsonl: {observation_id}")
        require(row == source, f"primary row differs from source occurrence: {observation_id}")
        battle = battle_by_id.get(str(row.get("battle_id")))
        require(battle is not None, f"primary row has unknown battle: {observation_id}")
        require(row.get("row_type") == "troop", f"non-troop row entered primary input: {observation_id}")
        require(row.get("analysis_status") == "included_primary", f"non-primary status entered primary input: {observation_id}")
        require(not row.get("needs_review"), f"review-needed row entered primary input: {observation_id}")
        require(row.get("side") == battle.get("player_side"), f"player/enemy side boundary violation: {observation_id}")
        require(row.get("battle_context") == battle.get("battle_context"), f"battle context mismatch: {observation_id}")
        require(row.get("source_image_sha256") in image_hashes, f"unknown source image hash: {observation_id}")
        validate_count_fields(row, f"primary row {observation_id}")

    consolidated_keys: set[tuple[str, str, str]] = set()
    derived: dict[tuple[str, str, str], dict[str, int]] = {}
    for row in primary:
        key = (
            str(row.get("battle_id")),
            str(row.get("battle_context")),
            str(row.get("display_name_normalized")),
        )
        require(bool(key[2]) and key[2] != "None", f"primary row lacks normalized display name: {row['observation_id']}")
        totals = derived.setdefault(key, {field: 0 for field in COUNT_FIELDS})
        for field in COUNT_FIELDS:
            totals[field] += int(row[field])
    for row in consolidated:
        key = (
            str(row.get("battle_id")),
            str(row.get("battle_context")),
            str(row.get("display_name_normalized")),
        )
        require(key not in consolidated_keys, f"duplicate consolidated key: {'|'.join(key)}")
        consolidated_keys.add(key)
        battle = battle_by_id.get(key[0])
        require(battle is not None, f"consolidated row has unknown battle: {'|'.join(key)}")
        require(key[1] in CONTEXTS, f"unknown consolidated context: {'|'.join(key)}")
        require(key[1] == battle.get("battle_context"), f"consolidated context mismatch: {'|'.join(key)}")
        require(not row.get("needs_review"), f"review-needed row entered consolidated input: {'|'.join(key)}")
        validate_count_fields(row, f"consolidated row {'|'.join(key)}")
        require(key in derived, f"consolidated row has no primary source: {'|'.join(key)}")
        for field in COUNT_FIELDS:
            require(row.get(field) == derived[key][field], f"consolidated {field} differs from primary rows: {'|'.join(key)}")
    require(consolidated_keys == set(derived), "consolidated rows do not exactly cover primary troop groups")

    for queued in review_queue:
        observation_id = queued.get("observation_id", "")
        require(observation_id in occurrence_by_id, f"review item lacks source observation: {observation_id}")
        require(observation_id not in primary_ids, f"review item leaked into primary rows: {observation_id}")
    actual_counts = {
        "screenshots": len(screenshots),
        "battles": len(battles),
        "observations": len(observations),
        "primary_troop_occurrences": len(primary),
        "review_queue": len(review_queue),
    }
    report_keys = {
        "screenshots": "image_count",
        "battles": "battle_count",
        "observations": "observation_count",
        "primary_troop_occurrences": "primary_troop_occurrences",
        "review_queue": "review_queue_count",
    }
    for summary_key, actual in actual_counts.items():
        report_key = report_keys[summary_key]
        require(summary_key in summary, f"normalization_summary.json lacks {summary_key}")
        require(report_key in report, f"validation_report.json lacks {report_key}")
        require(
            isinstance(summary[summary_key], int) and not isinstance(summary[summary_key], bool) and summary[summary_key] >= 0,
            f"normalization_summary.json {summary_key} must be a non-negative integer",
        )
        require(
            isinstance(report[report_key], int) and not isinstance(report[report_key], bool) and report[report_key] >= 0,
            f"validation_report.json {report_key} must be a non-negative integer",
        )
        require(summary[summary_key] == report[report_key], f"count mismatch: {summary_key} != {report_key}")
        require(summary[summary_key] == actual, f"declared count differs from archive records: {summary_key}")


def validate_count_fields(row: dict[str, object], label: str) -> None:
    for field in COUNT_FIELDS:
        value = row.get(field)
        require(isinstance(value, int) and not isinstance(value, bool) and value >= 0, f"invalid {field}: {label}")
    require(int(row["deployed"]) > 0, f"non-positive deployed count: {label}")
    accounted = sum(int(row[field]) for field in ("survivors", "deaths", "wounded"))
    require(accounted == int(row["deployed"]), f"troop arithmetic mismatch: {label}")


def validate_task(
    task: dict[str, object],
    *,
    branch: str,
    normalization_commit: str,
    expected_handoff_path: str,
    archive_sha256: str,
) -> None:
    require(task.get("protocol") == "bannerlord-analysis-task", "invalid analysis task protocol")
    require(task.get("version") == 1, "analysis task version must be 1")
    require(task.get("status") == "pending", "Phase 1 task mirror must have status pending")
    require(task.get("branch") == branch, "analysis task branch differs from the requested branch")
    require(task.get("handoff_path") == expected_handoff_path, "analysis task handoff_path is incorrect")
    require(task.get("normalization_commit") == normalization_commit, "analysis task normalization_commit is incorrect")
    require(task.get("normalized_archive_sha256") == archive_sha256, "analysis task normalized archive hash is incorrect")
    require(isinstance(task.get("task_id"), str) and bool(task["task_id"]), "analysis task lacks task_id")
    actions = task.get("required_actions")
    require(isinstance(actions, list) and all(isinstance(item, str) for item in actions), "analysis task required_actions must be a string list")
    missing_actions = sorted(REQUIRED_ACTIONS.difference(actions))
    require(not missing_actions, f"analysis task omits required actions: {', '.join(missing_actions)}")
    require(
        bool(ANALYSIS_ACTION_ALIASES.intersection(actions)),
        "analysis task omits an analysis-output action",
    )
    completion = task.get("completion")
    require(isinstance(completion, dict), "analysis task lacks completion object")
    require(completion.get("action") == "merge", "analysis task completion.action must be merge")
    require(completion.get("merge_method") in {"squash", "merge", "rebase"}, "invalid analysis task merge method")
    require(task.get("blockers") == [], "pending analysis task must have no blockers")


def validate_git_state(
    repo: Path,
    batch_relative: str,
    branch: str,
    normalization_commit: str,
) -> None:
    require(COMMIT_RE.fullmatch(normalization_commit) is not None, "normalization commit must be a full 40-character SHA")
    current_branch = git(repo, "branch", "--show-current").stdout.strip()
    require(current_branch == branch, f"current branch {current_branch!r} differs from task branch {branch!r}")
    require(git(repo, "cat-file", "-t", normalization_commit).stdout.strip() == "commit", "normalization_commit is not a commit")
    require(git(repo, "merge-base", "--is-ancestor", normalization_commit, "HEAD", check=False).returncode == 0, "normalization_commit is not an ancestor of HEAD")
    dirty = git(repo, "status", "--porcelain", "--", batch_relative).stdout.strip()
    require(not dirty, f"batch has uncommitted changes: {dirty}")
    changed = git(
        repo,
        "diff",
        "--name-only",
        normalization_commit,
        "HEAD",
        "--",
        batch_relative,
    ).stdout.splitlines()
    task_mirror = f"{batch_relative}/handoff/ANALYSIS_TASK_V1.json"
    immutable_changes = [path for path in changed if path != task_mirror]
    require(not immutable_changes, f"immutable Phase 1 files changed after normalization commit: {immutable_changes}")
    base_ref = "origin/main" if git(repo, "rev-parse", "--verify", "origin/main^{commit}", check=False).returncode == 0 else "main"
    require(git(repo, "rev-parse", "--verify", f"{base_ref}^{{commit}}", check=False).returncode == 0, "canonical main ref is unavailable")
    merge_base = git(repo, "merge-base", base_ref, "HEAD").stdout.strip()
    model_changed = git(repo, "diff", "--name-only", merge_base, "HEAD", "--", "analysis/model_versions").stdout.strip()
    require(not model_changed, f"frozen model files changed: {model_changed}")


def validate_documented_hashes(batch: Path, source_sha256: str, archive_sha256: str) -> None:
    source_text = (batch / "source/README.md").read_text(encoding="utf-8").casefold()
    require(source_sha256 in source_text, "source/README.md does not record the verified source SHA-256")
    bundle_text = (batch / "bundle/README.md").read_text(encoding="utf-8").casefold()
    documented = re.findall(
        r"(?:archive[_ -]sha-?256\s*:|#\s*expected\s*:)\s*`?([0-9a-f]{64})",
        bundle_text,
    )
    require(len(documented) == 1, "bundle/README.md must record exactly one expected archive SHA-256")
    require(documented[0] == archive_sha256, "bundle/README.md expected archive hash is incorrect")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Validate a publishable Bannerlord Phase 1 handoff")
    value.add_argument("--repo-root", type=Path, required=True)
    value.add_argument("--batch-dir", type=Path, required=True)
    value.add_argument("--branch", required=True)
    value.add_argument("--normalization-commit", required=True)
    return value


def validate_batch_layout(batch: Path) -> None:
    allowed_exact = set(REQUIRED_BATCH_FILES)
    unexpected: list[str] = []
    for path in batch.rglob("*"):
        if not (path.is_file() or path.is_symlink()):
            continue
        relative = path.relative_to(batch).as_posix()
        require(not path.is_symlink(), f"Phase 1 batch files must not be symlinks: {relative}")
        if relative in allowed_exact:
            continue
        parts = PurePosixPath(relative).parts
        if is_allowed_source_path(PurePosixPath(relative)):
            continue
        if parts[0] == "bundle" and (
            relative == "bundle/README.md"
            or re.fullmatch(r"bundle/.+\.base64\.part-\d+", relative)
        ):
            continue
        unexpected.append(relative)
    require(not unexpected, f"non-Phase-1 files are forbidden in the batch root: {sorted(unexpected)}")


def main() -> int:
    args = parser().parse_args()
    repo = args.repo_root.resolve()
    batch = args.batch_dir.resolve()
    require((repo / "AGENTS.md").is_file(), f"not a bannerlord-troop-analysis checkout: {repo}")
    try:
        batch_relative = batch.relative_to(repo).as_posix()
    except ValueError as error:
        raise HandoffError("batch directory must be inside the repository") from error
    require(batch_relative.startswith("data/combat_observations/"), "batch must live under data/combat_observations/")
    for relative in REQUIRED_BATCH_FILES:
        require((batch / relative).is_file(), f"missing Phase 1 file: {relative}")
    validate_batch_layout(batch)

    task = load_json(batch / "handoff/ANALYSIS_TASK_V1.json")
    parts = ordered_bundle_parts(batch / "bundle")
    archive = decode_archive(parts)
    archive_sha256 = sha256_bytes(archive)
    files = archive_files(archive)
    for relative in REQUIRED_ARCHIVE_FILES:
        require(relative in files, f"normalized archive lacks required file: {relative}")
    for relative in MIRRORED_ARCHIVE_FILES:
        require((batch / relative).read_bytes() == files[relative], f"batch root differs from archive: {relative}")
    manifest_count = validate_manifest(files["artifact_hashes.csv"], files)

    summary = load_archive_json(files, "normalization_summary.json")
    report = load_archive_json(files, "validation_report.json")
    validate_source_identity(summary, report, task)
    validate_counts(files, summary, report)
    validate_documented_hashes(batch, str(task["source_sha256"]), archive_sha256)

    expected_handoff = f"{batch_relative}/handoff/ANALYSIS_PROMPT.md"
    validate_task(
        task,
        branch=args.branch,
        normalization_commit=args.normalization_commit,
        expected_handoff_path=expected_handoff,
        archive_sha256=archive_sha256,
    )
    validate_git_state(repo, batch_relative, args.branch, args.normalization_commit)

    result = {
        "status": "passed",
        "batch_path": batch_relative,
        "branch": args.branch,
        "normalization_commit": args.normalization_commit,
        "task_id": task["task_id"],
        "source_sha256": task["source_sha256"],
        "normalized_archive_sha256": archive_sha256,
        "bundle_parts": len(parts),
        "manifest_entries": manifest_count,
        "protocol_status": "pending",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (HandoffError, OSError, UnicodeDecodeError, ValueError) as error:
        print(f"Phase 1 handoff validation failed: {error}", file=sys.stderr)
        raise SystemExit(2)
