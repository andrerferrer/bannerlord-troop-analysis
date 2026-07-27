# Analysis task comment protocol v1

## Purpose

Open pull requests are the work queue for local analysis. A pull request is considered an analysis task only when its conversation contains a valid versioned protocol comment.

The local operator instruction is intentionally minimal:

```text
Fecha as análises.
```

The local analysis agent must then discover all open pull requests, read their protocol comments, execute actionable tasks, publish completion state, and merge completed pull requests.

## Source of truth

Task state lives in append-only pull-request comments.

- Marker: `<!-- bannerlord-analysis-task:v1 -->`
- Payload: one fenced JSON object immediately after the marker.
- Identity: `task_id`.
- Authority: the newest valid v1 comment for the same `task_id` wins.
- Open PRs without a valid task comment are ignored by the analysis dispatcher.
- PR titles, labels, descriptions, issues, and chat history are not authoritative task state.
- Protocol comments must not be edited after publication. Publish a new full-state comment instead.

## Required payload

```json
{
  "protocol": "bannerlord-analysis-task",
  "version": 1,
  "task_id": "stable-batch-or-analysis-id",
  "status": "pending",
  "branch": "branch-containing-the-work",
  "handoff_path": "repository/path/to/ANALYSIS_PROMPT.md",
  "normalization_commit": "full-git-commit-sha",
  "required_actions": [
    "verify_handoff_hashes",
    "complete_review_layer",
    "generate_analysis_outputs",
    "validate_and_merge"
  ],
  "completion": {
    "action": "merge",
    "merge_method": "squash"
  },
  "blockers": []
}
```

Required fields:

- `protocol`: exactly `bannerlord-analysis-task`;
- `version`: integer `1`;
- `task_id`: stable identifier reused by every state transition;
- `status`: one of the allowed states below;
- `branch`: PR head branch that the local agent must check out;
- `handoff_path`: committed prompt containing the batch-specific work contract;
- `normalization_commit`: immutable Phase 1 handoff commit;
- `required_actions`: complete machine-readable action list;
- `completion.action`: normally `merge`;
- `completion.merge_method`: `squash`, `merge`, or `rebase`;
- `blockers`: current blockers, empty when none.

Additional hashes, paths, acceptance criteria, and metadata may be included without changing protocol version 1.

## States

- `pending`: Phase 1 is complete enough for the local agent to start.
- `in_progress`: a local agent has claimed the task and is executing it.
- `blocked`: execution cannot complete; `blockers` must explain why.
- `complete`: analysis and merge gates passed. The agent may perform the declared completion action.
- `cancelled`: no further work or merge is expected.

Allowed transitions:

```text
pending -> in_progress -> complete
pending -> blocked
in_progress -> blocked
blocked -> in_progress
pending|in_progress|blocked -> cancelled
```

A completion or blocker update must repeat the entire payload with the same `task_id`; partial update comments are invalid.

## Local dispatcher

From the repository root:

```bash
python scripts/analysis/discover_analysis_tasks.py
```

Machine-readable output:

```bash
python scripts/analysis/discover_analysis_tasks.py --json
```

The dispatcher scans every open PR and returns tasks whose latest state is `pending`, `in_progress`, or `blocked`.

The local analysis agent must, for each returned task:

1. verify that the comment branch equals the PR head branch;
2. check out and update that branch;
3. read `handoff_path` and repository `AGENTS.md`;
4. publish a new `in_progress` protocol comment before material analysis work;
5. execute and validate every required action;
6. publish either a full `blocked` or full `complete` protocol comment;
7. for `complete`, mark the PR ready when necessary and merge using the declared method;
8. verify that the PR is no longer open before moving to the next task.

## Merge safety

The agent must not publish `complete` or merge when:

- normalized inputs differ from the handoff hashes;
- required repository artifacts are absent;
- validation fails;
- frozen model files changed outside a dedicated model-change task;
- a track, side, or battle-context boundary was violated;
- unresolved blockers remain.

A blocked task remains an open draft PR and continues to appear in dispatcher output.

## Versioning

Breaking schema or state-semantics changes require a new marker and document, such as `bannerlord-analysis-task:v2`. Version 1 comments remain parseable under this document.