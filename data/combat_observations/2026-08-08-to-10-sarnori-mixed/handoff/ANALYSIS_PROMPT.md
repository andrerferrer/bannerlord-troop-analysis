# Phase 2 analysis handoff — combat_2026-08-08_to_10_sarnori_mixed

## Immutable inputs

- Batch directory: `data/combat_observations/2026-08-08-to-10-sarnori-mixed`
- Track: `realm_of_thrones` / `1.4.x`
- Contexts: 3 field battles and 3 siege attacks; never pool them
- Player/enemy sides: separate; primary input contains player-side ordinary troops only
- Source SHA-256: `adcb2b9f8545c042f57b5ced51374d919b2829e0d81500aba353507b3dff88bc`
- Normalized archive SHA-256: `54c5ed631540a13a59af5f799910b7253ad09d873b414e0776b1e64f25947bc1`
- Active scoreboard excluded: `2026-08-10 22:22:25`, because the screen shows `Retreat!` and no final result

## Required actions

1. Verify source, archive, ordered Base64 part, and artifact hashes.
2. Preserve all Phase 1 files byte-for-byte; corrections belong only in a separate reviewed layer.
3. Resolve troop identities only against the versioned `realm_of_thrones` audit; provisional normalized display names are not XML IDs.
4. Resolve every explicit review item without guessing and retain unresolved limitations.
5. Generate complete and reliable rankings separately for field and siege attack, player-side only.
6. Apply the 5-independent-battle and 20-deployed display gate per troop/context/side; do not reinterpret this six-battle batch as six observations for each context.
7. Calculate uncertainty with battles as the independent sampling unit.
8. Keep heroes, player rows, party totals, side totals, enemy rows, and the active scoreboard out of ordinary troop rankings.
9. Confirm `analysis/model_versions/` is unchanged.
10. Publish reviewed and analytical artifacts under this batch, update the PR, publish a full `complete` protocol comment, mark ready, squash-merge, and verify closure.

## Explicit analytical question

Evaluate the Sarnori troop family from the immutable normalized evidence without carrying the user's provisional `S Tier` conclusion into extraction. Report Sarnori Spider, Master Javelinier, Master Spearman, Javelinier, Elite Javelinier, Archer, Elite Archer, and Longbowman separately by context and evidence gate.
