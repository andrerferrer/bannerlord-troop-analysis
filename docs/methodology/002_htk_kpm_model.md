# HTK/KPM Scoring Model

## Purpose

The model estimates offense through expected kill conversion rather than abstract offensive stats.

The central question is:

```txt
How quickly does this troop convert actions into kills?
```

## HTK

Hits to kill:

```txt
HTK = effective_enemy_hp / effective_damage
```

For baseline vanilla human troops:

```txt
effective_enemy_hp = 100
```

Campaign modifiers may increase effective HP, especially Medicine perks.

## KPM

Expected kills per minute:

```txt
KPM = attempts_per_minute × hit_chance ÷ HTK
```

This makes offense depend on:

- damage after armor
- weapon speed
- hit chance
- skill
- damage type
- ranged accuracy
- target armor profile

## Target profiles

Use multiple target profiles instead of a single enemy.

Initial profiles:

```txt
Light target
Standard target
Heavy target
```

Overall offense can blend them:

```txt
offense_raw =
0.25 × KPM_vs_light
+ 0.50 × KPM_vs_standard
+ 0.25 × KPM_vs_heavy
```

For campaign-focused analysis, standard and heavy targets may deserve more weight.

## Split offense

Do not collapse melee and ranged too early.

Calculate separately:

```txt
melee_kpm
ranged_kpm
throwing_kpm
```

Then blend according to expected battlefield behavior.

Example:

```txt
ranged_blend = 0.80 × ranged_kpm + 0.20 × melee_kpm
throwing_blend = 0.35 × throwing_kpm + 0.65 × melee_kpm
melee_only = melee_kpm
```

Then:

```txt
offense = max(melee_only, ranged_blend, throwing_blend)
```

## Why split offense matters

Ranged and melee HTK are not equivalent.

Ranged output is affected by:

- accuracy
- line of sight
- ammo
- target shields
- range
- projectile speed

Melee output is affected by:

- contact uptime
- formation behavior
- weapon reach
- swing speed
- shield interference
- AI weapon usage

## Current total score direction

A working total score can use:

```txt
total =
0.65 × offense
+ 0.20 × defense
+ 0.15 × reliability
```

This should remain adjustable.

The important rule is that defense should not automatically multiply offense. Glass cannon troops can perform extremely well if they kill quickly and maintain output.

## Validation rule

The model should be judged by whether it predicts real battle outcomes.

If controlled tests show that a high-offense low-defense troop consistently dominates, the model should not penalize it just because it is fragile on paper.
