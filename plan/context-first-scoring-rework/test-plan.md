# Test plan: context-first scoring rework

## Purpose

Prove that the rework answers the declared gameplay question with the smallest allowed evidence set, remains deterministic and auditable, fails closed on uncertainty, and cannot be promoted without sufficient boundary-safe evidence. Tests must demonstrate feature behavior, not merely exercise functions.

## Test principles

1. Every acceptance criterion has at least one behavior-level assertion.
2. Fixtures vary excluded fields to prove they are inert, not just absent.
3. Missing evidence is asserted as blank plus a reason code; zero is never accepted as a substitute.
4. Rank tests include multiple populations so accidental pooling is observable.
5. Empirical tests group and resample by battle, never by troop row.
6. Determinism is byte-level and runs from isolated copies/staging directories.
7. Historical immutability is verified with hashes, not `git status` alone.
8. Promotion is tested as a state transition tied to exact candidate hashes.

## Test layers

### Unit and contract tests

Focused standard-library `unittest` suites cover parsing, enums, reason codes, evidence resolution, formulas, pairing, context transformation, ranking, and gate decisions. Small synthetic fixtures make the expected result calculable by hand.

### Feature tests

Each core question is tested through the public generator/report boundary:

- armor-only siege-defense defense;
- finite ranged field attack;
- unlimited ranged siege-defense attack;
- general capability without a combined score;
- crafted melee evidence rejected until fully reconstructed and validated;
- cross-track/context/side isolation.

The fixture must contain distractor fields—shield, Riding, mount, speed, skill, and incompatible ammunition—so the test proves they cannot influence the answer.

### Repository regression tests

Run existing model, normalization, empirical-gate, and full repository suites. Hash historical artifacts before and after generation.

### Reproducibility and promotion tests

Generate twice from identical pinned inputs, compare every output byte and manifest, then mutate one declaration/input to prove the run either produces a new declared hash set or stops before partial publication. Promotion tests require a passing verdict for the exact candidate hashes.

## Acceptance-to-test matrix

| AC | Required proof | Primary suite | Failure prevented |
|---|---|---|---|
| AC-1 | Audit names each mixed/irrelevant input and before/after hashes match | `tests.test_audit_context_first_candidates` | silently treating historical candidates as compliant |
| AC-2 | Missing fields and invalid cross-field tuples fail before evidence reads | `tests.test_context_first_contract` | implicit defaults and siege finite ammo |
| AC-3 | Equal worn armor remains equal while shield/weapon/skill/mount vary | `tests.test_context_first_armor` | composite defense score |
| AC-4 | Incomplete armor yields blank complete row plus review reason | `tests.test_context_first_armor` | missing-as-zero ranking |
| AC-5 | Published source attack row reconstructs selected damage | `tests.test_context_first_weapon_evidence` | opaque weapon score |
| AC-6 | Template-only/incomplete/unvalidated crafted item is unrankable | weapon evidence + reconstruction tests | crafted proxy rankings |
| AC-7 | Bow uses arrows only and sums compatible stacks exactly once | `tests.test_context_first_ranged` | incompatible/double ammunition |
| AC-8 | Alternative bows publish separate pairings | `tests.test_context_first_ranged` | simultaneous-fire inflation |
| AC-9 | Siege-defense output is invariant to stack count and has no infinity | ranged + feature test | finite ammo leakage |
| AC-10 | Cavalry is dismounted and all mounted distractors are inert | `tests.test_context_first_engine` | Riding/mount defense bias |
| AC-11 | Defense ranks armor, attack ranks weapon, general leaves blend blank | `tests.test_context_first_scores` | universal score reintroduction |
| AC-12 | Tracks/contexts/sides never share a rank population; heroes/mp excluded | scores + validation tests | invalid pooling |
| AC-13 | Two isolated runs match byte-for-byte; RoT reports explain short tables | `tests.test_context_first_reports` | nondeterministic or proxy top 10 |
| AC-14 | 4 battles or 19 deployed fails; eligible rows use battle-level uncertainty | `tests.test_context_first_validation` | row-level pseudo-replication |
| AC-15 | Blocked gate cannot promote; passing exact hashes can add one new version | validation + promotion feature test | premature or mutable promotion |

## Required fixtures

Store compact synthetic fixtures under `tests/fixtures/context_first/`. Every value must be intentional and documented in a fixture README or test name.

### Armor fixture

- two ordinary troops with identical worn armor;
- different shields, weapons, athletics/riding values, mount/harness, and class labels;
- one alternate equipment roster;
- one unresolved armor item;
- one hero and one multiplayer troop.

Expected: ordinary equal-armor defense ties; alternate-roster mean is hand-verifiable; unresolved row is blank/queued; hero/mp do not rank.

### Direct and crafted weapon fixture

- direct weapon with multiple valid attack rows;
- crafted item with only a template name;
- crafted item with incomplete piece data;
- fully reconstructed crafted item without tooltip validation;
- fully reconstructed and tooltip-validated crafted item;
- weapon with no valid swing/thrust row;
- non-finite/malformed damage value.

Expected: only direct and fully validated crafted evidence can contribute; selected damage and provenance are exact.

### Ranged fixture

- two alternative bows;
- two arrow stacks;
- one bolt stack;
- one crossbow and compatible bolts;
- incompatible/missing projectile records;
- identical rosters with different ammunition counts.

Expected: explicit pairings, hand-calculable finite capacity, separate alternatives, and stack-invariant siege-defense output.

