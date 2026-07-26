# Multi-track canonical identity audit — 2026-07-23 batch

## Decision

The 2026-07-23 result screens are a **mixed-track dataset**. They contain Realm of Thrones troops, official War Sails troops, and Rhodok-labelled troops whose exact source track is not yet proven. The dataset must not be canonicalized against the vanilla + War Sails audit alone.

## Conservative matching policy

A canonical ID is accepted only when a versioned repository artifact contains an exact `name → troop_id` relationship. Similar slugs, apparent naming conventions, and likely XML IDs are not enough.

Statuses:

- `confirmed_id`: exact versioned name-to-ID evidence;
- `track_confirmed_id_unresolved`: track is proven, but the reference does not expose an ID;
- `unresolved`: track or ID is not proven;
- `missing_audit_row`: baseline label was not represented in the audit table.

## Current coverage of the five-battle baseline

| Measure | Count |
|---|---:|
| Eligible overall labels | 24 |
| Confirmed canonical IDs | 2 |
| Track confirmed, ID unresolved | 4 |
| Fully unresolved | 18 |

Confirmed mappings:

| Observed label | Track | Canonical troop ID | Evidence |
|---|---|---|---|
| Baratheon Hammerknight [T6] | Realm of Thrones | `baratheon_pikeknight` | `data/rot_reference/hot_20260717/v43_top20_overall.csv` |
| Dragonstone Elite Halberdier [T5] | Realm of Thrones | `dragonstone_headsman` | `data/rot_reference/empirical/20260703_model_vs_empirical_delta_controls.csv` |

Track-only confirmations:

- Queen's Man [T6] — preserved RoT empirical aggregate;
- Stormlands Heavy Crossbowman [T5] — preserved RoT empirical aggregate;
- Dragonstone House Guard [T5] — preserved RoT empirical aggregate;
- Imperial Naute — official War Sails scope in the v7.3 model output.

## Important blocker

The V4.3 generator proves that a complete RoT audit existed and that its outputs carry real `troop_id` values. However, the complete all-troop V4.3 output or original RoT troop-audit input has not yet been located as a directly committed file. Selected outputs and scripts are present.

Until the full reference is recovered or re-exported:

- descriptive rankings continue to use the reviewed provisional slug;
- model joins requiring attributes must use `--require-complete` and fail;
- no unresolved slug may be silently treated as an XML troop ID;
- Rhodok-labelled rows remain a separate unresolved track.

## Next execution step

1. recover the full RoT V4.3 ranked/audit table from repository history or re-export the installed RoT/HOT modules;
2. recover the complete official vanilla + War Sails troop audit with IDs;
3. identify the source module for the Rhodok-labelled units;
4. regenerate this table and require 100% ID coverage for all labels entering attribute modeling;
5. then build canonical dataset v2.
