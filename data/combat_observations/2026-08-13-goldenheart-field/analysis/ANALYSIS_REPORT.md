# Phase 2 analysis — combat_2026-08-13_goldenheart_field

## Result

The two new Realm of Thrones field battles are valid player-side observations, but the current cohort does not clear the 5-independent-battle gate. It therefore produces no standalone reliable ranking or tier conclusion. `ranking_complete.csv` retains all 20 observed ordinary-troop labels, `ranking_reliable.csv` is correctly header-only, and `insufficient_evidence.csv` retains all 20 below-gate rows.

Goldenheart Warrior is independently resolved to canonical `summer_master_longbowman` by one exact normalized name-to-ID match repeated across four versioned Realm of Thrones audit tables. The two new battles record 92 kills from 29 deployed:

```text
current kills/deployed = 92 / 29 = 3.172414
```

Battle-level diagnostics are 36 / 7 = 5.142857 and 56 / 22 = 2.545455 kills/deployed. Those rates are published for inspection, not displayed as a reliable current-cohort estimate.

## Frozen-baseline extension

The frozen clean player-party Goldenheart control preserves 9 battle IDs, 428 kills, and 161 present/deployed. Its direct rate is:

```text
baseline kills/deployed = 428 / 161 = 2.658385
current minus baseline = 3.172414 - 2.658385 = +0.514029
combined kills/deployed = (428 + 92) / (161 + 29) = 520 / 190 = 2.736842
combined minus baseline = 2.736842 - 2.658385 = +0.078457
```

The extension is compatible only for this identity-anchored direct rate. The frozen aggregate does not preserve a field-versus-siege subtype or per-battle Goldenheart numerator/denominator rows. Consequently, the combined value is diagnostic, is not promoted to a field-only reliable ranking, and has no reconstructed battle-bootstrap interval. It modestly raises the historical aggregate and is consistent with the prior strong Goldenheart signal, but it does not prove an improvement, causal advantage, or universal tier.

## Current field coverage

| Troop | Canonical ID | Battles | Deployed | Kills/deployed | Status |
|---|---|---:|---:|---:|---|
| Goldenheart Warrior | `summer_master_longbowman` | 2 | 29 | 3.172414 | insufficient evidence |
| Summer Isles Spearmaster | `summer_pikeman` | 2 | 16 | 1.125000 | insufficient evidence |
| Summer Isles Longbowman | `summer_longbowman` | 2 | 25 | 0.960000 | insufficient evidence |
| Summer Isles Archer | `summer_veteran_bowman` | 2 | 58 | 0.724138 | insufficient evidence |
| Summer Isles Footman | `summer_footman` | 2 | 36 | 0.500000 | insufficient evidence |
| Summer Isles Bowman | `summer_bowman` | 2 | 71 | 0.309859 | insufficient evidence |

Summer Isles Horseman and Scout appear in only one battle each. No current troop reaches five independent field battles, regardless of deployed count.

## Identity and review

- 15 of 20 display labels have one conservative exact canonical ID; 5 labels remain provisional rather than guessed.
- All five white-icon queue items were resolved in the additive review layer as `icon_present_non_numeric`; no numeric `upgrade_ready` count was invented.
- All queued rows are heroes and remain outside ordinary-troop rankings.

## Boundaries and limitations

- Player and enemy rows are separate; only player-side ordinary troops enter rankings.
- Field and other battle contexts are not pooled.
- Both current scoreboards expose partial troop rows, so contribution index, whole-army share, and off-screen performance are not computed.
- The historical direct-rate extension is not a substitute for a context-strict combined field sample.
- Army composition, opponents, map, difficulty, and player choices remain observational confounders.
- `analysis/model_versions/` is unchanged.
