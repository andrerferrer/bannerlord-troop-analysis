# Bannerlord Troop Analysis — Complete Project Handoff

**Repository:** `andrerferrer/bannerlord-troop-analysis`  
**Authoritative branch:** `main`  
**Primary scope of this handoff:** official Bannerlord troops from vanilla modules plus War Sails / `NavalDLC`  
**Current overall model:** **v7.1 — head-weighted general battlefield score**  
**Current context model:** **v7.3 — tooltip-validated throwing burst score**  
**Open validation priority:** **Battanian Skipari empirical burst performance**  
**Purpose:** allow a new ChatGPT conversation with GitHub access to continue without relying on this chat history.

---

## 1. Read this first

The project now has **two authoritative rankings** that answer different questions:

```txt
v7.1 general_score
= overall battlefield value across sustained combat
```

```txt
v7.3 burst_score
= first-contact / short-duration kill pressure
```

Do not merge them into one score without a new, explicit calibration exercise.

Current headline results:

```txt
GENERAL TOP 3 — v7.1
1. Khuzait Khan's Guard
2. Battanian Fian Champion
3. Aserai Vanguard Faris
```

```txt
BURST TOP 3 — v7.3
1. Aserai Vanguard Faris
2. Battanian Skipari
3. Imperial Naute
```

The Imperial Naute is the clearest example of the distinction:

```txt
v7.1 regular combined general rank: #42
v7.3 regular combined burst rank:   #3
```

Interpretation:

- the Naute is **not** claimed to be the third-best troop in every battle;
- the Naute is claimed to have elite early kill pressure because it carries two real stacks of high-damage javelins;
- screenshots support the idea that it overperforms its general rank in short fights.

---

## 2. Exact files a new chat should read

Read these in order:

1. `docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md`
2. `docs/handoff/NEW_CHAT_STARTER.md`
3. `README.md`
4. `analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_summary.md`
5. `analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_assumptions.md`
6. `analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top20_burst_units_regular_compact.csv`
7. `analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_key_burst_cases_compact.csv`
8. `analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_findings_2026-06-04.md`
9. `analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_troop_aggregate_summary.csv`
10. `analysis/item_validation/2026-06-05_throwing_tooltips/findings.md`
11. `analysis/item_validation/2026-06-05_throwing_tooltips/item_tooltip_validation_20260605.csv`
12. `scripts/build_v72_burst_score.py`
13. `scripts/build_v73_tooltip_damage_burst.py`
14. GitHub issue `#2`

The repository also contains Realm of Thrones work. That material is separate. It must not be allowed to silently change the official vanilla + War Sails conclusions documented here.

---

## 3. Project objective

The project is not intended to be a casual tier list. It is an interpretable modeling pipeline built from exported Bannerlord XML and in-game validation.

The intended pipeline is:

```txt
XML export
→ troop/item/equipment normalization
→ per-roster loadout resolution
→ weapon and armor metrics
→ HTK/KPM offense estimates
→ defense and reliability scores
→ general and contextual rankings
→ empirical screenshot validation
→ item-tooltip validation
```

Primary questions:

```txt
Best troop overall
Best troop by tier
Best offensive infantry
Best defensive infantry
Best offensive cavalry
Best defensive cavalry
Best archer
Best crossbowman
Best horse archer
Best non-noble troop
Best upgrade path
Best burst troop
```

---

## 4. Official source scope

Official modules included in the full export/model work:

```txt
Native
SandBox
SandBoxCore
StoryMode
CustomBattle
NavalDLC
```

`NavalDLC` is the official module used by War Sails.

Observed dataset sizes during the v7 audit:

```txt
305 official troops in the full model
230 vanilla/pre-War-Sails troops
75 NavalDLC troops
150 regular culture-tree troops in the main combined ranking scope
```

The project distinguishes:

```txt
all official troops
```

from:

```txt
regular culture-tree troops
```

The main public rankings use regular culture-tree troops. The all-official table is diagnostic and may include caravan guards, mercenaries, special templates, or other nonstandard units.

