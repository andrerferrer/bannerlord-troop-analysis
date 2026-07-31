# Soldier role report — `realm_of_thrones` / `export_20260731_150800`

Intra-track soldier ranking across the seven combat roles: shock infantry, line infantry,
archer, crossbow, thrower, shock cavalry, horse archer.

## Labels

- `evidence_basis=xml_structural`, `empirical=false` (ADR-004). Zero battle-derived quantities.
- Model: `role_scores_v1` conservative, **used as published** — no formula in
  `scripts/scoring/generate_vanilla_role_scores.py` was changed or re-derived here.
  Model changes belong to a V4.4 PR, out of scope for this report.
- SSOT pin: `analysis_pack/realm_of_thrones/` + `data/realm_of_thrones/audit/` at
  `export_20260731_150800` (ADR-003). No XML was re-exported; no audit was rebuilt.
- Package digest: `fc87e360e884cc9aa4baa15e4bdd372824c1f7054b2a9acef6d8c0df3732db3b`
- **Intra-track only.** Every number below is normalised inside `realm_of_thrones`.
  Do not compare a rank or a score against `vanilla`, `nightmare_sails`, or `taom`.
- Secondary context: `OVERVIEW.md` in this same directory (four primary categories,
  full ranked lists). This report does not restate or modify it — it re-cuts the same
  scored population into the seven soldier roles.

## Filters applied

Applied in this order, all of them mandatory per `analysis_pack/SCHEMA.md` and
`analysis_pack/AGENT_PROMPT.md`:

| # | filter | effect on this track |
| --- | --- | --- |
| 1 | `item_found == True` | drops 31 of 55,436 audit rows (11 on soldiers, 9 distinct soldier troops: unresolved `wildling_shield`, `kg_gloves`, `chainmail_reinforcements`, `triangular_spear_t3`, plus 2 blank ids) |
| 2 | `occupation == Soldier` / `is_soldier == True` | 1,232 of 6,187 troops. Notables, wanderers, lords, townsfolk, caravan guards dropped |
| 3 | drop multiplayer + obsolete | 84 `mp_*` soldier ids present in the parse; all 84 are also `change_type=inalterado`, so filter 4 already removes them. Verified: 0 `mp_*` ids survive |
| 4 | drop untouched vanilla baseline (`change_type == inalterado` in `<track>_override_report.csv`) | 1,809 troop ids are `inalterado`; 367 of them are soldiers, taking 1,232 soldiers down to 865. Same filter the OVERVIEW uses — troops ROT neither added nor overrode |
| 5 | **keep NavalDLC** | no NavalDLC/Nord/marine troop was excluded by name or culture |

**Scored population: 865 soldier troops** — identical to the OVERVIEW's "after filters: 865",
so this report and the OVERVIEW rank the same set.

No name-based filters (no Greyjoy/specials exclusion). Every one of the 865 troops appears
in at least one role table or in the unscorable appendix.

## Roster aggregation choice

`roster_index` values are alternative equipment sets the game picks between at spawn, so
they are never summed. Two aggregations are in play and they are **not the same**:

1. **Columns taken from `role_scores_v1` (inherited, not re-derived).** The published
   `realm_of_thrones_troop_role_scores_v1.csv` already collapses rosters, and it does so
   per column: the four `*_role_score` columns and the `*_score_base` drivers use
   **max over `roster_index`** (best-roster); `armor_total`, `effective_armor` and
   `defense_score_base` use **mean over `roster_index`**; the `has_*` flags use max
   (true if any roster). Restated here for transparency — changing it is a model PR.
2. **Descriptive metrics computed in this report from the audit CSV.**
   **Arithmetic mean across every `roster_index` of the troop** (not index 0). Chosen so
   a troop that carries a heavy shield in 1 of 4 rosters is not credited as if it always
   does. Roster count per troop is carried in the companion CSVs as `roster_count`.

Where the two disagree the table header says which column it is: `*_role_score` and
`*_score_base` are inherited (best-roster); `shield_hp`, `horse_charge`, `accuracy` and
friends are mean-across-rosters.

## Role definitions and metric mapping

Roles are defined from the published flags so they are reproducible; a troop may appear
in more than one role table when it genuinely fills both (a javelin-carrying shieldman is
in both `line_infantry` and `thrower`). Cavalry roles are mutually exclusive with the foot
roles.

| role | membership predicate | ranked by (existing `role_scores_v1` column) | descriptive metrics added from the audit CSVs |
| --- | --- | --- | --- |
| shock infantry | `default_group == Infantry` AND NOT `has_horse` AND NOT `has_ranged` AND NOT `has_shield` | `offensive_melee_role_score` | — (melee is template-proxy only, see gaps) |
| line infantry | `default_group == Infantry` AND NOT `has_horse` AND NOT `has_ranged` AND `has_shield` | `defensive_role_score` | `shield_hp`, `shield_armor` |
| archer | `has_bow` AND NOT `has_horse` | `ranged_role_score` | `ranged_accuracy`, `ranged_missile_speed`, `ranged_speed_rating`, `ranged_base_damage`, `ammo_stack` |
| crossbow | `has_crossbow` AND NOT `has_horse` | `ranged_role_score` | same as archer (`speed_rating` shown instead of accuracy — it is the reload proxy) |
| thrower | `has_throwing` AND NOT `has_horse` | `skirmisher_role_score` | `thrown_damage`, `thrown_stack`, `thrown_speed_rating` (all structurally empty here, see gaps) |
| shock cavalry | `has_horse` AND NOT `has_ranged` | `defensive_role_score` | `horse_charge`, `horse_speed`, `horse_maneuver`, `horse_extra_health`, `harness_armor`, `shield_hp` |
| horse archer | `has_horse` AND `has_ranged` | `ranged_role_score` | horse stats as above + archer metrics |

Shock cavalry is ranked by `defensive_role_score` because that is the **only** published
column whose driver ingests mount quality: in the frozen scorer,
`defense_raw` adds `horse_charge_damage*0.25 + horse_speed*0.06 + horse_maneuver*0.04`
for mounted rosters, while `offensive_melee_role_score` only adds a flat `+4` for
`has_horse`. `offensive_melee_role_score` is shown as a second column in that table so a
lance-first reading is still possible. No new composite index was invented.

### Exact formulas for the descriptive metrics

All computed on the filtered audit rows (`item_found == True`, `occupation == Soldier`),
per `(troop_id, roster_index)`, then averaged across roster indices:

```
shield_hp           = max(hit_points)        over rows where slot LIKE 'Item%' AND type == 'Shield'
shield_armor        = max(shield_armor)      over the same rows
horse_charge        = max(horse_charge_damage)   over rows where slot == 'Horse'
horse_speed         = max(horse_speed)           over rows where slot == 'Horse'
horse_maneuver      = max(horse_maneuver)        over rows where slot == 'Horse'
horse_extra_health  = max(horse_extra_health)    over rows where slot == 'Horse'
harness_armor       = max(body_armor)            over rows where slot == 'HorseHarness'
ammo_stack          = sum(stack_amount)      over rows where type IN ('Arrows','Bolts')
ammo_thrust         = max(thrust_damage)     over rows where type IN ('Arrows','Bolts')

best ranged row     = argmax over rows where type IN ('Bow','Crossbow') of max(swing_damage, thrust_damage)
ranged_base_damage  = max(swing_damage, thrust_damage) of that row
ranged_accuracy     = accuracy       of that row
ranged_missile_speed= missile_speed  of that row
ranged_speed_rating = speed_rating   of that row

best thrown row     = argmax over rows where type == 'Thrown' of max(swing_damage, thrust_damage)
thrown_damage       = max(swing_damage, thrust_damage) of that row
thrown_stack        = stack_amount   of that row
```

