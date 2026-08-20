# Historical combat evidence reanalysis — pipeline v0.4

This reanalysis treats committed normalized bundles as immutable inputs. It does not infer player-side totals from partial troop rows and does not promote below-gate rates into the human-readable ranking.

## Status

**COMPLETE_WITH_EXTERNAL_BLOCKERS** — every reconstructible committed Phase 2 bundle was reprocessed locally in `offline-existing` mode. The remaining gaps require a valid historical archive or retained raw screenshot; they are not replaced with inferred data.

## Coverage

- Historical batches inventoried: **10**
- Historical screenshots inventoried: **66**
- Normalized archives verified and parsed: **8**
- Troop/context rows audited: **371**
- Troop/context rows with complete kill-share coverage: **258**
- Cross-batch screenshots already normalized: **2**
- Existing same-battle primary screens needing raw visual representative review: **4**

## Reliable rows under the new impact rule

| Batch | Context | Efficiency rank | Impact rank | Troop | Battles | Deployed | Kills/deployed | Player kill share | Share-adjusted impact |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|
| 2026-08-11-to-12-ravens-teeth-field-extension | field | 6 | 1 | Ravens' Teeth [T6] | 6 | 685 | 1.845 | 71.6% | 1.321 |
| 2026-08-11-to-12-ravens-teeth-field-extension | field | 20 | 14 | Westerlands Banner Knight [T6] | 5 | 30 | 0.900 | 1.7% | 0.016 |
| 2026-08-11-to-12-ravens-teeth-field-extension | field | 23 | 15 | Riverlands Cavalry [T5] | 6 | 40 | 0.825 | 1.9% | 0.015 |
| 2026-08-11-to-12-ravens-teeth-field-extension | field | 24 | 17 | Blackwood House Guard [T5] | 5 | 43 | 0.674 | 2.0% | 0.013 |

## Explicit blockers

- `archive_hash_mismatch`: 37 troop/context row(s).
- `missing_player_side_total`: 76 troop/context row(s).

Machine-readable diagnostics, including below-gate rates, are in `historical_kill_share_rankings.csv`. Screenshot decisions are in `historical_screenshot_deduplication_audit.csv`.

## Reproduce

```bash
python scripts/analysis/audit_historical_combat_evidence_v04.py \
  --data-root data/combat_observations \
  --output-dir analysis/historical_reanalysis_v04
```
