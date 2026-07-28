# Resolve canonical troop identities from local track audits

Canonical identity coverage of the 5-battle empirical baseline goes from **2/24 to 17/24** confirmed `troop_id`s, using track audits generated from the actually-installed game rather than recovered references.

## Modules and versions per track

| Track | Modules | Versions |
|---|---|---|
| `vanilla` | Native, Sandbox, SandboxCore, StoryMode | v1.4.7 |
| | NavalDLC (War Sails) | v1.2.7 |
| `realm_of_thrones` | the above baseline | v1.4.7 / v1.2.7 |
| | ROT-Core, ROT-Content, ROT-Map, ROT-Dragon | v8.1.6 |
| `rhodok_mod` | **not generated — see blocker below** | — |

Load order taken from the real `LauncherData.xml` / module dependency graph. NavalDLC is included in every track, as required.

## Audit sizes

| Track | Troops | Notes |
|---|---:|---|
| `vanilla` | 1,937 | 4,731 XML files in the snapshot manifest |
| `realm_of_thrones` | 6,187 | 5,111 XML files in the snapshot manifest |

Raw XML stays local-only per `.gitignore`; only manifests (with per-file SHA-256), audit CSVs and reports are versioned.

## Coverage before / after

| Measure | Before | After |
|---|---:|---:|
| Eligible overall labels | 24 | 24 |
| Confirmed canonical IDs | 2 | **17** |
| Track confirmed, ID unresolved | 4 | 0 |
| Ambiguous | 0 | 0 |
| Fully unresolved | 18 | 7 |

## Resolved IDs

| Observed label | Track | `troop_id` |
|---|---|---|
| Captain of the Kingsguard [T6] | realm_of_thrones | `mounted_kingsguard` |
| Celtigar Banneret [T6] | realm_of_thrones | `celtigar_banneret` |
| Baratheon Hammerknight [T6] | realm_of_thrones | `baratheon_pikeknight` *(preserved)* |
| Water Gardens Sentinel [T6] | realm_of_thrones | `garden_sentinel` |
| Queen's Man [T6] | realm_of_thrones | `dragonstone_steel_curtain` |
| Stormlands Elite Maceman [T5] | realm_of_thrones | `stormlands_crusher` |
| Dragonstone Elite Halberdier [T5] | realm_of_thrones | `dragonstone_headsman` *(preserved)* |
| Reach Flower Knight [T6] | realm_of_thrones | `reach_flower_knight` |
| Dragonstone Elite Archer [T5] | realm_of_thrones | `dragonstone_elite_archer` |
| Elite Hired Crossbow [T5] | vanilla | `western_crossbow_t5` |
| Riverlands Ranger [T5] | realm_of_thrones | `river_ranger` |
| Reach Master Archer [T5] | realm_of_thrones | `reach_master_archer` |
| Reach Horseman [T5] | realm_of_thrones | `reach_knight` |
| Stormlands Heavy Crossbowman [T5] | realm_of_thrones | `stormlands_heavy_crossbowman` |
| Dragonstone House Guard [T5] | realm_of_thrones | `dragonstone_houseguard` |
| Reach House Guard [T5] | realm_of_thrones | `reach_houseguard` |
| Imperial Naute | vanilla | `empire_marine_t5` |

Every confirmation is a unique exact normalized display-name match against a generated track audit. No fuzzy matching, no slug-to-ID conversion. Verified programmatically: all 17 `canonical_troop_id` values exist as real `troop_id`s in their declared track's audit.

## Remaining blockers (7/24)

**5 Rhodok-labelled troops** — `Rhodok Admiral Sharpshooter`, `Rhodok Sharpshooter`, `Rhodok River Guard`, `Rhodok Sarge`, `Rhodok River Hunter`.

