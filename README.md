# Bannerlord Troop Analysis

Data-driven troop analysis framework for Mount & Blade II: Bannerlord.

## Start here

- [`docs/research/EXECUTION_TRACKER.md`](docs/research/EXECUTION_TRACKER.md) — current task status and immediate execution order
- [`docs/research/EMPIRICAL_VALIDATION_ROADMAP.md`](docs/research/EMPIRICAL_VALIDATION_ROADMAP.md) — empirical research plan and phase gates
- [`analysis/empirical/2026-07-23/PHASE0_EXECUTION_REPORT.md`](analysis/empirical/2026-07-23/PHASE0_EXECUTION_REPORT.md) — latest image-backed review results
- [`TODO.md`](TODO.md) — broader historical implementation checklist
- [`docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md`](docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md)
- [`docs/methodology/ADR-001-combat-image-normalization.md`](docs/methodology/ADR-001-combat-image-normalization.md)

Current authoritative frozen models:

```text
v7.1 — general battlefield score
v7.3 — tooltip-validated throwing burst score
```

Files under `analysis/model_versions/` remain frozen until empirical evidence passes the documented recalibration gates.

## Combat screenshot pipeline status

The 2026-07-23 production sources are recovered and verified:

```text
60-screenshot source ZIP SHA-256:
00f83754687fe769fdfdea1bda0b68b4d7801c25195ff803aa1a1b35fa15d69f

Normalized archive SHA-256:
10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa
```

Current empirical state:

- player-side and enemy-side observations are separated;
- minimum display gate is **5 independent battles and 20 deployed troops**;
- all 50 high-impact P0 rows were checked against source screenshots;
- 28 P0 rows were corrected and 22 were confirmed;
- P0 remaining: 0;
- P1 remaining: 94;
- P2 remaining: 487;
- strict reviewed player-side sample: 456 occurrences across 40 battles;
- eligible labels: 23 overall, 17 field, 2 siege attack, and 0 siege defense.

The current rankings are exploratory campaign-performance evidence, not a universal tier list or causal estimate of intrinsic troop strength.

## Core methodological rules

- Preserve immutable raw extraction data.
- Apply corrections in a separate reviewed layer with provenance.
- Resolve troop identities against the selected module track before explanatory modeling.
- Keep field, siege attack, and siege defense separate.
- Use the battle as the independent sampling unit.
- Require at least **5 independent battles and 20 deployed troops** before displaying a troop/context estimate.
- Display uncertainty beside point estimates.
- Do not pool the victorious player side with the defeated enemy side.
- Do not recalibrate frozen models until canonicalization and out-of-sample validation gates pass.

## Goal

Create an interpretable troop-analysis pipeline using XML-exported game data, controlled tests, and real campaign observations.

The project should avoid shallow rankings based only on raw stats. Target outputs include:

- hits to kill;
- expected kills per minute;
- melee/ranged/throwing offense;
- defensive durability;
- reliability and AI usability;
- tier-by-tier and role-specific rankings;
- empirical campaign validation;
- controlled matchup evidence;
- eventually, calibrated battle predictions with uncertainty.

## Primary target

The primary track is Bannerlord 1.4.x with War Sails integrated into the baseline. Realm of Thrones data remains useful as a methodological and empirical reference track, but must not be silently mixed with vanilla data.

## Analysis pipeline

```text
XML/module export
→ deterministic normalization and load-order resolution
→ weapon, armor, mount, skill, and perk features
→ HTK/KPM and role scoring
→ screenshot/result normalization
→ reviewed canonical empirical dataset
→ descriptive battle-level baseline
→ attribute and equipment integration
→ controlled tests and explanatory models
→ out-of-sample validation
→ calibrated prediction, only if supported
```

## Current model direction

The preferred theoretical offense framework is based on HTK/KPM:

```text
HTK = effective_enemy_hp / effective_damage
KPM = attempts_per_minute × hit_chance / HTK
```

For mixed-loadout troops, melee, ranged, and throwing contribution are modeled separately before any context-dependent blend.

## Empirical baseline command

```bash
python scripts/analysis/build_empirical_baseline.py \
  reviewed_primary_troop_occurrences.jsonl \
  baseline_strict_player_side.csv
```

Defaults:

```text
minimum battles: 5
minimum deployed: 20
bootstrap repetitions: 5000
```