---

## 5. Normalized troop model

Important normalized troop fields include:

```txt
troop_id
name
culture
tier
is_noble
is_mounted
is_ranged
is_terminal
upgrade_targets
```

Skills:

```txt
onehanded
twohanded
polearm
bow
crossbow
throwing
riding
athletics
```

Armor:

```txt
head_armor
body_armor
arm_armor
leg_armor
armor_total
survivability_armor_v71
```

Equipment flags:

```txt
has_shield
has_bow
has_crossbow
has_throwing
has_polearm
has_twohander
has_horse
has_couch_lance
```

Weapon fields:

```txt
primary_melee_damage
primary_melee_damage_type
primary_melee_speed
primary_melee_reach
primary_ranged_damage
primary_ranged_damage_type
primary_ranged_speed
primary_ranged_accuracy
primary_ranged_ammo
primary_throw_damage
primary_throw_damage_type
primary_throw_ammo
```

Tooltip validation fields added later:

```txt
tooltip_throw_name
tooltip_throw_damage
tooltip_throw_damage_type
tooltip_throw_weapon_length
tooltip_throw_missile_speed
tooltip_throw_accuracy
tooltip_throw_stack_amount
tooltip_throw_visible_stacks
tooltip_throw_total_ammo
```

---

## 6. Simplified role taxonomy

The official model uses:

```txt
Offensive Infantry
Defensive Infantry
Offensive Cavalry
Defensive Cavalry
Archer
Crossbowman
Horse Archer
```

Important modeling rule:

```txt
Archer, Crossbowman, and Horse Archer are ranged-first roles.
```

Their melee weapons are fallback tools and must not automatically replace their ranged offense just because a melee KPM proxy is numerically higher.

---

## 7. Core HTK/KPM foundation

Standard target HP:

```txt
enemy_hp = 100
```

First-pass effective damage proxy:

```txt
base_after_armor = raw_damage × 100 / (100 + armor)
```

Damage-type modifiers used in the model lineage:

```txt
Blunt = 1.10
Pierce = 1.00
Cut = 0.85
```

Then:

```txt
effective_damage = base_after_armor × damage_type_modifier
HTK = enemy_hp / effective_damage
```

Melee attempts and hit chance:

```txt
melee_attempts_per_minute = 12 × weapon_speed / 100
melee_hit_chance = clamp(0.75 + melee_skill / 1000, 0.60, 0.95)
melee_kpm = attempts_per_minute × hit_chance / HTK
```

Bow hit chance:

```txt
bow_hit_chance = clamp(0.35 + bow_skill / 500, 0.30, 0.90)
```

Crossbow hit chance:

```txt
crossbow_hit_chance = clamp(0.45 + crossbow_skill / 650, 0.35, 0.90)
```

Ammo capacity concept:

```txt
expected_kill_capacity = ammo × hit_chance / HTK
```

These are transparent proxies, not claims of exact engine reproduction.

---

## 8. General score architecture

The authoritative general score remains:

```txt
total_score_v71 =
0.65 × offense_score_v7
+ 0.20 × defense_score_v71
+ 0.15 × reliability_score
```

Design intent:

- offense receives the largest weight;
- armor alone cannot create a top troop;
- reliability is separate from defense;
- a glass cannon can rank highly when its kill pressure is credible;
- shield and horse durability matter, but must not overwhelm offense.

---

## 9. Model version history and resolved failures

### Early vanilla pipeline

The first full analysis parsed troops, items, armor, horses, skills, trees, and equipment. It produced plausible headline units but exposed role and parsing problems.

### v4 — throwing calibration

Observed failure:

```txt
Aserai Vanguard Faris ranked around #46 instead of elite top 3.
```

Cause:

```txt
throw_blend = 0.35 × throw + 0.65 × melee
```

That treated Faris mainly as unreliable lance cavalry.

Correction:

- throwing received greater weight;
- mounted throwing received a bonus;
- high-ammo javelin troops gained real first-contact value;
- Faris returned to the expected elite group.

