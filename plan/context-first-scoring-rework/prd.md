# Context-First Scoring Rework PRD

## Overview

Replace the repository's universal/composite-first scoring path with a candidate pipeline that selects the game track, battle context, troop question, attack mode, and mount state before choosing the smallest evidence-backed driver set. The work applies issue #58 and `docs/methodology/006_context_first_scoring_rules.md` without rewriting historical candidates or the frozen v7.1 general and v7.3 burst model versions. The primary users are repository analysts and implementation agents who need deterministic, inspectable defense, attack, and general-capability outputs whose scope and evidence limits are explicit.

## Goals

1. Make every new score traceable to a validated context-first declaration.
2. Publish direct armor and weapon evidence before derived scores or ranks.
3. Implement simple, question-specific defense, attack, and general-capability outputs.
4. Apply finite and unlimited ammunition semantics correctly.
5. Treat cavalry as dismounted in siege defense and remove all mounted inputs there.
6. Fail closed when required evidence, especially crafted-weapon evidence, is absent or unvalidated.
7. Produce deterministic candidate artifacts, review queues, reports, and Realm of Thrones top-10 views.
8. Compare theoretical candidates with empirical evidence only within repository evidence and promotion gates.
9. Close the required evidence gaps, pass the documented promotion gates, and cut new scoring consumers over to a newly promoted context-first model without changing historical artifacts or previously frozen model versions.

## Non-goals

- Editing, regenerating, deleting, or relabeling frozen v7.1 or v7.3 artifacts.
- Rewriting `role_scores_v1` or `defensive_role_scores_v2_candidate`; they remain reproducible historical candidates.
- Defining one universal score across tracks, contexts, questions, attack modes, or mount states.
- Selecting a default numeric blend for general capability.
- Adding speed, skill, reach, damage type, mobility, shield, mount, harness, charge, perks, or reliability merely because the fields exist.
- Extending the bow/crossbow finite-ammunition formula to throwing weapons, slings, or other weapon families.
- Claiming universal troop superiority or causal attribute effects from campaign observations.
- Pooling tracks, player and enemy sides, or field, siege-attack, and siege-defense observations.
- Inferring off-screen rows, canonical IDs, missing equipment values, or missing attack rows.

## Settled decisions

1. The repository integration branch is `main`; implementation PRs must not target `dev`.
2. The declaration is the single source of truth for candidate intent. It is validated before audit rows are read and contains: schema version, candidate ID, track, context, question, attack mode, mount state, primary drivers, ammunition policy, secondary drivers, armor source fields, armor aggregation, weapon-damage source fields, projectile contribution, roster aggregation, and combination rule.
3. Canonical declaration values are:
   - `context`: `field`, `siege_attack`, or `siege_defense`;
   - `question`: `defense`, `attack`, or `general`;
   - `attack_mode`: `melee` or `ranged`;
   - `mount_state`: `mounted` or `dismounted`;
   - `ammunition_policy`: `finite`, `unlimited`, or `not_applicable`.
