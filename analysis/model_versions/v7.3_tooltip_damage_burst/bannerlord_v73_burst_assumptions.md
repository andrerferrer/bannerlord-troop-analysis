# v7.3 Burst Score Assumptions

## Decision

Tooltip-validated throwing damage is the source of truth for raw throwing item stats when available.

## What changed from v7.2

v7.2 used proxy/crafted throwing damage inside `throw_pressure_v7`.

v7.3 uses:

```txt
throw_damage_used_v73 = tooltip_throw_damage if available else primary_throw_damage
```

This prevents validated items like Hooked Javelin, Harpoon, Broad Blade Javelin, and Jereed from being undervalued by crafted/proxy damage.

## Why not simply multiply throw_pressure by tooltip/proxy ratio?

Because old `throw_pressure_v7` was calibrated on the proxy scale. A direct ratio would cause nearly every validated javelin troop to hit the burst ceiling and would remove useful ranking granularity.

Instead, v7.3 uses source-specific throw factors:

```txt
throw_damage_factor = clamp(damage / 110, 0.70, 1.10)
throw_skill_factor = clamp(0.75 + throwing / 400, 0.75, 1.20)
throw_ammo_factor = 0.70 + 0.08 × min(ammo, 5) + 0.04 × min(max(ammo - 5, 0), 5)
mounted_throw_bonus = 1.12 if mounted else 1.00
```

`burst_score_v73` remains a context-specific burst score and does not replace v7.1 general score.
