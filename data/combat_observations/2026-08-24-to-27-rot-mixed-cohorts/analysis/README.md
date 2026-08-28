# Phase 2 analytical outputs

All 339 ordinary occurrences partition into 90 cohort/context/participant rows: 28 reliable and 62 insufficient. `ranking_complete.csv` is the exact union. `ranking_reliable.csv` reranks reliable rows separately by efficiency and share-adjusted impact.

`result_splits.csv`, `battle_pressure_margin.csv`, `denominator_coverage.csv`, `focus_deep_dive.csv`, `focus_battle_rates.csv`, `canonical_identity_audit.csv`, and `cohort_compatibility.json` preserve the required boundaries and additive analysis.

Reproduce the analysis from the repository root with:

```bash
python3 data/combat_observations/2026-08-24-to-27-rot-mixed-cohorts/analysis/generate_phase2.py
```

Add `--source-zip /absolute/path/to/source.zip` to repeat optional raw ZIP and member-hash verification.
