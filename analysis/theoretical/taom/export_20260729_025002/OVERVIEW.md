# Troop overview — `taom` / `export_20260729_025002`

## Labels

- `evidence_basis=xml_structural`, `empirical=false` (ADR-004)
- Model: `role_scores_v1` conservative (crafted melee = proxy, not HTK)
- Package digest: `afef4c8483d4d27a228f13c78ed84f89fd624f9e7103d2801b1cec065eee767f`
- Rows scored: **1237**; after filters: **870** (excluded 367: untouched vanilla `change_type=inalterado` only)

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

## Ranked — Ranged (105 troops)

| rank | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | has_horse | has_shield | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Rhûn] Kharaghûl Karash Keshig | kharaghul_karash_keshig | 100.0 | 73.9 | 57.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 2 | [Rohan] Éothéod Horse Archer | rohan_wold_kings_own_horse_archer | 95.7 | 70.8 | 58.0 | steppe_war_bow | True | False | Ranged Troops | vlandia | 36.0 | main_or_minor_line |
| 3 | [Gondor] Tolfalas Sharpshooter | gondor_tol_sharpshooter | 95.4 | 98.0 | 103.0 | crossbow_f | False | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 4 | [Rhûn] Balcoth Farshot Horse Archer | balcoth_farshot_horse_archer | 92.7 | 73.9 | 57.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 5 | [Rhûn] Kharaghûl Keshig | kharaghul_keshig | 92.7 | 73.9 | 57.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 6 | [Rohan] Wold Eorlingas Horse Archer | rohan_wold_eorlingas_horse_archer | 90.5 | 70.8 | 58.0 | steppe_war_bow | True | False | Ranged Troops | vlandia | 31.0 | main_or_minor_line |
| 7 | [Rhûn] Sagarûn Storm Marked Arbalest | sagarun_storm_marked_arbalest | 84.6 | 90.9 | 96.0 | crossbow_d | False | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 8 | [Harad] Serpent Archer | harad_serpenthorsearcher | 79.6 | 71.9 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 9 | [Dale] Dalian Royal Crossbowman | dale_master_crossbowman | 76.4 | 93.2 | 103.0 | crossbow_f | False | False | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 10 | [Rohan] Wold Elite Horse Rider | rohan_wold_elite_horse_archer | 71.2 | 70.8 | 58.0 | steppe_war_bow | True | False | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 11 | [Rhûn] Balcoth Horse Archer | balcoth_horse_archer | 70.9 | 72.5 | 55.0 | composite_steppe_bow | True | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 12 | [Rhûn] Kharaghûl Horse Archer | kharaghul_horse_archer | 70.9 | 72.5 | 55.0 | composite_steppe_bow | True | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 13 | [Gundabad] Despoiler of the Vale | gundabad_despoiler_of_the_vale | 69.2 | 71.9 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | gundabad | 26.0 | main_or_minor_line |
| 14 | [Dunland] Draig-lûth Sharpshooter | dunland_dragon_sniper | 67.2 | 88.2 | 96.0 | crossbow_d | False | False | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 15 | [Rhûn] Dragon-Wrath Longbowman | dragon_wrath_longbowman | 66.2 | 73.9 | 57.0 | steppe_war_bow | False | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 16 | [Rhûn] Sagarûn Arbalest | sagarun_arbalest | 65.7 | 89.0 | 94.0 | crossbow_c | False | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 17 | [Gondor] Tolfalas Marksman | gondor_tol_marksman | 64.6 | 84.6 | 82.0 | crossbow_e | False | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 18 | [Gondor] Lond-Galen Pavise Crossbowman | gondor_lg_pavise_crossbowman | 64.6 | 84.6 | 82.0 | crossbow_e | False | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 19 | [Mordor] Black Uruk Heavy Crossbow | mordor_uruk_heavy_crossbow | 63.4 | 85.7 | 93.0 | crossbow_c | False | False | Ranged Troops | mordor | 31.0 | main_or_minor_line |
| 20 | [Dunland] Cigfran-lûth Master Ranger | dunland_raven_master_ranger | 61.7 | 82.2 | 67.0 | woodland_longbow | False | False | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 21 | [Harad] Rider of the Golden Veil | harad_horsearcher | 59.6 | 71.9 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 22 | [Rhûn] Black Sun Archer | black_sun_archer | 58.9 | 99.7 | 98.0 | noble_long_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 23 | [Gondor] Lond-Galen Crossbowman | gondor_lg_crossbowman | 58.3 | 94.3 | 98.0 | crossbow_d | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 24 | [Gondor] Tolfalas Veteran Crossbowman | gondor_tol_vet_crossbowman | 58.3 | 94.3 | 98.0 | crossbow_d | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 25 | [Dunland] Draig-lûth Firebolt | dunland_dragon_firebolt | 57.7 | 94.4 | 105.0 | crossbow_f | False | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 26 | [Harad] Serpent Eyes | harad_serpent_eye | 57.7 | 72.8 | 56.0 | composite_steppe_bow | False | False | Ranged Troops | aserai | 31.0 | main_or_minor_line |
| 27 | [Umbar] Beruthiel's Rangers | umbar_elite_root101 | 52.7 | 88.6 | 100.0 | crossbow_f | False | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 28 | [Rhûn] Wainrider Wind-Arrow Sharpshooter | wainrider_wind_arrow_sharpshooter | 52.2 | 73.9 | 57.0 | steppe_war_bow | False | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 29 | [Rhûn] Dragon-Wrath Archer | dragon_wrath_archer | 52.2 | 73.9 | 57.0 | steppe_war_bow | False | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 30 | [Rohan] Wold Veteran Horse Rider | rohan_wold_veteran_horse_archer | 50.7 | 69.3 | 56.0 | composite_steppe_bow | True | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 31 | [Dale] Dalian Master Crossbowman | dale_royal_crossbowman | 50.5 | 79.7 | 82.0 | crossbow_e | False | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 32 | [Dunland] Cigfran-lûth Ranger | dunland_raven_ranger | 48.5 | 82.2 | 67.0 | woodland_longbow | False | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 33 | [Rhûn] Kharaghûl Horse Scout | kharaghul_horse_scout | 47.6 | 68.1 | 55.0 | steppe_heavy_bow | True | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 34 | [Harad] Militia Veteran Archer | harad_militia_veteran_archer | 47.0 | 96.1 | 98.0 | noble_long_bow | False | False | Ranged Troops | aserai | 16.0 | special_or_unlinked |
| 35 | [Harad] Militia Archer | harad_militia_archer | 46.1 | 94.7 | 95.0 | hunting_bow|noble_long_bow | False | False | Ranged Troops | aserai | 11.0 | special_or_unlinked |
| 36 | [Mordor] Black Uruk Crossbow | mordor_uruk_crossbow | 46.0 | 80.2 | 84.0 | crossbow_b | False | False | Ranged Troops | mordor | 26.0 | main_or_minor_line |
| 37 | [Harad] Viper | harad_vipereye | 45.7 | 72.8 | 56.0 | composite_steppe_bow | False | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 38 | [Gundabad] Scout | gundabad_scout | 45.7 | 68.3 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | gundabad | 21.0 | main_or_minor_line |
| 39 | [Gondor] Gondor Veteran Militia Archer | gondor_militia_veteran_archer | 43.7 | 98.8 | 95.0 | noble_long_bow | False | False | Ranged Troops | gondor | 16.0 | special_or_unlinked |
| 40 | [Rohan] Eastfold Veteran Bowman | rohan_eastfold_veteran_bowman | 43.0 | 100.0 | 99.0 | noble_long_bow | False | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 41 | [Dale] Dalian Veteran Crossbowman | dale_veteran_crossbowman | 41.8 | 88.8 | 97.0 | crossbow_d | False | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 42 | [Gondor] Pinnath Gelin Veteran Archer | gondor_pg_vet_archer | 40.9 | 71.5 | 57.0 | steppe_war_bow | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 43 | [Rohan] Militia Veteran Archer | rohan_militia_veteran_archer | 40.7 | 96.1 | 98.0 | noble_long_bow | False | False | Ranged Troops | vlandia | 16.0 | special_or_unlinked |
| 44 | [Rhûn] Black Sun Scout | black_sun_scout | 40.4 | 99.7 | 98.0 | noble_long_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 45 | [Rohan] Militia Archer | rohan_militia_archer | 40.0 | 94.7 | 95.0 | hunting_bow|noble_long_bow | False | False | Ranged Troops | vlandia | 11.0 | special_or_unlinked |
| 46 | [Gondor] Belfalas Veteran Archer | gondor_bel_vet_archer | 39.8 | 70.1 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 47 | [Rhûn] Sagarûn Crossbowman | sagarun_crossbowman | 39.7 | 73.4 | 69.0 | crossbow_a | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 48 | [Rhûn] Militia Veteran Archer | rhun_militia_veteran_archer | 39.1 | 97.3 | 98.0 | noble_long_bow | False | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 49 | [Rhûn] Loke-Rim Archer | loke_rim_archer | 39.0 | 72.5 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 50 | [Rhûn] Easterling Veteran Archer | easterling_veteran_archer_new | 39.0 | 72.5 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 51 | [Rhûn] Sagarûn Skirmisher | sagarun_skirmisher | 39.0 | 72.5 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 52 | [Rhûn] Wainrider Veteran Archer | wainrider_veteran_archer | 39.0 | 72.5 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 53 | [Gondor] Tolfalas Crossbowman | gondor_tol_crossbowman | 38.9 | 90.5 | 93.0 | crossbow_c | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 54 | Mordor Militia Veteran Archer | mordor_militia_veteran_archer | 38.7 | 94.7 | 95.0 | noble_long_bow | False | False | Ranged Troops | mordor | 16.0 | special_or_unlinked |
| 55 | [Isengard] Militia Veteran Archer | isengard_militia_veteran_archer | 33.4 | 81.1 | 86.0 | crossbow_b | False | False | Ranged Troops | isengard | 16.0 | main_or_minor_line |
| 56 | [Mordor] Black Uruk Archer | mordor_uruk_archer | 32.4 | 61.1 | 42.0 | mountain_hunting_bow | False | False | Ranged Troops | mordor | 26.0 | main_or_minor_line |
| 57 | [Rohan] Wold Horse Archer | rohan_wold_horse_archer | 32.0 | 68.9 | 55.0 | composite_steppe_bow | True | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 58 | [Harad] Marksman | harad_marksman | 31.5 | 71.7 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 59 | [Umbar] Rozadan Bowmen | umbar_elite_root10 | 31.2 | 73.4 | 57.0 | lowland_longbow | False | False | Ranged Troops | umbar | 21.0 | main_or_minor_line |
| 60 | [Dunland] Draig-lûth Crossbowman | dunland_dragon_crossbowman | 30.7 | 77.3 | 78.0 | crossbow_e | False | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 61 | [Dunland] Cigfran-lûth Archer | dunland_raven_archer | 29.8 | 75.8 | 60.0 | lowland_longbow | False | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 62 | [Dunland] Militia Veteran Archer | dunland_militia_veteran_archer | 27.9 | 68.0 | 58.0 | lowland_longbow | False | False | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 63 | [Isengard] Militia Archer | isengard_militia_archer | 27.1 | 70.4 | 69.0 | crossbow_a | False | False | Ranged Troops | isengard | 11.0 | main_or_minor_line |
| 64 | [Dunland] Militia Archer | dunland_militia_archer | 27.0 | 68.4 | 57.0 | highland_ranger_bow|lowland_longbow | False | False | Ranged Troops | empire | 11.0 | special_or_unlinked |
| 65 | [Gondor] Belfalas Archer | gondor_bel_archer | 26.9 | 70.1 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 66 | [Gondor] Pinnath Gelin Archer | gondor_pg_archer | 26.9 | 70.1 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 67 | [Rhûn] Loke-Rim Bowman | loke_rim_bowman | 25.6 | 72.5 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 68 | [Rhûn] Balcoth Archer | balcoth_archer | 25.6 | 72.5 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 69 | [Rhûn] Easterling Archer | easterling_archer_new | 25.6 | 72.5 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 70 | [Mordor] Morannon Archer | morannon_archer | 24.3 | 69.6 | 54.0 | composite_bow | False | False | Ranged Troops | mordor | 21.0 | main_or_minor_line |
| 71 | [Mordor] Orc Archer | mordor_orc_archer | 24.3 | 69.6 | 54.0 | composite_bow | False | False | Ranged Troops | mordor | 21.0 | main_or_minor_line |
| 72 | [Goblin] Militia Archer | goblin_militia_archer | 23.2 | 58.2 | 40.0 | hunting_bow | False | False | Ranged Troops | goblin | 11.0 | special_or_unlinked |
| 73 | [Goblin] Militia Veteran Archer | goblin_militia_veteran_archer | 23.2 | 58.2 | 40.0 | hunting_bow | False | False | Ranged Troops | goblin | 16.0 | special_or_unlinked |
| 74 | [Dale] Dalian Crossbowman | dale_crossbowman | 22.4 | 84.8 | 91.0 | crossbow_c | False | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 75 | [Gondor] Gondor Militia Archer | gondor_militia_archer | 22.4 | 62.3 | 40.0 | hunting_bow | False | False | Ranged Troops | gondor | 11.0 | special_or_unlinked |
| 76 | [Dunland] Hebog-lûth Noble Horse Archer | dunland_falcon_noble_horse_archer | 20.8 | 71.9 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 77 | [Dunland] Hebog-lûth Horse Archer | dunland_falcon_wildrider | 20.2 | 71.9 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 78 | [Gondor] Tolfalas Arbalest | gondor_tol_arbalest | 18.8 | 85.9 | 86.0 | crossbow_b | False | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 79 | [Rohan] Wold Scout | rohan_wold_scout | 18.6 | 68.9 | 55.0 | composite_steppe_bow | True | False | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 80 | Mordor Militia Archer | mordor_militia_archer | 18.4 | 58.2 | 40.0 | hunting_bow | False | False | Ranged Troops | mordor | 11.0 | special_or_unlinked |
| 81 | [Dunland] Hebog-lûth Scout | dunland_falcon_archer | 18.2 | 71.1 | 54.0 | steppe_heavy_bow | True | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 82 | [Rhûn] Militia Archer | rhun_militia_archer | 17.8 | 58.2 | 40.0 | hunting_bow | False | False | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 83 | [Gundabad] Militia Archer | gundabad_militia_archer | 17.1 | 58.2 | 40.0 | hunting_bow | False | False | Ranged Troops | gundabad | 11.0 | special_or_unlinked |
| 84 | [Misty Mountains] Militia Archer | mistymountainorcs_militia_archer | 17.1 | 58.2 | 40.0 | hunting_bow | False | False | Ranged Troops | mistymountainorcs | 11.0 | special_or_unlinked |
| 85 | [Misty Mountains] Militia Veteran Archer | mistymountainorcs_militia_veteran_archer | 17.1 | 58.2 | 40.0 | hunting_bow | False | False | Ranged Troops | mistymountainorcs | 16.0 | special_or_unlinked |
| 86 | [Gundabad] Militia Veteran Archer | gundabad_militia_veteran_archer | 17.1 | 58.2 | 40.0 | hunting_bow | False | False | Ranged Troops | gundabad | 16.0 | special_or_unlinked |
| 87 | [Harad] Desert Archer | harad_archer | 16.9 | 71.7 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | aserai | 16.0 | main_or_minor_line |
| 88 | [Rohan] Wold Recruit | rohan_wold_recruit | 16.0 | 68.9 | 55.0 | composite_steppe_bow | True | False | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 89 | [Dunland] Tribal Skirmisher | dunland_skirmisher | 15.8 | 71.0 | 58.0 | lowland_longbow | False | False | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 90 | [Rohan] East-Fold Bowman | rohan_eastfold_bowman | 15.5 | 81.0 | 67.0 | woodland_longbow | False | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 91 | [Gondor] Belfalas Bowman | gondor_bel_bowman | 14.6 | 74.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 92 | [Umbar] Adûnaim Bowmen | umbar_elite_root1 | 13.5 | 72.1 | 51.0 | composite_bow | False | False | Ranged Troops | umbar | 16.0 | main_or_minor_line |
| 93 | [Dunland] Cigfran-lûth Skirmisher | dunland_raven_warrior | 12.8 | 71.0 | 58.0 | lowland_longbow | False | False | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 94 | [Rhûn] Easterling Skirmisher | easterling_skirmisher_new | 10.5 | 71.7 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 95 | [Harad] Skirmisher | harad_skirmisher | 7.2 | 72.1 | 54.0 | composite_bow | False | False | Ranged Troops | aserai | 11.0 | main_or_minor_line |
| 96 | [Mordor] Morannon Scout | morannon_scout | 6.4 | 57.7 | 41.0 | hunting_bow | False | False | Ranged Troops | mordor | 16.0 | main_or_minor_line |
| 97 | [Mordor] Orc Scout | mordor_orc_scout | 6.4 | 57.7 | 41.0 | hunting_bow | False | False | Ranged Troops | mordor | 16.0 | main_or_minor_line |
| 98 | [Rohan] Eastfold Yeoman Archer | rohan_eastfold_skirmisher | 5.4 | 77.8 | 62.0 | woodland_yew_bow | False | False | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 99 | [Gondor] Belfalas Hunter | gondor_bel_hunter | 4.4 | 74.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | gondor | 11.0 | main_or_minor_line |
| 100 | [Dunland] Tribal Hunter | dunland_hunter | 4.2 | 66.2 | 47.0 | highland_ranger_bow | False | False | Ranged Troops | empire | 11.0 | main_or_minor_line |
| 101 | [Rhûn] Easterling Bowman | easterling_bowman | 4.0 | 72.1 | 54.0 | composite_bow | False | False | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 102 | [Rohan] Eastfold Freeman | rohan_eastfold_recruit | 2.1 | 64.6 | 52.0 | glen_ranger_bow | False | False | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 103 | [Dunland] Cigfran-lûth Hunter | dunland_raven_noble_son | 1.8 | 64.7 | 48.0 | highland_ranger_bow | False | False | Ranged Troops | empire | 11.0 | main_or_minor_line |
| 104 | [Mordor] Orc Hunter | mordor_orc_hunter | 0.0 | 57.7 | 41.0 | hunting_bow | False | False | Ranged Troops | mordor | 11.0 | main_or_minor_line |
| 105 | [Mordor] Morannon Skirmisher | morannon_skirmisher | 0.0 | 57.7 | 41.0 | hunting_bow | False | False | Ranged Troops | mordor | 11.0 | main_or_minor_line |


