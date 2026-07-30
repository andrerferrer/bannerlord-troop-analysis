from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from normalization.rebuild_vanilla_audit import (  # noqa: E402
    parse_direct_items,
    parse_crafted_items,
)


ROT_BOW_SNIPPET = """<?xml version="1.0" encoding="utf-8"?>
<Items>
  <Item id="ravens_teeth_longbow" name="{=ravbow}Ravens' Teeth Longbow" culture="Culture.river" Type="Bow">
    <ItemComponent>
      <Weapon weapon_class="Bow" thrust_damage="96" thrust_damage_type="Pierce"
              speed_rating="94" missile_speed="87" accuracy="100" weapon_length="118" />
    </ItemComponent>
  </Item>
  <Item id="ravens_teeth_arrows" name="{=ravarrows}Ravens' Teeth Arrows" culture="Culture.river" Type="Arrows">
    <ItemComponent>
      <Weapon weapon_class="Arrow" stack_amount="33" thrust_damage="5" thrust_damage_type="Pierce" />
    </ItemComponent>
  </Item>
  <CraftedItem id="rot_crafted_in_assets" name="Crafted In Assets" crafting_template="OneHandedSword" culture="Culture.empire">
    <Pieces>
      <Piece id="blade_1" Type="Blade" />
    </Pieces>
  </CraftedItem>
</Items>
"""


class ItemXmlDiscoveryTests(unittest.TestCase):
    def test_parse_direct_items_reads_module_data_assets_outside_items_dir(self):
        """RoT puts bows in ModuleData/ROTassets.xml, not ModuleData/items/."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module_data = root / "ROT-Content" / "ModuleData"
            module_data.mkdir(parents=True)
            (module_data / "ROTassets.xml").write_text(ROT_BOW_SNIPPET, encoding="utf-8")

            direct = parse_direct_items(root, ["ROT-Content"])
            ids = set(direct["item_id"])
            self.assertIn("ravens_teeth_longbow", ids)
            self.assertIn("ravens_teeth_arrows", ids)
            bow = direct.loc[direct["item_id"].eq("ravens_teeth_longbow")].iloc[0]
            self.assertEqual(bow["type"], "Bow")
            self.assertEqual(bow["weapon_class"], "Bow")
            self.assertEqual(float(bow["thrust_damage"]), 96.0)

            crafted, _pieces = parse_crafted_items(root, ["ROT-Content"])
            self.assertIn("rot_crafted_in_assets", set(crafted["item_id"]))


if __name__ == "__main__":
    unittest.main()
