# Phase 2 analysis — combat_2026-08-11_ravens_teeth_field_compatible

## Result

All 3 normalized archive hashes and internal manifests passed, as did the common field projection's track, version, context, and row-arithmetic checks. The 1.1.0, 2.0.0 normalized schemas are joined only through their shared player-side ordinary-troop count fields; upgrade icons and whole-army contribution are outside this projection.

Boundary flags absent from historical normalization reports are recorded as unverified, not inferred. The compatibility decision is an explicit analytical judgment over the verified common fields, not a claim of full schema equivalence.

The current cohort alone has 4 independent field battles and 22 visible ordinary-troop labels. Because this is below the 5-battle gate, none can clear the standalone battle-count requirement. Across the compatible evidence there are 10 distinct field battles, 7 reliable rows, and 31 insufficient rows under the 5-battle / 20-deployed rule.

These are descriptive rates for visible player-side campaign rows. They are not an intrinsic-strength tier list, universal score, or causal estimate.

## Reliable combined field ranking

| Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle bootstrap interval | Casualty rate |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `ravens_teeth` | 9 | 404 | 3.153 | 1.816–4.358 | 0.040 |
| 2 | `blackwood_longbowman` | 7 | 97 | 1.433 | 1.191–1.592 | 0.093 |
| 3 | `river_admiral` | 6 | 50 | 1.340 | 0.500–2.250 | 0.480 |
| 4 | `river_ranger` | 6 | 175 | 1.063 | 0.428–1.632 | 0.029 |
| 5 | `blackwood_archer` | 5 | 104 | 0.875 | 0.704–0.985 | 0.048 |
| 6 | `westerlands_banner_knight` | 5 | 33 | 0.818 | 0.433–1.089 | 0.091 |
| 7 | `mallister_houseguard` | 6 | 117 | 0.547 | 0.282–0.726 | 0.068 |

## Ravens' Teeth focus

- Baseline cohort: 5 battles, 86 deployed, 3.326 kills/deployed (95% battle bootstrap 1.855–5.415); casualty rate 0.000.
- Current cohort: 4 battles, 318 deployed; rate withheld because this cohort is below the display gate.
- Compatible combined estimate: 9 battles, 404 deployed, 3.153 kills/deployed (95% battle bootstrap 1.816–4.358); casualty rate 0.040.
- The machine-readable delta remains `diagnostic_only_current_below_display_gate`; no increase or decline is claimed from the 4-battle current cohort.

## Identity and completeness

- 30 of 38 observed labels have one exact canonical ID in the versioned Realm of Thrones audit.
- Unresolved canonical labels remain provisional: `northern_colonel`, `northern_hero`, `northern_horseman`, `northern_mounted_warlord`, `northern_ranger`, `northern_sergeant`, `northern_soldier`, `westerlands_banner_knight`.
- `combined_ranking_complete.csv` retains every observed field label; `combined_ranking_reliable.csv` and `combined_insufficient_evidence.csv` split it without dropping low-sample rows.
- Rows marked for review and non-field battles are rejected from the projection. Where historical validation reports omit explicit side, hero, or off-screen flags, that missing verification is preserved in `compatibility_decision.json`.

## Limitations

- All screenshots are victory-only observational campaign evidence, confounded by army composition, enemy composition, map, difficulty, and player choices.
- Row visibility is partial, so total-army contribution, deployment share, and off-screen performance cannot be calculated.
- Raw PNGs for the current batch are not retained; its 12 field-level review decisions remain unresolved in the separate review layer.
- The schema join across 1.1.0, 2.0.0 is deliberately narrow. It does not imply that every field is interchangeable.
- No frozen model was changed or recalibrated.
