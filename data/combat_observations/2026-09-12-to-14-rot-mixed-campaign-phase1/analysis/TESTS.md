# Validation runs

- Red: the focused contract test failed with `FileNotFoundError` because `analysis/generate_phase2.py` did not exist.
- Green: `python3 -m unittest .../analysis/test_generate_phase2.py` passes.
- The generator runs twice with byte-identical artifacts.
- Focused repository validation: 90/90 passed (89 shared bundle, analyzer, identity, protocol, and role tests plus this batch contract).
- Full stdlib suite attempt: 387 tests passed; four additional test modules could not import because this documented local Python environment has no `pandas`.
- The 12,388-byte normalized archive matches its declared SHA-256 and all 10 members pass safe extraction.
- All 232 visible rows partition into 155 ordinary and 77 character rows; every ordinary occurrence maps to one reliable or insufficient aggregate.
- Three clipped ordinary rows preserve 13 null fields in the reviewed layer.
- Queue invariants pass with no mutation; frozen model files and published immutable Phase 1 inputs remain unchanged.
- Merge gate remains blocked: the Phase 1 handoff declared `screenshots_manifest.csv`, but that artifact is absent.
