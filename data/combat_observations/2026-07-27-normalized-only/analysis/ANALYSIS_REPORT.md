# Phase 2 analysis — 2026-07-27 Realm of Thrones batch

## Result

The deterministic local analysis passed all structural, boundary, ranking, and hash checks. Merge remains blocked only because the exact original source ZIP is not repository-addressable.

These rankings describe visible player-side campaign contribution. They are not a universal tier list, intrinsic-strength estimate, or causal equipment analysis.

## Coverage

- 10 independent battles: 4 field, 5 siege attack, 1 siege defense.
- 143 consolidated player-side ordinary-troop rows.
- 17 reliable troop/context rows and 107 insufficient-evidence rows under the 5-battle / 20-deployed gate.
- 6 of 48 display labels have a conservative exact canonical ID match.
- All 5 queued hero icon fields remain unresolved and excluded.

## Highest reliable overall descriptive rates

| Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle bootstrap interval | Casualty rate |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `northern_winter_champion` | 5 | 34 | 4.353 | 0.359–15.538 | 0.353 |
| 2 | `ravens_teeth` | 10 | 184 | 3.565 | 2.719–4.622 | 0.196 |
| 3 | `mallister_elite_archer` | 10 | 331 | 1.127 | 0.608–1.953 | 0.190 |
| 4 | `westerlands_banner_knight` | 7 | 58 | 0.948 | 0.696–1.145 | 0.121 |
| 5 | `riverlands_ranger` | 10 | 394 | 0.934 | 0.661–1.224 | 0.170 |

Field has only four independent battles and siege defense only one, so neither context produces a reliable row. Siege attack reaches five battles and has 6 reliable rows.

## Limitations

- Victory-only, observational campaign data are confounded by army composition, difficulty, map, siege state, enemy composition, and player choices.
- Only visible scoreboard rows are represented; off-screen rows are not inferred.
- Canonical identity coverage is incomplete, so unresolved labels remain provisional.
- The original screenshots cannot be re-reviewed until the exact source ZIP is restored.
- No earlier baseline comparison or model recalibration was performed.