4. Defense uses worn armor only. Shields are not armor. The first replacement candidate may reuse the existing, tested `survivability_armor_v71` aggregation (`0.35 × head + 0.55 × body + 0.05 × arm + 0.05 × leg`) but must declare it as candidate-specific, not universal.
5. Melee attack uses direct or tooltip-validated reconstructed attack-row damage. For the first candidate, item output is the maximum valid swing/thrust damage authorized by the item's attack rows. Blank or incomplete values remain blank.
6. A `CraftedItem` is eligible for attack/general output only when reconstruction provenance is complete and the required tooltip-validation gate passed. Template-name proxies are prohibited. Missing catalogs, incomplete reconstruction, absent attack rows, or failed tooltip validation produce no score and an explicit review-queue row.
7. The initial bow/crossbow per-shot output uses only declared bow/crossbow attack-row damage. Compatible arrow/bolt records determine family and usable stack count and remain published for provenance, but their damage fields do not enter candidate v1. A later candidate may include projectile contribution only through a new explicit declaration and test.
8. Outside siege defense, finite ranged capacity is `weapon_per_shot_damage × total_usable_ammunition_count`. Only compatible same-roster stacks are summed; audit literal `Bow` pairs with `Arrow` and `Crossbow` with `Bolt`. Alternative weapons remain separate pairings and are not treated as simultaneously fired.
9. In siege defense, ranged output records `ammunition_policy=unlimited`, compares per-shot output, ignores stack count, and never emits numeric infinity.
10. Alternative choices within a slot and alternative equipment rosters use arithmetic means unless a future candidate supplies evidenced roster probabilities. Every intermediate pairing remains published.
11. Siege-defense cavalry is always transformed to `mount_state=dismounted`. Riding, horse speed, maneuver, charge, mount health, and harness armor are excluded from both drivers and normalization.
12. General capability publishes armor and weapon components side by side. It emits no single rank unless a later dedicated candidate explicitly declares and validates a scale-conversion and combination rule.
13. Missing required evidence never becomes zero. The complete output retains the troop with blank result fields and a stable reason code in the review queue; rankable outputs omit it.
14. All outputs remain intra-track and context-specific. Heroes and multiplayer troops are excluded from ordinary rankings.
15. Candidate implementation writes only under `analysis/model_candidates/`; historical candidates and existing files under `analysis/model_versions/` remain byte-identical until a dedicated promotion PR passes the promotion gate. Promotion creates a new immutable version and never rewrites an old one.
16. SOLID/DRY boundary: declaration validation, equipment evidence resolution, context transformation, scoring, and reporting are separate responsibilities; all consumers use one contract and one evidence resolver rather than duplicating formulas.
17. Every implementation PR must validate its repository state, push and self-review the latest head, fix and revalidate actionable findings, update its PR body to match the final head, mark ready only after gates pass, squash-merge into `main`, and verify both that the PR is closed and that the squash commit is present on `main`.

## Functional requirements

**FR-1 — Current-candidate audit.** The system shall publish a reproducible audit of `role_scores_v1`, `defensive_role_scores_v2_candidate`, v7.1, v7.2, and v7.3 against the context-first matrix, identifying each undeclared context, mixed question, irrelevant driver, proxy, zero-filled gap, and non-applicable mounted/ammunition input without modifying those models.

**FR-2 — Declaration contract.** The system shall validate every context-first declaration against the settled fields, enums, cross-field rules, and candidate-specific aggregation/source requirements before scoring.

**FR-3 — Armor evidence lane.** The system shall resolve worn armor per roster, expose head/body/arm/leg inputs and provenance, apply only the declaration's armor aggregation, and queue incomplete armor evidence without shield or mount substitution.

**FR-4 — Weapon evidence lane.** The system shall first normalize component-level weapon attack rows with source provenance, because the current equipment audit retains only one scalar swing/thrust pair per item occurrence. It shall then publish every normalized attack row, selected direct damage, source record, reconstruction status, tooltip-validation status, and rejection reason used by melee or ranged scoring.

**FR-5 — CraftedItem fail-closed gate.** The system shall reject template proxies and unvalidated reconstructed `CraftedItem` values from attack and general-capability results while retaining affected troops and items in a review queue.

**FR-6 — Ranged ammunition policies.** The system shall build explicit compatible `Bow`/`Arrow` and `Crossbow`/`Bolt` pairings from the real audit vocabulary, calculate finite capacity from weapon damage and compatible stack count outside siege defense, and calculate per-shot unlimited-ammunition output in siege defense. Candidate v1 shall not add projectile damage to the weapon value.

**FR-7 — Context engine.** The system shall derive the effective scoring context from the declaration and force siege-defense cavalry to dismounted behavior before driver selection.

**FR-8 — Defense output.** The system shall produce complete, rankable, and review-queue defense artifacts based only on declared worn armor.

