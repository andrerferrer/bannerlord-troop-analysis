# Nightmare Sails field capture plan — 2026-07-31

> **Status: NO DATA CAPTURED YET.** This directory contains scaffolding only; it contains no battle observations, screenshots, normalized artifacts, or empirical results.

## Workflow status

| Phase | Status |
|---|---|
| Capture plan | ready |
| Raw-source retention | pending capture |
| Phase 1 normalization | not started |
| Structural validation | not started |
| Phase 2 analysis | not started |
| Final merge gate | blocked on capture, normalization, and analysis |

## Planned coverage

- Batch directory: `data/combat_observations/2026-07-31-ns-field-plan`
- Track: `nightmare_sails`
- Context: `field` only
- Evidence type: campaign battle-result screenshots and schema-v2 capture CSVs
- Pinned theoretical export: `export_20260731_150800`
- Theoretical join source: `analysis_pack/nightmare_sails/`
- Versioned identity audit: `data/nightmare_sails/audit/`
- Planned independent battles: 5
- NavalDLC/War Sails troops remain in scope; they are not test data

Do not re-export XML or rebuild the audit unless a hash mismatch against the pinned package is proven. The join must use the pinned `analysis_pack` and audit files only.

## Battle matrix

Run five separate campaign field battles, `NS-FIELD-B01` through `NS-FIELD-B05`. Before each battle, restore the player party to exactly five healthy, deployable troops of every target below (45 target troops total, plus the player character). Use no allied parties. Engage one ordinary roaming enemy party in open-field combat, play the battle manually rather than autoresolving, issue the same `F1` then `F3` charge order at battle start, and do not personally attack.

| Battle ID | Player setup | Opponent setup | Execution |
|---|---|---|---|
| `NS-FIELD-B01` | NS target package below; player party only | one ordinary roaming campaign party; record its actual composition | field, default formations, `F1` then `F3`, zero player attacks |
| `NS-FIELD-B02` | restore the same target package | a new roaming party in a new encounter | same execution |
| `NS-FIELD-B03` | restore the same target package | a new roaming party in a new encounter | same execution |
| `NS-FIELD-B04` | restore the same target package | a new roaming party in a new encounter | same execution |
| `NS-FIELD-B05` | restore the same target package | a new roaming party in a new encounter | same execution |

| Target troop | Canonical troop ID | Per battle | Planned battles | Planned deployed opportunity |
|---|---|---:|---:|---:|
| Nord Huscarl | `nord_huscarl` | 5 | 5 | 25 |
| Battanian Wildling | `battanian_wildling` | 5 | 5 | 25 |
| Imperial Elite Cataphract | `imperial_elite_cataphract` | 5 | 5 | 25 |
| Khuzait Khan's Guard | `khuzait_khans_guard` | 5 | 5 | 25 |
| Vlandian Marinier | `vlandian_marine_t5` | 5 | 5 | 25 |
| Aserai Bahriyyah | `aserai_marine_t5` | 5 | 5 | 25 |
| Battanian Skipari | `battanian_marine_t5` | 5 | 5 | 25 |
| Imperial Naute | `empire_marine_t5` | 5 | 5 | 25 |
| Sturgian Reaver | `sturgia_marine_t5` | 5 | 5 | 25 |

This matrix deepens four already observed Soldier anchors and adds the five top marine-line targets. It intentionally omits prior empirical labels whose pinned audit occupation is not `Soldier` or whose canonical identity was unresolved.

The matrix is a capture target, not evidence. Each battle must be a new encounter; do not reload or replay one encounter as another battle. A troop counts for a battle only when its result row is visible and its derived `deployed = survivors + deaths + wounded` is greater than zero. Replace wounded or missing troops before the next battle. Do not substitute troops silently; record deviations and still preserve the battle.

Enemy composition, terrain, campaign modifiers, perks, and battle outcome remain observational confounders. Record them; do not present this matrix as a controlled causal experiment.

## Display gate and boundaries

- No troop/context/side claim may be displayed until that troop has **at least 5 independent battles AND at least 20 deployed troops**.
- The battle is the independent sampling unit.
- Player and enemy sides remain separate.
- Field, siege attack, and siege defense remain separate; reject siege, raid, hideout, naval, and keep-phase screens from this batch.
- `nightmare_sails` evidence is never pooled with Realm of Thrones, vanilla/War Sails, or another track.
- Heroes are excluded from ordinary troop rankings.
- Off-screen rows are not inferred; capture every scroll page needed to show all rows.
- Provisional display-name slugs are not canonical XML IDs.
- `analysis/model_versions/` remains frozen.

## Expected future shape

The PC operator drops raw screenshots and capture CSVs under `source/` as specified in `docs/handoff/PC_BATTLE_CAPTURE_PROMPT.md`. Phase 1 later adds the root manifests, deterministic normalized bundle, review queue, validation report, and hashes. Phase 2 writes only under `review/` and `analysis/` and follows `handoff/ANALYSIS_PROMPT.md`.
