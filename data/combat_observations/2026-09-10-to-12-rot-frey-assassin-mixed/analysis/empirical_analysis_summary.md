# Phase 2 analysis — 2026-09-10-to-12-rot-frey-assassin-mixed

## Batch-wide findings

All **61** visible player-side ordinary-troop occurrences form **27** troop/context rows: **6 reliable** and **21 below the 5-battle / 20-deployed gate**. Field and siege attack remain separate, and the active last observation is an independent right-censored battle.

### Reliable rows

Only rows that pass the 5-battle / 20-deployed display gate publish rates and ranks.

| Context | Eff. rank | Impact rank | Troop | Canonical ID | Battles | Deployed | Kills | Kills/deployed | Kill share | Deploy share | Ratio | Retention | Grade |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| field | 1 | 1 | Frey Assassin [T6] | frey_assassin | 6 | 534 | 1549 | 2.900749 | 59.10% | 44.80% | 1.319227 | 54.49% | high |
| field | 2 | 2 | Celtigar Banneret [T6] | celtigar_banneret | 6 | 225 | 397 | 1.764444 | 15.15% | 18.88% | 0.802449 | 44.89% | high |
| field | 3 | 3 | Velaryon Sea Guard [T6] | velaryon_sea_guard | 6 | 186 | 300 | 1.612903 | 11.45% | 15.60% | 0.733529 | 33.33% | high |
| field | 4 | 5 | Mountain's Man [T6] | mountains_man | 5 | 24 | 35 | 1.458333 | 1.62% | 2.41% | 0.672506 | 29.17% | low |
| field | 5 | 4 | Queen's Man [T6] | dragonstone_steel_curtain | 6 | 116 | 151 | 1.301724 | 5.76% | 9.73% | 0.592009 | 40.52% | high |
| field | 6 | 6 | Baratheon Hammerknight [T6] | baratheon_pikeknight | 6 | 33 | 40 | 1.212121 | 1.53% | 2.77% | 0.551258 | 39.39% | medium |

### Insufficient-evidence rows

Every below-gate row is retained with identifiers, sample size, and remaining gate gaps.

| Context | Troop | Canonical ID | Battles | Deployed | More battles needed | More deployed needed |
|---|---|---|---:|---:|---:|---:|
| field | Blackwood Archer [T4] | blackwood_archer | 1 | 2 | 4 | 18 |
| field | Blackwood Longbowman [T5] | blackwood_longbowman | 1 | 4 | 4 | 16 |
| field | Gold Cloak Halberdier [T5] | kingsguard | 1 | 2 | 4 | 18 |
| field | Riverlands Admiral [T6] | river_admiral | 4 | 27 | 1 | 0 |
| field | Velaryon Marine [T4] | velaryon_warrior | 1 | 2 | 4 | 18 |
| field | Clegane Man at Arms [T4] | clegane_man_at_arms | 2 | 2 | 3 | 18 |
| field | Bracken House Guard [T5] | bracken_houseguard | 1 | 2 | 4 | 18 |
| field | Velaryon Renegade [T5] | velaryon_renegade | 2 | 2 | 3 | 18 |
| field | Clegane Levy [T2] | clegane_levy | 1 | 1 | 4 | 19 |
| field | Gold Cloak Petty Officer [T4] | goldcloak_officer | 1 | 1 | 4 | 19 |
| siege_attack | Velaryon Sea Guard [T6] | velaryon_sea_guard | 1 | 5 | 4 | 15 |
| siege_attack | Frey Assassin [T6] | frey_assassin | 1 | 96 | 4 | 0 |
| siege_attack | Celtigar Banneret [T6] | celtigar_banneret | 1 | 29 | 4 | 0 |
| siege_attack | Dragonstone Knight [T4] | dragonstone_knight | 1 | 7 | 4 | 13 |
| siege_attack | Velaryon Renegade [T5] | velaryon_renegade | 1 | 4 | 4 | 16 |
| siege_attack | Celtigar Man at Arms [T4] | celtigar_man_at_arms | 1 | 5 | 4 | 15 |
| siege_attack | Celtigar Halberdier [T5] | celtigar_halberdier | 1 | 7 | 4 | 13 |
| siege_attack | Velaryon Marine [T4] | velaryon_warrior | 1 | 7 | 4 | 13 |
| siege_attack | Squire [T3] | dragonstone_squire | 1 | 5 | 4 | 15 |
| siege_attack | Dragonstone Shock Knight [T5] | dragonstone_shock_knight | 1 | 6 | 4 | 14 |
| siege_attack | Baratheon Hammerknight [T6] | baratheon_pikeknight | 1 | 5 | 4 | 15 |

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