**FR-9 — Attack output.** The system shall produce complete, rankable, and review-queue melee or ranged attack artifacts based only on validated weapon evidence and the applicable ammunition policy.

**FR-10 — General-capability output.** The system shall publish armor and weapon components side by side, with independent ranks where rankable, and shall leave the combined score/rank blank unless the declaration supplies an explicit validated combination rule.

**FR-11 — Population boundaries.** The system shall keep tracks and contexts separate, exclude heroes and multiplayer troops, retain unresolved ordinary troops in complete/review artifacts, and never compare rank values across different normalization populations.

**FR-12 — Reproducible reports.** One command shall regenerate candidate CSV/JSON/Markdown artifacts, metadata, input/output SHA-256 manifests, the audit report, and Realm of Thrones top-10 views byte for byte from pinned inputs.

**FR-13 — Realm of Thrones views.** The report shall provide separate RoT top-10 tables for every rankable defense and attack tuple and side-by-side general-capability components; blocked tables shall state the evidence reason instead of substituting proxy rankings.

**FR-14 — Empirical validation.** Candidate comparisons shall join only through verified canonical troop IDs and shall preserve track, context, and side; displayed empirical estimates require at least five independent battles and 20 deployed troops and include battle-level uncertainty.

**FR-15 — Promotion and cutover.** The candidate shall remain non-canonical until a dedicated model-change PR passes canonical-join, grouped-by-battle out-of-sample, controlled-evidence, reproducibility, limitations, and review gates. The executor shall not declare the rework complete while that verdict is blocked. After the gates pass, final cutover shall publish a new immutable model version and route new scoring/report entry points to it while retaining historical commands and artifacts.

## Non-functional requirements

**NFR-1 — Determinism.** Identical declarations and hash-pinned inputs shall produce byte-identical artifacts, stable ordering, stable reason codes, and identical manifests.

**NFR-2 — Fail-closed integrity.** Missing, malformed, incompatible, ambiguous, non-finite, or unvalidated required inputs shall cause a non-zero run or an explicitly unrankable row; they shall never be coerced to a scoring zero.

**NFR-3 — Traceability.** Every published component and rank shall be reconstructible from fields in the same candidate package, with source paths and SHA-256 hashes.

**NFR-4 — Immutability.** Implementation and regeneration shall not alter existing files under audited historical candidate packages, committed `analysis/theoretical/**/export_20260731_150800/` role-score outputs, audited historical scoring/reconstruction scripts, or pre-existing `analysis/model_versions/` paths. D10 may add one new version directory only after the exact-hash promotion gate passes.

**NFR-5 — Separation of concerns.** Contract validation, evidence resolution, context policy, scoring, and report rendering shall have focused interfaces and tests. Shared semantics shall have one implementation.

**NFR-6 — Testability.** Each behavior shall have unit fixtures plus an end-to-end feature test that demonstrates the old composite/proxy path would answer the wrong question and the new path refuses or produces the expected context-specific result.

**NFR-7 — Offline reproducibility.** Candidate generation shall require no network calls or paid inference.

**NFR-8 — Safe reruns.** A second run with unchanged inputs shall be a deterministic overwrite of candidate-owned generated files; a declaration or input-hash mismatch shall stop before publishing a partial package.

## Use cases

### UC-1 — Rank siege-defense survivability

- **Actor:** Analyst
- **Goal:** Compare troops that hold a siege wall.
- **Precondition:** A valid declaration selects one track, `siege_defense`, `defense`, an attack mode, and the relevant mount state.
- **Main success scenario:**
  1. The contract validates.
  2. The context engine dismounts cavalry.
  3. The armor lane resolves worn armor.
  4. The scorer emits armor-only complete and rankable outputs.
  5. The report shows raw armor beside rank.
- **Extensions:** Incomplete armor enters the review queue; no shield, mount, or weapon field fills the gap.

### UC-2 — Rank finite ranged attack

