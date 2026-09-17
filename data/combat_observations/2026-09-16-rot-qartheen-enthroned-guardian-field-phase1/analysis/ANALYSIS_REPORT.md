# Phase 2 analysis — Sep 16 Qartheen Guardian follow-up

## Batch-wide findings

All **13 visible player-side ordinary occurrences** are covered across **12 troop/context rows**. None reaches the 5-independent-battle gate, so **0 rows are reliable** and **12 remain explicit insufficient evidence**. All **18 character rows** are retained separately and excluded from ordinary-troop metrics.

Player-side, field, Realm of Thrones, and Egon Emeros' Party boundaries remain separate. Every contributing battle has direct positive player-side kill and deployment totals, so shares are published without reconstructing off-screen troop rows.

Because every screenshot is a completed final result with direct side totals, battle-level pressure margins are published separately: **1.000000** against Forim's Party and **0.911765** against the Deserters. No tested frontline is predeclared in this mixed campaign evidence, so those side-level margins are not attributed to the Guardian or any other troop.

| troop | identity | battles | deployed | kills | kills/deployed | kill share | deployment share | contribution ratio | status |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Braavosi Soldier [T3] | unresolved_provisional_label | 1 | 1 | 1 | 1.000000 | 0.015625 | 0.005882 | 2.656250 | insufficient_battles_and_deployed |
| Broken Guard [T1] | confirmed_id | 1 | 1 | 1 | 1.000000 | 0.015625 | 0.005882 | 2.656250 | insufficient_battles_and_deployed |
| Qartheen Pureborn Champion [T5] | confirmed_id | 1 | 4 | 4 | 1.000000 | 0.041667 | 0.033058 | 1.260417 | insufficient_battles_and_deployed |
| Qartheen Enthroned Guardian [T6] | confirmed_id | 2 | 173 | 138 | 0.797688 | 0.862500 | 0.594502 | 1.450795 | insufficient_battles |
| Lengii Mounted Slayer [T4] | unresolved_provisional_label | 1 | 12 | 4 | 0.333333 | 0.062500 | 0.070588 | 0.885417 | insufficient_battles_and_deployed |
| Lengii Slaver [T3] | confirmed_id | 1 | 28 | 3 | 0.107143 | 0.046875 | 0.164706 | 0.284598 | insufficient_battles |
| Braavosi Footman [T2] | unresolved_provisional_label | 1 | 10 | 1 | 0.100000 | 0.015625 | 0.058824 | 0.265625 | insufficient_battles_and_deployed |
| Lengii Criminal [T2] | confirmed_id | 1 | 18 | 1 | 0.055556 | 0.010417 | 0.148760 | 0.070023 | insufficient_battles_and_deployed |
| Dornish Archer [T3] | unresolved_provisional_label | 1 | 1 | 0 | 0.000000 | 0.000000 | 0.005882 | 0.000000 | insufficient_battles_and_deployed |
| Qartheen Pureborn Fighter [T3] | confirmed_id | 1 | 1 | 0 | 0.000000 | 0.000000 | 0.005882 | 0.000000 | insufficient_battles_and_deployed |
| Qartheen Pureborn Warrior [T4] | confirmed_id | 1 | 1 | 0 | 0.000000 | 0.000000 | 0.005882 | 0.000000 | insufficient_battles_and_deployed |
| [unreadable ordinary label] | unresolved_label | 1 | 1 | 0 | 0.000000 | 0.000000 | 0.005882 | 0.000000 | insufficient_battles_and_deployed |

## Qartheen Enthroned Guardian focus

The requested focus is additive to the batch-wide table above. The three views below are deliberately separate.

| view | battles | deployed | survivors | kills | deaths | wounded | kills/deployed | kill share | deployment share | contribution ratio | retention | gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| historical_mixed_campaign | 5 | 195 | 164 | 698 | 7 | 24 | 3.579487 | 0.229003 | 0.099490 | 2.301770 | 0.841026 | pass |
| new_follow_up | 2 | 173 | 173 | 138 | 0 | 0 | 0.797688 | 0.862500 | 0.594502 | 1.450795 | 1.000000 | below gate |
| combined_descriptive_continuity | 7 | 368 | 337 | 836 | 7 | 24 | 2.271739 | 0.260599 | 0.163483 | 1.594041 | 0.915761 | pass |

The two-battle follow-up records **173 deployed / 138 kills = 0.797688 kills per deployed**. Its **86.25% kill share** remains above its **59.45% deployment share** (1.451x contribution ratio), with **100% retention**. The lower raw kills/deployed value is constrained by only 160 total enemy kills being available across these two small battles; it is not evidence of a causal performance collapse.

The compatibility audit permits the seven-battle combined row only as descriptive continuity: both inputs are Realm of Thrones field battles for Egon Emeros' Party, use the same confirmed Guardian identity, contain completed results, and have distinct battle IDs and source hashes. Exact game build remains unknown, and campaign opponent, map, roster, orders, difficulty, and enemy availability are uncontrolled.

PR #100's separate nine-field-battle dedicated cohort is not pooled into this continuity view. It already closed dedicated Guardian field testing after both the full cohort and its leave-one-highest-rate-battle sensitivity cleared the gate with kill share above deployment share. These two later distinct battles are directionally confirmatory on share and retention but remain below the battle gate, so they do not reopen or otherwise change that decision.

## Identity, queue, and limitations

Seven of the 12 ordinary labels resolve by one exact match in the versioned Realm of Thrones audit. `Lengii Mounted Slayer`, `Braavosi Soldier`, and `Braavosi Footman` remain provisional unmatched labels; `Dornish Archer [T3]` remains provisional because its prefix is occluded; the unreadable Deserters row remains unresolved and unpooled. No aliases or off-screen values are inferred.

The authoritative queue remains unchanged: `active_test` is null, `ordered_queue` is empty, Qartheen Enthroned Guardian is closed by PR #100, and Arryn Winged Knight remains on verification hold. No future target is authorized.

Raw PNG bytes are not retained in Git. Phase 2 verifies the exact Base64 Git blob, decoded archive, both checksum manifests, every member, repository mirrors, source links, and the two raw-source hashes preserved in the source manifest; later pixel-level rereview still requires the original uploads. Game version, command mode, and boost status remain unknown. `analysis/model_versions/` is unchanged, and no theoretical model recalibration is performed.
