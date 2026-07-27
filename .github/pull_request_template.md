## Batch

- Batch ID:
- Game track:
- Game/mod version:
- Source SHA-256:
- Normalized archive SHA-256:

## Phase 1 — normalization agent

- [ ] Source evidence is repository-addressable through Git LFS, ordinary Git, or a reconstructible archive.
- [ ] Source manifest and hashes are committed.
- [ ] Normalized records are committed.
- [ ] Player and enemy sides remain separate.
- [ ] Field, siege attack, and siege defense remain separate.
- [ ] Uncertain values are in the review queue rather than guessed.
- [ ] Structural validation passes or all failures are documented.
- [ ] Normalized artifact hashes are committed.
- [ ] `handoff/ANALYSIS_PROMPT.md` is committed.
- [ ] A valid append-only `bannerlord-analysis-task:v1` comment with status `pending` is published.
- [ ] No rankings, conclusions, or model changes were introduced during normalization.

Normalization agent / tool:

Normalization handoff commit:

Analysis task ID:

Protocol: [`docs/protocols/analysis-task-v1.md`](../docs/protocols/analysis-task-v1.md)

## Phase 2 — local analysis agent

- [ ] Latest protocol state was changed to `in_progress` before material work.
- [ ] Handoff hashes were verified before analysis.
- [ ] Normalized artifacts remain byte-for-byte unchanged.
- [ ] Corrections and exclusions are stored in a separate reviewed layer.
- [ ] Canonical identities use versioned track-audit evidence.
- [ ] The 5-battle / 20-deployed display gate is enforced.
- [ ] Insufficient-evidence rows are reported.
- [ ] Track, side, and context boundaries remain intact.
- [ ] Analysis report, generated tables, validation, and hashes are committed.
- [ ] Frozen model files under `analysis/model_versions/` are unchanged.
- [ ] Findings and limitations are summarized below.
- [ ] A full-state `complete` protocol comment is published.

Analysis agent / tool:

Analysis completion commit:

## Findings

Pending local analysis.

## Merge gate

- [ ] Phase 1 complete.
- [ ] Phase 2 complete.
- [ ] Latest valid protocol state is `complete`.
- [ ] All required artifacts live in the repository.
- [ ] PR is ready for final review and declared completion action.

Keep the PR in draft while any merge-gate item is unchecked.

The PR body is descriptive. The newest valid protocol comment for the task ID is the authoritative execution state.