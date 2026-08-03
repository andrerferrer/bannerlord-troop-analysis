# Locked execution plan: context-first scoring rework

Status: **ready for execution after this planning PR merges**

Tracking issue: [#58](https://github.com/andrerferrer/bannerlord-troop-analysis/issues/58)

Source decision: `docs/methodology/006_context_first_scoring_rules.md`

Product contract: `plan/context-first-scoring-rework/prd.md`

Technical contract: `plan/context-first-scoring-rework/design.md`

Verification contract: `plan/context-first-scoring-rework/test-plan.md`

## Objective

Replace the composite-first scoring path with the smallest context-appropriate model:

- defense: worn armor;
- attack: validated weapon output;
- general capability: armor and weapon output side by side, with no hidden blend;
- finite bow/crossbow contexts: per-shot output multiplied by compatible usable ammunition;
- siege defense: unlimited ammunition represented as per-shot output, never numeric infinity;
- siege-defense cavalry: dismounted before driver selection.

The rework is complete only when the approved candidate has passed the evidence and promotion gates, a new immutable model version has been published, consumers have been cut over, every implementation PR has been reviewed and squash-merged, and issue #58 can be closed. A blocked promotion verdict is an honest stopping point, not completion.

## Executor contract

Read `AGENTS.md`, then use `@execute-locked-plan`. Do not redesign while executing. Before every slice:

1. fetch `origin/main` and create a fresh branch/worktree from it;
2. confirm the worktree is clean and the step's assumptions still match the repository;
3. run the step's baseline verification before editing;
4. stop and report drift if the baseline, paths, schemas, or evidence differ materially;
5. add the meaningful failing test first, implement only the step, and run focused plus regression tests;
6. commit and push only the slice's files;
7. open a draft PR targeting `main` and link issue #58;
8. self-review the exact latest pushed head, fix every actionable finding, push, and repeat the latest-head review if the SHA changes;
9. before readying, update the PR body and `resume.md` with this PR URL, exact reviewed head, `ready_to_merge`, and the previous slice's verified squash SHA; then mark ready, squash-merge, and verify the PR is closed and its squash commit is present on `main`;
10. post the verified squash SHA to issue #58 after merge. The next slice backfills that SHA into `resume.md`. D10 instead commits `state: complete_on_verified_merge` and removes `plan/.active-plan`; its post-merge issue closure comment is the final receipt, so no eleventh repository PR is needed.

Never force-push `main`, skip hooks, mix unrelated files, fabricate evidence, convert missing values to zero, or edit historical candidate/frozen bytes. Until Step 10, all generated candidate artifacts belong under `analysis/model_candidates/context_first_scores_v1/`.

## Global invariants

- Keep Realm of Thrones, vanilla/War Sails, Nightmare Sails, and TAOM separate.
- Keep field, siege attack, and siege defense separate.
- Keep player and enemy observations separate.
- Treat a battle, not a troop row, as the independent empirical sample.
- Require at least five independent battles and 20 deployed troops for displayed empirical evidence.
- Exclude heroes and multiplayer troops from ordinary rankings.
- Resolve identities only through versioned canonical track audits.
- Leave incomplete values blank with stable review reason codes.
- Publish raw inputs and provenance before ranks.
- Preserve byte identity of existing historical candidates and frozen model versions.
- Require deterministic, offline regeneration from pinned repository inputs.

## Delivery sequence

```text
Step 1 -> Step 2 -> Step 3 -> Step 4 -> Step 5 -> Step 6
                                              -> Step 7 -> Step 8 -> Step 9 -> Step 10
```

Steps 3 and 4 have independent code ownership after Step 2, but the default single-agent execution is sequential. Do not begin Step 5 until both are merged. Each numbered step is one independently reviewable PR.

## Step 1 — Audit the current scoring paths

**Purpose:** establish a reproducible baseline and identify exactly where current candidates answer the wrong question.

**Branch:** `agent/context-first-01-audit`

**Primary files:**

- `scripts/scoring/audit_context_first_candidates.py`
- `tests/test_audit_context_first_candidates.py`
- `analysis/model_candidates/context_first_scores_v1/CURRENT_CANDIDATE_AUDIT.md`

**Actions:**

1. Hash the existing `role_scores_v1`, `role_scores_v2_defense`, v7.1, v7.2, and v7.3 inputs/artifacts.
2. Classify every formula input against context, question, attack mode, mount state, and ammunition policy.
3. Flag mixed defense/offense, undeclared blends, shields-as-armor, mount/mobility/skill leakage, crafted-template proxies, missing-as-zero behavior, and finite-ammunition misuse.
4. Emit file/field evidence and stable classifications; do not publish new rankings.
5. Prove the audit changes no historical artifact.

**Verify:**

```bash
python3 -m unittest -v tests.test_audit_context_first_candidates
git diff --check origin/main...HEAD
```

**Exit gate:** deterministic audit is committed; before/after historical hashes match; PR is reviewed, squash-merged, and verified on `main`.

## Step 2 — Lock the declaration contract

**Purpose:** make model intent explicit and reject invalid combinations before evidence is read.

**Branch:** `agent/context-first-02-contract`

**Primary files:**

- `scripts/scoring/context_first_contract.py`
- `tests/test_context_first_contract.py`
- `docs/methodology/007_context_first_scoring_candidate.md`
- `analysis/model_candidates/context_first_scores_v1/declarations/`

**Actions:**

1. Implement the versioned declaration types and parser from the design.
2. Validate candidate ID, track, context, question, attack mode, mount state, driver set, ammunition policy, source fields, aggregation, and combination rule.
3. Reject `siege_defense + finite`, hidden secondary drivers, undeclared blends, and mounted siege-defense inputs.
4. Add one declaration per intended candidate tuple, with pinned input hashes.
5. Publish stable field-specific error codes.

**Verify:**

```bash
python3 -m unittest -v tests.test_context_first_contract
git diff --check origin/main...HEAD
```

**Exit gate:** every valid tuple parses; every forbidden/missing combination fails before scoring; declarations and documentation agree; PR is merged and verified.

## Step 3 — Implement the armor evidence lane

**Purpose:** answer defense with worn armor only and preserve uncertainty.

**Branch:** `agent/context-first-03-armor`

**Primary files:**

- `scripts/scoring/context_first_equipment.py`
- `tests/test_context_first_armor.py`
- `tests/fixtures/context_first/armor/`

**Actions:**

1. Resolve assigned worn items per troop roster with source provenance.
2. Publish head, body, arm, and leg values before aggregation.
3. Apply only the declaration's armor aggregation; the initial candidate may declare the tested v7.1 weighted aggregation.
4. Average alternative roster outcomes arithmetically while retaining every intermediate.
5. Keep shields, weapons, mounts, harnesses, skills, and mobility out of this lane.
6. Retain incomplete troops in complete output and queue them with stable blank-not-zero reasons.

**Verify:**

```bash
python3 -m unittest -v tests.test_context_first_armor
python3 -m unittest -v tests.test_defensive_role_scores_v2
git diff --check origin/main...HEAD
```

**Exit gate:** equal worn armor produces equal defense regardless of shield/weapon/skill/mount; incomplete evidence is blank and queued; PR is merged and verified.

## Step 4 — Normalize weapon rows and implement fail-closed evidence

**Purpose:** allow attack output only from direct or fully reconstructed, tooltip-validated weapon evidence.

**Branch:** `agent/context-first-04-weapons`

**Primary files:**

- `scripts/scoring/context_first_equipment.py`
- `tests/test_context_first_weapon_evidence.py`
- `scripts/normalization/extract_weapon_attack_rows.py`
- `scripts/normalization/build_crafted_weapon_validation_receipt.py`
- `tests/test_extract_weapon_attack_rows.py`
- `tests/test_crafted_weapon_validation_receipt.py`
- `tests/fixtures/context_first/weapons/`

**Actions:**

1. Verify raw XML bodies and module load order against each track's committed `manifest.csv`, `manifest_modules.csv`, and source-package hashes; never treat the scalar equipment-audit damage cells as component provenance.
2. Normalize one deterministic row per XML weapon attack component, including source file hash and locator; for duplicate item IDs select only the highest-load-order module definition and fail closed on ambiguity inside the winner.
3. Build a per-item tooltip-validation receipt from the reconstructed CSV and repository-addressable tooltip observations; verify both hashes, reject empty/duplicate observations, and emit validated crafted swing/thrust values into the shared attack-row schema with reconstructed and receipt hashes.
4. Union direct and receipt-validated crafted attack rows, resolve the winning item definition, and publish every scoring row's provenance.
5. Select the declared maximum valid swing/thrust damage for the initial melee candidate.
6. Consume reconstructed crafted stats without weakening their completeness rules or changing the historical reconstruction producer.
7. Require PC piece/template catalogs plus the hash-pinned per-item tooltip receipt for crafted items.
8. Reject template-name proxies, incomplete reconstruction, missing attack rows, non-finite values, and failed validation.
9. Keep affected troop/item rows visible with blank results and stable review reasons.
10. If D4 ingests a new raw/source package, use the `AGENTS.md` evidence-batch protocol on this same branch and PR: a normalization agent owns the deterministic normalized artifacts and handoff, then a distinct local analysis agent consumes them as immutable input. A code-only slice over already repository-addressable inputs does not invent a new batch, and scoring code must never silently rewrite normalized evidence.

**Verify:**

```bash
python3 -m unittest -v tests.test_extract_weapon_attack_rows tests.test_crafted_weapon_validation_receipt tests.test_context_first_weapon_evidence tests.test_reconstruct_crafted_weapon_stats
git diff --check origin/main...HEAD
```

**Hard stop:** if the exact source XML package/PC root, crafting catalogs, or tooltip observations are absent, emit a hash-specific acquisition request and stop at D4. Do not reconstruct component rows from lossy audit scalars and do not issue an empty passing receipt.

**Exit gate:** component-level direct evidence and receipt-validated crafted evidence reconstruct output; module overrides resolve deterministically; receipt production is deterministic; no crafted proxy or zero can enter a rank; remaining RoT gaps are quantified rather than hidden; any new evidence batch has separate normalization and analysis ownership; PR is merged and verified.

## Step 5 — Implement finite and unlimited ranged semantics

**Purpose:** answer ranged attack using explicit compatible weapon/projectile pairings.

**Branch:** `agent/context-first-05-ranged`

**Primary files:**

- `scripts/scoring/context_first_ranged.py`
- `tests/test_context_first_ranged.py`
- `tests/fixtures/context_first/ranged/`

**Actions:**

1. Pair audit literal `Bow` only with `Arrow` and `Crossbow` only with `Bolt` from the same roster; fixtures include real audit vocabulary.
2. Enumerate deterministic loadouts by selecting one alternative per equipment slot; different slots are carried together, while same-slot alternatives are never summed.
3. Publish weapon damage, inert observed projectile fields, per-shot output, loadout/stack identities, and usable ammunition count. Candidate v1 declares `projectile_contribution=not_included`.
4. Outside siege defense, calculate `per_shot_output * total_compatible_ammunition` using only stacks selected in distinct slots of the same loadout.
5. Keep alternative weapons and loadouts as separate pairings and average alternatives only after publishing intermediates.
6. In siege defense, force `ammunition_policy=unlimited`, compare per-shot output, ignore stack count, and emit no infinity.
7. Fail closed on missing compatibility or damage evidence.

**Verify:**

```bash
python3 -m unittest -v tests.test_context_first_ranged
git diff --check origin/main...HEAD
```

**Exit gate:** compatible stacks in distinct slots sum once, same-slot alternatives are averaged as separate loadouts, alternative weapons do not double-use ammunition, unlimited results are stack-invariant, and PR is merged and verified.

## Step 6 — Apply context before selecting drivers

**Purpose:** centralize question/context policy, including dismounted siege cavalry.

**Branch:** `agent/context-first-06-engine`

**Primary files:**

- `scripts/scoring/context_first_engine.py`
- `tests/test_context_first_engine.py`

**Actions:**

1. Transform declaration plus troop metadata into an effective scoring context.
2. Force every siege-defense cavalry roster to `dismounted` before evidence selection.
3. Remove Riding, mount, harness, charge, horse speed/maneuver/health, and mounted normalization inputs.
4. Select armor for defense, weapon output for attack, and both independent components for general capability.
5. Preserve the original track, context, question, attack mode, and transformation provenance.
6. Reject any attempt to inject an undeclared secondary driver.

**Verify:**

```bash
python3 -m unittest -v tests.test_context_first_engine
git diff --check origin/main...HEAD
```

**Exit gate:** cavalry and infantry with equal worn armor/weapon evidence score equally in siege defense; all valid tuples select only declared drivers; PR is merged and verified.

## Step 7 — Generate simple candidate outputs

**Purpose:** create complete, rankable, and review artifacts without a universal score.

**Branch:** `agent/context-first-07-outputs`

**Primary files:**

- `scripts/scoring/generate_context_first_scores.py`
- `tests/test_context_first_scores.py`
- generated-schema fixtures under `tests/fixtures/context_first/generated/`; D7 feature tests use temporary scratch roots

**Actions:**

1. Compose the contract, evidence resolvers, ranged policy, and context engine.
2. Emit complete rows, rankable rows, and review queues per declaration.
3. Rank defense by armor and attack by weapon output within one track/context population.
4. For general capability, show armor and weapon components/ranks side by side and leave combined score/rank blank.
5. Exclude heroes and multiplayer troops from ordinary ranks without erasing audit rows.
6. Use stable ordering, decimal serialization, reason codes, and source references.
7. Keep D7 publication in test-owned temporary roots. The first committed candidate-root transaction belongs to D8, after the report renderer exists.

**Verify:**

```bash
python3 -m unittest -v tests.test_context_first_scores
git diff --check origin/main...HEAD
```

**Exit gate:** AC-3 through AC-11 and the theoretical track/context/hero portions of AC-12 pass; full player/enemy side proof remains owned by D9; all rank inputs are reconstructible; PR is merged and verified.

## Step 8 — Publish deterministic reports and RoT top 10s

**Purpose:** make the candidate inspectable and reproducible with one offline command.

**Branch:** `agent/context-first-08-reports`

**Primary files:**

- `scripts/scoring/build_context_first_candidate.py`
- `scripts/scoring/context_first_publication.py`
- `scripts/scoring/write_context_first_reports.py`
- `tests/test_context_first_reports.py`
- `analysis/model_candidates/context_first_scores_v1/README.md`
- `analysis/model_candidates/context_first_scores_v1/candidate_manifest.csv`
- `analysis/model_candidates/context_first_scores_v1/artifact_hashes.csv`
- `analysis/model_candidates/context_first_scores_v1/realm_of_thrones/TOP10.md`

**Actions:**

1. Generate metadata, an immutable `candidate_manifest.csv` for promotion identity, and an outer package `artifact_hashes.csv`; exclude D9 validation outputs from the candidate manifest.
2. Publish direct evidence tables before rankings and summarize review queues.
3. Produce separate RoT top-10 tables for each rankable defense/attack tuple.
4. Show general armor/weapon components side by side, not a synthetic top-10 blend.
5. If fewer than ten rows are rankable, publish the actual rows plus exact evidence reasons.
6. Keep core generation and report rendering independent; let `build_context_first_candidate.py` orchestrate both and let `context_first_publication.py` alone own lock/staging/journal primitives.
7. Build in a staging directory, verify hashes, and replace only the candidate-owned generated subtree atomically.
8. Document the exact single-command regeneration path.

**Verify:**

```bash
python3 -m unittest -v tests.test_context_first_reports
python3 scripts/scoring/build_context_first_candidate.py
python3 scripts/scoring/build_context_first_candidate.py
git diff --exit-code -- analysis/model_candidates/context_first_scores_v1
git diff --check origin/main...HEAD
```

**Exit gate:** isolated reruns are byte-identical; manifests verify; RoT tables are honest about blocked lanes; PR is merged and verified.

## Step 9 — Close evidence gaps and pass the empirical promotion gate

**Purpose:** prove the candidate is reproducible and empirically eligible without pooling or leakage.

**Branch:** `agent/context-first-09-validation`

**Primary files:**

- `scripts/scoring/validate_context_first_candidate.py`
- `tests/test_context_first_validation.py`
- `analysis/model_candidates/context_first_scores_v1/VALIDATION_REPORT.md`
- `analysis/model_candidates/context_first_scores_v1/promotion_gate.json`
- `analysis/model_candidates/context_first_scores_v1/validation_input_hashes.csv`
- repository-owned evidence/audit files needed to close declared gaps

**Actions:**

1. Inventory unresolved canonical IDs, required crafting catalogs/tooltip checks, and missing battle-context coverage.
2. Generate exact acquisition requests for evidence not present in the repository. Do not infer or synthesize it.
3. Ingest new evidence through the repository's normalization/analysis protocol when it arrives.
4. Join theoretical rows only through verified canonical IDs and preserve track, context, and side.
5. Enforce five independent battles and 20 deployed troops for display.
6. Compute uncertainty at battle level and use grouped-by-battle out-of-sample comparisons.
7. Hash every canonical-map, empirical, grouped-out-of-sample, controlled-evidence, and limitations-review input into sorted `validation_input_hashes.csv`; every gate evidence path must occur exactly once in it.
8. Run controlled-evidence checks, reproducibility checks, limitation review, and candidate-to-manifest verification.
9. Emit a machine-readable `passed` or `blocked` verdict with exact failed gates and pin both the exact `candidate_manifest.csv` SHA-256 and `validation_input_hashes.csv` SHA-256; regenerate the outer artifact manifest after validation outputs are staged.

**Verify:**

```bash
python3 -m unittest -v tests.test_context_first_validation tests.test_gate_status
python3 scripts/scoring/validate_context_first_candidate.py
git diff --check origin/main...HEAD
```

**Hard stop:** if RoT crafted melee evidence, canonical IDs, siege-defense battles, or another declared input is still insufficient, merge the honest validation/reporting slice if it is useful, set `resume.md` to `blocked_at: D9`, update issue #58 with the acquisition request, and stop. Do not start Step 10 and do not call the rework complete.

**Exit gate:** `promotion_gate.status=passed`, `promotion_allowed=true`, and both the evaluated candidate-manifest hash and validation-input-manifest hash plus all referenced input bytes match; every input is repository-addressable, boundary and uncertainty checks pass, and the validation PR is merged and verified.

## Step 10 — Promote a new immutable version and cut over

**Purpose:** complete the rework only after Step 9 passes.

**Branch:** `agent/context-first-10-promote`

**Primary files:**

- one new directory under `analysis/model_versions/`
- `README.md`
- `docs/research/EXECUTION_TRACKER.md`
- context-first entry-point documentation and tests

**Actions:**

1. Reconfirm that the latest machine-readable Step 9 verdict has `status=passed`, `promotion_allowed=true`, exact `candidate_manifest.csv` and `validation_input_hashes.csv` hash matches, and no referenced validation input changed.
2. Record SHA-256 hashes of every pre-existing historical candidate and frozen model artifact.
3. Copy the approved candidate into a new versioned immutable package; do not edit any existing version.
4. Point new scoring/report entry points and documentation to the promoted version while keeping historical commands available.
5. Regenerate the candidate twice and prove it matches the promoted package.
6. Run the full suite and verify every pre-existing hash remains unchanged.
7. Complete the latest-head self-review, squash merge, and post-merge verification.
8. In the D10 PR, set `resume.md` to `complete_on_verified_merge`, record the exact reviewed head/PR URL, and remove `plan/.active-plan`. After squash merge, verify `main`, post the squash SHA and final artifact links to issue #58, and close the issue. This external post-merge receipt avoids an eleventh repository PR.

**Verify:**

```bash
python3 -m unittest discover -v
python3 scripts/scoring/build_context_first_candidate.py
python3 scripts/scoring/validate_context_first_candidate.py
git diff --check origin/main...HEAD
```

**Exit gate / definition of done:**

- promotion verdict is `passed`, `promotion_allowed=true`, and its candidate and validation-input manifests plus every referenced input match the promoted bytes;
- a new immutable model version exists;
- all previous model/candidate bytes are unchanged;
- defense, attack, general, ranged, and siege-defense rules have feature coverage;
- deterministic regeneration succeeds twice;
- RoT top-10 views expose evidence-backed results or documented population limits;
- all ten PRs are reviewed, squash-merged, and verified on `main`;
- issue #58 is closed with links to the version, validation report, and final PR;
- no active blocker or unchecked acceptance criterion remains.

## Stop and escalation conditions

Stop at the current step and update `resume.md` when any of these occurs:

- repository reality contradicts the PRD/design/test contract;
- a required change would modify a historical candidate or existing frozen version;
- a proposed score needs an undeclared driver or blend;
- required weapon, armor, canonical identity, or battle evidence is absent;
- a focused or regression test fails outside the step's authorized scope;
- deterministic reruns differ;
- latest-head review finds an issue the step cannot fix without scope expansion;
- GitHub prevents review, readying, merge, or verification.

The escalation must include the current commit, exact failing command, relevant artifact/reason code, smallest proposed plan correction, and whether prior merged slices remain valid.

## Operator handoff prompt

> Execute `plan/context-first-scoring-rework/execution-plan.md` from the first incomplete step. Read `AGENTS.md`, `plan/context-first-scoring-rework/resume.md`, the PRD, design, and test plan before editing. Apply `@execute-locked-plan`; do not re-plan. Deliver one numbered step per PR to `main`, with meaningful tests, exact-head self-review, fixes, squash merge, post-merge verification, and resume/issue updates. Stop on drift. At Steps 4 and 9, never fabricate missing source or empirical evidence; record an exact blocked acquisition request. If Step 4 ingests a new evidence batch, use distinct normalization and analysis agents on the same branch/PR. Do not start Step 10 until `promotion_gate.status=passed`, `promotion_allowed=true`, and the candidate- and validation-input-manifest hashes plus every referenced input match. Continue until the definition of done is fully true or a documented hard stop requires operator evidence.
