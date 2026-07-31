# PC field-battle capture prompt — Realm of Thrones and Nightmare Sails

Use this checklist on the Windows PC that runs Mount & Blade II: Bannerlord. It is self-contained. The goal is to capture future empirical evidence; **do not fill gaps from memory, infer off-screen rows, or invent any result**.

## What this capture is for

Create two separate campaign field-battle batches:

| Session | Track | Battle IDs | Repository destination |
|---|---|---|---|
| Realm of Thrones | `realm_of_thrones` | `ROT-FIELD-B01`…`ROT-FIELD-B05` | `data/combat_observations/2026-07-31-rot-field-plan/source/` |
| Nightmare Sails | `nightmare_sails` | `NS-FIELD-B01`…`NS-FIELD-B05` | `data/combat_observations/2026-07-31-ns-field-plan/source/` |

Keep the sessions completely separate. Do not combine their screenshots or CSV rows. Both will later join only to the pinned theoretical export `export_20260731_150800`.

These are campaign observations, not custom battles and not causal experiments. Enemy composition, terrain, outcome, perks, and AI behavior are confounders that must be recorded rather than controlled away or guessed.

## Before each session

1. Start the intended module track and verify the track on screen before the first battle.
2. Record the exact game version and active module names/load order. Do not change modules, difficulty, campaign, character, equipment, perks, or battle-size settings within a five-battle session.
3. Create the four UTF-8 CSV files described below and a `screenshots/` folder under that session's destination.
4. Use only campaign **field** battles: no siege, village raid, hideout, naval battle, keep phase, or autoresolve.
5. Use the player party alone; do not join allied armies or allied parties.
6. Before every battle, make every target troop healthy and deployable. Replace casualties with the same canonical target before the next battle.
7. At deployment, use the default formation assignment. At battle start, issue `F1` then `F3` once to order all troops to charge. Do not issue other orders and do not personally attack. If this cannot be followed, finish and capture the battle, but record the deviation in every occurrence row's `provenance` object.
8. Engage one ordinary roaming enemy party on land. Capture the actual enemy roster from the result screen; never label an unseen enemy troop.
9. Every battle ID must be a new campaign encounter against a new roaming party. Never reload or replay one encounter and count it as another independent battle.

The per-battle matchup setup is:

| Battle IDs | Player side | Opponent side | Context and execution |
|---|---|---|---|
| `ROT-FIELD-B01`…`B05` | restored 40-troop RoT package below; no allies | one new ordinary roaming party per battle; actual roster recorded | field; default formations; `F1`, `F3`; no autoresolve; zero player attacks |
| `NS-FIELD-B01`…`B05` | restored 45-troop NS package below; no allies | one new ordinary roaming party per battle; actual roster recorded | field; default formations; `F1`, `F3`; no autoresolve; zero player attacks |

## Exact Realm of Thrones roster package

For each of `ROT-FIELD-B01` through `ROT-FIELD-B05`, the player party must contain exactly five healthy, deployable troops of each target below, plus the player character:

| Count | Display name | Canonical ID |
|---:|---|---|
| 5 | Ravens' Teeth | `ravens_teeth` |
| 5 | Goldenheart Warrior | `summer_master_longbowman` |
| 5 | Celtigar Banneret | `celtigar_banneret` |
| 5 | Lyseni Enforcer | `lyseni_enforcer` |
| 5 | Myrish Artisan of War | `myrish_artisan` |
| 5 | Golden Company Mahout | `golden_elite_pikeman` |
| 5 | Sarnori Spider | `sarnor_spider` |
| 5 | Baratheon Hammerknight | `baratheon_pikeknight` |

That is 40 target troops per battle. Do not add other ordinary troops. Heroes/player rows may appear on the scoreboard but are recorded as `hero`/`player` and never ranked as troops.

## Exact Nightmare Sails roster package

For each of `NS-FIELD-B01` through `NS-FIELD-B05`, the player party must contain exactly five healthy, deployable troops of each target below, plus the player character:

| Count | Display name | Canonical ID |
|---:|---|---|
| 5 | Nord Huscarl | `nord_huscarl` |
| 5 | Battanian Wildling | `battanian_wildling` |
| 5 | Imperial Elite Cataphract | `imperial_elite_cataphract` |
| 5 | Khuzait Khan's Guard | `khuzait_khans_guard` |
| 5 | Vlandian Marinier | `vlandian_marine_t5` |
| 5 | Aserai Bahriyyah | `aserai_marine_t5` |
| 5 | Battanian Skipari | `battanian_marine_t5` |
| 5 | Imperial Naute | `empire_marine_t5` |
| 5 | Sturgian Reaver | `sturgia_marine_t5` |

That is 45 target troops per battle. Do not add other ordinary troops. NavalDLC/War Sails units are intentional and must be kept.

## Capture every battle result

On the final result screen, before closing it:

1. Screenshot the whole visible table at native resolution.
2. Scroll and take overlapping pages until both sides and every party/troop row have been captured. A partial visible table is not permission to infer hidden rows.
3. Keep the original PNG files; do not crop, resize, recompress, annotate, or rename after calculating hashes.
4. Record every visible side-total, party, troop, player, and hero row exactly as displayed.
5. Record the six numeric columns exactly: `survivors`, `kills`, `upgrade_ready`, `deaths`, `wounded`, `routed`.
6. Derive `deployed = survivors + deaths + wounded` and `casualties = deaths + wounded`. Never add `routed` to deployed.
7. If a name or number is uncertain, leave its typed value empty, retain the raw visible text where possible, set `analysis_status=unresolved`, and describe the field in `provenance.uncertain_fields`. Do not guess.
8. Record the actual result (`victory`, `defeat`, or `retreat`), whether the player was attacker or defender, the displayed party/group hierarchy, capture time with timezone, game version, track, active modules, terrain/map description, enemy party size/composition, difficulty/battle-size settings, and any setup/order/player-intervention deviation.

## Screenshot file names and hashes

Use these names, adding page numbers as needed:

```text
screenshots/rot_field_20260731_B01_results_p01.png
screenshots/rot_field_20260731_B01_results_p02.png
...
screenshots/ns_field_20260731_B05_results_p01.png
```

After all files are final, calculate SHA-256 in PowerShell:

```powershell
Get-ChildItem .\screenshots\*.png | Sort-Object Name | ForEach-Object {
  [PSCustomObject]@{
    file = $_.Name
    sha256 = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
  }
} | Export-Csv .\screenshot_hashes.csv -NoTypeInformation -Encoding utf8
```

Do not hash a file and then edit or rename it.

## CSV encoding rules

- UTF-8, comma delimiter, one header row, RFC 4180 quoting.
- Empty/unknown scalar values are empty CSV cells, not zero and not `N/A`.
- Boolean values are lowercase `true`/`false`.
- Timestamps use ISO 8601 with timezone, for example `2026-07-31T21:15:00-03:00`.
- Array and object cells contain compact valid JSON. Escape their quotes using ordinary CSV quoting.
- Integer counts are non-negative whole numbers.
- Rate fields, when supplied, use six decimals; otherwise leave them empty for deterministic normalization.
- `canonical_troop_id` is filled only for the target IDs printed above or another exact versioned audit match. Otherwise leave it empty.

The contracts below map directly to `data/combat_observations/schemas/v2/`. Do not add columns.

### `screenshots.csv`

Schema: `screenshot.schema.json`.

```csv
schema_version,screenshot_id,source_filename,source_sha256,captured_at,analysis_status,exclusion_reason,observation_ids,game_versions,game_tracks,code_commit_shas
```

Use `schema_version=2.0.0` and `analysis_status=canonical_source` for a usable original image. JSON-array cells include all linked occurrence IDs and the exact version/track; use `[]` for `code_commit_shas` at capture time.

### `battles.csv`

