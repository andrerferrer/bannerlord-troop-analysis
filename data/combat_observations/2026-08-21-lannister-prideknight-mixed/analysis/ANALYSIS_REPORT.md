# Phase 2 analysis — combat_2026-08-21_lannister_prideknight_mixed

## Result

The deterministic local analysis passed all structural, boundary, ranking, and hash checks. The repository-reconstructible normalized archive is the authoritative downstream input; raw screenshot retention is optional.

These rankings describe visible player-side campaign contribution. They are not a universal tier list, intrinsic-strength estimate, or causal equipment analysis.

## Coverage

- 9 independent battles: 8 field, 1 siege attack, 0 siege defense.
- 110 consolidated player-side ordinary-troop rows.
- 7 reliable troop/context rows and 44 insufficient-evidence rows under the 5-battle / 20-deployed gate.
- 19 of 40 display labels have a conservative exact canonical ID match.
- Unresolved canonical labels: Northern Archer [T4], Northern Bowman [T3], Northern Colonel [T5], Northern Man at Arms [T4], Northern Mounted Warlord [T6], Northern Ranger [T5], Northern Sergeant [T4], Northern Woodsman [T2], Ravager [T3], Reaver [T4], Westerlands Banner Knight [T6], Westerlands Crossbowman [T3], Westerlands Duelist [T5], Westerlands Hardened Crossbowman [T4], Westerlands Horseman [T5], Westerlands Infantry [T3], Westerlands Master Longbowman [T5], Westerlands Sharpshooter [T5], Westerlands Skirmisher [T5], Westerlands Spearman [T3], Westerlands Swordsman [T4].
- Exact-image review resolved 4 of 6 queued fields as white non-numeric UI
  indicators. Jaime Lannister's kills and upgrade-ready cells remain null under
  the cursor. All five queued rows are heroes excluded from ordinary-troop rankings.

## Batch-wide roster analysis

Every visible player-side ordinary troop is included by context. Requested focus troops receive an additive deep dive and never filter this batch-wide analysis.

### Reliable descriptive rates

| Context | Efficiency rank | Impact rank | Troop | Canonical ID | Battles | Deployed | Kills/deployed | Player kill share | 95% battle bootstrap interval | Casualty rate |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|
| field | 1 | 5 | Westerlands Hardened Crossbowman [T4] | `westerlands_hardened_crossbowman` (provisional) | 5 | 37 | 2.514 | 5.5% | 0.467–3.600 | 0.135 |
| field | 2 | 1 | Westerlands Sharpshooter [T5] | `westerlands_sharpshooter` (provisional) | 7 | 295 | 1.861 | 20.9% | 0.930–2.777 | 0.271 |
| field | 3 | 21 | Northern Mounted Warlord [T6] | `northern_mounted_warlord` (provisional) | 5 | 25 | 1.440 | 2.9% | 0.960–1.840 | 0.000 |
| field | 4 | 22 | Westerlands Duelist [T5] | `westerlands_duelist` (provisional) | 7 | 90 | 1.100 | 3.8% | 0.648–1.537 | 0.778 |
| field | 5 | 2 | Lannister Prideknight [T6] | `lannister_prideknight` | 8 | 467 | 1.058 | 17.1% | 0.831–1.326 | 0.199 |
| field | 6 | 11 | Westerlands Banner Knight [T6] | `westerlands_banner_knight` (provisional) | 6 | 118 | 1.034 | 8.0% | 0.750–1.349 | 0.144 |
| field | 7 | 3 | Lannister Longbowman [T5] | `lannister_longbowman` | 8 | 448 | 0.991 | 15.4% | 0.526–1.583 | 0.176 |

### Below-gate coverage

Rates remain available as machine-readable diagnostics in `ranking_complete.csv`; the report lists coverage and the exact evidence gap without promoting them.

