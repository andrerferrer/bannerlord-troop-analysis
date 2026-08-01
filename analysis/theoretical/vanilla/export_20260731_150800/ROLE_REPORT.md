# Soldier role report — `vanilla` / `export_20260731_150800`

Intra-track only. Every number below is comparable **within the vanilla track and this export
only** — never against `nightmare_sails`, `realm_of_thrones` or `taom` (ADR-003, SCHEMA.md:100).

- Evidence basis: `xml_structural` (ADR-004). Empirical: `false`.
- Model: `role_scores_v1` conservative proxy (not HTK / V4.x / V7.x). Scorer logic unchanged.
- Secondary context: there is **no `OVERVIEW.md` in this export directory at the time of
  writing** (the vanilla overview lane had not landed yet). This report therefore stands on
  the SSOT CSVs alone; when the overview lands, read it alongside — this file does not
  restate or supersede it.

---

## 1. Inputs and integrity

Source of truth: `analysis_pack/vanilla/` (ADR-003). No XML was read, no audit was rebuilt.

| file | rows | sha256 (first 16) | matches `analysis_pack/MANIFEST.csv` |
|---|---|---|---|
| `vanilla_troop_equipment_audit.csv` | 18,153 | `9483c1f2f2519270` | yes |
| `vanilla_troops.csv` | 1,937 | `edaad2f7c33f3e76` | yes |
| `vanilla_tree_tiers.csv` | 367 | `07e367ca6d25d671` | yes |
| `vanilla_items_catalog.csv` | 2,316 | `78362875f40c148c` | yes |
| `vanilla_upgrade_edges.csv` | 218 | `64cf210793caa511` | yes |

All five files are byte-identical to `data/vanilla/audit/` for the same export (verified by
sha256), so the pack and the audit directory agree; nothing was re-exported.

`role_scores_v1` columns were produced by running
`scripts/scoring/generate_vanilla_role_scores.py` (git `96bd75c`, sha256 `bb38a720f79b272b`)
**unchanged**, with `--audit-dir` pointed at the filtered pack copy described in §2 and
`--output-dir` pointed at a scratch directory. No scorer file was edited, and no scorer output
was committed — only this report and its `role_report_*.csv` companions. Changing the v1
formulas is a V4.4 model PR and is out of scope here.

---

## 2. Filters applied

Applied in this order, as mandated by `analysis_pack/SCHEMA.md` §"Mandatory filters" and
`AGENT_PROMPT.md`:

1. **`item_found == True`** — 18,153 of 18,153 audit rows survive. The pack ships pre-resolved,
   so this filter is a no-op here; it is applied anyway so the pipeline stays correct if a
   future pack carries unresolved ids.
2. **Soldiers only** — `is_soldier == True` in `vanilla_troops.csv` (equivalent to
   `occupation == Soldier`): 367 of 1,937 troops. Notables, wanderers, lords and heroes dropped.
3. **Multiplayer dropped** — 84 soldiers whose `troop_id` starts with `mp_`.
4. **NavalDLC kept** — the whole Nord culture (27 soldiers here) and the `*_marine_t4/t5`
   troops of five cultures stay in. They are War Sails content, not test data.
5. **Giants / mammoths parked as S+ outliers** — the outlier regex used by the theoretical
   overviews (`giant`/`mammoth` in id or name) matches **0 vanilla soldiers**. The S–D
   commentary below is therefore complete for this track; see §7.

**Universe analysed: 367 soldiers → drop 84 `mp_*` → 283 soldiers, 784 rosters.**

### Known deviation from SCHEMA.md

`SCHEMA.md:88-90` states the clean vanilla baseline is **272** soldiers, i.e. 135 ids (95
soldiers) defined only in `mpcharacters.xml` / `obsolete_characters.xml` should be removed.
`analysis_pack` carries **no `is_obsolete` flag and no source-xml column for troops**, so the
~11 obsolete ids that are not `mp_*`-prefixed cannot be identified from the pack alone. Raw
module XML is deliberately not committed, so they cannot be recovered here either. This report
therefore analyses **283**, not 272. This is a **gap in the pack to fix at the source** (emit
`is_obsolete` or a `source_xml` column for troops) — not something worked around downstream. A
name-prefix heuristic was explicitly rejected: it is unverifiable by a later reader and would
drift per track. `SCHEMA.md` is not this task's path and was not edited.

Practical impact: the ~11 unidentified ids sit inside the ranking universe and inside the v1
min-max normalisation. Suspect entries are visible in the tables by their `troop_id` and by an
empty tree tier (e.g. `imperial_legionary`, `sturgian_shock_troop`, `sturgian_veteran_warrior`,
`vlandian_sharpshooter`, `battanian_wildling`, `aserai_master_archer`, the `tutorial_npc_*`
Training Masters). Two of those — `imperial_legionary` and `vlandian_sharpshooter` — are
`CONTROL_IDS` anchors of the frozen scorer, which is a second reason not to strike them by hand.

---

## 3. Roster aggregation — the explicit choice

`roster_index` rows are **alternative** kits; the game picks one at spawn. This report uses:

- **Descriptive metrics: arithmetic MEAN across all `roster_index` values of a troop**, computed
  per roster first and then averaged (784 rosters → 283 troops; 157 troops have 3 rosters, 52
  have 2, 41 have 4, 30 have 1, 3 have 5). Booleans (`has_shield`, `has_horse`, …) are OR-ed
  across rosters; item ids and crafting templates are unioned and shown `|`-separated. Nothing
  is ever summed across rosters.
