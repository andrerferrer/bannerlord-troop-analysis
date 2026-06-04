# Vanilla Audit Rebuild Notes

## Why this rebuild exists

The previous preliminary ranking was discarded.

It mixed:

```txt
XML normalization
CraftedItem stat inference
HTK/KPM scoring
```

That produced false positives such as mid/common troops ranking above known elite units.

This rebuild returns to audit mode.

## Rules

### No level-to-tier assumption

`level` is preserved as a raw field.

Tier is derived from upgrade-tree depth:

```txt
root troop = tree_tier 1
upgrade child = tree_tier 2
next upgrade = tree_tier 3
```

This avoids assuming that `level 31 = tier 7` or similar.

### No aggressive CraftedItem HTK

`CraftedItem` records are linked to troops but not reconstructed into final damage/speed.

```txt
crafted_stats_reconstructed = FALSE
score_usage_status = audit_only_no_aggressive_htk
```

### Sanity-check first

No global ranking should be generated until the sanity-check table is accepted.

Control troops:

```txt
Battanian Fian Champion
Khuzait Khan's Guard
Imperial Legionary
Vlandian Sergeant
Vlandian Sharpshooter
Imperial Elite Cataphract
Vlandian Banner Knight
Sturgian Druzhinnik Champion
Aserai Vanguard Faris
Khuzait Darkhan
```

## Generated datasets

```txt
vanilla_troops.csv
vanilla_upgrade_edges.csv
vanilla_tree_tiers.csv
vanilla_equipment_rosters.csv
vanilla_items_direct.csv
vanilla_items_crafted.csv
vanilla_troop_equipment_audit.csv
vanilla_roster_audit_summary.csv
vanilla_sanity_check_table.csv
```

## Next step

Choose a conservative strategy for CraftedItem stats before reintroducing scoring.
