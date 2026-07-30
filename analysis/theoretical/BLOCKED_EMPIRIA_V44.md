# Empiria / V4.4 — blocked-on-data (plan v3.1 Fase C)

Status: **partially unblocked, not queued**. Does not block theoretical Fase B.

## What is already online

- The reviewed Realm of Thrones combat batch from 2026-07-26/27 is repository-addressable and analyzed under `data/combat_observations/2026-07-27-normalized-only/` and `analysis/empirical/2026-07-27/`.
- Multi-track XML SSOT packages and theoretical `role_scores_v1` outputs are online for `nightmare_sails`, `taom`, and `realm_of_thrones`.
- The `bannerlord-analysis-task:v1` workflow, dispatcher, validation gates, and two-agent handoff protocol are online.

## Current 2026-07-27 to 2026-07-29 screenshot set

A new set of **11 final scoreboards** was normalized outside the repository into:

- `bannerlord_battles_normalized_2026-07-27_to_29.xlsx`
- `bannerlord_battles_normalized_2026-07-27_to_29.zip`
- CSV tables for battles, sides, parties, and visible player troops

These artifacts are **not yet repository-addressable** and therefore are not an authoritative empirical input.

The screenshots must not be treated as one track:

- B01–B02: visibly Realm of Thrones (`Lannister` / `Mallister`).
- B03–B11: track remains unresolved from the scoreboard alone; do not assign `nightmare_sails` or `taom` by guess.

Battle context is also unresolved for this set. The result screen alone does not reliably establish `field`, `siege_attack`, or `siege_defense`.

## Required next steps

1. **Split the intake by track.** Create separate evidence batches and separate draft PRs for B01–B02 and B03–B11.
2. **Resolve the track for B03–B11.** Confirm the campaign/module set before canonical identity matching.
3. **Label battle context.** Record `field`, `siege_attack`, or `siege_defense` for every battle; preserve unresolved cases in `review_queue.csv`.
4. **Rebuild canonical normalized bundles.** Convert the staging spreadsheet/CSVs into deterministic JSONL/CSV artifacts using the current batch schema.
5. **Add reproducibility metadata.** Commit source provenance, screenshot SHA-256 values, artifact hashes, validation report, reconstruction instructions, and normalized archive hash.
6. **Preserve partial visibility.** B03 and B04 have complete visible player troop lists; the other screenshots have off-screen rows and must remain explicitly partial.
7. **Create the Phase 2 handoff.** Add `handoff/ANALYSIS_PROMPT.md`, open one draft PR per track, and publish a valid `bannerlord-analysis-task:v1` `pending` comment.
8. **Run empirical analysis only after the gates pass.** Keep sides and contexts separate; display only cells with at least 5 independent battles and 20 deployed troops.

## Current blocker summary

- **Repository upload:** pending for the new 11-scoreboard set.
- **Track identity:** resolved for B01–B02; unresolved for B03–B11.
- **Battle context:** unresolved for all 11 battles.
- **Display gate:** cannot be assessed safely until track/context splitting is complete.

## Realm of Thrones priority troops

When a compatible RoT empirical batch reaches the display gate, prioritize:

- Ravens' Teeth
- Goldenheart Warrior
- Celtigar Banneret
- Lyseni Enforcer
- Myrish Artisan of War
- Golden Company Mahout
- Sarnori Spider
- Baratheon Hammerknight

## V4.4 kinetic overlay

Requires exact-item profiles / model-change PR. Outside this critical path.
`analysis/model_versions/` remains frozen.