`ranged_base_damage` is the weapon alone; the published `ranged_damage` column is
weapon + best ammo `thrust_damage`, which is why the two differ by a few points.

## Coverage gaps you must read before using the tables

These are properties of the data and of the frozen model, reported not fixed.

1. **No real melee damage exists in this track.** Every melee weapon on a ROT soldier
   resolves as `item_kind == CraftedItem` / `type == CraftedWeapon` with
   `crafted_stats_reconstructed = False` and `score_usage_status = audit_only_no_aggressive_htk`.
   All 3,501 crafted weapon rows on filtered soldiers have blank `swing_damage` and blank
   `thrust_damage`; there are **zero** direct-`Item` melee weapons to fall back on. So
   `crafted_melee_score_base` is a crafting-template class proxy (`TwoHandedSword` 60,
   `TwoHandedPolearm` 58, `Axe` 46, `OneHandedSword`/`OneHandedPolearm` 44, `Mace` 43,
   times a usability factor), never measured damage. Shock-infantry order is therefore
   **weapon class × skill × armor**, not hitting power. Do not read it as a damage ladder.
2. **The thrower ladder does not measure throwing power.** No filtered soldier carries a
   direct `Thrown` weapon: the only 7 `Thrown` rows in the track (slings and a throwing
   stone on `hidden_hand_*` / `borrowed_troop`) all belong to `inalterado` vanilla troops
   and are dropped by filter 4. Consequently `throw_damage` is 0 for all 41 throwers and
   `throw_score_base` takes exactly **two** values across them: 30.5 (crafted javelin) and
   28.8 (crafted throwing knife/dagger). Ordering inside the role comes from the
   `Throwing` skill, `crafted_melee_score_base` and `defense_score_base` — it is
   "javelin-carrying heavy infantry, sorted by skill", not "best javelin".
3. **46 ranged troops cannot be scored at all.** 92 of the 865 kept troops have every
   skill column blank in `<track>_troops.csv` because they are defined via
   `skill_template`, which SCHEMA lists as unmapped. In the frozen scorer the blank
   becomes NaN, `ranged_skill_factor` becomes NaN, and `ranged_role_score` becomes NaN —
   so 44 bow troops and 2 crossbow troops carry a populated `ranged_score_base` but no
   role score, and drop out of the ranked tables. All 46 are militia/city-watch lines
   across 23 cultures. They are listed in the appendix and in
   `role_report_unscored_ranged.csv` so their resolved drivers are not lost. The same
   NaN path blanks `offensive_melee_role_score` and `skirmisher_role_score` for those 92
   troops; none of them qualify for the shock-infantry or thrower predicates, so those
   two tables lose nothing. `defensive_role_score` has no skill factor, so the 92 do
   appear in the line-infantry ladder.
4. **The scorer does not apply the `item_found` filter.** `generate_vanilla_role_scores.py`
   reads the audit CSV unfiltered. Blast radius on this track is 11 soldier rows across 9
   troops (0.07% of filtered soldier rows), so the published columns are usable as-is.
   Flagged for the model PR; not corrected here. The descriptive metrics in this report
   **do** apply the filter.
5. **`upgrade_requires` is not modelled**, so recruitment gating is invisible. A troop
   ranking well at `tree_tier` 6 may be far harder to field than one at tier 4.
6. Scores are min–max normalised over the whole roster population, and that population
   includes the outsized units below. The ceiling for `defense_score_base` (100.0) is set
   by an elephant rider, which is why the best ordinary cavalry sits at 68.2 base rather
   than near 100. Tiers are assigned against the best **non-outlier** in each role, so the
   S–D ladders are not affected — but raw `*_score_base` values read low for that reason.

## Tiers

Same rule as the OVERVIEW, reused rather than re-invented
(`scripts/scoring/write_theoretical_overview.py:tier_letter_from_top_fraction`):
score as a fraction of the best **non-outlier** score in that role list — ≥0.90 S,
≥0.70 A, ≥0.40 B, ≥0.20 C, else D. Because roles are ranked separately, an S in
`crossbow` is not comparable to an S in `line_infantry`.

## S+ outliers — parked, excluded from all S–D commentary

Two kinds of outsized unit are pulled out of every ordinary ladder:

- **giants / mammoths** — the OVERVIEW's name regex (`giant`/`mammoth`), 4 troops.
- **elephant-mounted mahouts** — a documented extension of that regex: any troop whose
  mount has `horse_charge_damage >= 200`. In this track that is exactly the mounts
  `mammoth` (charge 400) and `elephant` (charge 350); the next mount down is `unicorn1`
  at 90, so the threshold is not near a boundary. This catches the three Volantene
  elephant units, which the name regex misses and which would otherwise take the top three
  shock-cavalry slots on mount charge alone.

Seven rows, across four roles. They are spectacle-scale and are **not** discussed in any
role section below.

| troop_name | troop_id | role | score column | score | why parked | horse_charge | armor_total | ranged_damage | crafted_melee_score_base | culture | level | tree_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Giant | giant | shock_infantry | offensive_melee_role_score | 64.4 | giant/mammoth name | 0 | 240 | 0 | 73.3 | freefolk | 26 | 1 |
| Giant Archer | giant_archer | archer | ranged_role_score | 88.5 | giant/mammoth name | 0 | 240 | 130 | 73.3 | freefolk | 31 | 2 |
| Elder Giant | elder_giant | archer | ranged_role_score | 69.4 | giant/mammoth name | 0 | 240 | 130 | 73.3 | freefolk | 35 | 2 |
| Golden Company Mahout | golden_elite_pikeman | shock_cavalry | defensive_role_score | 100.0 | outsized mount | 350 | 149 | 0 | 82.0 | volantine | 31 | 5 |
| Golden Company Elephant Rider | golden_horseman | shock_cavalry | defensive_role_score | 94.3 | outsized mount | 350 | 146 | 0 | 82.0 | volantine | 26 | 4 |
| Volantene Mahout | tigercloak_camel_cavalry | shock_cavalry | defensive_role_score | 83.3 | outsized mount | 350 | 168 | 0 | 82.0 | volantine | 26 | 5 |
| Mammoth Riding Giant | giant_rider | horse_archer | ranged_role_score | 100.0 | giant/mammoth name | 400 | 240 | 130 | 73.3 | freefolk | 31 | 2 |

Note `golden_elite_pikeman` (Golden Company Mahout) is a ROT priority anchor in
`REPORT.md` and tops the OVERVIEW's Skirmisher list. It is mounted, so under this report's
role predicates it belongs to shock cavalry, and it is parked here as an S+ outlier. Read
its skirmisher standing from the OVERVIEW, not from the thrower table below.

---

## 1. Shock infantry — 154 troops (+1 S+)

Unshielded foot melee. Ranked by `offensive_melee_role_score`.

