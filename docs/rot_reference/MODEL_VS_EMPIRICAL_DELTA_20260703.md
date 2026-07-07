# RoT Model vs Empirical Delta — Batch 1+2

This report joins V4.1 theory against empirical transcription batches 1 and 2.

## Scope

| Metric | Value |
|---|---:|
| Empirical aggregate rows | 33 |
| Matched to V4.1 theory | 26 |
| Unmatched | 7 |
| Battle groups represented | 10 |

## Empirical score method

The first empirical score combines:

```txt
55% median campaign contribution
25% overall kills per present
20% median contribution index
```

This is not final truth. It is a first normalized comparison layer to find candidates for model calibration.

## Top empirical matched rows

| Troop | Samples | K/P | Campaign CI | Empirical | Theory | Status |
|---|---:|---:|---:|---:|---:|---|
| Frey Assassin | 6 | 4.43 | 1.36 | 100.00 | 65.11 | empirical_overperformer |
| Goldenheart Warrior | 9 | 2.66 | 1.32 | 89.44 | 88.57 | confirmed_high |
| Westerling Hedgeknight | 5 | 2.18 | 1.30 | 82.06 | 100.00 | confirmed_high |
| Riverlands Axeman | 1 | 1.00 | 1.45 | 80.78 | 54.24 | insufficient_data |
| Qartheen Longbowman | 6 | 2.00 | 1.21 | 74.99 | 59.21 | mild_empirical_overperformer |
| Westerling Knight | 1 | 0.75 | 1.09 | 55.14 | 73.20 | insufficient_data |
| Myrish Artisan of War | 9 | 1.73 | 0.97 | 54.35 | 76.64 | mild_empirical_underperformer |
| Stormlands Heavy Crossbowman | 1 | 0.67 | 0.97 | 46.59 | 45.43 | insufficient_data |
| Riverlands Admiral | 6 | 2.36 | 0.71 | 44.87 | 83.49 | theory_overrank_or_bad_context |
| Dragonstone Elite Halberdier | 6 | 2.27 | 0.70 | 44.55 | 58.08 | roughly_aligned |
| Volantene Mahout | 1 | 2.00 | 0.74 | 43.98 | 70.56 | insufficient_data |
| Sarnori Spider | 5 | 1.12 | 0.84 | 41.36 | 58.90 | mild_empirical_underperformer |

## Key findings

### Goldenheart Warrior is confirmed high

Goldenheart is the cleanest high-confidence result so far.

```txt
samples = 9
total_kills = 428
total_present = 161
overall_kills_per_present = 2.66
median_campaign_contribution = 1.32
```

The empirical score and V4.1 theory score are almost aligned:

```txt
empirical = 89.44
theory = 88.57
```

### Frey Assassin is a major overperformer candidate

```txt
samples = 6
total_kills = 217
total_present = 49
overall_kills_per_present = 4.43
```

Theory is much lower than empirical:

```txt
empirical = 100.00
theory = 65.11
delta = +34.89
```

This may indicate Frey Assassin is under-modeled, but context review is required because one strong battle can distort totals.

### Qartheen Longbowman is overperforming relative to theory

```txt
empirical = 74.99
theory = 59.21
delta = +15.78
```

The qarth longbow appears to matter in campaign results.

### Myrish is strong but below Goldenheart empirically

```txt
samples = 9
total_kills = 194
total_present = 112
overall_kills_per_present = 1.73
median_campaign_contribution = 0.97
```

This supports the V4.1 correction that Myrish should not be ranked above Goldenheart in general carry value.

### Ravens' Teeth currently looks underperforming in this partial dataset

```txt
samples = 6
total_kills = 136
total_present = 79
empirical = 37.92
theory = 98.11
```

This should not trigger immediate re-ranking. Likely causes:

```txt
bad contexts
large deployed-share distortion
late-battle or reinforcement timing
partial transcription
insufficient clean Raven-centered battles
```

Ravens remains a calibration anchor until clean samples say otherwise.

### Ibbenese Navigator looks overranked by theory

Navigator has low empirical contribution in batch 1+2:

```txt
samples = 3
total_kills = 10
total_present = 15
median_campaign_contribution = 0.36
```

This supports the earlier reclassification: it is not a top skirmisher. It may also be a melee/defensive overrank in V4.1.

## Current statuses

### Confirmed high

```txt
Goldenheart Warrior
Westerling Hedgeknight
```

### Empirical overperformer

```txt
Frey Assassin
```

### Mild empirical overperformer

```txt
Qartheen Longbowman
```

### Theory overrank or bad context candidates

```txt
Ravens' Teeth
Riverlands Admiral
Grafton Flaming Knight
Mallister Eagle Knight
Black Goat Sacrificer
```

Do not automatically downgrade these until context segmentation is complete.

## Unmatched empirical rows

| Troop | Samples | Kills | Present | K/P | Campaign CI |
|---|---:|---:|---:|---:|---:|
| Westerlands Skirmisher | 1 | 6 | 4 | 1.50 | 2.18 |
| Lyseni Axeman | 1 | 3 | 2 | 1.50 | 1.61 |
| Lyseni Executioner | 1 | 4 | 3 | 1.33 | 1.44 |
| Sarnori Elite Javelinier | 1 | 6 | 6 | 1.00 | 1.08 |
| Qartheen Pureborn Warrior | 1 | 1 | 1 | 1.00 | 1.07 |
| Ibbenese Rower | 1 | 4 | 4 | 1.00 | 0.98 |
| Gallant Sword Sister | 3 | 25 | 13 | 1.92 | 0.48 |

## Next step

Segment empirical rows by:

```txt
party vs garrison
field vs siege
main army vs reinforcement
high-confidence vs medium/low transcription
```

Then rerun model-vs-empirical delta.
