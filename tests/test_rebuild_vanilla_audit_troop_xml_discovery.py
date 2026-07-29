from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from normalization.rebuild_vanilla_audit import parse_troops  # noqa: E402


class TroopXmlDiscoveryTests(unittest.TestCase):
    def test_parse_troops_reads_npccharacters_outside_spnpccharacters_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            module = root / "ModTroops"
            module_data = module / "ModuleData" / "troops"
            module_data.mkdir(parents=True)
            (module_data / "troops_faction.xml").write_text(
                """<?xml version="1.0" encoding="utf-8"?>
<NPCCharacters>
  <NPCCharacter id="mod_soldier" name="Mod Soldier" occupation="Soldier" culture="Culture.empire" level="21" />
</NPCCharacters>
""",
                encoding="utf-8",
            )
            troops, edges, equipment, overrides = parse_troops(
                root,
                ["ModTroops"],
                baseline_modules=set(),
            )
            self.assertEqual(list(troops["troop_id"]), ["mod_soldier"])
            self.assertEqual(overrides.iloc[0]["change_type"], "novo")
            self.assertEqual(overrides.iloc[0]["winner_module"], "ModTroops")


if __name__ == "__main__":
    unittest.main()
