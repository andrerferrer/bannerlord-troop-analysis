# Workflow reference

## Input decision

| Input | Action |
|---|---|
| Direct chat screenshots | Treat the attachment as the operator command. Inspect the rendered images in `host-vision`, use stable host attachment identifiers or deterministic upload order, record unavailable source bytes/hashes explicitly, and publish the first valid Phase 1 commit plus the batch draft PR before any user-facing response. |
| Screenshot ZIP | Run safe ZIP preflight, historical/visual deduplication, then queue/extract only accepted images. |
| Screenshot directory | Manifest files in place, perform historical/visual deduplication, then queue/extract. |
| Eleven normalized Base64 parts | Run strict reconstruction and exact-hash verification. |
| Existing normalized directory | Locate `troop_occurrences.jsonl`; build only with a verified troop registry. |
| Historical consolidation task | Read the newest valid `bannerlord-consolidation-task:v1` comment and its `consolidation_path`. Do not require screenshots, a ZIP, `screenshots_manifest.csv`, or a Phase 2 handoff merely to audit already-committed evidence. |
| Queue question | Read `data/combat_observations/test_queues/<track>.json`; do not infer the queue from chat or the newest batch report. |
| Corrupt/unsupported new input | Stop that input path with an actionable error; never treat it as empty. When safe partial work exists, publish it to the batch draft PR and record the blocker. |

## Task discovery

From the repository root, use the shared dispatcher:

```bash
python3 scripts/analysis/discover_analysis_tasks.py --json
```

It recognizes both:

```text
bannerlord-analysis-task:v1
bannerlord-consolidation-task:v1
```

Inspect `task_protocol` and `task_kind` before choosing a workflow.

- For `analysis`, read `handoff_path` and preserve the Phase 1 normalization commit.
- For `historical_consolidation`, read `consolidation_path` and
  `docs/protocols/consolidation-task-v1.md`.
- A zero Phase 2 count is not enough to declare the queue empty. The command's
  `actionable_count` covers both supported protocols.
- A consolidation task in `pending`, `in_progress`, or `blocked` state is valid
  analyzable input even without a local image/ZIP.

Before concluding that no work exists, inspect the current branch for
`data/combat_observations/consolidations/**/consolidation.json`. If such state
exists but the PR lacks a valid consolidation task comment, publish the missing
comment instead of asking for screenshots.

## Queue authority

Read `data/combat_observations/test_queues/README.md` and the relevant track JSON before interpreting a new batch, processing a historical consolidation, or answering what should be tested next.

- The track JSON is authoritative for the cross-batch queue.
- Batch-local `analysis/NEXT_TEST_RECOMMENDATION.md` files and PR text are proposals/history until the same merged change updates the queue.
- The newest valid trusted `bannerlord-analysis-task:v1` comment is authoritative for one new evidence batch's execution state.
- The newest valid trusted `bannerlord-consolidation-task:v1` comment is authoritative for one historical consolidation's execution state.
- Trust only `OWNER`, `MEMBER`, or `COLLABORATOR` comments; order equal-second
  transitions by numeric comment ID and reject comment-supplied paths that are
  not normalized repository-relative POSIX paths.
- `verification_holds` are not recommendations.
- An empty `ordered_queue` means no future target is approved.
- The working-branch queue controls continuation of its PR; `main` controls unrelated sessions.

## Publication order — new evidence

1. Resolve the repository and read `AGENTS.md`.
2. Read the relevant track queue and determine whether the uploaded evidence belongs to its `active_test`, a pending open batch PR, or a new operator-selected target.
3. Treat the screenshot upload itself as authorization to process and publish the batch.
4. Reuse an existing branch/PR when the evidence belongs to an open batch; otherwise create one batch branch.
5. Complete enough Phase 1 work to create durable source provenance, screenshot inventory, visual deduplication audit, current batch state, and handoff/protocol artifacts.
6. Phase 1 may confirm or set the queue's `active_test`; it must not select or reorder future targets from preliminary results.
7. Commit and push that state, then create or update the batch's single draft pull request.
8. Only after the pull request exists may the agent send a normal progress response. Continue the same delivery through the remaining repository workflow and merge gates unless explicitly instructed to leave the PR open.
9. Phase 2 must reconcile its final recommendation with the track queue. Update the queue in the same PR whenever the completed analysis closes, parks, holds, activates, or queues a troop.
10. A missing mounted file or unavailable source-byte hash is an integrity limitation, not permission to remain chat-only. Preserve it as an explicit state and continue every safe step.
11. If GitHub publication itself fails, report the exact failed action and platform error. Do not substitute preliminary prose for the missing pull request.

## Publication order — historical consolidation

1. Verify the PR head branch and newest valid consolidation protocol comment.
2. Read `AGENTS.md`, `docs/protocols/consolidation-task-v1.md`, and
   `consolidation_path`.
3. Publish an append-only full-state `in_progress` comment before material work.
4. Verify every reused source by repository path, ref/commit, Git blob SHA, and
   compatible track/context/cohort boundaries.
5. Copy recoverable evidence exactly and recompute every derived value.
6. Audit repository history without requiring a raw local ZIP merely to validate
   an already-committed aggregate.
7. Preserve remembered but unrecovered evidence as non-numeric history.
8. Reconcile the authoritative track queue.
9. Run task-specific validation and latest-head review.
10. Publish `blocked` or `complete` as a new full-state protocol comment.
11. Execute the declared completion action only when the consolidation gates
    pass.

