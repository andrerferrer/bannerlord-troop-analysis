# v7.2 Burst Score Assumptions

## Scope

v7.2 adds `burst_score_v72` as a **parallel context score**. It does not replace v7.1 `total_score_v71` / `general_score`.

Boarding score is intentionally excluded from this version.

## Goal

Capture short-contact and early-kill pressure that the general ranking hides, especially:

- high-ammo javelin infantry;
- mounted javelin cavalry;
- strong first-contact ranged output;
- shock cavalry charge impact;
- limited melee fallback for close-contact burst.

## Formula

For each troop, compute four raw burst candidates:

```txt
throw_burst_raw = throw_pressure_v7 × throw_ammo_factor × throw_damage_type_factor × mounted_throw_bonus
ranged_burst_raw = ranged_kpm_v7 × ranged_ammo_factor × ranged_type_factor
charge_burst_raw = charge_impact_score_v7 / 100 × 4.75
melee_burst_raw = melee_kpm_eff_v7 × 0.65
```

Then:

```txt
burst_raw = max(throw_burst_raw, ranged_burst_raw, charge_burst_raw, melee_burst_raw)
burst_offense_score = clamp(burst_raw / 7.0 × 100, 0, 100)

burst_score_v72 =
  0.70 × burst_offense_score
+ 0.20 × reliability_score
+ 0.10 × defense_score_v71
```

## Throwing ammo factor

```txt
throw_ammo_factor = clamp(0.55 + 0.07 × min(primary_throw_ammo, 10), 0.55, 1.25)
```

This keeps low-ammo axes/pila relevant but prevents them from acting like sustained javelin supply.

## Throwing damage type factor

```txt
Pierce = 1.10
Blunt  = 1.05
Cut    = 0.88
```

## Mounted throwing bonus

```txt
mounted_throw_bonus = 1.12 if is_mounted else 1.00
```

This preserves the Aserai Vanguard Faris behavior observed in practice: mounted javelins are more reliable as first-contact burst than equivalent foot throwing.

## Ranged factors

```txt
ranged_ammo_factor = clamp(0.75 + ranged_ammo_v7 / 80, 0.75, 1.35)
ranged_type_factor = 1.15 for crossbow, 1.05 for horse archer, 1.00 otherwise
```

## Interpretation

`burst_score_v72` answers:

```txt
Which unit can create the most early kill pressure in short-contact fights?
```

It does **not** answer:

```txt
Which unit is best overall in a long open-field battle?
```

Use v7.1 total score for general ranking.
