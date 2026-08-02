#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
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
    "generate_analysis_outputs",
    "confirm_frozen_models_unchanged",
    "validate_and_merge",
}
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
    encoded = b"".join(part.read_bytes() for part in parts)
    try:
        return base64.b64decode(encoded, validate=True)
    except ValueError as error:
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
    return result


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


def validate_source_identity(summary: dict[str, object], report: dict[str, object], task: dict[str, object]) -> None:
    source_hash = summary.get("source_zip_sha256")
    require(isinstance(source_hash, str) and SHA256_RE.fullmatch(source_hash) is not None, "normalization_summary.json lacks a valid source_zip_sha256")
    require(report.get("source_zip_sha256") == source_hash, "validation_report.json source hash differs from normalization summary")
    source_size = report.get("source_zip_size_bytes")
    require(isinstance(source_size, int) and not isinstance(source_size, bool) and source_size > 0, "validation_report.json lacks a positive source_zip_size_bytes")
    require(task.get("source_sha256") == source_hash, "analysis task source_sha256 differs from normalized evidence")
    require(report.get("status") == "passed", "Phase 1 validation_report.json status is not passed")
    errors = report.get("validation_errors")
    require(isinstance(errors, list) and not errors, "Phase 1 validation_report.json contains errors")


def validate_counts(summary: dict[str, object], report: dict[str, object]) -> None:
    pairs = (
        ("screenshots", "image_count"),
        ("battles", "battle_count"),
        ("observations", "observation_count"),
        ("primary_troop_occurrences", "primary_troop_occurrences"),
        ("review_queue", "review_queue_count"),
    )
    for summary_key, report_key in pairs:
        require(summary_key in summary, f"normalization_summary.json lacks {summary_key}")
        require(report_key in report, f"validation_report.json lacks {report_key}")
        require(summary[summary_key] == report[report_key], f"count mismatch: {summary_key} != {report_key}")


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
    immutable = [path for path in REQUIRED_BATCH_FILES if path != "handoff/ANALYSIS_TASK_V1.json"]
    changed = git(
        repo,
        "diff",
        "--name-only",
        normalization_commit,
        "HEAD",
        "--",
        *[f"{batch_relative}/{path}" for path in immutable],
    ).stdout.strip()
    require(not changed, f"immutable Phase 1 files changed after normalization commit: {changed}")
    model_changed = git(repo, "diff", "--name-only", f"{normalization_commit}^", "HEAD", "--", "analysis/model_versions").stdout.strip()
    require(not model_changed, f"frozen model files changed: {model_changed}")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Validate a publishable Bannerlord Phase 1 handoff")
    value.add_argument("--repo-root", type=Path, required=True)
    value.add_argument("--batch-dir", type=Path, required=True)
    value.add_argument("--branch", required=True)
    value.add_argument("--normalization-commit", required=True)
    return value


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
    for forbidden in (batch / "analysis", batch / "review"):
        require(not forbidden.exists(), f"Phase 2 directory is forbidden in Phase 1: {forbidden.name}")

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
    validate_counts(summary, report)

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
