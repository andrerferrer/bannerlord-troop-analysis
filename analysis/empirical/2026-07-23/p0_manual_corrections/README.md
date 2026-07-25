# P0 manual corrections

This directory contains 50 image-backed review records split into small CSV parts. Each part repeats the header.

- corrected rows: 28
- confirmed rows: 22
- source: exact-hash 60-screenshot ZIP
- published line endings: LF

Integrity hashes are recorded in `MANIFEST.json`.

## Reproduce the reviewed baseline

Starting from the immutable `primary_troop_occurrences.jsonl` in the verified normalized archive:

```bash
python scripts/analysis/apply_review_corrections.py \
  primary_troop_occurrences.jsonl \
  reviewed_primary_troop_occurrences.jsonl \
  --corrections analysis/empirical/2026-07-23/p0_manual_corrections/part-*.csv

python scripts/analysis/apply_troop_aliases.py \
  reviewed_primary_troop_occurrences.jsonl \
  analysis/empirical/2026-07-23/troop_aliases.csv \
  reviewed_primary_troop_occurrences_with_aliases.jsonl

python scripts/analysis/build_empirical_baseline.py \
  reviewed_primary_troop_occurrences_with_aliases.jsonl \
  baseline_strict_player_side.csv
```

The baseline builder defaults to five independent battles, 20 deployed troops, and 5,000 deterministic battle-bootstrap repetitions.
