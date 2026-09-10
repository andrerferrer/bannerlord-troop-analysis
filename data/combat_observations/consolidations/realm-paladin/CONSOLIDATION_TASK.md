# Realm Paladin historical consolidation task

## Task identity

```text
protocol: bannerlord-consolidation-task:v1
task_id: realm-paladin-historical-consolidation
branch: data/consolidate-realm-paladin
pull request: #95
workflow: historical_consolidation
```

## Objective

Create one auditable record of all compatible Realm Paladin field evidence in
committed repository artifacts, preserve context and battle boundaries, and
reconcile the authoritative Realm of Thrones test queue without inventing
values from memory.

## Resolution

The repository audit recovered two compatible committed sources:

1. merged PR #91: 11 field battles / 122 deployed / 330 kills;
2. merged PR #92: 4 later field battles / 70 deployed / 159 kills.

The normalized archives verify, and the 15 battle IDs and source-image hashes
are disjoint. The combined field result is 15 battles / 192 deployed / 489
kills. PR #91 clears the 5-battle / 20-deployed gate independently, so the field
test is complete even without relying on the four-battle follow-up.

Realm Paladin therefore moves from `verification_holds` to `closed` with status
`completed_no_additional_test`. No future target is selected.

## Authoritative sources

PR #91:

```text
path: data/combat_observations/2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts/analysis/ranking_reliable.csv
ref: main@3bde0f43bddec1e562937f8da66009c05af04042
Git blob SHA: c7b603bc0f77fc4d98c643a8efe81c44101c1489
archive SHA-256: 9cc8482caf6d37356b186c0a68dfa9e6f50303fb715f6ddfc3a49e2593b59c9d
bundle path: data/combat_observations/2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts/bundle
bundle tree SHA: 48992fc18dfd3a59b5510541a141f2b1d28a616f
```

PR #92:

```text
path: data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/analysis/insufficient_evidence.csv
ref: main@9c92910d499d2663cd77385e516fd25bbc7a4669
Git blob SHA: 8a9e888e30a16b1f29f71025542d1a4c0854b713
archive SHA-256: 1ba4c3c28db029bda23f57a6c830c0d57107b9a6e89dd1b1258a70514f56222a
bundle path: data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/bundle
bundle tree SHA: 94992e7cc381cd0e1c5870ed93fbd2bd9edf9360
```

The exact repository ref, path, and Git object for every aggregate, archive
part, checksum sidecar, reconstruction README, and structural input are listed
in `source_manifest.json`. The validation receipt verifies every entry before
attesting the reconstructed archive hashes.

Structural source:

```text
path: analysis/candidates/realm_of_thrones_archer_like_mounted_melee_field.csv
ref: main@bb71cfce293c2c7dc94497b9fe195e24d2e2b2d0
Git blob SHA: 3e5d026861f4e40f4bd437b38b5f124261bf770f
```

## Compatibility boundary

```text
track: realm_of_thrones
game version: 1.4.x
cohort: joffrey
context: field
participant scope: player_party
parent group: Joffrey Baratheon's Party
canonical troop: realm_paladin
canonical role: melee_cavalry
```

Two siege-attack observations in PR #91 are excluded from the field result.
Enemy-side observations, other cohorts, and other tracks are not pooled.

## Consolidated metrics

```text
battles: 15
deployed: 192
survivors: 87
kills: 489
deaths: 17
wounded: 88
routed: 0
victories / defeats: 11 / 4
kills/deployed: 2.546875
verified player-side total kills: 9,436
player-side kill share: 0.051823
share-adjusted impact: 0.131986
verified player-side total deployed: 4,736
player-side deployment share: 0.040541
offensive contribution ratio: 1.278296
offensive share gap: 0.011282
retention: 0.453125
death rate: 0.088542
casualty rate: 0.546875
reliability: reliable
```

## Completion checks

- [x] Read the repository workflow and consolidation protocol.
- [x] Publish append-only `in_progress` state before material edits.
- [x] Verify both pinned source blobs and merged pull requests.
- [x] Verify the structural source path, ref, and Git blob.
- [x] Pin and verify every committed archive reconstruction input.
- [x] Reconstruct and hash both normalized archives.
- [x] Verify archive-member safety and payload hashes.
- [x] Copy both compatible aggregate rows to `evidence.csv`.
- [x] Publish all 15 field observations in `battle_evidence.csv`.
- [x] Verify disjoint battle IDs and image hashes.
- [x] Recompute every combined metric and gate result.
- [x] Keep siege attack separate from field.
- [x] Reconcile with the newer merged Cerwyn queue transition.
- [x] Move Realm Paladin from hold to closed without selecting a next target.
- [ ] Validate the final pushed head, publish `complete`, mark ready, squash
  merge, and verify the merge.

## Completion action

```text
action: merge
merge method: squash
```
