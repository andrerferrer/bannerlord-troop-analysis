# Cross-track index — soldier ROLE_REPORTs, `export_20260731_150800`

> ## ⚠️ NON-COMPARABILITY WARNING — READ FIRST
>
> **Scores from different tracks are not comparable. No normalization exists yet.**
>
> Every `role_scores_v1` number is a min–max normalisation computed **inside one track's own
> troop universe**. A `ranged_role_score` of 98.0 in `nightmare_sails` and 85.7 in
> `realm_of_thrones` do not mean the first archer is better — they mean each is near the top of
> a *different* ladder, over a different population, with a different denominator. Adding,
> averaging, sorting or joining scores across tracks produces a number with no meaning.
>
> **This document contains no merged, pooled or cross-track ranking, and none may be derived
> from it.** Side-by-side tables below place each track's own ladder leader next to the others
> for *narrative* reading only — the columns are four separate ladders printed adjacently, never
> one ordering. Rows are never sorted by score across tracks.
>
> The blockers to any future normalization are structural, not cosmetic — see
> *Shared data limitations* (§2) and *Method divergences* (§4). At minimum, a stated
> normalization would first have to fix: hollow melee/thrown damage (§2.1), a common troop
> universe rule (§2.3), one S+ outlier criterion (§2.4), one roster-aggregation convention
> (§4.2) and one tier-band table (§4.3). None of those is settled today.
>
> Intra-track only (ADR-003, `SCHEMA.md:100`). Read each track's own ROLE_REPORT for anything
> beyond navigation.

- SSOT pin: `export_20260731_150800` + `analysis_pack/` (ADR-003).
- Package digest: `fc87e360e884cc9aa4baa15e4bdd372824c1f7054b2a9acef6d8c0df3732db3b`
  (`data/xml_exports/export_20260731_150800/PACKAGE.json:expected_package_sha256`, recomputed
  from `artifact_hashes.csv` over 102 rows — matches, so `OVERVIEW_INDEX.md` is current and was
  not touched by this task).
- Evidence basis for all four tracks: `xml_structural` (ADR-004). `empirical = false`.
  Zero battle-derived quantities anywhere in this run.
- Model: `role_scores_v1` conservative, `score_status = role_scores_v1_conservative_not_final`.
  No lane changed a scorer formula; every formula change is a V4.4 model PR.

---

## 1. The four reports

| track | ROLE_REPORT | branch / commit | universe analysed | companion CSVs |
|---|---|---|---|---|
| `vanilla` | [`vanilla/export_20260731_150800/ROLE_REPORT.md`](vanilla/export_20260731_150800/ROLE_REPORT.md) | `aferrer/role-report-vanilla` `41de266` | **283** soldiers, 784 rosters | 7 |
| `nightmare_sails` | [`nightmare_sails/export_20260731_150800/ROLE_REPORT.md`](nightmare_sails/export_20260731_150800/ROLE_REPORT.md) | `aferrer/role-report-ns` `6054d4a` | **256** troops, 759 troop×roster | 7 |
| `realm_of_thrones` | [`realm_of_thrones/export_20260731_150800/ROLE_REPORT.md`](realm_of_thrones/export_20260731_150800/ROLE_REPORT.md) | `aferrer/role-report-rot` `bb9f306` | **865** soldiers | 8 (incl. unscored-ranged) |
| `taom` | [`taom/export_20260731_150800/ROLE_REPORT.md`](taom/export_20260731_150800/ROLE_REPORT.md) | `aferrer/role-report-taom` `2eb8b09` | **870** mod-content troops (+283 vanilla-baseline appendix) | 7 |

The four universes are built by **four different filter chains** (§4.1) — the counts above are
not four measurements of one quantity.

Related, not restated here:

- `analysis/theoretical/OVERVIEW_INDEX.md` — the four-category OVERVIEW ladders and field-empiria
  status per track. Verified current; digest matches.
- `nightmare_sails/export_20260731_150800/THEORY_FIELD_JOIN.md`
  (`aferrer/ns-theory-field-join` `07a9e4c`) — exists; read it there.
