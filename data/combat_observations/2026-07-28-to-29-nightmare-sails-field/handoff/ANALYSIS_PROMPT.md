# Phase 2 analysis handoff — combat_2026-07-28_183356_2026-07-29_015856_nightmare_sails

## Immutable inputs

- Batch directory: `data/combat_observations/2026-07-28-to-29-nightmare-sails-field`
- Track: `nightmare_sails`
- Context: `field` for all 9 battles
- Normalized archive SHA-256: `67faffdb8dd882299c97d289136338d9c79fd33ce07c0b11db261514454facde`
- Artifact manifest: `artifact_hashes.csv`

## Required actions

1. Verify the ordered Base64 chunks, archive hash, and artifact manifest.
2. Treat normalized records as immutable.
3. Apply review decisions only in `review/`; do not rewrite normalized rows.
4. Exclude heroes and `needs_review=true` rows from ordinary troop rankings.
5. Resolve canonical identities only against versioned `nightmare_sails` audit files.
6. Aggregate by battle and context; do not pool tracks, sides, or contexts.
7. Publish complete and reliable rankings. Reliable display requires at least 5 independent battles and 20 deployed troops.
8. Bootstrap uncertainty at the battle level.
9. Document partial screenshot visibility and any insufficient-evidence result.
10. Confirm `analysis/model_versions/` is unchanged.
