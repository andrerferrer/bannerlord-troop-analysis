# Bannerlord combat screenshot normalization — 2026-07-27

Normalized host-vision extraction of the uploaded 13-image Realm of Thrones result-screen batch.

## Coverage

- Source ZIP SHA-256: `42d4adf2e8d9f9bce0dc90945832c673aeddf81d06044cb0e6f08a2ddb852617`
- Screenshots: **13**
- Final battles: **10**
- Active scoreboard excluded: **1**
- Player-side troop observations: **143**
- Review items: **5**

## Files

- `screenshots_manifest.csv` — immutable image hashes and battle grouping.
- `screenshots.jsonl` — screenshot provenance and inclusion status.
- `battles.jsonl` — normalized battle metadata.
- `troop_occurrences.jsonl` — party, troop, and hero rows.
- `primary_troop_occurrences.jsonl` — ordinary player-side troop rows.
- `troop_battle_consolidated.jsonl` — same-label rows consolidated within battle.
- `historical_troop_aggregates.jsonl` — context and overall aggregates.
- `ranking_complete.csv` / `ranking_reliable.csv` — descriptive rankings.
- `review_queue.csv` — unresolved hero level-up icon fields.
- `normalization_summary.json`, `validation_report.json`, and `ANALYSIS_REPORT.md`.

Raw images are intentionally not committed to standard Git history; the manifest records every SHA-256.