- **`vanilla` has no `OVERVIEW.md` in its export directory.** Its ROLE_REPORT stands alone and
  has no OVERVIEW to be read against; `OVERVIEW_INDEX.md` correspondingly carries no vanilla row.

---

## 2. Shared data limitations

These are **not per-track quirks**. Each was found independently by more than one lane, and each
changes how *every* ranking in this run must be read.

### 2.1 Melee and thrown damage are hollow in every track

Independently reported by three lanes on their own data:

| track | evidence |
|---|---|
| `vanilla` | all **3,619** melee/throwing weapon rows are `CraftedItem`, `crafted_stats_reconstructed == False`, zero swing/thrust |
| `nightmare_sails` | all **3,723** melee rows `CraftedItem`, `crafted_stats_reconstructed == False`, blank `swing_damage`/`thrust_damage`/`weapon_length`/`speed_rating` |
| `realm_of_thrones` | all **3,501** crafted weapon rows on filtered soldiers are `CraftedWeapon`, blank swing and thrust; **zero** direct-`Item` melee weapons exist to fall back on |
| `taom` | **4,397** soldier rows (2,740 in the primary pool), all `CraftedWeapon`/`CraftedItem`, **0** with any damage; zero `OneHandedWeapon`/`TwoHandedWeapon`/`Polearm` typed rows in the whole track |

**Consequence: every melee, shock-infantry and thrower ranking in this run is a
weapon-template-name proxy, not a damage model.** The score orders *what a troop is holding*, by
crafting-template class, times a skill factor. It does not order how hard the troop hits.

The proxy collapses to a handful of constants. TAOM's observed values:
`TwoHandedSword` 100.0 · `TwoHandedPolearm` 81.96 · `OneHandedSword` 75.72 · `TwoHandedAxe` 73.33.
NS reports exactly **6 distinct** `crafted_melee_score_base` values across all 256 of its troops.
For throwing, TAOM collapses to a **single constant 30.46 for 14 of its 15 top throwers**; ROT to
two values (30.5 javelin / 28.8 knife); NS to two (24.4 / 23.1); vanilla to one (30.5) across its
whole javelin block.

Only the **archer, crossbow and horse-archer** ladders rest on real resolved item stats (bows,
crossbows and ammunition carry populated damage, accuracy, missile speed). Everything else in
this run is proxy.

Per-track quantification of the hole (troops affected, share of every role ladder, top-50
dependency), reproducible with stdlib only:
[`analysis/item_validation/CRAFTED_DAMAGE_COVERAGE_export_20260731_150800.md`](../item_validation/CRAFTED_DAMAGE_COVERAGE_export_20260731_150800.md)
and `scripts/analysis/quantify_crafted_damage_coverage.py`. Real reconstruction is **blocked**
on a PC export of `crafting_pieces*.xml` + `crafting_templates*.xml`, specified in
[`docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md`](../../docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md);
the consumer that will use it is `scripts/normalization/reconstruct_crafted_weapon_stats.py`,
which exits non-zero rather than fabricating a number.

### 2.2 Armor is fixed — for armor only

The Armory/Wargs fix held. TAOM shows **9,290 resolved armor rows across 870 troops, zero with a
zero armor value** (3 zeros out of 12,695 across all soldier rows), with plausible,
tier-consistent per-slot spot checks.

**State this precisely: the fix is confirmed for armor and NOT for melee.** Commit #42 must not
be read as a blanket "TAOM fixed" — the same track's melee and thrown damage are still entirely
hollow (§2.1), and a new mount defect was found (§2.6). Armor-driven columns
(`defense_score_base`, `armor_total`, `effective_armor`) are trustworthy; melee-driven ones are
not.

### 2.3 Troop universe ruling — and the pack defect behind it

**Coordinator ruling for this run: universe = soldiers minus `mp_*` only.**

Obsolete troops are **unidentifiable from `analysis_pack`**: there is no `is_obsolete` flag and
no `source_xml` column for troops, and raw module XML is deliberately absent. All four lanes hit
this independently. `SCHEMA.md:88-90` cites a clean vanilla baseline of **272**; the `mp_` prefix
accounts for only 84 of the 95 ids that number removes, leaving ~11 non-`mp_*` obsolete soldiers
that cannot be found. **Vanilla is therefore 283, not 272.**

