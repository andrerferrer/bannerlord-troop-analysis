# Phase 1 execution report — 2026-07-23 combat batch

## Status

The complete 94-row P1 player-side core-review queue has been reviewed against the exact-hash source screenshots. P1 is complete. The remaining 487 rows are P2: enemy-side, undefined-context, secondary-impact, or otherwise lower-priority evidence.

## Review results

| Decision | Rows |
|---|---:|
| Corrected numeric values | 27 |
| Confirmed without numeric change | 44 |
| Excluded named characters or OCR artifacts | 23 |
| **Total reviewed** | **94** |
| Remaining P1 | **0** |

An earlier working summary reported 32 corrected and 39 confirmed. Replaying every decision against the immutable JSONL showed the correct auditable split is **27 corrected / 44 confirmed / 23 excluded**. The total and final dataset were unchanged.

## Exclusions

The 23 exclusions are not normal troop observations. Twenty are named characters or heroes, including Hake, Gendry, Benjen Stark, Tyrion Lannister, Robin Celtigar, Quirand Quarrelsmith, Daghild, Yana, Rhylan Blacktooth, Gorigos the Boar, and Nadric. Three are screen/header OCR artifacts.

## Alias layer

The approved provisional alias table now contains **18 aliases**: two from P0 and sixteen from P1. Only visually supported corrections are approved. Ambiguous artifacts remain unresolved. These are still provisional labels; matching to verified Bannerlord 1.4.x + War Sails troop IDs remains open.

## Before and after

| Measure | After P0 | After P1 |
|---|---:|---:|
| Strict player-side occurrences | 456 | 527 |
| Independent battles | 40 | 40 |
| Provisional troop identifiers | 190 | 214 |
| Overall eligible labels | 23 | 24 |
| Field eligible labels | 17 | 17 |
| Siege-attack eligible labels | 2 | 2 |
| Siege-defense eligible labels | 0 | 0 |
| Remaining review flags | 581 | 487 |

The increase in provisional identifiers occurs because reviewed rows below the display gate enter the strict dataset. It does not indicate worse normalization. Alias resolution reduced known OCR fragmentation, while many small-sample troop identities remain distinct.

## Material ranking changes

- **Rhodok Admiral Sharpshooter** absorbed a visually verified OCR-fragmented occurrence and moved from 10 battles / 474 deployed / 1.730 kills per deployed to 11 battles / 578 deployed / **2.045**. Its overall point-estimate rank moved from 11th to 7th.
- **Queen's Man [T6]** gained one siege-defense occurrence through alias resolution and moved from 17 battles / 313 deployed / 2.064 to 18 battles / 348 deployed / **2.089**.
- **Dragonstone Elite Archer [T5]** became newly eligible overall: 5 battles, 61 deployed, 114 kills, **1.869 kills per deployed**.
- **Elite Hired Crossbow [T5]**, **Reach House Guard [T5]**, **Rhodok River Guard**, and **Rhodok River Hunter** gained reviewed or alias-consolidated evidence.

These are descriptive campaign results. Rank movement caused by review is evidence that unreviewed OCR values must not be used for model recalibration.

## Integrity and reproduction

```text
P0 baseline SHA-256: 3c0d27a082801d3c8741faac627efaa55dccb3b3e7ad355699178cf096d69bbd
P1 baseline SHA-256: b6ed7790f52480b96fbea88b7f64bfb761eb93cd605374392872c01ab87783d6
```

The P1 baseline was reproduced byte for byte by applying:

1. the published P0 correction parts to the immutable first-pass JSONL;
2. the 94 P1 decision rows;
3. the approved alias table;
4. the five-battle / 20-deployed baseline builder.

Reproduction result:

```text
strict player-side occurrences: 527
independent battles: 40
provisional troop identifiers: 214
overall eligible: 24
field eligible: 17
siege attack eligible: 2
siege defense eligible: 0
P1 baseline SHA-256: b6ed7790f52480b96fbea88b7f64bfb761eb93cd605374392872c01ab87783d6
```

## Current gate decision

Approved:

- exploratory player-side campaign rankings;
- five-battle reporting gate;
- context-specific comparisons with battle-bootstrap intervals;
- use of reviewed P0 and P1 evidence for descriptive analysis.

Not approved:

- universal tier-list claims;
- causal equipment/skill weights;
- frozen-model recalibration;
- matchup claims without enemy-composition controls;
- simulator training.

## Next execution sequence

1. Resolve provisional labels against verified Bannerlord 1.4.x + War Sails troop IDs.
2. Build and validate canonical dataset v2.
3. Produce ranking-stability and coverage reports from canonical IDs.
4. Review P2 only where it supports matchup or context questions.
5. Collect additional siege-attack and especially siege-defense battles.
6. Design controlled speed-versus-damage and skill-versus-equipment experiments.