### v5 — ranged role correction

Observed failure:

```txt
Aserai Archer > Aserai Master Archer
```

The XML was not the main problem. The model used:

```txt
offense = max(melee, ranged, throw)
```

The T4 Archer's blunt melee weapon allowed it to beat the T5 Master Archer despite inferior bow skill and ranged KPM.

Correction:

- foot archers became ranged-first;
- crossbowmen became ranged-first;
- melee became a capped fallback;
- the correct line order was restored:

```txt
Aserai Master Archer > Aserai Archer > Aserai Light Archer
```

### v5.1 — horse archer ranged-first

Horse archers also became ranged-first with capped melee fallback.

This preserved Khan's Guard as elite, but exposed that Kheshig and Torguud had previously been carried heavily by melee/glaive output.

### War Sails failure — the Nord Huscarl false #1

An early combined ranking produced:

```txt
Nord Huscarl #1 overall
```

This was rejected as model slop.

Concrete causes:

1. alternative `EquipmentRoster` blocks were merged into one super-loadout;
2. arrows/bolts were summed across alternative rosters;
3. crafted weapon reconstructions were treated as exact;
4. spear + shield infantry KPM was overestimated;
5. low-ammo throwing axes were treated as sustained pressure;
6. offense normalization saturated too early.

### Crossbow roster bug

Example:

```txt
Vlandian Nauta correct ammo per spawn: 18 bolts
bugged merged-roster ammo:            54 bolts
```

This falsely put Nauta above Sharpshooter.

Corrected conclusion under v7.1:

```txt
Vlandian Sharpshooter > Vlandian Nauta
```

They have comparable basic ranged output, but Sharpshooter has much stronger defense.

### v7 — roster-first correction

Correct algorithm:

```txt
score roster 1
score roster 2
score roster 3
average the roster scores
```

Incorrect old algorithm:

```txt
roster 1 + roster 2 + roster 3
```

Important nuance:

```txt
Two javelin stacks inside one roster are real and must both count.
The same javelin stack repeated across alternative rosters must not be summed.
```

v7 sanity checks:

```txt
Sharpshooter > Nauta
Nord Huscarl is not #1 overall
Vanguard Faris remains top 3 vanilla
```

### v7.1 — head-weighted survivability armor

Old armor proxy:

```txt
0.70 body + 0.10 head + 0.10 arm + 0.10 leg
```

This overvalued torso-heavy troops with poor helmets.

Deep research found strong evidence that:

- Bannerlord tracks the struck body part;
- headshots are explicitly handled and more lethal;
- the pierce headshot multiplier was increased in official balancing;
- leg damage was explicitly reduced;
- no reliable public telemetry dataset gives exact head/body/arm/leg hit frequencies.

Therefore the new value is a **lethality-weighted survivability proxy**, not a measured hit-frequency equation:

```txt
survivability_armor_v71 =
0.55 × body_armor
+ 0.35 × head_armor
+ 0.05 × arm_armor
+ 0.05 × leg_armor
```

### v7.2 — context-only burst score

Empirical screenshots showed that high-ammo throwing infantry could heavily outperform their general rank in short engagements.

The user explicitly chose to add only:

```txt
burst_score
```

Intentionally rejected for now:

```txt
boarding_score
short_engagement_score
siege_defense_score
```

### v7.2.1 — in-game tooltip validation

In-game encyclopedia screenshots validated item names, damage, damage type, stack amount, and visible stack count.

### v7.3 — tooltip throwing damage becomes authoritative

The user correctly decided:

```txt
If the in-game tooltip displays the real item stat, use it as the source of truth.
```

For validated throwing items:

```txt
throw_damage_used_v73 = tooltip_throw_damage
```

For unvalidated items:

```txt
throw_damage_used_v73 = model proxy fallback
```

---

## 10. Authoritative general ranking — v7.1

### Regular combined top 10

