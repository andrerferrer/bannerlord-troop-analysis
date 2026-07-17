# Bannerlord Troop Analysis — Project Handoff Super Report

**Repository:** `andrerferrer/bannerlord-troop-analysis`  
**Authoritative branch:** `main`  
**Current general model:** **v7.1 — head-weighted survivability armor**  
**Current context model:** **v7.3 — tooltip-validated throwing burst**  
**Prepared for:** restarting the work in a clean ChatGPT conversation with GitHub access.

---

## 1. Executive summary

This project builds an interpretable, data-driven troop analysis pipeline for official **Mount & Blade II: Bannerlord**, covering:

```txt
vanilla modules
+
War Sails / NavalDLC
```

The project started as an HTK/KPM ranking exercise, but several iterations exposed important parsing and modeling errors. Those errors were audited and corrected rather than hidden.

The project now maintains **two separate authoritative scores**:

1. **v7.1 general score** — intended to rank overall battlefield value.
2. **v7.3 burst score** — intended to rank first-contact / short-duration kill pressure.

These scores must not be merged casually. A troop can be excellent at burst without being elite in sustained general combat.

The strongest current conclusions are:

```txt
General top 3:
1. Khuzait Khan's Guard
2. Battanian Fian Champion
3. Aserai Vanguard Faris
```

```txt
Burst top 3:
1. Aserai Vanguard Faris
2. Battanian Skipari
3. Imperial Naute
```

The **Imperial Naute** is the central example of why context scoring was added:

```txt
v7.1 general rank: #42 regular combined
v7.3 burst rank:   #3 regular combined
```

That does not mean the Naute is the third-best troop in every battle. It means its 10 high-damage javelins create elite first-contact pressure.

---

## 2. Scope and source data

### Official modules included

```txt
Native
SandBox
SandBoxCore
StoryMode
CustomBattle
NavalDLC
```

`NavalDLC` is the official module name used by **War Sails**.

### Dataset sizes observed during the v7 review

```txt
305 official troops in the full model
230 vanilla/pre-War-Sails troops
75 NavalDLC troops
150 regular culture-tree troops in the combined ranking scope
```

### Main scope distinction

The project distinguishes:

```txt
all official troops
```

from:

```txt
regular culture-tree troops
```

The regular culture-tree scope is the main ranking scope because it avoids caravan guards, special templates, minor-faction noise, and diagnostic-only troops.

---

## 3. Original model objective

The original workflow aimed to normalize game XML and calculate:

```txt
HTK
melee KPM
ranged KPM
throwing KPM
offense score
defense score
reliability score
total combat score
```

The standard general score remains:

```txt
total_score =
0.65 × offense_score
+ 0.20 × defense_score
+ 0.15 × reliability_score
```

The design intentionally gives offense the largest weight. High armor alone should not make a troop top-tier.

---

## 4. Model version history and what went wrong

### Early vanilla versions

The first vanilla pipeline normalized troops, equipment, skills, weapons, armor, horses, and troop trees. Initial results correctly identified many elite troops, but several model assumptions were too crude.

### v4 — throwing calibration

Problem discovered:

```txt
Aserai Vanguard Faris ranked far too low
```

Cause:

```txt
throw_blend = 0.35 throw + 0.65 melee
```

This treated Faris mainly as unreliable lance cavalry with incidental javelins.

Correction:

- throwing received a much larger role;
- mounted throwing received a bonus;
- Faris moved into the expected top-3 vanilla group.

### v5 — ranged role fix

Problem discovered:

```txt
Aserai Archer ranked above Aserai Master Archer
```

The XML parsing was not the main issue. The general offense formula used:

```txt
max(melee, ranged, throwing)
```

This allowed a foot archer with a favorable melee weapon to be ranked as a melee troop with a bow.

Correction:

- foot archers became ranged-first;
- crossbowmen became ranged-first;
- melee became a capped fallback;
- `Aserai Master Archer > Aserai Archer` was restored.

