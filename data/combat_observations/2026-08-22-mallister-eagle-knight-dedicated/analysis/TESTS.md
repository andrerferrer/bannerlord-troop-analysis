# Validation

Batch-local validation command:

```bash
python3 validation/validate_batch.py .
```

Result: **PASS**

Checks cover JSON/JSONL/CSV readability, SHA-256 manifests, accepted/duplicate counts, unique observation IDs, deployed arithmetic, ordinary-row filtering, per-battle visible sums not exceeding player-party totals, 7/7 positive player-side kill totals, ranking aggregation, the 5-battle / 20-deployed gate, and target arithmetic.

Repository-wide tests were not executed in this host session because the repository checkout was not locally available. The GitHub change is additive under one new batch directory and does not touch code, configuration, or frozen model files.
