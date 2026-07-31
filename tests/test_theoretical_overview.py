"""Filtered theoretical OVERVIEW.md must exclude spectacle units."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT_ID = "export_20260729_025002"


class TheoreticalOverviewTests(unittest.TestCase):
    def test_rot_overview_excludes_mammoth_giant_from_ranged_top(self) -> None:
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
        # Top ranged section should not lead with spectacle units.
        ranged = text.split("## Top 20 — Ranged", 1)[1].split("## Top 20 —", 1)[0]
        self.assertNotIn("Mammoth Riding Giant", ranged)
        self.assertNotIn("Giant Archer", ranged)
        self.assertIn("Myrish Artisan of War", ranged)

    def test_human_input_doc_exists(self) -> None:
        path = REPO / "analysis" / "theoretical" / "HUMAN_INPUT.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("TAOM item XML export", text)
        self.assertIn("RoT field empiria", text)


if __name__ == "__main__":
    unittest.main()