| rank | tier | troop_name | troop_id | offensive_melee_role_score | crafted_melee_score_base | melee_template | TwoHanded | Polearm | Athletics | armor_total | effective_armor | culture | level | tree_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | Mountain's Man | mountains_man | 88.9 | 100.0 | TwoHandedSword | 250 | 220 | 240 | 161 | 48.0 | vlandia | 31 | 6 |
| 2 | A | Umber Berzerker | umber_berzerker | 70.7 | 82.0 | TwoHandedPolearm | 250 | 220 | 240 | 160 | 49.2 | battania | 31 | 6 |
| 3 | B | Cerwyn Marauder | cerwyn_marauder | 61.6 | 73.3 | TwoHandedAxe | 250 | 220 | 240 | 147 | 43.4 | battania | 31 | 6 |
| 4 | B | Lyseni Enforcer | lyseni_enforcer | 56.8 | 73.3 | TwoHandedAxe | 230 | 220 | 230 | 190 | 58.5 | lyseni | 31 | 5 |
| 5 | B | Sadistic Wight | sadistic_wight | 51.8 | 73.3 | TwoHandedAxe | 220 | 210 | 220 | 127 | 31.0 | whitewalker | 31 | 6 |
| 6 | B | Qohorik Falxman | qohorik_falxman | 49.0 | 100.0 | TwoHandedSword | 150 | 140 | 140 | 180 | 55.8 | qohorik | 26 | 5 |
| 7 | B | Yi Ti Shi | yiti_pikeman | 48.8 | 100.0 | TwoHandedSword | 150 | 140 | 150 | 177 | 52.1 | yiti | 26 | 5 |
| 8 | C | Tyroshi Renegade | tyroshi_renegade | 32.7 | 73.3 | TwoHandedAxe | 150 | 130 | 140 | 169 | 52.9 | tyroshi | 26 | 5 |
| 9 | C | Reach Axeman | reach_axeman | 30.8 | 82.0 | TwoHandedPolearm | 130 | 110 | 130 | 156 | 45.8 | reach | 26 | 5 |
| 10 | C | Lyseni Executioner | lyseni_executioner | 29.9 | 73.3 | TwoHandedAxe | 140 | 130 | 140 | 176 | 55.8 | lyseni | 26 | 4 |
| 11 | C | Ibbenese Timberman | ibbenese_timberman | 29.6 | 73.3 | TwoHandedAxe | 140 | 110 | 140 | 179 | 51.6 | ibbenese | 26 | 5 |
| 12 | C | Skagosi Barbarian | skag_barbarian | 29.5 | 73.3 | TwoHandedAxe | 140 | 130 | 120 | 168 | 49.2 | skagosi | 26 | 5 |
| 13 | C | Free Folk Wildling Berzerker | freefolk_wildling_berzerker | 29.2 | 73.3 | TwoHandedAxe | 140 | 70 | 140 | 161 | 45.8 | freefolk | 26 | 5 |
| 14 | C | Riverlands Axeman | river_axeman | 26.3 | 73.3 | TwoHandedAxe | 130 | 80 | 140 | 162 | 46.2 | river | 26 | 5 |
| 15 | C | Baratheon Hammerman | baratheon_hammer | 24.4 | 82.0 | TwoHandedPolearm | 110 | 80 | 110 | 139 | 49.0 | stormlands | 21 | 4 |

**Why:** the ladder is almost entirely `crafted_melee_score_base` (weapon class) times the
melee skill factor. `Mountain's Man` wins because it is the only troop pairing the top
template class (`TwoHandedSword`, proxy 60) with maxed melee skills (TwoHanded 250,
Athletics 240) — nothing else in the role has both. `Umber Berzerker` and `Cerwyn Marauder`
have identical skills but step down a template class (`TwoHandedPolearm` 82.0, `TwoHandedAxe`
73.3). Ranks 6–7 (`Qohorik Falxman`, `Yi Ti Shi`) carry the same top template as the leader
but tier-5 skills near 150, and lose roughly half the score to the skill factor — the
clearest illustration that this ladder is skill-weighted, not damage-weighted.

The distribution is brutally top-heavy: 1 S, 1 A, 5 B, 13 C, **134 D**. That is a
consequence of the skill factor collapsing everything below veteran skill levels, plus
min–max normalisation across the whole population. Treat the D block as "unscorable at
this granularity" rather than as a fine-grained ordering.

`Lyseni Enforcer` (rank 4) is the best armoured body in the role's top 5 (armor_total 190,
effective_armor 58.5) — it is the pick if you want the unshielded damage profile without
the paper defence of `Cerwyn Marauder` (147 / 43.4).

