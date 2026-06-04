# Vanilla XML Import Summary

## Export inspection

The uploaded vanilla XML export was inspected and successfully parsed.

| Metric | Value |
|---|---:|
| Total files | 4124 |
| XML files | 3482 |

## Relevant files found

Primary troop file:

```txt
SandboxCore/ModuleData/spnpccharacters.xml
```

Relevant supporting files detected:

```txt
Native/ModuleData/crafting_pieces.xml
Native/ModuleData/item_modifiers.xml
Native/ModuleData/skins.xml
Native/ModuleData/monsters.xml
Sandbox/ModuleData/monsters.xml
SandboxCore/ModuleData/spcultures.xml
```

## Initial troop extraction

The first parsing pass extracted `NPCCharacter` records from:

```txt
SandboxCore/ModuleData/spnpccharacters.xml
```

Initial counts:

| Metric | Value |
|---|---:|
| NPCCharacter records | 548 |
| Soldier records | 186 |
| Combat soldier records with level | 180 |

## Level to tier mapping

Working approximation:

| Level | Tier estimate |
|---:|---:|
| 6 | 2 |
| 11 | 3 |
| 16 | 4 |
| 21 | 5 |
| 26 | 6 |
| 31 | special / outlier |

## Generated files

```txt
data/vanilla/normalized/vanilla_troops_raw_extracted.csv
data/vanilla/normalized/vanilla_combat_troops_raw.csv
data/vanilla/normalized/vanilla_combat_troop_level_summary.csv
```

## Next step

Parse equipment and item XMLs so each troop can be linked to:

```txt
weapons
armor
shield
mount
ammo
weapon damage
damage type
weapon speed
weapon reach
missile speed
```

After that, generate:

```txt
HTK dataset
KPM dataset
tier-by-tier rankings
overall rankings
```
