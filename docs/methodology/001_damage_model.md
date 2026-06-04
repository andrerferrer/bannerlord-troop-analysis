# Damage Model Notes

## Purpose

The troop model needs a practical estimate of damage after armor so we can calculate hits to kill.

The goal is not to perfectly reimplement the Bannerlord engine. The goal is to produce a stable and calibratable approximation that predicts troop performance better than raw damage numbers.

## Key idea

Raw weapon damage is not enough.

The relevant value is:

```txt
effective_damage = damage after armor and damage-type behavior
```

Then:

```txt
HTK = effective_enemy_hp / effective_damage
```

## Working assumptions

Human troop base HP:

```txt
100 HP
```

Armor reduces damage non-linearly. A useful approximation is based on:

```txt
armor_curve = 100 / (100 + armor)
```

Damage types should be treated differently against armor.

Working order against armor:

```txt
Blunt > Pierce > Cut
```

## Proxy formula

Initial proxy:

```txt
effective_damage = raw_damage × armor_curve × damage_type_modifier
```

Starting modifiers:

```txt
Blunt  = 1.10
Pierce = 1.00
Cut    = 0.90
```

These are not final constants. They should be calibrated against real battle results and controlled tests.

## Why HTK matters

A troop that crosses a breakpoint from 3 hits to kill to 2 hits to kill can be much stronger than raw score differences suggest.

This is especially important for:

- heavy armor matchups
- blunt weapons
- high damage bows
- crossbows
- elite two-handed weapons
- polearms with high thrust damage

## Future improvement

Replace inferred damage types with actual XML-parsed damage types from item records.

The normalization step should eventually extract:

```txt
weapon_id
weapon_class
damage
damage_type
speed
reach
missile_speed
ammo
handling
```