- **`role_scores_v1` columns: the frozen scorer's own aggregation is kept as-is** — that is
  `max` across rosters for the four role scores and for `ranged_score_base`,
  `crafted_melee_score_base` and `throw_score_base`, and `mean` across rosters for
  `defense_score_base`. Reproducing the frozen model faithfully is worth more than aggregation
  symmetry, so the two conventions are reported side by side rather than harmonised.

Where a table shows both (e.g. `v1 ranged` next to `bow+arrow dmg`), read the v1 column as
"best roster" and the descriptive columns as "average roster".

---

## 4. Role definitions and metric formulas

### 4.1 Role assignment

Each troop gets exactly one role, by the first rule that matches (evaluated on the
roster-OR-ed kit flags):

```txt
1. has Bow                          -> "horse archer" if has Horse else "archer"
2. has Crossbow (and no Bow)        -> "crossbow"
3. has Horse                        -> "shock cavalry"
4. has thrown/sling kit AND
   Throwing >= max(OneHanded, TwoHanded, Polearm)   -> "thrower"
5. has Shield                       -> "line infantry"
6. otherwise                        -> "shock infantry"
```

Notes on the edges:
- Rule 4 is skill-dominance, not kit-presence: 28 foot troops carry a javelin bundle but only
  19 of them are throw-dominant. A shielded spearman with one javelin stack stays line infantry.
- Mounted javelin cavalry (13 of the 49) land in **shock cavalry**; the role list has no
  "skirmisher cavalry" bucket, and their charge/armour still drives the index.
- Slings (`SlingStones`) count as throwing, matching v1, which treats only Bow/Crossbow as
  ranged. This affects exactly 2 troops (`hidden_hand_tier_1/2`).
- `default_group` from the XML was **not** used for assignment — it disagrees with the kit in
  several cases (e.g. `battanian_mounted_skirmisher` is `Cavalry` with a bow). The kit rules
  above are reproducible from the audit CSV; the resulting counts are:
  line infantry 90, archer 50, shock cavalry 49, shock infantry 41, thrower 21, horse archer 19,
  crossbow 13.

### 4.2 Per-roster metrics (computed from `vanilla_troop_equipment_audit.csv`)

Armour slots are `{Head, Body, Gloves, Leg, Cape}`; weapon slots are `Item0..Item4`.

```txt
head  = Σ head_armor over armour slots      body = Σ body_armor over armour slots
arm   = Σ arm_armor  over armour slots      leg  = Σ leg_armor  over armour slots
armor_total     = head + body + arm + leg
effective_armor = 0.20*head + 0.65*body + 0.10*arm + 0.05*leg     [v1 constant, reused verbatim]

shield_hp    = max(hit_points)   over weapon slots with type == Shield
shield_armor = max(shield_armor) over weapon slots with type == Shield
horse_charge / horse_speed / horse_maneuver = max(...) over slot == Horse
harness_armor = max(body_armor) over slot == HorseHarness
mounted_armor = effective_armor + 0.45 * harness_armor            [0.45 = v1 harness weight]

bow_damage  = max(thrust_damage over type==Bow)      + max(thrust_damage over type==Arrows)
xbow_damage = max(thrust_damage over type==Crossbow) + max(thrust_damage over type==Bolts)
arrow_stack = Σ stack_amount over type==Arrows ; bolt_stack likewise over type==Bolts
rider_skill = max(Polearm, OneHanded, TwoHanded)
```

Bows and crossbows in this pack carry **only** `thrust_damage` (no swing), and the ammo row
carries the projectile's own `thrust_damage`; adding the two is the same convention the frozen
scorer uses for `ranged_damage_real`. Damage types are not mixed anywhere in this report: every
`Cut`/`Pierce`/`Blunt` comparison would need an armour model that v1 does not have, so raw
damage is only ever compared within one weapon family.

### 4.3 Melee and throwing proxies

**All 3,619 melee/throwing weapon rows in vanilla are `CraftedItem` with
`crafted_stats_reconstructed == False` and zero swing/thrust damage.** There is no real melee
damage number anywhere in this track. Melee strength is therefore a *template proxy*, taken
verbatim from the frozen v1 tables:

```txt
proxy      : two_handed_polearm 58, two_handed_sword 60, one_handed_polearm 44,
             one_handed_sword 44, mace 43, axe 46, javelin 36, throwing 34, other 40
usability  : two_handed_polearm 0.78, two_handed_sword 0.92, one_handed_polearm 0.70,
             one_handed_sword 0.95, mace 0.90, axe 0.88, javelin 0.55, throwing 0.55, other 0.75

melee_proxy_best     = max(proxy(class) * usability(class)) over non-throwing crafted weapons
throw_template_proxy = 0.55 * proxy(class)  for the best javelin/throwing crafted weapon
```

Direct `Thrown` items exist on only 7 of 784 rosters (throwing stones and sling ammunition), so
the thrower ranking is essentially *template class + Throwing skill*, with no damage evidence.
Treat §5.5 as the weakest table in this report.

### 4.4 Role score used for ranking

| role | primary score | source |
|---|---|---|
| shock infantry | `offensive_melee_role_score` | role_scores_v1 |
| line infantry | `defensive_role_score` | role_scores_v1 |
| archer | `ranged_role_score` | role_scores_v1 |
| crossbow | `ranged_role_score` | role_scores_v1 |
| horse archer | `ranged_role_score` | role_scores_v1 |
| thrower | `skirmisher_role_score` | role_scores_v1 |
| shock cavalry | `shock_cav_index` | **descriptive, defined below** |

`role_scores_v1` has no cavalry column — cavalry is deliberately not a v1 category, and heavy
cavalry is spread across its defensive and offensive-melee scores. For the shock-cavalry table
this report therefore computes a descriptive index over the 49 shock-cavalry troops only:

