# Local analysis agent prompt — 2026-07-27 Realm of Thrones batch

Copy the prompt below into the local analysis agent. The agent must continue the existing branch and pull request rather than opening a separate analysis PR.

---

You are the **Phase 2 local analysis agent** for the Bannerlord troop-analysis batch normalized on 2026-07-27.

## Repository context

- Repository: `andrerferrer/bannerlord-troop-analysis`
- Branch: `agent/normalize-combat-batch-2026-07-27-only`
- Pull request: `#23`
- Batch directory: `data/combat_observations/2026-07-27-normalized-only`
- Game track: `realm_of_thrones`
- Game version family: `1.4.x`
- Related execution issue: `#21`

Continue this exact branch and PR. Do not open a second pull request for the analysis phase.

## Objective

Add a fully reproducible analytical layer for this batch while preserving the Phase 1 normalized evidence byte-for-byte.

The analysis must distinguish observed campaign contribution from intrinsic troop strength. Do not present the result as a universal tier list or causal estimate.

## Phase 1 handoff facts

- Source screenshots: 13
- Grouped final battles: 10
- Battle contexts: 4 field, 5 siege attack, 1 siege defense
- Structured observations: 328
- Player-side ordinary troop observations: 143
- Active/incomplete scoreboard excluded: 1
- Review-queue items: 5
- Structural validation errors: 0

Expected hashes:

```text
Source ZIP SHA-256:
42d4adf2e8d9f9bce0dc90945832c673aeddf81d06044cb0e6f08a2ddb852617

Normalized-only archive SHA-256:
031a7c60d4ed239a2fcb70a81bb6edf047711c3a422ee3ba4420c4a4af534855
```

## First action: verify and reconstruct the handoff

From the repository root on Bash/Linux/macOS:

```bash
batch='data/combat_observations/2026-07-27-normalized-only'
archive='/tmp/bannerlord_combat_normalized_only_2026-07-27.tar.xz'
input_dir='/tmp/bannerlord-analysis-input-2026-07-27'

cat "$batch"/bundle/bannerlord_combat_normalized_only_2026-07-27.tar.xz.base64.part-* \
  | base64 --decode > "$archive"

echo '031a7c60d4ed239a2fcb70a81bb6edf047711c3a422ee3ba4420c4a4af534855  '"$archive" \
  | sha256sum --check

rm -rf "$input_dir"
mkdir -p "$input_dir"
tar -xJf "$archive" -C "$input_dir"
```

PowerShell equivalent:

```powershell
$batch = 'data/combat_observations/2026-07-27-normalized-only'
$archive = Join-Path $env:TEMP 'bannerlord_combat_normalized_only_2026-07-27.tar.xz'
$inputDir = Join-Path $env:TEMP 'bannerlord-analysis-input-2026-07-27'

$parts = Get-ChildItem "$batch/bundle/bannerlord_combat_normalized_only_2026-07-27.tar.xz.base64.part-*" |
  Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_.FullName -Raw }) -join ''
[IO.File]::WriteAllBytes($archive, [Convert]::FromBase64String($base64))

$actual = (Get-FileHash $archive -Algorithm SHA256).Hash.ToLowerInvariant()
$expected = '031a7c60d4ed239a2fcb70a81bb6edf047711c3a422ee3ba4420c4a4af534855'
if ($actual -ne $expected) { throw "Archive hash mismatch: $actual" }

Remove-Item $inputDir -Recurse -Force -ErrorAction SilentlyContinue
New-Item $inputDir -ItemType Directory | Out-Null
tar -xJf $archive -C $inputDir
```

Stop and document the blocker if the reconstructed hash does not match.

## Raw-source retention status

The original source ZIP is not retained in the repository. Its recorded SHA-256 is:

```text
42d4adf2e8d9f9bce0dc90945832c673aeddf81d06044cb0e6f08a2ddb852617
```

Do not substitute regenerated screenshots or a different archive. Raw retention is optional after the deterministic normalized package passes its hash, manifest, and structural-validation gates. Its absence limits later visual re-review but does not block analysis or merge.

## Immutable Phase 1 inputs

Treat the following as immutable:

- `screenshots_manifest.csv`
- `normalization_summary.json`
- `validation_report.json`
- `artifact_hashes.csv`
- all reconstructed normalized JSONL files
- the four normalized archive parts

Do not edit these files during analysis. Confirm at completion that their hashes match the handoff commit. Any discovered extraction correction must be written as a separate reviewed correction/exclusion record with source-row identity, old value, new value, reason, reviewer, and evidence reference.

## Mandatory analytical boundaries

