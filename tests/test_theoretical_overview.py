"""Mod-track OVERVIEW lists: full mod-owned ranks; no name/specials filters."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT_ID = "export_20260729_025002"
sys.path.insert(0, str(REPO / "scripts" / "scoring"))

from write_theoretical_overview import (  # noqa: E402
    LATEST_REPORT_END,
    LATEST_REPORT_START,
    update_root_readme_latest_report,
)


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

    def test_update_root_readme_rewrites_latest_report_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            readme = repo / "README.md"
            readme.write_text(
                "\n".join(
                    [
                        "# Bannerlord Troop Analysis",
                        "",
                        "## Start here",
                        "",
                        "- older link",
                        "",
                        LATEST_REPORT_START,
                        "stale content",
                        LATEST_REPORT_END,
                        "",
                        "## Batch workflow",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            update_root_readme_latest_report(repo, package_sha="abc123")
            text = readme.read_text(encoding="utf-8")
            self.assertIn(LATEST_REPORT_START, text)
            self.assertIn(LATEST_REPORT_END, text)
            self.assertNotIn("stale content", text)
            self.assertIn(f"analysis/theoretical/OVERVIEW_INDEX.md", text)
            self.assertIn(EXPORT_ID, text)
            self.assertIn(
                f"analysis/theoretical/realm_of_thrones/{EXPORT_ID}/OVERVIEW.md",
                text,
            )
            self.assertIn("Batch workflow", text)

    def test_root_readme_has_latest_report_markers(self) -> None:
        text = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn(LATEST_REPORT_START, text)
        self.assertIn(LATEST_REPORT_END, text)
        self.assertIn("analysis/theoretical/OVERVIEW_INDEX.md", text)


if __name__ == "__main__":
    unittest.main()
