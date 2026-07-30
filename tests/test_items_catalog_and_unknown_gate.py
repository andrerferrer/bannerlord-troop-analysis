"""items_catalog + unknown_items fail-closed gate."""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from normalization.rebuild_vanilla_audit import (  # noqa: E402
    build_items_catalog,
    build_unknown_items_review_queue,
    gate_unknown_items,
)


class ItemsCatalogAndUnknownGateTests(unittest.TestCase):
    def test_build_items_catalog_unions_direct_and_crafted(self) -> None:
        direct = pd.DataFrame(
            [
                {
                    "item_id": "ravens_teeth_longbow",
                    "name": "Ravens' Teeth Longbow",
                    "item_kind": "Item",
                    "type": "Bow",
                    "crafting_template": None,
                    "culture": "river",
                    "source_xml": "ROT-Content/ModuleData/ROTassets.xml",
                    "_module": "ROT-Content",
                    "_load_order_rank": 6,
                }
            ]
        )
        crafted = pd.DataFrame(
            [
                {
                    "item_id": "vlandia_sword_3_t4",
                    "name": "Sword",
                    "item_kind": "CraftedItem",
                    "type": "CraftedWeapon",
                    "crafting_template": "OneHandedSword",
                    "culture": "vlandia",
                    "source_xml": "SandBoxCore/ModuleData/items/x.xml",
                    "_module": "SandBoxCore",
                    "_load_order_rank": 2,
                }
            ]
        )
        catalog = build_items_catalog(direct, crafted)
        ids = set(catalog["item_id"])
        self.assertEqual(ids, {"ravens_teeth_longbow", "vlandia_sword_3_t4"})
        bow = catalog.loc[catalog["item_id"].eq("ravens_teeth_longbow")].iloc[0]
        self.assertEqual(bow["item_kind"], "Item")
        self.assertEqual(bow["type"], "Bow")
        self.assertEqual(bow["winner_module"], "ROT-Content")

    def test_unknown_soldier_item_is_blocking(self) -> None:
        troops = pd.DataFrame(
            [
                {
                    "troop_id": "ravens_teeth",
                    "name": "Ravens' Teeth",
                    "occupation": "Soldier",
                    "is_soldier": True,
                    "culture": "river",
                    "default_group": "Ranged",
                }
            ]
        )
        audit = pd.DataFrame(
            [
                {
                    "troop_id": "ravens_teeth",
                    "roster_index": 0,
                    "slot": "Item1",
                    "item_id": "missing_bow",
                    "item_found": False,
                    "troop_name": "Ravens' Teeth",
                    "occupation": "Soldier",
                    "culture": "river",
                    "default_group": "Ranged",
                }
            ]
        )
        queue, counters = build_unknown_items_review_queue(audit, troops, allowlist=None)
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue.iloc[0]["severity"], "blocking")
        self.assertEqual(counters["blocking"], 1)
        code = gate_unknown_items(counters, allow_unknown_items=False)
        self.assertEqual(code, 2)

    def test_allowlist_marks_allowed_and_does_not_block(self) -> None:
        troops = pd.DataFrame(
            [
                {
                    "troop_id": "t1",
                    "name": "T1",
                    "occupation": "Soldier",
                    "is_soldier": True,
                    "culture": "empire",
                    "default_group": "Infantry",
                }
            ]
        )
        audit = pd.DataFrame(
            [
                {
                    "troop_id": "t1",
                    "roster_index": 0,
                    "slot": "Item0",
                    "item_id": "known_gap_item",
                    "item_found": False,
                    "troop_name": "T1",
                    "occupation": "Soldier",
                    "culture": "empire",
                    "default_group": "Infantry",
                }
            ]
        )
        allowlist = pd.DataFrame(
            [
                {
                    "item_id": "known_gap_item",
                    "reason": "fixture allow",
                    "added_by": "test",
                    "date": "2026-07-30",
                }
            ]
        )
        queue, counters = build_unknown_items_review_queue(audit, troops, allowlist=allowlist)
        self.assertEqual(queue.iloc[0]["severity"], "allowed")
        self.assertEqual(queue.iloc[0]["allowlist_reason"], "fixture allow")
        self.assertEqual(counters["blocking"], 0)
        self.assertEqual(counters["allowed"], 1)
        self.assertEqual(gate_unknown_items(counters, allow_unknown_items=False), 0)

    def test_zero_soldier_scope_errors_when_troops_exist(self) -> None:
        troops = pd.DataFrame(
            [
                {
                    "troop_id": "t1",
                    "name": "T1",
                    "occupation": "Soldier",
                    "is_soldier": True,
                    "culture": "empire",
                    "default_group": "Infantry",
                }
            ]
        )
        # Empty audit → evaluated=0 but soldiers>0
        audit = pd.DataFrame(
            columns=[
                "troop_id",
                "roster_index",
                "slot",
                "item_id",
                "item_found",
                "troop_name",
                "occupation",
                "culture",
                "default_group",
            ]
        )
        with self.assertRaises(ValueError):
            build_unknown_items_review_queue(audit, troops, allowlist=None)

    def test_cli_exits_2_on_blocking_unknown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module = root / "Mod" / "ModuleData" / "items"
            module.mkdir(parents=True)
            (module / "items.xml").write_text(
                """<?xml version="1.0" encoding="utf-8"?>
<Items>
  <Item id="known_sword" name="Sword" Type="OneHandedWeapon">
    <ItemComponent><Weapon weapon_class="OneHandedSword" /></ItemComponent>
  </Item>
</Items>
""",
                encoding="utf-8",
            )
            troops_dir = root / "Mod" / "ModuleData"
            (troops_dir / "spnpccharacters.xml").write_text(
                """<?xml version="1.0" encoding="utf-8"?>
<NPCCharacters>
  <NPCCharacter id="mod_soldier" name="Mod Soldier" occupation="Soldier" culture="Culture.empire" level="21" default_group="Infantry">
    <skills><skill id="OneHanded" value="100" /></skills>
    <Equipments>
      <EquipmentRoster>
        <equipment slot="Item0" id="Item.missing_axe" />
      </EquipmentRoster>
    </Equipments>
  </NPCCharacter>
</NPCCharacters>
""",
                encoding="utf-8",
            )
            out = root / "audit"
            out.mkdir()
            proc = subprocess.run(
                [
                    sys.executable,
                    str(REPO / "scripts/normalization/rebuild_vanilla_audit.py"),
                    "--raw-xml-root",
                    str(root),
                    "--output-dir",
                    str(out),
                    "--track",
                    "fixture",
                    "--load-order",
                    "Mod",
                    "--baseline-modules",
                    "",
                ],
                cwd=REPO,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 2, proc.stderr + proc.stdout)
            queue_path = out / "fixture_unknown_items_review_queue.csv"
            self.assertTrue(queue_path.is_file())
            rows = list(csv.DictReader(queue_path.open(encoding="utf-8")))
            self.assertTrue(any(r["item_id"] == "missing_axe" and r["severity"] == "blocking" for r in rows))
            catalog_path = out / "fixture_items_catalog.csv"
            self.assertTrue(catalog_path.is_file())


if __name__ == "__main__":
    unittest.main()
