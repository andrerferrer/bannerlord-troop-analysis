# RoT Empirical Screenshot Intake — 2026-07-03

This document tracks the empirical battle-result screenshot intake uploaded on 2026-07-03.

## Input

Uploaded local file:

```txt
Armoury Crate SE 03_07_2026 13_28_44.zip
```

## Contents

| Type | Count |
|---|---:|
| Images | 45 |
| Videos | 1 |
| Likely battle result scoreboards | 33 |
| Non-scoreboard / supporting screenshots | 12 |
| Likely battle groups | 26 |

## What was normalized

The upload was normalized into an intake dataset:

```txt
screenshot_manifest_20260703.csv
battle_groups_20260703.csv
empirical_battles_template.csv
empirical_troop_rows_template.csv
```

The screenshots are grouped by timestamp so repeated scroll captures from the same battle can be transcribed into one battle record.

## Current status

Troop-row transcription is pending.

The upload contains many valid result scoreboards, but the individual table rows still need extraction into:

```txt
troop_name
healthy
dead
wounded
kills
unknown_yellow_tool
```

## Metrics to compute after transcription

```txt
estimated_present = healthy + dead + wounded
kills_per_present = kills / estimated_present
death_rate = dead / estimated_present
wounded_rate = wounded / estimated_present
casualty_rate = (dead + wounded) / estimated_present
deployed_share = estimated_present / side_total_present
kill_share = kills / side_total_kills
contribution_index = kill_share / deployed_share
campaign_contribution = contribution_index × (1 - death_rate - 0.35 × wounded_rate)
```

## Priority troops to extract first

```txt
Ravens' Teeth
Goldenheart Warrior
Celtigar Banneret
Lyseni Enforcer
Myrish Artisan of War
Ibbenese Navigator
Mallister House Guard
Mallister Eagle Knight
Westerling Hedgeknight
Grafton Flaming Knight
```

## Immediate analysis

The upload is useful for campaign-realistic validation. It contains enough battle result screenshots to start validating the V4.1 model with empirical contribution metrics.

The most important next output is not another theoretical ranking. It is a normalized empirical table that can answer:

```txt
which troops overperform their deployed share?
which troops kill well but die too much?
which troops are context-dependent?
which V4.1 candidates are false positives?
```

## Next step

Transcribe the battle result scoreboards into `empirical_troop_rows_template.csv`, then join against the V4.1 theoretical ranking.
