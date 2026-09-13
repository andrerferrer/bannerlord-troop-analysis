# Validation runs

- Phase 2 generator run twice: passed with byte-identical generated artifacts.
- Normalized archive: 14,900 bytes, 22/22 declared member hashes and sizes verified.
- Exact partition: 61 occurrences into 27 rows (6 reliable, 21 insufficient).
- `python3 -m py_compile .../analysis/generate_phase2.py`: passed.
- `git diff --check`: passed.
- Focused archive, source-manifest, denominator, identity, partition, sensitivity, historical-pin, queue, artifact-hash, and human-report coverage assertions: passed.
- Focused repository unit tests: **89/89 passed** (normalized analysis, canonical identity, bundle safety, task protocol, and role diagnostics).
- Deliberate negative red/fix: permissive decoding first accepted a corrupted trailing Base64 byte; after compacting only ASCII whitespace and enabling strict validation, the same corruption fails closed.
- Added, missing, modified, or symlink-substituted immutable snapshot paths fail closed against the normalization commit.
- Changed identity audit and changed historical comparison source each fail closed.