Corroboration worth noting: TAOM's retained-vanilla-baseline appendix independently arrives at
**283** for the same population, by a different filter chain.

**Record this as an open pack-side defect** — emit `is_obsolete` or a `source_xml` column for
troops at the export layer. A name-prefix heuristic was explicitly rejected by the vanilla lane
as unverifiable by a later reader and prone to drift per track. Practical effect: the ~11
unidentified ids sit inside the ranking universe *and* inside the v1 min–max normalisation, so
they move every vanilla number slightly. Two of the suspects (`imperial_legionary`,
`vlandian_sharpshooter`) are `CONTROL_IDS` anchors of the frozen scorer — a second reason not to
strike them by hand.

### 2.4 The S+ outlier criterion diverged between lanes — needs one owner

Three different rules were applied, not two:

| track | criterion used | result |
|---|---|---|
| `vanilla` | OVERVIEW giant/mammoth name regex, verbatim | **0** matches (expected — outsized units are mod content) |
| `nightmare_sails` | same regex, pattern printed in the report | **0** matches |
| `realm_of_thrones` | name regex **widened**: name regex (4 troops) **plus** any mount with `horse_charge_damage >= 200` (3 troops) | **7** rows across 4 roles |
| `taom` | **not the name regex** — structural detection by mount id (`taom_mumakil`, `taom_war_elephant`, `taom_chariot_a`) plus `cave_troll` enumerated as a foot unit | **5** units |

**Do not silently harmonize these.** Two consequences to record:

1. ROT's widening parks **3 Volantene elephant mahouts** next to the 4 giants — including
   `golden_elite_pikeman` (Golden Company Mahout), a **ROT priority anchor** in its `REPORT.md`
   and the top of the OVERVIEW's Skirmisher list. ROT's own report says to read that troop's
   skirmisher standing from the OVERVIEW, not from its thrower table.
2. TAOM's criterion is structural rather than name-based, which the coordinator brief recorded as
   "the OVERVIEW regex" — flagging the discrepancy rather than papering over it. TAOM's rule
   would not fire on ROT's elephants (different mount ids) and ROT's rule would not fire on
   TAOM's `cave_troll` (a foot unit, no mount).

**The criterion needs one owner and one definition.** Until then, "S+" means three different
things in this run, and the S–D bands beneath it are computed against three differently-chosen
"best non-outlier" leaders.

### 2.5 Unscorable troops from blank `skill_template`

`skill_template` is not modelled (`SCHEMA.md` "Known limitations"). Blank skills become NaN, and
because v1 multiplies the ranged, offensive-melee and skirmisher scores by a skill factor, the
product is NaN and the troop silently drops out of its own ladder. `defensive_role_score` has no
skill factor, so those troops still appear in the line-infantry ladders on kit alone.

Per-track counts — **these are not summable into a cross-track total**, the universes overlap and
differ:

| track | unscorable | of what | notes |
|---|---|---|---|
| `vanilla` | **18** | of 283 (45 have all eight skill columns blank) | 14 `skill_template` militia + **4 arena fighters with every melee skill blank but `Bow = 300`** — an implausible value no real troop carries and no bow in their kit could use; raise as an audit-side data question |
| `nightmare_sails` | **14** | of 256 | all 7 cultures' `*_militia_archer` / `*_militia_veteran_archer`, incl. Vlandia's two militia crossbowmen and Nord's two militia archers |
| `realm_of_thrones` | **46** ranged | of 865 (92 troops have blank skills) | 44 bow + 2 crossbow, militia/city-watch lines across 23 cultures; preserved in `role_report_unscored_ranged.csv` |
| `taom` | not reported as a distinct count | — | TAOM's own open items list does not raise a NaN-skill population |

NS traced the mechanism to source: `generate_vanilla_role_scores.py:192-199` uses
`float(first.get("Bow") or 0)`, which does not coerce a pandas `NaN` (NaN is truthy), so
`float(nan) = nan` propagates. Suggested fix, for the V4.4 backlog:
`float(v) if pd.notna(v) else 0.0`.