| Rank | Troop | Tier | Category | General score v7.1 |
|---:|---|---:|---|---:|
| 1 | Khuzait Khan's Guard | 6 | Horse Archer | 92.901 |
| 2 | Battanian Fian Champion | 6 | Archer | 92.442 |
| 3 | Aserai Vanguard Faris | 6 | Offensive Cavalry | 90.156 |
| 4 | Battanian Fian | 5 | Archer | 89.055 |
| 5 | Imperial Elite Menavliaton | 5 | Offensive Infantry | 88.687 |
| 6 | Sturgian Heroic Line Breaker | 5 | Offensive Infantry | 87.696 |
| 7 | Vlandian Voulgier | 5 | Offensive Infantry | 86.995 |
| 8 | Imperial Menavliaton | 4 | Offensive Infantry | 85.208 |
| 9 | Battanian Veteran Falxman | 5 | Offensive Infantry | 84.555 |
| 10 | Imperial Legionary | 5 | Defensive Infantry | 84.229 |

### War Sails / NavalDLC general top 10

| Rank WS | Troop | Tier | Category | General score v7.1 |
|---:|---|---:|---|---:|
| 1 | Nord Ulfhedinn | 5 | Offensive Infantry | 78.402 |
| 2 | Aserai Bahriyyah | 5 | Archer | 75.618 |
| 3 | Nord Berserkir | 5 | Offensive Infantry | 74.952 |
| 4 | Nord Huscarl | 6 | Offensive Infantry | 74.803 |
| 5 | Vlandian Nauta | 5 | Crossbowman | 74.356 |
| 6 | Nord Skjaldbrestir | 5 | Offensive Infantry | 74.251 |
| 7 | Battanian Skipari | 5 | Offensive Infantry | 74.220 |
| 8 | Nord Sky-Gods Chosen | 5 | Archer | 74.041 |
| 9 | Imperial Naute | 5 | Offensive Infantry | 72.601 |
| 10 | Vlandian Seasoned Seafarer | 4 | Crossbowman | 72.553 |

### General interpretation

- Khan's Guard remains the best complete package: ranged uptime, mobility, survivability, and melee fallback.
- Fian Champion remains the strongest foot ranged benchmark.
- Vanguard Faris combines elite throwing burst with exceptional survivability.
- Imperial Elite Menavliaton, Heroic Line Breaker, Voulgier, and Falxman lead sustained shock infantry.
- Legionary remains a premier defensive infantry benchmark.
- Imperial Naute is a good T5 general troop but not an elite sustained-combat unit by the current general model.

---

## 11. Authoritative burst model — v7.3

### Purpose

`burst_score_v73` answers:

```txt
Which troop can generate the strongest first-contact or short-duration kill pressure?
```

It does not answer:

```txt
Which troop is best overall across a full battle?
```

### Tooltip-first throwing input

```txt
throw_damage_used_v73 =
tooltip_throw_damage if validated
else primary_throw_damage proxy
```

### Throw-specific calibration

A direct multiplication of old proxy throw pressure by `tooltip/proxy damage ratio` was rejected because it caused nearly all validated javelins to saturate at 100.

Instead:

```txt
throw_damage_factor_v73 = clamp(damage / 110, 0.70, 1.10)
```

```txt
throw_skill_factor_v73 =
clamp(0.75 + throwing_skill / 400, 0.75, 1.20)
```

```txt
throw_ammo_factor_v73 =
0.70
+ 0.08 × min(ammo, 5)
+ 0.04 × min(max(ammo - 5, 0), 5)
```

```txt
mounted_throw_bonus_v73 =
1.12 if mounted else 1.00
```

Throwing damage-type factor:

```txt
Pierce = 1.00
Blunt = 0.96
Cut = 0.88
```

The throw scale is normalized around a Faris-like benchmark:

```txt
Jereed
121 tooltip damage
140 throwing skill
5 ammo
mounted
```

### Parallel burst candidates

The v7.3 implementation compares context-specific burst candidates from:

```txt
throw
ranged
charge
melee
```

It selects the strongest burst source for each troop and then combines it with smaller reliability and defense contributions.

### v7.3 regular combined burst top 20

