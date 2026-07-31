"""Mod-track OVERVIEW lists: full mod-owned ranks; no name/specials filters."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT_ID = "export_20260729_025002"


class TheoreticalOverviewTests(unittest.TestCase):
    def test_rot_overview_keeps_mod_troops_drops_vanilla_baseline(self) -> None:
        path = (
            REPO
            / "analysis"
            / "theoretical"
            / "realm_of_thrones"
            / EXPORT_ID
            / "OVERVIEW.md"
        )
        self.assertTrue(path.is_file(), "run write_theoretical_overview.py first")
        text = path.read_text(encoding="utf-8")
        ranged = text.split("## Ranked — Ranged", 1)[1].split("## Ranked —", 1)[0]
        self.assertIn("Myrish Artisan of War", ranged)
        self.assertIn("Ravens' Teeth", ranged)
        self.assertIn("Goldenheart Warrior", ranged)
        # Name filters removed — spectacle / Greyjoy lines may appear.
        self.assertNotIn("Khuzait Khan's Guard", ranged)
        self.assertNotIn("Battanian Fian Champion", ranged)
        self.assertIn("change_type=inalterado", text)
        self.assertNotIn("Drop troop names matching", text)

    def test_human_input_doc_exists(self) -> None:
        path = REPO / "analysis" / "theoretical" / "HUMAN_INPUT.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("TAOM item XML export", text)
        self.assertIn("RoT field empiria", text)


if __name__ == "__main__":
    unittest.main()
