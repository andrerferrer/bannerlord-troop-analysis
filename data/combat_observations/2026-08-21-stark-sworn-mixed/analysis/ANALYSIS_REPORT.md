# Phase 2 analysis — combat_2026-08-21_stark_sworn_mixed

## Result

The deterministic local analysis passed all structural, boundary, ranking, and hash checks. The repository-reconstructible normalized archive is the authoritative downstream input; raw screenshot retention is optional.

These rankings describe visible player-side campaign contribution. They are not a universal tier list, intrinsic-strength estimate, or causal equipment analysis.

## Coverage

- 9 independent battles: 5 field, 4 siege attack, 0 siege defense.
- 106 consolidated player-side ordinary-troop rows.
- 1 reliable troop/context rows and 66 insufficient-evidence rows under the 5-battle / 20-deployed gate.
- 24 of 43 display labels have a conservative exact canonical ID match.
- Unresolved canonical labels: Andal Caravan Guard [T4], Andal Convoy Guard [T4], Andal Veteran Convoy Guard [T5], Hired Crossbow [T4], Northern Archer [T4], Northern Colonel [T5], Northern Man at Arms [T3], Northern Raider [T3], Northern Ranger [T5], Northern Sergeant [T4], Northern Woodsman [T2], Pirate [T2], Ravager [T3], Reaver [T4], Westerlands Banner Knight [T6], Westerlands Footman [T2], Westerlands Halberdier [T5], Westerlands Infantry [T3], Westerlands Sharpshooter [T5].
- Exact-image review closes 16 of 17 queued fields: 15 hero upgrade icons are
  non-numeric UI indicators and Silverhill's obscured attacker-side deaths total
  is 30 from the exact same-screen player-party row. Northern Soldier's cursor-covered
  kills cell remains null. No queued row enters ordinary-troop rankings.

## Batch-wide roster analysis

Every visible player-side ordinary troop is included by context. Requested focus troops receive an additive deep dive and never filter this batch-wide analysis.

### Reliable descriptive rates

| Context | Efficiency rank | Impact rank | Troop | Canonical ID | Battles | Deployed | Kills/deployed | Player kill share | 95% battle bootstrap interval | Casualty rate |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| field | 1 | 1 | Stark Sworn Sword [T6] | `stark_swornsword` | 5 | 255 | 1.973 | 25.7% | 1.565–2.391 | 0.616 |

### Below-gate coverage

Rates remain available as machine-readable diagnostics in `ranking_complete.csv`; the report lists coverage and the exact evidence gap without promoting them.

