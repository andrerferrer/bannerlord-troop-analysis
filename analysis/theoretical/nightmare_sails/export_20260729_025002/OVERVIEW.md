# Troop overview — `nightmare_sails` / `export_20260729_025002`

## Labels

- `evidence_basis=xml_structural`, `empirical=false` (ADR-004)
- Model: `role_scores_v1` conservative (crafted melee = proxy, not HTK)
- Package digest: `afef4c8483d4d27a228f13c78ed84f89fd624f9e7103d2801b1cec065eee767f`
- Rows scored: **371**; after filters: **270** (excluded 101: untouched vanilla `change_type=inalterado` only)

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

## Field empiria (reliable rows only)

From `2026-07-28-to-29-nightmare-sails-field` — descriptive kills/deployed, not the same as role_scores_v1.

| context | rank | display_name | provisional_slug | canonical_troop_id | identity_status | independent_battles | deployed | survivors | kills | deaths | wounded | routed | kills_per_deployed | death_rate | casualty_rate | ci95_low | ci95_high | reliability_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| field | 1 | Nord Huscarl [T6] | nord_huscarl | nord_huscarl | confirmed_id | 6 | 25 | 20 | 78 | 1 | 4 | 0 | 3.1 | 0.0 | 0.2 | 2.7 | 3.5 | reliable |
| field | 2 | Battanian Wildling [T5] | battanian_wildling | battanian_wildling | confirmed_id | 8 | 34 | 26 | 91 | 0 | 8 | 0 | 2.7 | 0.0 | 0.2 | 2.1 | 3.3 | reliable |
| field | 3 | Forest Reaper [T5] | forest_reaper | forest_bandits_bossen | confirmed_id | 6 | 24 | 24 | 33 | 0 | 0 | 0 | 1.4 | 0.0 | 0.0 | 0.9 | 1.8 | reliable |
| field | 4 | Imperial Elite Cataphract [T6] | imperial_elite_cataphract | imperial_elite_cataphract | confirmed_id | 7 | 140 | 129 | 189 | 1 | 10 | 0 | 1.4 | 0.0 | 0.1 | 0.9 | 1.8 | reliable |
| field | 5 | Veteran Outrider [T5] | veteran_outrider | eastern_mounted_mercenary_t5 | confirmed_id | 5 | 39 | 38 | 36 | 0 | 1 | 0 | 0.9 | 0.0 | 0.0 | 0.4 | 1.4 | reliable |
| field | 6 | Khuzait Khan's Guard [T6] | khuzait_khans_guard | khuzait_khans_guard | confirmed_id | 7 | 112 | 111 | 99 | 0 | 1 | 0 | 0.9 | 0.0 | 0.0 | 0.3 | 1.6 | reliable |
| field | 7 | Imperial Trained Infantryman [T3] | imperial_trained_infantryman | nan | unresolved | 5 | 41 | 39 | 32 | 0 | 2 | 0 | 0.8 | 0.0 | 0.0 | 0.6 | 1.0 | reliable |


## Ranked — Ranged (70 troops)

| rank | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | has_horse | has_shield | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Khuzait Khan's Guard | khuzait_khans_guard | 100.0 | 83.1 | 56.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 31.0 | noble_line |
| 2 | Battanian Fian Champion | battanian_fian_champion | 98.0 | 94.3 | 71.0 | woodland_longbow | False | False | Ranged Troops | battania | 31.0 | noble_line |
| 3 | Battanian Fian | battanian_fian | 74.9 | 94.3 | 71.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | noble_line |
| 4 | Khuzait Kheshig | khuzait_kheshig | 69.0 | 83.1 | 56.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 26.0 | noble_line |
| 5 | Aserai Mamluke Heavy Cavalry | aserai_mameluke_heavy_cavalry | 66.9 | 79.9 | 58.0 | steppe_war_bow | True | True | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 6 | Vlandian Sharpshooter | vlandian_sharpshooter | 62.6 | 100.0 | 102.0 | crossbow_f | False | True | Ranged Troops | vlandia | 26.0 | special_or_unlinked |
| 7 | Conspiracy Warworn Crossbowman | conspiracy_warworn_crossbowman | 61.4 | 97.6 | 102.0 | crossbow_f | False | True | Ranged Troops | vlandia | 26.0 | special_or_unlinked |
| 8 | Veteran Eleftheroi | eleftheroi_tier_3 | 61.1 | 87.5 | 87.0 | crossbow_g | True | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 9 | Nord Sky-Gods Chosen | nord_skathi | 59.8 | 91.1 | 70.0 | lowland_yew_bow | False | True | Ranged Troops | nord | 26.0 | main_or_minor_line |
| 10 | Imperial Bucellarii | bucellarii | 59.4 | 84.4 | 57.0 | steppe_war_bow | True | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 11 | Khuzait Heavy Horse Archer | khuzait_heavy_horse_archer | 56.8 | 79.2 | 54.0 | composite_steppe_bow | True | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 12 | Conspiracy Longbowman | conspiracy_longbowman | 54.6 | 94.3 | 71.0 | woodland_longbow | False | False | Ranged Troops | battania | 26.0 | special_or_unlinked |
| 13 | Karakhergit Elder | karakhuzaits_tier_3 | 53.4 | 77.5 | 55.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 14 | Aserai Bahriyyah | aserai_marine_t5 | 52.4 | 95.7 | 74.0 | longbow_recurve_desert_bow | False | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 15 | Vlandian Marinier | vlandian_marine_t5 | 51.6 | 92.9 | 90.0 | crossbow_g | False | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 16 | Aserai Mamluke Cavalry | aserai_mameluke_cavalry | 51.3 | 77.4 | 56.0 | steppe_heavy_bow | True | True | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 17 | Conspiracy Mounted Master Archer | conspiracy_mounted_master_archer | 49.8 | 81.5 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | khuzait | 26.0 | special_or_unlinked |
| 18 | Conspiracy Packmaster | conspiracy_packmaster | 49.4 | 83.8 | 56.0 | steppe_war_bow | True | False | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 19 | Chosen Wolf | wolfskins_tier_3 | 48.0 | 89.6 | 71.0 | woodland_longbow | False | True | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 20 | Sturgian Veteran Bowman | sturgian_veteran_bowman | 47.9 | 88.0 | 61.0 | nordic_shortbow | False | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 21 | Khuzait Marksman | khuzait_marksman | 47.0 | 93.3 | 72.0 | nomad_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 22 | Imperial Sergeant Boatsman | imperial_sergeant_crossbowman | 46.3 | 95.2 | 95.0 | crossbow_d | False | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 23 | Veteran Forester | forest_people_tier_3 | 45.8 | 93.0 | 70.0 | woodland_longbow | False | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 24 | Arboreal | brotherhood_of_woods_tier_3 | 45.6 | 93.9 | 71.0 | lowland_yew_bow | False | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 25 | Boar Champion | company_of_the_boar_tier_3 | 44.2 | 92.8 | 95.0 | crossbow_d | False | True | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 26 | Conspiracy Hunt Leader | conspiracy_hunt_leader | 44.0 | 79.4 | 57.0 | steppe_war_bow | False | False | Ranged Troops | empire | 26.0 | special_or_unlinked |
| 27 | Nord Marksman | nord_marksman | 43.8 | 91.1 | 70.0 | lowland_yew_bow | False | False | Ranged Troops | nord | 21.0 | main_or_minor_line |
| 28 | Imperial Palatine Guard | imperial_palatine_guard | 41.3 | 86.2 | 60.0 | lowland_longbow | False | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 29 | Battanian Hero | battanian_hero | 40.9 | 89.7 | 64.0 | woodland_yew_bow | False | False | Ranged Troops | battania | 21.0 | noble_line |
| 30 | Khuzait Horse Archer | khuzait_horse_archer | 38.6 | 80.6 | 54.0 | steppe_heavy_bow | True | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 31 | Karakhergit Rider | karakhuzaits_tier_2 | 37.0 | 75.1 | 53.0 | steppe_heavy_bow | True | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 32 | Khuzait Torguud | khuzait_torguud | 36.8 | 75.9 | 54.0 | steppe_heavy_bow | True | False | Ranged Troops | khuzait | 21.0 | noble_line |
| 33 | Expert Eleftheroi | eleftheroi_tier_2 | 36.0 | 81.5 | 79.0 | crossbow_e | True | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 34 | Khuzait Tengichi | khuzait_sailor | 33.9 | 79.2 | 54.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 35 | Seasoned Wolf | wolfskins_tier_2 | 30.6 | 85.0 | 64.0 | woodland_yew_bow | False | True | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 36 | Vlandian Seafarer | vlandian_marine_t4 | 30.4 | 88.6 | 89.0 | crossbow_g | False | True | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 37 | Khuzait Archer | khuzait_archer | 27.2 | 80.6 | 54.0 | steppe_heavy_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 38 | Expert Forester | forest_people_tier_2 | 27.1 | 88.0 | 61.0 | nordic_shortbow | False | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 39 | Sturgian Archer | sturgian_archer | 26.9 | 79.4 | 50.0 | nordic_shortbow2 | False | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 40 | Sapling | brotherhood_of_woods_tier_2 | 26.6 | 85.5 | 59.0 | lowland_longbow | False | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 41 | Boar Veteran | company_of_the_boar_tier_2 | 26.4 | 82.3 | 84.0 | crossbow_b | False | True | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 42 | Imperial Coastguard | imperial_crossbowman | 26.0 | 95.2 | 95.0 | crossbow_d | False | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 43 | Aserai Sahraq | aserai_marine_t4 | 23.7 | 86.9 | 62.0 | tribal_bow | False | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 44 | Imperial Veteran Archer | imperial_veteran_archer | 23.1 | 86.2 | 60.0 | lowland_longbow | False | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 45 | Khuzait Raider | khuzait_raider | 22.9 | 81.0 | 53.0 | composite_bow | True | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 46 | Battanian Highborn Warrior | battanian_highborn_warrior | 22.6 | 88.4 | 63.0 | woodland_yew_bow | False | False | Ranged Troops | battania | 16.0 | noble_line |
| 47 | Nord Freeman Archer | nord_freeman_archer | 22.3 | 85.5 | 62.0 | woodland_yew_bow | False | False | Ranged Troops | nord | 16.0 | main_or_minor_line |
| 48 | Khuzait Qanqli | khuzait_qanqli | 22.2 | 76.3 | 53.0 | composite_bow | True | False | Ranged Troops | khuzait | 16.0 | noble_line |
| 49 | Conspiracy Horse Archer | conspiracy_horse_archer | 19.4 | 80.6 | 54.0 | steppe_heavy_bow | True | False | Ranged Troops | khuzait | 16.0 | special_or_unlinked |
| 50 | Karakhergit Nomad | karakhuzaits_tier_1 | 17.7 | 66.6 | 43.0 | steppe_bow | True | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 51 | Conspiracy Mounted Hunstman | conspiracy_mounted_huntsman | 16.8 | 71.8 | 42.0 | hunting_bow | True | False | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 52 | Recruit Eleftheroi | eleftheroi_tier_1 | 16.7 | 72.6 | 69.0 | crossbow_a | True | False | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 53 | Conspiracy Trained Huntsman | conspiracy_trained_huntsman | 16.5 | 67.1 | 43.0 | hunting_bow|mountain_hunting_bow | False | False | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 54 | Conspiracy Trained Crossbowman | conspiracy_trained_crossbowman | 15.5 | 82.3 | 84.0 | crossbow_b | False | False | Ranged Troops | vlandia | 16.0 | special_or_unlinked |
| 55 | Conspiracy Trained Bowman | conspiracy_trained_bowman | 14.7 | 81.7 | 53.0 | composite_bow | False | False | Ranged Troops | aserai | 16.0 | special_or_unlinked |
| 56 | Boar Novice | company_of_the_boar_tier_1 | 14.0 | 82.3 | 84.0 | crossbow_b | False | True | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 57 | Khuzait Tribal Warrior | khuzait_tribal_warrior | 12.3 | 66.6 | 43.0 | steppe_bow | True | False | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 58 | Sturgian Hunter | sturgian_hunter | 11.9 | 79.4 | 50.0 | nordic_shortbow2 | False | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 59 | Khuzait Noble's Son | khuzait_noble_son | 11.6 | 66.6 | 43.0 | steppe_bow | True | False | Ranged Troops | khuzait | 11.0 | noble_line |
| 60 | Young Wolf | wolfskins_tier_1 | 11.2 | 72.8 | 50.0 | highland_ranger_bow | False | True | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 61 | Vlandian Shipmate | vlandian_infantry | 9.9 | 82.6 | 81.0 | crossbow_e | False | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 62 | Sprout | brotherhood_of_woods_tier_1 | 9.4 | 76.1 | 49.0 | highland_ranger_bow | False | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 63 | Khuzait Hunter | khuzait_hunter | 8.7 | 81.0 | 53.0 | composite_bow | False | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 64 | Recruit Forester | forest_people_tier_1 | 8.5 | 72.1 | 43.0 | mountain_hunting_bow | False | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 65 | Imperial Trained Archer | imperial_trained_archer | 8.3 | 80.1 | 54.0 | glen_ranger_bow | False | False | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 66 | Sea Hound Marksman | sea_hounds_marksman | 2.8 | 70.4 | 42.0 | mountain_hunting_bow | False | False | Ranged Troops | nord | 11.0 | special_or_unlinked |
| 67 | Nord Huntsman | nord_huntsman | 2.7 | 76.6 | 52.0 | glen_ranger_bow | False | False | Ranged Troops | nord | 11.0 | main_or_minor_line |
| 68 | Battanian Highborn Youth | battanian_highborn_youth | 2.5 | 76.1 | 49.0 | highland_ranger_bow | False | False | Ranged Troops | battania | 11.0 | noble_line |
| 69 | Vlandian Levy Crossbowman | vlandian_levy_crossbowman | 0.8 | 72.6 | 69.0 | crossbow_a | False | False | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 70 | Imperial Archer | imperial_archer | 0.7 | 76.8 | 50.0 | highland_ranger_bow | False | False | Ranged Troops | empire | 11.0 | main_or_minor_line |


