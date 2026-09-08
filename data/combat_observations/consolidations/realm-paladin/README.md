# Realm Paladin — empirical evidence consolidation

## Status

`PARTIAL — KNOWN COMMITTED EVIDENCE CONSOLIDATED; HISTORICAL RECOVERY STILL OPEN`

This directory is the durable cross-batch audit record for **Realm Paladin** (`realm_paladin`) in Realm of Thrones 1.4.x field combat.

The operator recalls that the troop has already been tested. The repository currently exposes one compatible committed aggregate, but no dedicated Realm Paladin evidence pull request was found in the pull-request history search. This consolidation therefore prevents an accidental retest while the missing batch or screenshots are located.

## Known committed empirical evidence

Source:

```text
data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/
  analysis/insufficient_evidence.csv
```

Pinned source identity:

```text
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

The copied row and every derived value above were rechecked against the pinned source artifact. See `validation_report.json`.

## Gate status

The committed aggregate clears the deployment threshold but not the independent-battle threshold:

```text
battle deficit = 5 - 4 = 1
deployment deficit = max(0, 20 - 70) = 0
```

This does **not** authorize an immediate new test. The operator's recollection of an already-completed block takes precedence while historical reconciliation is open.

## Structural rationale

Realm Paladin was previously placed in the `near_match_test_queue` by the field-only Captain-like mounted-melee structural screen:

```text
analysis/candidates/realm_of_thrones_archer_like_mounted_melee_field.csv
Git blob SHA: 3e5d026861f4e40f4bd437b38b5f124261bf770f
```

That row records a melee-skill floor of 230, mobility floor of 230, mean armor 194, shield HP 370, and mean harness armor 72. It is a candidate-screen result, not empirical proof and not an instruction to repeat a completed test.

## Repository-history audit

A pull-request search for both `Realm Paladin` and `realm_paladin` found the structural shortlist PR #71, but no dedicated Realm Paladin evidence PR. Repository code search was not treated as authoritative when unavailable; only concrete committed artifacts are promoted here.

Known unresolved possibilities:

1. the dedicated test was played but never normalized or published;
2. its screenshots were included under a mixed batch without a surviving canonical identity;
3. the remembered test corresponds to the four-battle Joffrey evidence already consolidated above;
4. additional compatible evidence exists outside the currently accessible repository artifacts.

## Decision

- **Do not recommend or retest Realm Paladin while this consolidation is open.**
- Keep the troop under a verification hold in the authoritative Realm of Thrones queue.
- Do not call the troop `reliable`, `closed`, or `completed` from the four-battle aggregate alone.
- When missing evidence is recovered, preserve cohort/context boundaries, deduplicate by battle identity, append only verified compatible observations, and regenerate the metrics.
- If the audit establishes that no additional battle exists, the remaining formal field gate is exactly one independent compatible battle; scheduling it requires a later operator decision.

## Files

- `README.md` — human-readable scope, evidence, arithmetic, and decision.
- `evidence.csv` — normalized copy of the known compatible aggregate with pinned source identity.
- `consolidation.json` — machine-readable state, metrics, gate calculation, and blockers.
- `validation_report.json` — source-row, arithmetic, queue, and PR-scope verification.
- `data/combat_observations/test_queues/realm_of_thrones.json` — authoritative queue state.
