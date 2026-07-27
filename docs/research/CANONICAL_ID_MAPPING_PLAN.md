# Canonical troop-ID mapping plan

## Objective

Replace provisional OCR-derived troop slugs with verified Bannerlord 1.4.x + War Sails game/XML troop IDs before attribute integration or model recalibration.

## Inputs

- reviewed empirical troop labels;
- selected-track troop audit;
- module load order and override report;
- versioned alias table;
- raw and normalized display names.

## Resolution order

1. exact verified display-name match;
2. exact normalized-name match;
3. approved alias-table match;
4. conservative unique fuzzy candidate;
5. manual review;
6. explicit unresolved status.

## Required output columns

```text
provisional_slug
display_name_raw
display_name_normalized
canonical_troop_id
canonical_display_name
match_method
match_confidence
source_module
source_xml
track
track_version
review_status
review_note
```

## Rules

- No empirical-to-feature join through display-name guessing.
- More than one viable candidate requires manual review.
- Later module definitions override earlier definitions according to selected load order.
- Missing or ambiguous identities remain explicit.
- Hero, lord, companion, player, and OCR-artifact rows are not mapped as normal troops.
- Realm of Thrones empirical data must not be silently joined to the vanilla + War Sails track.

## Validation

- every mapped ID exists in the selected track audit;
- every ranked label has a verified ID or explicit unresolved status;
- aliases are unique and versioned;
- no provisional label maps to multiple canonical IDs without an override record;
- output is deterministic and hash-addressed.

## Completion gate

Canonical dataset v1 may be generated only when every displayed five-battle result has a verified troop ID or is explicitly excluded from feature modeling.
