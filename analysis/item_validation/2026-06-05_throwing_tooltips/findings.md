# Item Tooltip Validation — Throwing Weapons — 2026-06-05

## Scope

Manual validation of user-provided in-game encyclopedia/tooltips for throwing weapons relevant to v7.2 `burst_score_v72`.

This batch focuses on item inputs only:

```txt
item name
throwing damage
damage type
weapon length
missile speed
accuracy
stack amount
visible stack count
```

It does not directly validate battle output.

## Main result

The most important v7.2 ammo assumptions are confirmed:

| Troop | Tooltip item | Stack amount | Visible stacks | Inferred ammo | v7.2 model ammo | Result |
|---|---|---:|---:|---:|---:|---|
| Imperial Naute | Hooked Javelin | 5 | 2 | 10 | 10 | confirmed |
| Battanian Skipari | Hooked Javelin | 5 | 2 | 10 | 10 | confirmed |
| Battanian River Raider | Broad Blade Javelin | 5 | 2 | 10 | 10 | confirmed |
| Imperial Coast Guard | Harpoon | 5 | 2 | 10 | 10 | ammo confirmed, item name corrected |
| Aserai Vanguard Faris | Jereed | assumed 5 | 1 | 5 | 5 | consistent |

## Key corrections

### Imperial Coast Guard item mismatch

The model currently labels the Coast Guard throwing item as:

```txt
Broad Blade Javelin
```

The tooltip shows:

```txt
Harpoon
Damage: 113 Pierce
Weapon Length: 83
Missile Speed: 28
Accuracy: 92
Stack Amount: 5
Visible stacks: 2
Total ammo inferred: 10
```

Action:

```txt
Replace Imperial Coast Guard primary_throw_name with Harpoon in the next model build.
```

The current v7.2 burst score is probably not inflated by ammo; if anything, the Coast Guard's item damage proxy is conservative.

### Tooltip damage is much higher than proxy damage

The v7/v7.2 model still stores crafted/proxy throw damage values such as:

```txt
Hooked Javelin proxy: 45.2
Broad Blade Javelin proxy: 48.0
Jereed proxy: 54.4
```

The in-game tooltips show:

```txt
Hooked Javelin: 117 Pierce
Broad Blade Javelin: 101 Pierce
Harpoon: 113 Pierce
Jereed: 121 Pierce
```

This does not automatically mean we should replace the HTK model damage 1:1, because Bannerlord tooltip damage already includes game-side weapon stat presentation and may not map directly to the model's post-armor proxy.

But it does mean the model should track a separate field:

```txt
tooltip_throw_damage
```

and stop treating crafted proxy damage as if it were validated raw item damage.

## Impact on v7.2 burst ranking

### Battanian Skipari

The high v7.2 Skipari ranking is no longer an item-loadout bug.

The tooltip batch supports:

```txt
Battanian Skipari
Hooked Javelin
2 stacks × 5 = 10 javelins
```

Remaining uncertainty:

```txt
Does Skipari empirically output like Imperial Naute/Faris in battle?
```

This is tracked in issue #2.

### Imperial Naute

The Imperial Naute empirical overperformance is supported by item validation:

```txt
Hooked Javelin
2 stacks × 5 = 10 javelins
117 Pierce tooltip damage
```

The v7.2 conclusion remains valid:

```txt
Imperial Naute should be elite in burst_score, not necessarily S-tier in general_score.
```

### Aserai Vanguard Faris

The Faris remains a valid burst benchmark:

```txt
Jereed
121 Pierce tooltip damage
single stack / 5 ammo assumption
mounted throw bonus remains appropriate
```

## Recommended v7.2.1 changes

Do not change `general_score`.

Add item-tooltip fields and update one item name:

```txt
tooltip_throw_damage
tooltip_throw_damage_type
tooltip_throw_stack_amount
tooltip_throw_visible_stacks
tooltip_throw_total_ammo
```

Specific correction:

```txt
Imperial Coast Guard primary_throw_name: Broad Blade Javelin -> Harpoon
```

Do not immediately rescale all throw damage off tooltip values until we decide whether tooltip damage should be used directly or only as a validation/calibration field.
