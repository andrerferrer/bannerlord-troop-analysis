# Phase 0 baseline audit — combat screenshots 2026-07-23

## Authoritative status

The exact source screenshot ZIP and normalized archive have been recovered and verified. The high-impact P0 review has been completed against the original screenshots.

```text
Screenshot ZIP SHA-256:
00f83754687fe769fdfdea1bda0b68b4d7801c25195ff803aa1a1b35fa15d69f

Normalized archive SHA-256:
10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa
```

For full execution details, see [`PHASE0_EXECUTION_REPORT.md`](PHASE0_EXECUTION_REPORT.md).

## Required analytical split

Captured result screens are victories. Pooling the player side with the defeated enemy side creates outcome bias. Primary campaign-performance rankings therefore use only rows where:

```text
side == player_side
```

Enemy rows remain available for separate matchup and defeat-side analyses.

## Strict baseline population

A strict row must be:

- an included troop row;
- on the player side;
- in a known battle context;
- free of unresolved core-field review flags;
- complete for survivors, kills, deaths, wounded, routed, and deployed;
- positive for deployed;
- free of the suspected siege-engine-outlier flag.

Repeated records are consolidated by battle × context × troop before aggregation.

After P0 review and safe alias consolidation:

| Measure | Count |
|---|---:|
| Source primary occurrences | 1,213 |
| Strict player-side occurrences | 456 |
| Independent battles | 40 |
| Provisional troop identifiers | 190 |
| Remaining reviewed/unresolved rows | 581 |
| Remaining P0 rows | 0 |
| Remaining P1 rows | 94 |
| Remaining P2 rows | 487 |

## Display gate

A troop/context result is displayed only with at least:

```text
5 independent battles
20 deployed troops
```

Current eligibility:

| Context | Eligible labels |
|---|---:|
| Overall | 23 |
| Field | 17 |
| Siege attack | 2 |
| Siege defense | 0 |

Five battles is a minimum reporting threshold, not a stability guarantee.

## Metrics

```text
kills_per_deployed = sum(kills) / sum(deployed)
death_rate         = sum(deaths) / sum(deployed)
casualty_rate      = sum(deaths + wounded) / sum(deployed)
```

Uncertainty intervals are produced by resampling consolidated battle-level troop rows.

## Review outcome

| P0 result | Rows |
|---|---:|
| Corrected | 28 |
| Confirmed | 22 |
| Total reviewed | 50 |
| Remaining | 0 |

All corrections are stored separately from the immutable raw layer as integrity-checked files under [`p0_manual_corrections/`](p0_manual_corrections/). The next 94 player-side review rows are published under [`p1_review_queue/`](p1_review_queue/).

## Interpretation

The output measures realized contribution in this campaign sample. It is affected by army composition, opponents, player commands, perks, terrain, battle duration, and survival selection.

It is suitable for exploratory reporting. It is not yet sufficient for:

- universal troop strength claims;
- causal attribution to equipment or skills;
- frozen score-model recalibration;
- matchup simulation.

## Next gate

Phase 0 becomes canonical after:

1. review of the remaining P1 rows;
2. verified alias and troop-ID resolution against the selected track audit;
3. canonical dataset generation;
4. stability analysis showing how review and alias consolidation affect rankings.
