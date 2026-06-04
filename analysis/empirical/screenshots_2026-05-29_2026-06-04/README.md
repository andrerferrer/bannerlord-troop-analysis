# Bannerlord Empirical Validation — Screenshot Batch 2026-05-29 to 2026-06-04

This directory contains normalized empirical observations from user-provided battle-result screenshots.

Use these files to compare model-predicted rankings against observed battlefield output:

- `empirical_battle_results_normalized.csv`
- `empirical_troop_aggregate_summary.csv`
- `empirical_findings_2026-06-04.md`
- `screenshot_manifest.csv`
- `schema.md`

Current baseline: v7.1 head-weighted survivability model.

Main finding: Imperial Naute is a strong empirical overperformer in short engagements and should receive a dedicated `burst_score` / `boarding_score` instead of being forced into only the general ranking.