Schema: `battle.schema.json`.

```csv
schema_version,battle_id,battle_context,result,classification_source,original_image_inference,original_confidence,review_reason,source_image_sha256s,observation_ids,review_correction_ids,game_versions,game_tracks,code_commit_shas
```

Use `schema_version=2.0.0`, `battle_context=field`, and `classification_source=raw_extraction`. Array cells are JSON arrays. `source_image_sha256s` lists every page for that battle.

### `party_groups.csv`

Schema: `party-group.schema.json`.

```csv
schema_version,group_id,battle_id,parent_group_id,side,row_type,display_name_raw,relationship_to_player,aggregation_status
```

Use scoreboard sides `attacker`/`defender`; represent player-party association with `relationship_to_player=player_party`, `allied_party`, `enemy_party`, or `unknown`. Use only `side_total` or `party` for `row_type`.

### `troop_occurrences.csv`

Schema: `troop-occurrence.schema.json`.

```csv
schema_version,observation_id,battle_id,battle_context,side,parent_group,row_type,display_name_raw,canonical_troop_id,relationship_to_player,source,survivors,kills,upgrade_ready,deaths,wounded,routed,deployed,casualties,kills_per_deployed,survival_rate,death_rate,wounded_rate,casualty_rate,routed_rate,analysis_status,review_correction_ids,game,provenance
```

Use `schema_version=2.0.0`. `source`, `game`, and `provenance` are JSON objects:

```json
{"image_file":"screenshots/rot_field_20260731_B01_results_p01.png","image_sha256":"<64 lowercase hex>"}
```

```json
{"version":"<exact game version>","track":"realm_of_thrones","active_modules":["<module in load order>"]}
```

```json
{"capture_method":"manual_scoreboard_transcription","uncertain_fields":[],"map_or_terrain":"<as observed>","enemy_party_size":"<as observed>","difficulty":"<exact settings>","battle_size":"<exact setting>","orders":"F1,F3 once at start","player_attacks":0,"setup_deviations":[]}
```

For the Nightmare Sails file, set `game.track` to `nightmare_sails`. Use `row_type=troop`, `player`, `hero`, or `artifact`. `review_correction_ids` is `[]` at capture time. A readable row is `analysis_status=raw`; an uncertain row is `unresolved`.

`battle-troop-consolidation.schema.json`, `historical-aggregate.schema.json`, and `review-correction.schema.json` describe downstream derived/reviewed files. Do not hand-calculate or create them on the PC.

## Final validation and delivery

For each session separately:

1. Confirm exactly five distinct battle IDs and at least one screenshot per battle.
2. Confirm every screenshot hash is 64 lowercase hexadecimal characters and matches the file.
3. Confirm every `source.image_sha256` and every battle `source_image_sha256s` entry points to a captured image.
4. Confirm every occurrence refers to an existing battle, screenshot, and parent group.
5. Confirm numeric identities: `deployed = survivors + deaths + wounded` and `casualties = deaths + wounded` whenever all inputs are readable.
6. Confirm track names are exact and no row from the other session is present.
7. Confirm no off-screen row or uncertain digit was inferred.
8. Keep `screenshot_hashes.csv` beside the four contract CSVs as a transport check; Phase 1 will reconcile it into the canonical screenshot manifest.

Drop the complete RoT folder into:

```text
data/combat_observations/2026-07-31-rot-field-plan/source/
```

Drop the complete Nightmare Sails folder into:

```text
data/combat_observations/2026-07-31-ns-field-plan/source/
```

If you are not working in a repository checkout, create two ZIP files named `2026-07-31-rot-field-plan-source.zip` and `2026-07-31-ns-field-plan-source.zip`, preserving each `source/` directory shape, and deliver them unchanged to the repository operator. Do not combine the two tracks in one archive.

The later display gate is per troop, context, and side: **at least 5 independent battles AND at least 20 deployed troops**. Completing five battles does not guarantee the gate if a target did not actually deploy or its row was not captured.
