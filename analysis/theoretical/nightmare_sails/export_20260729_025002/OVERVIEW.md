# Troop overview — `nightmare_sails` / `export_20260729_025002`

## Labels

- `evidence_basis=xml_structural`, `empirical=false` (ADR-004)
- Model: `role_scores_v1` conservative (crafted melee = proxy, not HTK)
- Package digest: `afef4c8483d4d27a228f13c78ed84f89fd624f9e7103d2801b1cec065eee767f`
- Rows scored: **371**; after filters: **179** (excluded 192: specials, spectacle names, and untouched vanilla `change_type=inalterado`)

## Filters

- Drop `line_status=special_or_unlinked`
- Drop troop names matching Giant / Mammoth / Dragon / Direwolf / Kraken
- Drop `change_type=inalterado` from the track override report (vanilla baseline troops that the mod did not add/override)
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


## Top 20 — Ranged

| rank | troop_name | troop_id | ranged_role_score | primary_category | culture | level |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Khuzait Khan's Guard | khuzait_khans_guard | 100.0 | Ranged Troops | khuzait | 31.0 |
| 2 | Battanian Fian Champion | battanian_fian_champion | 98.0 | Ranged Troops | battania | 31.0 |
| 3 | Battanian Fian | battanian_fian | 74.9 | Ranged Troops | battania | 26.0 |
| 4 | Khuzait Kheshig | khuzait_kheshig | 69.0 | Ranged Troops | khuzait | 26.0 |
| 5 | Aserai Mamluke Heavy Cavalry | aserai_mameluke_heavy_cavalry | 66.9 | Ranged Troops | aserai | 26.0 |
| 6 | Veteran Eleftheroi | eleftheroi_tier_3 | 61.1 | Ranged Troops | empire | 26.0 |
| 7 | Nord Sky-Gods Chosen | nord_skathi | 59.8 | Ranged Troops | nord | 26.0 |
| 8 | Imperial Bucellarii | bucellarii | 59.4 | Ranged Troops | empire | 26.0 |
| 9 | Khuzait Heavy Horse Archer | khuzait_heavy_horse_archer | 56.8 | Ranged Troops | khuzait | 26.0 |
| 10 | Karakhergit Elder | karakhuzaits_tier_3 | 53.4 | Ranged Troops | khuzait | 26.0 |
| 11 | Aserai Bahriyyah | aserai_marine_t5 | 52.4 | Ranged Troops | aserai | 26.0 |
| 12 | Vlandian Marinier | vlandian_marine_t5 | 51.6 | Ranged Troops | vlandia | 26.0 |
| 13 | Aserai Mamluke Cavalry | aserai_mameluke_cavalry | 51.3 | Ranged Troops | aserai | 21.0 |
| 14 | Chosen Wolf | wolfskins_tier_3 | 48.0 | Ranged Troops | battania | 26.0 |
| 15 | Sturgian Veteran Bowman | sturgian_veteran_bowman | 47.9 | Ranged Troops | sturgia | 26.0 |
| 16 | Khuzait Marksman | khuzait_marksman | 47.0 | Ranged Troops | khuzait | 26.0 |
| 17 | Imperial Sergeant Boatsman | imperial_sergeant_crossbowman | 46.3 | Ranged Troops | empire | 26.0 |
| 18 | Veteran Forester | forest_people_tier_3 | 45.8 | Ranged Troops | sturgia | 26.0 |
| 19 | Arboreal | brotherhood_of_woods_tier_3 | 45.6 | Ranged Troops | vlandia | 26.0 |
| 20 | Boar Champion | company_of_the_boar_tier_3 | 44.2 | Ranged Troops | vlandia | 26.0 |


## Top 20 — Defensive

