#!/usr/bin/env python3
"""Generate the Realm of Thrones archer-like mounted-melee field shortlist."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import fmean


STRICT_TEMPLATES = {"OneHandedSword", "TwoHandedPolearm", "TwoHandedSword"}
NEAR_TEMPLATES = {"OneHandedSword", "TwoHandedPolearm"}
OUTPUT_FIELDS = [
    "canonical_troop_id",
    "troop_name",
    "screen_band",
    "roster_count",
    "melee_skill_floor",
    "mobility_floor",
    "armor_total_mean",
    "shield_hp_mean",
    "harness_armor_mean",
    "core_coverage_rosters",
    "three_mode_rosters",
    "crafted_weapon_stat_status",
]


def number(value: str | None) -> float:
    return float(value or 0)


def truthy(value: str | None) -> bool:
    return value == "True"


def templates(row: dict[str, str]) -> set[str]:
    return {value for value in row.get("crafted_templates", "").split("|") if value}


def evaluate_candidate(
    troop: dict[str, str], rosters: list[dict[str, str]]
) -> dict[str, str] | None:
    if (
        not rosters
        or troop.get("default_group") != "Cavalry"
        or troop.get("is_soldier") != "True"
        or troop.get("is_hero") == "True"
    ):
        return None
    if not all(truthy(row.get("has_horse")) and truthy(row.get("has_shield")) for row in rosters):
        return None

    melee_floor = min(number(troop.get(key)) for key in ("OneHanded", "TwoHanded", "Polearm"))
    mobility_floor = min(number(troop.get(key)) for key in ("Riding", "Athletics"))
    armor_mean = fmean(number(row.get("armor_total")) for row in rosters)
    shield_mean = fmean(number(row.get("shield_hp_max")) for row in rosters)
    harness_mean = fmean(number(row.get("horse_harness_armor_max")) for row in rosters)
    core_coverage = sum(NEAR_TEMPLATES <= templates(row) for row in rosters)
    three_mode = sum(STRICT_TEMPLATES <= templates(row) for row in rosters)
    roster_count = len(rosters)

    near_match = all(
        (
            melee_floor >= 220,
            mobility_floor >= 220,
            armor_mean >= 190,
            shield_mean >= 350,
            harness_mean >= 70,
            core_coverage == roster_count,
        )
    )
    if not near_match:
        return None

    strict = all(
        (
            melee_floor >= 250,
            mobility_floor >= 240,
            armor_mean >= 200,
            shield_mean >= 350,
            harness_mean >= 75,
            three_mode == roster_count,
        )
    )
    statuses = sorted({row.get("crafted_weapon_stat_status", "") for row in rosters})
    return {
        "canonical_troop_id": troop["troop_id"],
        "troop_name": troop["name"],
        "screen_band": "captain_like_strict" if strict else "near_match_test_queue",
        "roster_count": str(roster_count),
        "melee_skill_floor": f"{melee_floor:.1f}",
        "mobility_floor": f"{mobility_floor:.1f}",
        "armor_total_mean": f"{armor_mean:.1f}",
        "shield_hp_mean": f"{shield_mean:.1f}",
        "harness_armor_mean": f"{harness_mean:.1f}",
        "core_coverage_rosters": str(core_coverage),
        "three_mode_rosters": str(three_mode),
        "crafted_weapon_stat_status": "|".join(statuses),
    }


def generate(troops_path: Path, rosters_path: Path) -> list[dict[str, str]]:
    with troops_path.open(encoding="utf-8-sig", newline="") as handle:
        troops = {row["troop_id"]: row for row in csv.DictReader(handle)}
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    with rosters_path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            grouped[row["troop_id"]].append(row)

    candidates = [
        candidate
        for troop_id, troop in troops.items()
        if (candidate := evaluate_candidate(troop, grouped.get(troop_id, []))) is not None
    ]
    return sorted(
        candidates,
        key=lambda row: (row["screen_band"] != "captain_like_strict", row["canonical_troop_id"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--troops",
        type=Path,
        default=Path("data/realm_of_thrones/audit/realm_of_thrones_troops.csv"),
    )
    parser.add_argument(
        "--rosters",
        type=Path,
        default=Path("data/realm_of_thrones/audit/realm_of_thrones_roster_audit_summary.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("analysis/candidates/realm_of_thrones_archer_like_mounted_melee_field.csv"),
    )
    args = parser.parse_args()
    rows = generate(args.troops, args.rosters)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
