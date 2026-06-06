# v7.3 Tooltip-Validated Throw Damage Burst Score

## Scope

v7.3 updates only the burst context score. It does **not** replace v7.1 `general_score`.

Primary change:

```txt
tooltip-validated throwing damage is now the source of truth when available.
```

Validated throwing damage examples:

```txt
Hooked Javelin = 117 Pierce
Broad Blade Javelin = 101 Pierce
Harpoon = 113 Pierce
Jereed = 121 Pierce
```

## Calibration change

v7.2 used proxy throwing damage inside `throw_pressure_v7`. v7.3 switches to a source-specific throw burst score:

```txt
throw_damage_used_v73 = tooltip_throw_damage if available else primary_throw_damage
throw_damage_factor_v73 = clamp(throw_damage_used_v73 / 110, 0.70, 1.10)
throw_skill_factor_v73 = clamp(0.75 + throwing / 400, 0.75, 1.20)
throw_ammo_factor_v73 = 0.70 + 0.08 × min(ammo, 5) + 0.04 × min(max(ammo - 5, 0), 5)
mounted_throw_bonus_v73 = 1.12 if mounted else 1.00
```

The throw score is normalized against a Faris-like reference:

```txt
Jereed / 140 throwing / 5 ammo / mounted
```

This avoids blindly multiplying old proxy KPM by `tooltip/proxy` while still treating tooltip damage as the real raw item stat.

## Top 10 burst units — regular combined

| Rank | Troop | Tier | Category | Scope | Burst v7.3 | Source | General rank v7.1 | v7.2 burst rank | Δ vs v7.2 |
|---:|---|---:|---|---|---:|---|---:|---:|---:|
| 1 | Aserai Vanguard Faris | 6 | Offensive Cavalry | Vanilla | 96.026 | throw | 3 | 1 | 0 |
| 2 | Battanian Skipari | 5 | Offensive Infantry | War Sails | 92.910 | throw | 38 | 2 | 0 |
| 3 | Imperial Naute | 5 | Offensive Infantry | War Sails | 92.828 | throw | 42 | 3 | 0 |
| 4 | Battanian Fian Champion | 6 | Archer | Vanilla | 90.161 | ranged | 2 | 4 | 0 |
| 5 | Aserai Veteran Faris | 5 | Offensive Cavalry | Vanilla | 85.218 | throw | 83 | 50 | -45 |
| 6 | Imperial Coast Guard | 4 | Offensive Infantry | War Sails | 84.188 | throw | 69 | 7 | -1 |
| 7 | Battanian Fian | 5 | Archer | Vanilla | 78.467 | ranged | 4 | 8 | -1 |
| 8 | Khuzait Khan's Guard | 6 | Horse Archer | Vanilla | 78.030 | ranged | 1 | 9 | -1 |
| 9 | Battanian River Raider | 4 | Offensive Infantry | War Sails | 77.213 | throw | 58 | 5 | +4 |
| 10 | Battanian Mounted Skirmisher | 5 | Defensive Cavalry | Vanilla | 71.127 | throw | 13 | 6 | +4 |

## Top 10 War Sails burst units

| Rank WS | Troop | Tier | Category | Burst v7.3 | Source | General rank v7.1 |
|---:|---|---:|---|---:|---|---:|
| 1 | Battanian Skipari | 5 | Offensive Infantry | 92.910 | throw | 38 |
| 2 | Imperial Naute | 5 | Offensive Infantry | 92.828 | throw | 42 |
| 3 | Imperial Coast Guard | 4 | Offensive Infantry | 84.188 | throw | 69 |
| 4 | Battanian River Raider | 4 | Offensive Infantry | 77.213 | throw | 58 |
| 5 | Nord Sky-Gods Chosen | 5 | Archer | 62.204 | ranged | 40 |
| 6 | Aserai Bahriyyah | 5 | Archer | 60.829 | ranged | 28 |
| 7 | Imperial Shipmate | 3 | Offensive Infantry | 59.096 | throw | 125 |
| 8 | Sturgian Reaver | 5 | Offensive Infantry | 58.990 | throw | 49 |
| 9 | Nord Huscarl | 6 | Offensive Infantry | 58.906 | throw | 32 |
| 10 | Nord Ulfhedinn | 5 | Offensive Infantry | 57.344 | melee | 19 |

## Key interpretation

- Aserai Vanguard Faris remains the top burst benchmark.
- Battanian Skipari remains a major War Sails burst outlier, but now because its tooltip-validated 10 Hooked Javelins are real, not due to ammo overcount.
- Imperial Naute remains elite in burst context while staying outside S-tier in general score.
- Fian Champion and Khan's Guard remain top general units; their burst ranks are lower because v7.3 measures first-contact pressure, not sustained battle value.

## Follow-up

The main open validation question remains empirical:

```txt
Does Battanian Skipari actually deliver its tooltip-supported burst in battle results?
```
