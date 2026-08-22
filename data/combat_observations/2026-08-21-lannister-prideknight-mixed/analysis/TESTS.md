# Phase 2 test record

## Targeted analysis suite

Command:

```bash
python -m unittest -v \
  tests.test_analyze_normalized_combat_batch \
  tests.test_audit_historical_combat_evidence_v04 \
  tests.test_combat_bundle \
  tests.test_combat_domain \
  tests.test_discover_analysis_tasks \
  tests.test_empirical_analysis \
  tests.test_audit_context_first_candidates \
  tests.test_context_first_armor \
  tests.test_context_first_contract
```

Result: 157 tests run; 156 passed and 1 failed.

## Complete repository suite

Command:

```bash
python -m unittest discover -s tests -v
```

Result: 373 tests run; 372 passed and 1 failed.

## Known unrelated failure

Both runs fail only
`test_audit_context_first_candidates.ContextFirstCandidateAuditTests.test_staged_path_substitution_fails_and_restores_target`.
The implementation correctly raises an `AuditError` because staged content
differs, but the existing test's `assertRaisesRegex` accepts only
`staged|identity|replacement`; the actual message is
`published audit output content differs: .../report.md`. This branch does not
modify that test or its implementation, and the failure predates the Phase 2
analysis changes.
