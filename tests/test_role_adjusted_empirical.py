import math
import unittest

from scripts.analysis.role_adjusted_empirical import (
    ROLE_FRONTLINE_INFANTRY,
    ROLE_MELEE_CAVALRY,
    ROLE_RANGED,
    deployment_share,
    midrank_percentile,
    offensive_contribution_ratio,
    offensive_share_gap,
    retention_rate,
    role_adjusted_score,
    role_from_default_group,
)


class RoleAdjustedEmpiricalTests(unittest.TestCase):
    def test_mallister_batch_shadow_diagnostics(self) -> None:
        side_deployed = 1005
        side_kills = 1029

        raven_deployment_share = deployment_share(170, side_deployed)
        raven_kill_share = 281 / side_kills
        self.assertAlmostEqual(raven_deployment_share, 0.1691542289)
        self.assertAlmostEqual(
            offensive_contribution_ratio(raven_kill_share, raven_deployment_share),
            1.6143886126,
        )
        self.assertAlmostEqual(
            offensive_share_gap(raven_kill_share, raven_deployment_share),
            0.1039264320,
        )

        house_guard_deployment_share = deployment_share(153, side_deployed)
        house_guard_kill_share = 179 / side_kills
        self.assertAlmostEqual(
            offensive_contribution_ratio(
                house_guard_kill_share, house_guard_deployment_share
            ),
            1.1426475352,
        )
        self.assertAlmostEqual(
            offensive_share_gap(
                house_guard_kill_share, house_guard_deployment_share
            ),
            0.0217164904,
        )

        eagle_deployment_share = deployment_share(159, side_deployed)
        eagle_kill_share = 102 / side_kills
        self.assertAlmostEqual(
            offensive_contribution_ratio(eagle_kill_share, eagle_deployment_share),
            0.6265471148,
        )

    def test_retention_uses_dead_and_wounded(self) -> None:
        self.assertAlmostEqual(retention_rate(170, 0, 3), 167 / 170)
        self.assertAlmostEqual(retention_rate(153, 3, 7), 143 / 153)
        self.assertAlmostEqual(retention_rate(159, 9, 19), 131 / 159)

    def test_role_mapping(self) -> None:
        self.assertEqual(role_from_default_group("Ranged", "field"), ROLE_RANGED)
        self.assertEqual(role_from_default_group("HorseArcher", "field"), ROLE_RANGED)
        self.assertEqual(
            role_from_default_group("Infantry", "field"),
            ROLE_FRONTLINE_INFANTRY,
        )
        self.assertEqual(
            role_from_default_group("Cavalry", "field"), ROLE_MELEE_CAVALRY
        )
        self.assertEqual(
            role_from_default_group("Cavalry", "siege_defense"),
            ROLE_FRONTLINE_INFANTRY,
        )

    def test_midrank_percentile_and_role_population_gate(self) -> None:
        self.assertIsNone(midrank_percentile(3, [1, 2, 3, 4], minimum_rows=5))
        self.assertEqual(midrank_percentile(1, [1, 2, 3, 4, 5]), 0.0)
        self.assertEqual(midrank_percentile(5, [1, 2, 3, 4, 5]), 100.0)
        self.assertEqual(midrank_percentile(3, [1, 2, 3, 4, 5]), 50.0)
        self.assertEqual(midrank_percentile(2, [1, 2, 2, 4, 5]), 37.5)

    def test_role_adjusted_weighting(self) -> None:
        self.assertEqual(
            role_adjusted_score(60, 90, ROLE_FRONTLINE_INFANTRY), 80.0
        )
        self.assertEqual(role_adjusted_score(60, 90, ROLE_MELEE_CAVALRY), 80.0)
        self.assertEqual(role_adjusted_score(90, 60, ROLE_RANGED), 80.0)
        self.assertIsNone(role_adjusted_score(None, 60, ROLE_RANGED))

    def test_invalid_inputs_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            deployment_share(2, 1)
        with self.assertRaises(ValueError):
            retention_rate(10, 6, 5)
        with self.assertRaises(ValueError):
            offensive_contribution_ratio(0.5, 0)
        with self.assertRaises(ValueError):
            midrank_percentile(6, [1, 2, 3, 4, 5])
        with self.assertRaises(ValueError):
            role_from_default_group("Unknown", "field")
        with self.assertRaises(ValueError):
            retention_rate(math.nan, 0, 0)
        with self.assertRaises(ValueError):
            role_adjusted_score(math.inf, 50, ROLE_RANGED)


if __name__ == "__main__":
    unittest.main()
