# Empirical validation roadmap

## Purpose

This document is the execution plan for turning Bannerlord combat-result screenshots into defensible empirical evidence about troop performance.

The project has two different goals that must not be conflated:

1. **Describe realized campaign contribution** in observed battles.
2. **Explain intrinsic troop strength** using game attributes and controlled tests.

Campaign observations can support the first goal immediately after review. They cannot establish the second goal without controlling for army composition, enemy composition, commands, terrain, perks, battle duration, and other confounders.

## Current methodological rules

### Primary analysis population

The default empirical baseline uses only troop rows that satisfy all of the following:

- `analysis_status == included`;
- `row_type == troop`;
- the troop is on the player side;
- context is `field`, `siege_attack`, or `siege_defense`;
- no unresolved core-field review flag;
- all core numeric fields are present;
- `deployed > 0`;
- no suspected siege-engine-assisted outlier flag;
- repeated rows are consolidated at battle × troop × context before aggregation.

Enemy-side rows are retained for separate matchup and defeat-side analyses. They must not be pooled into the same campaign-performance ranking.

### Display gate

A troop/context estimate is displayed only when it has at least:

```text
5 independent battles
20 deployed troops
```

Five battles is the minimum display gate, not proof of stability. Estimates at this boundary remain exploratory and must show battle-level uncertainty intervals.

### Metrics

```text
kills_per_deployed = sum(kills) / sum(deployed)
death_rate         = sum(deaths) / sum(deployed)
casualty_rate      = sum(deaths + wounded) / sum(deployed)
```

Rates are recomputed after aggregation. Child-row rates are never averaged.

### Independent sampling unit

The battle is the independent sampling unit. Confidence intervals and future train/test splits must resample or partition by battle, not by screenshot row or soldier.

### Data layers

- **Raw:** immutable first-pass extraction and OCR evidence.
- **Reviewed:** explicit corrections with provenance, reviewer, timestamp, reason, and original values.
- **Canonical:** reviewed records with verified troop identities and accepted aliases.
- **Analysis outputs:** reproducible derivatives generated from a named canonical dataset version.

## Phase plan

## Phase 0 — Data quality and canonicalization

### Objective

Produce a reviewed, reproducible canonical dataset before model recalibration.

### Completed

- recovered and verified the exact normalized archive;
- recovered and verified the exact 60-screenshot source ZIP;
- separated player-side and enemy-side observations;
- adopted a five-battle display gate;
- manually reviewed all 50 highest-impact P0 rows;
- corrected 28 rows and confirmed 22 rows;
- reduced the highest-impact review queue to zero;
- approved two conservative OCR aliases;
- generated a reviewed five-battle baseline and battle-bootstrap intervals.

### Remaining

- review 94 P1 player-side rows below the current display gate;
- triage 487 P2 rows, prioritizing future matchup and context analyses;
- resolve all safe troop-name aliases against the Bannerlord 1.4.x + War Sails track snapshot;
- assign verified game/XML troop IDs;
- resolve or explicitly retain undefined battle contexts;
- publish a canonical dataset version and validation report.

### Exit gate

Phase 0 passes when:

- all P0 rows are resolved;
- every ranked label has a verified canonical identity or an explicit unresolved status;
- reviewed corrections are replayable from raw data;
- validation reports contain no structural errors;
- ranking sensitivity to remaining unresolved rows is documented.

## Phase 1 — Descriptive empirical baseline

### Objective

Measure realized player-side contribution without claiming causal troop strength.

### Deliverables

- overall and context-specific rankings;
- five-battle and 20-deployed eligibility flags;
- battle counts, deployed counts, kills, casualties, and deaths;
- deterministic battle-bootstrap intervals;
- complete and eligible-only tables;
- ranking-stability comparisons across filters and dataset versions;
- explicit list of estimates too uncertain to rank.

### Exit gate

- outputs regenerate from the canonical dataset with one command;
- all displayed rows meet the evidence gate;
- no player/enemy pooling;
- no context pooling in context-specific claims;
- uncertainty is visible beside every point estimate.

