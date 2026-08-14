# Phase 2 analysis handoff — combat_2026-08-13_goldenheart_field

## Immutable inputs

- Batch directory: `data/combat_observations/2026-08-13-goldenheart-field`
- Track: `realm_of_thrones` / `1.4.x`
- Context: 2 independent field battles; do not mix with siege contexts
- Player side: defender at 01:47 and attacker at 18:15; preserve recorded side and relationship fields
- Player/enemy rows: separate; primary input contains player-side ordinary troops only
- Focus display label: `Goldenheart Warrior [T6]`; this is not yet a canonical XML ID
- Source SHA-256: `763f8fb7bceb6f34514fe4686a812ec714e4ec694de1c6ddc86dc9cbb11bb1d2`
- Normalized archive SHA-256: `b9b59cdd6547637b7dbf73ff66bef8370654df1dd3ecf7dd62cc48fe37577829`
- Artifact manifest: `artifact_hashes.csv`

## Required actions

1. Verify the selected-source algorithm, ordered Base64 part, normalized archive hash, mirrored manifests, and package artifact hashes.
2. Treat every normalized Phase 1 file as immutable; corrections must be additive under a reviewed layer.
3. Resolve all five queued white-icon fields only from retained evidence; never guess numeric values.
4. Resolve canonical identities only against versioned `realm_of_thrones` audit files. Provisional display slugs are not XML IDs.
5. Independently verify whether display `Goldenheart Warrior [T6]` maps to canonical `summer_master_longbowman`; do not assume the mapping from display similarity alone.
6. Analyze player-side ordinary troops by battle and field context. Enemy rows stay excluded from player rankings.
7. Evaluate schema/track compatibility with the frozen Realm of Thrones empirical controls under `data/rot_reference/empirical/`, especially the nine-battle Goldenheart baseline, before any join; record every joined source and battle ID.
8. Apply the 5-independent-battle / 20-deployed display gate per troop/context/side, with battles as the independent sampling unit. This new batch alone has only two battles and must not produce a standalone reliable conclusion.
9. Do not compute contribution index or whole-army share because both player scoreboards expose only partial troop rows.
10. Publish complete/reliable rankings, context coverage, insufficient-evidence rows, identity audit, input verification, validation report, Goldenheart battle rates, compatible-source provenance, combined comparison, and analysis artifact hashes.
11. Confirm `analysis/model_versions/` remains unchanged, update the PR summary, publish a full-state protocol comment, and squash merge only after every validation gate passes.

## Neutral analytical scope

Evaluate Goldenheart Warrior and the visible Summer Isles line in field context without carrying a tier claim, recommendation, or causal conclusion from Phase 1. Quantify how the two new independent battles affect the compatible historical Goldenheart sample only after provenance and canonical-identity checks pass.
