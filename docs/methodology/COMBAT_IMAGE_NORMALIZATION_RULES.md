# Combat Image Normalization Rules

- **Status:** Interview decisions in progress
- **Date:** 2026-07-24
- **Related ADR:** `ADR-001-combat-image-normalization.md`

This document records the accepted normalization rules derived from representative Bannerlord battle-result screenshots. It is intentionally updated during the schema interview and will later be converted into the final JSON Schema, extractor prompt, and validation code.

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

## Keep phases

Screens showing `Retreated to the keep!` and the subsequent keep-combat phases are excluded from the primary analysis.

They may be retained as raw evidence with:

```text
analysis_status=excluded
exclusion_reason=keep_phase_not_relevant
```

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

The `overall` view must be marked as mixing battle contexts and must not replace context-specific comparisons.

## Suspected siege-engine outliers

A siege-defense occurrence may be automatically marked as a probable siege-engine result when it combines:

- very small deployed count;
- extreme kills per deployed soldier;
- a large deviation from other troops in the same battle;
- a large deviation from that troop's historical distribution.

Policy:

1. Never delete the raw occurrence.
2. Mark the occurrence as `suspected_siege_engine_outlier`.
3. Exclude that occurrence automatically from the primary troop analysis.
4. Retain it in a separate siege-engine-assisted analysis and outlier report.
5. Apply exclusion at occurrence level only.
6. Other normal occurrences of the same troop, including another party in the same battle, remain in the consolidated primary analysis.
7. Detection thresholds remain open until calibrated against the empirical image set.

## Current open decisions

- exact treatment and analytical value of routed troops;
- how to identify and exclude all post-retreat keep screenshots automatically;
- minimum sample sizes and uncertainty reporting;
- siege-engine outlier thresholds;
- exact schema for side totals, party totals, troop occurrences, and historical aggregates;
- storage policy for raw images.
