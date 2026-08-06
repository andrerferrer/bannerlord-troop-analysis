# Execution resume: context-first scoring rework

This file is the compaction-proof source of truth for the rework. Update it after every merged slice and before every stop.

## Status

```yaml
plan_version: 1
state: in_progress
active_step: D3
completed_steps: [D1, D2]
blocked_at: null
base_branch: main
planning_branch: agent/context-first-scoring-rework-plan
tracking_issue: https://github.com/andrerferrer/bannerlord-troop-analysis/issues/58
candidate_root: analysis/model_candidates/context_first_scores_v1
promotion_gate: not_run
last_verified_main: 709dffae131ef1cd97a455cd6caede3672b8a0e1
```

Planning, D1, and D2 are merged. D3 is implementing direct worn-armor evidence.

## Read first

1. `AGENTS.md`
2. `plan/context-first-scoring-rework/execution-plan.md`
3. `plan/context-first-scoring-rework/prd.md`
4. `plan/context-first-scoring-rework/design.md`
5. `plan/context-first-scoring-rework/test-plan.md`
6. `docs/methodology/006_context_first_scoring_rules.md`
7. the current issue #58 body and latest comments
8. the `execute-locked-plan` skill

If any source conflicts, `AGENTS.md` wins for repository workflow, the PRD wins for behavior, the design wins for implementation boundaries, the test plan wins for proof, and this resume wins for current progress. Stop on a substantive contradiction.

## Settled decisions

- Choose context and question before drivers.
- Defense is armor-primary and excludes shield/mount substitution.
- Attack is weapon-primary and requires direct or validated reconstructed evidence.
- General capability exposes armor and weapon output side by side; no default blend exists.
- Finite bow/crossbow output is per-shot output times compatible usable ammunition.
- Siege-defense ammunition is unlimited, represented by per-shot output without infinity.
- Siege-defense cavalry is dismounted before scoring; Riding, mount, harness, charge, and mounted mobility are inert.
- Missing evidence is blank plus a stable review reason, never zero.
- Historical candidates and pre-existing frozen versions are immutable.
- The rework is not complete until the promotion gate passes and a new immutable version is cut over.
- Every slice targets `main` and includes push, latest-head self-review, fixes, ready, squash merge, and post-merge verification.

## Deliverable ledger

| ID | Deliverable | State | Depends on | Merge/notes |
|---|---|---|---|---|
| D1 | Current-candidate audit | merged | — | PR #61; squash `467ad05aa8b59a90766b40ead1a3f54420b26154` |
| D2 | Declaration contract | merged | D1 | PR #62; squash `709dffae131ef1cd97a455cd6caede3672b8a0e1` |
| D3 | Armor evidence lane | in_progress | D2 | branch `agent/context-first-03-armor` |
| D4 | Weapon-row normalization, override resolution, and crafted fail-closed gate | pending | D2 | may require exact raw XML/source package and operator tooltip observations; new evidence batches require two agents |
| D5 | Finite/unlimited ranged semantics with explicit loadouts | pending | D4 | D3 must also be merged before D6 |
| D6 | Context engine and dismounted siege cavalry | pending | D3, D4, D5 | — |
| D7 | Defense/attack/general candidate outputs | pending | D6 | — |
| D8 | Deterministic reports and RoT top 10s | pending | D7 | — |
| D9 | Evidence closure and hash-pinned empirical promotion gate | pending | D8 | hard stop on blocked verdict |
| D10 | New immutable version, cutover, cleanup | pending | D9 status=`passed`, promotion_allowed=`true`, exact candidate and validation-input manifests | final completion |

Allowed deliverable states are `pending`, `in_progress`, `ready_to_merge`, `merged`, and `blocked`. Record PR URL, exact reviewed head, validation command, and limitations before merge. The next slice backfills the previous squash SHA; D10 uses the issue closure comment as its final post-merge receipt.

## Acceptance ledger

