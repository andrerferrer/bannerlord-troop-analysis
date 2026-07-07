# RoT Empirical Transcription Batch 2 — 2026-07-03

This is the second manual/vision-assisted transcription batch from the 2026-07-03 screenshot upload.

## Scope

Transcribed selected visible rows from six additional battle groups:

```txt
rot_empirical_20260703_009
rot_empirical_20260703_014
rot_empirical_20260703_015
rot_empirical_20260703_016
rot_empirical_20260703_017
rot_empirical_20260703_018
```

Batch 2 rows: **86**  
Batch 2 unique troops: **28**

Combined batch 1 + 2 rows: **139**  
Combined unique troops: **40**

## Notes

This is a prioritized transcription pass, not full completion of every screenshot.

Some casualty columns are marked with `medium` or `low` confidence where column placement was partially ambiguous. Use high-confidence rows first when calibrating.

## Main combined control results

| Troop | Samples | Kills | Present | K/P | Median CI | Campaign CI |
|---|---:|---:|---:|---:|---:|---:|
| Frey Assassin | 6 | 217 | 49 | 4.429 | 1.376 | 1.358 |
| Goldenheart Warrior | 9 | 428 | 161 | 2.658 | 1.611 | 1.322 |
| Westerling Hedgeknight | 5 | 87 | 40 | 2.175 | 1.450 | 1.300 |
| Qartheen Longbowman | 6 | 96 | 48 | 2.000 | 1.379 | 1.206 |
| Myrish Artisan of War | 9 | 194 | 112 | 1.732 | 0.967 | 0.967 |
| Sarnori Spider | 5 | 58 | 52 | 1.115 | 0.837 | 0.837 |
| Ravens' Teeth | 6 | 136 | 79 | 1.722 | 0.725 | 0.715 |
| Riverlands Admiral | 6 | 132 | 56 | 2.357 | 0.861 | 0.715 |
| Dragonstone Elite Halberdier | 6 | 243 | 107 | 2.271 | 0.907 | 0.705 |
| Grafton Flaming Knight | 3 | 22 | 40 | 0.550 | 0.777 | 0.683 |
| Mallister Eagle Knight | 4 | 28 | 18 | 1.556 | 0.607 | 0.541 |
| Ibbenese Navigator | 3 | 10 | 15 | 0.667 | 0.355 | 0.355 |
| Lyseni Enforcer | 9 | 342 | 178 | 1.921 | 0.387 | 0.279 |

## Important interpretation

### Goldenheart Warrior

Still the cleanest high-confidence carry signal.

It now has 9 sampled rows:

```txt
total_kills = 428
total_present = 161
overall_kills_per_present = 2.658
median_contribution_index = 1.611
median_campaign_contribution = 1.322
```

### Ravens' Teeth

Ravens now has 6 rows:

```txt
total_kills = 136
total_present = 79
overall_kills_per_present = 1.722
```

The contribution index is lower than expected, likely because Ravens is being compared in mixed contexts and sometimes appears in larger/high-share groups. Do not downgrade Ravens yet without context segmentation.

### Frey Assassin

Frey Assassin spiked hard in one battle:

```txt
total_kills = 217
total_present = 49
overall_kills_per_present = 4.429
```

This is a major empirical signal, but it needs more context before model recalibration. It may indicate that Frey is better than the theory ranking suggests.

### Westerling Hedgeknight

Continues to look strong:

```txt
total_kills = 87
total_present = 40
overall_kills_per_present = 2.175
median_campaign_contribution = 1.300
```

Confirmed as a serious Castellan candidate.

### Ibbenese Navigator

Navigator still looks weaker empirically than V4.1 predicted:

```txt
total_kills = 10
total_present = 15
overall_kills_per_present = 0.667
median_campaign_contribution = 0.355
```

This supports caution: Navigator may be a model overrank or context-dependent melee unit.

### Lyseni Enforcer

Lyseni has high total kills but lower contribution index:

```txt
total_kills = 342
total_present = 178
overall_kills_per_present = 1.921
median_campaign_contribution = 0.279
```

Likely affected by large deployed share / garrison context. Requires context segmentation before downgrading.

## Next step

Continue transcription, but now prioritize:

```txt
Frey Assassin
Ravens' Teeth
Goldenheart Warrior
Ibbenese Navigator
Lyseni Enforcer
Celtigar Banneret
Mallister House Guard
Mallister Eagle Knight
Grafton Flaming Knight
Westerling Hedgeknight
```

The immediate analytical task is to join this empirical aggregate against V4.1 and generate `model_vs_empirical_delta`.
