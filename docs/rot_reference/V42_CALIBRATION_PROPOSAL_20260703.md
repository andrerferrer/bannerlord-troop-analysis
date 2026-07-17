# RoT V4.2 Calibration Proposal — 2026-07-03

This report applies a cautious empirical calibration layer to V4.1 after context segmentation.

V4.2 is **not** a full formula rewrite. It is a proposal layer used to decide which units need more validation and where V4.1 is too high or too low.

## Inputs

```txt
rot_hot_v41_all_humanoid_ranked.csv
contextual_control_status.csv
```

## Formula

```txt
total_v42_raw =
total_v41_integrated
+ capped_empirical_adjustment
```

Then scores are normalized to 100.

## Adjustment rules

- Ravens' Teeth is protected as a calibration anchor because current empirical samples are not Raven-centered clean samples.
- Goldenheart Warrior receives a small confirmation boost.
- Frey Assassin and Qartheen Longbowman receive empirical boosts.
- Ibbenese Navigator receives a heavy cut because it is new and empirically weak so far.
- Lyseni Enforcer receives a soft cut because prior evidence and current contexts are mixed.
- New/special troops with weak empirical performance receive caution cuts.
- Unobserved troops remain at V4.1.

## V4.2 Top 20 overall

| # | Troop | V4.2 | V4.1 | Adj | Empirical status | Samples |
|---:|---|---:|---:|---:|---|---:|
| 1 | Ravens' Teeth | 100.00 | 98.11 | 0.00 | context dependent | 6 |
| 2 | Westerling Hedgeknight | 97.85 | 100.00 | -4.00 | confirmed high | 4 |
| 3 | Grafton Flaming Knight | 97.64 | 95.79 | 0.00 | context dependent | 3 |
| 4 | Stark Sworn Sword | 93.57 | 91.80 | 0.00 | unobserved | 0 |
| 5 | Goldenheart Warrior | 92.83 | 88.57 | +2.50 | confirmed high | 9 |
| 6 | Tarly Vanguard | 88.76 | 87.08 | 0.00 | unobserved | 0 |
| 7 | Baratheon Hammerknight | 87.50 | 85.85 | 0.00 | unobserved | 0 |
| 8 | Mallister Eagle Knight | 86.48 | 84.84 | 0.00 | context dependent | 4 |
| 9 | Riverlands Admiral | 85.10 | 83.49 | 0.00 | context dependent | 6 |
| 10 | Norvoshi Grand Bearded Priest | 82.04 | 80.49 | 0.00 | unobserved | 0 |
| 11 | Harlaw Captain | 81.68 | 80.14 | 0.00 | unobserved | 0 |
| 12 | Tarth Master Halberdier | 81.59 | 80.05 | 0.00 | unobserved | 0 |
| 13 | Ibbenese Whaler | 81.00 | 79.46 | 0.00 | unobserved | 0 |
| 14 | Frey Assassin | 80.64 | 65.11 | +14.00 | empirical overperformer | 6 |
| 15 | Qartheen Elite Hoplite | 80.39 | 78.87 | 0.00 | unobserved | 0 |
| 16 | Mallister House Guard | 79.39 | 77.89 | 0.00 | unobserved | 0 |
| 17 | Myrish Artisan of War | 78.12 | 76.64 | 0.00 | solid empirical | 9 |
| 18 | Tyroshi Corsair | 77.94 | 76.47 | 0.00 | unobserved | 0 |
| 19 | Freefolk Thenn Impaler | 76.75 | 75.30 | 0.00 | unobserved | 0 |
| 20 | Mountain's Man | 76.48 | 75.03 | 0.00 | unobserved | 0 |

## Top likely-campaign ranking

Excludes militia, manual Castellan, and possible special-access troops.

| # | Troop | V4.2 | V4.1 | Adj | Empirical status | Samples |
|---:|---|---:|---:|---:|---|---:|
| 1 | Goldenheart Warrior | 92.83 | 88.57 | +2.50 | confirmed high | 9 |
| 2 | Ibbenese Whaler | 81.00 | 79.46 | 0.00 | unobserved | 0 |
| 3 | Qartheen Elite Hoplite | 80.39 | 78.87 | 0.00 | unobserved | 0 |
| 4 | Myrish Artisan of War | 78.12 | 76.64 | 0.00 | solid empirical | 9 |
| 5 | Tyroshi Corsair | 77.94 | 76.47 | 0.00 | unobserved | 0 |
| 6 | Freefolk Thenn Impaler | 76.75 | 75.30 | 0.00 | unobserved | 0 |
| 7 | Lyseni Enforcer | 74.65 | 81.23 | -8.00 | theory overrank candidate | 8 |
| 8 | Qartheen Longbowman | 74.63 | 59.21 | +14.00 | empirical overperformer | 6 |
| 9 | Ibbenese Horseman | 74.62 | 73.21 | 0.00 | unobserved | 0 |
| 10 | Qartheen Master Cameleer | 74.54 | 73.13 | 0.00 | unobserved | 0 |
| 11 | Greyjoy Finger Dancer | 74.33 | 72.93 | 0.00 | unobserved | 0 |
| 12 | Qohorik Falxman | 74.33 | 72.92 | 0.00 | unobserved | 0 |
| 13 | Black Goat Sacrificer | 73.67 | 72.27 | 0.00 | unobserved | 0 |
| 14 | Royce Heroine | 73.46 | 72.07 | 0.00 | unobserved | 0 |
| 15 | Ibbenese Navigator | 72.67 | 91.30 | -20.00 | theory overrank candidate | 3 |

## Main changes from V4.1

### Goldenheart Warrior

Confirmed high. Slightly boosted.

```txt
V4.1 = 88.57
V4.2 = 92.83
```

### Frey Assassin

Major empirical overperformer.

```txt
V4.1 = 65.11
V4.2 = 80.64
```

This is a capped boost, not a full rewrite. Frey needs more targeted testing.

### Qartheen Longbowman

Empirical overperformer.

```txt
V4.1 = 59.21
V4.2 = 74.63
```

### Ibbenese Navigator

Major theory overrank candidate.

```txt
V4.1 = 91.30
V4.2 = 72.67
```

This reflects the empirical result and the earlier finding that the javelin is weak.

### Lyseni Enforcer

Soft cut only.

```txt
V4.1 = 81.23
V4.2 = 74.65
```

This is not a definitive downgrade because prior evidence and context are mixed.

## Interpretation

V4.2 should be used as a **testing priority layer**.

Confirmed / stronger confidence:

```txt
Goldenheart Warrior
Westerling Hedgeknight
Frey Assassin
Qartheen Longbowman
Myrish Artisan of War
```

Needs clean targeted validation:

```txt
Ravens' Teeth
Lyseni Enforcer
Ibbenese Navigator
Grafton Flaming Knight
Mallister Eagle Knight
Riverlands Admiral
```

## Next step

Do not rewrite the core model yet. Continue transcribing remaining screenshots and gather cleaner battle samples for:

```txt
Ravens' Teeth
Frey Assassin
Qartheen Longbowman
Ibbenese Navigator
Lyseni Enforcer
Celtigar Banneret
```