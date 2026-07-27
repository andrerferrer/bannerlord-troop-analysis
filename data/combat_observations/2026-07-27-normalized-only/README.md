# Bannerlord combat screenshot normalization — 2026-07-27

This directory contains the normalized evidence layer for the uploaded Realm of Thrones combat-result screenshot batch.

## Scope

This batch intentionally stops before analytical ranking or model comparison. It preserves the extracted and normalized records required for later review, canonical identity resolution, aggregation, and analysis.

## Coverage

- Source ZIP SHA-256: `42d4adf2e8d9f9bce0dc90945832c673aeddf81d06044cb0e6f08a2ddb852617`
- Screenshots: **13**
- Grouped final battles: **10**
- Active scoreboard excluded: **1**
- Structured observations: **328**
- Player-side ordinary troop observations: **143**
- Review items: **5**

## Files

- `screenshots_manifest.csv` — image hashes, timestamps, grouping, and inclusion status.
- `screenshots.jsonl` — screenshot-level provenance and status.
- `battles.jsonl` — normalized battle metadata.
- `troop_occurrences.jsonl` — all extracted party, troop, hero, and artifact rows.
- `primary_troop_occurrences.jsonl` — ordinary player-side troop rows eligible for later analysis.
- `troop_battle_consolidated.jsonl` — duplicate/overlap-safe consolidation within each battle.
- `review_queue.csv` — fields that require later review.
- `normalization_summary.json` — batch-level counts and provenance.
- `validation_report.json` — structural validation result and known limitations.
- `artifact_hashes.csv` — SHA-256 and size for every committed normalized artifact.

Raw screenshots are intentionally not committed to normal Git history. Their SHA-256 hashes are preserved in the manifest.
