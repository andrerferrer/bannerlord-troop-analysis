# Agent workflow

## One batch, one pull request, two agents

Every new evidence batch must use one branch and one draft pull request from ingestion through analysis. The work is split into two explicitly separate phases owned by different agents.

The normalization agent must not perform the analytical phase. The analysis agent must not silently rewrite normalized evidence.

## Phase 1 — normalization agent

The normalization agent must:

1. preserve source provenance and calculate SHA-256 hashes;
2. store every source and generated artifact in the repository;
3. use Git LFS for large binary source files when available;
4. otherwise publish a reconstructible chunked archive with a manifest, reconstruction commands, and expected hash;
5. normalize the source into deterministic structured records;
6. keep player and enemy sides separate;
7. keep field, siege attack, and siege defense separate;
8. preserve uncertain values in an explicit review queue instead of guessing;
9. run structural validation;
10. generate `handoff/ANALYSIS_PROMPT.md` for the local analysis agent;
11. leave the pull request in draft state with the analysis phase unchecked.

The normalization agent must not publish rankings, gameplay conclusions, causal claims, model recalibration, or recommendations as part of Phase 1.

## Phase 2 — local analysis agent

The local analysis agent must:

1. check out the same branch and continue the same pull request;
2. read the batch-specific `handoff/ANALYSIS_PROMPT.md` before changing files;
3. verify source and normalized hashes;
4. treat normalized artifacts as immutable inputs;
5. record corrections in a separate reviewed layer with provenance;
6. resolve troop identities only against versioned track audits;
7. write analytical outputs under the batch `analysis/` directory;
8. use separate commits that identify the analysis phase;
9. update the pull-request checklist and analytical summary;
10. mark the pull request ready only after all acceptance checks pass.

## Repository layout for new batches

```text
data/combat_observations/<batch-id>/
├── README.md
├── source/
│   ├── README.md
│   ├── manifest.sha256
│   └── source archive, Git LFS pointer, or reconstructible parts
├── normalized/
│   ├── normalized records
│   ├── validation_report.json
│   └── artifact_hashes.csv
├── review/
│   └── review_queue.csv
├── handoff/
│   └── ANALYSIS_PROMPT.md
└── analysis/
    ├── ANALYSIS_REPORT.md
    ├── generated tables
    ├── validation_report.json
    └── artifact_hashes.csv
```

Existing batches may retain their current layout. New work must follow this structure unless a documented migration requires otherwise.

## Immutability and corrections

After Phase 1 is declared complete, normalized files are immutable. Any correction must be additive and auditable:

- keep the original normalized record;
- add a reviewed correction or exclusion record;
- identify the source row and reason;
- regenerate downstream outputs;
- update manifests and hashes;
- never overwrite uncertain evidence without provenance.

## Mandatory analytical boundaries

- Minimum display gate: **5 independent battles and 20 deployed troops**.
- The battle is the independent sampling unit.
- Player-side and enemy-side observations must not be pooled.
- Field, siege attack, and siege defense must remain separate.
- Realm of Thrones, vanilla/War Sails, and other mod tracks must not be silently mixed.
- Provisional labels are not canonical XML IDs.
- Off-screen rows must not be inferred.
- Heroes are excluded from ordinary troop rankings.
- `analysis/model_versions/` is frozen unless a dedicated model-change pull request passes the documented gates.

## Merge gate

A batch pull request remains draft after normalization. It may be marked ready only when:

- source evidence is repository-addressable;
- normalization and structural validation are complete;
- the analysis prompt is committed;
- the local agent has completed and validated the analysis;
- normalized hashes still match the Phase 1 handoff;
- unresolved limitations are documented;
- no track, side, or battle-context boundary was violated.
