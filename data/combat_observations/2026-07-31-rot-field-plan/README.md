# Realm of Thrones field capture plan — 2026-07-31

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

- Batch directory: `data/combat_observations/2026-07-31-rot-field-plan`
- Track: `realm_of_thrones`
- Context: `field` only
- Evidence type: campaign battle-result screenshots and schema-v2 capture CSVs
- Pinned theoretical export: `export_20260731_150800`
- Theoretical join source: `analysis_pack/realm_of_thrones/`
- Versioned identity audit: `data/realm_of_thrones/audit/`
- Planned independent battles: 5
- Custom battles: not used; this repository's RoT workflow treats campaign battles as the viable empirical source

Do not re-export XML or rebuild the audit unless a hash mismatch against the pinned package is proven. The join must use the pinned `analysis_pack` and audit files only.

## Battle matrix

Run five separate campaign field battles, `ROT-FIELD-B01` through `ROT-FIELD-B05`. Before each battle, restore the player party to exactly five healthy, deployable troops of every target below (40 target troops total, plus the player character). Use no allied parties. Engage one ordinary roaming enemy party in open-field combat, play the battle manually rather than autoresolving, issue the same `F1` then `F3` charge order at battle start, and do not personally attack.

| Battle ID | Player setup | Opponent setup | Execution |
|---|---|---|---|
| `ROT-FIELD-B01` | RoT target package below; player party only | one ordinary roaming campaign party; record its actual composition | field, default formations, `F1` then `F3`, zero player attacks |
| `ROT-FIELD-B02` | restore the same target package | a new roaming party in a new encounter | same execution |
| `ROT-FIELD-B03` | restore the same target package | a new roaming party in a new encounter | same execution |
| `ROT-FIELD-B04` | restore the same target package | a new roaming party in a new encounter | same execution |
| `ROT-FIELD-B05` | restore the same target package | a new roaming party in a new encounter | same execution |

| Target troop | Canonical troop ID | Per battle | Planned battles | Planned deployed opportunity |
|---|---|---:|---:|---:|
| Ravens' Teeth | `ravens_teeth` | 5 | 5 | 25 |
| Goldenheart Warrior | `summer_master_longbowman` | 5 | 5 | 25 |
| Celtigar Banneret | `celtigar_banneret` | 5 | 5 | 25 |
| Lyseni Enforcer | `lyseni_enforcer` | 5 | 5 | 25 |
| Myrish Artisan of War | `myrish_artisan` | 5 | 5 | 25 |
| Golden Company Mahout | `golden_elite_pikeman` | 5 | 5 | 25 |
| Sarnori Spider | `sarnor_spider` | 5 | 5 | 25 |
| Baratheon Hammerknight | `baratheon_pikeknight` | 5 | 5 | 25 |

The matrix is a capture target, not evidence. Each battle must be a new encounter; do not reload or replay one encounter as another battle. A troop counts for a battle only when its result row is visible and its derived `deployed = survivors + deaths + wounded` is greater than zero. Replace wounded or missing troops before the next battle. Do not substitute troops silently; record deviations and still preserve the battle.

Enemy composition, terrain, campaign modifiers, perks, and battle outcome remain observational confounders. Record them; do not present this matrix as a controlled causal experiment.

## Display gate and boundaries

- No troop/context/side claim may be displayed until that troop has **at least 5 independent battles AND at least 20 deployed troops**.
- The battle is the independent sampling unit.
- Player and enemy sides remain separate.
- Field, siege attack, and siege defense remain separate; reject siege, raid, hideout, naval, and keep-phase screens from this batch.
- `realm_of_thrones` evidence is never pooled with Nightmare Sails, vanilla/War Sails, or another track.
- Heroes are excluded from ordinary troop rankings.
- Off-screen rows are not inferred; capture every scroll page needed to show all rows.
- Provisional display-name slugs are not canonical XML IDs.
- `analysis/model_versions/` remains frozen.

## Expected future shape

The PC operator drops raw screenshots and capture CSVs under `source/` as specified in `docs/handoff/PC_BATTLE_CAPTURE_PROMPT.md`. Phase 1 later adds the root manifests, deterministic normalized bundle, review queue, validation report, and hashes. Phase 2 writes only under `review/` and `analysis/` and follows `handoff/ANALYSIS_PROMPT.md`.
