# Defensive role scoring v2 candidate

## Status

`defensive_role_scores_v2_candidate` is an XML-structural candidate model. It
does not replace the frozen v7.1 general model, the frozen v7.3 burst model, or
the published `role_scores_v1` outputs. Promotion requires the repository's
empirical and model-change gates.

The candidate implements the approved defensive-model review while retaining
spectacle-scale units in the normalization population.

## Goals

1. Make physical protection explainable without offensive features.
2. Keep infantry and cavalry on separate, non-comparable scales.
3. Average alternative equipment rosters instead of selecting the best roster.
4. Keep defensive utility separate from protection.
5. Use the v7.1 head-weighted armor proxy consistently.

## Population and boundaries

- Tracks are scored separately and never pooled.
- Heroes and `mp_*` troops are excluded.
- Mod tracks keep added or overridden soldiers and exclude untouched vanilla
  rows (`change_type=inalterado`).
- Audit rows whose item could not be resolved (`item_found != true`), and armor
  rows whose four armor-stat fields are all blank, do not contribute item
  attributes. Their roster still exists, so the unresolved slot contributes
  zero instead of borrowing values from another loadout. The exact item, slot,
  and missing-evidence class remain visible in `unresolved_item_evidence`, so
  this proxy zero cannot be mistaken for complete source evidence. When the
  source itself omits the item identity, `<missing-item-id>` makes that gap
  explicit instead of substituting the slot name.
- Every eligible troop must have at least one audit roster. Generation stops
  instead of silently dropping a troop when that evidence is missing.
- Mod tracks require their versioned override report. Generation stops instead
  of falling back to a vanilla-only population when that report is missing.
- A troop is assigned to the cavalry lane when at least half of its alternative
  equipment rosters contain a horse. Every other troop enters the infantry
  lane. The lanes are mutually exclusive. Operationally, `infantry` means
  unmounted here: ranged troops without horses share this normalization
  population. The existing label is retained for the candidate artifact
  contract, not as a claim that every row is melee infantry.
- A horse or harness row with a missing type or required movement/armor field is
  preserved in `*_defensive_review_queue_v2.csv`. Its troop remains visible in
  the complete troop output, but score and rank fields stay blank and it does
  not enter lane normalization. This prevents incomplete mount evidence from
  being guessed as a real zero.
- Every troop in a lane participates in that lane's min-max normalization.
  Giants, mammoths, elephants, trolls, and chariots are not removed. This is an
  explicit operator decision for v2, not an omission.
- Scores from different tracks or lanes are not comparable.

## Alternative roster aggregation

Equipment rosters are alternative spawn kits. A roster can also contain
multiple alternatives for the same equipment slot. For every feature, v2 first
computes the arithmetic mean of the alternatives within each slot, then the
arithmetic mean across all roster indices. A missing shield, horse, or harness
contributes zero for that roster. An unresolved alternative contributes zero
within its slot instead of allowing the other alternative to stand in for it.
Shield HP and shield armor each use the maximum slot-level expected value across
the roster's `Item*` slots before the cross-roster mean; those two maxima are
selected independently.

For example, a 600-HP shield present in one of two rosters contributes mean
shield HP 300 and `shield_share=0.5`. It does not give the troop permanent
credit for the best loadout.

## Ranking precision

Scores are serialized to six decimal places. Ranking and tie detection use
that same published precision, so two visibly equal scores always share a
rank. Unrounded floating-point residue cannot break a published tie.

## Spectacle audit

The output classifies spectacle-scale rows with the versioned criteria from
[ADR-005](ADR-005-spectacle-outlier-definition.md) and exposes the result in
`spectacle_reason`. Classification is audit-only for this candidate: those
rows remain in their lane's normalization and ranking. Each track's `meta.json`
pins both the criteria version and the complete active criteria list used to
produce the classification.

## Armor proxy

```text
survivability_armor_v71 =
    0.35 × head armor
  + 0.55 × body armor
  + 0.05 × arm armor
  + 0.05 × leg armor
```

This reuses the accepted v7.1 lethality-weighted proxy. It is not claimed to be
the engine's true hit-location distribution.

## Component normalization

Each raw feature below is min-max normalized to 0–100 inside its track and
lane, with all lane members included. A constant component becomes zero rather
than creating artificial separation.

## Protection score

Infantry:

```text
protection_score_v2 =
    0.70 × survivability armor component
  + 0.20 × shield HP component
  + 0.10 × shield armor component
```

Cavalry:

```text
protection_score_v2 =
    0.50 × rider survivability armor component
  + 0.15 × shield HP component
  + 0.05 × shield armor component
  + 0.20 × harness armor component
  + 0.10 × horse extra-health component
```

The audit exposes the mount's `horse_extra_health` modifier, not a complete
horse HP value. The output therefore retains the precise source name. Damage of
charge, speed, maneuver, weapon-template proxies, and throwing proxies do not
affect protection.

## Defensive utility score

```text
defensive_utility_score_v2 =
    0.80 × protection_score_v2
  + 0.10 × mobility component
  + 0.10 × counterpressure component
```

- Infantry mobility is Athletics.
- Cavalry mobility is the mean of normalized Riding, horse speed, and horse
  maneuver.
- Counterpressure is the maximum of OneHanded, TwoHanded, and Polearm skill.
- Charge damage is retained as an audit-only output column and affects neither
  score.
- Crafted weapon class and damage proxies affect neither score.

This score represents a transparent structural hypothesis about staying power,
formation movement, and ability to contest contact. Its weights are editorial,
not fitted.

## Confidence

| Element | Confidence | Reason |
|---|---|---|
| Armor, shield, harness inputs | High when complete | Direct, versioned XML audit values; incomplete mount evidence is queued instead of scored |
| Alternative-loadout mean | High | Averages mutually exclusive choices within slots, then alternative rosters |
| Infantry/cavalry split | Medium | Deterministic majority-horse rule; mixed rosters remain visible through `horse_share` |
| Mount extra-health and mobility components | Medium | Direct XML fields, but not a complete engine durability/movement simulation |
| Component weights | Low | Editorial and not empirically fitted |
| Intrinsic gameplay prediction | Unvalidated | Current campaign evidence does not pass predictive-model gates |

## Reproduction

```bash
python3 scripts/scoring/generate_defensive_role_scores_v2.py
python3 -m unittest -v tests.test_defensive_role_scores_v2
```

Generated artifacts and their SHA-256 hashes are stored under
`analysis/model_candidates/role_scores_v2_defense/`. A partial `--tracks`
rerun refreshes the requested tracks without removing untouched generated
files from the manifest.
