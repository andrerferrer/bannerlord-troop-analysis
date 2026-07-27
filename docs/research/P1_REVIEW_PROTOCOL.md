# P1 review protocol

## Scope

Review the 94 remaining player-side rows with unresolved core-field uncertainty that do not currently drive the five-battle display gate.

## Objective

Complete the remaining player-side image-backed review without modifying the immutable raw extraction layer.

## Review order

1. Rows belonging to troop labels with four independent battles.
2. Rows that could move a label above 20 deployed troops.
3. Rows with uncertain kills.
4. Rows with uncertain survivors, deaths, or wounded.
5. Rows with uncertain troop identity.
6. Remaining player-side core-field uncertainties.

## Required review record

Each reviewed row must preserve:

```text
battle_id
screenshot_id
source_row_identifier
original_display_name
reviewed_display_name
original_survivors
reviewed_survivors
original_kills
reviewed_kills
original_deaths
reviewed_deaths
original_wounded
reviewed_wounded
original_routed
reviewed_routed
changed_fields
review_status
review_reason
review_source
reviewer
reviewed_at
```

Allowed review statuses:

```text
confirmed
corrected
excluded
unresolved
```

## Rules

- Never overwrite the raw first-pass record.
- Never infer an unreadable value only to complete a row.
- Preserve unresolved values as null or unresolved.
- Recompute `deployed`, casualties, and all rates after applying reviewed values.
- Do not average child-row rates.
- Apply aliases only through the versioned alias table.
- Rebuild rankings after each review batch.
- Continue to require at least 5 independent battles and 20 deployed troops for display.

## Batch execution

Review in batches of 15–25 rows. After each batch:

1. validate correction-file structure;
2. replay corrections against raw JSONL;
3. regenerate the strict baseline;
4. compare eligible labels and rank movement;
5. record output hashes;
6. commit the batch with a short report.

## Completion criteria

- all 94 rows have a terminal review status;
- no correction lacks source provenance;
- correction replay is deterministic;
- ranking sensitivity before and after P1 is published;
- the P1 queue is reduced to zero or explicitly documented unresolved rows;
- canonical dataset generation may proceed.
