# Troop overview — `taom` / `export_20260731_150800`

## Labels

- `evidence_basis=xml_structural`, `empirical=false` (ADR-004)
- Model: `role_scores_v1` conservative (crafted melee = proxy, not HTK)
- Package digest: `9444e75330ea380c75a06492e6b9b4cbda89582223e079437ba48d976f547db4`
- Rows scored: **1239**; after filters: **872** (excluded 367: untouched vanilla `change_type=inalterado` only)

## Tiers

- Main tables: `rank` + `tier` in **S / A / B / C / D** vs the best non-outlier score in that role (~within 10% of the leader → S; then A/B/C/D)
- **S+** = spectacle-scale outliers (giants / mammoths): listed in a separate section and **excluded** from the main S–D ladder so they do not crowd ordinary troop tiers

## Why columns

- **Defensive:** `defense_score_base` (driver) + `armor_total` / `effective_armor` (raw) + shield/horse flags
- **Ranged:** `ranged_score_base` (driver) + `ranged_damage` (weapon+ammo thrust) + item + horse/shield
- **Offensive melee:** `crafted_melee_score_base` + template/item (**no real weapon damage** — template proxy only)
- **Skirmisher:** `throw_score_base` + `throw_damage` when the throw item is a direct `Thrown` weapon (crafted javelins stay proxy-only)

## Filters

- Drop `change_type=inalterado` from the track override report (vanilla baseline troops the mod did not add/override)
- No name filters on Greyjoy / specials; giants/mammoths → S+ outliers section
- Full ranked lists below — filter locally as needed
- Intra-track only; do not compare ranks across tracks

## Ranked — Ranged (212 troops)

| rank | tier | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | has_horse | has_shield | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rivendell] Rider of Himring | rider_of_himring | 100.0 | 99.3 | 120.0 | highelf_longbowc|highelf_longbowd | True | False | Ranged Troops | rivendell | 46.0 | main_or_minor_line |
| 2 | S | [Rivendell] Imladris Horse Archer | imladris_horse_archer | 99.1 | 99.3 | 120.0 | highelf_longbowc|highelf_longbowd | True | False | Ranged Troops | rivendell | 41.0 | main_or_minor_line |
| 3 | A | [Rivendell] Imladris Marchwarden | imladris_marchwarden | 76.5 | 99.3 | 120.0 | highelf_longbowc|highelf_longbowd | False | False | Ranged Troops | rivendell | 41.0 | main_or_minor_line |
| 4 | A | [Rivendell] Imladris Marksman | imladris_marksman | 76.3 | 99.3 | 120.0 | highelf_longbowc|highelf_longbowd | False | False | Ranged Troops | rivendell | 36.0 | main_or_minor_line |
| 5 | A | [Rivendell] Imladris Archer | imladris_archer | 73.0 | 99.3 | 120.0 | highelf_longbowc|highelf_longbowd | False | False | Ranged Troops | rivendell | 31.0 | main_or_minor_line |
| 6 | B | [Mirkwood] Thingol's Heirs | mirkwood_thingolheir | 68.4 | 91.1 | 104.0 | wm_mirkwood_bow_a01 | False | False | Ranged Troops | mirkwood | 51.0 | main_or_minor_line |
| 7 | B | [Mirkwood] Silvan Borderwarden | mirkwood_borderwardens | 68.4 | 91.1 | 104.0 | wm_mirkwood_bow_a01 | False | False | Ranged Troops | mirkwood | 46.0 | main_or_minor_line |
| 8 | B | [Gondor] Lond-Galen Haven Guard | gondor_lg_haven_guard | 68.0 | 88.2 | 102.0 | wm_ithilien_bow_b | False | True | Ranged Troops | gondor | 41.0 | main_or_minor_line |
| 9 | B | [Mirkwood] Silvan Sentinels | mirkwood_sentinels | 67.8 | 91.1 | 104.0 | wm_mirkwood_bow_a01 | False | False | Ranged Troops | mirkwood | 41.0 | main_or_minor_line |
| 10 | B | [Gondor] Ithilien Ranger | gondor_ithilien_ranger | 66.8 | 91.9 | 107.0 | wm_ithilien_bow|wm_ithilien_bow_b|wm_ithilien_bow_c | False | False | Ranged Troops | gondor | 51.0 | special_or_unlinked |
| 11 | B | [Gondor] Citadel Guard Sharpshooter | gondor_mt_sharpshooter | 64.7 | 88.2 | 102.0 | wm_ithilien_bow_b | False | False | Ranged Troops | gondor | 41.0 | main_or_minor_line |
| 12 | B | [Gondor] Blackroot Vale Shadowbow | gondor_brv_shadowbow | 64.7 | 88.2 | 102.0 | wm_ithilien_bow_b | False | False | Ranged Troops | gondor | 41.0 | main_or_minor_line |
| 13 | B | [Rohan] Éothéod Horse Archer | rohan_wold_kings_own_horse_archer | 63.4 | 59.5 | 58.0 | steppe_war_bow | True | True | Ranged Troops | vlandia | 36.0 | main_or_minor_line |
| 14 | B | [Gondor] Lond-Galen Pavise Guard | gondor_lg_pavise_guard | 62.9 | 84.9 | 96.0 | wm_ithilien_bow | False | True | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 15 | B | [Rhûn] Dragon-Wrath Obsidian Warbow | dragon_wrath_obsidian_warbow | 62.4 | 82.9 | 95.0 | sm_rh_drag_longbow_a | False | False | Ranged Troops | khuzait | 46.0 | main_or_minor_line |
| 16 | B | [Rhûn] Kharaghûl Karash Keshig | kharaghul_karash_keshig | 62.3 | 62.1 | 57.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 17 | B | [Rhûn] Black Sun Chosen Marksman | black_sun_chosen_marksman | 61.1 | 82.9 | 95.0 | sm_rh_drag_longbow_a | False | False | Ranged Troops | khuzait | 41.0 | main_or_minor_line |
| 18 | B | [Rivendell] Imladris Bowman | imladris_bowman | 60.8 | 99.3 | 120.0 | highelf_longbowc|highelf_longbowd | False | False | Ranged Troops | rivendell | 26.0 | main_or_minor_line |
| 19 | B | [Rhûn] Dragon-Wrath Ash Marksman | dragon_wrath_ash_marksman | 60.8 | 82.9 | 95.0 | sm_rh_drag_longbow_a | False | False | Ranged Troops | khuzait | 41.0 | main_or_minor_line |
| 20 | B | [Rhûn] Loke-Rim Gilded Marksman | loke_rim_gilded_marksman | 60.6 | 88.1 | 108.0 | sm_rh_loke_longbow_a | False | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 21 | B | [Dol Guldur] Khamûl's Shadowbow | dg_khamul_shadow_bowman | 60.1 | 83.2 | 97.0 | sm_dg_khml_longbow_a | False | False | Ranged Troops | dolguldur | 46.0 | main_or_minor_line |
| 22 | B | [Gondor] Blackroot Vale Shadowhunter | gondor_brv_shadowhunter | 59.6 | 84.9 | 96.0 | wm_ithilien_bow | False | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 23 | B | [Gondor] Methir Composite Archer | gondor_met_composite_archer | 59.6 | 84.9 | 96.0 | wm_ithilien_bow | False | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 24 | B | [Gondor] Blackroot Vale Ranger | gondor_brv_ranger | 59.6 | 84.9 | 96.0 | wm_ithilien_bow | False | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 25 | B | [Gondor] Citadel Guard Longbowman | gondor_mt_longbowman | 59.6 | 84.9 | 96.0 | wm_ithilien_bow | False | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 26 | B | [Rohan] Wold Eorlingas Horse Archer | rohan_wold_eorlingas_horse_archer | 59.3 | 59.5 | 58.0 | steppe_war_bow | True | True | Ranged Troops | vlandia | 31.0 | main_or_minor_line |
| 27 | B | [Rhûn] Kharaghûl Keshig | kharaghul_keshig | 58.0 | 62.1 | 57.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 28 | B | [Iron Hills] Veteran Sharpshooter | iron_hills_noble_veteran_sharpshooter | 57.9 | 100.0 | 138.0 | sm_dwarf_iron_crossbow_heavy_b | False | False | Ranged Troops | erebor | 31.0 | main_or_minor_line |
| 29 | B | [Rhûn] Balcoth Farshot Horse Archer | balcoth_farshot_horse_archer | 57.8 | 62.1 | 57.0 | steppe_war_bow | True | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 30 | B | [Ironpass] Sharpshooter | ironpass_sharpshooter | 57.7 | 100.0 | 138.0 | sm_dwarf_iron_crossbow_heavy_b | False | False | Ranged Troops | erebor | 31.0 | main_or_minor_line |
| 31 | B | [Gondor] Tolfalas Sharpshooter | gondor_tol_sharpshooter | 57.6 | 82.4 | 103.0 | crossbow_f | False | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 32 | B | [Dol Guldur] Khamûl's Veiled Marksman | dg_khamul_veiled_marksman | 57.5 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | dolguldur | 41.0 | main_or_minor_line |
| 33 | B | [Gondor] Moon Guard | gondor_ith_moon_guard | 56.1 | 77.0 | 85.0 | gondor_steel_bow | False | False | Ranged Troops | gondor | 46.0 | main_or_minor_line |
| 34 | B | [Rhûn] Black Sun Marksman | black_sun_marksman | 55.9 | 82.9 | 95.0 | sm_rh_drag_longbow_a | False | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 35 | B | [Gondor] Ithil Guard Sharpshooter | gondor_ith_sharpshooter | 55.8 | 77.0 | 85.0 | gondor_steel_bow | False | False | Ranged Troops | gondor | 41.0 | main_or_minor_line |
| 36 | B | [Dol Guldur] Shadow Marksman | dg_khamul_shadow_marksman | 53.3 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | dolguldur | 36.0 | main_or_minor_line |
| 37 | B | [Gondor] Ithil Guard Longbowman | gondor_ith_longbowman | 53.1 | 77.0 | 85.0 | gondor_steel_bow | False | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 38 | B | [Rhûn] Sagarûn Storm Marked Arbalest | sagarun_storm_marked_arbalest | 51.6 | 76.4 | 96.0 | crossbow_d | False | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 39 | B | [Dale] Dalian Royal Crossbowman | dale_master_crossbowman | 51.0 | 78.3 | 103.0 | crossbow_f | False | True | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 40 | B | [Harad] Serpent Archer | harad_serpenthorsearcher | 49.2 | 60.4 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 41 | B | [Rohan] Wold Elite Horse Rider | rohan_wold_elite_horse_archer | 48.1 | 59.5 | 58.0 | steppe_war_bow | True | True | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 42 | B | [Rhûn] Loke-Rim Marksman | loke_rim_marksman | 47.7 | 88.1 | 108.0 | sm_rh_loke_longbow_a | False | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 43 | B | [Erebor] Veteran Archer | erebor_noble_veteran_archer | 47.4 | 79.2 | 95.0 | sm_dwarf_erebor_bow_b | False | True | Ranged Troops | erebor | 31.0 | main_or_minor_line |
| 44 | B | [Ironpass] Veteran Arbalest | ironpass_veteran_arbalest | 46.6 | 100.0 | 138.0 | sm_dwarf_iron_crossbow_heavy_a|sm_dwarf_iron_crossbow_heavy_b | False | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 45 | B | [Gondor] Osgiliath Longbowman | gondor_osg_longbowman | 45.8 | 75.7 | 88.0 | wm_gondor_bow | False | True | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 46 | B | [Isengard] Uruk-Hai Veteran Crossbowman | urukhai_veterancrossbowman | 45.7 | 79.9 | 105.0 | wm_isengard_crossbow_a01 | False | False | Ranged Troops | isengard | 31.0 | main_or_minor_line |
| 47 | B | [Gondor] Methir Veteran Archer | gondor_met_vet_archer | 45.3 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 48 | B | [Gondor] Blackroot Vale Veteran Archer | gondor_brv_vet_archer | 45.3 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 49 | B | [Gondor] Lebennin Longbowman | gondor_leb_longbowman | 44.8 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 50 | B | [Dale] Dalian Barding | dale_black_arrow_marksman | 44.8 | 69.1 | 79.0 | dale_longbow_a | False | True | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 51 | B | [Rivendell] Militia Veteran Archer | rivendell_militia_veteran_archer | 44.7 | 92.5 | 115.0 | highelf_longbowa|highelf_longbowb | False | False | Ranged Troops | rivendell | 16.0 | special_or_unlinked |
| 52 | B | [Rhûn] Kharaghûl Horse Archer | kharaghul_horse_archer | 44.6 | 60.9 | 55.0 | composite_steppe_bow | True | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 53 | B | [Dol Guldur] Uruk Black Sharpshooter | dg_uruk_black_sharpshooter | 44.6 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | dolguldur | 31.0 | main_or_minor_line |
| 54 | B | [Rhûn] Balcoth Horse Archer | balcoth_horse_archer | 44.6 | 60.9 | 55.0 | composite_steppe_bow | True | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 55 | B | [Rhûn] Black Sun Longbowman | black_sun_longbowman | 44.6 | 82.9 | 95.0 | sm_rh_drag_longbow_a | False | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 56 | B | [Dunland] Draig-lûth Sharpshooter | dunland_dragon_sniper | 44.4 | 74.1 | 96.0 | crossbow_d | False | True | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 57 | B | [Iron Hills] Sharpshooter | iron_hills_noble_sharpshooter | 43.6 | 94.7 | 128.0 | sm_dwarf_iron_crossbow_heavy_a | False | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 58 | B | [Umbar] Abrazanim Nardubawib | umbar_elite_root100 | 43.5 | 95.6 | 117.0 | highelf_longbowc | False | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 59 | B | [Gundabad] Despoiler of the Vale | gundabad_despoiler_of_the_vale | 43.3 | 60.4 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | gundabad | 26.0 | main_or_minor_line |
| 60 | B | [Mirkwood] Militia Archer | mirkwood_militia_archer | 42.6 | 88.0 | 104.0 | wm_mirkwood_bow_a01|wm_mirkwood_bow_a02 | False | False | Ranged Troops | mirkwood | 11.0 | special_or_unlinked |
| 61 | B | [Rivendell] Militia Archer | rivendell_militia_archer | 41.4 | 89.9 | 110.0 | highelf_longbow_starter|highelf_longbowa | False | False | Ranged Troops | rivendell | 11.0 | special_or_unlinked |
| 62 | B | [Rhûn] Dragon-Wrath Longbowman | dragon_wrath_longbowman | 41.1 | 62.1 | 57.0 | steppe_war_bow | False | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 63 | B | [Dol Guldur] Shadow Archer | dg_khamul_shadow_archer | 40.8 | 77.8 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | dolguldur | 31.0 | main_or_minor_line |
| 64 | B | [Mirkwood] Militia Veteran Archer | mirkwood_militia_veteran_archer | 40.7 | 85.5 | 99.0 | wm_mirkwood_bow_a02|wm_mirkwood_bow_a03 | False | False | Ranged Troops | mirkwood | 16.0 | special_or_unlinked |
| 65 | B | [Mordor] Black Uruk Heavy Archer | mordor_uruk_heavy_archer | 40.5 | 74.4 | 84.0 | sm_uruk_bow_a | False | False | Ranged Troops | mordor | 31.0 | main_or_minor_line |
| 66 | C | [Rhûn] Sagarûn Arbalest | sagarun_arbalest | 40.0 | 74.8 | 94.0 | crossbow_c | False | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 67 | C | [Gondor] Tolfalas Marksman | gondor_tol_marksman | 39.7 | 71.1 | 82.0 | crossbow_e | False | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 68 | C | [Gondor] Lond-Galen Pavise Crossbowman | gondor_lg_pavise_crossbowman | 39.7 | 71.1 | 82.0 | crossbow_e | False | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 69 | C | [Goblin] Archer | goblin_archer | 39.1 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | goblin | 26.0 | main_or_minor_line |
| 70 | C | [Mordor] Black Uruk Heavy Crossbow | mordor_uruk_heavy_crossbow | 38.9 | 72.0 | 93.0 | crossbow_c | False | False | Ranged Troops | mordor | 31.0 | main_or_minor_line |
| 71 | C | [Dunland] Draig-lûth Firebolt | dunland_dragon_firebolt | 38.4 | 79.3 | 105.0 | crossbow_f | False | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 72 | C | [Dunland] Cigfran-lûth Master Ranger | dunland_raven_master_ranger | 38.3 | 69.1 | 67.0 | woodland_longbow | False | False | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 73 | C | [Erebor] Archer | erebor_noble_archer | 38.0 | 77.7 | 92.0 | sm_dwarf_erebor_bow_a | False | True | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 74 | C | [Harad] Rider of the Golden Veil | harad_horsearcher | 37.2 | 60.4 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 75 | C | [Gondor] Osgiliath Archer | gondor_osg_archer | 37.0 | 75.7 | 88.0 | wm_gondor_bow | False | True | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 76 | C | [Dale] Dalian Marksman | dale_royal_archer | 36.7 | 70.7 | 81.0 | dale_longbow_a | False | True | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 77 | C | [Umbar] Beruthiel's Rangers | umbar_elite_root101 | 36.6 | 83.6 | 108.0 | crossbow_f | False | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 78 | C | [Isengard] Uruk-Hai Crossbowman | urukhai_crossbowman | 36.3 | 79.9 | 105.0 | wm_isengard_crossbow_a01 | False | False | Ranged Troops | isengard | 26.0 | main_or_minor_line |
| 79 | C | [Gondor] Blackroot Vale Archer | gondor_brv_archer | 36.1 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 80 | C | [Gondor] Methir Archer | gondor_met_archer | 36.1 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 81 | C | [Rohan] Wold Veteran Horse Rider | rohan_wold_veteran_horse_archer | 36.0 | 58.3 | 56.0 | composite_steppe_bow | True | True | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 82 | C | [Dale] Dalian Master Crossbowman | dale_royal_crossbowman | 35.9 | 67.0 | 82.0 | crossbow_e | False | True | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 83 | C | [Gondor] Tolfalas Veteran Crossbowman | gondor_tol_vet_crossbowman | 35.9 | 79.2 | 98.0 | crossbow_d | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 84 | C | [Gondor] Lond-Galen Crossbowman | gondor_lg_crossbowman | 35.9 | 79.2 | 98.0 | crossbow_d | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 85 | C | [Isengard] Uruk-Hai Archer | urukhai_archer | 35.9 | 79.1 | 89.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | isengard | 26.0 | main_or_minor_line |
| 86 | C | [Gondor] Anórien Archer | gondor_ano_archer | 35.8 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 87 | C | [Iron Hills] Bowman | iron_hills_reg_bowman | 35.8 | 79.2 | 95.0 | sm_dwarf_erebor_bow_a|sm_dwarf_erebor_bow_b | False | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 88 | C | [Gondor] Lebennin Veteran Archer | gondor_leb_vet_archer | 35.4 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 89 | C | [Dol Guldur] Uruk Fell Archer | dg_uruk_fell_archer | 35.4 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | dolguldur | 26.0 | main_or_minor_line |
| 90 | C | [Rhûn] Black Sun Archer | black_sun_archer | 35.0 | 83.8 | 98.0 | noble_long_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 91 | C | [Erebor] Bowman | erebor_reg_bowman | 34.4 | 79.2 | 95.0 | sm_dwarf_erebor_bow_b | False | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 92 | C | [Dol Guldur] Orc Archer | dg_orc_archer | 34.1 | 77.8 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | dolguldur | 26.0 | main_or_minor_line |
| 93 | C | [Harad] Serpent Eyes | harad_serpent_eye | 33.9 | 61.2 | 56.0 | composite_steppe_bow | False | False | Ranged Troops | aserai | 31.0 | main_or_minor_line |
| 94 | C | [Gundabad] Archer | gundabad_archer | 33.7 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | gundabad | 26.0 | main_or_minor_line |
| 95 | C | [Dol Guldur] Goblin Fellbow | dg_goblin_fellbow | 33.6 | 77.8 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | dolguldur | 26.0 | main_or_minor_line |
| 96 | C | [Misty Mountains] Archer | mistymountainorcs_archer | 33.4 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | mistymountainorcs | 26.0 | main_or_minor_line |
| 97 | C | [Rhûn] Wainrider Wind-Arrow Sharpshooter | wainrider_wind_arrow_sharpshooter | 32.4 | 62.1 | 57.0 | steppe_war_bow | False | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 98 | C | [Rhûn] Dragon-Wrath Archer | dragon_wrath_archer | 32.3 | 62.1 | 57.0 | steppe_war_bow | False | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 99 | C | [Ironpass] Arbalest | ironpass_arbalest | 32.1 | 94.7 | 128.0 | sm_dwarf_iron_crossbow_heavy_a | False | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 100 | C | [Iron Hills] Scout | iron_hills_noble_scout | 31.9 | 94.7 | 128.0 | sm_dwarf_iron_crossbow_heavy_a | False | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 101 | C | [Mordor] Black Uruk Archer | mordor_uruk_archer | 31.5 | 71.8 | 82.0 | mountain_hunting_bow|sm_uruk_bow_a | False | False | Ranged Troops | mordor | 26.0 | main_or_minor_line |
| 102 | C | [Rhûn] Kharaghûl Horse Scout | kharaghul_horse_scout | 31.1 | 57.2 | 55.0 | steppe_heavy_bow | True | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 103 | C | [Dunland] Cigfran-lûth Ranger | dunland_raven_ranger | 30.4 | 69.1 | 67.0 | woodland_longbow | False | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 104 | C | [Dale] Dalian Veteran Crossbowman | dale_veteran_crossbowman | 30.3 | 74.6 | 97.0 | crossbow_d | False | True | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 105 | C | [Gundabad] Scout | gundabad_scout | 28.9 | 57.4 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | gundabad | 21.0 | main_or_minor_line |
| 106 | C | [Dale] Dalian Bowman | dale_longbowman | 28.7 | 71.7 | 81.0 | dale_longbow_a | False | True | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 107 | C | [Mordor] Black Uruk Crossbow | mordor_uruk_crossbow | 28.7 | 67.4 | 84.0 | crossbow_b | False | False | Ranged Troops | mordor | 26.0 | main_or_minor_line |
| 108 | C | [Gondor] Belfalas Veteran Archer | gondor_bel_vet_archer | 28.4 | 58.9 | 55.0 | composite_steppe_bow | False | True | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 109 | C | [Harad] Militia Veteran Archer | harad_militia_veteran_archer | 27.6 | 80.7 | 98.0 | noble_long_bow | False | False | Ranged Troops | aserai | 16.0 | special_or_unlinked |
| 110 | C | [Goblin] Sentry | goblin_sentry | 27.5 | 77.8 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | goblin | 21.0 | main_or_minor_line |
| 111 | C | [Erebor] Ranger | erebor_noble_ranger | 27.3 | 77.7 | 92.0 | sm_dwarf_erebor_bow_a | False | True | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 112 | C | [Harad] Militia Archer | harad_militia_archer | 27.0 | 79.6 | 95.0 | hunting_bow|noble_long_bow | False | False | Ranged Troops | aserai | 11.0 | special_or_unlinked |
| 113 | C | [Harad] Viper | harad_vipereye | 26.9 | 61.2 | 56.0 | composite_steppe_bow | False | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 114 | C | [Rohan] Eastfold Veteran Bowman | rohan_eastfold_veteran_bowman | 26.3 | 84.0 | 99.0 | noble_long_bow | False | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 115 | C | [Isengard] Uruk-Hai Arbalest | urukhai_arbalest | 25.9 | 79.9 | 105.0 | wm_isengard_crossbow_a01 | False | False | Ranged Troops | isengard | 21.0 | main_or_minor_line |
| 116 | C | [Gondor] Pinnath Gelin Veteran Archer | gondor_pg_vet_archer | 25.9 | 60.1 | 57.0 | steppe_war_bow | False | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 117 | C | [Gondor] Gondor Veteran Militia Archer | gondor_militia_veteran_archer | 25.8 | 83.0 | 95.0 | noble_long_bow | False | False | Ranged Troops | gondor | 16.0 | special_or_unlinked |
| 118 | C | [Isengard] Uruk-Hai Tracker | urukhai_tracker | 25.6 | 79.1 | 89.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | isengard | 21.0 | main_or_minor_line |
| 119 | C | [Gondor] Anórien Bowman | gondor_ano_bowman | 25.5 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 120 | C | [Gondor] Blackroot Vale Scout | gondor_brv_scout | 25.5 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 121 | C | [Gondor] Lond-Galen Noble | gondor_lg_noble | 25.5 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 122 | C | [Gondor] Lebennin Archer | gondor_leb_archer | 25.2 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 123 | C | [Rhûn] Loke-Rim Archer | loke_rim_archer | 25.0 | 60.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 124 | C | [Iron Hills] Skirmisher | iron_hills_reg_skirmisher | 24.9 | 77.7 | 92.0 | sm_dwarf_erebor_bow_a | False | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 125 | C | [Dol Guldur] Uruk Bowman | dg_uruk_bowman | 24.9 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | dolguldur | 21.0 | main_or_minor_line |
| 126 | C | [Erebor] Militia Veteran Archer | erebor_militia_veteran_archer | 24.9 | 79.2 | 95.0 | sm_dwarf_erebor_bow_a|sm_dwarf_erebor_bow_b | False | False | Ranged Troops | erebor | 16.0 | special_or_unlinked |
| 127 | C | [Rhûn] Sagarûn Skirmisher | sagarun_skirmisher | 24.9 | 60.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 128 | C | [Rohan] Militia Veteran Archer | rohan_militia_veteran_archer | 24.8 | 80.7 | 98.0 | noble_long_bow | False | False | Ranged Troops | vlandia | 16.0 | special_or_unlinked |
| 129 | C | [Rohan] Wold Horse Archer | rohan_wold_horse_archer | 24.8 | 57.9 | 55.0 | composite_steppe_bow | True | True | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 130 | C | [Gondor] Anórien Archer Militia | gondor_ano_archer_militia | 24.4 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 11.0 | main_or_minor_line |
| 131 | C | [Dale] Veteran Militia Archer | dale_militia_veteran_archer | 24.4 | 71.7 | 81.0 | dale_longbow_a | False | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 132 | C | [Erebor] Skirmisher | erebor_reg_skirmisher | 24.2 | 77.7 | 92.0 | sm_dwarf_erebor_bow_a | False | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 133 | C | [Rhûn] Easterling Veteran Archer | easterling_veteran_archer_new | 24.1 | 60.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 134 | C | [Rhûn] Wainrider Veteran Archer | wainrider_veteran_archer | 24.1 | 60.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 135 | C | [Rhûn] Black Sun Scout | black_sun_scout | 24.0 | 83.8 | 98.0 | noble_long_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 136 | C | [Gondor] Tolfalas Crossbowman | gondor_tol_crossbowman | 24.0 | 76.1 | 93.0 | crossbow_c | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 137 | C | [Dol Guldur] Goblin Archer | dg_goblin_archer | 23.9 | 77.8 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | dolguldur | 21.0 | main_or_minor_line |
| 138 | C | [Dol Guldur] Orc Scout | dg_orc_scout | 23.9 | 77.8 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | dolguldur | 21.0 | main_or_minor_line |
| 139 | C | [Rhûn] Sagarûn Crossbowman | sagarun_crossbowman | 23.8 | 61.7 | 69.0 | crossbow_a | False | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 140 | C | Mordor Militia Veteran Archer | mordor_militia_veteran_archer | 23.6 | 79.6 | 95.0 | noble_long_bow | False | False | Ranged Troops | mordor | 16.0 | special_or_unlinked |
| 141 | C | [Erebor] Militia Archer | erebor_militia_archer | 23.4 | 79.2 | 95.0 | sm_dwarf_erebor_bow_a|sm_dwarf_erebor_bow_b | False | False | Ranged Troops | erebor | 11.0 | special_or_unlinked |
| 142 | C | [Rhûn] Militia Veteran Archer | rhun_militia_veteran_archer | 23.4 | 81.8 | 98.0 | noble_long_bow | False | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 143 | C | [Rohan] Militia Archer | rohan_militia_archer | 23.3 | 79.6 | 95.0 | hunting_bow|noble_long_bow | False | False | Ranged Troops | vlandia | 11.0 | special_or_unlinked |
| 144 | C | [Dunland] Draig-lûth Crossbowman | dunland_dragon_crossbowman | 22.3 | 65.0 | 78.0 | crossbow_e | False | True | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 145 | C | Dol Guldur Militia Veteran Archer | dolguldur_militia_veteran_archer | 22.0 | 76.7 | 89.0 | wm_isengard_bow_a01|wm_isengard_bow_a02 | False | False | Ranged Troops | dolguldur | 16.0 | special_or_unlinked |
| 146 | C | [Misty Mountains] Sentry | mistymountainorcs_sentry | 21.9 | 77.8 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | mistymountainorcs | 21.0 | main_or_minor_line |
| 147 | C | [Gundabad] Sentry | gundabad_sentry | 21.9 | 77.8 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | gundabad | 21.0 | main_or_minor_line |
| 148 | C | [Gondor] Belfalas Archer | gondor_bel_archer | 20.5 | 58.9 | 55.0 | composite_steppe_bow | False | True | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 149 | C | Dol Guldur Militia Archer | dolguldur_militia_archer | 20.3 | 73.0 | 84.0 | sm_uruk_bow_a | False | False | Ranged Troops | dolguldur | 11.0 | special_or_unlinked |
| 150 | D | [Isengard] Militia Veteran Archer | isengard_militia_veteran_archer | 20.0 | 68.1 | 86.0 | crossbow_b | False | False | Ranged Troops | isengard | 16.0 | main_or_minor_line |
| 151 | D | [Dale] Militia Archer | dale_militia_archer | 19.6 | 62.3 | 62.0 | dale_recurve_bow_a | False | False | Ranged Troops | sturgia | 6.0 | main_or_minor_line |
| 152 | D | [Harad] Marksman | harad_marksman | 19.5 | 60.3 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 153 | D | [Dunland] Cigfran-lûth Archer | dunland_raven_archer | 18.7 | 63.7 | 60.0 | lowland_longbow | False | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 154 | D | [Mordor] Black Uruk Skirmisher | mordor_uruk_skirmisher | 18.7 | 64.7 | 77.0 | sm_uruk_bow_starter | False | False | Ranged Troops | mordor | 21.0 | main_or_minor_line |
| 155 | D | [Umbar] Rozadan Bowmen | umbar_elite_root10 | 17.8 | 61.7 | 57.0 | lowland_longbow | False | False | Ranged Troops | umbar | 21.0 | main_or_minor_line |
| 156 | D | [Gondor] Pinnath Gelin Archer | gondor_pg_archer | 17.2 | 58.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 157 | D | [Rhûn] Loke-Rim Bowman | loke_rim_bowman | 16.5 | 60.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 158 | D | [Rohan] Wold Scout | rohan_wold_scout | 16.5 | 57.9 | 55.0 | composite_steppe_bow | True | True | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 159 | D | [Rhûn] Balcoth Archer | balcoth_archer | 16.2 | 60.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 160 | D | [Goblin] Lurker | goblin_lurker | 16.2 | 75.6 | 84.0 | sm_uruk_bow_a | False | False | Ranged Troops | goblin | 16.0 | main_or_minor_line |
| 161 | D | [Isengard] Militia Archer | isengard_militia_archer | 16.1 | 59.1 | 69.0 | crossbow_a | False | False | Ranged Troops | isengard | 11.0 | main_or_minor_line |
| 162 | D | [Rhûn] Easterling Archer | easterling_archer_new | 16.0 | 60.9 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 163 | D | [Mordor] Orc Archer | mordor_orc_archer | 15.9 | 58.5 | 54.0 | composite_bow | False | False | Ranged Troops | mordor | 21.0 | main_or_minor_line |
| 164 | D | [Mordor] Morannon Archer | morannon_archer | 15.4 | 58.5 | 54.0 | composite_bow | False | False | Ranged Troops | mordor | 21.0 | main_or_minor_line |
| 165 | D | [Dunland] Militia Veteran Archer | dunland_militia_veteran_archer | 15.2 | 57.1 | 58.0 | lowland_longbow | False | False | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 166 | D | [Dunland] Hebog-lûth Noble Horse Archer | dunland_falcon_noble_horse_archer | 15.2 | 60.4 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 167 | D | [Dale] Dalian Crossbowman | dale_crossbowman | 15.0 | 71.3 | 91.0 | crossbow_c | False | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 168 | D | [Dunland] Militia Archer | dunland_militia_archer | 14.8 | 57.5 | 57.0 | highland_ranger_bow|lowland_longbow | False | False | Ranged Troops | empire | 11.0 | special_or_unlinked |
| 169 | D | [Goblin] Militia Veteran Archer | goblin_militia_veteran_archer | 14.7 | 48.9 | 40.0 | hunting_bow | False | False | Ranged Troops | goblin | 16.0 | special_or_unlinked |
| 170 | D | [Dunland] Hebog-lûth Horse Archer | dunland_falcon_wildrider | 14.6 | 60.4 | 54.0 | composite_steppe_bow | True | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 171 | D | [Isengard] Uruk-Hai Skirmisher | urukhai_skirmisher | 14.4 | 79.9 | 105.0 | wm_isengard_crossbow_a01 | False | False | Ranged Troops | isengard | 16.0 | main_or_minor_line |
| 172 | D | [Rohan] Wold Recruit | rohan_wold_recruit | 14.4 | 57.9 | 55.0 | composite_steppe_bow | True | True | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 173 | D | [Gondor] Anorien Skirmisher | gondor_ano_skirmisher | 14.1 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 174 | D | [Gondor] Blackroot Vale Bowman | gondor_brv_bowman | 14.1 | 79.7 | 88.0 | wm_gondor_bow | False | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 175 | D | [Isengard] Uruk-Hai Scout | urukhai_scout | 13.8 | 77.6 | 86.0 | wm_isengard_bow_a01 | False | False | Ranged Troops | isengard | 16.0 | main_or_minor_line |
| 176 | D | [Goblin] Militia Archer | goblin_militia_archer | 13.7 | 48.9 | 40.0 | hunting_bow | False | False | Ranged Troops | goblin | 11.0 | special_or_unlinked |
| 177 | D | [Gondor] Gondor Militia Archer | gondor_militia_archer | 13.0 | 52.3 | 40.0 | hunting_bow | False | False | Ranged Troops | gondor | 11.0 | special_or_unlinked |
| 178 | D | [Dunland] Hebog-lûth Scout | dunland_falcon_archer | 12.6 | 59.7 | 54.0 | steppe_heavy_bow | True | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 179 | D | [Dol Guldur] Uruk Skirmisher | dg_uruk_skirmisher | 12.3 | 80.4 | 90.0 | wm_isengard_bow_a02 | False | False | Ranged Troops | dolguldur | 16.0 | main_or_minor_line |
| 180 | D | [Gondor] Tolfalas Arbalest | gondor_tol_arbalest | 12.2 | 72.2 | 86.0 | crossbow_b | False | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 181 | D | [Misty Mountains] Militia Veteran Archer | mistymountainorcs_militia_veteran_archer | 11.1 | 48.9 | 40.0 | hunting_bow | False | False | Ranged Troops | mistymountainorcs | 16.0 | special_or_unlinked |
| 182 | D | [Gundabad] Militia Veteran Archer | gundabad_militia_veteran_archer | 11.0 | 48.9 | 40.0 | hunting_bow | False | False | Ranged Troops | gundabad | 16.0 | special_or_unlinked |
| 183 | D | [Dale] Dalian Yeoman | dale_bowman | 11.0 | 62.3 | 62.0 | dale_recurve_bow_a | False | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 184 | D | [Rhûn] Militia Archer | rhun_militia_archer | 11.0 | 48.9 | 40.0 | hunting_bow | False | False | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 185 | D | Mordor Militia Archer | mordor_militia_archer | 10.9 | 48.9 | 40.0 | hunting_bow | False | False | Ranged Troops | mordor | 11.0 | special_or_unlinked |
| 186 | D | [Harad] Desert Archer | harad_archer | 10.8 | 60.3 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | aserai | 16.0 | main_or_minor_line |
| 187 | D | [Misty Mountains] Lurker | mistymountainorcs_lurker | 10.6 | 75.6 | 84.0 | sm_uruk_bow_a | False | False | Ranged Troops | mistymountainorcs | 16.0 | main_or_minor_line |
| 188 | D | [Gundabad] Lurker | gundabad_lurker | 10.6 | 75.6 | 84.0 | sm_uruk_bow_a | False | False | Ranged Troops | gundabad | 16.0 | main_or_minor_line |
| 189 | D | [Misty Mountains] Militia Archer | mistymountainorcs_militia_archer | 10.1 | 48.9 | 40.0 | hunting_bow | False | False | Ranged Troops | mistymountainorcs | 11.0 | special_or_unlinked |
| 190 | D | [Rohan] East-Fold Bowman | rohan_eastfold_bowman | 10.1 | 68.1 | 67.0 | woodland_longbow | False | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 191 | D | [Gundabad] Militia Archer | gundabad_militia_archer | 10.1 | 48.9 | 40.0 | hunting_bow | False | False | Ranged Troops | gundabad | 11.0 | special_or_unlinked |
| 192 | D | [Rivendell] Imladris Recruit | imladris_recruit | 10.0 | 97.5 | 120.0 | highelf_longbowc|highelf_longbowd | False | False | Ranged Troops | rivendell | 21.0 | main_or_minor_line |
| 193 | D | [Gondor] Belfalas Bowman | gondor_bel_bowman | 9.7 | 63.0 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 194 | D | [Goblin] Hunter | goblin_hunter | 9.2 | 75.9 | 83.0 | sm_uruk_bow_a | False | False | Ranged Troops | goblin | 11.0 | main_or_minor_line |
| 195 | D | [Umbar] Adûnaim Bowmen | umbar_elite_root1 | 8.4 | 60.6 | 51.0 | composite_bow | False | False | Ranged Troops | umbar | 16.0 | main_or_minor_line |
| 196 | D | [Dunland] Cigfran-lûth Skirmisher | dunland_raven_warrior | 8.3 | 59.6 | 58.0 | lowland_longbow | False | False | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 197 | D | [Dunland] Tribal Skirmisher | dunland_skirmisher | 8.2 | 59.6 | 58.0 | lowland_longbow | False | False | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 198 | D | [Rhûn] Easterling Skirmisher | easterling_skirmisher_new | 6.8 | 60.3 | 55.0 | steppe_heavy_bow | False | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 199 | D | [Gundabad] Hunter | gundabad_hunter | 6.0 | 75.9 | 83.0 | sm_uruk_bow_a | False | False | Ranged Troops | gundabad | 11.0 | main_or_minor_line |
| 200 | D | [Misty Mountains] Hunter | mistymountainorcs_hunter | 5.8 | 75.9 | 83.0 | sm_uruk_bow_a | False | False | Ranged Troops | mistymountainorcs | 11.0 | main_or_minor_line |
| 201 | D | [Dol Guldur] Goblin Hunter | dg_goblin_hunter | 5.1 | 75.9 | 83.0 | sm_uruk_bow_a | False | False | Ranged Troops | dolguldur | 11.0 | main_or_minor_line |
| 202 | D | [Mordor] Morannon Scout | morannon_scout | 5.0 | 48.5 | 41.0 | hunting_bow | False | False | Ranged Troops | mordor | 16.0 | main_or_minor_line |
| 203 | D | [Mordor] Orc Scout | mordor_orc_scout | 4.8 | 48.5 | 41.0 | hunting_bow | False | False | Ranged Troops | mordor | 16.0 | main_or_minor_line |
| 204 | D | [Harad] Skirmisher | harad_skirmisher | 4.4 | 60.6 | 54.0 | composite_bow | False | False | Ranged Troops | aserai | 11.0 | main_or_minor_line |
| 205 | D | [Rohan] Eastfold Yeoman Archer | rohan_eastfold_skirmisher | 3.7 | 65.4 | 62.0 | woodland_yew_bow | False | False | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 206 | D | [Gondor] Belfalas Hunter | gondor_bel_hunter | 2.9 | 63.0 | 55.0 | composite_steppe_bow | False | False | Ranged Troops | gondor | 11.0 | main_or_minor_line |
| 207 | D | [Rhûn] Easterling Bowman | easterling_bowman | 2.9 | 60.6 | 54.0 | composite_bow | False | False | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 208 | D | [Dunland] Tribal Hunter | dunland_hunter | 1.5 | 55.6 | 47.0 | highland_ranger_bow | False | False | Ranged Troops | empire | 11.0 | main_or_minor_line |
| 209 | D | [Dunland] Cigfran-lûth Hunter | dunland_raven_noble_son | 1.5 | 54.3 | 48.0 | highland_ranger_bow | False | False | Ranged Troops | empire | 11.0 | main_or_minor_line |
| 210 | D | [Rohan] Eastfold Freeman | rohan_eastfold_recruit | 1.2 | 54.3 | 52.0 | glen_ranger_bow | False | False | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 211 | D | [Mordor] Morannon Skirmisher | morannon_skirmisher | 0.5 | 48.5 | 41.0 | hunting_bow | False | False | Ranged Troops | mordor | 11.0 | main_or_minor_line |
| 212 | D | [Mordor] Orc Hunter | mordor_orc_hunter | 0.4 | 48.5 | 41.0 | hunting_bow | False | False | Ranged Troops | mordor | 11.0 | main_or_minor_line |


