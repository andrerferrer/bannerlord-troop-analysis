# Realm of Thrones Troop Analysis — Full Handoff

This is the canonical handoff for continuing the Realm of Thrones troop-analysis project in a new chat with GitHub access.

The project briefly detoured into vanilla Bannerlord tooling. That work is useful as engineering reference, but this document is strictly about **Realm of Thrones / RoT**.

## Scope

Goal: build a practical troop-analysis framework for Realm of Thrones in Bannerlord.

The model should estimate real battlefield usefulness, not just sort by XML stats.

It needs to account for:

- terminal troop quality;
- ranged output;
- melee output;
- shields and armor;
- weapon speed and damage type;
- throwing burst;
- cavalry unreliability;
- siege context;
- AI weapon usability;
- campaign-realistic access;
- empirical validation from campaign battle result screenshots.

## Stable rules

These rules should be preserved unless strong evidence says otherwise.

1. Analyze terminal troops first.
2. Giants are excluded from normal humanoid rankings.
3. Castellan filtering is manual and campaign-oriented.
4. Scores are relative indices, not literal performance multipliers.
5. Do not automatically punish glass cannons.
6. Do not let defense silently multiply every offense score.
7. Do not reward reach by itself.
8. Throwing must be treated as burst with limited capacity.
9. RoT custom/crafted weapons are often incomplete in XML exports.
10. Campaign battle results are the main empirical source because custom battle testing is not very viable.

## Important project files from the previous work

Original reset package contained:

```txt
rot_context_reset.md
rot_ranged_full_no_castellan.csv
rot_damage_speed_rebalanced_csvs.zip
rot_line_cav_test_csvs.zip
```

Important generated snapshots:

```txt
rot_normalized_2026-05-23.zip
rot_field_score_v2_test_top.csv
rot_htk_v3b_2026-05-23.zip
rot_htk_v3c_split_offense_2026-05-23.zip
```

The normalized package contained:

```txt
troops_theory_normalized.csv
role_scores_long.csv
taxonomy_v1_classified.csv
empirical_battles.csv
empirical_troop_rows.csv
validation_join.csv
unmatched_empirical_troops.csv
battle_integrity_checks.csv
metric_dictionary.csv
sources_manifest.csv
analysis_summary.json
rot_normalization_pipeline.py
empirical_troop_rows_template.csv
```

Known normalized counts from the first pass:

| Dataset | Count |
|---|---:|
| theoretical terminal non-giant troops | 301 |
| long role-score rows | 2709 |
| classified taxonomy rows | 301 |
| empirical troop rows from first screenshot | 30 |
| empirical rows matched to theory | 8 |
| empirical rows unmatched | 22 |

## Data limitations

### Custom weapon data

Many RoT items are not cleanly represented as direct weapon records. This affects:

- two-handed weapons;
- polearms;
- throwing weapons;
- custom bows;
- custom crossbows;
- fantasy/special weapons.

All weapon proxies must expose confidence/source status. Do not silently treat proxy values as exact engine stats.

### HP baseline

The HTK model used:

```txt
human target HP = 100
```

This is a practical baseline. It should remain configurable.

### Armor approximation

When exact hit-location armor was unavailable, V3 used:

```txt
effective_armor = armor_total / 3.3
```

This is approximate and should be empirically calibrated.

### Damage type inference

When damage type was missing, it was inferred from item/family names:

```txt
bow/crossbow/arrow/bolt -> pierce
mace/hammer/maul/club -> blunt
spear/pike/lance/javelin -> pierce
other melee -> cut
```

## Model evolution

### Legacy field/siege model

The best pre-HTK score was a damage/speed rebalanced model.

Field score:

```txt
field_score =
0.75 × field_offense_composite
+ 0.20 × defense_norm
+ 0.05 × level_norm
```

Siege score:

```txt
siege_score =
0.70 × siege_offense_composite
+ 0.25 × defense_norm
+ 0.05 × level_norm
```

Melee offense concept:

```txt
melee_offense =
damage
× skill_multiplier
× speed_factor
× damage_type_factor
× weapon_role_factor
```

Reach was deliberately devalued. Long reach was not treated as an automatic positive.

Direct speed factor:

```txt
speed_factor = clamp(speed_rating / 90, 0.70, 1.20)
```

Multiple offensive domains were collapsed using:

```txt
best_domain + 0.15 × second_domain + 0.05 × third_domain
```

### Reliability experiment

A later V2 tested:

```txt
score_v2 =
0.65 × offense
+ 0.20 × defense
+ 0.15 × reliability
- fragility_penalty
```

Lesson: reliability matters, but it must not simply become defense under another name.

### HTK/KPM V3

The best conceptual improvement was replacing abstract offense with expected kill conversion.

Core formulas:

