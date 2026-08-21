# Phase 2 analysis handoff — combat_2026-08-21_lannister_prideknight_mixed

## Immutable Phase 1 inputs

- Batch directory: `data/combat_observations/2026-08-21-lannister-prideknight-mixed`
- Track: `realm_of_thrones` / `1.4.x`
- Contexts: 8 `field` battles and 1 `siege_attack` battle; never pool contexts
- Player side: defender at 13:42, 14:05, 17:24, and 19:09; attacker at 13:52, 18:53, 19:15, 19:22, and 19:27
- Data-driven requested focus display label: `Lannister Prideknight [T6]`; this is not a canonical XML ID in Phase 1 and must not filter batch-wide analysis
- Focus discrepancy: the user asked conversationally about retesting Mallister Eagle Knight, but none is present on the player side. The 19:27 screen shows Jason Mallister as the enemy and one enemy `Mallister Eagle Knight [T6]`; do not relabel or pool it. The actual repeat player-side T6 row in all nine screens is `Lannister Prideknight [T6]`, which Phase 2 must treat as the additive focus requested by the supplied data.
- Visible player-side ordinary-troop records: every readable row appears in `troop_occurrences.jsonl`; 110 ranking-critical numeric rows appear in `primary_troop_occurrences.jsonl`
- Enemy evidence: enemy side totals and visible party totals are preserved separately; enemy ordinary troop rows were not transcribed and must not enter player rankings
- Deterministic combined-input SHA-256: `62aa7f249e53ae5747cd9a30b44b9fdab957a9f9db8674bd28639be78e1266bb`
- Source inventory file SHA-256: `8d9483432fe9989e4f3d1277b79525565a0cb5ad19afc4199f392eb1f17123bf`
- Normalized archive SHA-256: `1ff30bba3440c89a338cbbdbe9a78c76f0eaf912bae2d5504ee9f05f42d82456`
- Ordered Base64 part SHA-256: `bc8b8032303bab5785b36bf3dd591963b30e928cddb007b1b4acfa87498e151c`
- Artifact manifest: `artifact_hashes.csv`
- Phase 1 delivery manifest: `delivery_hashes.csv`
- Visual and historical audit: `reports/screenshot_deduplication_audit.csv`
- Structural validation: `validation_report.json`, `reports/grouping_validation.csv`, and `reports/aggregation_validation.csv`
- Extractor/reviewer provenance: host vision, exact model/version `unknown`

## Battle-independence rules

All nine screens are distinct final-result tables. Eight are field battles. The Willow Wood 19:15 screen is a siege attack because Tywin is the attacker and the defender groups are the garrison and militia. There are no same-battle supplemental screens, interrupted screens, internal duplicates, or committed-history duplicates.

## Required Phase 2 actions

1. Reconstruct the archive and verify its SHA-256, ordered Base64-part hash, `artifact_hashes.csv`, every per-image hash, combined-input definition, source inventory hash, and historical/visual audit.
2. Treat every Phase 1 normalized file as immutable. Record corrections in a separate reviewed layer with original/reviewed values, evidence reference, reviewer, and source SHA-256.
3. Resolve all 5 queued hero-only UI items from exact retained evidence when accessible. Never invent cursor-obscured values or convert a white non-numeric upgrade icon into an integer.
4. Resolve identities only against versioned `realm_of_thrones` audit files. Provisional display slugs and visible names are not canonical XML IDs.
5. Analyze every visible player-side ordinary troop in every observed context. The Lannister Prideknight focus is additive and must not suppress any troop/context row. Do not use the enemy Mallister Eagle Knight as player-side focus evidence.
6. Keep player/enemy relationships, `field`, and `siege_attack` separate.
7. Apply the repository minimum display gate of 5 independent battles and 20 deployed troops per troop/context/side, using battles as the independent sampling unit. Publish every eligible row exactly once in reliable or insufficient evidence and the human-readable report.
8. Preserve efficiency and player-side kill share as separate metrics. Use only explicit player-side total kills; never reconstruct denominators from partial troop rows.
9. Evaluate compatibility with prior evidence only after exact track, version, side, context, identity, result-state, and count-field checks.
10. Publish reviewed decisions, canonical identity audit, input verification, rankings, insufficient-evidence coverage, context coverage, battle provenance/uncertainty, batch-wide report, validation report, and analysis hashes under `analysis/`.
11. Confirm `analysis/model_versions/` remains unchanged, update the draft PR, publish append-only protocol comments, mark ready only after gates pass, and squash merge as declared by the protocol.

## Neutral analytical scope

Do not carry a tier claim, gameplay conclusion, causal explanation, or recommendation from Phase 1. Summarize batch-wide findings before the additive Lannister Prideknight focus.

## Reconstruction

```bash
cd data/combat_observations/2026-08-21-lannister-prideknight-mixed/bundle
base64 --decode lannister_prideknight_mixed_2026-08-21.tar.xz.base64.part-00 > /tmp/lannister_prideknight_mixed_2026-08-21.tar.xz
printf '%s  %s\n' '1ff30bba3440c89a338cbbdbe9a78c76f0eaf912bae2d5504ee9f05f42d82456' '/tmp/lannister_prideknight_mixed_2026-08-21.tar.xz' | sha256sum --check
mkdir -p /tmp/lannister_prideknight_mixed_2026-08-21-extract
tar -xJf /tmp/lannister_prideknight_mixed_2026-08-21.tar.xz -C /tmp/lannister_prideknight_mixed_2026-08-21-extract
```
