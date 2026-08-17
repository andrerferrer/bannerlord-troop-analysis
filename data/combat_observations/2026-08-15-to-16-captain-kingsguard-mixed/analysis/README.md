# Phase 2 analysis outputs

Deterministic analysis for `combat_2026-08-15_to_16_captain_kingsguard_mixed` at normalization commit `5452495e30d7d3074d47acb8ea6a497d85aac5e4`.

Core rankings preserve field/siege-attack/siege-defense boundaries and the 5-battle/20-deployed gate. Supplemental outputs record exact source verification, battle-level focus rates, explicit compatibility decisions/provenance, mechanical audit facts, and the descriptive candidate ranking. `artifact_hashes.csv` covers every analysis and review artifact except itself.

Reproduce the standard core with `scripts/analysis/analyze_normalized_combat_batch.py`; the normalized archive is `captain_kingsguard_mixed_2026-08-15_to_16.tar.xz` (SHA-256 `6b16d78d32ca70ea5093431874d8a73b00e6a3b961fa2686ec8701659decbc4d`). Supplemental arithmetic is direct integer aggregation documented in `compatibility_decision.json`; no combined bootstrap or model update is performed.
