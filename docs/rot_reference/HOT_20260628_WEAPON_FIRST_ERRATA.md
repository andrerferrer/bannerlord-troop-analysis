# HOT 2026-06-28 Weapon-First Ranking Errata

The `weapon_first_v1` ranking should **not** be treated as the canonical overall RoT/HOT ranking.

It was a diagnostic pass created after the first HOT screening was too skill-heavy. It corrected one issue — weapon damage should matter more than raw troop skill — but introduced another issue: it overweighted single-hit weapon damage and defensive value relative to proven battlefield carry performance.

## Canonical correction

Based on prior theoretical work and player testing, these remain the main calibration anchors:

```txt
Ravens' Teeth
Goldenheart Warrior
```

Any overall model that pushes both Ravens' Teeth and Goldenheart Warrior out of the top practical tier should be treated as failed or incomplete.

## What weapon-first v1 is still useful for

Use it as an audit layer for:

- identifying high-damage weapons;
- identifying new suspicious HOT weapons;
- detecting blunt/crossbow/longbow outliers;
- reviewing new troops before HTK/KPM recalculation.

Do **not** use it as final overall troop ranking.

## Why weapon-first v1 overcorrected

It gave too much value to:

```txt
single-hit effective damage
armor/defense
blunt weapon damage
crossbow raw damage
```

It did not fully capture:

```txt
ranged uptime
bow rate of fire
kill safety
AI target access
battlefield carry effect
ammo-to-kill conversion
melee exposure risk
how fast glass-cannon ranged troops remove threats
```

This is why units such as Myrish Artisan of War, Westerling Hedgeknight, and some heavy defensive troops could appear too high relative to Ravens' Teeth and Goldenheart Warrior.

## Correct next model direction

The next model should be:

```txt
weapon damage layer
→ HTK
→ attack rate / reload rate
→ hit chance / skill application
→ ammo capacity
→ ranged uptime and kill safety
→ melee exposure and AI usability
→ defense/reliability
```

In particular, ranged carry score must include:

```txt
ranged_carry_score =
effective_damage_after_armor
× attacks_per_minute
× hit_probability
× ammo_sustain
× target_access
× range_safety
```

Crossbow and bow damage cannot be compared using raw damage alone.

## Acceptance tests for the next RoT/HOT overall model

The next overall ranking must satisfy these sanity checks unless strong empirical data proves otherwise:

1. Ravens' Teeth is top-tier overall.
2. Goldenheart Warrior is top-tier overall and top-tier non-Castellan.
3. Lyseni Enforcer remains a high melee-output control.
4. Celtigar Banneret remains a high defensive/uptime control, but should not automatically outrank elite ranged carries.
5. Myrish Artisan of War may be very high, especially in siege defense, but should not jump above proven carry controls on crossbow raw damage alone.
6. Golden Company Mahout remains flagged as possible false positive until more empirical campaign samples support it.

## Status

`weapon_first_v1` is now classified as:

```txt
diagnostic weapon audit, not final ranking
```

The previous V3c HTK/KPM split-offense ranking remains the better theoretical baseline until a V4 model is generated.
