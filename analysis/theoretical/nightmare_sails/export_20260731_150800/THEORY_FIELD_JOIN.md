# Nightmare Sails theory–field join

## Scope

This document descriptively joins the pinned `nightmare_sails`
`role_scores_v1` export at `export_20260731_150800` to
`data/combat_observations/2026-07-28-to-29-nightmare-sails-field/analysis/ranking_reliable.csv`.
It covers every row in that seven-row field file. It does not combine the two
sources into a score or ranking and does not treat either source as a causal
explanation of the other.

The comparison stays inside the `nightmare_sails` track and the `field`
context. The field rows describe visible player-side ordinary troops only;
enemy-side observations, siege attack, and siege defense are not added. The
theory values are XML-structural, `empirical=false`, and comparable only within
their own role lists. Field kills/deployed is campaign performance under the
observed battles, not the same quantity as a theoretical role score.

## Sources and evidence envelope

- Theory: `nightmare_sails_troop_role_scores_v1.csv` and `OVERVIEW.md`, package
  digest `fc87e360e884cc9aa4baa15e4bdd372824c1f7054b2a9acef6d8c0df3732db3b`.
  The overview reports 371 scored rows and 270 rows after its documented
  track-specific filter. Crafted-melee values are conservative template
  proxies, not measured damage or hit-to-kill results.
- Field: 9 independent field battles, 113 consolidated visible player-side
  ordinary-troop rows, and 37 troop labels. The existing analysis produced 7
  rows in `ranking_reliable.csv` and retained 30 other labels as insufficient
  evidence.
- The field reliability filter already applied by `ranking_reliable.csv`
  requires at least 5 independent battles **and** at least 20 deployed troops
  for each troop/context row. Heroes, review-needed rows, and medium-confidence
  rows were excluded upstream; uncertainty intervals were bootstrapped at the
  battle level.
- This document does **not** claim that a display gate is met. It reports the
  sample sizes and filter attached to the pre-existing reliable-field artifact.
  Only screenshot-visible rows are represented, off-screen rows are not
  inferred, and partial screenshots can undercount appearances.

Field row numbers below are positions within the seven-row reliable field
artifact. Theory ranks are positions within separate role-specific theory
lists. They are shown as source metadata and must not be compared as though
they were one ladder.

## Join coverage

Four field rows have a confirmed canonical ID present in the theoretical score
file. Two more have confirmed field IDs but are absent from theory because the
versioned troop audit marks them as non-soldiers; they are not imputed. The
remaining field row has no confirmed canonical ID and is not joined by its
provisional slug. Conversely, 266 of the overview's 270 post-filter theoretical
troops have no canonical counterpart in the reliable field artifact; no field
result is imputed for them.

## Per-troop comparison

### Nord Huscarl (`nord_huscarl`) — joined

- **Theory:** defensive score 71.7, rank 18 / tier A; offensive-melee score
  62.4, rank 8 / tier B. The structural drivers include 204.4 total armor,
  62.0 effective armor, and a shield. The melee score uses the conservative
  crafted-weapon proxy.
- **Field:** row 1; 6 battles, 25 deployed, 78 kills, 20 survivors, 1 death,
  4 wounded, and 0 routed. Kills/deployed is 3.120 (battle-bootstrap 95%
  interval 2.667–3.520); casualty rate is 0.200.
- **Agreement:** the high survival count is directionally consistent with a
  strong defensive structural profile.
- **Tension:** its field kill rate is the highest in this seven-row artifact,
  while theory places it below several troops in both its defensive and melee
  role lists. That is a descriptive mismatch in prominence, not evidence that
  the role model caused or underpredicted kills.

### Battanian Wildling (`battanian_wildling`) — joined

- **Theory:** skirmisher score 53.0, rank 18 / tier B; defensive score 59.4,
  rank 35 / tier B; offensive-melee score 27.5, rank 101 / tier C. Its
  structural record has a shield, 186.3 total armor, 58.2 effective armor, and
  a throwing loadout; the direct throw-damage field is unavailable, so the
  skirmisher score remains conservative.
- **Field:** row 2; 8 battles, 34 deployed, 91 kills, 26 survivors, 0 deaths,
  8 wounded, and 0 routed. Kills/deployed is 2.676 (95% interval
  2.059–3.286); casualty rate is 0.235.
- **Agreement:** the combination of substantial field output and no recorded
  deaths is directionally compatible with its skirmisher role and above-mid
  defensive profile.
