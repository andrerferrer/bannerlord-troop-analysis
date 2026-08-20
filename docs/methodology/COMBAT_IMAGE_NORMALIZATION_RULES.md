# Combat Image Normalization Rules

- **Status:** Interview decisions in progress
- **Date:** 2026-07-24
- **Related ADR:** `ADR-001-combat-image-normalization.md`

This document records the accepted normalization rules derived from representative Bannerlord battle-result screenshots. It is intentionally updated during the schema interview and will later be converted into the final JSON Schema, extractor prompt, and validation code.

## Screenshot and historical deduplication

1. Before extraction, compare the new input against all committed screenshot manifests and source inventories.
2. Skip and report exact SHA-256 matches. Because attachment transport can re-encode images, also skip an exact recorder filename plus embedded capture timestamp match even when bytes differ.
3. Inspect the visible scoreboard for every possible duplicate within the batch. Use side/party headings, totals, troop rows, result state, timer, and environment to establish same-screen or same-battle identity.
4. Duplicate final screens contribute once. Sequential active scoreboards belong to one battle and are excluded from primary evidence. Complementary scroll positions may be retained under the same battle only for otherwise hidden rows; overlapping occurrences contribute once.
5. Prefer a final result, then greater row coverage, fewer obstructions, and sharper text. Recency is only a tie-breaker.
6. Record accepted, skipped, supplemental, and already-normalized decisions in `reports/screenshot_deduplication_audit.csv` and surface the counts to the user.

## Battle context classification

Supported values:

```text
field
siege_attack
siege_defense
undefined
```

Rules:

1. Battle context is inferred from the image.
2. If the evidence is insufficient or conflicting, store `undefined` and request user classification later.
3. A later user correction is stored as an override without deleting the original inference.
4. `Garrison of ...` and `Militia of ...` are strong textual evidence of a siege.
5. Fortifications, walls, towers, gates, ladders, siege engines, or a city/castle environment are supporting visual evidence of a siege.
6. A natural open environment without siege evidence supports `field`.
7. The player-controlled party is visually highlighted in green.
8. Player party on the attacker side supports `siege_attack` when the battle is a siege.
9. Player party on the defender side supports `siege_defense` when the battle is a siege.
10. Very high player kills may be retained as supporting evidence, but are not sufficient by themselves to classify a siege defense.

## Dataset scope and unresolved keep-retreat discrepancy

The original rule interview stated that the supplied dataset contained no `Retreated to the keep!` screen. The later first-pass summary states that image 58 visibly contains that screen and was excluded.

The source image and normalized screenshot record are currently unavailable because the source ZIP is missing and the committed normalized bundle is corrupt. Repository history proves that PR #11 removed keep-phase scope before PR #12 added the conflicting first-pass claim, but it does not prove which visual classification is correct.

Canonical policy:

1. preserve image 58 in the manifest and exclusion audit;
2. label its current classification `explicitly_unresolved`;
3. do not implement a keep detector from the contradictory prose;
4. resolve only from the exact-hash source image or independently verified raw extraction evidence;
5. continue excluding it from production rankings until that evidence is reviewed, without claiming visual confirmation.

## Result-table columns

The visible numeric columns are, from left to right:

| Position | Visual cue | Field | Meaning | Primary-analysis relevance |
|---:|---|---|---|---|
| 1 | green | `survivors` | troops that survived | primary |
| 2 | blue, sword icon | `kills` | enemies killed | primary |
| 3 | gray | `upgrade_ready` | troops ready to upgrade | recorded, secondary |
| 4 | red, skull icon | `deaths` | troops killed | primary |
| 5 | yellow/orange, cracked shield | `wounded` | troops wounded | primary |
| 6 | final column | `routed` | troops that fled because of low morale | recorded, secondary |

The deployed count is derived as:

```text
deployed = survivors + deaths + wounded
```

`upgrade_ready` and `routed` are preserved because extraction cost is negligible, but they do not drive the primary troop-performance score at this stage.

## Routed troops and morale

Always preserve the visible `routed` count and derive:

```text
routed_rate = routed / deployed
```

Policy:

1. `routed` and `routed_rate` remain secondary contextual metrics.
2. They do not enter the primary troop-performance score.
3. They do not change the deployed-count formula and must not be added to `deployed` a second time.
4. Route behavior should be analyzed separately by battle result when the result is available, because army collapse and defeat strongly affect routing.
5. A high routed rate must not automatically be interpreted as an intrinsic weakness of the troop. Party morale, commander effects, casualties, battle context, and the wider army state may contribute.
6. Historical outputs may expose routed totals and rates, but primary rankings remain based on the accepted combat-performance metrics.

## Row hierarchy

Preserve all visible aggregation levels:

```text
side_total
party
troop
player
hero
```

Primary use:

- troop rows: unit-performance analysis;
- party, garrison, and militia rows: group-level analysis and aggregation validation;
- side totals: battle-level analysis and completeness checks;
- player row: contextual evidence only;
- companion and lord rows: excluded from troop rankings and do not require canonical hero-ID normalization.

## Relationship to the player

When it can be inferred reliably, retain the following optional metadata on troop occurrences:

```text
player_party
allied_party
enemy_party
unknown
```

This field is preserved for auditability and possible future sensitivity analysis, because player perks, captain bonuses, and tactical control may affect results.

