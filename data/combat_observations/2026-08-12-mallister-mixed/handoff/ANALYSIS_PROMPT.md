# Phase 2 analysis handoff — combat_2026-08-12_mallister_mixed

## Immutable inputs

- Batch directory: `data/combat_observations/2026-08-12-mallister-mixed`
- Track: `realm_of_thrones` / `1.4.x`
- Contexts: 4 field battles and 2 siege attacks; never pool them
- Player side: attacker in five battles; defender in the 15:18 field battle; preserve the recorded side and relationship fields
- Player/enemy rows: separate; primary input contains player-side ordinary troops only
- Source SHA-256: `da79e212250da1b9105f1c71b7ade09f463b4373de87c011b1a8987979e74016`
- Normalized archive SHA-256: `97db4b82f1d1b146d43c3f3afc421cb4594c2960bd418a045f70c2a0685758e7`
- Artifact manifest: `artifact_hashes.csv`

## Required actions

1. Verify the selected-source algorithm, ordered Base64 part, normalized archive hash, mirrored manifests, and package artifact hashes.
2. Treat every normalized Phase 1 file as immutable; corrections must be additive under a reviewed layer.
3. Resolve all 11 queued icon/clipped-row fields only from retained evidence; never guess missing cells.
4. Resolve canonical identities only against versioned `realm_of_thrones` audit files. Provisional display slugs are not XML IDs.
5. In particular, independently verify the audit mappings noted by the operator: display `Mallister Knight [T5]` is expected to resolve to `mallister_horseman`, display `Mallister Horseman [T4]` to `mallister_rider`, and display `Mallister Archer [T4]` to `mallister_archer`; never merge these display lines by name similarity.
6. Analyze player-side ordinary troops by battle and context. Enemy rows stay excluded from player rankings, and field/siege attack remain separate.
7. Evaluate schema/track compatibility with previously merged Realm of Thrones evidence before any join; record every joined source and battle ID.
8. Apply the 5-independent-battle / 20-deployed display gate per troop/context/side, with battles as the independent sampling unit. This new batch alone has four field battles and two siege attacks.
9. Do not compute contribution index or whole-army share because the screenshots expose only partial troop rows.
10. Publish complete/reliable rankings, context coverage, insufficient-evidence rows, identity audit, input verification, validation report, and analysis artifact hashes.
11. Confirm `analysis/model_versions/` remains unchanged, update the PR summary, publish a full-state protocol comment, and squash merge only after every validation gate passes.

## Neutral analytical scope

Evaluate the visible Mallister troop family separately by field and siege-attack context. Do not carry a tier claim, recommendation, or causal conclusion into the analysis. The Phase 1 records preserve only visible scoreboard evidence.
