# Phase 2 analysis prompt — Qartheen Enthroned Guardian

Continue the same pull request as the **downstream analysis role**.

## Immutable Phase 1 inputs

- `screenshots_manifest.csv`
- `source_manifest.json`
- `source_inventory.csv`
- `normalized/events.jsonl`
- `normalized/party_summaries.jsonl`
- `normalized/player_rows/index.json` plus one JSONL shard per battle under `normalized/player_rows/`
- `reports/screenshot_deduplication_audit.csv`
- `reports/unresolved_rows.csv`
- `integrity_report.json`
- deterministic bundle and member hashes under `bundle/`

Verify every hash before analysis. Do not rewrite normalized rows. Corrections, if any, belong under `reviewed/` with original and corrected values plus provenance.

## Required work

1. Analyze every visible player-side ordinary troop/context row; the focus troop is additive, not a filter.
2. Keep field and siege attack separate. Do not pool the single siege battle into the field stop decision.
3. Resolve identities only against `data/realm_of_thrones/audit/realm_of_thrones_troops.csv` pinned at SHA-256 `63ea983998e25aa0e6f8c0747bf42e44440f695bbe1fec717074e7ba64e42810`. Keep unmatched labels provisional.
4. Publish complete and reliable rankings; the display gate is 5 independent battles and 20 deployed troops.
5. Publish player-side deployment share, kill share, offensive contribution ratio, and share-adjusted impact only from unambiguous party totals.
6. For Qartheen Enthroned Guardian, publish the nine-battle field result, a leave-one-highest-rate-battle sensitivity, per-battle values, and the single siege result separately.
7. Update `data/combat_observations/test_queues/realm_of_thrones.json` in the same pull request. Close the target only if the field evidence gate and sensitivity pass. Do not invent a future target; Arryn Winged Knight remains on verification hold unless a separate historical audit resolves it.
8. Validate, self-review the latest head, mark ready, squash-merge, and verify the merge.
