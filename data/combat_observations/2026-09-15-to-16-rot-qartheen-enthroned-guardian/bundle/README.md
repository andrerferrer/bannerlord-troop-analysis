# Immutable normalized Phase 1 bundle

The interrupted publication was recovered from Git tree `9c23822a86d2a4429107da92cafaead0afcb3d7e`. No normalized evidence bytes were changed.

- Archive: `qartheen_enthroned_guardian_phase1.tar.xz`
- SHA-256: `7f75db2d12038c24a57a12f2bdb1f37b2220f873b34ea7247121aa7c5b9b4ced`
- Archive bytes: 10412
- Base64 text bytes: 14067
- Base64 text SHA-256: `8cf63f6e7ebe820a6046a61025798471229dea1083ee5fa8239d446b8fe355c5`
- Members: 24 regular files, with exact per-member checksums in `qartheen_enthroned_guardian_phase1.members.sha256`.

## Reconstruct from repository root

```bash
set -eu
ROOT=$(pwd)
BATCH=data/combat_observations/2026-09-15-to-16-rot-qartheen-enthroned-guardian
WORK=$(mktemp -d)
base64 --decode "$BATCH/bundle/qartheen_enthroned_guardian_phase1.tar.xz.base64" > "$WORK/qartheen_enthroned_guardian_phase1.tar.xz"
(cd "$WORK" && sha256sum -c "$ROOT/$BATCH/bundle/qartheen_enthroned_guardian_phase1.tar.xz.sha256")
mkdir "$WORK/normalized"
tar -xJf "$WORK/qartheen_enthroned_guardian_phase1.tar.xz" -C "$WORK/normalized"
(cd "$WORK/normalized" && sha256sum -c "$ROOT/$BATCH/bundle/qartheen_enthroned_guardian_phase1.members.sha256")
printf 'Verified immutable input directory: %s\n' "$WORK/normalized"
```

The source manifest, source inventory, normalized events, party summaries, ten player-row shards, shard index, deduplication audit, unresolved-row list and integrity report are repository-addressable **inside this archive**. They need not exist as expanded files in the checkout. Use the verified temporary extraction for downstream reads; keep Phase 2 outputs under the batch `analysis/` and `reviewed/` directories.

The batch-root README, screenshot manifest and both handoff files are exact mirrors of the corresponding archive members. `phase1_checkpoint.json`, `batch_state.json`, this bundle documentation and publication-recovery reports are transport/workflow metadata outside the immutable archive.

All ten original mounted PNG files were rehashed successfully during publication recovery. Raw image retention in Git remains absent. The original historical-search limitation remains documented; the recovery did not claim a new repository-wide historical deduplication pass or a completed independent Phase 2.
