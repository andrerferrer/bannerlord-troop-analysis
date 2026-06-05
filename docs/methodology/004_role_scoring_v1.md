# Role Scoring v1

## Purpose

This model scores troops by tactical role instead of forcing a single global ranking.

A score of `100` in Archer is not directly comparable to a score of `100` in Defensive Cavalry.

## Roles

```txt
Archer
Crossbow
Horse Archer
Defensive Infantry
Offensive Infantry
Defensive Cavalry
Offensive Cavalry
```

## Eligibility rule

Role eligibility is based primarily on `default_group`, not just equipment.

Examples:

```txt
Fian Champion = Archer, not Offensive Infantry
Khan's Guard = Horse Archer, not generic Cavalry
Vlandian Sharpshooter = Crossbow
```

Fallback weapons can improve a role score, but they do not redefine the troop's main role.

## Data policy

- Ranged weapons use direct XML stats.
- Defense uses direct armor, shield, horse, and harness stats.
- Crafted melee still uses conservative template proxy only.
- HTK/KPM is not used for CraftedItem yet.
- No global ranking should be generated from this model yet.

## Campaign line outputs

Each role has two outputs:

```txt
role_<role>_all.csv
role_<role>_campaign_lines.csv
```

The `campaign_lines` output excludes special or unlinked troops.

## Known limitations

The model is still conservative around melee because crafted weapon final stats are not reconstructed.

Next improvements:

1. Reconstruct or dump final CraftedItem stats.
2. Add direct-stat HTK for bows/crossbows.
3. Add role-specific empirical validation.
4. Only then consider a global score.