Every one of the 87 currently installed modules plus the base game was searched for these exact strings, including every module's `ModuleData/Languages` string files. Only `Rhodok Sharpshooter` was found, and it resolves to the ordinary base-game troop `rhodok_noble_crossbowman3` — Rhodok is a vanilla culture, so this is not evidence of a distinct mod. The other four names do not exist anywhere in the installation. The module that produced these labels in the 2026-07-23 battle screens is no longer installed. Registered as a confirmed blocker rather than guessed.

**2 near-miss-only labels**, deliberately left unresolved:

- `Rhoynar Bahriyyah [T5]` — the closest candidate is `Aserai Bahriyyah` (`aserai_marine_t5`); shares one word, different culture.
- `Reaver [T4]` — the closest candidate is `Sturgian Reaver` (`sturgia_marine_t5`, level 26); shares one word, wrong tier.

Accepting either would violate the exact-match rule that the identity gate exists to enforce.

## Parser fix: incremental patch vs. wholesale replacement

`rebuild_vanilla_audit.py` treated a later same-`id` `NPCCharacter` definition as a full replacement. Bannerlord treats it as an **incremental patch**.

`NavalDLC/ModuleData/naval_characters.xml` redefines 12 land troops carrying only `id`, `culture` and an `upgrade_targets` child, purely to splice in a marine upgrade path (e.g. `imperial_veteran_infantryman` → `empire_marine_t5`). Under wholesale replacement those 12 troops silently lost their `occupation`, skills and entire equipment set, dropping out of the soldier set altogether.

`merge_npc_definition()` now applies the real semantics: attributes are patch-wins-per-key, `upgrade_targets` are **unioned** (the DLC adds a path, it does not remove vanilla ones), and other children are replaced only when the patch supplies them. The override report gains a `merged_definitions` column.

## Canonical dataset v2 — partial layer only

`analysis/empirical/2026-07-23/canonical_dataset_v2/` contains the identity join for all 43 baseline rows (24 overall + 17 field + 2 siege_attack; siege_defense still has 0 eligible labels). Contexts are kept strictly separate.

**No attribute or equipment features are joined onto any row**, including confirmed ones, because coverage is 70.8% and the gate requires 100%. Ships with `insufficient_identity_coverage.csv`, `join_report.json`, and `input_output_hashes.json`.

## Input hashes

| File | SHA-256 |
|---|---|
| `baseline_strict_player_side.csv` | `b7e8ae047c96d09c9bd5f0e989fba3592e9aecc2ffd04c852f62daefc7f96a33` |
| `vanilla_troops.csv` | `669e57b2338f90615517466dff4a1baf0b9540c02cc093124ab1c8520d363df3` |
| `realm_of_thrones_troops.csv` | `88cc5ab6c3f9a0cb0164e36a1df8a8887e6cdc900ccf7b5c718c2c522861c903` |
| `vanilla` snapshot `manifest.csv` | `17463abb2644e323c8fc44802a556b1dda37cc6f629a9e4eff863aebc28aa1f0` |
| `realm_of_thrones` snapshot `manifest.csv` | `84b51d2b20444bb6fbd1769dc5e0caf88f51e046dde7e5c562c39851a7554092` |

Full input/output hash set in `canonical_dataset_v2/input_output_hashes.json`.

## XSLT gaps

`<track>_known_gaps_xslt.csv` is included for both tracks. Every `.xslt` under a module's `ModuleData` is recorded as `known_gap_not_applied` — the audit does not apply XSLT transforms. None of the 7 unresolved labels is attributable to an XSLT gap: the Rhodok names are absent from the raw XML entirely, not transformed into existence.

## Tests

```
python -m py_compile scripts/analysis/build_canonical_identity_audit.py   # clean
python -m unittest discover -s tests                                       # 63 tests, OK
```

Also verified: `git diff --stat` against `analysis/model_versions/` is empty — **the frozen v7.1 / v7.3 models were not touched**. Tracks are never pooled, and the 5-battle / 20-deployed gate is unchanged.
