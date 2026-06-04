# Empirical Battle Result Findings — Screenshots 2026-05-29 to 2026-06-04

## Status

This is a **manual high-confidence normalization** of the visible battle-result screenshots supplied in chat. It is intended as a repo-ready empirical-validation layer for the Bannerlord troop model.

Current model baseline referenced here:

```txt
v7.1 — head-weighted survivability armor
survivability_armor = 0.55 body + 0.35 head + 0.05 arm + 0.05 leg
```

## Parsing assumptions

The battle-result columns were interpreted as:

```txt
ready_alive, kills, upgrades, dead, wounded, prisoners
```

Derived metrics:

```txt
estimated_present = ready_alive + dead + wounded
kills_per_present = kills / estimated_present
casualty_rate = (dead + wounded) / estimated_present
```

Rows with unclear numbers were either omitted or marked `transcription_confidence = medium`. No mass OCR was used.

## Headline findings

### 1. Imperial Naute is a clear burst/skirmish overperformer

In the normalized sample, Imperial Naute has repeated high-output rows across short and medium field engagements.

Representative rows:

| Battle | Side | Ready | Kills | Dead | Wounded | Estimated present | Kills/present |
|---|---|---:|---:|---:|---:|---:|---:|
| BR-20260603-162358 | Darim | 6 | 11 | 0 | 0 | 6 | 1.83 |
| BR-20260603-153520 | Darim | 2 | 6 | 0 | 0 | 2 | 3.00 |
| BR-20260603-222535 | Darim | 8 | 22 | 1 | 2 | 11 | 2.00 |
| BR-20260603-234916 | Darim | 18 | 32 | 5 | 12 | 35 | 0.91 |
| BR-20260603-233549 | Darim | 24 | 22 | 3 | 3 | 30 | 0.73 |
| BR-20260603-194632 | Darim | 8 | 14 | 0 | 3 | 11 | 1.27 |

Interpretation:

```txt
Imperial Naute should remain around good-T5 in general_score,
but should rise sharply in burst_score / boarding_score / short_engagement_score.
```

### 2. Khan's Guard remains validated as S-tier

Khan's Guard shows strong output plus low casualties across several contexts. It does not always have the highest kills/present, but its combination of output, survivability, and consistency remains consistent with rank #1 in v7.1.

### 3. Imperial Sergeant Crossbowman is empirically stable

The Sergeant Crossbowman produced several consistent high rows, especially in defensive and mixed-field contexts. This supports the v7 roster-first crossbow fix: vanilla/Empire crossbowmen are strong, while the old War Sails crossbow overcount was the bug.

### 4. War Sails Nord infantry looks strong but not model-breaking

Nord Ulfhedinn, Berserkir, Sky-Gods Chosen, and Skjaldbrestir all show good rows, but also meaningful casualties and variance. This supports the v7/v7.1 correction that removed the old false `Nord Huscarl #1 overall` result.

### 5. Siege/chokepoint results should be separated from open-field results

The siege-defense screenshot creates extreme ranged values, e.g. Khan's Guard and crossbowmen. These should be used for a separate `siege_defense_score`, not blended directly into the generic field-combat model.

## Recommended model follow-up

Do **not** replace v7.1 yet. Add parallel empirical/context scores:

```txt
general_score
burst_score
boarding_score
siege_defense_score
short_engagement_score
```

Suggested immediate v7.2 addition:

```txt
burst_score = function(throw_pressure, throw_ammo, throwing_skill, first_contact_context)
boarding_score = burst_score + shield_value + athletics + short_melee_fallback
siege_defense_score = ranged_pressure + ammo_capacity + defensive_position_multiplier
```

## Data files

- `empirical_battle_results_normalized.csv` — row-level normalized battle result observations.
- `empirical_troop_aggregate_summary.csv` — troop-level aggregate empirical metrics.
- `empirical_findings_2026-06-04.md` — this findings note.
- `screenshot_manifest.csv` — screenshot-level inventory.

## Limitations

- Manual transcription from screenshots; not raw game telemetry.
- Several battles include RoT/modded troops, so enemy quality and context are not controlled.
- Some rows are from siege/village/chokepoint contexts, which inflate ranged and burst troops.
- No direct hit-location telemetry yet.

## Repository note

This folder is intended to be added under:

```txt
analysis/empirical/screenshots_2026-05-29_2026-06-04/
```
