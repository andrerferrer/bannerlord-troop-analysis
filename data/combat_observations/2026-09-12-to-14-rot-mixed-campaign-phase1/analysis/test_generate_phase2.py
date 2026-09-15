#!/usr/bin/env python3
"""Focused contract tests for this batch's deterministic Phase 2 generator."""

from __future__ import annotations

import importlib.util
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
            "46d9010bd6be2d9121539b2408a9da91f228a67ca5b08f4b9ced8e7abca7d59c",
        )
        self.assertEqual(validation["battles"], 15)
        self.assertEqual(validation["context_events"], {"field": 8, "siege_attack": 7})
        self.assertEqual(validation["ordinary_occurrences"], 155)
        self.assertEqual(validation["excluded_character_occurrences"], 77)
        self.assertEqual(validation["visible_rows"], 232)
        self.assertEqual(validation["partial_ordinary_occurrences"], 3)
        self.assertTrue(validation["visible_row_partition_exact"])
        self.assertTrue(validation["ordinary_partition_exact"])
        self.assertEqual(validation["pressure_margin_final_battles"], 12)
        self.assertEqual(validation["pressure_margin_censored_snapshots"], 3)
        self.assertFalse(validation["contexts_pooled"])
        self.assertFalse(validation["player_enemy_pooled"])
        self.assertFalse(validation["offscreen_rows_inferred"])
        self.assertEqual(result["analysis_state"]["queue_change"], "none")


if __name__ == "__main__":
    unittest.main()
