# Bannerlord combat screenshot normalization — first pass

This directory contains the first complete structural normalization of the screenshot batch `Configurações 23_07_2026 17_42_29.zip`.

> **Integrity warning (verified 2026-07-24):** the committed chunk set does not reconstruct the documented archive hash and contains overlapping/padded content. Treat the coverage below as recorded first-pass metadata, not as independently verified reconstructed records. See `reports/p0_recovery_audit.json`. No production canonical v2 dataset has been generated.

## Coverage

- Source images: **60**
- Distinct image/battle groups: **48**
- Final victory battles included in primary analysis: **42**
- Unsupported screenshots without a result table: **4**
- Active in-battle scoreboards excluded: **1**
- Keep-retreat result screens excluded: **1**
- Primary troop occurrences: **1213**
- Rows in the review queue: **756**

## Repository contents

Files available directly:

- `normalization_summary.json`: batch coverage, statuses, source ZIP hash, and context counts.
- `validation_report.json`: structural validation results.
- `combat_troop_occurrence.schema.json`: first-pass JSON Schema.
- `bundle/`: all normalized outputs stored in a reconstructible compressed archive.

The archive contains:

- `screenshots_manifest.csv`: one row for every source image, including SHA-256 and battle grouping.
- `screenshots.jsonl`: screenshot-level extraction and status.
- `battles.jsonl`: one normalized record per grouped battle/screen set.
- `troop_occurrences.jsonl`: all extracted party, troop, hero, and OCR-artifact rows with field-level provenance.
- `primary_troop_occurrences.jsonl`: ordinary troop rows from final victory screens included in primary analysis.
- `troop_battle_consolidated.jsonl`: same troop consolidated within each battle.
- `historical_troop_aggregates.jsonl`: pooled historical totals by `field`, `siege_attack`, `siege_defense`, and `overall`.
- `ranking_complete.csv` and `ranking_reliable.csv`.
- `review_queue.csv`.

See `bundle/README.md` for reconstruction commands and the expected archive SHA-256.

The supported reconstruction command is now the cross-platform Python CLI documented in `docs/combat_observations/CLI.md`; it rejects the current corrupt stream and emits deterministic forensics.

## Important limitations

This is a complete **first-pass normalization**, not a claim that every small number was read perfectly. The source UI uses small colored text over a variable game background. Uncertain OCR cells are retained with raw OCR text and per-field confidence, and affected rows are placed in `review_queue.csv` rather than silently corrected.

The original 85 MB image ZIP is **not** committed to ordinary Git history. Its SHA-256 is recorded in `normalization_summary.json`, and `screenshots_manifest.csv` records the SHA-256 of every individual screenshot.

## Primary metric

`deployed = survivors + deaths + wounded`

`historical_kills_per_deployed = total_kills / total_deployed`

`routed` is stored separately and does not enter the primary score.
