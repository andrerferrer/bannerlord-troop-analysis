# RoT/HOT V4.3 — Damage, Weapon Speed, Marginal Skill, and Castellan Package Analysis

Date: 2026-07-17

## Purpose

V4.3 integrates the user's requested combat concept:

```txt
applied output =
effective weapon damage
× weapon speed
× marginal skill modifier
× AI/application factor
```

Weapon damage remains the main input. Skill is no longer the base of offense and is deliberately capped as a marginal modifier.

V4.3 also fixes an empirical-data problem discovered after V4.2: contribution index had been calculated for partially transcribed battles where full side totals were unavailable. Those partial contribution indices are no longer used.

## V4.3 skill treatment

```txt
skill_speed_modifier =
clamp(0.95 + skill / 2500, 0.95, 1.08)

skill_accuracy_modifier =
clamp(0.95 + skill / 3000, 0.95, 1.05)
```

The combined skill effect is generally around:

```txt
0.90–1.13
```

Therefore, high skill helps enough to distinguish elite users of similar weapons, but it cannot rescue a weak weapon or dominate the damage model.

## Damage and speed

### Melee

```txt
melee KPM =
attacks_per_minute
× marginal hit/application
÷ HTK
× AI weapon application
```

Weapon speed is exact where available. Existing V3c melee speed proxies are retained for old troops; new crafted weapons use conservative family/length/weight speed priors.

### Ranged

```txt
ranged output includes:
- effective damage after armor
- shots per minute
- marginal skill
- hit probability
- ammo capacity
- representative 3-minute battle output
- range/application safety
- melee fallback
```

This preserves the correction:

```txt
Ravens' Teeth > Myrish Artisan of War
Goldenheart Warrior > Myrish Artisan of War
```

in general ranged carry value.

### Throwing

Throwing only activates a skirmisher blend if:

```txt
standard-target effective throw damage >= 25
```

Weak throwing sidearms do not convert melee troops into skirmishers.

## Existing-model integration

For troops with an old V3c baseline:

```txt
V4.3 offense =
0.60 × V3c offense
+ 0.40 × new damage-speed-skill offense
```

For new HOT troops:

```txt
V4.3 offense =
new damage-speed-skill offense
```

Total:

```txt
V4.3 total =
0.70 × offense
+ 0.18 × defense
+ 0.12 × reliability
```

## Empirical metric correction

The screenshot transcription contains two metric scopes:

| Scope | Rows | Battles | Contribution index usable? |
|---|---:|---:|:---:|
| Verified full side | 43 | 4 | YES |
| Partial transcription | 66 | 6 | NO |

For partial battles, only direct row metrics such as kills per present are used. Contribution index and kill share from partially transcribed subsets are not treated as full-battle metrics.

Robust empirical processing uses:

```txt
K/P winsorized at 5.0
20-troop prior exposure
survival-adjusted K/P
verified full-side contribution index only
confidence based on exposure, battle count, and verified full-side battles
small capped empirical adjustments
```

This supersedes the aggressive V4.2 calibration proposal.

## Top 20 overall V4.3

Humanoids only. Castellan and special-access troops included.