| rank | troop_name | troop_id | defensive_role_score | primary_category | culture | level |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Imperial Elite Cataphract | imperial_elite_cataphract | 100.0 | Defensive Troops | empire | 31.0 |
| 2 | Vlandian Banner Knight | vlandian_banner_knight | 98.9 | Defensive Troops | vlandia | 31.0 |
| 3 | Sturgian Druzhinnik Champion | druzhinnik_champion | 96.7 | Defensive Troops | sturgia | 31.0 |
| 4 | Sturgian Druzhinnik | druzhinnik | 93.6 | Defensive Troops | sturgia | 26.0 |
| 5 | Aserai Vanguard Faris | aserai_vanguard_faris | 93.2 | Skirmishers | aserai | 31.0 |
| 6 | Aserai Veteran Faris | aserai_veteran_faris | 90.9 | Skirmishers | aserai | 26.0 |
| 7 | Imperial Cataphract | imperial_cataphract | 90.6 | Defensive Troops | empire | 26.0 |
| 8 | Vlandian Champion | vlandian_champion | 89.9 | Defensive Troops | vlandia | 26.0 |
| 9 | Vlandian Vanguard | vlandian_vanguard | 83.2 | Defensive Troops | vlandia | 26.0 |
| 10 | Khuzait Heavy Lancer | khuzait_heavy_lancer | 81.0 | Defensive Troops | khuzait | 26.0 |
| 11 | Vlandian Knight | vlandian_knight | 79.9 | Defensive Troops | vlandia | 21.0 |
| 12 | Battanian Horseman | battanian_horseman | 79.8 | Defensive Troops | battania | 26.0 |
| 13 | Sturgian Horse Raider | sturgian_horse_raider | 78.9 | Skirmishers | sturgia | 26.0 |
| 14 | Imperial Heavy Horseman | imperial_heavy_horseman | 74.6 | Defensive Troops | empire | 21.0 |
| 15 | Aserai Mamluke Heavy Cavalry | aserai_mameluke_heavy_cavalry | 73.8 | Ranged Troops | aserai | 26.0 |
| 16 | Khuzait Lancer | khuzait_lancer | 72.7 | Defensive Troops | khuzait | 21.0 |
| 17 | Nord Huscarl | nord_huscarl | 71.7 | Defensive Troops | nord | 31.0 |
| 18 | Ghilman | ghilman_tier_2 | 70.9 | Defensive Troops | aserai | 21.0 |
| 19 | Aserai Mamluke Cavalry | aserai_mameluke_cavalry | 69.6 | Ranged Troops | aserai | 21.0 |
| 20 | Ghulam | ghilman_tier_3 | 68.1 | Defensive Troops | aserai | 26.0 |


## Top 20 — Offensive melee

| rank | troop_name | troop_id | offensive_melee_role_score | primary_category | culture | level |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Battanian Fian Champion | battanian_fian_champion | 94.2 | Ranged Troops | battania | 31.0 |
| 2 | Vlandian Banner Knight | vlandian_banner_knight | 78.3 | Defensive Troops | vlandia | 31.0 |
| 3 | Imperial Elite Cataphract | imperial_elite_cataphract | 77.8 | Defensive Troops | empire | 31.0 |
| 4 | Khuzait Khan's Guard | khuzait_khans_guard | 67.2 | Ranged Troops | khuzait | 31.0 |
| 5 | Aserai Vanguard Faris | aserai_vanguard_faris | 64.5 | Skirmishers | aserai | 31.0 |
| 6 | Sturgian Druzhinnik Champion | druzhinnik_champion | 62.7 | Defensive Troops | sturgia | 31.0 |
| 7 | Nord Huscarl | nord_huscarl | 62.4 | Defensive Troops | nord | 31.0 |
| 8 | Battanian Fian | battanian_fian | 60.4 | Ranged Troops | battania | 26.0 |
| 9 | Khuzait Tengri | khuzait_Tengri | 60.3 | Skirmishers | khuzait | 26.0 |
| 10 | Vlandian Captain | vlandian_pikeman | 57.4 | Offensive Melee | vlandia | 26.0 |
| 11 | Battanian Veteran Falxman | battanian_veteran_falxman | 56.8 | Offensive Melee | battania | 26.0 |
| 12 | Vlandian Marinier | vlandian_marine_t5 | 56.4 | Ranged Troops | vlandia | 26.0 |
| 13 | Imperial Cataphract | imperial_cataphract | 54.5 | Defensive Troops | empire | 26.0 |
| 14 | Vlandian Champion | vlandian_champion | 54.5 | Defensive Troops | vlandia | 26.0 |
| 15 | Sturgian Druzhinnik | druzhinnik | 52.6 | Defensive Troops | sturgia | 26.0 |
| 16 | Khuzait Tengichi | khuzait_sailor | 51.9 | Ranged Troops | khuzait | 26.0 |
| 17 | Imperial Heavy Horseman | imperial_heavy_horseman | 49.8 | Defensive Troops | empire | 21.0 |
| 18 | Ghulam | ghilman_tier_3 | 48.9 | Defensive Troops | aserai | 26.0 |
| 19 | Flame | embers_of_flame_tier_2 | 48.5 | Skirmishers | empire | 21.0 |
| 20 | Battanian Hero | battanian_hero | 47.2 | Ranged Troops | battania | 21.0 |