1. Use player-side ordinary troop rows for the primary campaign baseline.
2. Do not pool player and enemy rows.
3. Keep `field`, `siege_attack`, and `siege_defense` separate.
4. Use battle as the independent sampling unit.
5. Require at least **5 independent battles and 20 deployed troops** before displaying a troop/context estimate as reliable.
6. Publish insufficient-evidence rows separately rather than dropping them.
7. Exclude heroes from ordinary troop rankings.
8. Do not infer troops hidden below the visible scroll area.
9. Do not interpret provisional slugs as canonical XML IDs.
10. Resolve canonical identities only through versioned Realm of Thrones track audits.
11. Do not mix this batch with vanilla/War Sails or another mod track.
12. Do not modify `analysis/model_versions/`; v7.1 and v7.3 are frozen.
13. Report the siege-defense sample as insufficient unless additional independent battles from the same compatible track are explicitly added and versioned.

## Required work

### 1. Verify data integrity

- reconstruct the normalized archive;
- verify archive and individual artifact hashes;
- rerun structural invariants;
- produce a Phase 2 input-verification record.

### 2. Review uncertainty

Inspect all five entries in `review_queue.csv` against raw source evidence when it is retained. When it is unavailable, keep those fields null/unknown and document the limitation. Do not convert visual icons into numeric values without direct evidence. These entries are heroes excluded from ordinary-troop rankings, so unresolved visual review does not block the normalized analysis.

Store decisions in a separate reviewed layer. Do not change normalized rows.

### 3. Resolve identities conservatively

Use the repository's generated Realm of Thrones audit and canonical identity tooling where available.

Accept an ID only when supported by an exact normalized display-name match or an already-versioned reviewed mapping. Record unresolved and ambiguous labels explicitly. Never convert an OCR slug directly into an XML ID.

### 4. Build descriptive aggregates

At minimum calculate, by troop and context:

- independent battles;
- deployed;
- survivors;
- kills;
- deaths;
- wounded;
- routed;
- kills per deployed;
- death rate;
- casualty rate;
- reliable/insufficient-evidence status under the 5-battle / 20-deployed gate.

Consolidate repeated scroll captures within the same battle before aggregation.

### 5. Quantify uncertainty

For reliable estimates, calculate battle-level uncertainty using the repository baseline convention, including deterministic bootstrap intervals where supported. Keep the bootstrap seed and repetition count versioned.

### 6. Compare only compatible evidence

A comparison with an earlier campaign baseline is allowed only when the earlier data is explicitly verified as the same Realm of Thrones track and compatible schema. Never silently pool tracks. When comparability is incomplete, publish a blocked-comparison report instead of forcing a join.

### 7. Interpret cautiously

Discuss:

- consistent performers across independent battles;
- context-specific performance;
- outliers driven by a single battle or small deployment count;
- casualty/performance trade-offs;
- coverage gaps;
- possible confounding by player army composition, battle difficulty, map, siege state, enemy composition, and victory-only sampling.

Do not claim intrinsic superiority, causal equipment effects, universal rankings, or model recalibration readiness from this observational batch.

## Required repository outputs

Create:

```text
data/combat_observations/2026-07-27-normalized-only/
├── review/
│   ├── review_decisions.csv
│   └── README.md
└── analysis/
    ├── README.md
    ├── ANALYSIS_REPORT.md
    ├── input_verification.json
    ├── ranking_complete.csv
    ├── ranking_reliable.csv
    ├── insufficient_evidence.csv
    ├── context_coverage.csv
    ├── canonical_identity_audit.csv
    ├── validation_report.json
    └── artifact_hashes.csv
```

Add scripts under `scripts/analysis/` when computation is not already reproducible with existing repository tooling. Add or update tests for new analysis logic.

## Commit and PR requirements

- Commit analysis separately from normalization.
- Use commit messages prefixed with `analysis:` or `review:`.
- Identify the local agent/tool in the PR body.
- Update PR #23 rather than opening another PR.
- Replace the pending findings section with the actual analytical summary.
- Check every completed Phase 2 checklist item.
- Keep the PR draft while normalized-evidence reconstruction, review, analysis, validation, or hashes remain incomplete.
- Mark ready only after confirming normalized inputs are unchanged and all required outputs are committed.

## Completion report

At the end, report in the PR:

1. exact input and output hashes;
2. review decisions and unresolved fields;
3. canonical identity coverage;
4. reliable and insufficient-evidence counts by context;
5. key descriptive findings with uncertainty;
6. all known limitations and blocked claims;
7. tests and validation commands run;
8. confirmation that `analysis/model_versions/` and Phase 1 normalized files are unchanged.

---
