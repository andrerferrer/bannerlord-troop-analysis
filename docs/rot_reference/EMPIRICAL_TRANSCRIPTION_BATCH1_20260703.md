# RoT Empirical Transcription Batch 1 — 2026-07-03

This is the first manual/vision-assisted transcription batch from the 2026-07-03 screenshot upload.

## Scope

Transcribed selected high-value rows from four battle groups:

```txt
rot_empirical_20260703_005
rot_empirical_20260703_006
rot_empirical_20260703_007
rot_empirical_20260703_008
```

Rows transcribed: **53**

Unique troops: **27**

## Important note

This is not yet the full empirical dataset. It is a prioritized batch focused on visible high-value rows and model-control troops.

## Metrics included

```txt
estimated_present
kills_per_present
death_rate
wounded_rate
casualty_rate
deployed_share
kill_share
contribution_index
campaign_contribution
```

## High-signal observations

### Goldenheart Warrior

Goldenheart appears in four sampled battle groups:

```txt
total_kills = 221
total_present = 64
overall_kills_per_present = 3.453
median_contribution_index = 1.687
median_campaign_contribution = 1.525
```

This supports the prior conclusion that Goldenheart is a top practical carry.

### Myrish Artisan of War

Myrish appears in four sampled battle groups:

```txt
total_kills = 71
total_present = 24
overall_kills_per_present = 2.958
median_contribution_index = 1.229
median_campaign_contribution = 1.229
```

Strong, but below Goldenheart in the first batch.

### Westerling Hedgeknight

Westerling Hedgeknight appears in two sampled battle groups:

```txt
total_kills = 61
total_present = 19
overall_kills_per_present = 3.211
median_contribution_index = 1.481
median_campaign_contribution = 1.375
```

Promising, but needs more samples and confirmation as Castellan/special.

### Ravens' Teeth

Ravens appears in this batch only once, with a tiny stack:

```txt
total_kills = 2
total_present = 1
```

This row is not enough to validate or refute Ravens. Keep Ravens as theoretical/observed control from prior analysis.

### Lyseni Enforcer

Lyseni Enforcer appears in four rows but with mixed party contexts:

```txt
total_kills = 291
total_present = 97
overall_kills_per_present = 3.0
median_contribution_index = 0.462
median_campaign_contribution = 0.249
```

The very large Sunstone garrison stack had high kills but also enough deployed share/casualties to suppress contribution index. Needs context-aware aggregation.

## Top aggregate rows by median campaign contribution

| Troop | Samples | Total kills | Total present | K/P | Median CI | Campaign CI |
|---|---:|---:|---:|---:|---:|---:|
| Goldenheart Warrior | 4 | 221 | 64 | 3.453 | 1.687 | 1.525 |
| Westerling Hedgeknight | 2 | 61 | 19 | 3.211 | 1.481 | 1.375 |
| Myrish Artisan of War | 4 | 71 | 24 | 2.958 | 1.229 | 1.229 |
| Qartheen Longbowman | 3 | 61 | 24 | 2.542 | 1.249 | 1.194 |
| Dragonstone Elite Halberdier | 4 | 230 | 84 | 2.738 | 1.128 | 0.828 |
| Ravens' Teeth | 1 | 2 | 1 | 2.000 | 0.581 | 0.581 |
| Riverlands Admiral | 4 | 67 | 38 | 1.763 | 0.613 | 0.489 |
| Lyseni Enforcer | 4 | 291 | 97 | 3.000 | 0.462 | 0.249 |

Some one-off hero rows had very high contribution but are not useful for troop ranking and should be filtered or treated separately.

## Next step

Continue transcribing remaining scoreboards, then join against the V4.1 theoretical ranking.