It does **not** split the primary historical dataset at this stage. The main consolidations combine valid troop occurrences regardless of relationship to the player, while retaining the metadata so separate views can be generated later without reprocessing the screenshots.

Failure to infer this field does not invalidate an otherwise usable troop observation.

## Same troop in multiple parties

Each occurrence remains separate at extraction time.

The pipeline also creates a consolidated record for each `battle_id + troop_id` by summing all valid occurrences.

Rates must be recalculated from consolidated totals, not averaged from occurrence-level rates.

## Multiple screenshots from the same battle

Screenshots are grouped automatically when evidence indicates they are scroll states or pages of the same result table.

Grouping evidence includes:

- close capture timestamps;
- identical side totals;
- matching parties, garrisons, and militias;
- same scenario and battle context;
- overlapping troop rows;
- visible scroll continuity.

Ambiguous groupings are routed to user review.

Repeated rows across screenshots are deduplicated using the visible row identity and values, including side, parent group, name, survivors, kills, upgrade-ready count, deaths, wounded, and routed count.

## Historical consolidations

Generate all of the following:

```text
field
siege_attack
siege_defense
overall
```

The main historical metric uses summed totals:

```text
historical_kills_per_deployed = total_kills / total_deployed
```

Do not use an unweighted average of per-battle rates as the primary metric.

Also retain the verified kill total from the player's scoreboard side and derive:

```text
player_side_kill_share = troop_kills / verified_player_side_total_kills
share_adjusted_impact  = kills_per_deployed * player_side_kill_share
```

At context-aggregate level, recompute both components from compatible sums:

```text
historical_kills_per_deployed = sum(troop_kills) / sum(troop_deployed)
player_side_kill_share        = sum(troop_kills) / sum(player_side_total_kills)
share_adjusted_impact         = historical_kills_per_deployed * player_side_kill_share
```

The denominator is the total of the player's **side**, not the sum of visible
troop rows and not one selected party. The side total includes kills attributed
to heroes and other parties, which is intentional: the share measures how much
of the actual side output the troop supplied. Party totals remain useful for
hierarchy validation and separate party-level sensitivity views.

Publish both the efficiency rank (`historical_kills_per_deployed`) and the
impact rank (`share_adjusted_impact`). The impact rank is descriptive campaign
evidence and must not overwrite the frozen theoretical model. A troop with high
efficiency but low kill share is a high-output niche deployment; high efficiency
and high share indicates broad realized impact.

Only calculate an aggregate impact score when every contributing battle has one
unambiguous, positive player-side kill total and the troop-side relationship is
verified. Repeated equal side totals may corroborate one denominator; conflicting,
missing, or partial totals make the aggregate impact fields null. Report the
number of covered battles and whether coverage is complete. Never infer the
denominator from visible troop rows because off-screen, player, and hero rows may
be absent.

Example:

```text
2.0 kills/deployed * 90% player-side kill share = 1.80 impact
4.0 kills/deployed * 25% player-side kill share = 1.00 impact
```

The micro-aggregated kill share above is the primary share component. A simple
mean of battle-level kill shares may be emitted as a diagnostic for consistency,
but it must not replace the primary aggregate.

The `overall` view must be marked as mixing battle contexts and must not replace context-specific comparisons.

## Evidence grading and minimum samples

Do not discard troop observations solely because the sample is small. Instead, assign an `evidence_grade` using both total valid deployed troops and independent battle count.

The grade is the highest level for which **both** thresholds are met:

| Evidence grade | Valid deployed troops | Independent battles |
|---|---:|---:|
| `exploratory` | any amount | 1 |
| `low` | at least 10 | at least 2 |
| `medium` | at least 30 | at least 3 |
| `high` | at least 100 | at least 5 |

Examples:

- 300 deployed in one battle remains `exploratory`;
- 20 deployed across four battles is `low`;
- 80 deployed across three battles is `medium`;
- 150 deployed across six battles is `high`;
- 500 deployed across two battles is `low`.

Generate two analytical views:

1. a complete ranking containing every troop with at least one valid observation;
2. a reliable ranking containing only `medium` and `high` evidence grades.

Calculate the grade separately for `field`, `siege_attack`, `siege_defense`, and `overall`. A troop may therefore have different grades in different contexts.

Occurrences excluded from the primary analysis, including suspected siege-engine outliers, do not contribute to primary sample-size thresholds.

These thresholds are provisional and must be recalibrated after inspecting the distribution of the first processed empirical batch.

## Suspected siege-engine outliers

A siege-defense occurrence may be automatically marked as a probable siege-engine result when it combines:

- very small deployed count;
- extreme kills per deployed soldier;
- a large deviation from other troops in the same battle;
- a large deviation from that troop's historical distribution.

Policy:

1. Never delete the raw occurrence.
2. Mark the occurrence as `suspected_siege_engine_outlier`.
3. Exclude an occurrence automatically only when an explicit reviewed flag or a calibrated deterministic rule with retained provenance supports it.
4. Retain it in a separate siege-engine-assisted analysis and outlier report.
5. Apply exclusion at occurrence level only.
6. Other normal occurrences of the same troop, including another party in the same battle, remain in the consolidated primary analysis.
7. Uncalibrated descriptive thresholds route to review only; detection thresholds remain open until the verified empirical image set is available.

## Current open decisions

- siege-engine outlier thresholds;
- exact schema for side totals, party totals, troop occurrences, and historical aggregates;
- storage policy for raw images.
