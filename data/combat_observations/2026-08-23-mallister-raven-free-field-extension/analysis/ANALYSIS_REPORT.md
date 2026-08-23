# Phase 2 analysis — Mallister Raven-free field extension

## Batch-wide result

Six independent Realm of Thrones 1.4.x field results were verified: **3 victories and 3 defeats**. All 59 visible player-side ordinary-troop occurrences and all 21 distinct labels are represented below.

The isolated extension produces **3 reliable rows** and **18 below-gate rows** under the 5-battle / 20-deployed rule. The tiny-sample rows at the top of the raw kills/deployed ordering remain explicitly insufficient.

The three focus branches account for `1532 / 1827 = 0.838533` (**83.85%**) of verified player-side kills in the extension.

## Reliable extension rows

| Troop | Battles | Deployed | Kills | Kills/deployed | Kill share | Retention |
|---|---:|---:|---:|---:|---:|---:|
| Mallister Elite Archer [T5] | 6 | 401 | 676 | 1.685786 | 37.00% | 49.38% |
| Mallister House Guard [T5] | 6 | 330 | 474 | 1.436364 | 25.94% | 22.73% |
| Mallister Eagle Knight [T6] | 6 | 325 | 382 | 1.175385 | 20.91% | 33.54% |

## Victory/defeat split for the focus branches

| Troop | Result | Battles | Deployed | Kills | Kills/deployed | Retention |
|---|---|---:|---:|---:|---:|---:|
| Mallister Elite Archer [T5] | Victory | 3 | 201 | 272 | 1.353234 | 98.51% |
| Mallister Elite Archer [T5] | Defeat | 3 | 200 | 404 | 2.020000 | 0.00% |
| Mallister House Guard [T5] | Victory | 3 | 150 | 283 | 1.886667 | 50.00% |
| Mallister House Guard [T5] | Defeat | 3 | 180 | 191 | 1.061111 | 0.00% |
| Mallister Eagle Knight [T6] | Victory | 3 | 158 | 267 | 1.689873 | 68.99% |
| Mallister Eagle Knight [T6] | Defeat | 3 | 167 | 115 | 0.688623 | 0.00% |

Elite Archer output rises in the defeats (`404 / 200 = 2.020000`) while retention falls to 0%; this shows high pre-wipe damage, not defensive safety. House Guard and Eagle Knight are much more outcome-sensitive: their victory rates are `1.886667` and `1.689873`, versus `1.061111` and `0.688623` in defeats.

## Defensive context

Final battle pressure margins are `-23.86, -67.01, +58.64, +88.95, -58.60, +70.52` percentage points. Retention and pressure margin remain separate; no blended defensive score or individual causal credit is published.

## Compatible Raven-free join

The four-battle PR #84 cohort and this six-battle extension pass the explicit descriptive-join checks: same game track/version, same field context, same player-party boundary, Raven-free protocol, disjoint battle IDs, and disjoint source-image hashes. Opponent composition and three medium-confidence field classifications remain confounders, so the join is a cohort projection rather than a causal estimate.

| Troop | Battles | Deployed | Kills | Kills/deployed | Retention |
|---|---:|---:|---:|---:|---:|
| Mallister Elite Archer [T5] | 9 | 530 | 978 | 1.845283 | 49.25% |
| Mallister House Guard [T5] | 10 | 563 | 749 | 1.330373 | 30.37% |
| Mallister Eagle Knight [T6] | 10 | 559 | 684 | 1.223614 | 42.93% |

The ten-battle projection closes the Mallister field-isolation test. Elite Archer is the clear offensive leader (`978 / 530 = 1.845283`), followed by House Guard (`749 / 563 = 1.330373`) and Eagle Knight (`684 / 559 = 1.223614`). The Raven-present comparison remains diagnostic only.

## All extension rows

| Rank | Troop | Battles | Deployed | Kills | Kills/deployed | Kill share | Retention | Gate |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Lannister Longbowman [T5] | 3 | 3 | 10 | 3.333333 | 1.03% | 33.33% | insufficient_evidence |
| 2 | Lannister Officer [T5] | 4 | 4 | 12 | 3.000000 | 0.96% | 25.00% | insufficient_evidence |
| 3 | Riverlands Soldier [T3] | 1 | 1 | 3 | 3.000000 | 1.23% | 100.00% | insufficient_evidence |
| 4 | Riverlands Elite Archer [T4] | 2 | 4 | 9 | 2.250000 | 1.56% | 50.00% | insufficient_evidence |
| 5 | Riverlands Man at Arms [T4] | 2 | 2 | 4 | 2.000000 | 0.69% | 50.00% | insufficient_evidence |
| 6 | Mallister Man at Arms [T4] | 3 | 12 | 22 | 1.833333 | 2.19% | 8.33% | insufficient_evidence |
| 7 | Riverlands Archer [T3] | 3 | 7 | 12 | 1.714286 | 1.46% | 57.14% | insufficient_evidence |
| 8 | Mallister Elite Archer [T5] | 6 | 401 | 676 | 1.685786 | 37.00% | 49.38% | reliable |
| 9 | Riverlands Bowman [T2] | 2 | 5 | 8 | 1.600000 | 1.68% | 80.00% | insufficient_evidence |
| 10 | Riverlands Cavalry [T5] | 2 | 2 | 3 | 1.500000 | 0.52% | 50.00% | insufficient_evidence |
| 11 | Mallister Archer [T4] | 3 | 15 | 22 | 1.466667 | 2.19% | 33.33% | insufficient_evidence |
| 12 | Mallister House Guard [T5] | 6 | 330 | 474 | 1.436364 | 25.94% | 22.73% | reliable |
| 13 | Dornish Bowman [T2] | 2 | 4 | 5 | 1.250000 | 0.87% | 50.00% | insufficient_evidence |
| 14 | Mallister Eagle Knight [T6] | 6 | 325 | 382 | 1.175385 | 20.91% | 33.54% | reliable |
| 15 | Braavosi Footman [T2] | 1 | 1 | 1 | 1.000000 | 0.43% | 0.00% | insufficient_evidence |
| 16 | Broken Man [T1] | 1 | 1 | 1 | 1.000000 | 0.41% | 0.00% | insufficient_evidence |
| 17 | Dornish Archer [T3] | 1 | 1 | 1 | 1.000000 | 0.43% | 0.00% | insufficient_evidence |
| 18 | Mallister Knight [T5] | 1 | 2 | 2 | 1.000000 | 0.82% | 100.00% | insufficient_evidence |
| 19 | Mallister Levy [T2] | 3 | 3 | 2 | 0.666667 | 0.20% | 0.00% | insufficient_evidence |
| 20 | Mallister Horseman [T4] | 4 | 26 | 12 | 0.461538 | 0.96% | 15.38% | insufficient_evidence |
| 21 | Mallister Footman [T3] | 3 | 10 | 3 | 0.300000 | 0.31% | 10.00% | insufficient_evidence |

## Limitations

Campaign results remain composition- and opponent-confounded. Two extension fights and one PR #84 fight have medium field-context confidence because a named garrison appears in an open-field scoreboard. Four incidental labels lack a unique exact match in the versioned Realm of Thrones audit and remain unresolved. Frozen model files are unchanged.
