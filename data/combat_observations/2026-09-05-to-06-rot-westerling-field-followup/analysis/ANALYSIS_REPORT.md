# Phase 2 analysis — 2026-09-05-to-06-rot-westerling-field-followup

## Result

**Westerling Hedgeknight SURVIVES share/deployment adjustment in the isolated Westerling follow-up.** The current sample is **16 independent field battles / 437 deployed / 808 kills = 1.849 kills/deployed**. Its kill share is **30.78%** versus **19.54%** deployment share, for an offensive contribution ratio of **1.575×**. Retention is **62.7%**. Evidence gate: `reliable`.

The earlier mixed Joffrey field evidence was **5 battles / 73 deployed / 233 kills = 3.192 kills/deployed**, with **5.74% kill share vs 4.26% deployment share = 1.348× contribution ratio** and 45.2% retention. The two campaign cohorts are reported side by side but are **not pooled**; differences are descriptive, not causal.

Current Joffrey bridge evidence is kept separate: **4 battles / 98 deployed / 2.367 kills/deployed / gate insufficient_evidence**.

## Batch-wide coverage

The Phase 2 partition contains **57 troop/cohort rows**: **10 reliable** and **47 insufficient-evidence** under the 5-independent-battle / 20-deployed gate. All 217 fully visible player-side ordinary-troop occurrences are represented. Field context and player/enemy boundaries remain intact.

## Interpretation

Relative to the prior 3.192 kills/deployed mixed sample, the isolated follow-up changes by **-1.343 kills/deployed** (0.579× the prior rate). Because opponent mix, battle size, map and supporting roster differ, this is not treated as a controlled effect estimate.

The decisive test is share adjustment: a unit that simply occupies more of the army should take a similar share of kills. Here the current Hedgeknight kill share is compared directly with its deployment share; the ratio above 1.0 indicates disproportionate offensive contribution in this cohort.

## Review and identities

The six clipped/obscured Phase 1 rows remain unresolved and excluded from primary rankings. No missing number was inferred. Canonical identity decisions are additive in `review/phase2_identity_decisions.csv`; Phase 1 files are unchanged.

## Defensive/role boundary

`battle_pressure_margin.csv` remains a battle-level diagnostic and is not assigned to an individual troop. `role_adjusted_view.csv` groups reliable rows by canonical role but deliberately publishes no blended offense/defense score, matching current repository methodology.

## Next test

Test **Cerwyn Marauder** next in the Westerling field cohort.

Current coverage: **5 battles / 19 deployed**, at **1.737 kills/deployed**. The smallest gate-closing addition is **0 more independent battle(s)** and at least **1 additional deployed** overall. Keep support roster/orders stable and do not pool Joffrey bridge battles.

## Limits

Campaign observations remain confounded by opponent, roster, map, battle size and player orders. No off-screen row is inferred; Joffrey bridge battles are not pooled with Gawen Westerling battles; no frozen theoretical model is changed.
