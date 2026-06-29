# RoT/HOT V4 Integrated Weapon Output — 2026-06-28

This report supersedes the earlier `weapon_first_v1` overall ranking.

The earlier weapon-first pass correctly noticed that equipped weapon damage matters more than raw troop skill, but it overcorrected by comparing mostly **single-hit effective damage**. That made `crossbow_f` look too strong relative to elite longbows.

V4 integrates weapon damage into the previous V3c HTK/KPM baseline instead of replacing it.

## Core fix

Ranged output now includes:

```txt
single-shot effective damage
ammo capacity
throughput / fire rate
hit probability
range safety
melee fallback
```

So this is no longer true:

```txt
single-shot crossbow damage > longbow damage
therefore crossbow troop > longbow carry
```

## Formula

For existing baseline troops:

```txt
total_v4_integrated =
0.72 × total_v3c
+ 0.28 × weapon_throughput_total_score
```

For new HOT troops without V3c baseline:

```txt
total_v4_integrated = weapon_throughput_total_score
```

New troop rows are therefore provisional until they get empirical validation or full V3c-style calibration.

For ranged tactical output:

```txt
ranged_tactical_score =
0.85 × ranged_carry_score
+ 0.15 × melee_carry_score
```

For ranged carry:

```txt
ranged_capacity_raw =
effective_damage_vs_armor40
× ammo
× hit_probability
× safety

ranged_throughput_raw =
effective_damage_vs_armor40
× shots_per_minute
× hit_probability
× safety
```

## Corrected ranged capacity comparison

| Troop | Weapon | Single-shot | Ammo | Capacity | Throughput | Total V4 |
|---|---|---:|---:|---:|---:|---:|
| Ravens' Teeth | ravens_teeth_longbow | 72.14 | 66 | 4833.80 | 1223.91 | 98.11 |
| Goldenheart Warrior | goldenheart_longbow | 72.14 | 46 | 3297.33 | 1197.87 | 88.57 |
| Myrish Artisan of War | crossbow_f | 75.00 | 18 | 1154.25 | 403.99 | 76.64 |
| Qartheen Enthroned Guardian | qarth_longbow | 70.00 | 32 | 2225.66 | 1162.29 | 72.61 |

This fixes the error where Myrish looked stronger because `crossbow_f` had slightly higher single-hit damage.

## Key control results

| Troop | Total V4 | Total V3c | Weapon layer | Mode |
|---|---:|---:|---:|---|
| Westerling Hedgeknight | 100.00 | — | 100.00 | melee |
| Ravens' Teeth | 98.11 | 100.00 | 93.24 | ranged+fallback |
| Goldenheart Warrior | 88.57 | 95.17 | 71.60 | ranged+fallback |
| Lyseni Enforcer | 79.15 | 88.97 | 53.91 | melee |
| Myrish Artisan of War | 76.64 | 85.03 | 55.07 | melee |
| Celtigar Banneret | 72.78 | 78.40 | 58.32 | melee |
| Qartheen Enthroned Guardian | 72.61 | — | 72.61 | ranged+fallback |

Important sanity check:

```txt
Ravens' Teeth > Myrish Artisan of War
Goldenheart Warrior > Myrish Artisan of War
```

That is the intended correction. Myrish remains excellent, especially contextually, but `crossbow_f` single-hit damage no longer pushes it above proven ranged carries.

## Top likely-campaign ranking

This excludes militia, old Castellan flags, and possible special-access HOT rows.

| # | Troop | Total V4 | Total V3c | Weapon layer | Mode | Best weapon |
|---:|---|---:|---:|---:|---|---|
| 1 | Goldenheart Warrior | 88.57 | 95.17 | 71.60 | ranged+fallback | goldenheart_longbow |
| 2 | Ibbenese Navigator | 86.54 | — | 86.54 | throw+melee | ibb_sword |
| 3 | Ibbenese Whaler | 79.46 | — | 79.46 | melee | ibb_sword |
| 4 | Lyseni Enforcer | 79.15 | 88.97 | 53.91 | melee | aserai_2haxe_2_t4 |
| 5 | Qartheen Elite Hoplite | 78.87 | — | 78.87 | melee | qarth_sword |
| 6 | Myrish Artisan of War | 76.64 | 85.03 | 55.07 | melee | crossbow_f |
| 7 | Tyroshi Corsair | 75.53 | 69.89 | 90.06 | melee | tyroshi_axe3 |
| 8 | Freefolk Thenn Impaler | 75.01 | 68.96 | 90.56 | melee | bronze_axe |
| 9 | Ibbenese Horseman | 73.21 | — | 73.21 | melee | ibb_sword |
| 10 | Qartheen Master Cameleer | 73.13 | — | 73.13 | melee | qarth_sword |

## Top new likely-campaign troops

| # | Troop | Culture | Total V4 | Mode | Best weapon |
|---:|---|---|---:|---|---|
| 1 | Ibbenese Navigator | ibbenese | 86.54 | throw+melee | ibb_sword |
| 2 | Ibbenese Whaler | ibbenese | 79.46 | melee | ibb_sword |
| 3 | Qartheen Elite Hoplite | qartheen | 78.87 | melee | qarth_sword |
| 4 | Ibbenese Horseman | ibbenese | 73.21 | melee | ibb_sword |
| 5 | Qartheen Master Cameleer | qartheen | 73.13 | melee | qarth_sword |
| 6 | Qartheen Longbowman | qartheen | 66.34 | ranged+fallback | qarth_longbow |
| 7 | Ibbenese Master Huntsman | ibbenese | 65.97 | ranged+fallback | woodland_longbow |
| 8 | Ibbenese Timberman | ibbenese | 50.51 | melee | northern_axe_t3 |

## Important interpretation

### Goldenheart Warrior

Goldenheart is again above Myrish in campaign-realistic ranking because the model now counts longbow ammo and throughput, not just single-hit damage.

### Ravens' Teeth

Ravens remains a top overall control. It is still excluded from likely-campaign output by the manual Castellan filter.

### Myrish Artisan of War

Myrish remains strong, but the previous result was inflated by single-shot `crossbow_f` damage. With ammo and throughput included, it no longer outranks the proven bow carries in general/field carry ranking.

### New HOT troops

New HOT troops without V3c baselines are provisional. Good candidates to inspect manually:

```txt
Ibbenese Navigator
Ibbenese Whaler
Qartheen Elite Hoplite
Ibbenese Horseman
Qartheen Master Cameleer
Qartheen Longbowman
```

Special-access candidates remain separated:

```txt
Westerling Hedgeknight
Grafton Flaming Knight
Qartheen Enthroned Guardian
Mallister Eagle Knight
Mallister House Guard
```

## Status

This is the current best integration of:

```txt
V3c theory baseline
+ weapon damage layer
+ ranged capacity/throughput correction
```

It is still not an empirical final truth. The next step is campaign-battle validation with contribution index.
