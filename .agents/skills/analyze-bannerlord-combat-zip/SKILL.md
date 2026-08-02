---
name: analyze-bannerlord-combat-zip
description: Complete Phase 2 review and analysis for an existing committed Bannerlord combat-evidence handoff or a valid pending bannerlord-analysis-task:v1 pull-request task. Use when given a committed handoff/ANALYSIS_PROMPT.md, an existing analysis-queue PR, the operator command "Fecha as análises", or a request to canonicalize, rank, compare, or resume a published batch after normalization. Do not use for raw screenshots, raw screenshot ZIP normalization, unpublished normalized packages, creation of a new evidence-batch branch or pull request, or publication of a pending Phase 1 task.
---

# Analyze Bannerlord Combat ZIP

Consume the immutable Phase 1 handoff. Never act as the normalization agent.

## Resolve the task

1. Read the repository `AGENTS.md` and `docs/protocols/analysis-task-v1.md`.
2. For `Fecha as análises`, run `python scripts/analysis/discover_analysis_tasks.py --json` and process every actionable task exactly as `AGENTS.md` requires.
3. Otherwise require one of:
   - an open pull request whose newest valid protocol comment is `pending`, `in_progress`, or retryable `blocked`;
   - a committed batch-specific `handoff/ANALYSIS_PROMPT.md` plus its normalized bundle.
4. Reject raw screenshots and raw screenshot ZIPs. Route those to `$normalize-bannerlord-combat-batch` in a separate agent run.

## Execute Phase 2

Read [references/workflow.md](references/workflow.md) before changing files.

- Continue the same branch and pull request.
- Publish `in_progress` before material analysis on a queued task.
- Verify source, archive, and per-artifact hashes before using the data.
- Treat Phase 1 files as byte-for-byte immutable.
- Record corrections and exclusions only in a separate reviewed layer with provenance.
- Resolve identities only against the versioned audit for the declared track.
- Keep track, side, and battle context separate.
- Apply the 5-battle / 20-deployed display gate using battles as the independent unit.
- Write reviewed and analytical outputs only under the batch `review/` and `analysis/` directories.
- Keep `analysis/model_versions/` unchanged.

Follow the batch handoff commands and current repository scripts rather than reproducing formulas or schemas in this skill.

## Complete the task

Read [references/output-contract.md](references/output-contract.md). Publish a full-state `blocked` comment when any required gate cannot pass. Otherwise:

1. commit Phase 2 separately with an `analysis:` or `review:` prefix;
2. update the pull-request checklist and findings;
3. publish the append-only full-state `complete` comment;
4. mark the pull request ready when it is still draft;
5. merge with the method declared by the latest protocol comment;
6. verify the pull request is no longer open.

Never create a new batch pull request, publish a `pending` task, silently rewrite normalized evidence, or let a single agent run own both phases.
