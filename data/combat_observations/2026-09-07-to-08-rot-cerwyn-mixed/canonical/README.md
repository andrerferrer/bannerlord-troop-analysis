# Canonical Phase 1 records

The immutable canonical files are stored inside the reconstructible bundle at
`../bundle/cerwyn_mixed_phase1.tar.xz.base64.part-00` and are individually
hash-pinned by `../manifest/phase1_bundle_manifest.json`.

Archive members:

- `canonical_screenshots.jsonl`
- `canonical_battles.jsonl`
- `canonical_occurrences.jsonl`
- `canonical_troop_battle_consolidated.jsonl`
- `canonical_historical_aggregates.jsonl`

They are not duplicated as loose Git files because the occurrence layer is large;
the bundle is the authoritative immutable Phase 1 input for Phase 2.