### v5.1 — horse archer ranged-first

Horse archers were also changed to ranged-first, with capped melee fallback.

This preserved Khan's Guard as elite but exposed that Kheshig/Torguud had previously been carried heavily by glaive/melee output.

### War Sails failure in v4–v6

The early combined War Sails ranking produced obvious nonsense, including:

```txt
Nord Huscarl #1 overall
```

The causes were concrete:

1. **EquipmentRoster alternatives were merged into one super-loadout.**
2. Crossbow bolts/arrows were counted across multiple alternative rosters.
3. Crafted weapons were reconstructed by proxy and treated as exact.
4. Spear + shield infantry KPM was overestimated.
5. Low-ammo throwing axes were treated like sustained throwing pressure.

Example:

```txt
Vlandian Nauta
correct ammo per spawn: 18 bolts
bugged model ammo:       54 bolts
```

### v7 — roster-first correction

v7 corrected the major parsing error:

```txt
score roster 1
score roster 2
score roster 3
then average the roster scores
```

It no longer performs:

```txt
roster 1 + roster 2 + roster 3
```

v7 also preserved multiple throwing stacks **inside the same roster**, which is correct.

Sanity checks passed:

```txt
Vlandian Sharpshooter > Vlandian Nauta
Nord Huscarl is not #1 overall
Vanguard Faris remains top 3 vanilla
```

### v7.1 — head-weighted survivability armor

The old armor proxy was:

```txt
0.70 body
0.10 head
0.10 arm
0.10 leg
```

A deep research review found strong evidence that:

- the engine tracks the struck body part;
- headshots are explicitly treated as more lethal;
- TaleWorlds increased the pierce headshot multiplier;
- leg damage has been explicitly reduced;
- no reliable published hit-frequency dataset exists.

The new metric is explicitly a **lethality-weighted survivability proxy**, not a measured hit-location frequency formula:

```txt
survivability_armor_v71 =
0.55 × body_armor
+ 0.35 × head_armor
+ 0.05 × arm_armor
+ 0.05 × leg_armor
```

This reduced false positives such as torso-heavy troops with weak helmets.

### v7.2 — burst context score

Empirical screenshots showed that throwing troops, especially Imperial Naute, could kill far more than their general rank suggested in short fights.

The user explicitly chose to implement only:

```txt
burst_score
```

The following were intentionally not implemented:

```txt
boarding_score
short_engagement_score
siege_defense_score
```

### v7.2.1 — tooltip validation layer

In-game item screenshots confirmed key throwing loadouts and exposed item-proxy inaccuracies.

### v7.3 — tooltip damage as source of truth

The user correctly decided that in-game tooltip values should be treated as authoritative raw item stats when validated.

v7.3 therefore uses tooltip-validated throwing damage when available and falls back to proxy values only for unvalidated items.

---

## 5. Current authoritative general model: v7.1

### General score

```txt
total_score_v71 =
0.65 × offense_score_v7
+ 0.20 × defense_score_v71
+ 0.15 × reliability_score
```

### Survivability armor

```txt
survivability_armor_v71 =
0.55 × body
+ 0.35 × head
+ 0.05 × arm
+ 0.05 × leg
```

### General top 10 — regular combined

| Rank | Troop | Tier | Category | Total v7.1 |
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

### War Sails / NavalDLC general top 10 — v7.1

| Rank WS | Troop | Tier | Category | Total v7.1 |
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

### Interpretation

The general model says:

- Khan's Guard is the best complete battlefield package.
- Fian Champion is the best foot ranged unit.
- Vanguard Faris combines elite throwing burst with exceptional defense.
- Imperial Naute is a good T5 general troop, but not an S-tier sustained-combat troop.

---

## 6. Current authoritative burst model: v7.3

### Purpose

`burst_score_v73` answers:

