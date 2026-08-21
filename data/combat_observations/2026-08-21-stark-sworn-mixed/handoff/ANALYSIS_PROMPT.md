# Phase 2 analysis handoff — combat_2026-08-21_stark_sworn_mixed

## Immutable Phase 1 inputs

- Batch directory: `data/combat_observations/2026-08-21-stark-sworn-mixed`
- Track: `realm_of_thrones` / `1.4.x`
- Contexts: 5 `field` battles and 4 `siege_attack` battles; never pool contexts
- Player side: attacker at 00:31, 00:49, 01:15, 02:31, and 09:46; defender at 00:43, 01:31, 02:37, and 11:33
- Requested focus display label: `Stark Sworn Sword [T6]`; this is not a canonical XML ID in Phase 1 and must not filter the batch-wide analysis
- Visible player-side ordinary-troop records: every readable row appears in `troop_occurrences.jsonl`; 106 rows with ranking-critical numeric fields appear in `primary_troop_occurrences.jsonl`; the cursor-obscured Northern Soldier row remains in `review_queue.csv`
- Enemy evidence: enemy side totals and visible party totals are preserved separately; enemy ordinary troop rows were not transcribed and must not enter player rankings
- Original seven-image ZIP SHA-256: `aef41e69e9db4cb7998a328d24759140c812cd66e0be3be98f3dfb897b91a7a7`
- Deterministic combined-input SHA-256: `10b4e2e5e17116df7b8dd1beb8a8c679f6e119b0f7411a0c3ea6040898855498`
- Source inventory file SHA-256: `7f93bf8cbd05124e188e6089d295fab4f58061de0f7d5e6f792895701d4bef54`
- Normalized archive SHA-256: `d94a770ddcabeb24eda965fd289dcb1d91c2a4b0ed945322cd0b825057a5bb6e`
- Ordered Base64 part SHA-256: `ce5930a02c255e165dd355bf295ad57e7a233ecc8df08a700fafd954b4505dcd`
- Artifact manifest: `artifact_hashes.csv`
- Phase 1 delivery manifest: `delivery_hashes.csv`
- Visual and historical audit: `reports/screenshot_deduplication_audit.csv`
- Structural validation: `validation_report.json`, `reports/grouping_validation.csv`, and `reports/aggregation_validation.csv`
- Extractor/reviewer provenance: host vision, exact model/version `unknown`

## Battle-independence rules

The Stoney Sept 01:15 and Banefort 09:46 scoreboards are readable active
observations with one defender remaining. Treat each as its own independent
`siege_attack` battle exactly as shown. Never merge, subtract, complete, or
reconstruct either observation with any later cleanup or re-engagement. A
cleanup fight, if supplied later, is a new battle. The remaining seven screens
are distinct final-result tables. There are no same-battle supplemental screens
and no internal or committed-history duplicates in this batch.

## Required Phase 2 actions

1. Reconstruct the archive and verify its SHA-256, ordered Base64-part hash, `artifact_hashes.csv`, every per-image hash, the original ZIP hash, combined-input hash definition, source inventory hash, and the historical/visual audit.
2. Treat every Phase 1 normalized file as immutable. Record any correction in a separate reviewed layer with original value, reviewed value, evidence reference, reviewer, and source SHA-256.
3. Resolve all 17 queued items from exact retained evidence when accessible. Never guess the cursor-obscured Northern Soldier kills cell or convert a white non-numeric upgrade icon into an integer. A non-ranking side-total tooltip item may use the exact same-screen player-party row only with explicit provenance.
4. Resolve troop identities only against versioned `realm_of_thrones` audit files. Provisional display slugs and visible names are not canonical XML IDs.
5. Analyze every visible player-side ordinary troop in every observed context. The Stark Sworn Sword focus is additive and must not suppress any other troop/context row.
6. Keep player/enemy relationships, `field`, and `siege_attack` separate. Preserve `result=active` and the two interrupted battle identities.
7. Apply the repository minimum display gate of 5 independent battles and 20 deployed troops per troop/context/side, using battles as the independent sampling unit. Publish every eligible troop/context row exactly once in the reliable or insufficient-evidence partition and in the human-readable batch-wide report.
8. Preserve efficiency and player-side kill-share calculations as separate metrics. Use only the explicit player-side total kills stored for each contributing battle; do not reconstruct a denominator from partial troop rows. Publish share/impact only after verifying positive, unambiguous total-kill coverage for every contributing battle.
9. Evaluate compatibility with prior evidence only after exact track, version, side, context, identity, result-state, and count-field checks. Record every joined source batch and battle ID.
10. Publish reviewed decisions, canonical identity audit, input verification, complete/reliable rankings, insufficient-evidence coverage, context coverage, battle-level provenance/uncertainty, batch-wide report, validation report, and analysis artifact hashes under this batch's `analysis/` directory.
11. Confirm `analysis/model_versions/` remains unchanged, update the draft PR summary and checklist, publish append-only full-state protocol comments, mark the PR ready only after all gates pass, and squash merge as declared by the protocol.

## Neutral analytical scope

Do not carry a tier claim, recommendation, causal explanation, or model change
from Phase 1. Summarize batch-wide findings before the requested Stark Sworn
Sword focus in the Phase 2 user-facing handoff.

## Reconstruction

```bash
cd data/combat_observations/2026-08-21-stark-sworn-mixed/bundle
base64 --decode stark_sworn_mixed_2026-08-21.tar.xz.base64.part-00 > /tmp/stark_sworn_mixed_2026-08-21.tar.xz
printf '%s  %s\n' 'd94a770ddcabeb24eda965fd289dcb1d91c2a4b0ed945322cd0b825057a5bb6e' '/tmp/stark_sworn_mixed_2026-08-21.tar.xz' | sha256sum --check
mkdir -p /tmp/stark_sworn_mixed_2026-08-21-extract
tar -xJf /tmp/stark_sworn_mixed_2026-08-21.tar.xz -C /tmp/stark_sworn_mixed_2026-08-21-extract
```
