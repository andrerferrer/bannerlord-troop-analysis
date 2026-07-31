# Soldier ROLE_REPORT — `taom` / `export_20260731_150800`

Intra-track soldier rankings for seven combat roles. Companion to `OVERVIEW.md` in this
directory, which ranks the four `role_scores_v1` axes; this report re-cuts the same pinned
data into the seven roles a player actually recruits for. `OVERVIEW.md` is **secondary
context only and is not modified by this report**.

## Labels and provenance

- Track `taom`, export `export_20260731_150800` (SSOT pin, ADR-003)
- Package digest: `fc87e360e884cc9aa4baa15e4bdd372824c1f7054b2a9acef6d8c0df3732db3b`
- `evidence_basis = xml_structural`, `empirical = false` (ADR-004)
- Model consumed as-is: `role_scores_v1`. **No scorer formula was changed or re-derived**;
  role scores are read from `taom_roster_role_scores_v1.csv` and only aggregated across
  `roster_index`. Descriptive metrics computed in this report are limited to the shock-cavalry
  index (role 6) and the audit spot-checks, and both state their formula inline.
- Sources read: `analysis_pack/taom/*.csv`, `data/taom/audit/taom_unknown_items_*.csv`, and the
  `*_role_scores_v1.csv` files in this export directory. No XML was read; no export was re-run.
- Intra-track only. **Do not compare any number here against another track.**

## Filters applied

Applied in order, to the soldier population of the pinned pack:

| # | filter | rule | rows after |
| --- | --- | --- | --- |
| 1 | soldiers only | `occupation == Soldier` (drops Lords, Wanderers, Townsfolk, Merchants, GangLeaders, CaravanGuards) | **1239** troops |
| 2 | mod content only | keep `change_type in (novo, override)` from `taom_override_report.csv`; drops untouched vanilla baseline troops the mod neither added nor overrode | **872** troops (dropped 367) |
| 3 | drop multiplayer | drop remaining `mp_*` ids — `mp_orc_rider_isengard_hero`, `mp_orc_rider_isengard_troop` (Alliance.Wargs `CharactersTest` MP test roster) | **870** troops = the primary pool |
| 4 | resolved items only | `item_found == True` on every audit row used for a descriptive metric | 0 unresolved rows remain in the primary pool |
| 5 | obsolete | no `is_obsolete` troop survives filters 2–3 in this track; no separate filename filter was needed | — |
| 6 | NavalDLC | **not excluded.** No DLC-based filter was applied at any step | — |

**Two filter choices need stating plainly.**

*Filter 2 (mod content) is deliberate and matches `OVERVIEW.md` in this directory.* TAOM is a
total conversion: the 367 untouched vanilla soldiers are mostly bypassed via party templates
rather than deleted, and pooling them with mod content crowds the ladders with troops the
player will rarely field. **Side effect worth knowing:** all 367 are `inalterado`, and that set
includes the 36 NavalDLC soldiers and 84 vanilla `mp_*` ids. So NavalDLC content is *not*
excluded as test data (invariant respected) — it lands in the untouched-vanilla bucket that
filter 2 scopes out. Nothing is silently dropped: the retained vanilla baseline
(**283** soldiers after removing `mp_*`) gets its own appendix with the best five
per role, and the full mod-content lists are in the CSV companions.

*Filter 5:* `taom_troops.csv` carries no `is_obsolete` column, so obsolescence could only be
inferred. After filters 2–3 no obsolete-only id survives, so the question is moot here rather
than answered.

## Roster aggregation — MEAN across `roster_index`

**Every number in this report is the mean across all of a troop's `roster_index` values.**
Never a sum. Per-roster values are taken from `taom_roster_role_scores_v1.csv`; audit-derived
stats are reduced per roster first (max over that roster's matching slots — e.g. best body-armor
row) and then averaged across rosters. The `n_rosters` column in every table shows how many
rosters that mean covers.

**This differs from the shipped troop-level table.** `taom_troop_role_scores_v1.csv` aggregates
by **max** across rosters — verified, not assumed: for all 1,193 (troop x role-score) pairs on
multi-roster troops, the troop-level value equals the roster max (`idx0` matches only 604,
`mean` only 354). `OVERVIEW.md` is built on that max table. **Consequence: ranks here are
legitimately different from `OVERVIEW.md` for multi-roster troops, and the difference grows with
`n_rosters`.** Mean was chosen because the game rolls a roster at spawn, so the mean is what a
recruited stack averages, while max describes only the luckiest roll. Neither is wrong; they
answer different questions, and mixing them is what would be wrong.

## Role to metric mapping

| role | population filter | ranking metric | source |
| --- | --- | --- | --- |
| shock infantry | `Infantry`, no horse, no shield | `offensive_melee_role_score` | `role_scores_v1` column |
| line infantry | `Infantry`, no horse, has shield | `defensive_role_score` | `role_scores_v1` column |
| archer | `has_bow`, no horse | `ranged_role_score` | `role_scores_v1` column |
| crossbow | `has_crossbow`, no horse | `ranged_role_score` | `role_scores_v1` column |
| thrower | `has_throwing` | `skirmisher_role_score` | `role_scores_v1` column |
| shock cavalry | `has_horse`, not `has_ranged` | `shock_cav_index` | **computed here** — formula in role 6 |
| horse archer | `has_horse` and `has_ranged` | `ranged_role_score` | `role_scores_v1` column |

`role_scores_v1` has four axes (ranged / defensive / offensive-melee / skirmisher) against seven
roles, so archer, crossbow and horse archer all read the same `ranged_role_score` column and are
separated only by population filter. Shock cavalry is the one role with no usable column at all
(`offensive_melee_role_score` saturates at 80–85 across the whole cavalry pool), so it gets an
explicit descriptive index.

## Tiers

Per role, against the best **non-outsized** score in that role (`leader`):

| tier | band |
| --- | --- |
| S | `score >= 0.90 * leader` |
| A | `score >= 0.75 * leader` |
| B | `score >= 0.55 * leader` |
| C | `score >= 0.35 * leader` |
| D | below that |

Bands are per role, so an S in a weak role is not equivalent to an S in a strong one — the
`leader` value is printed in each section for exactly that reason. **S+** = outsized units
(mumakil / war elephants / chariots / troll), excluded from the S–D ladder entirely and listed
separately at the end.

---

# Data integrity — did the Armory/Wargs fix land?

Verdict up front: **armor is fixed and solid. Melee damage is still hollow. Throwing damage is
still hollow. Warg mounts are a new, distinct defect.**

## Armor — FIXED

In the primary pool: **9,290** resolved armor rows (Head / Body / Leg / Hand / Cape),
**0** of them with a zero armor value. Across all soldier rows it is
3 zero out of 12,695. Per-slot spot-check of the top entries in
each armored role (audit CSV, max per roster then mean across rosters):

| troop_id | rosters | head | body | leg | arm | cape | shield |
| --- | --- | --- | --- | --- | --- | --- | --- |
| battlemaster_of_the_first_age | 10 | 60.0 | 70.0 | 63.0 | 43.0 | 12.0 | 9.0 |
| imladris_warden | 6 | 65.0 | 62.5 | 65.0 | 45.0 | 12.0 | 9.0 |
| erebor_noble_royal_warden | 4 | 73.8 | 60.0 | 41.5 | 27.0 | 23.0 | 1.0 |
| darkhun_ironbound | 1 | 36.0 | 56.0 | 32.0 | 28.0 | 14.0 | 15.0 |
| imladris_blademaster | 11 | 60.0 | 58.2 | 62.7 | 42.7 | 12.0 | 0.0 |
| urukhai_nazg_hai | 1 | 40.0 | 35.0 | 36.0 | 40.0 | 38.0 | 0.0 |
| gondor_da_swan_knight | 2 | 32.0 | 42.0 | 28.0 | 14.0 | 15.0 | 1.0 |
| imladris_marchwarden | 8 | 50.0 | 50.0 | 53.8 | 43.8 | 12.0 | 0.0 |
| rider_of_himring | 9 | 62.2 | 62.2 | 63.3 | 46.7 | 12.0 | 0.0 |

Plausible, differentiated, tier-consistent. The pre-fix symptom (armour averaging near zero)
is gone. `defensive_role_score` and every `armor_total` / `effective_armor` figure in this
report can be trusted.

## Melee damage — STILL HOLLOW

**Every** melee weapon in the track is `type = CraftedWeapon` / `item_kind = CraftedItem`:
4,397 soldier rows (2,740 in the primary pool), of which
**0 have any `swing_damage` or `thrust_damage`**, and
`crafted_stats_reconstructed == False` on all of them. There are zero `OneHandedWeapon` /
`TwoHandedWeapon` / `Polearm` typed rows in the whole track.

`data/taom/audit/taom_crafted_item_pieces.csv` does carry 2,660 piece rows, but only
`piece_id` / `piece_type` / `scale_factor` — no per-piece damage table — so reconstruction
cannot produce damage from what is shipped.

**What this means for reading this report:** `crafted_melee_score_base` /
`offensive_melee_role_score` / `throw_score_base` are **weapon-template-name proxies**, not
damage. In practice `crafted_melee_score_base` takes a handful of constants —
`TwoHandedSword` 100.0, `TwoHandedPolearm` 81.96, `OneHandedSword` 75.72, `TwoHandedAxe` 73.33 —
so the shock-infantry ladder ranks weapon *class* and skill, and the crafted-javelin part of the
thrower ladder is a single constant (30.46) for every entry. **The Armory/Wargs fix resolved
item existence, not crafted item stats.** Anyone reading the melee numbers as damage will be
wrong. Fixing it is a V4.4 model / export concern and explicitly out of scope here.

## Throwing damage — STILL HOLLOW

Only 21 soldier rows in the entire track carry a *direct* `Thrown` item, and all of them are
`throwing_stone` (10 thrust), `sling_wool` (25 Blunt) or `sling_braided` (45 Blunt).
`swing_damage` is empty on all 21. Every javelin is crafted, so `throw_damage` reads **0** for
14 of the 15 top-ranked throwers. See role 5.

