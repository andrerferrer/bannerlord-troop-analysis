# Phase 2 analysis handoff — combat_2026-07-27_103534_104834_rot

## Immutable inputs

- Batch directory: `data/combat_observations/2026-07-27-rot-field-followup`
- Track: `realm_of_thrones`
- Context: `field` for all 2 battles
- Normalized archive SHA-256: `70abe0385130a6d96aa9c594b08edc9bfa528bfdddeedd94c92dcf1d9de940ce`
- Artifact manifest: `artifact_hashes.csv`

## Required actions

1. Verify the ordered Base64 chunks, archive hash, and artifact manifest.
2. Treat normalized records as immutable.
3. Apply review decisions only in `review/`; do not rewrite normalized rows.
4. Exclude heroes and `needs_review=true` rows from ordinary troop rankings.
5. Resolve canonical identities only against versioned `realm_of_thrones` audit files.
6. Aggregate by battle and context; do not pool tracks, sides, or contexts.
7. Publish complete and reliable rankings. Reliable display requires at least 5 independent battles and 20 deployed troops.
8. Bootstrap uncertainty at the battle level.
9. Document partial screenshot visibility and any insufficient-evidence result.
10. Confirm `analysis/model_versions/` is unchanged.
