# Output contract

## Required response

Report:

1. `COMPLETE`, `COMPLETE_WITH_EXTERNAL_BLOCKERS`, or `BLOCKED`;
2. input name and verified SHA-256;
3. mode, pipeline/schema versions, and model provenance;
4. image, battle, occurrence, canonical, excluded, outlier, and unresolved counts;
5. schema/semantic validation result;
6. complete/reliable and context ranking paths;
7. model comparison and residual paths;
8. highest-impact unresolved items;
9. limitations/evidence grades;
10. exact resume command.

Do not claim completion from prose alone. Link structured artifacts.

## Artifact classes

```text
manifest/
staging/
extraction/
reviewed/
canonical/
reports/
analysis/
batch_state.json
```

Expected canonical files:

```text
canonical_screenshots.jsonl
canonical_battles.jsonl
canonical_occurrences.jsonl
canonical_troop_battle_consolidated.jsonl
canonical_historical_aggregates.jsonl
```

Expected reports:

```text
review_resolutions.csv
unresolved_rows.csv
duplicate_report.csv
grouping_validation.csv
aggregation_validation.csv
outlier_report.csv
battle_context_review.csv
canonical_validation_report.json
model_vs_empirical.csv
empirical_residual_rankings.csv
empirical_analysis_summary.md
```

## Status rules

Use `COMPLETE` only after the requested production input passes integrity, review, canonical validation, and output gates.

Use `COMPLETE_WITH_EXTERNAL_BLOCKERS` after every safe local task is complete but images, paid authorization, upload authority, or human decisions remain.

Use `BLOCKED` when a missing prerequisite prevents meaningful processing of the supplied input.