```txt
n(x) = 100 * (x - min(x)) / (max(x) - min(x))     min/max taken over the 49 shock cavalry troops

shock_cav_index = 0.35*n(horse_charge)
                + 0.10*n(horse_speed)
                + 0.10*n(horse_maneuver)
                + 0.20*n(mounted_armor)
                + 0.10*n(melee_proxy_best)
                + 0.15*n(rider_skill)
```

It is a descriptive ordering, not a model output: it is not calibrated, not comparable to the
v1 0–100 scales, and must not be fed back into `analysis/model_versions/`. Both
`defensive_role_score` and `offensive_melee_role_score` are carried in
`role_report_shock_cavalry.csv` as a cross-check.

### 4.5 Tier letters

S–D follow the convention already used by the theoretical overviews — score relative to the best
non-outlier in that role list:

```txt
frac = score / max(score in role)
frac >= 0.90 -> S    >= 0.70 -> A    >= 0.40 -> B    >= 0.20 -> C    else D
```

Tiers are **per role**, so an S archer and an S line infantryman are not equivalent units.
`tier(tree)` in the tables is the separate `tree_tier` column from `vanilla_tree_tiers.csv`
(upgrade-tree depth); `—` means the troop is unlinked from an upgrade tree.

A `†` after a troop name means all eight skill columns are blank for that troop
(`skill_template` is not modelled — SCHEMA "Known limitations"); any skill-weighted number for
it reads as 0.

---

## 5. Rankings

Top 12 per role. Full ranked lists — every troop, every driver column — are in the companion
CSVs listed in §8.

### 5.1 Shock infantry — n=37 ranked (41 assigned)

Two-handed foot troops with no shield. Ranked by `offensive_melee_role_score`.

| # | tier | troop | troop_id | tier(tree) | culture | v1 offensive melee | melee base | best melee template | 2H | Pole | eff. armor | Athl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Conspiracy Knight | `conspiracy_knight` | — | vlandia | 66.1 | 100.0 | TwoHandedSword | 140 | 90 | 53.6 | 90 |
| 2 | S | Battanian Veteran Falxman | `battanian_veteran_falxman` | 5 | battania | 60.3 | 100.0 | TwoHandedSword | 130 | 70 | 42.6 | 130 |
| 3 | B | Battanian Falxman | `battanian_falxman` | 4 | battania | 46.2 | 100.0 | TwoHandedSword | 100 | 45 | 29.7 | 100 |
| 4 | B | Conspiracy Knight Trainee | `conspiracy_knight_trainee` | — | vlandia | 37.3 | 100.0 | TwoHandedSword | 80 | 40 | 22.7 | 60 |
| 5 | B | Conspiracy Spear Master | `conspiracy_spearmaster` | — | vlandia | 30.5 | 39.6 | TwoHandedPolearm | 80 | 150 | 41.7 | 110 |
| 6 | B | Nord Ulfhedinn | `nord_ulfhednar` | 5 | nord | 29.5 | 39.6 | TwoHandedPolearm | 90 | 140 | 49.4 | 150 |
| 7 | B | Imperial Elite Menavliaton | `imperial_elite_menavliaton` | 2 | empire | 27.3 | 39.6 | TwoHandedPolearm | 80 | 130 | 45.5 | 130 |
| 8 | C | Vlandian Voulgier | `vlandian_voulgier` | 5 | vlandia | 26.1 | 39.6 | TwoHandedPolearm | 130 | 130 | 35.3 | 130 |
| 9 | C | Nord Warfang | `nord_vargr` | 4 | nord | 23.2 | 39.6 | TwoHandedPolearm | 70 | 110 | 39.3 | 110 |
| 10 | C | Imperial Menavliaton | `imperial_menavliaton` | 1 | empire | 22.3 | 39.6 | TwoHandedPolearm | 60 | 100 | 41.8 | 100 |
| 11 | C | Sturgian Heroic Line Breaker | `sturgian_ulfhednar` | 2 | sturgia | 18.2 | 18.8 | OneHandedSword | 150 | 80 | 52.1 | 150 |
| 12 | C | Vlandian Pikeman | `vlandian_pikeman` | 5 | vlandia | 15.2 | 18.8 | Pike | 130 | 130 | 39.3 | 130 |

**Why.** The ordering is almost entirely `crafted_melee_score_base`, which is a *template* score:
`TwoHandedSword` (60 × 0.92 = 55.2) beats `TwoHandedPolearm` (58 × 0.78 = 45.2) by construction,
so every falx/greatsword troop clears every menavlion troop before skills are even read. The
skill factor (`max(1H,2H,Polearm)/220`, clipped 0.25–1.15) then separates same-template troops —
that is the whole gap between the Veteran Falxman (2H 130) and the Falxman (2H 100), which share
an identical melee base of 100. Sturgian Ulfhednar and Vlandian Pikeman rank low for a
*template* reason, not a combat reason: their best crafted class resolves to `one_handed_sword`
and `Pike` respectively, both of which carry a lower proxy than a menavlion. With zero real
swing damage in this track (§4.3), this table ranks *what a troop is holding*, not how hard it
hits — do not read the C/D tail as weak troops.

### 5.2 Line infantry — n=90 ranked

Shielded foot. Ranked by `defensive_role_score`.

