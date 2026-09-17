# Phase 2 analysis prompt — Qartheen Enthroned Guardian field follow-up

You are the **separate analysis agent** for the same branch and draft pull request created by the normalization agent.

## Mandatory first steps

1. Read `AGENTS.md`, `.agents/skills/analyze-bannerlord-combat-zip/SKILL.md`, `docs/methodology/ADR-002-two-agent-batch-workflow.md`, and `docs/protocols/analysis-task-v1.md`.
2. Run:
   ```bash
   cd data/combat_observations/2026-09-16-rot-qartheen-enthroned-guardian-field-phase1
   python3 source/rebuild_phase1_bundle.py --check
   python3 ../../../tests/test_rot_qartheen_enthroned_guardian_phase1_bundle.py
   ```
3. Verify the repository branch is fresh against `main`.
4. Preserve all Phase 1 normalized files byte-for-byte. Corrections must be additive under `reviewed/`.

## Analysis scope

Analyze **all 13 visible ordinary-troop rows**, not only the Guardian. Keep the 18 character rows excluded from ordinary-troop headline metrics.

Safe review boundaries:

- One ordinary row in the Deserters battle has an unreadable label but reliable numeric values (`0 survivors`, `1 wounded`, all other cells zero). Keep it unresolved and unpooled.
- `Dornish Archer [T3]` is a provisional raw transcription because the label prefix is crossed by chat text.
- Never allocate offscreen survivors or upgrade-ready counts to visible identities.
- Game version, commander mode, and boost status remain unknown.

## Primary research question

Determine what the two new completed field battles add to the existing evidence for `Qartheen Enthroned Guardian [T6]` (`canonical_troop_id=enthroned_guardian`).

The merged Sep 12–14 analysis already publishes a completed field cohort for the same player party:

```text
5 independent battles
195 deployed
698 kills
3.579487 kills/deployed
22.9003% player-side kill share
9.9490% player-side deployment share
2.301770 offensive contribution ratio
84.1026% retention
```

Use the repository files listed in `ANALYSIS_TASK_V1.json` as the source of truth and recompute rather than copying these values blindly.

For the new follow-up, publish at least:

- independent battles;
- Guardian deployed, survivors, kills, deaths, wounded, routed;
- kills/deployed;
- player-party kill share;
- player-party deployment share;
- offensive contribution ratio (`kill_share / deployment_share`);
- retention;
- battle-level rows;
- uncertainty/insufficient-battle status.

Publish three clearly separated views:

1. **Historical mixed-campaign completed field cohort**.
2. **New two-battle dedicated follow-up**.
3. **Combined descriptive continuity** only if compatibility checks pass, with an explicit non-causal caveat.

The absolute kills/deployed rate is constrained by enemy availability in these two small battles, so do not read a lower raw rate as a collapse without inspecting kill share and deployment share.

## Queue decision

Update `data/combat_observations/test_queues/realm_of_thrones.json` in this same pull request if the analysis changes the Guardian's testing status.

Rules:

- The operator selected the Guardian in practice by fielding 85 and 88 of them in these two follow-up battles.
- Do not invent a future target.
- Preserve the Arryn Winged Knight verification hold.
- If the historical 5-battle gate remains valid and the follow-up supports the same direction, close dedicated Guardian testing with evidence references.
- Otherwise set it as the active test and state the exact missing evidence.
- `ordered_queue` must remain empty unless an already-authorized repository source says otherwise.

## Required outputs

At minimum add:

```text
analysis/ANALYSIS_REPORT.md
analysis/guardian_battle_evidence.csv
analysis/guardian_cohort_comparison.csv
analysis/ordinary_occurrences.csv
analysis/insufficient_evidence.csv
analysis/excluded_character_rows.csv
analysis/screenshot_deduplication_audit.csv
analysis/input_verification.json
analysis/validation_report.json
analysis/artifact_hashes.csv
analysis/NEXT_TEST_RECOMMENDATION.md
analysis/analysis_state.json
reviewed/review_resolutions.csv
reviewed/phase2_review_summary.json
```

Add a deterministic generator and tests when practical. Update the pull-request body and append the versioned complete-state protocol comment. Keep the PR unmerged until human confirmation.