### 2.6 `item_found == True` is not proof of usable stats

A new class of defect, found by TAOM, that the `unknown_items` review queue **structurally cannot
catch**: items that resolve successfully (`item_found == True`) but carry a blank `type` and no
stats, because load-order resolution picks a stat-less reference stub over the real definition.

| item id | stub that wins | real definition (with stats) |
|---|---|---|
| `warg_dark`, `warg_brown`, `warg_albino` | `TAOM/ModuleData/culture_marketplace/culture_marketplace_config.xml` — type blank, no stats | `Alliance.Wargs/ModuleData/Items/LOTR/lotr_warg.xml` — `Horse`, speed 48, maneuver 70, charge 6–8 |
| `northern_round_shield` | `NavalDLC/ModuleData/items.xml` — type blank, no stats | `SandboxCore/ModuleData/items/shields.xml` — `Shield`, 300 HP, shield_armor 5 |

TAOM's queue is otherwise clean (41 rows, all severity `allowed`, all on two MP test troops
removed by filtering — zero unknown items touch its primary pool), which is exactly why this
class hides. Blast radius: **20 warg-rider troops in TAOM's shock-cavalry pool read
charge/speed/maneuver = 0** and occupy the ladder floor. TAOM's own sensitivity check (real warg
stats substituted) moves them from ranks 97–116 to roughly 83–100 — real defect, **bounded**
impact; read those ranks as *unknown, probably bottom-third*, not as measured. TAOM left the
table uncorrected on purpose, since correcting it would mean patching the SSOT.

Related, from ROT: **the scorer does not apply the `item_found` filter at all** —
`generate_vanilla_role_scores.py` reads the audit CSV unfiltered. ROT's blast radius is 11
soldier rows across 9 troops (0.07%), so its published columns remain usable, but the omission is
general.

Recommended follow-up (not done by any lane): have the export/catalog step prefer a definition
carrying a `type` over a stat-less same-id reference, and add a `resolved_but_untyped` counter to
the audit summary.

### 2.7 NS-specific, and kept as such: `sling_reinforced`

`sling_reinforced` is scored as a **thrown** weapon and wins the NS thrower role outright. It is
a sling (`type == Thrown`, `thrust_damage` 57) with separate `SlingStones` ammunition; because
its stats resolve for real, `embers_of_flame_tier_2` takes `throw_score_base = 100` at Throwing
50 while every actual javelin troop in the track is pinned at 24.4.

This is filed as an **NS-track finding**, not a shared limitation — but the *shape* of the
artifact recurs and is worth reading together (§3, thrower row): vanilla's thrower ladder is
topped by the same mechanism (`hidden_hand_tier_2`, sling ammunition, `throw_base` 100.0 against
a flat 30.5 for every javelin troop), TAOM's single real-throw entry (`throwing_stone`,
`throw_damage` 2) ranks *below* javelin cavalry with no measured damage at all, and ROT has no
direct `Thrown` rows in its filtered pool whatsoever. Four tracks, four different manifestations
of one missing stat table.

---

## 3. Role-by-role narrative comparison

> **These are four separate ladders printed side by side. The columns do not share a scale, a
> denominator, a population or (for shock cavalry) even a metric. Do not compare the numbers
> across columns.** Each cell reads: leader — score *(pool size)*.

