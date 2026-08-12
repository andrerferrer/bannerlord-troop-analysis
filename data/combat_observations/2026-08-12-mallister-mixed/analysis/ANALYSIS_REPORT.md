# Phase 2 analysis — combat_2026-08-12_mallister_field_compatible

## Result

All 4 normalized archive hashes and internal manifests passed, as did the common field projection's track, version, context, and row-arithmetic checks. The 1.1.0, 2.0.0 normalized schemas are joined only through their shared player-side ordinary-troop count fields; upgrade icons and whole-army contribution are outside this projection.

Boundary flags absent from historical normalization reports are recorded as unverified, not inferred. The compatibility decision is an explicit analytical judgment over the verified common fields, not a claim of full schema equivalence.

The current cohort alone has 4 independent field battles and 27 visible ordinary-troop labels. Because this is below the 5-battle gate, none can clear the standalone battle-count requirement. Across the compatible evidence there are 14 distinct field battles, 11 reliable rows, and 42 insufficient rows under the 5-battle / 20-deployed rule.

These are descriptive rates for visible player-side campaign rows. They are not an intrinsic-strength tier list, universal score, or causal estimate.

## Reliable combined field ranking

| Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle bootstrap interval | Casualty rate |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `ravens_teeth` | 9 | 404 | 3.153 | 1.825–4.365 | 0.040 |
| 2 | `river_axeman` | 5 | 38 | 1.763 | 1.048–2.793 | 0.447 |
| 3 | `river_admiral` | 8 | 71 | 1.634 | 0.797–2.532 | 0.451 |
| 4 | `blackwood_longbowman` | 7 | 97 | 1.433 | 1.173–1.588 | 0.093 |
| 5 | `river_ranger` | 7 | 185 | 1.168 | 0.584–1.831 | 0.032 |
| 6 | `river_calvary` | 6 | 29 | 1.103 | 0.800–1.375 | 0.276 |
| 7 | `mallister_elite_archer` | 8 | 340 | 1.065 | 0.561–1.482 | 0.056 |
| 8 | `mallister_knight` | 8 | 177 | 0.932 | 0.577–1.324 | 0.215 |
| 9 | `blackwood_archer` | 5 | 104 | 0.875 | 0.704–0.985 | 0.048 |
| 10 | `westerlands_banner_knight` (provisional) | 5 | 33 | 0.818 | 0.433–1.087 | 0.091 |

## Mallister Elite Archer focus

- Baseline cohort: 4 battles, 135 deployed; rate withheld because this cohort is below the display gate.
- Current cohort: 4 battles, 205 deployed; rate withheld because this cohort is below the display gate.
- Compatible combined estimate: 8 battles, 340 deployed, 1.065 kills/deployed (95% battle bootstrap 0.561–1.482); casualty rate 0.056.
- The machine-readable delta remains `diagnostic_only_below_display_gate`; below-gate cohorts: baseline, current. No increase or decline is claimed.

## Identity and completeness

- 42 of 53 observed labels have one exact canonical ID in the versioned audit for track `realm_of_thrones`.
- Unresolved canonical labels remain provisional: `brigand`, `broken_man`, `northern_colonel`, `northern_hero`, `northern_horseman`, `northern_mounted_warlord`, `northern_ranger`, `northern_sergeant`, `northern_soldier`, `westerlands_banner_knight`, `westerlands_recruit`.
- `combined_ranking_complete.csv` retains every observed field label; `combined_ranking_reliable.csv` and `combined_insufficient_evidence.csv` split it without dropping low-sample rows.
- Rows marked for review and non-field battles are rejected from the projection. Where historical validation reports omit explicit side, hero, or off-screen flags, that missing verification is preserved in `compatibility_decision.json`.

## Limitations

- All screenshots are victory-only observational campaign evidence, confounded by army composition, enemy composition, map, difficulty, and player choices.
- Row visibility is partial, so total-army contribution, deployment share, and off-screen performance cannot be calculated.
- Raw PNGs for the current batch are not retained; its 13 field-level review decisions remain unresolved in the separate review layer.
- The schema join across 1.1.0, 2.0.0 is deliberately narrow. It does not imply that every field is interchangeable.
- No frozen model was changed or recalibrated.
