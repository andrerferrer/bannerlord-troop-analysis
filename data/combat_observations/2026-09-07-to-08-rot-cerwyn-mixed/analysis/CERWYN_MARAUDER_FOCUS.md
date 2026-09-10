# Cerwyn Marauder focus

## Decision

**STOP dedicated Cerwyn Marauder testing.** Both exact field participant cohorts clear the repository evidence gate, and both keep kill share above deployment share. The large Medger Cerwyn cohort remains positive after removing its single highest-rate battle.

## Exact participant cohorts

### Gawen Westerling's Party

- Battles: **5**
- Deployed: **22**
- Kills: **57**
- Efficiency: **2.591 kills/deployed** (bootstrap 95% interval **1.364–3.833**)
- Kill share: **5.14%**
- Deployment share: **2.75%**
- Offensive contribution ratio: **1.868×**
- Retention: **54.5%**
- Reliable-cohort rank: **#1 efficiency / #3 share-adjusted impact**

### Medger Cerwyn's Party

- Battles: **11**
- Deployed: **494**
- Kills: **744**
- Efficiency: **1.506 kills/deployed** (bootstrap 95% interval **0.814–2.475**)
- Kill share: **43.74%**
- Deployment share: **29.98%**
- Offensive contribution ratio: **1.459×**
- Retention: **83.0%**
- Reliable-cohort rank: **#1 efficiency / #1 share-adjusted impact**

## Robustness

`battle_cm15` is the clear high outlier in the Medger cohort: **288 / 62 = 4.645 kills/deployed**. Removing it leaves **10 battles / 432 deployed / 456 kills = 1.056 kills/deployed**. The adjusted kill share remains above deployment share: **35.46% vs 29.13%**, or **1.217×** offensive contribution. Therefore the positive share-adjusted signal does not depend on that battle, although the full efficiency estimate is materially elevated by it.

The smaller Gawen cohort is exactly at the gate. Removing its highest-rate defeat (`battle_cm05`) leaves **4 battles / 17 deployed**, so that sensitivity row falls below the evidence gate and is diagnostic only.

## Interpretation boundary

The two participant cohorts are never pooled for primary rankings. The combined 16-battle summary is descriptive only. Opponent mix, map, supporting roster, battle size and orders remain uncontrolled campaign confounders; no outlier receives a causal explanation.
