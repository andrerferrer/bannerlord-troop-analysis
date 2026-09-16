#!/usr/bin/env python3
"""Focused contract tests for this batch's deterministic Phase 2 generator."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parent
GENERATOR_PATH = ANALYSIS_DIR / "generate_phase2.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("mixed_campaign_phase2", GENERATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Phase 2 generator: {GENERATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Phase2ContractTest(unittest.TestCase):
    def test_verified_batch_partition_and_queue_decision(self) -> None:
        result = load_generator().build_analysis(write_outputs=False)
        validation = result["validation"]

        self.assertEqual(
            result["input_verification"]["normalized_bundle"]["sha256"],
            "99754ec7fb614e86631bd6268c327140cd7c7882db7f612035015a6291b3adab",
        )
        self.assertEqual(result["input_verification"]["normalized_bundle"]["members"], 11)
        self.assertEqual(
            result["input_verification"]["screenshot_manifest"],
            {
                "status": "verified_repository_archive_exact",
                "sha256": "42edb4f73e88bad528ff318c019b561ccd3bf02b4151dd714ea08325ed0734dd",
                "rows": 16,
                "battle_ids": 15,
                "active_screens": 3,
                "final_result_screens": 13,
                "repository_archive_bytes_equal": True,
            },
        )
        self.assertEqual(validation["battles"], 15)
        self.assertEqual(validation["context_events"], {"field": 8, "siege_attack": 7})
        self.assertEqual(validation["ordinary_occurrences"], 155)
        self.assertTrue(validation["ordinary_occurrences_unique_within_battle"])
        self.assertEqual(validation["excluded_character_occurrences"], 77)
        self.assertEqual(validation["visible_rows"], 232)
        self.assertEqual(validation["partial_ordinary_occurrences"], 3)
        self.assertEqual(validation["partition_rows"], 95)
        self.assertEqual(validation["reliable_rows"], 7)
        self.assertEqual(validation["reliable_provisional_identity_rows"], 1)
        self.assertEqual(validation["insufficient_rows"], 88)
        self.assertTrue(validation["visible_row_partition_exact"])
        self.assertTrue(validation["ordinary_partition_exact"])
        self.assertEqual(validation["pressure_margin_final_battles"], 12)
        self.assertEqual(validation["pressure_margin_censored_snapshots"], 3)
        self.assertFalse(validation["contexts_pooled"])
        self.assertFalse(validation["player_enemy_pooled"])
        self.assertFalse(validation["offscreen_rows_inferred"])
        self.assertFalse(validation["final_active_observations_pooled"])
        self.assertEqual(validation["outlier_analysis_status"], "not_run_no_predeclared_campaign_outlier_rule")
        self.assertEqual(validation["primary_outlier_exclusions"], 0)
        self.assertEqual(result["analysis_state"]["queue_change"], "none")
        self.assertEqual(
            result["input_verification"]["handoff_inventory"]["missing_inputs"],
            [],
        )
        self.assertEqual(result["input_verification"]["handoff_inventory"]["verified_count"], 11)
        self.assertEqual(result["input_verification"]["handoff_inventory"]["status"], "passed")
        self.assertNotIn("blocker", result["input_verification"]["handoff_inventory"])
        self.assertEqual(result["input_verification"]["status"], "passed")
        self.assertEqual(validation["status"], "passed_with_documented_identity_limits")
        self.assertEqual(validation["validation_errors"], [])
        self.assertEqual(result["analysis_state"]["status"], "phase_2_complete_local_validation_passed")
        self.assertEqual(result["analysis_state"]["blockers"], [])

        below_gate = [row for row in result["rankings"] if not row["numeric_display_gate_passed"]]
        self.assertTrue(below_gate)
        for row in below_gate:
            self.assertEqual(row["efficiency_rank"], "")
            self.assertEqual(row["impact_rank"], "")
            self.assertEqual(row["kills_per_deployed"], "")
            self.assertEqual(row["player_side_kill_share"], "")
            self.assertEqual(row["player_side_deployment_share"], "")
            self.assertEqual(row["offensive_contribution_ratio"], "")
            self.assertEqual(row["retention_rate"], "")
            self.assertEqual(row["death_rate"], "")
            self.assertEqual(row["casualty_rate"], "")

        forest = next(row for row in result["identity_audit"] if row["display_name"] == "Forest Bandit")
        self.assertEqual(forest["resolution_status"], "unresolved_provisional_label")
        self.assertEqual(forest["canonical_troop_id"], "")
        self.assertEqual(forest["non_soldier_exact_match_ids"], "forest_bandits_chief")

    def test_repository_archive_manifest_divergence_is_rejected(self) -> None:
        generator = load_generator()
        files, _ = generator.extract_verified_bundle()
        source_manifest = json.loads(files["source_manifest.json"])
        events = {
            row["event_id"]: row
            for row in map(json.loads, files["normalized/events.jsonl"].splitlines())
        }
        files["screenshots_manifest.csv"] += b"\n"

        with self.assertRaisesRegex(
            ValueError,
            "repository/archive screenshots_manifest.csv bytes differ",
        ):
            generator.verify_screenshot_manifest(
                files,
                {row["source_key"]: row for row in source_manifest["sources"]},
                events,
            )


if __name__ == "__main__":
    unittest.main()