## `unknown_items` — clean in scope

`taom_unknown_items_review_queue.csv` has **41 rows, all severity
`allowed`**, spanning 13 item ids and exactly two troops:
`mp_orc_rider_isengard_hero`, `mp_orc_rider_isengard_troop`. Both are the Alliance.Wargs `CharactersTest` MP
test roster and are removed by filter 3, so **zero unknown items touch the primary pool**
(0 rows with `item_found == False` in the pool; 41 across all soldiers).
The allowlist reason is consistent for all of them: referenced only by that MP test roster, no
`<Item>` definition shipped, crafting pieces exist. No action needed.

## Residual defect found: resolved-but-stat-less items (NOT in the review queue)

This is a **new class of hollowness the review queue does not catch**, because these items
resolve successfully (`item_found == True`) but carry a blank `type` and no stats. 578 such
soldier rows exist; **92 of them are inside the primary pool** —
44 `Horse`, 44 `HorseHarness`, 4 `Item1`.

Root cause is **load-order resolution picking a stat-less reference stub over the real
definition**:

| item_id | winner in catalog | winner stats | real definition exists in | real stats |
| --- | --- | --- | --- | --- |
| `warg_dark` | `TAOM/ModuleData/culture_marketplace/culture_marketplace_config.xml` (rank 8) | type blank, no stats | `Alliance.Wargs/ModuleData/Items/LOTR/lotr_warg.xml` | `Horse`, speed 48, maneuver 70, charge 6 |
| `warg_brown` | same TAOM marketplace config | type blank, no stats | same Alliance.Wargs file | `Horse`, speed 48, maneuver 70, charge 6 |
| `warg_albino` | same TAOM marketplace config | type blank, no stats | same Alliance.Wargs file | `Horse`, speed 48, maneuver 70, charge 8, extra HP 100 |
| `northern_round_shield` | `NavalDLC/ModuleData/items.xml` (rank 4) | type blank, no stats | `SandboxCore/ModuleData/items/shields.xml` | `Shield`, `LargeShield`, 300 HP, shield_armor 5 |

**Blast radius:** 24 warg-rider soldier troops (20 of them in the primary shock-cavalry pool)
read `horse_charge = horse_speed = horse_maneuver = 0` with a blank `mount`, and 3 troops lose
their `northern_round_shield` stats. This is the residual tail of the Wargs fix — the Wargs
module is now *readable*, but its `lotr_warg.xml` still loses the load-order contest to a
marketplace-config stub.

**Sensitivity check.** Recomputing `shock_cav_index` for the 20 affected troops with the real
Alliance.Wargs stats substituted (same formula, same divisors):

| troop_name | warg | index as published | index with real warg stats |
| --- | --- | --- | --- |
| [Gundabad] Azog's Defiler | warg_albino | 15.68 | 56.88 |
| [Isengard] Orc Warg Ravager | warg_albino | 7.27 | 48.47 |
| [Dol Guldur] Fell Ravager | warg_dark | 14.45 | 44.82 |
| [Gundabad] Pale Uruk Fang Rider | warg_dark | 13.86 | 44.23 |
| [Gundabad] Pale Uruk Wolf Rider | warg_brown | 11.59 | 41.96 |
| [Dol Guldur] Warg Ravager | warg_dark | 9.68 | 40.05 |
| [Isengard] Orc Warg-Rider Lieutenant | warg_dark | 9.55 | 39.91 |
| [Mordor] Nurn Beast Master | warg_dark | 8.64 | 39.00 |
| [Dol Guldur] Warg Rider | warg_brown | 7.41 | 37.78 |
| [Isengard] Orc Warg-Rider Enforcer | warg_dark | 7.27 | 37.64 |
| [Dol Guldur] Warg Fang | warg_dark | 7.18 | 37.55 |
| [Mordor] Nurn Warg Ravager | warg_dark | 6.36 | 36.73 |
| [Dol Guldur] Warg Tracker | warg_brown | 5.36 | 35.73 |
| [Isengard] Orc Warg Raider | warg_dark | 5.23 | 35.59 |
| [Isengard] Orc Warg-Rider Overseer | warg_brown | 5.23 | 35.59 |
| [Mordor] Nurn Warg Reaver | warg_brown | 4.32 | 34.69 |
| [Isengard] Orc Warg Rider | warg_brown | 3.41 | 33.78 |
| [Isengard] Orc Warg-Rider Scout | warg_brown | 3.41 | 33.78 |
| [Mordor] Nurn Warg Raider | warg_brown | 2.50 | 32.87 |
| [Isengard] Orc Warg Scout | warg_brown | 2.05 | 32.41 |

Corrected, the best of them (`Azog's Defiler`) would rank ~83/116 instead of 97/116, and the
group would occupy roughly ranks 83–100 rather than the bottom 20. **So the defect is real but
its ranking impact is bounded** — wargs are genuinely low-charge (6–8 vs 24–32 for a warhorse),
fast-ish, high-maneuver mounts. The published shock-cavalry table below is left uncorrected on
purpose (correcting it would mean patching the SSOT, which this task does not own); read ranks
97–116 as *unknown, probably bottom-third* rather than as measured.

**Recommended follow-up (not done here):** have the export/catalog step prefer a definition
carrying a `type` over a stat-less same-id reference when resolving load-order conflicts, and
add a `resolved_but_untyped` counter to the audit summary so this class stops hiding behind a
clean `unknown_items` queue.

---

# Roles

## 1. Shock infantry

**Population:** `default_group == Infantry` **and** `has_horse == False` **and** `has_shield == False` — foot melee with both hands free.

**Metric:** `offensive_melee_role_score` (from `role_scores_v1`, mean across `roster_index`). Drivers shown: `crafted_melee_score_base` (weapon-template proxy) x `melee_skill_factor`, with `armor_total` / `effective_armor` for survivability context.

**Pool:** 128 troops, leader = **93.09** (S 7, A 3, B 32, C 27, D 59). Full ranked list: `role_report_shock_infantry.csv`.

### Top 15

| rank | tier | troop_name | troop_id | offensive_melee_role_score | crafted_melee_score_base | melee_skill_factor | crafted_melee_template | armor_total | effective_armor | armor_audit_sum | TwoHanded | OneHanded | Polearm | Athletics | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rivendell] Imladris Blademaster | imladris_blademaster | 93.09 | 100 | 1.15 | TwoHandedSword | 325.82 | 72.3 | 235.6 | 330 | 360 | 335 | 195 | rivendell | 41 | 11 | main_or_minor_line |
| 2 | S | [Isengard] Uruk-Hai Nazg-hai | urukhai_nazg_hai | 92.4 | 100 | 1.15 | TwoHandedSword | 225 | 64.2 | 189 | 265 | 280 | 290 | 150 | isengard | 36 | 1 | main_or_minor_line |
| 3 | S | [Gondor] Calembel Heavy Swordsman | gondor_cal_heavy_swordsman | 91.08 | 100 | 1.15 | TwoHandedSword | 157 | 48.85 | 131 | 215 | 255 | 225 | 125 | gondor | 31 | 1 | main_or_minor_line |
| 4 | S | [Gondor] Calembel Sergeant | gondor_cal_sergeant | 91.08 | 100 | 1.15 | TwoHandedSword | 157 | 48.85 | 131 | 255 | 280 | 280 | 145 | gondor | 36 | 1 | main_or_minor_line |
| 5 | S | [Gondor] Calembel Vale-Knight | gondor_cal_vale_knight | 91.08 | 100 | 1.15 | TwoHandedSword | 157 | 48.85 | 131 | 295 | 320 | 315 | 165 | gondor | 41 | 1 | main_or_minor_line |
| 6 | S | [Isengard] Uruk-Hai Berserker | urukhai_berserker | 88.69 | 100 | 1.14 | TwoHandedSword | 176 | 35.1 | 136 | 225 | 240 | 250 | 130 | isengard | 31 | 1 | main_or_minor_line |
| 7 | S | [Gondor] Lamedon Hill-Warden | gondor_lam_hill_warden | 85.95 | 100 | 1.09 | TwoHandedSword | 165 | 50.45 | 139 | 215 | 240 | 240 | 125 | gondor | 31 | 1 | main_or_minor_line |
| 8 | A | [Dale] Lake-Town Hearthguard | dale_lake_town_hearthguard | 73.43 | 81.96 | 1.15 | TwoHandedPolearm | 201 | 58.75 | 169 | 222 | 235 | 260 | 125 | sturgia | 31 | 2 | main_or_minor_line |
| 9 | A | [Mirkwood] Glaivesman of Amon | mirkwood_glaivesman | 72.51 | 81.96 | 1.15 | TwoHandedPolearm | 196 | 47.95 | 146 | 340 | 355 | 375 | 220 | mirkwood | 46 | 1 | main_or_minor_line |
| 10 | A | [Mirkwood] Greenwood Woodsman | mirkwood_woodsman | 72.51 | 81.96 | 1.15 | TwoHandedPolearm | 196 | 47.95 | 146 | 320 | 350 | 340 | 205 | mirkwood | 41 | 1 | main_or_minor_line |
| 11 | B | [Gondor] Lamedon Veteran Swordman | gondor_lam_vet_swordman | 69.57 | 100 | 0.91 | TwoHandedSword | 149 | 48.45 | 123 | 160 | 200 | 160 | 105 | gondor | 26 | 1 | main_or_minor_line |
| 12 | B | [Isengard] Uruk-Hai Veteran Pikeman | urukhai_veteranpikeman | 67.41 | 75.72 | 1.15 | OneHandedSword | 220 | 63 | 184 | 225 | 225 | 265 | 130 | isengard | 31 | 1 | main_or_minor_line |
| 13 | B | [Erebor] Shield-Breaker | erebor_noble_shield_breaker | 66.65 | 73.33 | 1.15 | TwoHandedAxe | 286.5 | 82.7 | 230.9 | 310 | 335 | 305 | 170 | erebor | 41 | 4 | main_or_minor_line |
| 14 | B | [Gondor] Cair Andros Pikewarden | gondor_ca_pikewarden | 66.19 | 75.72 | 1.15 | OneHandedSword | 157 | 48.85 | 131 | 255 | 265 | 295 | 145 | gondor | 36 | 1 | main_or_minor_line |
| 15 | B | [Gondor] Cair Andros Pikeman | gondor_ca_pikeman | 66.16 | 75.72 | 1.15 | OneHandedSword | 149 | 48.45 | 123 | 215 | 225 | 255 | 125 | gondor | 31 | 1 | main_or_minor_line |

