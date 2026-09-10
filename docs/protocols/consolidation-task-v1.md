# Historical consolidation task comment protocol v1

## Purpose

Historical evidence consolidations are repository tasks even when they introduce
no new screenshots, ZIP, normalized archive, or Phase 2 handoff.

This protocol makes those pull requests discoverable by the same local command
used for analysis work:

```bash
python scripts/analysis/discover_analysis_tasks.py --json
```

A consolidation task must not be rejected merely because
`screenshots_manifest.csv`, `handoff/ANALYSIS_PROMPT.md`, or a raw source ZIP is
absent. Those artifacts belong to new-evidence ingestion, not to a PR that only
audits and reconciles evidence already committed elsewhere.

## Source of truth

Task state lives in append-only pull-request comments.

- Marker: `<!-- bannerlord-consolidation-task:v1 -->`
- Payload: one fenced JSON object immediately after the marker.
- Identity: the pair `protocol` + `task_id`.
- Authority: the newest valid v1 comment for that identity wins.
- Author trust: only comments whose GitHub `author_association` is `OWNER`,
  `MEMBER`, or `COLLABORATOR` are authoritative.
- Ordering: compare `(created_at, comment_id)` so the higher numeric comment ID
  wins when two append-only transitions share GitHub's one-second timestamp.
- PR descriptions, labels, review text, chat history, and branch names are not
  substitutes for the protocol comment.
- Protocol comments must not be edited. Publish a new full-state comment for
  every transition.

## Required payload

```json
{
  "protocol": "bannerlord-consolidation-task",
  "version": 1,
  "task_id": "realm-paladin-historical-consolidation",
  "status": "pending",
  "branch": "data/consolidate-realm-paladin",
  "workflow": "historical_consolidation",
  "consolidation_path": "data/combat_observations/consolidations/realm-paladin/CONSOLIDATION_TASK.md",
  "required_actions": [
    "read_consolidation_contract",
    "verify_pinned_sources",
    "audit_repository_history",
    "reconcile_authoritative_queue",
    "validate_latest_head",
    "publish_final_protocol_state"
  ],
  "completion": {
    "action": "merge",
    "merge_method": "squash"
  },
  "blockers": []
}
```

Required fields:

- `protocol`: exactly `bannerlord-consolidation-task`;
- `version`: integer `1`;
- `task_id`: stable identifier reused by every state transition;
- `status`: one of the allowed states below;
- `branch`: PR head branch;
- `workflow`: exactly `historical_consolidation`;
- `consolidation_path`: committed task contract or state document;
- `required_actions`: complete machine-readable action list;
- `completion.action`: `merge`, `close`, or `none`;
- `completion.merge_method`: required for merge and one of `squash`, `merge`,
  or `rebase`;
- `blockers`: current blockers, empty when none.

Additional source identities, queue paths, acceptance criteria, and audit
metadata may be included.

Every comment-supplied path that the executor may read must be normalized
repository-relative POSIX syntax. Absolute paths, `.` or `..` components,
backslashes, drive-qualified paths, and other repository escapes are invalid.
After checkout, the executor must also confirm that required paths resolve to
committed files under the repository root.

## States

- `pending`: the consolidation is ready for repository audit.
- `in_progress`: an agent has claimed the task.
- `blocked`: a required consolidation action cannot complete; blockers must be
  explicit.
- `complete`: the consolidation contract and merge gates passed.
- `cancelled`: no further work or merge is expected.

Allowed transitions:

```text
pending -> in_progress -> complete
pending -> blocked
in_progress -> blocked
blocked -> in_progress
pending|in_progress|blocked -> cancelled
```

A state transition repeats the complete payload with the same `task_id`.

## Dispatcher behavior

`discover_analysis_tasks.py` supports both:

```text
bannerlord-analysis-task:v1
bannerlord-consolidation-task:v1
```

The JSON result exposes `task_protocol` and `task_kind`. A blocked consolidation
remains actionable so the next agent can check whether its blocker has become
resolvable.

Marked comments from untrusted author associations are invalid and produce a
warning rather than a task. Equal-second comments are ordered by numeric comment
ID, independently of API page or response order.

A zero count for analysis tasks is not a zero count for all repository work.
The dispatcher must consider both supported protocols before reporting an empty
queue.

## Local agent workflow

For a returned consolidation task:

1. verify that `branch` equals the PR head;
2. check out and update that branch;
3. read `AGENTS.md`, this protocol, and `consolidation_path`;
4. publish a full-state `in_progress` comment before material edits;
5. verify every pinned repository source by path, ref/commit, Git blob SHA, and
   declared context/cohort boundaries;
6. recompute every derived metric;
7. audit repository history and already-committed evidence without requiring a
   local raw ZIP merely to validate known committed rows;
8. keep remembered but unrecovered evidence non-numeric;
9. update the authoritative troop-test queue;
10. run task-specific tests and latest-head review;
11. publish a full-state `blocked` or `complete` comment;
12. execute the declared completion action only when its gates pass.

If previously unpublished screenshots or a ZIP are actually recovered, they
must enter through the ordinary new-evidence ingestion workflow before changing
consolidated totals.

## Merge safety

Do not publish `complete` or merge when:

- a pinned source identity does not match;
- copied evidence differs from its source;
- arithmetic validation fails;
- the authoritative queue conflicts with the consolidation decision;
- unrelated runtime, scoring, model, or evidence-bundle changes are present;
- a required repository audit remains unfinished;
- an explicit blocker still prevents the declared consolidation outcome.

The absence of raw screenshots is not itself a blocker when the consolidation
only claims already-committed aggregate evidence and records the missing history
as a limitation or verification hold.

## Versioning

Breaking schema or state-semantics changes require a new marker and document,
such as `bannerlord-consolidation-task:v2`. Version 1 comments remain parseable
under this document.