**Value picks (tree_tier ≤ 4):** `Lyseni Executioner` (#10 C, tier 4),
`Baratheon Hammerman` (#15 C, tier 4), `Harlaw Seaman` (#16 C, tier 4),
`Sarnori Elite Javelinier` (#17 C, tier 3 — best sub-tier-4 result in the role).

## 2. Line infantry — 318 troops

Shielded foot melee. Ranked by `defensive_role_score`.

| rank | tier | troop_name | troop_id | defensive_role_score | defense_score_base | armor_total | effective_armor | shield_hp | shield_armor | melee_template | OneHanded | culture | level | tree_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | Tarly Vanguard | tarly_vanguard | 47.8 | 47.3 | 176 | 56.8 | 470 | 17.0 | TwoHandedPolearm | 240 | reach | 31 | 6 |
| 2 | S | Celtigar Banneret | celtigar_banneret | 45.2 | 44.2 | 198 | 61.9 | 315 | 9.0 | TwoHandedPolearm | 230 | dragonstone | 31 | 6 |
| 3 | S | Kingsguard | kingsguard_captain | 44.9 | 42.6 | 211 | 65.0 | 370 | 1.0 | TwoHandedSword | 140 | crownlands | 26 | 4 |
| 4 | S | Guardian of the Rock | casterly_guardian | 44.7 | 44.7 | 209 | 61.8 | 400 | 8.0 | OneHandedSword | 240 | vlandia | 31 | 5 |
| 5 | S | Stark House Guard | stark_houseguard | 44.7 | 45.4 | 186 | 61.6 | 420 | 9.0 | TwoHandedPolearm | 140 | battania | 26 | 5 |
| 6 | S | Stark Sworn Sword | stark_swornsword | 44.7 | 45.4 | 204 | 61.6 | 420 | 9.0 | TwoHandedPolearm | 250 | battania | 31 | 6 |
| 7 | S | Mallister House Guard | mallister_houseguard | 44.7 | 45.4 | 197 | 62.0 | 400 | 9.0 | TwoHandedPolearm | 130 | river | 26 | 5 |
| 8 | S | Lannister Officer | lannister_officer | 44.5 | 42.1 | 178 | 57.2 | 400 | 8.0 | TwoHandedSword | 130 | vlandia | 26 | 5 |
| 9 | S | Grafton Flaming Knight | grafton_flameknight | 44.3 | 44.8 | 206 | 61.6 | 380 | 9.0 | TwoHandedPolearm | 230 | vale | 31 | 6 |
| 10 | S | Stark Pikeman | stark_pikeman | 43.8 | 45.4 | 186 | 61.6 | 420 | 9.0 | OneHandedAxe / OneHandedSword | 130 | battania | 26 | 5 |
| 11 | S | Casterly Rock Marshal | casterly_pikeman | 43.3 | 44.7 | 209 | 61.8 | 400 | 8.0 | OneHandedSword | 140 | vlandia | 26 | 4 |
| 12 | S | Grafton House Guard | grafton_houseguard | 43.2 | 43.6 | 187 | 59.5 | 380 | 9.0 | TwoHandedPolearm | 130 | vale | 26 | 5 |
| 13 | S | Westerling Hedgeknight | westerling_hedgeknight | 43.2 | 43.6 | 204 | 59.5 | 380 | 9.0 | TwoHandedPolearm | 230 | vlandia | 31 | 6 |
| 14 | A | Valyrian Captain | valyrian_captain | 42.8 | 43.2 | 184 | 60.0 | 400 | 7.0 | TwoHandedPolearm | 140 | valyrian | 26 | 5 |
| 15 | A | Bolton Flayer | bolton_flayer | 42.8 | 41.2 | 207 | 62.1 | 390 | 1.0 | TwoHandedPolearm | 240 | battania | 31 | 6 |

**Why:** `defensive_role_score` is `defense_score_base*0.72 + crafted_melee_score_base*0.12
+ throw_score_base*0.04 + 12 (shield) + 6 (horse)`, and `defense_score_base` is driven by
`effective_armor*1.25 + shield_hp/35 + shield_armor*1.1`. Everyone in this table has the
shield bonus, so separation comes from armour and shield quality.

`Tarly Vanguard` leads on shield quality, not armour: `shield_armor` 17 is the highest in the
role and its 470-hp shield is the heaviest in the top 15 (the role-wide `shield_hp` maximum,
520, sits on `Cerwyn Veteran Axeman` far down the ladder). It is not the best-armoured troop
in the top five
(176 / 56.8 versus `Kingsguard` 211 / 65.0). `Celtigar Banneret` is the inverse — best
armour of the top three (198 / 61.9) on a comparatively light 315-hp shield. `Kingsguard`
(#3) rides the highest `effective_armor` in the role (65.0) plus the top melee template
(`TwoHandedSword`, 100.0) to an S at only tier 4.

This is the flattest ladder in the report — 13 S, 127 A, 166 B, 12 C, no D. Shielded heavy
infantry is where ROT put its depth: dozens of house-guard lines land within a few points
of each other (`Stark House Guard`, `Stark Sworn Sword`, `Mallister House Guard` all at
44.7). Below the top ~20 the differences are inside the noise of a proxy model; pick on
availability and culture, not on rank.

**Value picks (tree_tier ≤ 4):** `Kingsguard` (#3 S, tier 4), `Casterly Rock Marshal`
(#11 S, tier 4), `Casterly Rock Pikeman` (#19 A, tier 3), `Black Goat Devout` (#20 A, tier 4),
`Qohorik Swordsman` (#26 A, tier 4).

## 3. Archer — 150 troops (+2 S+, +44 unscorable)

Foot bow users. Ranked by `ranged_role_score`.

| rank | tier | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | bow | accuracy | missile_speed | ammo_stack | Bow | effective_armor | culture | level | tree_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | Qartheen Enthroned Guardian | enthroned_guardian | 85.7 | 91.0 | 98 | qarth_longbow | 100 | 87 | 32 | 250 | 54.1 | qartheen | 31 | 5 |
| 2 | S | Ravens' Teeth | ravens_teeth | 84.7 | 97.2 | 101 | ravens_teeth_longbow | 100 | 87 | 66 | 260 | 56.9 | river | 31 | 6 |
| 3 | S | Goldenheart Warrior | summer_master_longbowman | 80.8 | 94.7 | 101 | goldenheart_longbow | 100 | 87 | 46 | 250 | 49.2 | summer | 31 | 6 |
| 4 | A | Mormont Bowmaiden | mormont_bowmaiden | 75.6 | 74.2 | 68 | woodland_longbow | 94 | 82 | 46 | 250 | 56.7 | battania | 31 | 6 |
| 5 | A | Greyjoy Sniper | greyjoy_sniper | 75.0 | 77.3 | 73 | lowland_yew_bow | 94 | 79 | 46 | 250 | 50.8 | sturgia | 31 | 6 |
| 6 | B | Triarch Guardian | triarch_guardian | 54.3 | 68.8 | 58 | steppe_war_bow | 95 | 80 | 46 | 240 | 56.6 | volantine | 31 | 5 |
| 7 | B | Night's Watch Protector of the Realm | nightswatch_protector | 52.1 | 67.2 | 54 | glen_ranger_bow | 88 | 70 | 64 | 230 | 52.6 | nightswatch | 31 | 5 |
| 8 | B | Qartheen Pureborn Champion | qartheen_champion | 45.3 | 89.4 | 97 | qarth_longbow | 100 | 87 | 24 | 140 | 54.1 | qartheen | 26 | 4 |
| 9 | B | Qartheen Longbowman | qartheen_longbowman | 40.3 | 92.7 | 97 | qarth_longbow | 100 | 87 | 48 | 140 | 44.3 | qartheen | 26 | 5 |
| 10 | C | Blackwood Longbowman | blackwood_longbowman | 34.3 | 76.2 | 67 | woodland_longbow | 94 | 82 | 64 | 150 | 41.8 | river | 26 | 5 |
| 11 | C | Tyrell Elite Longbowman | tyrell_longbowman | 33.2 | 79.2 | 72 | lowland_yew_bow | 94 | 79 | 64 | 140 | 44.6 | reach | 26 | 5 |
| 12 | C | Mormont Veteran Huntress | mormont_veteran_huntress | 33.0 | 73.1 | 67 | woodland_longbow | 94 | 82 | 42 | 150 | 43.1 | battania | 26 | 5 |
| 13 | C | Stark Master Longbowman | stark_master_archer | 32.1 | 76.2 | 67 | woodland_longbow | 94 | 82 | 64 | 140 | 38.6 | battania | 26 | 5 |
| 14 | C | Tully Longbowman | tully_longbowman | 31.2 | 70.3 | 60 | lowland_longbow | 94 | 74 | 64 | 150 | 46.6 | river | 26 | 5 |
| 15 | C | Greyjoy Marksman | greyjoy_marksman | 30.7 | 73.2 | 72 | lowland_yew_bow | 94 | 79 | 21 | 140 | 50.8 | sturgia | 26 | 5 |

**Why:** `ranged_role_score` is `ranged_score_base*0.78*ranged_skill_factor*mobility_factor
+ defense_score_base*0.10 + 8 (horse) + 3 (shield)`, and `ranged_score_base` is normalised
`ranged_damage + speed_rating*0.35 + accuracy*0.15 + missile_speed*0.10 + min(ammo,64)*0.25`.
Bow skill is the dominant multiplier: `ranged_skill_factor = max(Bow, Crossbow)/220`,
clipped to [0.25, 1.15].

The top three are the only bow troops that combine a 95+ damage longbow with 250+ Bow.
`Ravens' Teeth` has the highest bow driver of any non-outlier troop in the track
(`ranged_score_base` 97.2; only the S+ giants, at 100.0, are higher) and `Bow` 260, the
single highest bow skill among all filtered soldiers and the deepest quiver in
the top five (66 arrows). It finishes second only because `Qartheen Enthroned Guardian`
carries a shield (+3 flat) and slightly better `defense_score_base`. On sustained output
`Ravens' Teeth` is the better unit; on survivability the Qartheen is.

Ranks 8–9 are the clearest tier/skill decoupling in the report. `Qartheen Pureborn Champion`
and `Qartheen Longbowman` carry the same `qarth_longbow` as the S-tier leader —
`ranged_score_base` 89.4 and 92.7, `ranged_damage` 97 — but Bow 140 instead of 250, so the
skill factor cuts them roughly in half. Their **weapons** are S-tier; their **crews** are not.

Bow choice, from the audit stats: `qarth_longbow` / `ravens_teeth_longbow` /
`goldenheart_longbow` (accuracy 100, missile_speed 87, base damage 95–97) form a clear top
class; `woodland_longbow` and `lowland_yew_bow` (accuracy 94, base 64–69) are the mid class;
`steppe_*` bows (accuracy 89–95, base 51–58) are the low class. Anything ranked below ~#20
is carrying a mid or low bow.

**Value picks (tree_tier ≤ 4):** `Qartheen Pureborn Champion` (#8 B, tier 4 — S-tier bow at
tier 4), `Tigercloak Elite` (#16 C, tier 4), `Night's Watch Master Ranger` (#29 C, tier 4).

## 4. Crossbow — 28 troops (+2 unscorable)

Foot crossbow users. Ranked by `ranged_role_score`. `speed_rating` is shown instead of
accuracy because for crossbows it is the reload proxy — a low `speed_rating` on a crossbow
means slow reload, not poor handling.

| rank | tier | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | crossbow | speed_rating | missile_speed | ammo_stack | Crossbow | effective_armor | culture | level | tree_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | Myrish Artisan of War | myrish_artisan | 88.1 | 87.5 | 105 | crossbow_f | 63 | 97 | 18 | 240 | 58.8 | myrish | 31 | 5 |
| 2 | S | Frey Assassin | frey_assassin | 83.2 | 85.4 | 98 | crossbow_d | 62 | 90 | 36 | 250 | 41.6 | river | 31 | 6 |
| 3 | B | Myrish Master Crossbowman | myrish_master_crossbowman | 44.5 | 79.5 | 89 | crossbow_g | 80 | 70 | 18 | 150 | 47.1 | myrish | 26 | 4 |
| 4 | B | Gilded Bolt Rangers | golden_master_crossbowman | 40.7 | 82.0 | 93 | crossbow_c | 60 | 87 | 36 | 160 | 43.7 | volantine | 26 | 4 |
| 5 | B | Frey Sharpshooter | frey_sharpshooter | 39.6 | 85.4 | 98 | crossbow_d | 62 | 90 | 36 | 140 | 41.6 | river | 26 | 5 |
| 6 | B | Hightower Marksmen | hightower_marksman | 38.2 | 88.9 | 102 | crossbow_f | 63 | 97 | 40 | 130 | 44.7 | reach | 26 | 5 |
| 7 | B | Velaryon Marksman | velaryon_marksman | 38.1 | 88.9 | 102 | crossbow_f | 63 | 97 | 40 | 130 | 43.4 | dragonstone | 26 | 5 |
| 8 | B | Tarth Elite Crossbowman | tarth_elite_crossbowman | 37.5 | 88.9 | 102 | crossbow_f | 63 | 97 | 40 | 130 | 33.4 | stormlands | 26 | 5 |
| 9 | B | Casterly Rock Master Crossbowman | casterly_master_crossbowman | 36.7 | 86.1 | 102 | crossbow_f | 63 | 97 | 20 | 130 | 45.1 | vlandia | 26 | 4 |
| 10 | B | Tarly Elite Crossbowman | tarly_elite_crossbowman | 36.4 | 86.1 | 102 | crossbow_f | 63 | 97 | 20 | 130 | 40.8 | reach | 26 | 5 |
| 11 | C | Stormlands Heavy Crossbowman | stormlands_heavy_crossbowman | 34.4 | 81.4 | 91 | crossbow_c | 60 | 87 | 40 | 140 | 45.9 | stormlands | 26 | 5 |
| 12 | C | Grafton Elite Archer | grafton_elite_crossbowman | 34.0 | 81.5 | 88 | crossbow_g | 80 | 70 | 36 | 140 | 39.6 | vale | 26 | 5 |
| 13 | C | Night's Watch Master Crossbowman | nightswatch_master_crossbowman | 33.4 | 81.4 | 91 | crossbow_c | 60 | 87 | 40 | 140 | 30.2 | nightswatch | 26 | 5 |
| 14 | C | Frey Veteran Crossbowman | frey_veteran_crossbowman | 26.3 | 81.5 | 87 | crossbow_g | 80 | 70 | 40 | 110 | 33.8 | river | 21 | 4 |
| 15 | C | Myrish Elite Crossbowman | myrish_elite_crossbowman | 25.4 | 77.7 | 86 | crossbow_b | 61 | 80 | 36 | 110 | 46.5 | myrish | 21 | 3 |

**Why:** identical formula to the archer role, and the same skill-multiplier story, but the
population is far smaller and far more equipment-homogeneous — all ten of the top ten carry
`crossbow_c/d/f/g`, six of them the same `crossbow_f`. Separation is therefore almost purely `Crossbow` skill.

`Myrish Artisan of War` and `Frey Assassin` are the only two crossbow troops above 240
`Crossbow` skill, and they take both S slots with a ~44-point gap to third place. The
Myrish unit leads on equipment as well: `crossbow_f` is the best bolt-thrower in the track
(base damage 100, accuracy 100, missile_speed 97) and it is one of only two shielded units
in the crossbow top ten (the other is `Myrish Master Crossbowman` at #3).

The gap after rank 2 is the story. `Hightower Marksmen`, `Velaryon Marksman`,
`Tarth Elite Crossbowman`, `Casterly Rock Master Crossbowman` and `Tarly Elite Crossbowman`
all carry the same `crossbow_f` with `ranged_damage` 102 — better raw weapon output than
`Frey Assassin`'s `crossbow_d` (98) — and all land in B because their `Crossbow` skill is
130. Five different houses issue the best crossbow in the game to tier-5 troops who cannot
shoot it well.

Note the reload tradeoff the descriptive columns expose: `crossbow_f` has `speed_rating` 63
against `crossbow_g`'s 80. `Myrish Master Crossbowman` (#3) trades 16 points of damage for
that faster cycle.

**Value picks (tree_tier ≤ 4):** `Myrish Master Crossbowman` (#3 B, tier 4),
`Gilded Bolt Rangers` (#4 B, tier 4), `Casterly Rock Master Crossbowman` (#9 B, tier 4),
`Myrish Elite Crossbowman` (#15 C, tier 3).

## 5. Thrower — 41 troops

Foot troops with a throwing weapon. Ranked by `skirmisher_role_score`.
**Read gap 2 above before using this table** — `throw_damage` is structurally 0 for every
row and `throw_score_base` has only two distinct values, so this is not a javelin-power
ladder.

| rank | tier | troop_name | troop_id | skirmisher_role_score | throw_score_base | throw_damage | throw_item (crafted) | Throwing | crafted_melee_score_base | defense_score_base | has_shield | culture | level | tree_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | Ghiscari Lockstep Legionnaire | ghiscari_unsullied_unbroken | 71.0 | 30.5 | 0 | eastern_javelin_2_t3 | 220 | 100.0 | 29.4 | True | ghiscari | 31 | 5 |
| 2 | S | Tarly Vanguard | tarly_vanguard | 68.4 | 30.5 | 0 | western_javelin_3_t4 | 230 | 82.0 | 47.3 | True | reach | 31 | 6 |
| 3 | S | Celtigar Banneret | celtigar_banneret | 67.6 | 30.5 | 0 | northern_javelin_3_t4 | 230 | 82.0 | 44.2 | True | dragonstone | 31 | 6 |
| 4 | S | Ibbenese Navigator | ibbenese_navigator | 66.7 | 30.5 | 0 | northern_javelin_1_t2 | 230 | 82.0 | 41.1 | True | ibbenese | 31 | 5 |
| 5 | S | Glover Bushranger | glover_bushranger | 66.2 | 30.5 | 0 | northern_javelin_3_t4 | 240 | 82.0 | 39.2 | True | battania | 31 | 6 |
| 6 | S | Unsullied | unsullied | 65.0 | 30.5 | 0 | eastern_javelin_2_t3 | 270 | 82.0 | 35.0 | True | ghiscari | 31 | 0 |
| 7 | A | Bolton Flayer | bolton_flayer | 63.1 | 28.8 | 0 | celtic_throwing_dagger | 230 | 82.0 | 41.2 | True | battania | 31 | 6 |
| 8 | A | Umber Berzerker | umber_berzerker | 63.1 | 30.5 | 0 | northern_javelin_2_t3 | 220 | 82.0 | 28.2 | False | battania | 31 | 6 |
| 9 | A | Tyroshi Corsair | tyroshi_corsair | 62.0 | 30.5 | 0 | generic_javelin_1_t3 | 230 | 73.3 | 37.3 | True | tyroshi | 31 | 5 |
| 10 | A | Guardian of the Rock | casterly_guardian | 60.9 | 30.5 | 0 | western_javelin_2_t3 | 180 | 75.7 | 44.7 | True | vlandia | 31 | 5 |
| 11 | A | Yi Ti Shi | yiti_pikeman | 53.7 | 28.8 | 0 | empire_throwingknife_t5 | 150 | 100.0 | 29.9 | False | yiti | 26 | 5 |
| 12 | B | Ghiscari Elite Legionnaire | ghiscari_unsullied_unbent | 49.5 | 30.5 | 0 | eastern_javelin_1_t2 | 130 | 100.0 | 29.4 | True | ghiscari | 26 | 4 |
| 13 | B | Black Goat Devout | qohorik_goat_devout | 48.6 | 30.5 | 0 | eastern_javelin_1_t2 | 140 | 82.0 | 40.7 | True | qohorik | 26 | 4 |
| 14 | B | Glover Warrior | glover_warrior | 48.2 | 30.5 | 0 | northern_javelin_3_t4 | 140 | 82.0 | 39.2 | True | battania | 26 | 5 |
| 15 | B | Martell House Guard | martell_houseguard | 45.0 | 30.5 | 0 | eastern_javelin_2_t3 | 130 | 82.0 | 40.3 | True | aserai | 26 | 5 |

**Why:** with `throw_score_base` effectively constant, `skirmisher_role_score`
(`throw_score_base*0.65*throw_skill_factor + crafted_melee_score_base*0.15 +
defense_score_base*0.10 + 6 (horse)`) reduces to `Throwing` skill first, melee template
second, armour third. `Ghiscari Lockstep Legionnaire` leads on the melee term, not the
throw term: `crafted_melee_score_base` 100.0 (top class) with Throwing 220.
`Unsullied` has by far the highest `Throwing` in the track (270) and still finishes 6th
because its `defense_score_base` is 35.0 against `Tarly Vanguard`'s 47.3 — the defence term
outweighs 50 points of throwing skill. That is a model artefact, not a gameplay claim.

Every troop in the top ten except `Umber Berzerker` (the only unshielded one) also appears
in the line-infantry table: in ROT the thrower role is not a distinct light-skirmisher class, it is
a javelin sidearm bolted onto shielded heavy infantry. `Tarly Vanguard` and
`Celtigar Banneret` are #1 and #2 line infantry and #2 and #3 thrower.

The two `throw_score_base` values are worth stating plainly: 30.5 = a crafted javelin
(`*_javelin_*`), 28.8 = a crafted throwing knife or dagger. `Bolton Flayer` (#7) and
`Yi Ti Shi` (#11) are the 28.8 rows.

**Value picks (tree_tier ≤ 4):** `Unsullied` (#6 S, `special_or_unlinked` — no upgrade line
at all, recruit-only), `Ghiscari Elite Legionnaire` (#12 B, tier 4),
`Black Goat Devout` (#13 B, tier 4), `Tyroshi Firstmate` (#16 B, tier 4).

## 6. Shock cavalry — 159 troops (+3 S+)

Mounted troops without a ranged weapon. Ranked by `defensive_role_score` (the only
published column that ingests mount quality — see the mapping table).
`offensive_melee_role_score` is carried alongside for a lance-first reading.

| rank | tier | troop_name | troop_id | defensive_role_score | defense_score_base | horse_charge | horse_speed | horse_maneuver | harness_armor | armor_total | shield_hp | melee_template | offensive_melee_role_score | Riding | culture | level | tree_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | Captain of the Kingsguard | mounted_kingsguard | 71.9 | 65.8 | 32 | 64 | 68 | 80 | 211 | 370 | TwoHandedSword | 100.0 | 250 | crownlands | 31 | 5 |
| 2 | S | Mallister Eagle Knight | mallister_knight | 71.4 | 68.2 | 30 | 58 | 58 | 75 | 208 | 400 | TwoHandedPolearm | 77.6 | 240 | river | 31 | 6 |
| 3 | S | Captain of the Queen's Guard | queensguard_captain | 70.0 | 66.6 | 30 | 58 | 58 | 75 | 204 | 400 | TwoHandedPolearm | 70.7 | 220 | valyrian | 31 | 5 |
| 4 | S | Stark Cavalry | stark_cavalry | 69.9 | 66.0 | 22 | 55 | 66 | 74 | 186 | 420 | TwoHandedPolearm | 44.3 | 130 | battania | 26 | 5 |
| 5 | S | Valyrian Cavalry | targaryen_dragonknight | 69.9 | 64.8 | 30 | 58 | 58 | 75 | 184 | 400 | TwoHandedPolearm | 47.4 | 150 | valyrian | 26 | 5 |
| 6 | S | Targaryen Queen's Guard | targ_queensguard | 69.7 | 66.2 | 30 | 58 | 58 | 75 | 198 | 400 | TwoHandedPolearm | 44.2 | 140 | valyrian | 26 | 4 |
| 7 | S | Arryn Winged Knight | arryn_moonknight | 68.8 | 65.2 | 28 | 61 | 66 | 75 | 221 | 370 | TwoHandedPolearm | 80.5 | 250 | vale | 31 | 6 |
| 8 | S | Dondarrion Boltknight | dondarion_boltknight | 68.4 | 64.7 | 27 | 62 | 71 | 75 | 195 | 300 | TwoHandedPolearm | 77.1 | 230 | stormlands | 31 | 6 |
| 9 | S | Magister Guard Elite | magister_guard | 68.2 | 62.8 | 19 | 59 | 69 | 65 | 197 | 400 | TwoHandedPolearm | 70.3 | 220 | pentoshi | 31 | 5 |
| 10 | S | Lannister Prideknight | lannister_prideknight | 68.0 | 64.3 | 32 | 64 | 68 | 75 | 178 | 400 | TwoHandedPolearm | 77.1 | 240 | vlandia | 31 | 6 |
| 11 | S | Grafton Horseman | grafton_horseman | 68.0 | 64.2 | 22 | 53 | 61 | 75 | 187 | 380 | TwoHandedPolearm | 44.0 | 130 | vale | 26 | 5 |
| 12 | S | Lannister Knight | lannister_knight | 67.8 | 64.1 | 30 | 58 | 58 | 75 | 179 | 400 | TwoHandedPolearm | 44.0 | 140 | vlandia | 26 | 5 |
| 13 | S | White Harbor Knight Commander | whiteharbor_knight_commander | 67.8 | 64.0 | 23 | 62 | 69 | 75 | 191 | 400 | TwoHandedPolearm | 80.3 | 240 | battania | 31 | 6 |
| 14 | S | White Harbor Elite Knight | whiteharbor_elite_knight | 67.4 | 63.6 | 22 | 55 | 66 | 75 | 190 | 400 | TwoHandedPolearm | 47.2 | 140 | battania | 26 | 5 |
| 15 | S | Realm Knight | realm_knight | 67.4 | 61.8 | 22 | 53 | 61 | 72 | 182 | 300 | TwoHandedPolearm | 40.4 | 130 | crownlands | 26 | 4 |

**Why:** every row gets the horse (+6) flat and almost every row the shield (+12) —
all of the top 15, and 148 of 159 overall — so ordering comes from
`defense_score_base`, which for mounted rosters sums armour, shield and
`charge*0.25 + speed*0.06 + maneuver*0.04`. Because ordinary ROT warhorses cluster tightly
(charge 19–32, speed 53–64, maneuver 58–71), the mount term contributes only a few points
and rider armour decides the ladder.

`Captain of the Kingsguard` leads on the melee term rather than the mount: it holds the top
`offensive_melee_role_score` in the role (100.0, the only `TwoHandedSword` in the top 14)
plus the best armour (armor_total 211, harness 80) on a good horse (charge 32 / speed 64).
`Mallister Eagle Knight` has the highest `defense_score_base` of any non-outlier troop in
the track (68.2) and still ranks second because its `TwoHandedPolearm` template scores 82
against the leader's 100.

The two readings genuinely disagree and the table lets you see it. On
`offensive_melee_role_score`, `Arryn Winged Knight` (80.5, armor_total 221 — the heaviest
rider in the role), `White Harbor Knight Commander` (80.3) and `Mallister Eagle Knight`
(77.6) are the lance picks, while `Stark Cavalry` (#4) and `Grafton Horseman` (#11) sit
above them on the defensive ladder with melee scores in the 44s. `Stark Cavalry` earns its
place on the best shield in the role (`shield_hp` 420) and a 70-point `horse_extra_health`
mount, not on its lance.

Tier compression is extreme: 29 S, 70 A, 56 B, 4 C, no D. Heavy shielded knights are ROT's
deepest role after line infantry, and ranks ~15–90 are separated by low single digits.
Choose on culture and recruitment, not rank.

**Top by raw mount charge (ordinary mounts only, outliers excluded):** `unicorn1` (charge 90,
speed 60) and `unicorn3` (charge 80, speed 55) are the only mounts above the warhorse band, carried by
one and two troops respectively; the best conventional mounts are `noble_horse_western`
(King's Destrier, charge 36 / speed 69) and `noble_horse_imperial` (Andalos Destrier,
charge 36 / speed 68). No troop in the shock-cavalry top 15 rides better than
`t3_vlandia_horse` (charge 32 / speed 64).

**Value picks (tree_tier ≤ 4):** `Targaryen Queen's Guard` (#6 S, tier 4),
`Realm Knight` (#15 S, tier 4), `Dragonstone Shock Knight` (#17 S, tier 4),
`Casterly Rock Champion` (#21 S, tier 4).

## 7. Horse archer — 3 troops (+1 S+)

Mounted troops with a ranged weapon. Ranked by `ranged_role_score`.

| rank | tier | troop_name | troop_id | ranged_role_score | ranged_score_base | ranged_damage | bow | ammo_stack | Bow | Riding | horse_speed | horse_maneuver | effective_armor | culture | level | tree_tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | Mormont Mounted Huntress | mormont_mounted_huntress | 48.3 | 67.7 | 57 | steppe_war_bow | 42 | 150 | 140 | 52 | 57 | 43.1 | battania | 26 | 5 |
| 2 | A | Pentoshi Mounted Archer | pentoshi_mounted_archer | 42.6 | 65.0 | 54 | composite_steppe_bow | 36 | 140 | 140 | 54 | 67 | 43.2 | pentoshi | 26 | 5 |
| 3 | B | Ghiscari Mounted Archer | ghiscari_mounted_archer | 32.2 | 66.7 | 54 | composite_steppe_bow | 48 | 110 | 100 | 54 | 59 | 32.5 | ghiscari | 21 | 4 |

**Why:** this is the finding, not the ranking — **ROT has essentially no horse archers.**
Three of 865 filtered soldier troops are mounted with a bow, plus the mammoth rider parked
as S+. All three carry mid-class steppe bows (`steppe_war_bow` / `composite_steppe_bow`,
`ranged_damage` 54–57) with Bow 110–150, so against the foot archer leader (85.7) all three
would land in that ladder's B/C band; they rank S/A/B here only because the tier is computed against the best of
these three. Do not read `Mormont Mounted Huntress`'s S as track-leading archery.

`Mormont Mounted Huntress` leads on bow driver (`ranged_score_base` 67.7, Bow 150, 42
arrows). `Pentoshi Mounted Archer` has the better mount (maneuver 67 vs 57) and equal
Riding. `Ghiscari Mounted Archer` carries the deepest quiver (48) but the lowest skills
(Bow 110, Riding 100) and by far the lightest armour (effective 32.5 vs ~43).

Only 3 of 865 troops carry `default_group == HorseArcher` and they are exactly these three.
If you need mounted missile capability in this track, there is no depth to draw on — the
practical answer is foot archers plus shock cavalry.

**Value pick (tree_tier ≤ 4):** `Ghiscari Mounted Archer` (#3 B, tier 4) is the only
sub-tier-5 option in the role.

---

## Faction callouts

### Ravens — `Ravens' Teeth` (`ravens_teeth`, culture `river`)

The strongest bow unit in the track by driver, and a one-off. It is a single troop with no
sibling line: `ranged_score_base` 97.2 is the highest bow value among the 865 filtered
soldiers once the S+ giants (100.0) are parked, `Bow` 260 is the highest bow skill of any
filtered soldier, and `ravens_teeth_longbow` (base damage 96,
accuracy 100, missile_speed 87) sits in the top bow class. It also carries 66 arrows, more
than any other troop in the archer top five.

It ranks #2 archer rather than #1 purely on the model's flat bonuses: `Qartheen Enthroned
Guardian` gains +3 for a shield and a marginally higher `defense_score_base`, on a bow with
a *lower* driver (91.0 vs 97.2). Ravens' Teeth is unshielded (`effective_armor` 56.9, which
is still high for an archer). Read this as: highest sustained bow output in the track,
second on the composite because it trades a shield for it. It is the only Ravens-named
troop in the filtered set — no Ravens line exists in any other role.

### Goldenheart — `Goldenheart Warrior` (`summer_master_longbowman`, culture `summer`)

#3 archer, S tier, and the top of the Summer Isles bow line. `goldenheart_longbow` has the
highest base damage of any bow in the track (97, accuracy 100, missile_speed 87), paired
with Bow 250 and 46 arrows. Its `ranged_score_base` (94.7) is second only to Ravens' Teeth,
and its S placing is legitimate rather than tier-inflated.

The line beneath it drops off hard, and that is the point: `Summer Isles Longbowman` (#28 C),
`Summer Isles Archer` (#83 D) and `Summer Isles Bowman` (#120 D) all carry `tribal_bow`
(base damage 59–62), a low-class bow. Goldenheart is a tier-6 capstone, not the top of a
strong ladder — the culture's archery is one elite unit standing on a weak line.
Summer's other roles are unremarkable: best line infantry `Summer Isles Spearmaster` (#59 A),
best cavalry `Summer Isles Horseman` (#121 B), no shock infantry above D.

### Myrish — culture `myrish`

The crossbow specialist culture of the track, and the only culture with a genuinely
top-to-bottom crossbow ladder:

| troop | role rank | tier | crossbow | `ranged_damage` | `Crossbow` | tree_tier |
| --- | --- | --- | --- | --- | --- | --- |
| Myrish Artisan of War | crossbow #1 | S | `crossbow_f` | 105 | 240 | 5 |
| Myrish Master Crossbowman | crossbow #3 | B | `crossbow_g` | 89 | 150 | 4 |
| Myrish Elite Crossbowman | crossbow #15 | C | `crossbow_b` | 86 | 110 | 3 |
| Myrish Crossbowman | crossbow #25 | D | `crossbow_b` | 86 | 80 | 2 |

`Myrish Artisan of War` is the highest-ranked ranged troop of any kind in the OVERVIEW's
combined list, and here it takes crossbow #1 with the best bolt-thrower in the track
(`crossbow_f`: base damage 100, accuracy 100, missile_speed 97) plus a shield. `Myrish Master Crossbowman` at tier 4 is the best
value crossbow in the track.

Myrish bows are the mirror image: `Myrish Elite Archer` (#38 C), `Myrish Archer` (#109 D),
`Myrish Bowman` (#134 D) all carry `steppe_bow`/`composite_steppe_bow`, the low class.
Elsewhere Myrish is mid-table — `Myrish Legionnaire` (line infantry #52 A),
`Myrish Cavalry` (shock cavalry #48 A), nothing above D in shock infantry. Recruit Myrish
for bolts, not for anything else. One further note: `Myrish Militia Veteran Archer` is in
the unscorable set below, so Myrish's militia archery is invisible to the model.

---

## Appendix — ranged troops the model cannot score (46)

Populated `ranged_score_base` but NaN `ranged_role_score`, because every skill column is
blank (`skill_template`, unmapped per SCHEMA). Top 12 by `ranged_score_base`; full list in
`role_report_unscored_ranged.csv`.

| troop_name | troop_id | ranged_score_base | ranged_damage | ranged item | has_bow | has_crossbow | culture | level |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| City Watch Veteran Crossbowman | crownlands_militia_veteran_archer | 75.3 | 79 | crossbow_e | False | True | crownlands | 21 |
| City Watch Crossbowman | crownlands_militia_archer | 68.0 | 69 | crossbow_a | False | True | crownlands | 11 |
| Qartheen Militia Archer | qartheen_militia_archer | 66.0 | 51 | composite_bow | True | False | qartheen | 11 |
| Qartheen Militia Veteran Archer | qartheen_militia_veteran_archer | 66.0 | 51 | composite_bow | True | False | qartheen | 16 |
| Ghiscari Militia Veteran Archer | ghiscari_militia_veteran_archer | 65.6 | 52 | steppe_heavy_bow | True | False | ghiscari | 16 |
| Lyseni Militia Veteran Archer | lyseni_militia_veteran_archer | 65.6 | 52 | steppe_heavy_bow | True | False | lyseni | 16 |
| Myrish Militia Veteran Archer | myrish_militia_veteran_archer | 65.6 | 52 | steppe_heavy_bow | True | False | myrish | 16 |
| Norvoshi Militia Veteran Archer | norvos_militia_veteran_archer | 65.6 | 52 | steppe_heavy_bow | True | False | norvos | 16 |
| Pentoshi Militia Veteran Archer | pentoshi_militia_veteran_archer | 65.6 | 52 | steppe_heavy_bow | True | False | pentoshi | 16 |
| Qohorik Militia Veteran Archer | qohorik_militia_veteran_archer | 65.6 | 52 | steppe_heavy_bow | True | False | qohorik | 16 |
| Sarnori Militia Veteran Archer | sarnor_militia_veteran_archer | 65.6 | 52 | steppe_heavy_bow | True | False | sarnor | 16 |
| Summer Isles Militia Veteran Archer | summer_militia_veteran_archer | 65.6 | 52 | steppe_heavy_bow | True | False | summer | 16 |

`City Watch Veteran Crossbowman` would place mid-table in the crossbow role on its driver
alone (`ranged_score_base` 75.3, `crossbow_e`, damage 79) — it is missing from the ladder
for a data-mapping reason, not a quality one. The remaining rows are the per-culture militia
archer template repeated across 23 cultures.

---

## Companion CSVs

Written next to this report, one per role plus the unscorable appendix. Each carries the
full ranked list (not just the top 15), the inherited `role_scores_v1` columns, all four
`*_role_score` values for cross-role reading, and every descriptive metric defined above.
`role_score` / `role_score_column` name the ranking metric; `tier` is `S+` for parked
outliers and `spectacle_reason` says which rule parked them.

| file | rows (incl. S+) |
| --- | --- |
| `role_report_shock_infantry.csv` | 155 |
| `role_report_line_infantry.csv` | 318 |
| `role_report_archer.csv` | 152 |
| `role_report_crossbow.csv` | 28 |
| `role_report_thrower.csv` | 41 |
| `role_report_shock_cavalry.csv` | 162 |
| `role_report_horse_archer.csv` | 4 |
| `role_report_unscored_ranged.csv` | 46 |

## Limitations

- Proxy model, no empirical validation. `role_scores_v1` is conservative and explicitly
  `score_status = role_scores_v1_conservative_not_final`. No HTK, no time-to-kill, no
  battle data. The ROT priority anchors in `REPORT.md` (Ravens' Teeth, Goldenheart Warrior,
  Celtigar Banneret, Lyseni Enforcer, Myrish Artisan of War, Golden Company Mahout,
  Sarnori Spider, Baratheon Hammerknight) are the empirical validation targets; vanilla
  `CONTROL_IDS` do not transfer to this track.
- Melee ordering is weapon-class proxy times skill, never measured damage (gap 1).
  Thrower ordering does not measure throwing power (gap 2).
- `Cut` / `Pierce` / `Blunt` interact with armour differently and that is not modelled;
  no cross-damage-type comparison is made in this report.
- 46 ranged troops and, for the melee/skirmisher columns, 92 skill-template troops are
  outside the model's reach (gap 3).
- A troop surviving filter 4 means ROT added or overrode its XML — it does not prove the
  troop spawns. Party templates can bypass a defined troop entirely.
- Intra-track only. Do not join these rows into empirical rankings or compare them across
  tracks.