### Why these rank where they do

- **The whole ladder is decided by two inputs: which crafting template the melee weapon uses, and the melee skill factor.** `crafted_melee_score_base` takes exactly four values in the top 15 — `TwoHandedSword` = 100.0, `TwoHandedPolearm` = 81.96, `OneHandedSword` = 75.72, `TwoHandedAxe` = 73.33. There is **no real weapon damage anywhere in this track** (see the integrity section), so read this ranking as *"who carries the best weapon class and has the skills to use it"*, not as damage output.
- **Ranks 1–7 are all `TwoHandedSword` at base 100.0** and separate only on `melee_skill_factor` (1.15 cap for ranks 1–6, 1.09 for rank 7). `imladris_blademaster` leads on the skill cap plus by far the best armor in the group (`armor_total` 325.8, `effective_armor` 72.3 — audit per-slot 60/58/63/43 head/body/leg/arm).
- **Armor is the real tiebreaker the score under-weights.** `gondor_cal_heavy_swordsman` / `_sergeant` / `_vale_knight` score identically (91.08) on the same template and skill cap, yet carry only `effective_armor` 48.9 vs Imladris' 72.3. `urukhai_nazg_hai` (rank 2, 92.4) sits at 64.2.
- **`erebor_noble_shield_breaker` (rank 13, 66.65) is the clearest score/reality gap:** it has the second-best armor in the entire role (`armor_total` 286.5, `effective_armor` 82.7) and skill cap 1.15, but is dragged down purely because `TwoHandedAxe` scores 73.33 against `TwoHandedSword`'s 100.0 — a template ordering, not a measured damage difference.

### Surprises and caveats

- **Level-31 troops occupy 3 of the 7 S slots** (`gondor_cal_heavy_swordsman` 91.08, `urukhai_berserker` 88.69, `gondor_lam_hill_warden` 85.95). Because the driver is the weapon template, a tier-3 two-hander scores like a tier-5 one; upgrade depth buys skills, not weapon class.
- **`gondor_lam_vet_swordman` (rank 11, level 26)** already carries base 100.0 and only loses on `melee_skill_factor` 0.91 — the cheapest access to top-class melee in the pool.

---

## 2. Line infantry

**Population:** `default_group == Infantry` **and** `has_horse == False` **and** `has_shield == True` — shielded foot that holds a line.

**Metric:** `defensive_role_score` (from `role_scores_v1`, mean across `roster_index`). Drivers shown: `defense_score_base`, `armor_total`, `effective_armor`, plus `shield_armor` / `shield_hp` recomputed from the audit CSV (max per roster, then mean across rosters).

**Pool:** 358 troops, leader = **69.22** (S 6, A 43, B 215, C 94). Full ranked list: `role_report_line_infantry.csv`.

### Top 15

| rank | tier | troop_name | troop_id | defensive_role_score | defense_score_base | armor_total | effective_armor | armor_audit_sum | shield_armor | shield_hp | OneHanded | Athletics | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rivendell] Battlemaster of the First Age | battlemaster_of_the_first_age | 69.22 | 69.26 | 350.6 | 81.26 | 248 | 9 | 600 | 345 | 195 | rivendell | 41 | 10 | main_or_minor_line |
| 2 | S | [Rivendell] Imladris Warden | imladris_warden | 68.3 | 67.02 | 354.5 | 77.93 | 249.5 | 9 | 600 | 345 | 195 | rivendell | 41 | 6 | main_or_minor_line |
| 3 | S | [Rivendell] Imladris Nobleman | imladris_nobleman | 66.62 | 65.88 | 337.63 | 76.23 | 238.8 | 9 | 600 | 305 | 175 | rivendell | 36 | 19 | main_or_minor_line |
| 4 | S | [Erebor] Royal Warden | erebor_noble_royal_warden | 63.07 | 60.21 | 273.25 | 78.28 | 225.3 | 1 | 450 | 340 | 185 | erebor | 46 | 4 | main_or_minor_line |
| 5 | S | [Rhûn] Darkhûn Ironbound | darkhun_ironbound | 62.8 | 59.85 | 229 | 62 | 166 | 15 | 600 | 270 | 145 | khuzait | 36 | 1 | main_or_minor_line |
| 6 | S | [Erebor] Gate Warden | erebor_noble_gate_warden | 62.56 | 59.54 | 271.75 | 78.43 | 226.3 | 1 | 400 | 320 | 170 | erebor | 41 | 4 | main_or_minor_line |
| 7 | A | [Rivendell] Imladris Swordguard | imladris_swordguard | 61.95 | 59.78 | 304.17 | 67.17 | 209.7 | 9 | 600 | 280 | 155 | rivendell | 31 | 23 | main_or_minor_line |
| 8 | A | [Dol Guldur] Khamûl's Shadow-Guard | dg_khamul_shadow_guard | 61.91 | 60.67 | 253.67 | 67.52 | 182 | 14 | 450 | 345 | 187 | dolguldur | 46 | 3 | main_or_minor_line |
| 9 | A | [Rivendell] Imladris Guardsman | imladris_guardsman | 61.59 | 58.28 | 275.25 | 64.94 | 228.3 | 9 | 600 | 305 | 175 | rivendell | 36 | 8 | main_or_minor_line |
| 10 | A | [Rhûn] Dragon-Wrath Obsidian Shieldmaster | dragon_wrath_obsidian_shieldmaster | 60.9 | 57.38 | 232 | 60.55 | 167.7 | 13.3 | 566.7 | 345 | 180 | khuzait | 46 | 3 | main_or_minor_line |
| 11 | A | [Erebor] Royal Legionary | erebor_oathsworn_royal_legionary | 60.32 | 56.62 | 253.5 | 72.95 | 212.8 | 1 | 450 | 340 | 185 | erebor | 46 | 4 | main_or_minor_line |
| 12 | A | [Rhûn] Loke-Rim Gilded Shieldguard | loke_rim_gilded_shieldguard | 59.96 | 56.16 | 234.33 | 60.82 | 170 | 14 | 450 | 285 | 145 | khuzait | 36 | 3 | main_or_minor_line |
| 13 | A | [Iron Hills] Gate Warden | iron_hills_noble_gate_warden | 59.85 | 56 | 254 | 67 | 173 | 1 | 670 | 325 | 170 | erebor | 41 | 1 | main_or_minor_line |
| 14 | A | [Erebor] Legionary | erebor_oathsworn_legionary | 59.68 | 55.78 | 257.5 | 72.27 | 210.5 | 1 | 425 | 320 | 170 | erebor | 41 | 4 | main_or_minor_line |
| 15 | A | [Iron Hills] Shield-Guard | iron_hills_noble_shield_guard | 59.64 | 55.73 | 263 | 70.25 | 171 | 1 | 510 | 300 | 150 | erebor | 36 | 1 | main_or_minor_line |

### Why these rank where they do

- **This is the one role whose ranking rests on genuine, fully-populated numbers.** 9,290 armor rows in the filtered pool, **zero** with a zero armor value. `armor_total` in the top 15 spans 229–354.5 and `effective_armor` 60.6–81.3 — see the integrity section for the spot-check.
- **Rivendell wins on raw plate, Erebor wins on efficiency.** `battlemaster_of_the_first_age` (69.22) and `imladris_warden` (68.3) carry the highest per-slot armor in the track (60–65 head, 62–70 body, 63–65 leg, 43–45 arm) on a 9-armor / 600-HP shield. `erebor_noble_royal_warden` (63.07) reaches `effective_armor` 78.3 off a *lower* `armor_total` (273.3) — dwarf kit concentrates armor in head + body rather than spreading it.
- **Shield stats matter less than they look.** The Erebor / Iron Hills block (ranks 4, 6, 11, 13–15) all run `shield_armor` 1.0 with 400–670 `shield_hp`, while Rivendell runs `shield_armor` 9.0 / 600 HP and Rhûn's `darkhun_ironbound` runs 15.0 / 600. Rank order tracks body armor, not the shield.
- **`darkhun_ironbound` (rank 5, 62.8) is the outlier in kind:** the only S-tier entry with a single roster and modest armor (`armor_total` 229, per-slot 36/56/32/28), carried there by the best `shield_armor` in the top 15 (15.0) and a 600-HP shield.

### Surprises and caveats

- **`imladris_swordguard` (rank 7) and `imladris_nobleman` (rank 3) have 23 and 19 alternative rosters respectively.** Their score is a mean over that spread, so the *worst* roll is materially weaker than the table implies — high-roster-count troops carry variance the mean hides.
- **Tier-2 troops that punch far above level:** `[Ironpass] Recruit` (rank 129, level 11, 47.17), `[Rivendell] Militia Spearman` (rank 209, level 11, 41.91), `[Rivendell] Militia Veteran Spearman` (rank 30 at level 16, 55.49). Rivendell/Erebor militia get near-veteran armor at recruit level.

### S+ outsized entries excluded from this role's ladder

| troop_name | troop_id | defensive_role_score | defense_score_base | armor_total | effective_armor | armor_audit_sum | shield_armor | shield_hp | OneHanded | Athletics | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [AMordor] Armored Troll | cave_troll | 61.23 | 73.01 | 475 | 104.5 | 285 | 0.2 | 166.7 | 350 | 185 | mordor | 51 | 6 | special_or_unlinked |

