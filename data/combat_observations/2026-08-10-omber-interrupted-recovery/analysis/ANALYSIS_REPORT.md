# Phase 2 analysis — combat_2026-08-10_omber_interrupted_recovery

## Result

The deterministic local analysis passed all structural, boundary, ranking, and hash checks. The repository-reconstructible normalized archive is the authoritative downstream input; raw screenshot retention is optional.

These rankings describe visible player-side campaign contribution. They are not a universal tier list, intrinsic-strength estimate, or causal equipment analysis.

## Coverage

- 1 independent battle: 0 field, 1 siege attack, 0 siege defense.
- 9 consolidated player-side ordinary-troop rows.
- 0 reliable troop/context rows and 9 insufficient-evidence rows under the 5-battle / 20-deployed gate.
- 9 of 9 display labels have a conservative exact canonical ID match.
- Unresolved canonical labels: none.
- Exact-image review closes all 6 queued decisions as unreadable numeric values. They belong to two player/hero rows and four enemy-side rows, so none of the 9 eligible player-side ordinary-troop rows is excluded by these uncertainties.

## Batch-wide roster analysis

Every visible player-side ordinary troop is included by context. No focus troop was requested for this recovery batch.

### Reliable descriptive rates

No troop/context row reaches the configured display gate, so no reliable rate or bootstrap interval is displayed.

### Below-gate coverage

Rates remain available as machine-readable diagnostics in `ranking_complete.csv`; the report lists coverage and the exact evidence gap without promoting them.

| Context | Troop | Canonical ID | Battles | Deployed | More battles needed | More deployed needed |
|---|---|---|---:|---:|---:|---:|
| siege_attack | Unsullied [T6] | `unsullied` | 1 | 23 | 4 | 0 |
| siege_attack | Sarnori Spider [T6] | `sarnor_spider` | 1 | 53 | 4 | 0 |
| siege_attack | Sarnori Master Javelinier [T5] | `sarnor_master_javelinier` | 1 | 48 | 4 | 0 |
| siege_attack | Ibbenese Navigator [T6] | `ibbenese_navigator` | 1 | 28 | 4 | 0 |
| siege_attack | Sarnori Master Spearman [T5] | `sarnor_master_spearman` | 1 | 8 | 4 | 12 |
| siege_attack | Qartheen Enthroned Guardian [T6] | `enthroned_guardian` | 1 | 9 | 4 | 11 |
| siege_attack | Yi Ti Mounted Shi [T6] | `yiti_samurai` | 1 | 5 | 4 | 15 |
| siege_attack | Qartheen Longbowman [T5] | `qartheen_longbowman` | 1 | 12 | 4 | 8 |
| siege_attack | Qartheen Elite Hoplite [T5] | `qartheen_elite_hoplite` | 1 | 1 | 4 | 19 |

The only observed context has 1 independent battle. Contexts are never pooled to manufacture an overall display gate. Complete rates remain diagnostics only and do not support a tier conclusion by themselves.

## Interrupted-battle boundary

The 08m20s scoreboard is retained as one right-censored, independent
`siege_attack` observation with `result=active`. It records 716 player-side kills;
the nine visible eligible troop rows account for 290 of them. The unplayed remainder
and terminal result are unknown. Nothing is added from, subtracted against, or merged
with the 22:37 Casat field battle or any cleanup engagement.

## Limitations

- Victory-only, observational campaign data are confounded by army composition, difficulty, map, siege state, enemy composition, and player choices.
- Only visible scoreboard rows are represented; off-screen rows are not inferred.
- All nine visible eligible troop labels have exact matches in the versioned Realm of Thrones audit.
- The raw PNG is not retained in Git, but the exact external source was hash-verified and re-reviewed locally. Six non-primary queued values remain unreadable and their nulls are preserved.
- Because the scoreboard is active, its terminal outcome and any later combat contribution are unknown and are never estimated.
- No earlier baseline comparison or model recalibration was performed.
