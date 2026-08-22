# Provisional empirical combat criteria: offense and defense

## Status

Operator-approved provisional methodology as of 2026-08-22. This document
replaces the earlier role-percentile and 2:1 blended-score proposal that
previously occupied this path.

The current goal is deliberately modest: use very simple scoreboard-backed
measures that approximate battlefield reality, keep their meanings visible, and
avoid pretending that one formula can already compare every combat role.

No frozen model changes are authorized by this document. The third general
criterion remains undecided.

## Current decision

Keep the criteria independent. Do not average, multiply, percentile-normalize,
or weight offense and defense into one score.

```text
1. Offensive criterion
   kills / deployed

2. Defensive criterion
   a. frontline retention
   b. pressure margin

3. Third criterion
   unresolved
```

Kill share, deployment share, death rate, backline retention, and other values
may remain useful diagnostics. They are not substitutes for the two accepted
defensive components and do not currently determine a tier.

## 1. Offensive criterion

```text
offensive_efficiency = kills / deployed
```

This answers one narrow question:

> How many enemy kills did each deployed unit produce?

Ranged troops may dominate this criterion because they can attack with less
exposure. That is not corrected inside the offensive formula; the defensive
criterion exists to capture a different dimension.

Continue to keep track, battle context, player/enemy side, and the existing
5-independent-battle / 20-deployed display gate separate.

## 2. Defensive criterion

The defensive criterion has two separately published components. Neither is a
weighted input to the other.

### 2.1 Frontline retention

```text
frontline_retention = frontline_survivors / frontline_deployed
```

Under the combat-observation schema:

```text
deployed = survivors + deaths + wounded
```

`routed` remains separate. Dead and wounded are both unavailable at the end of
the observation, so neither counts as retained.

Frontline retention answers:

> How much of the tested frontline remained operational at the end?

This distinguishes a costly victory using disposable recruits from a cleaner
victory using stronger infantry, even when both battles end in a win.

Retention is still a proxy. High retention can result from strength, favorable
targeting, low exposure, late contact, or an easy matchup. For that reason,
ranged support may have retention recorded as a diagnostic, but it does not
compete as the tested defensive frontline.

### 2.2 Pressure margin

```text
allied_retention = allied_remaining / allied_deployed
enemy_retention  = enemy_remaining / enemy_deployed

pressure_margin = allied_retention - enemy_retention
```

For a symmetric 100-versus-100 test:

```text
pressure_margin = (allied_remaining - enemy_remaining) / 100
```

Pressure margin answers:

> How favorable was the final battlefield state, including close defeats and
> costly victories?

Interpretation:

- large positive value: decisive favorable result;
- small positive value: narrow or costly victory;
- near zero: battle decided at the limit;
- small negative value: close defeat;
- large negative value: heavy defeat.

This preserves information that a binary win/loss indicator discards. Losing
with three enemies remaining is correctly treated as very different from losing
with twenty-five enemies remaining.

Only a final result with direct positive side deployment totals and final
remaining counts receives a production pressure margin. An active,
interrupted, or otherwise right-censored scoreboard may retain a diagnostic
snapshot, but it must not be ranked as a final pressure margin.

## Controlled infantry exercise

The simplest intended benchmark is:

```text
50 tested infantry
+ 50 fixed archers
versus
100 fixed opponents
```

Only the tested frontline changes between candidates. Orders, support, opponent
composition, track, version, and battle context remain fixed as far as the test
setup allows.

### Example: recruit frontline

```text
frontline survivors = 0 / 50
allied remaining     = 40 / 100
enemy remaining      = 0 / 100

frontline retention = 0%
pressure margin      = 40% - 0% = +40 percentage points
```

The army wins, but spends its entire frontline.

### Example: stronger frontline

```text
frontline survivors = 35 / 50
allied remaining     = 82 / 100
enemy remaining      = 0 / 100

frontline retention = 35 / 50 = 70%
pressure margin      = 82% - 0% = +82 percentage points
```

Both armies win, but the stronger frontline preserves far more combat power and
produces a much better final battlefield state.

### Defeats remain informative

```text
heavy defeat:
0 / 100 allied remaining - 25 / 100 enemy remaining = -25 pp

close defeat:
0 / 100 allied remaining - 3 / 100 enemy remaining = -3 pp
```

The criterion therefore does not discard pressure tests simply because the
candidate loses.

## Reading the two defensive components together

| Frontline retention | Pressure margin | Interpretation |
|---|---|---|
| high | high | frontline survives and the formation dominates |
| low | high | sacrificial frontline that still enables a strong result |
| high | low or negative | durable unit that does not convert durability into formation success |
| low | strongly negative | defensive collapse |

Do not collapse these cases into one weighted number yet.

## Optional diagnostics

The following may be published beside the criterion without becoming additional
criteria:

```text
backline_retention = backline_survivors / backline_deployed
death_rate         = deaths / deployed
casualty_rate      = (deaths + wounded) / deployed
```

Backline retention can help explain whether the frontline protected the fixed
archers. Death rate distinguishes permanent campaign losses from wounded troops.
Neither receives a provisional weight.

## Campaign evidence boundary

Ordinary campaign battles may publish frontline retention and side-level
pressure margin when the necessary rows and totals are directly visible.
However, mixed campaign evidence does not isolate causality: army composition,
opponents, terrain, tactics, and exposure vary.

Use the controlled 50-infantry / 50-archer exercise for direct defensive
frontline comparisons. Campaign values remain descriptive evidence and must not
be presented as if only the tested infantry caused the side-level margin.

## Explicitly rejected for now

Do not implement any of the following as the current rule:

- defensive swing based only on win-rate differences;
- survivors/deployed as the sole defensive verdict;
- kill share or share-adjusted impact as defensive credit;
- a universal offense-plus-defense score;
- role-percentile blending with 2:1 weights;
- inferred support kills transferred from ranged troops to the frontline;
- a cavalry-specific criterion before the infantry defense criterion is settled.

## Publication contract

When the defensive inputs exist, publish at minimum:

```text
frontline_deployed
frontline_survivors
frontline_retention
allied_deployed
allied_remaining
enemy_deployed
enemy_remaining
allied_retention
enemy_retention
pressure_margin
result_state
```

Keep `offensive_efficiency` separate. Preserve raw numerators and denominators so
every percentage remains auditable.

The next methodology task is to validate these two defensive outputs against a
small set of intuitive infantry anchors. Do not define the third general
criterion until that check is complete.
