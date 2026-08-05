# Context-first scoring candidate v1

## Status

This is the declaration contract for `context_first_scores_v1`. It does not
publish rankings. It fixes the question and its smallest direct input set before
later evidence code is allowed to run.

## Deliberately simple questions

- `defense`: worn armor only, using the declared regional armor aggregation.
- `attack`: weapon output only. Melee and ranged are separate declarations.
- `general`: armor and weapon output side by side. There is no combined number,
  weight, normalization, or default blend.

Shields, skills, Riding, mounts, harnesses, charge, reach, speed, reliability,
perks, and mobility are not candidate-v1 drivers. Projectile damage is retained
later as provenance but is explicitly `not_included` in ranged weapon output.

## Context rules

`field`, `siege_attack`, and `siege_defense` are separate populations. Outside
siege defense, mounted and dismounted rosters are separate declarations. Siege
defense has only a dismounted declaration; mounted declarations fail validation.

Ranged field and siege-attack declarations use `finite` ammunition. Ranged
siege-defense declarations use `unlimited`, meaning per-shot output with stack
count ignored and no numeric infinity. Melee and defense declarations use
`not_applicable`.

## Declaration inventory

The repository contains 100 declarations: 25 supported tuples for each of
`vanilla`, `nightmare_sails`, `realm_of_thrones`, and `taom`.

For each track:

- field and siege attack each declare defense/melee, attack/melee,
  attack/ranged, general/melee, and general/ranged for both mount states;
- siege defense declares those five question/mode pairs only as dismounted.

Defense uses `attack_mode=melee` as the explicit no-ranged-driver lane; a ranged
defense declaration is invalid rather than a duplicate armor ranking.

## Fixed armor contract

Armor-capable declarations use only `head_armor`, `body_armor`, `arm_armor`, and
`leg_armor`, with `survivability_armor_v71` weights `0.35`, `0.55`, `0.05`, and
`0.05`. This preserves the already documented armor interpretation without
admitting shield or mounted-equipment substitution.

## Validation and failure behavior

Declarations are strict JSON: every field is required, unknown fields fail, no
implicit default exists, and schema-v1 secondary drivers are forbidden. The
validator checks the exact driver, armor, weapon, projectile, ammunition,
mount-state, roster-aggregation, and combination contracts before downstream
evidence is read.

Run:

```bash
python3 scripts/scoring/context_first_contract.py \
  analysis/model_candidates/context_first_scores_v1/declarations/realm_of_thrones__siege_defense__defense__melee__dismounted.json
```

Success exits 0 and prints the candidate and tuple. Invalid JSON or a contract
violation exits 2 and prints deterministic `error_code`, `field`, and `detail`
records. Numeric values must be finite. Calculation code in later slices uses
`Decimal`, six published places, and `ROUND_HALF_EVEN`.

Historical candidates and every frozen model version remain immutable. These
declarations authorize only the new candidate namespace.
