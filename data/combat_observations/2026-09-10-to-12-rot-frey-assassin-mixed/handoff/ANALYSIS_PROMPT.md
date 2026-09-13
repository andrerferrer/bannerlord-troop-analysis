# Phase 2 analysis handoff — 2026-09-10-to-12-rot-frey-assassin-mixed

Do not begin until Phase 1 publishes the immutable normalized archive and its manifest.

## Scope

- Track: Realm of Thrones 1.4.x
- Focus: Frey Assassin field dedicated-test review, additive to batch-wide coverage
- Source-set SHA-256: `23a83d0e0566e8fd2def0f9e7e950c5f19ea83f985f52b8bc71fcc212eaa5559`
- Source scope: 8 screenshots, 7 retained battle representatives, 1 internal same-battle duplicate
- Contexts: 6 field battles and 1 siege-attack battle
- Special state: `battle_fa07` is the readable active scoreboard retained under the last-observation rule

## Required Phase 2 actions

1. Verify every Phase 1 artifact hash and the deterministic normalized archive.
2. Treat normalized artifacts as immutable; place corrections only under `reviewed/`.
3. Resolve identities only against versioned Realm of Thrones audits.
4. Analyze every visible player-side ordinary troop/context row exactly once.
5. Keep player/enemy, field/siege, participant/cohort, and final/active boundaries separate.
6. Publish reliable and insufficient-evidence partitions using the 5-battle / 20-deployed gate.
7. Deep-dive Frey Assassin only after the batch-wide result.
8. Compare the new dedicated field cohort with the already-merged incidental Frey field cohort without silently pooling incompatible difficulty states.
9. Reconcile the final stop/next-test decision with `data/combat_observations/test_queues/realm_of_thrones.json` in this same PR.
10. Append a full-state `bannerlord-analysis-task:v1` comment (`in_progress`, then `complete` or `blocked`).
11. Validate, self-review, mark ready, squash-merge, and verify the merge when all gates pass.
