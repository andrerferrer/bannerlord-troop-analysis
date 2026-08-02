# Repository Phase 1 publication

The current repository files are authoritative. Do not duplicate their normative checklists or protocol schema here.

Read exact paths:

- `AGENTS.md` for phase ownership and merge boundaries;
- `docs/methodology/ADR-001-combat-image-normalization.md` for normalization rules;
- `docs/methodology/ADR-002-two-agent-batch-workflow.md` for the handoff contract;
- `docs/protocols/analysis-task-v1.md` for comment authority and payload semantics;
- `.github/pull_request_template.md` for the shared PR body;
- the nearest compatible merged batch for the current artifact layout and batch-specific `required_actions`.

## Required repository shape

The validator requires the batch root to contain the current Phase 1 manifests, summary, validation, review queue, source and bundle documentation, handoff prompt, and pending task mirror. The reconstructible archive must contain every normalized file named by `artifact_hashes.csv`, including the records consumed by the Phase 2 handoff.

`normalization_summary.json` and `validation_report.json` must record the source identity fields consumed by Phase 2. `handoff/ANALYSIS_TASK_V1.json` is a non-authoritative mirror; the newest valid pull-request comment remains task state.

## Git sequence

1. Start one branch from current `main` for exactly one batch.
2. Commit normalized artifacts and `handoff/ANALYSIS_PROMPT.md`; record that full SHA as `normalization_commit`.
3. Add the pending task mirror without changing immutable Phase 1 inputs.
4. Run `validate_phase1_handoff.py` with the exact branch and normalization commit.
5. Push only after the validator passes.
6. Open a draft PR titled `Normalize <date> <track/context> combat batch` using `.github/pull_request_template.md`; leave Phase 2 unchecked.
7. Post the validated task mirror as a new top-level protocol comment. Preserve batch-specific action and metadata extensions; the v1 example in the protocol document is a minimum shape, not a replacement for the handoff.
8. Stop. Do not mark ready or merge.

If local execution, GitHub authentication, or validation is unavailable, report the exact blocked operation. Never claim a write that the host did not confirm and never publish `pending` from an unvalidated connector-only run.
