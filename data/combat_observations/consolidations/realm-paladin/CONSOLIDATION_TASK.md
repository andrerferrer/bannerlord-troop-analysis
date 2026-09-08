# Realm Paladin historical consolidation task

## Task identity

```text
protocol: bannerlord-consolidation-task:v1
task_id: realm-paladin-historical-consolidation
branch: data/consolidate-realm-paladin
pull request: #95
workflow: historical_consolidation
```

This file is the executable handoff for PR #95. It is valid input for the
analysis skill and dispatcher even though the branch contains no new screenshot,
ZIP, `screenshots_manifest.csv`, normalized archive, or
`handoff/ANALYSIS_PROMPT.md`.

## Objective

Create one durable, auditable record of all Realm Paladin field evidence that
can currently be proven from repository-addressable artifacts; preserve the
operator's recollection of an additional completed test without converting it
into numbers; and prevent an accidental retest while the missing history is
unresolved.

## Authoritative inputs

Known empirical source:

```text
path:
data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/
analysis/insufficient_evidence.csv

source analysis:
merged PR #92

pinned ref:
main@9c92910d499d2663cd77385e516fd25bbc7a4669

Git blob SHA:
8a9e888e30a16b1f29f71025542d1a4c0854b713

selector:
canonical_troop_id=realm_paladin
cohort=joffrey
context=field
participant_scope=player_party
```

Structural source:

```text
path:
analysis/candidates/realm_of_thrones_archer_like_mounted_melee_field.csv

Git blob SHA:
3e5d026861f4e40f4bd437b38b5f124261bf770f
```

Queue source of truth:

```text
data/combat_observations/test_queues/realm_of_thrones.json
```

## Known numeric result

```text
battles: 4
deployed: 70
survivors: 13
kills: 159
deaths: 9
wounded: 48
victories / defeats: 1 / 3

kills/deployed:
159 / 70 = 2.271429

kill share:
159 / 2,682 = 0.059284

deployment share:
70 / 1,311 = 0.053394

offensive contribution ratio:
0.059284 / 0.053394 = 1.110307

share-adjusted impact:
(159 / 70) × (159 / 2,682) = 0.134660

retention:
13 / 70 = 0.185714

casualty rate:
(9 + 48) / 70 = 0.814286
```

The known source clears deployment but has `5 - 4 = 1` missing independent
battle for the formal display gate.

## Required actions

1. Read `AGENTS.md`, `docs/protocols/consolidation-task-v1.md`,
   `consolidation.json`, `validation_report.json`, `AUDIT_LOG.md`, and the
   authoritative queue.
2. Verify the pinned empirical and structural source identities.
3. Confirm `evidence.csv` is an exact compatible copy of the selected source
   row.
4. Recompute every published metric and gate deficit.
5. Search committed repository evidence and PR history for additional Realm
   Paladin observations, preserving track, context, cohort, side, and battle
   identity boundaries.
6. Do not request a raw screenshot/ZIP merely to validate the already-committed
   four-battle aggregate.
7. Do not infer an additional battle from operator memory.
8. Keep Realm Paladin absent from `active_test`, `ordered_queue`, and `parked`
   while reconciliation remains open.
9. Keep or resolve the verification hold based only on repository-addressable
   evidence or newly ingested raw evidence.
10. Update all consolidation artifacts, the queue, the PR body, and the newest
    protocol state so they describe the same latest head.
11. Run `tests.test_discover_analysis_tasks`, Python compilation, JSON parsing,
    PR-scope comparison, workflow-run/thread checks, and latest-head review.
12. Merge only when the final protocol state is `complete` and no declared
    consolidation blocker remains.

## Decision matrix

### Additional compatible committed evidence found

- deduplicate at battle level;
- append only verified observations;
- recompute totals and reliability;
- update the queue and consolidation state;
- publish a complete or blocked protocol transition according to validation.

### Previously unpublished raw evidence found

- do not paste remembered values into this consolidation;
- process the raw evidence through the ordinary ingestion and Phase 1 workflow;
- join it only after its hashes, battle identities, and compatibility pass.

### No additional repository-addressable evidence found

- preserve the four-battle aggregate as the complete known committed record;
- record the negative repository audit;
- keep the operator recollection as an unresolved historical lead;
- keep `do_not_retest` unless the operator later authorizes the one-battle
  fallback;
- the consolidation itself may complete and merge once its audit, queue state,
  validation, and protocol receipt are internally consistent.

## Prohibited stopping condition

Do not return:

```text
No analyzable input or pending Phase 2 task was found.
```

A valid `bannerlord-consolidation-task:v1` comment plus this file is the
analyzable input. `discover_analysis_tasks.py --json` must return this PR while
its latest protocol status is `pending`, `in_progress`, or `blocked`.