## Phase 2 — Attribute and equipment integration

### Objective

Join empirical observations to the correct Bannerlord 1.4.x + War Sails troop and equipment snapshot.

### Feature groups

- troop tier and level;
- health and skills;
- armor by body region;
- shield properties;
- mount and harness properties;
- weapon damage, damage type, speed, reach, handling, and ammunition;
- ranged and melee loadouts;
- troop class and tactical role;
- relevant player/captain perks when known.

### Deliverables

- versioned troop-feature table;
- deterministic item/loadout resolution;
- missing-feature and override reports;
- documented feature definitions and units;
- joins validated against canonical troop IDs.

### Exit gate

- no empirical row joins through display-name guessing;
- every modeled feature has provenance;
- later module overrides follow track load order;
- missing or ambiguous equipment remains explicit.

## Phase 3 — Explanatory modeling

### Objective

Estimate which attributes improve prediction after controlling for context and repeated battle structure.

### Model sequence

1. naive descriptive baseline;
2. regularized count/rate model with exposure for deployed troops;
3. battle-aware hierarchical model;
4. grouped out-of-sample validation by battle;
5. ablation tests for equipment, skills, armor, speed, reach, and context;
6. residual analysis to identify systematically over- or under-performing troops.

### Required safeguards

- no random row-level train/test split;
- no causal language from campaign correlations alone;
- correlated attributes reported together or regularized;
- model quality compared against simple baselines;
- coefficients supplemented by predictive importance and uncertainty.

### Exit gate

- out-of-sample performance materially exceeds the descriptive baseline;
- results are stable across reasonable filters;
- major conclusions survive battle-level resampling;
- unexplained residuals and limitations are published.

## Phase 4 — Controlled tests and matchups

### Objective

Separate intrinsic troop mechanics from campaign confounding.

### Initial controlled experiments

- weapon speed versus raw damage;
- combat skill versus otherwise similar equipment;
- reach versus speed in melee interruption scenarios;
- shield and armor effects on survival;
- ranged ammunition and firing-cycle effects;
- perk effects, including captain and party-leader perks;
- repeated troop-versus-troop matchups under fixed conditions.

### Test design

- fixed game version and module track;
- fixed map or documented map rotation;
- fixed army sizes and formation commands;
- fixed character perks unless the perk is the treatment;
- multiple independent repetitions;
- randomized side/spawn assignment when feasible;
- full run metadata and raw result preservation.

### Exit gate

- enough repetitions to estimate variability;
- tests are reproducible by script or documented procedure;
- conclusions distinguish controlled mechanics from campaign observations.

## Phase 5 — Predictive battle model

### Objective

Estimate expected battle outcomes and uncertainty for specified army compositions.

This phase begins only after Phases 2–4 demonstrate useful out-of-sample prediction.

### Candidate outputs

- expected kills and casualties by troop;
- expected remaining forces;
- context-conditional estimates;
- confidence or prediction intervals;
- warnings for extrapolation beyond observed compositions.

### Exit gate

- calibration tested on battles excluded from training;
- prediction intervals have measured coverage;
- performance exceeds simple composition baselines;
- simulator refuses or flags unsupported extrapolation.

## Immediate execution order

1. Merge the five-battle gate and Phase 0 review artifacts.
2. Review the 94 P1 player-side rows.
3. Build the verified alias/ID table against the selected track audit.
4. Regenerate the canonical player-side baseline.
5. Produce a ranking-stability report before and after review/alias consolidation.
6. Collect additional siege-attack and siege-defense battles.
7. Design the first controlled speed-versus-damage experiment.
8. Begin attribute integration only after canonical troop IDs are available.

## Non-negotiable interpretation limits

Until controlled evidence exists, the project may claim that a troop **contributed more in the observed campaign sample**. It may not claim that the troop is universally stronger, that an attribute caused the result, or that the ranking predicts arbitrary matchups.
