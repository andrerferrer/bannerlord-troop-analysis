# Phase 2 analysis handoff — combat_2026-08-10_omber_interrupted_recovery

## Immutable inputs

- Batch directory: `data/combat_observations/2026-08-10-omber-interrupted-recovery`
- Track: `realm_of_thrones` / `1.4.x`
- Context: one `siege_attack` battle; do not pool with field or siege-defense evidence
- Result: readable `active` scoreboard at 08m20s, accepted as the last observation before the fight was stopped
- Independence rule: never merge, subtract, or reconstruct this Omber battle with the later 22:37 Casat field battle or any cleanup engagement
- Player side: attacker (`Huzo Amai's Party`); enemy parties are `Garrison of Omber` and `Militia of Omber`
- Player/enemy rows: separate; primary input contains nine visible player-side ordinary troops only
- Source PNG SHA-256: `5371af51eb5ad2d18b3af126dfc7243a659bd8bd28c35774427420a8d1b6358a`
- Deterministic source-identity SHA-256: `f8fad8a43801f885d7428ca15558a78ac54e827a4dd186fd92d59132709ef1d3`
- Normalized archive SHA-256: `03ff1f4006603b424e5c4c3fc4b3955f5464bb5ed8489819b59a8c44c1e25774`
- Artifact manifest: `artifact_hashes.csv`
- Visual deduplication audit: `reports/screenshot_deduplication_audit.csv`

## Required actions

1. Reconstruct the archive, verify its SHA-256, artifact manifest, per-image hash, source identity, and visual deduplication decision.
2. Treat every normalized Phase 1 file as immutable; corrections must be additive under the reviewed layer with provenance.
3. Re-review the six queued fields from exact retained evidence when available; never guess values.
4. Resolve every ordinary troop identity only against versioned `realm_of_thrones` audit files. Provisional display slugs are not XML IDs.
5. Analyze all nine visible player-side ordinary troops in `siege_attack`; enemy rows remain excluded from player rankings.
6. Preserve `result=active` and the battle's independence. Do not combine it with Casat or any cleanup battle.
7. Apply the repository 5-independent-battle / 20-deployed display gate per troop/context/side, with battles as the independent sampling unit.
8. Publish reliable and insufficient-evidence outputs, context coverage, identity audit, input verification, validation report, human-readable batch-wide report, and analysis artifact hashes.
9. Confirm `analysis/model_versions/` remains unchanged, update the PR summary, publish a full-state protocol comment, and squash merge only after every gate passes.

## Neutral analytical scope

Evaluate the full visible player-side ordinary roster without carrying a tier claim, recommendation, causal conclusion, or canonical identity from Phase 1.

## Reconstruction

```bash
cd data/combat_observations/2026-08-10-omber-interrupted-recovery/bundle
base64 --decode omber_interrupted_recovery_2026-08-10.tar.xz.base64.part-00 > /tmp/omber_interrupted_recovery_2026-08-10.tar.xz
printf '%s  %s\n' '03ff1f4006603b424e5c4c3fc4b3955f5464bb5ed8489819b59a8c44c1e25774' '/tmp/omber_interrupted_recovery_2026-08-10.tar.xz' | sha256sum --check
mkdir -p /tmp/omber_interrupted_recovery_2026-08-10-extract
tar -xJf /tmp/omber_interrupted_recovery_2026-08-10.tar.xz -C /tmp/omber_interrupted_recovery_2026-08-10-extract
```
