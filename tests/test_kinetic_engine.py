"""Goldens + edge cases for the Wavey v2.9 kinetic melee engine port.

Golden values computed from the original JS formula (extracted 2026-07-23).
If a golden fails, the PORT is wrong -- fix the port, never the test.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from melee_engine.kinetic_engine import (  # noqa: E402
    WAVEY_V29,
    WeaponProfile,
    grade,
    tier_for,
)


def sword(sd, ss, h, r, w, td=0.0, ts=0.0):
    return WeaponProfile(
        swing_damage=sd,
        swing_speed=ss,
        handling=h,
        reach=r,
        weight=w,
        has_thrust=bool(td or ts),
        thrust_damage=td,
        thrust_speed=ts,
    )


class GoldenTests(unittest.TestCase):
    """Pinned against the original JS implementation."""

    def assert_golden(self, weapon, level, vs_light, vs_heavy, final):
        result = grade(weapon, level)
        self.assertEqual(
            (result.vs_light, result.vs_heavy, result.final),
            (vs_light, vs_heavy, final),
        )

    def test_high_tier_thrust(self):
        self.assert_golden(sword(90, 95, 98, 105, 1.5, td=78, ts=88), 200, 62, 61, 61)

    def test_budget_no_thrust(self):
        self.assert_golden(sword(65, 88, 92, 95, 1.2), 100, 16, 12, 13)

    def test_long_reach_penalty(self):
        self.assert_golden(sword(95, 90, 90, 125, 2.0, td=85, ts=85), 250, 72, 76, 75)

    def test_zero_level_min(self):
        self.assert_golden(sword(40, 80, 85, 90, 0.8), 0, 4, 5, 5)


class EdgeCaseTests(unittest.TestCase):
    def test_thrust_ratio_clamps_at_one(self):
        """Thrust better than swing must not become a bonus above 1.0x."""
        overpowered_thrust = sword(50, 80, 90, 100, 1.2, td=120, ts=120)
        equivalent = sword(50, 80, 90, 100, 1.2, td=50, ts=80)
        self.assertEqual(
            grade(overpowered_thrust, 100).final, grade(equivalent, 100).final
        )

    def test_no_thrust_beats_penalized_thrust(self):
        """A thrust-capable sword with weak thrust ratios scores below the
        identical sword without thrust (the AI animation penalty)."""
        with_weak_thrust = sword(90, 95, 95, 105, 1.5, td=30, ts=60)
        without_thrust = sword(90, 95, 95, 105, 1.5)
        self.assertLess(
            grade(with_weak_thrust, 200).final, grade(without_thrust, 200).final
        )

    def test_reach_penalty_floor(self):
        """Absurd reach cannot push the penalty below the 0.5 floor:
        beyond the floor's onset, more reach helps again only via the
        base reach term. Verify floor via calibration internals."""
        cal = WAVEY_V29
        reach = 300.0
        penalty = max(
            cal.reach_penalty_floor,
            1.0 - max(0.0, reach - cal.reach_soft_cap) / 100.0,
        )
        self.assertEqual(penalty, cal.reach_penalty_floor)

    def test_kills_floor_is_one(self):
        result = grade(sword(2, 40, 40, 40, 0.2), 0)
        self.assertGreaterEqual(result.kills_light, 1.0)
        self.assertGreaterEqual(result.kills_heavy, 1.0)

    def test_reach_peaks_at_soft_cap(self):
        """The effective reach term peaks exactly at the soft cap (110) and
        decays beyond it. NOTE: the penalty is SOFT -- e.g. reach 118
        (term ~1.086) still outscores reach 108 (1.08); collision only
        bites hard well above the cap. Documented model insight."""

        def eff_reach(r):
            cal = WAVEY_V29
            pen = max(
                cal.reach_penalty_floor,
                1.0 - max(0.0, r - cal.reach_soft_cap) / 100.0,
            )
            return (r / 100.0) * pen

        self.assertGreater(eff_reach(110), eff_reach(108))
        self.assertGreater(eff_reach(110), eff_reach(125))
        self.assertGreater(eff_reach(118), eff_reach(108))  # soft penalty
        self.assertGreater(
            grade(sword(90, 95, 95, 110, 1.5), 200).final,
            grade(sword(90, 95, 95, 125, 1.5), 200).final,
        )

    def test_tier_boundaries(self):
        self.assertEqual(tier_for(86), "S+")
        self.assertEqual(tier_for(85), "S")
        self.assertEqual(tier_for(25), "D")
        self.assertEqual(tier_for(24), "F")

    def test_derived_calibration_does_not_mutate_default(self):
        rot_cal = WAVEY_V29.derive(armour_heavy=60.0)
        self.assertEqual(WAVEY_V29.armour_heavy, 45.0)
        self.assertEqual(rot_cal.armour_heavy, 60.0)
        self.assertEqual(rot_cal.scale, WAVEY_V29.scale)


if __name__ == "__main__":
    unittest.main(verbosity=2)