| role | `vanilla` | `nightmare_sails` | `realm_of_thrones` | `taom` |
|---|---|---|---|---|
| shock infantry | Conspiracy Knight `conspiracy_knight` — 66.1 *(37 of 41)* | Conspiracy Knight `conspiracy_knight` — 62.2 *(45)* | Mountain's Man `mountains_man` — 88.9 *(154)* | Imladris Blademaster `imladris_blademaster` — 93.09 *(128)* |
| line infantry | Vlandian Sergeant `vlandian_sergeant` — 62.2 *(90)* | Nord Huscarl `nord_huscarl` — 71.7 *(83)* | Tarly Vanguard `tarly_vanguard` — 47.8 *(318)* | Battlemaster of the First Age `battlemaster_of_the_first_age` — 69.22 *(358)* |
| archer | Battanian Fian Champion `battanian_fian_champion` — 92.4 *(38 of 50)* | Battanian Fian Champion `battanian_fian_champion` — 98.0 *(39)* | Qartheen Enthroned Guardian `enthroned_guardian` — 85.7 *(150)* | Imladris Marchwarden `imladris_marchwarden` — 74.53 *(158)* |
| crossbow | Conspiracy Warworn Crossbowman — 75.6 *(11 of 13)* | Vlandian Sharpshooter `vlandian_sharpshooter` — 62.6 *(12)* | Myrish Artisan of War `myrish_artisan` — 88.1 *(28)* | Iron Hills Veteran Sharpshooter — 57.88 *(32)* |
| thrower | Hidden Soldati `hidden_hand_tier_2` — 82.0 *(21)* ⚠ sling artifact | Flame `embers_of_flame_tier_2` — 98.3 *(34)* ⚠ sling artifact | Ghiscari Lockstep Legionnaire — 71.0 *(41)* | Riders of Rohan `rohan_…_supreme_rider` — 67.98 *(90)* |
| shock cavalry | Elite Cataphract / Banner Knight — 73.5 tie *(49)* ⚠ own index | Vlandian Banner Knight — 92.2 *(41)* ⚠ different index | Captain of the Kingsguard `mounted_kingsguard` — 71.9 *(159)* ⚠ `defensive_role_score` | Rohan West Emnet Heavy Shock Cavalry — 88.84 *(116)* ⚠ different index |
| horse archer | Khuzait Khan's Guard `khuzait_khans_guard` — 100.0 *(19)* | Khuzait Khan's Guard `khuzait_khans_guard` — 100.0 *(22)* | Mormont Mounted Huntress — 48.3 *(**3**)* | Rider of Himring `rider_of_himring` — 97.35 *(22)* |

### What the four ladders have in common

- **Ranged roles are skill ladders, everywhere.** In all four tracks the bow/crossbow kit is
  compressed into a narrow band (`ranged_score_base` spans ~79–96 in NS, ~75–88 in NS horse
  archer, 82–100 in ROT crossbow), so `ranged_skill_factor` does the separating. The cleanest
  demonstration is repeated in two tracks: the Battanian Fian Champion, Fian and Conspiracy
  Longbowman carry the *identical* `woodland_longbow` and identical `ranged_score_base`, and
  finish far apart purely on Bow skill.
- **Melee roles are template ladders, everywhere** (§2.1). The recurring artifact is a
  `TwoHandedSword` troop out-ranking a better-armoured, higher-skilled polearm or axe troop on
  template class alone — vanilla's Sturgian Ulfhednar and Vlandian Pikeman, NS's Sturgian Heroic
  Line Breaker (pool-best melee skill 150, mid-B on a `OneHandedSword` template), ROT's Umber
  Berzerker/Cerwyn Marauder step-down at identical skills, TAOM's `erebor_noble_shield_breaker`
  (second-best armour in its role, dragged to rank 13 by `TwoHandedAxe` 73.33 vs 100.0).
- **The thrower role is the weakest table in all four reports**, and every lane says so in its
  own words (§2.7).
