# Phase 1 output contract

Report:

1. `COMPLETE`, `COMPLETE_WITH_EXTERNAL_BLOCKERS`, or `BLOCKED`;
2. batch ID and repository path;
3. source name, retention status, size, and SHA-256;
4. screenshot, battle, normalized-occurrence, and review-queue counts;
5. structural-validation result;
6. normalized archive SHA-256 and bundle reconstruction path;
7. Phase 1 validator command and result;
8. branch and full normalization commit SHA;
9. draft pull-request number and URL;
10. task ID and pending protocol-comment status.

Use `COMPLETE` only when validated artifacts, the draft pull request, and the valid pending comment all exist. Use `COMPLETE_WITH_EXTERNAL_BLOCKERS` when local artifacts pass but a required GitHub write is unavailable. Use `BLOCKED` when the supplied input cannot be normalized safely.

Analytical paths, rankings, comparisons, recommendations, `complete` protocol state, ready-for-review, and merge are intentionally absent.
