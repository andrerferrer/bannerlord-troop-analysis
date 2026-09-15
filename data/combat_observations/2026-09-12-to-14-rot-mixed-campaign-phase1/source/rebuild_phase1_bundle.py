#!/usr/bin/env python3
"""Rebuild the PR #99 Phase 1 manifest and deterministic normalized archive."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import tarfile
from pathlib import Path


BATCH = Path(__file__).resolve().parents[1]
ARCHIVE_TEXT = BATCH / "bundle/rot_mixed_campaign_phase1.tar.xz.base64"
ARCHIVE_NAME = "rot_mixed_campaign_phase1.tar.xz"
MEMBER_NAMES = (
    "README.md",
    "source_manifest.json",
    "source_inventory.csv",
    "screenshots_manifest.csv",
    "integrity_report.json",
    "phase1_checkpoint.json",
    "batch_state.json",
    "normalized/events.jsonl",
    "normalized/party_summaries.jsonl",
    "normalized/player_rows.jsonl",
    "handoff/ANALYSIS_TASK_V1.json",
)
IMMUTABLE_EVIDENCE_HASHES = {
    "source_manifest.json": "0234f98f5aa18dff530bcac56645ffde545111d55eac3a3f0032d8b501202053",
    "source_inventory.csv": "c9a03021d6acefebfc375ea4df341bef0b491de5252d9e6ce4e2cfa44c965ec8",
    "integrity_report.json": "60ee02c2f23649bcc8cc8fc231eb36f6c99da884d1e6bdf22fb7ebe6911fb15c",
    "normalized/events.jsonl": "1eee8abb9d472244be1e78b1d4a569c4fd1abdcdcdeb61468e9cdf630c7b05df",
    "normalized/party_summaries.jsonl": "74ebe66734ea0df46889f713c05bd160c0b2f8d84840f46d9dc9b46d40f6c13b",
    "normalized/player_rows.jsonl": "1bc97c2ca0c5ca7e8dbf57518c3ffd987188c43a29d6cab0a6dafc7bdff9b359",
}


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_archive() -> dict[str, bytes]:
    raw = base64.b64decode(b"".join(ARCHIVE_TEXT.read_bytes().split()), validate=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:xz") as handle:
        return {
            member.name: handle.extractfile(member).read()
            for member in handle.getmembers()
            if member.isfile()
        }


def load_preserved_evidence() -> dict[str, bytes]:
    members = read_archive()
    for name, expected in IMMUTABLE_EVIDENCE_HASHES.items():
        if name not in members or digest(members[name]) != expected:
            raise RuntimeError(f"immutable normalized evidence changed: {name}")
    return {name: members[name] for name in IMMUTABLE_EVIDENCE_HASHES}


def derive_screenshot_manifest(evidence: dict[str, bytes]) -> bytes:
    source_manifest = json.loads(evidence["source_manifest.json"])
    events = {
        row["event_id"]: row
        for row in map(json.loads, evidence["normalized/events.jsonl"].splitlines())
    }
    inventory = list(
        csv.DictReader(io.StringIO(evidence["source_inventory.csv"].decode("utf-8")))
    )
    sources = source_manifest["sources"]
    inventory_by_key = {row["source_key"]: row for row in inventory}
    if len(sources) != 16 or len(inventory_by_key) != 16 or len(events) != 15:
        raise RuntimeError("expected 16 sources and 15 battle identities")

    fields = [
        "screenshot_id",
        "image_file",
        "image_sha256",
        "captured_at",
        "battle_id",
        "screen_status",
        "included_in_primary",
        "game_version",
        "game_track",
    ]
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for source in sources:
        source_key = source["source_key"]
        inventory_row = inventory_by_key[source_key]
        event_ids = source["event_ids"]
        if len(event_ids) != 1:
            raise RuntimeError(f"source must map to exactly one battle: {source_key}")
        event_id = event_ids[0]
        event = events[event_id]
        expected_inventory = {
            "filename": source["filename"],
            "sha256": source["sha256"],
            "capture_timestamp_local": source["capture_timestamp_local"],
            "event_ids": event_id,
        }
        if any(inventory_row[key] != value for key, value in expected_inventory.items()):
            raise RuntimeError(f"source manifest/inventory mismatch: {source_key}")
        writer.writerow(
            {
                "screenshot_id": source_key.replace("src_", "screen_", 1),
                "image_file": source["filename"],
                "image_sha256": source["sha256"],
                "captured_at": source["capture_timestamp_local"],
                "battle_id": event_id,
                "screen_status": (
                    "active"
                    if event["result_status"] == "in_progress"
                    else "final_result"
                ),
                "included_in_primary": True,
                "game_version": "unknown",
                "game_track": "realm_of_thrones",
            }
        )
    return output.getvalue().encode("utf-8")


def phase1_readme() -> bytes:
    return b"""# Phase 1 \xe2\x80\x94 ROT mixed campaign screenshots (2026-09-12 to 2026-09-14)

