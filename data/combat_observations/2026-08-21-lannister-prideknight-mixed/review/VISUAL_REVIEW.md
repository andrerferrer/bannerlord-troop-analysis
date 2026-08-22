# Exact-image Phase 2 review

All five queued hero/UI rows were re-opened from the locally retained PNGs and
verified against the SHA-256 values in `source_inventory.csv`.

- Four Samwell Tarly `upgrade_ready` cells contain the white double-arrow UI
  icon, not an integer. They are resolved as non-numeric indicators and remain
  null in the immutable normalized layer.
- Jaime Lannister's kills and upgrade-ready cells at 17:24 are covered by the
  selection cursor. Both remain unresolved nulls; no value is inferred.
- All six fields belong to hero rows excluded from ordinary-troop rankings.

The reviewed decisions are additive in `review_decisions.csv`; no Phase 1 file
was rewritten.
