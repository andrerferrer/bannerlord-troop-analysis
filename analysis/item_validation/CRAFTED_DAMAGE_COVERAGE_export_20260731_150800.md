# Crafted-weapon damage coverage — `export_20260731_150800`

- Evidence basis: `xml_structural` (ADR-004). Empirical: `false`.
- Inputs: `data/<track>/audit/<track>_troop_equipment_audit.csv`,
  `<track>_troops.csv`, `<track>_crafted_item_pieces.csv`, and the role ladders in
  `analysis/theoretical/<track>/export_20260731_150800/role_report_*.csv`.
  All four track audits are byte-identical to their `analysis_pack/<track>/` copies
  (verified by SHA-256).
- Reproduce every number here with:

  ```bash
  python3 scripts/analysis/quantify_crafted_damage_coverage.py            # table form
  python3 scripts/analysis/quantify_crafted_damage_coverage.py --json     # machine form
  ```

- Tracks are never pooled. Every figure below is intra-track.

## The one-line statement

**Damage-derived melee and thrown rankings in this export are template-name proxies,
not damage numbers.** Not a single melee weapon in any of the four tracks carries a
real `swing_damage` or `thrust_damage` value, because every melee weapon in every
troop roster is a `CraftedItem`, and crafted-item stats were never reconstructed from
crafting pieces. `crafted_stats_reconstructed` is `False` on 100 % of crafted rows.

## Definition

A **hollow weapon slot** is an equipment row where:

- `slot` starts with `Item` (`Item0`…`Item4`, i.e. a weapon slot), and
- `item_kind == "CraftedItem"`, and
- both `swing_damage` and `thrust_damage` are blank.

Nothing downstream can read a real melee or thrown damage number out of such a row.

## Size of the hole, per track

| track | weapon-slot rows | crafted rows | **hollow rows** | hollow share | direct (non-crafted) melee rows | distinct crafted items | crafting templates |
|---|---:|---:|---:|---:|---:|---:|---:|
| `vanilla` | 6,001 | 3,619 | **3,619** | 60.3 % | **0** | 308 | 12 |
| `nightmare_sails` | 6,178 | 3,723 | **3,723** | 60.3 % | **0** | 370 | 12 |
| `realm_of_thrones` | 15,616 | 9,648 | **9,648** | 61.8 % | **0** | 409 | 13 |
| `taom` | 11,607 | 6,663 | **6,663** | 57.4 % | **0** | 545 | 12 |

Row counts here are over **every** troop in the audit, not only filtered soldiers, so they
are larger than the soldier-filtered figures quoted in
`analysis/theoretical/export_20260731_150800_CROSS_TRACK_INDEX.md` §2.1 (e.g. 9,648 vs
3,501 for `realm_of_thrones`). Both describe the same defect at different scopes; the
troop-level and ladder-level tables below are the ones that bound the analytical impact.

The `direct (non-crafted) melee rows` column is the sharpest fact in this document:
across all four tracks there are **zero** `<Item>`-defined `OneHandedWeapon`,
`TwoHandedWeapon`, or `Polearm` rows in any troop weapon slot. Bows, crossbows,
arrows, bolts, shields, sling stones and a small number of `Thrown` items are direct
items with real stats; **all** melee is crafted, therefore **all** melee damage is
hollow. There is no partially-good melee subset to fall back on.

### Troops affected

Denominator is `is_soldier == true` in `<track>_troops.csv` (the raw soldier universe,
before the multiplayer/obsolete filter that SCHEMA.md describes).

| track | soldiers | soldiers with ≥1 hollow slot | share | with hollow **melee** | with hollow **thrown** | with a real direct-thrown item |
|---|---:|---:|---:|---:|---:|---:|
| `vanilla` | 367 | **367** | 100.0 % | 367 | 48 | 3 |
| `nightmare_sails` | 371 | **371** | 100.0 % | 371 | 56 | 2 |
| `realm_of_thrones` | 1,232 | **1,232** | 100.0 % | 1,232 | 115 | 3 |
| `taom` | 1,239 | **1,205** | 97.3 % | 1,205 | 124 | 17 |

The 34 TAOM soldiers outside the hollow set are not healthy rows — they are soldiers
with no resolved weapon-slot rows at all (22 have no weapon row; 12 more have weapon
rows that resolved to no crafted item).

### Hollow rows by proxy class

Class assignment mirrors `crafted_class()` in `scripts/scoring/generate_vanilla_role_scores.py`.

| class | vanilla | nightmare_sails | realm_of_thrones | taom |
|---|---:|---:|---:|---:|
| `one_handed_sword` | 1,298 | 1,264 | 4,445 | 2,545 |
| `axe` | 888 | 969 | 1,802 | 1,456 |
| `two_handed_polearm` | 762 | 726 | 2,100 | 1,528 |
| `javelin` | 328 | 356 | 543 | 465 |
| `mace` | 240 | 236 | 530 | 427 |
| `two_handed_sword` | 56 | 88 | 149 | 159 |
| `throwing` | 35 | 68 | 41 | 35 |
| `other` | 12 | 16 | 38 | 48 |