This directory is a **normalization-only checkpoint** for 16 uploaded screenshots grouped into 15 battle events.

## Scope and counts

- Source PNGs: **16**
- Unique events: **15** (`16 files - 1 complementary view of the same 2026-09-14 20:57 battle = 15`)
- Final victories: **9**
- Completed `Retreated to the keep!` outside-stage transitions: **3**
- In-progress/right-censored snapshots: **3**
- Field events: **8**
- Siege attacks: **7**
- Game version: **unknown** (not visible or otherwise authoritatively recorded in the retained Phase 1 source metadata)

The event partition reconciles as `9 + 3 + 3 = 15`, and the context partition as `8 + 7 = 15`.

## Normalization contract

Columns are `survivors, kills, upgrade_ready, deaths, wounded, routed`. Visible blank numeric cells are zero. Occluded/clipped cells are `null`. Hero upgrade icons are retained as `upgrade_marker_visible` rather than converted into a number. Every visible player-side troop row is preserved, including allied player parties.

The screenshots at `2026-09-14 20:57:47` and `20:57:51` are complementary views of one battle because duration and both side totals are identical while the scroll positions expose different parties. Both sources are retained under the same battle ID.

`Retreated to the keep!` is recorded as a successful completed outside-wall siege stage, not a defeat. Active snapshots remain right-censored.

## Files

- `source_manifest.json` \xe2\x80\x94 source filenames, SHA-256, byte sizes, timestamps, dimensions, and event links.
- `source_inventory.csv` \xe2\x80\x94 compact review inventory.
- `screenshots_manifest.csv` \xe2\x80\x94 authoritative source-to-battle manifest using the repository schema.
- `normalized/events.jsonl` \xe2\x80\x94 one record per unique battle event.
- `normalized/party_summaries.jsonl` \xe2\x80\x94 player-side party totals and row-coverage deltas.
- `normalized/player_rows.jsonl` \xe2\x80\x94 all visible player-side rows.
- `integrity_report.json` \xe2\x80\x94 deterministic validation output.
- `phase1_checkpoint.json` / `batch_state.json` \xe2\x80\x94 workflow checkpoint and current Phase 1 bundle identity.
- `bundle/README.md` \xe2\x80\x94 archive reconstruction and deterministic rebuild verification.
- `bundle/rot_mixed_campaign_phase1.members.sha256` \xe2\x80\x94 hash for every archive member.
- `handoff/ANALYSIS_PROMPT.md` \xe2\x80\x94 Phase 2 instructions for a separate downstream agent.
- `handoff/ANALYSIS_TASK_V1.json` \xe2\x80\x94 machine-readable Phase 2 task metadata.

## Gate

No performance verdict, tier change, evidence-gate decision, or test-queue mutation is included. This repair adds the omitted authoritative screenshot manifest without changing normalized evidence bytes. Phase 2 must reverify the repaired Phase 1 archive before the pull request can pass its merge gate.

