import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/analysis/generate_archer_like_mounted_melee_candidates.py"


class ArcherLikeMountedMeleeCandidateTest(unittest.TestCase):
    def test_repository_audit_produces_expected_structural_screen(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "candidates.csv"
            subprocess.run(
                [sys.executable, str(SCRIPT), "--output", str(output)],
                cwd=ROOT,
                check=True,
            )
            with output.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))

        by_id = {row["canonical_troop_id"]: row for row in rows}
        self.assertEqual(
            set(by_id),
            {
                "arryn_moonknight",
                "dayne_starfall_knights",
                "mallister_knight",
                "mounted_kingsguard",
                "realm_paladin",
            },
        )
        self.assertEqual(by_id["mounted_kingsguard"]["screen_band"], "captain_like_strict")
        self.assertEqual(by_id["mounted_kingsguard"]["melee_skill_floor"], "270.0")
        self.assertEqual(by_id["mounted_kingsguard"]["three_mode_rosters"], "1")
        self.assertEqual(by_id["arryn_moonknight"]["roster_count"], "2")
        self.assertEqual(by_id["mallister_knight"]["screen_band"], "near_match_test_queue")


if __name__ == "__main__":
    unittest.main()
