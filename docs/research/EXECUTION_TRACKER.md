# Empirical validation execution tracker

## Current status

The project uses a minimum reporting gate of:

```text
5 independent battles
20 deployed troops
```

This gate is already implemented in `scripts/analysis/build_empirical_baseline.py` and applied to the reviewed baseline. Five battles is a minimum reporting threshold, not proof of stable ranking; battle-level uncertainty remains mandatory.

## Completed

- [x] Recover and verify the source screenshot ZIP.
- [x] Recover and verify the normalized archive.
- [x] Separate player-side and enemy-side observations.
- [x] Adopt the five-battle reporting gate.
- [x] Review all 50 P0 high-impact rows.
- [x] Store corrections separately from immutable raw data.
- [x] Generate a reviewed five-battle player-side baseline.
- [x] Publish battle-bootstrap uncertainty intervals.
- [x] Approve two conservative OCR aliases.

## Active workstream: Phase 0 completion

### P1 review

- [ ] Review the 94 remaining player-side core-uncertainty rows against screenshots.
- [ ] Preserve original values, reviewed values, changed fields, reason, source image, reviewer, and date.
- [ ] Rebuild the reviewed dataset after each review batch.
- [ ] Measure whether any troop enters or leaves the five-battle gate.
- [ ] Publish a P1 completion report and integrity manifest.

### Canonical troop identity

- [ ] Match every ranked provisional slug to the Bannerlord 1.4.x + War Sails track audit.
- [ ] Create a versioned alias table.
- [ ] Store verified XML/game troop IDs separately from display names.
- [ ] Mark ambiguous or missing IDs explicitly rather than guessing.
- [ ] Validate that all empirical joins use verified IDs.

### Canonical dataset v1

- [ ] Replay P0 and P1 corrections from the immutable raw layer.
- [ ] Apply approved aliases deterministically.
- [ ] Resolve accepted battle-context corrections.
- [ ] Generate canonical JSONL/CSV outputs.
- [ ] Generate structural, formula, hierarchy, and join validation reports.
- [ ] Record source and output hashes.

## Phase 1: descriptive empirical baseline

- [ ] Regenerate complete and eligible-only rankings from canonical dataset v1.
- [ ] Produce overall, field, siege-attack, and siege-defense tables.
- [ ] Show battle count, deployed, kills, deaths, casualties, and rates.
- [ ] Show battle-bootstrap intervals beside every displayed estimate.
- [ ] Produce ranking sensitivity across raw, P0-reviewed, P1-reviewed, and canonical versions.
- [ ] Publish an explicit unranked/insufficient-evidence table.

### Phase 1 exit gate

- [ ] Every displayed result has at least 5 battles and 20 deployed.
- [ ] Results regenerate with one command.
- [ ] Player and enemy sides are never pooled.
- [ ] Context-specific claims do not pool contexts.
- [ ] Ranking sensitivity to review and aliases is documented.

## Phase 2: attribute and equipment integration

- [ ] Freeze the Bannerlord 1.4.x + War Sails track snapshot.
- [ ] Build the versioned troop-feature table.
- [ ] Resolve deterministic loadouts, item overrides, armor, mounts, shields, weapons, skills, and tier.
- [ ] Define units and provenance for every feature.
- [ ] Join empirical rows only through verified canonical troop IDs.
- [ ] Publish missing-feature and ambiguous-loadout reports.

## Phase 3: explanatory modeling

- [ ] Establish simple predictive baselines.
- [ ] Fit regularized models with deployed troops as exposure.
- [ ] Add battle-aware hierarchical structure.
- [ ] Split and resample by battle, never by row.
- [ ] Run feature-family ablations: equipment, armor, skills, speed, damage, reach, context.
- [ ] Publish out-of-sample metrics, uncertainty, residuals, and limitations.

## Phase 4: controlled experiments

Initial priority:

1. weapon speed versus raw damage;
2. skill versus similar equipment;
3. reach versus interruption frequency;
4. shield/armor survival effects;
5. ranged firing cycle and ammunition;
6. captain and party-leader perk effects;
7. repeated fixed troop matchups.

Every experiment must preserve game version, module track, map, troop counts, commands, perks, side assignment, repetitions, and raw results.

## Phase 5: predictive battle model

This phase is blocked until Phases 2–4 demonstrate useful grouped out-of-sample prediction.

- [ ] Predict kills, casualties, and remaining forces by composition and context.
- [ ] Produce prediction intervals with measured coverage.
- [ ] Compare against simple composition baselines.
- [ ] Warn or refuse unsupported extrapolation.

## Immediate execution order

1. Review the 94 P1 rows.
2. Build the verified alias and troop-ID table.
3. Generate canonical dataset v1.
4. Regenerate the five-battle baseline.
5. Produce ranking-stability analysis.
6. Expand siege coverage.
7. Run the first controlled speed-versus-damage experiment.
8. Begin feature integration and explanatory modeling.

## Interpretation rule

Until controlled evidence exists, results describe realized contribution in this campaign sample. They do not establish universal troop superiority or causal effects of equipment, skills, perks, or other attributes.
