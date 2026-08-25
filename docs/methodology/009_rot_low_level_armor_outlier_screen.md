# Realm of Thrones low-level armor-outlier screen

## Question and scope

This screen answers a narrow operator question: which ordinary low-level Realm
of Thrones infantry or ranged troops wear unusually strong armor for their
level band, following the observed `Pentoshi Soldier` / `Pentoshi Pikeman`
example?

It is a candidate-selection map, not a combat ranking. The output contains no
kills, casualties, skills, weapon values, shield bonus, mount value, or hidden
composite score.

```text
track: realm_of_thrones
context: field
question: dismounted_worn_armor_outlier_screen
attack_mode: not_applicable
mount_state: dismounted
primary_drivers: worn_armor
ammunition_policy: not_applicable
secondary_drivers: none
armor_source_fields: head_armor, body_armor, arm_armor, leg_armor
armor_slots: Head, Body, Leg, Gloves, Cape
armor_aggregation: each hit zone is published separately; body-zone percentile selects candidates
weapon_damage_source_fields: not_applicable
projectile_contribution: not_applicable
roster_aggregation: arithmetic_mean
combination_rule: not_applicable
```

## Population

- canonical track audit: `realm_of_thrones_troop_equipment_audit.csv`;
- `occupation == Soldier`;
- corrected `line_status == main_or_minor_line`;
- `default_group` is `Infantry` or `Ranged`;
- level bands 11, 16, and 21, labeled `T2`, `T3`, and `T4` only to match the
  operator's in-game terminology;
- only resolved (`item_found == True`) worn-armor rows are used.

`tree_tier` remains a separate upgrade-depth field. The screen does not equate
it with the operator tier label. Cavalry and horse archers are excluded so
horse/harness effects cannot contaminate the dismounted comparison.

## Direct fields

`body_slot_armor` is the body protection contributed by the `Body` item alone.
`body_zone_armor` includes body protection contributed by all worn slots, such
as a cape or shoulders. The other zone columns follow the same worn-slot rule.

Shield HP and shield armor are published as context only. They do not change
the armor rank or percentile.

Alternative equipment rosters are averaged arithmetically. A troop with an
unresolved worn-armor item is excluded from the map and written to the review
queue instead of receiving a guessed zero.

## Interpretation

The body-zone percentile is a structural filter for controlled tests. It says
that a troop wears exceptional torso protection for its level cohort; it does
not prove overall survivability or field performance. Limbs, head, shield,
weapon, formation behavior, and battle evidence remain separate questions.
