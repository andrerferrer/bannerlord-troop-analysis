# Conservative Scoring v0

## Purpose

This scoring layer is intentionally conservative.

It exists to reintroduce scoring after the failed aggressive HTK/CraftedItem attempt, without pretending that crafted weapon final stats are known.

## Rules

### 1. Defensive score first

Defense uses only values directly available from XML:

```txt
armor
shield HP
shield armor
horse stats
horse harness armor
```

No inferred combat damage is used for defense.

### 2. Ranged score uses direct XML stats only

Bow and crossbow scoring uses direct `Item` stats:

```txt
damage
ammo damage bonus
speed_rating
accuracy
missile_speed
stack_amount
```

This means ranged scoring is more reliable than crafted melee scoring at this stage.

### 3. Crafted melee uses conservative proxy only

Most vanilla melee weapons used by troops are `CraftedItem` entries.

These are linked to troops, but final damage/speed is not reconstructed yet.

For now:

```txt
crafted_stats_reconstructed = FALSE
score_usage_status = conservative_proxy_no_htk
```

The proxy is compressed and capped by template type.

### 4. HTK/KPM remains disabled for CraftedItem

Do not use HTK/KPM for crafted weapons until final stats are reconstructed or externally dumped.

## Status

This is not a final ranking model.

Use `vanilla_sanity_scores_v0_conservative.csv` only as a control table.

Known limitation:

```txt
Fian Champion and Khan's Guard are likely undervalued because ranged tactical value is still under-modeled.
```

## Next step

The next scoring iteration should be role-specific:

```txt
Archer score
Crossbow score
Horse Archer score
Defensive Infantry score
Offensive Infantry score
Defensive Cavalry score
Offensive Cavalry score
```

Only after that should global ranking be reintroduced.