Raw PNG bytes are not copied into Git. The source and screenshot manifests pin the exact uploaded files by SHA-256; pixel-level reinspection later requires the matching upload.
"""


def updated_task(manifest_sha: str) -> dict[str, object]:
    task = json.loads((BATCH / "handoff/ANALYSIS_TASK_V1.json").read_text(encoding="utf-8"))
    task["status"] = "ready_for_revalidation"
    task["inputs"]["source_inventory"] = "source_inventory.csv"
    task["inputs"]["screenshots_manifest"] = "screenshots_manifest.csv"
    task["phase1_artifact_metadata"] = {
        "source_artifacts": 16,
        "battle_identities": 15,
        "game_track": "realm_of_thrones",
        "game_version": "unknown",
        "screenshots_manifest_sha256": manifest_sha,
        "normalized_evidence_bytes_changed": False,
    }
    task.pop("blocker_in_current_session", None)
    return task


def archive_metadata(*, repository_copy: bool, archive: bytes = b"", encoded: bytes = b"") -> dict[str, object]:
    metadata: dict[str, object] = {
        "path": "bundle/rot_mixed_campaign_phase1.tar.xz.base64",
        "encoding": "base64",
        "archive": "tar.xz",
        "member_count": len(MEMBER_NAMES),
        "member_hashes_path": "bundle/rot_mixed_campaign_phase1.members.sha256",
    }
    if repository_copy:
        metadata.update(
            {
                "sha256_encoded_text": digest(encoded),
                "bytes_encoded_text": len(encoded),
                "sha256_archive": digest(archive),
                "bytes_archive": len(archive),
            }
        )
    else:
        metadata["identity_metadata_scope"] = (
            "repository-level phase1_checkpoint.json; omitted here to avoid a self-referential archive hash"
        )
    return metadata


def updated_checkpoint(manifest_sha: str, *, repository_copy: bool, archive: bytes = b"", encoded: bytes = b"") -> dict[str, object]:
    checkpoint = json.loads((BATCH / "phase1_checkpoint.json").read_text(encoding="utf-8"))
    checkpoint["normalization"]["screenshot_manifest_rows"] = 16
    checkpoint["normalization"]["game_version"] = "unknown"
    checkpoint["files"]["screenshots_manifest"] = "screenshots_manifest.csv"
    checkpoint["files"]["bundle"] = archive_metadata(
        repository_copy=repository_copy, archive=archive, encoded=encoded
    )
    checkpoint["integrity"]["checks"]["screenshots_manifest_rows"] = 16
    checkpoint["integrity"]["checks"]["screenshots_manifest_sha256"] = manifest_sha
    checkpoint["phase2_gate"] = {
        "status": "requires_revalidation_after_phase1_repair",
        "reason": "The authoritative screenshots_manifest.csv was added and the Phase 1 archive identity changed; a separate Phase 2 agent must reverify the repaired inputs.",
        "safe_action": "Keep the pull request draft until Phase 2 revalidation and all repository gates pass.",
    }
    return checkpoint


def updated_state(*, repository_copy: bool, archive: bytes = b"", encoded: bytes = b"") -> dict[str, object]:
    state = json.loads((BATCH / "batch_state.json").read_text(encoding="utf-8"))
    state["phase"] = "normalization_complete_phase2_revalidation_required"
    state["phase1"]["game_version"] = "unknown"
    state["phase1"]["screenshots_manifest_rows"] = 16
    state["phase1"]["bundle"] = archive_metadata(
        repository_copy=repository_copy, archive=archive, encoded=encoded
    )
    state["phase2"] = {
        "agent_role": "separate_analysis_agent",
        "status": "revalidation_required",
        "reason": "Phase 1 archive identity changed when the omitted authoritative screenshot manifest was added.",
    }
    return state


def build_archive(evidence: dict[str, bytes], manifest: bytes, task: dict[str, object]) -> tuple[bytes, dict[str, bytes]]:
    manifest_sha = digest(manifest)
    members = {
        "README.md": phase1_readme(),
        **evidence,
        "screenshots_manifest.csv": manifest,
        "phase1_checkpoint.json": json_bytes(
            updated_checkpoint(manifest_sha, repository_copy=False)
        ),
        "batch_state.json": json_bytes(updated_state(repository_copy=False)),
        "handoff/ANALYSIS_TASK_V1.json": json_bytes(task),
    }
    if set(members) != set(MEMBER_NAMES):
        raise RuntimeError("unexpected archive member inventory")
    payload = io.BytesIO()
    with tarfile.open(fileobj=payload, mode="w:xz", format=tarfile.PAX_FORMAT) as handle:
        for name in MEMBER_NAMES:
            data = members[name]
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mtime = 0
            info.mode = 0o644
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            handle.addfile(info, io.BytesIO(data))
    return payload.getvalue(), members


def bundle_readme(archive: bytes, encoded: bytes) -> bytes:
    return f"""# Deterministic normalized Phase 1 bundle

