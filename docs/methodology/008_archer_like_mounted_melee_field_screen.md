# Mounted-melee archer-like field screen

## Status and question

This is a Realm of Thrones **candidate-discovery hypothesis**, not a frozen
combat model, causal claim, universal tier, or substitute for battle evidence.
It answers one narrow question:

> Which mounted melee troops are structurally plausible candidates for ranged-like
> sustained kill volume in field battles?

The operator observation is that `mounted_kingsguard` combines melee contact
with the kill volume and low death frequency normally associated with protected
ranged troops. The screen turns that observation into a reproducible test queue
without editing `analysis/model_versions/`.

```text
track: realm_of_thrones
context: field
question: mounted_melee_sustained_kill_volume_candidate
attack_mode: melee
mount_state: mounted_with_dismounted_transition
primary_drivers: direct_melee_weapon_output
ammunition_policy: not_applicable
secondary_drivers: melee_skill_floor, mobility_floor, worn_armor, shield_endurance, harness_armor, loadout_coverage
armor_source_fields: realm_of_thrones_roster_audit_summary.csv armor_total
armor_aggregation: arithmetic_mean_across_alternative_rosters
weapon_damage_source_fields: unavailable_for_realm_of_thrones_crafted_melee_weapons
projectile_contribution: not_applicable
roster_aggregation: arithmetic_mean_for_numeric_fields; all_rosters_for_required_coverage
combination_rule: conjunctive_candidate_screen_only; no_effectiveness_score
```

Direct crafted-melee damage is not reconstructed in the current audit. That
prevents a theoretical effectiveness rank. Skills, mobility, protection, and
loadout coverage are therefore used only as support prerequisites for selecting
the next empirical test.

## Observed outcome signature

The empirical signature keeps output and survival separate:

```text
kills_per_deployed = kills / deployed
death_rate = deaths / deployed
kills_per_death = kills / deaths  # undefined when deaths == 0
```

A troop has an **observed archer-like melee field result** only when all of the
following are true in compatible player-side field evidence:

1. at least 5 independent battles;
2. at least 20 deployed troops;
3. at least 2.0 kills per deployed troop; and
4. death rate no greater than 5%.

The 2.0 output boundary sits below both ranged anchors currently available:
Ravens' Teeth at 2.330579 and the Goldenheart direct aggregate at 2.736842.
Goldenheart lacks a compatible death numerator, so it is an output-only anchor.

| Troop | Mode | Battles | Deployed | Kills | Deaths | Kills/deployed | Death rate | Kills/death |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Captain of the Kingsguard | melee | 8 | 81 | 257 | 3 | 3.172840 | 3.7037% | 85.6667 |
| Ravens' Teeth | ranged | 15 | 1,089 | 2,538 | 25 | 2.330579 | 2.2957% | 101.5200 |
| Goldenheart Warrior | ranged | 11 | 190 | 520 | unavailable | 2.736842 | unavailable | unavailable |
| Mallister Eagle Knight | incidental melee co-observation | 8 | 177 | 165 | 6 | 0.932203 | 3.3898% | 27.5000 |

The Captain produces 3.172840 / 0.932203 = **3.4036 times** the Mallister
Knight's kills per deployed while their death rates remain similar
(3.7037% versus 3.3898%). Protection alone therefore does not explain the
Captain result.

## Structural rule: no weak link

Ranged troops gain sustained output from repeated access to targets while
remaining out of contact. A melee troop must manufacture the same property by
passing three simultaneous bottlenecks:

```text
sustained melee kill volume
    requires target access
    AND contact conversion
    AND combat uptime
```

- **Target access and transition:** high Riding and Athletics prevent the troop
  from becoming ineffective after the charge, horse loss, congestion, or a
  dismounted phase.
- **Contact conversion:** a high floor across OneHanded, TwoHanded, and Polearm,
  plus sword/polearm coverage, avoids a weak combat mode.
- **Combat uptime:** worn armor, shield endurance, and harness armor preserve
  time available to create additional contacts.

These are conjunctive gates. A large shield must not compensate numerically for
poor target access or conversion, so the screen deliberately has no weighted
sum.

### Captain-like strict signature

- ordinary cavalry soldier with horse and shield in every audited roster;
- `min(OneHanded, TwoHanded, Polearm) >= 250`;
- `min(Riding, Athletics) >= 240`;
- mean worn armor `>= 200`;
- mean shield HP `>= 350`;
- mean harness armor `>= 75`;
- every roster contains OneHandedSword, TwoHandedPolearm, and TwoHandedSword.

### Near-match test queue

- ordinary cavalry soldier with horse and shield in every audited roster;
- `min(OneHanded, TwoHanded, Polearm) >= 220`;
- `min(Riding, Athletics) >= 220`;
- mean worn armor `>= 190`;
- mean shield HP `>= 350`;
- mean harness armor `>= 70`;
- every roster contains OneHandedSword and TwoHandedPolearm.

`scripts/analysis/generate_archer_like_mounted_melee_candidates.py` applies
these gates to the versioned audit. The generated CSV is a shortlist, not a
rank. Passing it does not authorize an S-tier label.

## Current interpretation

Only Captain of the Kingsguard passes the strict signature. Arryn Winged
Knight, Mallister Eagle Knight, Realm Paladin, and Knights of Starfall pass the
near-match screen. Mallister is the essential negative contrast, but it was not
the deliberately isolated target of the Mallister test. The Eagle Knight was
co-observed while the House Guard/family composition was being tested and its
compatible presence happens to clear the display gate: 8 field battles, 177
deployed, and 0.932203 kills per deployed. This incidental evidence is useful
as a contrast but must not be described as a dedicated Eagle Knight test. It
also demonstrates why battle validation remains mandatory.

Arryn remains the next test because it is the closest below-gate candidate in
the batch-specific mechanical comparison. Its current field evidence is 2
battles and 13 deployed; the minimum extension is 3 additional independent
field battles and 7 additional deployed troops.

## Promotion boundary

Do not promote this screen into `analysis/model_versions/` until multiple
independent melee positives and negatives have gate-clearing field evidence,
crafted melee damage is directly available or validly reconstructed, and a
dedicated model-change review demonstrates out-of-sample discrimination. Field,
siege attack, and siege defense remain separate.