### Boundary fixture

- at least two tracks;
- field, siege attack, and siege defense;
- player and enemy observations;
- repeated troop rows within battles;
- populations immediately below and at 5-battle/20-deployed thresholds.

Expected: no pooled ranks/validation; repeated rows do not inflate independent sample size.

## Feature scenarios

### F1 — Siege-defense armor question

Given cavalry and infantry have equal worn armor but different shields, weapons, Riding, mounts, harnesses, and charge, when `siege_defense + defense` runs, both effective mount states are dismounted and their defense component/rank ties. A mutation test that changes every mounted field must leave generated bytes unchanged except raw audit provenance explicitly allowed by the schema.

### F2 — Finite field ranged attack

Given a bow, two arrow stacks, and an unrelated bolt stack, when `field + attack + ranged + finite` runs, output equals `(weapon damage + declared projectile contribution) * sum(arrows)`. The bolt is published as incompatible or ignored with provenance and never enters capacity.

### F3 — Unlimited siege-defense ranged attack

Given the F2 roster and a second roster with different stack counts, when `siege_defense + attack + ranged` runs, both use the same validated per-shot output, report `unlimited`, omit any ammunition multiplier, and serialize no numeric/string infinity.

### F4 — General capability

Given valid armor and weapon evidence, when `general` runs, complete/rankable output contains both raw components and independent ranks. `combined_score` and `combined_rank` are blank unless an explicit future validated combination contract is supplied.

### F5 — Crafted melee fail-closed

Given a RoT-style `CraftedItem` with only a template proxy, when attack/general runs, defense may still rank from complete armor but melee output remains blank and the review queue names the missing catalog/reconstruction/tooltip gate. Adding only a plausible numeric proxy must not change the result.

### F6 — Boundary preservation

Given identical IDs/names across different tracks, contexts, or sides, when reports and empirical validation run, each population remains separate and all join keys include the required boundary fields.

### F7 — Atomic failure

Given a valid published candidate package, when regeneration encounters a declaration/hash mismatch midway, the command exits non-zero and the previously published package remains byte-identical. No partial manifest or mixed-generation directory is visible.

### F8 — Promotion state machine

Given a blocked verdict, when promotion is requested, no model-version path changes. Given a passing verdict whose candidate hash differs from the current candidate, promotion also fails. Only a passing exact-hash verdict may add one new version, and all previous version hashes remain unchanged.

## Determinism protocol

1. Copy pinned inputs and declarations into two isolated temporary roots.
2. Fix locale/timezone-sensitive serialization through explicit code, not environment assumptions.
3. Run the documented generation/report commands independently.
4. Compare relative file lists, SHA-256 values, and bytes.
5. Assert stable row ordering, newline convention, decimal representation, JSON key order, reason-code order, and manifest order.
6. Rerun over an existing candidate package to exercise atomic replacement.
7. Verify source declarations are preserved and not overwritten by generated output.

No test may pass by normalizing away nondeterministic bytes after generation.

## Historical immutability protocol

At D1 create a test helper that hashes files by relative path and bytes. The protected set includes all pre-existing historical candidate packages named by the audit and all pre-existing `analysis/model_versions/` files. Run it:

- before and after every candidate end-to-end generation test;
- before and after D8 isolated reproduction;
- immediately before and after D10 promotion.

D10 may add paths only inside the newly declared version. Any modification/deletion of a baseline path fails.

## Empirical validation checks

- canonical IDs must be verified against the selected versioned track audit;
- provisional labels never join as canonical IDs;
- join keys retain track, context, and side;
- eligibility is calculated from distinct battles and deployed-troop totals;
- 4 battles/100 troops fails; 5 battles/19 troops fails; 5 battles/20 troops passes display eligibility;
- uncertainty and train/test splits use whole battles;
- no field evidence validates siege defense;
- no player-side evidence is pooled with enemy-side evidence;
- reports distinguish insufficient evidence from a negative result;
- controlled evidence and known limitations are included in the machine-readable verdict.

## Step verification commands

Run the focused command from each execution-plan step. Before merging every slice also run the touched regression suites. At D8-D10 run:

```bash
python3 -m unittest discover -v
python3 scripts/scoring/generate_context_first_scores.py
python3 scripts/scoring/write_context_first_reports.py
python3 scripts/scoring/validate_context_first_candidate.py
git diff --check
```

If a command is intentionally unavailable before its owning step, the executor must not substitute a fake no-op. The earlier step uses its focused suite; the final command set becomes mandatory once all entry points exist.

## PR review assertions

Every latest-head self-review must explicitly check:

- formulas against the declaration and methodology;
- excluded-field inertness;
- blank-versus-zero behavior;
- track/context/side and population boundaries;
- deterministic ordering and atomic publication;
- source provenance and hashes;
- historical immutability;
- honest limitations/top-10 shortfalls;
- promotion state/hash matching;
- PR body and verification evidence matching the exact head.

An approval/review of an earlier SHA does not satisfy the gate after fixes are pushed.

## Completion evidence

The final D10 PR must link:

- passing focused and full test output;
- two-run artifact hash comparison;
- `VALIDATION_REPORT.md` and passing `promotion_gate.json`;
- pre/post historical hash comparison;
- promoted version manifest;
- RoT report/top-10 artifacts;
- exact reviewed head and squash merge SHA;
- issue #58 closure comment.

The rework fails completion if any evidence is missing, any gate is blocked, or any prior frozen byte changed.
