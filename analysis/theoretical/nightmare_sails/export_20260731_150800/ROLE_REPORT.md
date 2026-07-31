# Soldier ROLE_REPORT — `nightmare_sails` / `export_20260731_150800`

Intra-track soldier ranking by **battlefield role**, one ladder per role. Companion to
`OVERVIEW.md` (which ranks by the four `role_scores_v1` model categories); this file cuts the
same data by the seven roles a player actually recruits for.

## Labels / provenance

- Evidence basis: `xml_structural` (ADR-004). Empirical: `false`. Zero battle-derived quantities.
- Model read: `role_scores_v1` conservative proxy — **columns consumed as shipped, formulas not
  re-derived**. Any formula change belongs in a V4.4 model PR, out of scope here.
- SSOT (ADR-003): `analysis_pack/nightmare_sails/*.csv` + the `role_scores_v1` CSVs under this
  export dir. No XML was read or re-exported.
- Package digest: `fc87e360e884cc9aa4baa15e4bdd372824c1f7054b2a9acef6d8c0df3732db3b`
- All 6 `nightmare_sails` files in `analysis_pack/MANIFEST.csv` re-hashed: **6/6 sha256 match**.
  `analysis_pack/nightmare_sails/nightmare_sails_troop_equipment_audit.csv` is byte-identical to
  `data/nightmare_sails/audit/nightmare_sails_troop_equipment_audit.csv` (same 18,736 rows).
- **Intra-track only.** Every number here is normalized inside `nightmare_sails`. Do not compare
  a rank or score in this file against `vanilla`, `realm_of_thrones`, or `taom`.

---

## Filters applied

Applied in this order to `nightmare_sails_troops.csv` → 371 soldiers → **256 troops in the
analysis pool**.

| # | Filter | Effect | Source of the rule |
|---|---|---|---|
| 1 | `item_found == True` | **0 rows dropped** — the pack ships pre-filtered (18,736/18,736 rows are `True`) | SCHEMA.md §Mandatory filters 1 |
| 2 | `occupation == Soldier` | 1,989 troops → **371 soldiers** (drops Lords, Wanderers, Townsfolk, Bandits, notables) | SCHEMA.md 2 |
| 3 | Drop multiplayer ids (`troop_id` starts with `mp_`) | −84 → 287 | SCHEMA.md 3 |
| 4 | Drop non-battlefield pseudo-troops (see list below) | −31 → **256** | this report; see caveat |
| 5 | **Keep NavalDLC** | 44 NavalDLC/marine troops retained (17% of the pool) | SCHEMA.md 4 |
| 6 | Giants / mammoths → S+ outlier section | **0 matches in this track** | OVERVIEW.md convention |

**Filter 4 — the 31 pseudo-troops dropped**, by regex on `troop_id`:
`^tutorial_` (5: `tutorial_npc_basic_melee`, `tutorial_npc_advanced_melee_easy`,
`tutorial_npc_advanced_melee_normal`, `tutorial_npc_mounted_ai`,
`tutorial_placeholder_volunteer`); arena/tournament contenders `_contender` and the four base
`{hardy,dignified,confident,bold}_contender` (20 total); arena fighters `regular_fighter`,
`veteran_fighter`, `champion_fighter`, `sword_sister` (4); quest loaners `borrowed_troop`,
`veteran_borrowed_troop` (2). These never appear in a field battle order of battle, so they would
distort a role ladder.

**Caveat on filter 3/4 — obsolete troops are not fully separable from this pack.**
`analysis_pack` carries no `is_obsolete` column, and `data/nightmare_sails/raw_xml/` holds only
manifests (no XML). SCHEMA.md states vanilla's mp+obsolete set is 135 ids / **95 soldiers**;
the `mp_` prefix accounts for only 84 of those 95, so roughly **11 obsolete soldiers are
unflagged** and some may still sit in the 256. Filter 4 removes the 31 ids that are demonstrably
non-battlefield by name; it is a proxy, not the `is_obsolete` attribute SCHEMA.md prefers.
Recommendation (out of scope here): add `is_obsolete` to the pack export.

**Kept on purpose, flagged rather than filtered:** settlement militia (28), `guard_<culture>` town
guards (7), and the conspiracy quest army (29). These do fight, but they are not recruitable
through a normal party — read their ranks as "what this unit is worth if you meet it", not "what
you can field".

### Divergence from `OVERVIEW.md`'s pool (deliberate)

`OVERVIEW.md` keeps mod-added/overridden troops only (drops `change_type == inalterado` from
`nightmare_sails_override_report.csv`): 371 → 270. This report instead keeps the **whole playable
soldier roster of the track**, because a player recruiting an archer does not care whether
NightmareSailsxDTAB rewrote that troop's XML. Concretely:

- 27 ids in OVERVIEW's 270 are **not** here: the 20 arena contenders, 5 tutorial NPCs, 2 borrowed
  troops (all filter 4).
- 13 ids here are **not** in OVERVIEW's 270 (untouched vanilla, `change_type=inalterado`):
  `galloglass_tier_{1,2,3}`, `guardians_tier_{1,2,3}`, `guard_{aserai,battania,empire,khuzait,sturgia,vlandia}`,
  `huskarl_swordsman`.
- Pool composition by `change_type`: `override` 239, `inalterado` 13, `novo` 4.

`change_type` is carried as a column in every companion CSV, so the OVERVIEW pool is reproducible
from these files by filtering `change_type != inalterado`.

---

## Roster aggregation — explicit choice

`roster_index` values are **alternative** loadouts; the game picks one at spawn. Two different
aggregations are in play in this file and both are stated on every column:

1. **`role_scores_v1` columns are used exactly as the frozen scorer emitted them at troop level**
   (`nightmare_sails_troop_role_scores_v1.csv`). That scorer aggregates
   (`scripts/scoring/generate_vanilla_role_scores.py:254-284`):
   - the four `*_role_score` columns, `*_score_base` (except defense), `ranged_damage`,
     `throw_damage`, and the `has_*` flags → **max across `roster_index`** (best-case loadout);
   - `defense_score_base`, `armor_total`, `effective_armor` → **mean across `roster_index`**.
   I did not re-aggregate them.
