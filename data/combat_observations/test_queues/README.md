# Empirical troop test queues

Each track has one machine-readable queue under this directory:

```text
data/combat_observations/test_queues/<track>.json
```

## Authority

The track queue is the repository source of truth for:

- the current dedicated empirical target;
- the ordered list of future targets;
- troops held for historical verification;
- completed, rejected, or parked targets.

Batch-local `analysis/NEXT_TEST_RECOMMENDATION.md` files, pull-request bodies, comments, candidate shortlists, and chat history are evidence or proposals. They do not alter the active queue unless the same repository change updates the track queue.

The newest valid `bannerlord-analysis-task:v1` comment remains authoritative for the execution state of one evidence batch. It does not replace the track queue for the cross-batch question “what troop should be tested next?”

## Read order

Before answering a queue question or interpreting a new screenshot batch:

1. read the queue for the relevant track;
2. inspect any open evidence pull request that modifies that queue;
3. read referenced batch reports only to verify the recorded rationale;
4. never rebuild the queue from the most recent recommendation file alone.

A pending change in an open pull request must be described as pending until merged. The version on the working branch controls continuation of that pull request; the version on `main` controls unrelated sessions.

## Update rules

- **Explicit operator decisions:** record immediately.
- **Phase 1:** may confirm or set the active target; it must not choose the next target from preliminary results.
- **Phase 2:** when completed analysis changes target status or the next recommendation, update the queue in the same pull request before merge.
- **Verification hold:** do not recommend or retest the troop until the historical audit is resolved.
- **Empty ordered queue:** means no future target is approved. Do not invent one.
- **Context boundaries:** field, siege attack, and siege defense remain distinct queue entries.

The queue must preserve the canonical troop ID when known, display name, context, status, reason, and evidence references needed to audit each decision.
