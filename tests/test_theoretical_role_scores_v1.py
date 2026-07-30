"""Theoretical role_scores_v1 outputs for mod tracks (ADR-004)."""

from __future__ import annotations

import csv
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT_ID = "export_20260729_025002"
TRACKS = ("nightmare_sails", "taom", "realm_of_thrones")
REQUIRED = (
    "REPORT.md",
    "README.md",
    "{track}_troop_role_scores_v1.csv",
    "{track}_primary_category_rankings_v1.csv",
    "{track}_roster_role_scores_v1.csv",
    "{track}_sanity_role_scores_v1.csv",
    "ranged_troops.csv",
    "defensive_troops.csv",
    "offensive_melee.csv",
    "skirmishers.csv",
    "meta.json",
)


class TheoreticalRoleScoresTests(unittest.TestCase):
    def test_outputs_exist_with_evidence_basis(self) -> None:
        for track in TRACKS:
            out = REPO / "analysis" / "theoretical" / track / EXPORT_ID
            self.assertTrue(out.is_dir(), f"missing {out}")
            for pattern in REQUIRED:
                name = pattern.format(track=track)
                path = out / name
                self.assertTrue(path.is_file(), f"missing {path}")
            troop_csv = out / f"{track}_troop_role_scores_v1.csv"
            with troop_csv.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertGreater(len(rows), 0, track)
            self.assertIn("evidence_basis", rows[0])
            self.assertIn("empirical", rows[0])
            self.assertTrue(
                all(row["evidence_basis"] == "xml_structural" for row in rows)
            )
            self.assertTrue(all(row["empirical"] == "false" for row in rows))

    def test_reports_cite_adr_004_and_export(self) -> None:
        for track in TRACKS:
            report = (
                REPO / "analysis" / "theoretical" / track / EXPORT_ID / "REPORT.md"
            ).read_text(encoding="utf-8")
            self.assertIn("ADR-004", report)
            self.assertIn(EXPORT_ID, report)
            self.assertIn("xml_structural", report)
            self.assertIn("role_scores_v1", report)


if __name__ == "__main__":
    unittest.main()
