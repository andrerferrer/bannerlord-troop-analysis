# Phase 2 handoff

Read `AGENTS.md` and verify the source ZIP hash `9280150e051a07990a5063df77853eec71e623acaba780048e13410587bcb3bd`.

Normalized Phase 1 inputs are immutable:
- `battles.jsonl`
- `troop_occurrences.jsonl`
- `primary_troop_occurrences.jsonl`
- `screenshots_manifest.csv`
- `review/review_queue.csv`
- `review/troop_identity_review.csv`

Batch boundary and deduplication facts:
- 22 source images total;
- 20 independent **field** battles;
- 1 visual same-table duplicate: `06_09_2026 22_29_11 (1).png` is represented by the clearer `06_09_2026 22_29_11.png` frame under the same battle identity;
- 1 non-evidence Vortex screen;
- no exact historical SHA-256 or filename/capture match against the merged PR #91 source inventory;
- 16 independent `Gawen Westerling's Party` field battles and 4 `Joffrey Baratheon's Party` field bridge battles;
- 217 complete player-side ordinary-troop occurrences and 6 unresolved clipped/obscured rows.

Required next actions for a **distinct Phase 2 agent**:
1. verify the Phase 1 bundle manifest, source hash, normalized archive hash, and immutable payload hashes;
2. resolve every `requires_roster_confirmation` identity against the committed Realm of Thrones 1.4.x roster, recording decisions in a reviewed layer rather than editing Phase 1;
3. preserve the six clipped/obscured rows as unresolved unless the source evidence truly resolves them; do not invent missing cells;
4. run batch-wide empirical analysis over **all** complete visible player-side ordinary troops, keeping field context and player/enemy relationship boundaries intact;
5. generate reliable/insufficient evidence coverage, outcome splits, denominator coverage, kill-share impact, retention/pressure-margin diagnostics, and any role-adjusted views required by current repository methodology;
6. explicitly continue the question handed off by merged PR #91: test whether the repeated `Westerling Hedgeknight` field sample survives deployment/share adjustment and how its signal compares with the earlier mixed-cohort evidence; treat this as a hypothesis to verify, not an assumed conclusion;
7. use the 4 Joffrey bridge battles only as compatible historical/context evidence where the methodology permits; do not pool incompatible cohorts merely to strengthen a conclusion;
8. produce the smallest next-test recommendation after the evidence gate is evaluated;
9. run repository tests, publish the append-only `bannerlord-analysis-task:v1` completion state, mark the PR ready, and squash-merge if validation passes.

Do not mutate the Phase 1 normalized files.
