# Phase 2 analysis — Sep 12–14 Realm of Thrones mixed campaign

## Merge blocker

The safe analytical work is complete, but the pull request cannot pass its merge gate: Phase 1 declared `screenshots_manifest.csv` as an immutable input and did not publish that file in the normalized archive or repository. The reviewed reconstruction is explicitly non-authoritative and does not replace the missing Phase 1 artifact.

## Batch-wide findings

The batch contains **15 independent battle events** (8 field, 7 siege attack), with **155 visible ordinary-troop rows** and **77 excluded character rows**. All ordinary occurrences map to exactly one of **7 reliable** or **88 below-gate** troop/party/context/result-state rows.

7 rows pass the 5-battle / 20-deployed gate; 1 row retains a provisional display label because the pinned track audit has no exact match. These are descriptive campaign measurements, not controlled causal comparisons.

### Reliable field rows

| Efficiency rank | Troop | Identity | Party | Observation state | Battles | Deployed | Kills | Kills/deployed | Kill share | Deployment share | Contribution ratio | Retention |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Qartheen Enthroned Guardian [T6] | confirmed_id | Egon Emeros' Party | completed | 5 | 195 | 698 | 3.579487 | 0.229003 | 0.099490 | 2.301770 | 0.841026 |
| 2 | Qartheen Longbowman [T5] | confirmed_id | Egon Emeros' Party | completed | 5 | 301 | 654 | 2.172757 | 0.214567 | 0.153571 | 1.397180 | 0.920266 |
| 3 | Unsullied [T6] | confirmed_id | Egon Emeros' Party | completed | 5 | 440 | 683 | 1.552273 | 0.224081 | 0.224490 | 0.998181 | 0.672727 |

### Reliable siege attack rows

| Efficiency rank | Troop | Identity | Party | Observation state | Battles | Deployed | Kills | Kills/deployed | Kill share | Deployment share | Contribution ratio | Retention |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Qartheen Enthroned Guardian [T6] | confirmed_id | Egon Emeros' Party | completed | 6 | 212 | 567 | 2.674528 | 0.250221 | 0.077970 | 3.209198 | 0.990566 |
| 2 | Qartheen Longbowman [T5] | confirmed_id | Egon Emeros' Party | completed | 6 | 322 | 365 | 1.133540 | 0.161077 | 0.118426 | 1.360148 | 0.965839 |
| 3 | Dothraki Khal's Guard [T6] | unresolved_provisional_label | Egon Emeros' Party | completed | 5 | 190 | 172 | 0.905263 | 0.106304 | 0.088951 | 1.195082 | 0.994737 |
| 4 | Unsullied [T6] | confirmed_id | Egon Emeros' Party | completed | 6 | 517 | 372 | 0.719536 | 0.164166 | 0.190143 | 0.863379 | 0.943907 |

## Identity boundary

Dothraki Khal's Guard [T6] / siege attack / completed clear the numeric display gate and are published as reliable within-batch evidence under provisional labels. Their canonical IDs remain blank because the pinned Realm of Thrones audit has no exact match; no XML ID is guessed or pooled across batches.

## Final versus censored battle state

`battle_pressure_margin.csv` publishes **12 final-stage** pressure margins. The remaining **3 active snapshots** are diagnostic and right-censored. Each `Retreated to the keep!` observation is retained as a completed outside-wall success, never a defeat.

## Complete ordinary-troop partition

Every visible ordinary occurrence appears in exactly one troop/party/context/result-state group. Below-gate rates and ranks are blank; blank counts mean the normalized row contained clipped values. No off-screen value was inferred.

