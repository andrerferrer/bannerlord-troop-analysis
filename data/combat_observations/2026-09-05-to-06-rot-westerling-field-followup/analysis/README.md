# Phase 2 analytical outputs

All 217 primary ordinary-troop occurrences partition into 57 cohort rows: 10 reliable and 47 below gate. Rankings keep efficiency and share-adjusted impact independent. Westerling and Joffrey are separate field-only cohorts and are never pooled.

Canonical reproduction from the repository root:

```bash
python3 data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/analysis/finalize_phase2.py
```

Add `--source-zip /absolute/path/to/source.zip` for optional raw-source/member hash verification. `generate_phase2.py` is the reused base engine; `finalize_phase2.py` applies the batch-specific historical comparison and final published layer.
