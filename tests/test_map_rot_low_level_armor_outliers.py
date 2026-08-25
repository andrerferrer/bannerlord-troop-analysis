from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from scripts.analysis.map_rot_low_level_armor_outliers import load_candidates


FIELDS = [
    "troop_id",
    "troop_name",
    "roster_index",
    "slot",
    "item_id",
    "item_found",
    "type",
    "hit_points",
    "shield_armor",
    "head_armor",
    "body_armor",
    "arm_armor",
    "leg_armor",
    "level",
    "occupation",
    "culture",
    "default_group",
    "tree_tier",
    "line_status",
    "line_status_corrected",
]


def armor_row(troop_id: str, roster: int, body: int) -> dict[str, object]:
    return {
        "troop_id": troop_id,
        "troop_name": troop_id.title(),
        "roster_index": roster,
        "slot": "Body",
        "item_id": f"{troop_id}_armor_{roster}",
        "item_found": "True",
        "type": "BodyArmor",
        "head_armor": 1,
        "body_armor": body,
        "arm_armor": 2,
        "leg_armor": 3,
        "level": 16,
        "occupation": "Soldier",
        "culture": "test",
        "default_group": "Infantry",
        "tree_tier": 2,
        "line_status": "main_or_minor_line",
        "line_status_corrected": "main_or_minor_line",
    }


class ArmorOutlierScreenTests(unittest.TestCase):
    def test_averages_rosters_and_ranks_body_zone_without_shield_bonus(self) -> None:
        rows = [
            armor_row("alpha", 0, 40),
            armor_row("alpha", 1, 60),
            armor_row("beta", 0, 45),
        ]
        rows.append(
            {
                **armor_row("beta", 0, 0),
                "slot": "Item1",
                "item_id": "beta_shield",
                "type": "Shield",
                "hit_points": 999,
                "shield_armor": 10,
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            candidates = {row["troop_id"]: row for row in load_candidates(path)}

        self.assertEqual(candidates["alpha"]["body_zone_armor"], 50)
        self.assertEqual(candidates["alpha"]["body_zone_rank"], 1)
        self.assertEqual(candidates["beta"]["body_zone_rank"], 2)
        self.assertEqual(candidates["beta"]["shield_hp"], 999)

    def test_unresolved_worn_item_is_queued_but_empty_slot_is_not(self) -> None:
        rows = [armor_row("valid", 0, 40), armor_row("blocked", 0, 50)]
        rows[1]["item_found"] = "False"
        rows.extend(
            [
                {
                    **armor_row("valid", 0, 0),
                    "slot": "Cape",
                    "item_id": "",
                    "item_found": "",
                }
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "audit.csv"
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            review_queue: list[dict[str, str]] = []
            candidates = load_candidates(path, review_queue)

        self.assertEqual([row["troop_id"] for row in candidates], ["valid"])
        self.assertEqual(review_queue[0]["troop_id"], "blocked")
        self.assertEqual(review_queue[0]["unresolved_item_ids"], "blocked_armor_0")


if __name__ == "__main__":
    unittest.main()
