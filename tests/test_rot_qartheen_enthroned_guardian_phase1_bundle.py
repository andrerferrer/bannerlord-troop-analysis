#!/usr/bin/env python3
"""Structural test for the 2026-09-16 Qartheen Guardian Phase 1 bundle."""

from __future__ import annotations

import base64
import hashlib
import io
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "data/combat_observations/2026-09-16-rot-qartheen-enthroned-guardian-field-phase1"
ARCHIVE_TEXT = BATCH / "bundle/rot_qartheen_enthroned_guardian_field_phase1.tar.xz.base64"
EXPECTED_SHA256 = "ae7c7998ae73a5f9adc358550644813770280512b05f06e0b79418d3dff78f0b"


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def main() -> None:
    archive = base64.b64decode(b"".join(ARCHIVE_TEXT.read_bytes().split()), validate=True)
    assert sha256(archive) == EXPECTED_SHA256
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as handle:
        members = {m.name: handle.extractfile(m).read() for m in handle.getmembers() if m.isfile()}

    assert len(members) == 15
    events = [json.loads(line) for line in members["normalized/events.jsonl"].splitlines()]
    rows = [json.loads(line) for line in members["normalized/player_rows.jsonl"].splitlines()]
    parties = [json.loads(line) for line in members["normalized/party_summaries.jsonl"].splitlines()]

    assert len(events) == 2
    assert len(rows) == 31
    assert sum(row["row_kind"] == "ordinary" for row in rows) == 13
    assert sum(row["row_kind"] == "character" for row in rows) == 18
    assert all(event["context"] == "field" and event["result"] == "victory" for event in events)
    assert [p["unaccounted_to_clipped_or_offscreen_rows"]["kills"] for p in parties] == [0, 0]
    assert [p["unaccounted_to_clipped_or_offscreen_rows"]["wounded"] for p in parties] == [0, 0]

    guardian = [row for row in rows if row["raw_name"] == "Qartheen Enthroned Guardian"]
    assert [(row["deployed"], row["kills"]) for row in guardian] == [(85, 90), (88, 48)]

    unresolved = [row for row in rows if row["raw_name"] is None]
    assert len(unresolved) == 1
    assert unresolved[0]["survivors"] == 0 and unresolved[0]["wounded"] == 1

    print("Phase 1 structural test passed")


if __name__ == "__main__":
    main()
