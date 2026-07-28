# RoT/HOT V4.4 — Kinetic melee integration

Date: 2026-07-27

## Status

The Wavey v2.9 kinetic engine is integrated as a versioned V4.4 overlay. V4.3
remains frozen and reproducible as the previous model.

The integration has two deliberately separate modes:

1. `canonical` requires the complete V4.3 all-humanoid output and exact,
   source-addressable one-handed-sword profiles;
2. `sensitivity` accepts the preserved V4.3 top 20 and uses explicit
   low-confidence family priors.

The committed 2026-07-17 artifacts are sufficient for the second mode only.
The full V4.3 ranking input, item reference, and exact weapon profile export
are not present in Git history or the local workspace. Therefore this change
does not supersede the canonical V4.3 ranking yet.

## Model integration

V4.3 already models:

- raw damage and damage type;
- armour response;
- weapon speed;
- marginal troop skill;
- broad family/application behavior.

V4.4 preserves those terms and applies the complementary kinetic multiplier:

```text
v44 melee KPM =
v43 melee KPM
× reach/collision term
× handling term
× weight/momentum term
× AI thrust-switching term
```

This avoids double-counting the Wavey damage and speed curves and preserves
V4.3's cut/pierce/blunt armour treatment.

The exact canonical layer is deliberately limited to one-handed swords, the
domain for which the source engine was designed. Unsupported weapon families
remain on their V4.3 value and are identified in the profile audit. Missing
eligible profiles fail the coverage gate instead of falling back silently.

## Exact input contract

The canonical item reference must provide:

```text
item_id
weapon_class
swing_speed
handling
weapon_length
weight
has_thrust
thrust_damage
thrust_speed
source
source_sha256
```

`thrust_damage` and `thrust_speed` are required only when `has_thrust=true`.
The template is:

```text
data/rot_reference/hot_20260717/v44_exact_item_profile_template.csv
```

The ranking input must be the complete
`rot_hot_v43_all_humanoid_ranked.csv`, not the preserved top-20 excerpt.

## Canonical command

```bash
python3 scripts/rot/rot_v44_kinetic_overlay.py \
  --mode canonical \
  --input <rot_hot_v43_all_humanoid_ranked.csv> \
  --item-reference <v44_exact_item_profiles.csv> \
  --family-audit <v43_item_family_audit.csv> \
  --domain-manifest <v43_all_humanoid_domain.json> \
  --source-root <repo-or-artifact-root> \
  --output <rot_hot_v44_all_humanoid_ranked.csv> \
  --audit-output <rot_hot_v44_profile_audit.csv> \
  --summary-output <rot_hot_v44_summary.json>
```

Canonical mode fails closed unless:

- `--domain-manifest` matches the input file SHA-256 and unique `troop_ids`;
- `--family-audit` supplies the versioned V4.3 family for every melee item
  (eligibility does not use item-id substring inference);
- each exact sword profile includes repository-addressable `source` and
  `source_sha256`, and the hash verifies;
- `--minimum-exact-coverage` is finite and inside `[0, 1]` (default 100%).

## Preserved-top-20 sensitivity

The current sensitivity uses family priors for 15 of 20 preserved rows.
Five ranged troops lack enough preserved melee-profile data and retain a
neutral factor. Scores are re-normalized over the visible melee domain before
the directional total is calculated.

Notable directional changes:

| V4.3 | sensitivity | troop | direction |
|---:|---:|---|---:|
| 2 | 1 | Ravens' Teeth | +1 |
| 4 | 2 | Goldenheart Warrior | +2 |
| 5 | 3 | Stark Sworn Sword | +2 |
| 1 | 4 | Westerling Hedgeknight | -3 |
| 3 | 8 | Mallister House Guard | -5 |
| 12 | 9 | Qohorik Falxman | +3 |
| 14 | 20 | Grafton Flaming Knight | -6 |

Interpretation:

- the existing result is sensitive to reach, handling, weight, and thrust;
- ranged anchors become relatively stronger when melee application is made
  more demanding;
- hammer and axe leaders are particularly sensitive to assumed handling and
  reach;
- Blackwood remains directionally favored because Ravens' Teeth moves to the
  top of the preserved comparison;
- Westerling, Mallister, and Grafton package conclusions require the complete
  terminal-troop rerun before they can be updated.

These are hypotheses for exact-profile validation, not replacement rankings.

## Generated artifacts

```text
data/rot_reference/hot_20260717/v44_kinetic_top20_sensitivity.csv
data/rot_reference/hot_20260717/v44_kinetic_profile_audit.csv
data/rot_reference/hot_20260717/v44_kinetic_sensitivity_summary.json
```

## Verification

```bash
python3 -m unittest -v \
  tests.test_kinetic_engine \
  tests.test_rot_v44_kinetic_overlay
```
