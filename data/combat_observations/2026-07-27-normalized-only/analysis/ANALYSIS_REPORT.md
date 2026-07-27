# Phase 2 analysis — combat_2026-07-27_222843_010541

## Result

The deterministic local analysis passed all structural, boundary, ranking, and hash checks. The repository-reconstructible normalized archive is the authoritative downstream input; raw screenshot retention is optional.

These rankings describe visible player-side campaign contribution. They are not a universal tier list, intrinsic-strength estimate, or causal equipment analysis.

## Coverage

- 10 independent battles: 4 field, 5 siege attack, 1 siege defense.
- 143 consolidated player-side ordinary-troop rows.
- 6 reliable troop/context rows and 70 insufficient-evidence rows under the 5-battle / 20-deployed gate.
- 6 of 48 display labels have a conservative exact canonical ID match.
- All 5 queued hero icon fields remain unresolved and excluded.

## Highest reliable siege-attack descriptive rates

| Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle bootstrap interval | Casualty rate |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `ravens_teeth` | 5 | 88 | 3.830 | 3.264–4.657 | 0.409 |
| 2 | `mallister_elite_archer` | 5 | 164 | 0.970 | 0.796–1.168 | 0.348 |
| 3 | `riverlands_ranger` | 5 | 175 | 0.817 | 0.638–0.921 | 0.337 |
| 4 | `blackwood_house_guard` | 5 | 98 | 0.776 | 0.340–1.231 | 0.286 |
| 5 | `mallister_house_guard` | 5 | 68 | 0.691 | 0.425–0.945 | 0.176 |

Field has only four independent battles and siege defense only one, so neither context produces a reliable row. Contexts are never pooled to manufacture an overall display gate. Siege attack reaches five battles and has 6 reliable rows.

## Limitations

- Victory-only, observational campaign data are confounded by army composition, difficulty, map, siege state, enemy composition, and player choices.
- Only visible scoreboard rows are represented; off-screen rows are not inferred.
- Canonical identity coverage is incomplete, so unresolved labels remain provisional.
- The original screenshots are not retained, so the five visual hero icon fields cannot be re-reviewed and remain unresolved; heroes are excluded from rankings.
- No earlier baseline comparison or model recalibration was performed.