| Context | Troop | Canonical ID | Battles | Deployed | More battles needed | More deployed needed |
|---|---|---|---:|---:|---:|---:|
| field | Riverlands Axeman [T5] | `river_axeman` | 1 | 3 | 4 | 17 |
| field | Westerlands Sharpshooter [T5] | `westerlands_sharpshooter (provisional)` | 1 | 1 | 4 | 19 |
| field | Gold Cloak Halberdier [T5] | `kingsguard` | 2 | 30 | 3 | 0 |
| field | Westerlands Infantry [T3] | `westerlands_infantry (provisional)` | 1 | 2 | 4 | 18 |
| field | Hired Crossbow [T4] | `hired_crossbow (provisional)` | 1 | 3 | 4 | 17 |
| field | Riverlands Footman [T2] | `river_footman` | 1 | 2 | 4 | 18 |
| field | Gold Cloak Petty Officer [T4] | `goldcloak_officer` | 2 | 8 | 3 | 12 |
| field | Northern Colonel [T5] | `northern_colonel (provisional)` | 4 | 111 | 1 | 0 |
| field | Riverlands Man at Arms [T4] | `river_man_at_arms` | 2 | 11 | 3 | 9 |
| field | Riverlands Elite Archer [T4] | `river_elite_archer` | 2 | 8 | 3 | 12 |
| field | Stark Master Longbowman [T5] | `stark_master_archer` | 1 | 58 | 4 | 0 |
| field | Riverlands Soldier [T3] | `river_soldier` | 1 | 15 | 4 | 5 |
| field | Northern Raider [T3] | `northern_raider (provisional)` | 1 | 3 | 4 | 17 |
| field | Northern Man at Arms [T3] | `northern_man_at_arms (provisional)` | 1 | 7 | 4 | 13 |
| field | Northern Ranger [T5] | `northern_ranger (provisional)` | 3 | 316 | 2 | 0 |
| field | Reaver [T4] | `reaver (provisional)` | 1 | 70 | 4 | 0 |
| field | Stark House Guard [T5] | `stark_houseguard` | 3 | 72 | 2 | 0 |
| field | Riverlands Admiral [T6] | `river_admiral` | 2 | 4 | 3 | 16 |
| field | Northern Woodsman [T2] | `northern_woodsman (provisional)` | 1 | 1 | 4 | 19 |
| field | Gold Cloak Soldier [T3] | `goldcloak_soldier` | 2 | 31 | 3 | 0 |
| field | Northern Archer [T4] | `northern_archer (provisional)` | 1 | 24 | 4 | 0 |
| field | Northern Sergeant [T4] | `northern_sergeant (provisional)` | 2 | 14 | 3 | 6 |
| field | Gold Cloak Sniper [T5] | `goldcloak_master_archer` | 3 | 111 | 2 | 0 |
| field | Westerlands Footman [T2] | `westerlands_footman (provisional)` | 1 | 6 | 4 | 14 |
| field | Stark Soldier [T4] | `stark_soldier` | 3 | 58 | 2 | 0 |
| field | Ravager [T3] | `ravager (provisional)` | 1 | 5 | 4 | 15 |
| field | Crownlands Levy [T2] | `crownlands_levy` | 3 | 30 | 2 | 0 |
| field | Gold Cloak Elite Archer [T4] | `goldcloak_elite_archer` | 1 | 22 | 4 | 0 |
| field | Gold Cloak Archer [T3] | `goldcloak_archer` | 1 | 23 | 4 | 0 |
| field | Stark Footman [T3] | `stark_footman` | 2 | 29 | 3 | 0 |
| field | Andal Convoy Guard [T4] | `andal_convoy_guard (provisional)` | 1 | 6 | 4 | 14 |
| field | Andal Veteran Convoy Guard [T5] | `andal_veteran_convoy_guard (provisional)` | 1 | 4 | 4 | 16 |
| field | Andal Caravan Guard [T4] | `andal_caravan_guard (provisional)` | 1 | 6 | 4 | 14 |
| field | Crownlands Recruit [T1] | `crownlands_recruit` | 1 | 20 | 4 | 0 |
| siege_attack | Riverlands Axeman [T5] | `river_axeman` | 2 | 8 | 3 | 12 |
| siege_attack | Riverlands Admiral [T6] | `river_admiral` | 1 | 3 | 4 | 17 |
| siege_attack | Northern Archer [T4] | `northern_archer (provisional)` | 1 | 2 | 4 | 18 |
| siege_attack | Westerlands Banner Knight [T6] | `westerlands_banner_knight (provisional)` | 1 | 1 | 4 | 19 |
| siege_attack | Stark House Guard [T5] | `stark_houseguard` | 2 | 29 | 3 | 0 |
| siege_attack | Stark Soldier [T4] | `stark_soldier` | 1 | 33 | 4 | 0 |
| siege_attack | Andal Convoy Guard [T4] | `andal_convoy_guard (provisional)` | 1 | 8 | 4 | 12 |
| siege_attack | Reaver [T4] | `reaver (provisional)` | 1 | 33 | 4 | 0 |
| siege_attack | Ravager [T3] | `ravager (provisional)` | 1 | 18 | 4 | 2 |
| siege_attack | Northern Ranger [T5] | `northern_ranger (provisional)` | 3 | 394 | 2 | 0 |
| siege_attack | Gold Cloak Sniper [T5] | `goldcloak_master_archer` | 3 | 170 | 2 | 0 |
| siege_attack | Stark Levy [T2] | `stark_levy` | 1 | 33 | 4 | 0 |
| siege_attack | Andal Veteran Convoy Guard [T5] | `andal_veteran_convoy_guard (provisional)` | 1 | 5 | 4 | 15 |
| siege_attack | Westerlands Halberdier [T5] | `westerlands_halberdier (provisional)` | 1 | 1 | 4 | 19 |
| siege_attack | Stark Sworn Sword [T6] | `stark_swornsword` | 4 | 191 | 1 | 0 |
| siege_attack | Northern Colonel [T5] | `northern_colonel (provisional)` | 3 | 75 | 2 | 0 |
| siege_attack | Stark Master Longbowman [T5] | `stark_master_archer` | 2 | 27 | 3 | 0 |
| siege_attack | Gold Cloak Petty Officer [T4] | `goldcloak_officer` | 1 | 10 | 4 | 10 |
| siege_attack | Stark Footman [T3] | `stark_footman` | 1 | 44 | 4 | 0 |
| siege_attack | Gold Cloak Halberdier [T5] | `kingsguard` | 3 | 48 | 2 | 0 |
| siege_attack | Pirate [T2] | `pirate (provisional)` | 1 | 31 | 4 | 0 |
| siege_attack | Riverlands Ranger [T5] | `river_ranger` | 1 | 19 | 4 | 1 |
| siege_attack | Stark Longbowman [T4] | `stark_archer` | 1 | 38 | 4 | 0 |
| siege_attack | Stark Bowman [T3] | `stark_bowman` | 1 | 79 | 4 | 0 |
| siege_attack | Westerlands Footman [T2] | `westerlands_footman (provisional)` | 1 | 10 | 4 | 10 |
| siege_attack | Gold Cloak Elite Archer [T4] | `goldcloak_elite_archer` | 1 | 11 | 4 | 9 |
| siege_attack | Riverlands Soldier [T3] | `river_soldier` | 1 | 20 | 4 | 0 |
| siege_attack | Crownlands Levy [T2] | `crownlands_levy` | 1 | 9 | 4 | 11 |
| siege_attack | Gold Cloak Soldier [T3] | `goldcloak_soldier` | 1 | 17 | 4 | 3 |
| siege_attack | Riverlands Man at Arms [T4] | `river_man_at_arms` | 1 | 12 | 4 | 8 |
| siege_attack | Crownlands Recruit [T1] | `crownlands_recruit` | 1 | 38 | 4 | 0 |
| siege_attack | Riverlands Recruit [T1] | `river_recruit` | 1 | 40 | 4 | 0 |

