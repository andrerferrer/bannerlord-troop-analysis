# Troop overview — `realm_of_thrones` / `export_20260729_025002`

## Labels

- `evidence_basis=xml_structural`, `empirical=false` (ADR-004)
- Model: `role_scores_v1` conservative (crafted melee = proxy, not HTK)
- Package digest: `afef4c8483d4d27a228f13c78ed84f89fd624f9e7103d2801b1cec065eee767f`
- Rows scored: **1232**; after filters: **865** (excluded 367: untouched vanilla `change_type=inalterado` only)

## Why columns

- **Defensive:** `defense_score_base` (driver) + `armor_total` / `effective_armor` (raw) + shield/horse flags
- **Ranged:** `ranged_score_base` (driver) + `ranged_damage` (weapon+ammo thrust) + item + horse/shield
- **Offensive melee:** `crafted_melee_score_base` + template/item (**no real weapon damage** — template proxy only)
- **Skirmisher:** `throw_score_base` + `throw_damage` when the throw item is a direct `Thrown` weapon (crafted javelins stay proxy-only)

## Filters

- Drop `change_type=inalterado` from the track override report (vanilla baseline troops the mod did not add/override)
- No name filters (Greyjoy Kraken lines, giants, specials stay if mod-owned)
- Full ranked lists below — filter locally as needed
- Intra-track only; do not compare ranks across tracks

## Ranked — Ranged (184 troops)

| rank | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | has_horse | has_shield | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Mammoth Riding Giant | giant_rider | 100.0 | 100.0 | 130.0 | giant_bow | True | False | Ranged Troops | freefolk | 31.0 | main_or_minor_line |
| 2 | Giant Archer | giant_archer | 88.5 | 100.0 | 130.0 | giant_bow | False | False | Ranged Troops | freefolk | 31.0 | main_or_minor_line |
| 3 | Myrish Artisan of War | myrish_artisan | 88.1 | 87.5 | 105.0 | crossbow_f | False | True | Ranged Troops | myrish | 31.0 | main_or_minor_line |
| 4 | Qartheen Enthroned Guardian | enthroned_guardian | 85.7 | 91.0 | 98.0 | qarth_longbow | False | True | Ranged Troops | qartheen | 31.0 | main_or_minor_line |
| 5 | Ravens' Teeth | ravens_teeth | 84.7 | 97.2 | 101.0 | ravens_teeth_longbow | False | False | Ranged Troops | river | 31.0 | main_or_minor_line |
| 6 | Frey Assassin | frey_assassin | 83.2 | 85.4 | 98.0 | crossbow_d | False | False | Ranged Troops | river | 31.0 | main_or_minor_line |
| 7 | Goldenheart Warrior | summer_master_longbowman | 80.8 | 94.7 | 101.0 | goldenheart_longbow | False | False | Ranged Troops | summer | 31.0 | main_or_minor_line |
| 8 | Mormont Bowmaiden | mormont_bowmaiden | 75.6 | 74.2 | 68.0 | woodland_longbow | False | False | Ranged Troops | battania | 31.0 | main_or_minor_line |
| 9 | Greyjoy Sniper | greyjoy_sniper | 75.0 | 77.3 | 73.0 | lowland_yew_bow | False | False | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 10 | Elder Giant | elder_giant | 69.4 | 100.0 | 130.0 | giant_bow | False | False | Ranged Troops | freefolk | 35.0 | main_or_minor_line |
| 11 | Triarch Guardian | triarch_guardian | 54.3 | 68.8 | 58.0 | steppe_war_bow | False | False | Ranged Troops | volantine | 31.0 | main_or_minor_line |
| 12 | Night's Watch Protector of the Realm | nightswatch_protector | 52.1 | 67.2 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | nightswatch | 31.0 | main_or_minor_line |
| 13 | Mormont Mounted Huntress | mormont_mounted_huntress | 48.3 | 67.7 | 57.0 | steppe_war_bow | True | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 14 | Qartheen Pureborn Champion | qartheen_champion | 45.3 | 89.4 | 97.0 | qarth_longbow | False | True | Ranged Troops | qartheen | 26.0 | main_or_minor_line |
| 15 | Myrish Master Crossbowman | myrish_master_crossbowman | 44.5 | 79.5 | 89.0 | crossbow_g | False | True | Ranged Troops | myrish | 26.0 | main_or_minor_line |
| 16 | Pentoshi Mounted Archer | pentoshi_mounted_archer | 42.6 | 65.0 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | pentoshi | 26.0 | main_or_minor_line |
| 17 | Gilded Bolt Rangers | golden_master_crossbowman | 40.7 | 82.0 | 93.0 | crossbow_c | False | False | Ranged Troops | volantine | 26.0 | main_or_minor_line |
| 18 | Qartheen Longbowman | qartheen_longbowman | 40.3 | 92.7 | 97.0 | qarth_longbow | False | False | Ranged Troops | qartheen | 26.0 | main_or_minor_line |
| 19 | Frey Sharpshooter | frey_sharpshooter | 39.6 | 85.4 | 98.0 | crossbow_d | False | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 20 | Hightower Marksmen | hightower_marksman | 38.2 | 88.9 | 102.0 | crossbow_f | False | False | Ranged Troops | reach | 26.0 | main_or_minor_line |
| 21 | Velaryon Marksman | velaryon_marksman | 38.1 | 88.9 | 102.0 | crossbow_f | False | False | Ranged Troops | dragonstone | 26.0 | main_or_minor_line |
| 22 | Tarth Elite Crossbowman | tarth_elite_crossbowman | 37.5 | 88.9 | 102.0 | crossbow_f | False | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 23 | Casterly Rock Master Crossbowman | casterly_master_crossbowman | 36.7 | 86.1 | 102.0 | crossbow_f | False | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 24 | Tarly Elite Crossbowman | tarly_elite_crossbowman | 36.4 | 86.1 | 102.0 | crossbow_f | False | False | Ranged Troops | reach | 26.0 | main_or_minor_line |
| 25 | Stormlands Heavy Crossbowman | stormlands_heavy_crossbowman | 34.4 | 81.4 | 91.0 | crossbow_c | False | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 26 | Blackwood Longbowman | blackwood_longbowman | 34.3 | 76.2 | 67.0 | woodland_longbow | False | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 27 | Grafton Elite Archer | grafton_elite_crossbowman | 34.0 | 81.5 | 88.0 | crossbow_g | False | False | Ranged Troops | vale | 26.0 | main_or_minor_line |
| 28 | Night's Watch Master Crossbowman | nightswatch_master_crossbowman | 33.4 | 81.4 | 91.0 | crossbow_c | False | False | Ranged Troops | nightswatch | 26.0 | main_or_minor_line |
| 29 | Tyrell Elite Longbowman | tyrell_longbowman | 33.2 | 79.2 | 72.0 | lowland_yew_bow | False | False | Ranged Troops | reach | 26.0 | main_or_minor_line |
| 30 | Mormont Veteran Huntress | mormont_veteran_huntress | 33.0 | 73.1 | 67.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 31 | Ghiscari Mounted Archer | ghiscari_mounted_archer | 32.2 | 66.7 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | ghiscari | 21.0 | main_or_minor_line |
| 32 | Stark Master Longbowman | stark_master_archer | 32.1 | 76.2 | 67.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 33 | Tully Longbowman | tully_longbowman | 31.2 | 70.3 | 60.0 | lowland_longbow | False | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 34 | Greyjoy Marksman | greyjoy_marksman | 30.7 | 73.2 | 72.0 | lowland_yew_bow | False | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 35 | Tigercloak Elite | tigercloak_master | 30.7 | 68.8 | 58.0 | steppe_war_bow | False | False | Ranged Troops | volantine | 26.0 | main_or_minor_line |
| 36 | Harlaw Longbowman | harlaw_longbowman | 30.2 | 73.2 | 72.0 | lowland_yew_bow | False | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 37 | Bolton Hunter | bolton_master_archer | 30.2 | 74.0 | 67.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 38 | Ibbenese Master Huntsman | ibbenese_master_huntsman | 30.1 | 74.2 | 68.0 | woodland_longbow | False | False | Ranged Troops | ibbenese | 26.0 | main_or_minor_line |
| 39 | Volantene Master Archer | tigercloak_master_archer | 29.9 | 68.8 | 58.0 | steppe_war_bow | False | False | Ranged Troops | volantine | 26.0 | main_or_minor_line |
| 40 | Glover Veteran Archer | glover_veteran_archer | 29.5 | 76.2 | 67.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 41 | Manderly Veteran Archer | manderly_veteran_archer | 28.9 | 76.2 | 67.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 42 | Skagosi Huntsman | skag_huntsman | 28.8 | 66.5 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | skagosi | 26.0 | main_or_minor_line |
| 43 | Cerwyn Veteran Archer | cerwyn_veteran_archer | 28.8 | 76.2 | 67.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 44 | Tyroshi Elite Archer | tyroshi_elite_archer | 28.5 | 66.5 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | tyroshi | 26.0 | main_or_minor_line |
| 45 | Riverlands Ranger | river_ranger | 28.5 | 70.3 | 60.0 | lowland_longbow | False | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 46 | Lyseni Elite Archer | lyseni_elite_archer | 28.3 | 66.2 | 54.0 | steppe_heavy_bow | False | False | Ranged Troops | lyseni | 26.0 | main_or_minor_line |
| 47 | Summer Isles Longbowman | summer_longbowman | 28.1 | 70.6 | 62.0 | tribal_bow | False | False | Ranged Troops | summer | 26.0 | main_or_minor_line |
| 48 | Night's Watch Master Ranger | nightswatch_master_ranger | 28.1 | 66.5 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | nightswatch | 26.0 | main_or_minor_line |
| 49 | Umber Marksman | umber_marksman | 27.6 | 74.0 | 67.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 50 | Pentoshi Elite Archer | pentoshi_elite_archer | 27.5 | 68.9 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | pentoshi | 26.0 | main_or_minor_line |
| 51 | Valyrian Master Archer | targaryen_master_archer | 27.4 | 68.5 | 57.0 | steppe_war_bow | False | False | Ranged Troops | valyrian | 26.0 | main_or_minor_line |
| 52 | Yi Ti Marksman | yiti_master_bowman | 27.3 | 68.0 | 56.0 | steppe_war_bow | False | False | Ranged Troops | yiti | 26.0 | main_or_minor_line |
| 53 | Free Folk Hawkeye | freefolk_hawkeye | 27.2 | 69.0 | 64.0 | woodland_yew_bow | False | False | Ranged Troops | freefolk | 26.0 | main_or_minor_line |
| 54 | Celtigar Veteran Archer | celtigar_veteran_archer | 27.0 | 67.7 | 59.0 | lowland_longbow | False | False | Ranged Troops | dragonstone | 26.0 | main_or_minor_line |
| 55 | Sarnori Longbowman | sarnor_longbowman | 26.7 | 68.0 | 60.0 | lowland_longbow | False | False | Ranged Troops | sarnor | 26.0 | main_or_minor_line |
| 56 | Baratheon Longbowman | baratheon_longbowman | 26.6 | 67.7 | 59.0 | lowland_longbow | False | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 57 | Myrish Elite Archer | myrish_elite_archer | 26.6 | 66.9 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | myrish | 26.0 | main_or_minor_line |
| 58 | Ghiscari Manticore | ghiscari_manticore | 26.5 | 66.7 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | ghiscari | 26.0 | main_or_minor_line |
| 59 | Gold Cloak Sniper | goldcloak_master_archer | 26.4 | 67.2 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | crownlands | 26.0 | main_or_minor_line |
| 60 | Royce Veteran Archer | royce_veteran_archer | 26.4 | 72.4 | 64.0 | woodland_yew_bow | False | False | Ranged Troops | vale | 26.0 | main_or_minor_line |
| 61 | Frey Veteran Crossbowman | frey_veteran_crossbowman | 26.3 | 81.5 | 87.0 | crossbow_g | False | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 62 | Bracken Elite Archer | bracken_elite_archer | 26.2 | 66.5 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 63 | Qohorik Elite Archer | qohorik_elite_archer | 26.2 | 66.7 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | qohorik | 26.0 | main_or_minor_line |
| 64 | Reach Master Archer | reach_master_archer | 26.2 | 67.2 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | reach | 26.0 | main_or_minor_line |
| 65 | Westerling Elite Archer | westerling_elite_archer | 26.2 | 66.5 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 66 | Norvoshi Master Archer | norvos_master_archer | 26.1 | 66.9 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | norvos | 26.0 | main_or_minor_line |
| 67 | Mallister Elite Archer | mallister_elite_archer | 26.0 | 66.5 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 68 | Arryn Master Archer | arryn_master_archer | 25.9 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | vale | 26.0 | main_or_minor_line |
| 69 | Myrish Elite Crossbowman | myrish_elite_crossbowman | 25.4 | 77.7 | 86.0 | crossbow_b | False | False | Ranged Troops | myrish | 21.0 | main_or_minor_line |
| 70 | Gleaming Shaft Marksmen | golden_veteran_crossbowman | 25.1 | 82.0 | 93.0 | crossbow_c | False | False | Ranged Troops | volantine | 21.0 | main_or_minor_line |
| 71 | Mormont Huntress | mormont_huntress | 24.7 | 73.1 | 67.0 | woodland_longbow | False | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 72 | Karstark Elite Archer | karstark_elite_archer | 24.3 | 68.0 | 60.0 | lowland_longbow | False | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 73 | Clegane Elite Archer | clegane_elite_archer | 24.2 | 68.0 | 60.0 | lowland_longbow | False | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 74 | Lannister Longbowman | lannister_longbowman | 24.0 | 67.7 | 59.0 | lowland_longbow | False | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 75 | Stormlands Master Archer | stormlands_master_archer | 24.0 | 66.5 | 53.0 | composite_bow | False | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 76 | Night's Watch Elite Crossbowman | nightswatch_elite_crossbowman | 23.9 | 81.4 | 91.0 | crossbow_c | False | False | Ranged Troops | nightswatch | 21.0 | main_or_minor_line |
| 77 | Casterly Rock Crossbowman | casterly_crossbowman | 23.8 | 81.5 | 95.0 | crossbow_d | False | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 78 | Dragonstone Elite Archer | dragonstone_elite_archer | 23.7 | 66.9 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | dragonstone | 26.0 | main_or_minor_line |
| 79 | Dondarrion Veteran Bowman | dondarion_veteran_bowman | 23.5 | 66.5 | 53.0 | composite_bow | False | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 80 | Tarly Crossbowman | tarly_crossbowman | 23.0 | 81.5 | 95.0 | crossbow_d | False | False | Ranged Troops | reach | 21.0 | main_or_minor_line |
| 81 | Vale Master Archer | vale_master_archer | 22.9 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | vale | 26.0 | main_or_minor_line |
| 82 | Hightower Crossbowman | hightower_crossbowman | 22.5 | 78.7 | 87.0 | crossbow_g | False | False | Ranged Troops | reach | 21.0 | main_or_minor_line |
| 83 | Martell Veteran Archer | martell_veteran_archer | 22.2 | 62.7 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 84 | Yronwood Veteran Archer | yronwood_veteran_archer | 22.2 | 62.7 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 85 | Dexterous Wight | dexterous_wight | 22.2 | 61.3 | 47.0 | nordic_shortbow | False | False | Ranged Troops | whitewalker | 26.0 | main_or_minor_line |
| 86 | Tarth Crossbowman | tarth_crossbowman | 21.8 | 78.7 | 87.0 | crossbow_g | False | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 87 | Velaryon Crossbowman | velaryon_crossbowman | 21.8 | 78.7 | 87.0 | crossbow_g | False | False | Ranged Troops | dragonstone | 21.0 | main_or_minor_line |
| 88 | Dayne Veteran Archer | dayne_veteran_archer | 21.8 | 62.7 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 89 | Qohorik Archer | qohorik_archer | 20.3 | 65.9 | 54.0 | steppe_heavy_bow | False | False | Ranged Troops | qohorik | 21.0 | main_or_minor_line |
| 90 | Tigercloak | tigercloak_elite | 20.0 | 68.0 | 56.0 | steppe_war_bow | False | False | Ranged Troops | volantine | 21.0 | main_or_minor_line |
| 91 | Blackwood Archer | blackwood_archer | 19.5 | 69.5 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 92 | Tyrell Longbowman | tyrell_bowman | 19.5 | 70.3 | 60.0 | lowland_longbow | False | False | Ranged Troops | reach | 21.0 | main_or_minor_line |
| 93 | Grafton Archer | grafton_crossbowman | 19.0 | 75.3 | 79.0 | crossbow_e | False | False | Ranged Troops | vale | 21.0 | main_or_minor_line |
| 94 | Tully Archer | tully_archer | 19.0 | 68.3 | 54.0 | composite_bow | False | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 95 | Bolton Veteran Archer | bolton_elite_archer | 18.8 | 68.0 | 60.0 | lowland_longbow | False | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 96 | Night's Watch Elite Ranger | nightswatch_elite_ranger | 18.6 | 64.6 | 52.0 | glen_ranger_bow | False | False | Ranged Troops | nightswatch | 21.0 | main_or_minor_line |
| 97 | Riverlands Elite Archer | river_elite_archer | 18.3 | 68.3 | 54.0 | composite_bow | False | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 98 | Volantene Archer | tigercloak_archer | 18.2 | 68.0 | 56.0 | steppe_war_bow | False | False | Ranged Troops | volantine | 21.0 | main_or_minor_line |
| 99 | Arryn Archer | arryn_archer | 17.9 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | vale | 21.0 | main_or_minor_line |
| 100 | Baratheon Archer | baratheon_archer | 17.8 | 66.5 | 53.0 | composite_bow | False | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 101 | Lyseni Archer | lyseni_archer | 17.4 | 66.5 | 53.0 | composite_bow | False | False | Ranged Troops | lyseni | 21.0 | main_or_minor_line |
| 102 | Tyroshi Archer | tyroshi_archer | 17.1 | 66.8 | 54.0 | composite_bow | False | False | Ranged Troops | tyroshi | 21.0 | main_or_minor_line |
| 103 | Ibbenese Hunter | ibbenese_hunter | 16.8 | 62.7 | 52.0 | glen_ranger_bow | False | False | Ranged Troops | ibbenese | 21.0 | main_or_minor_line |
| 104 | Pentoshi Archer | pentoshi_archer | 16.8 | 56.5 | 43.0 | steppe_bow | False | False | Ranged Troops | pentoshi | 21.0 | main_or_minor_line |
| 105 | Karstark Archer | karstark_archer | 16.5 | 68.0 | 60.0 | lowland_longbow | False | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 106 | Valyrian Archer | targaryen_archer | 16.5 | 66.9 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | valyrian | 21.0 | main_or_minor_line |
| 107 | Stormlands Crossbowman | stormlands_crossbowman | 16.4 | 68.0 | 69.0 | crossbow_a | False | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 108 | Yi Ti Archer | yiti_veteran_bowman | 16.4 | 66.7 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | yiti | 21.0 | main_or_minor_line |
| 109 | Yronwood Archer | yronwood_archer | 16.2 | 66.0 | 54.0 | composite_bow | False | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 110 | Free Folk Sharpshooter | freefolk_sharpshooter | 16.1 | 61.3 | 47.0 | nordic_shortbow | False | False | Ranged Troops | freefolk | 21.0 | main_or_minor_line |
| 111 | Celtigar Archer | celtigar_archer | 15.9 | 63.3 | 48.0 | nordic_shortbow | False | False | Ranged Troops | dragonstone | 21.0 | main_or_minor_line |
| 112 | Norvoshi Elite Archer | norvos_elite_archer | 15.9 | 66.9 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | norvos | 21.0 | main_or_minor_line |
| 113 | Summer Isles Archer | summer_veteran_bowman | 15.9 | 68.1 | 59.0 | tribal_bow | False | False | Ranged Troops | summer | 21.0 | main_or_minor_line |
| 114 | Lannister Archer | lannister_archer | 15.8 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 115 | Stormlands Elite Archer | stormlands_elite_archer | 15.8 | 66.5 | 53.0 | composite_bow | False | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 116 | Dondarrion Bowman | dondarion_bowman | 15.8 | 66.5 | 53.0 | composite_bow | False | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 117 | Bracken Archer | bracken_archer | 15.8 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 118 | Westerling Archer | westerling_archer | 15.7 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 119 | Qarthene Veteran Archer | qartheen_elite_archer | 15.7 | 66.1 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | qartheen | 21.0 | main_or_minor_line |
| 120 | Dayne Archer | dayne_archer | 15.7 | 66.0 | 54.0 | composite_bow | False | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 121 | Mallister Archer | mallister_archer | 15.6 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 122 | Ghiscari Elite Archer | ghiscari_elite_archer | 15.5 | 66.1 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | ghiscari | 21.0 | main_or_minor_line |
| 123 | Myrish Crossbowman | myrish_crossbowman | 15.4 | 77.7 | 86.0 | crossbow_b | False | False | Ranged Troops | myrish | 16.0 | main_or_minor_line |
| 124 | Royce Archer | royce_archer | 15.4 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | vale | 21.0 | main_or_minor_line |
| 125 | Sarnori Elite Archer | sarnor_elite_archer | 15.4 | 66.8 | 54.0 | composite_bow | False | False | Ranged Troops | sarnor | 21.0 | main_or_minor_line |
| 126 | Cerwyn Archer | cerwyn_archer | 15.3 | 64.1 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 127 | Dragonstone Archer | dragonstone_archer | 15.3 | 66.9 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | dragonstone | 21.0 | main_or_minor_line |
| 128 | Gold Cloak Elite Archer | goldcloak_elite_archer | 15.2 | 64.6 | 52.0 | glen_ranger_bow | False | False | Ranged Troops | crownlands | 21.0 | main_or_minor_line |
| 129 | Vale Elite Archer | vale_elite_archer | 15.1 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | vale | 21.0 | main_or_minor_line |
| 130 | Manderly Archer | manderly_archer | 14.9 | 64.1 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 131 | Glover Archer | glover_archer | 14.9 | 64.1 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 132 | Stark Longbowman | stark_archer | 14.9 | 64.1 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 133 | Martell Archer | martell_archer | 14.8 | 63.0 | 54.0 | composite_bow | False | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 134 | Umber Archer | umber_archer | 14.7 | 63.5 | 49.0 | nordic_shortbow | False | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 135 | Clegane Archer | clegane_archer | 14.7 | 63.5 | 49.0 | nordic_shortbow | False | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 136 | Reach Elite Archer | reach_elite_archer | 14.6 | 64.6 | 52.0 | glen_ranger_bow | False | False | Ranged Troops | reach | 21.0 | main_or_minor_line |
| 137 | Harlaw Archer | harlaw_archer | 14.5 | 63.0 | 54.0 | composite_bow | False | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 138 | Greyjoy Archer | greyjoy_archer | 14.5 | 63.0 | 54.0 | composite_bow | False | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 139 | Skagosi Archer | skag_archer | 13.8 | 55.5 | 44.0 | mountain_hunting_bow | False | False | Ranged Troops | skagosi | 21.0 | main_or_minor_line |
| 140 | Myrish Archer | myrish_archer | 12.8 | 56.5 | 42.0 | steppe_bow | False | False | Ranged Troops | myrish | 21.0 | main_or_minor_line |
| 141 | Mormont Trapper | mormont_trapper | 12.4 | 63.3 | 47.0 | nordic_shortbow | False | False | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 142 | Night's Watch Ranger | nightswatch_ranger | 11.0 | 64.6 | 52.0 | glen_ranger_bow | False | False | Ranged Troops | nightswatch | 16.0 | main_or_minor_line |
| 143 | Vale Archer | vale_archer | 10.1 | 66.5 | 52.0 | composite_bow | False | False | Ranged Troops | vale | 16.0 | main_or_minor_line |
| 144 | Blackwood Bowman | blackwood_bowman | 9.7 | 63.3 | 47.0 | nordic_shortbow | False | False | Ranged Troops | river | 16.0 | main_or_minor_line |
| 145 | Riverlands Archer | river_archer | 8.9 | 62.7 | 52.0 | composite_bow | False | False | Ranged Troops | river | 16.0 | main_or_minor_line |
| 146 | Frey Crossbowman | frey_crossbowman | 8.4 | 65.2 | 69.0 | crossbow_a | False | False | Ranged Troops | river | 16.0 | main_or_minor_line |
| 147 | Bolton Archer | bolton_archer | 8.2 | 58.6 | 42.0 | mountain_hunting_bow | False | False | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 148 | Goldenmark Marksmen | golden_crossbowman | 7.8 | 65.2 | 69.0 | crossbow_a | False | False | Ranged Troops | volantine | 16.0 | main_or_minor_line |
| 149 | Baratheon Bowman | baratheon_bowman | 7.8 | 58.3 | 41.0 | hunting_bow | False | False | Ranged Troops | stormlands | 16.0 | main_or_minor_line |
| 150 | Tyroshi Bowman | tyroshi_bowman | 7.6 | 63.4 | 54.0 | composite_bow | False | False | Ranged Troops | tyroshi | 16.0 | main_or_minor_line |
| 151 | Qohorik Bowman | qohorik_bowman | 7.5 | 62.9 | 53.0 | composite_bow | False | False | Ranged Troops | qohorik | 16.0 | main_or_minor_line |
| 152 | Lyseni Bowman | lyseni_bowman | 7.5 | 63.0 | 53.0 | composite_bow | False | False | Ranged Troops | lyseni | 16.0 | main_or_minor_line |
| 153 | Summer Isles Bowman | summer_bowman | 7.5 | 65.3 | 59.0 | tribal_bow | False | False | Ranged Troops | summer | 16.0 | main_or_minor_line |
| 154 | Night's Watch Crossbowman | nightswatch_crossbowman | 7.3 | 65.2 | 69.0 | crossbow_a | False | False | Ranged Troops | nightswatch | 16.0 | main_or_minor_line |
| 155 | Free Folk Archer | freefolk_archer | 6.6 | 53.8 | 42.0 | mountain_hunting_bow | False | False | Ranged Troops | freefolk | 16.0 | main_or_minor_line |
| 156 | Gold Cloak Archer | goldcloak_archer | 6.3 | 58.3 | 41.0 | hunting_bow | False | False | Ranged Troops | crownlands | 16.0 | main_or_minor_line |
| 157 | Stormlands Archer | stormlands_archer | 5.7 | 58.3 | 41.0 | hunting_bow | False | False | Ranged Troops | stormlands | 16.0 | main_or_minor_line |
| 158 | Qartheen Archer | qartheen_archer | 5.7 | 56.5 | 42.0 | steppe_bow | False | False | Ranged Troops | qartheen | 16.0 | main_or_minor_line |
| 159 | Ghiscari Archer | ghiscari_archer | 5.4 | 56.5 | 42.0 | steppe_bow | False | False | Ranged Troops | ghiscari | 16.0 | main_or_minor_line |
| 160 | Reach Archer | reach_archer | 5.4 | 58.3 | 41.0 | hunting_bow | False | False | Ranged Troops | reach | 16.0 | main_or_minor_line |
| 161 | Reach Voulgier | reach_hookman | 5.4 | 54.8 | 42.0 | hunting_bow | False | False | Ranged Troops | reach | 16.0 | main_or_minor_line |
| 162 | Martell Bowman | martell_bowman | 5.3 | 54.8 | 43.0 | steppe_bow | False | False | Ranged Troops | aserai | 16.0 | main_or_minor_line |
| 163 | Yi Ti Bowman | yiti_bowman | 5.2 | 54.8 | 43.0 | steppe_bow | False | False | Ranged Troops | yiti | 16.0 | main_or_minor_line |
| 164 | Lannister Bowman | lannister_bowman | 5.1 | 54.8 | 42.0 | mountain_hunting_bow | False | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 165 | Sarnori Archer | sarnor_archer | 5.1 | 56.5 | 42.0 | steppe_bow | False | False | Ranged Troops | sarnor | 16.0 | main_or_minor_line |
| 166 | Valyrian Bowman | targaryen_bowman | 4.9 | 55.0 | 43.0 | steppe_bow | False | False | Ranged Troops | valyrian | 16.0 | main_or_minor_line |
| 167 | Stark Bowman | stark_bowman | 4.8 | 54.8 | 42.0 | mountain_hunting_bow | False | False | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 168 | Myrish Bowman | myrish_bowman | 4.8 | 53.7 | 42.0 | steppe_bow | False | False | Ranged Troops | myrish | 16.0 | main_or_minor_line |
| 169 | Norvoshi Archer | norvos_archer | 4.5 | 55.0 | 43.0 | steppe_bow | False | False | Ranged Troops | norvos | 16.0 | main_or_minor_line |
| 170 | Volantene Bowman | volantine_bowman | 4.4 | 54.8 | 43.0 | steppe_bow | False | False | Ranged Troops | volantine | 16.0 | main_or_minor_line |
| 171 | Tigercloak Elite Initiate | tigercloak_elite_initiate | 4.4 | 54.8 | 43.0 | steppe_bow | False | False | Ranged Troops | volantine | 16.0 | main_or_minor_line |
| 172 | Dragonstone Bowman | dragonstone_bowman | 4.4 | 54.7 | 42.0 | steppe_bow | False | False | Ranged Troops | dragonstone | 16.0 | main_or_minor_line |
| 173 | Skagosi Bowman | skag_bowman | 3.6 | 53.8 | 42.0 | mountain_hunting_bow | False | False | Ranged Troops | skagosi | 16.0 | main_or_minor_line |
| 174 | Free Folk Bowman | freefolk_bowman | 1.5 | 54.2 | 41.0 | mountain_hunting_bow | False | False | Ranged Troops | freefolk | 11.0 | main_or_minor_line |
| 175 | Norvoshi Bowman | norvos_bowman | 1.3 | 55.0 | 43.0 | steppe_bow | False | False | Ranged Troops | norvos | 11.0 | main_or_minor_line |
| 176 | Stormlands Bowman | stormlands_bowman | 1.3 | 54.5 | 41.0 | hunting_bow | False | False | Ranged Troops | stormlands | 11.0 | main_or_minor_line |
| 177 | Reach Bowman | reach_bowman | 1.2 | 54.5 | 41.0 | hunting_bow | False | False | Ranged Troops | reach | 11.0 | main_or_minor_line |
| 178 | Crownlands Bowman | crownlands_bowman | 1.2 | 54.5 | 41.0 | hunting_bow | False | False | Ranged Troops | crownlands | 11.0 | main_or_minor_line |
| 179 | Night's Watch Ranger Recruit | nightswatch_ranger_recruit | 1.1 | 54.5 | 41.0 | hunting_bow | False | False | Ranged Troops | nightswatch | 11.0 | main_or_minor_line |
| 180 | Vale Bowman | vale_bowman | 0.5 | 54.5 | 41.0 | hunting_bow | False | False | Ranged Troops | vale | 11.0 | main_or_minor_line |
| 181 | Riverlands Bowman | river_bowman | 0.5 | 54.5 | 41.0 | hunting_bow | False | False | Ranged Troops | river | 11.0 | main_or_minor_line |
| 182 | Sarnori Bowman | sarnor_bowman | 0.1 | 53.7 | 42.0 | steppe_bow | False | False | Ranged Troops | sarnor | 11.0 | main_or_minor_line |
| 183 | Ghiscari Bowman | ghiscari_bowman | 0.1 | 53.7 | 42.0 | steppe_bow | False | False | Ranged Troops | ghiscari | 11.0 | main_or_minor_line |
| 184 | Qartheen Bowman | qartheen_bowman | 0.0 | 53.7 | 42.0 | steppe_bow | False | False | Ranged Troops | qartheen | 11.0 | main_or_minor_line |


