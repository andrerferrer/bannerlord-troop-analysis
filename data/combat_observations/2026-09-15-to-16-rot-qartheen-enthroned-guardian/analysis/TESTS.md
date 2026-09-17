# Validation runs

- Phase 2 generator: passed, including strict Base64/archive/member/mirror hashes, shard hashes, source links, identities, arithmetic, exact partition, focus, sensitivity, context, immutable-input, frozen-model, and queue assertions.
- Deterministic regeneration: passed with byte-identical generated analysis/review artifacts and queue.
- `python3 -m py_compile .../analysis/generate_phase2.py`: passed.
- Focused repository validation: **101/101 passed** across normalized analysis, combat bundle/domain, task protocol, empirical analysis, Qartheen Phase 1 bundle, canonical identity, role diagnostics, and historical evidence audit.
- `git diff --check`: passed.
- Full repository discovery: 394 tests ran; 390 passed and 4 unrelated modules could not import because this environment lacks optional `pandas` (item catalog, two vanilla-audit discovery modules, and the ROT S-tier ranged audit).
- No product-code behavior changed, so behavior-test red-before-green was not applicable to this deterministic batch generator and generated-report slice.
