# RoT Empirical Context Segmentation — 2026-07-03

This package segments empirical transcription batches 1+2 before changing the V4.1 formula.

## Input

```txt
empirical_troop_rows_transcribed_combined_batch1_2.csv
rot_hot_v41_all_humanoid_ranked.csv
```

## Why segmentation was needed

The first model-vs-empirical delta mixed:

```txt
player party troops
heroes / companions
garrison rows
militia rows
tiny 1-unit stacks
medium/low confidence rows
```

That can make contribution index misleading, especially for Ravens' Teeth, Lyseni Enforcer, and large deployed-share blocks.

## Segment labels added

Each row now has:

```txt
context_class
sample_quality_class
deployed_share_bucket
is_clean_troop_sample
is_hero_or_companion
is_garrison_party
is_militia_troop
```

## Clean sample definition

```txt
clean_player_party_troop =
not hero/companion
not garrison party
not militia troop
transcription confidence high/medium/unknown
party_name contains Kenned's Party
```

## Counts

| Dataset | Rows / troops |
|---|---:|
| segmented row records | 139 |
| clean player-party troop rows | 122 |
| clean aggregate troops | 28 |
| garrison/militia aggregate troops | 5 |
| hero/companion rows | 12 |
| tiny-stack rows | 22 |

## Clean contextual control results

| Troop | Samples | K/P | Campaign CI | Theory | Status |
|---|---:|---:|---:|---:|---|
| Frey Assassin | 6 | 4.43 | 1.36 | 65.11 | empirical_overperformer |
| Goldenheart Warrior | 9 | 2.66 | 1.32 | 88.57 | confirmed_high |
| Westerling Hedgeknight | 4 | 2.53 | 1.38 | 100.00 | confirmed_high |
| Qartheen Longbowman | 6 | 2.00 | 1.21 | 59.21 | empirical_overperformer |
| Myrish Artisan of War | 9 | 1.73 | 0.97 | 76.64 | solid_empirical |
| Riverlands Admiral | 6 | 2.36 | 0.71 | 83.49 | context_dependent_or_underperforming |
| Sarnori Spider | 5 | 1.12 | 0.84 | 58.90 | roughly_aligned_or_unclear |
| Ravens' Teeth | 6 | 1.72 | 0.72 | 98.11 | context_dependent_or_underperforming |
| Mallister Eagle Knight | 4 | 1.56 | 0.54 | 84.84 | context_dependent_or_underperforming |
| Grafton Flaming Knight | 3 | 0.55 | 0.68 | 95.79 | context_dependent_or_underperforming |
| Ibbenese Navigator | 3 | 0.67 | 0.36 | 91.30 | theory_overrank_candidate |
| Lyseni Enforcer | 8 | 0.69 | 0.25 | 81.23 | theory_overrank_candidate |

## Main interpretation

### Confirmed high

```txt
Goldenheart Warrior
Westerling Hedgeknight
```

Goldenheart remains the cleanest high-confidence result. Westerling continues to look strong, but it is Castellan/special.

### Empirical overperformers

```txt
Frey Assassin
Qartheen Longbowman
```

Frey Assassin is now the most important overperformer candidate. Qartheen Longbowman appears better than V4.1 theory predicted.

### Solid empirical, but below top carry

```txt
Myrish Artisan of War
```

Myrish has enough clean samples to call it solid, but it still sits below Goldenheart in empirical carry value.

### Context-dependent / possible underperformers

```txt
Ravens' Teeth
Riverlands Admiral
Mallister Eagle Knight
Grafton Flaming Knight
```

Do not automatically downgrade these yet. Ravens in particular has tiny-stack rows and still lacks clean Raven-centered battles.

### Theory overrank candidates

```txt
Ibbenese Navigator
Lyseni Enforcer
```

Navigator is now a stronger overrank signal after segmentation. Lyseni remains difficult because some rows likely reflect large-stack / context effects and it was empirically strong in earlier isolated samples.

## Next step

Use the clean contextual status table to produce a V4.2 calibration proposal. Do not fully recalibrate until more Raven-centered and Celtigar-centered samples are available.