## Requested focus troops by context

| Context | Troop | Canonical ID | Battles | Deployed | Kills/deployed | Casualty rate | Evidence gate |
|---|---|---|---:|---:|---:|---:|---|
| field | Stark Sworn Sword [T6] | `stark_swornsword` | 5 | 255 | 1.973 | 0.616 | reliable |
| siege_attack | Stark Sworn Sword [T6] | `stark_swornsword` | 4 | 191 | — | — | insufficient_evidence |

### Stark Sworn Sword deep dive

Field is sufficient under the 5-battle / 20-deployed gate:

- deployed: `25 + 62 + 61 + 39 + 68 = 255`;
- kills: `29 + 130 + 136 + 108 + 100 = 503`;
- efficiency: `503 / 255 = 1.972549` kills/deployed;
- explicit player-side kills: `140 + 486 + 591 + 378 + 361 = 1,956`;
- kill share: `503 / 1,956 = 0.257157`;
- share-adjusted impact: `(503 / 255) × (503 / 1,956) = 0.507256`;
- deaths: `1 + 4 + 5 + 6 + 5 = 21`, so death rate is `21 / 255 = 0.082353`;
- deaths plus wounded: `21 + 136 = 157`, so casualty rate is
  `157 / 255 = 0.615686`.

Siege attack remains below gate despite ample deployment: `4` battles,
`59 + 66 + 56 + 10 = 191` deployed, and `49 + 73 + 62 + 6 = 190` kills.
The diagnostic efficiency is `190 / 191 = 0.994764`; the explicit player-side
denominator is `270 + 554 + 312 + 363 = 1,499`, giving `190 / 1,499 = 0.126751`
kill share. One more independent siege attack is required; contexts are not pooled.

## Next troop and context

**Next distinct troop: `arryn_moonknight` (Arryn Winged Knight), field.** The
versioned mounted-melee screen ranks it first among below-gate near matches with
descriptive distance `5.250000`. Its compatible field coverage is 2 battles and
13 deployed, so the exact deficit is `5 - 2 = 3` field battles and
`20 - 13 = 7` deployed. Mallister Eagle Knight, the next structural neighbor,
already clears the gate and is retained as the observed contrast. See
`NEXT_TEST_RECOMMENDATION.md` for the full decision and source paths.

Each observed context has at most 5 independent battles. Contexts are never pooled to manufacture an overall display gate. Complete rates remain diagnostics only and do not support a tier conclusion by themselves.

## Limitations

- Victory-only, observational campaign data are confounded by army composition, difficulty, map, siege state, enemy composition, and player choices.
- Only visible scoreboard rows are represented; off-screen rows are not inferred.
- Canonical identity coverage is incomplete, so unresolved labels remain provisional.
- The original screenshots were locally hash-verified and re-reviewed. Fifteen
  hero icons are resolved as non-numeric, one non-ranking side total is resolved
  from the exact same-screen party row, and one Northern Soldier kills cell remains
  unreadable under the cursor. The immutable normalized null and exclusion remain.
- No earlier baseline comparison or model recalibration was performed.
