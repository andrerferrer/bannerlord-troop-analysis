# Troop overview — `realm_of_thrones` / `export_20260729_025002`

## Labels

- `evidence_basis=xml_structural`, `empirical=false` (ADR-004)
- Model: `role_scores_v1` conservative (crafted melee = proxy, not HTK)
- Package digest: `afef4c8483d4d27a228f13c78ed84f89fd624f9e7103d2801b1cec065eee767f`
- Rows scored: **1232**; after filters: **726** (excluded 506: specials, spectacle names, and untouched vanilla `change_type=inalterado`)

## Filters

- Drop `line_status=special_or_unlinked`
- Drop troop names matching Giant / Mammoth / Dragon / Direwolf / Kraken
- Drop `change_type=inalterado` from the track override report (vanilla baseline troops that the mod did not add/override)
- Intra-track only; do not compare ranks across tracks

## Top 20 — Ranged

| rank | troop_name | troop_id | ranged_role_score | primary_category | culture | level |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Myrish Artisan of War | myrish_artisan | 88.1 | Ranged Troops | myrish | 31.0 |
| 2 | Qartheen Enthroned Guardian | enthroned_guardian | 85.7 | Ranged Troops | qartheen | 31.0 |
| 3 | Ravens' Teeth | ravens_teeth | 84.7 | Ranged Troops | river | 31.0 |
| 4 | Frey Assassin | frey_assassin | 83.2 | Ranged Troops | river | 31.0 |
| 5 | Goldenheart Warrior | summer_master_longbowman | 80.8 | Ranged Troops | summer | 31.0 |
| 6 | Mormont Bowmaiden | mormont_bowmaiden | 75.6 | Ranged Troops | battania | 31.0 |
| 7 | Greyjoy Sniper | greyjoy_sniper | 75.0 | Ranged Troops | sturgia | 31.0 |
| 8 | Triarch Guardian | triarch_guardian | 54.3 | Ranged Troops | volantine | 31.0 |
| 9 | Night's Watch Protector of the Realm | nightswatch_protector | 52.1 | Ranged Troops | nightswatch | 31.0 |
| 10 | Mormont Mounted Huntress | mormont_mounted_huntress | 48.3 | Ranged Troops | battania | 26.0 |
| 11 | Qartheen Pureborn Champion | qartheen_champion | 45.3 | Ranged Troops | qartheen | 26.0 |
| 12 | Myrish Master Crossbowman | myrish_master_crossbowman | 44.5 | Ranged Troops | myrish | 26.0 |
| 13 | Pentoshi Mounted Archer | pentoshi_mounted_archer | 42.6 | Ranged Troops | pentoshi | 26.0 |
| 14 | Gilded Bolt Rangers | golden_master_crossbowman | 40.7 | Ranged Troops | volantine | 26.0 |
| 15 | Qartheen Longbowman | qartheen_longbowman | 40.3 | Ranged Troops | qartheen | 26.0 |
| 16 | Frey Sharpshooter | frey_sharpshooter | 39.6 | Ranged Troops | river | 26.0 |
| 17 | Hightower Marksmen | hightower_marksman | 38.2 | Ranged Troops | reach | 26.0 |
| 18 | Velaryon Marksman | velaryon_marksman | 38.1 | Ranged Troops | dragonstone | 26.0 |
| 19 | Tarth Elite Crossbowman | tarth_elite_crossbowman | 37.5 | Ranged Troops | stormlands | 26.0 |
| 20 | Casterly Rock Master Crossbowman | casterly_master_crossbowman | 36.7 | Ranged Troops | vlandia | 26.0 |


## Top 20 — Defensive

| rank | troop_name | troop_id | defensive_role_score | primary_category | culture | level |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Golden Company Mahout | golden_elite_pikeman | 100.0 | Skirmishers | volantine | 31.0 |
| 2 | Golden Company Elephant Rider | golden_horseman | 94.3 | Defensive Troops | volantine | 26.0 |
| 3 | Volantene Mahout | tigercloak_camel_cavalry | 83.3 | Defensive Troops | volantine | 26.0 |
| 4 | Captain of the Kingsguard | mounted_kingsguard | 71.9 | Defensive Troops | crownlands | 31.0 |
| 5 | Mallister Eagle Knight | mallister_knight | 71.4 | Defensive Troops | river | 31.0 |
| 6 | Captain of the Queen's Guard | queensguard_captain | 70.0 | Defensive Troops | valyrian | 31.0 |
| 7 | Stark Cavalry | stark_cavalry | 69.9 | Defensive Troops | battania | 26.0 |
| 8 | Valyrian Cavalry | targaryen_dragonknight | 69.9 | Skirmishers | valyrian | 26.0 |
| 9 | Targaryen Queen's Guard | targ_queensguard | 69.7 | Defensive Troops | valyrian | 26.0 |
| 10 | Arryn Winged Knight | arryn_moonknight | 68.8 | Defensive Troops | vale | 31.0 |
| 11 | Dondarrion Boltknight | dondarion_boltknight | 68.4 | Defensive Troops | stormlands | 31.0 |
| 12 | Magister Guard Elite | magister_guard | 68.2 | Skirmishers | pentoshi | 31.0 |
| 13 | Lannister Prideknight | lannister_prideknight | 68.0 | Defensive Troops | vlandia | 31.0 |
| 14 | Grafton Horseman | grafton_horseman | 68.0 | Defensive Troops | vale | 26.0 |
| 15 | Lannister Knight | lannister_knight | 67.8 | Defensive Troops | vlandia | 26.0 |
| 16 | White Harbor Knight Commander | whiteharbor_knight_commander | 67.8 | Defensive Troops | battania | 31.0 |
| 17 | White Harbor Elite Knight | whiteharbor_elite_knight | 67.4 | Defensive Troops | battania | 26.0 |
| 18 | Realm Knight | realm_knight | 67.4 | Skirmishers | crownlands | 26.0 |
| 19 | Westerling Knight | westerling_horseman | 66.9 | Defensive Troops | vlandia | 26.0 |
| 20 | Dondarrion Knight | dondarion_knight | 66.7 | Defensive Troops | stormlands | 26.0 |


