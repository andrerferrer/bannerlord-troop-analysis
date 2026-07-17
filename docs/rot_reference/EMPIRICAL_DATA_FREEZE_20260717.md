# RoT Empirical Data Freeze — 2026-07-17

## Status

The original full-resolution screenshot archive:

```txt
Armoury Crate SE 03_07_2026 13_28_44.zip
```

is no longer available locally or in the active analysis runtime.

The empirical dataset is therefore frozen at the material already normalized and transcribed.

## Preserved data

The following outputs remain available and are sufficient for reproducible analysis of the completed batches:

```txt
20260703_screenshot_manifest.csv
20260703_battle_groups.csv
20260703_empirical_troop_rows_template.csv
20260703_empirical_troop_aggregate_batch1.csv
20260703_empirical_control_aggregate_combined_batch1_2.csv
20260703_model_vs_empirical_delta_controls.csv
20260703_contextual_control_status.csv
20260717_metric_scope_audit.csv
20260717_robust_metric_audit.csv
```

Preserved scope:

```txt
139 manually/vision-assisted troop rows
40 unique troop names
10 represented battle groups
43 rows from verified full-side contexts
66 rows from partial-transcription contexts
```

## What can still be concluded

The preserved data supports cautious conclusions for:

```txt
Goldenheart Warrior
Westerling Hedgeknight
Myrish Artisan of War
Qartheen Longbowman
Riverlands Admiral
Frey Assassin
Ravens' Teeth
Ibbenese Navigator
Lyseni Enforcer
```

Only the verified full-side subset may use:

```txt
kill share
deployed share
contribution index
campaign contribution
```

Partial-transcription rows may use direct row metrics such as:

```txt
kills per present
death rate
wounded rate
casualty rate
```

## What is no longer recoverable from this upload

Without the original full-resolution images, the remaining untranscribed scoreboard rows cannot be recovered reliably.

The contact sheets are useful for screenshot classification but do not preserve enough text resolution for safe troop-row transcription.

## Analysis policy

Until new empirical screenshots are collected:

1. V4.3 remains the current theoretical model.
2. Robust empirical adjustments remain small and capped.
3. Ravens' Teeth remains a protected calibration anchor.
4. Goldenheart Warrior remains the strongest clean empirical confirmation.
5. Ibbenese Navigator remains flagged as possible theoretical overrank, not definitively downgraded.
6. Castellan package rankings remain theory-led with limited empirical overlays.
7. No additional claims should be attributed to the lost screenshots.

## Future capture policy

Use:

```txt
scripts/rot/archive_bannerlord_captures.ps1
```

The script creates dated ZIP archives and manifests from Bannerlord/Armoury Crate screenshots and videos before local cleanup.