- **The best unit in a role frequently has no upgrade tier.** vanilla (`sturgian_shock_troop`,
  `imperial_legionary`, `vlandian_sharpshooter` and others, blank tree tier), NS (5 of the top 9
  line infantry plus its #1 crossbow are `special_or_unlinked`), ROT (`Unsullied`, recruit-only).
  `upgrade_requires` is not modelled in any track, so the pack cannot say how a player reaches
  them.

### Where the tracks genuinely differ in shape

- **Horse-archer depth is the sharpest structural difference.** ROT has **3** mounted bow troops
  out of 865 — its own report calls that the finding, not the ranking, and warns that
  `Mormont Mounted Huntress`'s S tier is computed against the other two, not against real
  archery. vanilla (19) is a Khuzait monopoly, 14 of 19, with no Battanian, Sturgian, Vlandian or
  Nord horse archer at all. TAOM (22) is two elf troops and then a cliff — rank 1 at 97.35, rank
  3 at 63.37. NS (22) is 14 Khuzait but only two inside its top five.
- **Line-infantry depth vs top-heaviness.** ROT's line-infantry ladder is the flattest anywhere
  in the run (13 S, 127 A, 166 B, 12 C, no D — dozens of house-guard lines within a few points),
  while its shock-infantry ladder is the most top-heavy (1 S, 1 A, 5 B, 13 C, **134 D**). Its own
  report says to treat that D block as "unscorable at this granularity", not as a fine ordering.
- **The thrower role is a different *kind* of unit per track.** ROT: a javelin sidearm bolted
  onto shielded heavy infantry (every top-ten entry but one also appears in line infantry). TAOM:
  almost purely cavalry (every S/A entry but one is a Rohan, Dunland or Harad horseman). vanilla
  and NS: foot skirmishers, both topped by a sling artifact.
- **Crossbow is a one- or two-culture role in every track**, but which culture varies: Vlandia
  (vanilla 11 of 13, NS 10 of 12), Myrish (ROT — the only culture with a top-to-bottom crossbow
  ladder), Erebor/Iron Hills dwarves (TAOM, on the two hardest-hitting ranged items in that
  track).
- **NavalDLC is kept everywhere, but lands differently.** NS retains 44 NavalDLC troops (17% of
  its pool) and they matter: `nord_huscarl` is its outright best line infantryman,
  `aserai_marine_t5` its best-equipped bow, and **NavalDLC contributes zero cavalry** in that
  track. In TAOM the 36 NavalDLC soldiers fall inside the untouched-vanilla bucket that its
  mod-content filter scopes out — *not* excluded as test data (invariant respected), just routed
  to the appendix.

### One cross-lane reading worth chasing (not verified here)

TAOM's open item #3 reports several top crossbow entries with `Crossbow` skill of only 35–50 that
nonetheless score `ranged_skill_factor` 0.77–1.11, and concludes the scorer "is evidently not
gated on `Crossbow` alone". NS and ROT both document the formula as
`ranged_skill_factor = clip(max(Bow, Crossbow) / 220, 0.25, 1.15)` — **`max`, not `Crossbow`** —
which would fully explain TAOM's observation if those dwarf/Gondor troops carry a high `Bow`
value. **This is a plausible resolution, not a verified one**: it needs one lookup of the `Bow`
column for `iron_hills_noble_veteran_sharpshooter`, `ironpass_sharpshooter`,
`gondor_tol_sharpshooter` and `iron_hills_noble_sharpshooter` in `taom_troops.csv`. Whether the
`max` is *correct* modelling for a crossbowman is a separate V4.4 question.

---

## 4. Method divergences between the lanes

Recorded so a later reader knows the four reports are not four runs of one method. None of these
is an error; each lane stated and justified its choice. All of them are reasons the numbers do
not join.

### 4.1 Filter chains — four different universes

| track | chain | pool |
|---|---|---|
| `vanilla` | soldiers (367) → drop 84 `mp_*` → keep NavalDLC → keep tutorial/arena ids (shown, not dropped, "universe rule is reproducible from the pack") | **283** |
| `nightmare_sails` | soldiers (371) → drop 84 `mp_*` (287) → drop **31 non-battlefield pseudo-troops** by id regex (tutorial, arena contenders, arena fighters, quest loaners) → keep NavalDLC | **256** |
| `realm_of_thrones` | soldiers (1,232) → drop `change_type == inalterado` (removes 367 soldiers, and all 84 `mp_*` fall inside that set) → keep NavalDLC | **865** |
| `taom` | soldiers (1,239) → keep `change_type in (novo, override)` (872) → drop 2 `mp_*` | **870** + separate 283-troop vanilla-baseline appendix |

Two structural splits follow. **vanilla and NS rank the whole playable roster; ROT and TAOM rank
mod-touched content only.** And **NS deliberately diverges from its own OVERVIEW's pool** (270
mod-touched troops vs its 256): 27 OVERVIEW ids are absent here (arena/tutorial/borrowed) and 13
untouched-vanilla ids are present. NS carries `change_type` in every companion CSV so the
OVERVIEW pool is reproducible by filtering.