| # | tier | troop | troop_id | tier(tree) | culture | v1 defensive | defense base | eff. armor | shield HP | shield armor | best melee template | 1H | Pole |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Vlandian Sergeant | `vlandian_sergeant` | 5 | vlandia | 62.2 | 67.8 | 47.7 | 500 | 16 | TwoHandedPolearm | 130 | 130 |
| 2 | S | Sturgian Heavy Spearman | `sturgian_shock_troop` | — | sturgia | 61.0 | 65.7 | 52.1 | 547 | 7 | TwoHandedPolearm | 140 | 140 |
| 3 | S | Nord Huscarl | `nord_huscarl` | 5 | nord | 58.5 | 63.1 | 49.1 | 633 | 5 | TwoHandedPolearm | 200 | 200 |
| 4 | S | Aserai Veteran Infantry | `aserai_veteran_infantry` | 5 | aserai | 56.9 | 60.6 | 56.3 | 360 | 1 | TwoHandedPolearm | 160 | 130 |
| 5 | A | Nord Berserkir | `nord_berserkr` | 5 | nord | 55.1 | 65.1 | 54.0 | 513 | 5 | TwoHandedAxe | 140 | 40 |
| 6 | A | Conspiracy Commander | `imperial_conspiracy_boss` | — | vlandia | 54.5 | 31.8 | 30.5 | 200 | 0 | OneHandedSword\|TwoHandedPolearm | 240 | 240 |
| 7 | A | Imperial Legionary | `imperial_legionary` | — | empire | 54.1 | 59.7 | 51.5 | 530 | 1 | TwoHandedPolearm | 130 | 130 |
| 8 | A | Battanian Oathsworn | `battanian_oathsworn` | 5 | battania | 53.9 | 58.2 | 52.3 | 430 | 1 | TwoHandedPolearm | 130 | 130 |
| 9 | A | Sturgian Heavy Axeman | `sturgian_veteran_warrior` | — | sturgia | 53.3 | 63.5 | 49.2 | 573 | 7 | OneHandedAxe | 130 | 80 |
| 10 | A | Khuzait Darkhan | `khuzait_darkhan` | 5 | khuzait | 52.5 | 58.0 | 54.1 | 340 | 1 | TwoHandedPolearm | 130 | 130 |
| 11 | A | Nord Hearthguard | `nord_jarlsmann` | 3 | nord | 50.7 | 54.6 | 44.9 | 437 | 5 | TwoHandedPolearm | 110 | 110 |
| 12 | A | Nord Shield-Companion | `nord_hirdmann` | 4 | nord | 48.1 | 53.1 | 41.5 | 513 | 5 | TwoHandedPolearm | 140 | 140 |

**Why.** `defensive_role_score` is `0.72 × defense_base + 0.12 × melee_base + 0.04 × throw_base`
plus a flat +12 for a shield and +6 for a horse, and `defense_base` itself is
`1.25 × effective_armor + shield_hp/35 + 1.1 × shield_armor + 0.45 × harness_armor`. So the
table is driven by body armour first and shield hit points second, and it is *not* skill-gated —
which is why it is the only role where no troop is missing a score. The Vlandian Sergeant wins
on the only meaningful `shield_armor` value in the set (16 vs 1–7 everywhere else), the Nord
Huscarl on the biggest shield in vanilla (633 HP), and the Aserai Veteran Infantry on the
highest effective armour (56.3) despite the smallest shield of the top four. `nord_*` fills 15
of the 90 slots and 4 of the top 12 — the War Sails Nord line is a genuinely dense heavy-infantry
culture, which is the single strongest argument for keeping NavalDLC in the baseline.
Two entries are artefacts to read with care: the Conspiracy Commander is A-tier on flat
shield/horse bonuses and skills 240, not on armour (defense base 31.8); and `sturgian_shock_troop`
/ `sturgian_veteran_warrior` / `imperial_legionary` have no tree tier, so they are in the
suspected-obsolete set of §2.

### 5.3 Archer — n=38 ranked (50 assigned, 12 unscored)

Foot bow users. Ranked by `ranged_role_score`.

| # | tier | troop | troop_id | tier(tree) | culture | v1 ranged | ranged base | bow+arrow dmg | Bow skill | arrows | acc | eff. armor | bow |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Battanian Fian Champion | `battanian_fian_champion` | 5 | battania | 92.4 | 87.1 | 67 | 220 | 64 | 94 | 54.4 | woodland_longbow |
| 2 | B | Battanian Fian | `battanian_fian` | 4 | battania | 63.3 | 87.1 | 67 | 160 | 64 | 94 | 38.5 | woodland_longbow |
| 3 | B | Conspiracy Longbowman | `conspiracy_longbowman` | — | battania | 61.2 | 87.1 | 67 | 150 | 64 | 94 | 47.0 | woodland_longbow |
| 4 | B | Nord Sky-Gods Chosen | `nord_skathi` | 5 | nord | 56.2 | 82.0 | 65 | 140 | 32 | 93 | 44.9 | woodland_longbow\|woodland_yew_bow |
| 5 | B | Aserai Bahriyyah | `aserai_marine_t5` | 2 | aserai | 54.9 | 84.6 | 74 | 140 | 23 | 91 | 28.4 | nomad_bow |
| 6 | B | Aserai Master Archer | `aserai_master_archer` | — | aserai | 52.0 | 77.2 | 56 | 160 | 46 | 94 | 29.9 | composite_steppe_bow |
| 7 | B | Conspiracy Hunt Leader | `conspiracy_hunt_leader` | — | empire | 49.8 | 74.5 | 57 | 160 | 24 | 95 | 18.2 | steppe_war_bow |
| 8 | B | Imperial Palatine Guard | `imperial_palatine_guard` | 5 | empire | 43.9 | 78.3 | 57 | 140 | 48 | 95 | 33.4 | steppe_war_bow |
| 9 | B | Chosen Wolf | `wolfskins_tier_3` | 3 | battania | 43.4 | 78.8 | 64 | 130 | 20 | 93 | 22.1 | woodland_longbow\|woodland_yew_bow |
| 10 | B | Sturgian Veteran Bowman | `sturgian_veteran_bowman` | 5 | sturgia | 41.8 | 73.8 | 52 | 140 | 40 | 94 | 34.5 | composite_bow |
| 11 | B | Khuzait Marksman | `khuzait_marksman` | 5 | khuzait | 40.2 | 76.2 | 54 | 130 | 48 | 94 | 32.5 | composite_steppe_bow |
| 12 | B | Battanian Hero | `battanian_hero` | 3 | battania | 40.0 | 80.3 | 60 | 130 | 64 | 94 | 30.8 | lowland_longbow |

