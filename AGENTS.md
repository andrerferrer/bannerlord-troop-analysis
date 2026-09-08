# Agent workflow

## Git authorization (standing)

In this repository (`bannerlord-troop-analysis`), agents may **commit, push,
create pull requests, mark them ready, and merge them after the repository gates
pass** by default when finishing a slice of work. Do not wait for per-step
publication approval. Still never force-push to `main`/`master`, never skip
hooks, and never commit secrets or unrelated untracked files (for example
`arquivo.md`) unless explicitly asked.

## Operator command: combat-evidence upload

When the user attaches Bannerlord battle-result screenshots or a ZIP containing
them for this project, treat the upload itself as the operator command and
authorization to execute the complete repository workflow. Without asking for
per-batch or per-step confirmation, agents must normalize the evidence, commit
and publish the batch branch, create or update its single draft pull request,
publish the analysis-task protocol comments, run Phase 2 with the required
separate agent, validate, mark the pull request ready, merge it after all gates
pass, and verify the merge. A short conversational question accompanying the
upload does not narrow this default workflow unless the user explicitly asks
for inspection only, asks to leave the work unpublished/open, or cancels it.

Repository standing authorization does not override a host-platform approval
or permission boundary. If the platform blocks an otherwise authorized action,
report that concrete blocker instead of asking the user to reconfirm the
repository workflow.

## Pull request completion is part of the work

When an agent creates or updates a pull request in this repository, the task is
not complete at push, PR creation, or a pending draft review. The same delivery
must continue through:

1. repository validation;
2. self-review of the latest pushed head;
3. correction and revalidation of actionable findings;
4. an updated PR body and review that match the final head;
5. ready-for-review state after all applicable gates pass;
6. merge using the repository or protocol-declared method; and
7. verification that the PR is no longer open and the merge is present on the
   target branch.

Generic tool or skill defaults that stop after opening a PR or leave a review
pending do not override this repository workflow. Stop short of merge only when
the user explicitly asks to leave the PR open, an applicable gate is genuinely
blocked, or the Phase 1 normalization handoff below requires the PR to remain a
draft for the separate Phase 2 agent. In that last case, the repository's
end-to-end obligation resumes in Phase 2 and ends only after the required review
and merge verification.

## One batch, one pull request, two agents

Every new evidence batch must use one branch and one draft pull request from ingestion through analysis. The work is split into two explicitly separate phases owned by different agents.

The normalization agent must not perform the analytical phase. The analysis agent must not silently rewrite normalized evidence.

## Historical evidence consolidation pull requests

A pull request that only inventories, copies, audits, or reconciles evidence
that was already normalized and analyzed in merged repository artifacts is a
**historical consolidation**, not a new evidence batch.

A historical consolidation must declare that classification in its durable
machine-readable state and must pin every reused source by repository path,
commit/ref, Git blob SHA, and compatible track/context/cohort boundaries.

For a historical consolidation:

- do not invoke the new-evidence Phase 1 validator merely because the PR concerns
  combat evidence;
- `screenshots_manifest.csv`, a normalized archive,
  `handoff/ANALYSIS_PROMPT.md`, and `bannerlord-analysis-task:v1` comments are not
  required unless the PR actually introduces previously unpublished raw
  evidence;
- the absence of those Phase 1 artifacts is expected and must not be reported as
  a PR defect;
- do not ask the operator for a local screenshot/ZIP path just to validate an
  already-committed aggregate;
- copy recoverable rows exactly, recompute every derived metric, record missing
  evidence as a limitation or blocker, and update the authoritative troop-test
  queue;
- never infer missing battles or numeric values from memory;
- if previously unpublished screenshots or a ZIP are later recovered, those raw
  inputs must pass the ordinary evidence-ingestion and Phase 1 rules before they
  can change consolidated totals.

An open historical consolidation that requires local continuation must publish
an append-only `bannerlord-consolidation-task:v1` comment and a committed
`consolidation_path`. The shared dispatcher recognizes this protocol without
requiring a Phase 2 handoff. A valid consolidation task is analyzable input; do
not stop with “No analyzable input” merely because no screenshot/ZIP or
`bannerlord-analysis-task:v1` comment exists.

The protocol specification is
`docs/protocols/consolidation-task-v1.md`. The newest valid comment for the same
`protocol` + `task_id` pair is authoritative. Historical consolidations remain
outside the **Phase 2 evidence protocol**, but they are inside the shared local
task queue through their own protocol.

## Phase 1 — normalization agent

The normalization agent must:

1. preserve known source provenance and calculate SHA-256 hashes;
2. compare the batch with committed screenshot history and visually audit the whole batch for duplicate, sequential, improved, or complementary screens; skip and report previously normalized/repeated evidence and keep same-battle screens under one battle ID;
3. store every generated artifact required to reproduce downstream analysis in the repository;
4. publish a deterministic normalized archive with a manifest, reconstruction commands, and expected hash;
5. retain raw screenshots through Git LFS or a reconstructible source package when useful and available, but do not require raw retention after the normalized evidence passes its integrity and validation gates;
6. normalize the source into deterministic structured records;
7. keep player and enemy sides separate;
8. keep field, siege attack, and siege defense separate;
9. preserve uncertain values in an explicit review queue instead of guessing;
10. run structural validation;
11. generate `handoff/ANALYSIS_PROMPT.md` for the local analysis agent;
12. publish a valid `bannerlord-analysis-task:v1` PR comment with status `pending`;
13. leave the pull request in draft state with the analysis phase unchecked.

The normalization agent must not publish rankings, gameplay conclusions, causal claims, model recalibration, or recommendations as part of Phase 1.

