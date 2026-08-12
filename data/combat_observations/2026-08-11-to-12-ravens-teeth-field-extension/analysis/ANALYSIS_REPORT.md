# Phase 2 analysis — combat_2026-08-11_to_12_ravens_teeth_field_extension_compatible

## Result

All 4 normalized archive hashes and internal manifests passed, as did the common field projection's track, version, context, and row-arithmetic checks. The 1.1.0, 2.0.0 normalized schemas are joined only through their shared player-side ordinary-troop count fields; upgrade icons and whole-army contribution are outside this projection.

Boundary flags absent from historical normalization reports are recorded as unverified, not inferred. The compatibility decision is an explicit analytical judgment over the verified common fields, not a claim of full schema equivalence.

The current cohort alone has 6 independent field battles and 33 visible ordinary-troop labels. Per-label standalone eligibility is evaluated against the configured battle and deployment gates. Across the compatible evidence there are 16 distinct field battles, 10 reliable rows, and 48 insufficient rows under the 5-battle / 20-deployed rule.

These are descriptive rates for visible player-side campaign rows. They are not an intrinsic-strength tier list, universal score, or causal estimate.

## Reliable combined field ranking

| Rank | Troop | Battles | Deployed | Kills/deployed | 95% battle bootstrap interval | Casualty rate |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `ravens_teeth` | 15 | 1089 | 2.331 | 1.746–3.081 | 0.117 |
| 2 | `blackwood_longbowman` | 7 | 97 | 1.433 | 1.186–1.592 | 0.093 |
| 3 | `river_admiral` | 7 | 52 | 1.308 | 0.500–2.143 | 0.462 |
| 4 | `river_ranger` | 9 | 204 | 0.961 | 0.393–1.436 | 0.074 |
| 5 | `river_axeman` | 5 | 46 | 0.891 | 0.372–1.512 | 0.413 |
| 6 | `blackwood_archer` | 5 | 104 | 0.875 | 0.704–0.991 | 0.048 |
| 7 | `westerlands_banner_knight` (provisional) | 10 | 63 | 0.857 | 0.429–1.313 | 0.238 |
| 8 | `river_calvary` | 10 | 57 | 0.825 | 0.469–1.312 | 0.386 |
| 9 | `mallister_houseguard` | 6 | 117 | 0.547 | 0.282–0.726 | 0.068 |
| 10 | `blackwood_houseguard` | 9 | 116 | 0.509 | 0.299–0.759 | 0.138 |

## Ravens' Teeth focus

- Baseline cohort: 9 battles, 404 deployed, 3.153 kills/deployed (95% battle bootstrap 1.833–4.357); casualty rate 0.040.
- Current cohort: 6 battles, 685 deployed, 1.845 kills/deployed (95% battle bootstrap 1.412–2.291); casualty rate 0.162.
- Compatible combined estimate: 15 battles, 1089 deployed, 2.331 kills/deployed (95% battle bootstrap 1.746–3.081); casualty rate 0.117.
- Ravens' Teeth has enough current-batch field evidence to close the 5-battle / 20-deployed display gate (6 battles and 685 deployed).
- Current minus baseline: -1.308 kills/deployed (95% battle bootstrap -2.627–0.129). The interval crosses zero, so no increase or decline is established. This is a descriptive cohort difference, not a causal estimate.
- Focus-cohort battle results: baseline 9 Victory; current 5 Victory, 1 Defeat; combined 14 Victory, 1 Defeat. The cohort contrast is outcome-confounded when these compositions differ.

## Current batch context coverage

| Context | Battles | Visible labels | Deployed | Reliable labels | Insufficient labels |
|---|---:|---:|---:|---:|---:|
| `field` | 6 | 33 | 1246 | 4 | 29 |
| `siege_attack` | 1 | 11 | 175 | 0 | 11 |
| `siege_defense` | 0 | 0 | 0 | 0 | 0 |

- Ravens' Teeth in `siege_attack` remains below the display gate with 1 battle and 117 deployed; no rate from another context is substituted.
- No field and siege observations are pooled; each context must pass its own gate.

## Identity and completeness

- 39 of 58 observed labels have one exact canonical ID in the versioned audit for track `realm_of_thrones`.
- Unresolved canonical labels remain provisional: `northern_colonel`, `northern_hero`, `northern_horseman`, `northern_mounted_warlord`, `northern_ranger`, `northern_sergeant`, `northern_soldier`, `westerlands_banner_knight`, `westerlands_duelist`, `westerlands_footman`, `westerlands_horseman`, `westerlands_infantry`, `westerlands_militia_spearman`, `westerlands_noble_youth`, `westerlands_recruit`, `westerlands_scout`, `westerlands_sharpshooter`, `westerlands_skirmisher`, `westerlands_swordsman`.
- `combined_ranking_complete.csv` retains every observed field label; `combined_ranking_reliable.csv` and `combined_insufficient_evidence.csv` split it without dropping low-sample rows.
- Rows marked for review and non-field battles are rejected from the projection. Where historical validation reports omit explicit side, hero, or off-screen flags, that missing verification is preserved in `compatibility_decision.json`.

## Limitations

- These are observational campaign results, confounded by battle outcome, army composition, enemy composition, map, difficulty, and player choices. Battle-result composition is preserved in `combined_battle_provenance.csv` rather than assumed.
- Row visibility is partial, so total-army contribution, deployment share, and off-screen performance cannot be calculated.
- Raw PNGs for the current batch are not retained; its 11 field-level review decisions remain unresolved in the separate review layer.
- The schema join across 1.1.0, 2.0.0 is deliberately narrow. It does not imply that every field is interchangeable.
- No frozen model was changed or recalibrated.