---

## 3. Archer

**Population:** `has_bow == True` **and** `has_horse == False` — foot bow. Troops with a bow *and* a mount are ranked under horse archer instead, so the two lists do not overlap.

**Metric:** `ranged_role_score` (from `role_scores_v1`, mean across `roster_index`). Drivers shown: `ranged_score_base`, `ranged_damage` (bow thrust + arrow thrust), `ranged_item`, `Bow` skill, `ranged_skill_factor`.

**Pool:** 158 troops, leader = **74.53** (S 7, A 17, B 16, C 33, D 85). Full ranked list: `role_report_archer.csv`.

### Top 15

| rank | tier | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Bow | ranged_skill_factor | armor_total | has_shield | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rivendell] Imladris Marchwarden | imladris_marchwarden | 74.53 | 96.98 | 118.12 | highelf_longbowc/highelf_longbowd | 320 | 1.15 | 306.5 | False | rivendell | 41 | 8 | main_or_minor_line |
| 2 | S | [Rivendell] Imladris Marksman | imladris_marksman | 73.64 | 96.33 | 117.6 | highelf_longbowc/highelf_longbowd | 285 | 1.15 | 315 | False | rivendell | 36 | 15 | main_or_minor_line |
| 3 | S | [Rivendell] Imladris Archer | imladris_archer | 71.13 | 96.98 | 118.12 | highelf_longbowc/highelf_longbowd | 245 | 1.11 | 244 | False | rivendell | 31 | 8 | main_or_minor_line |
| 4 | S | [Mirkwood] Silvan Borderwarden | mirkwood_borderwardens | 68.36 | 91.07 | 104 | wm_mirkwood_bow_a01 | 350 | 1.15 | 246 | False | mirkwood | 46 | 1 | main_or_minor_line |
| 5 | S | [Mirkwood] Thingol's Heirs | mirkwood_thingolheir | 68.36 | 91.07 | 104 | wm_mirkwood_bow_a01 | 370 | 1.15 | 246 | False | mirkwood | 51 | 1 | main_or_minor_line |
| 6 | S | [Gondor] Lond-Galen Haven Guard | gondor_lg_haven_guard | 68.03 | 88.25 | 102 | wm_ithilien_bow_b | 280 | 1.15 | 157 | True | gondor | 41 | 1 | main_or_minor_line |
| 7 | S | [Mirkwood] Silvan Sentinels | mirkwood_sentinels | 67.82 | 91.07 | 104 | wm_mirkwood_bow_a01 | 330 | 1.15 | 230 | False | mirkwood | 41 | 1 | main_or_minor_line |
| 8 | A | [Gondor] Citadel Guard Sharpshooter | gondor_mt_sharpshooter | 64.72 | 88.25 | 102 | wm_ithilien_bow_b | 280 | 1.15 | 159 | False | gondor | 41 | 1 | main_or_minor_line |
| 9 | A | [Gondor] Blackroot Vale Shadowbow | gondor_brv_shadowbow | 64.71 | 88.25 | 102 | wm_ithilien_bow_b | 280 | 1.15 | 157 | False | gondor | 41 | 1 | main_or_minor_line |
| 10 | A | [Gondor] Ithilien Ranger | gondor_ithilien_ranger | 64.66 | 89.4 | 103.62 | wm_ithilien_bow/wm_ithilien_bow_b/wm_ithilien_bow_c | 320 | 1.15 | 93.25 | False | gondor | 51 | 8 | special_or_unlinked |
| 11 | A | [Gondor] Lond-Galen Pavise Guard | gondor_lg_pavise_guard | 62.89 | 84.92 | 96 | wm_ithilien_bow | 245 | 1.11 | 157 | True | gondor | 36 | 1 | main_or_minor_line |
| 12 | A | [Rhûn] Dragon-Wrath Obsidian Warbow | dragon_wrath_obsidian_warbow | 62.32 | 82.94 | 95 | sm_rh_drag_longbow_a | 290 | 1.15 | 236.5 | False | khuzait | 46 | 2 | main_or_minor_line |
| 13 | A | [Rhûn] Black Sun Chosen Marksman | black_sun_chosen_marksman | 61.14 | 82.94 | 95 | sm_rh_drag_longbow_a | 270 | 1.15 | 176 | False | khuzait | 41 | 1 | main_or_minor_line |
| 14 | A | [Rhûn] Dragon-Wrath Ash Marksman | dragon_wrath_ash_marksman | 60.73 | 82.94 | 95 | sm_rh_drag_longbow_a | 270 | 1.15 | 161 | False | khuzait | 41 | 2 | main_or_minor_line |
| 15 | A | [Rhûn] Loke-Rim Gilded Marksman | loke_rim_gilded_marksman | 60.52 | 88.07 | 108 | sm_rh_loke_longbow_a | 235 | 1.07 | 215.5 | False | khuzait | 36 | 2 | main_or_minor_line |

### Why these rank where they do

- **`ranged_damage` is real, resolved weapon data** — bow rows carry populated `thrust_damage` (mean 69.6, max 115 across 676 soldier bow rows) and arrow rows add 3–5. This ranking is not a proxy.
- **Bow tier caps the ceiling; skill decides placement inside it.** `highelf_longbowc/d` (118.1 damage) > `wm_mirkwood_bow_a01` (104) > `wm_ithilien_bow_b` (102) > `sm_rh_drag_longbow_a` (95). Rivendell takes ranks 1–3 on the elf longbow; Mirkwood's ranks 4, 5, 7 reach the same S band on a weaker bow purely via `Bow` 330–370 at the 1.15 skill cap.
- **`gondor_lg_haven_guard` (rank 6, 68.03) is the best-value archer in the track:** S tier on the third-best bow, and the only S entry carrying a shield (`has_shield = True`) — ranged output plus a melee-phase answer.
- **Armor separates otherwise-equal shooters.** `gondor_ithilien_ranger` (rank 10) matches Gondor's best bows and `Bow` 320 but averages `armor_total` 93.3 across 8 rosters, roughly a third of Rivendell's 244–315.

### Surprises and caveats

- **`imladris_bowman` (rank 21, level 26, 59.16)** shoots the same `highelf_longbowc/d` as the rank-1 Marchwarden — `ranged_score_base` 96.98 vs 96.98 — and loses only on skill. Cheapest access to the track's best bow.
- **`mirkwood_thingolheir` (level 51) and `mirkwood_borderwardens` (level 46) tie exactly at 68.36.** Fifteen levels of upgrade buy nothing here once both hit the 1.15 skill cap on the same bow — a flat spot in the Mirkwood archer line.

---

## 4. Crossbow

**Population:** `has_crossbow == True` **and** `has_horse == False`.

**Metric:** `ranged_role_score` (same column as archer — `role_scores_v1` does not split bow from crossbow; the split here is by the `has_crossbow` flag). Drivers shown include `Crossbow` skill so the skill-assignment problem below is visible.

**Pool:** 32 troops, leader = **57.88** (S 3, A 6, B 12, C 6, D 5). Full ranked list: `role_report_crossbow.csv`.

### Top 15

| rank | tier | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Crossbow | ranged_skill_factor | armor_total | has_shield | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Iron Hills] Veteran Sharpshooter | iron_hills_noble_veteran_sharpshooter | 57.88 | 100 | 138 | sm_dwarf_iron_crossbow_heavy_b | 45 | 0.93 | 210 | False | erebor | 31 | 1 | main_or_minor_line |
| 2 | S | [Ironpass] Sharpshooter | ironpass_sharpshooter | 57.64 | 80 | 110.4 | sm_dwarf_iron_crossbow_heavy_b | 40 | 0.93 | 204.6 | False | erebor | 31 | 5 | main_or_minor_line |
| 3 | S | [Gondor] Tolfalas Sharpshooter | gondor_tol_sharpshooter | 57.59 | 82.36 | 103 | crossbow_f | 50 | 1.11 | 157 | False | gondor | 36 | 1 | main_or_minor_line |
| 4 | A | [Rhûn] Sagarûn Storm Marked Arbalest | sagarun_storm_marked_arbalest | 51.52 | 76.42 | 96 | crossbow_d | 235 | 1.07 | 203 | False | khuzait | 36 | 2 | main_or_minor_line |
| 5 | A | [Dale] Dalian Royal Crossbowman | dale_master_crossbowman | 50.66 | 77.79 | 102 | crossbow_f | 217 | 0.99 | 203 | True | sturgia | 31 | 2 | main_or_minor_line |
| 6 | A | [Isengard] Uruk-Hai Veteran Crossbowman | urukhai_veterancrossbowman | 45.71 | 79.95 | 105 | wm_isengard_crossbow_a01 | 205 | 0.93 | 192 | False | isengard | 31 | 1 | main_or_minor_line |
| 7 | A | [Ironpass] Veteran Arbalest | ironpass_veteran_arbalest | 45.22 | 77.87 | 106.4 | sm_dwarf_iron_crossbow_heavy_a/sm_dwarf_iron_crossbow_heavy_b | 170 | 0.77 | 202.4 | False | erebor | 26 | 5 | main_or_minor_line |
| 8 | A | [Dunland] Draig-lûth Sharpshooter | dunland_dragon_sniper | 44.41 | 74.14 | 96 | crossbow_d | 40 | 0.93 | 160 | True | empire | 31 | 1 | main_or_minor_line |
| 9 | A | [Iron Hills] Sharpshooter | iron_hills_noble_sharpshooter | 43.58 | 94.67 | 128 | sm_dwarf_iron_crossbow_heavy_a | 40 | 0.77 | 191 | False | erebor | 26 | 1 | main_or_minor_line |
| 10 | B | [Rhûn] Sagarûn Arbalest | sagarun_arbalest | 39.91 | 74.82 | 94 | crossbow_c | 195 | 0.89 | 160.5 | False | khuzait | 31 | 2 | main_or_minor_line |
| 11 | B | [Gondor] Lond-Galen Pavise Crossbowman | gondor_lg_pavise_crossbowman | 39.67 | 71.07 | 82 | crossbow_e | 205 | 0.93 | 157 | False | gondor | 31 | 1 | main_or_minor_line |
| 12 | B | [Gondor] Tolfalas Marksman | gondor_tol_marksman | 39.67 | 71.07 | 82 | crossbow_e | 40 | 0.93 | 157 | False | gondor | 31 | 1 | main_or_minor_line |
| 13 | B | [Mordor] Black Uruk Heavy Crossbow | mordor_uruk_heavy_crossbow | 38.86 | 72.03 | 93 | crossbow_c | 205 | 0.93 | 180 | False | mordor | 31 | 1 | main_or_minor_line |
| 14 | B | [Dunland] Draig-lûth Firebolt | dunland_dragon_firebolt | 38.39 | 79.31 | 105 | crossbow_f | 35 | 0.77 | 121 | True | empire | 26 | 1 | main_or_minor_line |
| 15 | B | [Umbar] Beruthiel's Rangers | umbar_elite_root101 | 36.58 | 66.9 | 86.4 | crossbow_f | 35 | 0.77 | 91.2 | False | umbar | 26 | 5 | main_or_minor_line |