2. **Every metric I computed for this report uses the arithmetic MEAN across `roster_index`**,
   not index 0 and not max:
   - `mount_raw`, `harness_armor` — mean over the rosters that actually carry a `Horse` slot;
   - `shield_share`, `twoh_share`, `horse_share` — mean of the per-roster boolean (so 0.67 = "2 of
     3 rosters carry a shield").
   Mean was chosen because spawn picks a roster roughly arbitrarily, so the expected loadout is the
   honest summary; max would make every troop look like its best kit. All 41 shock-cavalry and 22
   horse-archer entries have `horse_share == 1.0`, so no cavalry ranking depends on this choice.

Pool sizes: **256 troops / 759 troop×roster rows** (mean 2.96 rosters per troop). The shipped
`nightmare_sails_roster_role_scores_v1.csv` holds 991 rows because it also covers the 115 troops
filters 3-4 removed.

---

## Role → metric mapping

Five of seven roles map onto an existing `role_scores_v1` column. Two do not (the model has no
cavalry-charge term at all), so they use **descriptive metrics computed here**, suffixed `_desc`
and never written back into any model file.

| role | pool definition (all: 256-troop pool) | ranked by | source |
|---|---|---|---|
| shock infantry | no horse, no bow, no crossbow, `shield_share < 0.5` | `offensive_melee_role_score` | `role_scores_v1` as shipped |
| line infantry | no horse, no bow, no crossbow, `shield_share >= 0.5` | `defensive_role_score` | `role_scores_v1` as shipped |
| archer | no horse, `has_bow` | `ranged_role_score` | `role_scores_v1` as shipped |
| crossbow | no horse, `has_crossbow` | `ranged_role_score` | `role_scores_v1` as shipped |
| thrower | no horse, `has_throwing` | `skirmisher_role_score` | `role_scores_v1` as shipped |
| shock cavalry | `has_horse`, not `has_ranged` | `shock_cav_index_desc` | **computed, formula below** |
| horse archer | `has_horse`, `has_ranged` | `ranged_role_score` | `role_scores_v1` as shipped (+ `mount_index_desc` as context) |

Shock infantry and line infantry partition the foot-melee pool exactly at `shield_share = 0.5`;
no troop appears in both.

### Descriptive formulas (this report only — not a model change)

Computed from `nightmare_sails_troop_equipment_audit.csv`, rows with `item_found == True`:

```
# per (troop_id, roster_index), over rows with slot == 'Horse' (max within the slot):
mount_raw_roster = horse_charge_damage
                 + 0.35 * horse_speed
                 + 0.15 * horse_maneuver
                 + 0.05 * horse_extra_health

mount_raw        = mean(mount_raw_roster) over the troop's horsed rosters
harness_armor    = mean(max body_armor of slot == 'HorseHarness') over horsed rosters

# min-max normalised WITHIN the role pool (so the scale differs between the
# shock-cavalry pool and the horse-archer pool — do not compare the two):
mount_index_desc = 100 * (mount_raw - min_pool) / (max_pool - min_pool)

shock_cav_index_desc = 0.50 * mount_index_desc
                     + 0.35 * offensive_melee_role_score   # role_scores_v1, NaN treated as 0
                     + 0.15 * defensive_role_score          # role_scores_v1, NaN treated as 0
```

Weight rationale: charge output is the defining act of shock cavalry, so the mount carries half;
the rider's melee proxy carries most of the rest; armour/shield gets a small share because a
lancer that dies on contact does not get a second charge. The weights are a judgement call, not a
fitted model — `mount_index_desc`, `offensive_melee_role_score` and `defensive_role_score` are all
in the companion CSV, so re-weighting is one sort away.

**`mount_raw` is the only real weapon-damage-bearing number available for melee cavalry.** All 3,723
melee weapon rows in this track are `item_kind == CraftedItem` with
`crafted_stats_reconstructed == False`: `swing_damage`, `thrust_damage`, `weapon_length` and
`speed_rating` are blank on **every one of them**. There is no lance reach or lance damage in this
pack, so no reach column is reported. Melee strength anywhere in this file is the model's
template proxy (`melee_proxy × melee_usability`, `generate_vanilla_role_scores.py:63-90`), not a
damage figure.

### Tier convention

Reused verbatim from `write_theoretical_overview.py:62-82`, applied **within each role pool**
against that pool's leader: `frac = score / best_in_pool` → S ≥ 0.90, A ≥ 0.70, B ≥ 0.40,
C ≥ 0.20, else D. A tier letter is therefore only meaningful next to its own role.

### S+ spectacle outliers

**None in this track.** The OVERVIEW's giant/mammoth regex
(`\bgiants?\b|\bmammoths?\b|(^|_)giant(_|$)|(^|_)mammoth(_|$)`) matches **0** of the 371
`nightmare_sails` soldiers — outsized units are `taom` / `realm_of_thrones` content. The S–D
ladders below are therefore uncrowded, and no unit was parked out of ordinary commentary.

---

## 1. Shock infantry

Pool 45 (9 NavalDLC). Tiers: S 4, A 2, B 12, C 18, D 9.

| rank | tier | troop_name | troop_id | culture | tree_tier | offensive_melee_role_score | crafted_melee_score_base | crafted_melee_template | TwoHanded | Polearm | effective_armor | shield_share | naval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Conspiracy Knight | conspiracy_knight | vlandia | – | 62.2 | 100.0 | `TwoHandedSword` | 140 | 90 | 55.2 | 0.0 |  |
| 2 | S | Khuzait Tengri | khuzait_Tengri | khuzait | 5 | 60.3 | 100.0 | `OneHandedSword / TwoHandedPolearm / TwoHandedSword` | 120 | 140 | 42.1 | 0.0 | yes |
| 3 | S | Vlandian Captain | vlandian_pikeman | vlandia | 5 | 57.4 | 100.0 | `TwoHandedAxe / TwoHandedSword` | 130 | 130 | 44.9 | 0.0 |  |
| 4 | S | Battanian Veteran Falxman | battanian_veteran_falxman | battania | 5 | 56.8 | 100.0 | `TwoHandedSword` | 130 | 100 | 43.8 | 0.0 |  |
| 5 | A | Flame | embers_of_flame_tier_2 | empire | 2 | 48.5 | 100.0 | `TwoHandedSword` | 115 | 65 | 24.0 | 0.0 |  |
| 6 | A | Battanian Falxman | battanian_falxman | battania | 4 | 43.7 | 100.0 | `TwoHandedSword` | 100 | 45 | 34.1 | 0.0 |  |
| 7 | B | Conspiracy Spear Master | conspiracy_spearmaster | vlandia | – | 41.9 | 60.5 | `TwoHandedPolearm` | 80 | 150 | 49.2 | 0.0 |  |
| 8 | B | Nord Ulfhednar | nord_ulfhednar | nord | 5 | 39.1 | 60.5 | `TwoHandedPolearm` | 90 | 140 | 49.5 | 0.0 | yes |
| 9 | B | Imperial Elite Menavliaton | imperial_elite_menavliaton | empire | 2 | 37.0 | 60.5 | `TwoHandedPolearm` | 80 | 130 | 47.0 | 0.0 |  |
| 10 | B | Vlandian Voulgier | vlandian_voulgier | vlandia | 5 | 35.6 | 60.5 | `TwoHandedPolearm` | 130 | 130 | 37.2 | 0.0 |  |
| 11 | B | Conspiracy Knight Trainee | conspiracy_knight_trainee | vlandia | – | 34.9 | 100.0 | `TwoHandedSword` | 80 | 40 | 23.0 | 0.0 |  |
| 12 | B | Sturgian Heroic Line Breaker | sturgian_ulfhednar | sturgia | 2 | 33.7 | 46.8 | `OneHandedSword` | 150 | 80 | 51.0 | 0.0 |  |
| 13 | B | Spark | embers_of_flame_tier_1 | empire | 1 | 31.8 | 100.0 | `TwoHandedSword` | 75 | 15 | 17.4 | 0.0 |  |
| 14 | B | Nord Warfang | nord_vargr | nord | 4 | 30.9 | 60.5 | `TwoHandedPolearm` | 70 | 110 | 41.0 | 0.0 | yes |
| 15 | B | Aserai Mamluke Palace Guard | mamluke_palace_guard | aserai | 5 | 28.5 | 41.6 | `TwoHandedAxe / TwoHandedMace` | 140 | 80 | 47.2 | 0.0 |  |

**Why.** `offensive_melee_role_score = crafted_melee_score_base × 0.70 × melee_skill_factor +
defense_score_base × 0.10 (+4 horse, −8 one-handed polearm)`, with
`melee_skill_factor = clip(max(OneHanded, TwoHanded, Polearm)/220, 0.25, 1.15)`. Two things move
a troop here: the **weapon template class** and the **best melee skill**.

- The template proxy is coarse and dominates the top. `crafted_melee_score_base` is `norm100` over a
  raw range of exactly [30.0 = `Dagger`, 55.2 = `TwoHandedSword`], so `TwoHandedSword`
  (proxy 60 × usability 0.92 = 55.2) lands on 100 while `TwoHandedPolearm` (58 × 0.78 = 45.24) caps
  at 60.5 no matter how good the actual weapon is. Ranks 1-6 are all
  two-handed-sword users; ranks 7-10 are all polearm users. That gap is a template artifact, not a
  measured damage difference.
- Skill then separates within a class: Conspiracy Knight and Khuzait Tengri both sit at
  `crafted_melee_score_base = 100`, and the 140-vs-120 `TwoHanded` skill plus armour decides the
  order. Sturgian Heroic Line Breaker (rank 12) has the pool's **highest melee skill at 150** but
  a `OneHandedSword` best-template, so it lands mid-B.
- Skill above 253 is wasted: `melee_skill_factor` clips at 1.15 (= 220 × 1.15).

**Best answer per culture** (excluding the conspiracy quest units): Vlandia `vlandian_pikeman`
(Vlandian Captain, T5, rank 3), Battania `battanian_veteran_falxman` (T5, rank 4), Khuzait
`khuzait_Tengri` (T5 NavalDLC, rank 2), Empire `embers_of_flame_tier_2` (T2 minor clan, rank 5) with
`imperial_elite_menavliaton` (T2, rank 9) as the best culture-tree option, Nord `nord_ulfhednar`
(T5, rank 8), Sturgia `sturgian_ulfhednar` (T2, rank 12), Aserai `mamluke_palace_guard` (T5,
rank 15).

**Surprises.** `embers_of_flame_tier_2` (Flame, rank 5) and `embers_of_flame_tier_1` (Spark, rank
13) are minor-clan T2/T1 troops sitting above most culture T5 shock infantry purely because their
best template is `TwoHandedSword` — with `effective_armor` 24.0 and 17.4 they will not survive a
fight the top four win. `imperial_elite_menavliaton` at T2 out-ranks every Aserai and Sturgian
option. Three of the top eleven are conspiracy quest troops (`conspiracy_knight`,
`conspiracy_spearmaster`, `conspiracy_knight_trainee`) — strong on paper, not recruitable.

---

## 2. Line infantry

Pool 83 (23 NavalDLC — the largest naval share of any role). Tiers: S 4, A 17, B 43, C 19, D 0.

| rank | tier | troop_name | troop_id | culture | tree_tier | defensive_role_score | defense_score_base | armor_total | effective_armor | crafted_melee_score_base | crafted_melee_template | naval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Nord Huscarl | nord_huscarl | nord | 5 | 71.7 | 72.8 | 204.4 | 62.0 | 60.5 | `TwoHandedPolearm` | yes |
| 2 | S | Vlandian Sergeant | vlandian_sergeant | vlandia | 5 | 66.8 | 66.0 | 175.7 | 49.1 | 60.5 | `TwoHandedPolearm` |  |
| 3 | S | Sturgian Heavy Spearman | sturgian_shock_troop | sturgia | – | 64.8 | 63.2 | 189.0 | 53.3 | 60.5 | `TwoHandedPolearm` |  |
| 4 | S | Nord Shield-Companion | nord_hirdmann | nord | 4 | 64.5 | 59.7 | 159.4 | 50.1 | 60.5 | `TwoHandedPolearm` | yes |
| 5 | A | Sturgian Heavy Axeman | sturgian_veteran_warrior | sturgia | – | 63.7 | 68.0 | 211.7 | 58.6 | 41.6 | `OneHandedAxe` |  |
| 6 | A | Imperial Legionary | imperial_legionary | empire | – | 61.1 | 61.0 | 202.0 | 56.0 | 60.5 | `TwoHandedPolearm` |  |
| 7 | A | Puppeteer | hidden_hand_tier_3 | empire | 3 | 60.6 | 54.5 | 189.0 | 54.0 | 60.5 | `OneHandedSword / TwoHandedPolearm` |  |
| 8 | A | Aserai Mamluke Warden | aserai_master_archer | aserai | – | 59.5 | 59.1 | 186.7 | 53.8 | 60.5 | `TwoHandedPolearm` |  |
| 9 | A | Battanian Wildling | battanian_wildling | battania | – | 59.4 | 61.7 | 186.3 | 58.2 | 41.6 | `OneHandedAxe` |  |
| 10 | A | Redshank | galloglass_tier_3 | battania | 3 | 58.9 | 58.9 | 177.0 | 52.7 | 41.6 | `OneHandedAxe` |  |
| 11 | A | Nord Berserkir | nord_berserkr | nord | 5 | 58.2 | 59.2 | 172.8 | 49.5 | 46.8 | `OneHandedSword / ThrowingAxe` | yes |
| 12 | A | Conspiracy Veteran Fighter | conspiracy_veteran_fighter | empire | – | 57.2 | 56.0 | 178.0 | 50.5 | 60.5 | `TwoHandedPolearm` |  |
| 13 | A | Conspiracy Commander | imperial_conspiracy_boss | vlandia | – | 56.7 | 32.0 | 110.0 | 30.5 | 60.5 | `OneHandedSword / TwoHandedPolearm` |  |
| 14 | A | Triarii | legion_of_the_betrayed_tier_3 | empire | 3 | 56.4 | 53.8 | 170.0 | 46.8 | 46.8 | `OneHandedSword` |  |
| 15 | A | Nord Hearthguard | nord_jarlsmann | nord | 3 | 55.7 | 49.0 | 126.0 | 40.0 | 60.5 | `TwoHandedPolearm` | yes |

**Why.** `defensive_role_score = defense_score_base × 0.72 + crafted_melee_score_base × 0.12 +
throw_score_base × 0.04 + 12 (shield) + 6 (horse)`, and
`defense_score_base = norm100(effective_armor × 1.25 + shield_hp/35 + shield_armor × 1.1 +
harness_armor × 0.45 + horse terms)` with
`effective_armor = 0.20·head + 0.65·body + 0.10·arm + 0.05·leg`. Body armour is ~2/3 of the
protection term, so **body armour plus shield quality is the whole ladder**; the +12 shield
constant is worth more than any melee weapon difference (max melee contribution is 0.12 × 100 = 12).

- `nord_huscarl` leads on raw protection: `armor_total` 204.4 / `effective_armor` 62.0, the highest
  pairing among shielded foot troops, plus a T5 shield.
- Note this score has **no skill factor at all** — that is why `sturgian_veteran_warrior` (rank 5)
  posts the pool's best `defense_score_base` (68.0) and best armour (211.7) yet ranks below
  `nord_hirdmann`: its `OneHandedAxe` template scores 41.6 against 60.5 for polearms, and
  0.12 × 18.9 ≈ 2.3 points is enough to flip a 0.8-point gap.
- `imperial_conspiracy_boss` at rank 13 is a scoring quirk worth ignoring for line-infantry
  purposes: `armor_total` 110 and `defense_score_base` 32.0 are mid-pool, but the shield and horse
  constants (+12, +6) plus a polearm template carry it into A.

**Surprises.** Five of the top nine carry no tier at all (`line_status = special_or_unlinked`):
`sturgian_shock_troop`, `sturgian_veteran_warrior`, `imperial_legionary`, `aserai_master_archer`,
`battanian_wildling`. These are the culture elites the track's upgrade graph does not link — they
are the best line infantry available and the tree data cannot tell you how to reach them
(`upgrade_requires` is not modelled in this pack). `galloglass_tier_3` (Redshank, T3, untouched
vanilla minor clan) beats every Aserai and Khuzait culture line-infantry option.
`aserai_master_archer` is named "Aserai Mamluke Warden" here and is a **shielded polearm
infantryman**, not an archer — read the equipment, not the id.

---

## 3. Archer

Pool 39 (8 NavalDLC). Tiers: S 1, A 1, B 12, C 11, D 14.

| rank | tier | troop_name | troop_id | culture | tree_tier | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Bow | effective_armor | has_shield | naval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Battanian Fian Champion | battanian_fian_champion | battania | 5 | 98.0 | 94.3 | 71 | `woodland_longbow` | 260 | 56.6 | no |  |
| 2 | A | Battanian Fian | battanian_fian | battania | 4 | 74.9 | 94.3 | 71 | `woodland_longbow` | 200 | 40.6 | no |  |
| 3 | B | Nord Sky-Gods Chosen | nord_skathi | nord | 5 | 59.8 | 91.1 | 70 | `lowland_yew_bow` | 160 | 44.3 | yes | yes |
| 4 | B | Conspiracy Longbowman | conspiracy_longbowman | battania | – | 54.6 | 94.3 | 71 | `woodland_longbow` | 150 | 46.5 | no |  |
| 5 | B | Aserai Bahriyyah | aserai_marine_t5 | aserai | 2 | 52.4 | 95.7 | 74 | `longbow_recurve_desert_bow` | 150 | 39.1 | no | yes |
| 6 | B | Chosen Wolf | wolfskins_tier_3 | battania | 3 | 48.0 | 89.6 | 71 | `woodland_longbow` | 140 | 45.3 | yes |  |
| 7 | B | Sturgian Veteran Bowman | sturgian_veteran_bowman | sturgia | 3 | 47.9 | 88.0 | 61 | `nordic_shortbow` | 150 | 44.8 | no |  |
| 8 | B | Khuzait Marksman | khuzait_marksman | khuzait | 5 | 47.0 | 93.3 | 72 | `nomad_bow` | 140 | 36.5 | no |  |
| 9 | B | Veteran Forester | forest_people_tier_3 | sturgia | 3 | 45.8 | 93.0 | 70 | `woodland_longbow` | 140 | 36.1 | no |  |
| 10 | B | Arboreal | brotherhood_of_woods_tier_3 | vlandia | 3 | 45.6 | 93.9 | 71 | `lowland_yew_bow` | 140 | 28.4 | no |  |
| 11 | B | Conspiracy Hunt Leader | conspiracy_hunt_leader | empire | – | 44.0 | 79.4 | 57 | `steppe_war_bow` | 160 | 23.5 | no |  |
| 12 | B | Nord Marksman | nord_marksman | nord | 4 | 43.8 | 91.1 | 70 | `lowland_yew_bow` | 140 | 36.1 | no | yes |
| 13 | B | Imperial Palatine Guard | imperial_palatine_guard | empire | 4 | 41.3 | 86.2 | 60 | `lowland_longbow` | 140 | 46.1 | no |  |
| 14 | B | Battanian Hero | battanian_hero | battania | 3 | 40.9 | 89.7 | 64 | `woodland_yew_bow` | 140 | 31.1 | no |  |
| 15 | C | Khuzait Tengichi | khuzait_sailor | khuzait | 5 | 33.9 | 79.2 | 54 | `composite_steppe_bow` | 130 | 33.0 | no | yes |

**Why.** `ranged_role_score = ranged_score_base × 0.78 × ranged_skill_factor × mobility_factor +
defense_score_base × 0.10 + 8 (horse) + 3 (shield)`, with
`ranged_skill_factor = clip(max(Bow, Crossbow)/220, 0.25, 1.15)` and
`ranged_score_base = norm100(bow_damage + ammo_thrust + 0.35·speed_rating + 0.15·accuracy +
0.10·missile_speed + 0.25·min(ammo_stack, 64))`. Unlike melee, **these are real item stats** —
bows and arrows resolve as direct `Item` rows with damage, speed and accuracy present.

- `ranged_score_base` is compressed: ranks 1-14 span only 79.4-95.7, because every serious bow in
  the game is within ~15% of every other one on this composite. **`Bow` skill is what actually
  separates archers.** `battanian_fian_champion` (Bow 260) and `battanian_fian` (Bow 200) share the
  identical `woodland_longbow` and identical `ranged_score_base` 94.3, and finish 98.0 vs 74.9.
- `conspiracy_longbowman` has that same bow and base at Bow 150 → 54.6. The three are a clean
  controlled demonstration that the ladder is skill-driven.
- The Fian Champion's Bow 260 is **clipped**: `ranged_skill_factor` caps at 1.15, i.e. skill 253.
  The last 7 points of Bow buy nothing in this model.
- `aserai_marine_t5` (Aserai Bahriyyah) owns the pool's best bow line —
  `longbow_recurve_desert_bow`, `ranged_damage` 74, `ranged_score_base` 95.7 — and only Bow 150.

**Surprises.** `aserai_marine_t5` at **tree_tier 2** ranks 5th, above every Khuzait, Sturgian,
Imperial and Vlandian archer, on equipment alone; it is NavalDLC content and the best-equipped
bowman in the track. `wolfskins_tier_3`, `forest_people_tier_3` and `brotherhood_of_woods_tier_3`
(all T3 minor clans) sit inside the top ten. `imperial_palatine_guard` is the Empire's best bow at
rank 13 — the Empire has no competitive archer in this track. Battania holds ranks 1, 2, 4, 6, 14.

---

## 4. Crossbow

Pool 12 (2 NavalDLC) — the whole pool is shown. Tiers: S 2, A 3, B 3, C 2, D 2.
Only Vlandia (10) and the Empire (2) field crossbows in this track.

| rank | tier | troop_name | troop_id | culture | tree_tier | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Crossbow | effective_armor | has_shield | naval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Vlandian Sharpshooter | vlandian_sharpshooter | vlandia | – | 62.6 | 100.0 | 102 | `crossbow_f` | 150 | 42.8 | yes |  |
| 2 | S | Conspiracy Warworn Crossbowman | conspiracy_warworn_crossbowman | vlandia | – | 61.4 | 97.6 | 102 | `crossbow_f` | 150 | 37.5 | yes |  |
| 3 | A | Vlandian Marinier | vlandian_marine_t5 | vlandia | 5 | 51.6 | 92.9 | 90 | `crossbow_g` | 150 | 39.2 | no | yes |
| 4 | A | Imperial Sergeant Boatsman | imperial_sergeant_crossbowman | empire | 4 | 46.3 | 95.2 | 95 | `crossbow_d` | 130 | 43.7 | yes |  |
| 5 | A | Boar Champion | company_of_the_boar_tier_3 | vlandia | 3 | 44.2 | 92.8 | 95 | `crossbow_d` | 130 | 34.1 | yes |  |
| 6 | B | Vlandian Seafarer | vlandian_marine_t4 | vlandia | 4 | 30.4 | 88.6 | 89 | `crossbow_g` | 100 | 23.4 | yes | yes |
| 7 | B | Boar Veteran | company_of_the_boar_tier_2 | vlandia | 2 | 26.4 | 82.3 | 84 | `crossbow_b` | 100 | 23.7 | yes |  |
| 8 | B | Imperial Coastguard | imperial_crossbowman | empire | 3 | 26.0 | 95.2 | 95 | `crossbow_d` | 100 | 22.4 | no |  |
| 9 | C | Conspiracy Trained Crossbowman | conspiracy_trained_crossbowman | vlandia | – | 15.5 | 82.3 | 84 | `crossbow_b` | 80 | 33.6 | no |  |
| 10 | C | Boar Novice | company_of_the_boar_tier_1 | vlandia | 1 | 14.0 | 82.3 | 84 | `crossbow_b` | 70 | 19.7 | yes |  |
| 11 | D | Vlandian Shipmate | vlandian_infantry | vlandia | 3 | 9.9 | 82.6 | 81 | `crossbow_e` | 70 | 19.3 | no |  |
| 12 | D | Vlandian Levy Crossbowman | vlandian_levy_crossbowman | vlandia | 2 | 0.8 | 72.6 | 69 | `crossbow_a` | 40 | 13.4 | no |  |

**Why.** Same `ranged_role_score` formula as archers, so the two ladders are directly comparable
inside this track (both normalised over the same `ranged_role_score` column). Crossbows carry far
more raw punch — `ranged_damage` 69-102 vs 53-74 for bows — but the **Crossbow skill ceiling is
150 against Bow 260**, so `ranged_skill_factor` never exceeds 0.68 for a crossbowman. That is why
the best crossbow (62.6) sits between the Fian Champion (98.0) and the Fian (74.9): the model says
Vlandia's answer to Battania is a good but not elite missile troop.

- `crossbow_f` (`ranged_damage` 102) is the ceiling item; `vlandian_sharpshooter` and
  `conspiracy_warworn_crossbowman` both carry it at Crossbow 150 and separate only on armour
  (42.8 vs 37.5).
- `imperial_crossbowman` (rank 8) has the same `crossbow_d` / `ranged_score_base` 95.2 as
  `imperial_sergeant_crossbowman` (rank 4); the entire 20-point gap is Crossbow 100 vs 130 plus a
  shield.
- 7 of 12 carry a shield, worth a flat +3 — enough to reorder adjacent entries but not tiers.

**Surprises.** The track's best crossbowman, `vlandian_sharpshooter`, has **no tree_tier**
(`special_or_unlinked`) — as with the line-infantry elites, the upgrade graph does not reach the
best unit. `company_of_the_boar_tier_3` (T3 minor clan) out-scores every Imperial crossbow except
the T4 sergeant. Both NavalDLC mariniers land in A/B on `crossbow_g`, making
`vlandian_marine_t5` the best *tiered* crossbow in the track.

---

## 5. Thrower

Pool 34 (10 NavalDLC). Tiers: S 1, A 1, B 11, C 12, D 9.
**Read this ladder with the caveat below — rank 1 is a scale artifact and ranks 2+ are ordered by
Throwing skill, not by javelin quality.**

| rank | tier | troop_name | troop_id | culture | tree_tier | skirmisher_role_score | throw_score_base | throw_damage | throw_source | direct_throw_item | crafted_throw_item | Throwing | naval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Flame | embers_of_flame_tier_2 | empire | 2 | 98.3 | 100.0 | 57 | direct_Thrown | `sling_reinforced` | – | 50 |  |
| 2 | A | Puppeteer | hidden_hand_tier_3 | empire | 3 | 70.8 | 23.1 | 0 | crafted_proxy | – | `leafblade_throwing_knife` | 160 |  |
| 3 | B | Khuzait Tengri | khuzait_Tengri | khuzait | 5 | 68.5 | 24.4 | 0 | crafted_proxy | – | `spear_blade_10_hewns` | 110 | yes |
| 4 | B | Battanian Falxman | battanian_falxman | battania | 4 | 61.1 | 23.1 | 0 | crafted_proxy | – | `woodland_throwing_axe_1_t1` | 100 |  |
| 5 | B | Battanian Skipari | battanian_marine_t5 | battania | 2 | 58.7 | 24.4 | 0 | crafted_proxy | – | `northern_javelin_6_t6` | 150 | yes |
| 6 | B | Battanian Wildling | battanian_wildling | battania | – | 53.0 | 24.4 | 0 | crafted_proxy | – | `northern_javelin_2_t3` | 130 |  |
| 7 | B | Skolder Veteran Broda | skolderbrotva_tier_3 | nord | 3 | 51.7 | 24.4 | 0 | crafted_proxy | – | `northern_javelin_3_t4` | 130 | yes |
| 8 | B | Lake Rat Wrecker | lakepike_tier_3 | sturgia | 3 | 49.5 | 24.4 | 0 | crafted_proxy | – | `western_javelin_3_t4` | 130 |  |
| 9 | B | Redshank | galloglass_tier_3 | battania | 3 | 49.1 | 24.4 | 0 | crafted_proxy | – | `northern_javelin_2_t3` | 120 |  |
| 10 | B | Aserai Lieutenant | aserai_veteran_infantry | aserai | 5 | 49.0 | 24.4 | 0 | crafted_proxy | – | `eastern_javelin_2_t3` | 120 |  |
| 11 | B | Imperial Naute | empire_marine_t5 | empire | 4 | 47.1 | 24.4 | 0 | crafted_proxy | – | `empire_javelin_1_t5` | 130 | yes |
| 12 | B | Sturgian Heavy Spearman | sturgian_shock_troop | sturgia | – | 46.2 | 24.4 | 0 | crafted_proxy | – | `northern_javelin_3_t4` | 80 |  |
| 13 | B | Hidden Soldati | hidden_hand_tier_2 | empire | 2 | 43.7 | 23.1 | 0 | crafted_proxy | – | `lowland_throwing_knife` | 130 |  |
| 14 | C | Triarii | legion_of_the_betrayed_tier_3 | empire | 3 | 35.8 | 24.4 | 0 | crafted_proxy | – | `empire_javelin_1_t4` | 80 |  |
| 15 | C | Battanian River Raider | battanian_marine_t4 | battania | 1 | 35.4 | 24.4 | 0 | crafted_proxy | – | `northern_javelin_6_t6` | 100 |  |

**Why, and why this ladder is weak.** `skirmisher_role_score = throw_score_base × 0.65 ×
throw_skill_factor + crafted_melee_score_base × 0.15 + defense_score_base × 0.10 + 6 (horse)`,
`throw_skill_factor = clip(Throwing/160, 0.25, 1.20)`, and
`throw_score_base = norm100(max(direct_throw_raw, crafted_throw_raw))` where
`direct_throw_raw = real_damage + 0.20·speed_rating + 0.50·stack_amount` but
`crafted_throw_raw = melee_proxy × 0.55` — a **flat constant per template class**
(javelin 36 × 0.55 = 19.8; throwing axe/knife 34 × 0.55 = 18.7).

- **33 of 34 throwers in this track use crafted javelins/axes**, so their `throw_score_base` takes
  only two values in the whole pool: 24.4 or 23.1. `throw_damage` is literally 0 for all of them.
  A `northern_javelin_6_t6` and a `northern_javelin_2_t3` score identically.
- Consequence: below rank 1, `skirmisher_role_score` is driven by `Throwing` skill and by the
  melee/defence side terms, **not by the throwing weapon**. `battanian_marine_t5` (Throwing 150,
  best javelin in the list) ranking below `khuzait_Tengri` (Throwing 110) is the side terms talking.
- **Rank 1 is not a javelin troop.** `embers_of_flame_tier_2` is the only pool member with a direct
  `Thrown` item, and that item is `sling_reinforced` — a **sling**, with `thrust_damage` 57 and no
  `stack_amount`. Real stats resolve, so it takes `throw_score_base = 100` while every real
  skirmisher is capped at 24.4, and it wins the role at Throwing 50. Across the entire audit only
  four direct `Thrown` ids exist (`throwing_stone`, `sling_wool`, `sling_braided`,
  `sling_reinforced`) and they belong to villagers, bandits and this one minor-clan troop.
- Treat **rank 2+ as the real thrower ladder**, and treat it as a skill ranking.

**Surprises.** `hidden_hand_tier_3` (Puppeteer, T3) at Throwing 160 is the highest-skilled thrower
in the track. Two units make the top 5 of both this ladder and the shock-infantry ladder:
`khuzait_Tengri` (NavalDLC T5, thrower 3 / shock inf 2) and `embers_of_flame_tier_2` (T2 minor clan,
thrower 1 / shock inf 5) — genuine dual-role melee-skirmishers, though the latter's rank here is the
sling artifact. Battania holds 4 of the top 9.

---

## 6. Shock cavalry

Pool 41, **0 NavalDLC** (see the naval section — this track has no mounted marine or Nord troop).
Tiers: S 2, A 5, B 15, C 11, D 8. Ranked by the descriptive `shock_cav_index_desc` defined above.

| rank | tier | troop_name | troop_id | culture | tree_tier | shock_cav_index_desc | mount_index_desc | mount_raw | offensive_melee_role_score | defensive_role_score | Polearm | Riding | harness_armor | armor_total | naval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Vlandian Banner Knight | vlandian_banner_knight | vlandia | 5 | 92.2 | 100.0 | 62.3 | 78.3 | 98.9 | 260 | 200 | 64.0 | 202.0 |  |
| 2 | S | Imperial Elite Cataphract | imperial_elite_cataphract | empire | 5 | 85.4 | 86.4 | 59.5 | 77.8 | 100.0 | 250 | 200 | 75.0 | 207.7 |  |
| 3 | A | Vlandian Champion | vlandian_champion | vlandia | 4 | 82.5 | 100.0 | 62.3 | 54.5 | 89.9 | 160 | 130 | 64.0 | 171.0 |  |
| 4 | A | Vlandian Knight | vlandian_knight | vlandia | 3 | 76.3 | 100.0 | 62.3 | 40.9 | 79.9 | 110 | 100 | 64.0 | 161.7 |  |
| 5 | A | Imperial Cataphract | imperial_cataphract | empire | 4 | 75.9 | 86.4 | 59.5 | 54.5 | 90.6 | 160 | 130 | 75.0 | 174.3 |  |
| 6 | A | Aserai Vanguard Faris | aserai_vanguard_faris | aserai | 5 | 68.0 | 62.9 | 54.7 | 64.5 | 93.2 | 200 | 170 | 58.0 | 207.3 |  |
| 7 | A | Vlandian Vanguard | vlandian_vanguard | vlandia | 5 | 65.2 | 73.1 | 56.8 | 46.2 | 83.2 | 130 | 130 | 52.0 | 153.7 |  |
| 8 | B | Sturgian Druzhinnik Champion | druzhinnik_champion | sturgia | 5 | 62.2 | 51.4 | 52.3 | 62.7 | 96.7 | 190 | 170 | 55.0 | 208.0 |  |
| 9 | B | Vlandian Gallant | vlandian_gallant | vlandia | 2 | 58.7 | 73.1 | 56.8 | 36.1 | 63.6 | 100 | 70 | 15.0 | 115.0 |  |
| 10 | B | Khuzait Heavy Lancer | khuzait_heavy_lancer | khuzait | 5 | 58.7 | 60.9 | 54.3 | 45.9 | 81.0 | 130 | 150 | 38.0 | 187.7 |  |
| 11 | B | Vlandian Cavalry | vlandian_cavalry | vlandia | 4 | 58.0 | 73.1 | 56.8 | 37.4 | 56.2 | 110 | 120 | 10.0 | 118.3 |  |
| 12 | B | Imperial Heavy Horseman | imperial_heavy_horseman | empire | 3 | 55.9 | 54.6 | 53.0 | 49.8 | 74.6 | 150 | 110 | 60.0 | 139.0 |  |
| 13 | B | Khuzait Lancer | khuzait_lancer | khuzait | 4 | 54.5 | 60.9 | 54.3 | 37.4 | 72.7 | 100 | 100 | 38.0 | 135.0 |  |
| 14 | B | Conspiracy Mounted Fighter | conspiracy_mounted_fighter | empire | – | 53.1 | 54.6 | 53.0 | 49.5 | 56.1 | 160 | 120 | 15.0 | 118.0 |  |
| 15 | B | Ghulam | ghilman_tier_3 | aserai | 3 | 53.0 | 51.5 | 52.3 | 48.9 | 68.1 | 150 | 150 | 10.0 | 178.0 |  |

**Why.** The mount is half the index and mounts are shared per culture per tier, so
`mount_index_desc` is effectively a **culture** term:

| horse item | speed | maneuver | charge | extra HP | mount_raw | users |
|---|---|---|---|---|---|---|
| `t3_vlandia_horse` | 49 | 68 | 32 | 60 | 62.3 | Vlandian Banner Knight / Champion / Knight |
| `t3_empire_horse` | 59 | 66 | 28 | 20 | 59.5 | Imperial (Elite) Cataphract |
| `t3_aserai_horse` | 65 | 73 | 20 | 20 | 54.7 | Aserai Vanguard Faris |
| `t3_khuzait_horse` | 60 | 77 | 20 | 35 | 54.3 | Khuzait Heavy Lancer; Khan's Guard (horse-archer pool) |
| `aserai_horse` | 54 | 59 | 14 | 0 | 41.8 | Aserai Mamluke Cavalry (track minimum) |

- Vlandia's `t3_vlandia_horse` wins on the two terms that matter for a charge — charge damage 32
  (highest in the track) and +60 HP — despite being the *slowest* elite horse at speed 49. Aserai
  and Khuzait mounts are faster and far more agile but hit for 20.
- The rider side is where Vlandia's lead narrows: `vlandian_banner_knight` and
  `imperial_elite_cataphract` are within 0.5 on `offensive_melee_role_score` (78.3 / 77.8) and the
  cataphract leads on armour (`harness_armor` 75 vs 64, `defensive_role_score` 100.0 vs 98.9). The
  7-point index gap is almost entirely the horse.
- `druzhinnik_champion` (rank 8) has the pool's **best armour** (`armor_total` 208.0) and third-best
  melee, and is held back only by `t2_sturgia_horse` on two of its three rosters
  (`mount_index_desc` 51.4). Under a mount-agnostic weighting it would be top four — flagged
  because the ranking is sensitive to my 0.50 mount weight here.
- 40 of the 41 entries have `TwoHandedPolearm` as best melee template (the lone exception is a
  `OneHandedAxe`/`OneHandedSword` rider), so `crafted_melee_score_base` takes just two values in
  this pool — 60.5 and 46.8 — and `offensive_melee_role_score` reduces to a
  Polearm/OneHanded-skill ranking.

**Surprises.** `vlandian_knight` at **tree_tier 3** ranks 4th — ahead of Sturgia's and Khuzait's T5
elites — and `vlandian_gallant` at **T2** ranks 9th, ahead of `khuzait_heavy_lancer` (T5). Both ride
on the shared Vlandian T3 horse: the cheapest genuinely dangerous charge in the track is a Vlandian
mid-tier. `ghilman_tier_3` (T3 minor clan, 53.0) lands within 1.5 points of `khuzait_lancer` (T4,
54.5). Khuzait, the culture with the best mounted *reputation*, has no shock-cavalry entry above
rank 10.

---

## 7. Horse archer

Pool 22, **0 NavalDLC**. Tiers: S 1, A 0, B 9, C 6, D 6.
Ranked by `ranged_role_score` (which already contains the mobility bonus); `mount_index_desc` is
shown as context and is **normalised inside this pool only** — it is not comparable to the
shock-cavalry column of the same name.

| rank | tier | troop_name | troop_id | culture | tree_tier | ranged_role_score | ranged_score_base | ranged_damage | ranged_item | Bow | Crossbow | Riding | mount_index_desc | effective_armor | naval |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Khuzait Khan's Guard | khuzait_khans_guard | khuzait | 5 | 100.0 | 83.1 | 56 | `steppe_war_bow` | 220 | 25 | 200 | 100.0 | 54.6 |  |
| 2 | B | Khuzait Kheshig | khuzait_kheshig | khuzait | 4 | 69.0 | 83.1 | 56 | `steppe_war_bow` | 160 | 20 | 130 | 100.0 | 44.1 |  |
| 3 | B | Aserai Mamluke Heavy Cavalry | aserai_mameluke_heavy_cavalry | aserai | 5 | 66.9 | 79.9 | 58 | `steppe_war_bow` | 150 | 20 | 130 | 40.2 | 42.5 |  |
| 4 | B | Veteran Eleftheroi | eleftheroi_tier_3 | empire | 3 | 61.1 | 87.5 | 87 | `crossbow_g` | 45 | 140 | 130 | 27.5 | 28.8 |  |
| 5 | B | Imperial Bucellarii | bucellarii | empire | 4 | 59.4 | 84.4 | 57 | `steppe_war_bow` | 140 | 60 | 120 | 89.6 | 39.5 |  |
| 6 | B | Khuzait Heavy Horse Archer | khuzait_heavy_horse_archer | khuzait | 5 | 56.8 | 79.2 | 54 | `composite_steppe_bow` | 130 | 20 | 130 | 56.2 | 39.4 |  |
| 7 | B | Karakhergit Elder | karakhuzaits_tier_3 | khuzait | 3 | 53.4 | 77.5 | 55 | `steppe_war_bow` | 140 | 15 | 100 | 59.8 | 44.2 |  |
| 8 | B | Aserai Mamluke Cavalry | aserai_mameluke_cavalry | aserai | 4 | 51.3 | 77.4 | 56 | `steppe_heavy_bow` | 120 | 15 | 110 | 0.0 | 38.0 |  |
| 9 | B | Conspiracy Mounted Master Archer | conspiracy_mounted_master_archer | khuzait | – | 49.8 | 81.5 | 54 | `composite_steppe_bow` | 120 | 20 | 130 | 56.2 | 38.9 |  |
| 10 | B | Conspiracy Packmaster | conspiracy_packmaster | empire | – | 49.4 | 83.8 | 56 | `steppe_war_bow` | 120 | 20 | 130 | 89.6 | 31.5 |  |
| 11 | C | Khuzait Horse Archer | khuzait_horse_archer | khuzait | 4 | 38.6 | 80.6 | 54 | `steppe_heavy_bow` | 100 | 15 | 100 | 56.2 | 31.7 |  |
| 12 | C | Karakhergit Rider | karakhuzaits_tier_2 | khuzait | 2 | 37.0 | 75.1 | 53 | `steppe_heavy_bow` | 110 | 10 | 60 | 56.2 | 29.7 |  |
| 13 | C | Khuzait Torguud | khuzait_torguud | khuzait | 3 | 36.8 | 75.9 | 54 | `steppe_heavy_bow` | 100 | 15 | 100 | 56.2 | 37.4 |  |
| 14 | C | Expert Eleftheroi | eleftheroi_tier_2 | empire | 2 | 36.0 | 81.5 | 79 | `crossbow_e` | 30 | 100 | 100 | 27.5 | 14.3 |  |
| 15 | C | Khuzait Raider | khuzait_raider | khuzait | 3 | 22.9 | 81.0 | 53 | `composite_bow` | 70 | 10 | 70 | 0.4 | 17.2 |  |

**Why.** Same `ranged_role_score` as foot missile troops plus `mobility_factor =
clip(1 + 0.08 + Riding/1000, 1.0, 1.25)` and a flat +8 for having a horse. `khuzait_khans_guard` is
the only S in the role and the gap to rank 2 is enormous (100.0 → 69.0) for one reason: **Bow 220
against 160**, on the identical `steppe_war_bow` with the identical `ranged_score_base` 83.1 and
the identical `t3_khuzait_horse`. Riding 200 vs 130 adds only ~5% through `mobility_factor`, which
saturates at 1.25.

- The `ranged_score_base` spread across the pool is 75.1-87.5 — again compressed, again meaning
  **skill is the ranking**.
- **Mounted crossbows land here:** `eleftheroi_tier_3` and `eleftheroi_tier_2` carry `crossbow_g` /
  `crossbow_e`. Their `ranged_damage` (87, 79) is the highest in the pool by 30 points, but
  `ranged_skill_factor` reads `max(Bow, Crossbow)` = 140 / 100 vs a Khan's Guard 220, so they place
  4th and 14th. `eleftheroi_tier_3` at T3 with `effective_armor` 28.8 out-ranking Khuzait's T5
  heavy horse archer is worth knowing.
- `aserai_mameluke_cavalry` shows the mount floor: plain `aserai_horse` (charge 14, no extra HP)
  → `mount_index_desc` 0.0. It still ranks 8th because the mount barely enters
  `ranged_role_score`; the flat +8 is all a horse is worth to a shooter in this model.

**Surprises.** Khuzait holds 14 of 22 slots but only two inside the top five. `bucellarii` (Empire, T4) and
`karakhuzaits_tier_3` (T3 minor clan) both beat three Khuzait culture-tree horse archers.
`aserai_mameluke_heavy_cavalry` at rank 3 is the best non-Khuzait horse archer in the track.

---

## NavalDLC / marine coverage

NavalDLC (War Sails) is **in scope and retained**: 44 of the 256 pool troops (17%) are NavalDLC
content, 42 of which appear in a role ladder. Breakdown:

| group | ids | in pool | where they land |
|---|---|---|---|
| Nord culture (whole faction) | 23 × `nord_*`, plus `guard_nord`, `sea_hounds_marksman`, `skolderbrotva_tier_{1,2,3}` | 28 | 21 Infantry / 7 Ranged (`default_group`); line infantry 1/4/11/15/…, archer 3/12/25/35/36, shock infantry 8/14/16/21/28/45 |
| Empire marines | `empire_marine_t2..t5` | 4 | line infantry 31/43/58, shock infantry 42, thrower 11/16/26/34 |
| Sturgian marines | `sturgia_marine_t3..t5` | 3 | line infantry 21/32/63 |
| Vlandian marines | `vlandian_marine_t4`, `vlandian_marine_t5` | 2 | crossbow 6 (t4), 3 (t5) |
| Aserai marines | `aserai_marine_t4`, `aserai_marine_t5` | 2 | archer 22 (t4), **5 (t5)** |
| Battanian marines | `battanian_marine_t4`, `battanian_marine_t5` | 2 | thrower 15 (t4), 5 (t5); line infantry 44 / 23 |
| Khuzait sailors | `khuzait_spear_sailor`, `khuzait_sailor`, `khuzait_Tengri` | 3 | shock infantry 2/22, archer 15, thrower 3/20 |

Naval share per role: line infantry 23/83, thrower 10/34, shock infantry 9/45, archer 8/39,
crossbow 2/12, **shock cavalry 0/41, horse archer 0/22**.

Where NavalDLC matters most in this track:

- **`nord_huscarl` is the outright best line infantryman** (rank 1, `armor_total` 204.4) and
  `nord_hirdmann` is rank 4. Nord supplies 4 of the top 15 shielded infantry (ranks 1, 4, 11, 15).
- **`aserai_marine_t5` (Aserai Bahriyyah) has the best-equipped bow in the track** —
  `longbow_recurve_desert_bow`, `ranged_damage` 74, `ranged_score_base` 95.7 — at tree_tier 2.
- **`vlandian_marine_t5` (Vlandian Marinier) is the best *tiered* crossbow** (rank 3); the two
  units above it are both `special_or_unlinked`.
- `khuzait_Tengri` is a NavalDLC T5 that ranks top-3 shock infantry *and* top-3 thrower.
- `nord_skathi` (Nord Sky-Gods Chosen) is the best non-Battanian archer at rank 3, and one of only
  two shielded archers in the top 6.
- **NavalDLC contributes zero cavalry.** No `nord_*`, `*_marine_*` or sailor troop has a `Horse`
  slot in any roster. Excluding NavalDLC would remove an entire faction and the best line
  infantryman, but would not change either mounted ladder.
- Two NavalDLC archers, `nord_militia_archer` and `nord_militia_veteran_archer`, are absent from
  the archer ladder — see the data-quality note below; the cause is upstream, not a filter here.

---

## Data-quality findings (for the V4.4 model backlog — not applied here)

Recording these because they change how the tables above should be read. **No scorer formula was
touched.**

1. **Blank skill attributes silently NaN out three of four role scores.** 28 militia troops
   (4 per culture × 7 cultures) plus `huskarl_swordsman` ship with empty `OneHanded`/`TwoHanded`/
   `Polearm`/`Bow`/`Crossbow`/`Throwing`/`Riding` values. `generate_vanilla_role_scores.py:192-199`
   uses `float(first.get("Bow") or 0)`, which does **not** coerce a pandas `NaN` (NaN is truthy),
   so `float(nan) = nan` propagates into `ranged_skill_factor`, `melee_skill_factor` and
   `throw_skill_factor`. Result: `ranged_role_score`, `offensive_melee_role_score` and
   `skirmisher_role_score` are blank for all of them, while `defensive_role_score` — the one
   formula with no skill factor — still computes. **14 troops are therefore unrankable in this
   report** (all 7 cultures' `*_militia_archer` and `*_militia_veteran_archer`, including
   Vlandia's two militia crossbowmen and Nord's two militia archers). They are the entire gap
   between the 256-troop pool and the 242 troops that appear in at least one ladder. Suggested fix:
   `float(v) if pd.notna(v) else 0.0`.
2. **Slings are scored as thrown weapons.** `sling_reinforced` (`type == Thrown`, `thrust_damage`
   57) gives `embers_of_flame_tier_2` `throw_score_base = 100` and first place in the thrower role
   at Throwing 50, while every actual javelin troop is pinned at 24.4. A sling is a ranged weapon
   with separate `SlingStones` ammo (30 rows in the audit); it should not enter the skirmisher
   term, or should be scored with its ammo like a bow.
3. **Crafted throwing weapons have no damage, so the skirmisher ladder cannot see javelin
   quality.** `crafted_throw_raw = melee_proxy × 0.55` is a per-class constant; `throw_damage` is 0
   for 33 of 34 throwers. Until javelin stats are reconstructed, treat `skirmisher_role_score` as a
   Throwing-skill ranking.
4. **`crafted_class` classifies throwing axes as melee axes.** `crafted_class()`
   (`generate_vanilla_role_scores.py:42-60`) tests `"Axe"` before `"Throwing"`, so template
   `ThrowingAxe` returns `axe` (melee proxy 46, usability 0.88) instead of `throwing`. Visible in
   the tables: `nord_berserkr` and `nord_skjaldbrestir` carry `ThrowingAxe` as their *melee*
   template. Same ordering bug would hit a hypothetical `ThrowingMace`. `Pike` and `Dagger` fall
   through to `other` (proxy 40).
5. **Melee is entirely proxy.** All 3,723 `CraftedItem` weapon rows have
   `crafted_stats_reconstructed == False` and blank `swing_damage`/`thrust_damage`/`weapon_length`/
   `speed_rating`. Both melee-facing role scores are template-class rankings, which is why
   `crafted_melee_score_base` takes exactly **6 distinct values across all 256 troops**, one per
   template class: 100.0 `TwoHandedSword` · 60.5 `TwoHandedPolearm` · 46.8 `OneHandedSword` ·
   41.6 `OneHandedAxe`/`TwoHandedAxe`/`ThrowingAxe` · 34.5 `Mace`/`TwoHandedMace` · 0.0 `Dagger`
   (the `other` fallback, and the pool minimum). Note the two-handed variants score identically to
   their one-handed namesakes for axes and maces. Rank ordering *within* a class is trustworthy;
   ordering *across* classes is the proxy table talking.
6. **`SCHEMA.md` item_kind values are stale.** SCHEMA documents `item_kind` as `direct` / `crafted`;
   the shipped CSVs use `Item` / `CraftedItem`. Cosmetic, but a filter written from the docs
   silently matches nothing. (`analysis_pack/SCHEMA.md` is not owned by this task.)
7. **The best unit in three roles has no upgrade tier.** `vlandian_sharpshooter` (crossbow rank 1),
   `sturgian_shock_troop` / `sturgian_veteran_warrior` / `imperial_legionary` / `battanian_wildling`
   / `aserai_master_archer` (line infantry top 9) are all `line_status = special_or_unlinked` in
   `nightmare_sails_tree_tiers.csv`. Since `upgrade_requires` is not modelled (SCHEMA §Known
   limitations), this pack cannot say how a player reaches them.

---

## Companion files

Full ranked pools (not just the top 15), same columns as the tables plus every driver, written
next to this report:

| file | rows | ranked by |
|---|---|---|
| `role_report_shock_infantry.csv` | 45 | `offensive_melee_role_score` |
| `role_report_line_infantry.csv` | 83 | `defensive_role_score` |
| `role_report_archer.csv` | 39 | `ranged_role_score` |
| `role_report_crossbow.csv` | 12 | `ranged_role_score` |
| `role_report_thrower.csv` | 34 | `skirmisher_role_score` |
| `role_report_shock_cavalry.csv` | 41 | `shock_cav_index_desc` |
| `role_report_horse_archer.csv` | 22 | `ranged_role_score` |

Each carries `rank`, `tier`, identity (`troop_id`, `culture`, `tree_tier`, `level`, `line_status`,
`default_group`, `primary_category`), provenance (`naval`, `change_type`, `roster_n`), all four
`role_scores_v1` scores and score bases, the descriptive `mount_index_desc` /
`shock_cav_index_desc` / `mount_raw` / `harness_armor`, the roster shares (`shield_share`,
`twoh_share`, `horse_share`), all eight skills, and the resolved item ids. A troop may appear in
more than one file (e.g. `khuzait_Tengri` in shock infantry and thrower) — the pools are
role-membership views, not a partition.

Secondary context, not rewritten by this report: `OVERVIEW.md` (same export dir) for the four
model-category ladders and the field-empiria table, `REPORT.md` for run provenance.
