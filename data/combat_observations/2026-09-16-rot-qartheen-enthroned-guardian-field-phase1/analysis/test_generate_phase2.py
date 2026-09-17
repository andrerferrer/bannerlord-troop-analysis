#!/usr/bin/env python3
"""Regression tests for the deterministic PR #101 Phase 2 generator."""

from __future__ import annotations

import csv
import json
import subprocess
import unittest
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parent
GENERATOR = ANALYSIS_DIR / "generate_phase2.py"
REVIEW_DIR = ANALYSIS_DIR.parent / "reviewed"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class Phase2GenerationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(["python3", str(GENERATOR), "--check"], check=True)

    def test_visible_row_partition_and_gate_partition(self) -> None:
        ordinary = read_csv(ANALYSIS_DIR / "ordinary_occurrences.csv")
        characters = read_csv(ANALYSIS_DIR / "excluded_character_rows.csv")
        reliable = read_csv(ANALYSIS_DIR / "ranking_reliable.csv")
        insufficient = read_csv(ANALYSIS_DIR / "insufficient_evidence.csv")
        self.assertEqual(len(ordinary), 13)
        self.assertEqual(len(characters), 18)
        self.assertEqual(len(reliable), 0)
        self.assertEqual(len(insufficient), 12)
        self.assertEqual(len(reliable) + len(insufficient), 12)
        self.assertTrue(all(row["efficiency_rank"] == "" and row["impact_rank"] == "" for row in insufficient))

    def test_guardian_cohorts_are_recomputed_and_separate(self) -> None:
        rows = {row["cohort_view"]: row for row in read_csv(ANALYSIS_DIR / "guardian_cohort_comparison.csv")}
        self.assertEqual(set(rows), {"historical_mixed_campaign", "new_follow_up", "combined_descriptive_continuity"})
        expected = {
            "historical_mixed_campaign": ("5", "195", "698"),
            "new_follow_up": ("2", "173", "138"),
            "combined_descriptive_continuity": ("7", "368", "836"),
        }
        for key, values in expected.items():
            self.assertEqual(
                (rows[key]["independent_battles"], rows[key]["deployed"], rows[key]["kills"]),
                values,
            )
        self.assertEqual(rows["new_follow_up"]["numeric_display_gate_passed"], "false")
        self.assertEqual(rows["combined_descriptive_continuity"]["interpretation"], "descriptive_non_causal")

    def test_identity_uncertainty_and_review_layer_are_preserved(self) -> None:
        ordinary = read_csv(ANALYSIS_DIR / "ordinary_occurrences.csv")
        unresolved = [row for row in ordinary if row["raw_name"] == ""]
        dornish = [row for row in ordinary if row["raw_name"] == "Dornish Archer"]
        self.assertEqual(len(unresolved), 1)
        self.assertEqual(unresolved[0]["identity_status"], "unresolved_label")
        self.assertEqual(dornish[0]["identity_status"], "unresolved_provisional_label")
        review = read_csv(REVIEW_DIR / "review_resolutions.csv")
        self.assertEqual(len(review), 4)
        self.assertTrue(all(row["resolution_action"] == "preserve_without_guessing" for row in review))

    def test_validation_and_queue_decision(self) -> None:
        validation = json.loads((ANALYSIS_DIR / "validation_report.json").read_text())
        state = json.loads((ANALYSIS_DIR / "analysis_state.json").read_text())
        queue = json.loads((ANALYSIS_DIR / "queue_validation.json").read_text())
        self.assertEqual(validation["status"], "passed_with_documented_limits")
        self.assertTrue(validation["ordinary_partition_exact"])
        self.assertFalse(validation["pr100_cohort_pooled"])
        self.assertEqual(state["queue_change"], "none_already_closed_on_main")
        self.assertEqual(queue["active_test_after"], None)
        self.assertEqual(queue["ordered_queue_after"], [])
        self.assertEqual(queue["verification_holds_after"], ["arryn_moonknight"])

    def test_required_contract_artifacts_and_pins(self) -> None:
        required = {
            "unresolved_rows.csv", "outlier_report.csv", "battle_context_review.csv",
            "battle_pressure_margin.csv", "canonical_validation_report.json",
            "empirical_analysis_summary.md",
        }
        self.assertTrue(all((ANALYSIS_DIR / name).is_file() for name in required))
        pressure = read_csv(ANALYSIS_DIR / "battle_pressure_margin.csv")
        self.assertEqual([row["pressure_margin"] for row in pressure], ["1.000000", "0.911765"])
        self.assertTrue(all(row["frontline_status"] == "not_designated_in_mixed_campaign_evidence" for row in pressure))
        verification = json.loads((ANALYSIS_DIR / "input_verification.json").read_text())
        self.assertEqual(verification["identity_audit"]["commit"], "03e56761316704ee44921368a751fb14b66d475c")
        pins = verification["historical_cohort_pins"] + verification["pr100_decision_cohort_pins"]
        self.assertTrue(all(pin["worktree_bytes_equal_pinned_commit"] for pin in pins))


if __name__ == "__main__":
    unittest.main()