### Why these rank where they do

- **Only 32 troops qualify, and the leader (57.88) sits well below the archer leader (74.53).** Crossbows out-damage bows per shot (`ranged_damage` up to 138 on `sm_dwarf_iron_crossbow_heavy_b` vs 118 for the elf longbow) but the role score's skill factor punishes them — see the next point.
- **Read `Crossbow` in this table before trusting the order.** Ranks 1, 2, 3, 8, 9, 14, 15 have `Crossbow` skill of **35–50**, yet still score `ranged_skill_factor` 0.77–1.11. The scorer is evidently not gated on `Crossbow` alone, so several dwarf/Gondor entries rank on weapon damage while their nominal crossbow skill is near-untrained. This is a **model-side question for V4.4**, not something this report re-derives.
- **Erebor owns the top of the damage curve.** `sm_dwarf_iron_crossbow_heavy_b` (138) and `_heavy_a` (128) are the two hardest-hitting ranged items in the track; `iron_hills_noble_veteran_sharpshooter` (57.88) and `ironpass_sharpshooter` (57.64) take S on them at level 31.
- **`sagarun_storm_marked_arbalest` (rank 4, 51.52) is the best *coherently statted* crossbow:** `Crossbow` 235 with `crossbow_d` at 96 damage — the highest crossbow skill in the top 5 by a factor of ~5.

### Surprises and caveats

- **`iron_hills_noble_sharpshooter` (rank 9) has the second-highest `ranged_score_base` in the role (94.67, 128 damage) but lands only A**, because `ranged_skill_factor` drops to 0.77 at level 26. Weapon-limited troops rank on skill here, not on the weapon.
- **`dale_master_crossbowman` (rank 5, 50.66) is the only top-10 crossbow with a shield** — the pick if the crossbow line has to survive contact.

---

## 5. Thrower

**Population:** `has_throwing == True` (any roster carries a throwing weapon). Mounted javelin cavalry qualify here **and** under shock cavalry — the lists intentionally overlap, because in TAOM throwing is almost entirely a cavalry sideline.

**Metric:** `skirmisher_role_score` (from `role_scores_v1`, mean across `roster_index`). Drivers shown: `throw_score_base`, `throw_damage`, the resolved throw item, and `Throwing` / `throw_skill_factor`.

**Pool:** 90 troops, leader = **67.98** (S 3, A 6, B 30, C 27, D 24). Full ranked list: `role_report_thrower.csv`.

### Top 15

| rank | tier | troop_name | troop_id | skirmisher_role_score | throw_score_base | throw_damage | direct_throw_item | crafted_throw_item | Throwing | throw_skill_factor | armor_total | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rohan] Riders of Rohan | rohan_edoras_golden_hall_supreme_rider | 67.98 | 30.46 | 0 |  | eastern_javelin_3_t4 | 72 | 0.45 | 201.4 | vlandia | 41 | 5 | main_or_minor_line |
| 2 | S | [Rohan] West Emnet Heavy Shock Cavalry | rohan_westemnet_kings_own_rider | 63.4 | 30.46 | 0 |  | northern_javelin_3_t4 | 62 | 0.39 | 173 | vlandia | 36 | 1 | main_or_minor_line |
| 3 | S | [Dunland] Caru-lûth Noble Lancer | dunland_stag_noble_lancer | 63.25 | 30.46 | 0 |  | northern_javelin_3_t4 | 65 | 0.41 | 173 | empire | 31 | 1 | main_or_minor_line |
| 4 | A | [Rohan] King's Royal Guard | rohan_edoras_golden_hall_kings_own_rider | 61.1 | 30.46 | 0 |  | eastern_javelin_3_t4 | 62 | 0.39 | 193.8 | vlandia | 36 | 5 | main_or_minor_line |
| 5 | A | [Dunland] Avanc-lûth Noble Cavalry | dunland_lizard_noble_cavalry | 58.08 | 30.46 | 0 |  | northern_javelin_3_t4 | 65 | 0.41 | 173 | empire | 31 | 1 | main_or_minor_line |
| 6 | A | [Dunland] Caru-lûth Rider | dunland_stag_rider | 57.36 | 30.46 | 0 |  | northern_javelin_3_t4 | 55 | 0.34 | 147 | empire | 26 | 1 | main_or_minor_line |
| 7 | A | [Rohan] King's Knight | rohan_edoras_golden_hall_eorlingas_rider | 55.57 | 30.46 | 0 |  | eastern_javelin_3_t4 | 52 | 0.33 | 175.4 | vlandia | 31 | 5 | main_or_minor_line |
| 8 | A | [Rohan] West Emnet Shock Cavalry | rohan_westemnet_royal_rider | 54.98 | 30.46 | 0 |  | northern_javelin_3_t4 | 52 | 0.33 | 169 | vlandia | 31 | 1 | main_or_minor_line |
| 9 | A | [Umbar] Naru n'Aru Royal Guard | umbar_elite_root0000 | 52.2 | 11.51 | 2 | throwing_stone |  | 80 | 0.5 | 156 | umbar | 31 | 5 | main_or_minor_line |
| 10 | B | [Dunland] Avanc-lûth Outrider | dunland_lizard_outrider | 50.82 | 30.46 | 0 |  | northern_javelin_3_t4 | 55 | 0.34 | 152 | empire | 26 | 1 | main_or_minor_line |
| 11 | B | [Harad] Fang of the King | harad_fangking | 50.56 | 30.46 | 0 |  | eastern_javelin_3_t4 | 50 | 0.31 | 169 | aserai | 31 | 1 | main_or_minor_line |
| 12 | B | [Dunland] Caru-lûth Lancer | dunland_stag_lancer | 46.76 | 30.46 | 0 |  | northern_javelin_3_t4 | 45 | 0.28 | 129 | empire | 21 | 1 | main_or_minor_line |
| 13 | B | [Harad] Serpent Guard | harad_serpentguard | 46.68 | 30.46 | 0 |  | eastern_javelin_3_t4 | 40 | 0.25 | 183 | aserai | 26 | 1 | main_or_minor_line |
| 14 | B | [Rohan] West Emnet Medium Cavalry | rohan_westemnet_eorlingas_rider | 46.22 | 30.46 | 0 |  | northern_javelin_3_t4 | 42 | 0.26 | 122 | vlandia | 26 | 1 | main_or_minor_line |
| 15 | B | [Gondor] Pinnath Gelin Veteran Horseman | gondor_pg_vet_cavalry | 46.06 | 30.46 | 0 |  | western_javelin_3_t4 | 40 | 0.25 | 152 | gondor | 31 | 1 | main_or_minor_line |

### Why these rank where they do

- **`throw_damage` is 0 for every entry in the top 15 except one.** Ranks 1–8 and 10–15 all carry *crafted* javelins (`eastern_javelin_3_t4`, `northern_javelin_3_t4`, `western_javelin_3_t4`) whose stats are never reconstructed, so `throw_score_base` is pinned at the template constant **30.46** for all of them. Only 21 soldier rows in the whole track carry a *direct* `Thrown` item, and those are `throwing_stone` (10 thrust) and slings (`sling_wool` 25 Blunt, `sling_braided` 45 Blunt).
- **Consequence: ranks 1–8 and 10–15 are ordered by `Throwing` skill alone.** `throw_score_base` is identical (30.46) down the list; `throw_skill_factor` runs 0.45 → 0.25 and reproduces the rank order exactly. `rohan_edoras_golden_hall_supreme_rider` leads on `Throwing` 72, nothing else.
- **`umbar_elite_root0000` (rank 9, 52.20) is the only entry scored on real throw data** — `throwing_stone`, `throw_damage` 2 (mean over 5 rosters, most of which have no throw item), `throw_score_base` 11.51, rescued to A tier by the highest `Throwing` in the top 15 (80). It ranks *below* javelin cavalry that have no measured damage at all.
- **The role is a cavalry role in this track.** Every S/A entry except `umbar_elite_root0000` is a Rohan, Dunland or Harad horseman; there is no dedicated foot skirmisher line near the top.

### Surprises and caveats

- **`harad_noble` / "Youngblood of the Serpent" (rank 18, level 11) scores 45.78** — within 68% of the leader at a fifth of the level, because the template constant does not scale with tier and only skill separates entries.
- **Low absolute confidence:** given the above, treat this table as a `Throwing`-skill ranking with an availability filter, not as a skirmisher damage ranking. It is the weakest-evidence role in this report.

---

## 6. Shock cavalry

**Population:** `has_horse == True` **and** `has_ranged == False` — melee cavalry. Horse archers are excluded by construction and ranked in role 7.

**Metric:** **No `role_scores_v1` column covers this role**, so a descriptive index is computed here from the audit CSV. Exact formula, applied per `roster_index` then averaged across rosters:

