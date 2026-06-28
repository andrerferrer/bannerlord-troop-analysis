# RoT/HOT Weapon-First Ranking v1 — 2026-06-28

This is a **weapon-damage-first screening** for the new RoT/HOT export.

It is not the final HTK/KPM v3c rebuild. The previous HOT screening was too skill-heavy, so this pass makes equipped weapon damage the main offensive driver and only uses role/skill signals as secondary modifiers.

## Source inputs

Input export:

```txt
rot_hot_xml_export_20260628_011949.zip
```

Prior audit packages used:

```txt
rot_hot_analysis_20260628.zip
rot_hot_screening_v0_20260628.zip
rot_hot_weapon_damage_audit_v1_20260628.zip
rot_hot_existing_update_review_20260628.zip
```

## Method summary

Weapon-first scoring uses:

```txt
weapon effective damage vs armor 40
raw weapon damage
ammo stack / ammo bonus
weapon speed
prior role score, secondary only
defense score, secondary only
```

The key correction is:

```txt
weapon damage > troop skill
```

Skill should modify application and accuracy, but should not be the base offensive score. This matters heavily in RoT/HOT because many troops have very high skill values, while the equipped weapon often determines whether the troop is actually dangerous.

## Outputs to keep

```txt
rot_hot_weapon_first_v1_all_humanoid_ranked.csv
rot_hot_weapon_first_v1_new_non_militia_ranked.csv
rot_hot_weapon_first_v1_new_likely_campaign_ranked.csv
rot_hot_weapon_first_v1_ranged_capability.csv
rot_hot_weapon_first_v1_offensive_melee_capability.csv
rot_hot_weapon_first_v1_defensive_capability.csv
rot_hot_weapon_first_v1_skirmisher_capability.csv
old_existing_troops_likely_real_updates.csv
key_old_control_troops_update_check.csv
```

## Counts

| Metric | Count |
|---|---:|
| humanoid rankable rows | 337 |
| new non-militia rankable rows | 18 |
| new likely-campaign rows | 8 |
| likely old real updates | 6 |

## Top new non-militia troops

| # | Troop | Culture | Access guess | Total | Offense | Defense | Best weapon | Eff dmg |
|---:|---|---|---|---:|---:|---:|---|---:|
| 1 | Westerling Hedgeknight | vlandia | possible special/Castellan | 100.00 | 97.82 | 86.74 | westerling_hammer | 55.45 |
| 2 | Qartheen Enthroned Guardian | qartheen | possible special/Castellan | 96.44 | 92.35 | 81.51 | qarth_longbow | 70.00 |
| 3 | Grafton Flaming Knight | vale | possible special/Castellan | 86.86 | 79.68 | 87.25 | grafton_axe | 42.43 |
| 4 | Mallister House Guard | river | possible special/Castellan | 86.75 | 82.99 | 82.37 | mallister_hammer | 48.05 |
| 5 | Mallister Eagle Knight | river | possible special/Castellan | 85.60 | 73.61 | 97.69 | mallister_sword | 37.71 |
| 6 | Ibbenese Navigator | ibbenese | likely campaign/faction | 84.40 | 76.45 | 83.23 | ibb_sword | 40.54 |
| 7 | Westerling Knight | vlandia | possible special/Castellan | 79.14 | 69.53 | 89.39 | mallister_sword | 37.71 |
| 8 | Grafton Horseman | vale | possible special/Castellan | 78.46 | 69.36 | 87.59 | mallister_sword | 37.71 |
| 9 | Ibbenese Horseman | ibbenese | likely campaign/faction | 78.38 | 72.62 | 79.89 | ibb_sword | 40.54 |
| 10 | Qartheen Longbowman | qartheen | likely campaign/faction | 78.37 | 85.48 | 44.29 | qarth_longbow | 69.29 |
| 11 | Qartheen Master Cameleer | qartheen | likely campaign/faction | 78.27 | 72.58 | 79.63 | qarth_sword | 40.54 |
| 12 | Ibbenese Whaler | ibbenese | likely campaign/faction | 76.67 | 72.37 | 74.75 | ibb_sword | 40.54 |
| 13 | Qartheen Elite Hoplite | qartheen | likely campaign/faction | 75.87 | 72.16 | 72.70 | qarth_sword | 40.54 |
| 14 | Grafton Elite Archer | vale | possible special/Castellan | 70.79 | 76.90 | 39.15 | crossbow_g | 62.86 |
| 15 | Ibbenese Master Huntsman | ibbenese | likely campaign/faction | 68.96 | 73.08 | 43.00 | woodland_longbow | 48.57 |
| 16 | Westerling Elite Archer | vlandia | possible special/Castellan | 64.13 | 67.25 | 40.69 | westerling_mace | 40.66 |
| 17 | Mallister Elite Archer | river | possible special/Castellan | 62.24 | 63.27 | 44.80 | steppe_heavy_bow | 39.29 |
| 18 | Ibbenese Timberman | ibbenese | likely campaign/faction | 58.56 | 55.85 | 53.79 | northern_axe_t3 | 31.11 |