```txt
Which troop can generate the strongest first-contact / short-duration kill pressure?
```

It does not answer:

```txt
Which troop is best overall in a long battle?
```

### Tooltip-first throwing damage

```txt
throw_damage_used_v73 =
tooltip_throw_damage if validated
else primary_throw_damage proxy
```

### v7.3 throwing factors

```txt
throw_damage_factor_v73 = clamp(damage / 110, 0.70, 1.10)

throw_skill_factor_v73 =
clamp(0.75 + throwing_skill / 400, 0.75, 1.20)

throw_ammo_factor_v73 =
0.70
+ 0.08 × min(ammo, 5)
+ 0.04 × min(max(ammo - 5, 0), 5)

mounted_throw_bonus_v73 =
1.12 if mounted else 1.00
```

The throwing score is normalized around a Faris-like benchmark:

```txt
Jereed
140 throwing
5 ammo
mounted
```

### v7.3 burst score composition

Each troop receives separate burst candidates for:

```txt
throwing
ranged
charge
melee
```

The best candidate becomes `burst_source_v73`, then:

```txt
burst_score_v73 =
0.70 × burst_offense_score_v73
+ 0.20 × reliability_score
+ 0.10 × defense_score_v71
```

### Burst top 10 — regular combined

| Rank | Troop | Tier | Category | Burst v7.3 | Source | General rank v7.1 |
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

### Important interpretation

```txt
Khan's Guard:
#1 general
#8 burst
```

This is not a contradiction. Khan's Guard wins through sustained ranged uptime, mobility, survival, and melee fallback.

```txt
Imperial Naute:
#42 general
#3 burst
```

This means the Naute is a specialist with elite early kill pressure but weaker long-battle survivability.

---

## 7. In-game tooltip validation

The item-validation batch is stored under:

```txt
analysis/item_validation/2026-06-05_throwing_tooltips/
```

### Confirmed values

| Troop | Item | Tooltip damage | Type | Stack | Visible stacks | Total ammo |
|---|---|---:|---|---:|---:|---:|
| Imperial Naute | Hooked Javelin | 117 | Pierce | 5 | 2 | 10 |
| Battanian Skipari | Hooked Javelin | 117 | Pierce | 5 | 2 | 10 |
| Battanian River Raider | Broad Blade Javelin | 101 | Pierce | 5 | 2 | 10 |
| Imperial Coast Guard | Harpoon | 113 | Pierce | 5 | 2 | 10 |
| Aserai Vanguard Faris | Jereed | 121 | Pierce | 5 inferred/consistent | 1 | 5 |

### Important item correction

The previous model labeled Imperial Coast Guard's throwing item as:

```txt
Broad Blade Javelin
```

The in-game tooltip shows:

```txt
Harpoon
```

The current tooltip-validation layer records that correction.

### Meaning for Skipari

Battanian Skipari's high burst rank is **not** caused by an ammo parsing bug.

The game confirms:

```txt
2 stacks × 5 Hooked Javelins = 10 total javelins
```

The remaining open question is empirical performance, not equipment data.

---

## 8. Empirical screenshot validation

Normalized battle results are stored under:

```txt
analysis/empirical/screenshots_2026-05-29_2026-06-04/
```

### Derived metrics

```txt
estimated_present = ready_alive + dead + wounded
kills_per_present = kills / estimated_present
casualty_rate = (dead + wounded) / estimated_present
```

### Key aggregate observations

| Troop | Observations | Present | Kills | Weighted kills/present | Casualty rate |
|---|---:|---:|---:|---:|---:|
| Khuzait Khan's Guard | 12 | 198 | 331 | 1.672 | 0.121 |
| Imperial Elite Menavliaton | 6 | 55 | 73 | 1.327 | 0.455 |
| Imperial Naute | 17 | 229 | 263 | 1.148 | 0.672 |
| Nord Sky-Gods Chosen | 9 | 49 | 56 | 1.143 | 0.408 |
| Imperial Sergeant Crossbowman | 12 | 183 | 196 | 1.071 | 0.240 |

