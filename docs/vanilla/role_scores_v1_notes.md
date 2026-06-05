# Vanilla Role Scores v1 — 2026-05-23

This package replaces the previous single-score approach with role-specific scoring.

## Categories

The tactical categories are:

```txt
Ranged Troops
Defensive Troops
Offensive Melee
Skirmishers
```

## Category rules

Primary category is assigned by tactical role, not by whichever subscore is highest.

```txt
has bow/crossbow -> Ranged Troops
else has throwing -> Skirmishers
else shield / horse / high defense -> Defensive Troops
else -> Offensive Melee
```

Horse archers are merged into Ranged Troops.

Cavalry is not a separate category. Heavy cavalry can rank as Defensive Troops. Melee cavalry can still receive Offensive Melee score, but it is not separated into its own bucket.

## Scoring constraints

This is still conservative and not final.

- Ranged uses direct XML stats only.
- Defense uses real armor, shield, horse and harness stats.
- Crafted melee uses conservative template proxies only.
- HTK/KPM is still disabled for CraftedItem.
- Role rankings are more meaningful than a global overall ranking.

## Files

| File | Purpose |
|---|---|
| `vanilla_roster_role_scores_v1.csv` | roster-level role score audit |
| `vanilla_troop_role_scores_v1.csv` | troop-level role score table |
| `vanilla_primary_category_rankings_v1.csv` | one primary category per troop |
| `ranged_troops.csv` | ranged troops ranking |
| `defensive_troops.csv` | defensive troops ranking |
| `offensive_melee.csv` | offensive melee ranking |
| `skirmishers.csv` | skirmisher ranking |
| `vanilla_sanity_role_scores_v1.csv` | control troop sanity table |

## Known limitation

Fian Champion and Khan's Guard are now in the right category, but the exact relative scores still need calibration.

The next step is role-specific sanity calibration, not global ranking.
