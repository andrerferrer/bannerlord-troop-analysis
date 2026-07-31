# Phase 2 analysis prompt — Nightmare Sails field plan

Copy the prompt below into the local analysis agent after this batch's capture and Phase 1 normalization are complete. Continue the same evidence-batch branch and draft pull request; do not open a separate analysis PR.

---

You are the **Phase 2 local analysis agent** for:

```text
data/combat_observations/2026-07-31-ns-field-plan
```

The batch track is `nightmare_sails`, its only permitted battle context is `field`, and its pinned theoretical export is `export_20260731_150800`.

## Stop conditions

Read `AGENTS.md` and this entire prompt before changing files. If the batch README still says `NO DATA CAPTURED YET`, Phase 1 is incomplete, any expected input is absent, or no valid pending `bannerlord-analysis-task:v1` protocol comment exists on the batch PR, stop and report the blocker. Do not manufacture empty results or observations.

## Inputs and integrity

1. Read `analysis_pack/SCHEMA.md` and `analysis_pack/AGENT_PROMPT.md` first.
2. Read the latest valid protocol comment and use its `handoff_path`, branch, task ID, expected archive hash, artifact hashes, raw-source hashes, and merge settings.
3. Reconstruct the normalized archive with the committed `bundle/README.md` commands.
4. Verify the archive SHA-256, every Phase 1 artifact hash, and every retained raw-source hash before analysis.
5. Rerun repository structural validation. If any hash or invariant fails, publish an append-only full-state `blocked` protocol comment and stop.
6. Treat root manifests, capture inputs, normalized JSONL/CSV records, bundle chunks, Phase 1 validation, and artifact hashes as immutable.

Record any correction only in `review/` using the review-correction contract and full provenance. Never silently rewrite normalized evidence.

## Canonical identity and theoretical join

- Resolve identities only against `analysis_pack/nightmare_sails/` and `data/nightmare_sails/audit/` from `export_20260731_150800`.
- Verify the pinned package manifest before joining. Do not re-export XML, rebuild the audit, or read raw module XML unless a package hash mismatch is first proven and documented.
- For theory-side rows, require `item_found == True` and `occupation == Soldier`; remove multiplayer and obsolete troops; keep NavalDLC troops.
- Aggregate alternative equipment rosters rather than summing them.
- Keep the empirical result and the XML-structural theory result visibly separate. A join is context, not calibration or causal proof.
- Do not compare or pool scores across tracks.

## Empirical boundaries

1. Use the battle as the independent sampling unit.
2. Keep player and enemy sides separate in every aggregate and output.
3. Accept only `field`; quarantine any siege attack, siege defense, naval, raid, hideout, keep-phase, or undefined-context record.
4. Exclude heroes, players, party totals, side totals, artifacts, and unresolved/review-needed rows from ordinary troop rankings.
5. Never infer off-screen rows or deployments.
6. Consolidate duplicate scroll-page occurrences within each battle before aggregation.
7. Recalculate rates from summed counts; do not average occurrence-level rates.
8. Require **at least 5 independent battles AND at least 20 deployed troops** for each troop/context/side estimate before displaying a claim.
9. Publish every below-gate row in `insufficient_evidence.csv`; do not drop it.
10. Do not modify `analysis/model_versions/`.

## Required analysis

For each canonical ordinary troop, separately by side and field context, calculate independent battles, deployed, survivors, kills, deaths, wounded, routed, kills/deployed, survival rate, death rate, wounded rate, casualty rate, and routed rate. Produce a complete view plus a display-gated view. For gated estimates, calculate deterministic battle-level bootstrap intervals and record the seed and repetitions.

Audit the planned priority set explicitly:

```text
nord_huscarl
battanian_wildling
imperial_elite_cataphract
khuzait_khans_guard
vlandian_marine_t5
aserai_marine_t5
battanian_marine_t5
empire_marine_t5
sturgia_marine_t5
```

Report actual coverage and deviations from the plan. Compare compatible historical Nightmare Sails field evidence only through an explicit same-track, same-context, same-side compatibility audit; never silently pool batches. Interpret results only as observed campaign contribution. Discuss enemy composition, terrain, outcome, captain/perk effects, player orders, roster deviations, partial screenshots, and victory/defeat selection as confounders. Do not claim universal superiority, causal equipment effects, predictive calibration, or a model change.

## Outputs and completion

Write analytical outputs under this batch's `analysis/` directory and review decisions under `review/`, following the filenames and conventions used by the completed Realm of Thrones and Nightmare Sails field batches. At minimum include input verification, canonical identity audit, context/side coverage, complete ranking, gated ranking, insufficient evidence, validation, artifact hashes, and an analytical report.

Use a separate analysis-phase commit. Publish an append-only full-state `in_progress` protocol comment before material work, then `blocked` or `complete` as appropriate. Update the PR checklist and analytical summary, mark the PR ready only after every acceptance gate passes, and merge only with the method declared by the protocol comment.

Before completion, prove that all Phase 1 hashes still match and that `analysis/model_versions/` is unchanged.

---