## Ranked — Defensive (488 troops)

| rank | troop_name | troop_id | defensive_role_score | defense_score_base | armor_total | effective_armor | has_shield | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Golden Company Mahout | golden_elite_pikeman | 100.0 | 100.0 | 149.0 | 49.1 | True | True | Skirmishers | volantine | 31.0 | main_or_minor_line |
| 2 | Golden Company Elephant Rider | golden_horseman | 94.3 | 95.1 | 146.0 | 47.7 | True | True | Defensive Troops | volantine | 26.0 | main_or_minor_line |
| 3 | Volantene Mahout | tigercloak_camel_cavalry | 83.3 | 82.1 | 168.0 | 51.7 | True | True | Defensive Troops | volantine | 26.0 | main_or_minor_line |
| 4 | Mammoth Riding Giant | giant_rider | 71.9 | 86.9 | 240.0 | 70.0 | False | True | Ranged Troops | freefolk | 31.0 | main_or_minor_line |
| 5 | Captain of the Kingsguard | mounted_kingsguard | 71.9 | 65.8 | 211.0 | 65.0 | True | True | Defensive Troops | crownlands | 31.0 | main_or_minor_line |
| 6 | Mallister Eagle Knight | mallister_knight | 71.4 | 68.2 | 208.0 | 64.2 | True | True | Defensive Troops | river | 31.0 | main_or_minor_line |
| 7 | Captain of the Queen's Guard | queensguard_captain | 70.0 | 66.6 | 204.0 | 63.1 | True | True | Defensive Troops | valyrian | 31.0 | main_or_minor_line |
| 8 | Stark Cavalry | stark_cavalry | 69.9 | 66.0 | 186.0 | 61.6 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 9 | Valyrian Cavalry | targaryen_dragonknight | 69.9 | 64.8 | 184.0 | 60.0 | True | True | Skirmishers | valyrian | 26.0 | main_or_minor_line |
| 10 | Targaryen Queen's Guard | targ_queensguard | 69.7 | 66.2 | 198.0 | 62.5 | True | True | Defensive Troops | valyrian | 26.0 | main_or_minor_line |
| 11 | Arryn Winged Knight | arryn_moonknight | 68.8 | 65.2 | 221.0 | 66.7 | True | True | Defensive Troops | vale | 31.0 | main_or_minor_line |
| 12 | Dondarrion Boltknight | dondarion_boltknight | 68.4 | 64.7 | 195.0 | 59.6 | True | True | Defensive Troops | stormlands | 31.0 | main_or_minor_line |
| 13 | Magister Guard Elite | magister_guard | 68.2 | 62.8 | 197.0 | 60.2 | True | True | Skirmishers | pentoshi | 31.0 | main_or_minor_line |
| 14 | Lannister Prideknight | lannister_prideknight | 68.0 | 64.3 | 178.0 | 57.2 | True | True | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 15 | Grafton Horseman | grafton_horseman | 68.0 | 64.2 | 187.0 | 59.5 | True | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 16 | Lannister Knight | lannister_knight | 67.8 | 64.1 | 179.0 | 57.9 | True | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 17 | White Harbor Knight Commander | whiteharbor_knight_commander | 67.8 | 64.0 | 191.0 | 57.8 | True | True | Defensive Troops | battania | 31.0 | main_or_minor_line |
| 18 | White Harbor Elite Knight | whiteharbor_elite_knight | 67.4 | 63.6 | 190.0 | 57.7 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 19 | Realm Knight | realm_knight | 67.4 | 61.8 | 182.0 | 57.4 | True | True | Skirmishers | crownlands | 26.0 | main_or_minor_line |
| 20 | Westerling Knight | westerling_horseman | 66.9 | 62.9 | 194.0 | 57.3 | True | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 21 | Dragonstone Shock Knight | dragonstone_shock_knight | 66.8 | 61.2 | 177.0 | 55.1 | True | True | Skirmishers | dragonstone | 26.0 | main_or_minor_line |
| 22 | Dondarrion Knight | dondarion_knight | 66.7 | 62.8 | 184.0 | 56.2 | True | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 23 | Valyrian Dragonlord Protector | valyrian_dragonlord_protector | 66.5 | 62.5 | 190.0 | 60.6 | True | True | Defensive Troops | valyrian | 31.0 | main_or_minor_line |
| 24 | Knights of Starfall | dayne_starfall_knights | 66.4 | 60.7 | 197.0 | 60.0 | True | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 25 | Casterly Rock Champion | casterly_champion | 66.2 | 60.4 | 191.0 | 58.4 | True | True | Skirmishers | vlandia | 26.0 | main_or_minor_line |
| 26 | Valyrian Dragonknight | valyrian_dragonknight | 66.1 | 62.0 | 178.0 | 59.8 | True | True | Defensive Troops | valyrian | 26.0 | main_or_minor_line |
| 27 | Realm Paladin | realm_paladin | 65.7 | 59.9 | 194.0 | 58.5 | True | True | Skirmishers | crownlands | 31.0 | main_or_minor_line |
| 28 | Royce Heroine | royce_heroine | 65.6 | 61.5 | 165.0 | 48.2 | True | True | Defensive Troops | vale | 31.0 | main_or_minor_line |
| 29 | Reach Flower Knight | reach_flower_knight | 65.5 | 61.4 | 188.0 | 58.0 | True | True | Defensive Troops | reach | 31.0 | main_or_minor_line |
| 30 | Mallister Knight | mallister_horseman | 65.5 | 61.4 | 177.0 | 54.0 | True | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 31 | Black Goat Sacrificer | qohorik_goat_sacrificer | 65.1 | 59.2 | 183.0 | 53.3 | True | True | Skirmishers | qohorik | 31.0 | main_or_minor_line |
| 32 | Pentoshi Lancer | pentoshi_lancer | 65.0 | 60.7 | 191.0 | 59.1 | True | True | Defensive Troops | pentoshi | 26.0 | main_or_minor_line |
| 33 | Qohorik Lancer | qohorik_lancer | 64.9 | 60.6 | 180.0 | 55.8 | True | True | Defensive Troops | qohorik | 26.0 | main_or_minor_line |
| 34 | Royce Cavalrywomen | royce_cavalrywomen | 64.6 | 60.3 | 165.0 | 48.2 | True | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 35 | Queen's Man | dragonstone_steel_curtain | 64.5 | 58.5 | 177.0 | 55.1 | True | True | Skirmishers | dragonstone | 31.0 | main_or_minor_line |
| 36 | Baratheon Knight | baratheon_knight | 64.5 | 59.1 | 177.0 | 56.1 | True | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 37 | Knight of the Vale | vale_knight_of | 64.3 | 59.9 | 178.0 | 57.4 | True | True | Defensive Troops | vale | 31.0 | main_or_minor_line |
| 38 | Pentoshi Cavalry | pentoshi_cavalry | 64.0 | 59.6 | 171.0 | 54.6 | True | True | Defensive Troops | pentoshi | 26.0 | main_or_minor_line |
| 39 | Mormont Horseman | mormont_horseman | 63.6 | 59.1 | 171.0 | 54.2 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 40 | White Harbor Knight | whiteharbor_knight | 63.4 | 58.9 | 164.0 | 51.0 | True | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 41 | Tyrell Cavalier | tyrell_cavalier | 63.2 | 58.6 | 169.0 | 54.9 | True | True | Defensive Troops | reach | 31.0 | main_or_minor_line |
| 42 | Greyjoy Horseman | greyjoy_horseman | 62.9 | 56.7 | 164.0 | 50.8 | True | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 43 | Riverrun Captain | riverrun_captain | 62.4 | 57.7 | 172.0 | 52.7 | True | True | Defensive Troops | river | 31.0 | main_or_minor_line |
| 44 | Vale Elite Knight | vale_elite_knight | 62.2 | 57.4 | 157.0 | 55.2 | True | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 45 | Arryn Knight | arryn_knight | 62.0 | 57.3 | 188.0 | 52.9 | True | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 46 | Yi Ti Glaiveman | yiti_horseman | 61.9 | 57.1 | 177.0 | 52.1 | True | True | Defensive Troops | yiti | 26.0 | main_or_minor_line |
| 47 | Water Gardens Sentinel | garden_sentinel | 61.6 | 55.1 | 170.0 | 53.6 | True | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 48 | Skagosi Stoneborn Champion | skagosi_stoneborn_champion | 61.1 | 54.6 | 184.0 | 54.5 | True | True | Skirmishers | skagosi | 31.0 | main_or_minor_line |
| 49 | Dragonstone Horseman | dragonstone_horseman | 61.1 | 56.2 | 156.0 | 48.0 | True | True | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 50 | Clegane Brigand | clegane_horseman | 61.1 | 56.2 | 161.0 | 48.0 | True | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 51 | Boneway Guardian | boneway_guardian | 61.0 | 54.4 | 168.0 | 51.8 | True | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 52 | Myrish Cavalry | myrish_cavalry | 61.0 | 56.1 | 173.0 | 54.4 | True | True | Defensive Troops | myrish | 26.0 | main_or_minor_line |
| 53 | Blackwood Horseman | blackwood_horseman | 60.8 | 55.9 | 155.0 | 44.1 | True | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 54 | Martell Horseman | martell_horseman | 60.8 | 54.2 | 164.0 | 52.0 | True | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 55 | Stormlands Horseman | stormlands_horseman | 60.8 | 55.9 | 151.0 | 45.9 | True | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 56 | Dayne Knight | dayne_knight | 60.8 | 55.8 | 169.0 | 51.5 | True | True | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 57 | Hightower Cavalry | hightower_cavalry | 60.7 | 55.7 | 175.0 | 55.3 | True | True | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 58 | Bracken Horseman | bracken_horseman | 60.4 | 55.3 | 153.0 | 43.8 | True | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 59 | Vale Elite Voulgier | vale_elite_voulgier | 60.3 | 55.3 | 162.0 | 51.5 | True | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 60 | Vale Elite Lancer | vale_elite_lancer | 60.3 | 55.3 | 162.0 | 51.5 | True | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 61 | Skagosi Stoneborn | skagosi_stoneborn | 59.9 | 53.1 | 183.0 | 54.4 | True | True | Skirmishers | skagosi | 26.0 | main_or_minor_line |
| 62 | Yronwood Knight | yronwood_knight | 59.6 | 54.4 | 168.0 | 51.8 | True | True | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 63 | Bolton Cavalry | bolton_knight | 59.6 | 54.4 | 172.0 | 49.6 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 64 | Celtigar Knight | celtigar_knight | 59.2 | 54.0 | 192.0 | 58.6 | True | True | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 65 | Dragonstone Knight | dragonstone_knight | 59.1 | 52.2 | 170.0 | 53.9 | True | True | Skirmishers | dragonstone | 21.0 | main_or_minor_line |
| 66 | Umber Horseman | umber_horseman | 59.1 | 53.8 | 152.0 | 44.7 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 67 | Norvoshi Grand Bearded Priest | mounted_priest | 59.0 | 53.8 | 185.0 | 54.9 | True | True | Defensive Troops | norvos | 31.0 | main_or_minor_line |
| 68 | Harlaw Raider | harlaw_horseman | 58.9 | 52.0 | 180.0 | 55.8 | True | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 69 | Casterly Rock Knight | casterly_knight | 58.5 | 53.2 | 197.0 | 59.6 | True | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 70 | Riverlands Cavalry | river_calvary | 58.0 | 52.6 | 162.0 | 46.2 | True | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 71 | High King Guardian | sarnor_highking_guardian | 58.0 | 50.9 | 155.0 | 47.7 | True | True | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 72 | Lannister Horseman | lannister_horseman | 58.0 | 52.5 | 164.0 | 50.4 | True | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 73 | Reach Horseman | reach_knight | 57.9 | 52.4 | 156.0 | 45.8 | True | True | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 74 | Glover Horseman | glover_horseman | 57.3 | 51.7 | 165.0 | 52.8 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 75 | Tyrell Horseman | tyrell_knight | 57.1 | 51.5 | 149.0 | 44.6 | True | True | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 76 | Karstark Shock Cavalry | karstark_shock_cavalry | 56.8 | 51.1 | 153.0 | 46.3 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 77 | Night's Watch Horseman | nightswatch_horseman | 56.7 | 51.0 | 153.0 | 49.5 | True | True | Defensive Troops | nightswatch | 26.0 | main_or_minor_line |
| 78 | Tully Knight | tully_knight | 56.6 | 51.0 | 172.0 | 52.7 | True | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 79 | Skagosi Rider | skagosi_rider | 56.6 | 49.3 | 143.0 | 47.6 | True | True | Skirmishers | skagosi | 21.0 | main_or_minor_line |
| 80 | Velaryon Horseman | velaryon_horseman | 56.6 | 50.9 | 168.0 | 53.2 | True | True | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 81 | Tyroshi Cavalry | tyroshi_cavalry | 56.6 | 50.9 | 157.0 | 47.0 | True | True | Defensive Troops | tyroshi | 26.0 | main_or_minor_line |
| 82 | Lyseni Cavalry | lyseni_cavalry | 56.5 | 50.9 | 159.0 | 46.7 | True | True | Defensive Troops | lyseni | 26.0 | main_or_minor_line |
| 83 | Targaryen Knight | targ_knight | 56.1 | 50.3 | 142.0 | 47.4 | True | True | Defensive Troops | valyrian | 21.0 | main_or_minor_line |
| 84 | Valyrian Knight | valyrian_knight | 55.8 | 50.0 | 163.0 | 50.0 | True | True | Defensive Troops | valyrian | 21.0 | main_or_minor_line |
| 85 | Ibbenese Horseman | ibbenese_horseman | 55.8 | 49.9 | 167.0 | 49.6 | True | True | Defensive Troops | ibbenese | 26.0 | main_or_minor_line |
| 86 | Ghiscari Queen's Guard | ghiscari_queens_guard | 55.4 | 46.5 | 144.0 | 43.5 | True | True | Defensive Troops | ghiscari | 26.0 | main_or_minor_line |
| 87 | Yronwood Horseman | yronwood_horseman | 54.8 | 48.8 | 168.0 | 51.8 | True | True | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 88 | Tarth Horseman | tarth_horseman | 54.8 | 48.8 | 167.0 | 48.0 | True | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 89 | Valyrian Scout | valyrian_scout | 54.6 | 46.9 | 149.0 | 45.0 | True | True | Skirmishers | valyrian | 21.0 | main_or_minor_line |
| 90 | Free Folk Horseman | freefolk_horseman | 54.6 | 46.9 | 148.0 | 40.0 | True | True | Skirmishers | freefolk | 26.0 | main_or_minor_line |
| 91 | Norvoshi Priest Guard | norvos_priestguard | 54.4 | 48.3 | 154.0 | 45.5 | True | True | Defensive Troops | norvos | 26.0 | main_or_minor_line |
| 92 | Tarly Knight | tarly_knight | 54.3 | 48.2 | 174.0 | 56.6 | True | True | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 93 | Celtigar Horseman | celtigar_horseman | 54.1 | 48.1 | 166.0 | 47.2 | True | True | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 94 | Greyjoy Rider | greyjoy_rider | 53.7 | 47.5 | 164.0 | 50.8 | True | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 95 | Qohorik Horseman | qohorik_horseman | 52.6 | 46.2 | 149.0 | 43.5 | True | True | Defensive Troops | qohorik | 21.0 | main_or_minor_line |
| 96 | Martell Rider | martell_rider | 52.5 | 46.1 | 142.0 | 42.1 | True | True | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 97 | Stark Horseman | stark_horseman | 51.6 | 45.0 | 134.5 | 36.5 | True | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 98 | Pentoshi Horseman | pentoshi_horseman | 51.3 | 45.8 | 143.0 | 43.2 | True | True | Defensive Troops | pentoshi | 21.0 | main_or_minor_line |
| 99 | Cerwyn Horseman | cerwyn_horseman | 51.3 | 44.7 | 147.0 | 43.4 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 100 | Sarnori Cavalry | sarnor_cavalry | 51.1 | 44.5 | 129.0 | 37.3 | True | True | Defensive Troops | sarnor | 21.0 | main_or_minor_line |
| 101 | Baratheon Horseman | baratheon_horseman | 51.0 | 44.4 | 149.0 | 43.0 | True | True | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 102 | Gold Cloak Captain | goldcloak_captain | 51.0 | 44.4 | 154.0 | 46.2 | True | True | Defensive Troops | crownlands | 26.0 | main_or_minor_line |
| 103 | Dayne Horseman | dayne_horseman | 50.9 | 44.2 | 149.0 | 43.8 | True | True | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 104 | Qartheen Master Cameleer | qartheen_master_cameleer | 50.0 | 43.3 | 161.0 | 45.6 | True | True | Defensive Troops | qartheen | 26.0 | main_or_minor_line |
| 105 | Arryn Horseman | arryn_horseman | 49.8 | 43.0 | 125.0 | 41.1 | True | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 106 | Grafton Rider | grafton_rider | 49.6 | 42.7 | 122.0 | 39.6 | True | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 107 | Dragonstone Rider | dragonstone_rider | 49.5 | 42.7 | 136.0 | 37.8 | True | True | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 108 | Vale Lancer | vale_lancer | 49.3 | 42.4 | 121.0 | 39.7 | True | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 109 | Vale Voulgier | vale_voulgier | 49.3 | 42.4 | 121.0 | 39.7 | True | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 110 | Bolton Horseman | bolton_horseman | 49.3 | 42.4 | 124.0 | 40.4 | True | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 111 | Golden Steed Riders | golden_rider | 49.0 | 42.1 | 134.0 | 43.0 | True | True | Defensive Troops | volantine | 21.0 | main_or_minor_line |
| 112 | Hightower Horseman | hightower_horseman | 48.8 | 41.8 | 152.0 | 44.7 | True | True | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 113 | Dondarrion Horseman | dondarion_horseman | 48.3 | 41.2 | 117.0 | 34.6 | True | True | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 114 | Norvoshi Cavalry | norvos_cavalry | 48.2 | 41.2 | 154.0 | 45.5 | True | True | Defensive Troops | norvos | 21.0 | main_or_minor_line |
| 115 | Yi Ti Rider | yiti_rider | 48.2 | 41.1 | 137.0 | 43.3 | True | True | Defensive Troops | yiti | 21.0 | main_or_minor_line |
| 116 | Yi Ti Mounted Shi | yiti_samurai | 48.2 | 53.2 | 198.0 | 60.0 | False | True | Skirmishers | yiti | 31.0 | main_or_minor_line |
| 117 | Vale Knight | vale_knight | 48.0 | 40.9 | 130.0 | 43.2 | True | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 118 | Harlaw Scout | harlaw_rider | 47.9 | 40.8 | 158.0 | 42.7 | True | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 119 | Frey Horseman | frey_horseman | 47.8 | 40.7 | 141.0 | 43.2 | True | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 120 | Tarly Vanguard | tarly_vanguard | 47.8 | 47.3 | 176.0 | 56.8 | True | False | Skirmishers | reach | 31.0 | main_or_minor_line |
| 121 | Myrish Horseman | myrish_horseman | 47.4 | 40.2 | 150.0 | 43.9 | True | True | Defensive Troops | myrish | 21.0 | main_or_minor_line |
| 122 | Tully Rider | tully_rider | 46.9 | 39.6 | 119.0 | 34.1 | True | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 123 | Bracken Rider | bracken_rider | 46.7 | 39.3 | 118.0 | 33.7 | True | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 124 | Riverlands Horseman | river_horseman | 46.5 | 39.1 | 115.0 | 33.2 | True | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 125 | Westerling Scout | westerling_rider | 46.4 | 39.0 | 113.0 | 33.1 | True | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 126 | Summer Isles Horseman | summer_horseman | 46.3 | 38.9 | 154.0 | 48.4 | True | True | Defensive Troops | summer | 26.0 | main_or_minor_line |
| 127 | Velaryon Scout | velaryon_scout | 46.0 | 38.5 | 127.0 | 30.5 | True | True | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 128 | Qohorik Rider | qohorik_rider | 45.9 | 38.5 | 123.0 | 29.9 | True | True | Defensive Troops | qohorik | 16.0 | main_or_minor_line |
| 129 | Gold Cloak Rider | goldcloak_rider | 45.8 | 38.3 | 141.0 | 38.7 | True | True | Defensive Troops | crownlands | 21.0 | main_or_minor_line |
| 130 | Blackwood Scout | blackwood_scout | 45.8 | 38.3 | 111.0 | 31.9 | True | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 131 | Lyseni Horseman | lyseni_horseman | 45.4 | 37.9 | 135.0 | 36.4 | True | True | Defensive Troops | lyseni | 21.0 | main_or_minor_line |
| 132 | Tyroshi Horseman | tyroshi_horseman | 45.4 | 37.8 | 132.0 | 36.5 | True | True | Defensive Troops | tyroshi | 21.0 | main_or_minor_line |
| 133 | Karstark Outrider | karstark_outrider | 45.3 | 37.7 | 136.0 | 38.8 | True | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 134 | Celtigar Banneret | celtigar_banneret | 45.2 | 44.2 | 198.0 | 62.0 | True | False | Skirmishers | dragonstone | 31.0 | main_or_minor_line |
| 135 | Kingsguard | kingsguard_captain | 44.9 | 42.6 | 211.0 | 65.0 | True | False | Defensive Troops | crownlands | 26.0 | main_or_minor_line |
| 136 | Guardian of the Rock | casterly_guardian | 44.7 | 44.7 | 209.0 | 61.8 | True | False | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 137 | Stark Sworn Sword | stark_swornsword | 44.7 | 45.4 | 204.0 | 61.6 | True | False | Defensive Troops | battania | 31.0 | main_or_minor_line |
| 138 | Stark House Guard | stark_houseguard | 44.7 | 45.4 | 186.0 | 61.6 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 139 | Mallister House Guard | mallister_houseguard | 44.7 | 45.4 | 197.0 | 62.0 | True | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 140 | Tarly Horseman | tarly_horseman | 44.7 | 37.0 | 126.0 | 42.5 | True | True | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 141 | Lannister Officer | lannister_officer | 44.5 | 42.1 | 178.0 | 57.2 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 142 | Qartheen Cameleer | qartheen_cameleer | 44.5 | 36.7 | 134.0 | 36.3 | True | True | Defensive Troops | qartheen | 21.0 | main_or_minor_line |
| 143 | Royce Rider | royce_rider | 44.5 | 36.7 | 141.0 | 38.0 | True | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 144 | Grafton Flaming Knight | grafton_flameknight | 44.3 | 44.8 | 206.0 | 61.6 | True | False | Defensive Troops | vale | 31.0 | main_or_minor_line |
| 145 | Qartheen Camel Rider | qartheen_camel_rider | 44.2 | 36.4 | 122.0 | 35.7 | True | True | Defensive Troops | qartheen | 16.0 | main_or_minor_line |
| 146 | Mallister Horseman | mallister_rider | 44.1 | 36.3 | 106.0 | 28.3 | True | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 147 | Glover Rider | glover_rider | 43.9 | 36.1 | 142.0 | 42.2 | True | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 148 | Ibbenese Rider | ibbenese_rider | 43.9 | 36.1 | 134.0 | 36.2 | True | True | Defensive Troops | ibbenese | 21.0 | main_or_minor_line |
| 149 | Reach Rider | reach_rider | 43.9 | 36.1 | 129.0 | 34.7 | True | True | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 150 | Stark Pikeman | stark_pikeman | 43.8 | 45.4 | 186.0 | 61.6 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 151 | Volantene Rider | tigercloak_rider | 43.8 | 36.0 | 134.0 | 39.2 | True | True | Defensive Troops | volantine | 21.0 | main_or_minor_line |
| 152 | Casterly Rock Marshal | casterly_pikeman | 43.3 | 44.7 | 209.0 | 61.8 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 153 | Grafton House Guard | grafton_houseguard | 43.2 | 43.6 | 187.0 | 59.5 | True | False | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 154 | Westerling Hedgeknight | westerling_hedgeknight | 43.2 | 43.6 | 204.0 | 59.5 | True | False | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 155 | Casterly Rock Squire | casterly_squire | 43.2 | 35.3 | 116.0 | 39.7 | True | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 156 | Cerwyn Scout | cerwyn_scout | 43.2 | 35.3 | 137.0 | 36.9 | True | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 157 | Valyrian Captain | valyrian_captain | 42.8 | 43.2 | 184.0 | 60.0 | True | False | Defensive Troops | valyrian | 26.0 | main_or_minor_line |
| 158 | Bolton Flayer | bolton_flayer | 42.8 | 41.2 | 207.0 | 62.1 | True | False | Skirmishers | battania | 31.0 | main_or_minor_line |
| 159 | Ibbenese Navigator | ibbenese_navigator | 42.5 | 41.1 | 187.0 | 54.6 | True | False | Skirmishers | ibbenese | 31.0 | main_or_minor_line |
| 160 | Pentoshi Spearman | pentoshi_spearman | 42.4 | 41.0 | 167.0 | 54.4 | True | False | Skirmishers | pentoshi | 26.0 | main_or_minor_line |
| 161 | Lannister House Guard | lannister_houseguard | 42.2 | 42.5 | 179.0 | 57.9 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 162 | Casterly Rock Pikeman | casterly_marshal | 42.2 | 43.5 | 197.0 | 59.6 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 163 | Black Goat Devout | qohorik_goat_devout | 42.2 | 40.7 | 183.0 | 53.3 | True | False | Skirmishers | qohorik | 26.0 | main_or_minor_line |
| 164 | Westerling House Guard | westerling_houseguard | 42.1 | 42.4 | 194.0 | 57.3 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 165 | Tarth Rider | tarth_rider | 42.1 | 34.0 | 106.0 | 31.1 | True | True | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 166 | White Harbor Squire | whiteharbor_squire | 42.1 | 34.0 | 106.0 | 28.3 | True | True | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 167 | Celtigar Halberdier | celtigar_halberdier | 42.1 | 42.3 | 192.0 | 58.6 | True | False | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 168 | Ghiscari Cavalry | ghiscari_cavalry | 42.0 | 33.9 | 124.0 | 33.9 | True | True | Defensive Troops | ghiscari | 21.0 | main_or_minor_line |
| 169 | Qohorik Elite Spearman | qohorik_elite_spearman | 42.0 | 42.1 | 180.0 | 55.8 | True | False | Defensive Troops | qohorik | 26.0 | main_or_minor_line |
| 170 | Valyrian Elite Pikeman | targaryen_elite_pikeman | 42.0 | 43.2 | 184.0 | 60.0 | True | False | Defensive Troops | valyrian | 26.0 | main_or_minor_line |
| 171 | Stormlands Thunder Knight | stormlands_thunderknight | 41.9 | 47.4 | 158.0 | 46.5 | False | True | Defensive Troops | stormlands | 31.0 | main_or_minor_line |
| 172 | Stormlands Fell Knight | stormlands_fell_knight | 41.8 | 47.3 | 158.0 | 46.5 | False | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 173 | Martell House Guard | martell_houseguard | 41.8 | 40.3 | 170.0 | 53.6 | True | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 174 | Clegane Scout | clegane_scout | 41.3 | 33.0 | 113.0 | 34.4 | True | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 175 | Qohorik Swordsman | qohorik_swordsman | 41.3 | 41.4 | 176.0 | 55.5 | True | False | Defensive Troops | qohorik | 21.0 | main_or_minor_line |
| 176 | Umber Scout | umber_scout | 41.1 | 32.9 | 115.0 | 34.7 | True | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 177 | Dondarrion House Guard | dondarion_houseguard | 41.1 | 41.2 | 184.0 | 56.2 | True | False | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 178 | Martell Spearman | martell_spearman | 41.0 | 39.4 | 164.0 | 52.0 | True | False | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 179 | Glover Bushranger | glover_bushranger | 40.9 | 39.2 | 165.0 | 52.8 | True | False | Skirmishers | battania | 31.0 | main_or_minor_line |
| 180 | Glover Warrior | glover_warrior | 40.9 | 39.2 | 165.0 | 52.8 | True | False | Skirmishers | battania | 26.0 | main_or_minor_line |
| 181 | Ibbenese Mariner | ibbenese_mariner | 40.9 | 40.9 | 183.0 | 54.2 | True | False | Defensive Troops | ibbenese | 26.0 | main_or_minor_line |
| 182 | Vale House Guard | vale_houseguard | 40.6 | 40.6 | 178.0 | 57.4 | True | False | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 183 | Frey Rider | frey_rider | 40.6 | 32.2 | 129.0 | 35.4 | True | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 184 | Reach Champion | reach_champion | 40.4 | 40.3 | 188.0 | 58.0 | True | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 185 | Freefolk Thenn Impaler | freefolk_thenn_impaler | 40.3 | 41.2 | 183.0 | 55.3 | True | False | Defensive Troops | freefolk | 31.0 | main_or_minor_line |
| 186 | Ghiscari Horseman | ghiscari_horseman | 40.1 | 32.7 | 103.0 | 31.8 | True | True | Defensive Troops | ghiscari | 16.0 | main_or_minor_line |
| 187 | Pentoshi Pike Warrior | pentoshi_pike_warrior | 39.9 | 40.8 | 175.0 | 55.0 | True | False | Defensive Troops | pentoshi | 21.0 | main_or_minor_line |
| 188 | Harlaw Chief Mate | harlaw_chief_mate | 39.8 | 39.6 | 178.0 | 55.5 | True | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 189 | Dragonstone Elite Halberdier | dragonstone_headsman | 39.8 | 39.6 | 170.0 | 53.9 | True | False | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 190 | Dragonstone House Guard | dragonstone_houseguard | 39.8 | 39.6 | 170.0 | 53.9 | True | False | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 191 | White Harbor Pike Knight | whiteharbor_elite_pikeman | 39.7 | 40.6 | 184.0 | 53.6 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 192 | Lannister Man at Arms | lannister_man_at_arms | 39.7 | 39.5 | 171.0 | 52.7 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 193 | Qartheen Pureborn Champion | qartheen_champion | 39.5 | 40.3 | 187.0 | 54.1 | True | False | Ranged Troops | qartheen | 26.0 | main_or_minor_line |
| 194 | Qartheen Enthroned Guardian | enthroned_guardian | 39.5 | 40.3 | 187.0 | 54.1 | True | False | Ranged Troops | qartheen | 31.0 | main_or_minor_line |
| 195 | Vale Rider | vale_rider | 39.5 | 32.0 | 91.0 | 27.5 | True | True | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 196 | Freefolk Thenn Cannibal | freefolk_thenn_cannibal | 39.5 | 40.3 | 177.0 | 53.6 | True | False | Defensive Troops | freefolk | 26.0 | main_or_minor_line |
| 197 | Harlaw Captain | harlaw_captain | 39.4 | 40.6 | 188.0 | 57.4 | True | False | Defensive Troops | sturgia | 31.0 | main_or_minor_line |
| 198 | Velaryon Renegade | velaryon_renegade | 39.4 | 39.2 | 168.0 | 53.2 | True | False | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 199 | Tyrell Scout | tyrell_scout | 39.4 | 30.8 | 105.0 | 28.2 | True | True | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 200 | Guardian of Oldtown | oldtown_guardian | 39.3 | 39.1 | 195.0 | 59.3 | True | False | Defensive Troops | reach | 31.0 | main_or_minor_line |
| 201 | Hightower Captain | hightower_guardian | 39.3 | 39.1 | 195.0 | 59.3 | True | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 202 | Myrish Artisan of War | myrish_artisan | 39.3 | 40.1 | 200.0 | 58.8 | True | False | Ranged Troops | myrish | 31.0 | main_or_minor_line |
| 203 | Royce Elite Warrior | royce_elite_warrior | 38.9 | 38.6 | 163.0 | 48.0 | True | False | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 204 | Ibbenese Whaler | ibbenese_whaler | 38.8 | 38.5 | 179.0 | 51.6 | True | False | Defensive Troops | ibbenese | 26.0 | main_or_minor_line |
| 205 | Arryn Rider | arryn_rider | 38.7 | 30.0 | 105.0 | 28.2 | True | True | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 206 | Mormont House Guard | mormont_houseguard | 38.6 | 38.3 | 171.0 | 54.2 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 207 | Skagosi Master Spearman | skag_master_spearman | 38.6 | 38.3 | 168.0 | 49.2 | True | False | Defensive Troops | skagosi | 26.0 | main_or_minor_line |
| 208 | Westerling Man at Arms | westerling_man_at_arms | 38.4 | 38.0 | 175.0 | 49.6 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 209 | Grafton Man at Arms | grafton_man_at_arms | 38.3 | 37.9 | 162.0 | 49.5 | True | False | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 210 | Myrish Legionnaire | myrish_axeman | 38.1 | 37.6 | 173.0 | 54.4 | True | False | Defensive Troops | myrish | 26.0 | main_or_minor_line |
| 211 | Tyrell Man at Arms | tyrell_man_at_arms | 38.1 | 37.6 | 169.0 | 54.9 | True | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 212 | Tyrell House Guard | tyrell_houseguard | 38.1 | 37.6 | 169.0 | 54.9 | True | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 213 | Mallister Man at Arms | mallister_man_at_arms | 38.0 | 37.6 | 167.0 | 48.5 | True | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 214 | Tyroshi Corsair | tyroshi_corsair | 38.0 | 37.3 | 179.0 | 55.5 | True | False | Skirmishers | tyroshi | 31.0 | main_or_minor_line |
| 215 | Tyroshi Firstmate | tyroshi_firstmate | 38.0 | 37.3 | 179.0 | 55.5 | True | False | Skirmishers | tyroshi | 26.0 | main_or_minor_line |
| 216 | Arryn House Guard | arryn_houseguard | 37.7 | 37.2 | 175.0 | 55.5 | True | False | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 217 | Summer Isles Spearmaster | summer_pikeman | 37.6 | 35.4 | 158.0 | 49.2 | True | False | Skirmishers | summer | 26.0 | main_or_minor_line |
| 218 | Bracken Pikemaster | bracken_master_pikeman | 37.6 | 38.0 | 177.0 | 56.3 | True | False | Defensive Troops | river | 31.0 | main_or_minor_line |
| 219 | City Watch Veteran Spearman | crownlands_militia_veteran_spearman | 37.5 | 29.9 | 141.0 | 38.7 | True | False | Defensive Troops | crownlands | 21.0 | special_or_unlinked |
| 220 | Unsullied | unsullied | 37.3 | 35.0 | 162.0 | 48.7 | True | False | Skirmishers | ghiscari | 31.0 | special_or_unlinked |
| 221 | Qartheen Elite Hoplite | qartheen_elite_hoplite | 37.3 | 36.6 | 166.0 | 47.8 | True | False | Defensive Troops | qartheen | 26.0 | main_or_minor_line |
| 222 | Tarly House Guard | tarly_houseguard | 37.2 | 36.6 | 174.0 | 56.6 | True | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 223 | Velaryon Sea Guard | velaryon_sea_guard | 37.2 | 37.6 | 168.0 | 53.2 | True | False | Defensive Troops | dragonstone | 31.0 | main_or_minor_line |
| 224 | Baratheon Hammerknight | baratheon_pikeknight | 37.1 | 36.4 | 174.0 | 54.2 | True | False | Defensive Troops | stormlands | 31.0 | main_or_minor_line |
| 225 | Baratheon House Guard | baratheon_houseguard | 37.1 | 36.4 | 174.0 | 54.2 | True | False | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 226 | Yronwood Veteran Pikeman | yronwood_veteran_pikeman | 37.0 | 37.4 | 168.0 | 51.8 | True | False | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 227 | Yronwood Pikeman | yronwood_pikeman | 37.0 | 37.4 | 168.0 | 51.8 | True | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 228 | Tyroshi Quartermaster | tyroshi_quartermaster | 36.9 | 36.0 | 156.0 | 53.2 | True | False | Skirmishers | tyroshi | 21.0 | main_or_minor_line |
| 229 | Dragonstone Man at Arms | dragonstone_man_at_arms | 36.9 | 36.2 | 156.0 | 48.0 | True | False | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 230 | Dragonstone Halberdier | dragonstone_brute | 36.9 | 36.2 | 156.0 | 48.0 | True | False | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 231 | Tarth Master Halberdier | tarth_master_halberdier | 36.8 | 36.2 | 164.0 | 47.4 | True | False | Defensive Troops | stormlands | 31.0 | main_or_minor_line |
| 232 | Tarth Halberdier | tarth_halberdier | 36.8 | 36.2 | 164.0 | 47.4 | True | False | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 233 | Stark Soldier | stark_soldier | 36.7 | 35.9 | 146.5 | 45.2 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 234 | Stormlands House Guard | stormlands_houseguard | 36.4 | 35.7 | 158.0 | 46.5 | True | False | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 235 | City Watch Spearman | crownlands_militia_spearman | 36.4 | 28.6 | 119.0 | 36.5 | True | False | Defensive Troops | crownlands | 11.0 | special_or_unlinked |
| 236 | Mormont Mounted Huntress | mormont_mounted_huntress | 36.3 | 45.4 | 148.0 | 43.0 | False | True | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 237 | Realm Hedge Knight | realm_hedge_knight | 36.3 | 35.5 | 165.0 | 46.3 | True | False | Defensive Troops | crownlands | 21.0 | main_or_minor_line |
| 238 | Black Goat Warrior | qohorik_goat_warrior | 36.2 | 33.7 | 149.0 | 41.1 | True | False | Skirmishers | qohorik | 21.0 | main_or_minor_line |
| 239 | Stormlands Elite Maceman | stormlands_crusher | 36.2 | 35.7 | 158.0 | 46.5 | True | False | Skirmishers | stormlands | 26.0 | main_or_minor_line |
| 240 | Umber House Guard | umber_houseguard | 36.1 | 35.3 | 160.0 | 49.2 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 241 | Stormlands Spearman | stormlands_spearman | 36.1 | 35.3 | 151.0 | 45.9 | True | False | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 242 | Greyjoy Finger Dancer | greyjoy_fingerdancer | 36.1 | 36.3 | 164.0 | 50.8 | True | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 243 | Ibbenese Sailor | ibbenese_sailor | 35.9 | 33.4 | 150.0 | 41.2 | True | False | Skirmishers | ibbenese | 21.0 | main_or_minor_line |
| 244 | Qartheen Hoplite | qartheen_hoplite | 35.9 | 35.0 | 154.0 | 44.9 | True | False | Defensive Troops | qartheen | 21.0 | main_or_minor_line |
| 245 | Stormlands Maceman | stormlands_basher | 35.8 | 35.3 | 151.0 | 45.9 | True | False | Skirmishers | stormlands | 21.0 | main_or_minor_line |
| 246 | Skagosi Spearman | skag_spearman | 35.8 | 34.9 | 151.0 | 44.7 | True | False | Defensive Troops | skagosi | 21.0 | main_or_minor_line |
| 247 | Riverlands Swordmaster | river_swordmaster | 35.7 | 31.9 | 162.0 | 46.2 | True | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 248 | Riverlands Admiral | river_admiral | 35.7 | 31.9 | 162.0 | 46.2 | True | False | Defensive Troops | river | 31.0 | main_or_minor_line |
| 249 | Riverlands Elite Swordsman | river_elite_swordsman | 35.7 | 31.9 | 162.0 | 46.2 | True | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 250 | Bracken House Guard | bracken_houseguard | 35.7 | 34.9 | 156.0 | 45.7 | True | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 251 | Volantine Elite Warrior | tigercloak_elite_warrior | 35.7 | 34.9 | 168.0 | 51.7 | True | False | Defensive Troops | volantine | 26.0 | main_or_minor_line |
| 252 | Free Folk Frosthedge | freefolk_frosthedge | 35.7 | 36.3 | 161.0 | 45.8 | True | False | Defensive Troops | freefolk | 26.0 | main_or_minor_line |
| 253 | Tarth Soldier | tarth_soldier | 35.7 | 34.8 | 141.0 | 45.1 | True | False | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 254 | Dreadfort Blackguard | dreadfort_blackguard | 35.7 | 34.8 | 158.0 | 50.9 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 255 | Clegane House Guard | clegane_houseguard | 35.5 | 34.6 | 161.0 | 48.0 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 256 | Qohorik Spearman | qohorik_spearman | 35.4 | 34.5 | 149.0 | 43.5 | True | False | Defensive Troops | qohorik | 21.0 | main_or_minor_line |
| 257 | Celtigar Man at Arms | celtigar_man_at_arms | 35.4 | 34.4 | 153.0 | 45.0 | True | False | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 258 | Dreadfort PIkeman | dreadfort_pikeman | 35.3 | 36.4 | 158.0 | 50.9 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 259 | Reach Hedge Knight | reach_hedge_knight | 35.3 | 34.4 | 167.0 | 47.6 | True | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 260 | Blackwood House Guard | blackwood_houseguard | 35.2 | 34.3 | 155.0 | 44.1 | True | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 261 | Tully House Guard | tully_houseguard | 35.2 | 34.3 | 157.0 | 46.3 | True | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 262 | Riverlands House Guard | river_houseguard | 35.2 | 34.3 | 162.0 | 46.2 | True | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 263 | Sarnori Spider | sarnor_spider | 35.2 | 40.9 | 155.0 | 47.7 | False | True | Skirmishers | sarnor | 31.0 | main_or_minor_line |
| 264 | Qartheen Pureborn Warrior | qartheen_pureborn_warrior | 35.1 | 32.5 | 144.0 | 40.5 | True | False | Skirmishers | qartheen | 21.0 | main_or_minor_line |
| 265 | Ghiscari Lockstep Legionnaire | ghiscari_unsullied_unbroken | 35.1 | 29.4 | 144.0 | 43.5 | True | False | Skirmishers | ghiscari | 31.0 | main_or_minor_line |
| 266 | Ghiscari Elite Legionnaire | ghiscari_unsullied_unbent | 35.1 | 29.4 | 144.0 | 43.5 | True | False | Skirmishers | ghiscari | 26.0 | main_or_minor_line |
| 267 | Yi Ti Spearman | yiti_spearman | 35.1 | 34.1 | 137.0 | 43.3 | True | False | Defensive Troops | yiti | 21.0 | main_or_minor_line |
| 268 | Pentoshi Man at Arms | pentoshi_man_at_arms | 35.0 | 34.0 | 143.0 | 43.2 | True | False | Defensive Troops | pentoshi | 21.0 | main_or_minor_line |
| 269 | Valyrian Man at Arms | targaryen_man_at_arms | 35.0 | 35.0 | 156.0 | 45.8 | True | False | Defensive Troops | valyrian | 21.0 | main_or_minor_line |
| 270 | Norvoshi Devout Bearded Priest | devout_bearded_priest | 34.9 | 33.9 | 178.0 | 52.5 | True | False | Defensive Troops | norvos | 26.0 | main_or_minor_line |
| 271 | Skagosi Savage | skag_savage | 34.9 | 34.9 | 151.0 | 44.7 | True | False | Defensive Troops | skagosi | 21.0 | main_or_minor_line |
| 272 | Manderly Man at Arms | manderly_man_at_arms | 34.9 | 33.9 | 157.0 | 42.9 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 273 | Kingsguard Initiate | kingsguard_initiate | 34.9 | 33.9 | 157.0 | 49.7 | True | False | Defensive Troops | crownlands | 21.0 | main_or_minor_line |
| 274 | Guard of the Crossing | guard_of_the_crossing | 34.8 | 33.8 | 141.0 | 43.2 | True | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 275 | Freefolk Thenn Warrior | freefolk_thenn_warrior | 34.7 | 34.7 | 140.0 | 43.9 | True | False | Defensive Troops | freefolk | 21.0 | main_or_minor_line |
| 276 | Velaryon Marine | velaryon_warrior | 34.6 | 33.6 | 147.0 | 43.4 | True | False | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 277 | Bracken Man at Arms | bracken_man_at_arms | 34.6 | 33.6 | 133.0 | 43.4 | True | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 278 | Dayne Man at Arms | dayne_pikeman | 34.6 | 33.5 | 160.0 | 48.5 | True | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 279 | Pentoshi Militia Veteran Spearman | pentoshi_militia_veteran_spearman | 34.6 | 33.5 | 143.0 | 41.4 | True | False | Defensive Troops | pentoshi | 16.0 | special_or_unlinked |
| 280 | Umber Axeman | umber_axeman | 34.6 | 35.0 | 157.0 | 48.6 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 281 | Dayne Pikeman | dayne_veteran_pikeman | 34.5 | 35.4 | 173.0 | 51.8 | True | False | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 282 | Sarnori Master Spearman | sarnor_master_spearman | 34.5 | 31.7 | 149.0 | 46.5 | True | False | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 283 | Valyrian Soldier | targaryen_soldier | 34.4 | 33.3 | 127.0 | 42.9 | True | False | Defensive Troops | valyrian | 16.0 | main_or_minor_line |
| 284 | Glover Man at Arms | glover_man_at_arms | 34.3 | 33.2 | 142.0 | 42.2 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 285 | Qohorik Militia Veteran Spearman | qohorik_militia_veteran_spearman | 34.2 | 33.1 | 142.0 | 41.6 | True | False | Defensive Troops | qohorik | 16.0 | special_or_unlinked |
| 286 | Tully Man at Arms | tully_man_at_arms | 34.2 | 33.1 | 136.0 | 44.2 | True | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 287 | Blackwood Man at Arms | blackwood_man_at_arms | 34.1 | 33.0 | 132.0 | 41.9 | True | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 288 | Royce Warrior | royce_warrior | 34.1 | 32.9 | 141.0 | 38.0 | True | False | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 289 | Valyrian Militia Veteran Spearman | valyrian_militia_veteran_spearman | 33.8 | 32.6 | 134.0 | 40.8 | True | False | Defensive Troops | valyrian | 16.0 | special_or_unlinked |
| 290 | Golden Company Aurum Spearbearers | golden_spearman | 33.8 | 32.6 | 139.0 | 46.3 | True | False | Defensive Troops | volantine | 21.0 | main_or_minor_line |
| 291 | Vale Man at Arms | vale_man_at_arms | 33.7 | 32.5 | 130.0 | 43.2 | True | False | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 292 | Myrish Militia Veteran Spearman | myrish_militia_veteran_spearman | 33.7 | 32.5 | 127.0 | 40.5 | True | False | Defensive Troops | myrish | 16.0 | special_or_unlinked |
| 293 | Ibbenese Warrior | ibbenese_warrior | 33.6 | 32.4 | 147.0 | 41.0 | True | False | Defensive Troops | ibbenese | 21.0 | main_or_minor_line |
| 294 | Lyseni Glaiveman | lyseni_glaiveman | 33.6 | 32.4 | 159.0 | 46.7 | True | False | Defensive Troops | lyseni | 26.0 | main_or_minor_line |
| 295 | Lyseni Spearman | lyseni_spearman | 33.6 | 32.4 | 159.0 | 46.7 | True | False | Defensive Troops | lyseni | 26.0 | main_or_minor_line |
| 296 | Riverlands Man at Arms | river_man_at_arms | 33.6 | 32.4 | 135.0 | 43.0 | True | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 297 | Myrish Master Crossbowman | myrish_master_crossbowman | 33.6 | 33.4 | 171.0 | 47.0 | True | False | Ranged Troops | myrish | 26.0 | main_or_minor_line |
| 298 | Golden Company Gilt Pike Wardens | golden_pikeman | 33.6 | 33.4 | 146.0 | 47.7 | True | False | Defensive Troops | volantine | 26.0 | main_or_minor_line |
| 299 | Karstark House Guard | karstark_brute | 33.5 | 32.3 | 153.0 | 46.3 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 300 | Karstark Loyalist | karstark_loyalist | 33.5 | 32.3 | 153.0 | 46.3 | True | False | Defensive Troops | battania | 31.0 | main_or_minor_line |
| 301 | Cerwyn Veteran Axeman | cerwyn_master_axeman | 33.5 | 32.2 | 147.0 | 43.4 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 302 | Pentoshi Soldier | pentoshi_soldier | 33.2 | 32.9 | 123.0 | 41.2 | True | False | Defensive Troops | pentoshi | 16.0 | main_or_minor_line |
| 303 | Gold Cloak Halberdier | kingsguard | 33.2 | 31.8 | 154.0 | 46.2 | True | False | Defensive Troops | crownlands | 26.0 | main_or_minor_line |
| 304 | Night's Watch Stalwart | nightswatch_stalwart | 33.1 | 31.8 | 153.0 | 49.5 | True | False | Defensive Troops | nightswatch | 26.0 | main_or_minor_line |
| 305 | Norvoshi Militia Veteran Spearman | norvos_militia_veteran_spearman | 33.0 | 31.7 | 130.0 | 39.2 | True | False | Defensive Troops | norvos | 16.0 | special_or_unlinked |
| 306 | Reach House Guard | reach_houseguard | 33.0 | 31.6 | 156.0 | 45.8 | True | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 307 | Myrish Warrior | myrish_warrior | 32.9 | 31.5 | 150.0 | 43.9 | True | False | Defensive Troops | myrish | 21.0 | main_or_minor_line |
| 308 | Volantene Militia Veteran Spearman | volantine_militia_veteran_spearman | 32.9 | 31.5 | 138.0 | 38.9 | True | False | Defensive Troops | volantine | 16.0 | special_or_unlinked |
| 309 | Mormont Man at Arms | mormont_man_at_arms | 32.5 | 31.1 | 128.0 | 41.7 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 310 | Lyseni Warrior | lyseni_warrior | 32.4 | 31.0 | 136.0 | 44.2 | True | False | Defensive Troops | lyseni | 21.0 | main_or_minor_line |
| 311 | Riverlands Pikeman | river_pikeman | 32.3 | 31.9 | 162.0 | 46.2 | True | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 312 | Ghiscari Militia Veteran Spearman | ghiscari_militia_veteran_spearman | 32.3 | 30.8 | 116.0 | 37.5 | True | False | Defensive Troops | ghiscari | 16.0 | special_or_unlinked |
| 313 | Hightower Guard | hightower_guard | 32.2 | 30.7 | 152.0 | 44.7 | True | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 314 | Greyjoy Deckman | greyjoy_houseguard | 32.1 | 30.7 | 143.0 | 41.0 | True | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 315 | Yronwood Man at Arms | yronwood_man_at_arms | 32.1 | 28.9 | 139.0 | 41.7 | True | False | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 316 | YiTish Militia Veteran Spearman | yiti_militia_veteran_spearman | 31.7 | 30.1 | 142.0 | 40.0 | True | False | Defensive Troops | yiti | 16.0 | special_or_unlinked |
| 317 | Lannister Footman | lannister_footman | 31.7 | 30.1 | 108.0 | 36.3 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 318 | Dondarrion Man at Arms | dondarion_man_at_arms | 31.6 | 30.1 | 138.0 | 36.8 | True | False | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 319 | Vale Soldier | vale_soldier | 31.6 | 30.0 | 107.0 | 39.0 | True | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 320 | Bolton Veteran | bolton_veteran | 31.5 | 30.0 | 145.0 | 42.5 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 321 | Lyseni Axeman | lyseni_axeman | 31.5 | 31.4 | 151.0 | 44.9 | True | False | Defensive Troops | lyseni | 21.0 | main_or_minor_line |
| 322 | Casterly Rock Soldier | casterly_soldier | 31.4 | 29.8 | 106.0 | 35.9 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 323 | Stormlands Knight | stormlands_knight | 31.4 | 35.1 | 151.0 | 45.9 | False | True | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 324 | Qartheen Soldier | qartheen_warrior | 31.3 | 29.7 | 122.0 | 35.7 | True | False | Defensive Troops | qartheen | 16.0 | main_or_minor_line |
| 325 | Ibbenese Tracker | ibbenese_tracker | 31.3 | 29.7 | 134.0 | 36.2 | True | False | Defensive Troops | ibbenese | 16.0 | main_or_minor_line |
| 326 | Ibbenese Rower | ibbenese_rower | 31.3 | 29.7 | 134.0 | 36.2 | True | False | Defensive Troops | ibbenese | 16.0 | main_or_minor_line |
| 327 | Hightower Soldier | hightower_soldier | 31.1 | 29.5 | 130.0 | 42.5 | True | False | Defensive Troops | reach | 16.0 | main_or_minor_line |
| 328 | Ghiscari Soldier | ghiscari_soldier | 31.0 | 28.6 | 144.0 | 43.5 | True | False | Skirmishers | ghiscari | 21.0 | main_or_minor_line |
| 329 | Summer Isles Militia Veteran Spearman | summer_militia_veteran_spearman | 30.8 | 29.2 | 126.0 | 38.3 | True | False | Defensive Troops | summer | 16.0 | special_or_unlinked |
| 330 | Dragonstone Soldier | dragonstone_soldier | 30.8 | 29.1 | 111.0 | 35.7 | True | False | Defensive Troops | dragonstone | 16.0 | main_or_minor_line |
| 331 | Skagosi Soldier | skag_soldier | 30.8 | 29.1 | 116.0 | 34.6 | True | False | Defensive Troops | skagosi | 16.0 | main_or_minor_line |
| 332 | Arryn Man at Arms | arryn_man_at_arms | 30.7 | 28.9 | 125.0 | 41.1 | True | False | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 333 | Qartheen Pureborn Fighter | qartheen_pureborn | 30.6 | 28.9 | 107.0 | 34.2 | True | False | Defensive Troops | qartheen | 16.0 | main_or_minor_line |
| 334 | Celtigar Footman | celtigar_footman | 30.5 | 28.8 | 131.0 | 35.1 | True | False | Defensive Troops | dragonstone | 16.0 | main_or_minor_line |
| 335 | Mormont Scout | mormont_scout | 30.5 | 37.1 | 149.0 | 43.8 | False | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 336 | Lyseni Militia Veteran Spearman | lyseni_militia_veteran_spearman | 30.5 | 28.7 | 133.0 | 40.5 | True | False | Defensive Troops | lyseni | 16.0 | special_or_unlinked |
| 337 | Free Folk Shieldman | freefolk_shieldman | 30.4 | 30.1 | 133.0 | 35.0 | True | False | Defensive Troops | freefolk | 21.0 | main_or_minor_line |
| 338 | Ghiscari Legionnaire | ghiscari_unsullied_hoplite | 30.3 | 23.8 | 124.0 | 33.9 | True | False | Skirmishers | ghiscari | 21.0 | main_or_minor_line |
| 339 | Tarly Man at Arms | tarly_man_at_arms | 30.3 | 28.5 | 126.0 | 42.5 | True | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 340 | Cerwyn Axeman | cerwyn_axeman | 30.3 | 28.5 | 137.0 | 36.9 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 341 | Norvoshi Master Axeman | norvos_master_axeman | 30.2 | 29.8 | 154.0 | 45.5 | True | False | Defensive Troops | norvos | 26.0 | main_or_minor_line |
| 342 | Norvoshi Pikeman | norvos_pikeman | 30.2 | 29.8 | 154.0 | 45.5 | True | False | Defensive Troops | norvos | 26.0 | main_or_minor_line |
| 343 | Umber Man at Arms | umber_man_at_arms | 30.1 | 28.2 | 138.0 | 37.0 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 344 | Norvoshi Bearded Priest | norvos_bearded_priest | 30.1 | 28.2 | 156.0 | 42.6 | True | False | Defensive Troops | norvos | 21.0 | main_or_minor_line |
| 345 | Clegane Man at Arms | clegane_man_at_arms | 29.9 | 28.0 | 135.0 | 36.6 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 346 | Free Folk Spearman | freefolk_spearman | 29.6 | 26.0 | 133.0 | 35.0 | True | False | Skirmishers | freefolk | 21.0 | main_or_minor_line |
| 347 | Volantene Warrior | tigercloak_warrior | 29.6 | 27.7 | 134.0 | 39.2 | True | False | Defensive Troops | volantine | 21.0 | main_or_minor_line |
| 348 | Tyroshi Militia Veteran Spearman | tyroshi_militia_veteran_spearman | 29.5 | 27.6 | 127.0 | 38.5 | True | False | Defensive Troops | tyroshi | 16.0 | special_or_unlinked |
| 349 | Vicious Wight | vicious_wight | 29.3 | 27.4 | 123.0 | 30.2 | True | False | Defensive Troops | whitewalker | 26.0 | main_or_minor_line |
| 350 | Sarnori Master Javelinier | sarnor_master_javelinier | 29.3 | 33.9 | 155.0 | 47.7 | False | True | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 351 | Cerwyn Soldier | cerwyn_soldier | 29.2 | 27.3 | 116.0 | 34.8 | True | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 352 | Tully Soldier | tully_soldier | 29.2 | 27.3 | 119.0 | 34.1 | True | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 353 | Pentoshi Mounted Archer | pentoshi_mounted_archer | 29.2 | 36.6 | 143.0 | 43.2 | False | True | Ranged Troops | pentoshi | 26.0 | main_or_minor_line |
| 354 | Ghiscari Elite Pikeman | ghiscari_elite_unsullied | 29.1 | 28.2 | 140.0 | 39.1 | True | False | Defensive Troops | ghiscari | 26.0 | main_or_minor_line |
| 355 | Ghiscari Pikeman | ghiscari_unsullied | 29.1 | 28.2 | 140.0 | 39.1 | True | False | Defensive Troops | ghiscari | 21.0 | main_or_minor_line |
| 356 | Riverlands Soldier | river_soldier | 29.0 | 27.0 | 117.0 | 33.7 | True | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 357 | Bracken Footman | bracken_footman | 29.0 | 27.0 | 118.0 | 33.7 | True | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 358 | Dragonstone Militia Veteran Spearman | dragonstone_militia_veteran_spearman | 28.9 | 26.9 | 132.0 | 39.1 | True | False | Defensive Troops | dragonstone | 16.0 | special_or_unlinked |
| 359 | Stormlands Militia Veteran Spearman | stormlands_militia_veteran_spearman | 28.8 | 26.8 | 131.0 | 38.9 | True | False | Defensive Troops | stormlands | 16.0 | special_or_unlinked |
| 360 | Vale Militia Veteran Spearman | vale_militia_veteran_spearman | 28.8 | 26.8 | 131.0 | 38.9 | True | False | Defensive Troops | vale | 16.0 | special_or_unlinked |
| 361 | Reach Militia Veteran Spearman | reach_militia_veteran_spearman | 28.8 | 26.8 | 131.0 | 38.9 | True | False | Defensive Troops | reach | 16.0 | special_or_unlinked |
| 362 | Westerling Footman | westerling_footman | 28.8 | 26.7 | 113.0 | 33.1 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 363 | Gold Cloak Petty Officer | goldcloak_officer | 28.8 | 27.7 | 143.0 | 39.0 | True | False | Defensive Troops | crownlands | 21.0 | main_or_minor_line |
| 364 | Qohorik Soldier | qohorik_soldier | 28.7 | 26.7 | 123.0 | 29.9 | True | False | Defensive Troops | qohorik | 16.0 | main_or_minor_line |
| 365 | Riverlands Militia Veteran Spearman | river_militia_veteran_spearman | 28.7 | 26.7 | 130.0 | 38.7 | True | False | Defensive Troops | river | 16.0 | special_or_unlinked |
| 366 | Grafton Footman | grafton_footman | 28.7 | 26.7 | 112.0 | 33.1 | True | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 367 | Freefolk Thenn | freefolk_thenn | 28.6 | 27.5 | 105.0 | 31.4 | True | False | Defensive Troops | freefolk | 16.0 | main_or_minor_line |
| 368 | Sarnori Spearman | sarnor_spearman | 28.6 | 26.5 | 129.0 | 37.3 | True | False | Defensive Troops | sarnor | 21.0 | main_or_minor_line |
| 369 | Sarnori Glaiveman | sarnor_glaiveman | 28.6 | 26.5 | 129.0 | 37.3 | True | False | Defensive Troops | sarnor | 21.0 | main_or_minor_line |
| 370 | Volantene Soldier | volantine_soldier | 28.5 | 26.4 | 108.0 | 37.0 | True | False | Defensive Troops | volantine | 16.0 | main_or_minor_line |
| 371 | Stark Footman | stark_footman | 28.5 | 26.4 | 105.0 | 28.5 | True | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 372 | Frey Man at Arms | frey_man_at_arms | 28.4 | 27.3 | 123.0 | 34.2 | True | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 373 | Reach Man at Arms | reach_hacker | 28.2 | 26.1 | 136.0 | 36.1 | True | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 374 | Blackwood Footman | blackwood_footman | 28.1 | 26.0 | 111.0 | 31.9 | True | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 375 | Sarnori Militia Veteran Spearman | sarnor_militia_veteran_spearman | 28.0 | 25.8 | 125.0 | 36.1 | True | False | Defensive Troops | sarnor | 16.0 | special_or_unlinked |
| 376 | Karstark Spearman | karstark_ruffian | 27.9 | 25.7 | 136.0 | 38.8 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 377 | Grafton Levy | grafton_levy | 27.7 | 26.5 | 104.0 | 32.7 | True | False | Defensive Troops | vale | 11.0 | main_or_minor_line |
| 378 | Westerling Levy | westerling_levy | 27.7 | 26.5 | 104.0 | 32.7 | True | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 379 | Gold Cloak Soldier | goldcloak_soldier | 27.4 | 25.1 | 119.0 | 36.5 | True | False | Defensive Troops | crownlands | 16.0 | main_or_minor_line |
| 380 | Valyrian Squire | valyrian_squire | 27.3 | 25.0 | 104.0 | 28.0 | True | False | Defensive Troops | valyrian | 16.0 | main_or_minor_line |
| 381 | Tyroshi Soldier | tyroshi_soldier | 27.3 | 25.0 | 104.0 | 34.1 | True | False | Defensive Troops | tyroshi | 16.0 | main_or_minor_line |
| 382 | Velaryon Sailor | velaryon_soldier | 27.2 | 24.9 | 105.0 | 28.4 | True | False | Defensive Troops | dragonstone | 16.0 | main_or_minor_line |
| 383 | Frey Cutthroat | frey_cutthroat | 27.2 | 25.9 | 100.0 | 31.7 | True | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 384 | Summer Isles Spearman | summer_spearman | 27.2 | 24.8 | 112.0 | 36.5 | True | False | Defensive Troops | summer | 21.0 | main_or_minor_line |
| 385 | Lannister Levy | lannister_levy | 27.1 | 24.7 | 100.0 | 35.3 | True | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 386 | Martell Footman | martell_footman | 27.1 | 24.1 | 103.0 | 33.2 | True | False | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 387 | Norvoshi Spearman | norvos_spearman | 26.9 | 24.5 | 133.0 | 36.2 | True | False | Defensive Troops | norvos | 21.0 | main_or_minor_line |
| 388 | Yi Ti Infantryman | yiti_infantryman | 26.8 | 25.5 | 107.0 | 28.3 | True | False | Defensive Troops | yiti | 16.0 | main_or_minor_line |
| 389 | Manderly Footman | whiteharbor_footman | 26.8 | 25.5 | 106.0 | 28.3 | True | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 390 | Mallister Footman | mallister_footman | 26.4 | 23.9 | 106.0 | 28.3 | True | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 391 | Beastbound Wight | beastbound_wight | 26.4 | 30.6 | 93.0 | 25.0 | False | True | Skirmishers | whitewalker | 26.0 | main_or_minor_line |
| 392 | Royce Soldier | royce_soldier | 26.3 | 23.8 | 105.0 | 28.0 | True | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 393 | Norvoshi Horseman | norvos_horseman | 26.2 | 32.1 | 129.0 | 35.4 | False | True | Defensive Troops | norvos | 16.0 | main_or_minor_line |
| 394 | Golden Company Giltblade Warriors | golden_infantryman | 26.0 | 23.5 | 106.0 | 30.5 | True | False | Defensive Troops | volantine | 16.0 | main_or_minor_line |
| 395 | Summer Isles Scout | summer_rider | 25.9 | 31.6 | 136.0 | 42.5 | False | True | Defensive Troops | summer | 21.0 | main_or_minor_line |
| 396 | Clegane Footman | clegane_footman | 25.8 | 24.7 | 106.0 | 35.2 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 397 | Greyjoy Soldier | greyjoy_soldier | 25.7 | 23.2 | 105.0 | 27.9 | True | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 398 | Umber Footman | umber_footman | 25.7 | 24.6 | 99.0 | 35.1 | True | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 399 | Stormlands Man at Arms | stormlands_man_at_arms | 25.7 | 23.1 | 107.0 | 34.5 | True | False | Defensive Troops | stormlands | 16.0 | main_or_minor_line |
| 400 | Dayne Footman | dayne_man_at_arms | 25.7 | 23.1 | 107.0 | 32.5 | True | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 401 | Casterly Rock Guard | casterly_guard | 25.6 | 23.0 | 78.0 | 24.0 | True | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 402 | Bolton Footman | bolton_scout | 25.6 | 24.0 | 124.0 | 32.8 | True | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 403 | Ghiscari Legion Trainee | ghiscari_unsullied_initiate | 25.3 | 22.7 | 104.0 | 31.9 | True | False | Defensive Troops | ghiscari | 16.0 | main_or_minor_line |
| 404 | Mallister Levy | mallister_levy | 25.3 | 23.7 | 98.0 | 27.9 | True | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 405 | Norvoshi Axeman | norvos_axeman | 25.3 | 24.1 | 133.0 | 36.2 | True | False | Defensive Troops | norvos | 21.0 | main_or_minor_line |
| 406 | Karstark Brute | karstark_soldier | 25.3 | 24.6 | 115.0 | 36.9 | True | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 407 | Bracken Levy | bracken_levy | 25.3 | 23.6 | 97.0 | 27.8 | True | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 408 | Riverlands Swordsman | river_swordsman | 25.2 | 19.6 | 88.0 | 24.8 | True | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 409 | Dondarrion Footman | dondarion_footman | 25.2 | 22.6 | 111.0 | 33.4 | True | False | Defensive Troops | stormlands | 16.0 | main_or_minor_line |
| 410 | Reach Soldier | reach_soldier | 25.2 | 22.5 | 95.0 | 32.0 | True | False | Defensive Troops | reach | 16.0 | main_or_minor_line |
| 411 | Blackwood Levy | blackwood_levy | 25.2 | 23.6 | 96.0 | 27.6 | True | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 412 | Ibbenese Militia Veteran Spearman | ibbenese_militia_veteran_spearman | 25.2 | 18.5 | 69.8 | 19.9 | True | False | Defensive Troops | ibbenese | 16.0 | special_or_unlinked |
| 413 | Tully Footman | tully_footman | 25.1 | 23.4 | 95.0 | 27.4 | True | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 414 | Night's Watch Defender | nightswatch_defender | 24.8 | 22.0 | 115.0 | 32.4 | True | False | Defensive Troops | nightswatch | 21.0 | main_or_minor_line |
| 415 | Tyrell Soldier | tyrell_soldier | 24.7 | 21.9 | 91.0 | 27.5 | True | False | Defensive Troops | reach | 16.0 | main_or_minor_line |
| 416 | Night's Watch Shieldbrother | nightswatch_shieldbrother | 24.6 | 21.8 | 104.0 | 30.2 | True | False | Defensive Troops | nightswatch | 16.0 | main_or_minor_line |
| 417 | Dayne Levy | dayne_levy | 24.6 | 22.9 | 98.0 | 32.0 | True | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 418 | Squire | dragonstone_squire | 24.6 | 21.1 | 70.0 | 21.2 | True | False | Skirmishers | dragonstone | 16.0 | main_or_minor_line |
| 419 | Vale Squire | vale_squire | 24.5 | 22.8 | 66.0 | 26.4 | True | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 420 | Night's Watch Militia Veteran Spearman | nightswatch_militia_veteran_spearman | 24.3 | 20.8 | 85.0 | 28.5 | True | False | Defensive Troops | nightswatch | 16.0 | special_or_unlinked |
| 421 | Targaryen Squire | targ_squire | 24.3 | 21.4 | 88.0 | 22.1 | True | False | Defensive Troops | valyrian | 16.0 | main_or_minor_line |
| 422 | Tarth Man at Arms | tarth_man_at_arms | 24.1 | 21.2 | 106.0 | 31.1 | True | False | Defensive Troops | stormlands | 16.0 | main_or_minor_line |
| 423 | Baratheon Soldier | baratheon_soldier | 23.9 | 21.1 | 101.0 | 27.4 | True | False | Defensive Troops | stormlands | 16.0 | main_or_minor_line |
| 424 | Tyroshi Boatswain | tyroshi_boatswain | 23.9 | 20.7 | 85.0 | 26.6 | True | False | Skirmishers | tyroshi | 16.0 | main_or_minor_line |
| 425 | Tarly Soldier | tarly_soldier | 23.9 | 21.0 | 89.0 | 29.3 | True | False | Defensive Troops | reach | 16.0 | main_or_minor_line |
| 426 | Norvoshi Soldier | norvos_soldier | 23.7 | 22.2 | 107.0 | 33.0 | True | False | Defensive Troops | norvos | 16.0 | main_or_minor_line |
| 427 | Free Folk Axeman | freefolk_axeman | 23.3 | 21.8 | 111.0 | 27.6 | True | False | Defensive Troops | freefolk | 16.0 | main_or_minor_line |
| 428 | Yronwood Levy | yronwood_levy | 23.0 | 21.0 | 97.0 | 27.8 | True | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 429 | Royce Footman | royce_footman | 22.7 | 19.7 | 69.0 | 20.9 | True | False | Defensive Troops | vale | 11.0 | main_or_minor_line |
| 430 | Arryn Levy | arryn_levy | 22.7 | 19.7 | 69.0 | 20.9 | True | False | Defensive Troops | vale | 11.0 | main_or_minor_line |
| 431 | Glover Footman | glover_footman | 22.6 | 19.5 | 104.0 | 28.0 | True | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 432 | Sarnori Warrior | sarnor_warrior | 22.6 | 19.5 | 88.0 | 25.1 | True | False | Defensive Troops | sarnor | 16.0 | main_or_minor_line |
| 433 | Night's Watch Militia Spearman | nightswatch_militia_spearman | 22.4 | 19.2 | 83.0 | 28.1 | True | False | Defensive Troops | nightswatch | 11.0 | special_or_unlinked |
| 434 | Free Folk Warrior | freefolk_warrior | 22.3 | 20.6 | 91.0 | 25.6 | True | False | Defensive Troops | freefolk | 11.0 | main_or_minor_line |
| 435 | Tarth Militia | tarth_militia | 22.3 | 20.2 | 88.0 | 29.3 | True | False | Defensive Troops | stormlands | 11.0 | main_or_minor_line |
| 436 | Riverlands Footman | river_footman | 22.3 | 20.2 | 62.0 | 21.7 | True | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 437 | Qohorik Footman | qohorik_footman | 22.3 | 21.1 | 95.0 | 27.6 | True | False | Defensive Troops | qohorik | 11.0 | main_or_minor_line |
| 438 | Pentoshi Footman | pentoshi_footman | 22.2 | 20.1 | 76.0 | 18.9 | True | False | Defensive Troops | pentoshi | 11.0 | main_or_minor_line |
| 439 | Summer Isles Infantryman | summer_infantryman | 22.2 | 19.1 | 84.0 | 26.4 | True | False | Defensive Troops | summer | 16.0 | main_or_minor_line |
| 440 | Sarnori Horseman | sarnor_horseman | 22.2 | 27.3 | 108.0 | 27.1 | False | True | Defensive Troops | sarnor | 16.0 | main_or_minor_line |
| 441 | Freefolk Militia Veteran Spearman | freefolk_militia_veteran_spearman | 22.1 | 18.9 | 85.0 | 25.3 | True | False | Defensive Troops | freefolk | 16.0 | special_or_unlinked |
| 442 | Lyseni Soldier | lyseni_soldier | 22.1 | 18.9 | 85.0 | 26.6 | True | False | Defensive Troops | lyseni | 16.0 | main_or_minor_line |
| 443 | Lyseni Axe Apprentice | lyseni_axe_apprentice | 21.7 | 19.9 | 100.0 | 28.2 | True | False | Defensive Troops | lyseni | 16.0 | main_or_minor_line |
| 444 | Martell Levy | martell_levy | 21.6 | 19.4 | 81.0 | 25.1 | True | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 445 | Karstark Levy | freehouses_levy | 21.2 | 19.9 | 68.0 | 21.2 | True | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 446 | Arryn Footman | arryn_footman | 21.1 | 17.7 | 80.0 | 23.0 | True | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 447 | Bolton Levy | bolton_levy | 20.8 | 19.4 | 60.0 | 20.4 | True | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 448 | Frey Levy | frey_levy | 20.8 | 19.4 | 60.0 | 20.4 | True | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 449 | Myrish Soldier | myrish_soldier | 20.8 | 17.4 | 72.0 | 24.0 | True | False | Defensive Troops | myrish | 16.0 | main_or_minor_line |
| 450 | Crownlands Squire | crownlands_squire | 20.8 | 17.4 | 71.0 | 23.1 | True | False | Defensive Troops | crownlands | 16.0 | main_or_minor_line |
| 451 | Kingsguard's Squire | kingsguard_squire | 20.8 | 17.4 | 71.0 | 23.1 | True | False | Defensive Troops | crownlands | 16.0 | main_or_minor_line |
| 452 | Ibbenese Militia Spearman | ibbenese_militia_spearman | 20.7 | 14.1 | 42.2 | 12.2 | True | False | Defensive Troops | ibbenese | 11.0 | special_or_unlinked |
| 453 | Dondarrion Levy | dondarion_levy | 20.5 | 18.1 | 84.0 | 25.6 | True | False | Defensive Troops | stormlands | 11.0 | main_or_minor_line |
| 454 | Baratheon Footman | baratheon_footman | 20.4 | 18.0 | 83.0 | 25.4 | True | False | Defensive Troops | stormlands | 11.0 | main_or_minor_line |
| 455 | Stark Levy | stark_levy | 20.0 | 17.5 | 80.0 | 24.6 | True | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 456 | YiTish Militia Spearman | yiti_militia_spearman | 19.8 | 16.2 | 70.0 | 22.4 | True | False | Defensive Troops | yiti | 11.0 | special_or_unlinked |
| 457 | Qartheen Militia Veteran Spearman | qartheen_militia_veteran_spearman | 19.7 | 15.5 | 51.0 | 14.7 | True | False | Defensive Troops | qartheen | 16.0 | special_or_unlinked |
| 458 | Valyrian Militia Spearman | valyrian_militia_spearman | 19.7 | 16.1 | 69.0 | 22.2 | True | False | Defensive Troops | valyrian | 11.0 | special_or_unlinked |
| 459 | Volantene Militia Spearman | volantine_militia_spearman | 19.7 | 16.1 | 69.0 | 22.2 | True | False | Defensive Troops | volantine | 11.0 | special_or_unlinked |
| 460 | Norvoshi Militia Spearman | norvos_militia_spearman | 19.7 | 16.1 | 69.0 | 22.2 | True | False | Defensive Troops | norvos | 11.0 | special_or_unlinked |
| 461 | Pentoshi Militia Spearman | pentoshi_militia_spearman | 19.7 | 16.1 | 69.0 | 22.2 | True | False | Defensive Troops | pentoshi | 11.0 | special_or_unlinked |
| 462 | Manderly Levy | whiteharbor_levy | 19.7 | 17.1 | 79.0 | 24.1 | True | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 463 | Qohorik Militia Spearman | qohorik_militia_spearman | 19.6 | 16.0 | 67.0 | 21.9 | True | False | Defensive Troops | qohorik | 11.0 | special_or_unlinked |
| 464 | Glover Levy | glover_levy | 19.5 | 17.3 | 79.0 | 24.2 | True | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 465 | Tyroshi Militia Spearman | tyroshi_militia_spearman | 19.5 | 15.9 | 61.0 | 21.8 | True | False | Defensive Troops | tyroshi | 11.0 | special_or_unlinked |
| 466 | Lyseni Militia Spearman | lyseni_militia_spearman | 19.5 | 15.9 | 61.0 | 21.8 | True | False | Defensive Troops | lyseni | 11.0 | special_or_unlinked |
| 467 | Myrish Militia Spearman | myrish_militia_spearman | 19.5 | 15.9 | 61.0 | 21.8 | True | False | Defensive Troops | myrish | 11.0 | special_or_unlinked |
| 468 | Summer Isles Militia Spearman | summer_militia_spearman | 19.5 | 15.9 | 61.0 | 21.8 | True | False | Defensive Troops | summer | 11.0 | special_or_unlinked |
| 469 | Ghiscari Militia Spearman | ghiscari_militia_spearman | 19.5 | 15.9 | 61.0 | 21.8 | True | False | Defensive Troops | ghiscari | 11.0 | special_or_unlinked |
| 470 | Ghiscari Mounted Archer | ghiscari_mounted_archer | 19.5 | 25.3 | 117.0 | 32.5 | False | True | Ranged Troops | ghiscari | 21.0 | main_or_minor_line |
| 471 | Vale Militia Spearman | vale_militia_spearman | 19.5 | 15.9 | 69.0 | 22.2 | True | False | Defensive Troops | vale | 11.0 | special_or_unlinked |
| 472 | Stormlands Militia Spearman | stormlands_militia_spearman | 19.5 | 15.9 | 69.0 | 22.2 | True | False | Defensive Troops | stormlands | 11.0 | special_or_unlinked |
| 473 | Dragonstone Militia Spearman | dragonstone_militia_spearman | 19.5 | 15.9 | 69.0 | 22.2 | True | False | Defensive Troops | dragonstone | 11.0 | special_or_unlinked |
| 474 | Riverlands Militia Spearman | river_militia_spearman | 19.5 | 15.9 | 69.0 | 22.2 | True | False | Defensive Troops | river | 11.0 | special_or_unlinked |
| 475 | Reach Militia Spearman | reach_militia_spearman | 19.5 | 15.9 | 69.0 | 22.2 | True | False | Defensive Troops | reach | 11.0 | special_or_unlinked |
| 476 | Cerwyn Levy | cerwyn_levy | 19.4 | 17.2 | 79.0 | 24.2 | True | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 477 | Umber Levy | umber_levy | 18.9 | 16.7 | 68.0 | 21.2 | True | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 478 | Skagosi Footman | skag_footman | 18.8 | 16.5 | 44.0 | 12.6 | True | False | Defensive Troops | skagosi | 11.0 | main_or_minor_line |
| 479 | Clegane Levy | clegane_levy | 18.5 | 16.2 | 60.0 | 20.4 | True | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 480 | Norvoshi Footman | norvos_footman | 18.5 | 15.7 | 66.0 | 21.6 | True | False | Defensive Troops | norvos | 11.0 | main_or_minor_line |
| 481 | Sarnori Militia Spearman | sarnor_militia_spearman | 18.4 | 14.6 | 58.0 | 19.6 | True | False | Defensive Troops | sarnor | 11.0 | special_or_unlinked |
| 482 | Lyseni Footman | lyseni_footman | 18.3 | 15.9 | 59.0 | 21.4 | True | False | Defensive Troops | lyseni | 11.0 | main_or_minor_line |
| 483 | Sarnori Footman | sarnor_footman | 18.1 | 15.3 | 49.0 | 17.8 | True | False | Defensive Troops | sarnor | 11.0 | main_or_minor_line |
| 484 | Wight Militia Veteran Spearman | wight_militia_veteran_spearman | 17.1 | 12.6 | 53.8 | 14.2 | True | False | Defensive Troops | whitewalker | 16.0 | special_or_unlinked |
| 485 | Stormlands Levy | stormlands_levy | 17.1 | 15.0 | 57.0 | 20.2 | True | False | Defensive Troops | stormlands | 11.0 | main_or_minor_line |
| 486 | Freefolk Militia Spearman | freefolk_militia_spearman | 15.5 | 11.2 | 52.0 | 14.1 | True | False | Defensive Troops | freefolk | 11.0 | special_or_unlinked |
| 487 | Wight Militia Spearman | wight_militia_spearman | 15.2 | 8.5 | 35.0 | 9.3 | True | False | Defensive Troops | whitewalker | 11.0 | special_or_unlinked |
| 488 | Qartheen Militia Spearman | qartheen_militia_spearman | 11.9 | 6.8 | 17.5 | 4.0 | True | False | Defensive Troops | qartheen | 11.0 | special_or_unlinked |