| Context | Troop | Canonical ID | Battles | Deployed | More battles needed | More deployed needed |
|---|---|---|---:|---:|---:|---:|
| field | White Harbor Pike Knight [T5] | `whiteharbor_elite_pikeman` | 1 | 1 | 4 | 19 |
| field | Northern Colonel [T5] | `northern_colonel (provisional)` | 2 | 3 | 3 | 17 |
| field | Northern Man at Arms [T4] | `northern_man_at_arms (provisional)` | 1 | 1 | 4 | 19 |
| field | Westerlands Master Longbowman [T5] | `westerlands_master_longbowman (provisional)` | 1 | 1 | 4 | 19 |
| field | Westerlands Skirmisher [T5] | `westerlands_skirmisher (provisional)` | 2 | 6 | 3 | 14 |
| field | Forest Bandit [T4] | `forest_bandits_chief` | 1 | 3 | 4 | 17 |
| field | Northern Sergeant [T4] | `northern_sergeant (provisional)` | 1 | 1 | 4 | 19 |
| field | Tully Longbowman [T5] | `tully_longbowman` | 1 | 1 | 4 | 19 |
| field | Northern Bowman [T3] | `northern_bowman (provisional)` | 1 | 8 | 4 | 12 |
| field | Reaver [T4] | `reaver (provisional)` | 1 | 5 | 4 | 15 |
| field | Westerlands Crossbowman [T3] | `westerlands_crossbowman (provisional)` | 4 | 33 | 1 | 0 |
| field | Lannister Archer [T4] | `lannister_archer` | 1 | 26 | 4 | 0 |
| field | Frey Horseman [T5] | `frey_horseman` | 1 | 1 | 4 | 19 |
| field | Lannister Bowman [T3] | `lannister_bowman` | 1 | 20 | 4 | 0 |
| field | Westerlands Infantry [T3] | `westerlands_infantry (provisional)` | 1 | 7 | 4 | 13 |
| field | Westerlands Swordsman [T4] | `westerlands_swordsman (provisional)` | 1 | 11 | 4 | 9 |
| field | Northern Archer [T4] | `northern_archer (provisional)` | 2 | 8 | 3 | 12 |
| field | Riverrun Captain [T6] | `riverrun_captain` | 3 | 12 | 2 | 8 |
| field | Lannister Levy [T2] | `lannister_levy` | 1 | 3 | 4 | 17 |
| field | Frey Assassin [T6] | `frey_assassin` | 3 | 22 | 2 | 0 |
| field | Ravager [T3] | `ravager (provisional)` | 1 | 12 | 4 | 8 |
| field | Northern Ranger [T5] | `northern_ranger (provisional)` | 4 | 56 | 1 | 0 |
| field | Lannister Knight [T5] | `lannister_knight` | 4 | 94 | 1 | 0 |
| field | Northern Woodsman [T2] | `northern_woodsman (provisional)` | 1 | 9 | 4 | 11 |
| field | Westerlands Horseman [T5] | `westerlands_horseman (provisional)` | 1 | 3 | 4 | 17 |
| field | Lannister Horseman [T4] | `lannister_horseman` | 3 | 130 | 2 | 0 |
| field | Lannister Footman [T3] | `lannister_footman` | 2 | 47 | 3 | 0 |
| field | Frey Sharpshooter [T5] | `frey_sharpshooter` | 2 | 3 | 3 | 17 |
| field | Riverlands Militia Spearman [T2] | `river_militia_spearman` | 1 | 28 | 4 | 0 |
| field | Westerlands Spearman [T3] | `westerlands_spearman (provisional)` | 1 | 5 | 4 | 15 |
| field | Frey Veteran Crossbowman [T4] | `frey_veteran_crossbowman` | 1 | 2 | 4 | 18 |
| field | Riverlands Militia Archer [T2] | `river_militia_archer` | 1 | 20 | 4 | 0 |
| field | Frey Crossbowman [T3] | `frey_crossbowman` | 1 | 1 | 4 | 19 |
| siege_attack | Frey Assassin [T6] | `frey_assassin` | 1 | 3 | 4 | 17 |
| siege_attack | Frey Sharpshooter [T5] | `frey_sharpshooter` | 1 | 3 | 4 | 17 |
| siege_attack | Frey Veteran Crossbowman [T4] | `frey_veteran_crossbowman` | 1 | 3 | 4 | 17 |
| siege_attack | Westerlands Sharpshooter [T5] | `westerlands_sharpshooter (provisional)` | 1 | 2 | 4 | 18 |
| siege_attack | Westerlands Hardened Crossbowman [T4] | `westerlands_hardened_crossbowman (provisional)` | 1 | 3 | 4 | 17 |
| siege_attack | Lannister Longbowman [T5] | `lannister_longbowman` | 1 | 61 | 4 | 0 |
| siege_attack | Frey Crossbowman [T3] | `frey_crossbowman` | 1 | 3 | 4 | 17 |
| siege_attack | Westerlands Crossbowman [T3] | `westerlands_crossbowman (provisional)` | 1 | 4 | 4 | 16 |
| siege_attack | Northern Mounted Warlord [T6] | `northern_mounted_warlord (provisional)` | 1 | 5 | 4 | 15 |
| siege_attack | Lannister Prideknight [T6] | `lannister_prideknight` | 1 | 85 | 4 | 0 |
| siege_attack | Westerlands Banner Knight [T6] | `westerlands_banner_knight (provisional)` | 1 | 33 | 4 | 0 |