## Ranked — Defensive (524 troops)

| rank | tier | troop_name | troop_id | defensive_role_score | defense_score_base | armor_total | effective_armor | has_shield | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rivendell] Nõldorin Lancer | noldorin_lancer | 100.0 | 92.1 | 338.6 | 77.3 | True | True | Defensive Troops | rivendell | 46.0 | main_or_minor_line |
| 2 | S | [Rivendell] Noble | rivendell_noble | 92.7 | 81.6 | 287.7 | 61.3 | True | True | Defensive Troops | rivendell | 36.0 | main_or_minor_line |
| 3 | S | [Rivendell] High Captain | rivendell_high_captain | 91.4 | 86.3 | 337.3 | 78.7 | True | True | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 4 | S | [Rivendell] Royal Guard | rivendell_royal_guard | 91.1 | 87.7 | 319.5 | 70.4 | True | True | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 5 | A | [Rivendell] Royal Knight | rivendell_royal_knight | 87.5 | 82.0 | 338.7 | 72.4 | True | True | Defensive Troops | rivendell | 46.0 | main_or_minor_line |
| 6 | A | [Mirkwood] Mirkwood Béleglas | mirkwood_beleglas | 83.2 | 78.0 | 246.0 | 66.8 | True | True | Defensive Troops | mirkwood | 46.0 | main_or_minor_line |
| 7 | A | [Mirkwood] Mirkwood Róchenlas | mirkwood_rochenlas | 83.2 | 78.0 | 246.0 | 66.8 | True | True | Defensive Troops | mirkwood | 41.0 | main_or_minor_line |
| 8 | A | [AMordor] Armored Troll | cave_troll | 83.1 | 73.0 | 475.0 | 104.5 | True | False | Defensive Troops | mordor | 51.0 | special_or_unlinked |
| 9 | A | [Dol Guldur] Khamûl's Shadow-Knight | dg_khamul_shadow_knight | 82.9 | 76.4 | 245.7 | 65.9 | True | True | Defensive Troops | dolguldur | 46.0 | main_or_minor_line |
| 10 | A | [Rivendell] Imladris Outrider | imladris_outrider | 81.8 | 75.6 | 259.0 | 62.5 | True | True | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 11 | A | [Rivendell] Rochannon Elenath | rivendell_glorfindel_guard | 80.5 | 74.6 | 205.0 | 51.2 | True | True | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 12 | A | [Rhûn] Loke-Rim Gilded Kataphract | loke_rim_gilded_cataphract | 80.4 | 73.0 | 234.3 | 60.8 | True | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 13 | A | [Rhûn] Dragon-Wrath Obsidian Knight | dragon_wrath_obsidian_knight | 79.9 | 73.0 | 234.3 | 60.8 | True | True | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 14 | A | [Dale] Dalian Veteran Northman Scout | dale_veteran_northman_scout | 79.6 | 73.4 | 197.0 | 57.8 | True | True | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 15 | A | [Dale] Dalian King's Guard | dale_kings_guard | 78.7 | 72.2 | 193.0 | 58.5 | True | True | Defensive Troops | sturgia | 31.0 | main_or_minor_line |
| 16 | A | [Rohan] Riders of Rohan | rohan_edoras_golden_hall_supreme_rider | 78.2 | 67.9 | 201.4 | 55.9 | True | True | Skirmishers | vlandia | 41.0 | main_or_minor_line |
| 17 | A | [Rhûn] Darkhûn Cultist Knight | darkhun_cultist_knight | 77.5 | 70.7 | 214.0 | 57.4 | True | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 18 | A | [Rohan] West Emnet Heavy Shock Cavalry | rohan_westemnet_kings_own_rider | 77.1 | 68.4 | 173.0 | 55.1 | True | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 19 | A | [Rhûn] Wainrider Warlord Chariot | wainrider_warlord_chariot | 76.8 | 69.7 | 218.0 | 58.2 | True | True | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 20 | A | [ARhûn] Wainrider Swift-Chariot | wainrider_swift_chariot | 75.5 | 68.1 | 209.0 | 55.9 | True | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 21 | A | [Dol Guldur] Khamûl's Veiled Knight | dg_khamul_veiled_knight | 75.1 | 66.5 | 208.3 | 56.2 | True | True | Defensive Troops | dolguldur | 41.0 | main_or_minor_line |
| 22 | A | [Dale] Dalian Northman Scout | dale_knight | 75.1 | 67.5 | 164.0 | 49.0 | True | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 23 | A | [Dale] Dalian Heavy Cavalry | dale_kinsman_of_eorl | 74.9 | 67.3 | 160.0 | 48.7 | True | True | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 24 | A | [Dale] Dalian Cavalry | dale_royal_cavalier | 74.7 | 67.0 | 156.0 | 48.2 | True | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 25 | A | [Rhûn] Dragon-Wrath Lancer | dragon_wrath_lancer | 74.1 | 65.6 | 206.5 | 55.0 | True | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 26 | A | [Dunland] Caru-lûth Noble Lancer | dunland_stag_noble_lancer | 73.9 | 64.3 | 173.0 | 54.0 | True | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 27 | A | [Dale] Dalian Merchant Guard | dale_outrider | 73.7 | 62.1 | 138.0 | 41.8 | True | True | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 28 | A | [Rivendell] Imladris Nobleman | imladris_nobleman | 73.4 | 65.9 | 337.6 | 76.2 | True | False | Defensive Troops | rivendell | 36.0 | main_or_minor_line |
| 29 | A | [Rhûn] Darkhûn Knight | darkhun_knight | 73.2 | 65.1 | 189.0 | 49.0 | True | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 30 | A | [Rhûn] Loke-Rim Cavalry | loke_rim_cavalry | 73.0 | 64.1 | 204.7 | 54.5 | True | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 31 | A | [Rohan] King's Royal Guard | rohan_edoras_golden_hall_kings_own_rider | 72.7 | 62.5 | 193.8 | 57.3 | True | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 32 | A | [Dunland] Avanc-lûth Noble Cavalry | dunland_lizard_noble_cavalry | 72.5 | 63.9 | 173.0 | 54.0 | True | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 33 | A | [Rohan] Éothéod Horse Archer | rohan_wold_kings_own_horse_archer | 72.3 | 63.9 | 165.0 | 50.0 | True | True | Ranged Troops | vlandia | 36.0 | main_or_minor_line |
| 34 | A | [Rohan] East Emnet King's Lancer | rohan_eastemnet_kings_own_lancer | 72.3 | 63.9 | 165.0 | 50.0 | True | True | Defensive Troops | vlandia | 36.0 | main_or_minor_line |
| 35 | A | [Rohan] King's Knight | rohan_edoras_golden_hall_eorlingas_rider | 72.2 | 60.5 | 175.4 | 53.3 | True | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 36 | A | [Dunland] Caru-lûth Rider | dunland_stag_rider | 71.7 | 61.4 | 147.0 | 49.7 | True | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 37 | A | [Rivendell] Imladris Swordguard | imladris_swordguard | 70.5 | 59.8 | 304.2 | 67.2 | True | False | Defensive Troops | rivendell | 31.0 | main_or_minor_line |
| 38 | A | [Rhûn] Far-Rhun Iron Kataphract | far_rhun_iron_cataphract | 70.5 | 61.5 | 187.0 | 47.3 | True | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 39 | A | [Rhûn] Kharaghûl Ashkur Nokor | kharaghul_ashkur_nokor | 70.4 | 61.4 | 185.0 | 47.1 | True | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 40 | A | [Rivendell] Imladris Warden | imladris_warden | 70.2 | 67.0 | 354.5 | 77.9 | True | False | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 41 | B | [Rivendell] Battlemaster of the First Age | battlemaster_of_the_first_age | 69.9 | 69.3 | 350.6 | 81.3 | True | False | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 42 | B | [Rohan] West Emnet Shock Cavalry | rohan_westemnet_royal_rider | 69.9 | 59.0 | 169.0 | 52.1 | True | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 43 | B | [Rhûn] Wainrider Khan's Chosen | wainrider_khans_chosen | 69.6 | 60.3 | 218.0 | 58.2 | True | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 44 | B | [Rhûn] Far-Rhun Kataphract | far_rhun_cataphract | 69.4 | 60.2 | 185.0 | 47.1 | True | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 45 | B | [Rhûn] Kharaghûl Nokor | kharaghul_nokor | 69.1 | 59.8 | 176.0 | 44.7 | True | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 46 | B | [Rhûn] Kharaghûl Horse Master | kharaghul_horse_master | 68.8 | 59.3 | 174.0 | 44.0 | True | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 47 | B | [Rohan] East Emnet Royal Lancer | rohan_eastemnet_royal_lancer | 68.6 | 59.0 | 169.0 | 52.1 | True | True | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 48 | B | [Dunland] Avanc-lûth Outrider | dunland_lizard_outrider | 67.6 | 57.5 | 152.0 | 51.8 | True | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 49 | B | [Rhûn] Loke-Rim Kataphract | loke_rim_cataphract | 67.2 | 57.0 | 150.3 | 37.0 | True | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 50 | B | [Rhûn] Dragon-Wrath Ash Knight | dragon_wrath_ash_knight | 67.2 | 57.0 | 150.3 | 37.0 | True | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 51 | B | [Rivendell] Rider of Himring | rider_of_himring | 67.1 | 70.1 | 342.3 | 76.4 | False | True | Ranged Troops | rivendell | 46.0 | main_or_minor_line |
| 52 | B | [Erebor] Gate Warden | erebor_noble_gate_warden | 66.9 | 59.5 | 271.8 | 78.4 | True | False | Defensive Troops | erebor | 41.0 | main_or_minor_line |
| 53 | B | [Rhûn] Wainrider Cavalry | wainrider_cavalry | 66.0 | 55.7 | 194.0 | 49.5 | True | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 54 | B | [Gondor] Swan Knight | gondor_da_swan_knight | 66.0 | 55.6 | 157.0 | 48.9 | True | True | Defensive Troops | gondor | 46.0 | main_or_minor_line |
| 55 | B | [Rohan] King's Lancer | rohan_edoras_golden_hall_elite_rider | 65.7 | 52.7 | 139.6 | 40.9 | True | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 56 | B | [Gondor] Dol Amroth Veteran Knight | gondor_da_vet_knight | 65.4 | 54.9 | 157.0 | 48.9 | True | True | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 57 | B | [Gondor] Dol Amroth Cavalry | gondor_da_cavalry | 65.0 | 54.4 | 157.0 | 48.9 | True | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 58 | B | [Gondor] Dol Amroth Knight | gondor_da_knight | 65.0 | 54.4 | 157.0 | 48.9 | True | True | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 59 | B | [Harad] Serpent Guard | harad_serpentguard | 64.8 | 52.4 | 183.0 | 46.8 | True | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 60 | B | [Rhûn] Darkhûn Veteran Cavalry | darkhun_veteran_cavalry | 64.7 | 54.0 | 156.0 | 37.8 | True | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 61 | B | [Erebor] Royal Warden | erebor_noble_royal_warden | 63.8 | 60.2 | 273.2 | 78.3 | True | False | Defensive Troops | erebor | 46.0 | main_or_minor_line |
| 62 | B | [Umbar] Naru n'Aru Royal Knights | umbar_elite_root0001 | 63.7 | 42.6 | 156.0 | 37.1 | True | True | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 63 | B | [Rhûn] Easterling Veteran Cavalry | easterling_veteran_cavalry | 63.7 | 52.7 | 146.0 | 36.0 | True | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 64 | B | [Rohan] King's Horseman | rohan_edoras_golden_hall_veteran_rider | 63.7 | 51.7 | 130.8 | 39.4 | True | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 65 | B | [Gondor] Pinnath Gelin Veteran Horseman | gondor_pg_vet_cavalry | 63.5 | 50.8 | 152.0 | 46.7 | True | True | Skirmishers | gondor | 31.0 | main_or_minor_line |
| 66 | B | [Gondor] Dol Amroth Squire | gondor_da_squire | 63.2 | 52.0 | 144.0 | 46.3 | True | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 67 | B | [Dol Guldur] Khamûl's Shadow-Guard | dg_khamul_shadow_guard | 63.1 | 60.7 | 253.7 | 67.5 | True | False | Defensive Troops | dolguldur | 46.0 | main_or_minor_line |
| 68 | B | [Rohan] East Emnet Eorlingas Lancer | rohan_eastemnet_eorlingas_lancer | 63.0 | 51.8 | 129.0 | 40.3 | True | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 69 | B | [Rohan] Wold Elite Horse Rider | rohan_wold_elite_horse_archer | 63.0 | 51.8 | 129.0 | 40.3 | True | True | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 70 | B | [Harad] Initiate of the Sand Blades | harad_sandblade | 63.0 | 50.1 | 169.0 | 43.3 | True | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 71 | B | [Harad] Youngblood of the Serpent | harad_noble | 63.0 | 50.1 | 169.0 | 43.3 | True | True | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 72 | B | [Harad] Warrior of the Gilded Fang | harad_gildedfang | 63.0 | 50.1 | 169.0 | 43.3 | True | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 73 | B | [Harad] Fang of the King | harad_fangking | 63.0 | 50.1 | 169.0 | 43.3 | True | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 74 | B | [Rhûn] Darkhûn Ironbound | darkhun_ironbound | 62.8 | 59.9 | 229.0 | 62.0 | True | False | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 75 | B | [Rhûn] Dragon-Wrath Obsidian Shieldmaster | dragon_wrath_obsidian_shieldmaster | 62.6 | 57.4 | 232.0 | 60.5 | True | False | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 76 | B | [Rivendell] Militia Veteran Spearman | rivendell_militia_veteran_spearman | 62.4 | 48.4 | 242.0 | 51.7 | True | False | Defensive Troops | rivendell | 16.0 | special_or_unlinked |
| 77 | B | [Erebor] Royal Legionary | erebor_oathsworn_royal_legionary | 62.3 | 56.6 | 253.5 | 73.0 | True | False | Defensive Troops | erebor | 46.0 | main_or_minor_line |
| 78 | B | [Gundabad] Azog's Defiler | gundabad_dread_rider_of_the_tower | 62.2 | 48.1 | 235.8 | 60.3 | True | True | Defensive Troops | gundabad | 41.0 | main_or_minor_line |
| 79 | B | [Rivendell] Imladris Guardsman | imladris_guardsman | 62.1 | 58.3 | 275.2 | 64.9 | True | False | Defensive Troops | rivendell | 36.0 | main_or_minor_line |
| 80 | B | [Rohan] Wold Eorlingas Horse Archer | rohan_wold_eorlingas_horse_archer | 62.0 | 50.5 | 130.0 | 39.5 | True | True | Ranged Troops | vlandia | 31.0 | main_or_minor_line |
| 81 | B | [Ironpass] Mountain Guard | ironpass_mountain_guard | 62.0 | 44.8 | 211.0 | 54.7 | True | False | Defensive Troops | erebor | 36.0 | main_or_minor_line |
| 82 | B | [Rohan] West Emnet Medium Cavalry | rohan_westemnet_eorlingas_rider | 61.9 | 48.7 | 122.0 | 35.8 | True | True | Skirmishers | vlandia | 26.0 | main_or_minor_line |
| 83 | B | [Rohan] Wold Veteran Horse Rider | rohan_wold_veteran_horse_archer | 61.7 | 50.1 | 106.0 | 37.0 | True | True | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 84 | B | [Rohan] West Emnet Light Cavalry | rohan_westemnet_elite_rider | 61.7 | 50.1 | 106.0 | 37.0 | True | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 85 | B | [Rohan] East Emnet Elite Lancer | rohan_eastemnet_elite_lancer | 61.7 | 50.1 | 106.0 | 37.0 | True | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 86 | B | [Gondor] Anórien Knight | gondor_ano_mt_knight | 61.7 | 50.0 | 143.0 | 42.0 | True | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 87 | B | [Ironpass] Veteran Axeman | ironpass_veteran_axeman | 61.2 | 44.8 | 211.6 | 54.7 | True | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 88 | B | [Dol Guldur] Fell Ravager | dg_fell_warg_rider | 61.2 | 49.4 | 230.0 | 62.2 | True | True | Defensive Troops | dolguldur | 36.0 | main_or_minor_line |
| 89 | B | [Erebor] Shield-Guard | erebor_noble_shield_guard | 61.2 | 55.1 | 252.5 | 70.7 | True | False | Defensive Troops | erebor | 36.0 | main_or_minor_line |
| 90 | B | [Erebor] Legionary | erebor_oathsworn_legionary | 61.1 | 55.8 | 257.5 | 72.3 | True | False | Defensive Troops | erebor | 41.0 | main_or_minor_line |
| 91 | B | [Rivendell] Imladris Horse Archer | imladris_horse_archer | 61.1 | 61.8 | 280.4 | 63.5 | False | True | Ranged Troops | rivendell | 41.0 | main_or_minor_line |
| 92 | B | [Gondor] Anfalas Veteran Cavalry | gondor_anf_vet_cavalry | 60.9 | 49.0 | 135.0 | 41.5 | True | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 93 | B | [Rhûn] Loke-Rim Gilded Shieldguard | loke_rim_gilded_shieldguard | 60.8 | 56.2 | 234.3 | 60.8 | True | False | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 94 | B | [Gondor] Anórien Heavy Cavalry | gondor_ano_mt_heavy_cavalry | 60.5 | 48.6 | 138.0 | 39.8 | True | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 95 | B | [Rhûn] Far-Rhun Cavalry | far_rhun_cavalry | 60.4 | 46.7 | 150.0 | 36.6 | True | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 96 | B | [Rhûn] Far-Rhun Horse Master | far_rhun_horse_master | 60.4 | 46.7 | 150.0 | 36.6 | True | True | Skirmishers | khuzait | 21.0 | special_or_unlinked |
| 97 | B | [Dunland] Avanc-lûth Horseman | dunland_lizard_horseman | 60.2 | 47.9 | 129.0 | 43.9 | True | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 98 | B | [Dunland] Caru-lûth Lancer | dunland_stag_lancer | 60.2 | 46.4 | 129.0 | 43.9 | True | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 99 | B | [Ironpass] Axeman | ironpass_axeman | 60.0 | 43.5 | 205.6 | 52.9 | True | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 100 | B | [Rhûn] Darkhûn Cavalry | darkhun_cavalry | 59.9 | 47.8 | 120.0 | 28.5 | True | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 101 | B | [Iron Hills] Gate Warden | iron_hills_noble_gate_warden | 59.8 | 56.0 | 254.0 | 67.0 | True | False | Defensive Troops | erebor | 41.0 | main_or_minor_line |
| 102 | B | [Gondor] Anfalas Cavalry | gondor_anf_cavalry | 59.8 | 47.6 | 130.0 | 39.4 | True | True | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 103 | B | [Iron Hills] Shield-Guard | iron_hills_noble_shield_guard | 59.6 | 55.7 | 263.0 | 70.2 | True | False | Defensive Troops | erebor | 36.0 | main_or_minor_line |
| 104 | B | [Rhûn] Easterling Cavalry | easterling_cavalry_new | 59.5 | 45.5 | 139.0 | 34.8 | True | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 105 | B | [Rohan] King's Rider | rohan_edoras_golden_hall_rider | 59.4 | 46.5 | 115.2 | 31.8 | True | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 106 | B | [Dol Guldur] Warg Fang | dg_warg_red_fang | 59.1 | 46.7 | 217.0 | 58.1 | True | True | Defensive Troops | dolguldur | 31.0 | main_or_minor_line |
| 107 | B | [Erebor] Oathsworn | erebor_oathsworn | 58.8 | 54.5 | 256.2 | 70.9 | True | False | Defensive Troops | erebor | 36.0 | main_or_minor_line |
| 108 | B | [Dale] Dalian Royal Swordsman | dale_running_river_warden | 58.8 | 47.3 | 198.0 | 59.0 | True | False | Defensive Troops | sturgia | 31.0 | main_or_minor_line |
| 109 | B | [Gondor] Pinnath Gelin Light Horseman | gondor_pg_cavalry | 58.7 | 44.5 | 127.0 | 40.0 | True | True | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 110 | B | [Rhûn] Kharaghûl Raider | kharaghul_raider | 58.6 | 44.3 | 131.0 | 33.0 | True | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 111 | B | [Dale] Dalian Royal Crossbowman | dale_master_crossbowman | 58.5 | 55.3 | 203.0 | 59.5 | True | False | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 112 | B | [Iron Hills] Guard | iron_hills_noble_guard | 58.3 | 54.0 | 253.0 | 67.7 | True | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 113 | B | [Rohan] Wold Horse Archer | rohan_wold_horse_archer | 58.2 | 45.6 | 100.0 | 31.5 | True | True | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 114 | B | [Rohan] East Emnet Veteran Lancer | rohan_eastemnet_veteran_lancer | 58.2 | 45.6 | 100.0 | 31.5 | True | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 115 | B | [Rohan] West Emnet Horseman | rohan_westemnet_veteran_rider | 58.2 | 45.6 | 100.0 | 31.5 | True | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 116 | B | [Dale] Dalian Barding | dale_black_arrow_marksman | 58.0 | 54.6 | 193.0 | 58.5 | True | False | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 117 | B | [Dol Guldur] Khamûl's Veiled Guard | dg_khamul_veiled_guard | 57.7 | 54.2 | 217.0 | 58.0 | True | False | Defensive Troops | dolguldur | 41.0 | main_or_minor_line |
| 118 | B | [Dale] Dalian Swordsman | dale_royal_guard | 57.6 | 47.0 | 159.5 | 47.2 | True | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 119 | B | [Dale] Dalian Master Crossbowman | dale_royal_crossbowman | 57.6 | 54.1 | 197.0 | 57.8 | True | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 120 | B | [Gondor] Anórien Cavalry | gondor_ano_mt_cavalry | 57.6 | 44.7 | 124.0 | 36.6 | True | True | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 121 | B | [Rhûn] Dragon-Wrath Infantry | dragon_wrath_infantry | 57.5 | 52.2 | 206.5 | 55.0 | True | False | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 122 | B | [Harad] Camel Rider | harad_camelrider | 57.4 | 42.8 | 154.0 | 45.4 | True | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 123 | B | [Dale] Dalian Mariner | dale_dalian_mariner | 57.0 | 51.6 | 197.0 | 57.8 | True | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 124 | B | [Gundabad] Pale Uruk Fang Rider | gundabad_tracker | 56.8 | 37.8 | 185.0 | 45.0 | True | True | Defensive Troops | gundabad | 36.0 | main_or_minor_line |
| 125 | B | [Erebor] Guard | erebor_noble_guard | 56.8 | 49.5 | 231.0 | 63.5 | True | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 126 | B | [Rhûn] Sagarûn Marine | sagarun_marine | 56.6 | 50.5 | 217.5 | 58.4 | True | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 127 | B | [Iron Hills] Royal Warden | iron_hills_noble_royal_warden | 56.6 | 51.7 | 242.0 | 60.7 | True | False | Defensive Troops | erebor | 46.0 | main_or_minor_line |
| 128 | B | [Rhûn] Sagarûn Storm Forged Marine | sagarun_storm_forged_marine | 56.5 | 50.7 | 219.5 | 58.8 | True | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 129 | B | [Rhûn] Darkhûn Guard | darkhun_guard | 56.4 | 51.5 | 212.0 | 56.4 | True | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 130 | B | [Rhûn] Darkhûn Horseman | darkhun_horseman | 56.1 | 42.8 | 85.0 | 21.1 | True | True | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 131 | B | [Ironpass] Infantry | ironpass_infantry | 55.9 | 40.7 | 188.8 | 48.5 | True | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 132 | B | [Dol Guldur] Warg Ravager | dg_warg_skirmisher | 55.9 | 42.5 | 210.0 | 52.0 | True | True | Defensive Troops | dolguldur | 26.0 | main_or_minor_line |
| 133 | B | [Harad] Camel Lancer | harad_camel_lancer | 55.8 | 40.7 | 149.0 | 42.3 | True | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 134 | B | [Isengard] Uruk-Hai Pavise Guard | urukhai_pavise | 55.4 | 50.2 | 226.0 | 63.5 | True | False | Defensive Troops | isengard | 31.0 | main_or_minor_line |
| 135 | B | [Ironpass] Warrior | ironpass_warrior | 54.9 | 33.9 | 141.2 | 38.3 | True | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 136 | B | [Isengard] Orthanc Bodyguard | orthanc_bodyguard | 54.9 | 50.5 | 237.0 | 63.9 | True | False | Defensive Troops | isengard | 41.0 | main_or_minor_line |
| 137 | B | [Isengard] Orthanc Warden | orthanc_warden | 54.7 | 50.3 | 231.4 | 63.5 | True | False | Defensive Troops | isengard | 36.0 | main_or_minor_line |
| 138 | B | [Rivendell] Aegedhrim Elenath | rivendell_warden_gondolin | 54.5 | 49.0 | 205.0 | 51.2 | True | False | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 139 | B | [Rhûn] Loke-Rim Infantry | loke_rim_infantry | 54.4 | 48.2 | 206.5 | 55.0 | True | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 140 | B | [Rohan] East Emnet Lance Rider | rohan_eastemnet_lance_rider | 54.3 | 40.4 | 81.0 | 23.0 | True | True | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 141 | B | [Rohan] Wold Scout | rohan_wold_scout | 54.3 | 40.4 | 81.0 | 23.0 | True | True | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 142 | B | [Rohan] West Emnet Rider | rohan_westemnet_rider | 54.3 | 40.4 | 81.0 | 23.0 | True | True | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 143 | B | [Mirkwood] Guardians of Felegoth | mirkwood_guardians | 54.2 | 48.6 | 205.0 | 61.1 | True | False | Defensive Troops | mirkwood | 46.0 | main_or_minor_line |
| 144 | B | [Mirkwood] Palace Guard | mirkwood_palaceguard | 54.2 | 48.6 | 205.0 | 61.1 | True | False | Defensive Troops | mirkwood | 51.0 | main_or_minor_line |
| 145 | B | [Mirkwood] Greenwood Wardens | mirkwood_wardens | 54.2 | 48.6 | 205.0 | 61.1 | True | False | Defensive Troops | mirkwood | 41.0 | main_or_minor_line |
| 146 | B | [Dol Guldur] Warg Rider | dg_warg_raider | 54.1 | 40.2 | 200.0 | 48.5 | True | True | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 147 | B | [Dale] Dalian Guardsman | dale_guardsman | 53.9 | 39.6 | 120.5 | 36.3 | True | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 148 | B | [Rivendell] Imladris Infantry | imladris_infantry | 53.9 | 48.5 | 204.2 | 50.3 | True | False | Defensive Troops | rivendell | 26.0 | main_or_minor_line |
| 149 | B | [Rohan] Meduseld Master Spearman | rohan_edoras_meduseld_master_spearman | 53.8 | 46.6 | 161.8 | 52.1 | True | False | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 150 | B | [Gundabad] Bolg's Ironfang | gundabad_bolgs_ironfang | 53.8 | 50.1 | 245.0 | 63.2 | True | False | Defensive Troops | gundabad | 36.0 | main_or_minor_line |
| 151 | B | [Rivendell] Megil-Aran Elenath | rivendell_gondolin_battlemaster | 53.7 | 44.2 | 205.0 | 51.2 | True | False | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 152 | B | [Gondor] Serelond Coastwarden | gondor_ser_coastwarden | 53.3 | 47.5 | 197.0 | 57.8 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 153 | B | [Isengard] Orc Warg-Rider Lieutenant | orc_warg_lieutenant | 53.1 | 38.9 | 147.0 | 46.7 | True | True | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 154 | B | [Isengard] Orc Warg-Rider Enforcer | orc_warg_enforcer | 53.1 | 38.9 | 146.0 | 46.5 | True | True | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 155 | B | [Rhûn] Darkhûn Veteran Infantry | darkhun_veteran_infantry | 53.0 | 47.1 | 205.0 | 53.3 | True | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 156 | B | [Dale] Dalian Veteran Crossbowman | dale_veteran_crossbowman | 52.7 | 47.7 | 162.0 | 48.3 | True | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 157 | B | [Gundabad] Pale Uruk Wolf Rider | gundabad_warg_tamer | 52.7 | 32.0 | 146.0 | 36.4 | True | True | Defensive Troops | gundabad | 31.0 | main_or_minor_line |
| 158 | B | [Erebor] Archer | erebor_noble_archer | 52.5 | 46.6 | 194.5 | 54.5 | True | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 159 | B | [Dale] Dalian Shipman | dale_shipman | 52.5 | 45.8 | 164.0 | 49.0 | True | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 160 | B | [Dale] Dalian Militia | dale_man_at_arms | 52.2 | 39.0 | 117.5 | 35.4 | True | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 161 | B | [Rhûn] Far-Rhun Horseman | far_rhun_horseman | 52.1 | 35.8 | 135.0 | 34.1 | True | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 162 | B | [Gondor] Lossarnach Noble Captain | gondor_loss_noble_captain | 52.0 | 47.3 | 191.0 | 57.5 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 163 | B | [Isengard] Orthanc Guard | orthanc_guard | 52.0 | 46.7 | 208.0 | 58.2 | True | False | Defensive Troops | isengard | 31.0 | main_or_minor_line |
| 164 | B | [Isengard] Orthanc Chosen | orthanc_chosen | 52.0 | 46.7 | 208.0 | 58.2 | True | False | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 165 | B | [Rohan] Edoras Master Swordsman | rohan_edoras_master_swordsman | 52.0 | 46.7 | 168.8 | 52.3 | True | False | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 166 | B | [Isengard] Champions of the White Hand | urukhai_veteraninfantry | 51.9 | 46.6 | 215.0 | 58.1 | True | False | Defensive Troops | isengard | 31.0 | main_or_minor_line |
| 167 | B | [Rhûn] Wainrider Horseman | wainrider_horseman | 51.7 | 37.1 | 149.0 | 38.1 | True | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 168 | B | [Isengard] Orc Warg-Rider Overseer | orc_warg_overseer | 51.7 | 37.0 | 129.0 | 41.5 | True | True | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 169 | B | [Dale] Dalian Riverman | dale_riverman | 51.6 | 44.6 | 158.0 | 47.3 | True | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 170 | B | [Isengard] Orc Warg Ravager | isengard_orc_warg_ravager_v2 | 51.5 | 36.8 | 138.0 | 43.5 | True | True | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 171 | B | [Isengard] Uruk-Hai Veteran Spearman | urukhai_veteranspearman | 51.4 | 45.0 | 195.0 | 55.8 | True | False | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 172 | B | [Erebor] Infantry | erebor_noble_infantry | 51.3 | 44.0 | 194.8 | 55.4 | True | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 173 | B | [Mordor] Black Uruk Captain | mordor_uruk_captain | 51.2 | 41.7 | 185.0 | 50.8 | True | False | Defensive Troops | mordor | 36.0 | main_or_minor_line |
| 174 | B | [Erebor] Veteran Archer | erebor_noble_veteran_archer | 50.9 | 44.8 | 189.0 | 51.7 | True | False | Ranged Troops | erebor | 31.0 | main_or_minor_line |
| 175 | B | [Harad] Camel Scout | harad_camelscout | 50.7 | 34.1 | 96.0 | 32.5 | True | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 176 | B | [Mordor] Black Uruk Barad-Dur Guard | mordor_uruk_baraddurguard | 50.6 | 43.2 | 169.0 | 49.5 | True | False | Defensive Troops | mordor | 36.0 | main_or_minor_line |
| 177 | B | Guard | guard_rivendell | 50.6 | 45.0 | 220.0 | 45.2 | True | False | Defensive Troops | rivendell | 16.0 | special_or_unlinked |
| 178 | B | [Iron Hills] Warrior | iron_hills_reg_warrior | 50.6 | 36.2 | 168.0 | 43.8 | True | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 179 | B | [Dol Guldur] Uruk Black Guard | dg_uruk_black_guard | 50.4 | 45.7 | 210.0 | 56.8 | True | False | Defensive Troops | dolguldur | 31.0 | main_or_minor_line |
| 180 | B | [Rhûn] Far-Rhun Iron Legionary | far_rhun_iron_legionary | 50.3 | 42.9 | 185.0 | 47.1 | True | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 181 | B | [Dol Guldur] Shadow Warden | dg_khamul_shadow_warden | 50.2 | 45.1 | 173.3 | 44.4 | True | False | Defensive Troops | dolguldur | 36.0 | main_or_minor_line |
| 182 | B | [Rivendell] Megil Mallenloth | rivendell_knight_golden_flower | 50.1 | 44.4 | 191.0 | 44.3 | True | False | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 183 | B | [Dunland] Hebog-lûth Noble Horse Archer | dunland_falcon_noble_horse_archer | 50.1 | 53.0 | 158.0 | 52.0 | False | True | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 184 | B | [Rhûn] Wain Darkhan | wain_darkhan | 50.1 | 41.6 | 209.0 | 55.9 | True | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 185 | B | [Dale] Dalian Bowman | dale_longbowman | 50.1 | 44.3 | 144.0 | 43.2 | True | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 186 | B | [Dunland] Turch-lûth Huskarl | dunland_boar_warlord | 49.9 | 41.4 | 168.0 | 51.9 | True | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 187 | B | [Gondor] Dol Amroth Swan Guard | gondor_da_swan_guard | 49.8 | 39.9 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 188 | B | [Gondor] Dol Amroth Foot Knight | gondor_da_foot_knight | 49.8 | 39.9 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 189 | B | [Gundabad] Pale Uruk Mountain Guard | gundabad_chosen_of_tharzog | 49.8 | 44.9 | 220.0 | 55.5 | True | False | Defensive Troops | gundabad | 36.0 | main_or_minor_line |
| 190 | B | [Mirkwood] Greenwood Swordsman | mirkwood_swordsman | 49.7 | 43.8 | 206.0 | 53.9 | True | False | Defensive Troops | mirkwood | 46.0 | main_or_minor_line |
| 191 | B | [Mirkwood] Greenwood Guards | mirkwood_guards | 49.7 | 43.8 | 206.0 | 53.9 | True | False | Defensive Troops | mirkwood | 41.0 | main_or_minor_line |
| 192 | B | [Isengard] Uruk-Hai Infantry | urukhai_infantry | 49.5 | 43.6 | 199.0 | 53.6 | True | False | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 193 | B | [Gondor] Harondor Frontier Guard | gondor_har_frontier_guard | 49.5 | 42.6 | 165.0 | 50.5 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 194 | B | [Gondor] Anfalas Veteran Infantry | gondor_anf_vet_infantry | 49.5 | 42.6 | 165.0 | 50.5 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 195 | B | [Mordor] Black Uruk Vanguard | mordor_uruk_vanguard | 49.5 | 40.8 | 180.0 | 49.5 | True | False | Defensive Troops | mordor | 31.0 | main_or_minor_line |
| 196 | B | [Dunland] Blaidd-lûth Champion | dunland_wolf_champion | 49.4 | 42.2 | 168.0 | 53.0 | True | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 197 | B | [Mordor] Black Uruk Shield Guard | mordor_uruk_shieldguard | 49.3 | 42.1 | 163.0 | 47.9 | True | False | Defensive Troops | mordor | 31.0 | main_or_minor_line |
| 198 | B | [Iron Hills] Fighter | iron_hills_reg_fighter | 49.3 | 34.3 | 158.4 | 40.9 | True | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 199 | B | [Dunland] Turch-lûth Ironhide | dunland_boar_boar_warrior | 49.3 | 40.6 | 161.0 | 50.7 | True | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 200 | B | [Rhûn] Kharaghûl Keshig | kharaghul_keshig | 49.2 | 50.5 | 184.0 | 47.6 | False | True | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 201 | B | [Gondor] Lebennin Sea Guard | gondor_leb_sea_guard | 49.2 | 41.5 | 157.0 | 48.9 | True | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 202 | B | [Rhûn] Far-Rhun Gate Guard | far_rhun_gate_guard | 49.0 | 41.3 | 176.0 | 44.7 | True | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 203 | B | [Gondor] Harondor Javelineer | gondor_har_javelineer | 48.9 | 41.1 | 160.0 | 48.3 | True | False | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 204 | B | [Gondor] Serelond Veteran Maceman | gondor_ser_vet_maceman | 48.9 | 41.7 | 172.0 | 49.2 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 205 | B | [Rhûn] Kharaghûl Karash Keshig | kharaghul_karash_keshig | 48.8 | 51.0 | 186.0 | 48.3 | False | True | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 206 | B | [Gondor] Methir Sun Warden | gondor_met_sun_warden | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 207 | B | [Gondor] Linhir Veteran Spearman | gondor_lin_vet_spearman | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 208 | B | [Gondor] Ringlo Vale Warden | gondor_ring_warden | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 209 | B | [Gondor] Ringlo Vale Spearman | gondor_ring_spearman | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 210 | B | [Gondor] Pelargir Veteran Infantry | gondor_pel_vet_infantry | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 211 | B | [Gondor] Pelargir Infantry | gondor_pel_infantry | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 212 | B | [Gondor] Pelargir Anchor Guard | gondor_pel_anchor_guard | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 213 | B | [Gondor] Belfalas Coastguard | gondor_bel_coastguard | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 214 | B | [Gondor] Methir Sun Knight | gondor_met_sun_knight | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 215 | B | [Gondor] Methir Glaive Guard | gondor_met_glaive_guard | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 216 | B | [Gondor] Linhir High Guard | gondor_lin_high_guard | 48.7 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 217 | B | [Gondor] Anfalas Infantry | gondor_anf_infantry | 48.5 | 41.2 | 149.0 | 48.5 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 218 | B | [Gondor] Belfalas Veteran Infantry | gondor_bel_vet_infantry | 48.5 | 41.2 | 149.0 | 48.5 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 219 | B | [Ironpass] Recruit | ironpass_recruit | 48.5 | 32.2 | 133.4 | 35.8 | True | False | Defensive Troops | erebor | 11.0 | main_or_minor_line |
| 220 | B | [Gondor] Harondor Infantry | gondor_har_infantry | 48.4 | 41.1 | 160.0 | 48.3 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 221 | B | [Dol Guldur] Uruk Fell Infantry | dg_uruk_fell_infantry | 48.2 | 42.9 | 195.0 | 52.5 | True | False | Defensive Troops | dolguldur | 26.0 | main_or_minor_line |
| 222 | B | [Gondor] Lossarnach Noble Warden | gondor_loss_noble_warden | 48.2 | 42.3 | 169.0 | 50.0 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 223 | B | [Dunland] Blaidd-lûth Axeman | dunland_wolf_axeman | 48.2 | 40.6 | 161.0 | 50.7 | True | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 224 | B | [Mordor] Black Uruk Shieldbearer | mordor_uruk_shieldbearer | 48.2 | 35.4 | 127.6 | 38.0 | True | False | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 225 | B | [Gondor] Osgiliath Dome Guard | gondor_osg_dome_guard | 48.1 | 40.0 | 163.0 | 49.5 | True | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 226 | B | [Erebor] Shield-Breaker | erebor_noble_shield_breaker | 48.1 | 55.7 | 286.5 | 82.7 | False | False | Defensive Troops | erebor | 41.0 | main_or_minor_line |
| 227 | B | [Rhûn] Darkhûn Infantry | darkhun_infantry | 48.0 | 40.5 | 174.0 | 43.6 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 228 | B | [Iron Hills] Noble | iron_hills_noble | 47.9 | 41.5 | 195.0 | 49.2 | True | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 229 | B | [Gundabad] Pale Uruk Infantry | gundabad_veteran_sword_warrior | 47.9 | 41.4 | 193.3 | 50.3 | True | False | Defensive Troops | gundabad | 31.0 | main_or_minor_line |
| 230 | B | [Gondor] Serelond Maceman | gondor_ser_maceman | 47.9 | 41.5 | 166.0 | 48.9 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 231 | B | [Gondor] Lossarnach Noble Sergeant | gondor_loss_noble_sergeant | 47.9 | 41.9 | 163.0 | 49.5 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 232 | B | [Gondor] Arndir Veteran Infantry | gondor_arn_vet_infantry | 47.9 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 233 | B | [Gondor] Cair Andros Warden | gondor_ca_warden | 47.9 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 234 | B | [Gondor] Arndir Foot-Knight | gondor_arn_foot_knight | 47.9 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 235 | B | [Rhûn] Loke-Rim Shieldguard | loke_rim_shieldguard | 47.9 | 40.1 | 150.3 | 37.0 | True | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 236 | B | [Rhûn] Dragon-Wrath Ash Shieldguard | dragon_wrath_ash_shieldguard | 47.9 | 40.1 | 150.3 | 37.0 | True | False | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 237 | B | [Gondor] Harondor Veteran Skirmisher | gondor_har_vet_skirmisher | 47.9 | 39.8 | 144.0 | 46.3 | True | False | Skirmishers | gondor | 21.0 | main_or_minor_line |
| 238 | B | [Rhûn] Loke-Rim Footman | loke_rim_footman | 47.8 | 39.6 | 162.5 | 42.2 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 239 | B | [Rhûn] Dragon-Wrath Disciple | dragon_wrath_disciple | 47.8 | 39.6 | 162.5 | 42.2 | True | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 240 | B | [Isengard] Uruk-Hai Spearman | urukhai_spearman | 47.7 | 40.2 | 176.0 | 48.6 | True | False | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 241 | B | [Gondor] Cair Andros Guard | gondor_ca_guard | 47.7 | 41.2 | 149.0 | 48.5 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 242 | B | [Gundabad] Pale Uruk Pike-Reaver | gundabad_veteran_spear_warrior | 47.7 | 38.0 | 183.3 | 49.0 | True | False | Defensive Troops | gundabad | 31.0 | main_or_minor_line |
| 243 | B | [Aharad] Elephant Rider | harad_elephant_rider | 47.7 | 48.5 | 71.0 | 17.4 | False | True | Defensive Troops | aserai | 51.0 | special_or_unlinked |
| 244 | B | [Rhûn] Kharaghûl Rider | kharaghul_rider | 47.6 | 30.0 | 106.0 | 25.6 | True | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 245 | B | [Gondor] Lossarnach Veteran Guard | gondor_loss_vet_guard | 47.6 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 246 | B | [Gondor] Lossarnach Guard | gondor_loss_guard | 47.6 | 41.5 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 247 | B | [Gondor] Arndir Hill-Knight | gondor_arn_hill_knight | 47.6 | 45.4 | 157.0 | 48.9 | False | True | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 248 | B | [Gondor] Arndir Veteran Knight | gondor_arn_vet_knight | 47.6 | 45.4 | 157.0 | 48.9 | False | True | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 249 | B | [Gondor] Arndir Knight | gondor_arn_knight | 47.6 | 45.4 | 157.0 | 48.9 | False | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 250 | B | [Dale] Veteran Militia Spearman | dale_militia_veteran_spearman | 47.5 | 40.0 | 122.0 | 36.7 | True | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 251 | B | [Gondor] Dol Amroth Veteran Infantry | gondor_da_vet_infantry | 47.5 | 39.9 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 252 | B | [Dunland] Uch-lûth Iron Wall | dunland_ox_iron_wall | 47.5 | 42.8 | 173.0 | 54.0 | True | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 253 | B | [Isengard] Uruk-Hai Swordman | urukhai_swordman | 47.5 | 40.9 | 182.0 | 49.6 | True | False | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 254 | B | [Umbar] Naru n'Aru Royal Guard | umbar_elite_root0000 | 47.4 | 32.3 | 156.0 | 37.1 | True | False | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 255 | B | [Gondor] Pelargir Veteran | gondor_pel_veteran | 47.4 | 39.8 | 144.0 | 46.3 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 256 | B | [Gondor] Linhir Spearman | gondor_lin_spearman | 47.4 | 39.8 | 144.0 | 46.3 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 257 | B | [Gondor] Methir Glaiveman | gondor_met_glaiveman | 47.4 | 39.8 | 144.0 | 46.3 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 258 | B | [Iron Hills] Infantry | iron_hills_noble_infantry | 47.4 | 39.7 | 192.0 | 46.5 | True | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 259 | B | [Dol Guldur] Uruk Swordsman | dg_uruk_swordsman | 47.3 | 40.7 | 190.0 | 49.2 | True | False | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 260 | B | [Mirkwood] Militia Veteran Spearman | mirkwood_militia_veteran_spearman | 47.2 | 27.5 | 134.5 | 32.5 | True | False | Defensive Troops | mirkwood | 16.0 | special_or_unlinked |
| 261 | B | [Rohan] Meduseld Helmingas Spearman | rohan_edoras_meduseld_helmingas_spearman | 47.2 | 38.0 | 129.0 | 39.3 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 262 | B | [Rohan] West Emnet Recruit | rohan_westemnet_recruit | 47.2 | 31.2 | 31.0 | 12.5 | True | True | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 263 | B | [Rohan] Wold Recruit | rohan_wold_recruit | 47.2 | 31.2 | 31.0 | 12.5 | True | True | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 264 | B | [Rohan] East Emnet Recruit | rohan_eastemnet_recruit | 47.2 | 31.2 | 31.0 | 12.5 | True | True | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 265 | B | [Gundabad] Pale Uruk Ravager | gundabad_brute | 47.1 | 40.8 | 185.0 | 49.5 | True | False | Defensive Troops | gundabad | 26.0 | main_or_minor_line |
| 266 | B | [Iron Hills] Company | iron_hills_reg_company | 47.1 | 27.9 | 114.2 | 31.4 | True | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 267 | B | [Isengard] Orc Warg Raider | isengard_orc_warg_raider_v2 | 47.0 | 30.9 | 114.0 | 34.8 | True | True | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 268 | B | [Rivendell] Militia Spearman | rivendell_militia_spearman | 46.9 | 28.6 | 108.2 | 24.5 | True | False | Defensive Troops | rivendell | 11.0 | special_or_unlinked |
| 269 | B | [Gondor] Fountain Guard | gondor_mt_fountain_guard | 46.9 | 40.2 | 165.0 | 49.6 | True | False | Defensive Troops | gondor | 46.0 | main_or_minor_line |
| 270 | B | [Gondor] Ithil Guard Captain | gondor_ith_captain | 46.9 | 35.7 | 165.0 | 49.6 | True | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 271 | B | [Dunland] Draig-lûth Sharpshooter | dunland_dragon_sniper | 46.8 | 40.5 | 160.0 | 49.0 | True | False | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 272 | B | [Gondor] Pinnath Gelin Veteran Spearman | gondor_pg_vet_spearman | 46.8 | 39.0 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 273 | B | [Gondor] Pinnath Gelin Spearwarden | gondor_pg_spearwarden | 46.8 | 39.0 | 157.0 | 48.9 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 274 | B | [Gondor] Belfalas Veteran Archer | gondor_bel_vet_archer | 46.8 | 40.0 | 152.0 | 46.7 | True | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 275 | B | [Dale] Dalian Marksman | dale_royal_archer | 46.7 | 40.0 | 122.0 | 36.7 | True | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 276 | B | [Isengard] Orc Warg Rider | isengard_orc_warg_rider_v2 | 46.7 | 30.6 | 102.0 | 32.0 | True | True | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 277 | B | [Rhûn] Balcoth Farshot Horse Archer | balcoth_farshot_horse_archer | 46.6 | 48.6 | 176.0 | 44.7 | False | True | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 278 | B | [Gondor] Citadel Guard Captain | gondor_mt_captain | 46.6 | 39.8 | 159.0 | 49.0 | True | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 279 | B | [Gondor] Osgiliath Longbowman | gondor_osg_longbowman | 46.6 | 39.8 | 155.0 | 49.0 | True | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 280 | B | [Gondor] Calembel Swordsman | gondor_cal_swordsman | 46.6 | 39.8 | 144.0 | 46.3 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 281 | B | [Gondor] Harondor Guardsman | gondor_har_guardsman | 46.6 | 39.8 | 144.0 | 46.3 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 282 | B | [Gondor] Arndir Infantry | gondor_arn_infantry | 46.6 | 39.8 | 144.0 | 46.3 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 283 | B | [Gondor] Citadel Guard Sergeant | gondor_mt_sergeant | 46.4 | 39.5 | 151.0 | 48.7 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 284 | B | [Dol Guldur] Shadow Infantry | dg_khamul_shadow_infantry | 46.4 | 40.1 | 163.3 | 43.0 | True | False | Defensive Troops | dolguldur | 31.0 | main_or_minor_line |
| 285 | B | [Gondor] Osgiliath Guard | gondor_osg_guard | 46.3 | 39.4 | 149.0 | 48.5 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 286 | B | [Mordor] Morannon Heavy Infantry | morannon_heavy_infantry | 46.3 | 39.4 | 158.0 | 47.3 | True | False | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 287 | B | [Gondor] Arndir Cavalry | gondor_arn_cavalry | 46.3 | 43.6 | 144.0 | 46.3 | False | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 288 | B | [Dol Guldur] Shadow Disciple | dg_khamul_shadow_disciple | 46.2 | 40.0 | 163.0 | 42.8 | True | False | Defensive Troops | dolguldur | 26.0 | main_or_minor_line |
| 289 | B | [Dol Guldur] Orc Reaver | dg_orc_reaver | 46.2 | 38.9 | 180.0 | 46.6 | True | False | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 290 | B | Guard | guard_rohan | 46.0 | 36.0 | 130.0 | 36.5 | True | False | Defensive Troops | vlandia | nan | special_or_unlinked |
| 291 | B | [Dunland] Hebog-lûth Horse Archer | dunland_falcon_wildrider | 46.0 | 47.7 | 137.0 | 47.7 | False | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 292 | B | [Rohan] Edoras Helmingas Swordsman | rohan_edoras_helmingas_swordsman | 45.9 | 38.5 | 134.6 | 40.1 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 293 | B | [Rohan] Meduseld Veteran Spearman | rohan_edoras_meduseld_veteran_spearman | 45.9 | 37.4 | 128.0 | 38.5 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 294 | B | [Dunland] Uch-lûth Bodyguard | dunland_ox_guard | 45.8 | 40.6 | 161.0 | 50.7 | True | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 295 | B | [Rhûn] Kharaghûl Youth | kharaghul_youth | 45.7 | 30.2 | 90.0 | 23.2 | True | True | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 296 | B | [Iron Hills] Swordsman | iron_hills_noble_swordsman | 45.6 | 38.5 | 185.0 | 44.7 | True | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 297 | B | [Erebor] Longbeard | erebor_noble_longbeard | 45.6 | 31.6 | 126.5 | 37.0 | True | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 298 | B | [Rohan] Edoras Veteran Swordsman | rohan_edoras_veteran_swordsman | 45.6 | 37.8 | 131.8 | 39.1 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 299 | B | [Gondor] Dol Amroth Infantry | gondor_da_infantry | 45.4 | 38.2 | 144.0 | 46.3 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 300 | B | [Harad] Warlance | harad_warlance | 45.2 | 35.3 | 169.0 | 43.3 | True | False | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 301 | B | [Harad] Sunlance | harad_sunlance | 45.2 | 35.3 | 169.0 | 43.3 | True | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 302 | B | [Harad] Bronze Fang | harad_bronzefang | 45.2 | 35.3 | 169.0 | 43.3 | True | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 303 | B | [Dunland] Turch-lûth Goreblade | dunland_boar_spearman | 45.2 | 35.3 | 143.0 | 43.5 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 304 | B | [Umbar] Abrazanim Nardutarik | umbar_elite_root000 | 45.2 | 30.8 | 156.0 | 37.1 | True | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 305 | B | [Harad] Serpent Archer | harad_serpenthorsearcher | 45.2 | 46.2 | 183.0 | 46.8 | False | True | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 306 | B | [Rohan] West Marches Veteran Spearman | rohan_westmarches_meduseld_spearman | 45.2 | 36.9 | 116.0 | 37.7 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 307 | B | [Umbar] Rozadan Footmen | umbar_elite_root00 | 45.2 | 29.9 | 156.0 | 37.1 | True | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 308 | B | [Gondor] Anórien Veteran Infantry | gondor_ano_vet_infantry | 45.1 | 36.8 | 143.0 | 42.0 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 309 | B | [Goblin] Goblin Pike-Reaver | goblin_veteran_spear_warrior | 45.1 | 34.3 | 138.0 | 43.5 | True | False | Defensive Troops | goblin | 31.0 | main_or_minor_line |
| 310 | B | [Misty Mountains] Orc Pike-Reaver | mistymountainorcs_veteran_spear_warrior | 45.1 | 34.3 | 138.0 | 43.5 | True | False | Defensive Troops | mistymountainorcs | 31.0 | main_or_minor_line |
| 311 | B | [Gondor] Belfalas Infantry | gondor_bel_infantry | 44.9 | 36.6 | 135.0 | 41.5 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 312 | B | [Erebor] Warrior | erebor_reg_warrior | 44.8 | 30.1 | 137.2 | 39.0 | True | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 313 | B | [Dol Guldur] Uruk Warrior | dg_uruk_veteran_warrior | 44.7 | 37.3 | 170.0 | 44.2 | True | False | Defensive Troops | dolguldur | 16.0 | main_or_minor_line |
| 314 | B | [Rhûn] Easterling Veteran Swordsman | easterling_veteran_swordsman_new | 44.5 | 35.4 | 146.0 | 36.0 | True | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 315 | B | [Rhûn] Balcoth Veteran Axeman | balcoth_veteran_axeman | 44.5 | 35.4 | 146.0 | 36.0 | True | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 316 | B | [Mirkwood] Silvan Levy | mirkwood_recruit | 44.5 | 37.1 | 176.0 | 44.0 | True | False | Defensive Troops | mirkwood | 36.0 | main_or_minor_line |
| 317 | B | Guard | guard_rhun | 44.5 | 37.1 | 179.0 | 46.0 | True | False | Defensive Troops | khuzait | 16.0 | special_or_unlinked |
| 318 | B | [Rhûn] Wain Iron-Glaive | wain_iron_glaive | 44.5 | 36.0 | 187.0 | 47.5 | True | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 319 | B | [Mordor] Black Uruk Infantry | mordor_uruk_infantry | 44.4 | 33.4 | 140.5 | 38.7 | True | False | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 320 | B | [Rhûn] Easterling Veteran Halberdier | easterling_veteran_halberdier_new | 44.4 | 35.8 | 150.0 | 36.6 | True | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 321 | B | [Gondor] Lebennin Veteran Infantry | gondor_leb_vet_infantry | 44.3 | 35.1 | 130.0 | 39.4 | True | False | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 322 | B | [Goblin] Goblin Infantry | goblin_veteran_sword_warrior | 44.3 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | goblin | 31.0 | main_or_minor_line |
| 323 | B | [Misty Mountains] Orc Infantry | mistymountainorcs_veteran_sword_warrior | 44.3 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | mistymountainorcs | 31.0 | main_or_minor_line |
| 324 | B | [Isengard] Orc Reaver | isengard_orc_reaver | 44.3 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 325 | B | [Mordor] Orc Infantry | mordor_orc_infantry | 44.3 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 326 | B | [Rohan] West-March Heavy Spearman | rohan_westmarches_veteran_spearman | 44.3 | 35.8 | 101.0 | 36.0 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 327 | B | [Isengard] Uruk-Hai Warrior | urukhai_warrior | 44.3 | 36.8 | 162.0 | 41.1 | True | False | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 328 | B | [Gondor] Osgiliath Archer | gondor_osg_archer | 44.1 | 36.6 | 135.0 | 41.5 | True | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 329 | B | [Gondor] Osgiliath Infantry | gondor_osg_infantry | 44.1 | 36.6 | 135.0 | 41.5 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 330 | B | [Gondor] Anórien Infantry | gondor_ano_infantry | 44.0 | 35.4 | 138.0 | 39.8 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 331 | B | [Goblin] Goblin Ravager | goblin_brute | 44.0 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | goblin | 26.0 | main_or_minor_line |
| 332 | B | [Misty Mountains] Orc Ravager | mistymountainorcs_brute | 44.0 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | mistymountainorcs | 26.0 | main_or_minor_line |
| 333 | B | [Dunland] Blaidd-lûth Raider | dunland_wolf_raider | 43.6 | 34.6 | 129.0 | 42.5 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 334 | B | [Goblin] Goblin Mountain Guard | goblin_chosen_of_tharzog | 43.6 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | goblin | 36.0 | main_or_minor_line |
| 335 | B | [Goblin] Bolg's Ironfang | goblin_bolgs_ironfang | 43.6 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | goblin | 36.0 | main_or_minor_line |
| 336 | B | [Misty Mountains] Orc Mountain Guard | mistymountainorcs_chosen_of_tharzog | 43.6 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | mistymountainorcs | 36.0 | main_or_minor_line |
| 337 | B | [Misty Mountains] Bolg's Ironfang | mistymountainorcs_bolgs_ironfang | 43.6 | 36.8 | 138.0 | 43.5 | True | False | Defensive Troops | mistymountainorcs | 36.0 | main_or_minor_line |
| 338 | B | [Erebor] Militia Veteran Spearman | erebor_militia_veteran_spearman | 43.4 | 22.8 | 93.8 | 26.4 | True | False | Defensive Troops | erebor | 16.0 | special_or_unlinked |
| 339 | B | [Isengard] Orc Warg-Rider Scout | orc_warg_scout | 43.3 | 26.1 | 104.0 | 25.3 | True | True | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 340 | B | [Rohan] Westfold Veteran Axeman | rohan_westfold_veteran_axeman | 43.2 | 35.8 | 101.0 | 36.0 | True | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 341 | B | [Erebor] Fighter | erebor_reg_fighter | 43.2 | 28.2 | 124.0 | 36.2 | True | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 342 | B | [Gondor] Ithil Guard Sergeant | gondor_ith_sergeant | 43.1 | 30.8 | 143.0 | 42.4 | True | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 343 | B | [Dunland] Turch-lûth Tuskrunner | dunland_boar_warrior | 43.1 | 34.0 | 138.0 | 42.7 | True | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 344 | B | [Dunland] Blaidd-lûth Warrior | dunland_clan_warrior | 43.1 | 34.0 | 138.0 | 42.7 | True | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 345 | B | [Mirkwood] Militia Spearman | mirkwood_militia_spearman | 43.0 | 26.7 | 110.8 | 31.3 | True | False | Defensive Troops | mirkwood | 11.0 | special_or_unlinked |
| 346 | B | [Gondor] Pinnath Gelin Spearman | gondor_pg_spearman | 43.0 | 34.1 | 135.0 | 41.5 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 347 | B | [Gondor] Cair Andros Infantry | gondor_ca_infantry | 43.0 | 35.1 | 130.0 | 39.4 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 348 | B | [Gondor] Belfalas Archer | gondor_bel_archer | 43.0 | 35.1 | 130.0 | 39.4 | True | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 349 | B | [Gondor] Anfalas Guardsman | gondor_anf_guardsman | 43.0 | 35.1 | 130.0 | 39.4 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 350 | B | [Gondor] Osgiliath Skirmisher | gondor_osg_skirmisher | 42.8 | 34.8 | 122.0 | 39.0 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 351 | B | [Gondor] Lossarnach Veteran Axebearer | gondor_loss_vet_axebearer | 42.7 | 35.1 | 130.0 | 39.4 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 352 | B | [Harad] Champion | harad_champion | 42.6 | 34.6 | 149.0 | 42.3 | True | False | Defensive Troops | aserai | 31.0 | main_or_minor_line |
| 353 | B | [Rhûn] Kharaghûl Horse Scout | kharaghul_horse_scout | 42.6 | 42.9 | 144.0 | 36.3 | False | True | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 354 | B | [Rhûn] Kharaghûl Horse Archer | kharaghul_horse_archer | 42.5 | 42.7 | 146.0 | 36.0 | False | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 355 | B | [Dunland] Draig-lûth Firebolt | dunland_dragon_firebolt | 42.5 | 34.8 | 121.0 | 42.1 | True | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 356 | B | [Harad] Rider of the Golden Veil | harad_horsearcher | 42.4 | 42.7 | 158.0 | 41.5 | False | True | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 357 | B | [Gondor] Ringlo Vale Guardsman | gondor_ring_guardsman | 42.4 | 33.2 | 124.0 | 36.6 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 358 | B | [Gondor] Linhir Footman | gondor_lin_footman | 42.4 | 33.2 | 124.0 | 36.6 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 359 | B | [Gondor] Pelargir Skirmisher | gondor_pel_skirmisher | 42.4 | 33.2 | 124.0 | 36.6 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 360 | B | [Gondor] Lebennin Infantry | gondor_leb_infantry | 42.4 | 32.6 | 110.0 | 35.6 | True | False | Skirmishers | gondor | 21.0 | main_or_minor_line |
| 361 | B | [Rohan] Westfold Helmingas Axeman | rohan_westfold_helmingas_axeman | 42.3 | 34.6 | 109.0 | 33.1 | True | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 362 | B | [Rhûn] Balcoth Horse Archer | balcoth_horse_archer | 42.0 | 42.5 | 140.0 | 35.7 | False | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 363 | B | [Rohan] West-March Spearman | rohan_westmarches_spearman | 42.0 | 32.7 | 100.0 | 31.5 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 364 | B | [Rohan] Meduseld Spearman | rohan_edoras_meduseld_spearman | 42.0 | 32.2 | 103.0 | 30.7 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 365 | B | [Gondor] Lossarnach Noble Veteran | gondor_loss_noble_veteran | 41.9 | 34.0 | 122.0 | 37.8 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 366 | B | [Rohan] Edoras Swordsman | rohan_edoras_swordsman | 41.8 | 32.9 | 110.8 | 31.8 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 367 | B | [Isengard] Uruk-Hai Fighter | urukhai_fighter | 41.7 | 33.5 | 139.0 | 36.2 | True | False | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 368 | B | [Dunland] Wild-man Spearman | dunland_veteran_spearman | 41.7 | 30.7 | 124.0 | 34.9 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 369 | B | [Gondor] Arndir Noble | gondor_arn_noble_t4 | 41.6 | 33.2 | 124.0 | 36.6 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 370 | B | [Gondor] Anórien Guardsman | gondor_ano_guardsman | 41.6 | 33.2 | 124.0 | 36.6 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 371 | B | [Gondor] Calembel Noble | gondor_cal_noble | 41.6 | 33.2 | 124.0 | 36.6 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 372 | B | [Gondor] Methir Noble | gondor_met_noble | 41.6 | 33.2 | 124.0 | 36.6 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 373 | B | [Gondor] Gondor Veteran Militia Spearman | gondor_militia_veteran_spearman | 41.4 | 32.0 | 102.0 | 34.8 | True | False | Defensive Troops | gondor | 16.0 | special_or_unlinked |
| 374 | B | [Gondor] Cair Andros Veteran | gondor_ca_veteran | 41.4 | 33.0 | 116.0 | 36.2 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 375 | B | [Erebor] Ranger | erebor_noble_ranger | 41.2 | 32.4 | 116.5 | 33.5 | True | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 376 | B | [Gondor] Harondor Footman | gondor_har_footman | 41.1 | 32.6 | 110.0 | 35.6 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 377 | B | [Gondor] Linhir Noble | gondor_lin_noble | 41.0 | 31.5 | 102.0 | 34.0 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 378 | B | [Gondor] Ringlo Vale Footman | gondor_ring_footman | 41.0 | 31.5 | 102.0 | 34.0 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 379 | B | [Rohan] Westfolders | rohan_westfold_axeman | 40.9 | 32.7 | 100.0 | 31.5 | True | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 380 | B | [Rohan] Militia Veteran Spearman | rohan_militia_veteran_spearman | 40.7 | 29.8 | 91.3 | 27.1 | True | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 381 | B | [Dale] Lake-Town Militia | dale_militia | 40.7 | 31.0 | 77.0 | 23.5 | True | False | Defensive Troops | sturgia | 11.0 | main_or_minor_line |
| 382 | B | [Dale] Militia Spearman | dale_militia_spearman | 40.7 | 31.0 | 77.0 | 23.5 | True | False | Defensive Troops | sturgia | 6.0 | main_or_minor_line |
| 383 | B | [Dale] Dalian Levy | dale_squire | 40.7 | 31.0 | 77.0 | 23.5 | True | False | Defensive Troops | sturgia | 11.0 | main_or_minor_line |
| 384 | B | [Gondor] Gondor Militia Spearman | gondor_militia_spearman | 40.6 | 30.9 | 94.0 | 33.2 | True | False | Defensive Troops | gondor | 11.0 | special_or_unlinked |
| 385 | B | [Gondor] Ithil Guard Veteran | gondor_ith_veteran | 40.5 | 26.1 | 120.0 | 34.6 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 386 | B | [Gondor] Anórien Footman | gondor_ano_footman | 40.4 | 31.7 | 110.0 | 34.4 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 387 | B | [Gondor] Dol Amroth Footman | gondor_da_footman | 40.4 | 31.7 | 124.0 | 36.6 | True | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 388 | B | [Aharad] Mumakil Rider | harad_mumakil_rider | 40.3 | 38.9 | 71.0 | 17.4 | False | True | Defensive Troops | aserai | 51.0 | special_or_unlinked |
| 389 | B | [Gondor] Anfalas Footman | gondor_anf_footman | 40.2 | 31.5 | 102.0 | 34.0 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 390 | B | [Gondor] Harondor Militia | gondor_har_militia | 40.2 | 31.5 | 102.0 | 34.0 | True | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 391 | B | [Gondor] Arndir Noble | gondor_arn_noble | 40.2 | 31.5 | 102.0 | 34.0 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 392 | B | [Rhûn] Easterling Halberdier | easterling_halberdier_new | 40.0 | 30.2 | 140.0 | 35.7 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 393 | C | [Goblin] Militia Veteran Spearman | goblin_militia_veteran_spearman | 40.0 | 24.9 | 90.5 | 28.6 | True | False | Defensive Troops | goblin | 16.0 | special_or_unlinked |
| 394 | C | [Misty Mountains] Militia Veteran Spearman | mistymountainorcs_militia_veteran_spearman | 40.0 | 24.9 | 90.5 | 28.6 | True | False | Defensive Troops | mistymountainorcs | 16.0 | special_or_unlinked |
| 395 | C | [Isengard] Orc Marauder | isengard_orc_marauder | 39.9 | 31.1 | 116.0 | 35.0 | True | False | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 396 | C | [Mordor] Morannon Infantry | morannon_infantry | 39.9 | 31.1 | 116.0 | 35.0 | True | False | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 397 | C | [Dunland] Wild-man Swordman | dunland_veteran_swordman | 39.9 | 29.4 | 98.0 | 32.9 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 398 | C | [Erebor] Company | erebor_reg_company | 39.9 | 23.4 | 95.6 | 29.0 | True | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 399 | C | [Iron Hills] Recruit | iron_hills_reg_recruit | 39.8 | 24.8 | 98.8 | 26.9 | True | False | Defensive Troops | erebor | 11.0 | main_or_minor_line |
| 400 | C | [Iron Hills] Militia | iron_hills_reg_militia | 39.8 | 25.0 | 99.6 | 27.1 | True | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 401 | C | [Dunland] Uch-lûth Pikeman | dunland_ox_pikeman | 39.7 | 32.7 | 123.0 | 39.7 | True | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 402 | C | [Misty Mountains] Orc Raider | mistymountainorcs_fighter | 39.6 | 31.1 | 116.0 | 35.0 | True | False | Defensive Troops | mistymountainorcs | 21.0 | main_or_minor_line |
| 403 | C | [Goblin] Goblin Raider | goblin_fighter | 39.6 | 31.1 | 116.0 | 35.0 | True | False | Defensive Troops | goblin | 21.0 | main_or_minor_line |
| 404 | C | [Isengard] Orc Warrior | isengard_orc_warrior | 39.4 | 30.4 | 96.0 | 31.8 | True | False | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 405 | C | Mordor Militia Veteran Spearman | mordor_militia_veteran_spearman | 39.4 | 23.1 | 96.0 | 26.0 | True | False | Defensive Troops | mordor | 16.0 | special_or_unlinked |
| 406 | C | [Gondor] Ithil Guard Watcher | gondor_ith_watcher | 39.4 | 24.6 | 102.0 | 32.4 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 407 | C | [Rhûn] Far-Rhun Infantry | far_rhun_infantry | 39.4 | 30.4 | 146.0 | 36.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 408 | C | [Gundabad] Militia Veteran Spearman | gundabad_militia_veteran_spearman | 39.3 | 21.2 | 97.5 | 23.1 | True | False | Defensive Troops | gundabad | 16.0 | special_or_unlinked |
| 409 | C | [Isengard] Orc Warg Scout | isengard_orc_warg_scout_v2 | 39.2 | 20.8 | 55.0 | 17.4 | True | True | Defensive Troops | isengard | 6.0 | main_or_minor_line |
| 410 | C | [Gondor] Pinnath Gelin Footman | gondor_pg_footman | 39.1 | 29.0 | 102.0 | 34.0 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 411 | C | [Gondor] Citadel Guard Veteran | gondor_mt_veteran | 39.1 | 30.0 | 120.0 | 34.6 | True | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 412 | C | [Gondor] Belfalas Soldier | gondor_bel_soldier | 39.1 | 30.0 | 96.0 | 31.8 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 413 | C | [Gondor] Dol Amroth Noble | gondor_da_noble | 39.1 | 29.9 | 102.0 | 34.0 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 414 | C | [Dunland] Draig-lûth Crossbowman | dunland_dragon_crossbowman | 38.9 | 30.1 | 109.0 | 37.0 | True | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 415 | C | [Erebor] Noble | erebor_noble | 38.8 | 28.8 | 114.0 | 32.8 | True | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 416 | C | [Mordor] Morannon Warrior | morannon_warrior | 38.7 | 29.5 | 116.0 | 35.0 | True | False | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 417 | C | [Rhûn] Wain Glaiveman | wain_glaiveman | 38.6 | 28.3 | 142.0 | 36.1 | True | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 418 | C | [Mordor] Black Uruk Warrior | mordor_uruk_warrior | 38.5 | 25.1 | 108.2 | 29.1 | True | False | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 419 | C | [Gundabad] Pale Uruk Raider | gundabad_fighter | 38.5 | 29.6 | 130.0 | 32.8 | True | False | Defensive Troops | gundabad | 21.0 | main_or_minor_line |
| 420 | C | [Mordor] Orc Warrior | mordor_orc_warrior | 38.4 | 29.5 | 116.0 | 35.0 | True | False | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 421 | C | [Dol Guldur] Shadow Initiate | dg_khamul_shadow_initiate | 38.3 | 30.0 | 106.0 | 27.9 | True | False | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 422 | C | Guard | guard_mirkwood | 38.3 | 27.9 | 145.0 | 30.2 | True | False | Defensive Troops | mirkwood | 16.0 | special_or_unlinked |
| 423 | C | [Gondor] Lond-Galen Pavise Guard | gondor_lg_pavise_guard | 38.2 | 41.5 | 157.0 | 48.9 | True | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 424 | C | [Gondor] Lond-Galen Haven Guard | gondor_lg_haven_guard | 38.2 | 41.5 | 157.0 | 48.9 | True | False | Ranged Troops | gondor | 41.0 | main_or_minor_line |
| 425 | C | [Dunland] Blaidd-lûth Noble Son | dunland_noble_son | 38.0 | 27.3 | 107.0 | 32.9 | True | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 426 | C | [Dunland] Turch-lûth Noble Son | dunland_boar_noble_son | 38.0 | 27.3 | 107.0 | 32.9 | True | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 427 | C | Rhun Veteran Caravan Guard | veteran_caravan_guard_rhun | 38.0 | 28.6 | 141.0 | 33.4 | True | False | Defensive Troops | khuzait | 21.0 | special_or_unlinked |
| 428 | C | [Gondor] Ringlo Vale Militia | gondor_ring_militia | 37.9 | 27.4 | 86.0 | 28.0 | True | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 429 | C | [Harad] Spear Guard | harad_spearguard | 37.9 | 28.4 | 121.0 | 33.1 | True | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 430 | C | [Harad] Footman | harad_footman | 37.9 | 28.4 | 121.0 | 33.1 | True | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 431 | C | [Rhûn] Easterling Swordsman | easterling_swordsman_new | 37.8 | 28.3 | 131.0 | 33.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 432 | C | [Rhûn] Far-Rhun Footman | far_rhun_footman | 37.8 | 28.3 | 131.0 | 33.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 433 | C | [Rhûn] Balcoth Axeman | balcoth_axeman | 37.8 | 28.3 | 131.0 | 33.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 434 | C | [Gondor] Citadel Guard Trainee | gondor_mt_trainee | 37.8 | 28.3 | 98.0 | 32.0 | True | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 435 | C | Guard | guard_mistymountainorcs | 37.6 | 27.0 | 100.0 | 29.0 | True | False | Defensive Troops | mistymountainorcs | 16.0 | special_or_unlinked |
| 436 | C | Guard | guard_goblin | 37.6 | 27.0 | 100.0 | 29.0 | True | False | Defensive Troops | goblin | 16.0 | special_or_unlinked |
| 437 | C | [Rhûn] Sagarûn Watchman | sagarun_watchman | 37.6 | 27.6 | 117.5 | 31.8 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 438 | C | [Rohan] Edoras Militia | rohan_edoras_militia | 37.6 | 26.9 | 83.0 | 22.8 | True | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 439 | C | [Rohan] West-March Guardsman | rohan_westmarches_guardsman | 37.4 | 26.7 | 79.0 | 22.6 | True | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 440 | C | [Gondor] Lossarnach Noble | gondor_loss_noble | 37.3 | 28.1 | 100.0 | 29.0 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 441 | C | [Gondor] Lossarnach Axebearer | gondor_loss_axebearer | 36.8 | 27.4 | 86.0 | 28.0 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 442 | C | [Rohan] Edoras Recruit | rohan_edoras_recruit | 36.8 | 25.8 | 64.4 | 21.2 | True | False | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 443 | C | Guard | guard_erebor | 36.8 | 27.4 | 136.0 | 34.1 | True | False | Defensive Troops | erebor | 16.0 | special_or_unlinked |
| 444 | C | [Umbar] Auxiliary Recruit | aux_basic | 36.7 | 21.2 | 68.6 | 22.2 | True | False | Skirmishers | umbar | 6.0 | special_or_unlinked |
| 445 | C | [Rohan] Westfold Militiaman | rohan_westfold_militiaman | 36.3 | 26.7 | 79.0 | 22.6 | True | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 446 | C | [Dale] Lake-Town Peasant | dale_recruit | 36.2 | 25.2 | 40.0 | 14.9 | True | False | Defensive Troops | sturgia | 6.0 | main_or_minor_line |
| 447 | C | Rhun Caravan Guard | caravan_guard_rhun | 36.2 | 26.2 | 137.0 | 29.9 | True | False | Defensive Troops | khuzait | 16.0 | special_or_unlinked |
| 448 | C | [Dol Guldur] Orc Warrior | dg_orc_warrior | 36.0 | 24.2 | 131.0 | 24.8 | True | False | Defensive Troops | dolguldur | 16.0 | main_or_minor_line |
| 449 | C | [Gondor] Osgiliath Veteran | gondor_osg_veteran | 36.0 | 26.0 | 86.0 | 25.8 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 450 | C | [Rhûn] Loke-Rim Initiate | loke_rim_initiate | 35.8 | 26.6 | 124.0 | 30.4 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 451 | C | [Rhûn] Dragon-Wrath Acolyte | dragon_wrath_acolyte | 35.8 | 26.6 | 124.0 | 30.4 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 452 | C | [Harad] Sword Fighter | harad_swordfighter | 35.8 | 25.7 | 111.0 | 29.1 | True | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 453 | C | [Harad] Spear Fighter | harad_spearfighter | 35.8 | 25.7 | 111.0 | 29.1 | True | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 454 | C | [Mordor] Nurn Warg Rider | mordor_warg_rider | 35.7 | 26.0 | 85.0 | 29.8 | True | False | Defensive Troops | mordor | 6.0 | main_or_minor_line |
| 455 | C | [Mordor] Black Uruk Fighter | mordor_uruk_fighter | 35.6 | 25.4 | 110.0 | 28.9 | True | False | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 456 | C | [Mordor] Black Uruk Grunt | mordor_uruk_grunt | 35.6 | 17.7 | 100.2 | 25.6 | True | False | Defensive Troops | mordor | 11.0 | main_or_minor_line |
| 457 | C | Dol Guldur Militia Veteran Spearman | dolguldur_militia_veteran_spearman | 35.4 | 20.6 | 117.5 | 22.2 | True | False | Defensive Troops | dolguldur | 16.0 | special_or_unlinked |
| 458 | C | [Rohan] Militia Spearman | rohan_militia_spearman | 35.1 | 22.8 | 48.7 | 16.8 | True | False | Defensive Troops | vlandia | 11.0 | special_or_unlinked |
| 459 | C | Isengard Veteran Caravan Guard | veteran_caravan_guard_isengard | 35.0 | 23.9 | 98.0 | 22.0 | True | False | Defensive Troops | isengard | 21.0 | special_or_unlinked |
| 460 | C | Guard | guard_isengard | 35.0 | 23.9 | 99.0 | 22.1 | True | False | Defensive Troops | isengard | 16.0 | special_or_unlinked |
| 461 | C | [Isengard] Militia Veteran Spearman | isengard_militia_veteran_spearman | 34.9 | 16.9 | 82.0 | 18.4 | True | False | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 462 | C | Guard | guard_dolguldur | 34.7 | 23.2 | 125.0 | 23.2 | True | False | Defensive Troops | dolguldur | 16.0 | special_or_unlinked |
| 463 | C | [Gondor] Belfalas Footman | gondor_bel_footman | 34.5 | 24.0 | 74.0 | 23.0 | True | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 464 | C | Isengard Caravan Guard | caravan_guard_isengard | 34.1 | 23.1 | 92.5 | 20.8 | True | False | Defensive Troops | isengard | 16.0 | special_or_unlinked |
| 465 | C | [Isengard] Orc Brawler | isengard_orc_brawler | 34.0 | 23.3 | 65.0 | 21.1 | True | False | Defensive Troops | isengard | 6.0 | main_or_minor_line |
| 466 | C | [Rhûn] Wain Footman | wain_footman | 33.8 | 22.1 | 107.0 | 27.0 | True | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 467 | C | [Rhûn] Militia Spearman | rhun_militia_spearman | 33.8 | 21.9 | 91.0 | 23.4 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 468 | C | Guard | guard_gundabad | 33.7 | 22.0 | 100.0 | 21.5 | True | False | Defensive Troops | gundabad | 16.0 | special_or_unlinked |
| 469 | C | [Rhûn] Militia Veteran Spearman | rhun_militia_veteran_spearman | 33.5 | 21.7 | 97.0 | 23.1 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 470 | C | [Rhûn] Sagarûn Deckhand | sagarun_deckhand | 33.3 | 21.9 | 92.5 | 23.5 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 471 | C | [Gundabad] Despoiler of the Vale | gundabad_despoiler_of_the_vale | 33.2 | 30.9 | 180.0 | 46.0 | False | True | Ranged Troops | gundabad | 26.0 | main_or_minor_line |
| 472 | C | Guard | guard_mordor | 33.2 | 21.5 | 97.0 | 21.9 | True | False | Defensive Troops | mordor | 16.0 | special_or_unlinked |
| 473 | C | Guard | guard_gondor | 33.1 | 22.2 | 78.0 | 20.2 | True | False | Defensive Troops | gondor | 16.0 | special_or_unlinked |
| 474 | C | [Mordor] Nurn Warg Ravager | mordor_warg_ravager | 32.9 | 29.3 | 138.0 | 43.5 | False | True | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 475 | C | [Mordor] Nurn Beast Master | mordor_warg_beastmaster | 32.9 | 29.3 | 138.0 | 43.5 | False | True | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 476 | C | [Dunland] Hebog-lûth Scout | dunland_falcon_archer | 32.9 | 30.6 | 96.0 | 31.4 | False | True | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 477 | C | [Dunland] Militia Veteran Spearman | dunland_militia_veteran_spearman | 32.8 | 19.1 | 68.3 | 19.5 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 478 | C | [Rhûn] Easterling Militia | easterling_militia | 32.8 | 21.7 | 90.0 | 23.2 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 479 | C | [Rhûn] Balcoth Volunteer | balcoth_volunteer | 32.8 | 21.7 | 90.0 | 23.2 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 480 | C | [Rhûn] Far-Rhun Levy | far_rhun_levy | 32.6 | 21.5 | 96.0 | 22.9 | True | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 481 | C | [Rhûn] Balcoth Footman | balcoth_footman | 32.5 | 21.4 | 95.0 | 22.8 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 482 | C | [Rhûn] Easterling Footman | easterling_footman_new | 32.5 | 21.4 | 95.0 | 22.8 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 483 | C | [Mordor] Orc Fighter | mordor_orc_fighter | 32.5 | 21.4 | 74.0 | 23.0 | True | False | Defensive Troops | mordor | 11.0 | main_or_minor_line |
| 484 | C | [Gondor] Lossarnach Woodsman | gondor_loss_woodsman | 32.3 | 21.5 | 64.0 | 19.2 | True | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 485 | C | [Rohan] West-March Recruit | rohan_westmarches_recruit | 32.1 | 19.9 | 31.0 | 12.5 | True | False | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 486 | C | [Mordor] Morannon Fighter | morannon_fighter | 31.6 | 20.2 | 65.0 | 21.1 | True | False | Defensive Troops | mordor | 11.0 | main_or_minor_line |
| 487 | C | [Mordor] Morannon Recruit | morannon_recruit | 31.6 | 20.2 | 65.0 | 21.1 | True | False | Defensive Troops | mordor | 7.0 | main_or_minor_line |
| 488 | C | Dol Guldur Militia Spearman | dolguldur_militia_spearman | 31.3 | 16.2 | 75.0 | 15.8 | True | False | Defensive Troops | dolguldur | 11.0 | special_or_unlinked |
| 489 | C | [Gondor] Harondor Conscript | gondor_har_conscript | 31.2 | 19.8 | 47.0 | 16.6 | True | False | Defensive Troops | gondor | 6.0 | main_or_minor_line |
| 490 | C | [Goblin] Militia Spearman | goblin_militia_spearman | 31.2 | 15.8 | 39.5 | 15.1 | True | False | Defensive Troops | goblin | 11.0 | special_or_unlinked |
| 491 | C | [Misty Mountains] Militia Spearman | mistymountainorcs_militia_spearman | 31.2 | 15.8 | 39.5 | 15.1 | True | False | Defensive Troops | mistymountainorcs | 11.0 | special_or_unlinked |
| 492 | C | [Isengard] Militia Spearman | isengard_militia_spearman | 31.1 | 18.2 | 82.0 | 18.1 | True | False | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 493 | C | [Rohan] Westfold Recruit | rohan_westfold_recruit | 31.0 | 19.9 | 31.0 | 12.5 | True | False | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 494 | C | [Gundabad] Militia Spearman | gundabad_militia_spearman | 30.8 | 15.2 | 67.5 | 14.2 | True | False | Defensive Troops | gundabad | 11.0 | special_or_unlinked |
| 495 | C | [Erebor] Militia Spearman | erebor_militia_spearman | 30.8 | 13.8 | 52.0 | 15.2 | True | False | Defensive Troops | erebor | 11.0 | special_or_unlinked |
| 496 | C | [Gondor] Anórien Militia | gondor_ano_militia | 30.7 | 19.1 | 64.0 | 19.2 | True | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 497 | C | [Harad] Militia Veteran Spearman | harad_militia_veteran_spearman | 30.6 | 17.8 | 71.0 | 17.4 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 498 | C | [Harad] Militia Spearman | harad_militia_spearman | 30.6 | 17.0 | 62.0 | 16.1 | True | False | Defensive Troops | aserai | 11.0 | special_or_unlinked |
| 499 | C | [Gondor] Ringlo Vale Peasant | gondor_ring_peasant | 30.5 | 17.7 | 32.0 | 13.6 | True | False | Defensive Troops | gondor | 6.0 | main_or_minor_line |
| 500 | C | [Erebor] Miner | erebor_reg_miner | 30.5 | 13.9 | 58.8 | 16.7 | True | False | Defensive Troops | erebor | 11.0 | main_or_minor_line |
| 501 | C | [Erebor] Militia | erebor_reg_militia | 30.5 | 14.9 | 58.4 | 16.8 | True | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 502 | C | [Rhûn] Wain Youngblood | wain_youngblood | 30.3 | 17.4 | 74.0 | 20.0 | True | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 503 | C | [Gondor] Lebennin Skirmisher | gondor_leb_skirmisher | 30.1 | 18.3 | 40.0 | 14.4 | True | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 504 | C | Harad Caravan Guard | caravan_guard_harad | 29.8 | 17.8 | 71.0 | 17.4 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 505 | C | Harad Veteran Caravan Guard | veteran_caravan_guard_harad | 29.8 | 17.8 | 71.0 | 17.4 | True | False | Defensive Troops | aserai | 21.0 | special_or_unlinked |
| 506 | C | [Harad] Militia | harad_militia | 29.8 | 17.8 | 71.0 | 17.4 | True | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 507 | C | [Harad] Levy | harad_levy | 29.8 | 17.8 | 71.0 | 17.4 | True | False | Defensive Troops | aserai | 6.0 | main_or_minor_line |
| 508 | C | Guard | guard_harad | 29.8 | 17.8 | 71.0 | 17.4 | True | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 509 | C | Mordor Militia Spearman | mordor_militia_spearman | 29.7 | 14.5 | 57.5 | 14.8 | True | False | Defensive Troops | mordor | 11.0 | special_or_unlinked |
| 510 | C | [Gondor] Lossarnach Lumberman | gondor_loss_lumberman | 29.4 | 17.7 | 32.0 | 13.6 | True | False | Defensive Troops | gondor | 6.0 | main_or_minor_line |
| 511 | C | [Dunland] Militia Spearman | dunland_militia_spearman | 29.2 | 12.6 | 31.7 | 11.0 | True | False | Defensive Troops | empire | 11.0 | special_or_unlinked |
| 512 | C | [Mordor] Orc Lackey | mordor_orc_lackey | 28.9 | 17.2 | 47.0 | 16.6 | True | False | Defensive Troops | mordor | 6.0 | main_or_minor_line |
| 513 | C | [Umbar] Adûnaim Recruits | umbar_elite | 28.9 | 13.8 | 46.4 | 12.6 | True | False | Skirmishers | umbar | 11.0 | main_or_minor_line |
| 514 | C | [Mordor] Nurn Warg Reaver | mordor_warg_reaver | 28.5 | 23.4 | 114.0 | 34.8 | False | True | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 515 | C | [Gundabad] Scout | gundabad_scout | 28.3 | 21.9 | 152.0 | 32.5 | False | True | Ranged Troops | gundabad | 21.0 | main_or_minor_line |
| 516 | C | [Gondor] Anórien Peasant | gondor_ano_peasant | 27.8 | 15.3 | 32.0 | 13.6 | True | False | Defensive Troops | gondor | 6.0 | main_or_minor_line |
| 517 | C | Guard | guard_dunland | 27.4 | 15.2 | 57.0 | 14.8 | True | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 518 | C | [Isengard] Uruk-Hai Recruit | urukhai_recruit | 27.1 | 14.3 | 42.0 | 7.8 | True | False | Defensive Troops | isengard | 6.0 | main_or_minor_line |
| 519 | C | [Rhûn] Easterling Recruit | easterling_recruit | 27.0 | 14.2 | 51.0 | 12.1 | True | False | Defensive Troops | khuzait | 6.0 | main_or_minor_line |
| 520 | C | Spider Rider | taom_spider_creature | 20.6 | 14.3 | 60.0 | 12.8 | False | True | Defensive Troops | dolguldur | 20.0 | special_or_unlinked |
| 521 | C | [Mordor] Nurn Warg Raider | mordor_warg_raider | 20.6 | 14.2 | 65.0 | 21.1 | False | True | Defensive Troops | mordor | 11.0 | main_or_minor_line |
| 522 | C | [Dol Guldur] Warg Tracker | dg_warg_scout | 20.0 | 13.5 | 120.0 | 20.0 | False | True | Defensive Troops | dolguldur | 16.0 | main_or_minor_line |
| 523 | D | Orc Rider Officer | mp_orc_rider_isengard_hero | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | empire | 20.0 | special_or_unlinked |
| 524 | D | Orc Rider | mp_orc_rider_isengard_troop | 0.0 | 0.0 | 0.0 | 0.0 | False | True | Defensive Troops | empire | 15.0 | special_or_unlinked |