**Why.** `ranged_role_score` multiplies the kit base by a skill factor (`Bow/220`, clipped
0.25–1.15) and then re-normalises, so the Bow skill is the dominant term once the bow is decent.
That is the whole Fian Champion story: identical kit to the Fian and the Conspiracy Longbowman
(same longbow, same 64-arrow load, ranged base 87.1 for all three) and 220 Bow against 160/150.
It is the only S in the role and the gap to #2 is 29 points — the largest leader gap of any role
in this track. Below it the table is one flat B band: `bow+arrow dmg` only spans 52–74 and
accuracy 91–95, so armour and arrow count do most of the remaining separation. Worth flagging:
`aserai_marine_t5` (Bahriyyah) posts the highest raw projectile damage in the whole role (74,
the `nomad_bow` line) at tree tier 2 — a NavalDLC troop out-damaging every tier-5 archer on
paper, held back only by a 23-arrow quiver and 28.4 armour.
**12 archers are unranked** — the militia archers of every culture, whose skills come from
`skill_template` and are blank in the pack, which makes v1's skill factor NaN. See §6.

### 5.4 Crossbow — n=11 ranked (13 assigned, 2 unscored)

Crossbow users, no bow. Ranked by `ranged_role_score`.

| # | tier | troop | troop_id | tier(tree) | culture | v1 ranged | ranged base | xbow+bolt dmg | Xbow skill | bolts | acc | eff. armor | shield |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Conspiracy Warworn Crossbowman | `conspiracy_warworn_crossbowman` | — | vlandia | 75.6 | 98.4 | 102 | 150 | 20 | 100 | 34.6 | yes |
| 2 | A | Vlandian Nauta | `vlandian_marine_t5` | 2 | vlandia | 64.7 | 100.0 | 105 | 130 | 18 | 100 | 26.0 | yes |
| 3 | A | Vlandian Sharpshooter | `vlandian_sharpshooter` | — | vlandia | 64.0 | 100.0 | 105 | 130 | 18 | 100 | 31.6 | yes |
| 4 | A | Imperial Sergeant Crossbowman | `imperial_sergeant_crossbowman` | 5 | empire | 55.3 | 93.5 | 96 | 130 | 18 | 99 | 34.1 | yes |
| 5 | B | Boar Champion | `company_of_the_boar_tier_3` | 3 | vlandia | 40.2 | 93.2 | 95 | 100 | 20 | 99 | 28.8 | yes |
| 6 | B | Vlandian Seasoned Seafarer | `vlandian_marine_t4` | 1 | vlandia | 39.3 | 90.9 | 89 | 100 | 18 | 90 | 21.1 | yes |
| 7 | C | Imperial Crossbowman | `imperial_crossbowman` | 4 | empire | 27.7 | 81.9 | 78 | 100 | 18 | 85 | 27.0 | no |
| 8 | C | Conspiracy Trained Crossbowman | `conspiracy_trained_crossbowman` | — | vlandia | 22.3 | 85.0 | 84 | 80 | 20 | 96 | 30.5 | no |
| 9 | C | Boar Veteran | `company_of_the_boar_tier_2` | 2 | vlandia | 21.7 | 85.0 | 84 | 70 | 20 | 96 | 18.5 | yes |
| 10 | D | Boar Novice | `company_of_the_boar_tier_1` | 1 | vlandia | 12.4 | 85.0 | 84 | 40 | 20 | 96 | 13.2 | yes |
| 11 | D | Vlandian Levy Crossbowman | `vlandian_levy_crossbowman` | 2 | vlandia | 7.1 | 85.0 | 84 | 40 | 20 | 96 | 9.1 | no |

**Why.** Crossbows are the flattest kit family in vanilla: 84–105 damage, 18–20 bolts, accuracy
85–100 across the entire role, and the whole role is Vlandian (11) plus two Imperials. The
ranking is therefore almost pure Crossbow skill — 150 / 130 / 130 / 130 at the top, 40 at the
bottom, on nearly identical hardware. Note the scale trap: raw crossbow damage (102–105) reads
as far above the best bow (67), but v1 normalises ranged base *within the ranged pool*, and the
bolt's slow reload is not modelled at all, so a crossbowman's v1 score is not "1.5× an archer".
`vlandian_marine_t5` (NavalDLC, tree tier 2) matches the tier-5 Sharpshooter on kit and skill and
loses only on armour — the strongest availability arbitrage in this track.
**2 unranked** (`vlandian_militia_archer`, `vlandian_militia_veteran_archer`), again blank skills.

### 5.5 Thrower — n=21 ranked

Throw-dominant foot (`Throwing >= max` melee skill). Ranked by `skirmisher_role_score`.
This is the **lowest-confidence table in the report** — see §4.3.

