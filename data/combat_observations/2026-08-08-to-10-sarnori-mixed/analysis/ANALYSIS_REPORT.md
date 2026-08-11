# Phase 2 analysis — combat_2026-08-08_to_10_sarnori_mixed

## Result

The deterministic local analysis passed all structural, boundary, ranking, and hash checks. The repository-reconstructible normalized archive is the authoritative downstream input; raw screenshot retention is optional.

These rankings describe visible player-side campaign contribution. They are not a universal tier list, intrinsic-strength estimate, or causal equipment analysis.

## Coverage

- 6 independent battles: 3 field, 3 siege attack, 0 siege defense.
- 71 consolidated player-side ordinary-troop rows.
- 0 reliable troop/context rows and 48 insufficient-evidence rows under the 5-battle / 20-deployed gate.
- 27 of 30 display labels have a conservative exact canonical ID match.
- Unresolved canonical labels: Dothraki Barbarian [T5], Dothraki Savage [T4], Lorathi Noble Youth [T2].
- All 13 queued fields remain unresolved; their source rows remain excluded from ordinary-troop rankings.

## Reliable descriptive rates

No troop/context row reaches the 5-independent-battle / 20-deployed display gate, so no reliable ranking or bootstrap interval is displayed.

## Requested Sarnori family by context

| Context | Troop | Canonical ID | Battles | Deployed | Kills/deployed | Casualty rate | Evidence gate |
|---|---|---|---:|---:|---:|---:|---|
| field | Sarnori Spider [T6] | `sarnor_spider` | 2 | 107 | 2.486 | 0.673 | insufficient_evidence |
| field | Sarnori Master Javelinier [T5] | `sarnor_master_javelinier` | 3 | 71 | 2.915 | 0.338 | insufficient_evidence |
| field | Sarnori Master Spearman [T5] | `sarnor_master_spearman` | 2 | 21 | 2.286 | 0.238 | insufficient_evidence |
| field | Sarnori Javelineer [T3] | `sarnor_javelinier` | 1 | 16 | — | — | insufficient_evidence |
| field | Sarnori Elite Javelinier [T4] | `sarnor_elite_javelinier` | 1 | 7 | — | — | insufficient_evidence |
| field | Sarnori Archer [T3] | `sarnor_archer` | 1 | 5 | — | — | insufficient_evidence |
| field | Sarnori Elite Archer [T4] | `sarnor_elite_archer` | 1 | 1 | — | — | insufficient_evidence |
| field | Sarnori Longbowman [T5] | `sarnor_longbowman` | 1 | 11 | — | — | insufficient_evidence |
| siege_attack | Sarnori Spider [T6] | `sarnor_spider` | 3 | 125 | 2.416 | 0.184 | insufficient_evidence |
| siege_attack | Sarnori Master Javelinier [T5] | `sarnor_master_javelinier` | 3 | 115 | 1.513 | 0.157 | insufficient_evidence |
| siege_attack | Sarnori Master Spearman [T5] | `sarnor_master_spearman` | 1 | 25 | 1.480 | 0.080 | insufficient_evidence |
| siege_attack | Sarnori Javelineer [T3] | `sarnor_javelinier` | 2 | 5 | — | — | insufficient_evidence |
| siege_attack | Sarnori Elite Javelinier [T4] | `sarnor_elite_javelinier` | 3 | 24 | 0.917 | 0.292 | insufficient_evidence |
| siege_attack | Sarnori Archer [T3] | `sarnor_archer` | 1 | 1 | — | — | insufficient_evidence |
| siege_attack | Sarnori Elite Archer [T4] | `sarnor_elite_archer` | 1 | 2 | — | — | insufficient_evidence |
| siege_attack | Sarnori Longbowman [T5] | `sarnor_longbowman` | 0 | 0 | — | — | not_observed |

Each observed context has at most 3 independent battles. Contexts are never pooled to manufacture an overall display gate. Complete rates remain diagnostics only and do not support the provisional S-tier conclusion.

## Limitations

- Victory-only, observational campaign data are confounded by army composition, difficulty, map, siege state, enemy composition, and player choices.
- Only visible scoreboard rows are represented; off-screen rows are not inferred.
- Canonical identity coverage is incomplete, so unresolved labels remain provisional.
- The original screenshots are not retained, so 13 queued fields cannot be re-reviewed and remain unresolved; queued rows are excluded from rankings.
- No earlier baseline comparison or model recalibration was performed.