## Ranked — Offensive melee (773 troops)

| rank | troop_name | troop_id | offensive_melee_role_score | crafted_melee_score_base | crafted_melee_template | crafted_melee_item | defense_score_base | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Captain of the Kingsguard | mounted_kingsguard | 100.0 | 100.0 | TwoHandedSword | vlandia_2hsword_1_t5 | 65.8 | True | Defensive Troops | crownlands | 31.0 | main_or_minor_line |
| 2 | Yi Ti Mounted Shi | yiti_samurai | 98.4 | 100.0 | TwoHandedSword | yiti_sword | 53.2 | True | Skirmishers | yiti | 31.0 | main_or_minor_line |
| 3 | Mountain's Man | mountains_man | 88.9 | 100.0 | TwoHandedSword | western_2hsword_t4 | 27.5 | False | Offensive Melee | vlandia | 31.0 | main_or_minor_line |
| 4 | Stormlands Thunder Knight | stormlands_thunderknight | 88.4 | 100.0 | TwoHandedSword | western_2hsword_t4 | 47.4 | True | Defensive Troops | stormlands | 31.0 | main_or_minor_line |
| 5 | Golden Company Mahout | golden_elite_pikeman | 85.9 | 82.0 | TwoHandedPolearm | golden_company_spear | 100.0 | True | Skirmishers | volantine | 31.0 | main_or_minor_line |
| 6 | Ghiscari Lockstep Legionnaire | ghiscari_unsullied_unbroken | 85.1 | 100.0 | TwoHandedSword | ghiscari_sword | 29.4 | False | Skirmishers | ghiscari | 31.0 | main_or_minor_line |
| 7 | Riverlands Admiral | river_admiral | 81.3 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 31.9 | False | Defensive Troops | river | 31.0 | main_or_minor_line |
| 8 | Arryn Winged Knight | arryn_moonknight | 80.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 65.2 | True | Defensive Troops | vale | 31.0 | main_or_minor_line |
| 9 | White Harbor Knight Commander | whiteharbor_knight_commander | 80.3 | 82.0 | TwoHandedPolearm | manderly_spear2 | 64.0 | True | Defensive Troops | battania | 31.0 | main_or_minor_line |
| 10 | Mallister Eagle Knight | mallister_knight | 77.6 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 68.2 | True | Defensive Troops | river | 31.0 | main_or_minor_line |
| 11 | Dondarrion Boltknight | dondarion_boltknight | 77.1 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 64.7 | True | Defensive Troops | stormlands | 31.0 | main_or_minor_line |
| 12 | Lannister Prideknight | lannister_prideknight | 77.1 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 64.3 | True | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 13 | Royce Heroine | royce_heroine | 76.7 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 61.5 | True | Defensive Troops | vale | 31.0 | main_or_minor_line |
| 14 | Knights of Starfall | dayne_starfall_knights | 76.6 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 60.7 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 15 | Water Gardens Sentinel | garden_sentinel | 75.9 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 55.1 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 16 | Boneway Guardian | boneway_guardian | 75.8 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 54.4 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 17 | Mammoth Riding Giant | giant_rider | 75.4 | 73.3 | TwoHandedAxe | giant_club | 86.9 | True | Ranged Troops | freefolk | 31.0 | main_or_minor_line |
| 18 | Reach Flower Knight | reach_flower_knight | 73.4 | 82.0 | TwoHandedPolearm | vlandia_polearm_1_t5 | 61.4 | True | Defensive Troops | reach | 31.0 | main_or_minor_line |
| 19 | Knight of the Vale | vale_knight_of | 73.2 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 59.9 | True | Defensive Troops | vale | 31.0 | main_or_minor_line |
| 20 | Realm Paladin | realm_paladin | 73.2 | 82.0 | TwoHandedPolearm | baratheon_spear | 59.9 | True | Skirmishers | crownlands | 31.0 | main_or_minor_line |
| 21 | Tyrell Cavalier | tyrell_cavalier | 73.0 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 58.6 | True | Defensive Troops | reach | 31.0 | main_or_minor_line |
| 22 | Queen's Man | dragonstone_steel_curtain | 73.0 | 82.0 | TwoHandedPolearm | baratheon_spear | 58.5 | True | Skirmishers | dragonstone | 31.0 | main_or_minor_line |
| 23 | Riverrun Captain | riverrun_captain | 72.9 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 57.7 | True | Defensive Troops | river | 31.0 | main_or_minor_line |
| 24 | Stark Sworn Sword | stark_swornsword | 72.9 | 82.0 | TwoHandedPolearm | bill_hook|northern_halberd | 45.4 | False | Defensive Troops | battania | 31.0 | main_or_minor_line |
| 25 | Grafton Flaming Knight | grafton_flameknight | 72.8 | 82.0 | TwoHandedPolearm | grafton_spear | 44.8 | False | Defensive Troops | vale | 31.0 | main_or_minor_line |
| 26 | Westerling Hedgeknight | westerling_hedgeknight | 72.7 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 43.6 | False | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 27 | Unsullied | unsullied | 72.6 | 82.0 | TwoHandedPolearm | unsullied_spear | 35.0 | False | Skirmishers | ghiscari | 31.0 | special_or_unlinked |
| 28 | Norvoshi Grand Bearded Priest | mounted_priest | 72.4 | 82.0 | TwoHandedPolearm | norvoshi_long_axe | 53.8 | True | Defensive Troops | norvos | 31.0 | main_or_minor_line |
| 29 | Ibbenese Navigator | ibbenese_navigator | 72.4 | 82.0 | TwoHandedPolearm | ibb_glaive | 41.1 | False | Skirmishers | ibbenese | 31.0 | main_or_minor_line |
| 30 | Sarnori Spider | sarnor_spider | 70.8 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 40.9 | True | Skirmishers | sarnor | 31.0 | main_or_minor_line |
| 31 | Captain of the Queen's Guard | queensguard_captain | 70.7 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 66.6 | True | Defensive Troops | valyrian | 31.0 | main_or_minor_line |
| 32 | Umber Berzerker | umber_berzerker | 70.7 | 82.0 | TwoHandedPolearm | northern_spear_4_t5 | 28.2 | False | Skirmishers | battania | 31.0 | main_or_minor_line |
| 33 | Magister Guard Elite | magister_guard | 70.3 | 82.0 | TwoHandedPolearm | pentoshi_spear | 62.8 | True | Skirmishers | pentoshi | 31.0 | main_or_minor_line |
| 34 | Valyrian Dragonlord Protector | valyrian_dragonlord_protector | 70.2 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 62.5 | True | Defensive Troops | valyrian | 31.0 | main_or_minor_line |
| 35 | Tarly Vanguard | tarly_vanguard | 69.8 | 82.0 | TwoHandedPolearm | ranseur | 47.3 | False | Skirmishers | reach | 31.0 | main_or_minor_line |
| 36 | Black Goat Sacrificer | qohorik_goat_sacrificer | 69.8 | 82.0 | TwoHandedPolearm | qohorik_spear | 59.2 | True | Skirmishers | qohorik | 31.0 | main_or_minor_line |
| 37 | Celtigar Banneret | celtigar_banneret | 69.4 | 82.0 | TwoHandedPolearm | crownlands_halberd | 44.2 | False | Skirmishers | dragonstone | 31.0 | main_or_minor_line |
| 38 | Skagosi Stoneborn Champion | skagosi_stoneborn_champion | 69.2 | 82.0 | TwoHandedPolearm | skagosi_spear | 54.6 | True | Skirmishers | skagosi | 31.0 | main_or_minor_line |
| 39 | Bolton Flayer | bolton_flayer | 69.1 | 82.0 | TwoHandedPolearm | bolton_spear | 41.2 | False | Skirmishers | battania | 31.0 | main_or_minor_line |
| 40 | Glover Bushranger | glover_bushranger | 68.8 | 82.0 | TwoHandedPolearm | highland_spear_4_t4 | 39.2 | False | Skirmishers | battania | 31.0 | main_or_minor_line |
| 41 | Baratheon Hammerknight | baratheon_pikeknight | 68.5 | 82.0 | TwoHandedPolearm | spiked_polehammer | 36.4 | False | Defensive Troops | stormlands | 31.0 | main_or_minor_line |
| 42 | Tarth Master Halberdier | tarth_master_halberdier | 68.4 | 82.0 | TwoHandedPolearm | stormlands_halberd | 36.2 | False | Defensive Troops | stormlands | 31.0 | main_or_minor_line |
| 43 | Karstark Loyalist | karstark_loyalist | 67.9 | 82.0 | TwoHandedPolearm | northern_halberd | 32.3 | False | Defensive Troops | battania | 31.0 | main_or_minor_line |
| 44 | Guardian of the Rock | casterly_guardian | 66.5 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 44.7 | False | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 45 | Bracken Pikemaster | bracken_master_pikeman | 65.7 | 75.7 | OneHandedSword | sturgia_sword_4_t4 | 38.0 | False | Defensive Troops | river | 31.0 | main_or_minor_line |
| 46 | Guardian of Oldtown | oldtown_guardian | 65.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 39.1 | False | Defensive Troops | reach | 31.0 | main_or_minor_line |
| 47 | Triarch Guardian | triarch_guardian | 64.7 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 32.5 | False | Ranged Troops | volantine | 31.0 | main_or_minor_line |
| 48 | Giant | giant | 64.4 | 73.3 | TwoHandedAxe | giant_club | 40.1 | False | Offensive Melee | freefolk | 26.0 | main_or_minor_line |
| 49 | Giant Archer | giant_archer | 64.4 | 73.3 | TwoHandedAxe | giant_club | 40.1 | False | Ranged Troops | freefolk | 31.0 | main_or_minor_line |
| 50 | Elder Giant | elder_giant | 64.4 | 73.3 | TwoHandedAxe | giant_club | 40.1 | False | Ranged Troops | freefolk | 35.0 | main_or_minor_line |
| 51 | Harlaw Captain | harlaw_captain | 63.6 | 73.3 | TwoHandedAxe | war_scythe | 40.6 | False | Defensive Troops | sturgia | 31.0 | main_or_minor_line |
| 52 | Qartheen Enthroned Guardian | enthroned_guardian | 62.9 | 75.7 | OneHandedSword | qarth_sword | 40.3 | False | Ranged Troops | qartheen | 31.0 | main_or_minor_line |
| 53 | Cerwyn Marauder | cerwyn_marauder | 61.6 | 73.3 | TwoHandedAxe | northern_twoh_axe | 24.9 | False | Offensive Melee | battania | 31.0 | main_or_minor_line |
| 54 | Velaryon Sea Guard | velaryon_sea_guard | 59.5 | 75.7 | OneHandedSword | velaryon_cutlass | 37.6 | False | Defensive Troops | dragonstone | 31.0 | main_or_minor_line |
| 55 | Ravens' Teeth | ravens_teeth | 58.9 | 75.7 | OneHandedSword | vlandia_sword_3_t4 | 32.7 | False | Ranged Troops | river | 31.0 | main_or_minor_line |
| 56 | Tyroshi Corsair | tyroshi_corsair | 57.3 | 73.3 | OneHandedAxe | tyroshi_axe3 | 37.3 | False | Skirmishers | tyroshi | 31.0 | main_or_minor_line |
| 57 | Freefolk Thenn Impaler | freefolk_thenn_impaler | 56.9 | 75.7 | OneHandedSword | thenn_sword2 | 41.2 | False | Defensive Troops | freefolk | 31.0 | main_or_minor_line |
| 58 | Lyseni Enforcer | lyseni_enforcer | 56.8 | 73.3 | TwoHandedAxe | aserai_2haxe_2_t4 | 33.5 | False | Offensive Melee | lyseni | 31.0 | main_or_minor_line |
| 59 | Mormont Bowmaiden | mormont_bowmaiden | 56.7 | 73.3 | TwoHandedAxe | sturgia_2haxe_1_t4 | 32.5 | False | Ranged Troops | battania | 31.0 | main_or_minor_line |
| 60 | Greyjoy Sniper | greyjoy_sniper | 55.4 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 29.1 | False | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 61 | Frey Assassin | frey_assassin | 54.7 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 23.9 | False | Ranged Troops | river | 31.0 | main_or_minor_line |
| 62 | Myrish Artisan of War | myrish_artisan | 53.7 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 40.1 | False | Ranged Troops | myrish | 31.0 | main_or_minor_line |
| 63 | Night's Watch Protector of the Realm | nightswatch_protector | 52.5 | 75.7 | OneHandedSword | broad_arming_sword_t4 | 30.2 | False | Ranged Troops | nightswatch | 31.0 | main_or_minor_line |
| 64 | Stormlands Fell Knight | stormlands_fell_knight | 52.0 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 47.3 | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 65 | Sadistic Wight | sadistic_wight | 51.8 | 73.3 | TwoHandedAxe | northern_axe_t3 | 17.8 | False | Offensive Melee | whitewalker | 31.0 | main_or_minor_line |
| 66 | Goldenheart Warrior | summer_master_longbowman | 49.2 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 28.2 | False | Ranged Troops | summer | 31.0 | main_or_minor_line |
| 67 | Qohorik Falxman | qohorik_falxman | 49.0 | 100.0 | TwoHandedSword | battania_2hsword_4_t4 | 32.0 | False | Offensive Melee | qohorik | 26.0 | main_or_minor_line |
| 68 | Yi Ti Shi | yiti_pikeman | 48.8 | 100.0 | TwoHandedSword | yiti_sword | 29.9 | False | Skirmishers | yiti | 26.0 | main_or_minor_line |
| 69 | Golden Company Elephant Rider | golden_horseman | 47.9 | 82.0 | TwoHandedPolearm | golden_company_spear | 95.1 | True | Defensive Troops | volantine | 26.0 | main_or_minor_line |
| 70 | Ghiscari Queen's Guard | ghiscari_queens_guard | 47.9 | 100.0 | TwoHandedSword | ghiscari_sword | 46.5 | True | Defensive Troops | ghiscari | 26.0 | main_or_minor_line |
| 71 | Valyrian Cavalry | targaryen_dragonknight | 47.4 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 64.8 | True | Skirmishers | valyrian | 26.0 | main_or_minor_line |
| 72 | White Harbor Elite Knight | whiteharbor_elite_knight | 47.2 | 82.0 | TwoHandedPolearm | manderly_spear | 63.6 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 73 | Pentoshi Lancer | pentoshi_lancer | 46.8 | 82.0 | TwoHandedPolearm | pentoshi_spear | 60.7 | True | Defensive Troops | pentoshi | 26.0 | main_or_minor_line |
| 74 | Kingsguard | kingsguard_captain | 46.4 | 100.0 | TwoHandedSword | vlandia_2hsword_1_t5 | 42.6 | False | Defensive Troops | crownlands | 26.0 | main_or_minor_line |
| 75 | Lannister Officer | lannister_officer | 46.3 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 42.1 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 76 | Clegane Brigand | clegane_horseman | 46.3 | 82.0 | TwoHandedPolearm | sturgia_lance_1_t4 | 56.2 | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 77 | Umber Horseman | umber_horseman | 46.0 | 82.0 | TwoHandedPolearm | sturgia_lance_1_t4 | 53.8 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 78 | Skagosi Stoneborn | skagosi_stoneborn | 45.9 | 82.0 | TwoHandedPolearm | skagosi_spear | 53.1 | True | Skirmishers | skagosi | 26.0 | main_or_minor_line |
| 79 | Karstark Shock Cavalry | karstark_shock_cavalry | 45.6 | 82.0 | TwoHandedPolearm | sturgia_lance_1_t4 | 51.1 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 80 | Riverlands Swordmaster | river_swordmaster | 45.0 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 31.9 | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 81 | Ghiscari Elite Legionnaire | ghiscari_unsullied_unbent | 44.7 | 100.0 | TwoHandedSword | ghiscari_sword | 29.4 | False | Skirmishers | ghiscari | 26.0 | main_or_minor_line |
| 82 | Stark Cavalry | stark_cavalry | 44.3 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 66.0 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 83 | Targaryen Queen's Guard | targ_queensguard | 44.2 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 66.2 | True | Defensive Troops | valyrian | 26.0 | main_or_minor_line |
| 84 | Grafton Horseman | grafton_horseman | 44.0 | 82.0 | TwoHandedPolearm | grafton_spear | 64.2 | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 85 | Lannister Knight | lannister_knight | 44.0 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 64.1 | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 86 | Westerling Knight | westerling_horseman | 43.8 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 62.9 | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 87 | Valyrian Dragonknight | valyrian_dragonknight | 43.7 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 62.0 | True | Defensive Troops | valyrian | 26.0 | main_or_minor_line |
| 88 | Mallister Knight | mallister_horseman | 43.6 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 61.4 | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 89 | Casterly Rock Champion | casterly_champion | 43.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 60.4 | True | Skirmishers | vlandia | 26.0 | main_or_minor_line |
| 90 | Royce Cavalrywomen | royce_cavalrywomen | 43.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 60.3 | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 91 | Baratheon Knight | baratheon_knight | 43.5 | 82.0 | TwoHandedPolearm | baratheon_spear | 59.1 | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 92 | Vale Elite Knight | vale_elite_knight | 43.1 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 57.4 | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 93 | Arryn Knight | arryn_knight | 43.1 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 57.3 | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 94 | Yi Ti Glaiveman | yiti_horseman | 43.1 | 82.0 | TwoHandedPolearm | yiti_qinglongji | 57.1 | True | Defensive Troops | yiti | 26.0 | main_or_minor_line |
| 95 | Greyjoy Horseman | greyjoy_horseman | 43.0 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 56.7 | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 96 | Volantene Mahout | tigercloak_camel_cavalry | 42.9 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 82.1 | True | Defensive Troops | volantine | 26.0 | main_or_minor_line |
| 97 | Hightower Cavalry | hightower_cavalry | 42.9 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 55.7 | True | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 98 | Bracken Horseman | bracken_horseman | 42.9 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 55.3 | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 99 | Martell Horseman | martell_horseman | 42.7 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 54.2 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 100 | Celtigar Knight | celtigar_knight | 42.7 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 54.0 | True | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 101 | Reach Horseman | reach_knight | 42.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 52.4 | True | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 102 | Harlaw Raider | harlaw_horseman | 42.4 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 52.0 | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 103 | Tyrell Horseman | tyrell_knight | 42.4 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 51.5 | True | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 104 | Tarly Knight | tarly_knight | 41.9 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 48.2 | True | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 105 | Gold Cloak Captain | goldcloak_captain | 41.5 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 44.4 | True | Defensive Troops | crownlands | 26.0 | main_or_minor_line |
| 106 | Frey Horseman | frey_horseman | 41.0 | 82.0 | TwoHandedPolearm | sturgia_lance_1_t4 | 40.7 | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 107 | Summer Isles Horseman | summer_horseman | 40.8 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 38.9 | True | Defensive Troops | summer | 26.0 | main_or_minor_line |
| 108 | Dondarrion Knight | dondarion_knight | 40.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 62.8 | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 109 | Realm Knight | realm_knight | 40.4 | 82.0 | TwoHandedPolearm | baratheon_spear | 61.8 | True | Skirmishers | crownlands | 26.0 | main_or_minor_line |
| 110 | Qohorik Lancer | qohorik_lancer | 40.2 | 82.0 | TwoHandedPolearm | qohorik_spear | 60.6 | True | Defensive Troops | qohorik | 26.0 | main_or_minor_line |
| 111 | Sarnori Master Javelinier | sarnor_master_javelinier | 40.1 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 33.9 | True | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 112 | Pentoshi Cavalry | pentoshi_cavalry | 40.1 | 82.0 | TwoHandedPolearm | pentoshi_spear | 59.6 | True | Defensive Troops | pentoshi | 26.0 | main_or_minor_line |
| 113 | Mormont Horseman | mormont_horseman | 40.0 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 59.1 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 114 | Dragonstone Horseman | dragonstone_horseman | 39.7 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 56.2 | True | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 115 | Myrish Cavalry | myrish_cavalry | 39.6 | 82.0 | TwoHandedPolearm | western_spear_5_t4 | 56.1 | True | Defensive Troops | myrish | 26.0 | main_or_minor_line |
| 116 | Blackwood Horseman | blackwood_horseman | 39.6 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 55.9 | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 117 | Stormlands Horseman | stormlands_horseman | 39.6 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 55.9 | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 118 | Dayne Knight | dayne_knight | 39.6 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 55.8 | True | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 119 | Vale Elite Voulgier | vale_elite_voulgier | 39.5 | 82.0 | TwoHandedPolearm | vlandia_polearm_1_t5 | 55.3 | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 120 | Vale Elite Lancer | vale_elite_lancer | 39.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 55.3 | True | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 121 | Yronwood Knight | yronwood_knight | 39.4 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 54.4 | True | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 122 | Bolton Cavalry | bolton_knight | 39.4 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 54.4 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 123 | Riverlands Cavalry | river_calvary | 39.2 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 52.6 | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 124 | Glover Horseman | glover_horseman | 39.1 | 82.0 | TwoHandedPolearm | sturgia_lance_1_t4 | 51.7 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 125 | Night's Watch Horseman | nightswatch_horseman | 39.0 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 51.0 | True | Defensive Troops | nightswatch | 26.0 | main_or_minor_line |
| 126 | Tully Knight | tully_knight | 39.0 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 51.0 | True | Defensive Troops | river | 26.0 | main_or_minor_line |
| 127 | High King Guardian | sarnor_highking_guardian | 39.0 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 50.9 | True | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 128 | Velaryon Horseman | velaryon_horseman | 39.0 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 50.9 | True | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 129 | Tyroshi Cavalry | tyroshi_cavalry | 39.0 | 82.0 | TwoHandedPolearm | highland_spear_4_t4 | 50.9 | True | Defensive Troops | tyroshi | 26.0 | main_or_minor_line |
| 130 | Lyseni Cavalry | lyseni_cavalry | 39.0 | 82.0 | TwoHandedPolearm | lyseni_spear | 50.9 | True | Defensive Troops | lyseni | 26.0 | main_or_minor_line |
| 131 | Royce Elite Warrior | royce_elite_warrior | 39.0 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 38.6 | False | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 132 | Ibbenese Whaler | ibbenese_whaler | 38.9 | 82.0 | TwoHandedPolearm | ibb_spear | 38.5 | False | Defensive Troops | ibbenese | 26.0 | main_or_minor_line |
| 133 | Ibbenese Horseman | ibbenese_horseman | 38.9 | 82.0 | TwoHandedPolearm | ibb_spear | 49.9 | True | Defensive Troops | ibbenese | 26.0 | main_or_minor_line |
| 134 | Tarth Horseman | tarth_horseman | 38.7 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 48.8 | True | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 135 | Qartheen Elite Hoplite | qartheen_elite_hoplite | 38.7 | 82.0 | TwoHandedPolearm | qarth_spear | 36.6 | False | Defensive Troops | qartheen | 26.0 | main_or_minor_line |
| 136 | Norvoshi Priest Guard | norvos_priestguard | 38.7 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 48.3 | True | Defensive Troops | norvos | 26.0 | main_or_minor_line |
| 137 | Summer Isles Spearmaster | summer_pikeman | 38.6 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 35.4 | False | Skirmishers | summer | 26.0 | main_or_minor_line |
| 138 | Free Folk Horseman | freefolk_horseman | 38.5 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 46.9 | True | Skirmishers | freefolk | 26.0 | main_or_minor_line |
| 139 | Cerwyn Horseman | cerwyn_horseman | 38.2 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 44.7 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 140 | Qartheen Master Cameleer | qartheen_master_cameleer | 38.0 | 82.0 | TwoHandedPolearm | qarth_spear | 43.3 | True | Defensive Troops | qartheen | 26.0 | main_or_minor_line |
| 141 | Dragonstone Shock Knight | dragonstone_shock_knight | 37.0 | 82.0 | TwoHandedPolearm | baratheon_spear | 61.2 | True | Skirmishers | dragonstone | 26.0 | main_or_minor_line |
| 142 | White Harbor Knight | whiteharbor_knight | 36.7 | 82.0 | TwoHandedPolearm | manderly_spear | 58.9 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 143 | Stark House Guard | stark_houseguard | 36.5 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 45.4 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 144 | Mallister House Guard | mallister_houseguard | 36.5 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 45.4 | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 145 | Beastbound Wight | beastbound_wight | 36.4 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 30.6 | True | Skirmishers | whitewalker | 26.0 | main_or_minor_line |
| 146 | Grafton House Guard | grafton_houseguard | 36.3 | 82.0 | TwoHandedPolearm | grafton_spear | 43.6 | False | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 147 | Valyrian Captain | valyrian_captain | 36.2 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 43.2 | False | Defensive Troops | valyrian | 26.0 | main_or_minor_line |
| 148 | Lannister House Guard | lannister_houseguard | 36.1 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 42.5 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 149 | Westerling House Guard | westerling_houseguard | 36.1 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 42.4 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 150 | Celtigar Halberdier | celtigar_halberdier | 36.1 | 82.0 | TwoHandedPolearm | crownlands_halberd | 42.3 | False | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 151 | Qohorik Elite Spearman | qohorik_elite_spearman | 36.1 | 82.0 | TwoHandedPolearm | qohorik_spear | 42.1 | False | Defensive Troops | qohorik | 26.0 | main_or_minor_line |
| 152 | Ghiscari Manticore | ghiscari_manticore | 36.0 | 100.0 | TwoHandedSword | ghiscari_sword | 25.0 | False | Ranged Troops | ghiscari | 26.0 | main_or_minor_line |
| 153 | Stark Pikeman | stark_pikeman | 36.0 | 75.7 | OneHandedAxe|OneHandedSword | northern_axe|northern_sword | 45.4 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 154 | Dondarrion House Guard | dondarion_houseguard | 36.0 | 82.0 | TwoHandedPolearm | stormlands_halberd | 41.2 | False | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 155 | Pentoshi Spearman | pentoshi_spearman | 36.0 | 82.0 | TwoHandedPolearm | pentoshi_spear | 41.0 | False | Skirmishers | pentoshi | 26.0 | main_or_minor_line |
| 156 | Ibbenese Mariner | ibbenese_mariner | 35.9 | 82.0 | TwoHandedPolearm | ibb_glaive | 40.9 | False | Defensive Troops | ibbenese | 26.0 | main_or_minor_line |
| 157 | Black Goat Devout | qohorik_goat_devout | 35.9 | 82.0 | TwoHandedPolearm | qohorik_spear | 40.7 | False | Skirmishers | qohorik | 26.0 | main_or_minor_line |
| 158 | Reach Champion | reach_champion | 35.9 | 82.0 | TwoHandedPolearm | vlandia_polearm_1_t5 | 40.3 | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 159 | Martell House Guard | martell_houseguard | 35.9 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 40.3 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 160 | Harlaw Chief Mate | harlaw_chief_mate | 35.8 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 39.6 | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 161 | Dragonstone Elite Halberdier | dragonstone_headsman | 35.8 | 82.0 | TwoHandedPolearm | dragonstone_elite_halberd | 39.6 | False | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 162 | Valyrian Elite Pikeman | targaryen_elite_pikeman | 35.8 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 43.2 | False | Defensive Troops | valyrian | 26.0 | main_or_minor_line |
| 163 | Velaryon Renegade | velaryon_renegade | 35.7 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 39.2 | False | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 164 | Hightower Captain | hightower_guardian | 35.7 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 39.1 | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 165 | Mormont House Guard | mormont_houseguard | 35.6 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 38.3 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 166 | Skagosi Master Spearman | skag_master_spearman | 35.6 | 82.0 | TwoHandedPolearm | skagosi_spear | 38.3 | False | Defensive Troops | skagosi | 26.0 | main_or_minor_line |
| 167 | Targaryen Knight | targ_knight | 35.6 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 50.3 | True | Defensive Troops | valyrian | 21.0 | main_or_minor_line |
| 168 | Valyrian Knight | valyrian_knight | 35.6 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 50.0 | True | Defensive Troops | valyrian | 21.0 | main_or_minor_line |
| 169 | Myrish Legionnaire | myrish_axeman | 35.5 | 82.0 | TwoHandedPolearm | western_spear_5_t4 | 37.6 | False | Defensive Troops | myrish | 26.0 | main_or_minor_line |
| 170 | Arryn House Guard | arryn_houseguard | 35.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 37.2 | False | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 171 | White Harbor Pike Knight | whiteharbor_elite_pikeman | 35.4 | 75.7 | OneHandedSword | manderly_sword | 40.6 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 172 | Freefolk Thenn Cannibal | freefolk_thenn_cannibal | 35.4 | 75.7 | OneHandedSword | thenn_sword2 | 40.3 | False | Defensive Troops | freefolk | 26.0 | main_or_minor_line |
| 173 | Baratheon House Guard | baratheon_houseguard | 35.4 | 82.0 | OneHandedSword|TwoHandedPolearm | spiked_polehammer|vlandia_sword_4_t4 | 36.4 | False | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 174 | Tarth Halberdier | tarth_halberdier | 35.3 | 82.0 | TwoHandedPolearm | stormlands_halberd | 36.2 | False | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 175 | Umber House Guard | umber_houseguard | 35.2 | 82.0 | TwoHandedPolearm | northern_spear_4_t5 | 35.3 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 176 | Bracken House Guard | bracken_houseguard | 35.2 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 34.9 | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 177 | Volantine Elite Warrior | tigercloak_elite_warrior | 35.2 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 34.9 | False | Defensive Troops | volantine | 26.0 | main_or_minor_line |
| 178 | Dreadfort Blackguard | dreadfort_blackguard | 35.2 | 82.0 | TwoHandedPolearm | bolton_spear | 34.8 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 179 | Clegane House Guard | clegane_houseguard | 35.1 | 82.0 | TwoHandedPolearm | western_spear_5_t4 | 34.6 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 180 | Blackwood House Guard | blackwood_houseguard | 35.1 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 34.3 | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 181 | Tully House Guard | tully_houseguard | 35.1 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 34.3 | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 182 | Norvoshi Devout Bearded Priest | devout_bearded_priest | 35.1 | 82.0 | TwoHandedPolearm | norvoshi_long_axe | 33.9 | False | Defensive Troops | norvos | 26.0 | main_or_minor_line |
| 183 | Guard of the Crossing | guard_of_the_crossing | 35.0 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 33.8 | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 184 | Lyseni Spearman | lyseni_spearman | 34.9 | 82.0 | TwoHandedPolearm | lyseni_spear | 32.4 | False | Defensive Troops | lyseni | 26.0 | main_or_minor_line |
| 185 | Lyseni Glaiveman | lyseni_glaiveman | 34.9 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 32.4 | False | Defensive Troops | lyseni | 26.0 | main_or_minor_line |
| 186 | Karstark House Guard | karstark_brute | 34.8 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 32.3 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 187 | Cerwyn Veteran Axeman | cerwyn_master_axeman | 34.8 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 32.2 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 188 | Gold Cloak Halberdier | kingsguard | 34.8 | 82.0 | TwoHandedPolearm | crownlands_halberd | 31.8 | False | Defensive Troops | crownlands | 26.0 | main_or_minor_line |
| 189 | Night's Watch Stalwart | nightswatch_stalwart | 34.8 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 31.8 | False | Defensive Troops | nightswatch | 26.0 | main_or_minor_line |
| 190 | Sarnori Master Spearman | sarnor_master_spearman | 34.8 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 31.7 | False | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 191 | Tigercloak Elite | tigercloak_master | 34.6 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 30.1 | False | Ranged Troops | volantine | 26.0 | main_or_minor_line |
| 192 | Golden Company Gilt Pike Wardens | golden_pikeman | 34.5 | 75.7 | OneHandedSword | golden_company_sword | 33.4 | False | Defensive Troops | volantine | 26.0 | main_or_minor_line |
| 193 | Stormlands Knight | stormlands_knight | 34.3 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 35.1 | True | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 194 | Vicious Wight | vicious_wight | 34.2 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 27.4 | False | Defensive Troops | whitewalker | 26.0 | main_or_minor_line |
| 195 | Karstark Outrider | karstark_outrider | 34.0 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 37.7 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 196 | Pentoshi Mounted Archer | pentoshi_mounted_archer | 33.9 | 75.7 | OneHandedSword | pentoshi_sword | 36.6 | True | Ranged Troops | pentoshi | 26.0 | main_or_minor_line |
| 197 | Ghiscari Elite Pikeman | ghiscari_elite_unsullied | 33.9 | 75.7 | OneHandedSword | empire_sword_3_t3 | 28.2 | False | Defensive Troops | ghiscari | 26.0 | main_or_minor_line |
| 198 | Mormont Mounted Huntress | mormont_mounted_huntress | 33.8 | 73.3 | OneHandedAxe | sturgia_axe_4_t4 | 45.4 | True | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 199 | Casterly Rock Marshal | casterly_pikeman | 32.9 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 44.7 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 200 | Riverlands Elite Swordsman | river_elite_swordsman | 32.9 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 31.9 | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 201 | Tyroshi Renegade | tyroshi_renegade | 32.7 | 73.3 | TwoHandedAxe | avalanche_2haxe | 30.3 | False | Offensive Melee | tyroshi | 26.0 | main_or_minor_line |
| 202 | Casterly Rock Knight | casterly_knight | 32.7 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 53.2 | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 203 | Vale House Guard | vale_houseguard | 32.6 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 40.6 | False | Defensive Troops | vale | 26.0 | main_or_minor_line |
| 204 | Lannister Horseman | lannister_horseman | 32.6 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 52.5 | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 205 | Dragonstone House Guard | dragonstone_houseguard | 32.5 | 82.0 | TwoHandedPolearm | sturgia_lance_2_t5 | 39.6 | False | Defensive Troops | dragonstone | 26.0 | main_or_minor_line |
| 206 | Glover Warrior | glover_warrior | 32.4 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 39.2 | False | Skirmishers | battania | 26.0 | main_or_minor_line |
| 207 | Qartheen Pureborn Champion | qartheen_champion | 32.3 | 75.7 | OneHandedSword | qarth_sword | 40.3 | False | Ranged Troops | qartheen | 26.0 | main_or_minor_line |
| 208 | Tyrell House Guard | tyrell_houseguard | 32.2 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 37.6 | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 209 | Skagosi Rider | skagosi_rider | 32.2 | 82.0 | TwoHandedPolearm | skagosi_spear | 49.3 | True | Skirmishers | skagosi | 21.0 | main_or_minor_line |
| 210 | Tarly House Guard | tarly_houseguard | 32.1 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 36.6 | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 211 | Yronwood Veteran Pikeman | yronwood_veteran_pikeman | 32.0 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 37.4 | False | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 212 | Stormlands House Guard | stormlands_houseguard | 32.0 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 35.7 | False | Defensive Troops | stormlands | 26.0 | main_or_minor_line |
| 213 | Ghiscari Legionnaire | ghiscari_unsullied_hoplite | 31.9 | 100.0 | TwoHandedSword | ghiscari_sword | 23.8 | False | Skirmishers | ghiscari | 21.0 | main_or_minor_line |
| 214 | Valyrian Scout | valyrian_scout | 31.9 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 46.9 | True | Skirmishers | valyrian | 21.0 | main_or_minor_line |
| 215 | Greyjoy Finger Dancer | greyjoy_fingerdancer | 31.8 | 75.7 | OneHandedSword | sturgia_sword_5_t4 | 36.3 | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 216 | Riverlands House Guard | river_houseguard | 31.8 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 34.3 | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 217 | Qohorik Horseman | qohorik_horseman | 31.8 | 82.0 | TwoHandedPolearm | qohorik_spear | 46.2 | True | Defensive Troops | qohorik | 21.0 | main_or_minor_line |
| 218 | Reach House Guard | reach_houseguard | 31.5 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 31.6 | False | Defensive Troops | reach | 26.0 | main_or_minor_line |
| 219 | Arryn Horseman | arryn_horseman | 31.4 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 43.0 | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 220 | Riverlands Pikeman | river_pikeman | 31.3 | 75.7 | OneHandedSword | vlandia_sword_3_t4 | 31.9 | False | Defensive Troops | river | 26.0 | main_or_minor_line |
| 221 | Reach Axeman | reach_axeman | 30.8 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 26.3 | False | Offensive Melee | reach | 26.0 | main_or_minor_line |
| 222 | Tyroshi Firstmate | tyroshi_firstmate | 30.6 | 73.3 | OneHandedAxe | tyroshi_axe3 | 37.3 | False | Skirmishers | tyroshi | 26.0 | main_or_minor_line |
| 223 | Royce Rider | royce_rider | 30.6 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 36.7 | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 224 | Free Folk Frosthedge | freefolk_frosthedge | 30.5 | 73.3 | OneHandedAxe | wildling_axe | 36.3 | False | Defensive Troops | freefolk | 26.0 | main_or_minor_line |
| 225 | Umber Axeman | umber_axeman | 30.3 | 73.3 | OneHandedAxe | battle_axe_t4 | 35.0 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 226 | Frey Rider | frey_rider | 30.0 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 32.2 | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 227 | Lyseni Executioner | lyseni_executioner | 29.9 | 73.3 | TwoHandedAxe | aserai_2haxe_2_t4 | 32.0 | False | Offensive Melee | lyseni | 26.0 | main_or_minor_line |
| 228 | Norvoshi Master Axeman | norvos_master_axeman | 29.7 | 73.3 | OneHandedAxe | tzkurion_axe_t3 | 29.8 | False | Defensive Troops | norvos | 26.0 | main_or_minor_line |
| 229 | Norvoshi Pikeman | norvos_pikeman | 29.7 | 73.3 | OneHandedAxe | tzkurion_axe_t3 | 29.8 | False | Defensive Troops | norvos | 26.0 | main_or_minor_line |
| 230 | Ibbenese Timberman | ibbenese_timberman | 29.6 | 73.3 | TwoHandedAxe | northern_axe_t3 | 29.6 | False | Skirmishers | ibbenese | 26.0 | main_or_minor_line |
| 231 | Skagosi Barbarian | skag_barbarian | 29.5 | 73.3 | TwoHandedAxe | sturgia_2haxe_2_t5 | 28.2 | False | Skirmishers | skagosi | 26.0 | main_or_minor_line |
| 232 | Dragonstone Knight | dragonstone_knight | 29.2 | 82.0 | TwoHandedPolearm | baratheon_spear | 52.2 | True | Skirmishers | dragonstone | 21.0 | main_or_minor_line |
| 233 | Free Folk Wildling Berzerker | freefolk_wildling_berzerker | 29.2 | 73.3 | TwoHandedAxe | northern_axe_t3 | 26.2 | False | Skirmishers | freefolk | 26.0 | main_or_minor_line |
| 234 | Pentoshi Horseman | pentoshi_horseman | 28.9 | 75.7 | OneHandedSword | pentoshi_sword | 45.8 | True | Defensive Troops | pentoshi | 21.0 | main_or_minor_line |
| 235 | Yronwood Horseman | yronwood_horseman | 28.8 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 48.8 | True | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 236 | Celtigar Horseman | celtigar_horseman | 28.7 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 48.1 | True | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 237 | Dreadfort PIkeman | dreadfort_pikeman | 28.7 | 70.1 | Mace | vlandia_mace_2_t4 | 36.4 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 238 | Greyjoy Rider | greyjoy_rider | 28.6 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 47.5 | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 239 | Qartheen Hoplite | qartheen_hoplite | 28.6 | 82.0 | TwoHandedPolearm | qarth_spear2 | 35.0 | False | Defensive Troops | qartheen | 21.0 | main_or_minor_line |
| 240 | Dayne Pikeman | dayne_veteran_pikeman | 28.6 | 70.1 | Mace | dayne_mace | 35.4 | False | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 241 | Martell Rider | martell_rider | 28.4 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 46.1 | True | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 242 | Myrish Master Crossbowman | myrish_master_crossbowman | 28.4 | 75.7 | OneHandedSword | empire_sword_4_t4 | 33.4 | False | Ranged Troops | myrish | 26.0 | main_or_minor_line |
| 243 | Royce Warrior | royce_warrior | 28.3 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 32.9 | False | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 244 | Stark Horseman | stark_horseman | 28.3 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 45.0 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 245 | Ibbenese Warrior | ibbenese_warrior | 28.2 | 82.0 | TwoHandedPolearm | ibb_spear | 32.4 | False | Defensive Troops | ibbenese | 21.0 | main_or_minor_line |
| 246 | Sarnori Cavalry | sarnor_cavalry | 28.2 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 44.5 | True | Defensive Troops | sarnor | 21.0 | main_or_minor_line |
| 247 | Baratheon Horseman | baratheon_horseman | 28.2 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 44.4 | True | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 248 | Dayne Horseman | dayne_horseman | 28.2 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 44.2 | True | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 249 | Grafton Rider | grafton_rider | 28.0 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 42.7 | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 250 | Dragonstone Rider | dragonstone_rider | 28.0 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 42.7 | True | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 251 | Vale Lancer | vale_lancer | 28.0 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 42.4 | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 252 | Vale Voulgier | vale_voulgier | 28.0 | 82.0 | TwoHandedPolearm | vlandia_polearm_1_t5 | 42.4 | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 253 | Bolton Horseman | bolton_horseman | 28.0 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 42.4 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 254 | Golden Steed Riders | golden_rider | 27.9 | 82.0 | TwoHandedPolearm | golden_company_spear | 42.1 | True | Defensive Troops | volantine | 21.0 | main_or_minor_line |
| 255 | Hightower Horseman | hightower_horseman | 27.9 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 41.8 | True | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 256 | Dondarrion Horseman | dondarion_horseman | 27.8 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 41.2 | True | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 257 | Norvoshi Cavalry | norvos_cavalry | 27.8 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 41.2 | True | Defensive Troops | norvos | 21.0 | main_or_minor_line |
| 258 | Yi Ti Rider | yiti_rider | 27.8 | 82.0 | TwoHandedPolearm | yiti_spear | 41.1 | True | Defensive Troops | yiti | 21.0 | main_or_minor_line |
| 259 | Vale Knight | vale_knight | 27.8 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 40.9 | True | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 260 | Harlaw Scout | harlaw_rider | 27.8 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 40.8 | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 261 | Myrish Horseman | myrish_horseman | 27.7 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 40.2 | True | Defensive Troops | myrish | 21.0 | main_or_minor_line |
| 262 | Tully Rider | tully_rider | 27.6 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 39.6 | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 263 | Bracken Rider | bracken_rider | 27.6 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 39.3 | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 264 | Riverlands Horseman | river_horseman | 27.6 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 39.1 | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 265 | Westerling Scout | westerling_rider | 27.5 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 39.0 | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 266 | Velaryon Scout | velaryon_scout | 27.5 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 38.5 | True | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 267 | Casterly Rock Master Crossbowman | casterly_master_crossbowman | 27.5 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 25.9 | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 268 | Gold Cloak Rider | goldcloak_rider | 27.5 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 38.3 | True | Defensive Troops | crownlands | 21.0 | main_or_minor_line |
| 269 | Blackwood Scout | blackwood_scout | 27.5 | 82.0 | TwoHandedPolearm | highland_spear_t2 | 38.3 | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 270 | Celtigar Veteran Archer | celtigar_veteran_archer | 27.4 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 25.8 | False | Ranged Troops | dragonstone | 26.0 | main_or_minor_line |
| 271 | Hightower Marksmen | hightower_marksman | 27.4 | 75.7 | OneHandedSword | velaryon_cutlass | 25.6 | False | Ranged Troops | reach | 26.0 | main_or_minor_line |
| 272 | Lyseni Horseman | lyseni_horseman | 27.4 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 37.9 | True | Defensive Troops | lyseni | 21.0 | main_or_minor_line |
| 273 | Tyroshi Horseman | tyroshi_horseman | 27.4 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 37.8 | True | Defensive Troops | tyroshi | 21.0 | main_or_minor_line |
| 274 | Gilded Bolt Rangers | golden_master_crossbowman | 27.4 | 75.7 | OneHandedSword | golden_company_sword | 25.1 | False | Ranged Troops | volantine | 26.0 | main_or_minor_line |
| 275 | Velaryon Marksman | velaryon_marksman | 27.3 | 75.7 | OneHandedSword | velaryon_cutlass | 24.9 | False | Ranged Troops | dragonstone | 26.0 | main_or_minor_line |
| 276 | Pentoshi Elite Archer | pentoshi_elite_archer | 27.3 | 75.7 | OneHandedSword | pentoshi_sword | 24.8 | False | Ranged Troops | pentoshi | 26.0 | main_or_minor_line |
| 277 | Mormont Scout | mormont_scout | 27.3 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 37.1 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 278 | Tarly Horseman | tarly_horseman | 27.3 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 37.0 | True | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 279 | Qartheen Cameleer | qartheen_cameleer | 27.3 | 82.0 | TwoHandedPolearm | qarth_spear2 | 36.7 | True | Defensive Troops | qartheen | 21.0 | main_or_minor_line |
| 280 | Blackwood Longbowman | blackwood_longbowman | 27.2 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 23.9 | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 281 | Frey Sharpshooter | frey_sharpshooter | 27.2 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 23.9 | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 282 | Mallister Horseman | mallister_rider | 27.2 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 36.3 | True | Defensive Troops | river | 21.0 | main_or_minor_line |
| 283 | Glover Rider | glover_rider | 27.2 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 36.1 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 284 | Ibbenese Rider | ibbenese_rider | 27.2 | 82.0 | TwoHandedPolearm | ibb_spear | 36.1 | True | Defensive Troops | ibbenese | 21.0 | main_or_minor_line |
| 285 | Reach Rider | reach_rider | 27.2 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 36.1 | True | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 286 | Volantene Rider | tigercloak_rider | 27.2 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 36.0 | True | Defensive Troops | volantine | 21.0 | main_or_minor_line |
| 287 | Tarly Elite Crossbowman | tarly_elite_crossbowman | 27.1 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 23.4 | False | Ranged Troops | reach | 26.0 | main_or_minor_line |
| 288 | Qohorik Elite Archer | qohorik_elite_archer | 27.1 | 75.7 | OneHandedSword | qohorik_sword | 23.3 | False | Ranged Troops | qohorik | 26.0 | main_or_minor_line |
| 289 | Cerwyn Scout | cerwyn_scout | 27.1 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 35.3 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 290 | Tarth Rider | tarth_rider | 26.9 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 34.0 | True | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 291 | Ghiscari Cavalry | ghiscari_cavalry | 26.9 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 33.9 | True | Defensive Troops | ghiscari | 21.0 | main_or_minor_line |
| 292 | Clegane Scout | clegane_scout | 26.8 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 33.0 | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 293 | Umber Scout | umber_scout | 26.8 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 32.9 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 294 | Summer Isles Scout | summer_rider | 26.6 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 31.6 | True | Defensive Troops | summer | 21.0 | main_or_minor_line |
| 295 | Tarth Elite Crossbowman | tarth_elite_crossbowman | 26.6 | 75.7 | OneHandedSword | velaryon_cutlass | 19.2 | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 296 | Tyrell Scout | tyrell_scout | 26.5 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 30.8 | True | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 297 | Riverlands Axeman | river_axeman | 26.3 | 73.3 | TwoHandedAxe | hooked_axe_t4 | 26.5 | False | Offensive Melee | river | 26.0 | main_or_minor_line |
| 298 | Qohorik Swordsman | qohorik_swordsman | 26.1 | 82.0 | TwoHandedPolearm | eastern_throwing_spear_1_t3 | 41.4 | False | Defensive Troops | qohorik | 21.0 | main_or_minor_line |
| 299 | Mormont Veteran Huntress | mormont_veteran_huntress | 26.1 | 73.3 | OneHandedAxe | sturgia_axe_4_t4 | 24.7 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 300 | Lannister Man at Arms | lannister_man_at_arms | 25.8 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 39.5 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 301 | Martell Spearman | martell_spearman | 25.8 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 39.4 | False | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 302 | Stormlands Elite Maceman | stormlands_crusher | 25.8 | 70.1 | Mace | empire_mace_4_t5 | 35.7 | False | Skirmishers | stormlands | 26.0 | main_or_minor_line |
| 303 | Valyrian Man at Arms | targaryen_man_at_arms | 25.6 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 35.0 | False | Defensive Troops | valyrian | 21.0 | main_or_minor_line |
| 304 | Dragonstone Halberdier | dragonstone_brute | 25.4 | 82.0 | TwoHandedPolearm | dragonstone_halberd | 36.2 | False | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 305 | Stark Soldier | stark_soldier | 25.4 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 35.9 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 306 | Skagosi Spearman | skag_spearman | 25.3 | 82.0 | TwoHandedPolearm | skagosi_spear | 34.9 | False | Defensive Troops | skagosi | 21.0 | main_or_minor_line |
| 307 | Tarth Soldier | tarth_soldier | 25.2 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 34.8 | False | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 308 | Reach Hedge Knight | reach_hedge_knight | 25.2 | 82.0 | TwoHandedPolearm | vlandia_polearm_1_t5 | 34.4 | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 309 | Yi Ti Spearman | yiti_spearman | 25.2 | 82.0 | TwoHandedPolearm | yiti_spear | 34.1 | False | Defensive Troops | yiti | 21.0 | main_or_minor_line |
| 310 | Kingsguard Initiate | kingsguard_initiate | 25.1 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 33.9 | False | Defensive Troops | crownlands | 21.0 | main_or_minor_line |
| 311 | Black Goat Warrior | qohorik_goat_warrior | 25.1 | 82.0 | TwoHandedPolearm | qohorik_spear | 33.7 | False | Skirmishers | qohorik | 21.0 | main_or_minor_line |
| 312 | Dayne Man at Arms | dayne_pikeman | 25.1 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 33.5 | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 313 | Ibbenese Sailor | ibbenese_sailor | 25.1 | 82.0 | TwoHandedPolearm | ibb_spear | 33.4 | False | Skirmishers | ibbenese | 21.0 | main_or_minor_line |
| 314 | Glover Man at Arms | glover_man_at_arms | 25.0 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 33.2 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 315 | Golden Company Aurum Spearbearers | golden_spearman | 25.0 | 82.0 | TwoHandedPolearm | golden_company_spear | 32.6 | False | Defensive Troops | volantine | 21.0 | main_or_minor_line |
| 316 | Qartheen Pureborn Warrior | qartheen_pureborn_warrior | 25.0 | 82.0 | TwoHandedPolearm | qarth_spear | 32.5 | False | Skirmishers | qartheen | 21.0 | main_or_minor_line |
| 317 | Night's Watch Master Ranger | nightswatch_master_ranger | 24.9 | 75.7 | OneHandedSword | broad_arming_sword_t4 | 29.4 | False | Ranged Troops | nightswatch | 26.0 | main_or_minor_line |
| 318 | Mormont Man at Arms | mormont_man_at_arms | 24.8 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 31.1 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 319 | Hightower Guard | hightower_guard | 24.7 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 30.7 | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 320 | Greyjoy Deckman | greyjoy_houseguard | 24.7 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 30.7 | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 321 | Ghiscari Pikeman | ghiscari_unsullied | 24.7 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 28.2 | False | Defensive Troops | ghiscari | 21.0 | main_or_minor_line |
| 322 | Tigercloak | tigercloak_elite | 24.7 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 30.1 | False | Ranged Troops | volantine | 21.0 | main_or_minor_line |
| 323 | Dondarrion Man at Arms | dondarion_man_at_arms | 24.6 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 30.1 | False | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 324 | Bolton Veteran | bolton_veteran | 24.6 | 82.0 | TwoHandedPolearm | bolton_spear | 30.0 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 325 | Glover Veteran Archer | glover_veteran_archer | 24.6 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 27.7 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 326 | Tully Longbowman | tully_longbowman | 24.5 | 75.7 | OneHandedSword | vlandia_sword_3_t4 | 26.7 | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 327 | Yi Ti Marksman | yiti_master_bowman | 24.5 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 26.6 | False | Ranged Troops | yiti | 26.0 | main_or_minor_line |
| 328 | Cerwyn Axeman | cerwyn_axeman | 24.4 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 28.5 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 329 | Umber Man at Arms | umber_man_at_arms | 24.4 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 28.2 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 330 | Norvoshi Bearded Priest | norvos_bearded_priest | 24.4 | 82.0 | TwoHandedPolearm | norvoshi_long_axe | 28.2 | False | Defensive Troops | norvos | 21.0 | main_or_minor_line |
| 331 | Baratheon Hammerman | baratheon_hammer | 24.4 | 82.0 | TwoHandedPolearm | spiked_polehammer | 28.1 | False | Offensive Melee | stormlands | 21.0 | main_or_minor_line |
| 332 | Riverlands Ranger | river_ranger | 24.4 | 75.7 | OneHandedSword | vlandia_sword_3_t4 | 25.8 | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 333 | Clegane Man at Arms | clegane_man_at_arms | 24.4 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 28.0 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 334 | Tyrell Elite Longbowman | tyrell_longbowman | 24.4 | 75.7 | OneHandedSword | vlandia_sword_3_t4 | 25.6 | False | Ranged Troops | reach | 26.0 | main_or_minor_line |
| 335 | Qartheen Longbowman | qartheen_longbowman | 24.3 | 75.7 | OneHandedSword | qarth_sword | 25.4 | False | Ranged Troops | qartheen | 26.0 | main_or_minor_line |
| 336 | Myrish Elite Archer | myrish_elite_archer | 24.3 | 75.7 | OneHandedSword | empire_sword_2_t3 | 25.1 | False | Ranged Troops | myrish | 26.0 | main_or_minor_line |
| 337 | Valyrian Master Archer | targaryen_master_archer | 24.2 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 24.6 | False | Ranged Troops | valyrian | 26.0 | main_or_minor_line |
| 338 | Skagosi Huntsman | skag_huntsman | 24.2 | 75.7 | OneHandedSword | skagosi_sword | 24.3 | False | Ranged Troops | skagosi | 26.0 | main_or_minor_line |
| 339 | Sarnori Spearman | sarnor_spearman | 24.2 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 26.5 | False | Defensive Troops | sarnor | 21.0 | main_or_minor_line |
| 340 | Sarnori Glaiveman | sarnor_glaiveman | 24.2 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 26.5 | False | Defensive Troops | sarnor | 21.0 | main_or_minor_line |
| 341 | Yronwood Veteran Archer | yronwood_veteran_archer | 24.2 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 24.1 | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 342 | Bracken Elite Archer | bracken_elite_archer | 24.1 | 75.7 | OneHandedSword | sturgia_sword_3_t3 | 23.8 | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 343 | Free Folk Spearman | freefolk_spearman | 24.1 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 26.0 | False | Skirmishers | freefolk | 21.0 | main_or_minor_line |
| 344 | Karstark Spearman | karstark_ruffian | 24.1 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 25.7 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 345 | Harlaw Seaman | harlaw_seaman | 24.0 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 25.3 | False | Offensive Melee | sturgia | 21.0 | main_or_minor_line |
| 346 | Summer Isles Spearman | summer_spearman | 24.0 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 24.8 | False | Defensive Troops | summer | 21.0 | main_or_minor_line |
| 347 | Norvoshi Spearman | norvos_spearman | 23.9 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 24.5 | False | Defensive Troops | norvos | 21.0 | main_or_minor_line |
| 348 | Royce Veteran Archer | royce_veteran_archer | 23.9 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 21.8 | False | Ranged Troops | vale | 26.0 | main_or_minor_line |
| 349 | Manderly Veteran Archer | manderly_veteran_archer | 23.9 | 75.7 | OneHandedSword | manderly_sword | 21.8 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 350 | Mallister Elite Archer | mallister_elite_archer | 23.9 | 75.7 | OneHandedSword | sturgia_sword_3_t3 | 21.6 | False | Ranged Troops | river | 26.0 | main_or_minor_line |
| 351 | Summer Isles Longbowman | summer_longbowman | 23.8 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 21.2 | False | Ranged Troops | summer | 26.0 | main_or_minor_line |
| 352 | Cerwyn Veteran Archer | cerwyn_veteran_archer | 23.8 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 21.2 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 353 | Ibbenese Master Huntsman | ibbenese_master_huntsman | 23.8 | 75.7 | OneHandedSword | ibb_sword | 21.1 | False | Ranged Troops | ibbenese | 26.0 | main_or_minor_line |
| 354 | Sarnori Longbowman | sarnor_longbowman | 23.8 | 75.7 | OneHandedSword | kopesh_sword | 20.8 | False | Ranged Troops | sarnor | 26.0 | main_or_minor_line |
| 355 | Dayne Veteran Archer | dayne_veteran_archer | 23.6 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 19.8 | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 356 | Sarnori Elite Javelinier | sarnor_elite_javelinier | 23.6 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 22.1 | False | Skirmishers | sarnor | 21.0 | main_or_minor_line |
| 357 | Pentoshi Pike Warrior | pentoshi_pike_warrior | 23.2 | 75.7 | OneHandedSword | pentoshi_sword | 40.8 | False | Defensive Troops | pentoshi | 21.0 | main_or_minor_line |
| 358 | Volantene Master Archer | tigercloak_master_archer | 22.8 | 73.3 | OneHandedAxe | bamboo_axe_t4 | 22.5 | False | Ranged Troops | volantine | 26.0 | main_or_minor_line |
| 359 | Yronwood Pikeman | yronwood_pikeman | 22.8 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 37.4 | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 360 | Karstark Elite Archer | karstark_elite_archer | 22.8 | 73.3 | OneHandedAxe | battania_axe_2_t4 | 22.3 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 361 | Tyroshi Elite Archer | tyroshi_elite_archer | 22.6 | 73.3 | OneHandedAxe | tyroshi_axe | 20.9 | False | Ranged Troops | tyroshi | 26.0 | main_or_minor_line |
| 362 | Lyseni Elite Archer | lyseni_elite_archer | 22.6 | 73.3 | OneHandedAxe | small_bit_axe_t2 | 20.5 | False | Ranged Troops | lyseni | 26.0 | main_or_minor_line |
| 363 | Norvoshi Master Archer | norvos_master_archer | 22.5 | 73.3 | OneHandedAxe | tzkurion_axe_t3 | 20.3 | False | Ranged Troops | norvos | 26.0 | main_or_minor_line |
| 364 | Skagosi Savage | skag_savage | 22.5 | 75.7 | OneHandedSword | skagosi_sword | 34.9 | False | Defensive Troops | skagosi | 21.0 | main_or_minor_line |
| 365 | Freefolk Thenn Warrior | freefolk_thenn_warrior | 22.5 | 75.7 | OneHandedSword | thenn_sword2 | 34.7 | False | Defensive Troops | freefolk | 21.0 | main_or_minor_line |
| 366 | Westerling Man at Arms | westerling_man_at_arms | 22.3 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 38.0 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 367 | Grafton Man at Arms | grafton_man_at_arms | 22.3 | 82.0 | TwoHandedPolearm | grafton_spear | 37.9 | False | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 368 | Tyrell Man at Arms | tyrell_man_at_arms | 22.3 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 37.6 | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 369 | Mallister Man at Arms | mallister_man_at_arms | 22.3 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 37.6 | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 370 | Dragonstone Man at Arms | dragonstone_man_at_arms | 22.1 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 36.2 | False | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 371 | Realm Hedge Knight | realm_hedge_knight | 22.0 | 82.0 | TwoHandedPolearm | baratheon_spear | 35.5 | False | Defensive Troops | crownlands | 21.0 | main_or_minor_line |
| 372 | Stormlands Spearman | stormlands_spearman | 22.0 | 82.0 | TwoHandedPolearm | vlandia_lance_3_t5 | 35.3 | False | Defensive Troops | stormlands | 21.0 | main_or_minor_line |
| 373 | Qohorik Spearman | qohorik_spearman | 21.9 | 82.0 | TwoHandedPolearm | eastern_throwing_spear_1_t3 | 34.5 | False | Defensive Troops | qohorik | 21.0 | main_or_minor_line |
| 374 | Celtigar Man at Arms | celtigar_man_at_arms | 21.9 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 34.4 | False | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 375 | Pentoshi Man at Arms | pentoshi_man_at_arms | 21.8 | 82.0 | TwoHandedPolearm | pentoshi_spear | 34.0 | False | Defensive Troops | pentoshi | 21.0 | main_or_minor_line |
| 376 | Manderly Man at Arms | manderly_man_at_arms | 21.8 | 82.0 | TwoHandedPolearm | manderly_spear | 33.9 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 377 | Velaryon Marine | velaryon_warrior | 21.8 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 33.6 | False | Defensive Troops | dragonstone | 21.0 | main_or_minor_line |
| 378 | Bracken Man at Arms | bracken_man_at_arms | 21.8 | 82.0 | TwoHandedPolearm | northern_spear_3_t4 | 33.6 | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 379 | Greyjoy Marksman | greyjoy_marksman | 21.8 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 29.1 | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 380 | Tully Man at Arms | tully_man_at_arms | 21.7 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 33.1 | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 381 | Blackwood Man at Arms | blackwood_man_at_arms | 21.7 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 33.0 | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 382 | Vale Man at Arms | vale_man_at_arms | 21.6 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 32.5 | False | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 383 | Riverlands Man at Arms | river_man_at_arms | 21.6 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 32.4 | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 384 | Gold Cloak Petty Officer | goldcloak_officer | 21.6 | 75.7 | OneHandedSword | vlandia_sword_3_t4 | 27.7 | False | Defensive Troops | crownlands | 21.0 | main_or_minor_line |
| 385 | Tyroshi Quartermaster | tyroshi_quartermaster | 21.6 | 73.3 | OneHandedAxe | tyroshi_axe2 | 36.0 | False | Skirmishers | tyroshi | 21.0 | main_or_minor_line |
| 386 | Frey Man at Arms | frey_man_at_arms | 21.5 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 27.3 | False | Defensive Troops | river | 21.0 | main_or_minor_line |
| 387 | Myrish Warrior | myrish_warrior | 21.5 | 82.0 | TwoHandedPolearm | western_spear_5_t4 | 31.5 | False | Defensive Troops | myrish | 21.0 | main_or_minor_line |
| 388 | Lyseni Warrior | lyseni_warrior | 21.4 | 82.0 | TwoHandedPolearm | lyseni_spear | 31.0 | False | Defensive Troops | lyseni | 21.0 | main_or_minor_line |
| 389 | Westerling Elite Archer | westerling_elite_archer | 21.4 | 70.1 | Mace | westerling_mace | 23.3 | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 390 | Grafton Elite Archer | grafton_elite_crossbowman | 21.3 | 70.1 | Mace | westerling_mace | 22.7 | False | Ranged Troops | vale | 26.0 | main_or_minor_line |
| 391 | Stark Master Longbowman | stark_master_archer | 21.2 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 22.1 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 392 | Arryn Man at Arms | arryn_man_at_arms | 21.2 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 28.9 | False | Defensive Troops | vale | 21.0 | main_or_minor_line |
| 393 | Harlaw Longbowman | harlaw_longbowman | 21.2 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 24.5 | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 394 | Tarly Man at Arms | tarly_man_at_arms | 21.1 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 28.5 | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 395 | Martell Veteran Archer | martell_veteran_archer | 21.1 | 75.7 | OneHandedSword | martell_sword | 24.2 | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 396 | Volantene Warrior | tigercloak_warrior | 21.0 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 27.7 | False | Defensive Troops | volantine | 21.0 | main_or_minor_line |
| 397 | Lyseni Axeman | lyseni_axeman | 21.0 | 73.3 | OneHandedAxe | imperial_axe_t3 | 31.4 | False | Defensive Troops | lyseni | 21.0 | main_or_minor_line |
| 398 | Gold Cloak Sniper | goldcloak_master_archer | 20.9 | 75.7 | OneHandedSword | narrow_sword_t3 | 22.2 | False | Ranged Troops | crownlands | 26.0 | main_or_minor_line |
| 399 | Reach Man at Arms | reach_hacker | 20.8 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 26.1 | False | Defensive Troops | reach | 21.0 | main_or_minor_line |
| 400 | Clegane Elite Archer | clegane_elite_archer | 20.7 | 75.7 | OneHandedSword | short_sword_t3 | 21.0 | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 401 | Tyroshi Axeman | tyroshi_axeman | 20.7 | 73.3 | TwoHandedAxe | avalanche_2haxe | 29.1 | False | Offensive Melee | tyroshi | 21.0 | main_or_minor_line |
| 402 | Free Folk Hawkeye | freefolk_hawkeye | 20.6 | 75.7 | OneHandedSword | wildling_knife | 20.1 | False | Ranged Troops | freefolk | 26.0 | main_or_minor_line |
| 403 | Reach Master Archer | reach_master_archer | 20.6 | 75.7 | OneHandedSword | vlandia_sword_3_t4 | 19.9 | False | Ranged Troops | reach | 26.0 | main_or_minor_line |
| 404 | Casterly Rock Pikeman | casterly_marshal | 20.5 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 43.5 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 405 | Casterly Rock Squire | casterly_squire | 20.5 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 35.3 | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 406 | Night's Watch Defender | nightswatch_defender | 20.3 | 82.0 | TwoHandedPolearm | western_spear_2_t2 | 22.0 | False | Defensive Troops | nightswatch | 21.0 | main_or_minor_line |
| 407 | Lannister Longbowman | lannister_longbowman | 20.3 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 17.6 | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 408 | White Harbor Squire | whiteharbor_squire | 20.3 | 82.0 | TwoHandedPolearm | trident | 34.0 | True | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 409 | Night's Watch Master Crossbowman | nightswatch_master_crossbowman | 20.3 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 17.3 | False | Ranged Troops | nightswatch | 26.0 | main_or_minor_line |
| 410 | Ghiscari Mounted Archer | ghiscari_mounted_archer | 20.2 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 25.3 | True | Ranged Troops | ghiscari | 21.0 | main_or_minor_line |
| 411 | Umber Marksman | umber_marksman | 20.2 | 73.3 | OneHandedAxe | woodland_axe_t3 | 25.3 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 412 | Norvoshi Axeman | norvos_axeman | 20.1 | 73.3 | OneHandedAxe | tzkurion_axe_t3 | 24.1 | False | Defensive Troops | norvos | 21.0 | main_or_minor_line |
| 413 | Bolton Hunter | bolton_master_archer | 20.0 | 73.3 | OneHandedAxe | battania_axe_2_t4 | 24.0 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 414 | Arryn Rider | arryn_rider | 19.8 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 30.0 | True | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 415 | Free Folk Berzerker | freefolk_berzerker | 19.5 | 73.3 | TwoHandedAxe | northern_axe_t3 | 20.1 | False | Skirmishers | freefolk | 21.0 | main_or_minor_line |
| 416 | Cursed Wight | cursed_wight | 19.3 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 13.2 | False | Offensive Melee | whitewalker | 21.0 | main_or_minor_line |
| 417 | Ghiscari Soldier | ghiscari_soldier | 18.6 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 28.6 | False | Skirmishers | ghiscari | 21.0 | main_or_minor_line |
| 418 | Dexterous Wight | dexterous_wight | 18.4 | 73.3 | OneHandedAxe | woodland_axe_t3 | 11.0 | False | Ranged Troops | whitewalker | 26.0 | main_or_minor_line |
| 419 | Myrish Elite Crossbowman | myrish_elite_crossbowman | 18.4 | 75.7 | OneHandedSword | empire_sword_4_t4 | 26.6 | False | Ranged Troops | myrish | 21.0 | main_or_minor_line |
| 420 | Casterly Rock Crossbowman | casterly_crossbowman | 18.3 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 25.9 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 421 | Yi Ti Archer | yiti_veteran_bowman | 18.2 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 24.8 | False | Ranged Troops | yiti | 21.0 | main_or_minor_line |
| 422 | Hightower Crossbowman | hightower_crossbowman | 18.1 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 24.4 | False | Ranged Troops | reach | 21.0 | main_or_minor_line |
| 423 | Gleaming Shaft Marksmen | golden_veteran_crossbowman | 17.9 | 75.7 | OneHandedSword | golden_company_sword | 23.2 | False | Ranged Troops | volantine | 21.0 | main_or_minor_line |
| 424 | Free Folk Shieldman | freefolk_shieldman | 17.9 | 73.3 | OneHandedAxe | wildling_axe | 30.1 | False | Defensive Troops | freefolk | 21.0 | main_or_minor_line |
| 425 | Dragonstone Elite Archer | dragonstone_elite_archer | 17.8 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 21.7 | False | Ranged Troops | dragonstone | 26.0 | main_or_minor_line |
| 426 | Celtigar Archer | celtigar_archer | 17.6 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 20.1 | False | Ranged Troops | dragonstone | 21.0 | main_or_minor_line |
| 427 | Qohorik Rider | qohorik_rider | 17.6 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3 | 38.5 | True | Defensive Troops | qohorik | 16.0 | main_or_minor_line |
| 428 | Frey Veteran Crossbowman | frey_veteran_crossbowman | 17.5 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 19.4 | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 429 | Valyrian Squire | valyrian_squire | 17.4 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 25.0 | False | Defensive Troops | valyrian | 16.0 | main_or_minor_line |
| 430 | Tarly Crossbowman | tarly_crossbowman | 17.3 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 18.1 | False | Ranged Troops | reach | 21.0 | main_or_minor_line |
| 431 | Qartheen Camel Rider | qartheen_camel_rider | 17.3 | 82.0 | TwoHandedPolearm | qarth_spear2 | 36.4 | True | Defensive Troops | qartheen | 16.0 | main_or_minor_line |
| 432 | Tarth Crossbowman | tarth_crossbowman | 17.3 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 17.8 | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 433 | Velaryon Crossbowman | velaryon_crossbowman | 17.2 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 17.5 | False | Ranged Troops | dragonstone | 21.0 | main_or_minor_line |
| 434 | Stormlands Maceman | stormlands_basher | 17.2 | 70.1 | Mace | morningstar_mace_t3 | 35.3 | False | Skirmishers | stormlands | 21.0 | main_or_minor_line |
| 435 | Mormont Huntress | mormont_huntress | 17.2 | 73.3 | OneHandedAxe | sturgia_axe_4_t4 | 24.7 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 436 | Tyrell Longbowman | tyrell_bowman | 17.1 | 75.7 | OneHandedSword | narrow_sword_t3 | 16.2 | False | Ranged Troops | reach | 21.0 | main_or_minor_line |
| 437 | Targaryen Squire | targ_squire | 16.9 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 21.4 | False | Defensive Troops | valyrian | 16.0 | main_or_minor_line |
| 438 | Summer Isles Archer | summer_veteran_bowman | 16.9 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 15.1 | False | Ranged Troops | summer | 21.0 | main_or_minor_line |
| 439 | Norvoshi Horseman | norvos_horseman | 16.7 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 32.1 | True | Defensive Troops | norvos | 16.0 | main_or_minor_line |
| 440 | Skagosi Archer | skag_archer | 16.6 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 19.9 | False | Ranged Troops | skagosi | 21.0 | main_or_minor_line |
| 441 | Sarnori Horseman | sarnor_horseman | 16.1 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 27.3 | True | Defensive Troops | sarnor | 16.0 | main_or_minor_line |
| 442 | Stormlands Heavy Crossbowman | stormlands_heavy_crossbowman | 16.1 | 70.1 | Mace | morningstar_mace_t3 | 26.3 | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 443 | Freefolk Thenn | freefolk_thenn | 15.4 | 75.7 | OneHandedSword | thenn_sword2 | 27.5 | False | Defensive Troops | freefolk | 16.0 | main_or_minor_line |
| 444 | Riverlands Swordsman | river_swordsman | 15.2 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 19.6 | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 445 | Valyrian Soldier | targaryen_soldier | 15.1 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 33.3 | False | Defensive Troops | valyrian | 16.0 | main_or_minor_line |
| 446 | Valyrian Archer | targaryen_archer | 15.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 24.6 | False | Ranged Troops | valyrian | 21.0 | main_or_minor_line |
| 447 | Ghiscari Horseman | ghiscari_horseman | 15.1 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 32.7 | True | Defensive Troops | ghiscari | 16.0 | main_or_minor_line |
| 448 | Vale Rider | vale_rider | 15.0 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 32.0 | True | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 449 | Pentoshi Archer | pentoshi_archer | 14.9 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 23.6 | False | Ranged Troops | pentoshi | 21.0 | main_or_minor_line |
| 450 | Ghiscari Warrior | ghiscari_warrior | 14.9 | 100.0 | TwoHandedSword | ghiscari_sword | 17.5 | False | Offensive Melee | ghiscari | 16.0 | main_or_minor_line |
| 451 | Yronwood Archer | yronwood_archer | 14.8 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 22.9 | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 452 | Lannister Footman | lannister_footman | 14.7 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 30.1 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 453 | Casterly Rock Soldier | casterly_soldier | 14.7 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 29.8 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 454 | Hightower Soldier | hightower_soldier | 14.6 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 29.5 | False | Defensive Troops | reach | 16.0 | main_or_minor_line |
| 455 | Karstark Archer | karstark_archer | 14.6 | 75.7 | OneHandedSword | narrow_sword_t3 | 21.1 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 456 | Gold Cloak Elite Archer | goldcloak_elite_archer | 14.6 | 75.7 | OneHandedSword | short_sword_t3 | 20.9 | False | Ranged Troops | crownlands | 21.0 | main_or_minor_line |
| 457 | Skagosi Soldier | skag_soldier | 14.6 | 82.0 | TwoHandedPolearm | skagosi_spear | 29.1 | False | Defensive Troops | skagosi | 16.0 | main_or_minor_line |
| 458 | Ibbenese Hunter | ibbenese_hunter | 14.6 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 20.8 | False | Ranged Troops | ibbenese | 21.0 | main_or_minor_line |
| 459 | Yronwood Man at Arms | yronwood_man_at_arms | 14.6 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 28.9 | False | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 460 | Night's Watch Elite Ranger | nightswatch_elite_ranger | 14.6 | 75.7 | OneHandedSword | broad_arming_sword_t4 | 20.6 | False | Ranged Troops | nightswatch | 21.0 | main_or_minor_line |
| 461 | Qarthene Veteran Archer | qartheen_elite_archer | 14.5 | 75.7 | OneHandedSword | empire_sword_1_t2 | 20.5 | False | Ranged Troops | qartheen | 21.0 | main_or_minor_line |
| 462 | Martell Archer | martell_archer | 14.5 | 75.7 | OneHandedSword | aserai_sword_2_t2 | 20.4 | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 463 | Cerwyn Archer | cerwyn_archer | 14.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 20.0 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 464 | Clegane Archer | clegane_archer | 14.4 | 75.7 | OneHandedSword | short_sword_t3 | 19.7 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 465 | Free Folk Sharpshooter | freefolk_sharpshooter | 14.4 | 75.7 | OneHandedSword | wildling_knife | 19.5 | False | Ranged Troops | freefolk | 21.0 | main_or_minor_line |
| 466 | Blackwood Archer | blackwood_archer | 14.4 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 19.5 | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 467 | Bracken Archer | bracken_archer | 14.4 | 75.7 | OneHandedSword | sturgia_sword_3_t3 | 19.3 | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 468 | Norvoshi Elite Archer | norvos_elite_archer | 14.4 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 19.2 | False | Ranged Troops | norvos | 21.0 | main_or_minor_line |
| 469 | Stormlands Squire | stormlands_squire | 14.4 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 13.2 | False | Offensive Melee | stormlands | 16.0 | main_or_minor_line |
| 470 | Cerwyn Soldier | cerwyn_soldier | 14.4 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 27.3 | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 471 | Tully Soldier | tully_soldier | 14.4 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 27.3 | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 472 | Riverlands Soldier | river_soldier | 14.3 | 82.0 | TwoHandedPolearm | wide_leaf_spear_t4 | 27.0 | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 473 | Bracken Footman | bracken_footman | 14.3 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 27.0 | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 474 | Dayne Archer | dayne_archer | 14.3 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 18.6 | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 475 | Ghiscari Elite Archer | ghiscari_elite_archer | 14.3 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 18.6 | False | Ranged Troops | ghiscari | 21.0 | main_or_minor_line |
| 476 | Westerling Footman | westerling_footman | 14.3 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 26.7 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 477 | Grafton Footman | grafton_footman | 14.3 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 26.7 | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 478 | Stark Footman | stark_footman | 14.2 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 26.4 | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 479 | Harlaw Archer | harlaw_archer | 14.2 | 75.7 | OneHandedSword | short_sword_t3 | 17.9 | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 480 | Blackwood Footman | blackwood_footman | 14.2 | 82.0 | TwoHandedPolearm | highland_spear_t2 | 26.0 | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 481 | Lannister Archer | lannister_archer | 14.2 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 17.6 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 482 | Mallister Archer | mallister_archer | 14.2 | 75.7 | OneHandedSword | sturgia_sword_3_t3 | 17.5 | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 483 | Greyjoy Archer | greyjoy_archer | 14.1 | 75.7 | OneHandedSword | short_sword_t3 | 17.2 | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 484 | Manderly Archer | manderly_archer | 14.0 | 75.7 | OneHandedSword | manderly_sword | 16.2 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 485 | Royce Archer | royce_archer | 14.0 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 16.1 | False | Ranged Troops | vale | 21.0 | main_or_minor_line |
| 486 | Stark Longbowman | stark_archer | 14.0 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 16.1 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 487 | Glover Archer | glover_archer | 14.0 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 16.1 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 488 | Qohorik Archer | qohorik_archer | 14.0 | 75.7 | OneHandedSword | qohorik_sword | 16.0 | False | Ranged Troops | qohorik | 21.0 | main_or_minor_line |
| 489 | Mallister Footman | mallister_footman | 13.9 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 23.9 | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 490 | Royce Soldier | royce_soldier | 13.9 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 23.8 | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 491 | Golden Company Giltblade Warriors | golden_infantryman | 13.9 | 82.0 | TwoHandedPolearm | golden_company_spear | 23.5 | False | Defensive Troops | volantine | 16.0 | main_or_minor_line |
| 492 | Reach Elite Archer | reach_elite_archer | 13.8 | 75.7 | OneHandedSword | short_sword_t3 | 15.0 | False | Ranged Troops | reach | 21.0 | main_or_minor_line |
| 493 | Greyjoy Soldier | greyjoy_soldier | 13.8 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 23.2 | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 494 | Stormlands Man at Arms | stormlands_man_at_arms | 13.8 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 23.1 | False | Defensive Troops | stormlands | 16.0 | main_or_minor_line |
| 495 | Dayne Footman | dayne_man_at_arms | 13.8 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 23.1 | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 496 | Sarnori Elite Archer | sarnor_elite_archer | 13.8 | 75.7 | OneHandedSword | kopesh_sword | 14.4 | False | Ranged Troops | sarnor | 21.0 | main_or_minor_line |
| 497 | Dondarrion Footman | dondarion_footman | 13.8 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 22.6 | False | Defensive Troops | stormlands | 16.0 | main_or_minor_line |
| 498 | Night's Watch Shieldbrother | nightswatch_shieldbrother | 13.7 | 82.0 | TwoHandedPolearm | western_spear_2_t2 | 21.8 | False | Defensive Troops | nightswatch | 16.0 | main_or_minor_line |
| 499 | Umber Archer | umber_archer | 13.6 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 19.9 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 500 | Tarth Man at Arms | tarth_man_at_arms | 13.6 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 21.2 | False | Defensive Troops | stormlands | 16.0 | main_or_minor_line |
| 501 | Baratheon Soldier | baratheon_soldier | 13.6 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 21.1 | False | Defensive Troops | stormlands | 16.0 | main_or_minor_line |
| 502 | Bolton Veteran Archer | bolton_elite_archer | 13.5 | 73.3 | OneHandedAxe | battania_axe_2_t4 | 18.8 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 503 | Norvoshi Acolyte | norvos_acolyte | 13.4 | 82.0 | TwoHandedPolearm | norvoshi_long_axe | 19.9 | False | Offensive Melee | norvos | 16.0 | main_or_minor_line |
| 504 | Black Goat Initiate | qohorik_goat_initiate | 13.4 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3 | 19.8 | False | Skirmishers | qohorik | 16.0 | main_or_minor_line |
| 505 | Glover Footman | glover_footman | 13.4 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 19.5 | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 506 | Sarnori Warrior | sarnor_warrior | 13.4 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 19.5 | False | Defensive Troops | sarnor | 16.0 | main_or_minor_line |
| 507 | Mormont Footman | mormont_footman | 13.4 | 82.0 | TwoHandedPolearm | northern_spear_1_t2 | 19.4 | False | Offensive Melee | battania | 16.0 | main_or_minor_line |
| 508 | Summer Isles Infantryman | summer_infantryman | 13.3 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 19.1 | False | Defensive Troops | summer | 16.0 | main_or_minor_line |
| 509 | Stormlands Master Archer | stormlands_master_archer | 13.2 | 70.1 | Mace | battania_mace_1_t2 | 26.3 | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 510 | Kingsguard's Squire | kingsguard_squire | 13.1 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 17.4 | False | Defensive Troops | crownlands | 16.0 | main_or_minor_line |
| 511 | Harlaw Footman | harlaw_footman | 13.0 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 16.7 | False | Offensive Melee | sturgia | 16.0 | main_or_minor_line |
| 512 | Sarnori Javelineer | sarnor_javelinier | 12.9 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 15.5 | False | Skirmishers | sarnor | 16.0 | main_or_minor_line |
| 513 | Reach Voulgier | reach_hookman | 12.8 | 82.0 | TwoHandedPolearm | vlandia_polearm_1_t5 | 15.0 | False | Ranged Troops | reach | 16.0 | main_or_minor_line |
| 514 | Dondarrion Veteran Bowman | dondarion_veteran_bowman | 12.6 | 70.1 | Mace | battania_mace_1_t2 | 21.0 | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 515 | Baratheon Longbowman | baratheon_longbowman | 12.5 | 70.1 | Mace | battania_mace_1_t2 | 20.6 | False | Ranged Troops | stormlands | 26.0 | main_or_minor_line |
| 516 | Westerling Archer | westerling_archer | 12.3 | 70.1 | Mace | westerling_mace | 19.0 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 517 | Grafton Archer | grafton_crossbowman | 12.3 | 70.1 | Mace | westerling_mace | 19.0 | False | Ranged Troops | vale | 21.0 | main_or_minor_line |
| 518 | Frey Cutthroat | frey_cutthroat | 12.2 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 25.9 | False | Defensive Troops | river | 16.0 | main_or_minor_line |
| 519 | Scorned Wight | scorned_wight | 12.1 | 82.0 | Mace|OneHandedAxe|TwoHandedPolearm | northern_spear_1_t2|sturgia_axe_2_t2|vlandia_mace_1_t2 | 9.6 | False | Offensive Melee | whitewalker | 16.0 | main_or_minor_line |
| 520 | Manderly Footman | whiteharbor_footman | 12.1 | 75.7 | OneHandedSword | manderly_sword | 25.5 | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 521 | Pentoshi Pikeman | pentoshi_pikeman | 12.1 | 75.7 | OneHandedSword | pentoshi_sword | 25.1 | False | Offensive Melee | pentoshi | 16.0 | main_or_minor_line |
| 522 | Martell Footman | martell_footman | 11.9 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 24.1 | False | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 523 | Bolton Footman | bolton_scout | 11.9 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 24.0 | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 524 | Squire | dragonstone_squire | 11.6 | 75.7 | OneHandedSword | vlandia_sword_4_t4 | 21.1 | False | Skirmishers | dragonstone | 16.0 | main_or_minor_line |
| 525 | Arryn Master Archer | arryn_master_archer | 11.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 20.6 | False | Ranged Troops | vale | 26.0 | main_or_minor_line |
| 526 | Volantene Archer | tigercloak_archer | 11.5 | 70.1 | Mace | aserai_mace_2_t2 | 12.5 | False | Ranged Troops | volantine | 21.0 | main_or_minor_line |
| 527 | Vale Soldier | vale_soldier | 11.4 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 30.0 | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 528 | Qartheen Soldier | qartheen_warrior | 11.4 | 82.0 | TwoHandedPolearm | qarth_spear2 | 29.7 | False | Defensive Troops | qartheen | 16.0 | main_or_minor_line |
| 529 | Ibbenese Rower | ibbenese_rower | 11.4 | 82.0 | TwoHandedPolearm | ibb_spear | 29.7 | False | Defensive Troops | ibbenese | 16.0 | main_or_minor_line |
| 530 | Ibbenese Tracker | ibbenese_tracker | 11.4 | 82.0 | TwoHandedPolearm | ibb_spear | 29.7 | False | Defensive Troops | ibbenese | 16.0 | main_or_minor_line |
| 531 | Tully Archer | tully_archer | 11.3 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 19.3 | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 532 | Dragonstone Soldier | dragonstone_soldier | 11.3 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 29.1 | False | Defensive Troops | dragonstone | 16.0 | main_or_minor_line |
| 533 | Qartheen Pureborn Fighter | qartheen_pureborn | 11.3 | 82.0 | TwoHandedPolearm | qarth_spear | 28.9 | False | Defensive Troops | qartheen | 16.0 | main_or_minor_line |
| 534 | Clegane Footman | clegane_footman | 11.3 | 73.3 | OneHandedAxe | woodland_axe_t3 | 24.7 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 535 | Celtigar Footman | celtigar_footman | 11.2 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 28.8 | False | Defensive Troops | dragonstone | 16.0 | main_or_minor_line |
| 536 | Umber Footman | umber_footman | 11.2 | 73.3 | OneHandedAxe | woodland_axe_t3 | 24.6 | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 537 | Qohorik Soldier | qohorik_soldier | 11.0 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3 | 26.7 | False | Defensive Troops | qohorik | 16.0 | main_or_minor_line |
| 538 | Volantene Soldier | volantine_soldier | 10.9 | 82.0 | TwoHandedPolearm | southern_spear_3_t3 | 26.4 | False | Defensive Troops | volantine | 16.0 | main_or_minor_line |
| 539 | Norvoshi Soldier | norvos_soldier | 10.9 | 73.3 | OneHandedAxe | tzkurion_axe_t3 | 22.2 | False | Defensive Troops | norvos | 16.0 | main_or_minor_line |
| 540 | Vale Master Archer | vale_master_archer | 10.9 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 15.7 | False | Ranged Troops | vale | 26.0 | main_or_minor_line |
| 541 | Free Folk Axeman | freefolk_axeman | 10.9 | 73.3 | OneHandedAxe | wildling_axe | 21.8 | False | Defensive Troops | freefolk | 16.0 | main_or_minor_line |
| 542 | Arryn Archer | arryn_archer | 10.8 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 15.4 | False | Ranged Troops | vale | 21.0 | main_or_minor_line |
| 543 | Gold Cloak Soldier | goldcloak_soldier | 10.8 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 25.1 | False | Defensive Troops | crownlands | 16.0 | main_or_minor_line |
| 544 | Tyroshi Soldier | tyroshi_soldier | 10.8 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 25.0 | False | Defensive Troops | tyroshi | 16.0 | main_or_minor_line |
| 545 | Velaryon Sailor | velaryon_soldier | 10.8 | 82.0 | TwoHandedPolearm | empire_lance_1_t3 | 24.9 | False | Defensive Troops | dragonstone | 16.0 | main_or_minor_line |
| 546 | Tyroshi Boatswain | tyroshi_boatswain | 10.7 | 73.3 | OneHandedAxe | tyroshi_axe2 | 20.7 | False | Skirmishers | tyroshi | 16.0 | main_or_minor_line |
| 547 | Night's Watch Elite Crossbowman | nightswatch_elite_crossbowman | 10.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 14.2 | False | Ranged Troops | nightswatch | 21.0 | main_or_minor_line |
| 548 | Lyseni Axe Apprentice | lyseni_axe_apprentice | 10.6 | 73.3 | OneHandedAxe | imperial_axe_t3 | 19.9 | False | Defensive Troops | lyseni | 16.0 | main_or_minor_line |
| 549 | Myrish Archer | myrish_archer | 10.6 | 75.7 | OneHandedSword | empire_sword_2_t3 | 13.8 | False | Ranged Troops | myrish | 21.0 | main_or_minor_line |
| 550 | Mormont Trapper | mormont_trapper | 10.6 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 19.4 | False | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 551 | Lyseni Archer | lyseni_archer | 10.6 | 73.3 | OneHandedAxe | small_bit_axe_t2 | 19.3 | False | Ranged Troops | lyseni | 21.0 | main_or_minor_line |
| 552 | Dragonstone Archer | dragonstone_archer | 10.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 12.9 | False | Ranged Troops | dragonstone | 21.0 | main_or_minor_line |
| 553 | Vale Elite Archer | vale_elite_archer | 10.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 12.7 | False | Ranged Troops | vale | 21.0 | main_or_minor_line |
| 554 | Ghiscari Legion Trainee | ghiscari_unsullied_initiate | 10.5 | 82.0 | TwoHandedPolearm | unsullied_spear | 22.7 | False | Defensive Troops | ghiscari | 16.0 | main_or_minor_line |
| 555 | Riverlands Elite Archer | river_elite_archer | 10.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 12.4 | False | Ranged Troops | river | 21.0 | main_or_minor_line |
| 556 | Reach Soldier | reach_soldier | 10.5 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 22.5 | False | Defensive Troops | reach | 16.0 | main_or_minor_line |
| 557 | Tyrell Soldier | tyrell_soldier | 10.4 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 21.9 | False | Defensive Troops | reach | 16.0 | main_or_minor_line |
| 558 | Tarly Soldier | tarly_soldier | 10.3 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 21.0 | False | Defensive Troops | reach | 16.0 | main_or_minor_line |
| 559 | Karstark Brute | karstark_soldier | 10.2 | 70.1 | Mace | morningstar_mace_t3 | 24.6 | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 560 | Tyroshi Archer | tyroshi_archer | 10.1 | 73.3 | OneHandedAxe | tyroshi_axe | 15.3 | False | Ranged Troops | tyroshi | 21.0 | main_or_minor_line |
| 561 | Pentoshi Soldier | pentoshi_soldier | 10.0 | 75.7 | OneHandedSword | pentoshi_sword | 32.9 | False | Defensive Troops | pentoshi | 16.0 | main_or_minor_line |
| 562 | Lyseni Soldier | lyseni_soldier | 10.0 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 18.9 | False | Defensive Troops | lyseni | 16.0 | main_or_minor_line |
| 563 | Arryn Footman | arryn_footman | 9.8 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 17.7 | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 564 | Myrish Soldier | myrish_soldier | 9.8 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 17.4 | False | Defensive Troops | myrish | 16.0 | main_or_minor_line |
| 565 | Crownlands Squire | crownlands_squire | 9.8 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 17.4 | False | Defensive Troops | crownlands | 16.0 | main_or_minor_line |
| 566 | Tigercloak Elite Initiate | tigercloak_elite_initiate | 9.1 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 12.2 | False | Ranged Troops | volantine | 16.0 | main_or_minor_line |
| 567 | Yi Ti Infantryman | yiti_infantryman | 9.1 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 25.5 | False | Defensive Troops | yiti | 16.0 | main_or_minor_line |
| 568 | Myrish Crossbowman | myrish_crossbowman | 8.9 | 75.7 | OneHandedSword | empire_sword_2_t3 | 23.9 | False | Ranged Troops | myrish | 16.0 | main_or_minor_line |
| 569 | Vale Squire | vale_squire | 8.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 22.8 | False | Defensive Troops | vale | 16.0 | main_or_minor_line |
| 570 | Night's Watch Ranger | nightswatch_ranger | 8.4 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 20.6 | False | Ranged Troops | nightswatch | 16.0 | main_or_minor_line |
| 571 | Martell Bowman | martell_bowman | 8.2 | 75.7 | OneHandedSword | aserai_sword_2_t2 | 18.8 | False | Ranged Troops | aserai | 16.0 | main_or_minor_line |
| 572 | Goldenmark Marksmen | golden_crossbowman | 8.2 | 75.7 | OneHandedSword | golden_company_sword | 18.4 | False | Ranged Troops | volantine | 16.0 | main_or_minor_line |
| 573 | Blackwood Bowman | blackwood_bowman | 8.2 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 18.3 | False | Ranged Troops | river | 16.0 | main_or_minor_line |
| 574 | Frey Crossbowman | frey_crossbowman | 8.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 18.2 | False | Ranged Troops | river | 16.0 | main_or_minor_line |
| 575 | Lannister Bowman | lannister_bowman | 8.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 17.6 | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 576 | Free Folk Archer | freefolk_archer | 7.8 | 75.7 | OneHandedSword | wildling_knife | 15.8 | False | Ranged Troops | freefolk | 16.0 | main_or_minor_line |
| 577 | Qohorik Bowman | qohorik_bowman | 7.8 | 75.7 | OneHandedSword | khuzait_sword_1_t2 | 15.8 | False | Ranged Troops | qohorik | 16.0 | main_or_minor_line |
| 578 | Tyroshi Bowman | tyroshi_bowman | 7.8 | 75.7 | OneHandedSword | falchion_sword_t2 | 15.3 | False | Ranged Troops | tyroshi | 16.0 | main_or_minor_line |
| 579 | Summer Isles Bowman | summer_bowman | 7.8 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 15.1 | False | Ranged Troops | summer | 16.0 | main_or_minor_line |
| 580 | Myrish Bowman | myrish_bowman | 7.6 | 75.7 | OneHandedSword | empire_sword_1_t2 | 13.8 | False | Ranged Troops | myrish | 16.0 | main_or_minor_line |
| 581 | Bolton Archer | bolton_archer | 7.4 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 17.6 | False | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 582 | Lyseni Bowman | lyseni_bowman | 7.1 | 73.3 | OneHandedAxe | small_bit_axe_t2 | 15.3 | False | Ranged Troops | lyseni | 16.0 | main_or_minor_line |
| 583 | Stormlands Crossbowman | stormlands_crossbowman | 6.8 | 70.1 | Mace | battania_mace_1_t2 | 20.2 | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 584 | Stormlands Elite Archer | stormlands_elite_archer | 6.8 | 70.1 | Mace | battania_mace_1_t2 | 19.8 | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 585 | Dondarrion Bowman | dondarion_bowman | 6.8 | 70.1 | Mace | battania_mace_1_t2 | 19.8 | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 586 | Baratheon Archer | baratheon_archer | 6.2 | 70.1 | Mace | battania_mace_1_t2 | 15.1 | False | Ranged Troops | stormlands | 21.0 | main_or_minor_line |
| 587 | Skagosi Bowman | skag_bowman | 6.1 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 7.2 | False | Ranged Troops | skagosi | 16.0 | main_or_minor_line |
| 588 | Lannister Levy | lannister_levy | 5.8 | 82.0 | TwoHandedPolearm | western_spear_2_t2 | 24.7 | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 589 | Guard | guard_ibbenese | 5.7 | 82.0 | TwoHandedPolearm | northern_spear_2_t3 | 23.4 | False | Offensive Melee | ibbenese | 4.0 | special_or_unlinked |
| 590 | Casterly Rock Guard | casterly_guard | 5.6 | 82.0 | TwoHandedPolearm | western_spear_2_t2 | 23.0 | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 591 | Guard | guard_qartheen | 5.5 | 82.0 | TwoHandedPolearm | imperial_spear_t2 | 16.7 | False | Offensive Melee | qartheen | 21.0 | special_or_unlinked |
| 592 | Gold Cloak Archer | goldcloak_archer | 5.4 | 75.7 | OneHandedSword | short_sword_t3 | 20.9 | False | Ranged Troops | crownlands | 16.0 | main_or_minor_line |
| 593 | Qartheen Archer | qartheen_archer | 5.3 | 75.7 | OneHandedSword | empire_sword_1_t2 | 20.0 | False | Ranged Troops | qartheen | 16.0 | main_or_minor_line |
| 594 | Yi Ti Bowman | yiti_bowman | 5.3 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 19.9 | False | Ranged Troops | yiti | 16.0 | main_or_minor_line |
| 595 | Royce Footman | royce_footman | 5.1 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 19.7 | False | Defensive Troops | vale | 11.0 | main_or_minor_line |
| 596 | Arryn Levy | arryn_levy | 5.1 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 19.7 | False | Defensive Troops | vale | 11.0 | main_or_minor_line |
| 597 | Guard | guard_valyrian | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | valyrian | 4.0 | special_or_unlinked |
| 598 | Guard | guard_ghiscari | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | ghiscari | 4.0 | special_or_unlinked |
| 599 | Guard | guard_freefolk | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | freefolk | 4.0 | special_or_unlinked |
| 600 | Guard | guard_tyroshi | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | tyroshi | 4.0 | special_or_unlinked |
| 601 | Guard | guard_dragonstone | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | dragonstone | 4.0 | special_or_unlinked |
| 602 | Guard | guard_lorathi | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | nord | 4.0 | special_or_unlinked |
| 603 | Guard | guard_crownlands | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | crownlands | 4.0 | special_or_unlinked |
| 604 | Guard | guard_lyseni | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | lyseni | 4.0 | special_or_unlinked |
| 605 | Guard | guard_myrish | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | myrish | 4.0 | special_or_unlinked |
| 606 | Guard | guard_norvos | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | norvos | 4.0 | special_or_unlinked |
| 607 | Guard | guard_stormlands | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | stormlands | 4.0 | special_or_unlinked |
| 608 | Guard | guard_summer | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | summer | 4.0 | special_or_unlinked |
| 609 | Guard | guard_pentoshi | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | pentoshi | 4.0 | special_or_unlinked |
| 610 | Guard | guard_vale | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | vale | 4.0 | special_or_unlinked |
| 611 | Guard | guard_qohorik | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | qohorik | 4.0 | special_or_unlinked |
| 612 | Guard | guard_reach | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | reach | 4.0 | special_or_unlinked |
| 613 | Guard | guard_river | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | river | 4.0 | special_or_unlinked |
| 614 | Guard | guard_volantine | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | volantine | 4.0 | special_or_unlinked |
| 615 | Guard | guard_sarnor | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | sarnor | 4.0 | special_or_unlinked |
| 616 | Guard | guard_skagosi | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | skagosi | 4.0 | special_or_unlinked |
| 617 | Dead Guard | guard_wight | 5.0 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 17.1 | False | Offensive Melee | whitewalker | 4.0 | special_or_unlinked |
| 618 | Ghiscari Archer | ghiscari_archer | 5.0 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 17.5 | False | Ranged Troops | ghiscari | 16.0 | main_or_minor_line |
| 619 | Valyrian Bowman | targaryen_bowman | 4.8 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 15.9 | False | Ranged Troops | valyrian | 16.0 | main_or_minor_line |
| 620 | Guard | guard_nightswatch | 4.7 | 82.0 | TwoHandedPolearm | billhook_polearm_t2 | 16.5 | False | Offensive Melee | nightswatch | 4.0 | special_or_unlinked |
| 621 | Guard | guard_yiti | 4.7 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3 | 15.8 | False | Offensive Melee | yiti | 4.0 | special_or_unlinked |
| 622 | Valyrian Levy | targaryen_levy | 4.6 | 82.0 | TwoHandedPolearm | western_spear_2_t2 | 15.8 | False | Offensive Melee | valyrian | 11.0 | main_or_minor_line |
| 623 | Hightower Levy | hightower_levy | 4.6 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 15.7 | False | Offensive Melee | reach | 11.0 | main_or_minor_line |
| 624 | Westerling Levy | westerling_levy | 4.6 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 26.5 | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 625 | Grafton Levy | grafton_levy | 4.6 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 26.5 | False | Defensive Troops | vale | 11.0 | main_or_minor_line |
| 626 | Sarnori Archer | sarnor_archer | 4.6 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 14.3 | False | Ranged Troops | sarnor | 16.0 | main_or_minor_line |
| 627 | Tyroshi Footman | tyroshi_footman | 4.6 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 15.3 | False | Offensive Melee | tyroshi | 11.0 | main_or_minor_line |
| 628 | Stark Bowman | stark_bowman | 4.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 13.9 | False | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 629 | Tarly Footman | tarly_footman | 4.5 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 15.0 | False | Offensive Melee | reach | 11.0 | main_or_minor_line |
| 630 | Night's Watch Crossbowman | nightswatch_crossbowman | 4.4 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 13.0 | False | Ranged Troops | nightswatch | 16.0 | main_or_minor_line |
| 631 | Reach Archer | reach_archer | 4.4 | 75.7 | OneHandedSword | short_sword_t3 | 12.8 | False | Ranged Troops | reach | 16.0 | main_or_minor_line |
| 632 | Vale Archer | vale_archer | 4.4 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 12.7 | False | Ranged Troops | vale | 16.0 | main_or_minor_line |
| 633 | Myrish Footman | myrish_footman | 4.4 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 13.8 | False | Offensive Melee | myrish | 11.0 | main_or_minor_line |
| 634 | Norvoshi Archer | norvos_archer | 4.4 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 12.6 | False | Ranged Troops | norvos | 16.0 | main_or_minor_line |
| 635 | Tyrell Footman | tyrell_footman | 4.4 | 82.0 | TwoHandedPolearm | western_spear_1_t2 | 13.7 | False | Offensive Melee | reach | 11.0 | main_or_minor_line |
| 636 | Riverlands Archer | river_archer | 4.4 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 12.4 | False | Ranged Troops | river | 16.0 | main_or_minor_line |
| 637 | Dragonstone Bowman | dragonstone_bowman | 4.3 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 11.9 | False | Ranged Troops | dragonstone | 16.0 | main_or_minor_line |
| 638 | Mallister Levy | mallister_levy | 4.3 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 23.7 | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 639 | Bracken Levy | bracken_levy | 4.2 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 23.6 | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 640 | Blackwood Levy | blackwood_levy | 4.2 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 23.6 | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 641 | Tully Footman | tully_footman | 4.2 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 23.4 | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 642 | Dayne Levy | dayne_levy | 4.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 22.9 | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 643 | Summer Isles Footman | summer_footman | 4.1 | 82.0 | TwoHandedPolearm | eastern_spear_1_t2 | 11.5 | False | Offensive Melee | summer | 11.0 | main_or_minor_line |
| 644 | Yronwood Levy | yronwood_levy | 3.9 | 75.7 | OneHandedSword | aserai_sword_2_t2 | 21.0 | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 645 | Ibbenese Deckhand | ibbenese_noble_recruit | 3.8 | 75.7 | OneHandedSword | battania_sword_1_t2 | 8.2 | False | Offensive Melee | ibbenese | 11.0 | main_or_minor_line |
| 646 | Tarth Militia | tarth_militia | 3.8 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 20.2 | False | Defensive Troops | stormlands | 11.0 | main_or_minor_line |
| 647 | Riverlands Footman | river_footman | 3.8 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 20.2 | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 648 | Pentoshi Footman | pentoshi_footman | 3.8 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 20.1 | False | Defensive Troops | pentoshi | 11.0 | main_or_minor_line |
| 649 | Crownlands Noble's Son | crownlands_noble_recruit | 3.8 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 7.9 | False | Offensive Melee | crownlands | 11.0 | main_or_minor_line |
| 650 | Reach Noble's Son | reach_noble_recruit | 3.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 7.6 | False | Offensive Melee | reach | 11.0 | main_or_minor_line |
| 651 | Stormlands Noble's Son | stormlands_noble_recruit | 3.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 7.5 | False | Offensive Melee | stormlands | 11.0 | main_or_minor_line |
| 652 | Valyrian Noble's Son | valyrian_noble_recruit | 3.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 7.5 | False | Offensive Melee | valyrian | 11.0 | main_or_minor_line |
| 653 | Dragonstone Noble's Son | dragonstone_noble_recruit | 3.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 7.5 | False | Offensive Melee | dragonstone | 11.0 | main_or_minor_line |
| 654 | Night's Watch Ranger Recruit | nightswatch_ranger_recruit | 3.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 7.4 | False | Ranged Troops | nightswatch | 11.0 | main_or_minor_line |
| 655 | Martell Levy | martell_levy | 3.7 | 75.7 | OneHandedSword | aserai_sword_2_t2 | 19.4 | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 656 | Riverlord's Son | river_noble_recruit | 3.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 7.3 | False | Offensive Melee | river | 11.0 | main_or_minor_line |
| 657 | Freefolk Son of Thenn | freefolk_thenn_son | 3.7 | 73.3 | TwoHandedAxe | bronze_axe | 11.8 | False | Offensive Melee | freefolk | 11.0 | main_or_minor_line |
| 658 | Ghiscari Former Slave | ghiscari_noble_recruit | 3.7 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 7.1 | False | Offensive Melee | ghiscari | 11.0 | main_or_minor_line |
| 659 | Norvoshi Initiate | norvos_initiate | 3.6 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 6.6 | False | Offensive Melee | norvos | 11.0 | main_or_minor_line |
| 660 | Qohorik Noble Youth | qohorik_noble_recruit | 3.6 | 75.7 | OneHandedSword | qohorik_sword | 6.6 | False | Offensive Melee | qohorik | 11.0 | main_or_minor_line |
| 661 | Volantene Noble Youth | volantine_noble_recruit | 3.6 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 6.6 | False | Offensive Melee | volantine | 11.0 | main_or_minor_line |
| 662 | Vale Page | vale_page | 3.6 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.6 | False | Offensive Melee | vale | 11.0 | main_or_minor_line |
| 663 | Sarnori Noble's Son | sarnor_noble_recruit | 3.6 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 6.4 | False | Offensive Melee | sarnor | 11.0 | main_or_minor_line |
| 664 | Clegane Recruit | clegane_recruit | 3.6 | 82.0 | Mace|OneHandedAxe|TwoHandedPolearm | peasant_hammer_1_t1|peasant_pickaxe_1_t1|peasant_pitchfork_1_t1|vlandia_mace_1_t2 | 7.2 | False | Offensive Melee | vlandia | 6.0 | main_or_minor_line |
| 665 | Dayne Recruit | dayne_recruit | 3.6 | 82.0 | Mace|OneHandedAxe|TwoHandedPolearm | peasant_hammer_1_t1|peasant_pickaxe_1_t1|peasant_pitchfork_1_t1|vlandia_mace_1_t2 | 7.5 | False | Offensive Melee | aserai | 6.0 | main_or_minor_line |
| 666 | Celtigar Recruit | celtigar_recruit | 3.6 | 82.0 | Mace|OneHandedAxe|TwoHandedPolearm | peasant_hammer_1_t1|peasant_pickaxe_1_t1|peasant_pitchfork_1_t1|vlandia_mace_1_t2 | 7.0 | False | Offensive Melee | dragonstone | 6.0 | main_or_minor_line |
| 667 | Dondarrion Levy | dondarion_levy | 3.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 18.1 | False | Defensive Troops | stormlands | 11.0 | main_or_minor_line |
| 668 | Yi Ti Recruit | yiti_recruit | 3.5 | 82.0 | Mace|OneHandedAxe|TwoHandedPolearm | khuzait_mace_1_t2|peasant_pitchfork_1_t1|peasant_polearm_1_t1|peasant_sickle_1_t1 | 7.1 | False | Offensive Melee | yiti | 6.0 | main_or_minor_line |
| 669 | Baratheon Footman | baratheon_footman | 3.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 18.0 | False | Defensive Troops | stormlands | 11.0 | main_or_minor_line |
| 670 | Golden Company Recruit | golden_recruit | 3.5 | 75.7 | OneHandedSword | golden_company_sword | 17.5 | False | Offensive Melee | volantine | 11.0 | main_or_minor_line |
| 671 | Stark Levy | stark_levy | 3.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 17.5 | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 672 | Manderly Levy | whiteharbor_levy | 3.4 | 75.7 | OneHandedSword | battania_sword_1_t2 | 17.1 | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 673 | Summer Isles Recruit | summer_recruit | 3.4 | 82.0 | Mace|OneHandedAxe|TwoHandedPolearm | khuzait_mace_1_t2|peasant_pitchfork_1_t1|peasant_polearm_1_t1|peasant_sickle_1_t1 | 6.2 | False | Offensive Melee | summer | 6.0 | main_or_minor_line |
| 674 | Free Folk Warrior | freefolk_warrior | 3.3 | 73.3 | OneHandedAxe | wildling_pickaxe | 20.6 | False | Defensive Troops | freefolk | 11.0 | main_or_minor_line |
| 675 | Greyjoy Footman | greyjoy_footman | 3.3 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 15.9 | False | Offensive Melee | sturgia | 11.0 | main_or_minor_line |
| 676 | Norvoshi Footman | norvos_footman | 3.2 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 15.7 | False | Defensive Troops | norvos | 11.0 | main_or_minor_line |
| 677 | Sarnori Footman | sarnor_footman | 3.2 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 15.3 | False | Defensive Troops | sarnor | 11.0 | main_or_minor_line |
| 678 | Celtigar Levy | celtigar_levy | 3.1 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 18.8 | False | Offensive Melee | dragonstone | 11.0 | main_or_minor_line |
| 679 | Qartheen Pureborn Youth | qartheen_noble_recruit | 3.1 | 75.7 | OneHandedSword | iron_spatha_sword_t2 | 2.5 | False | Offensive Melee | qartheen | 11.0 | main_or_minor_line |
| 680 | Harlaw Levy | harlaw_levy | 3.0 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 13.9 | False | Offensive Melee | sturgia | 11.0 | main_or_minor_line |
| 681 | Volantene Bowman | volantine_bowman | 3.0 | 70.1 | Mace | aserai_mace_2_t2 | 12.2 | False | Ranged Troops | volantine | 16.0 | main_or_minor_line |
| 682 | Glover Levy | glover_levy | 2.9 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 17.3 | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 683 | Cerwyn Levy | cerwyn_levy | 2.9 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 17.2 | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 684 | Reach Levy | reach_levy | 2.9 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 12.8 | False | Offensive Melee | reach | 11.0 | main_or_minor_line |
| 685 | Crownlands Levy | crownlands_levy | 2.9 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 12.8 | False | Offensive Melee | crownlands | 11.0 | main_or_minor_line |
| 686 | Umber Levy | umber_levy | 2.8 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 16.7 | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 687 | Yi Ti Footman | yiti_footman | 2.8 | 75.7 | OneHandedSword | simple_sabre_sword_t2 | 12.4 | False | Offensive Melee | yiti | 11.0 | main_or_minor_line |
| 688 | Skagosi Footman | skag_footman | 2.8 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 16.5 | False | Defensive Troops | skagosi | 11.0 | main_or_minor_line |
| 689 | Velaryon Shipmate | velaryon_shipman | 2.8 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 16.3 | False | Offensive Melee | dragonstone | 11.0 | main_or_minor_line |
| 690 | Clegane Levy | clegane_levy | 2.8 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 16.2 | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 691 | Night's Watch Soldier | nightswatch_soldier | 2.8 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 12.0 | False | Offensive Melee | nightswatch | 11.0 | main_or_minor_line |
| 692 | Lyseni Footman | lyseni_footman | 2.7 | 73.3 | OneHandedAxe | small_bit_axe_t2 | 15.9 | False | Defensive Troops | lyseni | 11.0 | main_or_minor_line |
| 693 | Norvoshi Bowman | norvos_bowman | 2.7 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 11.7 | False | Ranged Troops | norvos | 11.0 | main_or_minor_line |
| 694 | Crownlands Bowman | crownlands_bowman | 2.7 | 75.7 | OneHandedSword | short_sword_t3 | 11.5 | False | Ranged Troops | crownlands | 11.0 | main_or_minor_line |
| 695 | Reach Bowman | reach_bowman | 2.7 | 75.7 | OneHandedSword | short_sword_t3 | 11.5 | False | Ranged Troops | reach | 11.0 | main_or_minor_line |
| 696 | Vale Footman | vale_footman | 2.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 11.5 | False | Offensive Melee | vale | 11.0 | main_or_minor_line |
| 697 | Qohorik Footman | qohorik_footman | 2.7 | 70.1 | Mace | khuzait_mace_1_t2 | 21.1 | False | Defensive Troops | qohorik | 11.0 | main_or_minor_line |
| 698 | Free Folk Bowman | freefolk_bowman | 2.6 | 73.3 | OneHandedAxe | wildling_pickaxe | 14.7 | False | Ranged Troops | freefolk | 11.0 | main_or_minor_line |
| 699 | Mormont Woodswoman | mormont_woodswoman | 2.5 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 14.5 | False | Skirmishers | battania | 11.0 | main_or_minor_line |
| 700 | Karstark Levy | freehouses_levy | 2.5 | 70.1 | Mace | vlandia_mace_1_t2 | 19.9 | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 701 | Frey Levy | frey_levy | 2.5 | 70.1 | Mace | vlandia_mace_1_t2 | 19.4 | False | Defensive Troops | river | 11.0 | main_or_minor_line |
| 702 | Bolton Levy | bolton_levy | 2.5 | 70.1 | Mace | vlandia_mace_1_t2 | 19.4 | False | Defensive Troops | battania | 11.0 | main_or_minor_line |
| 703 | Lannister Recruit | lannister_recruit | 2.4 | 75.7 | Mace|OneHandedAxe|OneHandedSword | peasant_hammer_1_t1|peasant_pickaxe_1_t1|vlandia_mace_1_t2|vlandia_sword_1_t2 | 8.3 | False | Offensive Melee | vlandia | 6.0 | main_or_minor_line |
| 704 | Ibbenese Footman | ibbenese_footman | 2.3 | 75.7 | OneHandedSword | battania_sword_1_t2 | 8.2 | False | Offensive Melee | ibbenese | 11.0 | main_or_minor_line |
| 705 | Pentoshi Noble Youth | pentoshi_noble_recruit | 2.3 | 70.1 | Mace | empire_mace_1_t2 | 6.6 | False | Offensive Melee | pentoshi | 11.0 | main_or_minor_line |
| 706 | Myrish Noble Youth | myrish_noble_recruit | 2.2 | 70.1 | Mace | empire_mace_1_t2 | 6.4 | False | Offensive Melee | myrish | 11.0 | main_or_minor_line |
| 707 | Tyroshi Noble Youth | tyroshi_noble_recruit | 2.2 | 70.1 | Mace | empire_mace_1_t2 | 6.4 | False | Offensive Melee | tyroshi | 11.0 | main_or_minor_line |
| 708 | Lyseni Noble Youth | lyseni_noble_recruit | 2.2 | 70.1 | Mace | empire_mace_1_t2 | 6.4 | False | Offensive Melee | lyseni | 11.0 | main_or_minor_line |
| 709 | Dragonstone Footman | dragonstone_footman | 2.2 | 73.3 | OneHandedAxe | vlandia_axe_1_t3 | 11.9 | False | Offensive Melee | dragonstone | 11.0 | main_or_minor_line |
| 710 | Stark Recruit | stark_volunteer | 2.2 | 75.7 | Mace|OneHandedAxe|OneHandedSword | battania_mace_2_t2|peasant_hatchet_1_t1|vlandia_sword_1_t2 | 7.0 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 711 | Martell Recruit | martell_recruit | 2.1 | 75.7 | Mace|OneHandedAxe|OneHandedSword | aserai_sword_2_t2|peasant_hammer_1_t1|peasant_hammer_2_t1|peasant_hatchet_1_t1 | 6.7 | False | Offensive Melee | aserai | 6.0 | main_or_minor_line |
| 712 | Arryn Recruit | arryn_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.6 | False | Offensive Melee | vale | 6.0 | main_or_minor_line |
| 713 | Reach Recruit | reach_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | reach | 6.0 | main_or_minor_line |
| 714 | Tarly Recruit | tarly_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | reach | 6.0 | main_or_minor_line |
| 715 | Hightower Recruit | hightower_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | reach | 6.0 | main_or_minor_line |
| 716 | Crownlands Recruit | crownlands_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | crownlands | 6.0 | main_or_minor_line |
| 717 | Volantene Recruit | volantine_recruit | 2.1 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 6.4 | False | Offensive Melee | volantine | 6.0 | main_or_minor_line |
| 718 | Tyrell Recruit | tyrell_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | reach | 6.0 | main_or_minor_line |
| 719 | Tarth Recruit | tarth_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | stormlands | 6.0 | main_or_minor_line |
| 720 | Norvoshi Recruit | norvos_recruit | 2.1 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 6.4 | False | Offensive Melee | norvos | 6.0 | main_or_minor_line |
| 721 | Pentoshi Recruit | pentoshi_recruit | 2.1 | 75.7 | OneHandedSword | empire_sword_1_t2 | 6.4 | False | Offensive Melee | pentoshi | 6.0 | main_or_minor_line |
| 722 | Baratheon Recruit | baratheon_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | stormlands | 6.0 | main_or_minor_line |
| 723 | Velaryon Recruit | velaryon_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | dragonstone | 6.0 | main_or_minor_line |
| 724 | Mallister Recruit | mallister_recruit | 2.1 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 6.4 | False | Offensive Melee | river | 6.0 | main_or_minor_line |
| 725 | Blackwood Recruit | blackwood_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | river | 6.0 | main_or_minor_line |
| 726 | Manderly Recruit | whiteharbor_volunteer | 2.1 | 75.7 | Mace|OneHandedAxe|OneHandedSword | battania_mace_2_t2|battania_sword_1_t2|peasant_hatchet_1_t1 | 6.4 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 727 | Qohorik Recruit | qohorik_recruit | 2.1 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 6.4 | False | Offensive Melee | qohorik | 6.0 | main_or_minor_line |
| 728 | Frey Recruit | frey_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | river | 6.0 | main_or_minor_line |
| 729 | Valyrian Recruit | valyrian_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | valyrian | 6.0 | main_or_minor_line |
| 730 | Royce Recruit | royce_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | vale | 6.0 | main_or_minor_line |
| 731 | Tully Recruit | tully_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | river | 6.0 | main_or_minor_line |
| 732 | Westerling Recruit | westerling_recruit | 2.1 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 6.4 | False | Offensive Melee | vlandia | 6.0 | main_or_minor_line |
| 733 | Vale Recruit | vale_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | vale | 6.0 | main_or_minor_line |
| 734 | Riverlands Recruit | river_recruit | 2.1 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 6.4 | False | Offensive Melee | river | 6.0 | main_or_minor_line |
| 735 | Ghiscari Recruit | ghiscari_recruit | 2.1 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 6.4 | False | Offensive Melee | ghiscari | 6.0 | main_or_minor_line |
| 736 | Grafton Recruit | grafton_recruit | 2.1 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 6.4 | False | Offensive Melee | vale | 6.0 | main_or_minor_line |
| 737 | Bracken Recruit | bracken_recruit | 2.0 | 75.7 | OneHandedSword | sturgia_sword_1_t2 | 6.2 | False | Offensive Melee | river | 6.0 | main_or_minor_line |
| 738 | Tyroshi Recruit | tyroshi_recruit | 2.0 | 75.7 | OneHandedSword | empire_sword_1_t2 | 6.2 | False | Offensive Melee | tyroshi | 6.0 | main_or_minor_line |
| 739 | Sarnori Recruit | sarnor_recruit | 2.0 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 6.2 | False | Offensive Melee | sarnor | 6.0 | main_or_minor_line |
| 740 | Myrish Recruit | myrish_recruit | 2.0 | 75.7 | OneHandedSword | empire_sword_1_t2 | 6.2 | False | Offensive Melee | myrish | 6.0 | main_or_minor_line |
| 741 | Lyseni Recruit | lyseni_recruit | 2.0 | 75.7 | OneHandedSword | empire_sword_1_t2 | 6.2 | False | Offensive Melee | lyseni | 6.0 | main_or_minor_line |
| 742 | Stormlands Archer | stormlands_archer | 2.0 | 70.1 | Mace | battania_mace_1_t2 | 15.9 | False | Ranged Troops | stormlands | 16.0 | main_or_minor_line |
| 743 | Stormlands Levy | stormlands_levy | 1.9 | 70.1 | Mace | battania_mace_1_t2 | 15.0 | False | Defensive Troops | stormlands | 11.0 | main_or_minor_line |
| 744 | Vale Bowman | vale_bowman | 1.9 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 5.1 | False | Ranged Troops | vale | 11.0 | main_or_minor_line |
| 745 | Baratheon Bowman | baratheon_bowman | 1.9 | 70.1 | Mace | battania_mace_1_t2 | 14.6 | False | Ranged Troops | stormlands | 16.0 | main_or_minor_line |
| 746 | Riverlands Bowman | river_bowman | 1.8 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 4.6 | False | Ranged Troops | river | 11.0 | main_or_minor_line |
| 747 | Ibbenese Recruit | ibbenese_recruit | 1.8 | 75.7 | OneHandedSword | battania_sword_1_t2 | 4.2 | False | Offensive Melee | ibbenese | 6.0 | main_or_minor_line |
| 748 | Free Folk Clansman | freefolk_recruit | 1.7 | 73.3 | OneHandedAxe | wildling_pickaxe | 8.1 | False | Offensive Melee | freefolk | 6.0 | main_or_minor_line |
| 749 | Mormont Recruit | mormont_volunteer | 1.7 | 73.3 | Mace|OneHandedAxe | battania_axe_1_t2|battania_mace_2_t2|peasant_hatchet_1_t1|peasant_pickaxe_1_t1 | 6.9 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 750 | Umber Recruit | umber_volunteer | 1.7 | 73.3 | Mace|OneHandedAxe | battania_mace_2_t2|peasant_hatchet_1_t1|sturgia_axe_2_t2 | 6.9 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 751 | Cerwyn Recruit | cerwyn_volunteer | 1.7 | 73.3 | Mace|OneHandedAxe | battania_axe_1_t2|battania_mace_2_t2|peasant_hatchet_1_t1 | 6.9 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 752 | Ghiscari Footman | ghiscari_footman | 1.7 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 3.2 | False | Offensive Melee | ghiscari | 11.0 | main_or_minor_line |
| 753 | Kingsguard's Page | kingsguard_page | 1.7 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 3.2 | False | Offensive Melee | crownlands | 11.0 | main_or_minor_line |
| 754 | Sarnori Bowman | sarnor_bowman | 1.6 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 2.6 | False | Ranged Troops | sarnor | 11.0 | main_or_minor_line |
| 755 | Ghiscari Bowman | ghiscari_bowman | 1.6 | 75.7 | OneHandedSword | aserai_sword_1_t2 | 2.6 | False | Ranged Troops | ghiscari | 11.0 | main_or_minor_line |
| 756 | Qartheen Footman | qartheen_footman | 1.6 | 75.7 | OneHandedSword | empire_sword_1_t2 | 2.5 | False | Offensive Melee | qartheen | 11.0 | main_or_minor_line |
| 757 | Stormlands Bowman | stormlands_bowman | 1.6 | 70.1 | Mace | battania_mace_1_t2 | 12.3 | False | Ranged Troops | stormlands | 11.0 | main_or_minor_line |
| 758 | Dragonstone Recruit | dragonstone_recruit | 1.5 | 73.3 | OneHandedAxe | vlandia_axe_1_t3 | 6.4 | False | Offensive Melee | dragonstone | 6.0 | main_or_minor_line |
| 759 | Skagosi Lowborn | skag_recruit | 1.5 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 6.4 | False | Offensive Melee | skagosi | 6.0 | main_or_minor_line |
| 760 | Harlaw Deckhand | harlaw_recruit | 1.5 | 73.3 | Mace|OneHandedAxe | peasant_hammer_1_t1|peasant_hammer_2_t1|peasant_sickle_1_t1|sturgia_axe_2_t2 | 6.7 | False | Offensive Melee | sturgia | 6.0 | main_or_minor_line |
| 761 | Bolton Recruit | bolton_volunteer | 1.5 | 73.3 | Mace|OneHandedAxe | battania_mace_2_t2|peasant_hatchet_1_t1|peasant_pickaxe_1_t1|vlandia_mace_1_t2 | 6.9 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 762 | Night's Watch Recruit | nightswatch_recruit | 1.5 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 6.4 | False | Offensive Melee | nightswatch | 6.0 | main_or_minor_line |
| 763 | Glover Recruit | glover_volunteer | 1.5 | 73.3 | Mace|OneHandedAxe|TwoHandedMace | battania_mace_2_t2|peasant_hatchet_1_t1|peasant_maul_t1_2|peasant_pickaxe_1_t1 | 6.9 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 764 | Greyjoy Deckhand | greyjoy_recruit | 1.5 | 73.3 | Mace|OneHandedAxe | peasant_hammer_1_t1|peasant_hammer_2_t1|peasant_sickle_1_t1|sturgia_axe_2_t2 | 6.6 | False | Offensive Melee | sturgia | 6.0 | main_or_minor_line |
| 765 | Karstark Recruit | karstark_volunteer | 1.5 | 73.3 | Mace|OneHandedAxe|TwoHandedMace | battania_mace_2_t2|peasant_hatchet_1_t1|peasant_maul_t1_2|peasant_pickaxe_1_t1 | 6.9 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 766 | Qartheen Recruit | qartheen_recruit | 1.5 | 75.7 | OneHandedSword | empire_sword_1_t2 | 1.8 | False | Offensive Melee | qartheen | 6.0 | main_or_minor_line |
| 767 | Qartheen Bowman | qartheen_bowman | 1.5 | 75.7 | OneHandedSword | empire_sword_1_t2 | 1.8 | False | Ranged Troops | qartheen | 11.0 | main_or_minor_line |
| 768 | Volantene Footman | volantine_footman | 1.4 | 70.1 | Mace | aserai_mace_2_t2 | 10.9 | False | Offensive Melee | volantine | 11.0 | main_or_minor_line |
| 769 | Yronwood Recruit | yronwood_recruit | 0.8 | 70.1 | Mace | battania_mace_1_t2 | 6.4 | False | Offensive Melee | aserai | 6.0 | main_or_minor_line |
| 770 | Dondarrion Recruit | dondarion_recruit | 0.8 | 70.1 | Mace | battania_mace_1_t2 | 6.4 | False | Offensive Melee | stormlands | 6.0 | main_or_minor_line |
| 771 | Stormlands Recruit | stormlands_recruit | 0.8 | 70.1 | Mace | battania_mace_1_t2 | 6.4 | False | Offensive Melee | stormlands | 6.0 | main_or_minor_line |
| 772 | Angry Wight | angry_wight | 0.8 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 0.6 | False | Offensive Melee | whitewalker | 11.0 | main_or_minor_line |
| 773 | Wight | wight_recruit | 0.7 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 0.0 | False | Offensive Melee | whitewalker | 6.0 | main_or_minor_line |


