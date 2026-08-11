# Phase 2 analysis handoff — combat_2026-08-11_ravens_teeth_field

## Immutable inputs

- Batch directory: `data/combat_observations/2026-08-11-ravens-teeth-field`
- Track: `realm_of_thrones`
- Context: `field` for all four independent battles
- Source SHA-256: `78cac29a1a239a9435b83878762437057d36974fe890fc41bdd413f6a485f6f9`
- Normalized archive SHA-256: `78a6f3a80ea8351e847555b44f2e7f01c2b4db3d4b772a5af716dd5eedcebcb8`
- Artifact manifest: `artifact_hashes.csv`

## Required actions

1. Verify the ordered Base64 parts, normalized archive hash, mirrored manifests, and source provenance.
2. Treat every normalized Phase 1 file as immutable; corrections must be additive under a reviewed layer.
3. Resolve the eight queued icon/clipped-row fields only from retained evidence; never guess missing cells.
4. Resolve canonical identities only against versioned `realm_of_thrones` audit files.
5. Analyze player-side ordinary troops by battle and field context; enemy rows stay excluded from player rankings.
6. Explicitly evaluate schema/track compatibility with previously merged Realm of Thrones field evidence, especially the 2026-07-27 Ravens' Teeth batches. Join only when the decision and battle IDs are versioned and auditable.
7. Apply the 5-independent-battle / 20-deployed display gate to the compatible combined field evidence and bootstrap uncertainty at the battle level.
8. Do not compute contribution index or whole-army share because the screenshots expose only partial troop rows.
9. Publish complete/reliable rankings, context coverage, insufficient-evidence rows, and a focused Ravens' Teeth comparison with the earlier baseline when compatibility passes.
10. Confirm `analysis/model_versions/` remains unchanged, update the PR summary, publish a full-state protocol comment, and squash merge only after every validation gate passes.