## Top 20 — Offensive melee

| rank | troop_name | troop_id | offensive_melee_role_score | primary_category | culture | level |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Captain of the Kingsguard | mounted_kingsguard | 100.0 | Defensive Troops | crownlands | 31.0 |
| 2 | Yi Ti Mounted Shi | yiti_samurai | 98.4 | Skirmishers | yiti | 31.0 |
| 3 | Mountain's Man | mountains_man | 88.9 | Offensive Melee | vlandia | 31.0 |
| 4 | Stormlands Thunder Knight | stormlands_thunderknight | 88.4 | Defensive Troops | stormlands | 31.0 |
| 5 | Golden Company Mahout | golden_elite_pikeman | 85.9 | Skirmishers | volantine | 31.0 |
| 6 | Ghiscari Lockstep Legionnaire | ghiscari_unsullied_unbroken | 85.1 | Skirmishers | ghiscari | 31.0 |
| 7 | Riverlands Admiral | river_admiral | 81.3 | Defensive Troops | river | 31.0 |
| 8 | Arryn Winged Knight | arryn_moonknight | 80.5 | Defensive Troops | vale | 31.0 |
| 9 | White Harbor Knight Commander | whiteharbor_knight_commander | 80.3 | Defensive Troops | battania | 31.0 |
| 10 | Mallister Eagle Knight | mallister_knight | 77.6 | Defensive Troops | river | 31.0 |
| 11 | Dondarrion Boltknight | dondarion_boltknight | 77.1 | Defensive Troops | stormlands | 31.0 |
| 12 | Lannister Prideknight | lannister_prideknight | 77.1 | Defensive Troops | vlandia | 31.0 |
| 13 | Royce Heroine | royce_heroine | 76.7 | Defensive Troops | vale | 31.0 |
| 14 | Knights of Starfall | dayne_starfall_knights | 76.6 | Skirmishers | aserai | 31.0 |
| 15 | Water Gardens Sentinel | garden_sentinel | 75.9 | Skirmishers | aserai | 31.0 |
| 16 | Boneway Guardian | boneway_guardian | 75.8 | Skirmishers | aserai | 31.0 |
| 17 | Reach Flower Knight | reach_flower_knight | 73.4 | Defensive Troops | reach | 31.0 |
| 18 | Knight of the Vale | vale_knight_of | 73.2 | Defensive Troops | vale | 31.0 |
| 19 | Realm Paladin | realm_paladin | 73.2 | Skirmishers | crownlands | 31.0 |
| 20 | Tyrell Cavalier | tyrell_cavalier | 73.0 | Defensive Troops | reach | 31.0 |


## Top 20 — Skirmisher

| rank | troop_name | troop_id | skirmisher_role_score | primary_category | culture | level |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Golden Company Mahout | golden_elite_pikeman | 100.0 | Skirmishers | volantine | 31.0 |
| 2 | Yi Ti Mounted Shi | yiti_samurai | 90.8 | Skirmishers | yiti | 31.0 |
| 3 | Magister Guard Elite | magister_guard | 89.6 | Skirmishers | pentoshi | 31.0 |
| 4 | Knights of Starfall | dayne_starfall_knights | 89.0 | Skirmishers | aserai | 31.0 |
| 5 | Realm Paladin | realm_paladin | 88.8 | Skirmishers | crownlands | 31.0 |
| 6 | Black Goat Sacrificer | qohorik_goat_sacrificer | 88.6 | Skirmishers | qohorik | 31.0 |
| 7 | Queen's Man | dragonstone_steel_curtain | 88.4 | Skirmishers | dragonstone | 31.0 |
| 8 | Water Gardens Sentinel | garden_sentinel | 87.4 | Skirmishers | aserai | 31.0 |
| 9 | Skagosi Stoneborn Champion | skagosi_stoneborn_champion | 87.3 | Skirmishers | skagosi | 31.0 |
| 10 | Boneway Guardian | boneway_guardian | 87.2 | Skirmishers | aserai | 31.0 |
| 11 | Sarnori Spider | sarnor_spider | 83.4 | Skirmishers | sarnor | 31.0 |
| 12 | Valyrian Cavalry | targaryen_dragonknight | 72.1 | Skirmishers | valyrian | 26.0 |
| 13 | Ghiscari Lockstep Legionnaire | ghiscari_unsullied_unbroken | 71.0 | Skirmishers | ghiscari | 31.0 |
| 14 | Tarly Vanguard | tarly_vanguard | 68.4 | Skirmishers | reach | 31.0 |
| 15 | Realm Knight | realm_knight | 67.8 | Skirmishers | crownlands | 26.0 |
| 16 | Celtigar Banneret | celtigar_banneret | 67.6 | Skirmishers | dragonstone | 31.0 |
| 17 | Ibbenese Navigator | ibbenese_navigator | 66.7 | Skirmishers | ibbenese | 31.0 |
| 18 | Greyjoy Horseman | greyjoy_horseman | 66.4 | Skirmishers | sturgia | 26.0 |
| 19 | Glover Bushranger | glover_bushranger | 66.2 | Skirmishers | battania | 31.0 |
| 20 | Skagosi Stoneborn | skagosi_stoneborn | 65.4 | Skirmishers | skagosi | 26.0 |