| Rank | Troop | Tier | Category | Burst score | Burst source | v7.1 general rank |
|---:|---|---:|---|---:|---|---:|
| 1 | Aserai Vanguard Faris | 6 | Offensive Cavalry | 96.026 | throw | 3 |
| 2 | Battanian Skipari | 5 | Offensive Infantry | 92.910 | throw | 38 |
| 3 | Imperial Naute | 5 | Offensive Infantry | 92.828 | throw | 42 |
| 4 | Battanian Fian Champion | 6 | Archer | 90.161 | ranged | 2 |
| 5 | Aserai Veteran Faris | 5 | Offensive Cavalry | 85.218 | throw | 83 |
| 6 | Imperial Coast Guard | 4 | Offensive Infantry | 84.188 | throw | 69 |
| 7 | Battanian Fian | 5 | Archer | 78.467 | ranged | 4 |
| 8 | Khuzait Khan's Guard | 6 | Horse Archer | 78.030 | ranged | 1 |
| 9 | Battanian River Raider | 4 | Offensive Infantry | 77.213 | throw | 58 |
| 10 | Battanian Mounted Skirmisher | 5 | Defensive Cavalry | 71.127 | throw | 13 |
| 11 | Sturgian Horse Raider | 5 | Defensive Cavalry | 68.576 | throw | 84 |
| 12 | Vlandian Banner Knight | 6 | Offensive Cavalry | 67.728 | charge | 12 |
| 13 | Aserai Master Archer | 5 | Archer | 67.471 | ranged | 34 |
| 14 | Khuzait Heavy Horse Archer | 5 | Horse Archer | 66.907 | ranged | 25 |
| 15 | Imperial Elite Cataphract | 6 | Defensive Cavalry | 66.856 | charge | 17 |
| 16 | Imperial Palatine Guard | 5 | Archer | 66.828 | ranged | 41 |
| 17 | Vlandian Champion | 5 | Defensive Cavalry | 65.812 | charge | 14 |
| 18 | Sturgian Druzhinnik Champion | 6 | Defensive Cavalry | 65.024 | charge | 22 |
| 19 | Khuzait Kheshig | 5 | Horse Archer | 64.470 | melee | 105 |
| 20 | Imperial Cataphract | 5 | Defensive Cavalry | 64.314 | charge | 27 |

### Burst interpretation

- Faris is the validated mounted-javelin benchmark.
- Skipari and Naute are elite foot-javelin burst units because each carries two real stacks of five Hooked Javelins.
- Fian Champion remains elite because high ranged first-contact pressure is also burst.
- Khan's Guard ranks lower in burst than general because much of its value is sustained mobility, uptime, and fallback quality rather than only first-contact output.
- Banner Knight and Elite Cataphract appear through charge burst, but general cavalry modeling remains less empirically validated than throwing and ranged.

---

## 12. War Sails-specific findings

### Imperial naval line

```txt
Imperial Shipmate — Tier 3
→ Imperial Coast Guard — Tier 4
→ Imperial Naute — Tier 5
```

### Imperial Naute profile

Validated equipment behavior:

```txt
Hooked Javelin
stack amount: 5
visible throwing stacks: 2
total inferred ammo: 10
tooltip damage: 117 Pierce
```

Melee fallback:

```txt
Tzikourion
```

General model position:

```txt
War Sails regular general rank: #9
combined regular general rank:  #42
```

Burst model position:

```txt
combined regular burst rank: #3
```

### Imperial Coast Guard correction

The model had labeled the Coast Guard's throwing item as:

```txt
Broad Blade Javelin
```

The in-game tooltip showed:

```txt
Harpoon
113 Pierce
stack amount 5
2 visible stacks
10 total ammo
```

The model/input documentation was corrected to use Harpoon.

### Nord Huscarl conclusion

The Huscarl is a strong War Sails unit, but the old #1 overall result was invalid.

Current interpretation:

```txt
strong elite infantry
not best official troop in the game
```

Its low-ammo throwing axe must be treated as limited burst, and spear + shield utility must not be converted directly into shock-infantry KPM.

