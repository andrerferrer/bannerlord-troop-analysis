# Repository Phase 1 pull-request workflow

Use this workflow only for a new combat-evidence batch in `andrerferrer/bannerlord-troop-analysis`. The current repository files are authoritative. Re-read `AGENTS.md`, `docs/methodology/ADR-001-combat-image-normalization.md`, `docs/methodology/ADR-002-two-agent-batch-workflow.md`, and `docs/protocols/analysis-task-v1.md` immediately before publishing.

## Boundary

This is the normalization-agent phase only.

Allowed:

- source provenance and SHA-256 manifests;
- deterministic normalized records and reconstructible bundle;
- explicit review queue;
- structural validation;
- batch README and artifact hashes;
- `handoff/ANALYSIS_PROMPT.md`;
- `handoff/ANALYSIS_TASK_V1.json` when used by the nearest merged batch;
- one draft PR and one pending protocol comment.

Forbidden:

- rankings or tier lists;
- gameplay recommendations or conclusions;
- causal claims;
- model recalibration;
- edits under `analysis/model_versions/`;
- silent corrections to normalized evidence;
- pooling tracks, sides, or battle contexts;
- marking the PR ready or merging it.

## 1. Resolve repository and batch identity

1. Confirm the repository is `bannerlord-troop-analysis` and the default branch is `main`.
2. Start from current `main`, not a stale local branch.
3. Inspect the nearest merged batch with the same track/context and match its current layout and schema.
4. Create a stable batch ID and one repository directory under `data/combat_observations/`.
5. Use one branch for one batch, normally:

```text
agent/normalize-combat-YYYY-MM-DD-<track>-<context>-<slug>
```

Do not reuse a branch belonging to another batch or mix infrastructure changes into it.

## 2. Build Phase 1 artifacts

The exact files follow the nearest merged precedent. At minimum, Phase 1 must repository-address:

```text
data/combat_observations/<batch>/
  README.md
  screenshots_manifest.csv
  normalization_summary.json
  review_queue.csv
  validation_report.json
  artifact_hashes.csv
  source/README.md
  bundle/README.md
  bundle/<ordered reconstructible archive chunks>
  handoff/ANALYSIS_PROMPT.md
  handoff/ANALYSIS_TASK_V1.json   # when present in current precedent
```

Requirements:

- preserve original filenames and exact SHA-256 values;
- label duplicate, intermediate, incomplete, and excluded screenshots explicitly;
- keep field, siege attack, and siege defense separate;
- keep player and enemy sides separate;
- never infer off-screen rows;
- leave unreadable values null and route them to review;
- identify heroes/lords/companions without treating them as ordinary ranking rows;
- retain raw screenshots only through the repository-approved storage option; when raw files are not retained, document filenames, hashes, size/provenance when known, and the visual re-review limitation;
- make the normalized archive deterministically reconstructible and document the expected archive SHA-256;
- hash every committed reproducibility-critical artifact.

A partial host-vision queue is not a publishable Phase 1 handoff. Finish the normalized records, bundle, validation, and review queue first.

## 3. Validate before Git writes

Run the current repository validation commands that apply to the batch. At minimum verify:

- all required JSON/JSONL/CSV files parse;
- counts reconcile between summary, records, manifest, and validation report;
- all hashes match;
- the archive reconstructs to the expected SHA-256;
- no duplicated image is silently counted as a new battle;
- no track/side/context boundary was crossed;
- `analysis/model_versions/` is unchanged;
- no analytical output was added in Phase 1.

Record unavailable tests honestly. Do not convert an unrun test into a pass.

## 4. Commit and open the draft PR

1. Create the branch from current `main`.
2. Add only the batch artifacts.
3. Commit Phase 1 with a message that identifies normalization, for example:

```text
feat(combat_observations): normalize <batch summary>
```

4. Capture the full normalization commit SHA.
5. Push the branch or use the connected GitHub write tool.
6. Open one **draft** PR against `main`.

Recommended title:

```text
Normalize and analyze <date> <track/context> combat batch
```

The PR body is descriptive, not authoritative task state. Include:

- batch ID, track, version, contexts, screenshot/battle counts;
- source and normalized-archive hashes;
- Phase 1 checklist;
- source-retention limitation;
- explicit statement that Phase 2 remains pending and model files are unchanged.

Do not add the analysis-task marker to the PR body.

## 5. Publish the authoritative pending task comment

After the PR exists and the normalization commit SHA is final, publish one new top-level PR comment. Do not edit protocol comments after publication.

Use the current protocol document as the schema authority. The comment must have exactly this structure:

````markdown
<!-- bannerlord-analysis-task:v1 -->
```json
{
  "protocol": "bannerlord-analysis-task",
  "version": 1,
  "task_id": "<stable batch id>",
  "status": "pending",
  "branch": "<exact PR head branch>",
  "handoff_path": "data/combat_observations/<batch>/handoff/ANALYSIS_PROMPT.md",
  "normalization_commit": "<full commit SHA>",
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
````

Before posting, verify:

- `branch` exactly equals the PR head;
- `handoff_path` exists in that commit;
- `normalization_commit` is a full SHA containing the Phase 1 handoff;
- the JSON is valid;
- status is `pending`;
- blockers are empty only when the local analysis agent can start.

A draft PR without this valid comment is not in the analysis queue.

## 6. Stop at the handoff

After the pending comment:

- leave the PR draft;
- do not produce analysis files;
- do not publish rankings in the PR or chat as Phase 1 output;
- do not mark ready;
- do not merge;
- return the branch, normalization commit, PR number/link, task ID, and any unresolved review count.

## Write failure handling

When GitHub authentication or repository write access fails:

1. keep the validated artifacts unchanged;
2. preserve any local branch/commit already created;
3. report the exact failed operation and error;
4. provide the exact next command or connector action;
5. never claim that a branch, commit, PR, or comment exists unless the write succeeded.

Never force-push `main`, bypass hooks, commit secrets, or include unrelated untracked files.
