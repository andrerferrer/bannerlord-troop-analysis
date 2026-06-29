# RoT/HOT V4.1 Skirmisher Reclassification — 2026-06-28

This report reinterprets troops that carry weak throwing sidearms.

## Problem

The V4 integrated model correctly fixed ranged capacity and throughput, but some troops were still being described as `throw+melee` if they carried any throwing weapon.

This was misleading for units like:

```txt
Ibbenese Navigator
```

The Navigator carries:

```txt
northern_javelin_1_t2
throw_eff_damage = 17.36
```

That is not a serious skirmisher weapon. The unit's high score comes from its melee/defensive package, not from the javelin.

## New rule

```txt
meaningful_throwing = throw_eff_damage >= 25.0
weak_throwing_sidearm = throw_eff_damage > 0 and throw_eff_damage < 25.0
```

Weak throwing sidearms no longer qualify a troop for the skirmisher role.

## Skirmisher capability formula

Skirmisher capability now requires meaningful throwing:

```txt
skirmisher_capability =
0.70 × throw_output_score
+ 0.20 × melee_output_score
+ 0.10 × defense_score
```

If `meaningful_throwing = FALSE`, then:

```txt
skirmisher_capability = 0
```

This prevents strong melee troops with weak sidearms from polluting the skirmisher list.

## Ibbenese Navigator reclassification

Before:

```txt
throw+melee / skirmisher-ish
```

After:

```txt
melee / defensive-melee hybrid
weak_throwing_sidearm = TRUE
```

Navigator remains high because of:

```txt
ibb_sword
high armor
shield
melee stats
```

not because of the javelin.

## Key control results

| Troop | Total V4.1 | Mode | Throw dmg | Meaningful throw? | Weak sidearm? |
|---|---:|---|---:|:---:|:---:|
| Ravens' Teeth | 98.11 | ranged+fallback | 0.00 | FALSE | FALSE |
| Ibbenese Navigator | 91.30 | melee | 17.36 | FALSE | TRUE |
| Goldenheart Warrior | 88.57 | ranged+fallback | 0.00 | FALSE | FALSE |
| Lyseni Enforcer | 81.23 | melee | 27.34 | TRUE | FALSE |
| Myrish Artisan of War | 76.64 | melee | 0.00 | FALSE | FALSE |
| Celtigar Banneret | 74.96 | melee | 26.79 | TRUE | FALSE |
| Qartheen Enthroned Guardian | 72.61 | ranged+fallback | 0.00 | FALSE | FALSE |

## Likely-campaign top after reclassification

| # | Troop | Total V4.1 | Mode | Throw dmg | Weak sidearm? |
|---:|---|---:|---|---:|:---:|
| 1 | Ibbenese Navigator | 91.30 | melee | 17.36 | TRUE |
| 2 | Goldenheart Warrior | 88.57 | ranged+fallback | 0.00 | FALSE |
| 3 | Lyseni Enforcer | 81.23 | melee | 27.34 | FALSE |
| 4 | Ibbenese Whaler | 79.46 | melee | 0.00 | FALSE |
| 5 | Qartheen Elite Hoplite | 78.87 | melee | 0.00 | FALSE |
| 6 | Myrish Artisan of War | 76.64 | melee | 0.00 | FALSE |
| 7 | Tyroshi Corsair | 76.47 | melee | 23.14 | TRUE |
| 8 | Freefolk Thenn Impaler | 75.30 | melee | 33.94 | FALSE |
| 9 | Ibbenese Horseman | 73.21 | melee | 0.00 | FALSE |
| 10 | Qartheen Master Cameleer | 73.13 | melee | 0.00 | FALSE |

## Interpretation

The Navigator is still a serious new candidate, but not as a top skirmisher.

Correct reading:

```txt
Ibbenese Navigator = strong melee/defensive hybrid with weak throwing sidearm
```

This also means future skirmisher rankings should only include units whose throwing weapon meaningfully contributes to combat.

## Status

V4.1 supersedes V4 for skirmisher interpretation. V4.1 does not otherwise rewrite the V4 ranged-capacity fix.
