# Phase 2 analysis — 2026-09-10-to-12-rot-frey-assassin-mixed

## Batch-wide findings

All **61** visible player-side ordinary-troop occurrences form **27** troop/context rows: **6 reliable** and **21 below the 5-battle / 20-deployed gate**. Field and siege attack remain separate, and the active last observation is an independent right-censored battle.

### Exact reliable/insufficient partition

| Partition | Context | Eff. rank | Impact rank | Troop | Battles | Deployed | Kills | Kills/deployed | Kill share | Deploy share | Ratio | Retention | Grade |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| reliable | field | 1 | 1 | Frey Assassin [T6] | 6 | 534 | 1549 | 2.900749 | 59.10% | 44.80% | 1.319227 | 54.49% | high |
| insufficient_evidence | field | 2 | 7 | Blackwood Archer [T4] | 1 | 2 | 5 | 2.500000 | 0.99% | 1.04% | 0.953557 | 50.00% | exploratory |
| insufficient_evidence | field | 3 | 5 | Blackwood Longbowman [T5] | 1 | 4 | 8 | 2.000000 | 1.58% | 2.07% | 0.762846 | 50.00% | exploratory |
| insufficient_evidence | field | 4 | 10 | Gold Cloak Halberdier [T5] | 1 | 2 | 4 | 2.000000 | 0.87% | 1.03% | 0.849673 | 100.00% | exploratory |
| reliable | field | 5 | 2 | Celtigar Banneret [T6] | 6 | 225 | 397 | 1.764444 | 15.15% | 18.88% | 0.802449 | 44.89% | high |
| reliable | field | 6 | 3 | Velaryon Sea Guard [T6] | 6 | 186 | 300 | 1.612903 | 11.45% | 15.60% | 0.733529 | 33.33% | high |
| reliable | field | 7 | 8 | Mountain's Man [T6] | 5 | 24 | 35 | 1.458333 | 1.62% | 2.41% | 0.672506 | 29.17% | low |
| reliable | field | 8 | 4 | Queen's Man [T6] | 6 | 116 | 151 | 1.301724 | 5.76% | 9.73% | 0.592009 | 40.52% | high |
| insufficient_evidence | field | 9 | 6 | Riverlands Admiral [T6] | 4 | 27 | 34 | 1.259259 | 2.05% | 3.36% | 0.611379 | 29.63% | low |
| reliable | field | 10 | 9 | Baratheon Hammerknight [T6] | 6 | 33 | 40 | 1.212121 | 1.53% | 2.77% | 0.551258 | 39.39% | medium |
| insufficient_evidence | field | 11 | 11 | Velaryon Marine [T4] | 1 | 2 | 2 | 1.000000 | 0.44% | 1.03% | 0.424837 | 100.00% | exploratory |
| insufficient_evidence | field | 12 | 12 | Clegane Man at Arms [T4] | 2 | 2 | 1 | 0.500000 | 0.10% | 0.49% | 0.205466 | 50.00% | exploratory |
| insufficient_evidence | field | 13 | 13 | Bracken House Guard [T5] | 1 | 2 | 0 | 0.000000 | 0.00% | 1.04% | 0.000000 | 0.00% | exploratory |
| insufficient_evidence | field | 14 | 14 | Velaryon Renegade [T5] | 2 | 2 | 0 | 0.000000 | 0.00% | 0.52% | 0.000000 | 50.00% | exploratory |
| insufficient_evidence | field | 15 | 15 | Clegane Levy [T2] | 1 | 1 | 0 | 0.000000 | 0.00% | 0.50% | 0.000000 | 0.00% | exploratory |
| insufficient_evidence | field | 16 | 16 | Gold Cloak Petty Officer [T4] | 1 | 1 | 0 | 0.000000 | 0.00% | 0.51% | 0.000000 | 0.00% | exploratory |
| insufficient_evidence | siege_attack | 1 | 3 | Velaryon Sea Guard [T6] | 1 | 5 | 30 | 6.000000 | 5.23% | 2.51% | 2.080139 | 100.00% | exploratory |
| insufficient_evidence | siege_attack | 2 | 1 | Frey Assassin [T6] | 1 | 96 | 370 | 3.854167 | 64.46% | 48.24% | 1.336201 | 78.12% | exploratory |
| insufficient_evidence | siege_attack | 3 | 2 | Celtigar Banneret [T6] | 1 | 29 | 76 | 2.620690 | 13.24% | 14.57% | 0.908567 | 62.07% | exploratory |
| insufficient_evidence | siege_attack | 4 | 4 | Dragonstone Knight [T4] | 1 | 7 | 14 | 2.000000 | 2.44% | 3.52% | 0.693380 | 71.43% | exploratory |
| insufficient_evidence | siege_attack | 5 | 6 | Velaryon Renegade [T5] | 1 | 4 | 8 | 2.000000 | 1.39% | 2.01% | 0.693380 | 50.00% | exploratory |
| insufficient_evidence | siege_attack | 6 | 5 | Celtigar Man at Arms [T4] | 1 | 5 | 9 | 1.800000 | 1.57% | 2.51% | 0.624042 | 80.00% | exploratory |
| insufficient_evidence | siege_attack | 7 | 7 | Celtigar Halberdier [T5] | 1 | 7 | 9 | 1.285714 | 1.57% | 3.52% | 0.445744 | 57.14% | exploratory |
| insufficient_evidence | siege_attack | 8 | 8 | Velaryon Marine [T4] | 1 | 7 | 9 | 1.285714 | 1.57% | 3.52% | 0.445744 | 71.43% | exploratory |
| insufficient_evidence | siege_attack | 9 | 9 | Squire [T3] | 1 | 5 | 5 | 1.000000 | 0.87% | 2.51% | 0.346690 | 20.00% | exploratory |
| insufficient_evidence | siege_attack | 10 | 10 | Dragonstone Shock Knight [T5] | 1 | 6 | 5 | 0.833333 | 0.87% | 3.02% | 0.288908 | 50.00% | exploratory |
| insufficient_evidence | siege_attack | 11 | 11 | Baratheon Hammerknight [T6] | 1 | 5 | 4 | 0.800000 | 0.70% | 2.51% | 0.277352 | 40.00% | exploratory |

