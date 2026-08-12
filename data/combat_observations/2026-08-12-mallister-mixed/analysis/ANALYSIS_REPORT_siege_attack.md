# Phase 2 analysis — combat_2026-08-12_mallister_siege_attack_compatible

## Result

All 2 normalized archive hashes and internal manifests passed, as did the common siege attack projection's track, version, context, and row-arithmetic checks. The 1.1.0, 2.0.0 normalized schemas are joined only through their shared player-side ordinary-troop count fields; upgrade icons and whole-army contribution are outside this projection.

Boundary flags absent from historical normalization reports are recorded as unverified, not inferred. The compatibility decision is an explicit analytical judgment over the verified common fields, not a claim of full schema equivalence.

The current cohort alone has 2 independent siege attack battles and 21 visible ordinary-troop labels. Because this is below the 5-battle gate, none can clear the standalone battle-count requirement. Across the compatible evidence there are 7 distinct siege attack battles, 6 reliable rows, and 44 insufficient rows under the 5-battle / 20-deployed rule.

These are descriptive rates for visible player-side campaign rows. They are not an intrinsic-strength tier list, universal score, or causal estimate.

## Reliable combined siege attack ranking

| Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle bootstrap interval | Casualty rate |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `ravens_teeth` | 5 | 88 | 3.830 | 3.330–4.657 | 0.409 |
| 2 | `mallister_elite_archer` | 7 | 322 | 1.208 | 0.899–1.529 | 0.516 |
| 3 | `mallister_knight` | 7 | 123 | 1.057 | 0.468–1.473 | 0.309 |
| 4 | `mallister_houseguard` | 7 | 137 | 0.971 | 0.607–1.242 | 0.328 |
| 5 | `river_ranger` | 7 | 181 | 0.834 | 0.692–0.960 | 0.354 |
| 6 | `blackwood_houseguard` | 5 | 98 | 0.776 | 0.340–1.231 | 0.286 |

## Mallister Elite Archer focus

- Baseline cohort: 5 battles, 164 deployed, 0.970 kills/deployed (95% battle bootstrap 0.796–1.188); casualty rate 0.348.
- Current cohort: 2 battles, 158 deployed; rate withheld because this cohort is below the display gate.
- Compatible combined estimate: 7 battles, 322 deployed, 1.208 kills/deployed (95% battle bootstrap 0.899–1.529); casualty rate 0.516.
- The machine-readable delta remains `diagnostic_only_below_display_gate`; below-gate cohorts: current. No increase or decline is claimed.

## Identity and completeness

- 37 of 50 observed labels have one exact canonical ID in the versioned audit for track `realm_of_thrones`.
- Unresolved canonical labels remain provisional: `moon_brother_woodsman`, `northern_archer`, `northern_colonel`, `northern_horseman`, `northern_mounted_warlord`, `northern_noble_warrior`, `northern_pikeman`, `northern_ranger`, `northern_scout`, `northern_winter_champion`, `northern_winter_warrior`, `westerlands_banner_knight`, `westerlands_sharpshooter`.
- `combined_ranking_complete_siege_attack.csv` retains every observed siege attack label; `combined_ranking_reliable_siege_attack.csv` and `combined_insufficient_evidence_siege_attack.csv` split it without dropping low-sample rows.
- Rows marked for review and non-siege attack battles are rejected from the projection. Where historical validation reports omit explicit side, hero, or off-screen flags, that missing verification is preserved in `compatibility_decision_siege_attack.json`.

## Limitations

- All screenshots are victory-only observational campaign evidence, confounded by army composition, enemy composition, map, difficulty, and player choices.
- Row visibility is partial, so total-army contribution, deployment share, and off-screen performance cannot be calculated.
- Raw PNGs for the current batch are not retained; its 13 field-level review decisions remain unresolved in the separate review layer.
- The schema join across 1.1.0, 2.0.0 is deliberately narrow. It does not imply that every field is interchangeable.
- No frozen model was changed or recalibrated.