---

## 13. Item tooltip validation

Validated in-game throwing stats:

| Troop | Item | Tooltip damage | Type | Stack | Visible stacks | Total ammo |
|---|---|---:|---|---:|---:|---:|
| Aserai Vanguard Faris | Jereed | 121 | Pierce | 5 expected | 1 | 5 |
| Battanian Skipari | Hooked Javelin | 117 | Pierce | 5 | 2 | 10 |
| Imperial Naute | Hooked Javelin | 117 | Pierce | 5 | 2 | 10 |
| Battanian River Raider | Broad Blade Javelin | 101 | Pierce | 5 | 2 | 10 |
| Imperial Coast Guard | Harpoon | 113 | Pierce | 5 | 2 | 10 |

Important consequence:

```txt
The high Skipari and Naute burst scores are not caused by an ammo-counting bug.
```

The open uncertainty is AI battlefield performance, especially for Skipari.

Proxy versus tooltip examples:

```txt
Hooked Javelin proxy:       45.2
Hooked Javelin tooltip:    117

Broad Blade proxy:          48.0
Broad Blade tooltip:       101

Jereed proxy:               54.4
Jereed tooltip:            121
```

The proxy values remain useful only as fallbacks for unvalidated items.

---

## 14. Empirical screenshot validation

### Normalization schema

Battle-result columns were interpreted as:

```txt
ready_alive
kills
upgrades
dead
wounded
prisoners
```

Derived metrics:

```txt
estimated_present = ready_alive + dead + wounded
kills_per_present = kills / estimated_present
casualty_rate = (dead + wounded) / estimated_present
```

### Aggregate observations currently stored

Selected aggregate rows:

| Troop | Observations | Present | Kills | Weighted kills/present | Casualty rate | v7.1 general rank |
|---|---:|---:|---:|---:|---:|---:|
| Khuzait Khan's Guard | 12 | 198 | 331 | 1.672 | 12.1% | 1 |
| Imperial Elite Menavliaton | 6 | 55 | 73 | 1.327 | 45.5% | 5 |
| Imperial Naute | 17 | 229 | 263 | 1.148 | 67.2% | 42 |
| Nord Sky-Gods Chosen | 9 | 49 | 56 | 1.143 | 40.8% | 40 |
| Imperial Sergeant Crossbowman | 12 | 183 | 196 | 1.071 | 24.0% | 35 |
| Aserai Vanguard Faris | 4 | 35 | 35 | 1.000 | 77.1% | 3 |

### What the screenshots support

Strong current signals:

```txt
Khan's Guard S-tier general consistency: supported
Imperial Naute short-fight burst overperformance: supported
Imperial Sergeant Crossbowman stable output: supported
War Sails Nord infantry strong but not game-breaking: supported
Nord Huscarl #1 overall: rejected
```

### Empirical limitations

The screenshot dataset is not a controlled laboratory sample.

It includes:

- mixed troop compositions;
- different enemy quality;
- different commander/perk contexts;
- field battles, villages, chokepoints, and siege contexts;
- some modded/Realm of Thrones opponents;
- small-sample rows with unstable kills-per-present values.

Therefore:

```txt
Do not fit a full general-score regression directly to these aggregate rows.
```

Use them as directional validation and to design controlled future tests.

---

## 15. Armor research conclusion

The deep research result was:

```txt
Head armor should weigh much more than 10% in a survivability proxy.
```

What is well-supported:

- actual hit body part is tracked;
- headshots receive special treatment;
- head hits are more lethal;
- leg damage is deweighted;
- the four displayed armor values are only a compression of more granular hit zones.

What is not available:

```txt
A reliable public dataset proving exact AI hit frequencies such as
30% head / 60% body / 5% arm / 5% leg.
```

The adopted formula:

```txt
55% body
35% head
5% arm
5% leg
```

is a modeling choice for expected survival, not the game's hidden exact formula.

Do not silently rename it to “true effective armor.” Prefer:

```txt
survivability_armor_v71
```

---