## Additive Frey Assassin deep dive

The dedicated field cohort records **6 battles / 534 deployed / 1549 kills = 2.900749 kills/deployed**. It supplied **59.10%** of player-side kills from **44.80%** of deployments (**1.319x**, gap **14.30%**), with **54.49%** retention.

The final-results-only sensitivity still passes the gate at **5 battles / 446 deployed / 1203 kills = 2.697309**, with a **1.274x** contribution ratio. The active battle therefore does not create the stop decision.

The already-merged incidental PR #96 cohort was **6 battles / 292 deployed / 444 kills = 1.520548**, with **98.97%** retention. These cohorts are compared descriptively but never pooled: campaign date, roster, opponents, and difficulty state are not controlled as one experiment.

**Decision: stop dedicated Frey Assassin field testing.** The dedicated cohort and its final-only sensitivity both clear the display gate and retain kill share above deployment share. No future target is approved; the Arryn Winged Knight historical hold remains authoritative.

## Defensive context and boundaries

Five final field battles and the final siege attack publish production pressure margins. One active field scoreboard remains diagnostic only. Pressure margin stays battle-level and is not assigned to Frey Assassin or another troop.

## Identity, model, and evidence limits

The pinned Realm of Thrones audit confirms **21 of 21** labels by one exact tier-stripped name-to-ID match. No normalized value required correction.

No complete compatible Realm of Thrones v7.1/v7.3 model universe is committed here, so model comparison and residual outputs explicitly record `not_run`; frozen models are unchanged. Role populations do not reach five reliable rows inside one role/context, so no role-adjusted rank is published.

## Limitations

Raw PNGs are not retained after verified normalization. The Phase 1 source-hash prose says sorted lines, while the committed hash reproduces only in numeric `source_order`; Phase 2 records that wording ambiguity without changing provenance. Repository-wide historical exact-hash search previously returned HTTP 502, so historical duplicate risk remains low rather than zero. Campaign results remain confounded by opponent, map, roster, orders, and unrecorded difficulty. No off-screen row is inferred and no context, participant, or result-state boundary is crossed.