## Requested focus troops by context

| Context | Troop | Canonical ID | Battles | Deployed | Kills/deployed | Casualty rate | Evidence gate |
|---|---|---|---:|---:|---:|---:|---|
| field | Lannister Prideknight [T6] | `lannister_prideknight` | 8 | 467 | 1.058 | 0.199 | reliable |
| siege_attack | Lannister Prideknight [T6] | `lannister_prideknight` | 1 | 85 | — | — | insufficient_evidence |

### Lannister Prideknight deep dive

The field test is sufficient and should stop:

- deployed: `19 + 37 + 39 + 53 + 56 + 76 + 93 + 94 = 467`;
- kills: `23 + 50 + 53 + 67 + 28 + 114 + 71 + 88 = 494`;
- efficiency: `494 / 467 = 1.057816` kills/deployed;
- explicit player-side kills: `687 + 267 + 677 + 500 + 181 + 248 + 130 + 191 = 2,881`;
- kill share: `494 / 2,881 = 0.171468`;
- share-adjusted impact: `(494 / 467) × (494 / 2,881) = 0.181382`;
- deaths: `0 + 0 + 9 + 6 + 0 + 1 + 0 + 0 = 16`, so death rate is
  `16 / 467 = 0.034261`;
- casualties: `16 + 77 = 93`, so casualty rate is `93 / 467 = 0.199143`.

Among the seven gate-clearing field rows, Prideknight is fifth by efficiency
and second by share-adjusted impact. This supports a **reliable high-volume
field contributor** description, not a universal tier or causal equipment claim.

Siege attack remains below gate: `1` battle, `85` deployed and `42` kills.
Its diagnostic efficiency is `42 / 85 = 0.494118`; the explicit side total is
`242`, giving `42 / 242 = 0.173554` kill share. It needs `5 - 1 = 4` more
independent siege attacks if that context is pursued.

## Candidate-signature comparison and next test

The versioned Captain-neighbor screen previously ranked Prideknight third at
distance `6.175000`, with no candidate-specific gate-clearing evidence. This
batch fills that gap with `8` field battles, `467` deployed and `494` kills.
Distance remains a descriptive mechanical-neighbor measure, not an
effectiveness score; frozen models are unchanged.

For context only, the existing incidental Mallister Eagle Knight aggregate is
`8` field battles / `177` deployed / `165` kills, or `165 / 177 = 0.932203`.
Prideknight's raw difference is `1.057816 - 0.932203 = 0.125612` kills per
deployed (`13.47%` higher relative to that aggregate), but the cohorts are not
controlled and the difference is not causal. Arryn Winged Knight remains below
gate at `2` field battles / `13` deployed / `12` kills (`12 / 13 = 0.923077`).

**Next: run the user's originally intended dedicated Mallister Eagle Knight
field retest.** Use five independent battles with at least 20 Eagle Knights per
battle (`5 × 20 = 100` new deployments), with Eagle Knight as the only/main T6
melee cavalry. The enemy Eagle Knight at 19:27 is not counted. Arryn remains
queued immediately after this user-priority retest.

Each observed context has at most 8 independent battles. Contexts are never pooled to manufacture an overall display gate. Complete rates remain diagnostics only and do not support a tier conclusion by themselves.

## Limitations

- Observational campaign data (8 victories and 1 defeat) are confounded by army composition, difficulty, map, siege state, enemy composition, and player choices.
- Only visible scoreboard rows are represented; off-screen rows are not inferred.
- Canonical identity coverage is incomplete, so unresolved labels remain provisional.
- The original screenshots are locally hash-verified and directly re-reviewed.
  Four hero icon fields are resolved as non-numeric; two Jaime cells remain
  cursor-obscured and null. Queued hero rows are excluded from rankings.
- No older Prideknight battle was pooled. Mallister and Arryn are descriptive
  external contrasts only; no causal delta or model recalibration was performed.
