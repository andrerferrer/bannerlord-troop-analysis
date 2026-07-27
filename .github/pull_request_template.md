## Batch

- Batch ID:
- Game track:
- Game/mod version:
- Source SHA-256:
- Normalized archive SHA-256:

## Phase 1 — normalization agent

- [ ] Normalized evidence is repository-addressable and reconstructible.
- [ ] Raw-source retention status and known provenance are documented.
- [ ] Source manifest and hashes are committed.
- [ ] Normalized records and validation are committed.
- [ ] Side, track, and battle-context boundaries remain separate.
- [ ] Uncertain values are queued rather than guessed.
- [ ] `handoff/ANALYSIS_PROMPT.md` is committed.
- [ ] A valid `bannerlord-analysis-task:v1` comment with status `pending` is published.
- [ ] No analysis or frozen-model changes were introduced.

Normalization agent / tool:

Normalization handoff commit:

Analysis task ID:

## Phase 2 — local analysis agent

- [ ] Latest protocol state changed to `in_progress` before material work.
- [ ] Handoff hashes verified.
- [ ] Normalized artifacts remain byte-for-byte unchanged.
- [ ] Corrections use a separate reviewed layer.
- [ ] Required analysis outputs, validation, and hashes are committed.
- [ ] Frozen model files remain unchanged.
- [ ] A full-state `complete` protocol comment is published.

Analysis agent / tool:

Analysis completion commit:

## Findings

Pending local analysis.

## Merge gate

- [ ] Phase 1 complete.
- [ ] Phase 2 complete.
- [ ] Latest valid protocol state is `complete`.
- [ ] Completion action executed.

The PR body is descriptive. The newest valid protocol comment for the task ID is authoritative.
