# Agent workflow

## One batch, one pull request, two agents

Every new evidence batch must use one branch and one draft pull request from ingestion through analysis. The work is split into two explicitly separate phases owned by different agents.

The normalization agent must not perform the analytical phase. The analysis agent must not silently rewrite normalized evidence.

## Phase 1 — normalization agent

The normalization agent must:

1. preserve source provenance and calculate SHA-256 hashes;
2. store every source and generated artifact in the repository;
3. use Git LFS for large binary source files when available;
4. otherwise publish a reconstructible chunked archive with a manifest, reconstruction commands, and expected hash;
5. normalize the source into deterministic structured records;
6. keep player and enemy sides separate;
7. keep field, siege attack, and siege defense separate;
8. preserve uncertain values in an explicit review queue instead of guessing;
9. run structural validation;
10. generate `handoff/ANALYSIS_PROMPT.md` for the local analysis agent;
11. publish a valid `bannerlord-analysis-task:v1` PR comment with status `pending`;
12. leave the pull request in draft state with the analysis phase unchecked.

The normalization agent must not publish rankings, gameplay conclusions, causal claims, model recalibration, or recommendations as part of Phase 1.

A PR is not in the local analysis queue until its protocol comment exists. The PR body, labels, linked issue, and chat history are not substitutes for the comment.

## Phase 2 — local analysis agent

The local analysis agent must:

1. check out the same branch and continue the same pull request;
2. read the batch-specific `handoff/ANALYSIS_PROMPT.md` before changing files;
3. verify source and normalized hashes;
4. treat normalized artifacts as immutable inputs;
5. record corrections in a separate reviewed layer with provenance;
6. resolve troop identities only against versioned track audits;
7. write analytical outputs under the batch `analysis/` directory;
8. use separate commits that identify the analysis phase;
9. publish append-only protocol comments for `in_progress`, `blocked`, or `complete` state;
10. update the pull-request checklist and analytical summary;
11. mark the pull request ready only after all acceptance checks pass;
12. merge completed PRs using the method declared in the protocol comment.

## Operator command: `Fecha as análises`

When the user says `Fecha as análises`, treat it as an explicit instruction to process the repository analysis queue end to end. Do not ask which PRs to inspect.

From the repository root, first run:

```bash
python scripts/analysis/discover_analysis_tasks.py --json
```

Then, for every actionable task returned:

1. confirm the latest valid protocol comment is version 1 and its branch matches the PR head;
2. check out and update that branch;
3. read `AGENTS.md`, the protocol comment, and its `handoff_path`;
4. publish a new full-state `in_progress` comment before material work;
5. complete all required actions and repository validation;
6. publish a new full-state `blocked` comment when execution cannot safely finish;
7. otherwise publish a new full-state `complete` comment;
8. mark the PR ready when it is still draft;
9. merge it using `completion.merge_method` when `completion.action` is `merge`;
10. verify the PR is no longer open before processing the next task.

Do not rely on stale PR-body checklists to determine task state. For each `task_id`, the newest valid `bannerlord-analysis-task:v1` comment is authoritative. Protocol comments are append-only and must not be edited.

Open PRs without a valid protocol comment are outside this workflow and must be ignored. Tasks in `blocked` state remain visible and should be retried only after checking whether their recorded blockers can now be resolved.

Protocol specification:

- `docs/protocols/analysis-task-v1.md`
- dispatcher: `scripts/analysis/discover_analysis_tasks.py`

## Repository layout for new batches

```text
data/combat_observations/<batch-id>/
├── README.md
├── source/
│   ├── README.md
│   ├── manifest.sha256
│   └── source archive, Git LFS pointer, or reconstructible parts
├── normalized/
│   ├── normalized records
│   ├── validation_report.json
│   └── artifact_hashes.csv
├── review/
│   └── review_queue.csv
├── handoff/
│   └── ANALYSIS_PROMPT.md
└── analysis/
    ├── ANALYSIS_REPORT.md
    ├── generated tables
    ├── validation_report.json
    └── artifact_hashes.csv
```

Existing batches may retain their current layout. New work must follow this structure unless a documented migration requires otherwise.

## Immutability and corrections

After Phase 1 is declared complete, normalized files are immutable. Any correction must be additive and auditable:

- keep the original normalized record;
- add a reviewed correction or exclusion record;
- identify the source row and reason;
- regenerate downstream outputs;
- update manifests and hashes;
- never overwrite uncertain evidence without provenance.

## Mandatory analytical boundaries

- Minimum display gate: **5 independent battles and 20 deployed troops**.
- The battle is the independent sampling unit.
- Player-side and enemy-side observations must not be pooled.
- Field, siege attack, and siege defense must remain separate.
- Realm of Thrones, vanilla/War Sails, and other mod tracks must not be silently mixed.
- Provisional labels are not canonical XML IDs.
- Off-screen rows must not be inferred.
- Heroes are excluded from ordinary troop rankings.
- `analysis/model_versions/` is frozen unless a dedicated model-change pull request passes the documented gates.

## Merge gate

A batch pull request remains draft after normalization. It may be marked ready and merged only when:

- source evidence is repository-addressable;
- normalization and structural validation are complete;
- the analysis prompt is committed;
- the latest protocol comment for the task is `complete`;
- the local agent has completed and validated the analysis;
- normalized hashes still match the Phase 1 handoff;
- unresolved limitations are documented;
- no track, side, or battle-context boundary was violated.