```txt
HTK = target_hp / final_damage

KPM = attempts_per_minute × hit_chance / HTK
```

Target mix used:

```txt
0.25 × light
+ 0.50 × standard
+ 0.25 × heavy
```

Target profiles used in one V3 run:

| Target | HP | Armor |
|---|---:|---:|
| Light | 100 | 25.15 |
| Standard | 100 | 39.85 |
| Heavy | 100 | 50.91 |

Damage approximation preserved:

```txt
Blunt > Pierce > Cut
```

One approximation used:

```txt
damage_curve = raw_damage × 100 / (100 + armor)

final_damage =
damage_curve × blunt_damage_factor
+ max(0, damage_curve - armor × pierce_resistance)
  × (1 - blunt_damage_factor)
```

Parameters:

| Type | Blunt factor | Pierce resistance |
|---|---:|---:|
| Cut | 0.10 | 0.50 |
| Pierce | 0.25 | 0.33 |
| Blunt | 1.00 | 0.00 |

This is not guaranteed to be exact current Bannerlord engine code. It is a calibratable proxy.

### HTK/KPM V3c — current best theoretical snapshot

V3c split offense by tactical mode:

```txt
melee_only = melee_kpm

ranged_blend =
0.80 × ranged_kpm
+ 0.20 × melee_kpm

throw_blend =
0.35 × throw_kpm
+ 0.65 × melee_kpm

offense_raw = max(melee_only, ranged_blend, throw_blend)
```

Current total concept:

```txt
total_v3c = normalized(
  0.65 × offense_v3c_norm
  + 0.20 × defense_norm
  + 0.15 × reliability_v3
)
```

V3c is the current best theoretical baseline. It is not final truth.

## Current manual Castellan list

Working list based on prior filtering and user corrections:

```txt
Ravens' Teeth
Mormont Bowmaiden
Stark Sworn Sword
Celtigar Banneret
Harlaw Captain
Tarth Master Halberdier
Tarly Vanguard
Baratheon Hammerknight
Umber Berzerker
Cerwyn Marauder
Mountain's Man
Guardian of the Rock
Captain of the Kingsguard
Arryn Winged Knight
Frey Assassin
Greyjoy Sniper
Sarnori Spider
Norvoshi Grand Bearded Priest
Riverlands Admiral
Magister Guard Elite
Triarch Guardian
Realm Paladin
```

Keep this as explicit config, not hidden logic.

## V3c top overall snapshot

| # | Troop | Castellan | Total | Offense | Defense | Mode |
|---:|---|:---:|---:|---:|---:|---|
| 1 | Ravens' Teeth | TRUE | 100.00 | 100.00 | 73.24 | ranged+fallback |
| 2 | Goldenheart Warrior | FALSE | 95.17 | 96.25 | 64.70 | ranged+fallback |
| 3 | Stark Sworn Sword | TRUE | 91.47 | 80.66 | 95.47 | melee |
| 4 | Lyseni Enforcer | FALSE | 88.97 | 85.18 | 76.29 | melee |
| 5 | Baratheon Hammerknight | TRUE | 87.01 | 79.08 | 84.41 | melee |
| 6 | Myrish Artisan of War | FALSE | 85.03 | 72.89 | 92.94 | melee |
| 7 | Tarly Vanguard | TRUE | 84.94 | 73.87 | 88.20 | melee |
| 8 | Riverlands Admiral | TRUE | 80.91 | 71.28 | 79.14 | melee |
| 9 | Stormlands Thunder Knight | FALSE | 79.86 | 75.69 | 66.18 | melee |
| 10 | Norvoshi Grand Bearded Priest | TRUE | 79.71 | 68.10 | 83.35 | melee |
| 11 | Mountain's Man | TRUE | 79.31 | 74.58 | 67.12 | melee |
| 12 | Harlaw Captain | TRUE | 79.04 | 66.00 | 89.25 | melee |
| 13 | Celtigar Banneret | TRUE | 78.40 | 64.73 | 90.25 | melee |
| 14 | Tarth Master Halberdier | TRUE | 77.68 | 67.63 | 79.03 | melee |
| 15 | Umber Berzerker | TRUE | 75.70 | 69.52 | 66.81 | melee |
| 16 | Greyjoy Sniper | TRUE | 75.50 | 67.71 | 68.07 | ranged+fallback |
| 17 | Qohorik Falxman | FALSE | 75.23 | 68.71 | 67.23 | melee |
| 18 | Cerwyn Marauder | TRUE | 74.69 | 69.52 | 62.70 | melee |
| 19 | Mormont Bowmaiden | TRUE | 72.06 | 60.36 | 75.76 | ranged+fallback |
| 20 | Ghiscari Queen's Guard | FALSE | 72.04 | 64.85 | 61.28 | melee |

## Key control cases

