# Exact-image visual review

All eight source screenshots referenced by the 17 queue rows were recovered from
the supplied ZIP/direct attachments, matched against `screenshots_manifest.csv`
by SHA-256, and reviewed at original resolution.

- Fifteen `upgrade_ready` cells on hero rows contain the white upgrade indicator,
  not a readable number. They are closed as `resolved_visual_non_numeric_indicator`;
  no integer is invented and heroes remain outside ordinary-troop rankings.
- `stark_sworn_20260821_0013` (`Northern Soldier [T2]`, `kills`) is still covered
  by the selection cursor in the exact 00:31:14 image. Its null is preserved as
  `unresolved_visual_occlusion`; the row remains outside the primary partition.
- `stark_sworn_20260821_0102` (Silverhill attacker-side `deaths`) is covered by
  the Upgrades tooltip, but the exact same-screen Robb Stark party row
  `stark_sworn_20260821_0104` supplies 30 deaths and agrees on all other visible
  totals: 215 survivors, 312 kills, 13 upgrades, 113 wounded, and 0 routed. The
  additive reviewed layer therefore records 30 with same-screen provenance.

No normalized Phase 1 row is rewritten. The corrected side total is non-ranking,
the 15 icon decisions are hero-only, and the single unresolved ordinary-troop row
is already excluded from the 106 primary numeric occurrences.
