"""Feature: RoT S-tier archers must resolve bows so role_scores_v1 sees ranged."""

from __future__ import annotations

import unittest
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
EQ = REPO / "data/realm_of_thrones/audit/realm_of_thrones_troop_equipment_audit.csv"
SCORES = (
    REPO
    / "analysis/theoretical/realm_of_thrones/export_20260729_025002"
    / "realm_of_thrones_troop_role_scores_v1.csv"
)

S_TIER_BOWS = {
    "ravens_teeth": "ravens_teeth_longbow",
    "summer_master_longbowman": "goldenheart_longbow",
}


class RotStierRangedAuditFixTests(unittest.TestCase):
    def test_equipment_audit_resolves_s_tier_longbows(self) -> None:
        eq = pd.read_csv(EQ)
        for troop_id, bow_id in S_TIER_BOWS.items():
            rows = eq[(eq["troop_id"] == troop_id) & (eq["item_id"] == bow_id)]
            self.assertFalse(rows.empty, f"missing {bow_id} on {troop_id}")
            row = rows.iloc[0]
            self.assertTrue(bool(row["item_found"]), troop_id)
            self.assertEqual(row["type"], "Bow", troop_id)

    def test_theoretical_scores_mark_s_tier_as_ranged(self) -> None:
        self.assertTrue(SCORES.is_file(), "run run_theoretical_role_scores.py first")
        scores = pd.read_csv(SCORES)
        for troop_id in (*S_TIER_BOWS, "myrish_artisan"):
            row = scores.loc[scores["troop_id"] == troop_id].iloc[0]
            self.assertTrue(bool(row["has_ranged"]), troop_id)
            self.assertEqual(row["primary_category"], "Ranged Troops", troop_id)
            self.assertGreater(float(row["ranged_role_score"]), 80.0, troop_id)


if __name__ == "__main__":
    unittest.main()