| Troop | Expected interpretation |
|---|---|
| Ravens' Teeth | theoretical #1, ranged carry plus strong fallback |
| Goldenheart Warrior | non-Castellan top carry, already empirically supported |
| Lyseni Enforcer | elite melee HTK case, empirically supported |
| Myrish Artisan of War | high defense hybrid, mode may change by siege context |
| Celtigar Banneret | possible empirical overperformer via defense/uptime |
| Golden Company Mahout | possible model false positive or context failure |

## First empirical battle

Battle ID:

```txt
rot_empirical_001_2026-05-23_151452
```

Integrity check passed:

```txt
defender kills = attacker deaths + attacker wounded
669 = 111 + 558

attacker kills = defender deaths + defender wounded
120 = 21 + 99
```

Main matched rows:

| Troop | Kills | Estimated present | Kills/present | Interpretation |
|---|---:|---:|---:|---|
| Goldenheart Warrior | 338 | 82 | 4.1220 | supports high rank |
| Lyseni Enforcer | 108 | 26 | 4.1538 | supports high rank |
| Baratheon Hammerknight | 66 | 18 | 3.6667 | supports high rank |
| Golden Company Mahout | 10 | 35 | 0.2857 | possible false positive/context issue |
| Lyseni Elite Archer | 8 | 7 | 1.1429 | low-control result |
| Lyseni Militia Veteran Archer | 4 | 6 | 0.6667 | low-control result |

Final yellow tool/hammer column was not identified and was stored as:

```txt
unknown_yellow_tool
```

## Main conceptual findings

### Glass cannons can be excellent

Do not apply blanket fragility penalties. Ravens and Goldenheart show that high kill speed can preserve practical uptime.

### Defense matters, but should not dominate by default

Avoid:

```txt
effective_output = offense × defense
```

Use separate offense, defense, and reliability unless empirical results justify an interaction.

### Celtigar is a real concern

User testing suggested Celtigar can kill more than Ravens in some real battles. This likely reflects sustained contact, shield/armor, formation stability, and battle duration. It should become an empirical overperformer candidate, not an automatic formula rewrite.

### Role capability is multi-label

A troop can rank in multiple capability lists. Do not remove a strong ranged unit from a melee-capability list if it genuinely has strong melee fallback.

## Empirical plan going forward

Custom battle is not viable enough for this workflow. Use campaign battles.

For each battle screenshot, collect:

```txt
battle_id
context
side
troop_name
healthy
dead
wounded
kills
```

Optional context tags:

```txt
field
siege_attack
siege_defense
rough_terrain
chokepoint
large_army
small_party
player_commanded
auto_charge
```

Derived metrics:

```txt
estimated_present = healthy + dead + wounded
kills_per_present = kills / estimated_present
casualty_rate = (dead + wounded) / estimated_present
death_rate = dead / estimated_present
deployed_share = estimated_present / side_total_present
kill_share = kills / side_total_kills
contribution_index = kill_share / deployed_share
```

Campaign contribution candidate:

```txt
campaign_contribution = contribution_index × (1 - death_rate - 0.35 × wounded_rate)
```

Do not merge this into theory automatically. Store separately first.

Priority empirical units:

```txt
Ravens' Teeth
Goldenheart Warrior
Celtigar Banneret
Lyseni Enforcer
Myrish Artisan of War
Golden Company Mahout
Sarnori Spider
Baratheon Hammerknight
```

## Workflow for a new RoT version

A new RoT/HOT version with more troops should be handled as follows:

1. Export vanilla core XMLs plus the RoT/HOT module XMLs.
2. Preserve source module and source file for every record.
3. Rebuild troop/equipment/item tables.
4. Detect terminal troops from upgrade edges, not level.
5. Reapply giant and Castellan filters.
6. Produce audit tables before scores.
7. Only then run theory scoring.
8. Compare new troops to existing control cases.
9. Do not overwrite old results; save by date/version.

## Bootstrap prompt for a new chat

Use this in a new chat with GitHub access:

```txt
We are continuing Realm of Thrones troop analysis.

Start by reading:
- docs/rot_reference/ROT_ANALYSIS_FULL_HANDOFF.md

Do not mix in vanilla Bannerlord analysis except as engineering reference.

Current theoretical baseline: HTK/KPM v3c split offense.
Current practical goal: update the RoT dataset for a new RoT/HOT version with more troops, then validate using campaign battle screenshots.

Preserve these principles:
- terminal troops first;
- giants excluded from normal rankings;
- Castellan filtering manual;
- glass cannons are not automatically penalized;
- defense does not silently multiply all offense;
- role capability may be multi-label;
- empirical contribution remains separate from theoretical score until calibrated.

Next task: run the RoT/HOT XML export, rebuild audit tables for the new version, identify new terminal troops, and produce a delta report versus the previous 301-troop baseline.
```