| AC | Summary | Owning step | State |
|---|---|---|---|
| AC-1 | Existing model departures audited without mutation | D1 | passed: 49 focused tests + byte-identical audit/baseline regeneration |
| AC-2 | Invalid declarations fail before scoring | D2 | passed: 22 contract tests + exact-head review |
| AC-3 | Equal armor yields equal defense | D3 | pending |
| AC-4 | Armor uncertainty remains blank and queued | D3 | pending |
| AC-5 | Direct weapon rows reconstruct output | D4 | pending |
| AC-6 | Crafted proxies/unvalidated values cannot rank | D4 | pending |
| AC-7 | Compatible finite ammunition sums correctly | D5 | pending |
| AC-8 | Alternative ranged weapons stay separate | D5 | pending |
| AC-9 | Siege-defense unlimited output is stack-invariant | D5 | pending |
| AC-10 | Siege cavalry is dismounted and mounted fields are inert | D6 | pending |
| AC-11 | Defense/attack/general outputs stay simple | D7 | pending |
| AC-12 | Track/context/side/population boundaries hold | D7 theoretical boundaries + D9 player/enemy side proof | pending |
| AC-13 | Regeneration and RoT views are deterministic | D8 | pending |
| AC-14 | Empirical minimums and battle-level uncertainty hold | D9 | pending |
| AC-15 | Promotion, cutover, and full PR lifecycle pass | D10 | pending |

No AC may be marked complete from code inspection alone. Record the exact passing test or artifact.

## Known starting evidence state

- Current empirical tracker: 40 battles total, 24 overall display-eligible, 17 field, 2 siege attack, and 0 siege defense at planning time.
- Realm of Thrones has 9,414 non-multiplayer `CraftedItem` equipment rows without a complete damage/speed/class tuple in the current export.
- Trustworthy crafted melee output requires PC crafting piece/template catalogs plus tooltip validation.
- Current equipment-audit scalar damage cells do not preserve every XML `<Weapon>` component. D4 requires raw XML reconstructed from the committed source-package identity or an exact PC module root that verifies against the raw manifest.
- Duplicate item definitions must resolve through committed `manifest_modules.csv` load order; equipment roster provenance is not a module-winner signal.
- A passed crafted receipt must also produce shared-schema crafted attack rows; reconstructed values never bypass the attack-row contract.
- Canonical empirical identity coverage remains incomplete for some labels.
- Missing raw XML/catalog/tooltip inputs may block D4. Empirical coverage may block D9 and therefore D10. Earlier merged slices remain valid when a later evidence gate blocks.
- D9 must pin every empirical, canonical, grouped-OOS, controlled, and limitations input in `validation_input_hashes.csv`; D10 re-verifies that manifest and every referenced byte.

Recompute these facts at D9. Do not treat the planning-time counts as live truth.

## Immutable baselines

Before D1, record fresh tree hashes for:

- `analysis/model_candidates/role_scores_v2_defense/`
- all historical candidate packages included by the audit
- every existing directory under `analysis/model_versions/`

Before and after every generation/promotion step, compare them. D10 may add one new version directory only after a passing gate; it may not change an existing byte.

## Per-slice update template

### D1 — 2026-08-05

- Branch: `agent/context-first-01-audit`
- PR: https://github.com/andrerferrer/bannerlord-troop-analysis/pull/61
- Exact reviewed head: `7716f4d91473a98a2662b40845eb6aa028cfcff9`
- Delivery state: merged
- Squash merge SHA on main: `467ad05aa8b59a90766b40ead1a3f54420b26154`
- Focused verification: `python3 -m unittest tests.test_audit_context_first_candidates` — 49 passed
- Full/regression verification: 280 tests; only four pre-existing pandas import errors; deterministic regeneration byte-identical
- Generated artifacts and hashes: audit `cd74a30554518d41ee6dcbe9b779113ffd60a692bcb4c89ae7e4e4ea8e1e5257`; baseline `7ae42d15a19bffa2bb323c88352c625a4da54f109964b00e3f4681bd5487c274`
- Review findings fixed: transactional rollback ownership, file identity/content races, descriptor cleanup, and unsafe close retry
- Remaining limitations: four unrelated pandas-dependent tests cannot import in this environment
- Next step: D2 declaration contract

