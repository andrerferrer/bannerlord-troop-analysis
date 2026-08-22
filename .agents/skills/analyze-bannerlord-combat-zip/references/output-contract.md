# Output contract

## Required response

Report:

1. `COMPLETE`, `COMPLETE_WITH_EXTERNAL_BLOCKERS`, or `BLOCKED`;
2. input name and verified SHA-256;
3. mode, pipeline/schema versions, and model provenance;
4. new, already-normalized, duplicate, supplemental, interrupted/active, battle, occurrence, canonical, excluded, outlier, and unresolved counts;
5. schema/semantic validation result;
6. complete/reliable and context ranking paths;
7. model comparison and residual paths;
8. highest-impact unresolved items;
9. efficiency rank, player-side kill share, share-adjusted impact rank, kill-total coverage, directly verified deployment share, offensive contribution ratio/gap, and retention;
10. canonical role, role-peer coverage, and role-adjusted rank when the peer gate passes;
11. limitations/evidence grades;
12. exact resume command.

Do not claim completion from prose alone. Link structured artifacts.

Ranking CSVs must keep `historical_kills_per_deployed`, `player_side_kill_share`,
and `share_adjusted_impact` as separate columns, with independent efficiency and
impact ranks. Leave share/impact null unless verified player-side kill totals
cover every contributing battle.

When verified player-side deployment totals cover the same contributing battles,
also publish `player_side_deployment_share`, `offensive_contribution_ratio`,
`offensive_share_gap`, and `retention_rate`. Never reconstruct the deployment
denominator from partial visible troop rows.

Role-adjusted empirical outputs must follow
[`docs/methodology/010_role_adjusted_empirical_evaluation.md`](../../../docs/methodology/010_role_adjusted_empirical_evaluation.md):
rank only inside the same track, context, and role; weight defense twice for
frontline infantry and melee cavalry, weight offense twice for ranged troops,
and leave the blended score null until at least five reliable role peers exist.
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

## Status rules

Use `COMPLETE` only after the requested production input passes integrity, review, canonical validation, and output gates.

Use `COMPLETE_WITH_EXTERNAL_BLOCKERS` after every safe local task is complete but a required input, paid authorization, upload authority, or human decision remains. Optional raw-image retention does not force this status when a verified normalized bundle is the declared authoritative input and any non-reviewable fields remain explicitly unresolved or excluded.

Use `BLOCKED` when a missing prerequisite prevents meaningful processing of the supplied input.