- **Actor:** Analyst
- **Goal:** Compare ranged damage capacity in field or siege attack.
- **Main success scenario:**
  1. A ranged declaration selects `ammunition_policy=finite`.
  2. The resolver emits compatible same-roster weapon/projectile pairings.
  3. Compatible ammunition stacks are summed.
  4. Capacity is calculated per pairing and alternative results are averaged.
  5. The report exposes per-shot damage, ammunition count, capacity, and provenance.
- **Extensions:** Missing compatibility, damage, or stack evidence leaves the pairing unranked and queued.

### UC-3 — Rank ranged siege-defense attack

- **Actor:** Analyst
- **Goal:** Compare ranged offense where defenders have unlimited resupply.
- **Main success scenario:** The engine overrides ammunition to `unlimited`, ranks validated per-shot output, records no ammunition multiplier, and emits no infinity.
- **Extensions:** A declaration requesting finite ammunition in siege defense is rejected before scoring.

### UC-4 — Evaluate general capability

- **Actor:** Analyst
- **Goal:** Inspect survivability and offense together without hiding a weighting choice.
- **Main success scenario:** The report displays raw armor, armor rank, weapon output, and weapon rank side by side, with blank combined score/rank.
- **Extensions:** A future declaration may request a combined rank only when its scale conversion and combination rule are explicit and separately validated.

### UC-5 — Encounter incomplete crafted melee evidence

- **Actor:** Scoring pipeline
- **Goal:** Prevent proxy melee rankings.
- **Main success scenario:** A direct or fully reconstructed and tooltip-validated crafted weapon contributes attack evidence.
- **Extensions:** Missing PC catalogs, incomplete reconstruction, missing attack rows, or failed tooltip validation yields blank attack/general fields plus a review-queue reason; defense can still rank if armor is complete.

### UC-6 — Validate and promote a candidate

- **Actor:** Maintainer
- **Goal:** Decide whether a candidate may replace a frozen model.
- **Main success scenario:** Reproducibility passes, canonical IDs join, eligible empirical comparisons preserve boundaries and uncertainty, grouped-by-battle validation and controlled evidence pass, limitations are published, and a dedicated model-change PR performs promotion.
- **Extensions:** Any failed gate leaves the candidate under `analysis/model_candidates/` and leaves frozen versions unchanged.

## Acceptance criteria

### AC-1 — Candidate audit

**Given** the current historical scripts and model artifacts, **when** the audit runs, **then** it reports the mixed defense/offense, shield/mount/mobility/skill, proxy, and ammunition-policy departures with file/field evidence and changes no historical artifact.

### AC-2 — Declaration validation

**Given** a declaration missing a required field or containing an invalid cross-field combination such as `siege_defense` plus `finite`, **when** validation runs, **then** scoring does not start and the error names the exact field and rule.

### AC-3 — Armor-only defense

**Given** two troops with equal worn armor but different shields, weapons, skills, and mounts, **when** a defense declaration is scored, **then** their defense components are equal and the excluded fields cannot affect rank.

### AC-4 — Armor uncertainty

**Given** a troop with a missing worn-armor item or blank regional armor fields, **when** defense scoring runs, **then** the troop remains in complete output, has no fabricated component, and appears in the review queue.

### AC-5 — Direct weapon evidence

**Given** valid attack rows with source provenance, **when** attack scoring runs, **then** the selected swing/thrust value and source row are published and reconstruct the output.

### AC-6 — CraftedItem rejection

**Given** a `CraftedItem` with only a crafting-template name, incomplete reconstruction, or failed tooltip validation, **when** melee attack or general scoring runs, **then** no template proxy or zero enters the result and the stable rejection reason is published.

### AC-7 — Finite ammunition

**Given** a bow with two compatible `Arrow` stacks and an unrelated `Bolt` stack in one roster, **when** field ranged attack is scored, **then** only the arrow stacks are summed and capacity equals declared bow damage times that sum; projectile damage fields cannot change candidate-v1 output.

### AC-8 — Alternative ranged weapons

