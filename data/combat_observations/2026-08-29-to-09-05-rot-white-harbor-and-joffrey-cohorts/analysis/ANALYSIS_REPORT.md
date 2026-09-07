# Phase 2 analysis — 2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts

## Batch-wide findings

All **355** fully visible player-side ordinary-troop occurrences are represented in **134** cohort/context rows: **19 reliable** and **115 below gate**. White Harbor and Joffrey are separate cohorts, and field/siege contexts are never pooled.

Active last-readable scoreboards remain independent censored observations. The two `retreated_to_keep` siege stages are preserved as phase-complete observations rather than converted into victories/defeats.

### Reliable rows

| Cohort/context | Eff. rank | Impact rank | Troop | Battles | Deployed | Kills/deployed | Kill share | Deploy share | Offense ratio | Retention |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| joffrey / field | 1 | 1 | Ravens' Teeth | 7 | 129 | 6.062016 | 15.55% | 5.41% | 2.874 | 74.42% |
| joffrey / field | 2 | 4 | Westerling Hedgeknight | 5 | 73 | 3.191781 | 5.74% | 4.26% | 1.348 | 45.21% |
| joffrey / field | 3 | 5 | Realm Paladin | 11 | 122 | 2.704918 | 4.89% | 3.56% | 1.372 | 60.66% |
| joffrey / field | 4 | 9 | Frey Assassin | 7 | 43 | 2.674419 | 2.29% | 1.80% | 1.268 | 81.40% |
| joffrey / field | 5 | 8 | Realm Knight | 7 | 62 | 2.145161 | 3.92% | 3.08% | 1.271 | 41.94% |
| joffrey / field | 6 | 2 | Captain of the Kingsguard | 14 | 506 | 2.126482 | 14.83% | 12.08% | 1.228 | 67.19% |
| joffrey / field | 7 | 3 | Kingsguard | 13 | 585 | 1.743590 | 16.58% | 15.69% | 1.057 | 59.83% |
| joffrey / field | 8 | 7 | Gold Cloak Halberdier | 9 | 140 | 1.578571 | 6.01% | 5.46% | 1.101 | 36.43% |
| joffrey / field | 9 | 6 | Gold Cloak Sniper | 9 | 321 | 1.140187 | 9.54% | 12.34% | 0.773 | 70.72% |
| joffrey / field | 10 | 10 | Kingsguard Initiate | 8 | 107 | 0.971963 | 4.61% | 5.00% | 0.922 | 42.06% |
| joffrey / field | 11 | 12 | Gold Cloak Captain | 10 | 93 | 0.892473 | 1.77% | 3.19% | 0.555 | 55.91% |
| joffrey / field | 12 | 11 | Kingsguard's Squire | 7 | 154 | 0.597403 | 5.61% | 8.48% | 0.661 | 29.22% |
| white_harbor / field | 1 | 3 | Mormont Bowmaiden | 7 | 62 | 1.629032 | 7.05% | 4.05% | 1.739 | 79.03% |
| white_harbor / field | 2 | 6 | Umber Marksman | 5 | 20 | 1.250000 | 2.72% | 2.10% | 1.298 | 90.00% |
| white_harbor / field | 3 | 7 | Westerlands Banner Knight | 6 | 27 | 1.148148 | 2.82% | 2.27% | 1.243 | 62.96% |
| white_harbor / field | 4 | 4 | Manderly Veteran Archer | 8 | 95 | 1.105263 | 6.66% | 5.63% | 1.182 | 82.11% |
| white_harbor / field | 5 | 1 | White Harbor Knight Commander | 8 | 289 | 0.986159 | 18.07% | 17.14% | 1.054 | 78.20% |
| white_harbor / field | 6 | 5 | Glover Veteran Archer | 6 | 54 | 0.944444 | 4.64% | 4.54% | 1.023 | 87.04% |
| white_harbor / field | 7 | 2 | Bolton Hunter | 8 | 243 | 0.872428 | 13.44% | 14.41% | 0.933 | 79.01% |

### Below-gate partition

Every below-gate row is retained without promotion. See `insufficient_evidence.csv` for exact gaps.

## Focus conclusions

- **White Harbor Knight Commander — white_harbor / field**: `285 / 289 = 0.986159` kills/deployed; kill share **18.07%**, deployment share **17.14%**, offense ratio **1.054×**, retention **78.2%**; gate `reliable` (8 battles).
- **Westerling Hedgeknight — joffrey / field**: `233 / 73 = 3.191781` kills/deployed; kill share **5.74%**, deployment share **4.26%**, offense ratio **1.348×**, retention **45.2%**; gate `reliable` (5 battles).
- **Westerling Hedgeknight — joffrey / siege_attack**: `20 / 7 = 2.857143` kills/deployed; kill share **3.76%**, deployment share **—**, offense ratio **—**, retention **42.9%**; gate `insufficient_evidence` (1 battles).

### Interpretation

**White Harbor Knight Commander is high-evidence but proportional.** Its field sample clears the gate comfortably, but its share of kills is close to its share of deployed troops; it is useful, not a Raven/Sarnori-style disproportional outlier.

**Westerling Hedgeknight is the more interesting next isolated target.** The mixed Joffrey field sample already clears the minimum gate and shows much higher per-unit output and a >1 offensive contribution ratio, but retention is low enough that composition/opponent confounding matters. Isolation is the smallest test that can tell whether the signal is intrinsic.

## Defensive context and result splits

`result_splits.csv` keeps victory, defeat, phase-complete retreat, and active/censored observations separate. `battle_pressure_margin.csv` is battle-level only; it is never assigned to an individual troop.

## Identity and review limits

The committed ROT audit confirms **80 of 95** observed labels by one exact name-to-ID match. Unresolved labels remain provisional.

The three clipped/obscured Phase 1 rows remain excluded from primary rankings and unresolved in the review layer because no raw screenshot was available to this distinct Phase 2 run. No numeric value was inferred.

## Smallest next test

**Isolate Westerling Hedgeknight in field battles.** Run at least **5 independent field battles** with a stable supporting roster/orders and enough Westerling Hedgeknights to keep total deployment ≥20. Do not mix siege observations into this test. The purpose is no longer to close the minimum gate; it is to test whether the mixed-army 3.19 kills/deployed signal survives isolation.

## Limitations

Campaign observations remain opponent-, roster-, map-, result-, and player-order-confounded. Active observations are right-censored. No off-screen row is inferred, no cohort/context boundary is crossed, and no frozen model is changed.
