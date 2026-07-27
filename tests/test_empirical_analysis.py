from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.combat_observations.analysis import (
    build_tier_role_views,
    calibration_decision,
    compare_models,
)
from scripts.combat_observations.domain import write_jsonl


class EmpiricalAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.aggregates = self.root / "aggregates.jsonl"
        write_jsonl(
            self.aggregates,
            [
                {
                    "canonical_troop_id": "one",
                    "battle_context": "overall",
                    "battle_count": 5,
                    "total_deployed": 100,
                    "total_kills": 120,
                    "historical_kills_per_deployed": "1.200000",
                    "evidence_grade": "high",
                },
                {
                    "canonical_troop_id": "two",
                    "battle_context": "overall",
                    "battle_count": 3,
                    "total_deployed": 40,
                    "total_kills": 20,
                    "historical_kills_per_deployed": "0.500000",
                    "evidence_grade": "medium",
                },
                {
                    "canonical_troop_id": "one",
                    "battle_context": "field",
                    "battle_count": 5,
                    "total_deployed": 100,
                    "total_kills": 120,
                    "historical_kills_per_deployed": "1.200000",
                    "evidence_grade": "high",
                },
            ],
        )
        self.general = self.root / "general.csv"
        self.burst = self.root / "burst.csv"
        with self.general.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["troop_id", "name", "total_score_v71", "tier", "category"])
            writer.writeheader()
            writer.writerow({"troop_id": "one", "name": "One", "total_score_v71": 90, "tier": 5, "category": "Infantry"})
            writer.writerow({"troop_id": "two", "name": "Two", "total_score_v71": 50, "tier": 4, "category": "Archer"})
        with self.burst.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["troop_id", "name", "burst_score_v73"])
            writer.writeheader()
            writer.writerow({"troop_id": "one", "name": "One", "burst_score_v73": 80})
            writer.writerow({"troop_id": "two", "name": "Two", "burst_score_v73": 40})

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_model_comparison_keeps_models_separate(self) -> None:
        output = self.root / "comparison"
        summary = compare_models(self.aggregates, self.general, self.burst, output)
        self.assertEqual(summary["status"], "authoritative")
        self.assertEqual(summary["general_v71"]["rank_correlation"], 1.0)
        self.assertEqual(summary["burst_v73"]["rank_correlation"], 1.0)
        header = (output / "model_vs_empirical.csv").read_text(encoding="utf-8").splitlines()[0]
        self.assertIn("general_score_v71", header)
        self.assertIn("burst_score_v73", header)

    def test_tier_role_views_and_calibration_gate(self) -> None:
        output = self.root / "views"
        report = build_tier_role_views(self.aggregates, self.general, output)
        self.assertEqual(report["status"], "complete")
        self.assertTrue(any(name.startswith("ranking_tier_") for name in report["generated_views"]))

        comparison = self.root / "comparison"
        compare_models(self.aggregates, self.general, self.burst, comparison)
        decision = calibration_decision(
            comparison / "empirical_analysis_summary.json",
            self.aggregates,
            self.root / "calibration.json",
        )
        self.assertEqual(decision["decision"], "no_model_change")
        self.assertEqual(decision["frozen_models"], ["v7.1", "v7.3"])

    def test_zero_deployment_aggregate_does_not_crash_comparison(self) -> None:
        write_jsonl(
            self.aggregates,
            [
                {
                    "canonical_troop_id": "one",
                    "battle_context": "overall",
                    "battle_count": 1,
                    "total_deployed": 0,
                    "total_kills": 0,
                    "historical_kills_per_deployed": None,
                    "evidence_grade": "exploratory",
                }
            ],
        )
        summary = compare_models(
            self.aggregates,
            self.general,
            self.burst,
            self.root / "zero-comparison",
        )
        self.assertEqual(summary["canonical_overall_troops"], 0)
        self.assertEqual(summary["status"], "provisional_incomplete_model_universe")


if __name__ == "__main__":
    unittest.main()