**Given** alternative bows sharing an arrow stack, **when** finite capacity is scored, **then** each bow/ammunition pairing is published separately and the arrow stack is not added as though both bows fired simultaneously.

### AC-9 — Unlimited ammunition

**Given** otherwise identical siege-defense ranged rosters with different stack counts, **when** they are scored, **then** their ranged output is equal, `ammunition_policy` is `unlimited`, and no numeric infinity exists.

### AC-10 — Dismounted siege cavalry

**Given** cavalry and infantry with equal worn armor and weapon evidence, **when** a siege-defense tuple is scored, **then** cavalry is marked dismounted and Riding, horse, harness, charge, speed, maneuver, and mount health cannot change any result.

### AC-11 — Simple outputs

**Given** valid defense, attack, and general declarations, **when** reports are generated, **then** defense has an armor rank, attack has a weapon rank, and general shows both components while leaving the undeclared combined score/rank blank.

### AC-12 — Boundary preservation

**Given** records from multiple tracks, contexts, sides, heroes, and multiplayer troops, **when** generation runs, **then** no rank population pools boundaries and heroes/multiplayer rows do not enter ordinary rankings.

### AC-13 — Reproduction and RoT top 10

**Given** pinned candidate inputs, **when** the documented command runs twice, **then** manifests and all generated bytes match, and RoT top-10 views either contain ten evidence-eligible rows per tuple or explicitly explain why fewer can be ranked.

### AC-14 — Empirical gate

**Given** a troop/context with fewer than five independent battles or 20 deployed troops, **when** empirical comparison runs, **then** it is marked insufficient and not displayed as validation; eligible rows show battle-level uncertainty and never pool track, context, or side.

### AC-15 — Promotion, cutover, and PR completion

**Given** candidate implementation is complete, **when** no dedicated promotion PR has passed every gate, **then** existing frozen model files remain byte-identical, the candidate remains non-canonical, and execution is recorded as blocked rather than complete. **Given** every gate passes, **when** promotion runs, **then** it creates a new immutable version, cuts consumers over to that version, and preserves historical commands and bytes. **Given** any implementation PR, **when** it is delivered, **then** it targets `main`, validates, self-reviews the latest pushed head, fixes findings, updates the PR body, becomes ready, squash-merges, and is verified closed with its merge present on `main`.

## Deliverables

### D1 — Current-candidate audit

- **Scope:** Add a deterministic audit command and report covering `role_scores_v1`, `defensive_role_scores_v2_candidate`, v7.1, v7.2, and v7.3 against FR-1/AC-1.
- **Targets:** `scripts/scoring/audit_context_first_candidates.py`, `tests/test_audit_context_first_candidates.py`, and `analysis/model_candidates/context_first_scores_v1/CURRENT_CANDIDATE_AUDIT.md`.
- **Verify:** `python3 -m unittest -v tests.test_audit_context_first_candidates`; expected: all audit classifications and historical-artifact hash checks pass.
- **Dependencies:** None.

### D2 — Validated scoring declaration contract

- **Scope:** Implement the versioned declaration schema, parser, enums, cross-field validation, stable errors, and fixtures for FR-2.
- **Targets:** `scripts/scoring/context_first_contract.py`, `tests/test_context_first_contract.py`, `docs/methodology/007_context_first_scoring_candidate.md`, and declaration fixtures under `analysis/model_candidates/context_first_scores_v1/declarations/`.
- **Verify:** `python3 -m unittest -v tests.test_context_first_contract`; expected: valid tuples pass and every forbidden/missing combination fails before scoring.
- **Dependencies:** D1.

### D3 — Armor lane

- **Scope:** Implement worn-armor resolution, regional raw fields, candidate-specific aggregation, provenance, alternative-roster mean, and armor review reasons for FR-3 and FR-8.
- **Targets:** `scripts/scoring/context_first_equipment.py`, `tests/test_context_first_armor.py`, and armor fixtures under `tests/fixtures/context_first/`.
- **Verify:** `python3 -m unittest -v tests.test_context_first_armor`; expected: armor-only, uncertainty, roster-mean, and no-shield/no-mount substitution tests pass.
- **Dependencies:** D2.