| Party | Context | Participant | Observation state | Troop | Battles | Deployed | Kills | Kills/deployed | Status |
|---|---|---|---|---|---:|---:|---:|---:|---|
| Egon Emeros' Party | field | player_party | active_censored | Dothraki Barbarian [T5] | 1 | 7 | 11 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | active_censored | Dothraki Khal's Guard [T6] | 1 | 18 | 14 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | active_censored | Ghiscari Lockstep Legionnaire [T6] | 1 | 2 | 5 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | active_censored | Qartheen Enthroned Guardian [T6] | 1 | 32 | 97 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | active_censored | Qartheen Longbowman [T5] | 1 | 66 | 213 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | active_censored | Qartheen Pureborn Warrior [T4] | 1 | 5 | 1 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | active_censored | Qarthene Veteran Archer [T4] | 1 | 15 | 15 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | active_censored | Unsullied [T6] | 1 | 97 | 155 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qartheen Enthroned Guardian [T6] | 5 | 195 | 698 | 3.579487 | reliable |
| Egon Emeros' Party | field | player_party | completed | Qartheen Longbowman [T5] | 5 | 301 | 654 | 2.172757 | reliable |
| Egon Emeros' Party | field | player_party | completed | Unsullied [T6] | 5 | 440 | 683 | 1.552273 | reliable |
| Egon Emeros' Party | field | player_party | completed | Dothraki Barbarian [T5] | 3 | 43 | 84 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Dothraki Khal's Guard [T6] | 4 | 119 | 146 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Dothraki Nomad [T1] | 1 | 15 | 4 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Dothraki Savage [T4] | 1 | 8 | 11 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Ghiscari Lockstep Legionnaire [T6] | 4 | 8 | 19 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Ghiscari Soldier [T4] | 1 | 17 | 19 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Lengii Mounted Slayer [T4] | 1 | 2 | 2 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qartheen Archer [T3] | 2 |  |  |  | insufficient_missing_numeric_values |
| Egon Emeros' Party | field | player_party | completed | Qartheen Bowman [T2] | 1 | 2 | 1 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qartheen Elite Hoplite [T5] | 2 | 12 | 5 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qartheen Hoplite [T4] | 1 | 12 | 5 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qartheen Pureborn Champion [T5] | 4 | 11 | 23 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qartheen Pureborn Fighter [T3] | 2 | 6 | 4 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qartheen Pureborn Warrior [T4] | 3 | 15 | 9 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qartheen Pureborn Youth [T2] | 1 | 1 | 2 |  | insufficient_battles |
| Egon Emeros' Party | field | player_party | completed | Qarthene Veteran Archer [T4] | 3 | 27 | 38 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | active_censored | Ghiscari Lockstep Legionnaire [T6] | 1 | 1 | 3 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | active_censored | Qartheen Elite Hoplite [T5] | 1 | 31 | 44 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | active_censored | Qartheen Enthroned Guardian [T6] | 1 | 20 | 36 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | active_censored | Qartheen Hoplite [T4] | 1 | 3 | 3 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | active_censored | Qartheen Longbowman [T5] | 1 | 55 | 101 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | active_censored | Qartheen Master Cameleer [T5] | 1 | 9 | 8 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | active_censored | Qartheen Pureborn Champion [T5] | 1 | 2 | 4 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | active_censored | Qarthene Veteran Archer [T4] | 1 | 1 | 4 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Qartheen Enthroned Guardian [T6] | 6 | 212 | 567 | 2.674528 | reliable |
| Egon Emeros' Party | siege_attack | player_party | completed | Qartheen Longbowman [T5] | 6 | 322 | 365 | 1.133540 | reliable |
| Egon Emeros' Party | siege_attack | player_party | completed | Dothraki Khal's Guard [T6] | 5 | 190 | 172 | 0.905263 | reliable_provisional_identity |
| Egon Emeros' Party | siege_attack | player_party | completed | Unsullied [T6] | 6 | 517 | 372 | 0.719536 | reliable |
| Egon Emeros' Party | siege_attack | player_party | completed | Dothraki Archer [T4] | 1 | 14 | 5 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Dothraki Barbarian [T5] | 2 | 45 | 36 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Dothraki Bowlord [T5] | 2 | 16 | 18 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Dothraki Horse Archer [T4] | 1 | 1 | 2 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Dothraki Savage [T4] | 3 | 18 | 8 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Dothraki Warrior [T3] | 1 | 1 | 1 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Forest Bandit [T4] | 1 | 2 | 3 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Ghiscari Lockstep Legionnaire [T6] | 4 | 6 | 8 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Ghiscari Soldier [T4] | 1 | 16 | 9 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Lengii Mounted Slayer [T4] | 1 | 3 | 14 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Norvoshi Spearman [T4] | 1 | 1 | 3 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Qartheen Archer [T3] | 1 | 12 | 18 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Qartheen Elite Hoplite [T5] | 2 | 25 | 5 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Qartheen Pureborn Champion [T5] | 1 | 5 | 9 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Qarthene Veteran Archer [T4] | 3 | 15 | 10 |  | insufficient_battles |
| Egon Emeros' Party | siege_attack | player_party | completed | Qohorik Elite Archer [T5] | 1 | 3 | 2 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Dothraki Archer [T4] | 1 | 3 | 7 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Dothraki Barbarian [T5] | 1 | 2 | 4 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Dothraki Bowlord [T5] | 1 | 4 | 8 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Ghiscari Archer [T3] | 1 | 8 | 7 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Ghiscari Footman [T2] | 1 | 6 | 4 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Ghiscari Recruit [T1] | 1 | 6 | 4 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Ghiscari Soldier [T4] | 1 | 2 | 5 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qartheen Archer [T3] | 1 | 18 | 21 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qartheen Elite Hoplite [T5] | 1 | 23 | 18 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qartheen Footman [T2] | 1 | 17 | 10 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qartheen Hoplite [T4] | 1 | 8 | 10 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qartheen Pureborn Warrior [T4] | 1 | 2 | 8 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qartheen Pureborn Youth [T2] | 1 | 5 | 4 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qartheen Recruit [T1] | 1 | 16 | 10 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qartheen Soldier [T3] | 1 | 11 | 13 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Qarthene Veteran Archer [T4] | 1 | 6 | 15 |  | insufficient_battles |
| Jaime Lannister's Party | field | allied_party | completed | Unsullied [T6] | 2 |  | 90 |  | insufficient_missing_numeric_values |
| Rhoella Qar Deeth's Party | siege_attack | allied_party | completed | Qartheen Pureborn Champion [T5] | 1 |  | 6 |  | insufficient_missing_numeric_values |
| Walder Frey's Party | field | player_party | active_censored | Baratheon Hammerknight [T6] | 1 | 6 | 4 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Blackwood Archer [T4] | 1 | 2 | 1 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Blackwood Longbowman [T5] | 1 | 4 | 1 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Bracken House Guard [T5] | 1 | 2 | 0 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Celtigar Banneret [T6] | 1 | 34 | 27 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Frey Assassin [T6] | 1 | 88 | 111 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Mountain's Man [T6] | 1 | 5 | 1 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Queen's Man [T6] | 1 | 18 | 12 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Velaryon Renegade [T5] | 1 | 1 | 0 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | active_censored | Velaryon Sea Guard [T6] | 1 | 28 | 25 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Baratheon Hammerknight [T6] | 1 | 6 | 7 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Blackwood Archer [T4] | 1 | 2 | 1 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Blackwood Longbowman [T5] | 1 | 4 | 9 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Bracken House Guard [T5] | 1 | 1 | 0 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Celtigar Banneret [T6] | 1 | 33 | 76 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Frey Assassin [T6] | 1 | 88 | 231 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Mountain's Man [T6] | 1 | 5 | 1 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Queen's Man [T6] | 1 | 18 | 24 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Velaryon Renegade [T5] | 1 | 1 | 0 |  | insufficient_battles |
| Walder Frey's Party | field | player_party | completed | Velaryon Sea Guard [T6] | 1 | 25 | 38 |  | insufficient_battles |
| Wendello Qar Deeth's Party | siege_attack | allied_party | completed | Qartheen Hoplite [T4] | 1 | 19 | 5 |  | insufficient_battles |
| Wendello Qar Deeth's Party | siege_attack | allied_party | completed | Qartheen Soldier [T3] | 1 | 37 | 15 |  | insufficient_battles |

## Queue decision

No queue mutation is justified. `active_test` remains null and `ordered_queue` remains empty. The verification hold remains **Arryn Winged Knight**; a hold is not a recommendation.

## Integrity and limitations

The normalized archive matches `46d9010bd6be2d9121539b2408a9da91f228a67ca5b08f4b9ced8e7abca7d59c` exactly. The committed Base64 text omits only the final newline recorded by Phase 1; the reviewed layer records both transport hashes and confirms identical decoded bytes. The separate missing-manifest blocker remains unresolved.

The pinned track audit confirms **33/43 ordinary labels** by exact name. Three ordinary rows preserve clipped numeric cells, and 12 party summaries preserve visible coverage gaps. Raw PNGs are not retained, so Phase 2 verifies their committed manifest hashes but cannot repeat pixel-level review. Phase 1 did not record an exact game version, so this batch is not pooled with versioned historical cohorts.

No universal or role-blended score is published, frozen model files are unchanged, and model/residual files explicitly record `not_run`. No battle is excluded as an outlier because this mixed campaign batch has no predeclared outlier rule. Campaign opponent, composition, terrain, orders, exposure, and difficulty remain uncontrolled confounders.