```
mount stats per roster = max(horse_charge_damage), max(horse_speed),
                         max(horse_maneuver), max(horse_extra_health)
                         over that roster's Horse rows with item_found == True

N(x, m) = 100 * x / m          # m = max of that stat over the NON-outsized cavalry pool

shock_cav_index = 0.40 * N(horse_charge_damage, 32.0)
                + 0.20 * N(horse_speed,         68.0)
                + 0.10 * N(horse_maneuver,      80.0)
                + 0.10 * N(horse_extra_health, 120.0)
                + 0.20 * N(Polearm skill,      440.0)
```

Weights are a stated editorial choice (charge dominant, then speed, then a lance-skill term); the four `m` divisors are the observed maxima printed above and are held fixed so the index is reproducible. `has_lance` is `True` when any roster's melee crafting template contains `Polearm`. **This index is descriptive and intra-track only — it is not a `role_scores_v1` score and must not be pooled with one.**

**Pool:** 116 troops, leader = **88.84** (S 10, A 41, B 43, C 2, D 20). Full ranked list: `role_report_shock_cavalry.csv`.

### Top 15

| rank | tier | troop_name | troop_id | shock_cav_index | horse_charge | horse_speed | horse_maneuver | horse_hp | mount | has_lance | Polearm | Riding | armor_total | effective_armor | defensive_role_score | offensive_melee_role_score | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rohan] West Emnet Heavy Shock Cavalry | rohan_westemnet_kings_own_rider | 88.84 | 32 | 68 | 78 | 60 | noble_horse_southern/t3_vlandia_horse | True | 310 | 290 | 173 | 55.15 | 77.07 | 82.2 | vlandia | 36 | 1 | main_or_minor_line |
| 2 | S | [Gondor] Swan Knight | gondor_da_swan_knight | 85.41 | 31 | 62 | 71 | 30 | noble_horse_imperial | True | 375 | 365 | 157 | 48.85 | 65.96 | 80.58 | gondor | 46 | 2 | main_or_minor_line |
| 3 | S | [Rivendell] Imladris Outrider | imladris_outrider | 85.18 | 32 | 49 | 68 | 60 | t3_vlandia_horse | True | 380 | 350 | 259 | 62.5 | 81.3 | 83.12 | rivendell | 41 | 8 | main_or_minor_line |
| 4 | S | [Gondor] Dol Amroth Veteran Knight | gondor_da_vet_knight | 84.04 | 31 | 62 | 71 | 30 | noble_horse_imperial | True | 345 | 325 | 157 | 48.85 | 65.41 | 80.48 | gondor | 41 | 1 | main_or_minor_line |
| 5 | S | [Rivendell] High Captain | rivendell_high_captain | 82.25 | 24 | 68 | 78 | 30 | noble_horse_southern | True | 440 | 430 | 337.29 | 78.73 | 89.49 | 84.48 | rivendell | 51 | 7 | main_or_minor_line |
| 6 | S | [Rivendell] Rochannon Elenath | rivendell_glorfindel_guard | 82.25 | 24 | 68 | 78 | 30 | noble_horse_southern | True | 440 | 430 | 205 | 51.2 | 80.48 | 82.98 | rivendell | 51 | 32 | main_or_minor_line |
| 7 | S | [Gondor] Dol Amroth Knight | gondor_da_knight | 82.23 | 31 | 62 | 71 | 30 | noble_horse_imperial | True | 305 | 275 | 157 | 48.85 | 65.03 | 80.42 | gondor | 36 | 1 | main_or_minor_line |
| 8 | S | [Rivendell] Nõldorin Lancer | noldorin_lancer | 81.57 | 24 | 68 | 78 | 30 | noble_horse_southern | True | 425 | 390 | 338.58 | 77.27 | 93.94 | 85.22 | rivendell | 46 | 12 | main_or_minor_line |
| 9 | S | [Rivendell] Royal Knight | rivendell_royal_knight | 80.89 | 24 | 68 | 78 | 30 | noble_horse_southern | True | 410 | 390 | 338.67 | 72.38 | 86.21 | 83.94 | rivendell | 46 | 6 | main_or_minor_line |
| 10 | S | [Mirkwood] Mirkwood Béleglas | mirkwood_beleglas | 80.43 | 24 | 68 | 78 | 30 | noble_horse_southern | True | 400 | 365 | 246 | 66.85 | 83.15 | 83.43 | mirkwood | 46 | 1 | main_or_minor_line |
| 11 | A | [Gondor] Dol Amroth Cavalry | gondor_da_cavalry | 79.95 | 31 | 62 | 71 | 30 | noble_horse_imperial | True | 255 | 215 | 157 | 48.85 | 65.03 | 80.42 | gondor | 31 | 1 | main_or_minor_line |
| 12 | A | [Rivendell] Royal Guard | rivendell_royal_guard | 79.52 | 24 | 68 | 78 | 30 | noble_horse_southern | True | 380 | 350 | 319.5 | 70.39 | 90.57 | 84.66 | rivendell | 41 | 8 | main_or_minor_line |
| 13 | A | [Mirkwood] Mirkwood Róchenlas | mirkwood_rochenlas | 79.07 | 24 | 68 | 78 | 30 | noble_horse_southern | True | 370 | 325 | 246 | 66.85 | 83.15 | 83.43 | mirkwood | 41 | 1 | main_or_minor_line |
| 14 | A | [Rohan] King's Lancer | rohan_edoras_golden_hall_elite_rider | 78.89 | 31 | 56 | 76 | 50 | noble_horse_northern | True | 220 | 180 | 139.6 | 40.93 | 63.72 | 69.24 | vlandia | 26 | 5 | main_or_minor_line |
| 15 | A | [Rohan] Riders of Rohan | rohan_edoras_golden_hall_supreme_rider | 78.16 | 24 | 68 | 78 | 30 | noble_horse_southern | True | 350 | 340 | 201.4 | 55.94 | 76.65 | 82.14 | vlandia | 41 | 5 | main_or_minor_line |

### Why these rank where they do

- **Mount charge is the axis.** Only three non-outsized charge values reach the top: `noble_horse` 35, `t3_vlandia_horse` 32, `noble_horse_imperial` 31. `rohan_westemnet_kings_own_rider` (88.84) takes rank 1 by pairing the 32-charge Destrier with the best mobility pair in the pool (speed 68 / maneuver 78) and `Polearm` 310.
- **Rivendell trades charge for mobility and armor.** Ranks 5, 6, 8, 9 all ride `noble_horse_southern` at charge **24** — below Gondor's 31 — but recover through speed 68 / maneuver 78 and `Polearm` 400–440. `rivendell_high_captain` also carries the best armor in the role (`armor_total` 337.3, `effective_armor` 78.7).
- **Gondor's Dol Amroth line is the most consistent block:** ranks 2, 4, 7, 11 are the same `noble_horse_imperial` (31/62/71) with `Polearm` scaling 255 → 375 by level. Armor is flat at `armor_total` 157 / `effective_armor` 48.9 — glassier than Rivendell for the same index band.
- **Every top-15 entry has `has_lance = True`,** so the lance flag does not discriminate at the top; it matters in the tail.
- **`offensive_melee_role_score` is shown as a secondary column and is nearly useless here** (80.4–85.2 across the whole top 15) — the crafted-template proxy saturates on cavalry, which is another reason this role needed its own index.

### Surprises and caveats

- **Twenty warg-rider troops (ranks 97–116, all D) are ranked on a data defect, not on their mounts.** Their `horse_charge`/`speed`/`maneuver` all read 0 and `mount` is blank, because `warg_dark` / `warg_brown` / `warg_albino` resolve to a stat-less stub. Full detail and a corrected sensitivity table in the integrity section — corrected, they move to roughly ranks 83–100, i.e. still bottom-third but no longer the floor.
- **Tier-2 Rohan is startlingly good:** `[Rohan] East Emnet Lance Rider` (rank 29, level 11, 71.78) and `[Rohan] West Emnet Rider` (rank 33, level 11, 71.09) reach 80% of the leader's index at level 11, because mount charge does not scale with troop tier.

### S+ outsized entries excluded from this role's ladder

| troop_name | troop_id | shock_cav_index | horse_charge | horse_speed | horse_maneuver | horse_hp | mount | has_lance | Polearm | Riding | armor_total | effective_armor | defensive_role_score | offensive_melee_role_score | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Aharad] Mumakil Rider | harad_mumakil_rider | 269.37 | 200 | 5 | 5 | 0 | taom_mumakil | True | 380 | 385 | 71 | 17.4 | 40.34 | 78.45 | aserai | 51 | 1 | special_or_unlinked |
| [Aharad] Elephant Rider | harad_elephant_rider | 177.71 | 125 | 10 | 10 | 0 | taom_war_elephant | True | 380 | 385 | 71 | 17.4 | 47.67 | 79.66 | aserai | 51 | 1 | special_or_unlinked |
| [Rhûn] Wainrider Warlord Chariot | wainrider_warlord_chariot | 149.3 | 90 | 55 | 25 | 0 | taom_chariot_a | True | 385 | 378 | 218 | 58.2 | 76.75 | 82.37 | khuzait | 46 | 1 | main_or_minor_line |
| [ARhûn] Wainrider Swift-Chariot | wainrider_swift_chariot | 147.94 | 90 | 55 | 25 | 0 | taom_chariot_a | True | 355 | 338 | 209 | 55.85 | 75.54 | 82.17 | khuzait | 41 | 1 | main_or_minor_line |

---

## 7. Horse archer

**Population:** `has_horse == True` **and** `has_ranged == True` — mounted shooters, whether bow or crossbow.

**Metric:** `ranged_role_score` (from `role_scores_v1`, mean across `roster_index`). Drivers shown: `ranged_score_base`, `ranged_damage`, `Riding`, `mobility_factor`, plus `horse_speed` / `horse_maneuver` / `mount` recomputed from the audit CSV.

**Pool:** 22 troops, leader = **97.35** (S 2, B 5, C 7, D 8). Full ranked list: `role_report_horse_archer.csv`.

