# Five-battle reporting gate decision

## Decision

The empirical reporting threshold is:

```text
minimum independent battles = 5
minimum deployed troops = 20
```

This replaces the earlier exploratory three-battle threshold.

## Rationale

Three battles allow one or two unusual outcomes to dominate a troop estimate. Raising the minimum to five battles reduces the number of estimates driven by extremely small battle samples while preserving enough coverage for exploratory reporting.

The five-battle threshold does not guarantee ranking stability. Every displayed estimate must continue to include:

- independent battle count;
- total deployed troops;
- battle-level bootstrap interval;
- context;
- review/canonicalization status.

## Implementation

The default is implemented in:

```text
scripts/analysis/build_empirical_baseline.py
```

with:

```text
--minimum-battles 5
--minimum-deployed 20
```

## Interpretation

Passing the gate means that an estimate may be displayed as exploratory campaign evidence. It does not establish universal troop superiority, causal attribute effects, or matchup performance.
