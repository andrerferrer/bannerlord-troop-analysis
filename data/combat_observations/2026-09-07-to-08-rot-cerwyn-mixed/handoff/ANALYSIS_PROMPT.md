# Phase 2 analysis handoff — 2026-09-07-to-08-rot-cerwyn-mixed

Do not begin until Phase 1 publishes the immutable normalized archive and its manifest.

## Scope

- Track: Realm of Thrones 1.4.x
- Focus: Cerwyn Marauder field follow-up, additive to batch-wide coverage
- Source ZIP SHA-256: `88792f888ff37bcf29831b4f484f76bb27c84b0ec2686076f29fc18db714f770`
- Provisional source scope: 25 screenshots, 23 retained representatives, 2 internal same-battle duplicates
- Contexts: 22 field representatives and 1 siege-attack intermediate (`Retreated to the keep!`) representative

## Required Phase 2 actions

1. Verify every Phase 1 artifact hash and the deterministic normalized archive.
2. Treat normalized artifacts as immutable; place corrections only under `reviewed/`.
3. Resolve identities only against the versioned Realm of Thrones audit.
4. Analyze every visible player-side ordinary troop/context row exactly once.
5. Keep player/enemy, field/siege, participant/cohort, and final/intermediate boundaries separate.
6. Publish reliable and insufficient-evidence partitions using the 5-battle / 20-deployed gate.
7. Deep-dive Cerwyn Marauder only after the batch-wide result.
8. Reconcile the final stop/next-test decision with `data/combat_observations/test_queues/realm_of_thrones.json` in this same PR.
9. Append a full-state `bannerlord-analysis-task:v1` comment (`in_progress`, then `complete` or `blocked`).
10. Validate, self-review, mark ready, squash-merge, and verify the merge when all gates pass.