### Top 15

| rank | tier | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Bow | Crossbow | Riding | mobility_factor | horse_speed | horse_maneuver | mount | armor_total | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | [Rivendell] Rider of Himring | rider_of_himring | 97.35 | 96.83 | 118 | highelf_longbowc/highelf_longbowd | 385 | 85 | 410 | 1.25 | 68 | 78 | noble_horse_southern | 342.33 | rivendell | 46 | 9 | main_or_minor_line |
| 2 | S | [Rivendell] Imladris Horse Archer | imladris_horse_archer | 96.97 | 97.18 | 118.29 | highelf_longbowc/highelf_longbowd | 360 | 80 | 380 | 1.25 | 49 | 68 | t3_vlandia_horse | 280.43 | rivendell | 41 | 7 | main_or_minor_line |
| 3 | B | [Rohan] Éothéod Horse Archer | rohan_wold_kings_own_horse_archer | 63.37 | 59.47 | 58 | steppe_war_bow | 285 | 25 | 330 | 1.25 | 68 | 78 | noble_horse_southern | 165 | vlandia | 36 | 1 | main_or_minor_line |
| 4 | B | [Rhûn] Kharaghûl Karash Keshig | kharaghul_karash_keshig | 62.26 | 62.13 | 57 | steppe_war_bow | 280 | 25 | 328 | 1.25 | 65 | 73 | t3_aserai_horse | 186 | khuzait | 36 | 1 | main_or_minor_line |
| 5 | B | [Rohan] Wold Eorlingas Horse Archer | rohan_wold_eorlingas_horse_archer | 59.28 | 59.47 | 58 | steppe_war_bow | 240 | 20 | 275 | 1.25 | 65 | 73 | t3_aserai_horse | 130 | vlandia | 31 | 1 | main_or_minor_line |
| 6 | B | [Rhûn] Kharaghûl Keshig | kharaghul_keshig | 57.95 | 62.13 | 57 | steppe_war_bow | 235 | 20 | 273 | 1.25 | 65 | 73 | t3_aserai_horse | 184 | khuzait | 31 | 1 | main_or_minor_line |
| 7 | B | [Rhûn] Balcoth Farshot Horse Archer | balcoth_farshot_horse_archer | 57.79 | 62.13 | 57 | steppe_war_bow | 235 | 20 | 273 | 1.25 | 65 | 73 | t3_aserai_horse | 176 | khuzait | 31 | 1 | main_or_minor_line |
| 8 | C | [Harad] Serpent Archer | harad_serpenthorsearcher | 49.16 | 60.43 | 54 | composite_steppe_bow | 205 | 25 | 215 | 1.25 | 47 | 69 | t2_khuzait_horse | 183 | aserai | 26 | 1 | main_or_minor_line |
| 9 | C | [Rohan] Wold Elite Horse Rider | rohan_wold_elite_horse_archer | 48.06 | 59.47 | 58 | steppe_war_bow | 190 | 15 | 220 | 1.25 | 59 | 66 | t3_empire_horse | 129 | vlandia | 26 | 1 | main_or_minor_line |
| 10 | C | [Rhûn] Kharaghûl Horse Archer | kharaghul_horse_archer | 44.61 | 60.94 | 55 | composite_steppe_bow | 185 | 15 | 218 | 1.25 | 65 | 73 | t3_aserai_horse | 146 | khuzait | 26 | 1 | main_or_minor_line |
| 11 | C | [Rhûn] Balcoth Horse Archer | balcoth_horse_archer | 44.59 | 60.94 | 55 | composite_steppe_bow | 185 | 15 | 218 | 1.25 | 65 | 73 | t3_aserai_horse | 140 | khuzait | 26 | 1 | main_or_minor_line |
| 12 | C | [Gundabad] Despoiler of the Vale | gundabad_despoiler_of_the_vale | 43.24 | 60.43 | 54 | composite_steppe_bow | 185 | 15 | 195 | 1.25 | 0 | 0 |  | 180 | gundabad | 26 | 6 | main_or_minor_line |
| 13 | C | [Harad] Rider of the Golden Veil | harad_horsearcher | 37.2 | 60.43 | 54 | composite_steppe_bow | 155 | 20 | 165 | 1.25 | 47 | 69 | t2_khuzait_horse | 158 | aserai | 21 | 1 | main_or_minor_line |
| 14 | C | [Rohan] Wold Veteran Horse Rider | rohan_wold_veteran_horse_archer | 35.95 | 58.27 | 56 | composite_steppe_bow | 140 | 10 | 170 | 1.25 | 56 | 76 | noble_horse_northern | 106 | vlandia | 21 | 1 | main_or_minor_line |
| 15 | D | [Rhûn] Kharaghûl Horse Scout | kharaghul_horse_scout | 31.05 | 57.21 | 55 | steppe_heavy_bow | 135 | 10 | 168 | 1.25 | 65 | 73 | t3_aserai_horse | 144 | khuzait | 21 | 1 | main_or_minor_line |

### Why these rank where they do

- **A two-troop role, then a cliff.** `rider_of_himring` (97.35) and `imladris_horse_archer` (96.97) are S; rank 3 drops to 63.37. The gap is `ranged_damage` 118 (elf longbow) against 54–58 (`steppe_war_bow` / `composite_steppe_bow`) — a 2x weapon advantage that nothing in the rest of the pool closes.
- **`mobility_factor` is saturated at 1.25 for the entire top 15,** so mobility contributes nothing to the ordering. Rank order is `ranged_score_base` x `ranged_skill_factor`, i.e. bow tier then `Bow` skill.
- **Only 22 troops qualify** — TAOM is not a horse-archer-heavy track. Rohan (6) and Rhûn/Khuzait (6) supply most of the body of the list on vanilla steppe bows.
- **`rider_of_himring` also has the best mount in the role** (`noble_horse_southern`, speed 68 / maneuver 78) *and* the best armor (`armor_total` 342.3) — it is the unambiguous best mounted shooter in the track on every visible axis.

### Surprises and caveats

- **`gundabad_despoiler_of_the_vale` (rank 12) shows `horse_speed` 0, `horse_maneuver` 0 and a blank `mount`** while still satisfying `has_horse == True`. Same warg stub defect as in shock cavalry — its `ranged_role_score` is unaffected (mobility is saturated anyway) but its mobility columns are not usable.
- **`rohan_wold_kings_own_horse_archer` (rank 3, 63.37) is the only non-elf entry above 63** and carries a shield — the practical pick once Rivendell is unavailable.

---

# S+ outliers — outsized units

Detected structurally, not by name matching: a troop is outsized if any roster mounts
`taom_mumakil`, `taom_war_elephant` or `taom_chariot_a`, plus `cave_troll` (a foot unit of
outsized scale). Detected set: `cave_troll`, `harad_elephant_rider`, `harad_mumakil_rider`, `wainrider_swift_chariot`, `wainrider_warlord_chariot`.

**These are excluded from every S–D ladder above** and carry no `rank` / `tier`. They are not
comparable to ordinary troops: `taom_mumakil` has charge 200 / speed 5 / maneuver 5 and
`taom_war_elephant` charge 125 / speed 10 — a shock index three times the best warhorse's,
paired with mobility no line unit has to respect. Ranking them alongside cavalry would
mis-describe both.

| troop_id | troop_name | culture | level | mount | charge / speed / maneuver | shock_cav_index (info only) | armor_total | effective_armor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| harad_mumakil_rider | [Aharad] Mumakil Rider | aserai | 51 | taom_mumakil | 200 / 5 / 5 | 269.37 | 71 | 17.4 |
| harad_elephant_rider | [Aharad] Elephant Rider | aserai | 51 | taom_war_elephant | 125 / 10 / 10 | 177.71 | 71 | 17.4 |
| wainrider_warlord_chariot | [Rhûn] Wainrider Warlord Chariot | khuzait | 46 | taom_chariot_a | 90 / 55 / 25 | 149.30 | 218 | 58.2 |
| wainrider_swift_chariot | [ARhûn] Wainrider Swift-Chariot | khuzait | 41 | taom_chariot_a | 90 / 55 / 25 | 147.94 | 209 | 55.85 |
| cave_troll | [AMordor] Armored Troll | mordor | 51 | — (foot) | — | — | 475 | 104.5 |

Notes: the chariots are the only outsized units that are also *mobile* (speed 55), which makes
them the most disruptive of the five in practice. `cave_troll` would have placed 8th in line
infantry (`defensive_role_score` 61.23) on `armor_total` 475 / `effective_armor` 104.5 — both
well past the ordinary ceiling of 354.5 / 81.3 — which is exactly why it is parked here.

---

# Appendix — retained vanilla baseline (best five per role)

Filter 2 scopes the main ladders to mod content. For completeness, the same metrics over the
**283** retained untouched-vanilla soldiers (`change_type = inalterado`, `mp_*` removed,
**NavalDLC included**). Ranks/tiers below are computed within this baseline pool only and are
**not comparable** to the main tables.

**Shock infantry**

| troop_name | troop_id | offensive_melee_role_score | crafted_melee_score_base | melee_skill_factor | crafted_melee_template | armor_total | effective_armor | armor_audit_sum | TwoHanded | OneHanded | Polearm | Athletics | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Conspiracy Knight | conspiracy_knight | 45.7 | 100 | 0.64 | TwoHandedSword | 192.67 | 53.58 | 146.7 | 140 | 120 | 90 | 90 | vlandia | 26 | 3 | special_or_unlinked |
| Battanian Veteran Falxman | battanian_veteran_falxman | 40.7 | 100 | 0.59 | TwoHandedSword | 136 | 42.6 | 107 | 130 | 70 | 70 | 130 | battania | 26 | 1 | main_or_minor_line |
| Conspiracy Spear Master | conspiracy_spearmaster | 37.76 | 81.96 | 0.68 | TwoHandedPolearm | 169.33 | 41.68 | 124 | 80 | 90 | 150 | 110 | vlandia | 26 | 3 | special_or_unlinked |
| Nord Ulfhedinn | nord_ulfhednar | 35.11 | 81.96 | 0.64 | TwoHandedPolearm | 156.33 | 49.43 | 127.3 | 90 | 140 | 140 | 150 | nord | 26 | 3 | main_or_minor_line |
| Sturgian Heroic Line Breaker | sturgian_ulfhednar | 34.87 | 75.72 | 0.68 | OneHandedSword | 212 | 52.1 | 155 | 150 | 80 | 80 | 150 | sturgia | 26 | 3 | main_or_minor_line |

