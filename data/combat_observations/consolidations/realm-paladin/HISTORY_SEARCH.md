# Realm Paladin historical evidence search

## Result

The historical evidence was recovered from merged repository artifacts. The
operator's recollection was correct: Realm Paladin already had a reliable field
test in PR #91, followed by four additional compatible field observations in
PR #92.

## Why the first audit missed it

The initial pull-request title search found PR #71's structural shortlist and
PR #92's later aggregate, but no PR titled as a dedicated Realm Paladin batch.
PR #91 is titled `Normalize Aug–Sep ROT White Harbor and Joffrey evidence` and
contains Realm Paladin as one of the batch-wide player-party troops. Searching
committed analysis content for `Realm Paladin` and `realm_paladin` exposed its
reliable field row.

## Recovered repository sources

### PR #91 — gate-clearing field block

```text
merge commit: 3bde0f43bddec1e562937f8da66009c05af04042
source path: data/combat_observations/2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts/analysis/ranking_reliable.csv
source blob: c7b603bc0f77fc4d98c643a8efe81c44101c1489
normalized archive: 9cc8482caf6d37356b186c0a68dfa9e6f50303fb715f6ddfc3a49e2593b59c9d
field result: 11 battles / 122 deployed / 330 kills
```

### PR #92 — later compatible follow-up

```text
pinned ref: 9c92910d499d2663cd77385e516fd25bbc7a4669
source path: data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/analysis/insufficient_evidence.csv
source blob: 8a9e888e30a16b1f29f71025542d1a4c0854b713
normalized archive: 1ba4c3c28db029bda23f57a6c830c0d57107b9a6e89dd1b1258a70514f56222a
field result: 4 battles / 70 deployed / 159 kills
```

Both normalized archives reconstructed to their declared SHA-256 values and
passed an archive-member safety check. Their Realm Paladin field observations
use 15 unique battle IDs and 15 unique source-image hashes. The PR #91 IDs are
`battle_j07`, `battle_j08`, `battle_j09`, `battle_j11`, `battle_j12`,
`battle_j13`, `battle_j14`, `battle_j16`, `battle_j17`, `battle_j18`, and
`battle_j19`; PR #92 uses `battle_jf01` through `battle_jf04`.

The source capture sequence is also non-overlapping: PR #91's last included
Realm Paladin field screen is from 2026-09-05 18:48:50 and PR #92's first is
from 2026-09-05 19:55:03.

## Other findings

- PR #71 is structural candidate evidence only.
- PR #96 mentions Realm Paladin only as an existing queue hold and contributes
  no Realm Paladin combat observations.
- PR #91 also contains two siege-attack observations. They remain separate from
  the field consolidation.
- No remembered number was used.
- The earlier File Library search returned no unpublished Realm Paladin source
  package. That negative external search is no longer a completion blocker
  because the committed PR #91 evidence resolves the field gate.

## Outcome

The repository-addressable field record is 15 battles / 192 deployed / 489
kills. Realm Paladin is reliable for the compatible Joffrey player-party field
context and moves from historical verification hold to
`completed_no_additional_test`.

Any newly recovered raw screenshots must still enter through the ordinary
evidence-ingestion workflow before they can change these totals.
