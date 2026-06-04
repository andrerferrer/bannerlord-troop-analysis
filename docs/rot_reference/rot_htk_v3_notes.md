# Realm of Thrones Reference Notes

## Purpose

These notes preserve the methodology developed during Realm of Thrones testing.

The primary repo target is vanilla Bannerlord. RoT is included only as reference and calibration history.

## Important findings from RoT testing

### 1. Abstract offense was not enough

Early scores used a broad offensive composite. This was useful for initial rankings but not precise enough.

A better approach is:

```txt
offense = expected kill conversion
```

through HTK and KPM.

### 2. Glass cannon troops can be excellent

Do not automatically penalize low-defense troops.

RoT testing showed that some high-output troops can carry battles by killing quickly enough that fragility does not collapse their performance.

The model should penalize fragility only when empirical tests show output collapse.

### 3. Defense should not simply multiply offense

A previous idea was:

```txt
effective_output = offense × uptime
```

This overvalued defensive troops.

A better structure is:

```txt
total = offense + defense + reliability
```

where reliability is not the same as armor.

### 4. Split offense is useful

Melee and ranged output should be calculated separately.

```txt
melee_kpm
ranged_kpm
throwing_kpm
```

Then blend based on expected battlefield behavior.

### 5. HTK explains many real outcomes

The key question is often:

```txt
How many hits does this troop need to kill a standard target?
```

This captures damage breakpoints better than raw damage.

## Control cases used in RoT

These were useful for calibrating the model:

```txt
Ravens' Teeth
Goldenheart Warrior
Lyseni Enforcer
Celtigar Banneret
Myrish Artisan of War
```

These are not vanilla recommendations. They are only reference examples for model behavior.

## Current RoT model direction

The latest RoT working model used:

```txt
HTK = enemy_hp / effective_damage
KPM = attempts_per_minute × hit_chance ÷ HTK
```

with split offense:

```txt
melee_only = melee_kpm
ranged_blend = 0.80 × ranged_kpm + 0.20 × melee_kpm
throwing_blend = 0.35 × throwing_kpm + 0.65 × melee_kpm
offense = max(melee_only, ranged_blend, throwing_blend)
```

This should be treated as a starting point, not final truth.
