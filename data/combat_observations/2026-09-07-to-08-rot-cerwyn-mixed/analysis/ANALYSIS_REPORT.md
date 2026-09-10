# Phase 2 analysis — 2026-09-07-to-08-rot-cerwyn-mixed

## Result

**Cerwyn Marauder closes as a proven positive field signal, with no additional dedicated test required.**

The exact Gawen Westerling cohort is **5 battles / 22 deployed / 57 kills = 2.591 kills/deployed**. It produced **5.14%** of player-side kills from **2.75%** of deployments, a **1.868×** contribution ratio. Retention was **54.5%**.

The exact Medger Cerwyn cohort is **11 battles / 494 deployed / 744 kills = 1.506 kills/deployed**. It produced **43.74%** of kills from **29.98%** of deployments, a **1.459×** contribution ratio. Retention was **83.0%**.

## Batch-wide coverage

Phase 2 independently reproduces **89 exact participant/context troop rows** from **278 canonical ordinary-troop occurrences** across **23 independent battles**. The evidence partition is **17 reliable** and **72 insufficient-evidence** under the 5-battle / 20-deployed gate.

Field and siege observations remain separate. Gawen Westerling, Medger Cerwyn, Walder Frey and Jonos Bracken are separate participant scopes. The single `retreated_to_keep` siege observation is retained only in its siege cohort.

## Outlier and sensitivity result

Medger's `battle_cm15` has **288 kills / 62 deployed = 4.645 kills/deployed** and is flagged by both IQR and robust-MAD diagnostics. Deleting it yields **456 / 432 = 1.056 kills/deployed** and a **1.217×** contribution ratio, so the share-adjusted positive signal survives. The full efficiency estimate is nevertheless sensitive to this battle and should not be interpreted as a controlled unit coefficient.

## Review and identity boundaries

Eight clipped rows were retained at medium confidence after explicit review; one unreadable bottom row remains excluded. Cerwyn Marauder is the only canonical troop ID asserted by this batch. Other exact labels remain eligible for within-batch empirical aggregation without inventing registry IDs or roles.

## Model and role boundaries

No verified frozen theoretical model snapshot was supplied, so model residuals are explicitly `not_run`. Role-adjusted rankings are not published because this batch does not assert a verified role registry. Efficiency and share-adjusted impact remain separate empirical outputs.

## Queue decision

The batch closes `cerwyn_marauder` / field. The authoritative ordered queue remains empty. Realm Paladin and Arryn Winged Knight remain verification holds; the batch does not manufacture a next target.

## Limits

Campaign observations remain confounded by opponent composition, map, battle size, supporting roster and player orders. Cross-participant values are descriptive only and are never used as a primary pooled estimator.
