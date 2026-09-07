# Output contract

## Required response

Do not send a normal progress or completion response for a new evidence batch until its branch has been published and its single draft pull request exists. The only exception is a genuine GitHub/repository/host-platform failure that prevents the pull request itself; report the exact failed action and error in that case.

Report:

1. `COMPLETE`, `COMPLETE_WITH_EXTERNAL_BLOCKERS`, or `BLOCKED`;
2. pull request number, URL, current state, draft/ready status, branch, and latest head commit; when publication itself failed, replace this with the exact failed GitHub action and platform error;
3. input name and verified SHA-256, or explicit host-attachment provenance with source-byte hash unavailable;
4. mode, pipeline/schema versions, and model provenance;
5. new, already-normalized, duplicate, supplemental, interrupted/active, battle, occurrence, canonical, excluded, outlier, and unresolved counts;
6. schema/semantic validation result;
7. complete/reliable and context ranking paths;
8. model comparison and residual paths;
9. highest-impact unresolved items;
10. efficiency rank, player-side kill share, share-adjusted impact rank, kill-total coverage, directly verified deployment share, offensive contribution ratio/gap, and retention;
11. canonical role, role-population coverage, and role-adjusted rank when the role-population gate passes;
12. limitations/evidence grades;
13. exact resume command when incomplete, tied to the already-open pull request and branch.

Do not claim completion from prose alone. Link the repository pull request and structured artifacts. A chat-only preliminary calculation is not a delivered batch.

Ranking CSVs must keep `historical_kills_per_deployed`, `player_side_kill_share`,
and `share_adjusted_impact` as separate columns, with independent efficiency and
impact ranks. Leave share/impact null unless verified player-side kill totals
cover every contributing battle.

When verified player-side deployment totals cover the same contributing battles,
also publish `player_side_deployment_share`, `offensive_contribution_ratio`,
`offensive_share_gap`, and `retention_rate`. Never reconstruct the deployment
denominator from partial visible troop rows.

Role-adjusted empirical outputs must follow
[`docs/methodology/010_role_adjusted_empirical_evaluation.md`](../../../../docs/methodology/010_role_adjusted_empirical_evaluation.md):
rank only inside the same track, context, and role; weight defense twice for
frontline infantry and melee cavalry, weight offense twice for ranged troops,
and leave the blended score null until at least five reliable role rows exist.
Never use that result as a universal cross-role ladder or infer damage absorbed,
support credit, aggro, or counterfactual kills.

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
screenshot_deduplication_audit.csv
grouping_validation.csv
aggregation_validation.csv
outlier_report.csv
battle_context_review.csv
canonical_validation_report.json
model_vs_empirical.csv
empirical_residual_rankings.csv
empirical_analysis_summary.md
```

For directly attached screenshots whose bytes are not mounted, source artifacts must use stable host attachment identifiers or deterministic upload order and explicitly state that byte size and SHA-256 are unavailable. Never invent either value.

## Status rules

Use `COMPLETE` only after the requested production input passes integrity, review, canonical validation, output, repository review, and applicable merge gates.

Use `COMPLETE_WITH_EXTERNAL_BLOCKERS` after every safe task is complete and published in the existing pull request, but a required input, paid authorization, upload authority, source-byte integrity check, or human decision remains. Optional raw-image retention does not force this status when a verified normalized bundle is the declared authoritative input and any non-reviewable fields remain explicitly unresolved or excluded.

Use `BLOCKED` when a missing prerequisite prevents meaningful processing of the supplied input. Except when GitHub publication itself is the blocker, commit and publish every safe partial artifact to the batch draft pull request before returning this status.
