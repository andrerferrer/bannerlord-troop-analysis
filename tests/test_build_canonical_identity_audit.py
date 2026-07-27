from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "analysis" / "build_canonical_identity_audit.py"
spec = importlib.util.spec_from_file_location("canonical_builder", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class CanonicalIdentityResolverTests(unittest.TestCase):
    def test_tier_suffix_is_not_part_of_identity(self):
        self.assertEqual(
            module.normalize_display_name("Queen's Man [T6]"),
            module.normalize_display_name("Queen's Man"),
        )

    def test_unique_exact_match_confirms_id(self):
        row = {"canonical_name_slug": "queen_s_man_t6", "display_name": "Queen's Man [T6]"}
        candidates = {
            module.normalize_display_name("Queen's Man"): [
                module.Candidate("realm_of_thrones", "queens_man", "Queen's Man", "rot_troops.csv")
            ]
        }
        resolved = module.resolve_row(row, None, candidates)
        self.assertEqual(resolved["match_status"], module.CONFIRMED)
        self.assertEqual(resolved["canonical_troop_id"], "queens_man")

    def test_historical_exact_match_preserves_machine_readable_evidence_tier(self):
        row = {"canonical_name_slug": "riverlands_ranger_t5", "display_name": "Riverlands Ranger [T5]"}
        candidates = {
            module.normalize_display_name("Riverlands Ranger"): [
                module.Candidate(
                    "realm_of_thrones",
                    "river_ranger",
                    "Riverlands Ranger",
                    "SOURCE_PR_BODY.md",
                    module.HISTORICAL_REPORTED_EXACT,
                )
            ]
        }
        resolved = module.resolve_row(row, None, candidates)
        self.assertEqual(resolved["match_status"], module.CONFIRMED)
        self.assertEqual(
            resolved["resolution_method"],
            "historical_pr_reported_exact_name",
        )

    def test_cross_track_duplicate_is_ambiguous(self):
        row = {"canonical_name_slug": "reaver_t4", "display_name": "Reaver [T4]"}
        key = module.normalize_display_name("Reaver")
        candidates = {
            key: [
                module.Candidate("realm_of_thrones", "rot_reaver", "Reaver", "rot.csv"),
                module.Candidate("other_mod", "other_reaver", "Reaver", "other.csv"),
            ]
        }
        resolved = module.resolve_row(row, None, candidates)
        self.assertEqual(resolved["match_status"], "ambiguous_exact_name")
        self.assertEqual(resolved["candidate_count"], "2")

    def test_existing_confirmation_is_preserved_without_candidate(self):
        row = {"canonical_name_slug": "baratheon_hammerknight_t6", "display_name": "Baratheon Hammerknight [T6]"}
        existing = {
            "provisional_slug": "baratheon_hammerknight_t6",
            "display_name": "Baratheon Hammerknight [T6]",
            "observed_track": "realm_of_thrones",
            "canonical_troop_id": "baratheon_pikeknight",
            "match_status": "confirmed_id",
            "evidence_path": "v43.csv",
        }
        resolved = module.resolve_row(row, existing, {})
        self.assertEqual(resolved["match_status"], module.CONFIRMED)
        self.assertEqual(resolved["canonical_troop_id"], "baratheon_pikeknight")

    def test_conflicting_audit_blocks_existing_confirmation(self):
        row = {"canonical_name_slug": "baratheon_hammerknight_t6", "display_name": "Baratheon Hammerknight [T6]"}
        existing = {
            "observed_track": "realm_of_thrones",
            "canonical_troop_id": "baratheon_pikeknight",
            "match_status": "confirmed_id",
        }
        key = module.normalize_display_name("Baratheon Hammerknight")
        candidates = {
            key: [module.Candidate("realm_of_thrones", "different_id", "Baratheon Hammerknight", "rot.csv")]
        }
        resolved = module.resolve_row(row, existing, candidates)
        self.assertEqual(resolved["match_status"], "conflict_existing_vs_track_audit")
        self.assertEqual(resolved["canonical_troop_id"], "")


if __name__ == "__main__":
    unittest.main()