### Empirical conclusions

#### Khan's Guard

Validated as S-tier because it combines:

```txt
high output
low casualties
consistency across contexts
```

#### Imperial Naute

Validated as a burst overperformer:

```txt
strong kills/present
high casualties
excellent short-contact output
less convincing sustained survival
```

This supports separate general and burst rankings.

#### Imperial Sergeant Crossbowman

Shows stable performance. This supports the conclusion that crossbows were not inherently broken in the model; the earlier issue was War Sails roster overcount.

#### Nord infantry

Strong but variable. The screenshots do not support the old false conclusion that Nord Huscarl is the best troop in the game.

### Dataset limitations

- Manual transcription from screenshots.
- Mixed battle contexts.
- Some battles include overhaul/modded enemy troops.
- Siege and chokepoint battles inflate ranged output.
- This is not controlled laboratory telemetry.

---

## 9. Current repo structure relevant to the work

```txt
analysis/
  empirical/
    screenshots_2026-05-29_2026-06-04/
      README.md
      schema.md
      screenshot_manifest.csv
      empirical_battle_results_normalized.csv
      empirical_troop_aggregate_summary.csv
      empirical_aggregate_summary.md
      empirical_findings_2026-06-04.md

  item_validation/
    2026-06-05_throwing_tooltips/
      item_tooltip_validation_20260605.csv
      findings.md
      screenshot_manifest.csv

  model_versions/
    v7.2_burst_score/
      bannerlord_v72_burst_assumptions.md
      bannerlord_v72_burst_summary.md
      bannerlord_v72_top20_burst_units_regular_combined.csv
      bannerlord_v72_key_burst_cases.csv
      empirical_v72_burst_validation_summary.csv

    v7.3_tooltip_damage_burst/
      bannerlord_v73_burst_assumptions.md
      bannerlord_v73_burst_summary.md
      bannerlord_v73_top20_burst_units_regular_compact.csv
      bannerlord_v73_key_burst_cases_compact.csv

scripts/
  build_v72_burst_score.py
  build_v73_tooltip_damage_burst.py
```

---

## 10. GitHub issues and decisions

### Issue #1 — closed

```txt
v7.2: Add burst_score context scoring only
```

Decision:

```txt
implement burst_score only
```

Explicitly excluded:

```txt
boarding_score
short_engagement_score
siege_defense_score
```

### Issue #2 — open

```txt
v7.2 follow-up: validate Battanian Skipari burst ranking
```

Item loadout is already validated. The remaining requirement is controlled empirical battle evidence.

### Issue #3 — closed

```txt
v7.3: Use tooltip-validated throwing damage as source of truth
```

Decision:

```txt
tooltip damage is authoritative when validated
proxy damage is fallback only
```

---

## 11. Current confidence assessment

### High confidence

```txt
Khan's Guard is elite overall
Fian Champion is elite overall
Vanguard Faris is elite overall and #1-class burst
Master Archer > Aserai Archer
Sharpshooter > Vlandian Nauta in general combat
Imperial Naute has 10 Hooked Javelins
Battanian Skipari has 10 Hooked Javelins
Imperial Coast Guard uses Harpoon
old Nord Huscarl #1 result was invalid
```

### Medium confidence

```txt
v7.1 exact ordering below the top group
v7.3 exact ordering of Skipari vs Naute
War Sails infantry internal ranking
shock cavalry exact placement
```

### Low confidence / still proxy-dependent

```txt
unvalidated crafted throwing weapons
unvalidated crafted melee weapons
exact AI-use factors for some War Sails troops
exact body-part hit frequencies
```

---

## 12. Reproducibility warning

The repo contains scripts and compact outputs, but the full original XML export ZIPs are not stored in GitHub.

