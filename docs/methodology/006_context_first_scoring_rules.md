# Context-first scoring rules

## Status and purpose

This document records standing operator decisions for future troop-scoring work.
It exists so model intent is not reconstructed from chat history or inferred
from whichever candidate happens to be newest.

The central rule is: **start from the gameplay question, then use the smallest
set of direct drivers that can answer it**. Armor-only, weapon-only, and combined
scores are examples of this principle, not a mandatory sequence of models.

These rules constrain candidate design. They do not promote a model or change
the frozen outputs under `analysis/model_versions/`.

## Decision order

Before writing a formula, record these choices in order:

1. Track: Realm of Thrones, vanilla/War Sails, or another mod track.
2. Battle context: field, siege attack, or siege defense.
3. Troop question: defense, attack, or general capability.
4. Combat mode: melee, ranged, mounted, or explicitly dismounted.
5. Smallest direct driver set required by that question.

Do not begin with a universal score and then add weights until it appears to fit
all five choices. Different questions are allowed to produce different models.

## Standing scoring matrix

| Question | Primary drivers | Interpretation |
|---|---|---|
| Infantry defense | Worn armor | Who is hardest to kill while holding a defensive position? |
| Infantry attack | Weapon output | Who brings the strongest direct offensive equipment? |
| Infantry general capability | Worn armor and weapon output | Who has the best simple balance of survivability and offense? |
| Ranged attack or general capability with finite ammunition | Bow/crossbow damage multiplied by usable ammunition count; combine with armor only for a general-capability question | Who brings the most finite ranged damage capacity, with survivability included only when the question is general capability? |
| Cavalry in siege defense | Apply the infantry-defense rule as a dismounted troop | A cavalry label does not make `Riding` or mount stats relevant when the troop defends a siege on foot. |

“Primary” is deliberate. A model may include a secondary driver only when the
question requires it and the methodology states why. It must not accumulate
mobility, skill, speed, mount, shield, or other proxies merely because those
fields are available.

For the armor driver, default to armor worn by the troop. Shield durability is
not silently treated as armor; include it only when the question explicitly
asks about blocking or shield endurance.

## Siege-defense overrides

Siege defense changes how two troop families are interpreted:

- Cavalry is evaluated as dismounted infantry. Ignore `Riding`, horse speed,
  maneuver, charge, mount health, and harness armor.
- Ranged ammunition is treated as unlimited. Ammunition count must not create a
  larger score, a cap, or an “infinite” numeric value. If siege-defense analysis
  needs ranged offensive contribution, compare the weapon's per-shot attributes
  and treat ammunition availability as equal across troops.

The defensive question itself still prioritizes armor. Unlimited ammunition is
a context override for ranged offensive capacity, not a reason to replace the
defensive model with an ammo-based model.

## Simplicity rules

1. Prefer raw, inspectable inputs over editorial composites.
2. Start with the dominant driver named in the matrix.
3. Add one secondary driver at a time only to answer a documented deficiency.
4. Do not create separate “protection” and “utility” outputs unless the operator
   has asked two separate questions that need both answers.
5. Do not include `Athletics`, `Riding`, weapon speed, troop skill, reach, damage
   type, mount stats, or charge by default.
6. Speed or skill multipliers are later hypotheses, not automatic parts of
   weapon output. They require an explicit question and comparison against the
   simpler damage-based result.
7. Combined armor-and-weapon models must publish both raw components and state
   the combination rule. Do not hide scale conversion or weights.
8. Alternative equipment rosters remain alternatives. Aggregate them
   deterministically rather than silently selecting the most favorable loadout.

The correct model is the simplest one that answers the stated question, not the
one that consumes the most XML fields.

## Ranged ammunition rule

For bow and crossbow questions outside siege defense, finite ranged capacity is
based on the weapon's damage and the total usable ammunition carried by the
loadout:

```text
finite_ranged_capacity = weapon_damage × usable_ammunition_count
```

The audit must show which bow/crossbow and which compatible arrow/bolt stacks
produced those inputs. Multiple ammunition stacks are summed only when they are
usable by that weapon in the same equipment roster.

For siege defense, ammunition count is excluded because supply is treated as
unlimited. The output records `ammunition_policy=unlimited` rather than
fabricating a numeric infinity.

## Evidence and uncertainty

- Use direct or validated reconstructed values only.
- Missing evidence stays blank and enters an explicit review queue; it never
  becomes a guessed zero.
- Keep field, siege attack, and siege defense outputs separate.
- Keep mod tracks separate.
- Publish the raw drivers beside every score so a rank can be reconstructed.
- Treat theoretical rankings as structural hypotheses until empirical gates
  pass.

Realm of Thrones crafted melee damage remains an evidence limitation in the
current export. That limitation can block attack and general-capability models,
but it must not redefine the operator's scoring rules.

## Relationship to existing candidates

`defensive_role_scores_v2_candidate` remains a reproducible historical
candidate. Its protection/utility and infantry/cavalry split is not the standing
default for new work. New candidates must begin from this context-first matrix
and explain any departure from it.

## Required design note for every new candidate

Every candidate methodology must include a compact declaration like this:

```text
track: realm_of_thrones
context: siege_defense
question: infantry_defense
combat_mode: dismounted
primary_drivers: worn_armor
ammunition_policy: unlimited
secondary_drivers: none
```

If any value is absent or ambiguous, stop at design time and resolve it instead
of inferring a universal formula.
