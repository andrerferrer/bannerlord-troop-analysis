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
2. copy that row exactly into `evidence.csv`;
3. recompute every derived metric;
4. preserve the operator recollection as a historical lead only;
5. search committed evidence and PR history without inferring missing values;
6. update the authoritative troop-test queue so Realm Paladin cannot be
   recommended or retested during reconciliation;
7. keep protocol, task handoff, branch state, PR body, and validation receipt in
   agreement.

## Current durable state

The PR contains:

- the human-readable consolidation and arithmetic in `README.md`;
- the executable task in `CONSOLIDATION_TASK.md`;
- this two-stage audit record;
- the exact recoverable aggregate in `evidence.csv`;
- machine-readable workflow, evidence, gate, protocol, and blocker state in
  `consolidation.json`;
- the validation receipt in `validation_report.json`;
- the Realm Paladin hold and task references in the authoritative Realm of
  Thrones queue;
- a dedicated consolidation protocol document and dispatcher tests.

## Remaining evidence limitation

Only the additional historical evidence remembered by the operator, if it
exists, remains unrecovered. It must not be inferred. If previously unpublished
screenshots or a ZIP are recovered later, those raw inputs must pass the normal
evidence-ingestion and Phase 1 rules before their observations can change the
consolidated totals.

The absence of that raw package does not make PR #95 undiscoverable and does not
invalidate the four-battle committed aggregate.
