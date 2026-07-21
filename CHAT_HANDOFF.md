# Bannerlord Troop Analysis — Complete Chat Handoff

> **Repository:** `andrerferrer/bannerlord-troop-analysis`  
> **Primary branch:** `main`  
> **Game scope:** Mount & Blade II: Bannerlord 1.4.x + official War Sails / `NavalDLC`  
> **Current stable general model:** **v7.1**  
> **Current context-specific burst model:** **v7.3**  
> **Purpose of this file:** allow a new ChatGPT conversation with GitHub access to resume the project without relying on previous chat context.

---

# 0. Read This First

The project builds a transparent, data-driven Bannerlord troop-analysis pipeline from the game XMLs and empirical battle screenshots.

The key architectural decision is that there is **not one universal ranking** anymore:

```txt
v7.1 general_score = overall troop quality / long-form campaign usefulness
v7.3 burst_score   = first-contact / short-engagement kill pressure
```

Do not merge these scores casually. A troop can be mediocre overall and elite at burst. The canonical example is **Imperial Naute**:

```txt
v7.1 general regular rank: #42
v7.3 burst regular rank:   #3
```

This is intentional and is supported by empirical screenshots.

The next assistant should begin by reading:

```txt
CHAT_HANDOFF.md
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_summary.md
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_assumptions.md
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_findings_2026-06-04.md
analysis/item_validation/2026-06-05_throwing_tooltips/findings.md
scripts/build_v73_tooltip_damage_burst.py
```

---

# 1. Objective Final

Build a reproducible troop-analysis system for official Bannerlord content, including vanilla and War Sails, that answers:

```txt
Best troop overall
Best troop by tier
Best offensive infantry
Best defensive infantry
Best cavalry
Best archer / crossbowman / horse archer
Best non-noble troop
Best early-game upgrade paths
Best burst troop
Most overrated / underrated troop
```

The ranking must be explainable through:

```txt
XML equipment
skills
armor
shield / horse
HTK / KPM proxies
offense score
defense score
reliability score
context-specific burst score
empirical battle results
confidence / data-source quality
```

The project is not intended to produce a generic community tier list. It is a transparent model that can be audited and recalibrated.

---

# 2. Technical Context

## 2.1 Game modules analyzed

Vanilla export initially included:

```txt
Native
SandBox
SandBoxCore
StoryMode
CustomBattle
```

A later complete installed-module export confirmed the War Sails official module as:

```txt
NavalDLC
```

The official combined scope is therefore:

```txt
Native
SandBox
SandBoxCore
StoryMode
CustomBattle
NavalDLC
```

Third-party mods present in the export were intentionally excluded from the main official ranking.

## 2.2 Data sources

The pipeline has used:

```txt
Bannerlord XML / XSLT exports
NPC character definitions
item definitions
weapon definitions
armor definitions
horse/harness definitions
shield definitions
crafting templates and pieces
equipment rosters
upgrade trees
in-game item tooltips
battle-result screenshots
combat-log screenshots
```

## 2.3 Important Bannerlord data constraint

Many War Sails weapons are represented as:

```xml
<CraftedItem>
```

rather than normal items with every final stat directly exposed. Early model versions reconstructed these weapons with low-confidence proxies. In-game tooltips are now treated as the source of truth when available.

## 2.4 Primary tools and code

The repository contains builder scripts for the newer model layers:

```txt
scripts/build_v72_burst_score.py
scripts/build_v73_tooltip_damage_burst.py
```

Empirical and item-validation artifacts are committed under:

```txt
analysis/empirical/
analysis/item_validation/
analysis/model_versions/
```

## 2.5 Main constraints

- Equipment rosters are **alternative loadouts**, not cumulative equipment.
- Crafted weapon stats may be proxy/low-confidence until tooltip-validated.
- Screenshots are manually transcribed and are not raw telemetry.
- General, burst, siege, and other context rankings should not be collapsed into one number without evidence.
- The model should not force known community outcomes, but sanity checks are allowed.