## Ranked — Defensive (193 troops)

| rank | troop_name | troop_id | defensive_role_score | defense_score_base | armor_total | effective_armor | has_shield | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Harad] Camel Rider | harad_camelrider | 70.4 | 59.8 | 154.0 | 45.4 | True | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 2 | [Harad] Camel Scout | harad_camelscout | 61.1 | 47.6 | 96.0 | 32.5 | True | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 3 | [Dunland] Wild-man Spearman | dunland_veteran_spearman | 51.0 | 42.8 | 124.0 | 34.9 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 4 | [Dunland] Wild-man Swordman | dunland_veteran_swordman | 48.8 | 41.0 | 98.0 | 32.9 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 5 | [Rhûn] Wainrider Cavalry | wainrider_cavalry | 47.2 | 31.2 | 0.0 | 0.0 | True | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 6 | [Harad] Serpent Guard | harad_serpentguard | 47.0 | 29.2 | 0.0 | 0.0 | True | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 7 | [Harad] Fang of the King | harad_fangking | 47.0 | 29.2 | 0.0 | 0.0 | True | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 8 | [Harad] Youngblood of the Serpent | harad_noble | 47.0 | 29.2 | 0.0 | 0.0 | True | True | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 9 | [Harad] Initiate of the Sand Blades | harad_sandblade | 47.0 | 29.2 | 0.0 | 0.0 | True | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 10 | [Harad] Warrior of the Gilded Fang | harad_gildedfang | 47.0 | 29.2 | 0.0 | 0.0 | True | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 11 | [Rhûn] Kharaghûl Rider | kharaghul_rider | 38.3 | 17.9 | 0.0 | 0.0 | True | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 12 | [Rhûn] Far-Rhun Horseman | far_rhun_horseman | 38.3 | 17.9 | 0.0 | 0.0 | True | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 13 | [Rhûn] Kharaghûl Youth | kharaghul_youth | 38.1 | 20.4 | 0.0 | 0.0 | True | True | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 14 | [Harad] Camel Lancer | harad_camel_lancer | 37.7 | 17.1 | 0.0 | 0.0 | True | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 15 | [Rhûn] Wainrider Horseman | wainrider_horseman | 35.5 | 16.0 | 0.0 | 0.0 | True | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 16 | [Rhûn] Far-Rhun Horse Master | far_rhun_horse_master | 35.2 | 13.9 | 0.0 | 0.0 | True | True | Skirmishers | khuzait | 21.0 | special_or_unlinked |
| 17 | [Rhûn] Kharaghûl Raider | kharaghul_raider | 35.2 | 13.9 | 0.0 | 0.0 | True | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 18 | [Rhûn] Far-Rhun Cavalry | far_rhun_cavalry | 35.2 | 13.9 | 0.0 | 0.0 | True | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 19 | [Rhûn] Easterling Cavalry | easterling_cavalry_new | 35.2 | 13.9 | 0.0 | 0.0 | True | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 20 | [Dunland] Caru-lûth Rider | dunland_stag_rider | 33.7 | 28.6 | 0.0 | 0.0 | False | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 21 | [Dunland] Caru-lûth Noble Lancer | dunland_stag_noble_lancer | 33.7 | 28.5 | 0.0 | 0.0 | False | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 22 | [Umbar] Naru n'Aru Royal Knights | umbar_elite_root0001 | 29.9 | 18.4 | 2.4 | 0.6 | True | True | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 23 | [Rivendell] Noble | rivendell_noble | 27.6 | 36.0 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 36.0 | main_or_minor_line |
| 24 | [Rivendell] Royal Guard | rivendell_royal_guard | 27.6 | 36.0 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 25 | [ARhûn] Wainrider Swift-Chariot | wainrider_swift_chariot | 27.5 | 5.6 | 0.0 | 0.0 | True | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 26 | [Rhûn] Wainrider Warlord Chariot | wainrider_warlord_chariot | 27.5 | 5.6 | 0.0 | 0.0 | True | True | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 27 | [Mirkwood] Mirkwood Béleglas | mirkwood_beleglas | 27.4 | 35.7 | 0.0 | 0.0 | False | True | Defensive Troops | mirkwood | 46.0 | main_or_minor_line |
| 28 | [Mirkwood] Mirkwood Róchenlas | mirkwood_rochenlas | 27.4 | 35.7 | 0.0 | 0.0 | False | True | Defensive Troops | mirkwood | 41.0 | main_or_minor_line |
| 29 | [Rivendell] Nõldorin Lancer | noldorin_lancer | 27.4 | 35.7 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 46.0 | main_or_minor_line |
| 30 | [Rivendell] Rochannon Elenath | rivendell_glorfindel_guard | 27.4 | 35.7 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 31 | [Umbar] Auxiliary Recruit | aux_basic | 26.6 | 17.3 | 23.0 | 9.1 | True | False | Skirmishers | umbar | 6.0 | special_or_unlinked |
| 32 | [Harad] Rider of the Golden Veil | harad_horsearcher | 25.5 | 20.6 | 0.0 | 0.0 | False | True | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 33 | [Harad] Serpent Archer | harad_serpenthorsearcher | 25.5 | 20.6 | 0.0 | 0.0 | False | True | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 34 | [Harad] Sunlance | harad_sunlance | 24.7 | 8.6 | 0.0 | 0.0 | True | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 35 | [Harad] Bronze Fang | harad_bronzefang | 24.7 | 8.6 | 0.0 | 0.0 | True | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 36 | [Harad] Warlance | harad_warlance | 24.7 | 8.6 | 0.0 | 0.0 | True | False | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 37 | [Rhûn] Militia Spearman | rhun_militia_spearman | 23.4 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 38 | [Rhûn] Militia Veteran Spearman | rhun_militia_veteran_spearman | 23.4 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 39 | [Harad] Militia Spearman | harad_militia_spearman | 23.4 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 11.0 | special_or_unlinked |
| 40 | [Harad] Militia Veteran Spearman | harad_militia_veteran_spearman | 23.4 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 41 | [Dunland] Caru-lûth Lancer | dunland_stag_lancer | 22.9 | 14.5 | 0.0 | 0.0 | False | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 42 | [Harad] Spear Fighter | harad_spearfighter | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 43 | [Harad] Spear Guard | harad_spearguard | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 44 | [Rhûn] Far-Rhun Levy | far_rhun_levy | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 45 | Harad Veteran Caravan Guard | veteran_caravan_guard_harad | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 21.0 | special_or_unlinked |
| 46 | [Harad] Footman | harad_footman | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 47 | [Rhûn] Balcoth Volunteer | balcoth_volunteer | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 48 | [Rhûn] Sagarûn Watchman | sagarun_watchman | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 49 | [Rhûn] Sagarûn Deckhand | sagarun_deckhand | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 50 | [Harad] Sword Fighter | harad_swordfighter | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 51 | [Rhûn] Balcoth Axeman | balcoth_axeman | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 52 | Harad Caravan Guard | caravan_guard_harad | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 53 | Guard | guard_harad | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 54 | [Harad] Levy | harad_levy | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 6.0 | main_or_minor_line |
| 55 | [Rhûn] Far-Rhun Infantry | far_rhun_infantry | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 56 | [Rhûn] Far-Rhun Footman | far_rhun_footman | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 57 | [Rhûn] Easterling Halberdier | easterling_halberdier_new | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 58 | [Harad] Champion | harad_champion | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 31.0 | main_or_minor_line |
| 59 | [Rhûn] Balcoth Footman | balcoth_footman | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 60 | [Rhûn] Easterling Footman | easterling_footman_new | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 61 | [Harad] Militia | harad_militia | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 62 | [Rhûn] Easterling Militia | easterling_militia | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 63 | [Rhûn] Easterling Swordsman | easterling_swordsman_new | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 64 | [Rhûn] Easterling Recruit | easterling_recruit | 22.6 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 6.0 | main_or_minor_line |
| 65 | [Rhûn] Wainrider Khan's Chosen | wainrider_khans_chosen | 22.5 | 12.6 | 0.0 | 0.0 | True | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 66 | [Rhûn] Wain Footman | wain_footman | 21.1 | 5.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 67 | [Rhûn] Wain Youngblood | wain_youngblood | 21.1 | 5.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 68 | [Rhûn] Wain Glaiveman | wain_glaiveman | 21.1 | 5.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 69 | [Dunland] Avanc-lûth Noble Cavalry | dunland_lizard_noble_cavalry | 21.1 | 25.8 | 0.0 | 0.0 | False | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 70 | [Dale] Dalian Riverman | dale_riverman | 20.7 | 17.8 | 0.0 | 0.0 | True | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 71 | [Dale] Dalian Mariner | dale_dalian_mariner | 20.7 | 17.8 | 0.0 | 0.0 | True | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 72 | [Dale] Dalian Shipman | dale_shipman | 20.7 | 17.8 | 0.0 | 0.0 | True | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 73 | [Dale] Dalian Veteran Northman Scout | dale_veteran_northman_scout | 20.7 | 26.9 | 0.0 | 0.0 | False | True | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 74 | [Dale] Dalian Heavy Cavalry | dale_kinsman_of_eorl | 20.7 | 26.9 | 0.0 | 0.0 | False | True | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 75 | [Dale] Dalian Cavalry | dale_royal_cavalier | 20.7 | 26.9 | 0.0 | 0.0 | False | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 76 | [Dale] Dalian Northman Scout | dale_knight | 20.7 | 26.9 | 0.0 | 0.0 | False | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 77 | [Umbar] Adûnaim Recruits | umbar_elite | 20.5 | 15.3 | 19.2 | 8.3 | True | False | Skirmishers | umbar | 11.0 | main_or_minor_line |
| 78 | [Dale] Dalian Merchant Guard | dale_outrider | 20.0 | 26.1 | 0.0 | 0.0 | False | True | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 79 | [Dunland] Hebog-lûth Noble Horse Archer | dunland_falcon_noble_horse_archer | 19.3 | 25.2 | 0.0 | 0.0 | False | True | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 80 | [Rohan] Wold Veteran Horse Rider | rohan_wold_veteran_horse_archer | 18.6 | 10.6 | 0.0 | 0.0 | False | True | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 81 | [Rohan] Wold Scout | rohan_wold_scout | 18.4 | 10.3 | 0.0 | 0.0 | False | True | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 82 | [Rohan] Éothéod Horse Archer | rohan_wold_kings_own_horse_archer | 18.1 | 9.9 | 0.0 | 0.0 | False | True | Ranged Troops | vlandia | 36.0 | main_or_minor_line |
| 83 | [Rohan] Wold Elite Horse Rider | rohan_wold_elite_horse_archer | 18.1 | 9.9 | 0.0 | 0.0 | False | True | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 84 | [Rohan] Wold Horse Archer | rohan_wold_horse_archer | 17.8 | 9.5 | 0.0 | 0.0 | False | True | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 85 | [Dunland] Avanc-lûth Outrider | dunland_lizard_outrider | 17.4 | 21.0 | 0.0 | 0.0 | False | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 86 | [Rhûn] Darkhûn Cavalry | darkhun_cavalry | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 87 | [Rhûn] Kharaghûl Nokor | kharaghul_nokor | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 88 | [Rhûn] Kharaghûl Keshig | kharaghul_keshig | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 89 | [Rhûn] Darkhûn Cultist Knight | darkhun_cultist_knight | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 90 | [Rhûn] Kharaghûl Ashkur Nokor | kharaghul_ashkur_nokor | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 91 | [Rhûn] Darkhûn Horseman | darkhun_horseman | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 92 | [Rohan] Wold Eorlingas Horse Archer | rohan_wold_eorlingas_horse_archer | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Ranged Troops | vlandia | 31.0 | main_or_minor_line |
| 93 | [Rhûn] Easterling Veteran Cavalry | easterling_veteran_cavalry | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 94 | [Rhûn] Far-Rhun Kataphract | far_rhun_cataphract | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 95 | [Rhûn] Darkhûn Knight | darkhun_knight | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 96 | [Rhûn] Far-Rhun Iron Kataphract | far_rhun_iron_cataphract | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 97 | [Rhûn] Kharaghûl Horse Master | kharaghul_horse_master | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 98 | [Rhûn] Darkhûn Veteran Cavalry | darkhun_veteran_cavalry | 17.3 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 99 | [Dunland] Hebog-lûth Horse Archer | dunland_falcon_wildrider | 16.7 | 21.8 | 0.0 | 0.0 | False | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 100 | [Rhûn] Loke-Rim Cavalry | loke_rim_cavalry | 16.5 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 101 | [Rhûn] Kharaghûl Horse Archer | kharaghul_horse_archer | 16.5 | 8.9 | 0.0 | 0.0 | False | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 102 | [Rhûn] Kharaghûl Horse Scout | kharaghul_horse_scout | 16.5 | 8.9 | 0.0 | 0.0 | False | True | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 103 | [Umbar] Naru n'Aru Royal Guard | umbar_elite_root0000 | 16.1 | 10.7 | 2.4 | 0.6 | True | False | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 104 | [Rohan] Wold Recruit | rohan_wold_recruit | 16.1 | 7.3 | 0.0 | 0.0 | False | True | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 105 | [Umbar] Abrazanim Nardutarik | umbar_elite_root000 | 14.1 | 8.6 | 2.4 | 0.6 | True | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 106 | [Dunland] Avanc-lûth Horseman | dunland_lizard_horseman | 14.0 | 16.6 | 0.0 | 0.0 | False | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 107 | Rhun Caravan Guard | caravan_guard_rhun | 13.0 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | special_or_unlinked |
| 108 | Rhun Veteran Caravan Guard | veteran_caravan_guard_rhun | 13.0 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 21.0 | special_or_unlinked |
| 109 | Guard | guard_rhun | 13.0 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | special_or_unlinked |
| 110 | [Rhûn] Loke-Rim Initiate | loke_rim_initiate | 13.0 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 111 | [Rhûn] Dragon-Wrath Acolyte | dragon_wrath_acolyte | 13.0 | 8.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 112 | [Umbar] Rozadan Footmen | umbar_elite_root00 | 13.0 | 7.4 | 2.4 | 0.6 | True | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 113 | [Rhûn] Wain Darkhan | wain_darkhan | 12.0 | 5.6 | 0.0 | 0.0 | True | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 114 | [Mordor] Black Uruk Warrior | mordor_uruk_warrior | 10.9 | 1.5 | 0.0 | 0.0 | True | False | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 115 | [Rhûn] Wain Iron-Glaive | wain_iron_glaive | 10.7 | 5.6 | 0.0 | 0.0 | True | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 116 | [Aharad] Mumakil Rider | harad_mumakil_rider | 10.5 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | aserai | 51.0 | special_or_unlinked |
| 117 | [Aharad] Elephant Rider | harad_elephant_rider | 10.5 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | aserai | 51.0 | special_or_unlinked |
| 118 | [Dunland] Hebog-lûth Scout | dunland_falcon_archer | 10.2 | 13.3 | 0.0 | 0.0 | False | True | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 119 | [Rohan] West Emnet Heavy Shock Cavalry | rohan_westemnet_kings_own_rider | 10.1 | 11.4 | 0.0 | 0.0 | False | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 120 | [Rohan] Riders of Rohan | rohan_edoras_golden_hall_supreme_rider | 8.9 | 9.9 | 0.0 | 0.0 | False | True | Skirmishers | vlandia | 41.0 | main_or_minor_line |
| 121 | [Rohan] King's Knight | rohan_edoras_golden_hall_eorlingas_rider | 8.9 | 9.9 | 0.0 | 0.0 | False | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 122 | [Rohan] West Emnet Medium Cavalry | rohan_westemnet_eorlingas_rider | 8.9 | 9.9 | 0.0 | 0.0 | False | True | Skirmishers | vlandia | 26.0 | main_or_minor_line |
| 123 | [Gondor] Dol Amroth Veteran Knight | gondor_da_vet_knight | 8.3 | 10.8 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 124 | [Gondor] Dol Amroth Squire | gondor_da_squire | 8.3 | 10.8 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 125 | [Gondor] Dol Amroth Knight | gondor_da_knight | 8.3 | 10.8 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 126 | [Gondor] Dol Amroth Cavalry | gondor_da_cavalry | 8.3 | 10.8 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 127 | [Gondor] Swan Knight | gondor_da_swan_knight | 8.3 | 10.8 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 46.0 | main_or_minor_line |
| 128 | [Gondor] Pinnath Gelin Veteran Horseman | gondor_pg_vet_cavalry | 8.2 | 9.0 | 0.0 | 0.0 | False | True | Skirmishers | gondor | 31.0 | main_or_minor_line |
| 129 | [Rohan] West Emnet Light Cavalry | rohan_westemnet_elite_rider | 8.2 | 10.6 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 130 | [Rohan] East Emnet Elite Lancer | rohan_eastemnet_elite_lancer | 8.2 | 10.6 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 131 | [Rohan] King's Lancer | rohan_edoras_golden_hall_elite_rider | 8.2 | 10.6 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 132 | [Rohan] King's Royal Guard | rohan_edoras_golden_hall_kings_own_rider | 8.1 | 8.9 | 0.0 | 0.0 | False | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 133 | [Rohan] West Emnet Shock Cavalry | rohan_westemnet_royal_rider | 8.1 | 8.9 | 0.0 | 0.0 | False | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 134 | [Rivendell] Imladris Outrider | imladris_outrider | 7.9 | 10.3 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 135 | [Rohan] East Emnet Lance Rider | rohan_eastemnet_lance_rider | 7.9 | 10.3 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 136 | [Rivendell] Imladris Horse Archer | imladris_horse_archer | 7.9 | 10.3 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 137 | [Rohan] West Emnet Rider | rohan_westemnet_rider | 7.9 | 10.3 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 138 | [Rohan] East Emnet King's Lancer | rohan_eastemnet_kings_own_lancer | 7.6 | 9.9 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 36.0 | main_or_minor_line |
| 139 | [Rivendell] Rider of Himring | rider_of_himring | 7.6 | 9.9 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 46.0 | main_or_minor_line |
| 140 | [Rivendell] High Captain | rivendell_high_captain | 7.6 | 9.9 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 141 | [Rivendell] Royal Knight | rivendell_royal_knight | 7.6 | 9.9 | 0.0 | 0.0 | False | True | Defensive Troops | rivendell | 46.0 | main_or_minor_line |
| 142 | [Rohan] East Emnet Eorlingas Lancer | rohan_eastemnet_eorlingas_lancer | 7.6 | 9.9 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 143 | [Rohan] East Emnet Veteran Lancer | rohan_eastemnet_veteran_lancer | 7.3 | 9.5 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 144 | [Rohan] King's Horseman | rohan_edoras_golden_hall_veteran_rider | 7.3 | 9.5 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 145 | [Rohan] West Emnet Horseman | rohan_westemnet_veteran_rider | 7.3 | 9.5 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 146 | [Rohan] King's Rider | rohan_edoras_golden_hall_rider | 7.3 | 9.5 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 147 | [Gondor] Pinnath Gelin Light Horseman | gondor_pg_cavalry | 7.1 | 7.5 | 0.0 | 0.0 | False | True | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 148 | [Gondor] Anfalas Veteran Cavalry | gondor_anf_vet_cavalry | 6.9 | 9.0 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 149 | [Gondor] Arndir Veteran Knight | gondor_arn_vet_knight | 6.9 | 9.0 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 150 | [Gondor] Arndir Knight | gondor_arn_knight | 6.9 | 9.0 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 151 | [Gondor] Arndir Hill-Knight | gondor_arn_hill_knight | 6.9 | 9.0 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 152 | [Gondor] Arndir Cavalry | gondor_arn_cavalry | 6.9 | 9.0 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 153 | [Gondor] Anórien Knight | gondor_ano_mt_knight | 6.9 | 9.0 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 154 | [Gondor] Anórien Heavy Cavalry | gondor_ano_mt_heavy_cavalry | 6.9 | 9.0 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 155 | [Gondor] Anfalas Cavalry | gondor_anf_cavalry | 6.9 | 9.0 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 156 | [Rhûn] Balcoth Horse Archer | balcoth_horse_archer | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 157 | [Dol Guldur] Khamûl's Veiled Knight | dg_khamul_veiled_knight | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | dolguldur | 41.0 | main_or_minor_line |
| 158 | [Dol Guldur] Khamûl's Shadow-Knight | dg_khamul_shadow_knight | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | dolguldur | 46.0 | main_or_minor_line |
| 159 | [Rhûn] Dragon-Wrath Ash Knight | dragon_wrath_ash_knight | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 160 | [Rhûn] Balcoth Farshot Horse Archer | balcoth_farshot_horse_archer | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 161 | [Rhûn] Kharaghûl Karash Keshig | kharaghul_karash_keshig | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 162 | [Rhûn] Dragon-Wrath Obsidian Knight | dragon_wrath_obsidian_knight | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 163 | [Rhûn] Loke-Rim Gilded Kataphract | loke_rim_gilded_cataphract | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 164 | [Rhûn] Loke-Rim Kataphract | loke_rim_cataphract | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 165 | [Rhûn] Dragon-Wrath Lancer | dragon_wrath_lancer | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 166 | [Rohan] East Emnet Royal Lancer | rohan_eastemnet_royal_lancer | 6.8 | 8.9 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 167 | [Dale] Dalian King's Guard | dale_kings_guard | 6.4 | 8.3 | 0.0 | 0.0 | False | True | Defensive Troops | sturgia | 31.0 | main_or_minor_line |
| 168 | [Gondor] Anórien Cavalry | gondor_ano_mt_cavalry | 5.8 | 7.5 | 0.0 | 0.0 | False | True | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 169 | [Rohan] West Emnet Recruit | rohan_westemnet_recruit | 5.6 | 7.3 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 170 | [Rohan] East Emnet Recruit | rohan_eastemnet_recruit | 5.6 | 7.3 | 0.0 | 0.0 | False | True | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 171 | [Gundabad] Pale Uruk Wolf Rider | gundabad_warg_tamer | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | gundabad | 31.0 | main_or_minor_line |
| 172 | [Isengard] Orc Warg Scout | isengard_orc_warg_scout_v2 | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | isengard | 6.0 | main_or_minor_line |
| 173 | [Isengard] Orc Warg Rider | isengard_orc_warg_rider_v2 | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 174 | [Isengard] Orc Warg Ravager | isengard_orc_warg_ravager_v2 | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 175 | [Isengard] Orc Warg Raider | isengard_orc_warg_raider_v2 | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 176 | [Dol Guldur] Warg Ravager | dg_warg_skirmisher | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | dolguldur | 26.0 | main_or_minor_line |
| 177 | [Dol Guldur] Warg Tracker | dg_warg_scout | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | dolguldur | 16.0 | main_or_minor_line |
| 178 | [Dol Guldur] Warg Fang | dg_warg_red_fang | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | dolguldur | 31.0 | main_or_minor_line |
| 179 | [Dol Guldur] Warg Rider | dg_warg_raider | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 180 | [Dol Guldur] Fell Ravager | dg_fell_warg_rider | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | dolguldur | 36.0 | main_or_minor_line |
| 181 | [Gundabad] Despoiler of the Vale | gundabad_despoiler_of_the_vale | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Ranged Troops | gundabad | 26.0 | main_or_minor_line |
| 182 | [Gundabad] Azog's Defiler | gundabad_dread_rider_of_the_tower | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | gundabad | 41.0 | main_or_minor_line |
| 183 | [Mordor] Nurn Beast Master | mordor_warg_beastmaster | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 184 | [Mordor] Nurn Warg Ravager | mordor_warg_ravager | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 185 | Spider Rider | taom_spider_creature | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | dolguldur | 20.0 | special_or_unlinked |
| 186 | [Mordor] Nurn Warg Reaver | mordor_warg_reaver | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 187 | [Isengard] Orc Warg-Rider Enforcer | orc_warg_enforcer | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 188 | [Isengard] Orc Warg-Rider Lieutenant | orc_warg_lieutenant | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 189 | [Isengard] Orc Warg-Rider Overseer | orc_warg_overseer | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 190 | [Isengard] Orc Warg-Rider Scout | orc_warg_scout | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 191 | [Gundabad] Pale Uruk Fang Rider | gundabad_tracker | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | gundabad | 36.0 | main_or_minor_line |
| 192 | [Gundabad] Scout | gundabad_scout | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Ranged Troops | gundabad | 21.0 | main_or_minor_line |
| 193 | [Mordor] Nurn Warg Raider | mordor_warg_raider | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | mordor | 11.0 | main_or_minor_line |


