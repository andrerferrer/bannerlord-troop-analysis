#!/usr/bin/env python3
"""Reconstruct, verify, or extract the Qartheen Guardian Phase 1 bundle."""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import shutil
import tarfile
from pathlib import Path

BATCH = Path(__file__).resolve().parents[1]
ARCHIVE_NAME = "rot_qartheen_enthroned_guardian_field_phase1.tar.xz"
ARCHIVE_TEXT = BATCH / "bundle/rot_qartheen_enthroned_guardian_field_phase1.tar.xz.base64"
EXPECTED_ARCHIVE_SHA256 = "ae7c7998ae73a5f9adc358550644813770280512b05f06e0b79418d3dff78f0b"
EXPECTED_BASE64_TEXT_SHA256 = "d250d3caddee132d3e1fa80b03162498f77a698f78acb05a9b150c016241743c"
MEMBER_NAMES = ['README.md', 'source_manifest.json', 'source_inventory.csv', 'screenshots_manifest.csv', 'normalized/events.jsonl', 'normalized/party_summaries.jsonl', 'normalized/player_rows.jsonl', 'review_queue.csv', 'screenshot_deduplication_audit.csv', 'correspondence_check.json', 'integrity_report.json', 'phase1_checkpoint.json', 'batch_state.json', 'handoff/ANALYSIS_PROMPT.md', 'handoff/ANALYSIS_TASK_V1.json']
EXTERNAL_MIRRORS = (
    "README.md",
    "screenshots_manifest.csv",
    "phase1_checkpoint.json",
    "batch_state.json",
    "handoff/ANALYSIS_PROMPT.md",
    "handoff/ANALYSIS_TASK_V1.json",
)


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def decode_checked_in() -> bytes:
    encoded = ARCHIVE_TEXT.read_bytes()
    if digest(encoded) != EXPECTED_BASE64_TEXT_SHA256:
        raise SystemExit("checked-in Base64 text SHA-256 mismatch")
    archive = base64.b64decode(b"".join(encoded.split()), validate=True)
    if digest(archive) != EXPECTED_ARCHIVE_SHA256:
        raise SystemExit("decoded archive SHA-256 mismatch")
    return archive


def read_members(archive: bytes) -> dict[str, bytes]:
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as handle:
        members = {m.name: handle.extractfile(m).read() for m in handle.getmembers() if m.isfile()}
    if list(members) != MEMBER_NAMES:
        raise SystemExit(f"archive member order/inventory mismatch: {list(members)}")
    return members


def verify_members(members: dict[str, bytes]) -> None:
    expected = {
        line.split("  ", 1)[1]: line.split("  ", 1)[0]
        for line in (BATCH / "bundle/rot_qartheen_enthroned_guardian_field_phase1.members.sha256")
        .read_text(encoding="utf-8").splitlines()
        if line
    }
    for name in MEMBER_NAMES:
        actual = digest(members[name])
        if actual != expected.get(name):
            raise SystemExit(f"member hash mismatch: {name} {actual} != {expected.get(name)}")
    for name in EXTERNAL_MIRRORS:
        if (BATCH / name).read_bytes() != members[name]:
            raise SystemExit(f"external mirror differs from immutable archive member: {name}")


def extract_members(members: dict[str, bytes], destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name, payload in members.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--extract", type=Path)
    args = parser.parse_args()

    archive = decode_checked_in()
    members = read_members(archive)
    verify_members(members)
    if args.extract:
        extract_members(members, args.extract)
        print(f"extracted {len(members)} members to {args.extract}")
    if args.check or not args.extract:
        print("Phase 1 bundle verified")


if __name__ == "__main__":
    main()