## 16. Current confidence by subsystem

| Subsystem | Confidence | Reason |
|---|---|---|
| Vanilla troop/item XML parsing | High | Fully exported and repeatedly audited |
| EquipmentRoster alternatives | High | v7 roster-first logic fixes known overcount |
| Vanilla ranged role scoring | Medium-high | Archer/Master Archer bug corrected; plausible ordering |
| Crossbow ammo/loadout parsing | High | Nauta overcount found and corrected |
| High-ammo javelin loadouts | High | In-game tooltip and stack screenshots |
| v7.3 throwing raw item stats | High for validated items | Tooltip used as source of truth |
| General throwing performance | Medium | Empirical support exists but contexts vary |
| Battanian Skipari burst rank | Medium-low | Loadout validated, controlled battle output missing |
| Shock cavalry charge model | Medium-low | Directionally improved, insufficient controlled evidence |
| Crafted unvalidated War Sails weapons | Low-medium | Proxy fallback remains |
| General score exact ordering below top group | Medium | Sensitive to AI/context assumptions |
| Head/body armor exact weights | Medium | Direction supported, exact coefficients not empirically measured |

---

## 17. Known open question

The main official-model issue still open is GitHub issue `#2`:

```txt
Validate Battanian Skipari burst ranking empirically.
```

What is already validated:

```txt
Hooked Javelin
117 Pierce tooltip damage
5 per stack
2 visible stacks
10 total ammo
throwing skill around 140 in model data
```

What is not validated:

```txt
Does the AI produce battle output close to Imperial Naute and Vanguard Faris?
```

Recommended controlled test:

```txt
20–40 Battanian Skipari
20–40 Imperial Naute
20–40 Aserai Vanguard Faris
20–40 Battanian Fian Champion
```

Use the same or closely matched enemy composition and record multiple repetitions in:

```txt
short open-field contact
village/chokepoint contact
```

Do not close issue #2 based only on item screenshots; those validate loadout, not AI application.

---

## 18. Exact next recommended action

The next action should be **empirical**, not another broad formula rewrite.

### Priority 1 — Skipari controlled results

Collect at least three comparable battle-result screenshots for Skipari.

Minimum fields:

```txt
troop
initial or estimated present
remaining/ready
dead
wounded
kills
battle context
```

### Priority 2 — remaining tooltip-proxy throwing units

Useful next item screenshots:

```txt
Battanian Mounted Skirmisher
Sturgian Horse Raider
Imperial Shipmate
Sturgian Reaver
Nord Huscarl throwing axe
Nord Skjaldbrestir throwing axe
```

### Priority 3 — add confidence scoring

A future model version should add:

```txt
item_input_confidence
empirical_sample_confidence
model_confidence
```

Suggested factors:

```txt
tooltip validated?
exact XML weapon or crafted reconstruction?
number of empirical observations?
controlled or mixed battle context?
roster variation?
```

Do not change v7.1 general-score weights until new controlled evidence justifies it.

---

## 19. Reproduction scripts and artifacts

Current scripts:

```txt
scripts/build_v72_burst_score.py
scripts/build_v73_tooltip_damage_burst.py
```

Important note:

The repository intentionally stores compact ranking/audit outputs. Some full intermediate model artifacts originated as generated local CSVs and may not all be committed because of repository size and iteration history.

A new chat should therefore:

1. treat committed compact outputs and summaries as authoritative current snapshots;
2. inspect script input paths before claiming a clean end-to-end rebuild;
3. avoid saying “fully reproducible” unless every referenced input CSV exists on `main`;
4. add a reconstruction script or required compact input snapshot before the next full rerun.

This is a technical reproducibility gap, not a reason to discard the current validated conclusions.

---

## 20. Repository file map

### Handoff

```txt
docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md
docs/handoff/NEW_CHAT_STARTER.md
README.md
```

### Empirical screenshot validation

