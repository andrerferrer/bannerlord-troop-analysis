# Phase 1 workflow

Read the repository `AGENTS.md`, `docs/methodology/ADR-001-combat-image-normalization.md`, `docs/methodology/ADR-002-two-agent-batch-workflow.md`, and `docs/protocols/analysis-task-v1.md` before material work.

```text
source SHA-256 and safe preflight
→ deterministic image inventory
→ screen extraction with raw provenance
→ schema and arithmetic checks
→ normalized records separated by side, track, and context
→ explicit unresolved review queue
→ structural validation
→ deterministic normalized archive and per-artifact hashes
→ batch-specific ANALYSIS_PROMPT.md
→ ANALYSIS_TASK_V1.json pending mirror
→ executable Phase 1 handoff validation
→ one draft PR and one pending protocol comment
→ stop for a different local analysis agent
```

The portable runner may leave `extraction/extraction_queue.jsonl` for host vision. That queue is resumable work, not a publishable handoff. Do not publish until the final repository batch and reconstructed archive pass `validate_phase1_handoff.py`.

Do not provide a troop registry, corrections, aliases, or model snapshots to the Phase 1 runner. Those inputs belong to Phase 2.
