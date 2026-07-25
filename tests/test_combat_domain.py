from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.combat_observations.domain import (
    DomainError,
    TroopMatcher,
    derived_metrics,
    evidence_grade,
)
from scripts.combat_observations.review import categorize_review_row, triage_review_queue


class DomainTests(unittest.TestCase):
    def test_deployed_rates_and_routed_policy(self) -> None:
        metrics = derived_metrics(
            {
                "observation_id": "obs",
                "survivors": 7,
                "kills": 5,
                "upgrade_ready": 2,
                "deaths": 1,
                "wounded": 2,
                "routed": 4,
            }
        )
        self.assertEqual(metrics["deployed"], 10)
        self.assertEqual(metrics["casualties"], 3)
        self.assertEqual(metrics["kills_per_deployed"], "0.500000")
        self.assertEqual(metrics["routed_rate"], "0.400000")

    def test_null_and_zero_division(self) -> None:
        metrics = derived_metrics(
            {
                "observation_id": "obs",
                "survivors": 0,
                "kills": 0,
                "upgrade_ready": None,
                "deaths": 0,
                "wounded": 0,
                "routed": 0,
            }
        )
        self.assertEqual(metrics["deployed"], 0)
        self.assertIsNone(metrics["kills_per_deployed"])
        with self.assertRaises(DomainError):
            derived_metrics(
                {
                    "observation_id": "bad",
                    "survivors": -1,
                    "kills": 0,
                    "deaths": 0,
                    "wounded": 0,
                    "routed": 0,
                    "upgrade_ready": 0,
                }
            )

    def test_evidence_grade_requires_both_thresholds(self) -> None:
        self.assertEqual(evidence_grade(300, 1), "exploratory")
        self.assertEqual(evidence_grade(20, 4), "low")
        self.assertEqual(evidence_grade(80, 3), "medium")
        self.assertEqual(evidence_grade(150, 6), "high")
        self.assertEqual(evidence_grade(500, 2), "low")

    def test_troop_matching_order_and_collision(self) -> None:
        matcher = TroopMatcher(
            [("imperial_naute", "Imperial Naute"), ("imperial_nauta", "Imperial Nauta")],
            [("Naute", "imperial_naute")],
        )
        self.assertEqual(matcher.match("Imperial Naute")["method"], "exact")
        self.assertEqual(matcher.match("IMPERIAL  NAUTE")["method"], "normalized_exact")
        self.assertEqual(matcher.match("Naute")["method"], "alias")
        self.assertEqual(matcher.match("Imperial Naut")["status"], "ambiguous")
        with self.assertRaisesRegex(DomainError, "alias collision"):
            TroopMatcher(
                [("one", "One"), ("two", "Two")],
                [("shared", "one"), ("Shared", "two")],
            )

    def test_review_priority_and_categories(self) -> None:
        categorized = categorize_review_row(
            {
                "observation_id": "obs-1",
                "row_type": "troop",
                "analysis_status": "primary",
                "canonical_troop_id": "",
                "uncertain_fields": '["kills", "canonical_troop_id"]',
                "battle_context": "undefined",
            }
        )
        self.assertEqual(categorized["priority"], 1)
        self.assertTrue(categorized["ranking_impact"])
        self.assertIn("numeric_uncertainty", categorized["categories"])
        self.assertIn("ambiguous_troop_name", categorized["categories"])
        self.assertIn("battle_context_uncertainty", categorized["categories"])
        self.assertTrue(categorized["image_inspection_required"])

    def test_triage_outputs_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "review.csv"
            with source.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "observation_id", "row_type", "analysis_status", "canonical_troop_id",
                        "uncertain_fields", "battle_context",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "observation_id": "obs-1",
                        "row_type": "troop",
                        "analysis_status": "primary",
                        "canonical_troop_id": "",
                        "uncertain_fields": "kills",
                        "battle_context": "field",
                    }
                )
            first = root / "first"
            second = root / "second"
            self.assertEqual(triage_review_queue(source, first), triage_review_queue(source, second))
            for name in ("review_queue_categorized.csv", "review_progress.json", "review_category_summary.csv"):
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
