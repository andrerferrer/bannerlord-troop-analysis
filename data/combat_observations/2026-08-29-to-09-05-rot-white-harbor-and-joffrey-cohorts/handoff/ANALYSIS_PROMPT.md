# Phase 2 handoff

Read repository `AGENTS.md` and this entire file before changing artifacts.

## Immutable Phase 1 identity

- Source ZIP SHA-256: `198e895c17e03a9254c4d23e8611557da05271fec5a466966cffbddb36a9028a`
- Normalized archive SHA-256: `9cc8482caf6d37356b186c0a68dfa9e6f50303fb715f6ddfc3a49e2593b59c9d`
- Pipeline/schema: `0.4.0` / `2.0.0`
- Track/version: `realm_of_thrones` / `1.4.x`

Reconstruct and verify the normalized archive exactly as documented in `bundle/README.md`. Treat every reconstructed Phase 1 file as immutable. Add corrections only in a separate reviewed layer with provenance.

## Required actions

1. Verify the archive hash and every member against `manifest/phase1_bundle_manifest.json`.
2. Review the three clipped-row items in `review/review_queue.csv`; leave unresolved values null when the retained evidence cannot resolve them.
3. Resolve each `requires_roster_confirmation` identity in `review/troop_identity_review.csv` only against the committed versioned ROT audit/roster.
4. Analyze every visible player-side ordinary troop in every context; keep field, siege attack, and siege defense separate.
5. Publish complete reliable/insufficient partitions under the 5-independent-battle / 20-deployed display gate.
6. Produce the additive White Harbor Knight Commander deep dive and determine the smallest next dedicated field test.
7. Verify direct player-side kill/deployment denominators before publishing shares, contribution ratios, or impact ranks.
8. Run repository validation; confirm normalized inputs and frozen model files remain unchanged.
9. Publish append-only `in_progress` and then `complete` or `blocked` protocol comments.
10. Mark ready and squash-merge only after the distinct-agent Phase 2 and all merge gates pass.

Do not assume the provisional conversational conclusion. Verify it from the reconstructed evidence.
