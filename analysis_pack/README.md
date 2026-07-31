# analysis_pack — entry point for the analysis agent

Pre-joined troop/item tables for four Bannerlord tracks. **Do not fetch raw module
XML — it is intentionally not published.** Read `SCHEMA.md` first, then load the CSVs
you need from the raw URLs below.

- Built: 2026-07-31 · Bannerlord v1.4.7
- Files: 24 · Total: 39.0 MB
- Integrity: `MANIFEST.csv` carries sha256 + row counts for every file.


## Start here

1. `SCHEMA.md` — column meanings and the **mandatory filters** (`item_found`, soldiers
   only, drop multiplayer/obsolete, keep NavalDLC).
2. `<track>/<track>_troop_equipment_audit.csv` — the main flat table.
3. Everything else is a lookup.


## Row counts (main table)

| track | equipment rows | items resolved | troops |
|---|---:|---:|---:|
| `vanilla` | 18,153 | 2,316 | 1,937 |
| `nightmare_sails` | 18,736 | 2,430 | 1,989 |
| `realm_of_thrones` | 55,436 | 3,795 | 6,187 |
| `taom` | 40,351 | 5,858 | 5,257 |

## Files


### `vanilla`

- [`vanilla_items_catalog.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/vanilla/vanilla_items_catalog.csv) — 2,316 rows, 0.3 MB
- [`vanilla_override_report.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/vanilla/vanilla_override_report.csv) — 1,937 rows, 0.1 MB
- [`vanilla_tree_tiers.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/vanilla/vanilla_tree_tiers.csv) — 367 rows, 0.1 MB
- [`vanilla_troop_equipment_audit.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/vanilla/vanilla_troop_equipment_audit.csv) — 18,153 rows, 4.5 MB
- [`vanilla_troops.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/vanilla/vanilla_troops.csv) — 1,937 rows, 0.3 MB
- [`vanilla_upgrade_edges.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/vanilla/vanilla_upgrade_edges.csv) — 218 rows, 0.0 MB

### `nightmare_sails`

- [`nightmare_sails_items_catalog.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/nightmare_sails/nightmare_sails_items_catalog.csv) — 2,430 rows, 0.3 MB
- [`nightmare_sails_override_report.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/nightmare_sails/nightmare_sails_override_report.csv) — 1,989 rows, 0.2 MB
- [`nightmare_sails_tree_tiers.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/nightmare_sails/nightmare_sails_tree_tiers.csv) — 371 rows, 0.1 MB
- [`nightmare_sails_troop_equipment_audit.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/nightmare_sails/nightmare_sails_troop_equipment_audit.csv) — 18,736 rows, 4.7 MB
- [`nightmare_sails_troops.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/nightmare_sails/nightmare_sails_troops.csv) — 1,989 rows, 0.3 MB
- [`nightmare_sails_upgrade_edges.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/nightmare_sails/nightmare_sails_upgrade_edges.csv) — 241 rows, 0.0 MB

### `realm_of_thrones`

- [`realm_of_thrones_items_catalog.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/realm_of_thrones/realm_of_thrones_items_catalog.csv) — 3,795 rows, 0.4 MB
- [`realm_of_thrones_override_report.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/realm_of_thrones/realm_of_thrones_override_report.csv) — 6,187 rows, 0.3 MB
- [`realm_of_thrones_tree_tiers.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/realm_of_thrones/realm_of_thrones_tree_tiers.csv) — 1,232 rows, 0.2 MB
- [`realm_of_thrones_troop_equipment_audit.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/realm_of_thrones/realm_of_thrones_troop_equipment_audit.csv) — 55,436 rows, 13.1 MB
- [`realm_of_thrones_troops.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/realm_of_thrones/realm_of_thrones_troops.csv) — 6,187 rows, 0.8 MB
- [`realm_of_thrones_upgrade_edges.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/realm_of_thrones/realm_of_thrones_upgrade_edges.csv) — 902 rows, 0.0 MB

### `taom`

- [`taom_items_catalog.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/taom/taom_items_catalog.csv) — 5,858 rows, 0.9 MB
- [`taom_override_report.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/taom/taom_override_report.csv) — 5,257 rows, 0.2 MB
- [`taom_tree_tiers.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/taom/taom_tree_tiers.csv) — 1,239 rows, 0.2 MB
- [`taom_troop_equipment_audit.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/taom/taom_troop_equipment_audit.csv) — 40,351 rows, 11.1 MB
- [`taom_troops.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/taom/taom_troops.csv) — 5,257 rows, 0.8 MB
- [`taom_upgrade_edges.csv`](https://raw.githubusercontent.com/andrerferrer/bannerlord-troop-analysis/aferrer/analysis-pack-20260731/analysis_pack/taom/taom_upgrade_edges.csv) — 893 rows, 0.0 MB


## Provenance note (read this before trusting an older TAOM pack)

TAOM's item definitions live in `LOTRLOME_Armory` and `Alliance.Wargs`. In the game
install both are **unreadable symlinks**, so every previous export walked them as empty
directories and produced a TAOM catalog with 4 mod items and ~18,400 unresolvable
equipment references that were blanket-allowlisted. Those tracks' melee and armor scores
were hollow.

This build sources those two modules from `TAOM_2_0_12.zip` instead. TAOM now contributes
**3,538 resolved items**, and the allowlist is down to **13 ids** (`orc_rider_*`),
referenced only by a multiplayer test roster in
`Alliance.Wargs/ModuleData/CharactersTest/LOTR/lotr_mpcharacters_isengard.xml` and never
shipped as `<Item>` definitions — a mod-side gap, not a pipeline gap. Those troops are
excluded by the multiplayer filter anyway.

Any TAOM analysis produced before 2026-07-31 should be recomputed.