## Ranked — Offensive melee (177 troops)

| rank | troop_name | troop_id | offensive_melee_role_score | crafted_melee_score_base | crafted_melee_template | crafted_melee_item | defense_score_base | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Rhûn] Wainrider Cavalry | wainrider_cavalry | 89.8 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 31.2 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 2 | [Dunland] Caru-lûth Noble Lancer | dunland_stag_noble_lancer | 89.4 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 28.5 | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 3 | [Rhûn] Kharaghûl Nokor | kharaghul_nokor | 86.5 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 4 | [Rhûn] Kharaghûl Ashkur Nokor | kharaghul_ashkur_nokor | 86.5 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 5 | [Rhûn] Darkhûn Cultist Knight | darkhun_cultist_knight | 86.5 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 6 | [Rhûn] Far-Rhun Iron Kataphract | far_rhun_iron_cataphract | 86.5 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 7 | [Rhûn] Darkhûn Knight | darkhun_knight | 86.5 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 8 | [Rhûn] Darkhûn Veteran Cavalry | darkhun_veteran_cavalry | 86.5 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 9 | [Harad] Fang of the King | harad_fangking | 86.5 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 29.2 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 10 | [Rhûn] Wainrider Warlord Chariot | wainrider_warlord_chariot | 86.1 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 5.6 | True | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 11 | [ARhûn] Wainrider Swift-Chariot | wainrider_swift_chariot | 86.1 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 5.6 | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 12 | [Aharad] Mumakil Rider | harad_mumakil_rider | 85.2 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 0.0 | True | Defensive Troops | aserai | 51.0 | special_or_unlinked |
| 13 | [Aharad] Elephant Rider | harad_elephant_rider | 85.2 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 0.0 | True | Defensive Troops | aserai | 51.0 | special_or_unlinked |
| 14 | [Gondor] Pelargir Veteran Infantry | gondor_pel_vet_infantry | 79.3 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 0.0 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 15 | [Gondor] Pelargir Anchor Guard | gondor_pel_anchor_guard | 79.3 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 0.0 | False | Offensive Melee | gondor | 41.0 | main_or_minor_line |
| 16 | [Gondor] Serelond Coastwarden | gondor_ser_coastwarden | 79.3 | 82.0 | TwoHandedPolearm | imperial_spear_t2 | 0.0 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 17 | [Harad] Warlance | harad_warlance | 77.5 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 8.6 | False | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 18 | [Gondor] Harondor Frontier Guard | gondor_har_frontier_guard | 74.3 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3 | 0.0 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 19 | [Gondor] Pelargir Infantry | gondor_pel_infantry | 74.3 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 0.0 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 20 | [Gondor] Serelond Veteran Maceman | gondor_ser_vet_maceman | 74.3 | 82.0 | TwoHandedPolearm | imperial_spear_t2 | 0.0 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 21 | [Rohan] Éothéod Horse Archer | rohan_wold_kings_own_horse_archer | 72.1 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 9.9 | True | Ranged Troops | vlandia | 36.0 | main_or_minor_line |
| 22 | [Rhûn] Wainrider Horseman | wainrider_horseman | 71.0 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 16.0 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 23 | [Rhûn] Far-Rhun Kataphract | far_rhun_cataphract | 70.0 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 24 | [Rhûn] Kharaghûl Horse Master | kharaghul_horse_master | 70.0 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 25 | [Rhûn] Darkhûn Cavalry | darkhun_cavalry | 70.0 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 26 | [Rhûn] Easterling Veteran Cavalry | easterling_veteran_cavalry | 70.0 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 27 | [Harad] Camel Lancer | harad_camel_lancer | 69.3 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 17.1 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 28 | [Erebor] Shield-Breaker | erebor_noble_shield_breaker | 69.1 | 73.3 | ThrowingAxe | southern_throwing_axe_1_t4 | 0.0 | False | Offensive Melee | erebor | 41.0 | main_or_minor_line |
| 29 | [Erebor] Royal Warden | erebor_noble_royal_warden | 69.1 | 73.3 | ThrowingAxe | southern_throwing_axe_1_t4 | 0.0 | False | Offensive Melee | erebor | 46.0 | main_or_minor_line |
| 30 | [Erebor] Gate Warden | erebor_noble_gate_warden | 69.1 | 73.3 | ThrowingAxe | southern_throwing_axe_1_t4 | 0.0 | False | Offensive Melee | erebor | 41.0 | main_or_minor_line |
| 31 | [Erebor] Shield-Guard | erebor_noble_shield_guard | 69.1 | 73.3 | ThrowingAxe | southern_throwing_axe_1_t4 | 0.0 | False | Offensive Melee | erebor | 36.0 | main_or_minor_line |
| 32 | [Erebor] Veteran Axe-Guard | erebor_noble_veteran_axe_guard | 69.1 | 73.3 | ThrowingAxe | southern_throwing_axe_1_t4 | 0.0 | False | Offensive Melee | erebor | 36.0 | main_or_minor_line |
| 33 | [Umbar] Naru n'Aru Royal Knights | umbar_elite_root0001 | 68.5 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 18.4 | True | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 34 | [Dunland] Caru-lûth Rider | dunland_stag_rider | 67.1 | 82.0 | TwoHandedPolearm | empire_lance_2_t4 | 28.6 | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 35 | [Harad] Champion | harad_champion | 66.8 | 75.7 | OneHandedSword | aserai_sword_6_t4 | 8.6 | False | Defensive Troops | aserai | 31.0 | main_or_minor_line |
| 36 | [Harad] Serpent Guard | harad_serpentguard | 65.3 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 29.2 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 37 | [Umbar] Naru n'Aru Royal Guard | umbar_elite_root0000 | 65.0 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 10.7 | False | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 38 | [Rhûn] Loke-Rim Cavalry | loke_rim_cavalry | 63.8 | 75.7 | OneHandedSword | khuzait_sword_4_t4 | 8.9 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 39 | [Rhûn] Wain Glaiveman | wain_glaiveman | 59.7 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 5.6 | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 40 | [Rohan] Wold Eorlingas Horse Archer | rohan_wold_eorlingas_horse_archer | 58.4 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 8.9 | True | Ranged Troops | vlandia | 31.0 | main_or_minor_line |
| 41 | [Rhûn] Kharaghûl Keshig | kharaghul_keshig | 58.4 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 8.9 | True | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 42 | [Gondor] Pelargir Veteran | gondor_pel_veteran | 53.1 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 0.0 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 43 | [Gondor] Harondor Infantry | gondor_har_infantry | 53.1 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3 | 0.0 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 44 | [Rhûn] Easterling Veteran Halberdier | easterling_veteran_halberdier_new | 53.1 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Offensive Melee | khuzait | 26.0 | main_or_minor_line |
| 45 | [Harad] Bronze Fang | harad_bronzefang | 52.5 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 8.6 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 46 | [Harad] Sunlance | harad_sunlance | 52.5 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 8.6 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 47 | [Dunland] Caru-lûth Lancer | dunland_stag_lancer | 51.6 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 14.5 | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 48 | [Rhûn] Far-Rhun Horse Master | far_rhun_horse_master | 51.5 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 13.9 | True | Skirmishers | khuzait | 21.0 | special_or_unlinked |
| 49 | [Rhûn] Kharaghûl Raider | kharaghul_raider | 51.5 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 13.9 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 50 | [Rhûn] Easterling Cavalry | easterling_cavalry_new | 51.5 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 13.9 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 51 | [Rhûn] Far-Rhun Cavalry | far_rhun_cavalry | 51.5 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 13.9 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 52 | [Rhûn] Darkhûn Horseman | darkhun_horseman | 50.7 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.9 | True | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 53 | [Harad] Camel Rider | harad_camelrider | 50.5 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 59.8 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 54 | [Rhûn] Easterling Veteran Swordsman | easterling_veteran_swordsman_new | 49.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 55 | [Rhûn] Far-Rhun Gate Guard | far_rhun_gate_guard | 47.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 56 | [Rhûn] Balcoth Veteran Axeman | balcoth_veteran_axeman | 47.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 57 | [Gondor] Serelond Phalanx | gondor_ser_phalanx | 46.5 | 54.3 | Pike | vlandia_pike_1_t5 | 0.0 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 58 | [Gondor] Serelond Pikewarden | gondor_ser_pikewarden | 46.5 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 59 | [Gondor] Citadel Guard Captain | gondor_mt_captain | 46.5 | 54.3 | Pike | vlandia_pike_1_t5 | 0.0 | False | Offensive Melee | gondor | 41.0 | main_or_minor_line |
| 60 | [Gondor] Osgiliath Dome Guard | gondor_osg_dome_guard | 46.5 | 54.3 | Pike | vlandia_pike_1_t5 | 0.0 | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 61 | [Gondor] Citadel Guard Sergeant | gondor_mt_sergeant | 46.5 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 62 | [Gondor] Fountain Guard | gondor_mt_fountain_guard | 46.5 | 54.3 | Pike | vlandia_pike_1_t5 | 0.0 | False | Offensive Melee | gondor | 46.0 | main_or_minor_line |
| 63 | [Gondor] Ithil Guard Captain | gondor_ith_captain | 46.5 | 54.3 | Pike | vlandia_pike_1_t5 | 0.0 | False | Offensive Melee | gondor | 41.0 | main_or_minor_line |
| 64 | [Gondor] Cair Andros Pikeman | gondor_ca_pikeman | 46.5 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 65 | [Gondor] Ithil Guard Sergeant | gondor_ith_sergeant | 46.5 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 66 | [Gondor] Cair Andros Pikewarden | gondor_ca_pikewarden | 46.5 | 54.3 | Pike | vlandia_pike_1_t5 | 0.0 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 67 | [Umbar] Abrazanim Narduzagar | umbar_elite_root001 | 46.1 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 0.6 | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 68 | [Umbar] Abrazanim Nardutarik | umbar_elite_root000 | 46.1 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 8.6 | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 69 | [Umbar] Adûnaims Faithful | umbar_elite_root010 | 46.1 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 0.6 | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 70 | [Harad] Warrior of the Gilded Fang | harad_gildedfang | 46.0 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 29.2 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 71 | [Rhûn] Militia Veteran Spearman | rhun_militia_veteran_spearman | 44.8 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 8.6 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 72 | [Rhûn] Militia Spearman | rhun_militia_spearman | 44.8 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3|eastern_spear_4_t4 | 8.6 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 73 | [Dunland] Wild-man Spearman | dunland_veteran_spearman | 44.1 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 42.8 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 74 | [Rohan] Westfold Helmingas Heavy Axeman | rohan_westfold_veteran_2h_axeman | 43.9 | 73.3 | TwoHandedAxe | vlandia_2haxe_1_t4 | 0.0 | False | Offensive Melee | vlandia | 26.0 | main_or_minor_line |
| 75 | [Rohan] Westfold Helmingas Axeman | rohan_westfold_helmingas_axeman | 43.9 | 73.3 | OneHandedAxe | vlandia_axe_2_t4 | 0.0 | False | Offensive Melee | vlandia | 26.0 | main_or_minor_line |
| 76 | [Gondor] Osgiliath Guard | gondor_osg_guard | 43.2 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 77 | [Rohan] Wold Elite Horse Rider | rohan_wold_elite_horse_archer | 43.2 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 9.9 | True | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 78 | [Harad] Serpent Archer | harad_serpenthorsearcher | 42.4 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 20.6 | True | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 79 | [Harad] Serpent Eyes | harad_serpent_eye | 42.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | aserai | 31.0 | main_or_minor_line |
| 80 | [Gondor] Lossarnach Veteran Axe-Thrower | gondor_loss_vet_axe_thrower | 42.2 | 73.3 | ThrowingAxe | highland_throwing_axe_1_t2|southern_throwing_axe_1_t4 | 0.0 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 81 | [Dunland] Uch-lûth Iron Wall | dunland_ox_iron_wall | 41.9 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 82 | [Rohan] Militia Veteran Spearman | rohan_militia_veteran_spearman | 41.6 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 0.0 | False | Offensive Melee | vlandia | 16.0 | special_or_unlinked |
| 83 | [Rohan] Militia Spearman | rohan_militia_spearman | 41.6 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 0.0 | False | Offensive Melee | vlandia | 11.0 | special_or_unlinked |
| 84 | [Rhûn] Easterling Halberdier | easterling_halberdier_new | 40.1 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 8.6 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 85 | [Dunland] Militia Spearman | dunland_militia_spearman | 40.0 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 10.3 | False | Offensive Melee | empire | 11.0 | special_or_unlinked |
| 86 | [Dunland] Wild-man Swordman | dunland_veteran_swordman | 39.5 | 75.7 | OneHandedSword | battania_sword_4_t4 | 41.0 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 87 | [Rhûn] Kharaghûl Horse Archer | kharaghul_horse_archer | 38.9 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 8.9 | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 88 | [Rhûn] Wain Footman | wain_footman | 38.5 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 5.6 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 89 | [Harad] Militia Veteran Spearman | harad_militia_veteran_spearman | 37.1 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 8.6 | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 90 | [Harad] Militia Spearman | harad_militia_spearman | 37.1 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 8.6 | False | Defensive Troops | aserai | 11.0 | special_or_unlinked |
| 91 | [Rhûn] Balcoth Axeman | balcoth_axeman | 34.7 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 8.6 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 92 | [Rhûn] Far-Rhun Infantry | far_rhun_infantry | 34.7 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 8.6 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 93 | [Rhûn] Kharaghûl Rider | kharaghul_rider | 34.7 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 17.9 | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 94 | [Rhûn] Far-Rhun Horseman | far_rhun_horseman | 34.7 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 17.9 | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 95 | [Harad] Initiate of the Sand Blades | harad_sandblade | 34.5 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 29.2 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 96 | [Umbar] Abrazanim Nardubawib | umbar_elite_root100 | 34.0 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 0.6 | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 97 | [Umbar] Beruthiel's Rangers | umbar_elite_root101 | 34.0 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 0.6 | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 98 | [Gondor] Pelargir Skirmisher | gondor_pel_skirmisher | 33.9 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 0.0 | False | Offensive Melee | gondor | 21.0 | main_or_minor_line |
| 99 | [Harad] Viper | harad_vipereye | 33.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 100 | [Rhûn] Easterling Swordsman | easterling_swordsman_new | 33.0 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 8.6 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 101 | [Harad] Spear Guard | harad_spearguard | 33.0 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 8.6 | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 102 | [Umbar] Rozadan Halberdiers | umbar_elite_root01 | 32.3 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 0.6 | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 103 | [Rhûn] Easterling Veteran Archer | easterling_veteran_archer_new | 31.7 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 104 | [Rhûn] Wainrider Veteran Archer | wainrider_veteran_archer | 31.7 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 105 | [Rhûn] Sagarûn Crossbowman | sagarun_crossbowman | 31.7 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 106 | [Rhûn] Loke-Rim Archer | loke_rim_archer | 31.7 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 107 | [Rhûn] Sagarûn Skirmisher | sagarun_skirmisher | 31.7 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 108 | [Harad] Camel Scout | harad_camelscout | 31.4 | 82.0 | TwoHandedPolearm | southern_spear_3_t4 | 47.6 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 109 | [Gondor] Serelond Pikeman | gondor_ser_pikeman | 30.4 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 110 | [Gondor] Cair Andros Spearman | gondor_ca_spearman | 30.4 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 111 | [Rohan] Westfold Heavy Axeman | rohan_westfold_2h_axeman | 30.1 | 73.3 | TwoHandedAxe | sturgia_2haxe_1_t4 | 0.0 | False | Offensive Melee | vlandia | 21.0 | main_or_minor_line |
| 112 | [Rohan] Westfold Veteran Axeman | rohan_westfold_veteran_axeman | 30.1 | 73.3 | OneHandedAxe | vlandia_axe_2_t4 | 0.0 | False | Offensive Melee | vlandia | 21.0 | main_or_minor_line |
| 113 | Harad Veteran Caravan Guard | veteran_caravan_guard_harad | 29.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | aserai | 21.0 | special_or_unlinked |
| 114 | [Harad] Footman | harad_footman | 29.4 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 8.6 | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 115 | [Gondor] Osgiliath Infantry | gondor_osg_infantry | 29.1 | 54.3 | Pike | fine_pike_t4 | 0.0 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 116 | [Umbar] Rozadan Footmen | umbar_elite_root00 | 28.8 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 7.4 | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 117 | [Gondor] Lossarnach Axe-Thrower | gondor_loss_axe_thrower | 28.4 | 73.3 | ThrowingAxe | highland_throwing_axe_1_t2|northern_throwing_axe_1_t1|southern_throwing_axe_1_t4|western_throwing_axe_1_t1|woodland_throwing_axe_1_t1 | 0.0 | False | Offensive Melee | gondor | 21.0 | main_or_minor_line |
| 118 | [Harad] Rider of the Golden Veil | harad_horsearcher | 28.2 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 20.6 | True | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 119 | [Rohan] Wold Veteran Horse Rider | rohan_wold_veteran_horse_archer | 27.9 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 10.6 | True | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 120 | [Dunland] Uch-lûth Bodyguard | dunland_ox_guard | 27.9 | 54.3 | Pike | thamaskene_pike_t4 | 0.0 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 121 | [Dunland] Tribal Spearman | dunland_spearman | 27.3 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 20.7 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 122 | [Rhûn] Wain Youngblood | wain_youngblood | 25.1 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 5.6 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 123 | [Rhûn] Kharaghûl Horse Scout | kharaghul_horse_scout | 24.7 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 8.9 | True | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 124 | [Dunland] Tribal Swordsman | dunland_swordsman | 24.1 | 75.7 | OneHandedSword | empire_sword_5_t4 | 20.7 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 125 | [Rhûn] Sagarûn Watchman | sagarun_watchman | 22.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 126 | [Rhûn] Far-Rhun Footman | far_rhun_footman | 22.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 127 | [Harad] Sword Fighter | harad_swordfighter | 22.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 128 | [Rhûn] Balcoth Footman | balcoth_footman | 22.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 129 | [Rhûn] Easterling Footman | easterling_footman_new | 22.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 130 | [Dunland] Militia Veteran Archer | dunland_militia_veteran_archer | 21.5 | 75.7 | OneHandedAxe|OneHandedSword | battania_axe_1_t2|empire_sword_5_t4|sturgia_axe_2_t2 | 17.8 | False | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 131 | [Harad] Spear Fighter | harad_spearfighter | 20.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 132 | [Umbar] Rozadan Bowmen | umbar_elite_root10 | 20.2 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 21.3 | False | Ranged Troops | umbar | 21.0 | main_or_minor_line |
| 133 | [Dunland] Militia Archer | dunland_militia_archer | 20.0 | 73.3 | OneHandedAxe | battania_axe_1_t2|small_spurred_axe_t2|sturgia_axe_2_t2 | 9.5 | False | Ranged Troops | empire | 11.0 | special_or_unlinked |
| 134 | [Harad] Militia Archer | harad_militia_archer | 19.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | aserai | 11.0 | special_or_unlinked |
| 135 | [Harad] Marksman | harad_marksman | 19.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 136 | [Harad] Militia Veteran Archer | harad_militia_veteran_archer | 19.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | aserai | 16.0 | special_or_unlinked |
| 137 | [Dunland] Uch-lûth Pikeman | dunland_ox_pikeman | 18.9 | 54.3 | Pike | vlandia_pike_1_t5 | 0.0 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 138 | Harad Caravan Guard | caravan_guard_harad | 18.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 139 | [Rohan] Wold Horse Archer | rohan_wold_horse_archer | 18.1 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 9.5 | True | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 140 | [Rohan] Westfolders | rohan_westfold_axeman | 18.1 | 73.3 | OneHandedAxe | sturgia_axe_3_t3 | 0.0 | False | Offensive Melee | vlandia | 16.0 | main_or_minor_line |
| 141 | [Rhûn] Kharaghûl Youth | kharaghul_youth | 17.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 20.4 | True | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 142 | [Rhûn] Loke-Rim Bowman | loke_rim_bowman | 17.5 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 143 | [Rhûn] Easterling Archer | easterling_archer_new | 17.5 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 144 | [Rohan] Militia Archer | rohan_militia_archer | 17.5 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 0.0 | False | Ranged Troops | vlandia | 11.0 | special_or_unlinked |
| 145 | [Rohan] Eastfold Veteran Bowman | rohan_eastfold_veteran_bowman | 17.5 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 0.0 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 146 | [Rhûn] Militia Archer | rhun_militia_archer | 17.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 147 | [Rhûn] Militia Veteran Archer | rhun_militia_veteran_archer | 17.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 148 | [Rhûn] Balcoth Archer | balcoth_archer | 17.5 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 0.0 | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 149 | [Rohan] Militia Veteran Archer | rohan_militia_veteran_archer | 17.5 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 0.0 | False | Ranged Troops | vlandia | 16.0 | special_or_unlinked |
| 150 | [Umbar] Adûnaim Footmen | umbar_elite_root0 | 16.8 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 3.6 | False | Skirmishers | umbar | 16.0 | main_or_minor_line |
| 151 | [Harad] Youngblood of the Serpent | harad_noble | 15.2 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 29.2 | True | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 152 | [Rhûn] Sagarûn Deckhand | sagarun_deckhand | 13.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 153 | [Rhûn] Balcoth Volunteer | balcoth_volunteer | 13.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 154 | [Rhûn] Easterling Militia | easterling_militia | 13.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 155 | [Rhûn] Far-Rhun Levy | far_rhun_levy | 13.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 156 | Guard | guard_dale | 12.7 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 21.9 | False | Offensive Melee | sturgia | 16.0 | special_or_unlinked |
| 157 | Guard | guard_khand | 12.0 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 17.2 | False | Offensive Melee | battania | 16.0 | special_or_unlinked |
| 158 | Guard | guard_harad | 11.6 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 159 | Guard | guard_dunland | 11.5 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 14.0 | False | Offensive Melee | empire | 16.0 | special_or_unlinked |
| 160 | [Rohan] Wold Scout | rohan_wold_scout | 10.5 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 10.3 | True | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 161 | [Rohan] Wold Recruit | rohan_wold_recruit | 10.0 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 7.3 | True | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 162 | [Umbar] Adûnaim Bowmen | umbar_elite_root1 | 9.9 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 3.6 | False | Ranged Troops | umbar | 16.0 | main_or_minor_line |
| 163 | [Rohan] Westfold Militiaman | rohan_westfold_militiaman | 9.4 | 73.3 | OneHandedAxe | vlandia_axe_2_t4 | 0.0 | False | Offensive Melee | vlandia | 11.0 | main_or_minor_line |
| 164 | [Harad] Desert Archer | harad_archer | 8.6 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | aserai | 16.0 | main_or_minor_line |
| 165 | [Dunland] Tribal Raider | dunland_raider | 8.0 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 13.7 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 166 | [Rohan] East-Fold Bowman | rohan_eastfold_bowman | 6.8 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 0.0 | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 167 | [Umbar] Adûnaim Recruits | umbar_elite | 6.4 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 15.3 | False | Skirmishers | umbar | 11.0 | main_or_minor_line |
| 168 | [Harad] Militia | harad_militia | 6.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 169 | [Dunland] Tribal Hunter | dunland_hunter | 3.4 | 73.3 | OneHandedAxe | small_spurred_axe_t2 | 17.1 | False | Ranged Troops | empire | 11.0 | main_or_minor_line |
| 170 | [Harad] Levy | harad_levy | 2.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | aserai | 6.0 | main_or_minor_line |
| 171 | [Rhûn] Easterling Recruit | easterling_recruit | 2.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 8.6 | False | Defensive Troops | khuzait | 6.0 | main_or_minor_line |
| 172 | [Dunland] Peasant | dunland_peasant | 1.8 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 6.3 | False | Skirmishers | empire | 6.0 | main_or_minor_line |
| 173 | [Rohan] Eastfold Yeoman Archer | rohan_eastfold_skirmisher | 1.5 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 0.0 | False | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 174 | [Rohan] Eastfold Freeman | rohan_eastfold_recruit | 1.5 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 0.0 | False | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 175 | [Harad] Skirmisher | harad_skirmisher | 1.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 0.0 | False | Ranged Troops | aserai | 11.0 | main_or_minor_line |
| 176 | [Umbar] Auxiliary Recruit | aux_basic | 1.3 | 73.3 | TwoHandedAxe | peasant_2haxe_1_t1 | 17.3 | False | Skirmishers | umbar | 6.0 | special_or_unlinked |
| 177 | [Rohan] Westfold Recruit | rohan_westfold_recruit | 0.8 | 73.3 | OneHandedAxe | vlandia_axe_2_t4 | 0.0 | False | Offensive Melee | vlandia | 6.0 | main_or_minor_line |


