# Phase 2 output contract

Report:

1. `COMPLETE` or `BLOCKED`;
2. task ID, pull request, branch, and normalization commit;
3. verified source and normalized-archive SHA-256 values;
4. reviewed corrections, exclusions, and unresolved counts;
5. identity-resolution coverage;
6. battle, occurrence, reliable, and insufficient-evidence counts by side and context;
7. paths to `review/` and `analysis/` artifacts;
8. validation commands and results;
9. limitations and blocked claims;
10. latest append-only protocol state and completion action.

Use `COMPLETE` only after every required action and merge gate passes. A prose summary never substitutes for committed structured outputs or a valid `complete` protocol comment.

Use `BLOCKED` when integrity, handoff, identity, validation, or boundary requirements prevent safe completion. Keep the pull request open and draft, repeat the full protocol payload, and describe actionable blockers.

Never report Phase 1 branch creation, a new draft pull request, or a new `pending` task from this skill.
