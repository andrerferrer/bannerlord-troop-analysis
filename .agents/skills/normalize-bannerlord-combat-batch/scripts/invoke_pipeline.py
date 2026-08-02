#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import zipfile
from pathlib import Path


PIPELINE_VERSION = "0.2.0"
SKILL_RUNNER_VERSION = "0.3.0-phase1"
SCHEMA_VERSION = "2.0.0"
BUNDLE_PART_PREFIX = "bannerlord_normalized_v1.tar.xz.base64.part-"


class InvocationError(RuntimeError):
    pass


def stable_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def input_hash(path: Path) -> str:
    if path.is_file():
        return sha256_file(path)
    digest = hashlib.sha256()
    symlinks = sorted(item for item in path.rglob("*") if item.is_symlink())
    if symlinks:
        raise InvocationError(
            "input directories must not contain symlinks: "
            f"{symlinks[0].relative_to(path).as_posix()}"
        )
    for child in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(child.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256_file(child).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def is_repo(path: Path) -> bool:
    return (path / "scripts/combat_observations/__main__.py").is_file()


def discover_repo(explicit: Path | None) -> Path:
    candidates = []
    if explicit:
        candidates.append(explicit)
    environment = os.environ.get("BANNERLORD_TROOP_ANALYSIS_REPO")
    if environment:
        candidates.append(Path(environment))
    candidates.extend([Path.cwd(), *Path.cwd().parents, *Path(__file__).resolve().parents])
    for candidate in candidates:
        resolved = candidate.resolve()
        if is_repo(resolved):
            return resolved
    raise InvocationError(
        "compatible bannerlord-troop-analysis checkout not found; pass --repo /path/to/checkout "
        "containing scripts/combat_observations/__main__.py"
    )


def run(repo: Path, arguments: list[str], *, environment: dict[str, str] | None = None) -> None:
    command = [sys.executable, "-m", "scripts.combat_observations", *arguments]
    print("+", " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=repo, env=environment)
    if completed.returncode:
        raise InvocationError(
            f"pipeline command failed with exit code {completed.returncode}: {' '.join(arguments)}"
        )


def find_manifest(output: Path) -> Path:
    manifests = sorted((output / "manifest").glob("*.csv"))
    if len(manifests) != 1:
        raise InvocationError(f"expected one generated manifest, found {len(manifests)}")
    return manifests[0]


def find_existing_normalized(root: Path) -> Path | None:
    matches = sorted(root.rglob("troop_occurrences.jsonl"))
    if len(matches) > 1:
        raise InvocationError(
            f"ambiguous normalized input: found {len(matches)} troop_occurrences.jsonl files"
        )
    return matches[0] if matches else None


def load_config(path: Path | None) -> dict[str, object]:
    if path is None:
        return {}
    if not path.is_file():
        raise InvocationError(f"configuration file does not exist: {path}")
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=lambda constant: (_ for _ in ()).throw(
                ValueError(f"non-standard JSON constant {constant}")
            ),
        )
    except (OSError, ValueError) as error:
        raise InvocationError(f"invalid configuration JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise InvocationError("configuration root must be an object")
    return value


def option_hash(path: Path | None, label: str) -> str | None:
    if path is None:
        return None
    if not path.is_file():
        raise InvocationError(f"{label} file does not exist: {path}")
    return sha256_file(path)


def positive_config_number(
    section: dict[str, object],
    name: str,
    default: int | float,
) -> int | float:
    value = section.get(name, default)
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or value <= 0
    ):
        raise InvocationError(f"configuration {name} must be a positive number")
    return value


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--input", type=Path, required=True)
    value.add_argument("--output", type=Path, required=True)
    value.add_argument("--mode", choices=("offline-existing", "host-vision", "api-batch"), required=True)
    value.add_argument("--repo", type=Path)
    value.add_argument("--config", type=Path)
    value.add_argument("--authorize-paid-api", action="store_true")
    value.add_argument("--estimated-cost-per-image", type=float)
    return value


def main() -> int:
    args = parser().parse_args()
    source = args.input.resolve()
    if not source.exists():
        raise InvocationError(f"input path does not exist: {source}")
    repo = discover_repo(args.repo)
    output = args.output.resolve()
    if source.is_dir() and (output == source or output.is_relative_to(source)):
        raise InvocationError(
            "output directory must not be the input directory or one of its descendants"
        )
    output.mkdir(parents=True, exist_ok=True)
    digest = input_hash(source)
    input_name = source.name
    input_kind = "directory" if source.is_dir() else "zip"
    config = load_config(args.config)
    declared_pipeline_version = config.get("pipeline_version")
    if (
        declared_pipeline_version is not None
        and declared_pipeline_version != PIPELINE_VERSION
    ):
        raise InvocationError(
            "configuration pipeline_version is incompatible: "
            f"expected {PIPELINE_VERSION}, observed {declared_pipeline_version}"
        )
    archive_config = config.get("archive_limits", {})
    extraction_config = config.get("extraction", {})
    if not isinstance(archive_config, dict):
        raise InvocationError("archive_limits configuration section must be an object")
    if not isinstance(extraction_config, dict):
        raise InvocationError("extraction configuration section must be an object")
    max_members = int(positive_config_number(archive_config, "max_members", 10_000))
    max_uncompressed = int(
        positive_config_number(
            archive_config,
            "max_uncompressed_bytes",
            1_000_000_000,
        )
    )
    max_ratio = float(
        positive_config_number(archive_config, "max_compression_ratio", 1_000.0)
    )
    pipeline_environment = os.environ.copy()
    extraction_environment = {
        "prompt_version": ("COMBAT_PROMPT_VERSION", "combat-v2"),
        "image_detail": ("IMAGE_DETAIL", "high"),
        "max_retries": ("VISION_MAX_RETRIES", 2),
    }
    for key, (environment_name, default) in extraction_environment.items():
        value = extraction_config.get(key, default)
        pipeline_environment[environment_name] = str(value)
    configuration = {
        "mode": args.mode,
        "config": option_hash(args.config, "configuration"),
    }
    configuration_hash = hashlib.sha256(stable_json(configuration).encode("utf-8")).hexdigest()
    state_path = output / "batch_state.json"
    state = {
        "batch_id": f"batch_{digest[:20]}",
        "input_name": input_name,
        "input_kind": input_kind,
        "input_sha256": digest,
        "pipeline_version": PIPELINE_VERSION,
        "skill_runner_version": SKILL_RUNNER_VERSION,
        "schema_version": SCHEMA_VERSION,
        "configuration_hash": configuration_hash,
        "mode": args.mode,
        "phase_statuses": {},
        "processed_images": 0,
        "pending_images": 0,
        "review_queue_size": 0,
        "failed_items": [],
        "retry_counts": {},
        "generated_artifacts": [],
        "counts": {},
        "status": "in_progress",
        "next_action": "preflight",
        "resume_command": shlex.join([sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]]),
    }
    if state_path.exists():
        existing = json.loads(state_path.read_text(encoding="utf-8"))
        for field in (
            "input_sha256",
            "pipeline_version",
            "skill_runner_version",
            "schema_version",
            "configuration_hash",
            "mode",
        ):
            if existing.get(field) != state[field]:
                raise InvocationError(f"refusing incompatible resume: {field} changed")
        state = existing
    atomic_json(state_path, state)

    run(repo, ["--help"], environment=pipeline_environment)
    if source.is_file() and zipfile.is_zipfile(source):
        with zipfile.ZipFile(source) as archive:
            basenames = {Path(name).name for name in archive.namelist()}
        if "troop_occurrences.jsonl" in basenames or any(
            name.startswith(BUNDLE_PART_PREFIX) for name in basenames
        ):
            staged = output / "normalized-staging"
            run(
                repo,
                [
                    "stage-normalized-zip",
                    "--input", str(source),
                    "--output-dir", str(staged),
                    "--report", str(output / "reports/normalized_zip_preflight.json"),
                    "--max-members", str(max_members),
                    "--max-uncompressed-bytes", str(max_uncompressed),
                    "--max-compression-ratio", str(max_ratio),
                ],
                environment=pipeline_environment,
            )
            source = staged
            state["phase_statuses"]["normalized_zip_preflight"] = "complete"
            atomic_json(state_path, state)
    bundle_parts = list(source.rglob(f"{BUNDLE_PART_PREFIX}*")) if source.is_dir() else []
    if len(bundle_parts) == 11:
        bundle_dir = bundle_parts[0].parent
        reports = output / "reports"
        run(
            repo,
            [
                "reconstruct-bundle",
                "--bundle-dir", str(bundle_dir),
                "--archive", str(output / "normalized.tar.xz"),
                "--extract-dir", str(output / "normalized"),
                "--report", str(reports / "p0_verification_report.json"),
                "--forensic-report", str(reports / "p0_bundle_forensics.json"),
            ],
            environment=pipeline_environment,
        )
        source = output / "normalized"
        state["phase_statuses"]["bundle_verification"] = "complete"
        atomic_json(state_path, state)

    normalized = find_existing_normalized(source) if source.is_dir() else None
    if normalized is None:
        if args.mode == "offline-existing":
            raise InvocationError(
                "offline-existing requires a normalized input; use host-vision for screenshots"
            )
        run(
            repo,
            [
                "manifest-images",
                "--input", str(source),
                "--output-dir", str(output),
                "--max-members", str(max_members),
                "--max-uncompressed-bytes", str(max_uncompressed),
                "--max-compression-ratio", str(max_ratio),
            ],
            environment=pipeline_environment,
        )
        manifest = find_manifest(output)
        extraction_args = [
            "extract-combat-screens",
            "--manifest", str(manifest),
            "--output-dir", str(output / "extraction"),
            "--mode", args.mode,
        ]
        if args.authorize_paid_api:
            extraction_args.append("--authorize-paid-api")
        if args.estimated_cost_per_image is not None:
            extraction_args.extend(["--estimated-cost-per-image", str(args.estimated_cost_per_image)])
        run(repo, extraction_args, environment=pipeline_environment)
        plan = json.loads((output / "extraction/extraction_plan.json").read_text(encoding="utf-8"))
        state["phase_statuses"]["preflight"] = "complete"
        state["phase_statuses"]["extraction"] = "pending"
        state["pending_images"] = plan["queue_size"]
        state["counts"] = {"images_queued": plan["queue_size"]}
        state["generated_artifacts"] = [
            str(manifest.relative_to(output)),
            "extraction/extraction_queue.jsonl",
            "extraction/extraction_plan.json",
        ]
        state["next_action"] = (
            "process extraction/extraction_queue.jsonl, retain raw structured results, then rerun "
            "with an existing normalized directory"
        )
        state["status"] = "partial"
        atomic_json(state_path, state)
        print(f"partial batch ready; resume state: {state_path}")
        return 0

    state["phase_statuses"]["raw_verification"] = "complete"
    state["phase_statuses"]["phase1_packaging"] = "pending"
    state["phase_statuses"]["canonical"] = "not_permitted_in_phase1"
    state["phase_statuses"]["model_comparison"] = "not_permitted_in_phase1"
    state["pending_images"] = 0
    state["generated_artifacts"] = [str(normalized.relative_to(source))]
    state["status"] = "partial"
    state["next_action"] = (
        "assemble the repository Phase 1 bundle and handoff, then run "
        ".agents/skills/normalize-bannerlord-combat-batch/scripts/"
        "validate_phase1_handoff.py before publication"
    )
    atomic_json(state_path, state)
    print(f"normalized Phase 1 input found; analysis intentionally not run: {state_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except InvocationError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)
