# Realm Paladin consolidation audit log

## 2026-09-08 — local Codex run classification

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

## Adjudication

The exit-2 result is **not a defect in PR #95**. It came from applying the
new-evidence Phase 1 validator to the wrong workflow class.

PR #95 is classified as:

```text
workflow: historical_consolidation
new evidence batch: no
Phase 1 normalization required: no
screenshots_manifest.csv required: no
handoff/ANALYSIS_PROMPT.md required: no
bannerlord-analysis-task:v1 comment required: no
```

The source row being consolidated was already normalized and analyzed in the
merged Westerling follow-up batch. This PR does not pretend to recreate that
batch, manufacture raw-image provenance, or promote remembered values into
numeric evidence.

The absent Phase 1 files are therefore **intentionally absent**. The applicable
checks for this PR are:

1. pin the immutable committed source row and its Git blob identity;
2. copy that row exactly into `evidence.csv`;
3. recompute every published derived metric;
4. preserve the operator recollection as a historical lead only;
5. update the authoritative test queue so Realm Paladin cannot be recommended
   or retested during reconciliation;
6. document the unresolved one-battle formal gate deficit without authorizing a
   new battle.

Those checks are represented in `validation_report.json`.

## Current durable state

The PR contains:

- the human-readable consolidation and arithmetic in `README.md`;
- the exact recoverable aggregate in `evidence.csv`;
- machine-readable workflow, evidence, gate, and blocker state in
  `consolidation.json`;
- the validation receipt in `validation_report.json`;
- the Realm Paladin hold and PR references in the authoritative Realm of
  Thrones queue;
- this audit record explaining why Phase 1 artifacts and protocol comments are
  not applicable.

## Remaining blocker

Only the **additional historical evidence**, if it exists, remains unresolved.
It must not be inferred. If previously unpublished screenshots or a ZIP are
recovered later, those raw inputs must pass the normal evidence-ingestion and
Phase 1 validation rules before their observations can be added to the
consolidated totals.

Until that happens, Realm Paladin remains `do_not_retest` and PR #95 remains a
draft historical-consolidation PR.
