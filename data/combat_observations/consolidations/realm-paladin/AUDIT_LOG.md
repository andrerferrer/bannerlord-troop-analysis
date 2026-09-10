# Realm Paladin consolidation audit log

## 2026-09-08 — incorrect Phase 1 validation attempt

The operator supplied a screenshot of a local Codex run on branch
`data/consolidate-realm-paladin`. The run reported:

```text
$normalize-bannerlord-combat-batch validation exited 2
missing Phase 1 file: screenshots_manifest.csv
```

It also established that:

- no raw Realm Paladin screenshots or source ZIP were present in the checkout;
- the recoverable numeric evidence referenced by this branch came from the
  already-merged PR #92 analysis;
- the attempted run made no edits, commits, pushes, or protocol comments;
- it recommended locating an unpublished source package before treating the
  missing historical battle as recovered evidence.

### Adjudication

The exit-2 result was not a defect in PR #95. It came from applying the
new-evidence Phase 1 validator to the wrong workflow class.

PR #95 is classified as:

```text
workflow: historical_consolidation
new evidence batch: no
Phase 1 normalization required: no
screenshots_manifest.csv required: no
handoff/ANALYSIS_PROMPT.md required: no
```

The source row being consolidated was already normalized and analyzed in the
merged Westerling follow-up batch. This PR does not pretend to recreate that
batch, manufacture raw-image provenance, or promote remembered values into
numeric evidence.

## 2026-09-08 — consolidation task was not discoverable

A second operator-provided screenshot showed the local agent reading:

- `.agents/skills/analyze-bannerlord-combat-zip/SKILL.md`;
- the skill workflow and output contract;
- `AGENTS.md`.

The agent then ran:

```bash
python3 scripts/analysis/discover_analysis_tasks.py --json
```

The result contained:

```json
{
  "actionable_count": 0,
  "warnings": []
}
```

The agent stopped with:

```text
No analyzable input or pending Phase 2 task was found.
```

That stop exposed a real repository workflow gap. Historical consolidations had
been documented as distinct from new evidence, but the dispatcher recognized
only `bannerlord-analysis-task:v1`. PR #95 therefore had no machine-discoverable
task despite containing a valid consolidation state.

### Fix committed in PR #95

The pull request now contains:

1. `docs/protocols/consolidation-task-v1.md`, defining the append-only
   `bannerlord-consolidation-task:v1` protocol;
2. dispatcher support for both analysis and consolidation protocols in
   `scripts/analysis/discover_analysis_tasks.py`;
3. regression coverage in `tests/test_discover_analysis_tasks.py`;
4. `CONSOLIDATION_TASK.md`, the executable Realm Paladin handoff;
5. a valid pending `bannerlord-consolidation-task:v1` PR comment with task ID
   `realm-paladin-historical-consolidation`.

After the branch is updated, the same dispatcher command must return PR #95 as
an actionable `historical_consolidation` task. A raw screenshot, ZIP,
`screenshots_manifest.csv`, or Phase 2 handoff is not required to discover or
audit this already-committed aggregate.

## Applicable consolidation checks

1. pin the immutable committed source row and its Git blob identity;
2. copy every source column into `evidence.csv` without changing its value,
   adding only provenance and compatibility columns;
3. recompute every derived metric;
4. preserve the operator recollection as a historical lead only;
5. search committed evidence and PR history without inferring missing values;
6. update the authoritative troop-test queue so Realm Paladin cannot be
   recommended or retested during reconciliation;
7. keep protocol, task handoff, branch state, PR body, and validation receipt in
   agreement.

## State before history recovery

The PR contains:

- the human-readable consolidation and arithmetic in `README.md`;
- the executable task in `CONSOLIDATION_TASK.md`;
- this two-stage audit record;
- the recoverable aggregate with every source column preserved in
  `evidence.csv`;
- machine-readable workflow, evidence, gate, protocol, and blocker state in
  `consolidation.json`;
- the validation receipt in `validation_report.json`;
- the Realm Paladin hold and task references in the authoritative Realm of
  Thrones queue;
- a dedicated consolidation protocol document and dispatcher tests.

## Evidence limitation at that stage

Only the additional historical evidence remembered by the operator, if it
exists, remains unrecovered. It must not be inferred. If previously unpublished
screenshots or a ZIP are recovered later, those raw inputs must pass the normal
evidence-ingestion and Phase 1 rules before their observations can change the
consolidated totals.