## Ranked — Defensive (178 troops)

| rank | troop_name | troop_id | defensive_role_score | defense_score_base | armor_total | effective_armor | has_shield | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Imperial Elite Cataphract | imperial_elite_cataphract | 100.0 | 97.0 | 207.7 | 60.2 | True | True | Defensive Troops | empire | 31.0 | noble_line |
| 2 | Vlandian Banner Knight | vlandian_banner_knight | 98.9 | 97.4 | 202.0 | 58.6 | True | True | Defensive Troops | vlandia | 31.0 | noble_line |
| 3 | Sturgian Druzhinnik Champion | druzhinnik_champion | 96.7 | 94.8 | 208.0 | 57.9 | True | True | Defensive Troops | sturgia | 31.0 | noble_line |
| 4 | Sturgian Druzhinnik | druzhinnik | 93.6 | 90.0 | 188.3 | 53.1 | True | True | Defensive Troops | sturgia | 26.0 | noble_line |
| 5 | Aserai Vanguard Faris | aserai_vanguard_faris | 93.2 | 88.9 | 207.3 | 59.3 | True | True | Skirmishers | aserai | 31.0 | noble_line |
| 6 | Aserai Veteran Faris | aserai_veteran_faris | 90.9 | 86.1 | 194.3 | 57.2 | True | True | Skirmishers | aserai | 26.0 | noble_line |
| 7 | Imperial Cataphract | imperial_cataphract | 90.6 | 86.7 | 174.3 | 49.9 | True | True | Defensive Troops | empire | 26.0 | noble_line |
| 8 | Vlandian Champion | vlandian_champion | 89.9 | 87.0 | 171.0 | 52.0 | True | True | Defensive Troops | vlandia | 26.0 | noble_line |
| 9 | Conspiracy Battle Rider | conspiracy_battlerider | 85.9 | 82.4 | 170.0 | 53.5 | True | True | Skirmishers | sturgia | 26.0 | special_or_unlinked |
| 10 | Vlandian Vanguard | vlandian_vanguard | 83.2 | 76.7 | 153.7 | 43.0 | True | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 11 | Khuzait Heavy Lancer | khuzait_heavy_lancer | 81.0 | 77.5 | 187.7 | 54.4 | True | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 12 | Vlandian Knight | vlandian_knight | 79.9 | 75.0 | 161.7 | 43.1 | True | True | Defensive Troops | vlandia | 21.0 | noble_line |
| 13 | Battanian Horseman | battanian_horseman | 79.8 | 71.0 | 174.5 | 49.2 | True | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 14 | Sturgian Horse Raider | sturgian_horse_raider | 78.9 | 73.0 | 171.7 | 48.0 | True | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 15 | Imperial Heavy Horseman | imperial_heavy_horseman | 74.6 | 68.5 | 139.0 | 36.0 | True | True | Defensive Troops | empire | 21.0 | noble_line |
| 16 | Aserai Mamluke Heavy Cavalry | aserai_mameluke_heavy_cavalry | 73.8 | 70.4 | 167.0 | 42.5 | True | True | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 17 | Khuzait Lancer | khuzait_lancer | 72.7 | 67.5 | 135.0 | 43.3 | True | True | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 18 | Nord Huscarl | nord_huscarl | 71.7 | 72.8 | 204.4 | 62.0 | True | False | Defensive Troops | nord | 31.0 | main_or_minor_line |
| 19 | Ghilman | ghilman_tier_2 | 70.9 | 63.0 | 128.5 | 35.5 | True | True | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 20 | Aserai Mamluke Cavalry | aserai_mameluke_cavalry | 69.6 | 65.4 | 131.0 | 38.0 | True | True | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 21 | Battanian Mounted Skirmisher | battanian_mounted_skirmisher | 68.3 | 63.5 | 139.7 | 40.9 | True | True | Skirmishers | battania | 26.0 | special_or_unlinked |
| 22 | Ghulam | ghilman_tier_3 | 68.1 | 61.8 | 178.0 | 49.9 | True | True | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 23 | Vlandian Sergeant | vlandian_sergeant | 66.8 | 66.0 | 175.7 | 49.1 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 24 | Khuzait Heavy Horse Archer | khuzait_heavy_horse_archer | 65.4 | 60.5 | 129.0 | 39.4 | True | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 25 | Sturgian Heavy Spearman | sturgian_shock_troop | 64.8 | 63.2 | 189.0 | 53.3 | True | False | Skirmishers | sturgia | 26.0 | special_or_unlinked |
| 26 | Sturgian Hardened Brigand | sturgian_hardened_brigand | 64.8 | 57.6 | 118.0 | 35.8 | True | True | Skirmishers | sturgia | 21.0 | main_or_minor_line |
| 27 | Nord Shield-Companion | nord_hirdmann | 64.5 | 59.7 | 159.4 | 50.1 | True | False | Defensive Troops | nord | 26.0 | main_or_minor_line |
| 28 | Sturgian Heavy Axeman | sturgian_veteran_warrior | 63.7 | 68.0 | 211.7 | 58.6 | True | False | Defensive Troops | sturgia | 26.0 | special_or_unlinked |
| 29 | Vlandian Gallant | vlandian_gallant | 63.6 | 57.7 | 115.0 | 36.9 | True | True | Defensive Troops | vlandia | 16.0 | noble_line |
| 30 | Khuzait Khan's Guard | khuzait_khans_guard | 63.2 | 69.9 | 181.0 | 54.6 | False | True | Ranged Troops | khuzait | 31.0 | noble_line |
| 31 | Jawwal Bedouin | jawwal_tier_3 | 62.2 | 51.4 | 96.7 | 31.6 | True | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 32 | Imperial Legionary | imperial_legionary | 61.1 | 61.0 | 202.0 | 56.0 | True | False | Defensive Troops | empire | 26.0 | special_or_unlinked |
| 33 | Puppeteer | hidden_hand_tier_3 | 60.6 | 54.5 | 189.0 | 54.0 | True | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 34 | Aserai Mamluke Warden | aserai_master_archer | 59.5 | 59.1 | 186.7 | 53.8 | True | False | Defensive Troops | aserai | 26.0 | special_or_unlinked |
| 35 | Battanian Wildling | battanian_wildling | 59.4 | 61.7 | 186.3 | 58.2 | True | False | Skirmishers | battania | 26.0 | special_or_unlinked |
| 36 | Aserai Faris | aserai_faris | 59.2 | 51.3 | 104.3 | 37.8 | True | True | Skirmishers | aserai | 21.0 | noble_line |
| 37 | Nord Berserkir | nord_berserkr | 58.2 | 59.2 | 172.8 | 49.5 | True | False | Defensive Troops | nord | 26.0 | main_or_minor_line |
| 38 | Battanian Scout | battanian_scout | 58.0 | 50.0 | 109.3 | 36.3 | True | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 39 | Jawwal Camel Rider | jawwal_tier_2 | 57.5 | 43.5 | 60.8 | 24.2 | True | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 40 | Conspiracy Veteran Fighter | conspiracy_veteran_fighter | 57.2 | 56.0 | 178.0 | 50.5 | True | False | Defensive Troops | empire | 26.0 | special_or_unlinked |
| 41 | Training Master | tutorial_npc_basic_melee | 56.9 | 39.6 | 38.0 | 14.7 | True | True | Defensive Troops | battania | 10.0 | special_or_unlinked |
| 42 | Conspiracy Commander | imperial_conspiracy_boss | 56.7 | 32.0 | 110.0 | 30.5 | True | False | Defensive Troops | vlandia | 31.0 | special_or_unlinked |
| 43 | Triarii | legion_of_the_betrayed_tier_3 | 56.4 | 53.8 | 170.0 | 46.8 | True | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 44 | Vlandian Cavalry | vlandian_cavalry | 56.2 | 49.4 | 118.3 | 34.2 | True | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 45 | Conspiracy Mounted Fighter | conspiracy_mounted_fighter | 56.1 | 46.9 | 118.0 | 28.3 | True | True | Defensive Troops | empire | 26.0 | special_or_unlinked |
| 46 | Nord Hearthguard | nord_jarlsmann | 55.7 | 49.0 | 126.0 | 40.0 | True | False | Defensive Troops | nord | 21.0 | main_or_minor_line |
| 47 | Khuzait Darkhan | khuzait_darkhan | 55.3 | 55.8 | 171.3 | 49.5 | True | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 48 | Imperial Equite | imperial_equite | 54.2 | 45.8 | 96.7 | 30.6 | True | True | Defensive Troops | empire | 16.0 | noble_line |
| 49 | Aserai Tribal Horseman | aserai_tribal_horseman | 53.9 | 44.7 | 94.0 | 31.6 | True | True | Skirmishers | aserai | 16.0 | noble_line |
| 50 | Vlandian Sharpshooter | vlandian_sharpshooter | 53.4 | 54.7 | 160.0 | 42.8 | True | False | Ranged Troops | vlandia | 26.0 | special_or_unlinked |
| 51 | Khuzait Kheshig | khuzait_kheshig | 53.3 | 60.4 | 146.0 | 44.0 | False | True | Ranged Troops | khuzait | 26.0 | noble_line |
| 52 | Battanian Oathsworn | battanian_oathsworn | 52.9 | 53.5 | 168.0 | 49.1 | True | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 53 | Chosen Wolf | wolfskins_tier_3 | 52.7 | 51.6 | 137.7 | 45.3 | True | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 54 | Aserai Lieutenant | aserai_veteran_infantry | 52.6 | 54.3 | 165.0 | 48.4 | True | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 55 | Nord Sky-Gods Chosen | nord_skathi | 51.2 | 54.4 | 142.3 | 44.3 | True | False | Ranged Troops | nord | 26.0 | main_or_minor_line |
| 56 | Khuzait Horseman | khuzait_horseman | 51.1 | 42.3 | 94.7 | 28.3 | True | True | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 57 | Lake Rat Wrecker  | lakepike_tier_3 | 51.1 | 46.9 | 124.5 | 32.7 | True | False | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 58 | Beni Zilal Royal Guard | beni_zilal_tier_3 | 50.9 | 56.7 | 133.0 | 33.7 | False | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 59 | Sturgian Reaver | sturgia_marine_t5 | 50.8 | 54.2 | 174.7 | 50.6 | True | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 60 | Training Master | tutorial_npc_mounted_ai | 50.5 | 41.0 | 20.0 | 6.6 | True | True | Defensive Troops | battania | 4.0 | special_or_unlinked |
| 61 | Training Master | tutorial_npc_advanced_melee_normal | 50.5 | 41.0 | 20.0 | 6.6 | True | True | Defensive Troops | battania | 4.0 | special_or_unlinked |
| 62 | Skolder Veteran Broda | skolderbrotva_tier_3 | 50.2 | 46.8 | 105.0 | 32.6 | True | False | Skirmishers | nord | 26.0 | main_or_minor_line |
| 63 | Battanian Skipari | battanian_marine_t5 | 49.3 | 48.1 | 138.0 | 43.2 | True | False | Skirmishers | battania | 26.0 | main_or_minor_line |
| 64 | Imperial Sergeant Boatsman | imperial_sergeant_crossbowman | 48.5 | 48.4 | 139.3 | 43.7 | True | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 65 | Vlandian Swordsman | vlandian_swordsman | 48.2 | 49.8 | 135.3 | 39.7 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 66 | Conspiracy Guardian | conspiracy_guardian | 48.0 | 48.5 | 160.0 | 44.8 | True | False | Defensive Troops | aserai | 26.0 | special_or_unlinked |
| 67 | Battanian Picked Warrior | battanian_picked_warrior | 47.9 | 45.4 | 128.3 | 39.7 | True | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 68 | Conspiracy Mounted Master Archer | conspiracy_mounted_master_archer | 46.9 | 54.8 | 148.7 | 38.9 | False | True | Ranged Troops | khuzait | 26.0 | special_or_unlinked |
| 69 | Vlandian Squire | vlandian_squire | 46.8 | 35.9 | 45.0 | 14.3 | True | True | Defensive Troops | vlandia | 11.0 | noble_line |
| 70 | Nord Shield Biter | nord_boandi | 46.6 | 46.8 | 102.7 | 37.6 | True | False | Defensive Troops | nord | 21.0 | main_or_minor_line |
| 71 | Khuzait Torguud | khuzait_torguud | 46.0 | 53.4 | 123.5 | 37.4 | False | True | Ranged Troops | khuzait | 21.0 | noble_line |
| 72 | Conspiracy Kern | conspiracy_kern | 45.9 | 46.6 | 131.3 | 41.0 | True | False | Skirmishers | battania | 16.0 | special_or_unlinked |
| 73 | Khuzait Spear Infantry | khuzait_spear_infantry | 45.7 | 45.7 | 122.0 | 38.2 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 74 | Vlandian Light Cavalry | vlandian_light_cavalry | 45.7 | 35.8 | 77.0 | 22.1 | True | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 75 | Imperial Naute | empire_marine_t5 | 45.7 | 46.9 | 137.0 | 42.0 | True | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 76 | Conspiracy Warworn Crossbowman | conspiracy_warworn_crossbowman | 45.6 | 50.0 | 133.0 | 37.5 | True | False | Ranged Troops | vlandia | 26.0 | special_or_unlinked |
| 77 | Conspiracy Noble Horseman | conspiracy_noble_horseman | 45.4 | 34.2 | 71.3 | 17.7 | True | True | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 78 | Sturgian Veteran Shipman | sturgia_marine_t4 | 44.6 | 43.9 | 126.0 | 37.5 | True | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 79 | Karakhergit Elder | karakhuzaits_tier_3 | 44.2 | 51.5 | 142.0 | 44.2 | False | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 80 | Conspiracy Commander | anti_imperial_conspiracy_boss | 43.9 | 30.3 | 72.5 | 22.9 | True | False | Defensive Troops | sturgia | 31.0 | special_or_unlinked |
| 81 | Boar Champion | company_of_the_boar_tier_3 | 43.4 | 47.0 | 119.0 | 34.1 | True | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 82 | Vlandian Mercenary | vlandian_spearman | 43.0 | 37.1 | 106.7 | 32.0 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 83 | Imperial Bucellarii | bucellarii | 42.4 | 49.0 | 141.3 | 39.5 | False | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 84 | Conspiracy Fighter | conspiracy_fighter | 42.2 | 43.2 | 106.3 | 36.2 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 85 | Confident Contender | confident_contender_very_hard | 41.6 | 36.0 | 88.5 | 34.6 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 86 | Confident Contender | confident_contender_normal | 41.6 | 36.0 | 88.5 | 34.6 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 87 | Confident Contender | confident_contender_hard | 41.6 | 36.0 | 88.5 | 34.6 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 88 | Confident Contender | confident_contender_easy | 41.6 | 36.0 | 88.5 | 34.6 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 89 | Confident Contender | confident_contender | 41.6 | 36.0 | 88.5 | 34.6 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 90 | Imperial Vigla Recruit | imperial_vigla_recruit | 41.5 | 32.0 | 60.7 | 17.3 | True | True | Defensive Troops | empire | 11.0 | noble_line |
| 91 | Skolder Warrior Broda | skolderbrotva_tier_2 | 41.3 | 34.8 | 88.0 | 23.9 | True | False | Defensive Troops | nord | 21.0 | main_or_minor_line |
| 92 | Nord Axe Warrior | nord_axe_warrior | 40.8 | 38.5 | 101.6 | 32.0 | True | False | Defensive Troops | nord | 16.0 | main_or_minor_line |
| 93 | Headman's Troop | tutorial_placeholder_volunteer | 40.7 | 29.8 | 26.0 | 6.3 | True | True | Defensive Troops | empire | 21.0 | special_or_unlinked |
| 94 | Hardy Contender | hardy_contender_easy | 40.6 | 31.1 | 87.5 | 28.0 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 95 | Hardy Contender | hardy_contender_very_hard | 40.6 | 31.1 | 87.5 | 28.0 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 96 | Hardy Contender | hardy_contender_normal | 40.6 | 31.1 | 87.5 | 28.0 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 97 | Hardy Contender | hardy_contender_hard | 40.6 | 31.1 | 87.5 | 28.0 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 98 | Hardy Contender | hardy_contender | 40.6 | 31.1 | 87.5 | 28.0 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 99 | Aserai Mamluke Regular | aserai_mameluke_regular | 40.3 | 28.3 | 46.3 | 15.3 | True | True | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 100 | Aserai Boatswain | aserai_infantry | 40.2 | 40.1 | 126.0 | 38.0 | True | False | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 101 | Nord War-Proven | nord_thegn | 40.0 | 36.5 | 97.3 | 29.9 | True | False | Defensive Troops | nord | 16.0 | main_or_minor_line |
| 102 | Conspiracy Warmonger | conspiracy_warmonger | 39.9 | 42.4 | 109.0 | 36.8 | True | False | Defensive Troops | battania | 26.0 | special_or_unlinked |
| 103 | Nord Spear Warrior | nord_spear_warrior | 39.6 | 32.4 | 79.3 | 25.4 | True | False | Skirmishers | nord | 16.0 | main_or_minor_line |
| 104 | Khuzait Horse Archer | khuzait_horse_archer | 39.2 | 48.3 | 112.7 | 31.6 | False | True | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 105 | Imperial Coast Guard | empire_marine_t4 | 38.9 | 39.3 | 108.0 | 31.4 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 106 | Battanian River Raider | battanian_marine_t4 | 38.2 | 35.7 | 106.7 | 31.9 | True | False | Skirmishers | battania | 21.0 | main_or_minor_line |
| 107 | Conspiracy Raider | conspiracy_raider | 38.0 | 28.6 | 46.0 | 12.7 | True | True | Defensive Troops | battania | 16.0 | special_or_unlinked |
| 108 | Sturgian Brigand | sturgian_brigand | 37.9 | 38.0 | 92.0 | 31.0 | True | False | Skirmishers | sturgia | 16.0 | main_or_minor_line |
| 109 | Vlandian Militia Veteran Spearman | vlandian_militia_veteran_spearman | 37.1 | 24.8 | 49.0 | 14.2 | True | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 110 | Vlandian Seafarer | vlandian_marine_t4 | 36.4 | 35.1 | 78.7 | 23.4 | True | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 111 | Veteran Eleftheroi | eleftheroi_tier_3 | 36.3 | 41.2 | 83.3 | 28.8 | False | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 112 | Training Master | tutorial_npc_advanced_melee_easy | 35.9 | 29.3 | 29.0 | 9.9 | False | True | Defensive Troops | battania | 15.0 | special_or_unlinked |
| 113 | Khuzait Spearman | khuzait_spearman | 35.8 | 32.7 | 94.3 | 27.1 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 114 | Conspiracy Trained Spearman | conspiracy_trained_spearman | 35.6 | 31.2 | 74.0 | 21.8 | True | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 115 | Vlandian Footman | vlandian_footman | 35.0 | 32.2 | 68.7 | 20.1 | True | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 116 | Nord Scion | nord_ungmann | 35.0 | 27.0 | 79.0 | 22.3 | True | False | Defensive Troops | nord | 11.0 | main_or_minor_line |
| 117 | Seasoned Wolf | wolfskins_tier_2 | 34.9 | 31.6 | 90.0 | 24.7 | True | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 118 | Principes | legion_of_the_betrayed_tier_2 | 34.8 | 34.0 | 92.5 | 27.7 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 119 | Hastati | legion_of_the_betrayed_tier_1 | 34.4 | 30.2 | 54.2 | 20.1 | True | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 120 | Battanian Trained Warrior | battanian_trained_warrior | 34.3 | 30.1 | 95.0 | 25.7 | True | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 121 | Nord Militia Veteran Spearman | nord_militia_veteran_spearman | 34.3 | 29.9 | 63.8 | 20.8 | True | False | Defensive Troops | nord | 16.0 | special_or_unlinked |
| 122 | Conspiracy Packmaster | conspiracy_packmaster | 33.8 | 41.8 | 120.7 | 31.5 | False | True | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 123 | Aserai Youth | aserai_youth | 33.8 | 21.7 | 33.3 | 8.0 | True | True | Skirmishers | aserai | 11.0 | noble_line |
| 124 | Boar Veteran | company_of_the_boar_tier_2 | 33.7 | 30.8 | 77.0 | 23.7 | True | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 125 | Karakhergit Rider | karakhuzaits_tier_2 | 33.2 | 38.1 | 94.5 | 29.7 | False | True | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 126 | Khuzait Militia Veteran Spearman | khuzait_militia_veteran_spearman | 33.0 | 27.0 | 68.5 | 17.4 | True | False | Defensive Troops | khuzait | 16.0 | special_or_unlinked |
| 127 | Sturgian Militia Veteran Spearman | sturgian_militia_veteran_spearman | 32.9 | 24.0 | 58.5 | 16.4 | True | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 128 | Nord Warrior | nord_drengr | 32.0 | 26.2 | 61.7 | 18.3 | True | False | Defensive Troops | nord | 11.0 | main_or_minor_line |
| 129 | Imperial Shipmate | empire_marine_t3 | 31.9 | 30.5 | 82.0 | 25.3 | True | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 130 | Blaze | embers_of_flame_tier_3 | 31.9 | 33.7 | 126.0 | 30.8 | True | False | Defensive Troops | empire | 26.0 | main_or_minor_line |
| 131 | Dignified Contender | dignified_contender_hard | 31.8 | 28.5 | 79.0 | 26.3 | True | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 132 | Dignified Contender | dignified_contender | 31.8 | 28.5 | 79.0 | 26.3 | True | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 133 | Dignified Contender | dignified_contender_very_hard | 31.8 | 28.5 | 79.0 | 26.3 | True | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 134 | Dignified Contender | dignified_contender_easy | 31.8 | 28.5 | 79.0 | 26.3 | True | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 135 | Dignified Contender | dignified_contender_normal | 31.8 | 28.5 | 79.0 | 26.3 | True | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 136 | Bold Contender | bold_contender_easy | 31.7 | 24.7 | 51.5 | 20.7 | True | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 137 | Bold Contender | bold_contender | 31.7 | 24.7 | 51.5 | 20.7 | True | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 138 | Bold Contender | bold_contender_normal | 31.7 | 24.7 | 51.5 | 20.7 | True | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 139 | Bold Contender | bold_contender_hard | 31.7 | 24.7 | 51.5 | 20.7 | True | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 140 | Bold Contender | bold_contender_very_hard | 31.7 | 24.7 | 51.5 | 20.7 | True | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 141 | Koleman | ghilman_tier_1 | 31.7 | 21.4 | 22.0 | 5.8 | True | True | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 142 | Conspiracy Wilder | conspiracy_wilder | 31.6 | 31.0 | 73.0 | 26.6 | True | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 143 | Aserai Sailor | aserai_footman | 31.3 | 31.9 | 89.0 | 28.9 | True | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 144 | Young Wolf | wolfskins_tier_1 | 30.8 | 27.5 | 79.3 | 20.1 | True | False | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 145 | Imperial Militia Veteran Spearman | imperial_militia_veteran_spearman | 30.8 | 25.4 | 56.2 | 15.9 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 146 | Sturgian Crewman | sturgia_marine_t3 | 30.2 | 29.2 | 70.7 | 25.1 | True | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 147 | Khuzait Qanqli | khuzait_qanqli | 29.8 | 33.4 | 89.7 | 25.3 | False | True | Ranged Troops | khuzait | 16.0 | noble_line |
| 148 | Nord Militia Spearman | nord_militia_spearman | 29.4 | 23.5 | 44.5 | 13.6 | True | False | Defensive Troops | nord | 11.0 | special_or_unlinked |
| 149 | Aserai Mamluke Soldier | aserai_mameluke_soldier | 28.6 | 23.4 | 58.0 | 18.4 | True | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 150 | Boar Novice | company_of_the_boar_tier_1 | 28.5 | 24.7 | 53.0 | 19.7 | True | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 151 | Vlandian Militia Spearman | vlandian_militia_spearman | 28.5 | 21.6 | 34.5 | 10.6 | True | False | Defensive Troops | vlandia | 11.0 | special_or_unlinked |
| 152 | Aserai Militia Veteran Spearman | aserai_militia_veteran_spearman | 27.9 | 21.0 | 56.2 | 15.8 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 153 | Skolder Recruit | skolderbrotva_tier_1 | 27.4 | 21.4 | 43.2 | 12.6 | True | False | Defensive Troops | nord | 16.0 | main_or_minor_line |
| 154 | Battanian Clan Warrior | battanian_clanwarrior | 27.1 | 23.1 | 76.3 | 19.9 | True | False | Skirmishers | battania | 11.0 | main_or_minor_line |
| 155 | Karakhergit Nomad | karakhuzaits_tier_1 | 26.4 | 29.3 | 50.5 | 21.3 | False | True | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 156 | Battanian Militia Veteran Spearman | battanian_militia_veteran_spearman | 26.2 | 21.9 | 61.5 | 16.5 | True | False | Defensive Troops | battania | 16.0 | special_or_unlinked |
| 157 | Conspiracy Mounted Hunstman | conspiracy_mounted_huntsman | 25.1 | 31.4 | 81.0 | 21.4 | False | True | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 158 | Battanian Wood Runner | battanian_woodrunner | 24.9 | 21.1 | 63.7 | 17.6 | True | False | Skirmishers | battania | 11.0 | main_or_minor_line |
| 159 | Sturgian Militia Spearman | sturgian_militia_spearman | 24.4 | 20.2 | 39.2 | 8.9 | True | False | Defensive Troops | sturgia | 11.0 | special_or_unlinked |
| 160 | Beni Zilal Soldier | beni_zilal_tier_2 | 24.4 | 25.4 | 45.8 | 16.4 | False | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 161 | Conspiracy Horse Archer | conspiracy_horse_archer | 24.1 | 30.8 | 64.3 | 22.3 | False | True | Ranged Troops | khuzait | 16.0 | special_or_unlinked |
| 162 | Sturgian Warrior | sturgian_warrior | 23.3 | 22.3 | 58.3 | 18.1 | True | False | Defensive Troops | sturgia | 11.0 | main_or_minor_line |
| 163 | Aserai Cadet | aserai_tribesman | 23.2 | 18.7 | 43.7 | 14.4 | True | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 164 | Khuzait Tribal Warrior | khuzait_tribal_warrior | 22.4 | 25.8 | 47.3 | 15.4 | False | True | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 165 | Khuzait Raider | khuzait_raider | 20.8 | 26.1 | 51.0 | 17.2 | False | True | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 166 | Battanian Militia Spearman | battanian_militia_spearman | 20.7 | 13.4 | 37.2 | 9.4 | True | False | Defensive Troops | battania | 11.0 | special_or_unlinked |
| 167 | Lake Rat Recruit | lakepike_tier_1 | 20.6 | 16.5 | 29.8 | 11.4 | True | False | Skirmishers | sturgia | 16.0 | main_or_minor_line |
| 168 | Khuzait Footman | khuzait_footman | 20.1 | 16.4 | 36.0 | 11.4 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 169 | Jawwal Recruit | jawwal_tier_1 | 20.0 | 13.7 | 23.4 | 8.4 | True | False | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 170 | Expert Eleftheroi | eleftheroi_tier_2 | 19.6 | 23.4 | 45.0 | 14.3 | False | True | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 171 | Conspiracy Guardsman | conspiracy_guardsman | 18.0 | 13.9 | 45.0 | 8.0 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 172 | Aserai Militia Spearman | aserai_militia_spearman | 17.7 | 12.0 | 28.5 | 6.7 | True | False | Defensive Troops | aserai | 11.0 | special_or_unlinked |
| 173 | Beni Zilal Recruit | beni_zilal_tier_1 | 17.1 | 17.9 | 26.3 | 9.0 | False | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 174 | Khuzait Militia Spearman | khuzait_militia_spearman | 16.3 | 11.5 | 28.8 | 6.9 | True | False | Defensive Troops | khuzait | 11.0 | special_or_unlinked |
| 175 | Khuzait Noble's Son | khuzait_noble_son | 15.9 | 21.6 | 36.3 | 10.7 | False | True | Ranged Troops | khuzait | 11.0 | noble_line |
| 176 | Recruit Eleftheroi | eleftheroi_tier_1 | 14.8 | 15.6 | 24.0 | 6.4 | False | True | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 177 | Imperial Militia Spearman | imperial_militia_spearman | 14.4 | 9.6 | 17.5 | 4.0 | True | False | Defensive Troops | empire | 11.0 | special_or_unlinked |
| 178 | Veteran Borrowed Troop | veteran_borrowed_troop | 11.5 | 8.7 | 10.0 | 3.0 | True | False | Defensive Troops | empire | 11.0 | main_or_minor_line |