| # | Troop | V4.3 | Mode | Empirical status | Castellan | Special? |
|---|---|---|---|---|---|---|
| 1 | Westerling Hedgeknight | 100.00 | melee | confirmed_high | FALSE | TRUE |
| 2 | Ravens' Teeth | 95.57 | ranged+fallback | anchor_needs_verified_full_side | TRUE | FALSE |
| 3 | Mallister House Guard | 93.26 | melee | unobserved | FALSE | TRUE |
| 4 | Goldenheart Warrior | 88.64 | ranged+fallback | confirmed_high | FALSE | FALSE |
| 5 | Stark Sworn Sword | 87.41 | melee | unobserved | TRUE | FALSE |
| 6 | Tarly Vanguard | 83.79 | melee | unobserved | TRUE | TRUE |
| 7 | Ibbenese Navigator | 83.40 | melee | provisional_overrank_risk_low_confidence | FALSE | FALSE |
| 8 | Baratheon Hammerknight | 79.72 | melee | unobserved | TRUE | TRUE |
| 9 | Qartheen Enthroned Guardian | 79.39 | ranged+fallback | unobserved | FALSE | TRUE |
| 10 | Riverlands Admiral | 79.24 | melee | empirically_strong | TRUE | FALSE |
| 11 | Ibbenese Whaler | 77.52 | melee | unobserved | FALSE | FALSE |
| 12 | Qohorik Falxman | 77.04 | melee | unobserved | FALSE | FALSE |
| 13 | Qartheen Elite Hoplite | 76.16 | melee | unobserved | FALSE | FALSE |
| 14 | Grafton Flaming Knight | 75.55 | melee | context_dependent_or_unclear | FALSE | TRUE |
| 15 | Norvoshi Grand Bearded Priest | 74.04 | melee | insufficient_data | TRUE | FALSE |
| 16 | Qartheen Longbowman | 73.85 | ranged+fallback | empirically_strong | FALSE | FALSE |
| 17 | Harlaw Captain | 72.89 | melee | unobserved | TRUE | FALSE |
| 18 | Velaryon Sea Guard | 72.63 | melee | unobserved | FALSE | TRUE |
| 19 | Myrish Artisan of War | 71.91 | ranged+fallback | empirically_strong | FALSE | FALSE |
| 20 | Greyjoy Finger Dancer | 71.89 | melee | unobserved | FALSE | FALSE |

## Important control readings

### Ravens' Teeth

```txt
V4.3 = 95.57
```

Still the strongest known proven ranged control. The current screenshot sample has no verified full-side Raven stack large enough to justify a negative empirical adjustment.

### Goldenheart Warrior

```txt
V4.3 = 88.64
empirical status = confirmed_high
```

Goldenheart has the cleanest empirical support and receives only a small positive adjustment.

### Myrish Artisan of War

```txt
V4.3 = 71.91
```

Myrish remains strong, but its crossbow rate/ammo prevents single-shot damage from pushing it above Raven/Goldenheart.

### Frey Assassin

```txt
V4.3 = 60.42
empirical status = empirically_strong
```

Frey's empirical signal remains interesting, but two high K/P rows were outliers and there are no verified full-side Frey samples with meaningful stack size. V4.3 gives only a small empirical boost instead of the previous +14 adjustment.

### Ibbenese Navigator

```txt
V4.3 = 83.40
empirical status = provisional_overrank_risk_low_confidence
```

Theoretical output remains high because of sword, armor, and shield—not the weak javelin. Current empirical exposure is only 15 troops across 3 battles, so it is flagged rather than aggressively cut.

## Castellan package model

The user asked a different question from “what is the strongest single troop?”:

```txt
If I choose only one Castellan/castle, which complete troop tree is best?
```

Terminal descendants are grouped automatically by upgrade-tree root. This correctly groups:

```txt
Blackwood:
- Ravens' Teeth
- Blackwood House Guard
- Blackwood Horseman

Frey:
- Frey Assassin
- Guard of the Crossing
- Frey Horseman

Mallister:
- Mallister Elite Archer
- Mallister House Guard
- Mallister Eagle Knight
```

Castle package formula:

```txt
32% ranged branch
32% infantry branch
10% cavalry branch
16% peak troop
5% second-best troop
5% role coverage
```

Cavalry is deliberately weighted lower because Bannerlord cavalry AI is generally less reliable.

## Best full Castellan packages