---

# 3. Data Export Workflow

Two PowerShell scripts were created during the work:

```txt
export_vanilla_relevant_xmls.ps1
export_vanilla_xmls.ps1
```

The original full-export script was hardcoded to vanilla modules only. That caused an early misunderstanding because War Sails was not included. The later installed-module export contained `NavalDLC` and was used for the official combined model.

Recommended future export behavior:

```powershell
Get-ChildItem -Path $BannerlordModulesPath -Directory
```

and export all modules with `ModuleData`, then filter official modules during analysis.

Do not assume a file named “vanilla export” includes War Sails.

---

# 4. Normalized Model Structure

The model has normalized troop fields similar to:

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
survivability_armor
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
primary_melee_name
primary_melee_damage
primary_melee_damage_type
primary_melee_speed
primary_melee_reach
primary_ranged_name
ranged_damage
ranged_ammo
ranged_kpm
primary_throw_name
primary_throw_damage
primary_throw_ammo
throw_pressure
```

Data confidence fields should be expanded in the future:

```txt
exact_xml
crafted_reconstructed
tooltip_validated
proxy_low_confidence
```

---

# 5. Simplified Troop Categories

The current taxonomy is deliberately small:

```txt
Offensive Infantry
Defensive Infantry
Offensive Cavalry
Defensive Cavalry
Archer
Crossbowman
Horse Archer
```

Do not create unnecessary micro-categories unless needed for a specific context score.

---

# 6. Model Evolution and Major Corrections

## v3 — Initial HTK/KPM model

Initial structure:

```txt
enemy_hp = 100
base_after_armor = raw_damage × 100 / (100 + armor)
Blunt modifier = 1.10
Pierce modifier = 1.00
Cut modifier = 0.85
HTK = enemy_hp / effective_damage
```

General score:

```txt
total_score =
0.65 × offense_score
+ 0.20 × defense_score
+ 0.15 × reliability_score
```

Problem: throwing troops were severely undervalued. Vanguard Faris appeared around rank #46.

## v4 — Throwing calibration

Throwing was changed from a minor melee supplement to a real burst/pressure source.

Important result:

```txt
Vanilla top 3 became:
1. Khan's Guard
2. Fian Champion
3. Vanguard Faris
```

This aligned better with observed play.

## v5 — Ranged role fix

The old offense model used:

```txt
offense = max(melee, ranged, throw)
```

This caused archers to be ranked by melee fallback. Example:

```txt
Aserai Archer > Aserai Master Archer
```

because the lower-tier Archer had a blunt mace.

The fix made foot archers and crossbowmen ranged-first.

Validated order:

```txt
Aserai Master Archer > Aserai Archer > Aserai Light Archer
```

## v5.1 — Ranged-first horse archers

Horse archers were also made ranged-first, with melee only as capped fallback.

Khan’s Guard remained elite. Kheshig/Torguud dropped because their old score relied heavily on melee/glaive behavior.

This exposed another issue: shock cavalry remained undervalued.

## v6 — War Sails XML-first correction

Early War Sails rankings were invalid. The worst result was:

```txt
Nord Huscarl #1 overall
```

This came from:

```txt
spear + shield treated as sustained elite KPM
low-ammo throwing axes treated as sustained pressure
crafted weapon proxies treated as exact
```

v6 added:

```txt
spear + shield sustained KPM penalty
low-ammo throwing burst limits
crafted/proxy confidence warnings
```

## v7 — Roster-first correction

This was a critical parser correction.

Wrong behavior:

```txt
EquipmentRoster 1 + EquipmentRoster 2 + EquipmentRoster 3
= one false super-loadout
```

Correct behavior:

```txt
score(roster 1)
score(roster 2)
score(roster 3)
troop score = average of alternative roster scores
```

Concrete bug fixed:

```txt
Vlandian Nauta bolts:
wrong = 18 + 18 + 18 = 54
correct = 18 per spawned roster
```

After correction:

```txt
Vlandian Sharpshooter > Vlandian Nauta
```

because their basic ranged output was similar, while Sharpshooter defense was much stronger.

## v7.1 — Head-weighted survivability armor

The original armor aggregate was:

```txt
0.70 body + 0.10 head + 0.10 arm + 0.10 leg
```

Deep research found:

- Bannerlord tracks hit body part separately.
- Headshots are explicitly handled and have higher damage multipliers.
- Leg damage was officially reduced in patch notes.
- No credible public dataset gives exact AI hit-location frequencies.

The selected lethality-weighted survivability proxy became:

```txt
survivability_armor_v71 =
0.55 × body_armor
+ 0.35 × head_armor
+ 0.05 × arm_armor
+ 0.05 × leg_armor
```

This is not claimed as the engine’s real hit-location formula. It is a survivability proxy.

The model field should conceptually be called:

```txt
survivability_armor
```

rather than generic `effective_armor`.

## v7.2 — Burst context score

Empirical screenshots showed throwing troops, especially Imperial Naute, killing far more than their general rank suggested in short fights.

Decision:

```txt
Keep v7.1 general_score unchanged.
Add burst_score_v72 as a separate context score.
```

Boarding, siege-defense, and short-engagement scores were explicitly removed from scope.

## v7.2.1 — Tooltip validation layer

In-game tooltips confirmed ammo/loadouts and exposed proxy inaccuracies.

Validated:

```txt
Imperial Naute: 2 × Hooked Javelin stacks, 5 each = 10 ammo
Battanian Skipari: 2 × Hooked Javelin stacks, 5 each = 10 ammo
Battanian River Raider: 2 × Broad Blade Javelin stacks, 5 each = 10 ammo
Imperial Coast Guard: 2 × Harpoon stacks, 5 each = 10 ammo
Vanguard Faris: Jereed line consistent with 5 ammo
```

Important item correction:

```txt
Imperial Coast Guard primary throw:
wrong model name = Broad Blade Javelin
correct tooltip item = Harpoon
```

## v7.3 — Tooltip damage becomes source of truth

The validated tooltip values are treated as real raw item stats:

```txt
Hooked Javelin = 117 Pierce
Broad Blade Javelin = 101 Pierce
Harpoon = 113 Pierce
Jereed = 121 Pierce
```

The old crafted/proxy values were much lower:

```txt
Hooked Javelin proxy = 45.2
Broad Blade Javelin proxy = 48.0
Jereed proxy = 54.4
```

v7.3 does not simply multiply the old score by tooltip/proxy ratio because that would saturate all javelins at the ceiling. It recalibrates throwing using separate source-specific factors.

---

# 7. Current Stable General Model — v7.1

## 7.1 General score

```txt
general_score_v71 =
0.65 × offense_score_v7
+ 0.20 × defense_score_v71
+ 0.15 × reliability_score
```

## 7.2 Survivability armor

```txt
survivability_armor_v71 =
0.55 × body
+ 0.35 × head
+ 0.05 × arm
+ 0.05 × leg
```

## 7.3 Top 10 regular combined — v7.1

```txt
1. Khuzait Khan's Guard
2. Battanian Fian Champion
3. Aserai Vanguard Faris
4. Battanian Fian
5. Imperial Elite Menavliaton
6. Sturgian Heroic Line Breaker
7. Vlandian Voulgier
8. Imperial Menavliaton
9. Battanian Veteran Falxman
10. Imperial Legionary
```

These are the current general-ranking baseline results.

Do not replace this list with burst results.

---

# 8. Current Burst Model — v7.3

## 8.1 Purpose

`burst_score_v73` answers:

```txt
Which troop can produce the strongest first-contact / short-fight kill pressure?
```

It does not answer overall campaign quality.

## 8.2 Tooltip-first throwing inputs

```txt
throw_damage_used_v73 =
tooltip_throw_damage if available
else model/proxy throwing damage
```

## 8.3 Throwing factors

```txt
throw_damage_factor_v73 = clamp(throw_damage_used_v73 / 110, 0.70, 1.10)