Also note vanilla keeps the four `tutorial_npc_*` Training Masters visible — they occupy ranks 5,
9, 10 and 11 of its shock-cavalry table on a tutorial-only horse (35/65/65) with almost no armour
and no skills, and its report says plainly to ignore them as troops. NS drops the same ids by
regex. Same data, opposite handling, both documented.

### 4.2 Roster aggregation — TAOM is the odd one out, on purpose

`roster_index` rows are **alternative** kits; the game picks one at spawn. Nothing is ever summed.

| track | `role_scores_v1` columns | descriptive metrics computed by the lane |
|---|---|---|
| `vanilla` | frozen scorer's own aggregation kept as-is (max across rosters for role scores and most bases; mean for `defense_score_base`) | arithmetic **mean** across rosters; booleans OR-ed; item ids unioned |
| `nightmare_sails` | used exactly as the scorer emitted them (same max/mean split) | arithmetic **mean** across rosters |
| `realm_of_thrones` | inherited, not re-derived (same max/mean split) | arithmetic **mean** across rosters |
| `taom` | **re-aggregated to mean across rosters** from the per-roster CSV | **mean** |

**TAOM is the only lane that re-aggregated the v1 role scores themselves.** It verified the
shipped troop-level table is a max (for all 1,193 troop×role-score pairs on multi-roster troops,
the troop value equals the roster max) and deliberately chose mean instead, on the grounds that
the game rolls a roster at spawn. The consequence it states itself: **TAOM's ranks legitimately
differ from TAOM's own `OVERVIEW.md`, and the gap grows with `n_rosters`** — and some TAOM troops
carry a lot of rosters (`imladris_swordguard` 23, `imladris_nobleman` 19,
`rivendell_glorfindel_guard` 32). Neither convention is wrong; mixing them is. TAOM's own open
item #4 asks for one convention track-wide.

### 4.3 Tier bands — TAOM diverges

| track | S | A | B | C |
|---|---|---|---|---|
| `vanilla`, `nightmare_sails`, `realm_of_thrones` | ≥ 0.90 | ≥ 0.70 | ≥ 0.40 | ≥ 0.20 |
| `taom` | ≥ 0.90 | **≥ 0.75** | **≥ 0.55** | **≥ 0.35** |

All four compute `frac = score / best-non-outlier-in-role`, and all four state that tiers are
per-role (an S archer and an S line infantryman are not equivalent units). But **the letters
themselves are not comparable across tracks**: a TAOM "B" and a ROT "B" are different fractions
of their respective leaders. Combined with §2.4 — three different definitions of which troop
counts as the "best non-outlier" — the tier letter is the *least* portable field in this run.

### 4.4 Role assignment — partition vs overlapping views

- **`vanilla`** assigns exactly one role per troop, by a first-match cascade on roster-OR-ed kit
  flags (bow → horse archer/archer; crossbow; horse → shock cavalry; throw-dominance → thrower;
  shield → line infantry; else shock infantry). Rule 4 is **skill dominance, not kit presence**:
  28 foot troops carry a javelin bundle but only 19 are throw-dominant. It deliberately does not
  use `default_group`, which disagrees with the kit in several cases.
- **`nightmare_sails`** splits foot melee at `shield_share >= 0.5` (a roster-mean, not a boolean)
  and otherwise uses `has_*` flags; pools overlap (a troop can be shock infantry *and* thrower).
- **`realm_of_thrones`** uses `default_group == Infantry` plus flags; pools overlap by design.
- **`taom`** uses `default_group` plus flags, and its thrower pool **includes mounted troops** —
  which is why its thrower ladder is a cavalry ladder (§3).

So "thrower" names four different populations, and only vanilla's seven roles form a partition.

### 4.5 Shock cavalry — four different metrics

`role_scores_v1` has no cavalry column. Each lane solved it differently:

| track | metric |
|---|---|
| `vanilla` | descriptive `shock_cav_index` = 0.35·n(charge) + 0.10·n(speed) + 0.10·n(maneuver) + 0.20·n(mounted_armor) + 0.10·n(melee_proxy) + 0.15·n(rider_skill), min–max over its 49 cavalry only |
| `nightmare_sails` | descriptive `shock_cav_index_desc` = 0.50·mount_index_desc + 0.35·`offensive_melee_role_score` + 0.15·`defensive_role_score` |
| `realm_of_thrones` | **no new index** — ranked by `defensive_role_score`, the only published column whose driver ingests mount quality (`charge·0.25 + speed·0.06 + maneuver·0.04`), with `offensive_melee_role_score` carried alongside for a lance-first reading |
| `taom` | descriptive `shock_cav_index` = 0.40·N(charge,32) + 0.20·N(speed,68) + 0.10·N(maneuver,80) + 0.10·N(extra_hp,120) + 0.20·N(Polearm,440), **fixed divisors** rather than pool min–max |

Every lane states its weights are an editorial judgement, not a fitted model, and that the index
must never be written back into `analysis/model_versions/`. NS additionally flags that its own
ranking is sensitive to the 0.50 mount weight (`druzhinnik_champion` would be top four under a
mount-agnostic weighting instead of eighth).

**The shock-cavalry column of §3 is therefore the least joinable row in this document** — four
metrics, four scales, one of which is not even a descriptive index but a repurposed defensive
score.

---

## 5. Consolidated defect list

Model / scorer (V4.4 backlog — no lane touched a formula):

1. Crafted melee and thrown stats are not reconstructed; both melee-facing role scores and the
   skirmisher score are template-name constants (§2.1). Reported by all four lanes.
2. Blank `skill_template` skills NaN out three of four role scores;
   `generate_vanilla_role_scores.py:192-199` `float(x or 0)` does not coerce NaN (§2.5). NS.
3. The scorer does not apply the `item_found` filter (§2.6). ROT.
4. `ranged_skill_factor` uses `max(Bow, Crossbow)` — arguably wrong for crossbowmen, and the
   likely explanation of TAOM's open item #3 (§3, last block).
5. Slings are scored as thrown weapons; a sling tops two of the four thrower ladders (§2.7). NS,
   vanilla.
6. `crafted_class()` tests `"Axe"` before `"Throwing"`, so a `ThrowingAxe` template is classified
   as a melee axe (proxy 46, usability 0.88). Visible on `nord_berserkr`, `nord_skjaldbrestir`.
   `Pike` and `Dagger` fall through to `other`. NS.

Pack / export:

7. No `is_obsolete` flag and no `source_xml` column for troops — the 272-vs-283 gap (§2.3). All
   four lanes.
8. Load-order resolution prefers stat-less reference stubs over real definitions; the
   `unknown_items` queue cannot catch this class (§2.6). TAOM. Wants a `resolved_but_untyped`
   counter in the audit summary.
9. `SCHEMA.md` documents `item_kind` as `direct`/`crafted`; the shipped CSVs use
   `Item`/`CraftedItem`. Cosmetic, but a filter written from the docs silently matches nothing.
   NS. (`analysis_pack/SCHEMA.md` is owned by neither this task nor that lane.)
10. `upgrade_requires` is not modelled anywhere, so availability commentary from `tree_tier`
    ignores upgrade gating — and the best unit in a role is often unlinked from any tree (§3).

Process, for a human to settle:

11. **One owner for the S+ outlier criterion** (§2.4) — three definitions in play.
12. **One roster-aggregation convention** (§4.2) — TAOM's mean vs the shipped max, which already
    puts TAOM's ROLE_REPORT and TAOM's OVERVIEW out of step with each other.
13. **One tier-band table** (§4.3) — TAOM's A/B/C thresholds differ from the other three.
14. Vanilla has no `OVERVIEW.md` for this export; its ROLE_REPORT has no companion to be read
    against (§1).

---

## 6. Scope of this document

Narrative comparison only. No merged ranking, no pooled ladder, no normalization — and none is
possible until at least §5 items 1, 7, 11, 12 and 13 are settled. Nothing here modifies any
track's ROLE_REPORT, `OVERVIEW.md`, `analysis/model_versions/`, or `analysis_pack/`. No XML was
read and no export was re-run.