```txt
analysis/empirical/screenshots_2026-05-29_2026-06-04/README.md
analysis/empirical/screenshots_2026-05-29_2026-06-04/schema.md
analysis/empirical/screenshots_2026-05-29_2026-06-04/screenshot_manifest.csv
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_battle_results_normalized.csv
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_troop_aggregate_summary.csv
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_aggregate_summary.md
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_findings_2026-06-04.md
```

### Item tooltip validation

```txt
analysis/item_validation/2026-06-05_throwing_tooltips/item_tooltip_validation_20260605.csv
analysis/item_validation/2026-06-05_throwing_tooltips/findings.md
analysis/item_validation/2026-06-05_throwing_tooltips/screenshot_manifest.csv
```

### v7.2 burst context

```txt
analysis/model_versions/v7.2_burst_score/bannerlord_v72_burst_assumptions.md
analysis/model_versions/v7.2_burst_score/bannerlord_v72_burst_summary.md
analysis/model_versions/v7.2_burst_score/bannerlord_v72_top20_burst_units_regular_combined.csv
analysis/model_versions/v7.2_burst_score/bannerlord_v72_key_burst_cases.csv
analysis/model_versions/v7.2_burst_score/empirical_v72_burst_validation_summary.csv
```

### v7.3 tooltip-first burst

```txt
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_assumptions.md
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_summary.md
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top20_burst_units_regular_compact.csv
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_key_burst_cases_compact.csv
```

### Scripts

```txt
scripts/build_v72_burst_score.py
scripts/build_v73_tooltip_damage_burst.py
```

---

## 21. Rules a new chat must preserve

1. **Do not merge general and burst ranks.**
2. **Do not implement boarding score unless the user explicitly reopens that decision.**
3. **Do not merge alternative EquipmentRosters into one loadout.**
4. **Count multiple throwing stacks only when they coexist inside the same roster.**
5. **Use tooltip damage as source of truth for validated items.**
6. **Use proxy/crafted damage only as a fallback and label its confidence.**
7. **Do not accept Nord Huscarl #1 overall; that result came from known bugs.**
8. **Keep Master Archer above Aserai Archer in ranged-role evaluation unless new data proves otherwise.**
9. **Keep Faris in the elite general group unless controlled evidence contradicts it.**
10. **Do not alter v7.1 general-score weights based only on mixed-context screenshots.**
11. **Do not claim exact engine simulation; HTK/KPM and survivability armor are proxies.**
12. **State assumptions, data source, and confidence for every material model change.**

---

## 22. Current accepted answers

```txt
Best general troop: Khuzait Khan's Guard
Best foot archer: Battanian Fian Champion
Best throwing cavalry / burst benchmark: Aserai Vanguard Faris
Best general defensive infantry benchmark: Imperial Legionary
Best general crossbow comparison: Vlandian Sharpshooter > Vlandian Nauta
Imperial Naute: good T5 general unit, elite burst specialist
Nord Huscarl: strong War Sails elite, not #1 overall
Battanian Skipari: tooltip-supported #2 burst candidate, empirical validation pending
```

---

## 23. Copy-paste prompt for a fresh chat

A shorter ready-to-paste prompt is stored in:

```txt
docs/handoff/NEW_CHAT_STARTER.md
```

Minimum fresh-chat instruction:

```txt
Open andrerferrer/bannerlord-troop-analysis.
Read docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md and docs/handoff/NEW_CHAT_STARTER.md first.
Treat v7.1 as the authoritative general model and v7.3 as the separate burst model.
Do not merge the scores, do not implement boarding_score, and do not merge alternative EquipmentRosters.
Tooltip-validated throwing damage overrides proxy damage.
Issue #2 is the current priority: empirically validate Battanian Skipari's high burst rank.
Before changing a formula, identify the supporting repo files and state the remaining uncertainty.
```

---

## 24. Final state

The model is no longer a single opaque ranking. It is a layered system:

```txt
v7.1 general battlefield value
+
v7.3 first-contact burst value
+
empirical screenshot evidence
+
in-game item-tooltip validation
+
explicit confidence and known limitations
```

The highest-value next work is controlled validation, not another uncontrolled round of formula tuning.
