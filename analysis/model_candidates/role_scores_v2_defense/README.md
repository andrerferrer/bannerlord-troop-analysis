# Defensive role scores v2 — candidate outputs

These files are the reproducible outputs of
`defensive_role_scores_v2_candidate` for XML export
`export_20260731_150800`.

This is a candidate model, not a promoted canonical model. Nothing under
`analysis/model_versions/` changed. See
`docs/methodology/005_defensive_role_scoring_v2_candidate.md` for formulas,
population rules, assumptions, and confidence.

## What changed from v1

- Protection contains only armor, shield, harness, and the mount's
  `horse_extra_health` modifier.
- Charge damage is audit-only and cannot affect protection or defensive
  utility.
- Infantry and cavalry have separate normalization and rankings.
- Alternative choices within an equipment slot are averaged first, then
  alternative rosters are averaged; absent or unresolved equipment contributes
  zero.
- Defensive utility is a separate 80/10/10 protection/mobility/melee-skill
  hypothesis.
- Spectacle-scale units remain in normalization, by explicit operator decision,
  while `spectacle_reason` preserves the ADR-005 classification for audit.
- The `infantry` artifact lane is operationally unmounted and therefore also
  contains ranged foot troops; its population rule is horse-based, not a melee
  role filter.
- Incomplete mount/harness evidence is written to an explicit review queue and
  excluded from score normalization and rankings instead of being treated as
  zero. The current TAOM queue contains 22 affected warg troops.
- Other `item_found=false` equipment and armor items whose stat fields are all
  blank retain the documented zero contribution, while
  `unresolved_item_evidence` identifies the exact source item, slot, and gap in
  every published row. The outputs expose 36 scored troops with blank armor
  evidence and nine Realm of Thrones troops with unresolved item identities.

## Review anchors

The new lanes remove the concrete anomalies that triggered this review. Every
v1 rank below comes from the `Ranked — Defensive` table in that track's
`analysis/theoretical/<track>/export_20260731_150800/OVERVIEW.md`; the v2 rank
comes from the matching lane-specific `*_protection_v2.csv` file:

- Nightmare Sails `sturgian_veteran_warrior`: v1 broad defensive rank 28;
  v2 infantry protection rank 2.
- Nightmare Sails `nord_huscarl`: v1 broad defensive rank 18; v2 infantry
  protection rank 1.
- Realm of Thrones `golden_elite_pikeman`: v1 broad defensive rank 1 because
  elephant charge entered defense; v2 cavalry protection rank 29. Its charge
  350 remains visible only in the audit column.
- TAOM `imladris_warden`: v1 broad defensive rank 40; v2 infantry protection
  rank 2.
- TAOM `cave_troll`: v1 broad defensive rank 8; v2 infantry protection rank 3.
  Its shield exists in only one of six loadouts, so v2 credits one sixth of the
  shield instead of the best roster.

These movements establish formula behavior, not empirical superiority.

## Layout

Each track contains:

- per-roster defensive features;
- complete troop-level scores;
- a track-specific evidence review queue (empty when all score inputs resolve);
- infantry protection and utility rankings;
- cavalry protection and utility rankings;
- input hashes, formula weights, population counts, and status in `meta.json`.

`artifact_hashes.csv` pins every generated CSV and JSON already present under
this output root, including untouched tracks during a partial `--tracks` run.
Regenerate with:

```bash
python3 scripts/scoring/generate_defensive_role_scores_v2.py
```
