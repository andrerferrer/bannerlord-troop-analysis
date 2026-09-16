# Phase 1 publication recovery — PR #101

## Read first

This is the entrypoint for the separate Phase 2 agent. Read the current repository `AGENTS.md`, then this addendum and the original batch `handoff/ANALYSIS_PROMPT.md`. Continue the same branch and PR; do not create a second evidence PR.

The operator required that tasks never end before their PR is opened and that this be saved in the repository rules. That rule is merged into `main` through PR #102. Update the working branch from `main` before Phase 2 material work.

## Authorization correction

The archived `ANALYSIS_PROMPT.md` ends with a generic human-confirmation instruction and `ANALYSIS_TASK_V1.json` contains `human_confirmation_required: true`. Those were assistant-generated, not an operator-imposed restriction. They do not override `AGENTS.md` or the authoritative PR protocol comment.

Keep the evidence PR draft for the required separate Phase 2 agent. After the documented analysis, validation, and review gates pass, mark it ready, squash-merge, and verify the merge without asking for another publication authorization. A genuine host approval boundary or a later explicit operator instruction still takes precedence. This correction changes workflow metadata only; preserve the archived normalized evidence byte-for-byte.

## Recovery performed

- Attached the 13 previously orphaned blobs to commit `a058d507759ff3ac2aa159d7b67ff9e0cf4aaac7`, published the branch, and opened draft PR #101.
- Fresh verification detected three transcription substitutions in the previously uploaded Base64 text. Commit `20da0d2dff2379d8df3b56dda03865c794e3bed2` restores the exact original uploaded Base64 bytes; it does not alter any normalized observation or declared archive hash.
- Correct Base64 Git blob: `6dfc56ad73516c0c8b8bb2e5eab3dbd6a973a790`.
- Base64 SHA-256: `d250d3caddee132d3e1fa80b03162498f77a698f78acb05a9b150c016241743c` (11,798 bytes).
- Decoded archive SHA-256: `ae7c7998ae73a5f9adc358550644813770280512b05f06e0b79418d3dff78f0b` (8,732 bytes).
- Member-checksum manifest Git blob: `be7ac7d81455ca7e5e6a45b751c9e86416a7726c`.

## Fresh recovery verification

Independent Python verification passed for the corrected Git blob identity, Base64 SHA-256, decoded archive SHA-256 and size, all 15 unique safe regular-file members, the complete member-checksum manifest, both handoff mirrors, 2 field/victory events, the 31-row partition (13 ordinary / 18 characters), party kill/wounded reconciliation, and preservation of the unresolved-label row.

Both mounted source PNG SHA-256 hashes also match the archived source manifest exactly:

- `da236eaec047d226bcdf8f55b1f902ba5c2cf53fd174ed3d378cf12953fd45ea`
- `ecb136913cbfc052f49b7119798447326353e8cb95746e0a92e52ff4c222c433`

This is transport/integrity and structural verification, not Phase 2 analysis or a complete repository test-suite claim. Run the committed checks again after checkout:

```bash
python3 data/combat_observations/2026-09-16-rot-qartheen-enthroned-guardian-field-phase1/source/rebuild_phase1_bundle.py --check
python3 tests/test_rot_qartheen_enthroned_guardian_phase1_bundle.py
```

## Remaining work

The separate Phase 2 agent must claim the versioned pending task, verify inputs, resolve review rows additively, analyze every visible ordinary-troop/context row under the existing evidence gates, perform the requested historical comparison without silently pooling cohorts, update the authoritative test queue only when justified, publish validated analytical artifacts and a full complete-state protocol comment, then finish the repository merge workflow. No Phase 2 result is claimed by this recovery.