**Line infantry**

| troop_name | troop_id | defensive_role_score | defense_score_base | armor_total | effective_armor | armor_audit_sum | shield_armor | shield_hp | OneHanded | Athletics | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Vlandian Sergeant | vlandian_sergeant | 54.54 | 49.08 | 173 | 47.7 | 141 | 15.7 | 500 | 130 | 130 | vlandia | 26 | 3 | main_or_minor_line |
| Sturgian Heavy Spearman | sturgian_shock_troop | 53.4 | 47.61 | 195.33 | 52.07 | 147.3 | 7 | 546.7 | 140 | 125 | sturgia | 26 | 3 | special_or_unlinked |
| Nord Huscarl | nord_huscarl | 52 | 45.78 | 143.33 | 49.13 | 112 | 5 | 633.3 | 200 | 160 | nord | 31 | 3 | main_or_minor_line |
| Nord Berserkir | nord_berserkr | 51.97 | 47.18 | 167.33 | 53.95 | 122.4 | 5 | 513.3 | 140 | 140 | nord | 26 | 3 | main_or_minor_line |
| Aserai Veteran Infantry | aserai_veteran_infantry | 51.96 | 44.03 | 181 | 56.3 | 160 | 1 | 360 | 160 | 130 | aserai | 26 | 3 | main_or_minor_line |

**Archer**

| troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Bow | ranged_skill_factor | armor_total | has_shield | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Battanian Fian Champion | battanian_fian_champion | 43.36 | 69.09 | 67 | woodland_longbow | 220 | 1 | 167 | False | battania | 31 | 3 | noble_line |
| Battanian Fian | battanian_fian | 29.72 | 69.09 | 67 | woodland_longbow | 160 | 0.73 | 125 | False | battania | 26 | 3 | noble_line |
| Conspiracy Longbowman | conspiracy_longbowman | 28.57 | 69.09 | 67 | woodland_longbow | 150 | 0.68 | 135.67 | False | battania | 26 | 3 | special_or_unlinked |
| Nord Sky-Gods Chosen | nord_skathi | 26.52 | 64.06 | 65 | woodland_longbow/woodland_yew_bow | 140 | 0.64 | 125 | True | nord | 26 | 3 | main_or_minor_line |
| Aserai Bahriyyah | aserai_marine_t5 | 26.22 | 67.13 | 74 | nomad_bow | 140 | 0.64 | 91.33 | True | aserai | 26 | 3 | main_or_minor_line |

**Crossbow**

| troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Crossbow | ranged_skill_factor | armor_total | has_shield | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Conspiracy Warworn Crossbowman | conspiracy_warworn_crossbowman | 35.98 | 78.05 | 102 | crossbow_f | 150 | 0.68 | 125 | True | vlandia | 26 | 1 | special_or_unlinked |
| Vlandian Nauta | vlandian_marine_t5 | 30.62 | 79.31 | 105 | crossbow_f | 130 | 0.59 | 98 | True | vlandia | 26 | 3 | main_or_minor_line |
| Vlandian Sharpshooter | vlandian_sharpshooter | 30.5 | 79.31 | 105 | crossbow_f | 130 | 0.59 | 138 | True | vlandia | 26 | 1 | special_or_unlinked |
| Imperial Sergeant Crossbowman | imperial_sergeant_crossbowman | 26.27 | 74.14 | 96 | crossbow_d | 130 | 0.59 | 145.33 | True | empire | 26 | 3 | main_or_minor_line |
| Boar Champion | company_of_the_boar_tier_3 | 19.25 | 73.88 | 95 | crossbow_d | 100 | 0.45 | 110 | True | vlandia | 21 | 1 | main_or_minor_line |

**Thrower**

| troop_name | troop_id | skirmisher_role_score | throw_score_base | throw_damage | direct_throw_item | crafted_throw_item | Throwing | throw_skill_factor | armor_total | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Aserai Vanguard Faris | aserai_vanguard_faris | 100 | 30.46 | 0 |  | eastern_javelin_3_t4 | 140 | 0.88 | 207 | aserai | 31 | 3 | noble_line |
| Hidden Soldati | hidden_hand_tier_2 | 95.38 | 100 | 45 | sling_braided |  | 70 | 0.44 | 67.33 | empire | 16 | 3 | main_or_minor_line |
| Battanian Mounted Skirmisher | battanian_mounted_skirmisher | 93.45 | 30.46 | 0 |  | western_javelin_3_t4 | 150 | 0.94 | 156 | battania | 26 | 3 | special_or_unlinked |
| Sturgian Horse Raider | sturgian_horse_raider | 85.38 | 30.46 | 0 |  | northern_javelin_3_t4 | 130 | 0.81 | 160 | sturgia | 26 | 3 | main_or_minor_line |
| Jawwal Bedouin | jawwal_tier_3 | 82.3 | 30.46 | 0 |  | eastern_javelin_1_t2 | 140 | 0.88 | 22.33 | aserai | 21 | 3 | main_or_minor_line |

**Shock cavalry**

| troop_name | troop_id | shock_cav_index | horse_charge | horse_speed | horse_maneuver | horse_hp | mount | has_lance | Polearm | Riding | armor_total | effective_armor | defensive_role_score | offensive_melee_role_score | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Vlandian Banner Knight | vlandian_banner_knight | 89.05 | 32 | 49 | 68 | 60 | t3_vlandia_horse | True | 260 | 200 | 189 | 51.6 | 74.68 | 82.02 | vlandia | 31 | 3 | noble_line |
| Imperial Elite Cataphract | imperial_elite_cataphract | 81.58 | 28 | 59 | 66 | 20 | t3_empire_horse | True | 260 | 200 | 204 | 58.8 | 78.21 | 82.61 | empire | 31 | 3 | noble_line |
| Vlandian Champion | vlandian_champion | 81.36 | 32 | 49 | 68 | 60 | t3_vlandia_horse | True | 160 | 130 | 171.67 | 47.35 | 71.64 | 50.63 | vlandia | 26 | 3 | noble_line |
| Training Master | tutorial_npc_advanced_melee_easy | 78.44 | 35 | 65 | 65 | 70 | noble_horse | False | None | None | 29 | 9.95 | 30.46 | None | battania | 15 | 2 | special_or_unlinked |
| Training Master | tutorial_npc_advanced_melee_normal | 78.44 | 35 | 65 | 65 | 70 | noble_horse | False | None | None | 18 | 5.8 | 46.47 | None | battania | 4 | 2 | special_or_unlinked |

**Horse archer**

| troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Bow | Crossbow | Riding | mobility_factor | horse_speed | horse_maneuver | mount | armor_total | culture | level | n_rosters | line_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Khuzait Khan's Guard | khuzait_khans_guard | 48.26 | 60.43 | 54 | composite_steppe_bow | 200 | 25 | 200 | 1.25 | 60 | 77 | t3_khuzait_horse | 172 | khuzait | 31 | 3 | noble_line |
| Khuzait Kheshig | khuzait_kheshig | 35.67 | 58.18 | 55.33 | composite_steppe_bow/steppe_war_bow | 160 | 20 | 130 | 1.21 | 60 | 77 | t3_khuzait_horse | 126 | khuzait | 26 | 3 | noble_line |
| Aserai Mamluke Heavy Cavalry | aserai_mameluke_heavy_cavalry | 32.71 | 58.27 | 56 | composite_steppe_bow | 130 | 20 | 130 | 1.21 | 51 | 73 | t2_aserai_horse | 161 | aserai | 26 | 3 | main_or_minor_line |
| Imperial Bucellarii | bucellarii | 31.05 | 58.91 | 53 | composite_steppe_bow | 140 | 60 | 120 | 1.2 | 50 | 60 | t2_empire_horse | 139.67 | empire | 26 | 3 | main_or_minor_line |
| Khuzait Heavy Horse Archer | khuzait_heavy_horse_archer | 30.84 | 60.43 | 54 | composite_steppe_bow | 130 | 20 | 130 | 1.21 | 47 | 69 | t2_khuzait_horse | 168 | khuzait | 26 | 3 | main_or_minor_line |

---

# Companion CSVs

Full ranked lists (all troops per role, not just the top 15), same filters, same aggregation:

- `role_report_shock_infantry.csv` — 128 rows
- `role_report_line_infantry.csv` — 358 rows
- `role_report_archer.csv` — 158 rows
- `role_report_crossbow.csv` — 32 rows
- `role_report_thrower.csv` — 90 rows
- `role_report_shock_cavalry.csv` — 116 rows
- `role_report_horse_archer.csv` — 22 rows

Every CSV carries `rank`, `tier`, the ranking metric, its drivers, `n_rosters`, `culture`,
`level` and `line_status`. Outsized units are excluded from the CSVs as well as the tables.

# Open items for other workers

1. **Crafted melee/throw stats are not reconstructed** — the entire offensive-melee and
   crafted-javelin scoring rests on template-name constants. V4.4 model concern.
2. **Load-order resolution prefers stat-less stubs** (`warg_*`, `northern_round_shield`).
   Export/catalog concern; 20 shock-cavalry troops are mis-ranked as a result.
3. **`ranged_role_score` does not distinguish bow from crossbow skill** — several top crossbow
   entries have `Crossbow` 35–50 yet rank on weapon damage. Model concern.
4. **Mean vs max roster aggregation** — this report uses mean, `OVERVIEW.md` uses max. Worth
   picking one convention track-wide.
