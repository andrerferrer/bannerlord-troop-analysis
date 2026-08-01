# ADR-005 — One definition of "S+ / spectacle outlier"

## Status

Accepted (2026-07-31). Owner module: `scripts/scoring/outliers.py`
(`SPECTACLE_OUTLIER_VERSION = "v2"`).

## Context

"S+" / "spectacle outlier" means **a unit whose scale puts it outside the
ordinary troop ladder** (giants, mammoths, war elephants, mumakil, chariots,
trolls). Such a unit is parked in its own S+ section and excluded from the S–D
ladder so it does not crowd ordinary troop tiers, and so tier bands are computed
against the best *non-outlier* score in each role.

Before this ADR the concept existed in three separate places, with three
different criteria and no shared code:

| # | Where | Criterion | Kind |
|---|---|---|---|
| 1 | `scripts/scoring/write_theoretical_overview.py` (`_SPECTACLE_RE`, `is_spectacle_outlier`, `split_spectacle_outliers`) | name regex `\bgiants?\b\|\bmammoths?\b\|(^\|_)giant(_\|$)\|(^\|_)mammoth(_\|$)` on `troop_id` + `troop_name` | **executable**, drives every generated `OVERVIEW.md` |
| 2 | `analysis/theoretical/realm_of_thrones/export_20260731_150800/ROLE_REPORT.md` ("S+ outliers — parked") | criterion 1 **plus** "any troop whose mount has `horse_charge_damage >= 200`" — in RoT that is the mounts `mammoth` (charge 400) and `elephant` (350); next mount down is `unicorn1` at 90 | **prose only**, applied by hand in that report (3 Volantene elephant units: `golden_elite_pikeman`, `golden_horseman`, `tigercloak_camel_cavalry`) |
| 3 | `analysis/theoretical/taom/export_20260731_150800/ROLE_REPORT.md` ("S+ outliers — outsized units") | explicitly *not* name matching: any roster mounting `taom_mumakil`, `taom_war_elephant` or `taom_chariot_a`, **plus** the foot unit `cave_troll` | **prose only**, applied by hand in that report (5 troops) |

A fourth, unrelated `"S+"` string exists in
`scripts/melee_engine/kinetic_engine.py:99` (`TIER_TABLE`): it maps a 0–100
kinetic score to a letter ladder (`S+` = score ≥ 86, then `S`, `S-`, `A+`, …).
That is a **score band, not a unit-scale flag** — a heavily-optimised ordinary
two-hander can reach `S+` there while never being a spectacle unit. It is
deliberately **not** merged into this definition, and `outliers.py` says so in
its module docstring.

Consequences of the split: reviewers could not tell which criterion produced a
given S+ row; the RoT/TAOM criteria were unreproducible (prose, not code); and
`OVERVIEW.md` gave no per-troop reason.

## Decision

1. **One owner.** `scripts/scoring/outliers.py` is the single source of truth for
   the predicate. `write_theoretical_overview.py` imports
   `is_spectacle_outlier` / `split_spectacle_outliers` / `classify_row` from it;
   **no other module may re-derive the regex or a mount heuristic.**
2. **Versioned.** `SPECTACLE_OUTLIER_VERSION = "v2"` — v1 was the inline regex.
   The version is stamped into the generated `OVERVIEW.md` "Tiers" section.
3. **Explicit criteria registry.** Criteria live in the `CRITERIA` tuple, each a
   frozen `Criterion(key, reason, summary, default_enabled, matches)` over a
   `TroopFacts(troop_id, troop_name, mount_ids, mount_charge_damage)` record:

   | key | reason | rule | default |
   |---|---|---|---|
   | `giant_mammoth_name` | `giant/mammoth name` | the v1 regex, byte-identical | **enabled** |
   | `outsized_mount_charge` | `outsized mount` | any roster mount `horse_charge_damage >= 200` | opt-in |
   | `outsized_mount_id` | `outsized mount` | mount id in `taom_chariot_a`, `taom_mumakil`, `taom_war_elephant` | opt-in |
   | `outsized_foot_id` | `outsized foot unit` | `troop_id` in `cave_troll` | opt-in |

4. **The API returns a reason, not just a boolean.** `classify(...)` /
   `classify_row(row)` return `SpectacleVerdict(is_outlier, reason)`, so the
   generated S+ tables carry a `spectacle_reason` column naming the criterion
   that parked each row. `is_spectacle_outlier(troop_id, troop_name)` is kept as
   the v1-compatible boolean shim.
5. **Defaults do not change behaviour.** `DEFAULT_CRITERIA` is
   `("giant_mammoth_name",)` only. Criteria 2 and 3 above are registered and
   executable but **opt-in**, so every published score, rank and tier stays
   reproducible. Enabling them is a deliberate, separately-reviewed change (see
   *Diff if the opt-ins are enabled*).
6. **Pandas-free core.** `outliers.py` imports nothing beyond the stdlib, so it
   is unit-testable in environments without pandas (`tests/test_outliers.py`).
   `split_spectacle_outliers` is duck typed: it uses `.apply` on a pandas frame
   and falls back to the list-backed `_rows` test frame.