## Top new likely-campaign troops

This excludes possible special/Castellan troops.

| # | Troop | Culture | Total | Offense | Defense | Best weapon | Eff dmg |
|---:|---|---|---:|---:|---:|---|---:|
| 1 | Ibbenese Navigator | ibbenese | 84.40 | 76.45 | 83.23 | ibb_sword | 40.54 |
| 2 | Ibbenese Horseman | ibbenese | 78.38 | 72.62 | 79.89 | ibb_sword | 40.54 |
| 3 | Qartheen Longbowman | qartheen | 78.37 | 85.48 | 44.29 | qarth_longbow | 69.29 |
| 4 | Qartheen Master Cameleer | qartheen | 78.27 | 72.58 | 79.63 | qarth_sword | 40.54 |
| 5 | Ibbenese Whaler | ibbenese | 76.67 | 72.37 | 74.75 | ibb_sword | 40.54 |
| 6 | Qartheen Elite Hoplite | qartheen | 75.87 | 72.16 | 72.70 | qarth_sword | 40.54 |
| 7 | Ibbenese Master Huntsman | ibbenese | 68.96 | 73.08 | 43.00 | woodland_longbow | 48.57 |
| 8 | Ibbenese Timberman | ibbenese | 58.56 | 55.85 | 53.79 | northern_axe_t3 | 31.11 |

## Important interpretation

### Qartheen Enthroned Guardian

Still looks like one of the strongest new units, but now the reason is better grounded:

```txt
qarth_longbow ≈ 70 effective damage vs armor 40
```

This should be treated as possible special/Castellan until access is confirmed.

### Westerling Hedgeknight

The weapon-first pass pushes it very high because it appears to carry:

```txt
westerling_hammer
```

with strong blunt effective damage. This should be manually checked in game because blunt damage tends to overperform against armor.

### Ibbenese Navigator

Best likely-campaign new unit in this pass. It combines solid defense with respectable weapon output.

### Qartheen Longbowman

Likely-campaign ranged standout. The `qarth_longbow` is the important factor, not just skill.

## Existing troop update review

Likely real updates remain concentrated in:

```txt
City Watch Spearman
Stark Sworn Sword
Umber Berzerker
Cerwyn Marauder
Karstark Loyalist
Wight Militia Spearman
```

Do not use raw old-vs-new damage deltas as proof by themselves because the new weapon reconstruction differs from the old V3c proxy.

## Next step

Before final ranking:

1. confirm access for Westerling/Grafton/Mallister/Qartheen special-looking troops;
2. rerun the full V3c HTK/KPM style model using this weapon-damage layer;
3. preserve separate outputs for overall, non-Castellan, likely-campaign, ranged, defensive, offensive melee, and skirmisher capability;
4. keep empirical contribution separate until enough campaign battles exist.
