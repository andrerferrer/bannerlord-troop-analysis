# Realm Paladin — empirical evidence consolidation

## Status

`COMPLETE — RELIABLE FIELD EVIDENCE RECOVERED; NO ADDITIONAL TEST RECOMMENDED`

This historical consolidation resolves the operator's recollection that Realm
Paladin had already been tested. The missing gate-clearing record was committed
in merged PR #91 under a mixed Joffrey/White Harbor batch, so its PR title did
not identify Realm Paladin. A second, later field block was committed in merged
PR #92.

No new screenshots or remembered values are introduced here. Both source rows
and their immutable normalized bundles are repository-addressable.

## Workflow classification

```text
workflow: historical_consolidation
new evidence batch: no
Phase 1 normalization: not applicable
screenshots_manifest.csv: intentionally not required for this PR
handoff/ANALYSIS_PROMPT.md: intentionally not required for this PR
bannerlord-analysis-task:v1: not applicable
bannerlord-consolidation-task:v1: required and published
```

## Compatible field sources

| Source | Battles | Deployed | Kills | Kills/deployed | Kill share | Deployment share | Contribution | Retention | Gate |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PR #91 | 11 | 122 | 330 | 2.704918 | 4.8860% | 3.5620% | 1.371683× | 60.6557% | reliable |
| PR #92 | 4 | 70 | 159 | 2.271429 | 5.9284% | 5.3394% | 1.110307× | 18.5714% | below battle gate alone |
| Combined | 15 | 192 | 489 | 2.546875 | 5.1823% | 4.0541% | 1.278296× | 45.3125% | reliable |

The sources share the same compatibility boundaries:

```text
track: realm_of_thrones
game version: 1.4.x
cohort: joffrey
context: field
participant: player_party
parent group: Joffrey Baratheon's Party
canonical troop: realm_paladin
canonical role: melee_cavalry
```

The 11 PR #91 field battle IDs are `battle_j07`, `battle_j08`, `battle_j09`,
`battle_j11`, `battle_j12`, `battle_j13`, `battle_j14`, `battle_j16`,
`battle_j17`, `battle_j18`, and `battle_j19`. The four PR #92 field battle IDs
are `battle_jf01` through `battle_jf04`. Their source-image hashes are also
disjoint. The last PR #91 observation precedes the first PR #92 observation, so
no battle is counted twice.

Two PR #91 Realm Paladin siege-attack observations remain separate and are not
included in the field result.

## Pinned source identities

PR #91 field row:

```text
path: data/combat_observations/2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts/analysis/ranking_reliable.csv
ref: main@3bde0f43bddec1e562937f8da66009c05af04042
Git blob SHA: c7b603bc0f77fc4d98c643a8efe81c44101c1489
size: 8,212 bytes
normalized archive SHA-256: 9cc8482caf6d37356b186c0a68dfa9e6f50303fb715f6ddfc3a49e2593b59c9d
```

PR #92 field row:

```text
path: data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/analysis/insufficient_evidence.csv
ref: main@9c92910d499d2663cd77385e516fd25bbc7a4669
Git blob SHA: 8a9e888e30a16b1f29f71025542d1a4c0854b713
size: 18,200 bytes
normalized archive SHA-256: 1ba4c3c28db029bda23f57a6c830c0d57107b9a6e89dd1b1258a70514f56222a
```

## Consolidated field result

```text
battles = 11 + 4 = 15
deployed = 122 + 70 = 192
survivors = 74 + 13 = 87
kills = 330 + 159 = 489
deaths = 8 + 9 = 17
wounded = 40 + 48 = 88
victories / defeats = 11 / 4

kills per deployed = 489 / 192 = 2.546875
kill share = 489 / 9,436 = 0.051823
deployment share = 192 / 4,736 = 0.040541
offensive contribution ratio = (489 / 9,436) / (192 / 4,736) = 1.278296×
share-adjusted impact = (489 / 192) × (489 / 9,436) = 0.131986
offensive share gap = 0.051823 - 0.040541 = 0.011282
retention = 87 / 192 = 0.453125
death rate = 17 / 192 = 0.088542
casualty rate = (17 + 88) / 192 = 0.546875
```

## Interpretation

Realm Paladin clears the repository display gate with 15 independent field
battles and 192 deployed. The conclusion does not depend on pooling the later
four-battle block: PR #91 already clears the gate on its own with 11 battles and
122 deployed.

Across the combined observations, Realm Paladin generated 5.1823% of verified
player-side kills from 4.0541% of verified player-side deployments. The 1.278296×
offensive contribution ratio is positive descriptive evidence for this Joffrey
field cohort. Retention varied sharply between the two blocks (60.6557% versus
18.5714%), so survival should not be treated as a troop-only causal effect.

PR #91 ranked Realm Paladin third by efficiency and fifth by share-adjusted
impact inside that batch's reliable Joffrey field comparison. This
consolidation does not invent a new cross-batch rank or alter a frozen model.

## Queue decision

- Move `realm_paladin` / field from `verification_holds` to `closed`.
- Record `completed_no_additional_test`.
- Keep `active_test` null and `ordered_queue` empty.
- Do not recommend another troop until the authoritative queue records one.
- Keep Arryn Winged Knight on its separate historical verification hold.

## Files

- `evidence.csv` — the two pinned compatible source aggregates.
- `battle_evidence.csv` — the 15 field occurrences, battle IDs, image hashes,
  and verified player-side denominators.
- `consolidation.json` — machine-readable combined result and decision.
- `validation_report.json` — source, archive, identity, arithmetic, queue, and
  dispatcher checks.
- `HISTORY_SEARCH.md` — the recovered-history audit.
- `AUDIT_LOG.md` — workflow failures and final resolution.
- `CONSOLIDATION_TASK.md` — executable task contract and completion outcome.