### D4 — Weapon normalization, evidence, and CraftedItem fail-closed handling

- **Scope:** Add deterministic component-level attack-row normalization and a machine-readable crafted-tooltip validation receipt producer; resolve those artifacts plus validated reconstructed crafted stats; reject template proxies; publish provenance; and emit review reasons for FR-4 and FR-5.
- **Targets:** add `scripts/normalization/extract_weapon_attack_rows.py`, `scripts/normalization/build_crafted_weapon_validation_receipt.py`, `tests/test_extract_weapon_attack_rows.py`, and `tests/test_crafted_weapon_validation_receipt.py`; extend `scripts/scoring/context_first_equipment.py`; add `tests/test_context_first_weapon_evidence.py`; consume, without weakening, `scripts/normalization/reconstruct_crafted_weapon_stats.py`.
- **Verify:** `python3 -m unittest -v tests.test_extract_weapon_attack_rows tests.test_crafted_weapon_validation_receipt tests.test_context_first_weapon_evidence tests.test_reconstruct_crafted_weapon_stats`; expected: component rows and their source provenance reproduce deterministically, a receipt is emitted only from hash-matched per-item tooltip comparisons, direct evidence passes, and every incomplete/unvalidated crafted path remains blank and queued.
- **Dependencies:** D2. May run in parallel with D3.

### D5 — Ranged finite/unlimited ammunition

- **Scope:** Implement explicit compatible pairings, finite capacity, alternative-weapon handling, and unlimited siege-defense semantics for FR-6.
- **Targets:** `scripts/scoring/context_first_ranged.py`, `tests/test_context_first_ranged.py`, and ranged fixtures under `tests/fixtures/context_first/`.
- **Verify:** `python3 -m unittest -v tests.test_context_first_ranged`; expected: compatible stack sums, alternative pairing isolation, and stack-invariant unlimited results pass.
- **Dependencies:** D2 and D4.

### D6 — Context engine, including dismounted siege cavalry

- **Scope:** Apply context/question/mode/mount policy before driver selection and force siege-defense cavalry to dismounted behavior for FR-7 and FR-11.
- **Targets:** `scripts/scoring/context_first_engine.py` and `tests/test_context_first_engine.py`.
- **Verify:** `python3 -m unittest -v tests.test_context_first_engine`; expected: all valid tuples select only allowed drivers and mounted fields are inert in siege defense.
- **Dependencies:** D2, D3, D4, and D5.

### D7 — Simple defense, attack, and general outputs

- **Scope:** Build complete, rankable, and review artifacts; defense ranks armor, attack ranks weapon output, and general publishes side-by-side components without an undeclared blend.
- **Targets:** `scripts/scoring/generate_context_first_scores.py`, `tests/test_context_first_scores.py`, and scratch/generated-schema fixtures under `tests/fixtures/context_first/generated/`. D7 does not publish the committed candidate root before the D8 renderer/transaction exists.
- **Verify:** `python3 -m unittest -v tests.test_context_first_scores`; expected: FR-8 through FR-11 and AC-11/AC-12 pass.
- **Dependencies:** D6.

### D8 — Reproducible reports and Realm of Thrones top 10s

- **Scope:** Add one-command report generation, metadata, input/output manifests, review summaries, and evidence-eligible RoT top-10 tables for FR-12 and FR-13.
- **Targets:** `scripts/scoring/write_context_first_reports.py`, `tests/test_context_first_reports.py`, `analysis/model_candidates/context_first_scores_v1/README.md`, `candidate_manifest.csv`, `artifact_hashes.csv`, and `realm_of_thrones/TOP10.md`. The promotion gate later pins `candidate_manifest.csv`; the outer artifact manifest must not participate in a hash cycle.
- **Verify:** `python3 -m unittest -v tests.test_context_first_reports && python3 scripts/scoring/generate_context_first_scores.py && python3 scripts/scoring/write_context_first_reports.py`; expected: two isolated regenerations are byte-identical and blocked RoT lanes explain their evidence gaps.
- **Dependencies:** D7.