- **Tension:** its field kill rate is second in this artifact, more prominent
  than its tier-B skirmisher/defensive and tier-C melee placements. The field
  artifact does not identify which weapon or role produced those kills.

### Forest Reaper (`forest_bandits_bossen`) — field only

- **Theory:** no row exists in `nightmare_sails_troop_role_scores_v1.csv`. The
  versioned audit identifies this troop's occupation as `Bandit` and
  `is_soldier=False`, so it is outside the soldier-only theory input. No theory
  score or rank is imputed.
- **Field:** row 3; 6 battles, 24 deployed, 33 kills, 24 survivors, no deaths,
  wounded, or routed. Kills/deployed is 1.375 (95% interval 0.917–1.792);
  casualty rate is 0.000.
- **Comparison:** theory–field agreement or disagreement cannot be assessed
  because the theoretical side is missing.

### Imperial Elite Cataphract (`imperial_elite_cataphract`) — joined

- **Theory:** defensive score 100.0, rank 1 / tier S; offensive-melee score
  77.8, rank 3 / tier A. Its structural drivers include a shield, horse, 207.7
  total armor, and 60.2 effective armor; melee is a crafted-polearm proxy.
- **Field:** row 4; 7 battles, 140 deployed, 189 kills, 129 survivors, 1 death,
  10 wounded, and 0 routed. Kills/deployed is 1.350 (95% interval
  0.935–1.752); casualty rate is 0.079.
- **Agreement:** the low casualty rate is directionally consistent with the
  strongest defensive theory placement.
- **Tension:** its kill rate is fourth in this reliable-field artifact rather
  than similarly dominant. Theory's defensive rank is not a prediction of
  kills/deployed, so this is a difference in observed prominence, not a model
  error claim.

### Veteran Outrider (`eastern_mounted_mercenary_t5`) — field only

- **Theory:** no row exists in `nightmare_sails_troop_role_scores_v1.csv`. The
  versioned audit identifies the occupation as `Mercenary` and
  `is_soldier=False`, outside the soldier-only theory input. No theory score or
  rank is imputed.
- **Field:** row 5; 5 battles, 39 deployed, 36 kills, 38 survivors, 0 deaths,
  1 wounded, and 0 routed. Kills/deployed is 0.923 (95% interval
  0.410–1.400); casualty rate is 0.026.
- **Comparison:** theory–field agreement or disagreement cannot be assessed
  because the theoretical side is missing.

### Khuzait Khan's Guard (`khuzait_khans_guard`) — joined

- **Theory:** ranged score 100.0, rank 1 / tier S; offensive-melee score 67.2,
  rank 4 / tier A; defensive score 63.2, rank 30 / tier B. The structural
  record is mounted, with 181.0 total armor, 54.6 effective armor, a
  `steppe_war_bow`, and a crafted-polearm melee proxy.
- **Field:** row 6; 7 battles, 112 deployed, 99 kills, 111 survivors, 0 deaths,
  1 wounded, and 0 routed. Kills/deployed is 0.884 (95% interval
  0.321–1.563); casualty rate is 0.009.
- **Agreement:** the near-zero casualty rate is directionally compatible with
  a capable mounted troop whose theory profile is not defensively weak.
- **Tension:** the field kill rate is sixth in this artifact despite the
  top-ranked ranged and high-ranked melee theory placements. The wide field
  interval and campaign confounders prevent interpreting that difference as a
  causal contradiction.

### Imperial Trained Infantryman (`imperial_trained_infantryman`) — unresolved field identity

- **Theory:** no join is made. The field artifact leaves
  `canonical_troop_id` empty and marks the identity `unresolved`. A
  matching-looking provisional slug is not treated as a canonical XML ID, even
  though that string occurs in the audit. No theory score or identity is
  imputed.
- **Field:** row 7; 5 battles, 41 deployed, 32 kills, 39 survivors, 0 deaths,
  2 wounded, and 0 routed. Kills/deployed is 0.780 (95% interval
  0.567–0.973); casualty rate is 0.049.
- **Comparison:** theory–field agreement or disagreement cannot be assessed
  until the field identity is canonically resolved in a reviewed layer.

## Interpretation boundary

The four directional agreements and tensions above do not recalibrate
`role_scores_v1`, establish intrinsic troop strength, or recommend gameplay
choices. The field batch is victory-only observational evidence affected by
army composition, enemy composition, map, campaign progression, player orders,
and screenshot visibility. Theory describes structural loadouts and role
proxies; field describes observed campaign contribution. Keeping those
quantities separate is the result of this join.