throw_skill_factor_v73 = clamp(
  0.75 + throwing_skill / 400,
  0.75,
  1.20
)

throw_ammo_factor_v73 =
0.70
+ 0.08 × min(ammo, 5)
+ 0.04 × min(max(ammo - 5, 0), 5)

mounted_throw_bonus_v73 =
1.12 if mounted else 1.00
```

Throw damage-type factor:

```txt
Pierce = 1.00
Blunt  = 0.96
Cut    = 0.88
```

The throwing score is normalized against a Faris-like benchmark:

```txt
Jereed
140 throwing
5 ammo
mounted
```

## 8.4 Other burst candidates

The model still calculates:

```txt
ranged burst
charge burst
melee burst
```

Then:

```txt
burst_offense_score_v73 = max(
  throw_burst_offense,
  ranged_burst_offense,
  charge_burst_offense,
  melee_burst_offense
)
```

Final context score:

```txt
burst_score_v73 =
0.70 × burst_offense_score_v73
+ 0.20 × reliability_score
+ 0.10 × defense_score_v71
```

## 8.5 Top 10 regular burst — v7.3

```txt
1. Aserai Vanguard Faris — 96.026
2. Battanian Skipari — 92.910
3. Imperial Naute — 92.828
4. Battanian Fian Champion — 90.161
5. Aserai Veteran Faris — 85.218
6. Imperial Coast Guard — 84.188
7. Battanian Fian — 78.467
8. Khuzait Khan's Guard — 78.030
9. Battanian River Raider — 77.213
10. Battanian Mounted Skirmisher — 71.127
```

Interpretation:

```txt
Faris = strongest burst benchmark
Skipari = tooltip-supported high burst, empirical validation still needed
Naute = empirically supported burst specialist
Fian/Khan = still elite overall, but burst score is not their only strength
```

---

# 9. Current Armor Findings

## 9.1 Why head armor is heavily weighted

Research established that:

```txt
headshots have explicit extra lethality
legs have lower damage multiplier
body part is tracked by the engine
```

But exact hit-location frequency is not publicly established.

Therefore:

```txt
55 body / 35 head / 5 arm / 5 leg
```

is a lethality-weighted survivability proxy, not a measured hit-frequency distribution.

## 9.2 Example effect

The older torso-heavy model incorrectly pushed Battanian Wildling very high because of excellent body armor but weak helmet protection.

The head-weighted model appropriately improves units with strong helmets and balanced armor, such as:

```txt
Nord Huscarl
Imperial Elite Cataphract
Aserai Vanguard Faris
Aserai Veteran Infantry
Sturgian Druzhinnik Champion
Battanian Fian Champion
Khuzait Darkhan
```

---

# 10. Empirical Screenshot Validation

## 10.1 Repository location

```txt
analysis/empirical/screenshots_2026-05-29_2026-06-04/
```

Files:

```txt
README.md
schema.md
screenshot_manifest.csv
empirical_battle_results_normalized.csv
empirical_troop_aggregate_summary.csv
empirical_aggregate_summary.md
empirical_findings_2026-06-04.md
```

## 10.2 Normalization formulas

```txt
estimated_present = ready_alive + dead + wounded
kills_per_present = kills / estimated_present
casualty_rate = (dead + wounded) / estimated_present
```

The rows were manually transcribed from battle-result screenshots.

## 10.3 Main empirical findings

### Imperial Naute

Aggregate sample showed repeated strong killing output, including several short battles with:

```txt
kills_per_present around 1.5–3.0
```

Overall manually normalized aggregate included approximately:

```txt
17 observations
229 estimated present
263 kills
weighted kills/present ≈ 1.15
```

Interpretation:

```txt
Not S-tier general.
Elite burst specialist.
```

This is the core justification for separating v7.1 and v7.3.

### Khan’s Guard

Empirical evidence supports:

```txt
high output
low casualties
strong consistency
```

Its v7.1 #1 general rank remains defensible.

### Imperial Sergeant Crossbowman

The screenshots support stable crossbow performance and confirm that the previous crossbow problem was War Sails roster aggregation, not crossbows generally.

### Nord infantry

Nord Ulfhedinn, Berserkir, Sky-Gods Chosen, Huscarl, and Skjaldbrestir appear strong but variable. Empirical data does not support the old false “Nord Huscarl #1 overall” result.

### Siege/chokepoint caution

Siege screenshots heavily inflate ranged output. Do not use those results to directly recalibrate field-combat general score.

---

# 11. Item Tooltip Validation

## 11.1 Repository location

```txt
analysis/item_validation/2026-06-05_throwing_tooltips/
```

Files:

```txt
item_tooltip_validation_20260605.csv
findings.md
screenshot_manifest.csv
```

## 11.2 Validated items

```txt
Imperial Naute — Hooked Javelin — 117 Pierce — 2 stacks × 5
Battanian Skipari — Hooked Javelin — 117 Pierce — 2 stacks × 5
Battanian River Raider — Broad Blade Javelin — 101 Pierce — 2 stacks × 5
Imperial Coast Guard — Harpoon — 113 Pierce — 2 stacks × 5
Aserai Vanguard Faris — Jereed — 121 Pierce — 5 ammo assumption consistent
Aserai Veteran Faris — Jereed — 121 Pierce
```

## 11.3 Important open tooltip targets

Several burst-relevant troops still rely on `model_proxy` throwing data:

```txt
Battanian Mounted Skirmisher
Sturgian Horse Raider
Imperial Shipmate
Sturgian Reaver
Nord Huscarl
Nord Skjaldbrestir
```

Collect tooltip screenshots for these before treating their v7.3 throwing inputs as high-confidence.

---

# 12. Repository Artifacts

## 12.1 Empirical validation

```txt
analysis/empirical/screenshots_2026-05-29_2026-06-04/README.md
analysis/empirical/screenshots_2026-05-29_2026-06-04/schema.md
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_battle_results_normalized.csv
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_troop_aggregate_summary.csv
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_aggregate_summary.md
analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_findings_2026-06-04.md
analysis/empirical/screenshots_2026-05-29_2026-06-04/screenshot_manifest.csv
```

## 12.2 v7.2 burst

```txt
analysis/model_versions/v7.2_burst_score/bannerlord_v72_burst_assumptions.md
analysis/model_versions/v7.2_burst_score/bannerlord_v72_burst_summary.md
analysis/model_versions/v7.2_burst_score/bannerlord_v72_top20_burst_units_regular_combined.csv
analysis/model_versions/v7.2_burst_score/bannerlord_v72_key_burst_cases.csv
analysis/model_versions/v7.2_burst_score/empirical_v72_burst_validation_summary.csv
scripts/build_v72_burst_score.py
```

## 12.3 Tooltip validation

```txt
analysis/item_validation/2026-06-05_throwing_tooltips/item_tooltip_validation_20260605.csv
analysis/item_validation/2026-06-05_throwing_tooltips/findings.md
analysis/item_validation/2026-06-05_throwing_tooltips/screenshot_manifest.csv
```

## 12.4 v7.3 tooltip-first burst

```txt
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_assumptions.md
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_summary.md
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top20_burst_units_regular_compact.csv
analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_key_burst_cases_compact.csv
scripts/build_v73_tooltip_damage_burst.py
```

---

# 13. GitHub Issues

## Closed

```txt
#1 v7.2: Add burst_score context scoring only
#3 v7.3: Use tooltip-validated throwing damage as source of truth
```

## Open

```txt
#2 v7.2 follow-up: validate Battanian Skipari burst ranking
```

Issue #2 remains the main empirical blocker.

The Skipari loadout is confirmed:

```txt
Hooked Javelin
2 stacks × 5 = 10 ammo
117 Pierce tooltip damage
```

What is not confirmed is whether its AI/battle performance matches Imperial Naute and Vanguard Faris.

---

# 14. Known Problems and Blockers

## 14.1 Reproducibility gap

The repository has the v7.3 builder, summaries, and compact outputs, but the complete upstream v7.2.1 model input may not be fully committed in a reproducible path.

The script example expects something similar to:

```txt
analysis/model_versions/v7.2.1_tooltip_throw_validation/
bannerlord_v721_tooltip_throw_model_all_official_troops.csv
```

A future task should either:

```txt
A. commit the required v7.2.1 input CSV
```

or preferably:

```txt
B. implement a builder that reconstructs v7.2.1 from v7.2 output + item validation CSV
```

Option B is cleaner.

## 14.2 Skipari empirical validation

The model ranks Skipari #2 in burst. The item inputs are confirmed, but battle performance is not.

Recommended controlled comparison:

```txt
20–40 Battanian Skipari
20–40 Imperial Naute
20–40 Aserai Vanguard Faris
20–40 Battanian Fian Champion
same enemy composition
similar terrain
multiple repetitions
```

## 14.3 Tooltip coverage incomplete

Several throwing troops remain proxy-based.

## 14.4 Crafted weapon confidence

War Sails still contains many crafted weapons. A troop-level confidence score should distinguish:

```txt
exact XML
tooltip validated
crafted reconstructed
proxy only
```

## 14.5 No raw hit-location telemetry

The 55/35/5/5 armor weights are evidence-based but not empirically fitted from logged combat events.

A future telemetry mod could record:

```txt
VictimHitBodyPart
DamageType
MovementSpeedDamageModifier
AbsorbedByArmor
InflictedDamage
weapon class
attacker troop
victim troop
shield state
melee/ranged
```

## 14.6 General and burst scores are separate

Do not average them unless a clear use case and calibration method are defined.

---

# 15. Recommended Next Steps

Execute in this order.

## Step 1 — Make v7.3 fully reproducible

Implement:

```txt
scripts/build_v721_tooltip_validation.py
```

or equivalent, which takes:

```txt
v7.2 model output
+ analysis/item_validation/2026-06-05_throwing_tooltips/item_tooltip_validation_20260605.csv
```

and emits the exact v7.2.1 input needed by:

```txt
scripts/build_v73_tooltip_damage_burst.py
```

Add a one-command build path, ideally:

```bash
python scripts/build_v721_tooltip_validation.py ...
python scripts/build_v73_tooltip_damage_burst.py ...
```

or a wrapper:

```bash
python scripts/build_current_models.py
```

## Step 2 — Validate Battanian Skipari empirically

Collect multiple battle-result screenshots with enough Skipari units to avoid tiny-sample noise.

Update:

```txt
analysis/empirical/
issue #2
```

## Step 3 — Collect missing throwing tooltips

Priority:

```txt
Battanian Mounted Skirmisher
Sturgian Horse Raider
Imperial Shipmate
Sturgian Reaver
Nord Huscarl
Nord Skjaldbrestir
```

## Step 4 — Add confidence score

Suggested fields:

```txt
item_data_confidence
roster_confidence
empirical_sample_size
empirical_confidence
model_confidence
```

Possible categories:

```txt
HIGH
MEDIUM
LOW
```

Do not let confidence directly inflate performance score; expose it alongside the score.

## Step 5 — Consider v7.3.1 only after evidence

Possible changes:

```txt
AI/reliability correction for foot javelins
throwing ammo scaling adjustment
new tooltip inputs
```

Do not create v8 general score until the evidence requires it.

---

# 16. Mistakes That Must Not Be Repeated

1. **Do not invent troop names or upgrade lines.**  
   Early chat responses invented War Sails “Imperial Marine” names. Always inspect XML/repo/tooltips first.

2. **Do not assume War Sails was included in vanilla exports.**  
   Confirm `NavalDLC` exists in the dataset.

3. **Do not combine alternative equipment rosters.**  
   Score each roster and average.

4. **Do not treat crafted proxy stats as exact.**  
   Track the stat source.

5. **Do not use melee fallback as the main offense for archers.**

6. **Do not treat low-ammo throwing axes as sustained ranged pressure.**

7. **Do not treat spear + shield infantry as shock-infantry KPM.**

8. **Do not make one ranking answer every context.**  
   General and burst are separate.

9. **Do not change the model just to force a preferred ranking.**  
   Use observed inconsistencies to locate input/formula bugs.

10. **Do not accept a surprising top rank without auditing its source fields.**

---

# 17. Current Conclusions

## General ranking conclusions

```txt
Khan's Guard, Fian Champion, and Vanguard Faris form the validated vanilla top tier.
```

## Burst ranking conclusions

```txt
Vanguard Faris is the top burst benchmark.
Imperial Naute is an elite burst specialist.
Battanian Skipari has validated elite item inputs but still needs empirical validation.
```

## Crossbow conclusion

```txt
Vlandian Sharpshooter > Vlandian Nauta overall.
```

The old opposite result was caused by alternative-roster ammo overcount.

## War Sails conclusion

War Sails troops are strong but early rankings were heavily distorted by:

```txt
crafted proxies
roster aggregation
spear KPM inflation
low-ammo throwing inflation
```

The v7+ data is substantially more credible.

## Armor conclusion

```txt
55% body / 35% head / 5% arm / 5% leg
```

is the current survivability proxy. Head armor deserves far more than 10%, but the exact coefficient is not empirically proven.

---

# 18. Prompt for the Next Chat

Copy this into a new ChatGPT conversation that has GitHub access:

```txt
We are continuing the Bannerlord troop-analysis project in the GitHub repository:

andrerferrer/bannerlord-troop-analysis

Start by reading these files from main:

1. CHAT_HANDOFF.md
2. analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_summary.md
3. analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_assumptions.md
4. analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_findings_2026-06-04.md
5. analysis/item_validation/2026-06-05_throwing_tooltips/findings.md
6. scripts/build_v73_tooltip_damage_burst.py

Important current state:

- v7.1 is the stable general ranking.
- v7.3 is a separate tooltip-first burst ranking.
- Do not merge general_score and burst_score.
- Issue #2 is open to validate Battanian Skipari empirically.
- The highest-priority engineering task is to make the v7.3 pipeline fully reproducible by rebuilding the missing v7.2.1 tooltip-validation input from committed sources.

Execute the next engineering step directly:

Create a reproducible v7.2.1 builder that joins the v7.2 model output with the committed tooltip-validation CSV and produces the exact input expected by scripts/build_v73_tooltip_damage_burst.py. Add tests or sanity checks for Imperial Naute, Battanian Skipari, Imperial Coast Guard, Battanian River Raider, and Aserai Vanguard Faris. Commit the implementation and update CHAT_HANDOFF.md if the repository state changes.
```

---

# 19. Compact Machine-Readable State

```json
{
  "repository": "andrerferrer/bannerlord-troop-analysis",
  "branch": "main",
  "game_version_context": "Bannerlord 1.4.x + War Sails/NavalDLC",
  "stable_general_model": "v7.1",
  "stable_burst_model": "v7.3",
  "general_armor_formula": {
    "body": 0.55,
    "head": 0.35,
    "arm": 0.05,
    "leg": 0.05
  },
  "general_top3": [
    "Khuzait Khan's Guard",
    "Battanian Fian Champion",
    "Aserai Vanguard Faris"
  ],
  "burst_top4": [
    "Aserai Vanguard Faris",
    "Battanian Skipari",
    "Imperial Naute",
    "Battanian Fian Champion"
  ],
  "open_issue": 2,
  "primary_blocker": "Empirical validation of Battanian Skipari burst performance",
  "primary_engineering_gap": "Reproducible v7.2.1 tooltip-validation builder/input",
  "do_not_merge_scores": [
    "general_score_v71",
    "burst_score_v73"
  ]
}
```
