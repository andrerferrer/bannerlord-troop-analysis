# Empirical research phase gates

## Global evidence gate

A troop/context result may be displayed only when both conditions hold:

```text
battle_count >= 5
sum(deployed) >= 20
```

The five-battle threshold is a reporting minimum, not a claim of stability. Battle-level uncertainty intervals remain required.

## Phase 0 — Canonicalization

Passes when:

- P0 review is complete;
- P1 review is complete or remaining unresolved rows are explicit;
- all displayed labels have verified troop IDs or explicit exclusions;
- corrections replay deterministically from raw data;
- canonical outputs and validation reports are hash-addressed;
- ranking sensitivity to review and aliases is published.

## Phase 1 — Descriptive baseline

Passes when:

- complete and eligible-only outputs regenerate with one command;
- every displayed estimate passes the five-battle and 20-deployed gate;
- player and enemy sides are separated;
- contexts are reported separately;
- uncertainty accompanies all displayed estimates;
- insufficient-evidence labels are listed explicitly.

## Phase 2 — Feature integration

Passes when:

- empirical records join through verified IDs;
- feature definitions and units are documented;
- item/loadout/module overrides are deterministic;
- missing and ambiguous features remain explicit;
- feature provenance is complete.

## Phase 3 — Explanatory modeling

Passes when:

- evaluation is grouped by battle;
- predictive performance exceeds simple baselines out of sample;
- conclusions are stable across reasonable filters and battle resampling;
- feature ablations are published;
- residuals, uncertainty, and limitations are documented;
- campaign correlations are not described as causal effects.

## Phase 4 — Controlled experiments

Passes when:

- treatment and controls are documented;
- game version, module track, map, formations, commands, perks, and troop counts are fixed or recorded;
- repetitions are sufficient to estimate variability;
- side/spawn assignment is randomized where feasible;
- raw results and metadata are preserved;
- the procedure is reproducible.

## Phase 5 — Predictive model

Passes when:

- predictions are tested on held-out battles;
- prediction intervals have measured coverage;
- performance exceeds simple composition baselines;
- unsupported extrapolation is flagged or refused;
- calibration and failure modes are published.
