# Validation runs

- Phase 2 generator: passed immutable bundle SHA-256/size, safe tar preflight, all 17 payload manifest hashes, schema/arithmetic boundaries, exact partition, denominator coverage, and focus gates.
- `python3 -m py_compile .../analysis/generate_phase2.py`: passed.
- Repository unit test results are recorded after publication/branch validation.
- Full `python -m unittest discover -s tests -v`: **380/381 passed**, **1 failed**, **0 errors**. Status: `known_pre_existing_failure_only`.
- Sole failure: `test_staged_path_substitution_fails_and_restores_target`, pre-existing assertion-message mismatch; this PR does not modify that implementation/test.