## What the proxy actually is

`role_scores_v1` fills the hole with a substring match on the crafting-template **name**:

```
crafted_melee_raw = melee_proxy(template) * melee_usability(template)
```

Both are 9-entry lookup tables keyed on a token found in the template id
(`scripts/scoring/generate_vanilla_role_scores.py`, lines 42–90). Consequences measured
on this export:

1. **The melee axis has 6 distinct values.** Before normalisation,
   `crafted_melee_raw` takes exactly six values in **every** track:
   `{30.00, 38.70, 40.48, 41.80, 45.24, 55.20}`. 3,619–9,648 hollow rows collapse onto
   six numbers. Blade tier, length, weight, piece composition and `scale_factor` — all
   present in the XML — contribute nothing.
2. **Template → class mapping is coarse and, in two places, wrong.**
   `ThrowingAxe` and `ROT_ThrowingAxe` are classified `axe` (a melee class) because the
   `"Axe"` token is tested before `"Throwing"`. `Pike` and `Dagger` both fall through to
   `other`, so a pike and a dagger receive the identical melee value of 30.00 — the
   lowest bucket in the table.
3. **Length, speed and damage type are absent, not approximated.** Reach, swing speed
   and `Cut`/`Pierce`/`Blunt` never enter any melee term, although SCHEMA.md warns that
   damage type interacts with armor.

## Share of each track's role ladders affected

`entries` are the rows in `analysis/theoretical/<track>/export_20260731_150800/role_report_<role>.csv`.
`hollow` counts entries whose `troop_id` owns at least one hollow weapon slot.
`top-50` is the first 50 ranked rows (or all of them when the ladder is shorter).

### `vanilla`

| role ladder | entries | hollow | share | top-50 hollow |
|---|---:|---:|---:|---:|
| `archer` | 38 | 38 | 100 % | 38 / 38 |
| `crossbow` | 11 | 11 | 100 % | 11 / 11 |
| `horse_archer` | 19 | 19 | 100 % | 19 / 19 |
| `line_infantry` | 90 | 90 | 100 % | **50 / 50** |
| `shock_cavalry` | 49 | 49 | 100 % | 49 / 49 |
| `shock_infantry` | 37 | 37 | 100 % | 37 / 37 |
| `thrower` | 21 | 21 | 100 % | 21 / 21 |

### `nightmare_sails`

| role ladder | entries | hollow | share | top-50 hollow |
|---|---:|---:|---:|---:|
| `archer` | 39 | 39 | 100 % | 39 / 39 |
| `crossbow` | 12 | 12 | 100 % | 12 / 12 |
| `horse_archer` | 22 | 22 | 100 % | 22 / 22 |
| `line_infantry` | 83 | 83 | 100 % | **50 / 50** |
| `shock_cavalry` | 41 | 41 | 100 % | 41 / 41 |
| `shock_infantry` | 45 | 45 | 100 % | 45 / 45 |
| `thrower` | 34 | 34 | 100 % | 34 / 34 |

### `realm_of_thrones`

| role ladder | entries | hollow | share | top-50 hollow |
|---|---:|---:|---:|---:|
| `archer` | 152 | 152 | 100 % | **50 / 50** |
| `crossbow` | 28 | 28 | 100 % | 28 / 28 |
| `horse_archer` | 4 | 4 | 100 % | 4 / 4 |
| `line_infantry` | 318 | 318 | 100 % | **50 / 50** |
| `shock_cavalry` | 162 | 162 | 100 % | **50 / 50** |
| `shock_infantry` | 155 | 155 | 100 % | **50 / 50** |
| `thrower` | 41 | 41 | 100 % | 41 / 41 |
| `unscored_ranged` | 46 | 46 | 100 % | 46 / 46 |

### `taom`

| role ladder | entries | hollow | share | top-50 hollow |
|---|---:|---:|---:|---:|
| `archer` | 158 | 148 | 93.7 % | **48 / 50** |
| `crossbow` | 32 | 32 | 100 % | 32 / 32 |
| `horse_archer` | 22 | 22 | 100 % | 22 / 22 |
| `line_infantry` | 358 | 358 | 100 % | **50 / 50** |
| `shock_cavalry` | 116 | 116 | 100 % | **50 / 50** |
| `shock_infantry` | 128 | 128 | 100 % | **50 / 50** |
| `thrower` | 90 | 90 | 100 % | **50 / 50** |

Every ladder in every track is at ≥93.7 % affected, and 27 of the 29 ladders are at
100 %. The only exception is TAOM `archer`, where 10 entries are troops with no
resolved weapon row at all — a different defect, not healthier data.

## How the hollow slot enters each score

Read off the published `role_scores_v1` formula
(`scripts/scoring/generate_vanilla_role_scores.py`, lines 228–248). This is the column
that matters for deciding which rankings are safe to quote.