### D2 — 2026-08-05

- Branch: `agent/context-first-02-contract`
- PR: https://github.com/andrerferrer/bannerlord-troop-analysis/pull/62
- Exact reviewed head: `8e30a811b73796ec7c2041d678bf2625630d74d9`
- Delivery state: merged
- Squash merge SHA on main: `709dffae131ef1cd97a455cd6caede3672b8a0e1`
- Focused verification: `python3 -m unittest tests.test_context_first_contract` — 22 passed
- Full/regression verification: 302 tests; only four pre-existing pandas import errors; D1 audit byte-identical
- Generated artifacts and hashes: 100 declarations; tree digest `c0482f76b4d48e2ab6d737c27685758e82e7679d68d707601e65105db1ebfbcc`
- Review findings fixed: invalid UTF-8, duplicate JSON keys, exact armor-field diagnostics, and misleading cross-contract errors
- Remaining limitations: four unrelated pandas-dependent tests cannot import in this environment
- Next step: D3 worn-armor evidence

Append one entry after each merged PR:

```markdown
### Dn — YYYY-MM-DD

- Branch:
- PR:
- Exact reviewed head:
- Delivery state: ready_to_merge | merged
- Squash merge SHA on main (backfilled by next slice; D10 receipt lives on issue #58):
- Focused verification:
- Full/regression verification:
- Generated artifacts and hashes:
- Review findings fixed:
- Remaining limitations:
- Next step:
```

Then update `active_step`, `completed_steps`, the deliverable ledger, and acceptance ledger above.

## Blocked-state template

```yaml
state: blocked
blocked_at: D9
blocking_gate: <stable gate/reason code>
candidate_sha256: <hash>
validation_input_manifest_sha256: <hash-or-not_run>
failing_command: <exact command>
required_evidence: <exact repository-addressable inputs needed>
acquisition_method: <normalization/analysis path>
safe_completed_scope: <merged steps that remain valid>
next_action_after_unblock: <single exact action>
```

Do not mark `state: complete_on_verified_merge` while `promotion_gate` is `blocked`, `not_run`, or tied to different candidate or validation-input hashes. D10 may commit `complete_on_verified_merge` only after its exact head is reviewed and ready; completion becomes true only after the issue #58 receipt verifies the squash on `main`.

## Final completion checklist

- [ ] D1 through D10 are merged and verified on `main`.
- [ ] AC-1 through AC-15 cite passing proof.
- [ ] `promotion_gate.status=passed`, `promotion_allowed=true`, and the evaluated candidate- plus validation-input-manifest hashes and all referenced bytes match the promoted candidate.
- [ ] A new immutable model version is repository-addressable.
- [ ] Every pre-existing model/candidate hash is unchanged.
- [ ] Context-first entry points and documentation target the promoted version.
- [ ] Full tests and two deterministic regenerations pass.
- [ ] RoT reports/top 10s are published with honest evidence limitations.
- [ ] All PRs have exact-head self-review and are closed after squash merge; D10 has a post-merge receipt on issue #58.
- [ ] Issue #58 is closed with final links.
- [ ] `plan/.active-plan` is removed or redirected according to the next active plan.

## Continuation prompt

Execute the first incomplete deliverable in `plan/context-first-scoring-rework/execution-plan.md`. Read all sources in “Read first,” run the pre-flight, and apply `@execute-locked-plan`. Make no scope changes. Use one PR per numbered step, target `main`, add meaningful tests first, validate, push, self-review the exact latest head, fix findings, mark ready, squash-merge, verify on `main`, and update this resume plus issue #58 using the documented backfill rule. Stop on drift. Never fabricate raw XML, tooltip, or empirical evidence or skip a blocked D4/D9 gate. If D4 ingests a new evidence batch, use distinct normalization and analysis agents on the same branch/PR as required by `AGENTS.md`. Continue through D10 only when `promotion_gate.status=passed`, `promotion_allowed=true`, and the exact candidate- and validation-input-manifest hashes plus all referenced bytes match.
