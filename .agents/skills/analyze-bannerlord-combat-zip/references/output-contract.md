# Output contract

## Required response

Report:

1. `COMPLETE`, `COMPLETE_WITH_EXTERNAL_BLOCKERS`, or `BLOCKED`;
2. input name and verified SHA-256;
3. mode, pipeline/schema versions, and model provenance;
4. image, battle, occurrence, canonical, excluded, outlier, and unresolved counts;
5. schema/semantic validation result;
6. complete/reliable and context ranking paths when analytical execution was requested;
7. model comparison and residual paths when analytical execution was requested;
8. highest-impact unresolved items;
9. limitations/evidence grades;
10. exact resume command;
11. for a published Phase 1 batch: repository batch path, branch, full normalization commit SHA, draft PR number/link, task ID, and pending protocol-comment status.

Do not claim completion from prose alone. Link structured artifacts. Never claim a repository write that the host did not confirm.

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

## Phase 1 publication response

For a normalization-only repository handoff, analytical paths and rankings are intentionally absent. Report instead:

```text
phase: normalization
batch_id: <id>
batch_path: data/combat_observations/<batch>
validation: pass|fail
review_queue: <count>
branch: <branch>
normalization_commit: <full SHA>
draft_pr: <number and URL>
analysis_task_comment: pending|missing|failed
task_id: <id>
```

Use `COMPLETE` only when the requested Phase 1 artifacts, draft PR, and valid pending task comment all exist. A branch or PR without the authoritative task comment is incomplete.

## Status rules

Use `COMPLETE` only after the requested production input passes the gates for the requested scope. For analytical runs, that means integrity, review, canonical validation, and requested outputs. For Phase 1 publication, that means validated normalization, repository-addressable handoff artifacts, a draft PR, and a valid pending protocol comment.

Use `COMPLETE_WITH_EXTERNAL_BLOCKERS` after every safe local task is complete but a required input, paid authorization, upload authority, GitHub write, or human decision remains. Optional raw-image retention does not force this status when a verified normalized bundle is the declared authoritative input and any non-reviewable fields remain explicitly unresolved or excluded.

Use `BLOCKED` when a missing prerequisite prevents meaningful processing of the supplied input.
