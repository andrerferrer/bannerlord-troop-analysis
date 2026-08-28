# Validation runs

- `python3 .../analysis/generate_phase2.py --source-zip <attachment>`: passed; source ZIP, 29 members, 26 Phase 1 artifacts, bundle, schema boundaries, partition, and metrics regenerated.
- `python3 -m py_compile .../analysis/generate_phase2.py`: passed.
- `git diff --check`: passed.
- Targeted `unittest` run for protocol, role diagnostics, canonical identity, normalized analysis, and bundle safety: **73/73 passed**.
- Full `python3 -m unittest discover -s tests -v`: **380 passed, 1 failed**. The sole failure is the unrelated pre-existing assertion-message regex in `test_staged_path_substitution_fails_and_restores_target`. The same test was reproduced failing unchanged on detached `main` (`fb8cf889330f9fe570189c081e5dd23fe078837b`); this Phase 2 changes neither the tested script nor test.
