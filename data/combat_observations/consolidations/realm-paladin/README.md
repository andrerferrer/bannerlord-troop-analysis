# Realm Paladin — empirical evidence consolidation

## Status

`PARTIAL — KNOWN COMMITTED EVIDENCE CONSOLIDATED; HISTORICAL RECOVERY STILL OPEN`

## Workflow classification

```text
workflow: historical_consolidation
new evidence batch: no
Phase 1 normalization: not applicable
screenshots_manifest.csv: intentionally not required
handoff/ANALYSIS_PROMPT.md: intentionally not required
bannerlord-analysis-task:v1: not applicable
bannerlord-consolidation-task:v1: required and published
```

This PR consolidates an already-normalized, already-analyzed committed aggregate.
It is **not** an unpublished screenshot batch. Do not run
`$normalize-bannerlord-combat-batch` against this directory and do not treat the
absence of `screenshots_manifest.csv` as a missing PR artifact.

A first local Codex attempt applied that Phase 1 workflow and exited 2 on the
absent manifest. A second attempt ran the repository dispatcher, received
`actionable_count: 0`, and stopped because historical consolidation tasks were
not yet discoverable. Both observations, and their corrections, are preserved
in `AUDIT_LOG.md`.

## Discoverable task contract

PR #95 now has a dedicated append-only task protocol:

```text
marker: bannerlord-consolidation-task:v1
task_id: realm-paladin-historical-consolidation
workflow: historical_consolidation
handoff: data/combat_observations/consolidations/realm-paladin/CONSOLIDATION_TASK.md
```

The common dispatcher now recognizes both analysis and consolidation tasks:

```bash
python3 scripts/analysis/discover_analysis_tasks.py --json
```

While the latest consolidation task state is `pending`, `in_progress`, or
`blocked`, that command must return PR #95 as actionable. A screenshot, ZIP,
Phase 1 manifest, or Phase 2 handoff is not required to discover or audit this
already-committed aggregate.

The executable contract is `CONSOLIDATION_TASK.md`; the protocol specification
is `docs/protocols/consolidation-task-v1.md`.

This directory is the durable cross-batch audit record for **Realm Paladin**
(`realm_paladin`) in Realm of Thrones 1.4.x field combat.

The operator recalls that the troop has already been tested. The repository
currently exposes one compatible committed aggregate, but no dedicated Realm
Paladin evidence pull request was found in the pull-request history search. This
consolidation therefore prevents an accidental retest while the missing batch or
screenshots are located.

## Known committed empirical evidence

Source:

```text
data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/
  analysis/insufficient_evidence.csv
```

Pinned source identity:

```text
source analysis: merged PR #92
repository ref: main@9c92910d499d2663cd77385e516fd25bbc7a4669
Git blob SHA: 8a9e888e30a16b1f29f71025542d1a4c0854b713
size: 18,200 bytes
```

Scope is intentionally narrow:

```text
track: realm_of_thrones
version: 1.4.x
cohort: joffrey
context: field
participant: player_party
parent group: Joffrey Baratheon's Party
```

| Metric | Value |
|---|---:|
| Independent battles | 4 |
| Deployed | 70 |
| Survivors | 13 |
| Kills | 159 |
| Deaths | 9 |
| Wounded | 48 |
| Victories / defeats | 1 / 3 |
| Kills per deployed | 2.271429 |
| Player-side total kills | 2,682 |
| Player-side kill share | 5.9284% |
| Player-side total deployed | 1,311 |
| Deployment share | 5.3394% |
| Offensive contribution ratio | 1.110307× |
| Share-adjusted impact | 0.134660 |
| Retention | 18.5714% |
| Casualty rate | 81.4286% |

Arithmetic:

```text
kills per deployed = 159 / 70 = 2.271429
kill share = 159 / 2,682 = 0.059284 = 5.9284%
deployment share = 70 / 1,311 = 0.053394 = 5.3394%
offensive contribution ratio = 0.059284 / 0.053394 = 1.110307×
share-adjusted impact = (159 / 70) × (159 / 2,682) = 0.134660
retention = 13 / 70 = 0.185714 = 18.5714%
casualty rate = (9 + 48) / 70 = 0.814286 = 81.4286%
```

The copied row and every derived value above were rechecked against the pinned
source artifact. See `validation_report.json`.

## Gate status

The committed aggregate clears the deployment threshold but not the
independent-battle threshold:

```text
battle deficit = 5 - 4 = 1
deployment deficit = max(0, 20 - 70) = 0
```

This does **not** authorize an immediate new test. The operator's recollection
of an already-completed block takes precedence while historical reconciliation
is open.

## Structural rationale

Realm Paladin was previously placed in the `near_match_test_queue` by the
field-only Captain-like mounted-melee structural screen:

```text
analysis/candidates/realm_of_thrones_archer_like_mounted_melee_field.csv
Git blob SHA: 3e5d026861f4e40f4bd437b38b5f124261bf770f
```

That row records a melee-skill floor of 230, mobility floor of 230, mean armor
194, shield HP 370, and mean harness armor 72. It is a candidate-screen result,
not empirical proof and not an instruction to repeat a completed test.

## Repository-history audit

A pull-request search for both `Realm Paladin` and `realm_paladin` found the
structural shortlist PR #71, but no dedicated Realm Paladin evidence PR. Only
concrete committed artifacts are promoted here.

Known unresolved possibilities:

1. the dedicated test was played but never normalized or published;
2. its screenshots were included under a mixed batch without a surviving
   canonical identity;
3. the remembered test corresponds to the four-battle Joffrey evidence already
   consolidated above;
4. additional compatible evidence exists outside the currently accessible
   repository artifacts.

## Decision

- **Do not recommend or retest Realm Paladin while this consolidation is open.**
- Keep the troop under a verification hold in the authoritative Realm of
  Thrones queue.
- Do not call the troop `reliable`, `closed`, or `completed` from the four-battle
  aggregate alone.
- Do not ask for a local screenshot/ZIP path merely to validate the
  already-committed aggregate in this PR.
- When missing raw evidence is actually recovered, process it through the normal
  evidence-ingestion rules before adding it to the consolidated totals.
- Preserve cohort/context boundaries, deduplicate by battle identity, append
  only verified compatible observations, and regenerate the metrics.
- If the audit establishes that no additional battle exists, the remaining
  formal field gate is exactly one independent compatible battle; scheduling it
  requires a later operator decision.

## Files

- `README.md` — human-readable scope, evidence, arithmetic, and decision.
- `CONSOLIDATION_TASK.md` — executable task handoff used by the dispatcher.
- `AUDIT_LOG.md` — durable record of both local Codex failure modes and fixes.
- `evidence.csv` — exact copy of the known compatible aggregate with pinned
  source identity.
- `consolidation.json` — machine-readable workflow, protocol, evidence, metrics,
  gate calculation, and blockers.
- `validation_report.json` — source-row, arithmetic, workflow, dispatcher,
  queue, and PR-scope verification.
- `data/combat_observations/test_queues/realm_of_thrones.json` — authoritative
  queue state.
- `docs/protocols/consolidation-task-v1.md` — task-comment protocol.
- `scripts/analysis/discover_analysis_tasks.py` — shared task dispatcher.
- `tests/test_discover_analysis_tasks.py` — analysis/consolidation protocol
  regression tests.
