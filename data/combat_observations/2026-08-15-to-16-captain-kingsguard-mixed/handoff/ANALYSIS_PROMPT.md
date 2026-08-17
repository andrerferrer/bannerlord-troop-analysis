# Phase 2 analysis handoff — combat_2026-08-15_to_16_captain_kingsguard_mixed

## Immutable inputs

- Batch directory: `data/combat_observations/2026-08-15-to-16-captain-kingsguard-mixed`
- Track: `realm_of_thrones` / `1.4.x`
- Contexts: 3 field, 4 siege attack, and 2 siege defense battles; never pool contexts
- Player side: defender in the three field and two siege-defense battles; attacker in the four siege-attack battles
- Player/enemy rows: separate; primary input contains visible player-side ordinary troops only
- Focus display labels: `Captain of the Kingsguard [T6]` and `Gold Cloak Sniper [T5]`; neither label is a canonical XML ID in Phase 1
- Selected-source SHA-256: `7862cd371ef8e3353035cd89c2bb9fe4aed3853637caeec67aee2832b4663dce`
- Full source-inventory SHA-256: `cad08ea85f618c1882cb289ae07604730bd5ee15a1178b7a31455c636de3c5ee`
- Normalized archive SHA-256: `6b16d78d32ca70ea5093431874d8a73b00e6a3b961fa2686ec8701659decbc4d`
- Artifact manifest: `artifact_hashes.csv`

## Required actions

1. Verify all source-selection decisions, per-image hashes, both ordered-entry source hashes, ordered Base64 parts, normalized archive hash, mirrored manifests, and package artifact hashes.
2. Treat every normalized Phase 1 file as immutable; corrections must be additive under a reviewed layer.
3. Re-review all queued white-icon and cursor-obscured fields from retained evidence; never guess numeric values.
4. Resolve canonical identities only against versioned `realm_of_thrones` audit files. Provisional display slugs are not XML IDs.
5. Analyze visible player-side ordinary troops by battle, side, and context. Enemy rows stay excluded from player rankings; field, siege attack, and siege defense remain separate.
6. Apply the repository 5-independent-battle / 20-deployed display gate per troop/context/side, with battles as the independent sampling unit.
7. Do not compute contribution index or whole-army share because every selected scoreboard exposes only partial troop rows.
8. Evaluate compatibility with prior evidence only after exact track, version, side, context, identity, and count-field checks; record every joined source and battle ID.
9. Publish complete/reliable outputs, context coverage, insufficient-evidence rows, identity audit, input verification, validation report, battle-level uncertainty where supported, compatible-source provenance, and analysis artifact hashes.
10. Confirm `analysis/model_versions/` remains unchanged, update the PR summary, publish a full-state protocol comment, and squash merge only after every validation gate passes.

## Neutral analytical scope

Evaluate the two focus display labels and the visible player-side roster without carrying a tier claim, recommendation, causal conclusion, or canonical identity from Phase 1. Preserve the explicit source exclusions and all context/side boundaries.
