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
    add_ranks,
    build_candidate_scores,
    serialized,
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

    def test_same_slot_alternatives_are_averaged_before_roster_aggregation(self) -> None:
        troops = [troop("mounted_guard", default_group="Cavalry")]
        audit = [
            item("mounted_guard", 0, "Head", head_armor=20),
            item("mounted_guard", 0, "Head", head_armor=40),
            horse(
                "mounted_guard",
                0,
                item_id="slow_durable_horse",
                horse_extra_health=60,
                horse_speed=48,
                horse_maneuver=60,
            ),
            horse(
                "mounted_guard",
                0,
                item_id="fast_fragile_horse",
                horse_extra_health=20,
                horse_speed=68,
                horse_maneuver=80,
            ),
        ]

        row = by_id(build_candidate_scores(troops, audit))["mounted_guard"]

        self.assertEqual(row["armor_total_mean"], 30)
        self.assertEqual(row["horse_extra_health_mean"], 40)
        self.assertEqual(row["horse_speed_mean"], 58)
        self.assertEqual(row["horse_maneuver_mean"], 70)

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

    def test_lane_boundary_uses_at_least_half_horsed_rosters(self) -> None:
        troops = [troop("half_horsed"), troop("third_horsed")]
        audit = [
            body("half_horsed", 0, body_armor=10),
            horse("half_horsed", 0),
            body("half_horsed", 1, body_armor=10),
            body("third_horsed", 0, body_armor=10),
            horse("third_horsed", 0),
            body("third_horsed", 1, body_armor=10),
            body("third_horsed", 2, body_armor=10),
        ]

        rows = by_id(build_candidate_scores(troops, audit))

        self.assertEqual(rows["half_horsed"]["horse_share"], 0.5)
        self.assertEqual(rows["half_horsed"]["defensive_lane"], "cavalry")
        self.assertAlmostEqual(rows["third_horsed"]["horse_share"], 1 / 3)
        self.assertEqual(rows["third_horsed"]["defensive_lane"], "infantry")

    def test_population_filters_heroes_multiplayer_and_untouched_mod_rows(self) -> None:
        troops = [
            troop("kept"),
            troop("hero", is_hero=True),
            troop("mp_guard"),
            troop("untouched"),
        ]
        overrides = [
            {"troop_id": "kept", "change_type": "novo"},
            {"troop_id": "untouched", "change_type": "inalterado"},
        ]

        rows = build_candidate_scores(
            troops,
            [body("kept", 0, body_armor=10)],
            overrides,
        )

        self.assertEqual([row["troop_id"] for row in rows], ["kept"])

    def test_unresolved_item_contributes_zero_without_dropping_roster(self) -> None:
        troops = [troop("guard")]
        audit = [
            body("guard", 0, body_armor=50),
            item(
                "guard",
                0,
                "Head",
                item_found=False,
                head_armor=500,
            ),
        ]

        row = by_id(build_candidate_scores(troops, audit))["guard"]

        self.assertEqual(row["roster_count"], 1)
        self.assertEqual(row["armor_total_mean"], 50)

    def test_incomplete_mount_evidence_is_queued_instead_of_scored(self) -> None:
        troops = [
            troop("resolved_rider", default_group="Cavalry"),
            troop("warg_rider", default_group="Cavalry"),
        ]
        audit = [
            body("resolved_rider", 0, body_armor=50),
            horse(
                "resolved_rider",
                0,
                horse_extra_health=20,
                horse_speed=50,
                horse_maneuver=60,
            ),
            harness("resolved_rider", 0, armor=20),
            body("warg_rider", 0, body_armor=100),
            item(
                "warg_rider",
                0,
                "Horse",
                item_id="warg_brown",
                type="",
                horse_extra_health="",
                horse_speed="",
                horse_maneuver="",
            ),
            item(
                "warg_rider",
                0,
                "HorseHarness",
                item_id="warg_saddle",
                type="",
                body_armor="",
            ),
        ]

        rows = by_id(build_candidate_scores(troops, audit))

        self.assertEqual(rows["resolved_rider"]["protection_rank_v2"], 1)
        self.assertEqual(
            rows["warg_rider"]["score_status"],
            "review_required_mount_evidence",
        )
        self.assertNotIn("protection_score_v2", rows["warg_rider"])
        self.assertIn(
            "warg_brown:type,horse_speed,horse_maneuver",
            rows["warg_rider"]["unresolved_mount_evidence"],
        )
        self.assertIn(
            "warg_saddle:type,body_armor",
            rows["warg_rider"]["unresolved_mount_evidence"],
        )

    def test_taom_warg_gaps_are_written_to_an_explicit_review_queue(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            generated = write_track(REPO, output, "taom")
            queue_path = output / "taom" / "taom_defensive_review_queue_v2.csv"

            self.assertIn(queue_path, generated)
            queue = read_csv_rows(queue_path)

        self.assertEqual(len(queue), 22)
        self.assertTrue(all(not row["protection_score_v2"] for row in queue))
        self.assertTrue(
            all(row["score_status"] == "review_required_mount_evidence" for row in queue)
        )
        self.assertTrue(any("warg_brown" in row["unresolved_mount_evidence"] for row in queue))

    def test_eligible_troop_without_audit_roster_fails_closed(self) -> None:
        with self.assertRaisesRegex(
            ValueError,
            "eligible troops missing equipment audit rosters: missing",
        ):
            build_candidate_scores([troop("missing")], [])

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

    def test_spectacle_reason_is_exposed_without_removing_outlier(self) -> None:
        row = by_id(
            build_candidate_scores(
                [troop("cave_troll")],
                [body("cave_troll", 0, body_armor=100)],
            )
        )["cave_troll"]

        self.assertEqual(row["spectacle_reason"], "outsized foot unit")
        self.assertTrue(row["normalization_includes_outliers"])

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

    def test_equal_published_scores_share_a_rank(self) -> None:
        rows = [
            {"troop_id": "alpha", "score": 7.9530524},
            {"troop_id": "bravo", "score": 7.9530523},
        ]

        add_ranks(rows, "score", "rank")

        self.assertEqual(serialized(rows[0]["score"]), serialized(rows[1]["score"]))
        self.assertEqual(rows[0]["rank"], rows[1]["rank"])

    def test_mod_track_requires_its_override_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self.assertRaises(FileNotFoundError) as raised:
                write_track(root, root / "output", "taom")

        self.assertEqual(
            Path(raised.exception.filename).name,
            "taom_override_report.csv",
        )

    def test_partial_track_rerun_keeps_existing_artifacts_in_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory)
            generated = []
            for track_name in TRACKS:
                generated.extend(write_track(REPO, output, track_name))
            write_manifest(output, generated)

            vanilla_outputs = write_track(REPO, output, "vanilla")
            write_manifest(output, vanilla_outputs)

            paths = read_manifest_paths(output / "artifact_hashes.csv")
            self.assertEqual(len(paths), 32)
            self.assertTrue(any(path.startswith("taom/") for path in paths))

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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    import csv

    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
