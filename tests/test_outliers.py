"""S+ / spectacle-outlier definition (ADR-005). Stdlib only — no pandas."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts" / "scoring"))

from outliers import (  # noqa: E402
    ALL_CRITERIA,
    CRITERIA_BY_KEY,
    DEFAULT_CRITERIA,
    OUTSIZED_MOUNT_CHARGE_THRESHOLD,
    REASON_FOOT,
    REASON_MOUNT,
    REASON_NAME,
    SPECTACLE_OUTLIER_VERSION,
    TroopFacts,
    classify,
    classify_facts,
    classify_row,
    describe_criteria,
    facts_from_row,
    is_spectacle_outlier,
    matched_criteria,
    spectacle_reason,
    split_spectacle_outliers,
)

ALL_ON = ALL_CRITERIA


class _ListFrame:
    """List-backed frame, same shape as the one in test_theoretical_overview."""

    def __init__(self, rows: list[dict]):
        self._rows = rows

    def __len__(self) -> int:
        return len(self._rows)


class RegistryTests(unittest.TestCase):
    def test_version_and_default_criteria_are_v1_behaviour(self) -> None:
        self.assertEqual(SPECTACLE_OUTLIER_VERSION, "v2")
        # Default must stay name-only so published scores/tiers reproduce.
        self.assertEqual(DEFAULT_CRITERIA, ("giant_mammoth_name",))
        self.assertTrue(CRITERIA_BY_KEY["giant_mammoth_name"].default_enabled)
        for key in set(ALL_CRITERIA) - {"giant_mammoth_name"}:
            self.assertFalse(
                CRITERIA_BY_KEY[key].default_enabled, f"{key} must be opt-in"
            )

    def test_unknown_criterion_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            classify("giant", "Giant", criteria=("no_such_rule",))

    def test_describe_criteria_reports_active_rules(self) -> None:
        described = describe_criteria()
        self.assertEqual(len(described), 1)
        self.assertIn("giant_mammoth_name", described[0])
        self.assertIn(REASON_NAME, described[0])
        self.assertEqual(len(describe_criteria(ALL_ON)), len(ALL_CRITERIA))


class GiantMammothNameTests(unittest.TestCase):
    def test_giants_and_mammoths_are_outliers_with_reason(self) -> None:
        for troop_id, troop_name in [
            ("giant_rider", "Mammoth Riding Giant"),
            ("elder_giant", "Elder Giant"),
            ("giant", "Giant"),
            ("giant_archer", "Giant Archer"),
        ]:
            verdict = classify(troop_id, troop_name)
            self.assertTrue(verdict.is_outlier, troop_id)
            self.assertEqual(verdict.reason, REASON_NAME, troop_id)
            self.assertTrue(is_spectacle_outlier(troop_id, troop_name))
            self.assertEqual(spectacle_reason(troop_id, troop_name), REASON_NAME)

    def test_ordinary_troops_are_not_outliers(self) -> None:
        for troop_id, troop_name in [
            ("dragonstone_elite_archer", "Dragonstone Elite Archer"),
            ("greyjoy_sniper", "Greyjoy Sniper"),
            ("myrish_artisan", "Myrish Artisan of War"),
            ("ravens_teeth", "Ravens' Teeth"),
            ("imladris_blademaster", "[Rivendell] Imladris Blademaster"),
            ("mountains_man", "Mountain's Man"),
            ("gigantic_shield_bearer", "Gigantic Shield Bearer"),
        ]:
            verdict = classify(troop_id, troop_name)
            self.assertFalse(verdict.is_outlier, troop_id)
            self.assertIsNone(verdict.reason, troop_id)
            self.assertFalse(is_spectacle_outlier(troop_id, troop_name))

    def test_missing_values_do_not_crash(self) -> None:
        self.assertFalse(is_spectacle_outlier(None, None))
        self.assertEqual(classify_facts(TroopFacts()).is_outlier, False)


class RealmOfThronesCaseTests(unittest.TestCase):
    """RoT ROLE_REPORT parks 4 giants by name + 3 elephant mahouts by mount charge."""

    NAME_PARKED = [
        ("giant", "Giant"),
        ("giant_archer", "Giant Archer"),
        ("elder_giant", "Elder Giant"),
        ("giant_rider", "Mammoth Riding Giant"),
    ]
    MOUNT_PARKED = [
        ("golden_elite_pikeman", "Golden Company Mahout", 350.0),
        ("golden_horseman", "Golden Company Elephant Rider", 350.0),
        ("tigercloak_camel_cavalry", "Volantene Mahout", 350.0),
    ]

    def test_rot_name_parked_rows_fire_by_default(self) -> None:
        for troop_id, troop_name in self.NAME_PARKED:
            self.assertEqual(
                classify(troop_id, troop_name),
                (True, REASON_NAME),
                troop_id,
            )

    def test_rot_elephant_mahouts_are_not_parked_by_default(self) -> None:
        # Documented-as-prose-only in the RoT report; must NOT change OVERVIEW output.
        for troop_id, troop_name, charge in self.MOUNT_PARKED:
            verdict = classify(
                troop_id, troop_name, mount_charge_damage=charge
            )
            self.assertFalse(verdict.is_outlier, troop_id)

    def test_rot_elephant_mahouts_park_when_criterion_opted_in(self) -> None:
        for troop_id, troop_name, charge in self.MOUNT_PARKED:
            verdict = classify(
                troop_id,
                troop_name,
                mount_charge_damage=charge,
                criteria=("giant_mammoth_name", "outsized_mount_charge"),
            )
            self.assertEqual(verdict, (True, REASON_MOUNT), troop_id)

    def test_rot_mammoth_rider_matches_both_criteria(self) -> None:
        facts = TroopFacts(
            troop_id="giant_rider",
            troop_name="Mammoth Riding Giant",
            mount_charge_damage=400.0,
        )
        self.assertEqual(
            matched_criteria(facts, ALL_ON),
            ("giant_mammoth_name", "outsized_mount_charge"),
        )
        # Registry order decides the reported reason.
        self.assertEqual(classify_facts(facts, ALL_ON).reason, REASON_NAME)

    def test_rot_ordinary_mounts_stay_below_threshold(self) -> None:
        # unicorn1 charge 90 is the next mount down; warhorses are 19-36.
        for charge in (90.0, 80.0, 36.0, 32.0, 0.0):
            self.assertLess(charge, OUTSIZED_MOUNT_CHARGE_THRESHOLD)
            self.assertFalse(
                classify(
                    "lannister_prideknight",
                    "Lannister Prideknight",
                    mount_charge_damage=charge,
                    criteria=ALL_ON,
                ).is_outlier,
                charge,
            )


class TaomCaseTests(unittest.TestCase):
    """TAOM ROLE_REPORT parks 4 mount-based units + cave_troll (foot), no name match."""

    MOUNT_PARKED = [
        ("harad_mumakil_rider", "[Aharad] Mumakil Rider", "taom_mumakil"),
        ("harad_elephant_rider", "[Aharad] Elephant Rider", "taom_war_elephant"),
        (
            "wainrider_warlord_chariot",
            "[Rhûn] Wainrider Warlord Chariot",
            "taom_chariot_a",
        ),
        (
            "wainrider_swift_chariot",
            "[ARhûn] Wainrider Swift-Chariot",
            "taom_chariot_a",
        ),
    ]

    def test_taom_outsized_units_are_invisible_to_the_name_regex(self) -> None:
        for troop_id, troop_name, mount in self.MOUNT_PARKED:
            self.assertFalse(
                classify(troop_id, troop_name, mount_ids=(mount,)).is_outlier,
                troop_id,
            )
        self.assertFalse(
            classify("cave_troll", "[AMordor] Armored Troll").is_outlier
        )

    def test_taom_mount_ids_park_when_criterion_opted_in(self) -> None:
        for troop_id, troop_name, mount in self.MOUNT_PARKED:
            self.assertEqual(
                classify(
                    troop_id,
                    troop_name,
                    mount_ids=(mount,),
                    criteria=("outsized_mount_id",),
                ),
                (True, REASON_MOUNT),
                troop_id,
            )

    def test_taom_cave_troll_parks_as_foot_unit_when_opted_in(self) -> None:
        self.assertEqual(
            classify(
                "cave_troll", "[AMordor] Armored Troll", criteria=ALL_ON
            ),
            (True, REASON_FOOT),
        )

    def test_taom_ordinary_mount_ids_do_not_park(self) -> None:
        for mount in ("noble_horse", "t3_vlandia_horse", "warg_dark", ""):
            self.assertFalse(
                classify(
                    "rohan_westemnet_kings_own_rider",
                    "[Rohan] West Emnet Heavy Shock Cavalry",
                    mount_ids=(mount,),
                    criteria=ALL_ON,
                ).is_outlier,
                mount,
            )


class RowAndFrameTests(unittest.TestCase):
    def test_facts_from_row_reads_optional_mount_columns(self) -> None:
        facts = facts_from_row(
            {
                "troop_id": "golden_horseman",
                "troop_name": "Golden Company Elephant Rider",
                "mount": "war_elephant",
                "horse_charge_damage": "350",
            }
        )
        self.assertEqual(facts.troop_id, "golden_horseman")
        self.assertEqual(facts.mount_ids, ("war_elephant",))
        self.assertEqual(facts.mount_charge_damage, "350")
        self.assertTrue(
            classify_facts(facts, ("outsized_mount_charge",)).is_outlier
        )

    def test_facts_from_row_without_mount_columns(self) -> None:
        facts = facts_from_row({"troop_id": "giant", "troop_name": "Giant"})
        self.assertEqual(facts.mount_ids, ())
        self.assertIsNone(facts.mount_charge_damage)
        self.assertTrue(classify_facts(facts, ALL_ON).is_outlier)

    def test_classify_row_handles_non_numeric_charge(self) -> None:
        row = {"troop_id": "x", "troop_name": "X", "horse_charge_damage": "n/a"}
        self.assertFalse(classify_row(row, ALL_ON).is_outlier)

    def test_split_uses_default_criteria_on_list_frame(self) -> None:
        frame = _ListFrame(
            [
                {"troop_id": "giant_rider", "troop_name": "Mammoth Riding Giant"},
                {"troop_id": "ravens_teeth", "troop_name": "Ravens' Teeth"},
                {
                    "troop_id": "golden_elite_pikeman",
                    "troop_name": "Golden Company Mahout",
                    "horse_charge_damage": 350,
                },
            ]
        )
        standard, outliers = split_spectacle_outliers(frame)
        self.assertEqual([r["troop_id"] for r in outliers._rows], ["giant_rider"])
        self.assertEqual(
            [r["troop_id"] for r in standard._rows],
            ["ravens_teeth", "golden_elite_pikeman"],
        )

    def test_split_with_opt_in_criteria_parks_the_mahout(self) -> None:
        frame = _ListFrame(
            [
                {"troop_id": "ravens_teeth", "troop_name": "Ravens' Teeth"},
                {
                    "troop_id": "golden_elite_pikeman",
                    "troop_name": "Golden Company Mahout",
                    "horse_charge_damage": 350,
                },
            ]
        )
        standard, outliers = split_spectacle_outliers(frame, ALL_ON)
        self.assertEqual(
            [r["troop_id"] for r in outliers._rows], ["golden_elite_pikeman"]
        )
        self.assertEqual([r["troop_id"] for r in standard._rows], ["ravens_teeth"])

    def test_split_on_empty_frame(self) -> None:
        frame = _ListFrame([])
        standard, outliers = split_spectacle_outliers(frame)
        self.assertEqual(len(standard), 0)
        self.assertEqual(len(outliers), 0)


class KineticLadderIsADifferentConceptTests(unittest.TestCase):
    def test_kinetic_engine_splus_is_a_score_band_not_a_scale_flag(self) -> None:
        sys.path.insert(0, str(REPO / "scripts"))
        from melee_engine.kinetic_engine import tier_for

        self.assertEqual(tier_for(90), "S+")
        # An ordinary troop can reach that band without being a spectacle unit.
        self.assertFalse(
            is_spectacle_outlier("imladris_blademaster", "Imladris Blademaster")
        )
        # ...and a spectacle unit is not defined by any kinetic score.
        self.assertTrue(is_spectacle_outlier("giant", "Giant"))


if __name__ == "__main__":
    unittest.main()
