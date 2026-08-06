from __future__ import annotations

import csv
import sys
import unittest
from dataclasses import FrozenInstanceError
from decimal import Decimal
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts/scoring"))
import context_first_contract as contract  # noqa: E402
import context_first_equipment as equipment  # noqa: E402


FIXTURE = REPO_ROOT / "tests/fixtures/context_first/armor/armor_rows.csv"
AGGREGATION = contract.ArmorAggregation(
    "survivability_armor_v71", Decimal("0.35"), Decimal("0.55"),
    Decimal("0.05"), Decimal("0.05"),
)


def fixture_rows() -> list[dict[str, str]]:
    with FIXTURE.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


class ContextFirstArmorTests(unittest.TestCase):
    def resolve(self, rows=None) -> equipment.ArmorResolution:
        return equipment.resolve_armor_evidence(
            fixture_rows() if rows is None else rows,
            source_path="tests/fixtures/context_first/armor/armor_rows.csv",
            source_sha256="a" * 64,
            aggregation=AGGREGATION,
        )

    def test_equal_worn_armor_stays_equal_when_shield_mount_and_skill_vary(self) -> None:
        by_troop = {roster.troop_id: roster for roster in self.resolve().rosters}
        self.assertEqual(by_troop["equal_a"].armor_output, by_troop["equal_b"].armor_output)
        self.assertEqual(Decimal("29.750000"), by_troop["equal_a"].armor_output)

    def test_only_five_worn_slots_can_contribute(self) -> None:
        result = self.resolve()
        self.assertEqual(
            {"Body", "Head"},
            {item.slot for item in result.items if item.troop_id == "equal_a"},
        )
        self.assertNotIn("shield_a", {item.item_id for item in result.items})
        self.assertNotIn("horse_a", {item.item_id for item in result.items})

    def test_alternatives_are_averaged_inside_slot_not_summed_or_maxed(self) -> None:
        roster = next(row for row in self.resolve().rosters if row.troop_id == "alternatives")
        self.assertEqual(Decimal("40.000000"), roster.body_armor)
        self.assertEqual(Decimal("10.000000"), roster.arm_armor)
        self.assertEqual(Decimal("5.000000"), roster.leg_armor)
        self.assertEqual(Decimal("22.750000"), roster.armor_output)

    def test_missing_worn_slot_is_numeric_zero(self) -> None:
        row = {
            "troop_id": "bare", "roster_index": "0", "slot": "Item0",
            "item_id": "sword", "item_found": "False",
        }
        roster = self.resolve([row]).rosters[0]
        self.assertEqual(Decimal("0.000000"), roster.armor_output)
        self.assertEqual((), roster.reasons)

    def test_blank_region_blanks_whole_roster_and_queues_reason(self) -> None:
        roster = next(row for row in self.resolve().rosters if row.troop_id == "incomplete")
        self.assertIsNone(roster.armor_output)
        self.assertIn(contract.ARMOR_REGION_MISSING, {reason.code for reason in roster.reasons})

    def test_unresolved_item_blanks_whole_roster(self) -> None:
        roster = next(row for row in self.resolve().rosters if row.troop_id == "unresolved")
        self.assertIsNone(roster.head_armor)
        self.assertEqual([contract.ARMOR_ITEM_UNRESOLVED], [reason.code for reason in roster.reasons])

    def test_missing_item_id_has_distinct_reason(self) -> None:
        row = {
            "troop_id": "x", "roster_index": "0", "slot": "Body", "item_id": "",
            "item_found": "True", "head_armor": "0", "body_armor": "1",
            "arm_armor": "0", "leg_armor": "0",
        }
        roster = self.resolve([row]).rosters[0]
        self.assertEqual([contract.ARMOR_ITEM_ID_MISSING], [reason.code for reason in roster.reasons])

    def test_malformed_negative_and_nonfinite_values_are_invalid_not_zero(self) -> None:
        for value in ("bad", "-1", "NaN", "Infinity"):
            row = {
                "troop_id": value, "roster_index": "0", "slot": "Body",
                "item_id": "armor", "item_found": "True", "head_armor": "0",
                "body_armor": value, "arm_armor": "0", "leg_armor": "0",
            }
            with self.subTest(value=value):
                roster = self.resolve([row]).rosters[0]
                self.assertIsNone(roster.armor_output)
                self.assertEqual([contract.ARMOR_VALUE_INVALID], [reason.code for reason in roster.reasons])

    def test_one_invalid_alternative_blanks_roster_but_keeps_valid_item_evidence(self) -> None:
        rows = [
            {"troop_id": "x", "roster_index": "0", "slot": "Body", "item_id": "a", "item_found": "True", "head_armor": "0", "body_armor": "10", "arm_armor": "0", "leg_armor": "0"},
            {"troop_id": "x", "roster_index": "0", "slot": "Body", "item_id": "b", "item_found": "True", "head_armor": "0", "body_armor": "", "arm_armor": "0", "leg_armor": "0"},
        ]
        result = self.resolve(rows)
        self.assertEqual(["a"], [item.item_id for item in result.items])
        self.assertIsNone(result.rosters[0].armor_output)
        self.assertEqual(("a", "b"), result.rosters[0].source_item_ids)

    def test_alternative_index_is_deterministic_after_sorting(self) -> None:
        rows = [
            {"troop_id": "x", "roster_index": "0", "slot": "Body", "item_id": item, "item_found": "True", "head_armor": "0", "body_armor": "1", "arm_armor": "0", "leg_armor": "0", "source_row_number": number}
            for item, number in (("z", 8), ("a", 9), ("a", 7))
        ]
        items = self.resolve(rows).items
        self.assertEqual([("a", 7, 0), ("a", 9, 1), ("z", 8, 2)], [(item.item_id, item.source.row_number, item.alternative_index) for item in items])

    def test_results_and_sources_are_immutable_and_provenanced(self) -> None:
        result = self.resolve()
        item = result.items[0]
        self.assertEqual("a" * 64, item.source.sha256)
        with self.assertRaises(FrozenInstanceError):
            item.item_id = "changed"

    def test_wrapper_and_empty_input_are_deterministic(self) -> None:
        rows = fixture_rows()
        resolved = self.resolve(rows)
        wrapped = equipment.resolve_armor_rosters(
            rows, source_path="tests/fixtures/context_first/armor/armor_rows.csv",
            source_sha256="a" * 64, aggregation=AGGREGATION,
        )
        self.assertEqual(resolved.rosters, wrapped)
        self.assertEqual((), self.resolve([]).rosters)


if __name__ == "__main__":
    unittest.main()