| # | Castle/House | Package | Peak troop | Ranged branch | Infantry branch | Cavalry branch |
|---|---|---|---|---|---|---|
| 1 | Blackwood | 100.00 | Ravens' Teeth | Ravens' Teeth | Blackwood House Guard | Blackwood Horseman |
| 2 | Westerling | 96.78 | Westerling Hedgeknight | Westerling Elite Archer | Westerling Hedgeknight | Westerling Knight |
| 3 | Stark | 93.64 | Stark Sworn Sword | Stark Master Longbowman | Stark Sworn Sword | Stark Cavalry |
| 4 | Mallister | 92.86 | Mallister House Guard | Mallister Elite Archer | Mallister House Guard | Mallister Eagle Knight |
| 5 | Greyjoy | 90.44 | Greyjoy Finger Dancer | Greyjoy Sniper | Greyjoy Finger Dancer | Greyjoy Horseman |
| 6 | Tarly | 85.76 | Tarly Vanguard | Tarly Elite Crossbowman | Tarly Vanguard | Tarly Knight |
| 7 | Grafton | 85.51 | Grafton Flaming Knight | Grafton Elite Archer | Grafton Flaming Knight | Grafton Horseman |
| 8 | Harlaw | 81.79 | Harlaw Captain | Harlaw Longbowman | Harlaw Captain | Harlaw Raider |
| 9 | Baratheon | 80.99 | Baratheon Hammerknight | Baratheon Longbowman | Baratheon Hammerknight | Baratheon Knight |
| 10 | Tarth | 76.34 | Tarth Master Halberdier | Tarth Elite Crossbowman | Tarth Master Halberdier | Tarth Horseman |
| 11 | Cerwyn | 75.92 | Cerwyn Marauder | Cerwyn Veteran Archer | Cerwyn Marauder | Cerwyn Horseman |
| 12 | Frey | 75.00 | Frey Assassin | Frey Assassin | Guard of the Crossing | Frey Horseman |
| 13 | Umber | 74.44 | Umber Berzerker | Umber Marksman | Umber House Guard | Umber Horseman |
| 14 | Mormont | 74.36 | Mormont Bowmaiden | Mormont Bowmaiden | Mormont House Guard | Mormont Horseman |
| 15 | Casterly Rock | 74.28 | Guardian of the Rock | Casterly Rock Master Crossbowman | Guardian of the Rock | Casterly Rock Champion |

## Direct answer: Blackwood vs Frey vs Mallister

### Blackwood — current best package

```txt
package score = 100.00
```

Ravens' Teeth is so far ahead as a ranged branch that Blackwood remains #1 even though House Guard and Horseman are only moderate.

### Frey — more balanced than the old single-row view, but not #1

```txt
package score = 75.00
```

Frey is now evaluated correctly as a full three-branch tree:

```txt
Frey Assassin
Guard of the Crossing
Frey Horseman
```

The Assassin receives empirical upside, but its crossbow throughput still does not approach Ravens' Teeth. Guard of the Crossing is reasonable; Horseman is mediocre. Frey is a credible balanced middle-tier package, not the current best castle.

### Mallister — strongest melee/defensive package among the three

```txt
package score = 92.86
```

Mallister House Guard becomes a serious theoretical candidate after damage + speed + marginal skill are applied:

```txt
blunt hammer
strong armor
shield
usable speed
```

Mallister Eagle Knight is solid defensively, but the Elite Archer is weak. Mallister is #4 overall as a castle package and is the strongest of these three when the priority is armored frontline quality rather than ranged dominance.

## Current castle recommendation

### Best proven choice

```txt
Blackwood
```

Reason:

```txt
Ravens' Teeth is the strongest proven troop
and the supporting branches are sufficient
```

### Best new melee-heavy alternative

```txt
Westerling
```

The Hedgeknight is empirically promising, but this is still a newer and less proven package.

### Best defensive/frontline alternative

```txt
Mallister
```

The House Guard is the key unit. It requires targeted empirical testing before being accepted as a true #3 overall troop.

### Frey

```txt
Good balanced package and important empirical upside,
but currently below Blackwood, Westerling, Stark, Mallister, and Greyjoy.
```

## Files

```txt
rot_hot_v43_all_humanoid_ranked.csv
rot_hot_v43_top20_overall.csv
rot_hot_v43_likely_campaign_ranked.csv
rot_hot_v43_key_controls.csv
rot_empirical_robust_metric_audit.csv
rot_empirical_metric_scope_audit.csv
rot_castellan_terminal_troops_v43.csv
rot_castellan_house_package_ranking_v43.csv
rot_castellan_single_line_elites_v43.csv
summary.json
```

## Next blocker

The remaining screenshot transcriptions require the original 2026-07-03 screenshot ZIP at full resolution. The current runtime retained the normalized/transcribed outputs and contact sheets, but not the original 45 full-resolution images.

Once the original ZIP is available again, the next extraction priorities are:

```txt
Ravens' Teeth in a meaningful stack
Celtigar Banneret
Mallister House Guard
Frey Assassin
Grafton Flaming Knight
Ibbenese Navigator
```