The Base64 file reconstructs `{ARCHIVE_NAME}` with {len(MEMBER_NAMES)} members. Raw PNG bytes are not included.

From this batch directory:

```bash
BATCH_DIR=$PWD
OUT=$(mktemp -d)
base64 --decode < bundle/rot_mixed_campaign_phase1.tar.xz.base64 > /tmp/{ARCHIVE_NAME}
echo '{digest(archive)}  /tmp/{ARCHIVE_NAME}' | sha256sum -c -
tar -xJf /tmp/{ARCHIVE_NAME} -C "$OUT"
(cd "$OUT" && sha256sum -c "$BATCH_DIR/bundle/rot_mixed_campaign_phase1.members.sha256")
```

- Archive SHA-256: `{digest(archive)}`
- Archive size: `{len(archive)}` bytes
- Base64 text SHA-256: `{digest(encoded)}`
- Base64 text size: `{len(encoded)}` bytes
- Archive member count: `{len(MEMBER_NAMES)}`

To verify that the checked-in archive is a deterministic rebuild of the retained Phase 1 evidence and metadata:

```bash
python3 source/rebuild_phase1_bundle.py --check
```
""".encode("utf-8")


def handoff_prompt(archive: bytes, encoded: bytes, manifest_sha: str) -> bytes:
    existing = (BATCH / "handoff/ANALYSIS_PROMPT.md").read_text(encoding="utf-8")
    marker = "\n## Repaired Phase 1 bundle identity\n"
    existing = existing.split(marker, 1)[0].rstrip() + "\n"
    return (
        existing
        + marker
        + "\n"
        + f"- Screenshot manifest SHA-256: `{manifest_sha}`\n"
        + f"- Archive SHA-256: `{digest(archive)}` ({len(archive)} bytes, {len(MEMBER_NAMES)} members)\n"
        + f"- Base64 text SHA-256: `{digest(encoded)}` ({len(encoded)} bytes, including the final newline)\n"
        + "- Rebuild verification: `python3 source/rebuild_phase1_bundle.py --check` from the batch directory.\n"
        + "- Game version remains `unknown`; do not infer it from neighboring batches.\n"
    ).encode("utf-8")


def expected_outputs() -> dict[Path, bytes]:
    evidence = load_preserved_evidence()
    manifest = derive_screenshot_manifest(evidence)
    task = updated_task(digest(manifest))
    archive, members = build_archive(evidence, manifest, task)
    encoded = base64.b64encode(archive) + b"\n"
    member_hashes = "".join(
        f"{digest(members[name])}  {name}\n" for name in MEMBER_NAMES
    ).encode("utf-8")
    return {
        BATCH / "README.md": phase1_readme(),
        BATCH / "screenshots_manifest.csv": manifest,
        BATCH / "phase1_checkpoint.json": json_bytes(
            updated_checkpoint(digest(manifest), repository_copy=True, archive=archive, encoded=encoded)
        ),
        BATCH / "batch_state.json": json_bytes(
            updated_state(repository_copy=True, archive=archive, encoded=encoded)
        ),
        BATCH / "handoff/ANALYSIS_TASK_V1.json": json_bytes(task),
        BATCH / "handoff/ANALYSIS_PROMPT.md": handoff_prompt(
            archive, encoded, digest(manifest)
        ),
        ARCHIVE_TEXT: encoded,
        BATCH / "bundle/rot_mixed_campaign_phase1.tar.xz.sha256": (
            f"{digest(archive)}  {ARCHIVE_NAME}\n".encode("ascii")
        ),
        BATCH / "bundle/rot_mixed_campaign_phase1.members.sha256": member_hashes,
        BATCH / "bundle/README.md": bundle_readme(archive, encoded),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs = expected_outputs()
    if args.check:
        mismatches = [path.relative_to(BATCH) for path, data in outputs.items() if not path.is_file() or path.read_bytes() != data]
        if mismatches:
            raise SystemExit("deterministic rebuild mismatch: " + ", ".join(map(str, mismatches)))
        print("deterministic rebuild verified")
        return
    for path, data in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


if __name__ == "__main__":
    main()