## Ranked — Offensive melee (812 troops)

| rank | tier | troop_name | troop_id | offensive_melee_role_score | crafted_melee_score_base | crafted_melee_template | crafted_melee_item | defense_score_base | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rivendell] Imladris Horse Archer | imladris_horse_archer | 100.0 | 100.0 | TwoHandedSword | he_sword | 61.8 | True | Ranged Troops | rivendell | 41.0 | main_or_minor_line |
| 2 | S | [Gondor] Arndir Hill-Knight | gondor_arn_hill_knight | 97.8 | 100.0 | TwoHandedSword | numenorean_sword_2h_l | 45.4 | True | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 3 | S | [Gondor] Arndir Knight | gondor_arn_knight | 97.8 | 100.0 | TwoHandedSword | numenorean_sword_2h_f | 45.4 | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 4 | S | [Gondor] Arndir Veteran Knight | gondor_arn_vet_knight | 97.8 | 100.0 | TwoHandedSword | numenorean_sword_2h_i | 45.4 | True | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 5 | S | [Rivendell] Imladris Blademaster | imladris_blademaster | 93.8 | 100.0 | TwoHandedSword | he_sword | 48.7 | False | Offensive Melee | rivendell | 41.0 | main_or_minor_line |
| 6 | S | [Rivendell] Imladris Marchwarden | imladris_marchwarden | 92.6 | 100.0 | TwoHandedSword | he_sword | 44.0 | False | Ranged Troops | rivendell | 41.0 | main_or_minor_line |
| 7 | S | [Isengard] Uruk-Hai Nazg-hai | urukhai_nazg_hai | 92.4 | 100.0 | TwoHandedSword | isengard_berserker_sword_2h | 43.2 | False | Offensive Melee | isengard | 36.0 | main_or_minor_line |
| 8 | S | [Mordor] Black Uruk Captain | mordor_uruk_captain | 92.2 | 100.0 | OneHandedSword|TwoHandedSword | isengard_berserker_sword_2h|sm_uruk_sword_a|sm_uruk_sword_b|sm_uruk_sword_i | 41.7 | False | Defensive Troops | mordor | 36.0 | main_or_minor_line |
| 9 | S | [Gondor] Dol Amroth Swan Guard | gondor_da_swan_guard | 92.0 | 100.0 | TwoHandedPolearm|TwoHandedSword | numenorean_sword_2h_b|wm_gondor_gondorknight_spearb|wm_gondor_pg_spearb | 39.9 | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 10 | S | [Gondor] Dol Amroth Foot Knight | gondor_da_foot_knight | 92.0 | 100.0 | TwoHandedPolearm|TwoHandedSword | numenorean_sword_2h_a|wm_gondor_gondorknight_spearb|wm_gondor_pg_spearb | 39.9 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 11 | S | [Rivendell] Megil-Aran Elenath | rivendell_gondolin_battlemaster | 91.3 | 100.0 | OneHandedSword|TwoHandedSword | wm_gf_knight_broadsword|wm_gf_knight_longsword | 44.2 | False | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 12 | S | [Gondor] Ithil Guard Captain | gondor_ith_captain | 91.2 | 100.0 | OneHandedSword|TwoHandedPolearm|TwoHandedSword | wm_gondor_lamedon_2h_sword_e|wm_gondor_swanknight_speara|wm_gondor_sword_a10 | 35.7 | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 13 | S | [Gondor] Calembel Heavy Swordsman | gondor_cal_heavy_swordsman | 91.1 | 100.0 | TwoHandedSword | wm_gondor_lamedon_2h_sword_b | 32.9 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 14 | S | [Gondor] Calembel Sergeant | gondor_cal_sergeant | 91.1 | 100.0 | TwoHandedSword | wm_gondor_lamedon_2h_sword_c | 32.9 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 15 | S | [Gondor] Calembel Vale-Knight | gondor_cal_vale_knight | 91.1 | 100.0 | TwoHandedSword | wm_gondor_lamedon_2h_sword_c | 32.9 | False | Offensive Melee | gondor | 41.0 | main_or_minor_line |
| 16 | S | [Gondor] Ithil Guard Sergeant | gondor_ith_sergeant | 90.5 | 100.0 | OneHandedSword|TwoHandedPolearm|TwoHandedSword | wm_gondor_lamedon_2h_sword_e|wm_gondor_swanknight_speara|wm_gondor_sword_a08 | 30.8 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 17 | A | [Mordor] Black Uruk Vanguard | mordor_uruk_vanguard | 89.5 | 100.0 | OneHandedSword|TwoHandedSword | isengard_berserker_sword_2h|sm_uruk_sword_a | 40.8 | False | Defensive Troops | mordor | 31.0 | main_or_minor_line |
| 18 | A | [Isengard] Uruk-Hai Berserker | urukhai_berserker | 88.7 | 100.0 | TwoHandedSword | isengard_berserker_sword_2h | 23.6 | False | Offensive Melee | isengard | 31.0 | main_or_minor_line |
| 19 | A | [Rivendell] Nõldorin Lancer | noldorin_lancer | 86.2 | 82.0 | TwoHandedPolearm | he_spear | 92.1 | True | Defensive Troops | rivendell | 46.0 | main_or_minor_line |
| 20 | A | [Gondor] Lamedon Hill-Warden | gondor_lam_hill_warden | 86.0 | 100.0 | TwoHandedSword | wm_gondor_lamedon_2h_sword_d | 34.0 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 21 | A | [Rivendell] Noble | rivendell_noble | 85.0 | 82.0 | TwoHandedPolearm | he_spear | 81.6 | True | Defensive Troops | rivendell | 36.0 | main_or_minor_line |
| 22 | A | [Rivendell] High Captain | rivendell_high_captain | 84.8 | 82.0 | TwoHandedPolearm | he_spear | 86.3 | True | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 23 | A | [Rivendell] Royal Guard | rivendell_royal_guard | 84.8 | 82.0 | TwoHandedPolearm | he_spear | 87.7 | True | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 24 | A | [Gondor] Ithil Guard Veteran | gondor_ith_veteran | 84.6 | 100.0 | OneHandedSword|TwoHandedPolearm|TwoHandedSword | wm_gondor_lamedon_2h_sword_e|wm_gondor_swanknight_speara|wm_gondor_sword_a08 | 26.1 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 25 | A | [Rivendell] Royal Knight | rivendell_royal_knight | 84.1 | 82.0 | TwoHandedPolearm | he_spear | 82.0 | True | Defensive Troops | rivendell | 46.0 | main_or_minor_line |
| 26 | A | [Rivendell] Imladris Marksman | imladris_marksman | 83.8 | 100.0 | TwoHandedSword | he_sword | 44.1 | False | Ranged Troops | rivendell | 36.0 | main_or_minor_line |
| 27 | A | [Mirkwood] Mirkwood Róchenlas | mirkwood_rochenlas | 83.4 | 82.0 | TwoHandedPolearm | mirkwood_spear_a02 | 78.0 | True | Defensive Troops | mirkwood | 41.0 | main_or_minor_line |
| 28 | A | [Mirkwood] Mirkwood Béleglas | mirkwood_beleglas | 83.4 | 82.0 | TwoHandedPolearm | mirkwood_spear_a02 | 78.0 | True | Defensive Troops | mirkwood | 46.0 | main_or_minor_line |
| 29 | A | [Dol Guldur] Khamûl's Shadow-Knight | dg_khamul_shadow_knight | 83.4 | 82.0 | TwoHandedPolearm | sm_dg_khml_spear_a | 76.4 | True | Defensive Troops | dolguldur | 46.0 | main_or_minor_line |
| 30 | A | [Rivendell] Imladris Outrider | imladris_outrider | 83.2 | 82.0 | TwoHandedPolearm | he_spear | 75.6 | True | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 31 | A | [Rivendell] Rochannon Elenath | rivendell_glorfindel_guard | 83.0 | 82.0 | TwoHandedPolearm | wm_gf_knight_spear | 74.6 | True | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 32 | A | [Rhûn] Loke-Rim Gilded Kataphract | loke_rim_gilded_cataphract | 83.0 | 82.0 | TwoHandedPolearm | sm_rh_loke_spear_a | 73.0 | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 33 | A | [Rhûn] Dragon-Wrath Obsidian Knight | dragon_wrath_obsidian_knight | 82.9 | 82.0 | TwoHandedPolearm | sm_rh_drag_spear_a | 73.0 | True | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 34 | A | [Dale] Dalian King's Guard | dale_kings_guard | 82.7 | 82.0 | TwoHandedPolearm | dale_winged_spear_b | 72.2 | True | Defensive Troops | sturgia | 31.0 | main_or_minor_line |
| 35 | A | [Rhûn] Darkhûn Cultist Knight | darkhun_cultist_knight | 82.5 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 70.7 | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 36 | A | [Rohan] Riders of Rohan | rohan_edoras_golden_hall_supreme_rider | 82.4 | 82.0 | TwoHandedPolearm | wm_rohan_spear_b|wm_rohan_spear_f|wm_rohan_ws_spear_a01 | 67.9 | True | Skirmishers | vlandia | 41.0 | main_or_minor_line |
| 37 | A | [Rhûn] Wainrider Warlord Chariot | wainrider_warlord_chariot | 82.4 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 69.7 | True | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 38 | A | [Rohan] West Emnet Heavy Shock Cavalry | rohan_westemnet_kings_own_rider | 82.2 | 82.0 | TwoHandedPolearm | wm_rohan_spear_a | 68.4 | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 39 | A | [ARhûn] Wainrider Swift-Chariot | wainrider_swift_chariot | 82.2 | 82.0 | TwoHandedPolearm | khuzait_lance_3_t5 | 68.1 | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 40 | A | [Dol Guldur] Khamûl's Veiled Knight | dg_khamul_veiled_knight | 82.1 | 82.0 | TwoHandedPolearm | sm_dg_khml_spear_a | 66.5 | True | Defensive Troops | dolguldur | 41.0 | main_or_minor_line |
| 41 | A | [Rhûn] Dragon-Wrath Lancer | dragon_wrath_lancer | 81.9 | 82.0 | TwoHandedPolearm | sm_rh_drag_spear_a | 65.6 | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 42 | A | [Rhûn] Darkhûn Knight | darkhun_knight | 81.8 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 65.1 | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 43 | A | [Dunland] Caru-lûth Noble Lancer | dunland_stag_noble_lancer | 81.7 | 82.0 | TwoHandedPolearm | vlandia_lance_2_t4 | 64.3 | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 44 | A | [Rohan] East Emnet King's Lancer | rohan_eastemnet_kings_own_lancer | 81.6 | 82.0 | TwoHandedPolearm | wm_rohan_spear_f | 63.9 | True | Defensive Troops | vlandia | 36.0 | main_or_minor_line |
| 45 | A | [Rohan] King's Royal Guard | rohan_edoras_golden_hall_kings_own_rider | 81.5 | 82.0 | TwoHandedPolearm | wm_rohan_spear_d|wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 62.5 | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 46 | A | [Rohan] King's Knight | rohan_edoras_golden_hall_eorlingas_rider | 81.4 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 60.5 | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 47 | A | [Rhûn] Far-Rhun Iron Kataphract | far_rhun_iron_cataphract | 81.3 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 61.5 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 48 | A | [Rhûn] Kharaghûl Ashkur Nokor | kharaghul_ashkur_nokor | 81.3 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 61.4 | True | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 49 | A | [Rhûn] Wainrider Khan's Chosen | wainrider_khans_chosen | 81.2 | 82.0 | TwoHandedPolearm | wm_harad_glaive_a01 | 60.3 | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 50 | A | [Rhûn] Kharaghûl Nokor | kharaghul_nokor | 81.1 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 59.8 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 51 | A | [Rohan] East Emnet Royal Lancer | rohan_eastemnet_royal_lancer | 81.0 | 82.0 | TwoHandedPolearm | wm_rohan_spear_c | 59.0 | True | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 52 | A | [Rohan] West Emnet Shock Cavalry | rohan_westemnet_royal_rider | 81.0 | 82.0 | TwoHandedPolearm | wm_rohan_spear_b | 59.0 | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 53 | A | [Rhûn] Loke-Rim Kataphract | loke_rim_cataphract | 80.8 | 82.0 | TwoHandedPolearm | sm_rh_loke_spear_a | 57.0 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 54 | A | [Rhûn] Dragon-Wrath Ash Knight | dragon_wrath_ash_knight | 80.8 | 82.0 | TwoHandedPolearm | sm_rh_drag_spear_a | 57.0 | True | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 55 | A | [Rhûn] Wainrider Cavalry | wainrider_cavalry | 80.6 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 55.7 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 56 | A | [Gondor] Swan Knight | gondor_da_swan_knight | 80.6 | 82.0 | TwoHandedPolearm | wm_gondor_gondorknight_spearb|wm_swan_knight_lance_b | 55.6 | True | Defensive Troops | gondor | 46.0 | main_or_minor_line |
| 57 | A | [Gondor] Dol Amroth Veteran Knight | gondor_da_vet_knight | 80.5 | 82.0 | TwoHandedPolearm | wm_gondor_swanknight_speara | 54.9 | True | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 58 | A | [Gondor] Dol Amroth Knight | gondor_da_knight | 80.4 | 82.0 | TwoHandedPolearm | wm_gondor_swanknight_speara | 54.4 | True | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 59 | A | [Gondor] Dol Amroth Cavalry | gondor_da_cavalry | 80.4 | 82.0 | TwoHandedPolearm | wm_gondor_swanknight_spearb | 54.4 | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 60 | A | [Rhûn] Darkhûn Veteran Cavalry | darkhun_veteran_cavalry | 80.4 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 54.0 | True | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 61 | A | [Gundabad] Azog's Defiler | gundabad_dread_rider_of_the_tower | 80.0 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a01 | 48.1 | True | Defensive Troops | gundabad | 41.0 | main_or_minor_line |
| 62 | A | [Gondor] Pinnath Gelin Veteran Horseman | gondor_pg_vet_cavalry | 80.0 | 82.0 | TwoHandedPolearm | wm_gondor_pg_spearb | 50.8 | True | Skirmishers | gondor | 31.0 | main_or_minor_line |
| 63 | A | [Gondor] Anórien Knight | gondor_ano_mt_knight | 79.9 | 82.0 | TwoHandedPolearm | wm_gondor_gondorknight_spearb | 50.0 | True | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 64 | A | [Dol Guldur] Fell Ravager | dg_fell_warg_rider | 79.8 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a01 | 49.4 | True | Defensive Troops | dolguldur | 36.0 | main_or_minor_line |
| 65 | A | [Aharad] Elephant Rider | harad_elephant_rider | 79.7 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 48.5 | True | Defensive Troops | aserai | 51.0 | special_or_unlinked |
| 66 | A | [AMordor] Armored Troll | cave_troll | 79.4 | 82.0 | Mace|TwoHandedMace|TwoHandedPolearm | wm_cave_troll_1h_mace_a|wm_cave_troll_1h_mace_b|wm_cave_troll_1h_mace_c|wm_cave_troll_2h_mace_a|wm_cave_troll_spear_a | 73.0 | False | Defensive Troops | mordor | 51.0 | special_or_unlinked |
| 67 | A | [Umbar] Naru n'Aru Royal Knights | umbar_elite_root0001 | 79.2 | 82.0 | TwoHandedAxe|TwoHandedPolearm | peasant_2haxe_1_t1|wm_gondor_spear_a | 42.6 | True | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 68 | A | [Gundabad] Pale Uruk Fang Rider | gundabad_tracker | 79.1 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a01|wm_gundabad_spear_a03 | 37.8 | True | Defensive Troops | gundabad | 36.0 | main_or_minor_line |
| 69 | A | [Aharad] Mumakil Rider | harad_mumakil_rider | 78.4 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 38.9 | True | Defensive Troops | aserai | 51.0 | special_or_unlinked |
| 70 | A | [Gundabad] Pale Uruk Wolf Rider | gundabad_warg_tamer | 78.4 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a02|wm_gundabad_spear_a03 | 32.0 | True | Defensive Troops | gundabad | 31.0 | main_or_minor_line |
| 71 | A | [Rivendell] Imladris Warden | imladris_warden | 77.2 | 82.0 | TwoHandedPolearm | wm_rivendell_spear_a01 | 67.0 | False | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 72 | A | [Harad] Fang of the King | harad_fangking | 77.2 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 50.1 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 73 | A | [Erebor] Gate Warden | erebor_noble_gate_warden | 76.7 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 59.5 | False | Defensive Troops | erebor | 41.0 | main_or_minor_line |
| 74 | A | [Rivendell] Rider of Himring | rider_of_himring | 76.6 | 75.7 | OneHandedSword | wm_rivendell_sword_a01_silver|wm_rivendell_sword_a02_silver | 70.1 | True | Ranged Troops | rivendell | 46.0 | main_or_minor_line |
| 75 | A | [Erebor] Royal Warden | erebor_noble_royal_warden | 76.2 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 60.2 | False | Defensive Troops | erebor | 46.0 | main_or_minor_line |
| 76 | A | [Gondor] Arndir Cavalry | gondor_arn_cavalry | 76.1 | 100.0 | TwoHandedSword | numenorean_sword_2h_d | 43.6 | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 77 | A | [Rhûn] Darkhûn Ironbound | darkhun_ironbound | 76.0 | 82.0 | TwoHandedPolearm | sm_dg_khml_spear_a | 59.9 | False | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 78 | A | [Rhûn] Dragon-Wrath Obsidian Shieldmaster | dragon_wrath_obsidian_shieldmaster | 76.0 | 82.0 | TwoHandedPolearm | sm_rh_drag_spear_a | 57.4 | False | Defensive Troops | khuzait | 46.0 | main_or_minor_line |
| 79 | A | [Erebor] Royal Legionary | erebor_oathsworn_royal_legionary | 75.9 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 56.6 | False | Defensive Troops | erebor | 46.0 | main_or_minor_line |
| 80 | A | [Rivendell] Imladris Guardsman | imladris_guardsman | 75.9 | 82.0 | TwoHandedPolearm | wm_rivendell_spear_a01 | 58.3 | False | Defensive Troops | rivendell | 36.0 | main_or_minor_line |
| 81 | A | [Ironpass] Mountain Guard | ironpass_mountain_guard | 75.9 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 44.8 | False | Defensive Troops | erebor | 36.0 | main_or_minor_line |
| 82 | A | [Erebor] Shield-Guard | erebor_noble_shield_guard | 75.7 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 55.1 | False | Defensive Troops | erebor | 36.0 | main_or_minor_line |
| 83 | A | [Erebor] Legionary | erebor_oathsworn_legionary | 75.7 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 55.8 | False | Defensive Troops | erebor | 41.0 | main_or_minor_line |
| 84 | A | [Rhûn] Loke-Rim Gilded Shieldguard | loke_rim_gilded_shieldguard | 75.7 | 82.0 | TwoHandedPolearm | sm_rh_loke_spear_a | 56.2 | False | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 85 | A | [Iron Hills] Gate Warden | iron_hills_noble_gate_warden | 75.5 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a | 56.0 | False | Defensive Troops | erebor | 41.0 | main_or_minor_line |
| 86 | A | [Iron Hills] Shield-Guard | iron_hills_noble_shield_guard | 75.5 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a | 55.7 | False | Defensive Troops | erebor | 36.0 | main_or_minor_line |
| 87 | A | [Erebor] Oathsworn | erebor_oathsworn | 75.4 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 54.5 | False | Defensive Troops | erebor | 36.0 | main_or_minor_line |
| 88 | A | [Iron Hills] Guard | iron_hills_noble_guard | 75.3 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a | 54.0 | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 89 | A | [Rhûn] Dragon-Wrath Infantry | dragon_wrath_infantry | 75.1 | 82.0 | TwoHandedPolearm | sm_rh_drag_spear_a | 52.2 | False | Defensive Troops | khuzait | 36.0 | main_or_minor_line |
| 90 | A | [Iron Hills] Royal Warden | iron_hills_noble_royal_warden | 75.0 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a | 51.7 | False | Defensive Troops | erebor | 46.0 | main_or_minor_line |
| 91 | A | [Rivendell] Aegedhrim Elenath | rivendell_warden_gondolin | 74.6 | 82.0 | TwoHandedPolearm | wm_gf_knight_spear | 49.0 | False | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 92 | A | [Mirkwood] Greenwood Wardens | mirkwood_wardens | 74.6 | 82.0 | TwoHandedPolearm | mirkwood_spear_a01 | 48.6 | False | Defensive Troops | mirkwood | 41.0 | main_or_minor_line |
| 93 | A | [Mirkwood] Guardians of Felegoth | mirkwood_guardians | 74.6 | 82.0 | TwoHandedPolearm | mirkwood_spear_a01 | 48.6 | False | Defensive Troops | mirkwood | 46.0 | main_or_minor_line |
| 94 | A | [Mirkwood] Palace Guard | mirkwood_palaceguard | 74.6 | 82.0 | TwoHandedPolearm | mirkwood_spear_a01 | 48.6 | False | Defensive Troops | mirkwood | 51.0 | main_or_minor_line |
| 95 | A | [Rohan] Meduseld Master Spearman | rohan_edoras_meduseld_master_spearman | 74.5 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 46.6 | False | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 96 | A | [Gondor] Serelond Coastwarden | gondor_ser_coastwarden | 74.4 | 82.0 | TwoHandedPolearm | imperial_spear_t2 | 47.5 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 97 | A | [Dale] Dalian Royal Swordsman | dale_running_river_warden | 74.4 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_sword_a|dale_winged_spear_a | 47.3 | False | Defensive Troops | sturgia | 31.0 | main_or_minor_line |
| 98 | A | [Mordor] Black Uruk Barad-Dur Guard | mordor_uruk_baraddurguard | 74.0 | 82.0 | TwoHandedPolearm | isengard_spear_a|isengard_spear_b | 43.2 | False | Defensive Troops | mordor | 36.0 | main_or_minor_line |
| 99 | A | [Rhûn] Darkhûn Guard | darkhun_guard | 74.0 | 82.0 | TwoHandedPolearm | sm_dg_khml_spear_a | 51.5 | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 100 | A | [Isengard] Uruk-Hai Pavise Guard | urukhai_pavise | 73.8 | 82.0 | TwoHandedPolearm | isengard_spear_a | 50.2 | False | Defensive Troops | isengard | 31.0 | main_or_minor_line |
| 101 | A | [Mordor] Black Uruk Shield Guard | mordor_uruk_shieldguard | 73.8 | 82.0 | TwoHandedPolearm | isengard_spear_a|isengard_spear_b | 42.1 | False | Defensive Troops | mordor | 31.0 | main_or_minor_line |
| 102 | A | [Rhûn] Wain Darkhan | wain_darkhan | 73.7 | 82.0 | TwoHandedPolearm | wm_harad_glaive_a01 | 41.6 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 103 | A | [Gondor] Ringlo Vale Spearman | gondor_ring_spearman | 73.7 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 41.5 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 104 | A | [Gondor] Methir Glaive Guard | gondor_met_glaive_guard | 73.7 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 41.5 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 105 | A | [Gondor] Linhir High Guard | gondor_lin_high_guard | 73.7 | 82.0 | TwoHandedPolearm | wm_gondor_spear_a | 41.5 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 106 | A | [Gondor] Methir Sun Knight | gondor_met_sun_knight | 73.7 | 82.0 | TwoHandedPolearm | wm_gondor_spear_a | 41.5 | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 107 | A | [Gondor] Methir Sun Warden | gondor_met_sun_warden | 73.7 | 82.0 | TwoHandedPolearm | wm_gondor_spear_a | 41.5 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 108 | A | [Gondor] Ringlo Vale Warden | gondor_ring_warden | 73.7 | 82.0 | TwoHandedPolearm | wm_gondor_spear_a | 41.5 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 109 | A | [Gondor] Pelargir Veteran Infantry | gondor_pel_vet_infantry | 73.7 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 41.5 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 110 | A | [Gondor] Pelargir Anchor Guard | gondor_pel_anchor_guard | 73.7 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 41.5 | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 111 | A | [Gondor] Linhir Veteran Spearman | gondor_lin_vet_spearman | 73.7 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 41.5 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 112 | A | [Rhûn] Dragon-Wrath Ash Shieldguard | dragon_wrath_ash_shieldguard | 73.5 | 82.0 | TwoHandedPolearm | sm_rh_drag_spear_a | 40.1 | False | Defensive Troops | khuzait | 41.0 | main_or_minor_line |
| 113 | A | [Gundabad] Pale Uruk Pike-Reaver | gundabad_veteran_spear_warrior | 73.5 | 82.0 | Pike|TwoHandedPolearm | isengard_pike_a|wm_gundabad_spear_a02 | 38.0 | False | Defensive Troops | gundabad | 31.0 | main_or_minor_line |
| 114 | A | [Dale] Lake-Town Hearthguard | dale_lake_town_hearthguard | 73.4 | 82.0 | TwoHandedPolearm | dale_halberd_a|dale_halberd_b | 39.5 | False | Offensive Melee | sturgia | 31.0 | main_or_minor_line |
| 115 | A | [Gondor] Pinnath Gelin Spearwarden | gondor_pg_spearwarden | 73.4 | 82.0 | TwoHandedPolearm | wm_gondor_pg_speara | 39.0 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 116 | A | [Ironpass] Veteran Axeman | ironpass_veteran_axeman | 73.1 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 44.8 | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 117 | A | [Misty Mountains] Orc Pike-Reaver | mistymountainorcs_veteran_spear_warrior | 73.1 | 82.0 | Pike|TwoHandedPolearm | isengard_pike_a|wm_gundabad_spear_a02 | 34.3 | False | Defensive Troops | mistymountainorcs | 31.0 | main_or_minor_line |
| 118 | A | [Rhûn] Wain Iron-Glaive | wain_iron_glaive | 73.0 | 82.0 | TwoHandedPolearm | wm_harad_glaive_a01 | 36.0 | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 119 | A | [Rhûn] Dragon-Wrath Disciple | dragon_wrath_disciple | 72.5 | 82.0 | TwoHandedPolearm | sm_rh_drag_spear_a | 39.6 | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 120 | A | [Mirkwood] Greenwood Woodsman | mirkwood_woodsman | 72.5 | 82.0 | TwoHandedPolearm | mirkwood_glaive_a01 | 32.3 | False | Offensive Melee | mirkwood | 41.0 | main_or_minor_line |
| 121 | A | [Mirkwood] Glaivesman of Amon | mirkwood_glaivesman | 72.5 | 82.0 | TwoHandedPolearm | mirkwood_glaive_a01 | 32.3 | False | Offensive Melee | mirkwood | 46.0 | main_or_minor_line |
| 122 | A | [Erebor] Guard | erebor_noble_guard | 72.4 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 49.5 | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 123 | A | [Dunland] Avanc-lûth Noble Cavalry | dunland_lizard_noble_cavalry | 71.9 | 73.3 | TwoHandedAxe | dunland_caerdh_axe_2h_d | 63.9 | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 124 | A | [Dale] Dalian Veteran Northman Scout | dale_veteran_northman_scout | 71.9 | 82.0 | TwoHandedPolearm | dale_winged_spear_b | 73.4 | True | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 125 | A | [Rivendell] Imladris Nobleman | imladris_nobleman | 71.5 | 75.7 | OneHandedSword | wm_rivendell_sword_a01|wm_rivendell_sword_a02 | 65.9 | False | Defensive Troops | rivendell | 36.0 | main_or_minor_line |
| 126 | A | [Dale] Dalian Heavy Cavalry | dale_kinsman_of_eorl | 71.1 | 82.0 | TwoHandedPolearm | dale_winged_spear_b | 67.3 | True | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 127 | A | [Rivendell] Imladris Swordguard | imladris_swordguard | 71.0 | 75.7 | OneHandedSword | wm_rivendell_sword_a01|wm_rivendell_sword_a02 | 59.8 | False | Defensive Troops | rivendell | 31.0 | main_or_minor_line |
| 128 | A | [Rivendell] Battlemaster of the First Age | battlemaster_of_the_first_age | 70.9 | 75.7 | OneHandedSword | wm_rivendell_sword_a01|wm_rivendell_sword_a02 | 69.3 | False | Defensive Troops | rivendell | 41.0 | main_or_minor_line |
| 129 | A | [Rhûn] Loke-Rim Shieldguard | loke_rim_shieldguard | 70.9 | 82.0 | TwoHandedPolearm | sm_rh_loke_spear_a | 40.1 | False | Defensive Troops | khuzait | 31.0 | main_or_minor_line |
| 130 | A | [Rivendell] Imladris Archer | imladris_archer | 70.8 | 100.0 | TwoHandedSword | he_sword | 42.1 | False | Ranged Troops | rivendell | 31.0 | main_or_minor_line |
| 131 | A | [Dunland] Hebog-lûth Noble Horse Archer | dunland_falcon_noble_horse_archer | 70.5 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 53.0 | True | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 132 | A | [Harad] Warlance | harad_warlance | 70.2 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 35.3 | False | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 133 | B | [Gondor] Lamedon Veteran Swordman | gondor_lam_vet_swordman | 69.6 | 100.0 | TwoHandedSword | wm_gondor_lamedon_2h_sword_c | 32.6 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 134 | B | [Rohan] King's Lancer | rohan_edoras_golden_hall_elite_rider | 69.6 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 52.7 | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 135 | B | [Gondor] Harondor Frontier Guard | gondor_har_frontier_guard | 69.5 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3 | 42.6 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 136 | B | [Gondor] Anfalas Veteran Infantry | gondor_anf_vet_infantry | 69.5 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 42.6 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 137 | B | [Goblin] Goblin Pike-Reaver | goblin_veteran_spear_warrior | 69.4 | 82.0 | Pike|TwoHandedPolearm | isengard_pike_a|wm_gundabad_spear_a02 | 34.3 | False | Defensive Troops | goblin | 31.0 | main_or_minor_line |
| 138 | B | [Gondor] Serelond Veteran Maceman | gondor_ser_vet_maceman | 69.4 | 82.0 | TwoHandedPolearm | imperial_spear_t2 | 41.7 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 139 | B | [Gondor] Belfalas Coastguard | gondor_bel_coastguard | 69.4 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 41.5 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 140 | B | [Gondor] Pelargir Infantry | gondor_pel_infantry | 69.4 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 41.5 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 141 | B | [Gondor] Dol Amroth Veteran Infantry | gondor_da_vet_infantry | 69.2 | 82.0 | OneHandedSword|TwoHandedPolearm | wm_gondor_pg_spearb|wm_swan_knight_sworda | 39.9 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 142 | B | [Umbar] Naru n'Aru Royal Guard | umbar_elite_root0000 | 69.2 | 82.0 | TwoHandedAxe|TwoHandedPolearm | peasant_2haxe_1_t1|wm_gondor_spear | 32.3 | False | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 143 | B | [Rohan] East Emnet Eorlingas Lancer | rohan_eastemnet_eorlingas_lancer | 69.1 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a03 | 51.8 | True | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 144 | B | [Rohan] Éothéod Horse Archer | rohan_wold_kings_own_horse_archer | 69.0 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 63.9 | True | Ranged Troops | vlandia | 36.0 | main_or_minor_line |
| 145 | B | [Gondor] Anórien Veteran Infantry | gondor_ano_vet_infantry | 68.8 | 82.0 | TwoHandedPolearm | wm_gondor_spear_a | 36.8 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 146 | B | [Isengard] Orthanc Bodyguard | orthanc_bodyguard | 68.4 | 75.7 | OneHandedSword | isengard_berserker_sword | 50.5 | False | Defensive Troops | isengard | 41.0 | main_or_minor_line |
| 147 | B | [Isengard] Orthanc Warden | orthanc_warden | 68.4 | 75.7 | OneHandedSword | isengard_berserker_sword | 50.3 | False | Defensive Troops | isengard | 36.0 | main_or_minor_line |
| 148 | B | [Isengard] Orthanc Guard | orthanc_guard | 68.0 | 75.7 | OneHandedSword | isengard_berserker_sword | 46.7 | False | Defensive Troops | isengard | 31.0 | main_or_minor_line |
| 149 | B | [Mirkwood] Silvan Borderwarden | mirkwood_borderwardens | 67.7 | 75.7 | OneHandedSword | mirkwood_sword_a01 | 45.0 | False | Ranged Troops | mirkwood | 46.0 | main_or_minor_line |
| 150 | B | [Mirkwood] Thingol's Heirs | mirkwood_thingolheir | 67.7 | 75.7 | OneHandedSword | mirkwood_sword_a01 | 45.0 | False | Ranged Troops | mirkwood | 51.0 | main_or_minor_line |
| 151 | B | [Iron Hills] Warrior | iron_hills_reg_warrior | 67.7 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a|sm_dwarf_iron_sword_b | 36.2 | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 152 | B | [Dunland] Turch-lûth Huskarl | dunland_boar_warlord | 67.7 | 82.0 | TwoHandedPolearm | dunland_caerdh_spear_c | 41.4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 153 | B | [Rivendell] Megil Mallenloth | rivendell_knight_golden_flower | 67.7 | 75.7 | OneHandedSword | wm_gf_knight_broadsword | 44.4 | False | Defensive Troops | rivendell | 51.0 | main_or_minor_line |
| 154 | B | [Rhûn] Sagarûn Marine | sagarun_marine | 67.6 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_a | 50.5 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 155 | B | [Mirkwood] Greenwood Swordsman | mirkwood_swordsman | 67.6 | 75.7 | OneHandedSword | mirkwood_sword_a01 | 43.8 | False | Defensive Troops | mirkwood | 46.0 | main_or_minor_line |
| 156 | B | [Mirkwood] Greenwood Guards | mirkwood_guards | 67.6 | 75.7 | OneHandedSword | mirkwood_sword_a01 | 43.8 | False | Defensive Troops | mirkwood | 41.0 | main_or_minor_line |
| 157 | B | [Mirkwood] Silvan Sentinels | mirkwood_sentinels | 67.5 | 75.7 | OneHandedSword | mirkwood_sword_a01 | 42.8 | False | Ranged Troops | mirkwood | 41.0 | main_or_minor_line |
| 158 | B | [Rhûn] Loke-Rim Cavalry | loke_rim_cavalry | 67.5 | 82.0 | TwoHandedPolearm | sm_rh_loke_spear_a | 64.1 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 159 | B | [Isengard] Uruk-Hai Veteran Pikeman | urukhai_veteranpikeman | 67.4 | 75.7 | OneHandedSword | isengard_1h_sword_a | 42.4 | False | Offensive Melee | isengard | 31.0 | main_or_minor_line |
| 160 | B | [Gondor] Cair Andros Warden | gondor_ca_warden | 67.3 | 75.7 | OneHandedSword | wm_gondor_sword_a09 | 41.5 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 161 | B | [Gondor] Lebennin Sea Guard | gondor_leb_sea_guard | 67.3 | 75.7 | OneHandedSword | wm_pelargir_sword_a02 | 41.5 | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 162 | B | [Gondor] Arndir Foot-Knight | gondor_arn_foot_knight | 67.3 | 75.7 | OneHandedSword | wm_gondor_sword_a09 | 41.5 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 163 | B | [Gondor] Fountain Guard | gondor_mt_fountain_guard | 67.1 | 75.7 | OneHandedSword | wm_gondor_sword_a10 | 40.2 | False | Defensive Troops | gondor | 46.0 | main_or_minor_line |
| 164 | B | [Gondor] Osgiliath Dome Guard | gondor_osg_dome_guard | 67.1 | 75.7 | OneHandedSword | wm_gondor_sword_a09 | 40.0 | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 165 | B | [Gondor] Citadel Guard Captain | gondor_mt_captain | 67.1 | 75.7 | OneHandedSword | wm_gondor_sword_a10 | 39.8 | False | Defensive Troops | gondor | 41.0 | main_or_minor_line |
| 166 | B | [Erebor] Shield-Breaker | erebor_noble_shield_breaker | 67.0 | 73.3 | TwoHandedAxe | sm_dwarf_erebor_axe_2h_a2|sm_dwarf_erebor_axe_2h_b2|sm_dwarf_erebor_axe_2h_c2|sm_dwarf_erebor_axe_2h_d2 | 55.7 | False | Defensive Troops | erebor | 41.0 | main_or_minor_line |
| 167 | B | [Gondor] Citadel Guard Sergeant | gondor_mt_sergeant | 67.0 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 39.5 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 168 | B | [Isengard] Champions of the White Hand | urukhai_veteraninfantry | 67.0 | 75.7 | OneHandedSword | isengard_1h_sword_a | 46.6 | False | Defensive Troops | isengard | 31.0 | main_or_minor_line |
| 169 | B | [Rhûn] Far-Rhun Kataphract | far_rhun_cataphract | 66.9 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 60.2 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 170 | B | [Rhûn] Kharaghûl Horse Master | kharaghul_horse_master | 66.8 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 59.3 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 171 | B | [Mirkwood] Silvan Levy | mirkwood_recruit | 66.7 | 75.7 | OneHandedSword | mirkwood_sword_a01 | 37.1 | False | Defensive Troops | mirkwood | 36.0 | main_or_minor_line |
| 172 | B | [Rhûn] Far-Rhun Iron Legionary | far_rhun_iron_legionary | 66.5 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_a | 42.9 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 173 | B | [Gondor] Cair Andros Pikewarden | gondor_ca_pikewarden | 66.2 | 75.7 | OneHandedSword | wm_gondor_sword_a09 | 32.9 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 174 | B | [Gondor] Cair Andros Pikeman | gondor_ca_pikeman | 66.2 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 32.6 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 175 | B | [Rhûn] Sagarûn Storm Forged Marine | sagarun_storm_forged_marine | 66.1 | 73.3 | OneHandedAxe | sm_rh_loke_1h_axe_a | 50.7 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 176 | B | [Rhûn] Easterling Veteran Cavalry | easterling_veteran_cavalry | 65.9 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 52.7 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 177 | B | [Erebor] Veteran Axe-Guard | erebor_noble_veteran_axe_guard | 65.8 | 73.3 | TwoHandedAxe | sm_dwarf_erebor_axe_2h_b|sm_dwarf_erebor_axe_2h_c|sm_dwarf_erebor_axe_2h_d | 46.7 | False | Offensive Melee | erebor | 36.0 | main_or_minor_line |
| 178 | B | [Dol Guldur] Warg Ravager | dg_warg_skirmisher | 65.6 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a01 | 42.5 | True | Defensive Troops | dolguldur | 26.0 | main_or_minor_line |
| 179 | B | [Gondor] Lossarnach Noble Captain | gondor_loss_noble_captain | 65.6 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_silver_full_a | 47.3 | False | Defensive Troops | gondor | 36.0 | main_or_minor_line |
| 180 | B | [Rohan] Edoras Master Swordsman | rohan_edoras_master_swordsman | 65.5 | 75.7 | OneHandedSword | wm_rohan_ws_sword_a02|wm_rohan_ws_sword_a03 | 46.7 | False | Defensive Troops | vlandia | 31.0 | main_or_minor_line |
| 181 | B | [Gondor] Moon Guard | gondor_ith_moon_guard | 65.3 | 75.7 | OneHandedSword | wm_gondor_sword_a09 | 33.4 | False | Ranged Troops | gondor | 46.0 | main_or_minor_line |
| 182 | B | [Rhûn] Darkhûn Cavalry | darkhun_cavalry | 65.3 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 47.8 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 183 | B | [Dol Guldur] Uruk Black Slayer | dg_uruk_black_slayer | 64.9 | 73.3 | TwoHandedAxe | wm_dol_goldur_axe_a01 | 41.7 | False | Offensive Melee | dolguldur | 31.0 | main_or_minor_line |
| 184 | B | [Gundabad] Pale Uruk Infantry | gundabad_veteran_sword_warrior | 64.8 | 75.7 | OneHandedSword | wm_gundabad_sword_a02 | 41.4 | False | Defensive Troops | gundabad | 31.0 | main_or_minor_line |
| 185 | B | [Gondor] Ithilien Ranger | gondor_ithilien_ranger | 64.6 | 75.7 | OneHandedSword | wm_gondor_sword_a10 | 17.5 | False | Ranged Troops | gondor | 51.0 | special_or_unlinked |
| 186 | B | [Rhûn] Black Sun Scourge | black_sun_scourge | 64.3 | 73.3 | TwoHandedAxe | sm_rh_drag_2h_axe_a | 37.6 | False | Offensive Melee | khuzait | 36.0 | main_or_minor_line |
| 187 | B | [Misty Mountains] Orc Infantry | mistymountainorcs_veteran_sword_warrior | 64.2 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 36.8 | False | Defensive Troops | mistymountainorcs | 31.0 | main_or_minor_line |
| 188 | B | [Dol Guldur] Khamûl's Shadow-Guard | dg_khamul_shadow_guard | 64.2 | 70.1 | Mace | sm_dg_khml_1h_mace_a|sm_dg_khml_1h_mace_b | 60.7 | False | Defensive Troops | dolguldur | 46.0 | main_or_minor_line |
| 189 | B | [Iron Hills] Axe Warrior | iron_hills_reg_axe_warrior | 64.2 | 73.3 | TwoHandedAxe | sm_dwarf_iron_axe_a|sm_dwarf_iron_axe_b|sm_dwarf_iron_axe_c|sm_dwarf_iron_axe_d | 29.4 | False | Offensive Melee | erebor | 31.0 | main_or_minor_line |
| 190 | B | [Isengard] Orc Warg-Rider Lieutenant | orc_warg_lieutenant | 64.2 | 82.0 | TwoHandedPolearm | isengard_spear_b | 38.9 | True | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 191 | B | [Rhûn] Wainrider Horseman | wainrider_horseman | 63.9 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 37.1 | True | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 192 | B | [Dol Guldur] Khamûl's Shadow-Reaper | dg_khamul_shadow_reaper | 63.9 | 73.3 | TwoHandedAxe | sm_dg_khml_2h_axe_a|sm_dg_khml_2h_axe_b | 32.8 | False | Offensive Melee | dolguldur | 46.0 | main_or_minor_line |
| 193 | B | [Rohan] West Emnet Medium Cavalry | rohan_westemnet_eorlingas_rider | 63.8 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a03 | 48.7 | True | Skirmishers | vlandia | 26.0 | main_or_minor_line |
| 194 | B | [Isengard] Uruk-Hai Reaver | urukhai_reaver | 63.6 | 73.3 | TwoHandedAxe | isengard_2h_axe_c | 39.1 | False | Offensive Melee | isengard | 31.0 | main_or_minor_line |
| 195 | B | [Dol Guldur] Khamûl's Veiled Reaper | dg_khamul_veiled_reaper | 63.6 | 73.3 | TwoHandedAxe | sm_dg_khml_2h_axe_a|sm_dg_khml_2h_axe_b | 30.8 | False | Offensive Melee | dolguldur | 41.0 | main_or_minor_line |
| 196 | B | [Dol Guldur] Khamûl's Shadowbow | dg_khamul_shadow_bowman | 63.4 | 73.3 | TwoHandedAxe | sm_dg_khml_2h_axe_a|sm_dg_khml_2h_axe_b | 29.4 | False | Ranged Troops | dolguldur | 46.0 | main_or_minor_line |
| 197 | B | [Gondor] Arndir Veteran Infantry | gondor_arn_vet_infantry | 63.3 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 41.5 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 198 | B | [Dol Guldur] Khamûl's Veiled Guard | dg_khamul_veiled_guard | 63.3 | 70.1 | Mace | sm_dg_khml_1h_mace_a|sm_dg_khml_1h_mace_b | 54.2 | False | Defensive Troops | dolguldur | 41.0 | main_or_minor_line |
| 199 | B | [Gondor] Cair Andros Guard | gondor_ca_guard | 63.3 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 41.2 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 200 | B | [Umbar] Abrazanim Narduzagar | umbar_elite_root001 | 63.3 | 100.0 | TwoHandedAxe|TwoHandedSword | numenorean_sword_2h_y|peasant_2haxe_1_t1 | 25.0 | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 201 | B | [Gondor] Osgiliath Guard | gondor_osg_guard | 63.0 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 39.4 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 202 | B | [Erebor] Axe-Guard | erebor_noble_axe_guard | 62.8 | 73.3 | TwoHandedAxe | sm_dwarf_erebor_axe_2h_a|sm_dwarf_erebor_axe_2h_b|sm_dwarf_erebor_axe_2h_c|sm_dwarf_erebor_axe_2h_d | 42.3 | False | Offensive Melee | erebor | 31.0 | main_or_minor_line |
| 203 | B | [Rhûn] Black Sun Executioner | black_sun_executioner | 62.7 | 73.3 | TwoHandedAxe | sm_rh_drag_2h_axe_a | 32.0 | False | Offensive Melee | khuzait | 31.0 | main_or_minor_line |
| 204 | B | [Harad] Camel Lancer | harad_camel_lancer | 62.7 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 40.7 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 205 | B | [Gundabad] Bolg's Ironfang | gundabad_bolgs_ironfang | 62.6 | 70.1 | Mace | wm_gundabad_mace_a01 | 50.1 | False | Defensive Troops | gundabad | 36.0 | main_or_minor_line |
| 206 | B | [Gondor] Dol Amroth Squire | gondor_da_squire | 62.5 | 82.0 | TwoHandedPolearm | wm_gondor_swanknight_spearb | 52.0 | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 207 | B | [Isengard] Uruk-Hai Champion | urukhai_champion | 62.4 | 100.0 | TwoHandedSword | isengard_berserker_sword_2h | 24.0 | False | Offensive Melee | isengard | 26.0 | main_or_minor_line |
| 208 | B | [Iron Hills] Anvilguard | iron_hills_noble_anvilguard | 62.2 | 70.1 | TwoHandedMace | sm_dwarf_iron_hammer_b | 46.8 | False | Offensive Melee | erebor | 36.0 | main_or_minor_line |
| 209 | B | [Gondor] Anfalas Veteran Cavalry | gondor_anf_vet_cavalry | 62.1 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 49.0 | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 210 | B | [Gondor] Ithil Guard Watcher | gondor_ith_watcher | 62.1 | 100.0 | OneHandedSword|TwoHandedPolearm|TwoHandedSword | wm_gondor_lamedon_2h_sword_e|wm_gondor_swanknight_speara|wm_gondor_sword_a08 | 24.6 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 211 | B | [Gondor] Anórien Heavy Cavalry | gondor_ano_mt_heavy_cavalry | 62.1 | 82.0 | TwoHandedPolearm | wm_gondor_gondorknight_speara | 48.6 | True | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 212 | B | [Dol Guldur] Uruk Black Guard | dg_uruk_black_guard | 62.1 | 70.1 | Mace | wm_dol_goldur_1h_mace_a01 | 45.7 | False | Defensive Troops | dolguldur | 31.0 | main_or_minor_line |
| 213 | B | [Dunland] Caru-lûth Rider | dunland_stag_rider | 62.1 | 82.0 | TwoHandedPolearm | empire_lance_2_t4 | 61.4 | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 214 | B | [Dol Guldur] Shadow Warden | dg_khamul_shadow_warden | 62.0 | 70.1 | Mace | sm_dg_khml_1h_mace_a|sm_dg_khml_1h_mace_b | 45.1 | False | Defensive Troops | dolguldur | 36.0 | main_or_minor_line |
| 215 | B | [Iron Hills] Hammer-Guard | iron_hills_noble_hammer_guard | 62.0 | 70.1 | TwoHandedMace | sm_dwarf_iron_hammer_a | 45.2 | False | Offensive Melee | erebor | 31.0 | main_or_minor_line |
| 216 | B | [Erebor] Warrior | erebor_reg_warrior | 62.0 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_c|sm_dwarf_erebor_1h_axe_d|sm_dwarf_erebor_1h_axe_e | 30.1 | False | Defensive Troops | erebor | 31.0 | main_or_minor_line |
| 217 | B | [Gundabad] Pale Uruk Mountain Guard | gundabad_chosen_of_tharzog | 62.0 | 70.1 | Mace | wm_gundabad_mace_a01 | 44.9 | False | Defensive Troops | gundabad | 36.0 | main_or_minor_line |
| 218 | B | [Rhûn] Kharaghûl Karash Keshig | kharaghul_karash_keshig | 61.9 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_a | 51.0 | True | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 219 | B | [Gondor] Citadel Guard Veteran | gondor_mt_veteran | 61.8 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 30.0 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 220 | B | [Goblin] Goblin Infantry | goblin_veteran_sword_warrior | 61.8 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 36.8 | False | Defensive Troops | goblin | 31.0 | main_or_minor_line |
| 221 | B | [Rhûn] Dragon-Wrath Obsidian War-Reaver | dragon_wrath_obsidian_war_reaver | 61.6 | 70.1 | TwoHandedMace | sm_rh_drag_2h_mace_b | 41.5 | False | Offensive Melee | khuzait | 46.0 | main_or_minor_line |
| 222 | B | [Gondor] Pinnath Gelin Light Horseman | gondor_pg_cavalry | 61.6 | 82.0 | TwoHandedPolearm | wm_gondor_pg_speara | 44.5 | True | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 223 | B | [Rhûn] Loke-Rim Gilded Champion | loke_rim_gilded_champion | 61.6 | 70.1 | TwoHandedMace | sm_rh_loke_2h_mace_b | 40.6 | False | Offensive Melee | khuzait | 36.0 | main_or_minor_line |
| 224 | B | [Iron Hills] Ironbreaker | iron_hills_noble_ironbreaker | 61.4 | 70.1 | TwoHandedMace | sm_dwarf_iron_hammer_c | 40.8 | False | Offensive Melee | erebor | 41.0 | main_or_minor_line |
| 225 | B | [Dol Guldur] Shadow Infantry | dg_khamul_shadow_infantry | 61.4 | 70.1 | Mace | sm_dg_khml_1h_mace_a|sm_dg_khml_1h_mace_b | 40.1 | False | Defensive Troops | dolguldur | 31.0 | main_or_minor_line |
| 226 | B | [Gundabad] Pale Uruk Skull Crusher | gundabad_veteran_berserker | 61.4 | 70.1 | TwoHandedMace | wm_gundabad_mace_b01 | 39.5 | False | Skirmishers | gundabad | 36.0 | main_or_minor_line |
| 227 | B | [Gondor] Lossarnach Noble Warden | gondor_loss_noble_warden | 61.1 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_silver_b | 42.3 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 228 | B | [Gondor] Lossarnach Veteran Guard | gondor_loss_vet_guard | 61.0 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_a|wm_gondor_lossarnach_1h_axe_b|wm_gondor_lossarnach_1h_axe_black_ash_a|wm_gondor_lossarnach_1h_axe_silver_a|wm_gondor_lossarnach_1h_axe_silver_b|wm_gondor_lossarnach_1h_axe_silver_full_a | 41.5 | False | Defensive Troops | gondor | 31.0 | main_or_minor_line |
| 229 | B | [Misty Mountains] Bolg's Ironfang | mistymountainorcs_bolgs_ironfang | 60.9 | 70.1 | Mace | wm_dol_goldur_1h_mace_a02 | 36.8 | False | Defensive Troops | mistymountainorcs | 36.0 | main_or_minor_line |
| 230 | B | [Goblin] Goblin Mountain Guard | goblin_chosen_of_tharzog | 60.9 | 70.1 | Mace | wm_dol_goldur_1h_mace_a02 | 36.8 | False | Defensive Troops | goblin | 36.0 | main_or_minor_line |
| 231 | B | [Goblin] Bolg's Ironfang | goblin_bolgs_ironfang | 60.9 | 70.1 | Mace | wm_dol_goldur_1h_mace_a02 | 36.8 | False | Defensive Troops | goblin | 36.0 | main_or_minor_line |
| 232 | B | [Misty Mountains] Orc Mountain Guard | mistymountainorcs_chosen_of_tharzog | 60.9 | 70.1 | Mace | wm_dol_goldur_1h_mace_a02 | 36.8 | False | Defensive Troops | mistymountainorcs | 36.0 | main_or_minor_line |
| 233 | B | [Harad] Champion | harad_champion | 60.9 | 75.7 | OneHandedSword | aserai_sword_6_t4 | 34.6 | False | Defensive Troops | aserai | 31.0 | main_or_minor_line |
| 234 | B | [Erebor] Mattock Warrior | erebor_reg_mattock_warrior | 60.5 | 73.3 | OneHandedAxe|TwoHandedMace | sm_dwarf_erebor_1h_axe_a|sm_dwarf_iron_mattock_a|sm_dwarf_iron_mattock_b|sm_dwarf_iron_mattock_c|sm_dwarf_iron_mattock_d | 26.3 | False | Offensive Melee | erebor | 31.0 | main_or_minor_line |
| 235 | B | [Mordor] Black Uruk Heavy Archer | mordor_uruk_heavy_archer | 60.4 | 100.0 | TwoHandedSword | isengard_berserker_sword_2h | 34.2 | False | Ranged Troops | mordor | 31.0 | main_or_minor_line |
| 236 | B | [Dol Guldur] Warg Fang | dg_warg_red_fang | 60.2 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a01 | 46.7 | True | Defensive Troops | dolguldur | 31.0 | main_or_minor_line |
| 237 | B | [Goblin] Goblin Skull Crusher | goblin_veteran_berserker | 60.0 | 70.1 | Mace | wm_gundabad_mace_a02 | 29.3 | False | Skirmishers | goblin | 36.0 | main_or_minor_line |
| 238 | B | [Misty Mountains] Orc Skull Crusher | mistymountainorcs_veteran_berserker | 60.0 | 70.1 | Mace | wm_gundabad_mace_a02 | 29.3 | False | Skirmishers | mistymountainorcs | 36.0 | main_or_minor_line |
| 239 | B | [Dunland] Blaidd-lûth Champion | dunland_wolf_champion | 59.6 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 42.2 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 240 | B | [Rhûn] Dragon-Wrath Ash Executioner | dragon_wrath_ash_executioner | 59.5 | 70.1 | TwoHandedMace | sm_rh_drag_2h_mace_a | 25.1 | False | Offensive Melee | khuzait | 41.0 | main_or_minor_line |
| 241 | B | [Harad] Serpent Guard | harad_serpentguard | 59.2 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 52.4 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 242 | B | [Gondor] Ithil Guard Sharpshooter | gondor_ith_sharpshooter | 59.2 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 33.4 | False | Ranged Troops | gondor | 41.0 | main_or_minor_line |
| 243 | B | [Gondor] Citadel Guard Sharpshooter | gondor_mt_sharpshooter | 59.2 | 75.7 | OneHandedSword | wm_gondor_sword_a10 | 33.0 | False | Ranged Troops | gondor | 41.0 | main_or_minor_line |
| 244 | B | [Gondor] Blackroot Vale Shadowbow | gondor_brv_shadowbow | 59.1 | 75.7 | OneHandedSword | wm_gondor_sword_a10 | 32.9 | False | Ranged Troops | gondor | 41.0 | main_or_minor_line |
| 245 | B | [Dale] Lake-Town Veteran Pikeman | dale_veteran_spearman | 59.1 | 82.0 | TwoHandedPolearm | dale_halberd_a|dale_poleaxe_a | 38.9 | False | Offensive Melee | sturgia | 26.0 | main_or_minor_line |
| 246 | B | [Rhûn] Loke-Rim Maceman | loke_rim_maceman | 58.6 | 70.1 | TwoHandedMace | sm_rh_loke_2h_mace_a | 24.9 | False | Offensive Melee | khuzait | 31.0 | main_or_minor_line |
| 247 | B | [Dunland] Arth-lûth Executioner | dunland_bear_executioner | 58.6 | 73.3 | TwoHandedAxe | dunland_caerdh_axe_2h_b | 34.3 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 248 | B | [Dol Guldur] Khamûl's Veiled Marksman | dg_khamul_veiled_marksman | 58.0 | 73.3 | TwoHandedAxe | sm_dg_khml_2h_axe_a|sm_dg_khml_2h_axe_b | 28.8 | False | Ranged Troops | dolguldur | 41.0 | main_or_minor_line |
| 249 | B | [Rhûn] Dragon-Wrath Obsidian Warbow | dragon_wrath_obsidian_warbow | 57.9 | 70.1 | Mace | sm_rh_drag_1h_mace_b | 41.2 | False | Ranged Troops | khuzait | 46.0 | main_or_minor_line |
| 250 | B | [Gundabad] Pale Uruk Bone Breaker | gundabad_berserker | 56.8 | 70.1 | TwoHandedMace | wm_gundabad_mace_b01 | 33.0 | False | Skirmishers | gundabad | 31.0 | main_or_minor_line |
| 251 | B | [Mordor] Black Uruk Shieldbearer | mordor_uruk_shieldbearer | 56.7 | 82.0 | TwoHandedPolearm | isengard_spear_a|isengard_spear_b | 35.4 | False | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 252 | B | [Isengard] Uruk-Hai Veteran Spearman | urukhai_veteranspearman | 56.5 | 82.0 | TwoHandedPolearm | isengard_spear_a | 45.0 | False | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 253 | B | [Mordor] Nurn Beast Master | mordor_warg_beastmaster | 56.3 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a01 | 29.3 | True | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 254 | B | [Dale] Dalian Mariner | dale_dalian_mariner | 55.8 | 82.0 | TwoHandedPolearm | dale_winged_spear_a|dale_winged_spear_b | 51.6 | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 255 | B | [Misty Mountains] Orc Bone Breaker | mistymountainorcs_berserker | 55.7 | 70.1 | Mace | wm_gundabad_mace_a02 | 29.3 | False | Skirmishers | mistymountainorcs | 31.0 | main_or_minor_line |
| 256 | B | [Rhûn] Kharaghûl Keshig | kharaghul_keshig | 55.7 | 82.0 | TwoHandedPolearm | khuzait_polearm_1_t4 | 50.5 | True | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 257 | B | [Rohan] Wold Eorlingas Horse Archer | rohan_wold_eorlingas_horse_archer | 55.7 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 50.5 | True | Ranged Troops | vlandia | 31.0 | main_or_minor_line |
| 258 | B | [Rhûn] Easterling Veteran Halberdier | easterling_veteran_halberdier_new | 55.4 | 82.0 | TwoHandedPolearm | mirkwood_spear_a01 | 35.8 | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 259 | B | [Rivendell] Imladris Infantry | imladris_infantry | 55.1 | 75.7 | OneHandedSword | wm_rivendell_sword_a01|wm_rivendell_sword_a02 | 48.5 | False | Defensive Troops | rivendell | 26.0 | main_or_minor_line |
| 260 | B | [Dunland] Avanc-lûth Outrider | dunland_lizard_outrider | 54.7 | 73.3 | TwoHandedAxe | dunland_caerdh_axe_2h_c | 57.5 | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 261 | B | [Ironpass] Axeman | ironpass_axeman | 54.6 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a | 43.5 | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 262 | B | [Dale] Dalian Northman Scout | dale_knight | 54.5 | 82.0 | TwoHandedPolearm | dale_winged_spear_a | 67.5 | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 263 | B | [Dale] Dalian Cavalry | dale_royal_cavalier | 54.5 | 82.0 | TwoHandedPolearm | dale_winged_spear_a | 67.0 | True | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 264 | B | [Rhûn] Wain Glaiveman | wain_glaiveman | 54.4 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 28.3 | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 265 | B | [Dale] Dalian Swordsman | dale_royal_guard | 54.2 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_sword_a|dale_winged_spear_b | 47.0 | False | Defensive Troops | sturgia | 26.0 | main_or_minor_line |
| 266 | B | [Rohan] Meduseld Helmingas Spearman | rohan_edoras_meduseld_helmingas_spearman | 54.2 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 38.0 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 267 | B | [Rohan] West Marches Veteran Spearman | rohan_westmarches_meduseld_spearman | 53.8 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a03 | 36.9 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 268 | B | [Dunland] Hebog-lûth Horse Archer | dunland_falcon_wildrider | 53.5 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 47.7 | True | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 269 | B | [Rivendell] Militia Veteran Spearman | rivendell_militia_veteran_spearman | 53.4 | 82.0 | TwoHandedPolearm | wm_rivendell_spear_a01|wm_rivendell_spear_a01_silver | 48.4 | False | Defensive Troops | rivendell | 16.0 | special_or_unlinked |
| 270 | B | [Dale] Lake-Town Officer of the Watch | dale_lake_town_veteran | 53.3 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_halberd_b|dale_sword_a | 32.7 | False | Offensive Melee | sturgia | 26.0 | main_or_minor_line |
| 271 | B | [Goblin] Goblin Bone Breaker | goblin_berserker | 52.6 | 70.1 | Mace | wm_gundabad_mace_a02 | 29.3 | False | Skirmishers | goblin | 31.0 | main_or_minor_line |
| 272 | B | [Gondor] Methir Glaiveman | gondor_met_glaiveman | 52.5 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 39.8 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 273 | B | [Gondor] Linhir Spearman | gondor_lin_spearman | 52.5 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 39.8 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 274 | B | [Iron Hills] Infantry | iron_hills_noble_infantry | 52.5 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_b | 39.7 | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 275 | B | [Gondor] Pinnath Gelin Veteran Spearman | gondor_pg_vet_spearman | 52.4 | 82.0 | TwoHandedPolearm | wm_gondor_pg_speara | 39.0 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 276 | B | [Rohan] East Emnet Elite Lancer | rohan_eastemnet_elite_lancer | 52.3 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a02 | 50.1 | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 277 | B | [Rhûn] Loke-Rim Infantry | loke_rim_infantry | 52.0 | 82.0 | TwoHandedPolearm | sm_rh_loke_spear_a | 48.2 | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 278 | B | [Rhûn] Darkhûn Veteran Infantry | darkhun_veteran_infantry | 51.8 | 82.0 | TwoHandedPolearm | sm_dg_khml_spear_a | 47.1 | False | Defensive Troops | khuzait | 26.0 | main_or_minor_line |
| 279 | B | [Erebor] Infantry | erebor_noble_infantry | 51.5 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 44.0 | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 280 | B | [Gondor] Blackroot Vale Shadowhunter | gondor_brv_shadowhunter | 51.5 | 75.7 | OneHandedSword | wm_gondor_sword_a09 | 32.9 | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 281 | B | [Gondor] Methir Composite Archer | gondor_met_composite_archer | 51.5 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 32.9 | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 282 | B | [Gondor] Blackroot Vale Ranger | gondor_brv_ranger | 51.5 | 75.7 | OneHandedSword | wm_gondor_sword_a09 | 32.9 | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 283 | B | [Gondor] Tolfalas Sharpshooter | gondor_tol_sharpshooter | 51.5 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 32.9 | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 284 | B | [Gondor] Citadel Guard Longbowman | gondor_mt_longbowman | 51.4 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 32.7 | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 285 | B | [Gundabad] Pale Uruk Spearman | gundabad_spear_warrior | 51.1 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a02 | 28.3 | False | Offensive Melee | gundabad | 26.0 | main_or_minor_line |
| 286 | B | [Gondor] Belfalas Veteran Infantry | gondor_bel_vet_infantry | 51.1 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 41.2 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 287 | B | [Gondor] Anfalas Infantry | gondor_anf_infantry | 51.1 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 41.2 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 288 | B | [Gondor] Harondor Infantry | gondor_har_infantry | 51.0 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3 | 41.1 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 289 | B | [Gondor] Ithil Guard Longbowman | gondor_ith_longbowman | 50.9 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 28.5 | False | Ranged Troops | gondor | 36.0 | main_or_minor_line |
| 290 | B | [Gondor] Pelargir Veteran | gondor_pel_veteran | 50.9 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 39.8 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 291 | B | [Rhûn] Black Sun Chosen Marksman | black_sun_chosen_marksman | 50.8 | 70.1 | Mace | sm_rh_drag_1h_mace_a | 31.2 | False | Ranged Troops | khuzait | 41.0 | main_or_minor_line |
| 292 | B | [Gondor] Calembel Swordsman | gondor_cal_swordsman | 50.8 | 75.7 | OneHandedSword | wm_gondor_lamedon_1h_sword_a | 39.8 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 293 | B | [Rivendell] Militia Spearman | rivendell_militia_spearman | 50.8 | 82.0 | TwoHandedPolearm | wm_rivendell_spear_a01|wm_rivendell_spear_a01_silver | 28.6 | False | Defensive Troops | rivendell | 11.0 | special_or_unlinked |
| 294 | B | [Isengard] Orthanc Chosen | orthanc_chosen | 50.8 | 75.7 | OneHandedSword | isengard_berserker_sword | 46.7 | False | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 295 | B | [Isengard] Uruk-Hai Pikeman | urukhai_pikeman | 50.5 | 75.7 | OneHandedSword | isengard_1h_sword_b | 37.5 | False | Offensive Melee | isengard | 26.0 | main_or_minor_line |
| 296 | B | [Gondor] Anórien Infantry | gondor_ano_infantry | 50.3 | 82.0 | TwoHandedPolearm | wm_gondor_spear_a | 35.4 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 297 | B | [Rhûn] Dragon-Wrath Ash Marksman | dragon_wrath_ash_marksman | 50.3 | 70.1 | Mace | sm_rh_drag_1h_mace_a | 26.4 | False | Ranged Troops | khuzait | 41.0 | main_or_minor_line |
| 298 | B | [Misty Mountains] Orc Spearman | mistymountainorcs_spear_warrior | 50.2 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a02 | 26.7 | False | Offensive Melee | mistymountainorcs | 26.0 | main_or_minor_line |
| 299 | B | [Mordor] Black Uruk Archer | mordor_uruk_archer | 49.9 | 100.0 | OneHandedSword|TwoHandedSword | isengard_berserker_sword_2h|sm_uruk_sword_c | 17.4 | False | Ranged Troops | mordor | 26.0 | main_or_minor_line |
| 300 | B | [Dol Guldur] Shadow Marksman | dg_khamul_shadow_marksman | 49.6 | 73.3 | TwoHandedAxe | sm_dg_khml_2h_axe_a|sm_dg_khml_2h_axe_b | 21.7 | False | Ranged Troops | dolguldur | 36.0 | main_or_minor_line |
| 301 | B | [Dunland] Turch-lûth Ironhide | dunland_boar_boar_warrior | 49.3 | 82.0 | TwoHandedPolearm | dunland_caerdh_spear_b | 40.6 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 302 | B | [Rhûn] Loke-Rim Gilded Marksman | loke_rim_gilded_marksman | 49.2 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_a | 38.4 | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 303 | B | [Rhûn] Balcoth Farshot Horse Archer | balcoth_farshot_horse_archer | 49.1 | 73.3 | OneHandedAxe | sm_rh_loke_1h_axe_a | 48.6 | True | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 304 | B | [Dol Guldur] Warg Rider | dg_warg_raider | 48.7 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a02 | 40.2 | True | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 305 | B | [Harad] Sunlance | harad_sunlance | 48.6 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 35.3 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 306 | B | [Harad] Bronze Fang | harad_bronzefang | 48.6 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 35.3 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 307 | B | [Rhûn] Far-Rhun Cavalry | far_rhun_cavalry | 48.6 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 46.7 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 308 | B | [Rhûn] Far-Rhun Horse Master | far_rhun_horse_master | 48.6 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 46.7 | True | Skirmishers | khuzait | 21.0 | special_or_unlinked |
| 309 | B | [Dunland] Caru-lûth Lancer | dunland_stag_lancer | 48.5 | 82.0 | TwoHandedPolearm | vlandia_lance_1_t3 | 46.4 | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 310 | B | [Rhûn] Easterling Cavalry | easterling_cavalry_new | 48.4 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 45.5 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 311 | B | [Rhûn] Kharaghûl Raider | kharaghul_raider | 48.2 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 44.3 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 312 | B | [Mordor] Morannon Heavy Spearman | morannon_heavy_spearman | 48.2 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a01 | 31.8 | False | Offensive Melee | mordor | 26.0 | main_or_minor_line |
| 313 | B | [Iron Hills] Fighter | iron_hills_reg_fighter | 48.2 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a|sm_dwarf_iron_sword_b | 34.3 | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 314 | B | [Rhûn] Darkhûn Horseman | darkhun_horseman | 48.1 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 42.8 | True | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 315 | B | [Rohan] King's Horseman | rohan_edoras_golden_hall_veteran_rider | 47.7 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 51.7 | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 316 | B | [Rohan] Edoras Helmingas Swordsman | rohan_edoras_helmingas_swordsman | 47.6 | 75.7 | OneHandedSword | wm_rohan_ws_sword_a02|wm_rohan_ws_sword_a03 | 38.5 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 317 | B | [Isengard] Orc Warg-Rider Enforcer | orc_warg_enforcer | 47.6 | 82.0 | TwoHandedPolearm | isengard_spear_a | 38.9 | True | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 318 | B | [Mirkwood] Militia Veteran Spearman | mirkwood_militia_veteran_spearman | 47.5 | 82.0 | TwoHandedPolearm | mirkwood_spear_a01|mirkwood_spear_a02 | 27.5 | False | Defensive Troops | mirkwood | 16.0 | special_or_unlinked |
| 319 | B | [Rohan] West Emnet Light Cavalry | rohan_westemnet_elite_rider | 47.3 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a02 | 50.1 | True | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 320 | B | [Isengard] Orc Warg Ravager | isengard_orc_warg_ravager_v2 | 47.3 | 82.0 | TwoHandedPolearm | isengard_spear_b | 36.8 | True | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 321 | B | [Rhûn] Easterling Veteran Swordsman | easterling_veteran_swordsman_new | 47.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 35.4 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 322 | B | [Rhûn] Sagarûn Storm Marked Arbalest | sagarun_storm_marked_arbalest | 46.9 | 73.3 | OneHandedAxe | sm_rh_loke_1h_axe_a | 35.5 | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 323 | B | [Rhûn] Sagarûn Storm Helmed Naffatun | sagarun_storm_helmed_naffatun | 46.9 | 73.3 | OneHandedAxe | sm_rh_loke_1h_axe_a | 35.5 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 324 | B | [Mirkwood] Militia Spearman | mirkwood_militia_spearman | 46.8 | 82.0 | TwoHandedPolearm | mirkwood_spear_a01|mirkwood_spear_a02 | 26.7 | False | Defensive Troops | mirkwood | 11.0 | special_or_unlinked |
| 325 | B | [Isengard] Uruk-Hai Infantry | urukhai_infantry | 46.7 | 75.7 | OneHandedSword | isengard_1h_sword_a | 43.6 | False | Defensive Troops | isengard | 26.0 | main_or_minor_line |
| 326 | B | [Goblin] Goblin Spearman | goblin_spear_warrior | 46.6 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a02 | 26.7 | False | Offensive Melee | goblin | 26.0 | main_or_minor_line |
| 327 | B | [Mordor] Black Uruk Infantry | mordor_uruk_infantry | 46.5 | 75.7 | OneHandedSword | sm_uruk_sword_b|sm_uruk_sword_d | 33.4 | False | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 328 | B | [Gondor] Serelond Maceman | gondor_ser_maceman | 46.4 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 41.5 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 329 | B | [Rhûn] Far-Rhun Gate Guard | far_rhun_gate_guard | 46.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 41.3 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 330 | B | [Gondor] Arndir Infantry | gondor_arn_infantry | 46.2 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 39.8 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 331 | B | [Gondor] Lossarnach Noble Sergeant | gondor_loss_noble_sergeant | 46.2 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_silver_a | 41.9 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 332 | B | [Gondor] Cair Andros Spearman | gondor_ca_spearman | 46.1 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 26.5 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 333 | B | [Gondor] Dol Amroth Infantry | gondor_da_infantry | 46.0 | 75.7 | OneHandedSword | wm_swan_knight_sworda | 38.2 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 334 | B | [Umbar] Abrazanim Nardutarik | umbar_elite_root000 | 46.0 | 75.7 | OneHandedSword|TwoHandedAxe | peasant_2haxe_1_t1|wm_swan_knight_sworda | 30.8 | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 335 | B | [Dale] Veteran Militia Spearman | dale_militia_veteran_spearman | 45.9 | 82.0 | TwoHandedPolearm | dale_winged_spear_a | 40.0 | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 336 | B | [Gondor] Osgiliath Infantry | gondor_osg_infantry | 45.8 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 36.6 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 337 | B | [Rhûn] Balcoth Veteran Axeman | balcoth_veteran_axeman | 45.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 35.4 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 338 | B | [Gondor] Lebennin Veteran Infantry | gondor_leb_vet_infantry | 45.6 | 75.7 | OneHandedSword | wm_pelargir_sword_a02 | 35.1 | False | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 339 | B | [Gondor] Cair Andros Infantry | gondor_ca_infantry | 45.6 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 35.1 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 340 | B | [Gondor] Anfalas Cavalry | gondor_anf_cavalry | 45.3 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 47.6 | True | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 341 | B | [Gondor] Serelond Phalanx | gondor_ser_phalanx | 45.0 | 54.3 | Pike | vlandia_pike_1_t5 | 38.9 | False | Offensive Melee | gondor | 36.0 | main_or_minor_line |
| 342 | B | [Gondor] Anórien Cavalry | gondor_ano_mt_cavalry | 45.0 | 82.0 | TwoHandedPolearm | wm_gondor_spear_b | 44.7 | True | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 343 | B | [Dale] Lake-Town Pikeman | dale_spearman | 45.0 | 82.0 | TwoHandedPolearm | dale_halberd_a|dale_poleaxe_a | 32.5 | False | Offensive Melee | sturgia | 21.0 | main_or_minor_line |
| 344 | B | [Gundabad] Pale Uruk War-Pike | gundabad_guardian_of_the_tower | 44.8 | 54.3 | Pike | isengard_pike_b | 37.4 | False | Offensive Melee | gundabad | 36.0 | main_or_minor_line |
| 345 | B | [Dol Guldur] Uruk Black Sharpshooter | dg_uruk_black_sharpshooter | 44.8 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a01 | 41.1 | False | Ranged Troops | dolguldur | 31.0 | main_or_minor_line |
| 346 | B | [Dale] Militia Spearman | dale_militia_spearman | 44.8 | 82.0 | TwoHandedPolearm | dale_spear_a | 31.0 | False | Defensive Troops | sturgia | 6.0 | main_or_minor_line |
| 347 | B | [Gondor] Citadel Guard Trainee | gondor_mt_trainee | 44.7 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 28.3 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 348 | B | [Rhûn] Dragon-Wrath Longbowman | dragon_wrath_longbowman | 44.7 | 70.1 | Mace | sm_rh_drag_1h_mace_a | 38.2 | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 349 | B | [Gondor] Lossarnach Guard | gondor_loss_guard | 44.6 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_a|wm_gondor_lossarnach_1h_axe_b|wm_gondor_lossarnach_1h_axe_black_ash_a|wm_gondor_lossarnach_1h_axe_silver_a|wm_gondor_lossarnach_1h_axe_silver_b|wm_gondor_lossarnach_1h_axe_silver_full_a | 41.5 | False | Defensive Troops | gondor | 26.0 | main_or_minor_line |
| 350 | B | [Gondor] Serelond Pikewarden | gondor_ser_pikewarden | 44.3 | 54.3 | Pike | fine_pike_t4 | 33.1 | False | Offensive Melee | gondor | 31.0 | main_or_minor_line |
| 351 | B | [Iron Hills] Veteran Sharpshooter | iron_hills_noble_veteran_sharpshooter | 44.1 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_b | 35.4 | False | Ranged Troops | erebor | 31.0 | main_or_minor_line |
| 352 | B | [Isengard] Uruk-Hai Slayer | urukhai_slayer | 43.9 | 73.3 | TwoHandedAxe | isengard_2h_axe_b | 36.1 | False | Offensive Melee | isengard | 26.0 | main_or_minor_line |
| 353 | B | [Erebor] Fighter | erebor_reg_fighter | 43.9 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_b|sm_dwarf_erebor_1h_axe_c|sm_dwarf_erebor_1h_axe_d | 28.2 | False | Defensive Troops | erebor | 26.0 | main_or_minor_line |
| 354 | B | [Misty Mountains] Orc War-Pike | mistymountainorcs_guardian_of_the_tower | 43.8 | 54.3 | Pike | isengard_pike_b | 29.3 | False | Offensive Melee | mistymountainorcs | 36.0 | main_or_minor_line |
| 355 | B | [Goblin] Goblin War-Pike | goblin_guardian_of_the_tower | 43.8 | 54.3 | Pike | isengard_pike_b | 29.3 | False | Offensive Melee | goblin | 36.0 | main_or_minor_line |
| 356 | B | [Dol Guldur] Uruk Fell Infantry | dg_uruk_fell_infantry | 43.8 | 70.1 | Mace | wm_dol_goldur_1h_mace_a02 | 42.9 | False | Defensive Troops | dolguldur | 26.0 | main_or_minor_line |
| 357 | B | [Dale] Dalian Royal Crossbowman | dale_master_crossbowman | 43.6 | 75.7 | OneHandedSword | dale_sword_a | 55.3 | False | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 358 | B | [Rhûn] Black Sun Marksman | black_sun_marksman | 43.5 | 70.1 | Mace | sm_rh_drag_1h_mace_a | 29.4 | False | Ranged Troops | khuzait | 36.0 | main_or_minor_line |
| 359 | B | [Dale] Dalian Barding | dale_black_arrow_marksman | 43.5 | 75.7 | OneHandedSword | dale_sword_a | 54.6 | False | Ranged Troops | sturgia | 31.0 | main_or_minor_line |
| 360 | B | [Dol Guldur] Shadow Disciple | dg_khamul_shadow_disciple | 43.5 | 70.1 | Mace | sm_dg_khml_1h_mace_a|sm_dg_khml_1h_mace_b | 40.0 | False | Defensive Troops | dolguldur | 26.0 | main_or_minor_line |
| 361 | B | [Rivendell] Imladris Recruit | imladris_recruit | 43.2 | 75.7 | OneHandedSword | wm_rivendell_sword_a01|wm_rivendell_sword_a02 | 37.6 | False | Ranged Troops | rivendell | 21.0 | main_or_minor_line |
| 362 | B | [Gondor] Osgiliath Longbowman | gondor_osg_longbowman | 43.1 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 39.8 | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 363 | B | [Mordor] Morannon Heavy Infantry | morannon_heavy_infantry | 43.1 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a01 | 39.4 | False | Defensive Troops | mordor | 26.0 | main_or_minor_line |
| 364 | B | [Dol Guldur] Uruk Fell Fang | dg_uruk_fell_fang | 42.9 | 70.1 | TwoHandedMace | wm_dol_goldur_2h_mace_a02 | 35.3 | False | Offensive Melee | dolguldur | 26.0 | main_or_minor_line |
| 365 | B | [Mordor] Black Uruk Heavy Crossbow | mordor_uruk_heavy_crossbow | 42.8 | 75.7 | OneHandedSword | sm_uruk_sword_d | 32.0 | False | Ranged Troops | mordor | 31.0 | main_or_minor_line |
| 366 | B | [Isengard] Uruk-Hai Veteran Crossbowman | urukhai_veterancrossbowman | 42.7 | 75.7 | OneHandedSword | isengard_1h_sword_a | 36.6 | False | Ranged Troops | isengard | 31.0 | main_or_minor_line |
| 367 | B | [Isengard] Uruk-Hai Spearman | urukhai_spearman | 42.6 | 82.0 | TwoHandedPolearm | isengard_spear_a | 40.2 | False | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 368 | B | [Rohan] Wold Elite Horse Rider | rohan_wold_elite_horse_archer | 42.6 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 51.8 | True | Ranged Troops | vlandia | 26.0 | main_or_minor_line |
| 369 | B | [Rivendell] Imladris Bowman | imladris_bowman | 42.5 | 75.7 | OneHandedSword | wm_rivendell_sword_a01|wm_rivendell_sword_a02 | 34.7 | False | Ranged Troops | rivendell | 26.0 | main_or_minor_line |
| 370 | B | [Rhûn] Black Sun Reaver | black_sun_reaver | 42.4 | 73.3 | OneHandedAxe | sm_rh_drag_1h_axe_a | 24.3 | False | Offensive Melee | khuzait | 26.0 | main_or_minor_line |
| 371 | B | [Harad] Warrior of the Gilded Fang | harad_gildedfang | 42.3 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 50.1 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 372 | B | [Rohan] Westfold Helmingas Axeman | rohan_westfold_helmingas_axeman | 42.3 | 73.3 | OneHandedAxe | vlandia_axe_2_t4 | 34.6 | False | Defensive Troops | vlandia | 26.0 | main_or_minor_line |
| 373 | B | [Gondor] Methir Veteran Archer | gondor_met_vet_archer | 42.3 | 75.7 | OneHandedSword | wm_gondor_sword_a06 | 32.9 | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 374 | B | [Gondor] Lond-Galen Pavise Crossbowman | gondor_lg_pavise_crossbowman | 42.3 | 75.7 | OneHandedSword | wm_gondor_sword_a06 | 32.9 | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 375 | B | [Gondor] Blackroot Vale Veteran Archer | gondor_brv_vet_archer | 42.3 | 75.7 | OneHandedSword | wm_gondor_sword_a08 | 32.9 | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 376 | B | [Gondor] Tolfalas Marksman | gondor_tol_marksman | 42.3 | 75.7 | OneHandedSword | wm_gondor_sword_a06 | 32.9 | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 377 | B | [Erebor] Veteran Archer | erebor_noble_veteran_archer | 42.2 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_b | 44.8 | False | Ranged Troops | erebor | 31.0 | main_or_minor_line |
| 378 | B | [Dunland] Arth-lûth Berserker | dunland_bear_berserker | 42.2 | 73.3 | TwoHandedAxe | dunland_caerdh_axe_2h_c | 34.1 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 379 | B | [Dale] Dalian Guardsman | dale_guardsman | 42.0 | 82.0 | TwoHandedPolearm | dale_spear_b|dale_winged_spear_a | 39.6 | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 380 | B | [Ironpass] Sharpshooter | ironpass_sharpshooter | 42.0 | 73.3 | TwoHandedAxe | sm_dwarf_erebor_axe_2h_c|sm_dwarf_iron_axe_c | 35.4 | False | Ranged Troops | erebor | 31.0 | main_or_minor_line |
| 381 | B | [Dale] Dalian Shipman | dale_shipman | 41.8 | 82.0 | TwoHandedPolearm | dale_spear_b|dale_winged_spear_a | 45.8 | False | Defensive Troops | sturgia | 21.0 | main_or_minor_line |
| 382 | B | [Gondor] Lebennin Longbowman | gondor_leb_longbowman | 41.6 | 75.7 | OneHandedSword | wm_pelargir_sword_a02 | 28.0 | False | Ranged Troops | gondor | 31.0 | main_or_minor_line |
| 383 | B | Dol Guldur Militia Veteran Spearman | dolguldur_militia_veteran_spearman | 41.6 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a01|wm_dol_goldur_halberd_a03|wm_dol_goldur_halberd_a04 | 20.6 | False | Defensive Troops | dolguldur | 16.0 | special_or_unlinked |
| 384 | B | [Dunland] Uch-lûth Iron Wall | dunland_ox_iron_wall | 41.6 | 54.3 | Pike | fine_pike_t4 | 42.8 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 385 | B | [Gundabad] Pale Uruk Ravager | gundabad_brute | 41.6 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01 | 40.8 | False | Defensive Troops | gundabad | 26.0 | main_or_minor_line |
| 386 | B | [Dunland] Blaidd-lûth Axeman | dunland_wolf_axeman | 41.5 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 40.6 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 387 | B | [Harad] Camel Rider | harad_camelrider | 41.4 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 42.8 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 388 | B | [Misty Mountains] Orc Mauler | mistymountainorcs_sword_warrior | 41.4 | 70.1 | Mace | wm_gundabad_mace_a02 | 23.6 | False | Offensive Melee | mistymountainorcs | 26.0 | main_or_minor_line |
| 389 | B | [Rhûn] Easterling Halberdier | easterling_halberdier_new | 41.4 | 82.0 | TwoHandedPolearm | easterling_spear | 30.2 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 390 | B | [Gundabad] Pale Uruk Mauler | gundabad_sword_warrior | 41.2 | 70.1 | TwoHandedMace | wm_gundabad_mace_b01 | 22.7 | False | Offensive Melee | gundabad | 26.0 | main_or_minor_line |
| 391 | B | [Misty Mountains] Orc Ravager | mistymountainorcs_brute | 41.1 | 73.3 | OneHandedAxe | wm_gundabad_axe_a02 | 36.8 | False | Defensive Troops | mistymountainorcs | 26.0 | main_or_minor_line |
| 392 | B | Dol Guldur Militia Spearman | dolguldur_militia_spearman | 40.9 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a01|wm_dol_goldur_halberd_a02|wm_dol_goldur_halberd_a03 | 16.2 | False | Defensive Troops | dolguldur | 11.0 | special_or_unlinked |
| 393 | B | [Dol Guldur] Orc Archer | dg_orc_archer | 40.8 | 82.0 | TwoHandedMace|TwoHandedPolearm | wm_dol_goldur_2h_mace_a03|wm_dol_goldur_2h_mace_a04|wm_dol_goldur_halberd_a02|wm_dol_goldur_halberd_a04|wm_dol_goldur_halberd_a05 | 36.8 | False | Ranged Troops | dolguldur | 26.0 | main_or_minor_line |
| 394 | B | [Rohan] Westfold Helmingas Heavy Axeman | rohan_westfold_veteran_2h_axeman | 40.7 | 73.3 | TwoHandedAxe | vlandia_2haxe_1_t4 | 22.3 | False | Offensive Melee | vlandia | 26.0 | main_or_minor_line |
| 395 | B | [Rohan] Meduseld Veteran Spearman | rohan_edoras_meduseld_veteran_spearman | 40.7 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 37.4 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 396 | B | [Gondor] Lossarnach Veteran Axe-Thrower | gondor_loss_vet_axe_thrower | 40.6 | 73.3 | ThrowingAxe | highland_throwing_axe_1_t2|southern_throwing_axe_1_t4 | 32.9 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 397 | B | [Rohan] West-March Heavy Spearman | rohan_westmarches_veteran_spearman | 40.4 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a02 | 35.8 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 398 | B | [Rhûn] Militia Spearman | rhun_militia_spearman | 40.3 | 82.0 | TwoHandedPolearm | eastern_spear_3_t3|eastern_spear_4_t4 | 21.9 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 399 | B | [Rhûn] Militia Veteran Spearman | rhun_militia_veteran_spearman | 40.3 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 21.7 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 400 | B | [Erebor] Militia Veteran Spearman | erebor_militia_veteran_spearman | 40.2 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 22.8 | False | Defensive Troops | erebor | 16.0 | special_or_unlinked |
| 401 | B | [Dunland] Draig-lûth Sharpshooter | dunland_dragon_sniper | 40.0 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_c | 40.5 | False | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 402 | B | [Dale] Lake-Town Veteran Watchman | dale_lake_town_mariner | 40.0 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_poleaxe_a|dale_sword_a | 32.7 | False | Offensive Melee | sturgia | 21.0 | main_or_minor_line |
| 403 | C | [Harad] Serpent Archer | harad_serpenthorsearcher | 39.9 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 46.2 | True | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 404 | C | [Dol Guldur] Shadow Archer | dg_khamul_shadow_archer | 39.8 | 73.3 | TwoHandedAxe | sm_dg_khml_2h_axe_a | 14.6 | False | Ranged Troops | dolguldur | 31.0 | main_or_minor_line |
| 405 | C | [Rohan] Militia Veteran Spearman | rohan_militia_veteran_spearman | 39.8 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 29.8 | False | Defensive Troops | vlandia | 16.0 | special_or_unlinked |
| 406 | C | [Mordor] Nurn Warg Ravager | mordor_warg_ravager | 39.7 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a02 | 29.3 | True | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 407 | C | [Umbar] Adûnaims Faithful | umbar_elite_root010 | 39.6 | 73.3 | Pike|TwoHandedAxe | isengard_pike_a|peasant_2haxe_1_t1 | 25.0 | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 408 | C | [Dunland] Cigfran-lûth Master Ranger | dunland_raven_master_ranger | 39.6 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 37.0 | False | Ranged Troops | empire | 31.0 | main_or_minor_line |
| 409 | C | [Dale] Dalian Merchant Guard | dale_outrider | 39.4 | 82.0 | TwoHandedPolearm | dale_winged_spear_a | 62.1 | True | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 410 | C | [Rhûn] Wainrider Wind-Arrow Sharpshooter | wainrider_wind_arrow_sharpshooter | 39.1 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_a | 32.0 | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 411 | C | [Goblin] Goblin Mauler | goblin_sword_warrior | 39.1 | 70.1 | Mace | wm_gundabad_mace_a02 | 23.6 | False | Offensive Melee | goblin | 26.0 | main_or_minor_line |
| 412 | C | [Dol Guldur] Orc Reaver | dg_orc_reaver | 39.0 | 82.0 | TwoHandedMace|TwoHandedPolearm | wm_dol_goldur_2h_mace_a01|wm_dol_goldur_2h_mace_a02|wm_dol_goldur_2h_mace_a04|wm_dol_goldur_halberd_a01 | 38.9 | False | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 413 | C | [Rohan] Militia Spearman | rohan_militia_spearman | 38.9 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 22.8 | False | Defensive Troops | vlandia | 11.0 | special_or_unlinked |
| 414 | C | [Goblin] Goblin Ravager | goblin_brute | 38.7 | 73.3 | OneHandedAxe | wm_gundabad_axe_a02 | 36.8 | False | Defensive Troops | goblin | 26.0 | main_or_minor_line |
| 415 | C | [Rhûn] Sagarûn Arbalest | sagarun_arbalest | 38.7 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_a | 28.1 | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 416 | C | [Dunland] Avanc-lûth Horseman | dunland_lizard_horseman | 38.7 | 73.3 | TwoHandedAxe | dunland_caerdh_axe_2h_b | 47.9 | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 417 | C | [Gondor] Pinnath Gelin Spearman | gondor_pg_spearman | 38.5 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 34.1 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 418 | C | [Gondor] Pinnath Gelin Veteran Archer | gondor_pg_vet_archer | 38.4 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 32.9 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 419 | C | [Gondor] Gondor Veteran Militia Spearman | gondor_militia_veteran_spearman | 38.3 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 32.0 | False | Defensive Troops | gondor | 16.0 | special_or_unlinked |
| 420 | C | [Erebor] Militia Spearman | erebor_militia_spearman | 38.2 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 13.8 | False | Defensive Troops | erebor | 11.0 | special_or_unlinked |
| 421 | C | [Gondor] Gondor Militia Spearman | gondor_militia_spearman | 38.1 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 30.9 | False | Defensive Troops | gondor | 11.0 | special_or_unlinked |
| 422 | C | [Harad] Serpent Eyes | harad_serpent_eye | 38.1 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 12.2 | False | Ranged Troops | aserai | 31.0 | main_or_minor_line |
| 423 | C | [Rhûn] Loke-Rim Marksman | loke_rim_marksman | 38.0 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_a | 23.4 | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 424 | C | [Gundabad] Militia Veteran Spearman | gundabad_militia_veteran_spearman | 37.9 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a01|wm_gundabad_spear_a02|wm_gundabad_spear_a03 | 21.2 | False | Defensive Troops | gundabad | 16.0 | special_or_unlinked |
| 425 | C | [Rhûn] Kharaghûl Horse Archer | kharaghul_horse_archer | 37.9 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 42.7 | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 426 | C | [Rhûn] Darkhûn Infantry | darkhun_infantry | 37.7 | 82.0 | TwoHandedPolearm | sm_dg_khml_spear_a | 40.5 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 427 | C | [Rhûn] Loke-Rim Footman | loke_rim_footman | 37.7 | 82.0 | TwoHandedPolearm | sm_rh_loke_spear_a | 39.6 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 428 | C | [Dol Guldur] Goblin Impaler | dg_goblin_impaler | 37.6 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a01|wm_dol_goldur_halberd_a02 | 30.6 | False | Offensive Melee | dolguldur | 21.0 | main_or_minor_line |
| 429 | C | [Misty Mountains] Militia Veteran Spearman | mistymountainorcs_militia_veteran_spearman | 37.4 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a01|wm_gundabad_spear_a02|wm_gundabad_spear_a03 | 24.9 | False | Defensive Troops | mistymountainorcs | 16.0 | special_or_unlinked |
| 430 | C | [Ironpass] Infantry | ironpass_infantry | 37.3 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a | 40.7 | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 431 | C | [Dol Guldur] Uruk Swordsman | dg_uruk_swordsman | 37.1 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a02 | 40.7 | False | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 432 | C | [Rhûn] Sagarûn Naffatun | sagarun_naffatun | 37.1 | 73.3 | OneHandedAxe | sm_rh_loke_1h_axe_a | 28.1 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 433 | C | [Iron Hills] Swordsman | iron_hills_noble_swordsman | 36.8 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a | 38.5 | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 434 | C | [Rohan] East Emnet Veteran Lancer | rohan_eastemnet_veteran_lancer | 36.8 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a02 | 45.6 | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 435 | C | [Dol Guldur] Uruk Fell Archer | dg_uruk_fell_archer | 36.8 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a02 | 37.9 | False | Ranged Troops | dolguldur | 26.0 | main_or_minor_line |
| 436 | C | [Isengard] Militia Veteran Spearman | isengard_militia_veteran_spearman | 36.6 | 75.7 | OneHandedSword | isengard_1h_sword_b | 16.9 | False | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 437 | C | [Gundabad] Militia Spearman | gundabad_militia_spearman | 36.5 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a01|wm_gundabad_spear_a02|wm_gundabad_spear_a03 | 15.2 | False | Defensive Troops | gundabad | 11.0 | special_or_unlinked |
| 438 | C | [Rhûn] Balcoth Horse Archer | balcoth_horse_archer | 36.5 | 73.3 | OneHandedAxe | sm_rh_loke_1h_axe_a | 42.5 | True | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 439 | C | [Dunland] Hebog-lûth Scout | dunland_falcon_archer | 36.5 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 30.6 | True | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 440 | C | [Dunland] Wild-man Spearman | dunland_veteran_spearman | 36.4 | 82.0 | TwoHandedPolearm | highland_spear_3_t3 | 30.7 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 441 | C | [Iron Hills] Bowman | iron_hills_reg_bowman | 36.4 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a|sm_dwarf_iron_sword_b | 27.3 | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 442 | C | [Misty Mountains] Militia Spearman | mistymountainorcs_militia_spearman | 35.9 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a01|wm_gundabad_spear_a02|wm_gundabad_spear_a03 | 15.8 | False | Defensive Troops | mistymountainorcs | 11.0 | special_or_unlinked |
| 443 | C | [Iron Hills] Sharpshooter | iron_hills_noble_sharpshooter | 35.9 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_b | 31.2 | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 444 | C | [Dale] Dalian Master Crossbowman | dale_royal_crossbowman | 35.8 | 75.7 | OneHandedSword | dale_sword_a | 54.1 | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 445 | C | [Dol Guldur] Goblin Fellbow | dg_goblin_fellbow | 35.7 | 75.7 | OneHandedSword|TwoHandedMace | wm_dol_goldur_1h_sword_a03|wm_dol_goldur_2h_mace_a03|wm_dol_goldur_2h_mace_a04 | 30.9 | False | Ranged Troops | dolguldur | 26.0 | main_or_minor_line |
| 446 | C | [Gondor] Harondor Javelineer | gondor_har_javelineer | 35.6 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 41.1 | False | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 447 | C | [Isengard] Uruk-Hai Swordman | urukhai_swordman | 35.6 | 75.7 | OneHandedSword | isengard_1h_sword_a | 40.9 | False | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 448 | C | [Iron Hills] Company | iron_hills_reg_company | 35.5 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a | 27.9 | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 449 | C | [Gondor] Belfalas Veteran Archer | gondor_bel_vet_archer | 35.5 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 40.0 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 450 | C | [Rhûn] Wain Footman | wain_footman | 35.3 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 22.1 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 451 | C | [Rhûn] Dragon-Wrath Archer | dragon_wrath_archer | 35.2 | 70.1 | Mace | sm_rh_drag_1h_mace_a | 30.6 | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 452 | C | [Dunland] Militia Veteran Spearman | dunland_militia_veteran_spearman | 35.2 | 82.0 | TwoHandedPolearm | dunland_caerdh_spear_a|dunland_caerdh_spear_b|dunland_caerdh_spear_c | 19.1 | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 453 | C | [Gondor] Osgiliath Archer | gondor_osg_archer | 35.1 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 36.6 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 454 | C | [Erebor] Archer | erebor_noble_archer | 35.0 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_b | 46.6 | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 455 | C | [Mordor] Black Uruk Crossbow | mordor_uruk_crossbow | 34.9 | 75.7 | OneHandedSword | sm_uruk_sword_c | 30.6 | False | Ranged Troops | mordor | 26.0 | main_or_minor_line |
| 456 | C | Mordor Militia Veteran Spearman | mordor_militia_veteran_spearman | 34.6 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a01|wm_mordor_set1_polearm_a02|wm_mordor_set1_polearm_a04 | 23.1 | False | Defensive Troops | mordor | 16.0 | special_or_unlinked |
| 457 | C | [Dunland] Militia Spearman | dunland_militia_spearman | 34.6 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 12.6 | False | Defensive Troops | empire | 11.0 | special_or_unlinked |
| 458 | C | [Isengard] Uruk-Hai Archer | urukhai_archer | 34.5 | 75.7 | OneHandedSword | isengard_1h_sword_a | 31.9 | False | Ranged Troops | isengard | 26.0 | main_or_minor_line |
| 459 | C | [Isengard] Uruk-Hai Crossbowman | urukhai_crossbowman | 34.5 | 75.7 | OneHandedSword | isengard_1h_sword_a | 31.9 | False | Ranged Troops | isengard | 26.0 | main_or_minor_line |
| 460 | C | [Ironpass] Veteran Arbalest | ironpass_veteran_arbalest | 34.5 | 73.3 | TwoHandedAxe | sm_dwarf_erebor_axe_2h_b|sm_dwarf_iron_axe_b | 34.8 | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 461 | C | [Gondor] Methir Archer | gondor_met_archer | 34.4 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 31.2 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 462 | C | [Gondor] Tolfalas Veteran Crossbowman | gondor_tol_vet_crossbowman | 34.4 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 31.2 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 463 | C | [Gondor] Lond-Galen Crossbowman | gondor_lg_crossbowman | 34.4 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 31.2 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 464 | C | [Gondor] Blackroot Vale Archer | gondor_brv_archer | 34.4 | 75.7 | OneHandedSword | wm_gondor_sword_a07 | 31.2 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 465 | C | [Gondor] Lamedon Swordman | gondor_lam_swordman | 34.3 | 100.0 | TwoHandedSword | wm_gondor_lamedon_2h_sword_b | 26.3 | False | Offensive Melee | gondor | 16.0 | main_or_minor_line |
| 466 | C | [Umbar] Abrazanim Nardubawib | umbar_elite_root100 | 34.3 | 75.7 | OneHandedSword|TwoHandedAxe | peasant_2haxe_1_t1|wm_gondor_sword_a06 | 25.0 | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 467 | C | [Rhûn] Black Sun Longbowman | black_sun_longbowman | 34.3 | 70.1 | Mace | sm_rh_drag_1h_mace_a | 23.7 | False | Ranged Troops | khuzait | 31.0 | main_or_minor_line |
| 468 | C | [Dale] Dalian Marksman | dale_royal_archer | 34.0 | 75.7 | OneHandedSword | dale_sword_a | 40.0 | False | Ranged Troops | sturgia | 26.0 | main_or_minor_line |
| 469 | C | [Umbar] Rozadan Footmen | umbar_elite_root00 | 33.9 | 82.0 | TwoHandedAxe|TwoHandedPolearm | peasant_2haxe_1_t1|wm_gondor_spear | 29.9 | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 470 | C | [Mordor] Morannon Spearman | morannon_spearman | 33.9 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a02 | 23.6 | False | Offensive Melee | mordor | 21.0 | main_or_minor_line |
| 471 | C | [Gondor] Belfalas Infantry | gondor_bel_infantry | 33.9 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 36.6 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 472 | C | [Gondor] Anórien Archer | gondor_ano_archer | 33.8 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 26.8 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 473 | C | [Goblin] Militia Veteran Spearman | goblin_militia_veteran_spearman | 33.7 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a01|wm_gundabad_spear_a02|wm_gundabad_spear_a03 | 24.9 | False | Defensive Troops | goblin | 16.0 | special_or_unlinked |
| 474 | C | [Isengard] Orc Reaver | isengard_orc_reaver | 33.6 | 75.7 | OneHandedSword | isengard_1h_sword_a | 36.8 | False | Defensive Troops | isengard | 21.0 | main_or_minor_line |
| 475 | C | [Gondor] Ringlo Vale Guardsman | gondor_ring_guardsman | 33.4 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 33.2 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 476 | C | [Gondor] Pelargir Skirmisher | gondor_pel_skirmisher | 33.4 | 82.0 | TwoHandedPolearm | imperial_throwing_spear_1_t4 | 33.2 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 477 | C | [Gondor] Linhir Footman | gondor_lin_footman | 33.4 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 33.2 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 478 | C | [Gondor] Lebennin Veteran Archer | gondor_leb_vet_archer | 33.3 | 75.7 | OneHandedSword | wm_pelargir_sword_a02 | 23.1 | False | Ranged Troops | gondor | 26.0 | main_or_minor_line |
| 479 | C | [Gondor] Lossarnach Noble Veteran | gondor_loss_noble_veteran | 33.3 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_b | 34.0 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 480 | C | [Gundabad] Despoiler of the Vale | gundabad_despoiler_of_the_vale | 33.3 | 70.1 | Mace | wm_gundabad_mace_a02 | 30.9 | True | Ranged Troops | gundabad | 26.0 | main_or_minor_line |
| 481 | C | [Umbar] Beruthiel's Rangers | umbar_elite_root101 | 33.3 | 75.7 | OneHandedSword|TwoHandedAxe | peasant_2haxe_1_t1|wm_gondor_sword_a10 | 18.3 | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 482 | C | [Harad] Militia Spearman | harad_militia_spearman | 33.1 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 17.0 | False | Defensive Troops | aserai | 11.0 | special_or_unlinked |
| 483 | C | [Harad] Militia Veteran Spearman | harad_militia_veteran_spearman | 33.1 | 82.0 | TwoHandedPolearm | khuzait_lance_2_t4 | 17.8 | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 484 | C | Mordor Militia Spearman | mordor_militia_spearman | 33.0 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a01|wm_mordor_set1_polearm_a02|wm_mordor_set1_polearm_a03 | 14.5 | False | Defensive Troops | mordor | 11.0 | special_or_unlinked |
| 485 | C | [Rhûn] Far-Rhun Infantry | far_rhun_infantry | 32.7 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 30.4 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 486 | C | [Dunland] Wild-man Swordman | dunland_veteran_swordman | 32.6 | 75.7 | OneHandedSword | battania_sword_4_t4 | 29.4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 487 | C | [Rhûn] Balcoth Axeman | balcoth_axeman | 32.5 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 28.3 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 488 | C | [Isengard] Orc Warg-Rider Overseer | orc_warg_overseer | 32.4 | 82.0 | TwoHandedPolearm | isengard_spear_a | 37.0 | True | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 489 | C | [Harad] Initiate of the Sand Blades | harad_sandblade | 32.4 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 50.1 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 490 | C | [Erebor] Bowman | erebor_reg_bowman | 32.3 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_b|sm_dwarf_erebor_1h_axe_c | 18.9 | False | Ranged Troops | erebor | 26.0 | main_or_minor_line |
| 491 | C | [Goblin] Militia Spearman | goblin_militia_spearman | 32.3 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a01|wm_gundabad_spear_a02|wm_gundabad_spear_a03 | 15.8 | False | Defensive Troops | goblin | 11.0 | special_or_unlinked |
| 492 | C | [Rohan] Edoras Veteran Swordsman | rohan_edoras_veteran_swordsman | 32.2 | 75.7 | OneHandedSword | wm_rohan_ws_sword_a02|wm_rohan_ws_sword_a03 | 37.8 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 493 | C | [Rhûn] Far-Rhun Horseman | far_rhun_horseman | 32.2 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 35.8 | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 494 | C | [Dunland] Turch-lûth Goreblade | dunland_boar_spearman | 32.0 | 82.0 | TwoHandedPolearm | dunland_caerdh_spear_a | 35.3 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 495 | C | [Rohan] King's Rider | rohan_edoras_golden_hall_rider | 32.0 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a03 | 46.5 | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 496 | C | [Gundabad] Pale Uruk Impaler | gundabad_guard | 31.9 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a03 | 21.4 | False | Offensive Melee | gundabad | 21.0 | main_or_minor_line |
| 497 | C | [Dunland] Draig-lûth Firebolt | dunland_dragon_firebolt | 31.9 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_c | 34.8 | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 498 | C | [Rhûn] Loke-Rim Archer | loke_rim_archer | 31.8 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 34.9 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 499 | C | [Dunland] Cigfran-lûth Ranger | dunland_raven_ranger | 31.8 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 34.2 | False | Ranged Troops | empire | 26.0 | main_or_minor_line |
| 500 | C | [Rohan] West Emnet Horseman | rohan_westemnet_veteran_rider | 31.8 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a02 | 45.6 | True | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 501 | C | [Isengard] Uruk-Hai Feller | urukhai_feller | 31.7 | 73.3 | TwoHandedAxe | isengard_2h_axe_a | 33.4 | False | Offensive Melee | isengard | 21.0 | main_or_minor_line |
| 502 | C | [Mordor] Black Uruk Warrior | mordor_uruk_warrior | 31.7 | 75.7 | OneHandedSword | sm_uruk_sword_a|sm_uruk_sword_c|sm_uruk_sword_d|sm_uruk_sword_f | 25.1 | False | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 503 | C | [Rhûn] Sagarûn Skirmisher | sagarun_skirmisher | 31.6 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 33.2 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 504 | C | [Isengard] Orc Warg Raider | isengard_orc_warg_raider_v2 | 31.6 | 82.0 | TwoHandedPolearm | isengard_spear_a | 30.9 | True | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 505 | C | [Gundabad] Archer | gundabad_archer | 31.5 | 75.7 | OneHandedSword | wm_gundabad_sword_a03 | 33.0 | False | Ranged Troops | gundabad | 26.0 | main_or_minor_line |
| 506 | C | [Rhûn] Kharaghûl Rider | kharaghul_rider | 31.5 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 30.0 | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 507 | C | [Mirkwood] Militia Veteran Archer | mirkwood_militia_veteran_archer | 31.4 | 75.7 | OneHandedSword | mirkwood_sword_a01 | 20.9 | False | Ranged Troops | mirkwood | 16.0 | special_or_unlinked |
| 508 | C | [Mordor] Orc Reaver | mordor_orc_reaver | 31.3 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a01 | 29.3 | False | Offensive Melee | mordor | 21.0 | main_or_minor_line |
| 509 | C | [Misty Mountains] Orc Impaler | mistymountainorcs_guard | 31.2 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a03 | 20.8 | False | Offensive Melee | mistymountainorcs | 21.0 | main_or_minor_line |
| 510 | C | [Isengard] Orc Slayer | isengard_orc_slayer | 31.2 | 73.3 | TwoHandedAxe | isengard_2h_axe_a | 29.3 | False | Offensive Melee | isengard | 21.0 | main_or_minor_line |
| 511 | C | [Misty Mountains] Archer | mistymountainorcs_archer | 31.0 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a02 | 29.0 | False | Ranged Troops | mistymountainorcs | 26.0 | main_or_minor_line |
| 512 | C | [Harad] Spear Guard | harad_spearguard | 31.0 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 28.4 | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 513 | C | [Rhûn] Easterling Swordsman | easterling_swordsman_new | 30.9 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 28.3 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 514 | C | [Erebor] Longbeard | erebor_noble_longbeard | 30.9 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_b | 31.6 | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 515 | C | [Rivendell] Militia Veteran Archer | rivendell_militia_veteran_archer | 30.9 | 75.7 | OneHandedSword | wm_rivendell_sword_a01|wm_rivendell_sword_a02|wm_rivendell_sword_a02_silver | 27.7 | False | Ranged Troops | rivendell | 16.0 | special_or_unlinked |
| 516 | C | [Gondor] Harondor Guardsman | gondor_har_guardsman | 30.9 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 39.8 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 517 | C | [Mirkwood] Militia Archer | mirkwood_militia_archer | 30.7 | 75.7 | OneHandedSword | mirkwood_sword_a01 | 20.6 | False | Ranged Troops | mirkwood | 11.0 | special_or_unlinked |
| 518 | C | [Rohan] Westfold Veteran Axeman | rohan_westfold_veteran_axeman | 30.5 | 73.3 | OneHandedAxe | vlandia_axe_2_t4 | 35.8 | False | Defensive Troops | vlandia | 21.0 | main_or_minor_line |
| 519 | C | [Rhûn] Wainrider Veteran Archer | wainrider_veteran_archer | 30.5 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 24.6 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 520 | C | [Rhûn] Easterling Veteran Archer | easterling_veteran_archer_new | 30.5 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 24.6 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 521 | C | [Harad] Viper | harad_vipereye | 30.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 12.2 | False | Ranged Troops | aserai | 26.0 | main_or_minor_line |
| 522 | C | [Gondor] Serelond Pikeman | gondor_ser_pikeman | 30.4 | 54.3 | Pike | fine_pike_t4 | 32.9 | False | Offensive Melee | gondor | 26.0 | main_or_minor_line |
| 523 | C | [Gondor] Anfalas Guardsman | gondor_anf_guardsman | 30.3 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 35.1 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 524 | C | [Gondor] Osgiliath Skirmisher | gondor_osg_skirmisher | 30.2 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 34.8 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 525 | C | [Dol Guldur] Shadow Initiate | dg_khamul_shadow_initiate | 30.2 | 70.1 | Mace | sm_dg_khml_1h_mace_a | 30.0 | False | Defensive Troops | dolguldur | 21.0 | main_or_minor_line |
| 526 | C | [Gondor] Arndir Noble | gondor_arn_noble_t4 | 30.0 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 33.2 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 527 | C | [Gondor] Methir Noble | gondor_met_noble | 30.0 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 33.2 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 528 | C | [Gondor] Anórien Guardsman | gondor_ano_guardsman | 30.0 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 33.2 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 529 | C | [Gondor] Calembel Noble | gondor_cal_noble | 30.0 | 75.7 | OneHandedSword | wm_gondor_lamedon_1h_sword_a | 33.2 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 530 | C | [Gondor] Cair Andros Veteran | gondor_ca_veteran | 30.0 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 33.0 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 531 | C | [Dale] Dalian Riverman | dale_riverman | 30.0 | 82.0 | TwoHandedPolearm | dale_spear_b|dale_winged_spear_a | 44.6 | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 532 | C | [Erebor] Company | erebor_reg_company | 30.0 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_b|sm_dwarf_erebor_1h_axe_c | 23.4 | False | Defensive Troops | erebor | 21.0 | main_or_minor_line |
| 533 | C | [Gondor] Lebennin Infantry | gondor_leb_infantry | 29.9 | 75.7 | OneHandedSword | wm_pelargir_sword_a02 | 32.6 | False | Skirmishers | gondor | 21.0 | main_or_minor_line |
| 534 | C | [Rhûn] Black Sun Raider | black_sun_raider | 29.9 | 73.3 | OneHandedAxe | sm_rh_drag_1h_axe_a | 19.3 | False | Offensive Melee | khuzait | 21.0 | main_or_minor_line |
| 535 | C | [Gondor] Dol Amroth Footman | gondor_da_footman | 29.8 | 75.7 | OneHandedSword | wm_gondor_sword_a01 | 31.7 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 536 | C | [Rhûn] Sagarûn Crossbowman | sagarun_crossbowman | 29.4 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 15.9 | False | Ranged Troops | khuzait | 26.0 | main_or_minor_line |
| 537 | C | [Dunland] Uch-lûth Bodyguard | dunland_ox_guard | 29.2 | 54.3 | Pike | thamaskene_pike_t4 | 40.6 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 538 | C | [Rohan] Westfold Heavy Axeman | rohan_westfold_2h_axeman | 29.1 | 73.3 | TwoHandedAxe | sturgia_2haxe_1_t4 | 24.3 | False | Offensive Melee | vlandia | 21.0 | main_or_minor_line |
| 539 | C | [Rohan] Wold Veteran Horse Rider | rohan_wold_veteran_horse_archer | 29.1 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 50.1 | True | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 540 | C | [Gondor] Lossarnach Veteran Axebearer | gondor_loss_vet_axebearer | 29.0 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_a|wm_gondor_lossarnach_1h_axe_b|wm_gondor_lossarnach_1h_axe_black_ash_a|wm_gondor_lossarnach_1h_axe_silver_a|wm_gondor_lossarnach_1h_axe_silver_b|wm_gondor_lossarnach_1h_axe_silver_full_a | 35.1 | False | Defensive Troops | gondor | 21.0 | main_or_minor_line |
| 541 | C | [Rhûn] Dragon-Wrath Acolyte | dragon_wrath_acolyte | 29.0 | 70.1 | Mace | sm_rh_drag_1h_mace_a | 26.6 | False | Defensive Troops | khuzait | 21.0 | main_or_minor_line |
| 542 | C | [Gondor] Serelond Veteran | gondor_ser_veteran | 28.9 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 24.6 | False | Offensive Melee | gondor | 21.0 | main_or_minor_line |
| 543 | C | [Goblin] Archer | goblin_archer | 28.6 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a02 | 29.0 | False | Ranged Troops | goblin | 26.0 | main_or_minor_line |
| 544 | C | [Rohan] Meduseld Spearman | rohan_edoras_meduseld_spearman | 28.4 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 32.2 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 545 | C | [Rohan] West-March Spearman | rohan_westmarches_spearman | 28.4 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a02 | 32.7 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 546 | C | [Dale] Lake-Town Patrolman | dale_footman | 28.3 | 82.0 | TwoHandedPolearm | dale_halberd_a|dale_war_spear_a | 31.8 | False | Offensive Melee | sturgia | 16.0 | main_or_minor_line |
| 547 | C | [Gundabad] Pale Uruk Raider | gundabad_fighter | 28.3 | 73.3 | OneHandedAxe | wm_gundabad_axe_a02 | 29.6 | False | Defensive Troops | gundabad | 21.0 | main_or_minor_line |
| 548 | C | [Dale] Dalian Militia | dale_man_at_arms | 28.2 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_spear_b|dale_sword_b | 39.0 | False | Defensive Troops | sturgia | 16.0 | main_or_minor_line |
| 549 | C | [Rivendell] Militia Archer | rivendell_militia_archer | 28.1 | 75.7 | OneHandedSword | wm_rivendell_sword_a01|wm_rivendell_sword_a01_silver|wm_rivendell_sword_a02 | 12.0 | False | Ranged Troops | rivendell | 11.0 | special_or_unlinked |
| 550 | C | Rhun Veteran Caravan Guard | veteran_caravan_guard_rhun | 27.9 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_b | 28.6 | False | Defensive Troops | khuzait | 21.0 | special_or_unlinked |
| 551 | C | [Harad] Footman | harad_footman | 27.9 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 28.4 | False | Defensive Troops | aserai | 21.0 | main_or_minor_line |
| 552 | C | [Gondor] Lossarnach Axe-Thrower | gondor_loss_axe_thrower | 27.9 | 73.3 | ThrowingAxe | highland_throwing_axe_1_t2|northern_throwing_axe_1_t1|southern_throwing_axe_1_t4|western_throwing_axe_1_t1|woodland_throwing_axe_1_t1 | 26.5 | False | Offensive Melee | gondor | 21.0 | main_or_minor_line |
| 553 | C | [Misty Mountains] Orc Raider | mistymountainorcs_fighter | 27.9 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01 | 31.1 | False | Defensive Troops | mistymountainorcs | 21.0 | main_or_minor_line |
| 554 | C | [Umbar] Rozadan Halberdiers | umbar_elite_root01 | 27.7 | 73.3 | Pike|TwoHandedAxe | isengard_pike_b|peasant_2haxe_1_t1 | 25.0 | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 555 | C | [Goblin] Goblin Impaler | goblin_guard | 27.5 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a03 | 20.8 | False | Offensive Melee | goblin | 21.0 | main_or_minor_line |
| 556 | C | [Mordor] Orc Infantry | mordor_orc_infantry | 27.4 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 36.8 | False | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 557 | C | Isengard Veteran Caravan Guard | veteran_caravan_guard_isengard | 27.4 | 75.7 | OneHandedSword | isengard_1h_sword_b | 23.9 | False | Defensive Troops | isengard | 21.0 | special_or_unlinked |
| 558 | C | [Dunland] Blaidd-lûth Raider | dunland_wolf_raider | 27.4 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_a | 34.6 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 559 | C | [Dol Guldur] Warg Tracker | dg_warg_scout | 27.4 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a03 | 13.5 | True | Defensive Troops | dolguldur | 16.0 | main_or_minor_line |
| 560 | C | [Dale] Lake-Town Watchman | dale_lake_town_skirmisher | 27.2 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_sword_b|dale_war_spear_a | 23.0 | False | Offensive Melee | sturgia | 16.0 | main_or_minor_line |
| 561 | C | [Harad] Rider of the Golden Veil | harad_horsearcher | 27.1 | 75.7 | OneHandedSword | aserai_sword_5_t4 | 42.7 | True | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 562 | C | [Mordor] Morannon Infantry | morannon_infantry | 26.7 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a01 | 31.1 | False | Defensive Troops | mordor | 21.0 | main_or_minor_line |
| 563 | C | [Dunland] Arth-lûth Chosen | dunland_bear_chosen | 26.6 | 73.3 | TwoHandedAxe | dunland_caerdh_axe_2h_a | 28.6 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 564 | C | Harad Veteran Caravan Guard | veteran_caravan_guard_harad | 26.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 17.8 | False | Defensive Troops | aserai | 21.0 | special_or_unlinked |
| 565 | C | [Gundabad] Scout | gundabad_scout | 25.6 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a02 | 21.9 | True | Ranged Troops | gundabad | 21.0 | main_or_minor_line |
| 566 | C | [Rhûn] Kharaghûl Horse Scout | kharaghul_horse_scout | 25.6 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 42.9 | True | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 567 | C | [Ironpass] Warrior | ironpass_warrior | 25.6 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 33.9 | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 568 | C | [Harad] Camel Scout | harad_camelscout | 25.4 | 82.0 | TwoHandedPolearm | southern_spear_3_t4 | 34.1 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 569 | C | [Dol Guldur] Orc Warrior | dg_orc_warrior | 25.0 | 82.0 | OneHandedSword|TwoHandedPolearm | wm_dol_goldur_1h_sword_a01|wm_dol_goldur_halberd_a01|wm_dol_goldur_halberd_a02|wm_dol_goldur_halberd_a03|wm_dol_goldur_halberd_a04 | 24.2 | False | Defensive Troops | dolguldur | 16.0 | main_or_minor_line |
| 570 | C | [Iron Hills] Noble | iron_hills_noble | 25.0 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a | 41.5 | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 571 | C | [Goblin] Goblin Raider | goblin_fighter | 24.6 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01 | 31.1 | False | Defensive Troops | goblin | 21.0 | main_or_minor_line |
| 572 | C | [Gondor] Pinnath Gelin Archer | gondor_pg_archer | 24.3 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 26.5 | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 573 | C | [Dol Guldur] Goblin Skirmisher | dg_goblin_skirmisher | 24.2 | 82.0 | OneHandedSword|TwoHandedMace|TwoHandedPolearm | wm_dol_goldur_1h_sword_a03|wm_dol_goldur_2h_mace_a03|wm_dol_goldur_2h_mace_a04|wm_dol_goldur_halberd_a01|wm_dol_goldur_halberd_a02 | 16.9 | False | Offensive Melee | dolguldur | 16.0 | main_or_minor_line |
| 574 | C | [Mordor] Nurn Warg Reaver | mordor_warg_reaver | 24.0 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a03 | 23.4 | True | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 575 | C | [Iron Hills] Scout | iron_hills_noble_scout | 24.0 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a | 33.7 | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 576 | C | [Dol Guldur] Uruk Bowman | dg_uruk_bowman | 23.9 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a02 | 33.2 | False | Ranged Troops | dolguldur | 21.0 | main_or_minor_line |
| 577 | C | [Dol Guldur] Orc Scout | dg_orc_scout | 23.8 | 75.7 | OneHandedSword|TwoHandedMace | wm_dol_goldur_1h_sword_a01|wm_dol_goldur_1h_sword_a02|wm_dol_goldur_1h_sword_a03|wm_dol_goldur_2h_mace_a03|wm_dol_goldur_2h_mace_a04 | 31.4 | False | Ranged Troops | dolguldur | 21.0 | main_or_minor_line |
| 578 | C | [Dol Guldur] Uruk Warrior | dg_uruk_veteran_warrior | 23.8 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a02 | 37.3 | False | Defensive Troops | dolguldur | 16.0 | main_or_minor_line |
| 579 | C | [Iron Hills] Skirmisher | iron_hills_reg_skirmisher | 23.7 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a | 21.1 | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 580 | C | [Iron Hills] Militia | iron_hills_reg_militia | 23.6 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a|sm_dwarf_iron_sword_b | 25.0 | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 581 | C | [Gondor] Harondor Veteran Skirmisher | gondor_har_vet_skirmisher | 23.2 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 39.8 | False | Skirmishers | gondor | 21.0 | main_or_minor_line |
| 582 | C | [Rhûn] Wain Youngblood | wain_youngblood | 23.1 | 82.0 | TwoHandedPolearm | khuzait_lance_1_t3 | 17.4 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 583 | C | [Rohan] East Emnet Lance Rider | rohan_eastemnet_lance_rider | 22.8 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01 | 40.4 | True | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 584 | C | [Isengard] Uruk-Hai Warrior | urukhai_warrior | 22.8 | 75.7 | OneHandedSword | isengard_1h_sword_a | 36.8 | False | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 585 | C | [Dunland] Tribal Spearman | dunland_spearman | 22.8 | 82.0 | TwoHandedPolearm | western_spear_3_t3 | 14.8 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 586 | C | [Dale] Dalian Veteran Crossbowman | dale_veteran_crossbowman | 22.7 | 75.7 | OneHandedSword | dale_sword_a|dale_sword_b | 47.7 | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 587 | C | [Gondor] Belfalas Archer | gondor_bel_archer | 22.6 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 35.1 | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 588 | C | [Isengard] Militia Spearman | isengard_militia_spearman | 22.6 | 54.3 | Pike | isengard_pike_a|isengard_pike_b | 18.2 | False | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 589 | C | [Ironpass] Arbalest | ironpass_arbalest | 22.3 | 73.3 | TwoHandedAxe | sm_dwarf_erebor_axe_2h_a|sm_dwarf_iron_axe_a | 32.8 | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 590 | C | [Dale] Dalian Bowman | dale_longbowman | 22.2 | 75.7 | OneHandedSword | dale_sword_a|dale_sword_b | 44.3 | False | Ranged Troops | sturgia | 21.0 | main_or_minor_line |
| 591 | C | [Isengard] Orc Marauder | isengard_orc_marauder | 22.1 | 75.7 | OneHandedSword | isengard_1h_sword_a | 31.1 | False | Defensive Troops | isengard | 16.0 | main_or_minor_line |
| 592 | C | Spider Rider | taom_spider_creature | 22.0 | 75.7 | OneHandedSword|TwoHandedAxe | wm_dol_goldur_1h_sword_a02|wm_dol_goldur_1h_sword_a03|wm_dol_goldur_axe_a03 | 14.3 | True | Defensive Troops | dolguldur | 20.0 | special_or_unlinked |
| 593 | C | [Isengard] Uruk-Hai Arbalest | urukhai_arbalest | 21.8 | 75.7 | OneHandedSword | isengard_1h_sword_b | 28.9 | False | Ranged Troops | isengard | 21.0 | main_or_minor_line |
| 594 | C | [Isengard] Uruk-Hai Tracker | urukhai_tracker | 21.8 | 75.7 | OneHandedSword | isengard_1h_sword_b | 28.9 | False | Ranged Troops | isengard | 21.0 | main_or_minor_line |
| 595 | C | Dol Guldur Militia Veteran Archer | dolguldur_militia_veteran_archer | 21.7 | 75.7 | Mace|OneHandedSword | wm_dol_goldur_1h_mace_a02|wm_dol_goldur_1h_sword_a02|wm_dol_goldur_1h_sword_a03 | 15.0 | False | Ranged Troops | dolguldur | 16.0 | special_or_unlinked |
| 596 | C | [Rhûn] Far-Rhun Footman | far_rhun_footman | 21.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 28.3 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 597 | C | [Rhûn] Sagarûn Watchman | sagarun_watchman | 21.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 27.6 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 598 | C | [Mordor] Black Uruk Skirmisher | mordor_uruk_skirmisher | 21.7 | 75.7 | OneHandedSword | sm_uruk_sword_b | 23.2 | False | Ranged Troops | mordor | 21.0 | main_or_minor_line |
| 599 | C | [Gondor] Linhir Noble | gondor_lin_noble | 21.6 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 31.5 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 600 | C | [Gondor] Ringlo Vale Footman | gondor_ring_footman | 21.6 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 31.5 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 601 | C | [Umbar] Rozadan Bowmen | umbar_elite_root10 | 21.4 | 75.7 | OneHandedSword|TwoHandedAxe | peasant_2haxe_1_t1|wm_gondor_sword_a09 | 21.2 | False | Ranged Troops | umbar | 21.0 | main_or_minor_line |
| 602 | C | [Harad] Sword Fighter | harad_swordfighter | 21.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 25.7 | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 603 | C | [Gondor] Pinnath Gelin Footman | gondor_pg_footman | 21.3 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 29.0 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 604 | C | [Erebor] Ranger | erebor_noble_ranger | 21.3 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_c | 32.4 | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 605 | C | [Gondor] Anórien Bowman | gondor_ano_bowman | 21.3 | 75.7 | OneHandedSword | wm_gondor_sword_a04 | 24.6 | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 606 | C | [Gondor] Blackroot Vale Scout | gondor_brv_scout | 21.3 | 75.7 | OneHandedSword | wm_gondor_sword_a05 | 24.6 | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 607 | C | [Gondor] Tolfalas Crossbowman | gondor_tol_crossbowman | 21.3 | 75.7 | OneHandedSword | wm_gondor_sword_a04 | 24.6 | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 608 | C | [Dol Guldur] Goblin Archer | dg_goblin_archer | 21.2 | 70.1 | Mace|TwoHandedMace | wm_dol_goldur_1h_mace_a01|wm_dol_goldur_1h_mace_a02|wm_dol_goldur_1h_mace_a03|wm_dol_goldur_2h_mace_a01|wm_dol_goldur_2h_mace_a04 | 31.6 | False | Ranged Troops | dolguldur | 21.0 | main_or_minor_line |
| 609 | C | Dol Guldur Militia Archer | dolguldur_militia_archer | 21.1 | 75.7 | Mace|OneHandedSword | wm_dol_goldur_1h_mace_a01|wm_dol_goldur_1h_sword_a01|wm_dol_goldur_1h_sword_a02 | 11.1 | False | Ranged Troops | dolguldur | 11.0 | special_or_unlinked |
| 610 | C | [Rohan] Edoras Swordsman | rohan_edoras_swordsman | 20.9 | 75.7 | OneHandedSword | wm_rohan_ws_sword_a02|wm_rohan_ws_sword_a03 | 32.9 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 611 | C | [Rhûn] Balcoth Footman | balcoth_footman | 20.9 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 21.4 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 612 | C | [Rhûn] Easterling Footman | easterling_footman_new | 20.9 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 21.4 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 613 | C | [Gondor] Lebennin Archer | gondor_leb_archer | 20.8 | 75.7 | OneHandedSword | wm_pelargir_sword_a02 | 21.4 | False | Ranged Troops | gondor | 21.0 | main_or_minor_line |
| 614 | C | [Gondor] Lossarnach Noble | gondor_loss_noble | 20.6 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_a | 28.1 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 615 | C | [Erebor] Militia Veteran Archer | erebor_militia_veteran_archer | 20.6 | 73.3 | OneHandedAxe|TwoHandedMace | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_c|sm_dwarf_erebor_mace_a | 16.6 | False | Ranged Troops | erebor | 16.0 | special_or_unlinked |
| 616 | C | [Dunland] Uch-lûth Pikeman | dunland_ox_pikeman | 20.5 | 54.3 | Pike | vlandia_pike_1_t5 | 32.7 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 617 | C | [Mordor] Black Uruk Fighter | mordor_uruk_fighter | 20.4 | 75.7 | OneHandedSword | sm_uruk_sword_b | 25.4 | False | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 618 | C | [Erebor] Skirmisher | erebor_reg_skirmisher | 20.4 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_b|sm_dwarf_erebor_1h_axe_d | 18.6 | False | Ranged Troops | erebor | 21.0 | main_or_minor_line |
| 619 | C | [Rhûn] Darkhûn Footman | darkhun_footman | 20.4 | 73.3 | OneHandedAxe | sm_dg_khml_1h_axe_a | 25.8 | False | Offensive Melee | khuzait | 16.0 | main_or_minor_line |
| 620 | C | [Rohan] Wold Horse Archer | rohan_wold_horse_archer | 20.2 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 45.6 | True | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 621 | C | [Isengard] Militia Veteran Archer | isengard_militia_veteran_archer | 20.1 | 75.7 | OneHandedSword | isengard_1h_sword_b | 12.5 | False | Ranged Troops | isengard | 16.0 | main_or_minor_line |
| 622 | C | [Dunland] Tribal Swordsman | dunland_swordsman | 20.0 | 75.7 | OneHandedSword | empire_sword_5_t4 | 14.8 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 623 | D | [Dale] Dalian Levy | dale_squire | 19.9 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_spear_a|dale_sword_c | 31.0 | False | Defensive Troops | sturgia | 11.0 | main_or_minor_line |
| 624 | D | [Dale] Lake-Town Militia | dale_militia | 19.9 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_spear_a|dale_sword_c | 31.0 | False | Defensive Troops | sturgia | 11.0 | main_or_minor_line |
| 625 | D | [Harad] Spear Fighter | harad_spearfighter | 19.9 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 25.7 | False | Defensive Troops | aserai | 16.0 | main_or_minor_line |
| 626 | D | [Gondor] Gondor Veteran Militia Archer | gondor_militia_veteran_archer | 19.9 | 75.7 | OneHandedSword | wm_gondor_sword_a02 | 13.6 | False | Ranged Troops | gondor | 16.0 | special_or_unlinked |
| 627 | D | [Isengard] Orc Butcher | isengard_orc_butcher | 19.9 | 73.3 | TwoHandedAxe | isengard_2h_axe_a | 21.9 | False | Offensive Melee | isengard | 16.0 | main_or_minor_line |
| 628 | D | [Gondor] Anórien Archer Militia | gondor_ano_archer_militia | 19.8 | 75.7 | OneHandedSword | wm_gondor_sword_a02 | 12.9 | False | Ranged Troops | gondor | 11.0 | main_or_minor_line |
| 629 | D | [Dale] Veteran Militia Archer | dale_militia_veteran_archer | 19.7 | 75.7 | OneHandedSword | dale_sword_b | 24.7 | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 630 | D | [Rohan] Westfolders | rohan_westfold_axeman | 19.7 | 73.3 | OneHandedAxe | sturgia_axe_3_t3 | 32.7 | False | Defensive Troops | vlandia | 16.0 | main_or_minor_line |
| 631 | D | [Isengard] Militia Archer | isengard_militia_archer | 19.7 | 75.7 | OneHandedSword | isengard_1h_sword_b | 11.5 | False | Ranged Troops | isengard | 11.0 | main_or_minor_line |
| 632 | D | [Harad] Marksman | harad_marksman | 19.4 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 22.3 | False | Ranged Troops | aserai | 21.0 | main_or_minor_line |
| 633 | D | [Dunland] Draig-lûth Crossbowman | dunland_dragon_crossbowman | 19.4 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_c | 30.1 | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 634 | D | [Erebor] Noble | erebor_noble | 19.4 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_b|sm_dwarf_erebor_1h_axe_c | 28.8 | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 635 | D | [Rhûn] Black Sun Footman | black_sun_footman | 19.3 | 73.3 | OneHandedAxe | sm_rh_drag_1h_axe_a | 17.8 | False | Offensive Melee | khuzait | 16.0 | main_or_minor_line |
| 636 | D | [Gondor] Harondor Footman | gondor_har_footman | 19.2 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 32.6 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 637 | D | [Gondor] Anórien Footman | gondor_ano_footman | 19.1 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 31.7 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 638 | D | [Gondor] Lossarnach Axebearer | gondor_loss_axebearer | 19.1 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_a|wm_gondor_lossarnach_1h_axe_b|wm_gondor_lossarnach_1h_axe_black_ash_a|wm_gondor_lossarnach_1h_axe_silver_a|wm_gondor_lossarnach_1h_axe_silver_b|wm_gondor_lossarnach_1h_axe_silver_full_a | 27.4 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 639 | D | [Gondor] Anfalas Footman | gondor_anf_footman | 19.1 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 31.5 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 640 | D | [Gondor] Arndir Noble | gondor_arn_noble | 19.1 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 31.5 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 641 | D | [Rhûn] Loke-Rim Initiate | loke_rim_initiate | 19.0 | 70.1 | Mace | sm_rh_loke_1h_mace_a | 26.6 | False | Defensive Troops | khuzait | 16.0 | main_or_minor_line |
| 642 | D | [Gondor] Belfalas Soldier | gondor_bel_soldier | 18.9 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 30.0 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 643 | D | [Gondor] Dol Amroth Noble | gondor_da_noble | 18.9 | 75.7 | OneHandedSword | wm_gondor_sword_a01 | 29.9 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 644 | D | [Erebor] Militia Archer | erebor_militia_archer | 18.9 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_b|sm_dwarf_erebor_1h_axe_d|sm_dwarf_erebor_1h_axe_e | 10.2 | False | Ranged Troops | erebor | 11.0 | special_or_unlinked |
| 645 | D | [Mordor] Orc Archer | mordor_orc_archer | 18.8 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 29.0 | False | Ranged Troops | mordor | 21.0 | main_or_minor_line |
| 646 | D | [Dunland] Cigfran-lûth Archer | dunland_raven_archer | 18.8 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 24.9 | False | Ranged Troops | empire | 21.0 | main_or_minor_line |
| 647 | D | [Dale] Militia Archer | dale_militia_archer | 18.6 | 75.7 | OneHandedSword | dale_sword_c | 15.8 | False | Ranged Troops | sturgia | 6.0 | main_or_minor_line |
| 648 | D | [Rhûn] Loke-Rim Bowman | loke_rim_bowman | 18.6 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 26.9 | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 649 | D | Rhun Caravan Guard | caravan_guard_rhun | 18.4 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_b | 26.2 | False | Defensive Troops | khuzait | 16.0 | special_or_unlinked |
| 650 | D | [Gondor] Osgiliath Veteran | gondor_osg_veteran | 18.4 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 26.0 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 651 | D | [Isengard] Orc Warg Rider | isengard_orc_warg_rider_v2 | 18.3 | 82.0 | TwoHandedPolearm | isengard_spear_a | 30.6 | True | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 652 | D | [Rhûn] Balcoth Archer | balcoth_archer | 18.1 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 23.1 | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 653 | D | [Rohan] Eastfold Veteran Bowman | rohan_eastfold_veteran_bowman | 18.1 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 24.0 | False | Ranged Troops | vlandia | 21.0 | main_or_minor_line |
| 654 | D | [Harad] Militia Veteran Archer | harad_militia_veteran_archer | 18.1 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 11.2 | False | Ranged Troops | aserai | 16.0 | special_or_unlinked |
| 655 | D | Isengard Caravan Guard | caravan_guard_isengard | 18.1 | 75.7 | OneHandedSword | isengard_1h_sword_b | 23.1 | False | Defensive Troops | isengard | 16.0 | special_or_unlinked |
| 656 | D | [Mordor] Morannon Archer | morannon_archer | 18.0 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 23.4 | False | Ranged Troops | mordor | 21.0 | main_or_minor_line |
| 657 | D | [Misty Mountains] Sentry | mistymountainorcs_sentry | 18.0 | 75.7 | OneHandedSword | wm_gundabad_sword_a02 | 23.4 | False | Ranged Troops | mistymountainorcs | 21.0 | main_or_minor_line |
| 658 | D | [Gundabad] Sentry | gundabad_sentry | 18.0 | 75.7 | OneHandedSword | wm_gundabad_sword_a04 | 23.2 | False | Ranged Troops | gundabad | 21.0 | main_or_minor_line |
| 659 | D | [Erebor] Militia | erebor_reg_militia | 18.0 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_b|sm_dwarf_erebor_1h_axe_c | 14.9 | False | Defensive Troops | erebor | 16.0 | main_or_minor_line |
| 660 | D | [Gondor] Serelond Noble | gondor_ser_noble | 18.0 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 23.1 | False | Offensive Melee | gondor | 16.0 | main_or_minor_line |
| 661 | D | [Dunland] Militia Veteran Archer | dunland_militia_veteran_archer | 18.0 | 75.7 | OneHandedAxe|OneHandedSword | battania_axe_1_t2|empire_sword_5_t4|sturgia_axe_2_t2 | 12.8 | False | Ranged Troops | empire | 16.0 | special_or_unlinked |
| 662 | D | [Harad] Militia Archer | harad_militia_archer | 18.0 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 10.0 | False | Ranged Troops | aserai | 11.0 | special_or_unlinked |
| 663 | D | [Rhûn] Easterling Archer | easterling_archer_new | 17.9 | 75.7 | OneHandedSword | khuzait_sword_3_t3 | 22.2 | False | Ranged Troops | khuzait | 21.0 | main_or_minor_line |
| 664 | D | [Rohan] West Emnet Rider | rohan_westemnet_rider | 17.9 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01 | 40.4 | True | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 665 | D | Mordor Militia Veteran Archer | mordor_militia_veteran_archer | 17.8 | 75.7 | OneHandedAxe|OneHandedSword | wm_mordor_set1_axe_a02|wm_mordor_set1_sword_a01|wm_mordor_set1_sword_a02 | 15.6 | False | Ranged Troops | mordor | 16.0 | special_or_unlinked |
| 666 | D | [Rohan] Militia Veteran Archer | rohan_militia_veteran_archer | 17.8 | 75.7 | OneHandedSword | vlandia_sword_2_t3 | 18.9 | False | Ranged Troops | vlandia | 16.0 | special_or_unlinked |
| 667 | D | [Isengard] Orc Warg-Rider Scout | orc_warg_scout | 17.7 | 82.0 | TwoHandedPolearm | isengard_spear_a | 26.1 | True | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 668 | D | [Misty Mountains] Militia Veteran Archer | mistymountainorcs_militia_veteran_archer | 17.5 | 75.7 | Mace|OneHandedAxe|OneHandedSword | wm_dol_goldur_1h_sword_a01|wm_gundabad_axe_a01|wm_gundabad_mace_a02 | 18.4 | False | Ranged Troops | mistymountainorcs | 16.0 | special_or_unlinked |
| 669 | D | [Gundabad] Pale Uruk Brawler | gundabad_grunt | 17.4 | 73.3 | OneHandedAxe | wm_gundabad_axe_a02|wm_gundabad_axe_a03 | 21.7 | False | Offensive Melee | gundabad | 16.0 | main_or_minor_line |
| 670 | D | [Umbar] Adûnaim Footmen | umbar_elite_root0 | 17.4 | 75.7 | OneHandedSword|TwoHandedAxe | peasant_2haxe_1_t1|wm_gondor_lamedon_1h_sword_a | 15.2 | False | Skirmishers | umbar | 16.0 | main_or_minor_line |
| 671 | D | [Gondor] Lebennin Skirmisher | gondor_leb_skirmisher | 17.4 | 75.7 | OneHandedSword | wm_pelargir_sword_a01 | 18.3 | False | Defensive Troops | gondor | 16.0 | main_or_minor_line |
| 672 | D | Harad Caravan Guard | caravan_guard_harad | 17.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 17.8 | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 673 | D | [Gondor] Cair Andros Noble | gondor_ca_noble | 17.3 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 17.4 | False | Offensive Melee | gondor | 16.0 | main_or_minor_line |
| 674 | D | [Mordor] Orc Impaler | mordor_orc_impaler | 17.3 | 82.0 | TwoHandedPolearm | wm_mordor_set1_polearm_a02 | 23.6 | False | Offensive Melee | mordor | 16.0 | main_or_minor_line |
| 675 | D | [Rhûn] Militia Veteran Archer | rhun_militia_veteran_archer | 17.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 16.5 | False | Ranged Troops | khuzait | 16.0 | main_or_minor_line |
| 676 | D | [Rhûn] Militia Archer | rhun_militia_archer | 17.1 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 15.8 | False | Ranged Troops | khuzait | 11.0 | main_or_minor_line |
| 677 | D | [Dunland] Blaidd-lûth Warrior | dunland_clan_warrior | 16.9 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_a | 34.0 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 678 | D | [Dunland] Turch-lûth Tuskrunner | dunland_boar_warrior | 16.9 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_a | 34.0 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 679 | D | [Gondor] Lamedon Footman | gondor_lam_footman | 16.9 | 100.0 | TwoHandedSword | wm_gondor_lamedon_2h_sword_a | 17.0 | False | Offensive Melee | gondor | 11.0 | main_or_minor_line |
| 680 | D | [Gundabad] Militia Veteran Archer | gundabad_militia_veteran_archer | 16.9 | 75.7 | Mace|OneHandedAxe|OneHandedSword | wm_gundabad_axe_a02|wm_gundabad_mace_a02|wm_gundabad_sword_a01 | 14.7 | False | Ranged Troops | gundabad | 16.0 | special_or_unlinked |
| 681 | D | [Dunland] Militia Archer | dunland_militia_archer | 16.8 | 73.3 | OneHandedAxe | battania_axe_1_t2|small_spurred_axe_t2|sturgia_axe_2_t2 | 6.8 | False | Ranged Troops | empire | 11.0 | special_or_unlinked |
| 682 | D | [Gondor] Lossarnach Skirmisher | gondor_loss_skirmisher | 16.5 | 73.3 | TwoHandedAxe | wm_gondor_lossarnach_2h_axe_a|wm_gondor_lossarnach_2h_axe_b|wm_gondor_lossarnach_2h_axe_black_ash_a|wm_gondor_lossarnach_2h_axe_silver_a|wm_gondor_lossarnach_2h_axe_silver_b|wm_gondor_lossarnach_2h_axe_silver_full_a | 18.8 | False | Skirmishers | gondor | 16.0 | main_or_minor_line |
| 683 | D | Mordor Militia Archer | mordor_militia_archer | 16.4 | 75.7 | OneHandedAxe|OneHandedSword | wm_mordor_set1_axe_a01|wm_mordor_set1_sword_a01|wm_mordor_set1_sword_a02 | 9.3 | False | Ranged Troops | mordor | 11.0 | special_or_unlinked |
| 684 | D | [Rohan] Militia Archer | rohan_militia_archer | 16.4 | 75.7 | OneHandedSword | vlandia_sword_1_t2 | 9.6 | False | Ranged Troops | vlandia | 11.0 | special_or_unlinked |
| 685 | D | [Misty Mountains] Orc Brawler | mistymountainorcs_grunt | 16.4 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01|wm_mordor_set1_axe_a01 | 19.1 | False | Offensive Melee | mistymountainorcs | 16.0 | main_or_minor_line |
| 686 | D | [Rhûn] Kharaghûl Youth | kharaghul_youth | 16.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 30.2 | True | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 687 | D | [Ironpass] Recruit | ironpass_recruit | 16.2 | 82.0 | TwoHandedPolearm | sm_dwarf_erebor_spear_a|sm_dwarf_erebor_spear_b | 32.2 | False | Defensive Troops | erebor | 11.0 | main_or_minor_line |
| 688 | D | [Iron Hills] Recruit | iron_hills_reg_recruit | 15.9 | 75.7 | OneHandedSword | sm_dwarf_iron_sword_a | 24.8 | False | Defensive Troops | erebor | 11.0 | main_or_minor_line |
| 689 | D | [Harad] Youngblood of the Serpent | harad_noble | 15.8 | 82.0 | TwoHandedPolearm | aserai_lance_1_t5 | 50.1 | True | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 690 | D | [Mordor] Morannon Warrior | morannon_warrior | 15.8 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a01 | 29.5 | False | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 691 | D | [Goblin] Sentry | goblin_sentry | 15.6 | 75.7 | OneHandedSword | wm_gundabad_sword_a02 | 23.4 | False | Ranged Troops | goblin | 21.0 | main_or_minor_line |
| 692 | D | [Misty Mountains] Militia Archer | mistymountainorcs_militia_archer | 15.5 | 73.3 | Mace|OneHandedAxe | wm_dol_goldur_1h_mace_a02|wm_gundabad_axe_a01|wm_gundabad_axe_a02 | 10.2 | False | Ranged Troops | mistymountainorcs | 11.0 | special_or_unlinked |
| 693 | D | [Gundabad] Militia Archer | gundabad_militia_archer | 15.4 | 73.3 | Mace|OneHandedAxe | wm_gundabad_axe_a01|wm_gundabad_axe_a02|wm_gundabad_mace_a01 | 9.6 | False | Ranged Troops | gundabad | 11.0 | special_or_unlinked |
| 694 | D | [Dol Guldur] Orc Gnasher | dg_orc_gnasher | 15.3 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a01|wm_dol_goldur_halberd_a02|wm_dol_goldur_halberd_a03|wm_dol_goldur_halberd_a04 | 11.8 | False | Offensive Melee | dolguldur | 11.0 | main_or_minor_line |
| 695 | D | [Goblin] Militia Veteran Archer | goblin_militia_veteran_archer | 15.1 | 75.7 | Mace|OneHandedAxe|OneHandedSword | wm_dol_goldur_1h_sword_a01|wm_gundabad_axe_a01|wm_gundabad_mace_a02 | 18.4 | False | Ranged Troops | goblin | 16.0 | special_or_unlinked |
| 696 | D | [Dol Guldur] Uruk Fighter | dg_uruk_warrior | 15.0 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a03 | 11.3 | False | Offensive Melee | dolguldur | 13.0 | main_or_minor_line |
| 697 | D | [Mordor] Orc Warrior | mordor_orc_warrior | 14.9 | 73.3 | OneHandedAxe | wm_mordor_set1_axe_a01 | 29.5 | False | Defensive Troops | mordor | 16.0 | main_or_minor_line |
| 698 | D | [Isengard] Uruk-Hai Fighter | urukhai_fighter | 14.7 | 75.7 | OneHandedSword | isengard_1h_sword_b | 33.5 | False | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 699 | D | Guard | guard_rivendell | 14.7 | 75.7 | OneHandedSword | wm_rivendell_sword_a02 | 45.0 | False | Defensive Troops | rivendell | 16.0 | special_or_unlinked |
| 700 | D | Guard | guard_mirkwood | 14.5 | 82.0 | TwoHandedPolearm | mirkwood_spear_a01 | 27.9 | False | Defensive Troops | mirkwood | 16.0 | special_or_unlinked |
| 701 | D | Guard | guard_mistymountainorcs | 14.4 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a02 | 27.0 | False | Defensive Troops | mistymountainorcs | 16.0 | special_or_unlinked |
| 702 | D | Guard | guard_goblin | 14.4 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a02 | 27.0 | False | Defensive Troops | goblin | 16.0 | special_or_unlinked |
| 703 | D | [Rohan] Edoras Militia | rohan_edoras_militia | 14.4 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 26.9 | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 704 | D | [Rohan] West-March Guardsman | rohan_westmarches_guardsman | 14.3 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01 | 26.7 | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 705 | D | [Isengard] Orc Warrior | isengard_orc_warrior | 14.3 | 75.7 | OneHandedSword | isengard_1h_sword_b | 30.4 | False | Defensive Troops | isengard | 11.0 | main_or_minor_line |
| 706 | D | [Mordor] Black Uruk Grunt | mordor_uruk_grunt | 14.3 | 82.0 | OneHandedSword|TwoHandedPolearm | sm_uruk_sword_a|wm_mordor_set1_polearm_a02|wm_mordor_set1_polearm_a03|wm_mordor_set1_polearm_a04 | 17.7 | False | Defensive Troops | mordor | 11.0 | main_or_minor_line |
| 707 | D | Guard | guard_dolguldur | 13.9 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a02 | 23.2 | False | Defensive Troops | dolguldur | 16.0 | special_or_unlinked |
| 708 | D | Guard | guard_gundabad | 13.7 | 82.0 | TwoHandedPolearm | wm_gundabad_spear_a02 | 22.0 | False | Defensive Troops | gundabad | 16.0 | special_or_unlinked |
| 709 | D | Guard | guard_rhun | 13.6 | 75.7 | OneHandedSword | sm_rh_loke_1h_sword_b | 37.1 | False | Defensive Troops | khuzait | 16.0 | special_or_unlinked |
| 710 | D | [Rhûn] Sagarûn Deckhand | sagarun_deckhand | 13.3 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 21.9 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 711 | D | [Rhûn] Easterling Militia | easterling_militia | 13.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 21.7 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 712 | D | [Rhûn] Balcoth Volunteer | balcoth_volunteer | 13.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 21.7 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 713 | D | [Rhûn] Far-Rhun Levy | far_rhun_levy | 13.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 21.5 | False | Defensive Troops | khuzait | 11.0 | main_or_minor_line |
| 714 | D | [Goblin] Militia Archer | goblin_militia_archer | 13.1 | 73.3 | Mace|OneHandedAxe | wm_dol_goldur_1h_mace_a02|wm_gundabad_axe_a01|wm_gundabad_axe_a02 | 10.2 | False | Ranged Troops | goblin | 11.0 | special_or_unlinked |
| 715 | D | [Goblin] Goblin Brawler | goblin_grunt | 13.1 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01|wm_mordor_set1_axe_a01 | 19.1 | False | Offensive Melee | goblin | 16.0 | main_or_minor_line |
| 716 | D | [Rohan] Wold Scout | rohan_wold_scout | 12.9 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 40.4 | True | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 717 | D | [Dol Guldur] Uruk Foul | dg_uruk_foul | 12.8 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a03 | 11.3 | False | Offensive Melee | dolguldur | 11.0 | main_or_minor_line |
| 718 | D | [Gondor] Ringlo Vale Militia | gondor_ring_militia | 12.8 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 27.4 | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 719 | D | [Dol Guldur] Uruk Skirmisher | dg_uruk_skirmisher | 12.5 | 75.7 | OneHandedSword | wm_dol_goldur_1h_sword_a03 | 16.2 | False | Ranged Troops | dolguldur | 16.0 | main_or_minor_line |
| 720 | D | [Isengard] Uruk-Hai Skirmisher | urukhai_skirmisher | 12.2 | 75.7 | OneHandedSword | isengard_1h_sword_b | 25.7 | False | Ranged Troops | isengard | 16.0 | main_or_minor_line |
| 721 | D | [Isengard] Uruk-Hai Scout | urukhai_scout | 12.2 | 75.7 | OneHandedSword | isengard_1h_sword_b | 25.7 | False | Ranged Troops | isengard | 16.0 | main_or_minor_line |
| 722 | D | [Isengard] Orc Ravager | isengard_orc_ravager | 12.2 | 73.3 | TwoHandedAxe | isengard_2h_axe_b | 20.0 | False | Offensive Melee | isengard | 11.0 | main_or_minor_line |
| 723 | D | Guard | guard_isengard | 12.1 | 75.7 | OneHandedSword | isengard_1h_sword_b | 23.9 | False | Defensive Troops | isengard | 16.0 | special_or_unlinked |
| 724 | D | [Gondor] Harondor Skirmisher | gondor_har_skirmisher | 12.0 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 24.0 | False | Skirmishers | gondor | 16.0 | main_or_minor_line |
| 725 | D | [Gondor] Blackroot Vale Bowman | gondor_brv_bowman | 11.8 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 22.9 | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 726 | D | [Gondor] Anorien Skirmisher | gondor_ano_skirmisher | 11.8 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 22.9 | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 727 | D | [Gondor] Tolfalas Arbalest | gondor_tol_arbalest | 11.8 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 22.9 | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 728 | D | [Gondor] Belfalas Bowman | gondor_bel_bowman | 11.8 | 75.7 | OneHandedSword | wm_gondor_sword_a03 | 22.9 | False | Ranged Troops | gondor | 16.0 | main_or_minor_line |
| 729 | D | [Rhûn] Darkhûn Recruit | darkhun_recruit | 11.8 | 73.3 | OneHandedAxe | sm_dg_khml_1h_axe_a | 16.8 | False | Offensive Melee | khuzait | 11.0 | main_or_minor_line |
| 730 | D | Guard | guard_mordor | 11.8 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a01|wm_mordor_set1_sword_a02 | 21.5 | False | Defensive Troops | mordor | 16.0 | special_or_unlinked |
| 731 | D | Guard | guard_gondor | 11.7 | 75.7 | OneHandedSword | wm_gondor_sword_a02 | 22.2 | False | Defensive Troops | gondor | 16.0 | special_or_unlinked |
| 732 | D | [Rohan] West Emnet Recruit | rohan_westemnet_recruit | 11.7 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01 | 31.2 | True | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 733 | D | [Rohan] East Emnet Recruit | rohan_eastemnet_recruit | 11.7 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01 | 31.2 | True | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 734 | D | [Rohan] Wold Recruit | rohan_wold_recruit | 11.7 | 82.0 | TwoHandedPolearm | eastern_spear_4_t4 | 31.2 | True | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 735 | D | Guard | guard_erebor | 11.6 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a | 27.4 | False | Defensive Troops | erebor | 16.0 | special_or_unlinked |
| 736 | D | [Rohan] Westfold Militiaman | rohan_westfold_militiaman | 11.6 | 73.3 | OneHandedAxe | vlandia_axe_2_t4 | 26.7 | False | Defensive Troops | vlandia | 11.0 | main_or_minor_line |
| 737 | D | [Dale] Dalian Crossbowman | dale_crossbowman | 11.4 | 75.7 | OneHandedSword | dale_sword_b|dale_sword_c | 31.8 | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 738 | D | [Gondor] Pinnath Gelin Militia | gondor_pg_militia | 11.4 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 17.0 | False | Offensive Melee | gondor | 11.0 | main_or_minor_line |
| 739 | D | [Gondor] Harondor Militia | gondor_har_militia | 11.4 | 75.7 | OneHandedSword | wm_gondor_sword_a02 | 31.5 | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 740 | D | [Rhûn] Black Sun Trainee | black_sun_trainee | 11.4 | 73.3 | OneHandedAxe | sm_rh_drag_1h_axe_a | 13.7 | False | Offensive Melee | khuzait | 11.0 | main_or_minor_line |
| 741 | D | [Umbar] Adûnaim Bowmen | umbar_elite_root1 | 11.3 | 75.7 | OneHandedSword|TwoHandedAxe | peasant_2haxe_1_t1|wm_gondor_sword_a01 | 15.2 | False | Ranged Troops | umbar | 16.0 | main_or_minor_line |
| 742 | D | Guard | guard_harad | 11.2 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 17.8 | False | Defensive Troops | aserai | 16.0 | special_or_unlinked |
| 743 | D | [Erebor] Miner | erebor_reg_miner | 10.6 | 73.3 | OneHandedAxe | sm_dwarf_erebor_1h_axe_a|sm_dwarf_erebor_1h_axe_b|sm_dwarf_erebor_1h_axe_c|sm_dwarf_erebor_1h_axe_d | 13.9 | False | Defensive Troops | erebor | 11.0 | main_or_minor_line |
| 744 | D | [Gondor] Belfalas Footman | gondor_bel_footman | 10.5 | 75.7 | OneHandedSword | wm_gondor_sword_a02 | 24.0 | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 745 | D | [Isengard] Orc Warg Scout | isengard_orc_warg_scout_v2 | 10.4 | 82.0 | TwoHandedPolearm | isengard_spear_a | 20.8 | True | Defensive Troops | isengard | 6.0 | main_or_minor_line |
| 746 | D | Guard | guard_dale | 10.1 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 15.7 | False | Offensive Melee | sturgia | 16.0 | special_or_unlinked |
| 747 | D | Guard | guard_dunland | 10.1 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 15.2 | False | Defensive Troops | empire | 16.0 | special_or_unlinked |
| 748 | D | [Harad] Desert Archer | harad_archer | 9.9 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 19.6 | False | Ranged Troops | aserai | 16.0 | main_or_minor_line |
| 749 | D | [Gundabad] Pale Uruk Warrior | gundabad_snaga | 9.8 | 73.3 | OneHandedAxe | wm_gundabad_axe_a02|wm_gundabad_axe_a03 | 19.7 | False | Offensive Melee | gundabad | 11.0 | main_or_minor_line |
| 750 | D | [Gondor] Anórien Militia | gondor_ano_militia | 9.8 | 75.7 | OneHandedSword | wm_gondor_sword_a02 | 19.1 | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 751 | D | Guard | guard_khand | 9.7 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 12.3 | False | Offensive Melee | battania | 16.0 | special_or_unlinked |
| 752 | D | [Gondor] Anfalas Militia | gondor_anf_militia | 9.5 | 75.7 | OneHandedSword | wm_gondor_sword_a02 | 17.0 | False | Offensive Melee | gondor | 11.0 | main_or_minor_line |
| 753 | D | [Dale] Dalian Yeoman | dale_bowman | 9.4 | 75.7 | OneHandedSword | dale_sword_b|dale_sword_c | 15.8 | False | Ranged Troops | sturgia | 16.0 | main_or_minor_line |
| 754 | D | [Gondor] Lossarnach Woodsman | gondor_loss_woodsman | 9.4 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_a|wm_gondor_lossarnach_1h_axe_b|wm_gondor_lossarnach_1h_axe_black_ash_a|wm_gondor_lossarnach_1h_axe_silver_a|wm_gondor_lossarnach_1h_axe_silver_b|wm_gondor_lossarnach_1h_axe_silver_full_a | 21.5 | False | Defensive Troops | gondor | 11.0 | main_or_minor_line |
| 755 | D | [Dunland] Cigfran-lûth Skirmisher | dunland_raven_warrior | 9.0 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_b | 18.5 | False | Ranged Troops | empire | 16.0 | main_or_minor_line |
| 756 | D | [Mordor] Morannon Scout | morannon_scout | 8.8 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 23.4 | False | Ranged Troops | mordor | 16.0 | main_or_minor_line |
| 757 | D | [Misty Mountains] Orc Warrior | mistymountainorcs_snaga | 8.8 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01|wm_mordor_set1_axe_a01 | 18.0 | False | Offensive Melee | mistymountainorcs | 11.0 | main_or_minor_line |
| 758 | D | [Dunland] Blaidd-lûth Noble Son | dunland_noble_son | 8.7 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_a | 27.3 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 759 | D | [Dunland] Turch-lûth Noble Son | dunland_boar_noble_son | 8.7 | 73.3 | OneHandedAxe | dunland_caerdh_axe_1h_a | 27.3 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 760 | D | [Mordor] Orc Scout | mordor_orc_scout | 8.6 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 21.5 | False | Ranged Troops | mordor | 16.0 | main_or_minor_line |
| 761 | D | [Rohan] East-Fold Bowman | rohan_eastfold_bowman | 8.6 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 21.2 | False | Ranged Troops | vlandia | 16.0 | main_or_minor_line |
| 762 | D | [Gondor] Lebennin Militia | gondor_leb_militia | 8.6 | 75.7 | OneHandedSword | wm_pelargir_sword_a01 | 9.2 | False | Offensive Melee | gondor | 11.0 | main_or_minor_line |
| 763 | D | [Misty Mountains] Lurker | mistymountainorcs_lurker | 8.2 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01 | 23.5 | False | Ranged Troops | mistymountainorcs | 16.0 | main_or_minor_line |
| 764 | D | [Mordor] Nurn Warg Raider | mordor_warg_raider | 8.2 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 14.2 | True | Defensive Troops | mordor | 11.0 | main_or_minor_line |
| 765 | D | [Gondor] Lamedon Clansman | gondor_lam_clansman | 8.2 | 100.0 | TwoHandedSword | wm_gondor_lamedon_2h_sword_a | 11.7 | False | Offensive Melee | gondor | 6.0 | main_or_minor_line |
| 766 | D | [Gundabad] Lurker | gundabad_lurker | 8.1 | 73.3 | OneHandedAxe | wm_gundabad_axe_a02 | 22.3 | False | Ranged Troops | gundabad | 16.0 | main_or_minor_line |
| 767 | D | [Umbar] Adûnaim Recruits | umbar_elite | 8.0 | 75.7 | OneHandedSword|TwoHandedAxe | peasant_2haxe_1_t1|wm_gondor_boromir_sword | 13.8 | False | Skirmishers | umbar | 11.0 | main_or_minor_line |
| 768 | D | [Mordor] Orc Fighter | mordor_orc_fighter | 7.0 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 21.4 | False | Defensive Troops | mordor | 11.0 | main_or_minor_line |
| 769 | D | [Mordor] Morannon Fighter | morannon_fighter | 6.9 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 20.2 | False | Defensive Troops | mordor | 11.0 | main_or_minor_line |
| 770 | D | [Harad] Militia | harad_militia | 6.6 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 17.8 | False | Defensive Troops | aserai | 11.0 | main_or_minor_line |
| 771 | D | [Dunland] Tribal Raider | dunland_raider | 6.4 | 73.3 | OneHandedAxe | battania_axe_1_t2 | 9.8 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 772 | D | [Rohan] Edoras Recruit | rohan_edoras_recruit | 6.0 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01|wm_rohan_ws_spear_a03 | 25.8 | False | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 773 | D | [Dale] Lake-Town Peasant | dale_recruit | 5.9 | 82.0 | OneHandedSword|TwoHandedPolearm | dale_spear_a|dale_sword_c | 25.2 | False | Defensive Troops | sturgia | 6.0 | main_or_minor_line |
| 774 | D | [Goblin] Lurker | goblin_lurker | 5.8 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01 | 23.5 | False | Ranged Troops | goblin | 16.0 | main_or_minor_line |
| 775 | D | [Goblin] Goblin Warrior | goblin_snaga | 5.6 | 73.3 | OneHandedAxe | wm_gundabad_axe_a01|wm_mordor_set1_axe_a01 | 18.0 | False | Offensive Melee | goblin | 11.0 | main_or_minor_line |
| 776 | D | [Rohan] West-March Recruit | rohan_westmarches_recruit | 5.2 | 82.0 | TwoHandedPolearm | wm_rohan_ws_spear_a01 | 19.9 | False | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 777 | D | [Gondor] Ringlo Vale Peasant | gondor_ring_peasant | 4.9 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 17.7 | False | Defensive Troops | gondor | 6.0 | main_or_minor_line |
| 778 | D | [Umbar] Auxiliary Recruit | aux_basic | 4.7 | 75.7 | OneHandedSword|TwoHandedAxe | peasant_2haxe_1_t1|wm_gondor_sword_a01 | 21.2 | False | Skirmishers | umbar | 6.0 | special_or_unlinked |
| 779 | D | [Isengard] Orc Brawler | isengard_orc_brawler | 4.2 | 75.7 | OneHandedSword | isengard_1h_sword_b | 23.3 | False | Defensive Troops | isengard | 6.0 | main_or_minor_line |
| 780 | D | [Mordor] Nurn Warg Rider | mordor_warg_rider | 4.0 | 73.3 | OneHandedAxe | wm_mordor_set1_axe_a02 | 26.0 | False | Defensive Troops | mordor | 6.0 | main_or_minor_line |
| 781 | D | [Dol Guldur] Orc Recruit | dg_orc_recruit | 4.0 | 82.0 | TwoHandedPolearm | wm_dol_goldur_halberd_a01|wm_dol_goldur_halberd_a02|wm_dol_goldur_halberd_a03|wm_dol_goldur_halberd_a04 | 9.1 | False | Offensive Melee | dolguldur | 6.0 | main_or_minor_line |
| 782 | D | [Gundabad] Hunter | gundabad_hunter | 3.9 | 73.3 | OneHandedAxe | wm_gundabad_axe_a03 | 19.7 | False | Ranged Troops | gundabad | 11.0 | main_or_minor_line |
| 783 | D | [Mordor] Morannon Recruit | morannon_recruit | 3.8 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 20.2 | False | Defensive Troops | mordor | 7.0 | main_or_minor_line |
| 784 | D | [Gondor] Pinnath Gelin Volunteer | gondor_pg_volunteer | 3.8 | 82.0 | TwoHandedPolearm | wm_gondor_spear | 9.2 | False | Offensive Melee | gondor | 6.0 | main_or_minor_line |
| 785 | D | [Gondor] Harondor Conscript | gondor_har_conscript | 3.8 | 75.7 | OneHandedSword | wm_gondor_sword_a01 | 19.8 | False | Defensive Troops | gondor | 6.0 | main_or_minor_line |
| 786 | D | [Harad] Levy | harad_levy | 3.5 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 17.8 | False | Defensive Troops | aserai | 6.0 | main_or_minor_line |
| 787 | D | [Misty Mountains] Hunter | mistymountainorcs_hunter | 3.5 | 73.3 | OneHandedAxe | wm_mordor_set1_axe_a01 | 18.0 | False | Ranged Troops | mistymountainorcs | 11.0 | main_or_minor_line |
| 788 | D | [Goblin] Hunter | goblin_hunter | 3.5 | 73.3 | OneHandedAxe | wm_mordor_set1_axe_a01 | 18.0 | False | Ranged Troops | goblin | 11.0 | main_or_minor_line |
| 789 | D | [Rohan] Westfold Recruit | rohan_westfold_recruit | 3.3 | 73.3 | OneHandedAxe | vlandia_axe_2_t4 | 19.9 | False | Defensive Troops | vlandia | 6.0 | main_or_minor_line |
| 790 | D | [Gondor] Anórien Peasant | gondor_ano_peasant | 3.2 | 75.7 | OneHandedSword | wm_gondor_sword_a01 | 15.3 | False | Defensive Troops | gondor | 6.0 | main_or_minor_line |
| 791 | D | [Rohan] Eastfold Yeoman Archer | rohan_eastfold_skirmisher | 3.2 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 15.2 | False | Ranged Troops | vlandia | 11.0 | main_or_minor_line |
| 792 | D | [Isengard] Uruk-Hai Recruit | urukhai_recruit | 3.1 | 75.7 | OneHandedSword | isengard_1h_sword_b | 14.3 | False | Defensive Troops | isengard | 6.0 | main_or_minor_line |
| 793 | D | [Rhûn] Easterling Recruit | easterling_recruit | 3.1 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 14.2 | False | Defensive Troops | khuzait | 6.0 | main_or_minor_line |
| 794 | D | [Mordor] Morannon Skirmisher | morannon_skirmisher | 3.1 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a02 | 14.2 | False | Ranged Troops | mordor | 11.0 | main_or_minor_line |
| 795 | D | [Gondor] Lossarnach Lumberman | gondor_loss_lumberman | 3.0 | 73.3 | OneHandedAxe | wm_gondor_lossarnach_1h_axe_a|wm_gondor_lossarnach_1h_axe_b|wm_gondor_lossarnach_1h_axe_black_ash_a|wm_gondor_lossarnach_1h_axe_silver_a|wm_gondor_lossarnach_1h_axe_silver_b|wm_gondor_lossarnach_1h_axe_silver_full_a | 17.7 | False | Defensive Troops | gondor | 6.0 | main_or_minor_line |
| 796 | D | [Dol Guldur] Goblin Hunter | dg_goblin_hunter | 3.0 | 75.7 | OneHandedSword|TwoHandedMace | wm_dol_goldur_1h_sword_a01|wm_dol_goldur_1h_sword_a02|wm_dol_goldur_2h_mace_a03|wm_dol_goldur_2h_mace_a04 | 11.8 | False | Ranged Troops | dolguldur | 11.0 | main_or_minor_line |
| 797 | D | [Mordor] Orc Lackey | mordor_orc_lackey | 2.9 | 73.3 | OneHandedAxe | wm_mordor_set1_axe_a02 | 17.2 | False | Defensive Troops | mordor | 6.0 | main_or_minor_line |
| 798 | D | [Gondor] Belfalas Hunter | gondor_bel_hunter | 2.9 | 75.7 | OneHandedSword | wm_gondor_sword_a02 | 12.9 | False | Ranged Troops | gondor | 11.0 | main_or_minor_line |
| 799 | D | [Mordor] Orc Hunter | mordor_orc_hunter | 2.9 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a01 | 12.9 | False | Ranged Troops | mordor | 11.0 | main_or_minor_line |
| 800 | D | [Harad] Skirmisher | harad_skirmisher | 2.7 | 75.7 | OneHandedSword | aserai_sword_3_t3 | 11.7 | False | Ranged Troops | aserai | 11.0 | main_or_minor_line |
| 801 | D | [Isengard] Orc Grunt | isengard_orc_grunt | 2.7 | 75.7 | OneHandedSword | isengard_1h_sword_b | 11.7 | False | Offensive Melee | isengard | 1.0 | main_or_minor_line |
| 802 | D | [Mordor] Nurn Warg Tamer | mordor_warg_tamer | 2.7 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a01 | 11.2 | False | Offensive Melee | mordor | 1.0 | main_or_minor_line |
| 803 | D | [Mordor] Orc Recruit | mordor_orc_recruit | 2.7 | 75.7 | OneHandedSword | wm_mordor_set1_sword_a01 | 11.2 | False | Offensive Melee | mordor | 1.0 | main_or_minor_line |
| 804 | D | [Dol Guldur] Goblin Crawler | dg_goblin_crawler | 2.6 | 75.7 | OneHandedSword|TwoHandedAxe | wm_dol_goldur_1h_sword_a02|wm_dol_goldur_1h_sword_a03|wm_dol_goldur_axe_a01|wm_dol_goldur_axe_a03 | 9.1 | False | Offensive Melee | dolguldur | 6.0 | main_or_minor_line |
| 805 | D | [Gondor] Anfalas Levy | gondor_anf_levy | 2.4 | 75.7 | OneHandedSword | wm_gondor_sword_a01 | 9.2 | False | Offensive Melee | gondor | 6.0 | main_or_minor_line |
| 806 | D | [Gondor] Belfalas Recruit | gondor_bel_recruit | 2.4 | 75.7 | OneHandedSword | wm_gondor_sword_a01 | 9.2 | False | Offensive Melee | gondor | 6.0 | main_or_minor_line |
| 807 | D | [Dol Guldur] Goblin Harrier | dg_goblin_harrier | 2.3 | 75.7 | OneHandedSword|TwoHandedAxe | wm_dol_goldur_1h_sword_a02|wm_dol_goldur_1h_sword_a03|wm_dol_goldur_axe_a01|wm_dol_goldur_axe_a03 | 9.1 | False | Offensive Melee | dolguldur | 6.0 | main_or_minor_line |
| 808 | D | [Rohan] Eastfold Freeman | rohan_eastfold_recruit | 2.3 | 75.7 | OneHandedSword | sturgia_sword_2_t3 | 8.4 | False | Ranged Troops | vlandia | 6.0 | main_or_minor_line |
| 809 | D | [Dunland] Tribal Hunter | dunland_hunter | 2.3 | 73.3 | OneHandedAxe | small_spurred_axe_t2 | 12.2 | False | Ranged Troops | empire | 11.0 | main_or_minor_line |
| 810 | D | [Isengard] Orc Berserker | isengard_orc_berserker | 2.2 | 73.3 | TwoHandedAxe | isengard_2h_axe_b | 11.7 | False | Offensive Melee | isengard | 6.0 | main_or_minor_line |
| 811 | D | [Dunland] Peasant | dunland_peasant | 1.3 | 73.3 | OneHandedAxe | sturgia_axe_2_t2 | 4.5 | False | Skirmishers | empire | 6.0 | main_or_minor_line |
| 812 | D | [Dol Guldur] Goblin Runt | dg_goblin_slave | 0.8 | 73.3 | TwoHandedAxe | wm_dol_goldur_axe_a04 | 0.5 | False | Offensive Melee | dolguldur | 1.0 | main_or_minor_line |


