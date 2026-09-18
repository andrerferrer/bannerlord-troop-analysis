# Retention of the complete weapon-first delivery

Classification: archive-only publication supplement to merged PR #105. This is
not new battle evidence, historical battle consolidation, model recalibration,
or a queue transition. No source data, rankings, test results or queue state changes.

## What is retained

All **29 file payloads** from the delivered
`bannerlord_weapon_first_gauntlet_2026-09-17.zip` are recoverable from this repository:

- **22 files** already versioned by PR #105, pinned at commit
  `e79827d9fd61834479bcbad2d7a2f2fd6f7ce26d`: the reports, data, code, tests,
  workflow and canonical queue snapshot.
- **7 files** preserved byte-for-byte inside `delivery_supplement.tar.xz`:
  five original execution logs, the delivery `LEIA-ME.md`, and `delivery_hashes.json`.

The archive retains the complete initial green, adversarial red, corrected green,
full-suite and unchanged-baseline-failure logs. Their original byte counts and
SHA-256 values match `validation_report.json` at the pinned source commit.
The earlier statement that logs were only retained in the delivered ZIP describes
the state at PR #105; this supplement closes that repository-retention gap.

The original ZIP container itself is not duplicated. Every file's contents are
retained, but a newly repacked ZIP is not claimed to have identical container bytes.
Original ZIP SHA-256 for provenance:
`69fe8ef1d1d7c0932c3a8338ed394cfec30d5e9c179a79339a9de2e09e387f2b`.

## Integrity and reproduction

Supplement size: 14,048 bytes.
Supplement SHA-256:
`f1076c2618db989b33d3379e015d7ed5d1cd7888d0849fa6dc4b4b9174758065`.
Original delivery manifest SHA-256:
`94c48ec80afb94895c84a2559e6acdc80deca2beda1a20cebc6009d1bb0c8be6`.

From a repository checkout containing the pinned source commit:

```bash
python3 analysis/weapon_first/2026-09-17/verify_delivery_archive.py
```

The verifier reads the archive without extracting files, checks the exact member
set and original manifest, verifies every original file against either the archive
or `git show` at the source commit, and rechecks all five logs against the original
validation report. It never rewrites the working tree or restores an old queue.
Later changes to the active troop therefore do not invalidate archival verification.

Local checks passed against the original delivered ZIP: all 29 file payloads;
archive round-trip and original log hashes; intentionally corrupted archive and
altered source payload rejected. The accompanying read-only CI runs the verifier
against actual Git objects and reruns the existing 32 scoped weapon-first tests.
The previous three baseline full-suite failures are retained, not repaired or
relabeled as passing by this archival change.

The initial archival CI run exposed an incorrect hardcoded parent-directory lookup
and an LFS pointer warning. Repository discovery now uses `git rev-parse` from the
script directory. A local `.gitattributes` entry explicitly stores only this tiny,
immutable test-log archive in ordinary Git; root LFS rules for large archives and
raw evidence remain unchanged. CI checks the exact file's filter is unset and the
working tree is clean, rather than suppressing the warning or weakening hashes.

## Scope and rollback

Only this note, the archive, its verifier, the single-file Git attribute and a
branch-bounded read-only CI workflow are added. The 22 existing delivered files
remain unchanged. Reverting this supplement removes the extra retained material
without changing PR #105's audit or the canonical troop queue.
