# analysis_pack — schema

Normalized, pre-joined Bannerlord troop/item data. **No raw module XML is needed to use
this pack.** Every file is UTF-8 CSV with a header row.

Four tracks, identical schema:

| track | contents |
|---|---|
| `vanilla` | Native + Sandbox + SandboxCore + StoryMode + **NavalDLC (War Sails)** |
| `nightmare_sails` | vanilla baseline + `NightmareSailsxDTAB` |
| `realm_of_thrones` | vanilla baseline + `ROT-Core`, `ROT-Content`, `ROT-Dragon`, `ROT-Map` |
| `taom` | vanilla baseline + `TAOM.Dependencies`, `Alliance.Wargs`, `LOTRLOME_Armory`, `TAOM`, `TAOM_Map` |

NavalDLC is part of every baseline, not a separate track. It carries the whole Nord culture
(24 troops) plus marines for five cultures — excluding it drops a faction.

---

## `<track>_troop_equipment_audit.csv` — the main table

One row per **troop x roster_index x equipment slot**, with the resolved item's stats
already joined in. This is the table to start from; the others are lookups.

**Identity / roster**

| column | meaning |
|---|---|
| `troop_id` | stable id, join key across all files |
| `troop_name` | display name |
| `roster_index` | a troop may have several alternative equipment rosters; the game picks one at spawn. Aggregate across rosters (mean) or pick index 0 — do not sum. |
| `slot` | `Item0`..`Item4`, `Head`, `Body`, `Leg`, `Gloves`, `Cape`, `Horse`, `HorseHarness` |
| `equipment_source` | which module's roster the row came from |

**Item resolution**

| column | meaning |
|---|---|
| `item_id` | referenced item id |
| `item_found` | `True` if the item definition was located. **Filter on this before scoring.** |
| `item_kind` | `direct` (an `<Item>` def) or `crafted` (assembled from crafting pieces) |
| `type` | `OneHandedWeapon`, `Bow`, `BodyArmor`, `Horse`, ... |
| `crafting_template`, `crafted_stats_reconstructed` | for crafted weapons: template used, and whether stats were rebuilt from pieces |
| `score_usage_status` | whether the row is safe to score |

**Item stats** (blank when not applicable to the type)

`weapon_class`, `stack_amount`, `speed_rating`, `missile_speed`, `accuracy`,
`weapon_length`, `swing_damage`, `swing_damage_type`, `thrust_damage`,
`thrust_damage_type`, `hit_points`, `shield_armor`, `head_armor`, `body_armor`,
`arm_armor`, `leg_armor`, `horse_speed`, `horse_maneuver`, `horse_charge_damage`,
`horse_extra_health`

Damage types are `Cut` / `Pierce` / `Blunt` and interact with armor differently — do not
compare raw damage numbers across types without modelling that.

**Troop attributes** (repeated on every row of that troop)

`level`, `occupation`, `culture`, `default_group` (`Infantry` / `Ranged` / `Cavalry` /
`HorseArcher`), and skills `OneHanded`, `TwoHanded`, `Polearm`, `Bow`, `Crossbow`,
`Throwing`, `Riding`, `Athletics`.

**Upgrade tree**

`tree_root_id`, `upgrade_depth`, `tree_tier`, `line_status`, `line_status_corrected`
(prefer the `_corrected` variant).

---

## Supporting files

- `<track>_troops.csv` — one row per troop (NPCs included, not only soldiers).
- `<track>_items_catalog.csv` — one row per resolved item id: `item_id`, `item_kind`,
  `type`, `crafting_template`, `name`, `culture`, `source_xml`, `winner_module`,
  `load_order_rank`. `winner_module` is the module that won the load-order conflict.
- `<track>_upgrade_edges.csv` — `from_troop_id` -> `to_troop_id` upgrade graph.
- `<track>_tree_tiers.csv` — tier/depth per troop.
- `<track>_override_report.csv` — which mod redefined which baseline id.

---

## Mandatory filters before ranking anything

1. **`item_found == True`.** Unresolved ids carry no stats; averaging over them silently
   deflates scores.
2. **Soldiers only.** Keep `occupation == Soldier`; drop notables, wanderers, lords.
3. **Drop multiplayer and obsolete troops.** Content-based parsing pulls in ids defined
   only in `mpcharacters.xml` / `obsolete_characters.xml`. In vanilla this is 135 ids
   (95 soldiers); removing them leaves a clean baseline of **272 soldiers**. Prefer the
   `is_obsolete` XML attribute over filename matching where available.
4. **Keep NavalDLC troops.** They are War Sails content, not test data.

## Known limitations

- `upgrade_requires` is not modelled — upgrade gating is invisible here.
- Unmapped and ignorable: `voice`, `age`, `is_female`, `face_mesh_cache`,
  `banner_symbol_*`, `skill_template`.
- A mod not overriding a vanilla troop does **not** mean that troop still spawns; a total
  conversion can bypass it via party templates without touching its XML.
- Per-track scores are comparable **within** a track only.
