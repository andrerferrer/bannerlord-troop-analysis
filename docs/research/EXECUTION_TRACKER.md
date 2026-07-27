# Empirical validation execution tracker

## Current status

The project uses a minimum reporting gate of:

```text
5 independent battles
20 deployed troops
```

Five battles is a minimum reporting threshold, not proof of stable ranking; battle-level uncertainty remains mandatory.

Current reviewed sample:

```text
strict player-side occurrences: 527
independent battles: 40
eligible overall labels: 24
eligible field labels: 17
eligible siege-attack labels: 2
eligible siege-defense labels: 0
remaining review flags: 487 P2 rows
```

## Completed

- [x] Recover and verify the source screenshot ZIP.
- [x] Recover and verify the normalized archive.
- [x] Separate player-side and enemy-side observations.
- [x] Adopt the five-battle reporting gate.
- [x] Review all 50 P0 high-impact rows.
- [x] Review all 94 P1 player-side core-uncertainty rows.
- [x] Store corrections, confirmations, and exclusions separately from immutable raw data.
- [x] Publish compact P1 decisions with source-row fingerprints.
- [x] Expand the approved provisional alias table to 18 visually supported aliases.
- [x] Generate a reviewed five-battle player-side baseline.
- [x] Publish battle-bootstrap uncertainty intervals.
- [x] Publish P0-to-P1 ranking sensitivity.
- [x] Reproduce the P1 baseline byte for byte.
- [x] Establish a conservative multi-track canonical identity gate.
- [x] Add deterministic resolution from generated `<track>_troops.csv` audits.
- [x] Detect cross-track exact-name ambiguity and conflicts with existing confirmations.
- [x] Preserve unresolved identities explicitly and block incomplete attribute joins.
- [x] Recover and version the 17 exact identity relationships published by historical PR #20.
- [x] Re-run the resolver against the recovered RoT, vanilla, and War Sails evidence.

## Active workstream: canonical troop identity

- [ ] Export or recover complete troop audits for every represented track.
- [ ] Match every ranked provisional slug to the correct track audit.
- [x] Create a versioned canonical troop-ID audit table.
- [x] Store verified XML/game troop IDs separately from raw and normalized display names.
- [x] Mark ambiguous or missing IDs explicitly rather than guessing.
- [x] Add a fail-closed gate so unresolved identities cannot enter attribute joins.
- [x] Distinguish Realm of Thrones evidence from vanilla/War Sails data at every canonical join boundary.
- [ ] Run the automated resolver against complete RoT, official vanilla/War Sails, and Rhodok-source audits.
- [ ] Reach complete or explicitly approved identity coverage for every label entering modeling.

## Canonical dataset v2

- [x] Replay P0 corrections from the immutable raw layer.
- [x] Replay P1 corrections, confirmations, and exclusions.
- [x] Apply approved provisional aliases deterministically.
- [ ] Replace provisional labels with verified track troop IDs where available.
- [ ] Resolve accepted battle-context corrections.
- [ ] Generate canonical JSONL/CSV outputs.
- [ ] Generate structural, formula, hierarchy, and join validation reports.
- [ ] Record source and output hashes.

## Phase 1: descriptive empirical baseline

- [x] Regenerate eligible rankings from the reviewed P1 dataset.
- [x] Produce overall, field, and siege-attack tables.
- [x] Show battle count, deployed, kills, deaths, casualties, and rates.
- [x] Show battle-bootstrap intervals beside every displayed estimate.
- [x] Produce ranking sensitivity from P0 to P1.
- [ ] Regenerate complete and eligible-only rankings from canonical dataset v2.
- [ ] Publish an explicit unranked/insufficient-evidence table.
- [ ] Expand siege-defense evidence until at least one troop meets the gate.

### Phase 1 exit gate

- [x] Every displayed result has at least 5 battles and 20 deployed.
- [x] Player and enemy sides are never pooled.
- [x] Context-specific claims do not pool contexts.
- [x] Ranking sensitivity to P1 review and provisional aliases is documented.
- [ ] Results regenerate from canonical IDs with one command.
- [ ] All displayed provisional slugs are resolved or explicitly approved as unresolved.

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

1. Identify and audit the missing Rhodok-source module and the two near-miss-only labels.
2. Recover or regenerate complete `realm_of_thrones_troops.csv` and official vanilla/War Sails audits.
3. Run `scripts/run_canonical_identity_pipeline.ps1` with all track audits and `-RequireComplete`.
4. Generate canonical dataset v2.
5. Regenerate reviewed rankings and insufficient-evidence tables from canonical IDs.
6. Expand siege coverage, especially siege defense.
7. Define and run the first controlled speed-versus-damage experiment.
8. Build the versioned attribute/equipment feature table.
9. Begin grouped out-of-sample explanatory modeling.

## Interpretation rule

Until canonical joins and controlled evidence exist, results describe realized contribution in this campaign sample. They do not establish universal troop superiority or causal effects of equipment, skills, perks, or other attributes.
