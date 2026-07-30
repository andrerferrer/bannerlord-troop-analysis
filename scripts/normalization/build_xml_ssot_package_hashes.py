#!/usr/bin/env python3
"""Build xml_ssot_package hashes + PACKAGE.json for an XML export snapshot.

This is an XML audit SSOT package, not an ADR-002 combat evidence package.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

TRACKS = ("vanilla", "nightmare_sails", "realm_of_thrones", "taom")
ALLOWLISTED_RAW_NAMES = ("manifest.csv", "manifest_modules.csv", "MANIFEST.md")
SOURCE_ZIP_SHA256 = (
    "307d9eab533b1b83bb76545141226f86144af6712ed0b64b29e3efc3e23f3ad8"
)
SOURCE_ZIP_FILENAME = "bannerlord_xml_export_20260729_025002.zip"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def package_digest(rows: list[dict[str, str]]) -> str:
    lines = [
        f"{row['path']},{row['bytes']},{row['sha256']}"
        for row in sorted(rows, key=lambda item: item["path"])
    ]
    payload = "\n".join(lines) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def collect_paths(repo: Path, export_id: str) -> list[Path]:
    package_root = repo / "data" / "xml_exports" / export_id
    paths: list[Path] = []
    for path in sorted(package_root.iterdir()):
        if not path.is_file():
            continue
        if path.name in {"artifact_hashes.csv", "PACKAGE.json"}:
            continue
        paths.append(path)
    for track in TRACKS:
        audit_dir = repo / "data" / track / "audit"
        paths.extend(sorted(audit_dir.glob("*.csv")))
        raw_dir = repo / "data" / track / "raw_xml"
        for name in ALLOWLISTED_RAW_NAMES:
            candidate = raw_dir / name
            if candidate.is_file():
                paths.append(candidate)
    return paths


def build_rows(repo: Path, paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        rel = path.relative_to(repo).as_posix()
        if rel.lower().endswith(".xml"):
            raise SystemExit(f"refusing to hash XML body: {rel}")
        rows.append(
            {
                "path": rel,
                "bytes": str(path.stat().st_size),
                "sha256": sha256_file(path),
            }
        )
    rows.sort(key=lambda item: item["path"])
    return rows


def write_hashes(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--export-id", default="export_20260729_025002")
    parser.add_argument(
        "--source-zip",
        type=Path,
        default=None,
        help="Optional local zip for size_bytes; SHA must match pin",
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    package_root = repo / "data" / "xml_exports" / args.export_id
    package_root.mkdir(parents=True, exist_ok=True)

    rows = build_rows(repo, collect_paths(repo, args.export_id))
    write_hashes(package_root / "artifact_hashes.csv", rows)
    digest = package_digest(rows)

    size_bytes = None
    source_zip = args.source_zip
    if source_zip is None:
        env_zip = Path.home() / "Downloads" / SOURCE_ZIP_FILENAME
        if env_zip.is_file():
            source_zip = env_zip
    if source_zip is not None and source_zip.is_file():
        actual = sha256_file(source_zip)
        if actual != SOURCE_ZIP_SHA256:
            raise SystemExit(
                f"source zip sha mismatch: expected {SOURCE_ZIP_SHA256}, got {actual}"
            )
        size_bytes = source_zip.stat().st_size

    package = {
        "export_id": args.export_id,
        "game_version": "v1.4.7",
        "package_kind": "xml_ssot_package",
        "not_combat_evidence_package": True,
        "analysis_task_protocol": None,
        "tracks": list(TRACKS),
        "source_zip": {
            "filename": SOURCE_ZIP_FILENAME,
            "size_bytes": size_bytes,
            "sha256": SOURCE_ZIP_SHA256,
            "retention": "local_only",
            "lfs_declined": True,
            "git_declined": True,
            "local_path_convention": [
                "$BANNERLORD_XML_EXPORT_ZIP",
                f"~/Downloads/{SOURCE_ZIP_FILENAME}",
            ],
        },
        "reconstruction_commands": [
            f"unzip -d /tmp/{args.export_id} ~/Downloads/{SOURCE_ZIP_FILENAME}",
            (
                "python3 scripts/normalization/rebuild_vanilla_audit.py "
                "--raw-xml-root data/<track>/raw_xml --output-dir data/<track>/audit "
                "--track <track> --load-order <ordered-modules> --baseline-modules <baseline>"
            ),
            (
                "python3 scripts/normalization/build_xml_ssot_package_hashes.py "
                f"--export-id {args.export_id}"
            ),
        ],
        "expected_package_sha256": digest,
        "hash_algorithm": (
            "SHA-256 of UTF-8 text formed by sorting artifact_hashes.csv data rows as "
            "path,bytes,sha256 lines joined by \\n with a trailing \\n; "
            "artifact_hashes.csv and PACKAGE.json are excluded from the row set"
        ),
    }
    (package_root / "PACKAGE.json").write_text(
        json.dumps(package, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(rows)} hash rows")
    print(f"expected_package_sha256={digest}")


if __name__ == "__main__":
    main()