### D9 — Evidence closure, empirical validation, and promotion gate

- **Scope:** Inventory and close the evidence gaps required by the declared candidate, join candidates to canonical empirical evidence, enforce 5-battle/20-deployed and battle-level uncertainty, publish boundary-safe comparisons, and implement a machine-readable promotion verdict for FR-14 and the promotion portion of FR-15. For gaps that require operator-provided PC catalogs, screenshots, or battles, emit an exact acquisition request and stop at this gate until repository-addressable evidence is supplied.
- **Targets:** `scripts/scoring/validate_context_first_candidate.py`, `tests/test_context_first_validation.py`, and `analysis/model_candidates/context_first_scores_v1/VALIDATION_REPORT.md` plus `promotion_gate.json`.
- **Verify:** `python3 -m unittest -v tests.test_context_first_validation tests.test_gate_status`; expected: under-gate, unresolved-ID, pooled-context, pooled-side, and row-level split attempts cannot pass promotion.
- **Dependencies:** D8 and repository-addressable canonical empirical inputs. Lack of sufficient evidence yields a reproducible blocked verdict and pauses the locked execution at D9; it is not permission to fabricate evidence or skip to D10.

### D10 — Dedicated promotion, final cutover, and cleanup

- **Scope:** Only after D9 reports `passed` for the exact `candidate_manifest.csv` hash, open a dedicated model-change slice that copies the approved package into a new immutable version, routes new scoring/report documentation and entry points to that version, removes only superseded scaffolding introduced by D1-D9, preserves every historical candidate and prior frozen version, runs full validation, and completes the PR lifecycle in Settled Decision 17.
- **Targets:** a new version directory under `analysis/model_versions/`, `README.md`, `docs/research/EXECUTION_TRACKER.md`, relevant new context-first modules/tests, and explicit pre/post hashes for every pre-existing frozen artifact.
- **Verify:** `python3 -m unittest discover -v`; regenerate the D8 package twice; compare candidate-to-promoted and historical/frozen manifests; self-review the latest pushed head; expected: all tests pass, regenerated bytes match, the promoted package matches the approved candidate, all pre-existing historical/frozen bytes are unchanged, the PR targets `main`, is squash-merged, is no longer open, and its merge commit is present on `main`.
- **Dependencies:** D9 with `promotion_gate.status=passed`, `promotion_allowed=true`, and an exact candidate-manifest match. A blocked verdict is a hard stop, not a completion state.

## Dependency map and execution order

```text
D1 -> D2
D2 -> D3
D2 -> D4
D4 -> D5
D3 + D4 + D5 -> D6
D6 -> D7 -> D8 -> D9 -> D10
```

D3 and D4 are the only planned parallel implementation lane. Each deliverable is one reviewable PR unless an executor proves that combining adjacent deliverables produces a smaller independently verifiable change. Every PR follows test-first development: add the feature test, run it and confirm the expected failure, implement the minimum change, run focused tests, then run repository validation and the full delivery workflow.

## Implementation boundaries

- Do not touch `analysis/model_versions/` before D10. At D10, add one new immutable version only; never modify an existing version.
- Do not rewrite or regenerate historical candidate artifacts.
- Do not add dependencies unless the standard library and existing pandas/numpy stack cannot satisfy a requirement.
- Do not reformat unrelated files or rename stable historical symbols.
- Do not add a general-capability blend, secondary driver, or new weapon-family formula in this work.
- A rerun owns only `analysis/model_candidates/context_first_scores_v1/` and must stop before partially replacing that package.
- Commit and push are authorized by the repository standing workflow for implementation slices; force-push to `main` is prohibited.

Executor: read @execute-locked-plan before editing.
