# Empiria / V4.4 — execution status (plan v3.1 Fase C)

Status: **field empiria available for Nightmare Sails; the Realm of Thrones field follow-up batch remains below the display gate on its own, and 7 of its 8 priority troops still have zero confirmed-identity evidence in any context**. Theoretical Fase B remains independent.

Do not read this file as the source of truth for the current gate. Run the executable check instead:

```bash
python3 -m scripts.combat_observations gate-status
```

It scans every committed batch under `data/combat_observations/`, sums independent battles and deployed troops per (track, battle context, side) — never pooling field with siege, or player with enemy — and exits `0` only when every track it was asked about already meets the gate. `--track <name>` scopes it to one track; `--format json` gives a machine-readable report. See `scripts/combat_observations/gate_status.py` for the exact aggregation rules and their documented caveats (identity confirmation, the player-side default, cross-batch combination).

## Executable gate status (2026-07-31, as run for this update)

Real output of `python3 -m scripts.combat_observations gate-status`, trimmed to the passing rows and the closest below-gate rows per context (the tool's own output lists every troop; run it locally for the full list):

```text
== nightmare_sails :: GATE MET ==
  captured batches: data/combat_observations/2026-07-28-to-29-nightmare-sails-field
  [field] independent battles captured: 9 -- gate met
    7 troop(s) reaching the gate:
      Battanian Wildling (battanian_wildling): 8 battles, 34 deployed
      Imperial Elite Cataphract (imperial_elite_cataphract): 7 battles, 140 deployed
      Khuzait Khan's Guard (khuzait_khans_guard): 7 battles, 112 deployed
      Nord Huscarl (nord_huscarl): 6 battles, 25 deployed
      Forest Reaper (forest_bandits_bossen): 6 battles, 24 deployed
      Imperial Trained Infantryman (unresolved id): 5 battles, 41 deployed
      Veteran Outrider (eastern_mounted_mercenary_t5): 5 battles, 39 deployed
  [siege_attack] independent battles captured: 0 -- below gate (not observed)
  [siege_defense] independent battles captured: 0 -- below gate (not observed)

== realm_of_thrones :: GATE MET (siege_attack and field only; siege_defense still below) ==
  captured batches: data/combat_observations/2026-07-27-normalized-only,
                     data/combat_observations/2026-07-27-rot-field-followup
  [field] independent battles captured: 6 (2026-07-27-normalized-only: 4 + rot-field-followup: 2) -- gate met
    2 troop(s) reaching the gate:
      Mallister House Guard (mallister_houseguard): 6 battles, 117 deployed
      Ravens' Teeth (ravens_teeth): 5 battles, 86 deployed
    closest below-gate: Riverlands Ranger (river_ranger) 4 battles/167 deployed;
                         Mallister Elite Archer (mallister_elite_archer) 4 battles/135 deployed
  [siege_attack] independent battles captured: 5 -- gate met
    6 troop(s) reaching the gate:
      Riverlands Ranger (river_ranger): 5 battles, 175 deployed
      Mallister Elite Archer (mallister_elite_archer): 5 battles, 164 deployed
      Blackwood House Guard (unresolved id): 5 battles, 98 deployed
      Ravens' Teeth (ravens_teeth): 5 battles, 88 deployed
      Mallister House Guard (mallister_houseguard): 5 battles, 68 deployed
      Mallister Eagle Knight (mallister_knight): 5 battles, 67 deployed
  [siege_defense] independent battles captured: 1 -- below gate
    0 troop(s) reaching the gate; closest: Riverlands Ranger 1 battle/52 deployed (needs 4 more battles)

== vanilla :: below gate (no batches captured) ==
== taom :: below gate (no batches captured) ==

Overall (all four tracks requested): at least one requested track is below the gate.
```

This is a genuinely new result versus the paragraph below it: **combining the two already-merged Realm of Thrones field batches** (`2026-07-27-normalized-only`, 4 field battles, and `2026-07-27-rot-field-followup`, 2 field battles — disjoint battle IDs, disjoint screenshot hashes, same versioned `data/realm_of_thrones/audit/realm_of_thrones_troops.csv` identity resolution) already clears the field gate for `ravens_teeth` (5 battles / 86 deployed) and `mallister_houseguard` (6 battles / 117 deployed). Neither is one of the 8 RoT priority troops except Ravens' Teeth. `siege_attack` was already gated by the older `2026-07-27-normalized-only` batch alone and was simply never called out as "gate met" in this file before. `siege_defense` and 7 of the 8 RoT priority troops (everything but Ravens' Teeth) still have **zero** confirmed-identity evidence in any context — that is what `2026-07-31-rot-field-plan/` targets.

None of this changes `nightmare_sails`, which remains gated purely on the strength of its own single field batch (no cross-batch combination needed).

## Online empirical batches

### Realm of Thrones

- Reviewed 2026-07-26/27 batch: `data/combat_observations/2026-07-27-normalized-only/`.
- Field follow-up B01–B02: `data/combat_observations/2026-07-27-rot-field-followup/`.
- Follow-up coverage: 2 independent field battles, 17 included ordinary-troop occurrences, 0 reliable rows.
- The follow-up is valid evidence but is insufficient **by itself** for the 5-battle / 20-deployed display gate. Combined with the older `2026-07-27-normalized-only` field battles it does cross the gate for 2 troops — see the "Executable gate status" section above.

### Nightmare Sails

- Field batch B03–B11: `data/combat_observations/2026-07-28-to-29-nightmare-sails-field/`.
- Coverage: 9 independent field battles, 113 included ordinary-troop occurrences, 7 reliable rows.
- Track resolution is backed by exact display-name matches in `data/nightmare_sails/audit/nightmare_sails_troops.csv`.
- Two partially obscured rows remain excluded in the reviewed layer rather than guessed.

Reliable field rows:

1. Nord Huscarl — 6 battles, 25 deployed, 3.120 kills/deployed.
2. Battanian Wildling — 8 battles, 34 deployed, 2.676 kills/deployed.
3. Forest Reaper — 6 battles, 24 deployed, 1.375 kills/deployed.
4. Imperial Elite Cataphract — 7 battles, 140 deployed, 1.350 kills/deployed.
5. Veteran Outrider — 5 battles, 39 deployed, 0.923 kills/deployed.
6. Khuzait Khan's Guard — 7 battles, 112 deployed, 0.884 kills/deployed.
7. Imperial Trained Infantryman — 5 battles, 41 deployed, 0.780 kills/deployed.

These are descriptive campaign-contribution rates, not intrinsic-strength rankings. Tracks, sides, and contexts remain separate.

## Reproducibility state

- All 11 scoreboards are split into track-correct repository batches.
- Deterministic normalized archives, reconstruction instructions, SHA-256 manifests, structural validation, review layers, analytical outputs, and protocol state are repository-addressable.
- Raw screenshots are not retained in Git; original filenames and image SHA-256 values are versioned. This is allowed after deterministic normalization passes the repository gates.
- Off-screen rows are not inferred.
- Heroes are excluded from ordinary troop rankings.

## Realm of Thrones priority troops

When compatible RoT evidence reaches the display gate, prioritize:

- Ravens' Teeth
- Goldenheart Warrior
- Celtigar Banneret
- Lyseni Enforcer
- Myrish Artisan of War
- Golden Company Mahout
- Sarnori Spider
- Baratheon Hammerknight

## V4.4 kinetic overlay

Still blocked on exact-item profiles and a dedicated model-change pull request. This is outside the empirical batch critical path.

`analysis/model_versions/` remains frozen.