| # | tier | troop | troop_id | tier(tree) | culture | v1 skirmisher | throw base | throw template | Throw skill | melee template | eff. armor | shield |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Hidden Soldati | `hidden_hand_tier_2` | 2 | empire | 82.0 | 100.0 | — | 70 | OneHandedSword | 19.1 | no |
| 2 | B | Battanian Wildling | `battanian_wildling` | — | battania | 56.4 | 30.5 | Javelin | 130 | OneHandedSword | 53.0 | yes |
| 3 | B | Battanian Skipari | `battanian_marine_t5` | 2 | battania | 53.4 | 30.5 | Javelin | 140 | OneHandedSword | 29.9 | yes |
| 4 | B | Redshank | `galloglass_tier_3` | 3 | battania | 49.9 | 30.5 | Javelin | 120 | OneHandedAxe | 49.5 | yes |
| 5 | B | Lake Rat Wrecker | `lakepike_tier_3` | 3 | sturgia | 47.7 | 30.5 | Javelin | 120 | OneHandedAxe | 37.0 | yes |
| 6 | B | Puppeteer | `hidden_hand_tier_3` | 3 | empire | 47.4 | 28.8 | ThrowingKnife | 100 | OneHandedSword\|TwoHandedPolearm | 34.4 | yes |
| 7 | B | Imperial Naute | `empire_marine_t5` | 3 | empire | 46.3 | 30.5 | Javelin | 130 | OneHandedAxe | 32.0 | yes |
| 8 | B | Skolder Veteran Broda | `skolderbrotva_tier_3` | 3 | nord | 42.4 | 30.5 | Javelin | 100 | OneHandedSword | 29.1 | yes |
| 9 | B | Hidden Pawn | `hidden_hand_tier_1` | 1 | empire | 38.8 | 70.8 | — | 55 | OneHandedSword | 7.3 | no |
| 10 | B | Battanian River Raider | `battanian_marine_t4` | 1 | battania | 34.0 | 30.5 | Javelin | 100 | OneHandedSword | 20.5 | yes |
| 11 | C | Imperial Coast Guard | `empire_marine_t4` | 2 | empire | 31.3 | 30.5 | Javelin | 100 | OneHandedAxe | 18.2 | yes |
| 12 | C | Conspiracy Kern | `conspiracy_kern` | — | battania | 30.9 | 30.5 | Javelin | 80 | Mace\|OneHandedSword | 34.4 | yes |

**Why.** The two Hidden Hand troops are the only entries in the role with a *real* thrown weapon
(sling ammunition, resolved as direct items with damage and stack), so their `throw_base` (100.0
and 70.8) is computed from actual stats while every javelin troop gets the flat template proxy
`0.55 × 36 = 19.8`, which normalises to 30.5 for all of them. That single data asymmetry, not
combat merit, is why a tier-2 sling user tops the table by 26 points and a 140-Throwing Skipari
sits at #3. Read the table as: *inside* the javelin block (#2–#12, identical throw base) the
ordering is Throwing skill and armour only. Availability is worth noting even so — 8 of the 21
are Battanian and 8 Imperial, and the NavalDLC marine lines supply five of the top eleven.
This role would be the first beneficiary of thrown-weapon stat reconstruction in the audit.

### 5.6 Shock cavalry — n=49 ranked

Mounted, no bow. Ranked by the descriptive `shock_cav_index` of §4.4 (not a v1 column).

| # | tier | troop | troop_id | tier(tree) | culture | shock-cav index | charge | hspeed | manv | mounted armor | best melee template | rider skill | Ride |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Imperial Elite Cataphract | `imperial_elite_cataphract` | 5 | empire | 73.5 | 28 | 59 | 66 | 92.5 | TwoHandedPolearm | 260 | 200 |
| 2 | S | Vlandian Banner Knight | `vlandian_banner_knight` | 5 | vlandia | 73.5 | 32 | 49 | 68 | 80.4 | TwoHandedPolearm | 260 | 200 |
| 3 | S | Vlandian Champion | `vlandian_champion` | 4 | vlandia | 66.7 | 32 | 49 | 68 | 76.2 | TwoHandedPolearm | 160 | 130 |
| 4 | A | Imperial Cataphract | `imperial_cataphract` | 4 | empire | 65.0 | 28 | 59 | 66 | 80.7 | TwoHandedPolearm | 160 | 130 |
| 5 | A | Training Master† | `tutorial_npc_advanced_melee_easy` | — | battania | 63.9 | 35 | 65 | 65 | 25.0 | TwoHandedSword | — | — |
| 6 | A | Aserai Vanguard Faris | `aserai_vanguard_faris` | 5 | aserai | 61.1 | 20 | 65 | 73 | 85.6 | TwoHandedPolearm | 200 | 170 |
| 7 | A | Vlandian Knight | `vlandian_knight` | 3 | vlandia | 60.2 | 32 | 49 | 68 | 60.4 | TwoHandedPolearm | 110 | 100 |
| 8 | A | Sturgian Druzhinnik Champion | `druzhinnik_champion` | 5 | sturgia | 55.9 | 22 | 56 | 66 | 79.8 | TwoHandedPolearm | 200 | 170 |
| 9 | A | Training Master† | `tutorial_npc_basic_melee` | — | battania | 54.8 | 35 | 65 | 65 | 26.5 | OneHandedSword | — | — |
| 10 | A | Training Master | `tutorial_npc_mounted_ai` | — | battania | 53.5 | 35 | 65 | 65 | 20.9 | OneHandedSword | — | 100 |
| 11 | A | Training Master† | `tutorial_npc_advanced_melee_normal` | — | battania | 53.5 | 35 | 65 | 65 | 20.9 | OneHandedSword | — | — |
| 12 | A | Vlandian Vanguard | `vlandian_vanguard` | 5 | vlandia | 52.1 | 30 | 46 | 58 | 60.8 | TwoHandedPolearm | 130 | 130 |