## Top 20 — Skirmisher

| rank | troop_name | troop_id | skirmisher_role_score | primary_category | culture | level |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Aserai Vanguard Faris | aserai_vanguard_faris | 100.0 | Skirmishers | aserai | 31.0 |
| 2 | Flame | embers_of_flame_tier_2 | 98.3 | Skirmishers | empire | 21.0 |
| 3 | Sturgian Horse Raider | sturgian_horse_raider | 90.1 | Skirmishers | sturgia | 26.0 |
| 4 | Jawwal Bedouin | jawwal_tier_3 | 86.6 | Skirmishers | aserai | 26.0 |
| 5 | Beni Zilal Royal Guard | beni_zilal_tier_3 | 86.2 | Skirmishers | aserai | 26.0 |
| 6 | Aserai Veteran Faris | aserai_veteran_faris | 76.8 | Skirmishers | aserai | 26.0 |
| 7 | Jawwal Camel Rider | jawwal_tier_2 | 73.5 | Skirmishers | aserai | 16.0 |
| 8 | Sturgian Hardened Brigand | sturgian_hardened_brigand | 72.9 | Skirmishers | sturgia | 21.0 |
| 9 | Puppeteer | hidden_hand_tier_3 | 70.8 | Skirmishers | empire | 26.0 |
| 10 | Aserai Faris | aserai_faris | 70.5 | Skirmishers | aserai | 21.0 |
| 11 | Khuzait Tengri | khuzait_Tengri | 68.5 | Skirmishers | khuzait | 26.0 |
| 12 | Beni Zilal Soldier | beni_zilal_tier_2 | 61.8 | Skirmishers | aserai | 21.0 |
| 13 | Battanian Falxman | battanian_falxman | 61.1 | Skirmishers | battania | 21.0 |
| 14 | Battanian Skipari | battanian_marine_t5 | 58.7 | Skirmishers | battania | 26.0 |
| 15 | Aserai Tribal Horseman | aserai_tribal_horseman | 57.1 | Skirmishers | aserai | 16.0 |
| 16 | Skolder Veteran Broda | skolderbrotva_tier_3 | 51.7 | Skirmishers | nord | 26.0 |
| 17 | Lake Rat Wrecker  | lakepike_tier_3 | 49.5 | Skirmishers | sturgia | 26.0 |
| 18 | Aserai Lieutenant | aserai_veteran_infantry | 49.0 | Skirmishers | aserai | 26.0 |
| 19 | Beni Zilal Recruit | beni_zilal_tier_1 | 47.5 | Skirmishers | aserai | 16.0 |
| 20 | Imperial Naute | empire_marine_t5 | 47.1 | Skirmishers | empire | 26.0 |

