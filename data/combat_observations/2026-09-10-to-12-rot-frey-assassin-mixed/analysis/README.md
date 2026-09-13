# Phase 2 analytical outputs

All 61 ordinary occurrences partition into 27 troop/context rows: 6 reliable and 21 insufficient. `ranking_complete.csv` contains the full partition; `ranking_reliable.csv` contains only gate-passing rows and reranks them independently, so its rank numbers intentionally differ from the complete view.

The focus, sensitivity, historical comparison, result splits, denominators, pressure margins, identities, model status, and review decisions are separate auditable artifacts.

Reproduce the analysis from the repository root with:

```bash
python3 data/combat_observations/2026-09-10-to-12-rot-frey-assassin-mixed/analysis/generate_phase2.py
```
