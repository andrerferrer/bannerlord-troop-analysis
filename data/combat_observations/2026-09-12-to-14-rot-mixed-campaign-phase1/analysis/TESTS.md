# Validation runs

- Red (targeted, after updating the repaired identity pins only): the manifest-divergence test raised `AttributeError: module 'mixed_campaign_phase2' has no attribute 'verify_screenshot_manifest'`; the main contract raised `ValueError: unexpected handoff input inventory: missing=[]`.
- Green: `python3 -m unittest -v data.combat_observations.2026-09-12-to-14-rot-mixed-campaign-phase1.analysis.test_generate_phase2` passes both tests.
- The generator runs twice with byte-identical artifacts.
- Focused repository validation: 120/120 passed across the shared bundle, analyzer, identity, protocol, role, Phase 1 repair, and Phase 2 batch contracts.
- Full stdlib suite attempt: 389 tests passed; four additional test modules could not import because this documented local Python environment has no `pandas`.
- The 12,944-byte normalized archive matches its declared SHA-256 and all 11 members pass safe extraction.
- The authoritative screenshot manifest matches byte-for-byte between the repository and archive: 16 screens, 15 battle IDs, 3 active, and 13 final-result screens.
- All 232 visible rows partition into 155 ordinary and 77 character rows; every ordinary occurrence maps to one reliable or insufficient aggregate.
- Three clipped ordinary rows preserve 13 null fields in the reviewed layer.
- Queue invariants pass with no mutation; frozen model files and published immutable Phase 1 inputs remain unchanged.
- Local Phase 2 validation has no unresolved blockers.