7. **The scorer does not park anything.** `generate_vanilla_role_scores.py`
   normalises over the whole population, outliers included — which is why raw
   `*_score_base` values read low on tracks with elephants (RoT gap 6). It has
   **no** spectacle predicate to import; a comment there points at this ADR so a
   future reader does not add a second heuristic next to `horse_charge_damage`.

### Why giants / mammoths are parked outside S–D

Tier letters are assigned as a fraction of the best score in the role
(`tier_letter_from_top_fraction`: ≥0.90 S, ≥0.70 A, ≥0.40 B, ≥0.20 C, else D).
A single off-scale unit therefore rescales the whole ladder: in RoT
`giant_rider` (mammoth, mount charge 400) and the elephant mahouts hold
`defense_score_base` 100.0 and `ranged_role_score` 100.0, which pushes the best
ordinary cavalry from ~100 down to ~68 and would demote genuinely elite troops a
whole band. They are also not a real player choice on the same axis — a mammoth
is spectacle content, recruited (if at all) for different reasons than a
knight. So they are listed, with scores, in their own S+ section and excluded
from the S–D ladder rather than deleted: nothing is hidden, but nothing ordinary
is measured against them.

### How to add a criterion

1. Add a `_matches_*` function and a `Criterion(...)` entry to `CRITERIA` in
   `scripts/scoring/outliers.py`. Keep `default_enabled=False` unless the
   behaviour change is intended and reviewed.
2. If it needs a new input, add a field to `TroopFacts` and read it in
   `facts_from_row` (add the column name to `_MOUNT_ID_COLUMNS` /
   `_MOUNT_CHARGE_COLUMNS` or the equivalent). Rows lacking the column simply
   never fire the criterion.
3. Add positive **and** negative cases to `tests/test_outliers.py`.
4. Bump `SPECTACLE_OUTLIER_VERSION` and amend this ADR if the **default** set
   changes; document the resulting rank/tier diff.
5. Regenerate the overviews in an environment that has pandas (see below).

### Diff if the opt-ins are enabled (not done here)

Enabling `outsized_mount_charge` + `outsized_mount_id` + `outsized_foot_id`
would move these already-identified troops from the S–D ladders into the S+
section of the generated overviews:

- `realm_of_thrones`: `golden_elite_pikeman` (Golden Company Mahout),
  `golden_horseman` (Golden Company Elephant Rider), `tigercloak_camel_cavalry`
  (Volantene Mahout) — all mount charge 350. `golden_elite_pikeman` currently
  **tops the OVERVIEW Skirmisher list**, so enabling this rescales that role's
  tier bands.
- `taom`: `harad_mumakil_rider`, `harad_elephant_rider`,
  `wainrider_warlord_chariot`, `wainrider_swift_chariot` (mount ids) and
  `cave_troll` (foot). `cave_troll` would otherwise sit ~8th in line infantry on
  `armor_total` 475 / `effective_armor` 104.5 against an ordinary ceiling of
  354.5 / 81.3.
- `vanilla`, `nightmare_sails`: no change — neither track has outsized units
  (both role reports already state the regex matches 0 troops).

Tier letters of every other troop in the affected roles would shift, because the
`leader` score used for the bands changes. That is exactly why it is not the
default.

### Reconciliation of the three prior criteria

- **Criterion 1 (name regex) survives as executable code and as the only
  default.** Byte-identical pattern, now in `outliers.py`.
- **Criterion 2 (RoT `horse_charge_damage >= 200`) is promoted from prose to a
  registered, tested, opt-in criterion** (`outsized_mount_charge`). The RoT
  `ROLE_REPORT.md` stays valid as written: it documents applying criterion 1 +
  criterion 2 by hand in that report only. It is **not** retroactively applied
  to `OVERVIEW.md`.
- **Criterion 3 (TAOM mount ids + `cave_troll`) is likewise promoted to two
  registered opt-in criteria** (`outsized_mount_id`, `outsized_foot_id`). The
  TAOM report's claim "detected structurally, not by name matching" remains
  accurate for that report.
- **The `kinetic_engine.py` `S+` band is explicitly a different concept** and is
  left untouched.
- Both role reports remain the **prose** record of a per-report choice; the ADR
  is the record of the shared definition. Where a report's parked set differs
  from `OVERVIEW.md`'s, that is now traceable to which criteria were active.

## Regeneration

`python3` in the agent environment has **no pandas**, so `OVERVIEW.md` and the
role CSVs **cannot** be regenerated here, and the committed generated outputs
are deliberately left untouched by this change (hand-editing them to imitate a
regeneration is forbidden). On the PC environment that has pandas:

```bash
python3 scripts/scoring/write_theoretical_overview.py
```

That run adds, to each `OVERVIEW.md`: the S+ owner/version/criteria line, the
crafted-damage provenance banner, and a `spectacle_reason` column on the S+
tables. **No score, rank, tier or role CSV changes** — the default predicate is
identical to v1.

## Consequences

- One grep (`outliers.py`) answers "what is an S+ outlier here".
- Every parked row can state *why* it was parked (`spectacle_reason`).
- The RoT/TAOM criteria are now reproducible instead of prose-only, without
  silently changing any published ladder.
- Adding a criterion is a registry entry plus tests, not a new regex in a
  generator.
