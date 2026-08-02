"""Behavioral tests for the candidate defensive role model v2."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts" / "scoring"))

from generate_defensive_role_scores_v2 import (  # noqa: E402
    TRACKS,
    build_candidate_scores,
    survivability_armor_v71,
    write_manifest,
    write_track,
)


def troop(troop_id: str, **values: object) -> dict[str, str]:
    row: dict[str, object] = {
        "troop_id": troop_id,
        "name": troop_id.replace("_", " ").title(),
        "is_soldier": "True",
        "is_hero": "False",
        "default_group": "Infantry",
        "OneHanded": "100",
        "TwoHanded": "0",
        "Polearm": "0",
        "Riding": "0",
        "Athletics": "100",
    }
    row.update(values)
    return {key: str(value) for key, value in row.items()}


def item(
    troop_id: str,
    roster_index: int,
    slot: str,
    **values: object,
) -> dict[str, str]:
    row: dict[str, object] = {
        "troop_id": troop_id,
        "roster_index": roster_index,
        "slot": slot,
        "item_id": f"{troop_id}_{slot}_{roster_index}",
        "item_found": "True",
        "type": "Armor",
        "head_armor": "0",
        "body_armor": "0",
        "arm_armor": "0",
        "leg_armor": "0",
        "hit_points": "0",
        "shield_armor": "0",
        "horse_speed": "0",
        "horse_maneuver": "0",
        "horse_charge_damage": "0",
        "horse_extra_health": "0",
    }
    row.update(values)
    return {key: str(value) for key, value in row.items()}


def body(troop_id: str, roster_index: int, **values: object) -> dict[str, str]:
    return item(troop_id, roster_index, "Body", **values)


def horse(troop_id: str, roster_index: int, **values: object) -> dict[str, str]:
    return item(troop_id, roster_index, "Horse", type="Horse", **values)


def harness(troop_id: str, roster_index: int, armor: float) -> dict[str, str]:
    return item(
        troop_id,
        roster_index,
        "HorseHarness",
        type="HorseHarness",
        body_armor=armor,
    )


def shield(
    troop_id: str,
    roster_index: int,
    hit_points: float,
    armor: float,
) -> dict[str, str]:
    return item(
        troop_id,
        roster_index,
        "Item0",
        type="Shield",
        hit_points=hit_points,
        shield_armor=armor,
    )


def by_id(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {str(row["troop_id"]): row for row in rows}


class DefensiveRoleScoresV2Tests(unittest.TestCase):
    def test_survivability_armor_uses_v71_head_weighting(self) -> None:
        self.assertAlmostEqual(survivability_armor_v71(100, 100, 100, 100), 100)
        self.assertAlmostEqual(survivability_armor_v71(100, 0, 0, 0), 35)
        self.assertAlmostEqual(survivability_armor_v71(0, 100, 0, 0), 55)

    def test_alternative_loadouts_are_averaged_including_missing_shields(self) -> None:
        troops = [troop("shield_guard")]
        audit = [
            body("shield_guard", 0, body_armor=50),
            shield("shield_guard", 0, hit_points=600, armor=10),
            body("shield_guard", 1, body_armor=50),
        ]

        rows = by_id(build_candidate_scores(troops, audit))

        self.assertEqual(rows["shield_guard"]["roster_count"], 2)
        self.assertEqual(rows["shield_guard"]["shield_share"], 0.5)
        self.assertEqual(rows["shield_guard"]["shield_hp_mean"], 300)
        self.assertEqual(rows["shield_guard"]["shield_armor_mean"], 5)

    def test_mount_charge_does_not_change_either_defensive_score(self) -> None:
        troops = [
            troop("calm_mount", default_group="Cavalry", Riding=100),
            troop("charging_mount", default_group="Cavalry", Riding=100),
        ]
        audit = []
        for troop_id, charge in (("calm_mount", 5), ("charging_mount", 400)):
            audit.extend(
                [
                    body(troop_id, 0, head_armor=40, body_armor=60),
                    horse(
                        troop_id,
                        0,
                        horse_charge_damage=charge,
                        horse_speed=50,
                        horse_maneuver=60,
                        horse_extra_health=20,
                    ),
                    harness(troop_id, 0, armor=50),
                ]
            )

        rows = by_id(build_candidate_scores(troops, audit))

        self.assertEqual(
            rows["calm_mount"]["protection_score_v2"],
            rows["charging_mount"]["protection_score_v2"],
        )
        self.assertEqual(
            rows["calm_mount"]["defensive_utility_score_v2"],
            rows["charging_mount"]["defensive_utility_score_v2"],
        )

    def test_mount_durability_changes_protection_but_mobility_only_changes_utility(self) -> None:
        troops = [
            troop("baseline", default_group="Cavalry", Riding=100),
            troop("durable", default_group="Cavalry", Riding=100),
            troop("mobile", default_group="Cavalry", Riding=200),
        ]
        audit = []
        mounts = {
            "baseline": (20, 50, 60),
            "durable": (100, 50, 60),
            "mobile": (20, 70, 80),
        }
        for troop_id, (health, speed, maneuver) in mounts.items():
            audit.extend(
                [
                    body(troop_id, 0, head_armor=40, body_armor=60),
                    horse(
                        troop_id,
                        0,
                        horse_speed=speed,
                        horse_maneuver=maneuver,
                        horse_extra_health=health,
                    ),
                    harness(troop_id, 0, armor=50),
                ]
            )

        rows = by_id(build_candidate_scores(troops, audit))

        self.assertGreater(
            rows["durable"]["protection_score_v2"],
            rows["baseline"]["protection_score_v2"],
        )
        self.assertEqual(
            rows["mobile"]["protection_score_v2"],
            rows["baseline"]["protection_score_v2"],
        )
        self.assertGreater(
            rows["mobile"]["defensive_utility_score_v2"],
            rows["baseline"]["defensive_utility_score_v2"],
        )

    def test_infantry_and_cavalry_lanes_are_exclusive(self) -> None:
        troops = [troop("foot"), troop("mounted", default_group="Cavalry")]
        audit = [
            body("foot", 0, body_armor=50),
            body("mounted", 0, body_armor=50),
            horse("mounted", 0, horse_extra_health=20),
        ]

        rows = by_id(build_candidate_scores(troops, audit))

        self.assertEqual(rows["foot"]["defensive_lane"], "infantry")
        self.assertEqual(rows["mounted"]["defensive_lane"], "cavalry")

    def test_outlier_remains_in_the_normalization_population(self) -> None:
        troops = [
            troop("ordinary_low", default_group="Cavalry"),
            troop("ordinary_high", default_group="Cavalry"),
            troop("outlier", default_group="Cavalry"),
        ]
        audit = []
        for troop_id, health in (
            ("ordinary_low", 0),
            ("ordinary_high", 50),
            ("outlier", 500),
        ):
            audit.extend(
                [
                    body(troop_id, 0, body_armor=50),
                    horse(troop_id, 0, horse_extra_health=health),
                ]
            )

        rows = by_id(build_candidate_scores(troops, audit))

        self.assertEqual(rows["outlier"]["mount_health_component_v2"], 100)
        self.assertEqual(rows["ordinary_high"]["mount_health_component_v2"], 10)
        self.assertTrue(rows["ordinary_high"]["normalization_includes_outliers"])

    def test_weapon_template_does_not_affect_defensive_scores(self) -> None:
        troops = [troop("sword"), troop("axe")]
        audit = []
        for troop_id, template in (("sword", "TwoHandedSword"), ("axe", "Axe")):
            audit.extend(
                [
                    body(troop_id, 0, body_armor=50),
                    item(
                        troop_id,
                        0,
                        "Item0",
                        type="CraftedWeapon",
                        crafting_template=template,
                    ),
                ]
            )

        rows = by_id(build_candidate_scores(troops, audit))

        self.assertEqual(
            rows["sword"]["protection_score_v2"],
            rows["axe"]["protection_score_v2"],
        )
        self.assertEqual(
            rows["sword"]["defensive_utility_score_v2"],
            rows["axe"]["defensive_utility_score_v2"],
        )

    def test_committed_outputs_rebuild_byte_for_byte(self) -> None:
        committed = REPO / "analysis/model_candidates/role_scores_v2_defense"
        with tempfile.TemporaryDirectory() as temporary_directory:
            rebuilt = Path(temporary_directory)
            generated = []
            for track_name in TRACKS:
                generated.extend(write_track(REPO, rebuilt, track_name))
            write_manifest(rebuilt, generated)

            committed_manifest = committed / "artifact_hashes.csv"
            rebuilt_manifest = rebuilt / "artifact_hashes.csv"
            self.assertEqual(rebuilt_manifest.read_bytes(), committed_manifest.read_bytes())
            for relative_path in read_manifest_paths(rebuilt_manifest):
                self.assertEqual(
                    (rebuilt / relative_path).read_bytes(),
                    (committed / relative_path).read_bytes(),
                    relative_path,
                )


def read_manifest_paths(path: Path) -> list[str]:
    import csv

    with path.open(newline="", encoding="utf-8") as handle:
        return [row["path"] for row in csv.DictReader(handle)]


if __name__ == "__main__":
    unittest.main()
