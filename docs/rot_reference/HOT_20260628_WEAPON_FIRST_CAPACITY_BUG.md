# HOT 2026-06-28 Weapon-First Capacity Bug

The first `weapon_first_v1` ranking made a second important mistake:

```txt
it compared mostly single-hit effective damage
instead of total applied weapon output
```

This is why Myrish Artisan of War could appear above Ravens' Teeth / Goldenheart Warrior in a weapon-first table.

## The concrete issue

From the weapon audit:

| Troop | Weapon | Eff dmg vs armor 40 | Ammo | Speed |
|---|---|---:|---:|---:|
| Myrish Artisan of War | crossbow_f | 75.00 | 18 | 63 |
| Ravens' Teeth | ravens_teeth_longbow | 72.14 | 66 | 94 |
| Goldenheart Warrior | goldenheart_longbow | 72.14 | 46 | 94 |

Myrish has slightly higher single-shot effective damage:

```txt
75.00 vs 72.14
```

But Ravens and Goldenheart have vastly higher total ranged damage capacity and rate of fire.

Approximate damage capacity:

```txt
Myrish = 75.00 × 18 = 1350
Ravens = 72.14 × 66 = 4761
Goldenheart = 72.14 × 46 = 3318
```

Approximate capacity ratio:

```txt
Ravens / Myrish ≈ 3.53×
Goldenheart / Myrish ≈ 2.46×
```

If speed/reload is included, the gap grows further because the longbows are faster and bows have better sustained output than crossbows.

## Correct interpretation

Weapon damage should not mean:

```txt
best single hit damage
```

It should mean:

```txt
total applied weapon output
```

For ranged units, the next formula must include at least:

```txt
effective_damage_after_armor
× shots_per_minute
× hit_probability
× ammo_capacity
× target_access
× range_safety
```

A crossbow can have higher single-shot damage and still be much weaker as a battlefield carry than an elite longbow unit.

## Correct sanity rule

Even under a weapon-first concept, Ravens' Teeth and Goldenheart Warrior should remain above Myrish Artisan of War in open-field / general carry ranking unless empirical data strongly contradicts that.

Myrish may still be excellent, especially in siege defense, but the previous weapon-first table overranked it because it did not include ammo capacity and fire-rate throughput.

## Required fix for V4

Replace:

```txt
weapon_score = max(single_hit_effective_damage)
```

with a separated ranged throughput model:

```txt
ranged_single_shot_damage = effective_damage_after_armor
ranged_capacity_damage = effective_damage_after_armor × ammo
ranged_throughput = effective_damage_after_armor × shots_per_minute × hit_probability
ranged_battle_output = min(ranged_capacity_damage, ranged_throughput × expected_ranged_uptime_minutes)
```

For broad ranking, use:

```txt
ranged_carry_score =
0.35 × normalized(ranged_throughput)
+ 0.35 × normalized(ranged_capacity_damage)
+ 0.20 × normalized(range_safety / target_access)
+ 0.10 × melee_fallback
```

The exact weights are provisional, but capacity and rate must be present.

## Status

`weapon_first_v1` remains useful as a weapon audit layer only.

It is **not** a correct overall ranking and should not be used to compare elite bow carries against crossbow or blunt-heavy troops until the capacity/rate bug is fixed.
