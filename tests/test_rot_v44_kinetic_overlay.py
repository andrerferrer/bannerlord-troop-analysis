from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from rot.rot_v44_kinetic_overlay import (  # noqa: E402
    apply_canonical,
    apply_sensitivity,
    build_item_lookup,
    resolve_exact_profile,
)


def v43_row(
    troop_id: str,
    item_id: str,
    *,
    mode: str = "melee",
    raw_damage: str = "60",
    melee_kpm: str = "5",
    melee_score: str = "70",
    rank: str = "1",
) -> dict[str, str]:
    return {
        "troop_id": troop_id,
        "name": troop_id.replace("_", " ").title(),
        "rank_v43": rank,
        "is_giant": "False",
        "v43_melee_mixed_kpm": melee_kpm,
        "v43_melee_carry_score": melee_score,
        "v43_melee_speed": "90",
        "v43_ranged_carry_score": "0",
        "v43_throw_carry_score": "0",
        "v43_weapon_mode": mode,
        "v43_weapon_offense_score": melee_score,
        "offense_v3c_norm": "",
        "v43_defense": "60",
        "v43_reliability": "70",
        "v43_emp_adjustment_robust": "0",
        "v43_robust_total": melee_score,
        "best_melee_item": item_id,
        "best_melee_raw_damage": raw_damage,
        "best_weapon_item": item_id,
        "best_weapon_raw_damage": raw_damage,
        "best_weapon_damage_type": "Cut",
        "total_v3c": "",
    }


def exact_sword(item_id: str) -> dict[str, str]:
    return {
        "item_id": item_id,
        "weapon_class": "OneHandedSword",
        "speed_rating": "90",
        "handling": "90",
        "weapon_length": "100",
        "weight": "1.3",
        "has_thrust": "true",
        "thrust_damage": "45",
        "thrust_speed": "81",
    }


class ProfileResolutionTests(unittest.TestCase):
    def test_exact_one_handed_sword_profile_is_applied(self):
        row = v43_row("swordsman", "test_sword")
        lookup = build_item_lookup([exact_sword("test_sword")])
        resolution = resolve_exact_profile(row, lookup)
        self.assertEqual(resolution.status, "applied_exact")
        self.assertEqual(resolution.family, "onehand_sword")
        self.assertEqual(resolution.profile.reach, 100)
        self.assertTrue(resolution.profile.has_thrust)

    def test_exact_profile_requires_explicit_thrust_provenance(self):
        row = v43_row("swordsman", "test_sword")
        item = exact_sword("test_sword")
        del item["has_thrust"]
        resolution = resolve_exact_profile(row, build_item_lookup([item]))
        self.assertEqual(resolution.status, "missing_exact_profile")
        self.assertIn("has_thrust", resolution.missing_fields)

    def test_non_sword_family_remains_on_v43(self):
        row = v43_row("hammerman", "test_hammer")
        resolution = resolve_exact_profile(row, {})
        self.assertEqual(resolution.status, "unsupported_family")
        self.assertIsNone(resolution.profile)


class OverlayTests(unittest.TestCase):
    def test_canonical_overlay_applies_exact_sword_and_keeps_other_family(self):
        rows = [
            v43_row("swordsman", "test_sword", melee_kpm="6", rank="1"),
            v43_row("hammerman", "test_hammer", melee_kpm="5", rank="2"),
        ]
        ranked, audit, summary = apply_canonical(
            rows,
            build_item_lookup([exact_sword("test_sword")]),
            1.0,
        )
        audit_by_id = {row["troop_id"]: row for row in audit}
        self.assertEqual(audit_by_id["swordsman"]["kinetic_status"], "applied_exact")
        self.assertEqual(
            audit_by_id["hammerman"]["kinetic_status"],
            "unsupported_family",
        )
        self.assertEqual(summary["exact_profile_coverage"], 1.0)
        self.assertEqual({row["rank_v44"] for row in ranked}, {1, 2})

    def test_canonical_overlay_fails_closed_on_incomplete_exact_coverage(self):
        rows = [v43_row("swordsman", "test_sword")]
        with self.assertRaisesRegex(ValueError, "coverage"):
            apply_canonical(rows, {}, 1.0)

    def test_canonical_overlay_preserves_v43_melee_axis_without_supported_profiles(self):
        rows = [
            v43_row(
                "weak_hammerman",
                "weak_hammer",
                melee_kpm="5",
                melee_score="0",
                rank="2",
            ),
            v43_row(
                "strong_hammerman",
                "strong_hammer",
                melee_kpm="10",
                melee_score="100",
                rank="1",
            ),
        ]
        ranked, _, _ = apply_canonical(rows, {}, 1.0)
        by_id = {row["troop_id"]: row for row in ranked}
        self.assertEqual(by_id["weak_hammerman"]["v44_melee_carry_score"], 0.0)
        self.assertEqual(by_id["strong_hammerman"]["v44_melee_carry_score"], 100.0)

    def test_sensitivity_is_explicitly_noncanonical(self):
        rows = [
            v43_row("swordsman", "test_sword", rank="1"),
            v43_row("hammerman", "test_hammer", rank="2"),
        ]
        ranked, audit, summary = apply_sensitivity(rows)
        self.assertEqual(summary["mode"], "sensitivity_noncanonical")
        self.assertEqual(len(ranked), 2)
        self.assertTrue(
            all(row["profile_source"] == "low_confidence_family_prior" for row in audit)
        )


if __name__ == "__main__":
    unittest.main()
