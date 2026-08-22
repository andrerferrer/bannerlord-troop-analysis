# Role-adjusted empirical combat evaluation

## Status and purpose

This document adds a small empirical interpretation layer for Bannerlord
campaign scoreboards. It does not replace the existing combat evidence,
`kills_per_deployed`, kill share, share-adjusted impact, or frozen theoretical
models.

It addresses two recurring distortions:

1. A dominant ranged troop can consume a large share of the side's available
   kills, making useful frontline troops look irrelevant in a zero-sum kill-share
   table.
2. Ranged troops can deal damage while avoiding contact, while infantry and
   melee cavalry must usually accept contact losses to perform their role.

The solution is not to transfer kills from a ranged troop to a melee troop or to
invent support credit. Keep offensive contribution, retention, and role value as
separate inspectable outputs.

## Required boundaries

Keep track, battle context, player/enemy side, and ordinary-troop rules exactly as
specified by the combat workflow. Apply the existing 5-independent-battle / 20-
deployed evidence gate before publishing a reliable role result.

Role-adjusted results are comparable only inside the same:

```text
track + battle context + role bucket
```

They do not authorize a universal ranged-versus-infantry-versus-cavalry tier.

## 1. Offensive composition diagnostic

Preserve the existing offensive metrics:

```text
kills_per_deployed = troop_kills / troop_deployed
player_side_kill_share = troop_kills / verified_player_side_kills
share_adjusted_impact = kills_per_deployed × player_side_kill_share
```

Add directly verified deployment share over the same contributing battles:

```text
player_side_deployment_share =
    troop_deployed / verified_player_side_deployed

offensive_contribution_ratio =
    player_side_kill_share / player_side_deployment_share

offensive_share_gap =
    player_side_kill_share - player_side_deployment_share
```

Interpretation:

- ratio `> 1`: the troop produced more kills than its manpower share;
- ratio `= 1`: kills were proportional to manpower;
- ratio `< 1`: the troop produced fewer kills than its manpower share;
- a large positive gap on one troop records army-level offensive concentration
  and explains why other units may appear visually overshadowed.

This is an offensive diagnostic only. It must not be described as damage
absorbed, target access created, protection supplied, or kills that another troop
would have produced without the dominant unit.

The deployment denominator must be a direct positive player-side total covering
exactly the same battles as the kill-share denominator. Never reconstruct it from
partial visible troop rows.

## 2. Defensive proxy

Use combat retention as the smallest scoreboard-backed defensive measure:

```text
retention_rate = survivors / deployed
               = 1 - ((deaths + wounded) / deployed)
```

Dead and wounded are both unavailable at the end of that battle. `routed`
remains a separate diagnostic under the repository schema and is not added to
`deployed` or silently folded into retention.

Retention is a durability proxy, not proof of damage absorbed. A troop can retain
units because it was well protected, avoided contact, arrived late, or fought an
easy matchup. That is why retention is interpreted only within a role and battle
context.

Keep `death_rate` beside retention because permanent deaths and recoverable
wounds have different campaign costs, but do not add a third weight to the role
score.

## 3. Role buckets

Resolve the role from the versioned canonical troop `default_group`:

| `default_group` | Empirical role |
|---|---|
| `Ranged`, `HorseArcher` | `ranged` |
| `Infantry` | `frontline_infantry` |
| `Cavalry` | `melee_cavalry` |

For siege defense, map `Cavalry` to `frontline_infantry`, matching the standing
context-first dismounted-cavalry rule. A horse archer remains in the ranged bucket
because its primary attack mode remains ranged.

Unresolved role identity blocks the blended role rank but does not block the raw
offense, kill share, deployment share, or retention outputs.

## 4. Minimal role-adjusted score

Do not blend raw `kills_per_deployed` and retention because their scales differ.
Convert each to a deterministic 0-100 midrank percentile among reliable peers in
the same track, context, and role:

```text
offense_percentile = percentile(kills_per_deployed)
defense_percentile = percentile(retention_rate)
```

Require at least **5 reliable peer rows** in that role bucket. Below that peer
gate, publish the two raw components and withhold the blended score.

Use one simple 2:1 role weight:

```text
frontline_role_score =
    (offense_percentile + 2 × defense_percentile) / 3

melee_cavalry_role_score =
    (offense_percentile + 2 × defense_percentile) / 3

ranged_role_score =
    (2 × offense_percentile + defense_percentile) / 3
```

The 2:1 rule makes the dominant job explicit without adding armor, skills, speed,
reach, horse stats, damage type, or hidden tuning constants. Publish both
percentiles, the role, and the selected weight beside every score.

The blend is an empirical role rank, not a causal equipment model. It does not
change `analysis/model_versions/`.

## Mallister field example — 2026-08-22

The five accepted field battles contain 1,005 directly verified player-side
deployments and 1,029 player-side kills.

| Troop | Role | Deployed | Kills | Deployment share | Kill share | Contribution ratio | Share gap | Retention |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Ravens' Teeth [T6] | ranged | 170 | 281 | 16.92% | 27.31% | 1.61 | +10.39 pp | 98.24% |
| Mallister House Guard [T5] | frontline infantry | 153 | 179 | 15.22% | 17.40% | 1.14 | +2.17 pp | 93.46% |
| Mallister Knight [T5] | melee cavalry | 37 | 30 | 3.68% | 2.92% | 0.79 | -0.77 pp | 83.78% |
| Mallister Eagle Knight [T6] | melee cavalry | 159 | 102 | 15.82% | 9.91% | 0.63 | -5.91 pp | 82.39% |

Intermediate checks:

```text
Ravens deployment share = 170 / 1,005 = 0.169154
Ravens kill share       = 281 / 1,029 = 0.273081
Ravens ratio            = 0.273081 / 0.169154 = 1.614389

House Guard deployment share = 153 / 1,005 = 0.152239
House Guard kill share       = 179 / 1,029 = 0.173955
House Guard ratio            = 0.173955 / 0.152239 = 1.142648
House Guard retention        = 143 / 153 = 0.934641

Eagle Knight deployment share = 159 / 1,005 = 0.158209
Eagle Knight kill share       = 102 / 1,029 = 0.099125
Eagle Knight ratio            = 0.099125 / 0.158209 = 0.626547
Eagle Knight retention        = 131 / 159 = 0.823899
```

The result separates two claims that the offense-only ranking obscures:

- Ravens' Teeth are the army's dominant offensive carry.
- Mallister House Guard is still a strong frontline result: it exceeds its
  manpower share offensively and retains 93.46% of deployments.

The same correction does not automatically rescue Mallister Eagle Knight. Its
retention is almost identical to the whole field side's 82.59% retention, while
its offensive contribution ratio is 0.63. It may move relative to other melee
cavalry once a reliable cavalry peer set exists, but the current data do not
support an elite defensive classification.

## Publication contract

Future empirical reports should publish, when denominators are complete:

1. existing offense rank and share-adjusted impact rank;
2. deployment share, offensive contribution ratio, and offensive share gap;
3. retention and death rate;
4. canonical role and peer coverage;
5. role-adjusted score and role rank only after the five-peer gate.

Do not use the role-adjusted score to reorder different roles into one universal
ladder. When the peer gate is not met, the correct output is a component-level
interpretation, not a provisional blended number.