## Ranked — Skirmisher (67 troops)

| rank | troop_name | troop_id | skirmisher_role_score | throw_score_base | throw_damage | direct_throw_item | crafted_throw_item | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Golden Company Mahout | golden_elite_pikeman | 100.0 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | volantine | 31.0 | main_or_minor_line |
| 2 | Yi Ti Mounted Shi | yiti_samurai | 90.8 | 28.8 | 0.0 | nan | empire_throwingknife_t5 | True | Skirmishers | yiti | 31.0 | main_or_minor_line |
| 3 | Magister Guard Elite | magister_guard | 89.6 | 30.5 | 0.0 | nan | western_javelin_3_t4 | True | Skirmishers | pentoshi | 31.0 | main_or_minor_line |
| 4 | Knights of Starfall | dayne_starfall_knights | 89.0 | 30.5 | 0.0 | nan | western_javelin_2_t3 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 5 | Realm Paladin | realm_paladin | 88.8 | 30.5 | 0.0 | nan | western_javelin_3_t4 | True | Skirmishers | crownlands | 31.0 | main_or_minor_line |
| 6 | Black Goat Sacrificer | qohorik_goat_sacrificer | 88.6 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | True | Skirmishers | qohorik | 31.0 | main_or_minor_line |
| 7 | Queen's Man | dragonstone_steel_curtain | 88.4 | 30.5 | 0.0 | nan | western_javelin_3_t4 | True | Skirmishers | dragonstone | 31.0 | main_or_minor_line |
| 8 | Water Gardens Sentinel | garden_sentinel | 87.4 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 9 | Skagosi Stoneborn Champion | skagosi_stoneborn_champion | 87.3 | 30.5 | 0.0 | nan | generic_javelin_1_t3 | True | Skirmishers | skagosi | 31.0 | main_or_minor_line |
| 10 | Boneway Guardian | boneway_guardian | 87.2 | 30.5 | 0.0 | nan | western_javelin_2_t3 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 11 | Sarnori Spider | sarnor_spider | 83.4 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | sarnor | 31.0 | main_or_minor_line |
| 12 | Valyrian Cavalry | targaryen_dragonknight | 72.1 | 30.5 | 0.0 | nan | western_javelin_2_t3 | True | Skirmishers | valyrian | 26.0 | main_or_minor_line |
| 13 | Ghiscari Lockstep Legionnaire | ghiscari_unsullied_unbroken | 71.0 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | ghiscari | 31.0 | main_or_minor_line |
| 14 | Tarly Vanguard | tarly_vanguard | 68.4 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | reach | 31.0 | main_or_minor_line |
| 15 | Realm Knight | realm_knight | 67.8 | 30.5 | 0.0 | nan | western_javelin_3_t4 | True | Skirmishers | crownlands | 26.0 | main_or_minor_line |
| 16 | Dragonstone Shock Knight | dragonstone_shock_knight | 67.6 | 30.5 | 0.0 | nan | western_javelin_3_t4 | True | Skirmishers | dragonstone | 26.0 | main_or_minor_line |
| 17 | Celtigar Banneret | celtigar_banneret | 67.6 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | dragonstone | 31.0 | main_or_minor_line |
| 18 | Ibbenese Navigator | ibbenese_navigator | 66.7 | 30.5 | 0.0 | nan | northern_javelin_1_t2 | False | Skirmishers | ibbenese | 31.0 | main_or_minor_line |
| 19 | Greyjoy Horseman | greyjoy_horseman | 66.4 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 20 | Glover Bushranger | glover_bushranger | 66.2 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | battania | 31.0 | main_or_minor_line |
| 21 | Skagosi Stoneborn | skagosi_stoneborn | 65.4 | 30.5 | 0.0 | nan | generic_javelin_1_t3 | True | Skirmishers | skagosi | 26.0 | main_or_minor_line |
| 22 | Harlaw Raider | harlaw_horseman | 65.1 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 23 | Unsullied | unsullied | 65.0 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | ghiscari | 31.0 | special_or_unlinked |
| 24 | High King Guardian | sarnor_highking_guardian | 64.8 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | True | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 25 | Casterly Rock Champion | casterly_champion | 64.0 | 30.5 | 0.0 | nan | western_javelin_2_t3 | True | Skirmishers | vlandia | 26.0 | main_or_minor_line |
| 26 | Sarnori Master Javelinier | sarnor_master_javelinier | 63.5 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 27 | Bolton Flayer | bolton_flayer | 63.1 | 28.8 | 0.0 | nan | celtic_throwing_dagger | False | Skirmishers | battania | 31.0 | main_or_minor_line |
| 28 | Umber Berzerker | umber_berzerker | 63.1 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | battania | 31.0 | main_or_minor_line |
| 29 | Martell Horseman | martell_horseman | 62.2 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 30 | Tyroshi Corsair | tyroshi_corsair | 62.0 | 30.5 | 0.0 | nan | generic_javelin_1_t3 | False | Skirmishers | tyroshi | 31.0 | main_or_minor_line |
| 31 | Guardian of the Rock | casterly_guardian | 60.9 | 30.5 | 0.0 | nan | western_javelin_2_t3 | False | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 32 | Free Folk Horseman | freefolk_horseman | 60.2 | 30.5 | 0.0 | nan | northern_javelin_1_t2 | True | Skirmishers | freefolk | 26.0 | main_or_minor_line |
| 33 | Beastbound Wight | beastbound_wight | 55.6 | 30.5 | 0.0 | nan | northern_javelin_1_t2 | True | Skirmishers | whitewalker | 26.0 | main_or_minor_line |
| 34 | Yi Ti Shi | yiti_pikeman | 53.7 | 28.8 | 0.0 | nan | empire_throwingknife_t5 | False | Skirmishers | yiti | 26.0 | main_or_minor_line |
| 35 | Dragonstone Knight | dragonstone_knight | 51.3 | 30.5 | 0.0 | nan | western_javelin_1_t2 | True | Skirmishers | dragonstone | 21.0 | main_or_minor_line |
| 36 | Valyrian Scout | valyrian_scout | 49.8 | 30.5 | 0.0 | nan | western_javelin_2_t3 | True | Skirmishers | valyrian | 21.0 | main_or_minor_line |
| 37 | Ghiscari Elite Legionnaire | ghiscari_unsullied_unbent | 49.5 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | ghiscari | 26.0 | main_or_minor_line |
| 38 | Black Goat Devout | qohorik_goat_devout | 48.6 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | qohorik | 26.0 | main_or_minor_line |
| 39 | Glover Warrior | glover_warrior | 48.2 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | battania | 26.0 | main_or_minor_line |
| 40 | Martell House Guard | martell_houseguard | 45.0 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 41 | Tyroshi Firstmate | tyroshi_firstmate | 44.0 | 30.5 | 0.0 | nan | generic_javelin_1_t3 | False | Skirmishers | tyroshi | 26.0 | main_or_minor_line |
| 42 | Sarnori Master Spearman | sarnor_master_spearman | 42.6 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | sarnor | 26.0 | main_or_minor_line |
| 43 | Ibbenese Timberman | ibbenese_timberman | 38.4 | 30.5 | 0.0 | nan | northern_javelin_1_t2 | False | Skirmishers | ibbenese | 26.0 | main_or_minor_line |
| 44 | Pentoshi Spearman | pentoshi_spearman | 38.2 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | pentoshi | 26.0 | main_or_minor_line |
| 45 | Martell Spearman | martell_spearman | 37.8 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 46 | Ghiscari Legionnaire | ghiscari_unsullied_hoplite | 37.6 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | ghiscari | 21.0 | main_or_minor_line |
| 47 | Free Folk Wildling Berzerker | freefolk_wildling_berzerker | 37.4 | 30.5 | 0.0 | nan | northern_javelin_1_t2 | False | Skirmishers | freefolk | 26.0 | main_or_minor_line |
| 48 | Black Goat Warrior | qohorik_goat_warrior | 36.2 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | qohorik | 21.0 | main_or_minor_line |
| 49 | Stormlands Elite Maceman | stormlands_crusher | 35.2 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | stormlands | 26.0 | main_or_minor_line |
| 50 | Tyroshi Quartermaster | tyroshi_quartermaster | 33.2 | 30.5 | 0.0 | nan | generic_javelin_1_t3 | False | Skirmishers | tyroshi | 21.0 | main_or_minor_line |
| 51 | Skagosi Rider | skagosi_rider | 33.1 | 30.5 | 0.0 | nan | generic_javelin_1_t3 | True | Skirmishers | skagosi | 21.0 | main_or_minor_line |
| 52 | Sarnori Elite Javelinier | sarnor_elite_javelinier | 33.0 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | sarnor | 21.0 | main_or_minor_line |
| 53 | Ibbenese Sailor | ibbenese_sailor | 32.7 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | ibbenese | 21.0 | main_or_minor_line |
| 54 | Qartheen Pureborn Warrior | qartheen_pureborn_warrior | 32.4 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | qartheen | 21.0 | main_or_minor_line |
| 55 | Free Folk Spearman | freefolk_spearman | 30.6 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | freefolk | 21.0 | main_or_minor_line |
| 56 | Free Folk Berzerker | freefolk_berzerker | 25.3 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | freefolk | 21.0 | main_or_minor_line |
| 57 | Ghiscari Soldier | ghiscari_soldier | 25.2 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | ghiscari | 21.0 | main_or_minor_line |
| 58 | Stormlands Maceman | stormlands_basher | 24.7 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | stormlands | 21.0 | main_or_minor_line |
| 59 | Black Goat Initiate | qohorik_goat_initiate | 21.9 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | qohorik | 16.0 | main_or_minor_line |
| 60 | Yronwood Man at Arms | yronwood_man_at_arms | 21.0 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 61 | Sarnori Javelineer | sarnor_javelinier | 20.7 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | sarnor | 16.0 | main_or_minor_line |
| 62 | Tyroshi Boatswain | tyroshi_boatswain | 18.6 | 30.5 | 0.0 | nan | generic_javelin_1_t3 | False | Skirmishers | tyroshi | 16.0 | main_or_minor_line |
| 63 | Martell Footman | martell_footman | 17.0 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 64 | Squire | dragonstone_squire | 16.2 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | dragonstone | 16.0 | main_or_minor_line |
| 65 | Summer Isles Spearmaster | summer_pikeman | 12.4 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | summer | 26.0 | main_or_minor_line |
| 66 | Skagosi Barbarian | skag_barbarian | 6.8 | 30.5 | 0.0 | nan | generic_javelin_1_t3 | False | Skirmishers | skagosi | 26.0 | main_or_minor_line |
| 67 | Mormont Woodswoman | mormont_woodswoman | 2.9 | 30.5 | 0.0 | nan | northern_javelin_1_t2 | False | Skirmishers | battania | 11.0 | main_or_minor_line |