A new evidence PR is not in the local analysis queue until its protocol comment exists. The PR body, labels, linked issue, and chat history are not substitutes for the comment.

## Phase 2 — local analysis agent

The local analysis agent must:

1. check out the same branch and continue the same pull request;
2. read the batch-specific `handoff/ANALYSIS_PROMPT.md` before changing files;
3. verify the normalized archive and artifact hashes, plus raw-source hashes when raw evidence is retained;
4. treat normalized artifacts as immutable inputs;
5. record corrections in a separate reviewed layer with provenance;
6. resolve troop identities only against versioned track audits;
7. analyze every visible player-side ordinary troop in every observed context;
8. treat requested focus troops as an additive deep dive, never as a filter on the batch-wide analysis;
9. publish every reliable troop/context row and retain explicit below-gate coverage for every insufficient row;
10. write analytical outputs under the batch `analysis/` directory;
11. use separate commits that identify the analysis phase;
12. publish append-only protocol comments for `in_progress`, `blocked`, or `complete` state;
13. update the pull-request checklist and analytical summary;
14. summarize batch-wide findings before the requested focus in the user-facing handoff;
15. mark the pull request ready only after all acceptance checks pass;
16. merge completed PRs using the method declared in the protocol comment.

## Operator command: `Fecha as análises`

When the user says `Fecha as análises`, treat it as an explicit instruction to process the repository task queue end to end. Do not ask which PRs to inspect.

From the repository root, first run:

```bash
python scripts/analysis/discover_analysis_tasks.py --json
```

The dispatcher returns both `bannerlord-analysis-task:v1` and
`bannerlord-consolidation-task:v1` tasks. Then, for every actionable task
returned:

1. confirm the latest valid protocol comment is version 1 and its branch matches the PR head;
2. check out and update that branch;
3. read `AGENTS.md` and the full protocol comment;
4. for `bannerlord-analysis-task`, read `handoff_path`; for
   `bannerlord-consolidation-task`, read `consolidation_path` and
   `docs/protocols/consolidation-task-v1.md`;
5. publish a new full-state `in_progress` comment before material work;
6. complete all required actions and repository validation under the task's own workflow boundaries;
7. publish a new full-state `blocked` comment when execution cannot safely finish;
8. otherwise publish a new full-state `complete` comment;
9. mark the PR ready when it is still draft and its applicable gates pass;
10. execute `completion.action` with `completion.merge_method` when declared;
11. verify the PR is no longer open before processing the next task.

Do not rely on stale PR-body checklists to determine task state. For each
`protocol` + `task_id` pair, the newest valid supported protocol comment is
authoritative. Protocol comments are append-only and must not be edited.

Open PRs without a valid supported task comment are outside this workflow and
must be ignored. Tasks in `blocked` state remain visible and should be retried
only after checking whether their recorded blockers can now be resolved. A zero
count for Phase 2 analysis tasks is not a zero count for all work; inspect the
shared dispatcher's consolidation tasks before reporting an empty queue.

Protocol specifications:

- `docs/protocols/analysis-task-v1.md`
- `docs/protocols/consolidation-task-v1.md`
- dispatcher: `scripts/analysis/discover_analysis_tasks.py`

## Mandatory analytical boundaries

- Minimum display gate: **5 independent battles and 20 deployed troops**.
- The battle is the independent sampling unit.
- A readable active scoreboard that is the last observation before a fight was
  stopped is a valid battle observation. A later re-engagement or cleanup fight
  is a separate battle, even when it targets a single enemy left by a bug. Never
  combine, subtract, or reconstruct values across those battles. Share one
  `battle_id` only for proven views of the same result table, such as a rare
  complementary scroll split, and deduplicate overlapping rows.
- Player-side and enemy-side observations must not be pooled.
- Field, siege attack, and siege defense must remain separate.
- Realm of Thrones, vanilla/War Sails, and other mod tracks must not be silently mixed.
- Provisional labels are not canonical XML IDs.
- Off-screen rows must not be inferred.
- Heroes are excluded from ordinary troop rankings.
- A requested focus troop must never filter the batch-wide analysis. Every visible
  player-side ordinary troop/context row must appear exactly once in either the
  reliable or insufficient-evidence output and in the human-readable report.
- New scoring work must follow
  [`docs/methodology/006_context_first_scoring_rules.md`](docs/methodology/006_context_first_scoring_rules.md):
  select track, battle context, troop question, attack mode, and mount state
  before choosing the smallest direct driver set. Do not infer a universal score
  from chat examples or from the newest candidate.
- `analysis/model_versions/` is frozen unless a dedicated model-change pull request passes the documented gates.
- Controlled mixed-opponent tests must use a versioned fixed composition and
  remain separate from campaign and homogeneous-test aggregates.

## Merge gate

A new evidence batch pull request remains draft after normalization. It may be marked ready and merged only when:

- the deterministic normalized evidence is repository-addressable and reconstructible;
- normalization and structural validation are complete;
- the analysis prompt is committed;
- the latest protocol comment for the task is `complete`;
- the local agent has completed and validated the analysis;
- normalized hashes still match the Phase 1 handoff;
- unresolved limitations are documented;
- no track, side, or battle-context boundary was violated.
- no visible eligible player-side ordinary troop/context row was omitted from the
  batch-wide analytical outputs or report.

A historical consolidation may be marked ready and merged only when its newest
`bannerlord-consolidation-task:v1` state is `complete`, every pinned source and
derived metric validates, the authoritative queue matches the decision, and any
unrecovered external evidence is represented honestly as a limitation or hold
rather than fabricated numeric data.
