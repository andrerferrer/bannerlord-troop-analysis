# Workflow reference

## Input decision

| Input | Action |
|---|---|
| Screenshot ZIP | Run safe ZIP preflight, historical/visual deduplication, then queue/extract only accepted images |
| Screenshot directory | Manifest files in place, perform historical/visual deduplication, then queue/extract |
| Eleven normalized Base64 parts | Run strict reconstruction and exact-hash verification |
| Existing normalized directory | Locate `troop_occurrences.jsonl`; build only with a verified troop registry |
| Corrupt/unsupported input | Stop that input path with an actionable error; never treat it as empty |

## Modes

`offline-existing` performs deterministic verification, correction application, canonical build, rankings, and comparison without model calls.

`host-vision` uses the current session to inspect queued images. For each image:

1. read the full screen rather than standalone OCR;
2. emit strict structured rows, including visible side-total and party rows;
3. leave unreadable fields null;
4. retain raw response/provenance;
5. validate schema and arithmetic;
6. route uncertain/invalid rows to review;
7. checkpoint before the next batch.

Before row extraction, compare every screenshot with committed history and with the other screenshots in the batch. Inspect the actual scoreboard: same sides, party headings, totals, troop rows, result state, battle timer, and environment. Write `reports/screenshot_deduplication_audit.csv`. Skip prior normalized and repeated screens; group supplemental or sequential screens under one battle rather than treating them as new samples.

`api-batch` uses configured extractor/reviewer adapters. Require explicit upload/paid authorization, bounded retries/concurrency, and a usage estimate or cap. Exact provider models are configuration values.

## Phase sequence

```text
preflight and SHA-256
→ safe staging
→ committed-history lookup by hash and capture identity
→ full-batch visual duplicate/same-battle audit
→ screen extraction
→ schema and semantic validation
→ troop matching
→ review queue and explicit decisions
→ conservative deduplication
→ canonical occurrence build
→ context aggregates, kill-total coverage, and evidence grades
→ separate efficiency and share-adjusted-impact ranks in complete/reliable rankings
→ frozen-model comparison
→ artifact index and state
```

Do not advance ranking-critical unresolved values into the primary dataset. Preserve partial hierarchy evidence.

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
