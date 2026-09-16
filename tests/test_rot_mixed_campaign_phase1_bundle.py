from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import tarfile
import unittest
from collections import Counter
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BATCH = (
    REPOSITORY_ROOT
    / "data/combat_observations/2026-09-12-to-14-rot-mixed-campaign-phase1"
)
ARCHIVE_TEXT = BATCH / "bundle/rot_mixed_campaign_phase1.tar.xz.base64"
ARCHIVE_CHECKSUM = BATCH / "bundle/rot_mixed_campaign_phase1.tar.xz.sha256"
MEMBER_CHECKSUMS = BATCH / "bundle/rot_mixed_campaign_phase1.members.sha256"
MANIFEST = BATCH / "screenshots_manifest.csv"
MANIFEST_FIELDS = [
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
IMMUTABLE_EVIDENCE_HASHES = {
    "source_manifest.json": "0234f98f5aa18dff530bcac56645ffde545111d55eac3a3f0032d8b501202053",
    "source_inventory.csv": "c9a03021d6acefebfc375ea4df341bef0b491de5252d9e6ce4e2cfa44c965ec8",
    "integrity_report.json": "60ee02c2f23649bcc8cc8fc231eb36f6c99da884d1e6bdf22fb7ebe6911fb15c",
    "normalized/events.jsonl": "1eee8abb9d472244be1e78b1d4a569c4fd1abdcdcdeb61468e9cdf630c7b05df",
    "normalized/party_summaries.jsonl": "74ebe66734ea0df46889f713c05bd160c0b2f8d84840f46d9dc9b46d40f6c13b",
    "normalized/player_rows.jsonl": "1bc97c2ca0c5ca7e8dbf57518c3ffd987188c43a29d6cab0a6dafc7bdff9b359",
}


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_archive() -> tuple[bytes, dict[str, bytes]]:
    archive = base64.b64decode(b"".join(ARCHIVE_TEXT.read_bytes().split()), validate=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as handle:
        members = {
            item.name: handle.extractfile(item).read()
            for item in handle.getmembers()
            if item.isfile()
        }
    return archive, members


class RotMixedCampaignPhase1BundleTests(unittest.TestCase):
    def test_authoritative_screenshot_manifest_is_complete_and_bundled(self) -> None:
        self.assertTrue(MANIFEST.is_file(), "missing authoritative screenshots_manifest.csv")

        with MANIFEST.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertEqual(reader.fieldnames, MANIFEST_FIELDS)
            rows = list(reader)

        archive, members = load_archive()
        self.assertIn("screenshots_manifest.csv", members)
        self.assertEqual(members["screenshots_manifest.csv"], MANIFEST.read_bytes())
        self.assertEqual(len(rows), 16)
        self.assertEqual(len({row["screenshot_id"] for row in rows}), 16)
        self.assertEqual(len({row["image_sha256"] for row in rows}), 16)
        self.assertEqual(len({row["battle_id"] for row in rows}), 15)
        self.assertEqual(
            Counter(Counter(row["battle_id"] for row in rows).values()),
            Counter({1: 14, 2: 1}),
        )
        self.assertEqual({row["game_version"] for row in rows}, {"unknown"})
        self.assertEqual({row["game_track"] for row in rows}, {"realm_of_thrones"})

        sources = json.loads(members["source_manifest.json"])["sources"]
        events = {
            row["event_id"]: row
            for row in map(json.loads, members["normalized/events.jsonl"].splitlines())
        }
        actual_by_source = {row["screenshot_id"].replace("screen_", "src_"): row for row in rows}
        self.assertEqual(set(actual_by_source), {source["source_key"] for source in sources})
        for source in sources:
            row = actual_by_source[source["source_key"]]
            event_id = source["event_ids"][0]
            expected_status = (
                "active"
                if events[event_id]["result_status"] == "in_progress"
                else "final_result"
            )
            self.assertEqual(row["image_file"], source["filename"])
            self.assertEqual(row["image_sha256"], source["sha256"])
            self.assertEqual(row["captured_at"], source["capture_timestamp_local"])
            self.assertEqual(row["battle_id"], event_id)
            self.assertEqual(row["screen_status"], expected_status)
            self.assertEqual(row["included_in_primary"], "True")

        archive_sha = sha256(archive)
        archive_size = len(archive)
        encoded = ARCHIVE_TEXT.read_bytes()
        for metadata_path in (BATCH / "phase1_checkpoint.json", BATCH / "batch_state.json"):
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            bundle = metadata["files"]["bundle"] if "files" in metadata else metadata["phase1"]["bundle"]
            self.assertEqual(bundle["sha256_archive"], archive_sha)
            self.assertEqual(bundle["bytes_archive"], archive_size)
            self.assertEqual(bundle["sha256_encoded_text"], sha256(encoded))
            self.assertEqual(bundle["bytes_encoded_text"], len(encoded))
            self.assertEqual(bundle["member_count"], len(members))

        self.assertEqual(ARCHIVE_CHECKSUM.read_text(encoding="utf-8").split()[0], archive_sha)
        declared_member_hashes = {
            line.split(maxsplit=1)[1]: line.split(maxsplit=1)[0]
            for line in MEMBER_CHECKSUMS.read_text(encoding="utf-8").splitlines()
        }
        self.assertEqual(declared_member_hashes, {name: sha256(data) for name, data in members.items()})

    def test_preexisting_normalized_evidence_bytes_are_unchanged(self) -> None:
        _, members = load_archive()
        self.assertEqual(
            {name: sha256(members[name]) for name in IMMUTABLE_EVIDENCE_HASHES},
            IMMUTABLE_EVIDENCE_HASHES,
        )


if __name__ == "__main__":
    unittest.main()
