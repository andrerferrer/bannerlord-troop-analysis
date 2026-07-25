from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.combat_observations.canonical import (
    apply_corrections,
    build_canonical_dataset,
    deduplicate_occurrences,
)
from scripts.combat_observations.domain import DomainError, read_jsonl, write_jsonl


def occurrence(
    observation_id: str,
    battle_id: str,
    troop_name: str,
    *,
    parent_group: str = "party-a",
    context: str = "field",
    survivors: int | None = 8,
    kills: int | None = 5,
    deaths: int | None = 1,
    wounded: int | None = 1,
    overlap_group_id: str | None = None,
    screenshot_group_id: str | None = None,
) -> dict[str, object]:
    return {
        "schema_version": "1.0.0-first-pass",
        "observation_id": observation_id,
        "battle_id": battle_id,
        "battle_context": context,
        "classification_source": "raw_extraction",
        "side": "attacker",
        "parent_group": parent_group,
        "row_type": "troop",
        "display_name_raw": troop_name,
        "canonical_troop_id": None,
        "relationship_to_player": "player_party",
        "source": {"image_file": f"{battle_id}.png", "image_sha256": (battle_id[-1] * 64)},
        "survivors": survivors,
        "kills": kills,
        "upgrade_ready": 0,
        "deaths": deaths,
        "wounded": wounded,
        "routed": 0,
        "analysis_status": "raw",
        "needs_review": kills is None,
        "uncertain_fields": ["kills"] if kills is None else [],
        "overlap_group_id": overlap_group_id,
        "screenshot_group_id": screenshot_group_id,
        "game": {"version": "1.4.x", "track": "vanilla_war_sails_1.4.x", "active_modules": []},
        "provenance": {"extractor_model": "fixture", "prompt_version": "fixture"},
    }


class CanonicalPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.registry = self.root / "troops.csv"
        with self.registry.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["troop_id", "name", "tier", "category"])
            writer.writeheader()
            writer.writerow({"troop_id": "imperial_naute", "name": "Imperial Naute", "tier": 5, "category": "Offensive Infantry"})
            writer.writerow({"troop_id": "battanian_skipari", "name": "Battanian Skipari", "tier": 5, "category": "Offensive Infantry"})

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_corrections_preserve_raw_and_reject_drift(self) -> None:
        raw = [occurrence("obs-1", "battle-1", "Imperial Naute", kills=None)]
        decision = {
            "review_id": "review-1",
            "observation_id": "obs-1",
            "field_path": "kills",
            "original_value": None,
            "corrected_value": 6,
            "resolution_status": "canonical",
        }
        reviewed, resolutions, unresolved = apply_corrections(raw, [decision])
        self.assertIsNone(raw[0]["kills"])
        self.assertEqual(reviewed[0]["kills"], 6)
        self.assertEqual(len(resolutions), 1)
        self.assertFalse(unresolved)
        bad = {**decision, "original_value": 99}
        with self.assertRaisesRegex(DomainError, "original value mismatch"):
            apply_corrections(raw, [bad])

    def test_deduplication_requires_explicit_overlap_identity(self) -> None:
        one = occurrence("obs-1", "battle-1", "Imperial Naute", overlap_group_id="overlap", screenshot_group_id="screens")
        two = occurrence("obs-2", "battle-1", "Imperial Naute", overlap_group_id="overlap", screenshot_group_id="screens")
        retained, report = deduplicate_occurrences([one, two])
        self.assertEqual(len(retained), 1)
        self.assertEqual(report[0]["status"], "deduplicated_proven_overlap")

        different_party = occurrence("obs-3", "battle-1", "Imperial Naute", parent_group="party-b")
        retained, _ = deduplicate_occurrences([one, different_party])
        self.assertEqual(len(retained), 2)

        ambiguous = occurrence("obs-4", "battle-1", "Imperial Naute")
        retained, report = deduplicate_occurrences([occurrence("obs-5", "battle-1", "Imperial Naute"), ambiguous])
        self.assertEqual(len(retained), 2)
        self.assertEqual(report[0]["status"], "candidate_preserved")

        missing_screenshot_identity = occurrence(
            "obs-6",
            "battle-1",
            "Imperial Naute",
            overlap_group_id="overlap",
        )
        retained, report = deduplicate_occurrences(
            [
                missing_screenshot_identity,
                occurrence(
                    "obs-7",
                    "battle-1",
                    "Imperial Naute",
                    overlap_group_id="overlap",
                ),
            ]
        )
        self.assertEqual(len(retained), 2)
        self.assertEqual(report[0]["status"], "candidate_preserved")

    def test_end_to_end_is_deterministic_and_raw_immutable(self) -> None:
        raw_path = self.root / "raw.jsonl"
        records = [
            occurrence("obs-1", "battle-1", "Imperial Naute", overlap_group_id="o1", screenshot_group_id="s1"),
            occurrence("obs-2", "battle-1", "Imperial Naute", overlap_group_id="o1", screenshot_group_id="s1"),
            occurrence("obs-3", "battle-2", "Imperial Naute", kills=10),
            occurrence("obs-4", "battle-3", "Battanian Skipari", context="siege_attack", kills=7),
        ]
        records[1]["source"] = records[0]["source"]
        write_jsonl(raw_path, records)
        raw_before = raw_path.read_bytes()
        first = self.root / "first"
        second = self.root / "second"
        first_report = build_canonical_dataset(raw_path, first, self.registry)
        second_report = build_canonical_dataset(raw_path, second, self.registry)
        self.assertEqual(first_report, second_report)
        self.assertEqual(raw_before, raw_path.read_bytes())
        self.assertTrue(first_report["raw_input_unchanged"])
        self.assertEqual(first_report["schema_errors"], [])
        self.assertEqual(first_report["counts"]["primary_occurrences"], 3)

        first_files = sorted(path.relative_to(first) for path in first.rglob("*") if path.is_file())
        second_files = sorted(path.relative_to(second) for path in second.rglob("*") if path.is_file())
        self.assertEqual(first_files, second_files)
        for relative in first_files:
            self.assertEqual((first / relative).read_bytes(), (second / relative).read_bytes(), relative)

        aggregates = read_jsonl(first / "canonical/canonical_historical_aggregates.jsonl")
        naute_overall = next(
            row for row in aggregates
            if row["canonical_troop_id"] == "imperial_naute" and row["battle_context"] == "overall"
        )
        self.assertEqual(naute_overall["total_deployed"], 20)
        self.assertEqual(naute_overall["total_kills"], 15)
        self.assertEqual(naute_overall["historical_kills_per_deployed"], "0.750000")
        self.assertEqual(naute_overall["context_distribution"], {"field": 2})
        self.assertEqual(naute_overall["variation_by_battle"], "0.250000")
        self.assertIn(naute_overall["best_battle_id"], {"battle-1", "battle-2"})

    def test_unresolved_critical_value_is_quarantined(self) -> None:
        raw_path = self.root / "raw-unresolved.jsonl"
        write_jsonl(raw_path, [occurrence("obs-1", "battle-1", "Imperial Naute", kills=None)])
        corrections = self.root / "corrections.jsonl"
        write_jsonl(
            corrections,
            [
                {
                    "review_id": "review-1",
                    "observation_id": "obs-1",
                    "field_path": "kills",
                    "original_value": None,
                    "original_raw_text": "?",
                    "corrected_value": None,
                    "resolution_status": "unresolved",
                    "correction_source": "source_image",
                    "reviewer": "fixture",
                    "reviewed_at": "2026-07-24T00:00:00Z",
                    "reason": "unreadable",
                    "source_image_sha256": "1" * 64,
                }
            ],
        )
        report = build_canonical_dataset(
            raw_path,
            self.root / "unresolved-output",
            self.registry,
            corrections_path=corrections,
        )
        self.assertEqual(report["counts"]["primary_occurrences"], 0)
        self.assertEqual(report["counts"]["quarantined_occurrences"], 1)

    def test_duplicate_observation_id_is_rejected(self) -> None:
        duplicate = occurrence("obs-1", "battle-1", "Imperial Naute")
        with self.assertRaisesRegex(DomainError, "duplicate raw observation_id"):
            apply_corrections([duplicate, duplicate], [])

    def test_invalid_existing_identity_is_quarantined(self) -> None:
        raw_path = self.root / "raw-invalid-id.jsonl"
        record = occurrence("obs-1", "battle-1", "Imperial Naute")
        record["canonical_troop_id"] = "not_in_registry"
        write_jsonl(raw_path, [record])
        output = self.root / "invalid-id-output"
        report = build_canonical_dataset(raw_path, output, self.registry)
        self.assertEqual(report["counts"]["primary_occurrences"], 0)
        self.assertEqual(report["counts"]["quarantined_occurrences"], 1)
        canonical = read_jsonl(output / "canonical/canonical_occurrences.jsonl")
        self.assertIsNone(canonical[0]["canonical_troop_id"])

    def test_conflicting_battle_context_is_quarantined(self) -> None:
        raw_path = self.root / "raw-conflict.jsonl"
        write_jsonl(
            raw_path,
            [
                occurrence("obs-1", "battle-1", "Imperial Naute", context="field"),
                occurrence("obs-2", "battle-1", "Battanian Skipari", context="siege_attack"),
            ],
        )
        report = build_canonical_dataset(
            raw_path,
            self.root / "context-conflict-output",
            self.registry,
        )
        self.assertEqual(report["counts"]["primary_occurrences"], 0)
        self.assertEqual(report["counts"]["quarantined_occurrences"], 2)
        self.assertTrue(
            any(
                "inconsistent_battle_context" in error["error"]
                for error in report["semantic_errors"]
            )
        )

    def test_undefined_context_does_not_enter_rankings(self) -> None:
        raw_path = self.root / "raw-undefined.jsonl"
        write_jsonl(
            raw_path,
            [occurrence("obs-1", "battle-1", "Imperial Naute", context="undefined")],
        )
        output = self.root / "undefined-output"
        report = build_canonical_dataset(raw_path, output, self.registry)
        self.assertEqual(report["counts"]["primary_occurrences"], 0)
        self.assertEqual(report["counts"]["historical_aggregates"], 0)


if __name__ == "__main__":
    unittest.main()