**Why.** The two archetypes split cleanly on the two heavy terms of the index. Vlandian knights
buy charge (32, the highest real value in the set) on a slower horse (49); Imperial cataphracts
buy mounted armour (80.7–92.5, the highest in the set) on a faster one (59). At the top they
cancel out — the Elite Cataphract and the Banner Knight tie at 73.5, from opposite directions —
and rider skill 260/200 is what lifts both above their tier-4 versions. The Faris is the
outlier build: worst charge of the top ten (20) but the best manoeuvre (73) and near-top armour,
so it ranks on staying power rather than impact.
**Four `tutorial_npc_*` Training Masters occupy ranks 5, 9, 10 and 11 and should be ignored as
troops.** They ride the fastest, highest-charge horse in the game (35/65/65) with almost no
armour (20.9–26.5) and, being `skill_template` troops, contribute 0 to the rider-skill term.
They are exactly the kind of id the §2 obsolete gap would remove; they are shown rather than
silently dropped because the universe rule is "reproducible from the pack".
Cross-check columns `defensive_role_score` and `offensive_melee_role_score` are in the CSV, and
they only partly agree with the index. v1 defensive ranks the Elite Cataphract first as well
(100.0), but puts the Druzhinnik Champion second (97.6) where the index has it eighth, and the
Faris fourth (94.8) against sixth here. The reason is mechanical and worth stating: v1 defensive
is armour-and-shield weighted and reads the horse only as a flat +6, while the index gives 55%
of its weight to horse charge, speed and manoeuvre. Sturgian and Aserai cavalry are armoured on
slow or low-charge mounts, so they place higher on v1 defensive than on a shock reading. Where
the two disagree, prefer v1 for "will it survive" and the index for "will the charge land" —
and treat neither as calibrated.

### 5.7 Horse archer — n=19 ranked

Mounted bow users. Ranked by `ranged_role_score` (v1 merges horse archers into Ranged and adds
`+8` for a horse plus a mobility factor `1 + 0.08·has_horse + Riding/1000`, clipped at 1.25).

| # | tier | troop | troop_id | tier(tree) | culture | v1 ranged | ranged base | bow+arrow dmg | Bow skill | arrows | Ride | hspeed | eff. armor |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | Khuzait Khan's Guard | `khuzait_khans_guard` | 5 | khuzait | 100.0 | 76.2 | 54 | 200 | 48 | 200 | 60 | 50.0 |
| 2 | A | Khuzait Kheshig | `khuzait_kheshig` | 4 | khuzait | 73.7 | 73.9 | 55 | 160 | 24 | 130 | 60 | 34.9 |
| 3 | B | Aserai Mamluke Heavy Cavalry | `aserai_mameluke_heavy_cavalry` | 5 | aserai | 66.0 | 73.5 | 56 | 130 | 23 | 130 | 51 | 37.0 |
| 4 | B | Imperial Bucellarii | `bucellarii` | 5 | empire | 63.5 | 74.3 | 53 | 140 | 40 | 120 | 50 | 35.1 |
| 5 | B | Khuzait Heavy Horse Archer | `khuzait_heavy_horse_archer` | 5 | khuzait | 63.1 | 76.2 | 54 | 130 | 48 | 130 | 47 | 45.1 |
| 6 | B | Conspiracy Mounted Master Archer | `conspiracy_mounted_master_archer` | — | khuzait | 57.3 | 76.2 | 54 | 120 | 48 | 130 | 47 | 32.6 |
| 7 | B | Conspiracy Packmaster | `conspiracy_packmaster` | — | empire | 54.8 | 75.8 | 55 | 120 | 40 | 130 | 50 | 28.4 |
| 8 | B | Aserai Mamluke Cavalry | `aserai_mameluke_cavalry` | 4 | aserai | 50.9 | 72.6 | 56 | 100 | 23 | 110 | 54 | 34.1 |
| 9 | B | Karakhergit Elder | `karakhuzaits_tier_3` | 3 | khuzait | 48.2 | 73.1 | 54 | 110 | 27 | 100 | 60 | 39.1 |
| 10 | B | Khuzait Horse Archer | `khuzait_horse_archer` | 4 | khuzait | 45.9 | 75.3 | 54 | 100 | 48 | 100 | 47 | 34.7 |
| 11 | B | Khuzait Torguud | `khuzait_torguud` | 3 | khuzait | 42.7 | 71.5 | 54 | 100 | 24 | 100 | 47 | 29.0 |
| 12 | C | Karakhergit Rider | `karakhuzaits_tier_2` | 2 | khuzait | 30.8 | 70.7 | 52 | 80 | 27 | 60 | 47 | 25.6 |

**Why.** The kit is almost constant across the role — ranged base 70.7–76.2, damage 52–56,
horse speed 47–60 — so this table is a skill ladder. The Khan's Guard takes the normalised 100.0
on 200 Bow *and* 200 Riding (the only troop maxing both terms of the score) with the joint-best
armour; strip the skills and its hardware is the same steppe bow as the tier-4 Horse Archer at
#10. Culture concentration is extreme: 14 of 19 are Khuzait, 3 Imperial, 2 Aserai, and there is
no Battanian, Sturgian, Vlandian or Nord horse archer at all in vanilla. That, not the top of
the table, is the tactically relevant fact — the role is a Khuzait monopoly with two thin
imports.

---

## 6. Troops that could not be ranked in their role

18 of the 283 soldiers carry no score in their own role's primary column, all for the same
reason: v1 multiplies the ranged, offensive-melee and skirmisher scores by a skill factor, and
the skill that factor needs is blank in the pack, so the product is NaN. Fourteen are
`skill_template` troops with all eight skill columns empty. The other four are arena fighters
with a stranger defect — every melee skill blank but `Bow = 300`, a value no real troop carries
and which no bow in their kit could use. They are listed here rather than imputed: filling in
skills would be a model change, and the `Bow = 300` rows should be raised as an audit-side data
question.