## Ranked — Skirmisher (90 troops)

| rank | tier | troop_name | troop_id | skirmisher_role_score | throw_score_base | throw_damage | direct_throw_item | crafted_throw_item | has_horse | primary_category | culture | level | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rohan] Riders of Rohan | rohan_edoras_golden_hall_supreme_rider | 68.7 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | vlandia | 41.0 | main_or_minor_line |
| 2 | S | [Rohan] West Emnet Heavy Shock Cavalry | rohan_westemnet_kings_own_rider | 63.4 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 3 | S | [Dunland] Caru-lûth Noble Lancer | dunland_stag_noble_lancer | 63.3 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 4 | A | [Rohan] King's Royal Guard | rohan_edoras_golden_hall_kings_own_rider | 61.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | vlandia | 36.0 | main_or_minor_line |
| 5 | A | [Dunland] Avanc-lûth Noble Cavalry | dunland_lizard_noble_cavalry | 58.1 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 31.0 | main_or_minor_line |
| 6 | A | [Dunland] Caru-lûth Rider | dunland_stag_rider | 57.4 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 7 | A | [Rohan] King's Knight | rohan_edoras_golden_hall_eorlingas_rider | 56.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 8 | A | [Rohan] West Emnet Shock Cavalry | rohan_westemnet_royal_rider | 55.0 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | vlandia | 31.0 | main_or_minor_line |
| 9 | A | [Umbar] Naru n'Aru Royal Guard | umbar_elite_root0000 | 52.2 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 10 | A | [Dunland] Avanc-lûth Outrider | dunland_lizard_outrider | 50.8 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 26.0 | main_or_minor_line |
| 11 | A | [Harad] Fang of the King | harad_fangking | 50.6 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 12 | B | [Dunland] Caru-lûth Lancer | dunland_stag_lancer | 46.8 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 13 | B | [Harad] Serpent Guard | harad_serpentguard | 46.7 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 14 | B | [Rohan] West Emnet Medium Cavalry | rohan_westemnet_eorlingas_rider | 46.2 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | vlandia | 26.0 | main_or_minor_line |
| 15 | B | [Gondor] Pinnath Gelin Veteran Horseman | gondor_pg_vet_cavalry | 46.1 | 30.5 | 0.0 | nan | western_javelin_3_t4 | True | Skirmishers | gondor | 31.0 | main_or_minor_line |
| 16 | B | [Harad] Youngblood of the Serpent | harad_noble | 45.8 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 11.0 | main_or_minor_line |
| 17 | B | [Harad] Warrior of the Gilded Fang | harad_gildedfang | 45.8 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 18 | B | [Harad] Initiate of the Sand Blades | harad_sandblade | 45.8 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 19 | B | [Dunland] Turch-lûth Huskarl | dunland_boar_warlord | 45.5 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 20 | B | [Rhûn] Far-Rhun Horse Master | far_rhun_horse_master | 44.5 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 21.0 | special_or_unlinked |
| 21 | B | [Rhûn] Far-Rhun Cavalry | far_rhun_cavalry | 44.5 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 22 | B | [Rhûn] Easterling Cavalry | easterling_cavalry_new | 44.0 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 23 | B | [Gondor] Pinnath Gelin Light Horseman | gondor_pg_cavalry | 43.6 | 30.5 | 0.0 | nan | western_javelin_2_t3 | True | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 24 | B | [Rhûn] Kharaghûl Raider | kharaghul_raider | 43.6 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 21.0 | main_or_minor_line |
| 25 | B | [Umbar] Abrazanim Narduzagar | umbar_elite_root001 | 43.2 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 26 | B | [Umbar] Abrazanim Nardutarik | umbar_elite_root000 | 43.2 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 27 | B | [Umbar] Adûnaims Faithful | umbar_elite_root010 | 43.2 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 26.0 | main_or_minor_line |
| 28 | B | [Harad] Camel Rider | harad_camelrider | 43.0 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 21.0 | main_or_minor_line |
| 29 | B | [Dunland] Avanc-lûth Horseman | dunland_lizard_horseman | 42.3 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | True | Skirmishers | empire | 21.0 | main_or_minor_line |
| 30 | B | [Harad] Camel Lancer | harad_camel_lancer | 42.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 31 | B | [Dunland] Blaidd-lûth Champion | dunland_wolf_champion | 40.8 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 32 | B | [Rhûn] Wain Darkhan | wain_darkhan | 40.8 | 30.5 | 0.0 | nan | eastern_javelin_1_t2 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 33 | B | [Dunland] Turch-lûth Ironhide | dunland_boar_boar_warrior | 40.5 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 34 | B | [Rhûn] Far-Rhun Horseman | far_rhun_horseman | 40.3 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 35 | B | [Rhûn] Sagarûn Storm Forged Marine | sagarun_storm_forged_marine | 39.6 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 36 | B | [Harad] Camel Scout | harad_camelscout | 39.6 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | aserai | 16.0 | main_or_minor_line |
| 37 | B | [Gundabad] Pale Uruk Skull Crusher | gundabad_veteran_berserker | 38.2 | 30.5 | 0.0 | nan | wm_gundabad_javelin_a02 | False | Skirmishers | gundabad | 36.0 | main_or_minor_line |
| 38 | B | [Rhûn] Kharaghûl Rider | kharaghul_rider | 38.0 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | True | Skirmishers | khuzait | 16.0 | main_or_minor_line |
| 39 | B | [Dunland] Arth-lûth Executioner | dunland_bear_executioner | 37.8 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 40 | B | [Rhûn] Sagarûn Marine | sagarun_marine | 36.1 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 41 | B | [Harad] Warlance | harad_warlance | 36.0 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | aserai | 31.0 | main_or_minor_line |
| 42 | B | [Dunland] Blaidd-lûth Axeman | dunland_wolf_axeman | 35.5 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 43 | B | [Gondor] Lebennin Sea Guard | gondor_leb_sea_guard | 34.8 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 44 | B | [Gondor] Osgiliath Dome Guard | gondor_osg_dome_guard | 34.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | gondor | 36.0 | main_or_minor_line |
| 45 | B | [Misty Mountains] Orc Skull Crusher | mistymountainorcs_veteran_berserker | 34.0 | 30.5 | 0.0 | nan | wm_gundabad_javelin_a02 | False | Skirmishers | mistymountainorcs | 36.0 | main_or_minor_line |
| 46 | B | [Dunland] Arth-lûth Berserker | dunland_bear_berserker | 33.0 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 47 | B | [Rhûn] Far-Rhun Iron Legionary | far_rhun_iron_legionary | 33.0 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 48 | B | [Harad] Sunlance | harad_sunlance | 31.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 49 | B | [Harad] Bronze Fang | harad_bronzefang | 31.2 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | aserai | 26.0 | main_or_minor_line |
| 50 | B | [Gundabad] Pale Uruk Bone Breaker | gundabad_berserker | 30.7 | 30.5 | 0.0 | nan | wm_gundabad_javelin_a01 | False | Skirmishers | gundabad | 31.0 | main_or_minor_line |
| 51 | B | [Dunland] Uch-lûth Iron Wall | dunland_ox_iron_wall | 30.1 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 31.0 | main_or_minor_line |
| 52 | B | [Misty Mountains] Orc Bone Breaker | mistymountainorcs_berserker | 29.2 | 30.5 | 0.0 | nan | wm_gundabad_javelin_a01 | False | Skirmishers | mistymountainorcs | 31.0 | main_or_minor_line |
| 53 | B | [Goblin] Goblin Skull Crusher | goblin_veteran_berserker | 29.2 | 30.5 | 0.0 | nan | wm_gundabad_javelin_a02 | False | Skirmishers | goblin | 36.0 | main_or_minor_line |
| 54 | B | [Dunland] Turch-lûth Goreblade | dunland_boar_spearman | 28.8 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 55 | B | [Rhûn] Far-Rhun Gate Guard | far_rhun_gate_guard | 27.5 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 56 | C | [Dunland] Wild-man Spearman | dunland_veteran_spearman | 27.1 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 57 | C | [Rhûn] Balcoth Veteran Axeman | balcoth_veteran_axeman | 25.3 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 58 | C | [Rhûn] Easterling Veteran Swordsman | easterling_veteran_swordsman_new | 25.3 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 26.0 | main_or_minor_line |
| 59 | C | [Umbar] Beruthiel's Rangers | umbar_elite_root101 | 25.1 | 57.5 | 10.0 | throwing_stone | nan | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 60 | C | [Umbar] Abrazanim Nardubawib | umbar_elite_root100 | 25.1 | 57.5 | 10.0 | throwing_stone | nan | False | Ranged Troops | umbar | 26.0 | main_or_minor_line |
| 61 | C | [Umbar] Naru n'Aru Royal Knights | umbar_elite_root0001 | 25.1 | 57.5 | 10.0 | throwing_stone | nan | True | Skirmishers | umbar | 31.0 | main_or_minor_line |
| 62 | C | [Umbar] Rozadan Halberdiers | umbar_elite_root01 | 25.1 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 63 | C | [Umbar] Rozadan Footmen | umbar_elite_root00 | 25.1 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 21.0 | main_or_minor_line |
| 64 | C | [Dunland] Uch-lûth Bodyguard | dunland_ox_guard | 24.4 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 26.0 | main_or_minor_line |
| 65 | C | [Goblin] Goblin Bone Breaker | goblin_berserker | 24.4 | 30.5 | 0.0 | nan | wm_gundabad_javelin_a01 | False | Skirmishers | goblin | 31.0 | main_or_minor_line |
| 66 | C | [Rhûn] Sagarûn Storm Helmed Naffatun | sagarun_storm_helmed_naffatun | 24.1 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 36.0 | main_or_minor_line |
| 67 | C | [Dunland] Blaidd-lûth Raider | dunland_wolf_raider | 23.6 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 68 | C | [Dunland] Wild-man Swordman | dunland_veteran_swordman | 22.9 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 69 | C | [Gondor] Lebennin Veteran Infantry | gondor_leb_vet_infantry | 22.8 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 70 | C | [Dunland] Arth-lûth Chosen | dunland_bear_chosen | 21.3 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 71 | C | [Rhûn] Sagarûn Naffatun | sagarun_naffatun | 16.5 | 30.5 | 0.0 | nan | eastern_javelin_3_t4 | False | Skirmishers | khuzait | 31.0 | main_or_minor_line |
| 72 | C | [Umbar] Adûnaim Bowmen | umbar_elite_root1 | 16.1 | 57.5 | 10.0 | throwing_stone | nan | False | Ranged Troops | umbar | 16.0 | main_or_minor_line |
| 73 | C | [Umbar] Rozadan Bowmen | umbar_elite_root10 | 16.1 | 57.5 | 10.0 | throwing_stone | nan | False | Ranged Troops | umbar | 21.0 | main_or_minor_line |
| 74 | C | [Umbar] Adûnaim Recruits | umbar_elite | 16.1 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 11.0 | main_or_minor_line |
| 75 | C | [Umbar] Adûnaim Footmen | umbar_elite_root0 | 16.1 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 16.0 | main_or_minor_line |
| 76 | C | [Umbar] Auxiliary Recruit | aux_basic | 16.1 | 57.5 | 10.0 | throwing_stone | nan | False | Skirmishers | umbar | 6.0 | special_or_unlinked |
| 77 | C | [Gondor] Harondor Javelineer | gondor_har_javelineer | 15.5 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | gondor | 26.0 | main_or_minor_line |
| 78 | C | [Gondor] Harondor Veteran Skirmisher | gondor_har_vet_skirmisher | 15.0 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | gondor | 21.0 | main_or_minor_line |
| 79 | C | [Dunland] Blaidd-lûth Warrior | dunland_clan_warrior | 13.8 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 80 | C | [Dunland] Turch-lûth Tuskrunner | dunland_boar_warrior | 13.8 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 81 | D | [Gondor] Lebennin Infantry | gondor_leb_infantry | 12.2 | 30.5 | 0.0 | nan | eastern_javelin_2_t3 | False | Skirmishers | gondor | 21.0 | main_or_minor_line |
| 82 | D | [Dunland] Uch-lûth Pikeman | dunland_ox_pikeman | 11.8 | 30.5 | 0.0 | nan | northern_javelin_3_t4 | False | Skirmishers | empire | 21.0 | main_or_minor_line |
| 83 | D | [Dunland] Tribal Spearman | dunland_spearman | 11.4 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 84 | D | [Gondor] Harondor Skirmisher | gondor_har_skirmisher | 8.9 | 30.5 | 0.0 | nan | western_javelin_3_t4 | False | Skirmishers | gondor | 16.0 | main_or_minor_line |
| 85 | D | [Dunland] Blaidd-lûth Noble Son | dunland_noble_son | 8.8 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 86 | D | [Dunland] Turch-lûth Noble Son | dunland_boar_noble_son | 8.8 | 30.5 | 0.0 | nan | northern_javelin_2_t3 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 87 | D | [Dunland] Tribal Swordsman | dunland_swordsman | 7.8 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 16.0 | main_or_minor_line |
| 88 | D | [Gondor] Lossarnach Skirmisher | gondor_loss_skirmisher | 5.5 | 30.5 | 0.0 | nan | eastern_javelin_2_t3|generic_javelin_1_t3|northern_javelin_2_t3|western_javelin_1_t2|western_javelin_2_t3 | False | Skirmishers | gondor | 16.0 | main_or_minor_line |
| 89 | D | [Dunland] Tribal Raider | dunland_raider | 2.1 | 30.5 | 0.0 | nan | western_javelin_1_t2 | False | Skirmishers | empire | 11.0 | main_or_minor_line |
| 90 | D | [Dunland] Peasant | dunland_peasant | 0.0 | 30.5 | 0.0 | nan | northern_javelin_1_t2 | False | Skirmishers | empire | 6.0 | main_or_minor_line |