## Ranked — Skirmisher (84 troops)

| rank | troop_name | troop_id | skirmisher_role_score | throw_score_base | throw_damage | direct_throw_item | crafted_throw_item | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Umbar] Naru n'Aru Royal Guard | umbar_elite_root0000 | 62.6 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 2 | [Harad] Camel Rider | harad_camelrider | 60.7 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 3 | [Dunland] Caru-lûth Noble Lancer | dunland_stag_noble_lancer | 60.6 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 4 | [Harad] Camel Scout | harad_camelscout | 57.7 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 5 | [Dunland] Caru-lûth Rider | dunland_stag_rider | 57.6 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 6 | [Umbar] Abrazanim Nardutarik | umbar_elite_root000 | 56.8 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 7 | [Umbar] Adûnaims Faithful | umbar_elite_root010 | 56.8 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 8 | [Umbar] Abrazanim Narduzagar | umbar_elite_root001 | 56.8 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 9 | [Harad] Fang of the King | harad_fangking | 56.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 10 | [Harad] Serpent Guard | harad_serpentguard | 53.1 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 11 | [Harad] Initiate of the Sand Blades | harad_sandblade | 53.1 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 12 | [Harad] Youngblood of the Serpent | harad_noble | 53.1 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 13 | [Harad] Warrior of the Gilded Fang | harad_gildedfang | 53.1 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 14 | [Dunland] Caru-lûth Lancer | dunland_stag_lancer | 51.0 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 15 | [Rhûn] Kharaghûl Rider | kharaghul_rider | 50.3 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 16 | [Rhûn] Far-Rhun Horseman | far_rhun_horseman | 50.3 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 17 | [Harad] Camel Lancer | harad_camel_lancer | 50.0 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 18 | [Rhûn] Easterling Cavalry | easterling_cavalry_new | 49.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 19 | [Rhûn] Far-Rhun Horse Master | far_rhun_horse_master | 49.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 21.0 | special_or_unlinked |
| 20 | [Rhûn] Kharaghûl Raider | kharaghul_raider | 49.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 21 | [Rhûn] Far-Rhun Cavalry | far_rhun_cavalry | 49.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 22 | [Dunland] Wild-man Spearman | dunland_veteran_spearman | 49.2 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 23 | [Dunland] Wild-man Swordman | dunland_veteran_swordman | 46.4 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 24 | [Harad] Warlance | harad_warlance | 45.3 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 25 | [Umbar] Naru n'Aru Royal Knights | umbar_elite_root0001 | 45.1 | 57.5 | 10.0 | throwing_stone | nan | True | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 26 | [Umbar] Rozadan Halberdiers | umbar_elite_root01 | 45.1 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 27 | [Umbar] Abrazanim Nardubawib | umbar_elite_root100 | 45.1 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 28 | [Umbar] Rozadan Footmen | umbar_elite_root00 | 45.1 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 29 | [Umbar] Beruthiel's Rangers | umbar_elite_root101 | 45.1 | 57.5 | 10.0 | throwing_stone | nan | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 30 | [Harad] Bronze Fang | harad_bronzefang | 42.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 31 | [Harad] Sunlance | harad_sunlance | 42.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 32 | [Umbar] Adûnaim Recruits | umbar_elite | 39.3 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 11.0 | main_or_minor_line |
| 33 | [Umbar] Adûnaim Footmen | umbar_elite_root0 | 39.3 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 16.0 | main_or_minor_line |
| 34 | [Umbar] Auxiliary Recruit | aux_basic | 39.3 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 6.0 | special_or_unlinked |
| 35 | [Umbar] Rozadan Bowmen | umbar_elite_root10 | 39.3 | 57.5 | 10.0 | throwing_stone | nan | False | Ranged Troops | umbar | 21.0 | main_or_minor_line |
| 36 | [Umbar] Adûnaim Bowmen | umbar_elite_root1 | 39.3 | 57.5 | 10.0 | throwing_stone | nan | False | Ranged Troops | umbar | 16.0 | main_or_minor_line |
| 37 | [Dunland] Tribal Spearman | dunland_spearman | 37.5 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 38 | [Dunland] Uch-lûth Iron Wall | dunland_ox_iron_wall | 37.4 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 39 | [Rhûn] Balcoth Veteran Axeman | balcoth_veteran_axeman | 36.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 40 | [Rhûn] Easterling Veteran Swordsman | easterling_veteran_swordsman_new | 36.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 41 | [Rhûn] Far-Rhun Gate Guard | far_rhun_gate_guard | 36.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 42 | [Dunland] Tribal Swordsman | dunland_swordsman | 35.1 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 43 | [Dunland] Uch-lûth Bodyguard | dunland_ox_guard | 34.3 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 44 | [Gondor] Osgiliath Dome Guard | gondor_osg_dome_guard | 32.8 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 45 | [Dunland] Tribal Raider | dunland_raider | 31.0 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 46 | [Dunland] Avanc-lûth Noble Cavalry | dunland_lizard_noble_cavalry | 29.2 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 47 | [Dunland] Peasant | dunland_peasant | 29.1 | 30.5 | 0.0 | nan | northern_javelin_1_t2 | False | Skirmishers | empire | 6.0 | main_or_minor_line |
| 48 | [Dunland] Uch-lûth Pikeman | dunland_ox_pikeman | 28.1 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 49 | [Rohan] Riders of Rohan | rohan_edoras_golden_hall_supreme_rider | 27.4 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | vlandia | 41.0 | main_or_minor_line |
| 50 | [Dunland] Avanc-lûth Outrider | dunland_lizard_outrider | 24.9 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 51 | [Rohan] West Emnet Heavy Shock Cavalry | rohan_westemnet_kings_own_rider | 24.7 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 52 | [Rohan] King's Royal Guard | rohan_edoras_golden_hall_kings_own_rider | 24.0 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 53 | [Rohan] King's Knight | rohan_edoras_golden_hall_eorlingas_rider | 21.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 54 | [Rohan] West Emnet Shock Cavalry | rohan_westemnet_royal_rider | 21.0 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 55 | [Dunland] Avanc-lûth Horseman | dunland_lizard_horseman | 20.7 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 56 | [Rohan] West Emnet Medium Cavalry | rohan_westemnet_eorlingas_rider | 18.1 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | vlandia | 26.0 | main_or_minor_line |
| 57 | [Gondor] Pinnath Gelin Veteran Horseman | gondor_pg_vet_cavalry | 17.3 | 30.5 | 0.0 | nan | western_javelin_3_t4 | True | Skirmishers | gondor | 31.0 | main_or_minor_line |
| 58 | [Dunland] Turch-lûth Huskarl | dunland_boar_warlord | 17.0 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 59 | [Dunland] Blaidd-lûth Champion | dunland_wolf_champion | 17.0 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 60 | [Dunland] Arth-lûth Executioner | dunland_bear_executioner | 17.0 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 61 | [Gondor] Pinnath Gelin Light Horseman | gondor_pg_cavalry | 16.9 | 30.5 | 0.0 | nan | western_javelin_2_t3 | True | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 62 | [Rhûn] Wain Darkhan | wain_darkhan | 15.3 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 63 | [Dunland] Arth-lûth Berserker | dunland_bear_berserker | 13.9 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 64 | [Dunland] Turch-lûth Ironhide | dunland_boar_boar_warrior | 13.9 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 65 | [Rhûn] Sagarûn Storm Forged Marine | sagarun_storm_forged_marine | 13.9 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 66 | [Dunland] Blaidd-lûth Axeman | dunland_wolf_axeman | 13.9 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 67 | [Gondor] Lebennin Sea Guard | gondor_leb_sea_guard | 12.4 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 68 | [Rhûn] Sagarûn Marine | sagarun_marine | 10.8 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 69 | [Rhûn] Far-Rhun Iron Legionary | far_rhun_iron_legionary | 10.8 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 70 | [Dunland] Blaidd-lûth Raider | dunland_wolf_raider | 7.7 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 71 | [Dunland] Arth-lûth Chosen | dunland_bear_chosen | 7.7 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 72 | [Rhûn] Sagarûn Storm Helmed Naffatun | sagarun_storm_helmed_naffatun | 7.7 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 73 | [Dunland] Turch-lûth Goreblade | dunland_boar_spearman | 7.7 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 74 | [Gondor] Lebennin Veteran Infantry | gondor_leb_vet_infantry | 6.2 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 75 | [Rhûn] Sagarûn Naffatun | sagarun_naffatun | 4.6 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 76 | [Dunland] Blaidd-lûth Warrior | dunland_clan_warrior | 1.5 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 77 | [Dunland] Turch-lûth Tuskrunner | dunland_boar_warrior | 1.5 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 78 | [Gondor] Harondor Javelineer | gondor_har_javelineer | 0.0 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 79 | [Dunland] Blaidd-lûth Noble Son | dunland_noble_son | 0.0 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 80 | [Gondor] Harondor Skirmisher | gondor_har_skirmisher | 0.0 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | gondor | 16.0 | main_or_minor_line |
| 81 | [Dunland] Turch-lûth Noble Son | dunland_boar_noble_son | 0.0 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 82 | [Gondor] Harondor Veteran Skirmisher | gondor_har_vet_skirmisher | 0.0 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | gondor | 21.0 | main_or_minor_line |
| 83 | [Gondor] Lebennin Infantry | gondor_leb_infantry | 0.0 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | gondor | 21.0 | main_or_minor_line |
| 84 | [Gondor] Lossarnach Skirmisher | gondor_loss_skirmisher | 0.0 | 30.5 | 0.0 | nan | eastern_javelin_2_t3|generic_javelin_1_t3|northern_javelin_2_t3|western_javelin_1_t2|western_javelin_2_t3 | False | Skirmishers | gondor | 16.0 | main_or_minor_line |