## Ranked — Offensive melee (225 troops)

| rank | troop_name | troop_id | offensive_melee_role_score | crafted_melee_score_base | crafted_melee_template | crafted_melee_item | defense_score_base | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Battanian Fian Champion | battanian_fian_champion | 94.2 | 100.0 | TwoHandedSword | battania_2hsword_5_t4 | 51.0 | False | Ranged Troops | battania | 31.0 | noble_line |
| 2 | Vlandian Banner Knight | vlandian_banner_knight | 78.3 | 60.5 | TwoHandedPolearm | nord_spear_4_t5 | 97.4 | True | Defensive Troops | vlandia | 31.0 | noble_line |
| 3 | Imperial Elite Cataphract | imperial_elite_cataphract | 77.8 | 60.5 | TwoHandedPolearm | empire_lance_3_t5 | 97.0 | True | Defensive Troops | empire | 31.0 | noble_line |
| 4 | Khuzait Khan's Guard | khuzait_khans_guard | 67.2 | 60.5 | TwoHandedPolearm | khuzait_polearm_1_t4 | 69.9 | True | Ranged Troops | khuzait | 31.0 | noble_line |
| 5 | Conspiracy Commander | imperial_conspiracy_boss | 65.1 | 60.5 | OneHandedSword|TwoHandedPolearm | empire_sword_5_t4|imperial_throwing_spear_1_t4 | 32.0 | False | Defensive Troops | vlandia | 31.0 | special_or_unlinked |
| 6 | Aserai Vanguard Faris | aserai_vanguard_faris | 64.5 | 60.5 | TwoHandedPolearm | aserai_lance_1_t5 | 88.9 | True | Skirmishers | aserai | 31.0 | noble_line |
| 7 | Sturgian Druzhinnik Champion | druzhinnik_champion | 62.7 | 60.5 | TwoHandedPolearm | sturgia_lance_2_t5 | 94.8 | True | Defensive Troops | sturgia | 31.0 | noble_line |
| 8 | Nord Huscarl | nord_huscarl | 62.4 | 60.5 | TwoHandedPolearm | nord_spear_3_t5 | 72.8 | False | Defensive Troops | nord | 31.0 | main_or_minor_line |
| 9 | Conspiracy Knight | conspiracy_knight | 62.2 | 100.0 | TwoHandedSword | western_2hsword_t4 | 49.7 | False | Offensive Melee | vlandia | 26.0 | special_or_unlinked |
| 10 | Battanian Fian | battanian_fian | 60.4 | 100.0 | TwoHandedSword | battania_2hsword_5_t4 | 36.6 | False | Ranged Troops | battania | 26.0 | noble_line |
| 11 | Khuzait Tengri | khuzait_Tengri | 60.3 | 100.0 | OneHandedSword|TwoHandedPolearm|TwoHandedSword | khu_sailorglav_1_t5|khu_teng_sword_1_t5|ridged_3hsword_t4 | 37.9 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 12 | Vlandian Captain | vlandian_pikeman | 57.4 | 100.0 | TwoHandedAxe|TwoHandedSword | vlandia_2haxe_2_t5|vlandia_2hsword_1_t5 | 40.4 | False | Offensive Melee | vlandia | 26.0 | main_or_minor_line |
| 13 | Battanian Veteran Falxman | battanian_veteran_falxman | 56.8 | 100.0 | TwoHandedSword | battania_2hsword_4_t4 | 39.4 | False | Offensive Melee | battania | 26.0 | main_or_minor_line |
| 14 | Vlandian Marinier | vlandian_marine_t5 | 56.4 | 100.0 | TwoHandedSword | western_2hsword_t4 | 35.3 | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 15 | Imperial Cataphract | imperial_cataphract | 54.5 | 60.5 | TwoHandedPolearm | empire_lance_3_t5 | 86.7 | True | Defensive Troops | empire | 26.0 | noble_line |
| 16 | Vlandian Champion | vlandian_champion | 54.5 | 60.5 | TwoHandedPolearm | vlandia_lance_3_t5 | 87.0 | True | Defensive Troops | vlandia | 26.0 | noble_line |
| 17 | Conspiracy Battle Rider | conspiracy_battlerider | 53.7 | 60.5 | TwoHandedPolearm | sturgia_lance_1_t4 | 82.4 | True | Skirmishers | sturgia | 26.0 | special_or_unlinked |
| 18 | Sturgian Druzhinnik | druzhinnik | 52.6 | 60.5 | TwoHandedPolearm | sturgia_lance_1_t4 | 90.0 | True | Defensive Troops | sturgia | 26.0 | noble_line |
| 19 | Khuzait Tengichi | khuzait_sailor | 51.9 | 100.0 | TwoHandedSword | ridged_3hsword_t4 | 29.7 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 20 | Imperial Heavy Horseman | imperial_heavy_horseman | 49.8 | 60.5 | TwoHandedPolearm | western_spear_4_t4 | 68.5 | True | Defensive Troops | empire | 21.0 | noble_line |
| 21 | Headman's Troop | tutorial_placeholder_volunteer | 49.7 | 60.5 | TwoHandedPolearm | western_spear_3_t3 | 29.8 | True | Defensive Troops | empire | 21.0 | special_or_unlinked |
| 22 | Conspiracy Mounted Fighter | conspiracy_mounted_fighter | 49.5 | 60.5 | TwoHandedPolearm | western_spear_4_t4 | 46.9 | True | Defensive Troops | empire | 26.0 | special_or_unlinked |
| 23 | Ghulam | ghilman_tier_3 | 48.9 | 60.5 | TwoHandedPolearm | western_spear_5_t4 | 61.8 | True | Defensive Troops | aserai | 26.0 | main_or_minor_line |
| 24 | Flame | embers_of_flame_tier_2 | 48.5 | 100.0 | TwoHandedSword | justicier_2hsword | 21.6 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 25 | Battanian Hero | battanian_hero | 47.2 | 100.0 | TwoHandedSword | battania_2hsword_3_t3 | 28.0 | False | Ranged Troops | battania | 21.0 | noble_line |
| 26 | Aserai Veteran Faris | aserai_veteran_faris | 47.1 | 60.5 | TwoHandedPolearm | aserai_lance_1_t5 | 86.1 | True | Skirmishers | aserai | 26.0 | noble_line |
| 27 | Nord Shield-Companion | nord_hirdmann | 46.8 | 60.5 | TwoHandedPolearm | nord_spear_3_t5 | 59.7 | False | Defensive Troops | nord | 26.0 | main_or_minor_line |
| 28 | Vlandian Vanguard | vlandian_vanguard | 46.2 | 60.5 | TwoHandedPolearm | vlan_lance_1_t3 | 76.7 | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 29 | Khuzait Heavy Lancer | khuzait_heavy_lancer | 45.9 | 60.5 | TwoHandedPolearm | khu_spear_2_t5 | 77.5 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 30 | Battanian Horseman | battanian_horseman | 45.7 | 60.5 | TwoHandedPolearm | highland_spear_4_t4 | 71.0 | True | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 31 | Sturgian Horse Raider | sturgian_horse_raider | 45.4 | 60.5 | TwoHandedPolearm | northern_spear_4_t4 | 73.0 | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 32 | Conspiracy Commander | anti_imperial_conspiracy_boss | 45.4 | 41.6 | OneHandedAxe | sturgia_axe_4_t4 | 30.3 | False | Defensive Troops | sturgia | 31.0 | special_or_unlinked |
| 33 | Khuzait Kheshig | khuzait_kheshig | 44.0 | 60.5 | TwoHandedPolearm | khuzait_polearm_1_t4 | 60.4 | True | Ranged Troops | khuzait | 26.0 | noble_line |
| 34 | Battanian Falxman | battanian_falxman | 43.7 | 100.0 | TwoHandedSword | battania_2hsword_6 | 30.7 | False | Skirmishers | battania | 21.0 | main_or_minor_line |
| 35 | Beni Zilal Royal Guard | beni_zilal_tier_3 | 43.4 | 60.5 | TwoHandedPolearm | eastern_spear_4_t4 | 56.7 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 36 | Jawwal Bedouin | jawwal_tier_3 | 43.0 | 60.5 | TwoHandedPolearm | eastern_spear_5_t5 | 51.4 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 37 | Ghilman | ghilman_tier_2 | 42.0 | 60.5 | TwoHandedPolearm | eastern_spear_2_t3 | 63.0 | True | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 38 | Conspiracy Guardian | conspiracy_guardian | 42.0 | 60.5 | TwoHandedPolearm | wide_leaf_spear_t4 | 48.5 | False | Defensive Troops | aserai | 26.0 | special_or_unlinked |
| 39 | Conspiracy Spear Master | conspiracy_spearmaster | 41.9 | 60.5 | TwoHandedPolearm | western_spear_4_t4 | 44.3 | False | Offensive Melee | vlandia | 26.0 | special_or_unlinked |
| 40 | Sturgian Heavy Spearman | sturgian_shock_troop | 41.8 | 60.5 | TwoHandedPolearm | northern_spear_3_t4 | 63.2 | False | Skirmishers | sturgia | 26.0 | special_or_unlinked |
| 41 | Vlandian Knight | vlandian_knight | 40.9 | 60.5 | TwoHandedPolearm | vlandia_lance_2_t4 | 75.0 | True | Defensive Troops | vlandia | 21.0 | noble_line |
| 42 | Vlandian Sergeant | vlandian_sergeant | 39.8 | 60.5 | TwoHandedPolearm | western_spear_4_t4 | 66.0 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 43 | Nord Ulfhednar | nord_ulfhednar | 39.1 | 60.5 | TwoHandedPolearm | nord_spear_atgeir_1_t5 | 44.6 | False | Offensive Melee | nord | 26.0 | main_or_minor_line |
| 44 | Imperial Legionary | imperial_legionary | 39.0 | 60.5 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 61.0 | False | Defensive Troops | empire | 26.0 | special_or_unlinked |
| 45 | Aserai Mamluke Warden | aserai_master_archer | 38.8 | 60.5 | TwoHandedPolearm | easter_polesword_t4 | 59.1 | False | Defensive Troops | aserai | 26.0 | special_or_unlinked |
| 46 | Conspiracy Veteran Fighter | conspiracy_veteran_fighter | 38.4 | 60.5 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 56.0 | False | Defensive Troops | empire | 26.0 | special_or_unlinked |
| 47 | Khuzait Darkhan | khuzait_darkhan | 38.2 | 60.5 | TwoHandedPolearm | eastern_throwing_spear_2_t4 | 55.8 | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 48 | Battanian Highborn Warrior | battanian_highborn_warrior | 38.1 | 100.0 | TwoHandedSword | battania_2hsword_2_t3 | 18.7 | False | Ranged Troops | battania | 16.0 | noble_line |
| 49 | Conspiracy Mounted Master Archer | conspiracy_mounted_master_archer | 38.1 | 46.8 | OneHandedSword | khuzait_sword_4_t4 | 54.8 | True | Ranged Troops | khuzait | 26.0 | special_or_unlinked |
| 50 | Aserai Mamluke Heavy Cavalry | aserai_mameluke_heavy_cavalry | 38.0 | 46.8 | OneHandedSword | aserai_sword_6_t4 | 70.4 | True | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 51 | Battanian Oathsworn | battanian_oathsworn | 37.8 | 60.5 | TwoHandedPolearm | battania_polearm_1_t5 | 53.5 | False | Defensive Troops | battania | 26.0 | main_or_minor_line |
| 52 | Aserai Faris | aserai_faris | 37.7 | 60.5 | TwoHandedPolearm | aserai_lance_1_t5 | 51.3 | True | Skirmishers | aserai | 21.0 | noble_line |
| 53 | Jawwal Camel Rider | jawwal_tier_2 | 37.4 | 60.5 | TwoHandedPolearm | triangluar_spear_t3 | 43.5 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 54 | Vlandian Cavalry | vlandian_cavalry | 37.4 | 60.5 | TwoHandedPolearm | western_spear_3_t3 | 49.4 | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 55 | Khuzait Lancer | khuzait_lancer | 37.4 | 60.5 | TwoHandedPolearm | khu_spear_1_t4 | 67.5 | True | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 56 | Imperial Elite Menavliaton | imperial_elite_menavliaton | 37.0 | 60.5 | TwoHandedPolearm | empire_polearm_1_t4 | 42.4 | False | Offensive Melee | empire | 26.0 | main_or_minor_line |
| 57 | Khuzait Heavy Horse Archer | khuzait_heavy_horse_archer | 36.8 | 46.8 | OneHandedSword | khuzait_sword_4_t4 | 60.5 | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 58 | Battanian Mounted Skirmisher | battanian_mounted_skirmisher | 36.7 | 46.8 | OneHandedAxe|OneHandedSword | battania_axe_2_t4|battania_sword_4_t4 | 63.5 | True | Skirmishers | battania | 26.0 | special_or_unlinked |
| 59 | Conspiracy Packmaster | conspiracy_packmaster | 36.2 | 46.8 | Mace|OneHandedSword | empire_sword_3_t3|light_mace_t3 | 41.8 | True | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 60 | Vlandian Gallant | vlandian_gallant | 36.1 | 60.5 | TwoHandedPolearm | vlan_lance_1_t3 | 57.7 | True | Defensive Troops | vlandia | 16.0 | noble_line |
| 61 | Sturgian Hardened Brigand | sturgian_hardened_brigand | 36.1 | 60.5 | TwoHandedPolearm | northern_spear_3_t4 | 57.6 | True | Skirmishers | sturgia | 21.0 | main_or_minor_line |
| 62 | Nord Hearthguard | nord_jarlsmann | 35.8 | 60.5 | TwoHandedPolearm | nord_spear_1_t4 | 49.0 | False | Defensive Troops | nord | 21.0 | main_or_minor_line |
| 63 | Vlandian Voulgier | vlandian_voulgier | 35.6 | 60.5 | TwoHandedPolearm | vlandia_polearm_1_t5 | 33.5 | False | Offensive Melee | vlandia | 26.0 | main_or_minor_line |
| 64 | Khuzait Torguud | khuzait_torguud | 35.6 | 60.5 | TwoHandedPolearm | khuzait_polearm_1_t4 | 53.4 | True | Ranged Troops | khuzait | 21.0 | noble_line |
| 65 | Imperial Bucellarii | bucellarii | 35.5 | 46.8 | OneHandedSword | empire_sword_5_t4 | 49.0 | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 66 | Karakhergit Elder | karakhuzaits_tier_3 | 35.4 | 60.5 | TwoHandedPolearm | eastern_spear_4_t4 | 51.5 | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 67 | Battanian Scout | battanian_scout | 35.3 | 60.5 | TwoHandedPolearm | highland_spear_3_t3 | 50.0 | True | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 68 | Conspiracy Knight Trainee | conspiracy_knight_trainee | 34.9 | 100.0 | TwoHandedSword | western_2hsword_t3 | 20.7 | False | Offensive Melee | vlandia | 16.0 | special_or_unlinked |
| 69 | Imperial Equite | imperial_equite | 34.7 | 60.5 | TwoHandedPolearm | western_spear_3_t3 | 45.8 | True | Defensive Troops | empire | 16.0 | noble_line |
| 70 | Veteran Eleftheroi | eleftheroi_tier_3 | 34.2 | 60.5 | TwoHandedPolearm | empire_lance_2_t4 | 41.2 | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 71 | Sturgian Heroic Line Breaker | sturgian_ulfhednar | 33.7 | 46.8 | OneHandedSword | sturgia_sword_5_t4 | 45.9 | False | Offensive Melee | sturgia | 26.0 | main_or_minor_line |
| 72 | Triarii | legion_of_the_betrayed_tier_3 | 33.2 | 46.8 | OneHandedSword | aserai_noble_sword_6_t5 | 53.8 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 73 | Nord Berserkir | nord_berserkr | 33.2 | 46.8 | OneHandedSword|ThrowingAxe | nord_sword_1_t5|nord_throwing_axe_2_t5 | 59.2 | False | Defensive Troops | nord | 26.0 | main_or_minor_line |
| 74 | Sturgian Reaver | sturgia_marine_t5 | 33.1 | 41.6 | ThrowingAxe | stur_throwing_axe_2_t5 | 54.2 | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 75 | Aserai Lieutenant | aserai_veteran_infantry | 32.6 | 46.8 | OneHandedAxe|OneHandedSword | aser_battle_axe_4_t4|aserai_noble_sword_3_t5 | 54.3 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 76 | Battanian Picked Warrior | battanian_picked_warrior | 32.2 | 60.5 | TwoHandedPolearm | highland_spear_4_t4 | 45.4 | False | Defensive Troops | battania | 21.0 | main_or_minor_line |
| 77 | Battanian Skipari | battanian_marine_t5 | 32.2 | 46.8 | OneHandedSword | battania_sword_5_t5 | 48.1 | False | Skirmishers | battania | 26.0 | main_or_minor_line |
| 78 | Spark | embers_of_flame_tier_1 | 31.8 | 100.0 | TwoHandedSword | justicier_2hsword | 15.7 | False | Offensive Melee | empire | 16.0 | main_or_minor_line |
| 79 | Aserai Mamluke Cavalry | aserai_mameluke_cavalry | 31.8 | 46.8 | OneHandedSword | aserai_sword_6_t4 | 65.4 | True | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 80 | Puppeteer | hidden_hand_tier_3 | 31.5 | 60.5 | OneHandedSword|TwoHandedPolearm | empire_sword_5_t4|triangluar_spear_t3 | 54.5 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 81 | Vlandian Sharpshooter | vlandian_sharpshooter | 31.1 | 46.8 | OneHandedSword | vlandia_sword_4_t4 | 54.7 | False | Ranged Troops | vlandia | 26.0 | special_or_unlinked |
| 82 | Nord Warfang | nord_vargr | 30.9 | 60.5 | TwoHandedPolearm | nord_spear_atgeir_1_t4|nord_spear_atgeir_1_t5 | 36.9 | False | Offensive Melee | nord | 21.0 | main_or_minor_line |
| 83 | Skolder Veteran Broda | skolderbrotva_tier_3 | 30.4 | 46.8 | OneHandedSword | sturgia_sword_4_t4 | 46.8 | False | Skirmishers | nord | 26.0 | main_or_minor_line |
| 84 | Imperial Sergeant Boatsman | imperial_sergeant_crossbowman | 30.3 | 46.8 | Mace|OneHandedSword | aserai_noble_sword_6_t5|empire_mace_2_t4 | 48.4 | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 85 | Sturgian Heavy Axeman | sturgian_veteran_warrior | 29.9 | 41.6 | OneHandedAxe | sturgia_axe_4_t4 | 68.0 | False | Defensive Troops | sturgia | 26.0 | special_or_unlinked |
| 86 | Conspiracy Warmonger | conspiracy_warmonger | 29.8 | 41.6 | OneHandedAxe | battania_axe_2_t4 | 42.4 | False | Defensive Troops | battania | 26.0 | special_or_unlinked |
| 87 | Khuzait Spear Infantry | khuzait_spear_infantry | 29.5 | 60.5 | TwoHandedPolearm | eastern_throwing_spear_2_t4 | 45.7 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 88 | Khuzait Horse Archer | khuzait_horse_archer | 29.4 | 46.8 | OneHandedSword | khuzait_sword_3_t3 | 48.3 | True | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 89 | Imperial Palatine Guard | imperial_palatine_guard | 29.3 | 46.8 | OneHandedSword | empire_sword_3_t3 | 41.5 | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 90 | Vlandian Light Cavalry | vlandian_light_cavalry | 28.6 | 60.5 | TwoHandedPolearm | western_spear_4_t3 | 35.8 | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 91 | Conspiracy Noble Horseman | conspiracy_noble_horseman | 28.6 | 60.5 | TwoHandedPolearm | western_spear_3_t3 | 34.2 | True | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 92 | Aserai Bahriyyah | aserai_marine_t5 | 28.6 | 46.8 | OneHandedAxe|OneHandedSword | aserai_noble_sword_2_t5|pirate_axe_2 | 35.2 | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 93 | Aserai Mamluke Palace Guard | mamluke_palace_guard | 28.5 | 41.6 | TwoHandedAxe|TwoHandedMace | aserai_2haxe_2_t4|aserai_mace_6_t4 | 42.5 | False | Offensive Melee | aserai | 26.0 | main_or_minor_line |
| 94 | Nord Skjaldbrestir | nord_skjaldbrestir | 28.5 | 41.6 | ThrowingAxe | nord_throwing_axe_1_t5|nord_throwing_axe_2_t4 | 38.8 | False | Offensive Melee | nord | 26.0 | main_or_minor_line |
| 95 | Chosen Wolf | wolfskins_tier_3 | 28.3 | 41.6 | OneHandedAxe | battania_axe_2_t4 | 51.6 | False | Ranged Troops | battania | 26.0 | main_or_minor_line |
| 96 | Imperial Menavliaton | imperial_menavliaton | 28.3 | 60.5 | TwoHandedPolearm | empire_polearm_1_t4 | 34.7 | False | Offensive Melee | empire | 21.0 | main_or_minor_line |
| 97 | Khuzait Marksman | khuzait_marksman | 28.3 | 46.8 | OneHandedSword | khuzait_sword_3_t3 | 32.8 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 98 | Nord Sky-Gods Chosen | nord_skathi | 28.1 | 41.6 | OneHandedAxe | nord_biter_axe_1_t4 | 54.4 | False | Ranged Troops | nord | 26.0 | main_or_minor_line |
| 99 | Conspiracy Hellion | conspiracy_hellion | 28.1 | 41.6 | TwoHandedAxe | sturgia_2haxe_1_t4 | 28.6 | False | Offensive Melee | sturgia | 26.0 | special_or_unlinked |
| 100 | Lake Rat Wrecker  | lakepike_tier_3 | 27.9 | 41.6 | OneHandedAxe | battle_axe_t4 | 46.9 | False | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 101 | Battanian Wildling | battanian_wildling | 27.5 | 41.6 | OneHandedAxe | battania_axe_2_t4 | 61.7 | False | Skirmishers | battania | 26.0 | special_or_unlinked |
| 102 | Aserai Tribal Horseman | aserai_tribal_horseman | 27.2 | 60.5 | TwoHandedPolearm | eastern_spear_3_t3 | 44.7 | True | Skirmishers | aserai | 16.0 | noble_line |
| 103 | Imperial Naute | empire_marine_t5 | 27.1 | 41.6 | OneHandedAxe | imperial_axe_t3 | 46.9 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 104 | Khuzait Horseman | khuzait_horseman | 27.0 | 60.5 | TwoHandedPolearm | khuzait_lance_1_t3 | 42.3 | True | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 105 | Karakhergit Rider | karakhuzaits_tier_2 | 26.5 | 60.5 | TwoHandedPolearm | eastern_spear_2_t3 | 38.1 | True | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 106 | Confident Contender | confident_contender | 26.5 | 60.5 | OneHandedAxe|TwoHandedPolearm | wide_leaf_spear_t4|woodland_axe_t3 | 36.0 | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 107 | Hardy Contender | hardy_contender | 26.3 | 60.5 | OneHandedSword|TwoHandedPolearm | broad_arming_sword_t4|western_spear_3_t3 | 31.1 | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 108 | Khuzait Qanqli | khuzait_qanqli | 26.0 | 60.5 | TwoHandedPolearm | eastern_spear_3_t3 | 33.4 | True | Ranged Troops | khuzait | 16.0 | noble_line |
| 109 | Aserai Mamluke Regular | aserai_mameluke_regular | 25.4 | 60.5 | TwoHandedPolearm | khuzait_lance_1_t3 | 28.3 | True | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 110 | Sturgian Veteran Bowman | sturgian_veteran_bowman | 25.2 | 41.6 | OneHandedAxe | sturgia_axe_4_t4 | 40.4 | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 111 | Conspiracy Raider | conspiracy_raider | 25.1 | 60.5 | TwoHandedPolearm | triangluar_spear_t3 | 28.6 | True | Defensive Troops | battania | 16.0 | special_or_unlinked |
| 112 | Dignified Contender | dignified_contender | 25.0 | 60.5 | OneHandedSword|TwoHandedPolearm | vlandia_sword_4_t4|western_spear_3_t3 | 28.5 | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 113 | Bold Contender | bold_contender_hard | 25.0 | 60.5 | OneHandedSword|TwoHandedPolearm | northern_spear_3_t4|sturgia_sword_4_t4 | 24.7 | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 114 | Bold Contender | bold_contender_normal | 25.0 | 60.5 | OneHandedSword|TwoHandedPolearm | northern_spear_3_t4|sturgia_sword_4_t4 | 24.7 | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 115 | Bold Contender | bold_contender | 25.0 | 60.5 | OneHandedSword|TwoHandedPolearm | northern_spear_3_t4|sturgia_sword_4_t4 | 24.7 | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 116 | Bold Contender | bold_contender_very_hard | 25.0 | 60.5 | OneHandedSword|TwoHandedPolearm | northern_spear_3_t4|sturgia_sword_4_t4 | 24.7 | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 117 | Vlandian Swordsman | vlandian_swordsman | 24.7 | 46.8 | OneHandedSword | vlandia_sword_3_t4 | 49.8 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 118 | Expert Eleftheroi | eleftheroi_tier_2 | 24.5 | 60.5 | TwoHandedPolearm | empire_lance_2_t4 | 23.4 | True | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 119 | Sturgian Line Breaker | sturgian_berzerker | 24.4 | 46.8 | OneHandedSword | sturgia_sword_4_t4 | 33.6 | False | Offensive Melee | sturgia | 21.0 | main_or_minor_line |
| 120 | Principes | legion_of_the_betrayed_tier_2 | 24.4 | 46.8 | OneHandedSword | empire_sword_2_t3|empire_sword_3_t3 | 34.0 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 121 | Nord Shield Biter | nord_boandi | 24.1 | 41.6 | OneHandedAxe | nord_biter_axe_1_t4 | 46.8 | False | Defensive Troops | nord | 21.0 | main_or_minor_line |
| 122 | Conspiracy Longbowman | conspiracy_longbowman | 23.8 | 46.8 | OneHandedSword | battania_sword_2_t3 | 41.9 | False | Ranged Troops | battania | 26.0 | special_or_unlinked |
| 123 | Skolder Warrior Broda | skolderbrotva_tier_2 | 23.7 | 46.8 | OneHandedSword | sturgia_sword_3_t3 | 34.8 | False | Defensive Troops | nord | 21.0 | main_or_minor_line |
| 124 | Conspiracy Trained Spearman | conspiracy_trained_spearman | 23.2 | 60.5 | TwoHandedPolearm | western_spear_3_t3 | 31.2 | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 125 | Imperial Vigla Recruit | imperial_vigla_recruit | 23.2 | 60.5 | TwoHandedPolearm | western_spear_2_t2 | 32.0 | True | Defensive Troops | empire | 11.0 | noble_line |
| 126 | Battanian River Raider | battanian_marine_t4 | 23.0 | 46.8 | OneHandedSword | bat_sword_7_t2 | 35.7 | False | Skirmishers | battania | 21.0 | main_or_minor_line |
| 127 | Vlandian Seafarer | vlandian_marine_t4 | 22.9 | 46.8 | OneHandedSword | vlandia_sword_2_t3 | 35.1 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 128 | Battanian Highborn Youth | battanian_highborn_youth | 22.9 | 100.0 | TwoHandedAxe|TwoHandedSword | battania_2haxe_1_t2|battania_2hsword_1_t2 | 10.7 | False | Ranged Troops | battania | 11.0 | noble_line |
| 129 | Vlandian Squire | vlandian_squire | 22.7 | 60.5 | TwoHandedPolearm | vlandia_lance_1_t3 | 35.9 | True | Defensive Troops | vlandia | 11.0 | noble_line |
| 130 | Nord Marksman | nord_marksman | 22.7 | 41.6 | OneHandedAxe | nord_battle_axe_5_t3 | 32.5 | False | Ranged Troops | nord | 21.0 | main_or_minor_line |
| 131 | Beni Zilal Soldier | beni_zilal_tier_2 | 22.6 | 60.5 | TwoHandedPolearm | eastern_spear_3_t3 | 25.4 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 132 | Conspiracy Hunt Leader | conspiracy_hunt_leader | 22.5 | 41.6 | OneHandedAxe | vlandia_axe_2_t4 | 21.1 | False | Ranged Troops | empire | 26.0 | special_or_unlinked |
| 133 | Aserai Mamluke Guard | aserai_mameluke_guard | 22.5 | 41.6 | TwoHandedAxe|TwoHandedMace | aserai_2haxe_2_t4|aserai_mace_5_t4|axe_craft_19_head_hewns | 36.0 | False | Offensive Melee | aserai | 21.0 | main_or_minor_line |
| 134 | Sturgian Veteran Shipman | sturgia_marine_t4 | 22.1 | 41.6 | ThrowingAxe | stur_throwing_axe_1_t4 | 43.9 | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 135 | Nord Marauder | nord_hew-bearer | 22.1 | 41.6 | ThrowingAxe | nord_throwing_axe_1_t5 | 27.2 | False | Offensive Melee | nord | 21.0 | main_or_minor_line |
| 136 | Imperial Veteran Archer | imperial_veteran_archer | 22.1 | 46.8 | OneHandedSword | empire_sword_3_t3 | 27.1 | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 137 | Sapling | brotherhood_of_woods_tier_2 | 22.0 | 46.8 | OneHandedSword | star_falchion_sword_t3 | 13.5 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 138 | Sturgian Archer | sturgian_archer | 22.0 | 46.8 | OneHandedAxe|OneHandedSword | sturgia_axe_2_t2|sturgia_sword_1_t2 | 28.6 | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 139 | Conspiracy Fighter | conspiracy_fighter | 21.9 | 46.8 | OneHandedSword | empire_sword_2_t3|empire_sword_3_t3|vlandia_sword_2_t3 | 43.2 | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 140 | Aserai Youth | aserai_youth | 21.9 | 60.5 | TwoHandedPolearm | eastern_spear_1_t2 | 21.7 | True | Skirmishers | aserai | 11.0 | noble_line |
| 141 | Karakhergit Nomad | karakhuzaits_tier_1 | 21.9 | 60.5 | TwoHandedPolearm | eastern_spear_1_t2 | 29.3 | True | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 142 | Vlandian Mercenary | vlandian_spearman | 21.8 | 60.5 | TwoHandedPolearm | western_spear_3_t3 | 37.1 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 143 | Khuzait Jishig | khuzait_spear_sailor | 21.8 | 46.8 | OneHandedSword | khuzait_sword_4_t4 | 25.4 | False | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 144 | Blaze | embers_of_flame_tier_3 | 21.8 | 34.5 | TwoHandedMace | sturgia_mace_2_t4 | 33.7 | False | Defensive Troops | empire | 26.0 | main_or_minor_line |
| 145 | Conspiracy Mounted Hunstman | conspiracy_mounted_huntsman | 21.8 | 46.8 | OneHandedSword | empire_sword_1_t2 | 31.4 | True | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 146 | Conspiracy Horse Archer | conspiracy_horse_archer | 21.6 | 46.8 | Mace|OneHandedAxe|OneHandedSword | aserai_mace_3_t3|khuzait_sword_3_t3|woodland_axe_t3 | 30.8 | True | Ranged Troops | khuzait | 16.0 | special_or_unlinked |
| 147 | Nord War-Proven | nord_thegn | 21.4 | 60.5 | TwoHandedPolearm | nord_spear_1_t3|nord_spear_2_t3 | 36.5 | False | Defensive Troops | nord | 16.0 | main_or_minor_line |
| 148 | Aserai Boatswain | aserai_infantry | 21.3 | 41.6 | OneHandedAxe | aser_battle_axe_4_t4|bamboo_axe_t4 | 40.1 | False | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 149 | Khuzait Tribal Warrior | khuzait_tribal_warrior | 21.3 | 60.5 | TwoHandedPolearm | eastern_spear_1_t2 | 25.8 | True | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 150 | Imperial Coast Guard | empire_marine_t4 | 21.1 | 41.6 | OneHandedAxe | tzkurion_axe_t3 | 39.3 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 151 | Khuzait Raider | khuzait_raider | 21.1 | 46.8 | OneHandedSword | khuzait_sword_3_t3 | 26.1 | True | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 152 | Nord Spear Warrior | nord_spear_warrior | 21.1 | 60.5 | TwoHandedPolearm | nord_spear_1_t3|nord_spear_2_t3 | 32.4 | False | Skirmishers | nord | 16.0 | main_or_minor_line |
| 153 | Imperial Coastguard | imperial_crossbowman | 21.0 | 46.8 | Mace|OneHandedSword | empire_mace_2_t4|empire_sword_7_t2 | 20.2 | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 154 | Sturgian Varyag Guard | varyag_veteran | 20.9 | 41.6 | TwoHandedAxe | stu_2haxe_2_t3 | 35.4 | False | Offensive Melee | sturgia | 21.0 | noble_line |
| 155 | Khuzait Spearman | khuzait_spearman | 20.8 | 60.5 | TwoHandedPolearm | eastern_throwing_spear_2_t4 | 32.7 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 156 | Seasoned Wolf | wolfskins_tier_2 | 20.7 | 41.6 | OneHandedAxe | battania_axe_1_t2|woodland_axe_t3 | 31.6 | False | Ranged Troops | battania | 21.0 | main_or_minor_line |
| 157 | Boar Veteran | company_of_the_boar_tier_2 | 20.7 | 46.8 | OneHandedSword | vlandia_sword_1_t2 | 30.8 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 158 | Conspiracy Guardsman | conspiracy_guardsman | 20.6 | 60.5 | TwoHandedPolearm | eastern_spear_2_t3 | 13.9 | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 159 | Battanian Trained Warrior | battanian_trained_warrior | 20.6 | 60.5 | TwoHandedPolearm | western_spear_3_t3 | 30.1 | False | Defensive Troops | battania | 16.0 | main_or_minor_line |
| 160 | Koleman | ghilman_tier_1 | 20.5 | 60.5 | TwoHandedPolearm | eastern_spear_1_t2 | 21.4 | True | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 161 | Vlandian Billman | vlandian_billman | 20.4 | 41.6 | TwoHandedAxe | vlandia_2haxe_1_t4 | 30.6 | False | Offensive Melee | vlandia | 21.0 | main_or_minor_line |
| 162 | Beni Zilal Recruit | beni_zilal_tier_1 | 20.3 | 60.5 | TwoHandedPolearm | eastern_spear_1_t2 | 17.9 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 163 | Conspiracy Trained Huntsman | conspiracy_trained_huntsman | 20.2 | 46.8 | OneHandedAxe|OneHandedSword | empire_sword_1_t2|small_bit_axe_t2 | 15.1 | False | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 164 | Recruit Eleftheroi | eleftheroi_tier_1 | 20.2 | 60.5 | TwoHandedPolearm | empire_lance_2_t4 | 15.6 | True | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 165 | Arboreal | brotherhood_of_woods_tier_3 | 20.0 | 46.8 | OneHandedSword | vlandia_sword_3_t4 | 25.6 | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 166 | Khuzait Archer | khuzait_archer | 20.0 | 46.8 | OneHandedSword | khuzait_sword_3_t3 | 25.3 | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 167 | Conspiracy Warworn Crossbowman | conspiracy_warworn_crossbowman | 19.6 | 34.5 | Mace | morningstar_mace_t3 | 50.0 | False | Ranged Troops | vlandia | 26.0 | special_or_unlinked |
| 168 | Boar Champion | company_of_the_boar_tier_3 | 19.3 | 34.5 | Mace | vlandia_mace_2_t4 | 47.0 | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 169 | Lake Rat Veteran | lakepike_tier_2 | 18.9 | 41.6 | OneHandedAxe | woodland_axe_t3 | 17.6 | False | Skirmishers | sturgia | 21.0 | main_or_minor_line |
| 170 | Veteran Forester | forest_people_tier_3 | 18.9 | 41.6 | OneHandedAxe | battle_axe_t4 | 32.5 | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 171 | Conspiracy Wilder | conspiracy_wilder | 18.5 | 46.8 | OneHandedSword | battania_sword_2_t3 | 31.0 | False | Defensive Troops | sturgia | 16.0 | special_or_unlinked |
| 172 | Nord Axe Warrior | nord_axe_warrior | 18.2 | 41.6 | ThrowingAxe | nord_throwing_axe_2_t4 | 38.5 | False | Defensive Troops | nord | 16.0 | main_or_minor_line |
| 173 | Sturgian Brigand | sturgian_brigand | 17.7 | 41.6 | OneHandedAxe | sturgia_axe_2_t2 | 38.0 | False | Skirmishers | sturgia | 16.0 | main_or_minor_line |
| 174 | Khuzait Noble's Son | khuzait_noble_son | 17.6 | 46.8 | OneHandedSword | khuzait_sword_1_t2 | 21.6 | True | Ranged Troops | khuzait | 11.0 | noble_line |
| 175 | Hidden Soldati | hidden_hand_tier_2 | 17.3 | 46.8 | OneHandedSword | empire_sword_4_t4 | 35.3 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 176 | Guard | guard_nord | 17.2 | 60.5 | TwoHandedPolearm | northern_spear_2_t3 | 30.8 | False | Offensive Melee | nord | 4.0 | special_or_unlinked |
| 177 | Skolder Recruit | skolderbrotva_tier_1 | 17.1 | 60.5 | TwoHandedPolearm | northern_spear_1_t2 | 21.4 | False | Defensive Troops | nord | 16.0 | main_or_minor_line |
| 178 | Vlandian Footman | vlandian_footman | 17.0 | 60.5 | TwoHandedPolearm | western_spear_1_t2|western_spear_2_t2 | 32.2 | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 179 | Nord Scion | nord_ungmann | 17.0 | 60.5 | TwoHandedPolearm | nord_spear_1_t2|nord_spear_2_t2 | 27.0 | False | Defensive Troops | nord | 11.0 | main_or_minor_line |
| 180 | Hastati | legion_of_the_betrayed_tier_1 | 16.8 | 46.8 | OneHandedSword | empire_sword_1_t2 | 30.2 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 181 | Conspiracy Kern | conspiracy_kern | 16.6 | 46.8 | Mace|OneHandedSword | battania_sword_2_t3|light_mace_t3 | 46.6 | False | Skirmishers | battania | 16.0 | special_or_unlinked |
| 182 | Conspiracy Berserker | conspiracy_berserker | 16.6 | 41.6 | TwoHandedAxe | northern_axe_t3 | 17.1 | False | Offensive Melee | sturgia | 16.0 | special_or_unlinked |
| 183 | Nord Warrior | nord_drengr | 16.6 | 60.5 | TwoHandedPolearm | nord_spear_1_t2|nord_spear_2_t2 | 26.2 | False | Defensive Troops | nord | 11.0 | main_or_minor_line |
| 184 | Aserai Mamluke Axeman | aserai_mameluke_axeman | 16.1 | 41.6 | TwoHandedAxe | axe_craft_19_head_hewns | 24.1 | False | Offensive Melee | aserai | 16.0 | main_or_minor_line |
| 185 | Aserai Mamluke Soldier | aserai_mameluke_soldier | 16.1 | 60.5 | TwoHandedPolearm | eastern_spear_1_t2 | 23.4 | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 186 | Battanian Raider | battanian_raider | 16.0 | 46.8 | OneHandedSword | battania_sword_1_t2 | 24.8 | False | Skirmishers | battania | 16.0 | main_or_minor_line |
| 187 | Battanian Clan Warrior | battanian_clanwarrior | 15.7 | 60.5 | TwoHandedPolearm | western_spear_2_t2 | 23.1 | False | Skirmishers | battania | 11.0 | main_or_minor_line |
| 188 | Aserai Sailor | aserai_footman | 15.2 | 41.6 | OneHandedAxe | aser_battle_axe_3_t4 | 31.9 | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 189 | Young Wolf | wolfskins_tier_1 | 15.1 | 41.6 | OneHandedAxe | battania_axe_1_t2|battania_axe_5_t2 | 27.5 | False | Ranged Troops | battania | 16.0 | main_or_minor_line |
| 190 | Imperial Shipmate | empire_marine_t3 | 15.1 | 41.6 | OneHandedAxe | small_spurred_axe_t2 | 30.5 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 191 | Imperial Trained Archer | imperial_trained_archer | 15.1 | 46.8 | OneHandedSword | empire_sword_1_t2 | 17.7 | False | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 192 | Sturgian Crewman | sturgia_marine_t3 | 15.0 | 41.6 | ThrowingAxe | stur_throwing_axe_2_t4 | 29.2 | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 193 | Jawwal Recruit | jawwal_tier_1 | 14.7 | 60.5 | TwoHandedPolearm | eastern_spear_1_t2 | 13.7 | False | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 194 | Vlandian Shipmate | vlandian_infantry | 14.6 | 46.8 | OneHandedAxe|OneHandedSword | vlandia_axe_1_t3|vlandia_sword_2_t3 | 17.4 | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 195 | Khuzait Hunter | khuzait_hunter | 14.5 | 46.8 | OneHandedSword | khuzait_sword_1_t2 | 12.1 | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 196 | Sturgian Varyag | varyag | 14.4 | 41.6 | TwoHandedAxe | northern_axe_t3|sturgia_2haxe_1_t4 | 24.7 | False | Offensive Melee | sturgia | 16.0 | noble_line |
| 197 | Conspiracy Trained Crossbowman | conspiracy_trained_crossbowman | 13.5 | 46.8 | Mace|OneHandedSword | empire_mace_1_t2|vlandia_mace_1_t2|vlandia_sword_1_t2 | 30.2 | False | Ranged Troops | vlandia | 16.0 | special_or_unlinked |
| 198 | Boar Novice | company_of_the_boar_tier_1 | 13.3 | 46.8 | OneHandedSword | vlandia_sword_1_t2 | 24.7 | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 199 | Borrowed Troop | borrowed_troop | 13.1 | 60.5 | OneHandedAxe|TwoHandedPolearm | peasant_pickaxe_1_t1|peasant_pitchfork_2_t1|peasant_polearm_1_t1 | 2.6 | False | Skirmishers | empire | 6.0 | main_or_minor_line |
| 200 | Sturgian Hunter | sturgian_hunter | 12.7 | 46.8 | OneHandedAxe|OneHandedSword | sturgia_axe_2_t2|sturgia_sword_1_t2 | 14.9 | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 201 | Battanian Wood Runner | battanian_woodrunner | 12.3 | 46.8 | OneHandedAxe|OneHandedSword | battania_axe_5_t2|battania_sword_1_t2 | 21.1 | False | Skirmishers | battania | 11.0 | main_or_minor_line |
| 202 | Sea Hound Marksman | sea_hounds_marksman | 12.2 | 41.6 | OneHandedAxe | nord_hatchett_1_t2|nord_hatchett_2_t2 | 16.6 | False | Ranged Troops | nord | 11.0 | special_or_unlinked |
| 203 | Nord Freeman Archer | nord_freeman_archer | 12.2 | 41.6 | OneHandedAxe | nord_hatchett_1_t2 | 21.2 | False | Ranged Troops | nord | 16.0 | main_or_minor_line |
| 204 | Khuzait Footman | khuzait_footman | 12.1 | 46.8 | Mace|OneHandedSword | khuzait_mace_1_t2|khuzait_sword_1_t2 | 16.4 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 205 | Hidden Pawn | hidden_hand_tier_1 | 12.1 | 46.8 | OneHandedSword | iron_spatha_sword_t2 | 15.4 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 206 | Vlandian Levy Crossbowman | vlandian_levy_crossbowman | 11.8 | 46.8 | OneHandedSword | vlandia_sword_1_t2 | 12.1 | False | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 207 | Sturgian Warrior | sturgian_warrior | 11.5 | 41.6 | OneHandedAxe | sturgia_axe_2_t2 | 22.3 | False | Defensive Troops | sturgia | 11.0 | main_or_minor_line |
| 208 | Expert Forester | forest_people_tier_2 | 11.5 | 41.6 | OneHandedAxe | woodland_axe_t3 | 21.9 | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 209 | Aserai Cadet | aserai_tribesman | 11.5 | 41.6 | ThrowingAxe | southern_throwing_axe_1_t4 | 18.7 | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 210 | Lake Rat Recruit | lakepike_tier_1 | 11.0 | 41.6 | OneHandedAxe | small_bit_axe_t2 | 16.5 | False | Skirmishers | sturgia | 16.0 | main_or_minor_line |
| 211 | Sprout | brotherhood_of_woods_tier_1 | 11.0 | 46.8 | OneHandedSword | falchion_sword_t2 | 7.1 | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 212 | Sturgian Otrok | sturgian_warrior_son | 10.9 | 41.6 | TwoHandedAxe | bearded_axe_t3|simple_sparth_axe_t2 | 18.1 | False | Offensive Melee | sturgia | 11.0 | noble_line |
| 213 | Veteran Borrowed Troop | veteran_borrowed_troop | 10.9 | 46.8 | OneHandedSword | falchion_sword_t2|simple_back_sword_t2 | 8.7 | False | Defensive Troops | empire | 11.0 | main_or_minor_line |
| 214 | Conspiracy Trained Bowman | conspiracy_trained_bowman | 10.5 | 34.5 | Mace | aserai_mace_2_t2 | 23.7 | False | Ranged Troops | aserai | 16.0 | special_or_unlinked |
| 215 | Khuzait Nomad | khuzait_nomad | 10.4 | 46.8 | Mace|OneHandedSword | falchion_sword_t2|khuzait_mace_1_t2|khuzait_sword_1_t2 | 5.4 | False | Offensive Melee | khuzait | 6.0 | main_or_minor_line |
| 216 | Vlandian Recruit | vlandian_recruit | 10.4 | 46.8 | Mace|OneHandedAxe|OneHandedSword | peasant_pickaxe_1_t1|vlandia_mace_1_t2|vlandia_sword_1_t2 | 4.7 | False | Offensive Melee | vlandia | 6.0 | main_or_minor_line |
| 217 | Recruit Forester | forest_people_tier_1 | 10.4 | 41.6 | OneHandedAxe | woodland_axe_t3 | 10.8 | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 218 | Aserai Beduin | aserai_recruit | 10.3 | 46.8 | OneHandedSword | simple_back_sword_t2 | 3.8 | False | Offensive Melee | aserai | 6.0 | main_or_minor_line |
| 219 | Imperial Oarsman | empire_marine_t2 | 10.2 | 41.6 | OneHandedAxe | vlandia_axe_1_t3 | 11.7 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 220 | Battanian Volunteer | battanian_volunteer | 10.0 | 41.6 | Mace|OneHandedAxe|TwoHandedMace | battania_mace_1_t3|battania_mace_2_t2|peasant_maul_t1_2|peasant_pickaxe_1_t1 | 10.2 | False | Offensive Melee | battania | 6.0 | main_or_minor_line |
| 221 | Sturgian Recruit | sturgian_recruit | 10.0 | 41.6 | OneHandedAxe | small_spurred_axe_t2 | 7.0 | False | Offensive Melee | sturgia | 6.0 | main_or_minor_line |
| 222 | Nord Huntsman | nord_huntsman | 9.9 | 41.6 | OneHandedAxe | nord_hatchett_2_t2 | 9.3 | False | Ranged Troops | nord | 11.0 | main_or_minor_line |
| 223 | Nord Youngling | nord_youngling | 9.7 | 41.6 | OneHandedAxe | naval_one_handed_axe_t1 | 5.7 | False | Offensive Melee | nord | 6.0 | main_or_minor_line |
| 224 | Aserai Sahraq | aserai_marine_t4 | 2.7 | 0.0 | Dagger | dagger_golden_claw | 23.9 | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 225 | Imperial Archer | imperial_archer | 0.5 | 0.0 | Dagger | pugio | 6.5 | False | Ranged Troops | empire | 11.0 | main_or_minor_line |


