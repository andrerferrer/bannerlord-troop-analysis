# Repository Phase 1 publication

The current repository files are authoritative. Do not duplicate their normative checklists or protocol schema here.

Read exact paths:

- `AGENTS.md` for phase ownership and merge boundaries;
- `docs/methodology/ADR-001-combat-image-normalization.md` for normalization rules;
- `docs/methodology/ADR-002-two-agent-batch-workflow.md` for the handoff contract;
- `docs/protocols/analysis-task-v1.md` for comment authority and payload semantics;
- `.github/pull_request_template.md` for the shared PR body;
- the nearest compatible merged batch only for track-specific handoff details and additional `required_actions`.

## Required repository shape

The executable validator, not a historical batch, defines the artifact layout for new handoffs. The batch root contains the Phase 1 manifests, summary, validation, review queue, source and bundle documentation, handoff prompt, pending task mirror, and ordered Base64 archive parts.

The archive has one top-level directory and contains:

- `README.md`, `screenshots_manifest.csv`, and `battles.jsonl`;
- `troop_occurrences.jsonl`, `primary_troop_occurrences.jsonl`, and `troop_battle_consolidated.jsonl`;
- `review_queue.csv`, `normalization_summary.json`, and `validation_report.json`;
- one archive-scoped `artifact_hashes.csv` that covers every other archive file and excludes itself.

Optional Phase 1 material is limited to `screenshots.jsonl`, `combat_troop_occurrence.schema.json`, files beneath `extraction/`, `provenance/`, and `schemas/`, or raw archive/image/hash material beneath `source/`. Other archive paths are rejected. At the batch root, only the required files plus those narrowly typed retained-source files and ordered bundle parts are permitted; analytical/review/report layouts cannot be smuggled into the normalization commit.

The batch-root manifest, summary, review queue, validation report, and artifact hash manifest are byte-identical mirrors of their archive members. `bundle/README.md` records exactly one expected reconstructed-archive SHA-256, and `source/README.md` records the verified source SHA-256. Analysis, review, canonical, ranking, historical-aggregate, and model-comparison outputs are forbidden inside the Phase 1 archive.

`normalization_summary.json` and `validation_report.json` record the source identity and counts consumed by Phase 2; their counts must match the actual JSONL and CSV records. Battles must agree on one declared track/version and a supported context. Primary rows must be value-identical records from the all-occurrence layer, and consolidated values must be derived from those primary rows without context drift. `deployed` equals survivors + deaths + wounded; routed remains a separate metric. `handoff/ANALYSIS_TASK_V1.json` is a non-authoritative mirror; the newest valid pull-request comment remains task state.

For new pending handoffs, `required_actions` includes the integrity, immutable-input, reviewed-layer, identity-resolution, frozen-model, and merge actions enforced by the validator, plus either `generate_analysis_outputs` or the established `generate_reliable_and_complete_rankings` action. Add track-specific actions from a compatible precedent; never replace the current semantic minimum with a historical list.

## Git sequence

1. Start one branch from current `main` for exactly one batch.
2. Commit normalized artifacts and `handoff/ANALYSIS_PROMPT.md`; record that full SHA as `normalization_commit`.
3. Add the pending task mirror without changing immutable Phase 1 inputs.
4. Run `validate_phase1_handoff.py` with the exact branch and normalization commit. The validator derives the canonical mainline ref and does not accept a caller-controlled base.
5. Push only after the validator passes.
6. Open a draft PR titled `Normalize <date> <track/context> combat batch` using `.github/pull_request_template.md`; leave Phase 2 unchecked.
7. Post the validated task mirror as a new top-level protocol comment. Preserve batch-specific action and metadata extensions without replacing the validator's semantic minimum.
8. Stop. Do not mark ready or merge.

If local execution, GitHub authentication, or validation is unavailable, report the exact blocked operation. Never claim a write that the host did not confirm and never publish `pending` from an unvalidated connector-only run.
