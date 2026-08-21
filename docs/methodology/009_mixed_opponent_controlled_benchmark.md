# Mixed-opponent controlled benchmark v1

- **Status:** accepted secondary test protocol
- **Date:** 2026-08-21
- **Scope:** field performance of one target troop against a fixed varied army

## Purpose

Measure how a mono-troop force handles several battlefield threats in one repeatable test. This complements campaign evidence and homogeneous matchups; it does not replace or pool with either dataset.

## Primary setup

Use one versioned profile for every candidate:

```text
player: 50 copies of the target troop
enemy:  100 fixed reference troops
```

The enemy profile contains 20 troops from each role:

1. shield infantry;
2. shock or polearm infantry;
3. foot ranged;
4. heavy cavalry;
5. horse archer.

Before the first official run for a game track, resolve each role to one concrete canonical troop ID and freeze the result as an `opponent_composition_id`. Do not silently replace unavailable troops between candidates. Version the composition when the game/mod version or any member changes.

Use `50 vs 100` as the primary stress test because `50 vs 50` is more likely to produce easy wins that fail to separate strong candidates. A `50 vs 50` profile may be added later as a separately named diagnostic; never pool the two ratios.

## Repetition and controls

Run at least five independent battles per target troop. Use the same versioned map suite and keep constant:

- game/mod track and version;
- difficulty and damage settings;
- time, weather, and other battle options;
- player perks and captain effects;
- spawn/deployment rules;
- command protocol;
- opponent composition.

The v1 command protocol is `F1 F3` once at the start, followed by no intervention. The player must not contribute kills. If the interface cannot create the exact mixed army, first establish a deterministic setup method and freeze it; approximate ad hoc compositions are not comparable official runs.

## Metrics

Report per battle and across the five-battle set:

- target kills per target deployed;
- enemy neutralization rate: target kills / 100 enemy deployed;
- target survival, death, wounded, and casualty rates;
- win rate;
- median, best, worst, and battle-level variation;
- duration only when it is captured reliably for every candidate.

Player-side kill share is not a discriminator here because the target troop is the only eligible player-side troop. Mark it as structurally uninformative rather than awarding a 100% impact bonus.

## Data boundaries

Store the benchmark under its own controlled-test scope with the target troop ID, `opponent_composition_id`, map-suite ID, command-protocol ID, force ratio, and game track. Never mix it into campaign rankings, homogeneous matchup results, siege contexts, or a different composition version.

An interrupted readable scoreboard remains one valid battle exactly as shown. Any cleanup re-engagement is another battle. Never reconstruct or merge values across them; only complementary screenshots proven to show the same result table may share a `battle_id`.

## Interpretation

Treat this as a combined robustness and AI-usability test under a 2:1 mixed threat. It answers whether the target troop can carry a varied field fight under the fixed protocol. It does not isolate which enemy role caused success or failure; follow-up homogeneous or role-specific tests are required for that causal question.