## Ranked — Skirmisher (46 troops)

| rank | troop_name | troop_id | skirmisher_role_score | throw_score_base | throw_damage | direct_throw_item | crafted_throw_item | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Aserai Vanguard Faris | aserai_vanguard_faris | 100.0 | 24.4 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 31.0 | noble_line |
| 2 | Flame | embers_of_flame_tier_2 | 98.3 | 100.0 | 57.0 | sling_reinforced | nan | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 3 | Sturgian Horse Raider | sturgian_horse_raider | 90.1 | 24.4 | 0.0 | nan | sturg_javelin_3_t4 | True | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 4 | Jawwal Bedouin | jawwal_tier_3 | 86.6 | 24.4 | 0.0 | nan | eastern_javelin_1_t2 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 5 | Beni Zilal Royal Guard | beni_zilal_tier_3 | 86.2 | 24.4 | 0.0 | nan | northern_javelin_4_t3 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 6 | Battanian Mounted Skirmisher | battanian_mounted_skirmisher | 85.3 | 24.4 | 0.0 | nan | northern_javelin_5_t5 | True | Skirmishers | battania | 26.0 | special_or_unlinked |
| 7 | Aserai Veteran Faris | aserai_veteran_faris | 76.8 | 24.4 | 0.0 | nan | northern_javelin_4_t3 | True | Skirmishers | aserai | 26.0 | noble_line |
| 8 | Conspiracy Battle Rider | conspiracy_battlerider | 74.6 | 24.4 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | sturgia | 26.0 | special_or_unlinked |
| 9 | Jawwal Camel Rider | jawwal_tier_2 | 73.5 | 24.4 | 0.0 | nan | eastern_javelin_1_t2 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 10 | Sturgian Hardened Brigand | sturgian_hardened_brigand | 72.9 | 24.4 | 0.0 | nan | sturg_javelin_3_t2 | True | Skirmishers | sturgia | 21.0 | main_or_minor_line |
| 11 | Puppeteer | hidden_hand_tier_3 | 70.8 | 23.1 | 0.0 | nan | leafblade_throwing_knife | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 12 | Aserai Faris | aserai_faris | 70.5 | 24.4 | 0.0 | nan | northern_javelin_4_t3 | True | Skirmishers | aserai | 21.0 | noble_line |
| 13 | Khuzait Tengri | khuzait_Tengri | 68.5 | 24.4 | 0.0 | nan | spear_blade_10_hewns | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 14 | Beni Zilal Soldier | beni_zilal_tier_2 | 61.8 | 24.4 | 0.0 | nan | eastern_javelin_2_t3 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 15 | Battanian Falxman | battanian_falxman | 61.1 | 23.1 | 0.0 | nan | woodland_throwing_axe_1_t1 | False | Skirmishers | battania | 21.0 | main_or_minor_line |
| 16 | Battanian Skipari | battanian_marine_t5 | 58.7 | 24.4 | 0.0 | nan | northern_javelin_6_t6 | False | Skirmishers | battania | 26.0 | main_or_minor_line |
| 17 | Aserai Tribal Horseman | aserai_tribal_horseman | 57.1 | 24.4 | 0.0 | nan | eastern_javelin_1_t2 | True | Skirmishers | aserai | 16.0 | noble_line |
| 18 | Battanian Wildling | battanian_wildling | 53.0 | 24.4 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | battania | 26.0 | special_or_unlinked |
| 19 | Skolder Veteran Broda | skolderbrotva_tier_3 | 51.7 | 24.4 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | nord | 26.0 | main_or_minor_line |
| 20 | Lake Rat Wrecker  | lakepike_tier_3 | 49.5 | 24.4 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | sturgia | 26.0 | main_or_minor_line |
| 21 | Aserai Lieutenant | aserai_veteran_infantry | 49.0 | 24.4 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 22 | Beni Zilal Recruit | beni_zilal_tier_1 | 47.5 | 24.4 | 0.0 | nan | eastern_javelin_1_t2 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 23 | Imperial Naute | empire_marine_t5 | 47.1 | 24.4 | 0.0 | nan | empire_javelin_1_t5 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 24 | Sturgian Heavy Spearman | sturgian_shock_troop | 46.2 | 24.4 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | sturgia | 26.0 | special_or_unlinked |
| 25 | Hidden Soldati | hidden_hand_tier_2 | 43.7 | 23.1 | 0.0 | nan | lowland_throwing_knife | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 26 | Aserai Youth | aserai_youth | 37.3 | 24.4 | 0.0 | nan | eastern_javelin_1_t2 | True | Skirmishers | aserai | 11.0 | noble_line |
| 27 | Triarii | legion_of_the_betrayed_tier_3 | 35.8 | 24.4 | 0.0 | nan | empire_javelin_1_t4 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 28 | Battanian River Raider | battanian_marine_t4 | 35.4 | 24.4 | 0.0 | nan | northern_javelin_6_t6 | False | Skirmishers | battania | 21.0 | main_or_minor_line |
| 29 | Imperial Coast Guard | empire_marine_t4 | 33.1 | 24.4 | 0.0 | nan | empire_javelin_1_t4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 30 | Nord Spear Warrior | nord_spear_warrior | 31.7 | 24.4 | 0.0 | nan | nord_spear_javelin_1_t3 | False | Skirmishers | nord | 16.0 | main_or_minor_line |
| 31 | Conspiracy Kern | conspiracy_kern | 31.3 | 24.4 | 0.0 | nan | northern_javelin_1_t2 | False | Skirmishers | battania | 16.0 | special_or_unlinked |
| 32 | Principes | legion_of_the_betrayed_tier_2 | 30.2 | 24.4 | 0.0 | nan | empire_javelin_1_t4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 33 | Khuzait Jishig | khuzait_spear_sailor | 28.0 | 24.4 | 0.0 | nan | spear_blade_10_hewns | False | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 34 | Lake Rat Veteran | lakepike_tier_2 | 26.5 | 24.4 | 0.0 | nan | generic_javelin_1_t3 | False | Skirmishers | sturgia | 21.0 | main_or_minor_line |
| 35 | Aserai Boatswain | aserai_infantry | 26.2 | 24.4 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 36 | Hidden Pawn | hidden_hand_tier_1 | 26.1 | 23.1 | 0.0 | nan | empire_throwingknife_t5 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 37 | Sturgian Brigand | sturgian_brigand | 21.5 | 24.4 | 0.0 | nan | sturg_javelin_3_t2 | False | Skirmishers | sturgia | 16.0 | main_or_minor_line |
| 38 | Imperial Shipmate | empire_marine_t3 | 19.0 | 24.4 | 0.0 | nan | empire_javelin_1_t4 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 39 | Hastati | legion_of_the_betrayed_tier_1 | 18.9 | 24.4 | 0.0 | nan | empire_javelin_1_t4 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 40 | Battanian Raider | battanian_raider | 18.7 | 23.1 | 0.0 | nan | woodland_throwing_axe_1_t1 | False | Skirmishers | battania | 16.0 | main_or_minor_line |
| 41 | Battanian Clan Warrior | battanian_clanwarrior | 14.4 | 23.1 | 0.0 | nan | celtic_throwing_dagger | False | Skirmishers | battania | 11.0 | main_or_minor_line |
| 42 | Jawwal Recruit | jawwal_tier_1 | 12.1 | 24.4 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 43 | Borrowed Troop | borrowed_troop | 10.1 | 46.2 | 10.0 | throwing_stone | nan | False | Skirmishers | empire | 6.0 | main_or_minor_line |
| 44 | Battanian Wood Runner | battanian_woodrunner | 6.5 | 24.4 | 0.0 | nan | northern_javelin_5_t5 | False | Skirmishers | battania | 11.0 | main_or_minor_line |
| 45 | Lake Rat Recruit | lakepike_tier_1 | 4.8 | 24.4 | 0.0 | nan | western_javelin_3_t3 | False | Skirmishers | sturgia | 16.0 | main_or_minor_line |
| 46 | Imperial Oarsman | empire_marine_t2 | 0.6 | 24.4 | 0.0 | nan | generic_javelin_1_t3 | False | Skirmishers | empire | 11.0 | main_or_minor_line |

