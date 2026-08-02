# Phase 2 workflow

The repository `AGENTS.md`, the newest valid pull-request protocol comment, and the batch-specific `handoff/ANALYSIS_PROMPT.md` are authoritative, in that order.

## Queue path

```text
discover actionable protocol comments
→ verify PR head equals comment branch
→ check out and update the existing branch
→ read the committed handoff
→ publish in_progress
→ verify archive, artifact, and retained-source hashes
→ preserve normalized inputs byte-for-byte
→ add reviewed corrections/exclusions
→ resolve identities against the declared track audit
→ aggregate by side and battle context
→ apply the 5-battle / 20-deployed display gate
→ write review/ and analysis/ outputs
→ validate hashes, boundaries, and frozen models
→ publish complete or blocked
→ ready and merge only after complete
```

Start queue discovery with:

```bash
python scripts/analysis/discover_analysis_tasks.py --json
```

Use the commands committed in each task's `handoff/ANALYSIS_PROMPT.md`. The repository contains batch-specific Phase 2 tooling such as `scripts/analysis/analyze_normalized_combat_batch.py`; do not substitute the portable Phase 1 runner.

## Stop conditions

Publish `blocked` rather than continuing when:

- the newest protocol comment is invalid or names another branch;
- the handoff is absent;
- a source or normalized hash differs;
- required files are absent;
- the track audit is missing or incompatible;
- normalized evidence changed after handoff;
- frozen model files changed;
- side, track, or battle-context boundaries cannot be preserved.
- the normalized package is unpublished and has no committed Phase 1 handoff.