| role | troop_id | troop | culture | reason |
|---|---|---|---|---|
| shock infantry | `champion_fighter` | Champion Fighter | empire | melee skills blank (`Bow = 300`, no bow) |
| shock infantry | `regular_fighter` | Regular Fighter | empire | melee skills blank (`Bow = 300`, no bow) |
| shock infantry | `sword_sister` | Sword Sister | empire | melee skills blank (`Bow = 300`, no bow) |
| shock infantry | `veteran_fighter` | Veteran Fighter | empire | melee skills blank (`Bow = 300`, no bow) |
| archer | `aserai_militia_archer` / `aserai_militia_veteran_archer` | Aserai Militia (Veteran) Archer | aserai | blank skills |
| archer | `battanian_militia_archer` / `battanian_militia_veteran_archer` | Battanian Militia (Veteran) Archer | battania | blank skills |
| archer | `imperial_militia_archer` / `imperial_militia_veteran_archer` | Imperial Militia (Veteran) Archer | empire | blank skills |
| archer | `khuzait_militia_archer` / `khuzait_militia_veteran_archer` | Khuzait Militia (Veteran) Archer | khuzait | blank skills |
| archer | `nord_militia_archer` / `nord_militia_veteran_archer` | Nord Militia (Veteran) Archer | nord | blank skills |
| archer | `sturgian_militia_archer` / `sturgian_militia_veteran_archer` | Sturgian Militia (Veteran) Archer | sturgia | blank skills |
| crossbow | `vlandian_militia_archer` / `vlandian_militia_veteran_archer` | Vlandian Militia (Veteran) Crossbowman | vlandia | blank skills |

Line infantry, shock cavalry and thrower have no unranked members: `defensive_role_score` and
the descriptive cavalry index are not skill-gated, and the militia spearmen therefore do appear
in §5.2 on armour and shield alone. Their skill columns are still blank — read their positions
as kit-only.

---

## 7. S+ outliers (giants / mammoths and other outsized units)

**None in this track.** The outlier test used by the theoretical overviews —
`giant`/`mammoth` matched against `troop_id` and `troop_name` — returns 0 of 283 vanilla
soldiers, which is expected: outsized units are mod content (ROT dragons/giants, TAOM mammoths),
not Native/NavalDLC. Consequently the S–D bands in §5 cover the whole vanilla roster and no
troop was excluded from ordinary commentary on spectacle grounds. The section is kept so the
vanilla report reads against the mod-track reports without a structural gap.

The nearest vanilla analogue is the `tutorial_npc_*` Training Masters of §5.6 — not outsized,
but off-scale for a different reason (tutorial-only horse, no skills). They are called out in
place rather than parked here, because "S+ outlier" in this project means *unit scale*, not
*data artefact*.

---

## 8. Companion CSVs

Full ranked lists, every troop in the role, with rank, tier, `troop_id`, tree tier, culture,
level, `line_status_corrected`, roster count, the primary score and every driver column named
in §4:

| file | rows |
|---|---|
| `role_report_shock_infantry.csv` | 37 |
| `role_report_line_infantry.csv` | 90 |
| `role_report_archer.csv` | 38 |
| `role_report_crossbow.csv` | 11 |
| `role_report_thrower.csv` | 21 |
| `role_report_shock_cavalry.csv` | 49 |
| `role_report_horse_archer.csv` | 19 |

Rows are the *ranked* members of each role; the 18 unranked troops of §6 are listed in this
document only.

---

## 9. Limitations

1. **No melee damage exists in this track.** All 3,619 melee/throwing weapon rows are
   `CraftedItem` with `crafted_stats_reconstructed == False`. Every melee ordering here is a
   template-class proxy from the frozen v1 tables; §5.1 in particular ranks weapon classes, not
   damage output.
2. **No thrown-weapon stats.** Only 7 of 784 rosters carry a direct `Thrown` item; the javelin
   block of §5.5 shares one flat proxy value.
3. **`skill_template` is not modelled** (SCHEMA "Known limitations"), leaving 45 of 283 soldiers
   with all eight skill columns blank. 18 soldiers end up unrankable in their own role (§6):
   14 of those 45, plus 4 arena fighters whose only non-blank skill is an implausible
   `Bow = 300`.
4. **Universe is 283, not the documented 272** — the ~11 non-`mp_*` obsolete ids cannot be
   identified from the pack (§2). Fix belongs at the pack/export layer.
5. **`upgrade_requires` is not modelled**, so availability commentary based on `tree_tier`
   ignores upgrade gating; `tree_tier` is also blank for unlinked troops, which makes the
   "surprise" reading of low-tier marines softer than it looks.
6. **Damage types are not compared across `Cut`/`Pierce`/`Blunt`**, and crossbow reload is not
   modelled — §5.4's raw damage advantage over bows is not a combat advantage.
7. **role_scores_v1 is conservative and not final** (`score_status =
   role_scores_v1_conservative_not_final`). Its 0–100 scales are min-max normalisations over
   *this* universe: adding or removing troops moves every number. The scores in this report are
   normalised over the 283-soldier universe defined in §2 and are therefore not directly
   comparable to any earlier vanilla v1 file computed over a different universe (e.g.
   `data/vanilla/role_scores/`, which includes `mp_*` troops).
8. **Recommendations only.** Where the data contradicts a frozen ranking, this report says so
   and stops; `analysis/model_versions/` was not touched.