The v7.3 builder expects a tooltip-enriched model input. If that full input CSV is not present in the repo checkout, use the archived local package from the original conversation or regenerate it from:

```txt
v7.1/v7.2 model data
+
analysis/item_validation/2026-06-05_throwing_tooltips/item_tooltip_validation_20260605.csv
```

Do not silently reconstruct missing fields with guesses. Record every fallback with a source marker such as:

```txt
exact_xml
tooltip_validated
crafted_reconstructed
model_proxy
low_confidence
```

---

## 13. Immediate next steps

### Priority 1 — controlled Skipari validation

Run comparable battles using approximately:

```txt
20–40 Battanian Skipari
20–40 Imperial Naute
20–40 Aserai Vanguard Faris
20–40 Battanian Fian Champion
```

Keep enemy composition and terrain as similar as possible.

Measure:

```txt
kills_per_present
casualty_rate
variance across battles
```

### Priority 2 — validate remaining proxy throwing items

Recommended order:

```txt
Battanian Mounted Skirmisher
Sturgian Horse Raider
Imperial Shipmate
Sturgian Reaver
Nord Huscarl throwing axe
Nord Skjaldbrestir throwing axe
```

### Priority 3 — add confidence score

Recommended fields:

```txt
item_data_confidence
empirical_sample_confidence
roster_parse_confidence
model_confidence
```

Possible inputs:

```txt
tooltip validated?
exact XML weapon?
crafted proxy?
number of empirical observations?
total empirical present count?
context diversity?
```

### Priority 4 — do not alter general score without evidence

The current split should remain:

```txt
v7.1 = general battlefield ranking
v7.3 = burst context ranking
```

Do not promote a burst specialist into the general top 10 solely because of burst score.

---

## 14. Decisions that should not be reopened casually

1. **Do not merge EquipmentRoster alternatives.** Score each roster separately and average.
2. **Do not classify foot archers by max melee output.** They are ranged-first with capped fallback.
3. **Do not treat horse archers as pure melee glaive troops.** They are ranged-first with meaningful fallback.
4. **Do not use 70/10/10/10 armor weighting as the main survivability proxy.** It is too torso-heavy.
5. **Do not treat low-ammo throwing axes as sustained javelin pressure.**
6. **Do not use crafted proxy damage when an in-game tooltip has validated the real value.**
7. **Do not merge general and burst rankings.**
8. **Do not accept a surprising top result without auditing XML, roster structure, and item source.**

---

## 15. Recommended new-chat workflow

A new ChatGPT conversation with GitHub access should begin by reading, in this order:

```txt
1. docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md
2. README.md
3. analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_summary.md
4. analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_assumptions.md
5. analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top20_burst_units_regular_compact.csv
6. analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_findings_2026-06-04.md
7. analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_troop_aggregate_summary.csv
8. analysis/item_validation/2026-06-05_throwing_tooltips/findings.md
9. analysis/item_validation/2026-06-05_throwing_tooltips/item_tooltip_validation_20260605.csv
10. GitHub issue #2
```

Then the new chat should state back:

```txt
current authoritative general model
current authoritative burst model
open validation issue
next proposed action
```

before making any model changes.

---

## 16. Ready-to-use handoff statement

```txt
This project has two authoritative outputs:

- v7.1 general score for overall battlefield value.
- v7.3 burst score for first-contact / short-duration kill pressure.

The general top 3 are Khan's Guard, Fian Champion, and Vanguard Faris.
The burst top 3 are Vanguard Faris, Battanian Skipari, and Imperial Naute.

War Sails must be parsed roster-first. Alternative EquipmentRosters are alternatives, not additive loadouts. Tooltip-validated throwing damage overrides crafted/proxy damage. The only major open issue is empirical validation of Battanian Skipari's #2 burst ranking.

Do not implement boarding_score. Do not change v7.1 general_score without new empirical evidence.
```
