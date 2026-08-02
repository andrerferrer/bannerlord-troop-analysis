# Workflow reference

## Input decision

| Input | Action |
|---|---|
| Screenshot ZIP | Run safe ZIP preflight, manifest images, then queue/extract |
| Screenshot directory | Manifest files in place, then queue/extract |
| Eleven normalized Base64 parts | Run strict reconstruction and exact-hash verification |
| Existing normalized directory | Locate `troop_occurrences.jsonl`; build only with a verified troop registry |
| Corrupt/unsupported input | Stop that input path with an actionable error; never treat it as empty |

## Modes

`offline-existing` performs deterministic verification, correction application, canonical build, rankings, and comparison without model calls.

`host-vision` uses the current session to inspect queued images. For each image:

1. read the full screen rather than standalone OCR;
2. emit strict structured rows;
3. leave unreadable fields null;
4. retain raw response/provenance;
5. validate schema and arithmetic;
6. route uncertain/invalid rows to review;
7. checkpoint before the next batch.

`api-batch` uses configured extractor/reviewer adapters. Require explicit upload/paid authorization, bounded retries/concurrency, and a usage estimate or cap. Exact provider models are configuration values.

## Phase sequence

```text
preflight and SHA-256
→ safe staging
→ image inventory and exact duplicates
→ screen extraction
→ schema and semantic validation
→ troop matching
→ review queue and explicit decisions
→ conservative deduplication
→ canonical occurrence build
→ context aggregates and evidence grades
→ complete/reliable rankings
→ frozen-model comparison
→ artifact index and state
```

Do not advance ranking-critical unresolved values into the primary dataset. Preserve partial hierarchy evidence.

## Repository Phase 1 publication

When the requested output is a new evidence PR, stop the pipeline at the normalization handoff rather than continuing into analytical rankings.

```text
preflight and SHA-256
→ deterministic normalized records
→ review queue
→ structural validation
→ reconstructible normalized archive
→ artifact hashes
→ batch-specific ANALYSIS_PROMPT.md
→ one normalization branch
→ one draft PR
→ one pending bannerlord-analysis-task:v1 comment
→ stop for the separate local analysis agent
```

Read [repository-pr-workflow.md](repository-pr-workflow.md). The repository's current `AGENTS.md` and protocol documents override stale examples in this skill.

Do not publish a Phase 1 PR from an extraction queue alone. The normalized evidence, bundle, hashes, validation, and handoff must be complete enough for the local analysis agent to verify and start.

## Common commands

Prepare or resume:

```bash
python3 scripts/invoke_pipeline.py \
  --input "/path/to/input.zip" \
  --output "/path/to/output" \
  --mode host-vision \
  --repo "/path/to/bannerlord-troop-analysis"
```

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

When incomplete, return the state path and the same command with the missing verified argument added.

For a repository evidence batch, copy only the validated Phase 1 artifacts into the batch directory, generate the batch handoff, validate hashes, and then execute the repository publication workflow. Do not use analytical outputs from an `offline-existing` continuation in that Phase 1 commit.
