# Empiria / V4.4 — execution status (plan v3.1 Fase C)

Status: **field empiria available for Nightmare Sails; Realm of Thrones follow-up remains below display gate**. Theoretical Fase B remains independent.

## Online empirical batches

### Realm of Thrones

- Reviewed 2026-07-26/27 batch: `data/combat_observations/2026-07-27-normalized-only/`.
- Field follow-up B01–B02: `data/combat_observations/2026-07-27-rot-field-followup/`.
- Follow-up coverage: 2 independent field battles, 17 included ordinary-troop occurrences, 0 reliable rows.
- The follow-up is valid evidence but is insufficient by itself for the 5-battle / 20-deployed display gate.

### Nightmare Sails

- Field batch B03–B11: `data/combat_observations/2026-07-28-to-29-nightmare-sails-field/`.
- Coverage: 9 independent field battles, 113 included ordinary-troop occurrences, 7 reliable rows.
- Track resolution is backed by exact display-name matches in `data/nightmare_sails/audit/nightmare_sails_troops.csv`.
- Two partially obscured rows remain excluded in the reviewed layer rather than guessed.

Reliable field rows:

1. Nord Huscarl — 6 battles, 25 deployed, 3.120 kills/deployed.
2. Battanian Wildling — 8 battles, 34 deployed, 2.676 kills/deployed.
3. Forest Reaper — 6 battles, 24 deployed, 1.375 kills/deployed.
4. Imperial Elite Cataphract — 7 battles, 140 deployed, 1.350 kills/deployed.
5. Veteran Outrider — 5 battles, 39 deployed, 0.923 kills/deployed.
6. Khuzait Khan's Guard — 7 battles, 112 deployed, 0.884 kills/deployed.
7. Imperial Trained Infantryman — 5 battles, 41 deployed, 0.780 kills/deployed.

These are descriptive campaign-contribution rates, not intrinsic-strength rankings. Tracks, sides, and contexts remain separate.

## Reproducibility state

- All 11 scoreboards are split into track-correct repository batches.
- Deterministic normalized archives, reconstruction instructions, SHA-256 manifests, structural validation, review layers, analytical outputs, and protocol state are repository-addressable.
- Raw screenshots are not retained in Git; original filenames and image SHA-256 values are versioned. This is allowed after deterministic normalization passes the repository gates.
- Off-screen rows are not inferred.
- Heroes are excluded from ordinary troop rankings.

## Realm of Thrones priority troops

When compatible RoT evidence reaches the display gate, prioritize:

- Ravens' Teeth
- Goldenheart Warrior
- Celtigar Banneret
- Lyseni Enforcer
- Myrish Artisan of War
- Golden Company Mahout
- Sarnori Spider
- Baratheon Hammerknight

## V4.4 kinetic overlay

Still blocked on exact-item profiles and a dedicated model-change pull request. This is outside the empirical batch critical path.

`analysis/model_versions/` remains frozen.