The absence of that raw package does not make PR #95 undiscoverable and does not
invalidate the four-battle committed aggregate.

## 2026-09-10 — committed history recovered and consolidation resolved

After the task became discoverable, a content search across committed analysis
artifacts found the missing gate-clearing Realm Paladin result in merged PR #91.
Its pull-request title describes the mixed White Harbor/Joffrey batch rather
than Realm Paladin, which explains why the earlier title-oriented search missed
it.

The audit then:

1. pinned PR #91's reliable field row by merge commit, path, Git blob SHA, and
   byte size;
2. reconstructed the PR #91 and PR #92 normalized archives and verified their
   declared SHA-256 values;
3. checked all archive members for absolute paths, traversal, and links;
4. recovered 11 PR #91 and 4 PR #92 Realm Paladin field occurrences;
5. verified 15 unique battle IDs and 15 unique source-image hashes;
6. confirmed the last PR #91 source capture precedes the first PR #92 capture;
7. kept two PR #91 siege-attack observations outside the field aggregate;
8. recomputed the combined 15-battle / 192-deployed / 489-kill result;
9. merged the newer main queue state from PR #96, preserving Cerwyn Marauder as
   closed and leaving the ordered queue empty; and
10. moved Realm Paladin from historical hold to
    `completed_no_additional_test`.

The operator recollection is now resolved by repository-addressable evidence.
No remembered numeric value was used, and no additional field test is
recommended.

## 2026-09-10 — post-push review corrections

The first latest-head review at `ef05cb6e5d5a86848b5f1cfa6c13b82d6ebf0bb2`
found four blocking issues. A separate three-pass recheck unanimously confirmed
the critical findings before correction.

The corrected consolidation now:

1. accepts protocol authority only from GitHub `OWNER`, `MEMBER`, or
   `COLLABORATOR` comments;
2. orders same-second protocol transitions by numeric comment ID;
3. rejects absolute, traversing, drive-qualified, backslash, and otherwise
   non-normalized comment-supplied repository paths;
4. pins every aggregate, structural source, archive bundle tree,
   reconstruction input, and its Git object in `source_manifest.json`; and
5. preserves every original source-column value in `evidence.csv`, adding only
   explicit provenance and compatibility fields.

Validation reconstructed both archives, checked 19 pinned reconstruction
inputs and 34 payload members, reproduced all 15 battle rows and published
metrics, passed 18 dispatcher tests, and passed all 394 repository tests. The
pull-request description and final append-only protocol transition remain
publication steps after this corrected head is pushed and reviewed.

## 2026-09-10 — exact-head review round 2

Five read-only passes reviewed
`c72efa1bf12f4caa1175f30a98ea978a8306e8d7`. The empirical source, archive,
row-preservation, arithmetic, and queue claims survived. Four passes reproduced
a path-collection bypass; one pass additionally raised edited-comment and
invalid-transition handling. Because those were critical non-unanimous
findings, a separate three-pass adversarial recheck attempted to refute them.
All three recheck passes confirmed all three defects as merge blockers.

The dispatcher correction now:

1. validates strings in singular and plural path, file, artifact, part, and
   directory metadata, including collection members;
2. rejects protocol comments whose GitHub update timestamp differs from their
   creation timestamp; and
3. sorts each task's comment history, requires `pending` as its initial state,
   and ignores invalid successors instead of letting them replace the last
   valid state.

Direct regression cases cover all three failures. The focused dispatcher suite
now passes 21 tests, the full repository suite passes 397 tests, and live
discovery still returns the trusted Realm Paladin `in_progress` task with no
warnings.

## 2026-09-10 — exact-head review round 3

All five passes reviewing
`27e23fa4b4c4a291dc45cd232e78d3e3d64756fd` verified that the round-2 findings
were fixed, then reproduced one remaining nested-container bypass. A recognized
path-bearing field lost its path context when a collection member was itself a
list or mapping.

The recursive validator now carries path context through every nested list and
mapping string. Regression inputs include nested lists, mappings, lists of
mappings, leading/trailing whitespace, and control characters. Numeric metadata
such as an archive-input file count remains valid because it cannot direct an
executor to a filesystem location.