| ladder | primary score column | proxy weight in that column | verdict |
|---|---|---|---|
| `shock_infantry` | `offensive_melee_role_score` | `0.70 × crafted_melee_score_base × melee_skill_factor`, and the NaN gate is `crafted_melee_item.isna()` | **proxy-driven.** The dominant term and the eligibility gate are both the template proxy. Not a damage ranking. |
| `thrower` | `skirmisher_role_score` | `0.65 × throw_score_base` where `throw_score_base = norm100(max(direct_throw_raw, crafted_throw_raw))` and `crafted_throw_raw = melee_proxy × 0.55`; plus `0.15 × crafted_melee_score_base` | **proxy-driven for most entries** — see table below. |
| `line_infantry` | `defensive_role_score` | `0.12 × crafted_melee_score_base + 0.04 × throw_score_base` | mostly real (armor, shield HP, shield armor, harness are direct-item stats); **up to 16 % of the score is proxy**, enough to reorder near-ties. |
| `shock_cavalry` | `shock_cav_index` (composite; includes `offensive_melee_role_score` and `melee_template`) | inherits the proxy through `offensive_melee_role_score` | **partly proxy-driven.** Horse stats are real; the melee contribution is not. |
| `archer`, `crossbow`, `horse_archer` | `ranged_role_score` | none — `ranged_role_score` has no crafted-melee term | **score is real** (bow/crossbow/ammo are direct items with real damage). The `melee_template` column these reports display is still a proxy label and must not be read as damage. |

### Thrower ladders: how many entries have no real thrown damage at all

An entry is proxy-driven when the troop owns no direct `Thrown` item carrying a real
damage value, so its whole throw term comes from `melee_proxy × 0.55`.

| track | thrower entries | entries with **no** real direct-thrown item | top-50 |
|---|---:|---:|---:|
| `vanilla` | 21 | 18 (85.7 %) | 18 / 21 |
| `nightmare_sails` | 34 | 33 (97.1 %) | 33 / 34 |
| `realm_of_thrones` | 41 | **41 (100 %)** | 41 / 41 |
| `taom` | 90 | 76 (84.4 %) | 46 / 50 |

## What is present and what is missing

Present in the repository, complete and usable:

- `data/<track>/audit/<track>_crafted_item_pieces.csv` — the crafted-item **composition**.
  Columns: `item_id, piece_id, piece_type, scale_factor`. Piece types are `Blade`,
  `Handle`, `Pommel`, `Guard`. Every crafted item has exactly one `Blade` and one
  `Handle`. **100 % of the crafted items referenced by troop rosters are covered** by
  this file in all four tracks (0 missing).
- 2,171 distinct `piece_id` values across the union of the four tracks
  (vanilla 1,064 / nightmare_sails 1,111 / realm_of_thrones 1,469 / taom 1,719).
- 13 distinct crafting templates across the union: `Dagger`, `Javelin`, `Mace`,
  `OneHandedAxe`, `OneHandedSword`, `Pike`, `ROT_ThrowingAxe`, `ThrowingAxe`,
  `ThrowingKnife`, `TwoHandedAxe`, `TwoHandedMace`, `TwoHandedPolearm`, `TwoHandedSword`.

Missing, and the only thing missing:

- **Per-piece stats.** There is no `length`, `weight`, `swing_damage_factor`,
  `thrust_damage_factor`, damage type, or speed factor for any piece anywhere in this
  repository. `scale_factor` is the only numeric column in the pieces file.
- **Per-template base stats.** No template-level base damage / speed / weapon class.

Both live only in `crafting_pieces*.xml` and `crafting_templates*.xml` on the Bannerlord
PC. Raw module XML is gitignored by ADR-003 and was not part of the
`bannerlord_analysis_pack_20260731.zip` transfer, which carried already-normalized
audits only.

## Status

- **Blocked.** Real reconstruction cannot be done from anything in this repository. It
  is blocked on a new PC export of `crafting_pieces*.xml` + `crafting_templates*.xml`,
  specified in [`docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md`](../../docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md).
- The consumer is written and tested and refuses to run without those inputs:
  `scripts/normalization/reconstruct_crafted_weapon_stats.py`
  (`formula_version = piece_composition_v1`, exit code 2 with a `blocked:` message).
- Until the export lands and its `piece_composition_v1` output passes an in-game
  tooltip validation gate, every melee-derived and thrown-derived ranking in
  `analysis/theoretical/*/export_20260731_150800/` must be read as a
  **template-name proxy ordering**, not a damage ordering. `role_scores_v1` already
  labels itself `role_scores_v1_conservative_not_final`; this document quantifies why.
- Writing `<track>_crafted_weapon_stats.csv` into `data/<track>/audit/` will invalidate
  `data/xml_exports/export_20260731_150800/artifact_hashes.csv`, because
  `build_xml_ssot_package_hashes.py` globs `data/<track>/audit/*.csv` and
  `run_theoretical_role_scores.py` hard-fails its preflight on any audit CSV absent from
  that manifest. Re-run the hash builder in the same change, or scoring will refuse to
  start.
