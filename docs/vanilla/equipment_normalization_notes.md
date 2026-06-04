# Vanilla Equipment Normalization Notes

## Status

The first troop extraction pass worked, but equipment required a second pass because vanilla troops do not store all equipment in a single flat structure.

## XML structure

Troop equipment appears under:

```txt
NPCCharacter
└─ Equipments
   ├─ EquipmentRoster
   │  ├─ equipment slot="Item0"
   │  ├─ equipment slot="Item1"
   │  ├─ equipment slot="Body"
   │  └─ ...
   ├─ EquipmentRoster
   ├─ EquipmentRoster
   ├─ EquipmentSet equipmentType="Civilian"
   ├─ equipment slot="Horse"
   └─ equipment slot="HorseHarness"
```

Important detail:

```txt
Horse and HorseHarness can appear directly under Equipments, outside EquipmentRoster.
```

Those common equipment entries should be applied to every combat roster for that troop.

## Item types

Normal items are defined as:

```xml
<Item id="...">
```

Many troop weapons are defined as:

```xml
<CraftedItem id="...">
```

So item parsing must handle both.

## CraftedItem limitation

`CraftedItem` entries do not expose final in-game damage/speed as simple XML attributes.

For now, the pipeline uses proxy stats derived from:

```txt
crafting_template
blade tier
piece tier
piece length
piece weight
```

This is good enough for pipeline validation but should not be treated as final scoring truth.

## Current known limitation

The preliminary rankings overvalue some crafted melee/polearm weapons because crafted weapon damage is inferred, not engine-calculated.

Before final vanilla rankings, we need either:

1. a better crafted weapon stat reconstruction, or
2. an in-game/exported item stat dump, or
3. empirical calibration against known troop tests.

## Fixed issues

### Equipment rosters

The parser now supports multiple `EquipmentRoster` variants per troop.

### Horses

Horse and harness equipment are now applied to mounted troops correctly.

### Ammo

Arrows and bolts store ammo count in:

```txt
stack_amount
```

not `ammo_limit`.

### Crafted weapons

Crafted weapons are now parsed and linked to troops.

## Useful control cases

The following cases are useful for sanity checks:

```txt
Battanian Fian Champion
Khuzait Khan's Guard
Aserai Vanguard Faris
Imperial Legionary
Vlandian Sergeant
Vlandian Sharpshooter
Sturgian Heavy Axeman
```

Expected parser behavior:

```txt
Fian Champion         -> bow + 2H fallback
Khan's Guard         -> horse + bow + glaive
Vanguard Faris       -> horse + lance + throwing
Legionary            -> shield + armor + 1H/throwing spear setup
Vlandian Sharpshooter -> crossbow + shield
```