If previously unpublished screenshots are actually recovered, ingest them under
the ordinary new-evidence workflow before they change consolidated totals.

## Modes

`offline-existing` performs deterministic verification, correction application, canonical build, rankings, and comparison without model calls.

`host-vision` uses the current session to inspect queued local images or directly attached chat screenshots. For each image:

1. read the full screen rather than standalone OCR;
2. emit strict structured rows, including visible side-total and party rows;
3. leave unreadable fields null;
4. retain raw response/provenance;
5. validate schema and arithmetic;
6. route uncertain/invalid rows to review;
7. checkpoint before the next batch.

For directly attached screenshots without local bytes, retain the host attachment identifier or deterministic upload-order identifier and mark byte size/SHA-256 as unavailable. Never invent a hash or claim the local invocation script read those images. This condition can block final integrity completion, but it does not block visual extraction, committed structured artifacts, or opening the draft pull request.

Before row extraction, compare every screenshot with committed history and with the other screenshots in the batch. Inspect the actual scoreboard: same sides, party headings, totals, troop rows, result state, battle timer, and environment. Write `reports/screenshot_deduplication_audit.csv`. Skip prior normalized and repeated screens; group supplemental or sequential screens only when they show the same actual battle. Accept the best/latest readable active scoreboard when it is the final observation before that fight was stopped. Give any later re-engagement or cleanup fight a new `battle_id`, and never combine or reconstruct values across the two battles.

`api-batch` uses configured extractor/reviewer adapters. Require explicit upload/paid authorization, bounded retries/concurrency, and a usage estimate or cap. Exact provider models are configuration values.

`historical-consolidation` is a repository workflow, not an extraction mode. It operates only on pinned committed sources and the task's explicit state. Do not invoke the screenshot pipeline when no new raw evidence is being added.

## New-evidence phase sequence

```text
read authoritative track queue
→ preflight and SHA-256, or explicit byte-hash-unavailable host provenance
→ safe staging or inline host-vision inventory
→ committed-history lookup by hash and capture identity
→ full-batch visual duplicate/same-battle audit
→ interrupted-versus-new-battle classification
→ Phase 1 may confirm/set active_test only
→ durable Phase 1 checkpoint commit
→ create/update the single draft pull request
→ screen extraction
→ schema and semantic validation
→ troop matching
→ review queue and explicit decisions
→ conservative deduplication
→ canonical occurrence build
→ context aggregates, kill-total coverage, and evidence grades
→ separate efficiency and share-adjusted-impact ranks in complete/reliable rankings
→ frozen-model comparison
→ reconcile final recommendation with historical evidence
→ atomically update the authoritative track queue
→ validate queue invariants and artifact index/state
→ repository self-review, ready state, merge, and merge verification when gates pass
```

## Historical-consolidation sequence

```text
discover bannerlord-consolidation-task:v1
→ read consolidation_path
→ publish in_progress state
→ verify pinned committed sources
→ verify exact copied evidence
→ recompute all metrics
→ audit repository history and compatibility
→ preserve unrecovered memory as non-numeric
→ reconcile authoritative queue
→ validate dispatcher, artifacts, and PR scope
→ publish blocked or complete state
→ ready/merge/verify when complete
```

Do not advance ranking-critical unresolved values into the primary dataset. Preserve partial hierarchy evidence. Do not return a chat-only preliminary analysis while no batch pull request exists. Do not merge a completed analysis whose recommendation changed but whose track queue remained stale. Do not report a historical consolidation as input-less when it has a valid protocol comment and task path.

## Queue validation

Before merge, verify:

- valid JSON and declared schema version;
- at most one `active_test`;
- unique integer priorities in `ordered_queue`;
- no troop/context appears simultaneously as active, queued, held, parked, or closed;
- every queue transition records a reason and evidence reference;
- an explicit operator decision is preserved rather than overwritten by an inferred recommendation;
- empty `ordered_queue` is treated as no approved next troop.

## Common commands

Discover every supported repository task:

```bash
python3 scripts/analysis/discover_analysis_tasks.py --json
```

Prepare or resume new evidence when a local path exists:

```bash
python3 scripts/invoke_pipeline.py \
  --input "/path/to/input.zip" \
  --output "/path/to/output" \
  --mode host-vision \
  --repo "/path/to/bannerlord-troop-analysis"
```

For inline-only screenshots, create the equivalent host-vision inventory and structured extraction artifacts directly from the rendered images, without claiming a local-byte preflight. Commit those artifacts and explicit provenance to the batch branch before opening the draft PR.

Complete deterministic build from normalized records:

```bash
python3 scripts/invoke_pipeline.py \
  --input "/path/to/normalized" \
  --output "/path/to/output" \
  --mode offline-existing \
  --repo "/path/to/bannerlord-troop-analysis" \
  --troop-registry "/path/to/track/troops.csv" \
  --corrections "/path/to/review_corrections.jsonl" \
  --aliases "/path/to/troop_aliases.csv" \
  --general-model "/path/to/v7.1.csv" \
  --burst-model "/path/to/v7.3.csv"
```

When incomplete, return the existing PR, current supported task protocol, task/state path, authoritative queue path, explicit blocker, and the exact command needed to resume that workflow.
