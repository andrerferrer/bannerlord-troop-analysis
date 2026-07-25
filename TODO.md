# TODO — Bannerlord Troop Analysis

- **Status date:** 2026-07-24
- **Purpose:** operational handoff for continuing the project in another chat, machine, or work session
- **Current priority:** turn the first-pass combat screenshot normalization into a reviewed, reproducible canonical dataset before using it to recalibrate troop scores

## Execution update — 2026-07-24

The P0–P8 implementation program has been attempted. Local deterministic tooling, schemas, tests, forensic reports, review/canonical builders, empirical analysis scaffolding, storage ADR, and portable-skill packaging are the current workstream. Production data review/generation is blocked because the committed bundle is corrupt and neither exact-hash source artifact is available.

Current classification:

| Phase | Local implementation | Production data |
|---|---|---|
| P0 | complete and tested | blocked: exact archive hash cannot be reconstructed |
| P1 | triage/correction/matching/dedup/validation tooling complete | blocked: review queue and images unavailable |
| P2 | schemas and deterministic canonical builder complete | blocked: no verified raw records |
| P3 | offline CLI, ZIP safety, resumability, extraction queues complete | live provider execution intentionally not performed |
| P4 | rankings/model-comparison tooling complete | blocked: no canonical production records |
| P5 | evidence gate complete; decision is no model change | no calibration justified |
| P6 | storage ADR and reproducibility configuration complete | release/upload pending recovery and authorization |
| P7 | documentation updated to the evidence-backed state | complete |
| P8 | see `.agents/skills/analyze-bannerlord-combat-zip/` | runtime support varies by host |

The unchecked legacy checklist below remains the original production definition of done. Do not interpret local fixture-tested tooling as completion of image-dependent production review.

Exact unblock:

```text
source ZIP SHA-256:
00f83754687fe769fdfdea1bda0b68b4d7801c25195ff803aa1a1b35fa15d69f

or normalized archive SHA-256:
10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa
```

## Start here

Read these files in order:

1. `TODO.md`
2. `data/combat_observations/2026-07-23/README.md`
3. `data/combat_observations/2026-07-23/bundle/README.md`
4. `docs/methodology/COMBAT_IMAGE_NORMALIZATION_RULES.md`
5. `docs/methodology/ADR-001-combat-image-normalization.md`
6. `docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md`
7. `docs/handoff/NEW_CHAT_STARTER.md`

## Current state

The repository contains a complete **first-pass structural normalization** of the screenshot batch captured on 2026-07-23.

Recorded first-pass coverage:

- 60 source screenshots represented by hashes and manifest data;
- 48 grouped screenshot/battle sets;
- 42 final-victory battles included in the primary first-pass analysis;
- 1,260 extracted troop occurrences;
- 1,213 occurrences retained in the primary first-pass dataset;
- 756 rows routed to review because of OCR or classification uncertainty;
- 5 battle groups with undefined context;
- 1 suspected siege-engine-assisted outlier occurrence.

The normalized bundle is stored as 11 ordered Base64 chunks under:

```text
data/combat_observations/2026-07-23/bundle/
```

Expected reconstructed archive SHA-256:

```text
10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa
```

The approximately 85 MB raw screenshot ZIP is **not** committed to normal Git history. Its hash and the individual image hashes are retained in the normalized dataset.

> Important: the current output is a first pass. Do not treat the provisional rankings as authoritative until the review queue and battle classifications have been resolved.

---

# P0 — Restore and verify the normalized bundle

This is the first task in any new environment.

## P0.1 Reconstruct the archive

### Bash

```bash
cd data/combat_observations/2026-07-23/bundle
cat bannerlord_normalized_v1.tar.xz.base64.part-* \
  | base64 --decode \
  > bannerlord_normalized_v1.tar.xz
```

### PowerShell

```powershell
cd data/combat_observations/2026-07-23/bundle

$base64 = (
  Get-ChildItem "bannerlord_normalized_v1.tar.xz.base64.part-*" |
  Sort-Object Name |
  ForEach-Object { Get-Content $_.FullName -Raw }
) -join ""

[IO.File]::WriteAllBytes(
  "bannerlord_normalized_v1.tar.xz",
  [Convert]::FromBase64String($base64)
)
```

## P0.2 Verify integrity

### Bash

```bash
sha256sum bannerlord_normalized_v1.tar.xz
```

### PowerShell

```powershell
(Get-FileHash .\bannerlord_normalized_v1.tar.xz -Algorithm SHA256).Hash.ToLower()
```

Expected result:

```text
10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa
```

## P0.3 Extract the bundle

```bash
mkdir -p reconstructed
tar -xJf bannerlord_normalized_v1.tar.xz -C reconstructed
```

PowerShell can use the same `tar` command on current Windows installations.

## P0.4 Verify expected outputs

Confirm the reconstructed package contains at least:

- `screenshots_manifest.csv`;
- `screenshots.jsonl`;
- `battles.jsonl`;
- `troop_occurrences.jsonl`;
- `primary_troop_occurrences.jsonl`;
- `troop_battle_consolidated.jsonl`;
- `historical_troop_aggregates.jsonl`;
- `ranking_complete.csv`;
- `ranking_reliable.csv`;
- `review_queue.csv`;
- `validation_report.json`;
- `combat_troop_occurrence.schema.json`.

## P0 completion criteria

- [ ] All 11 parts are present.
- [ ] Archive reconstructs without Base64 errors.
- [ ] SHA-256 matches exactly.
- [ ] Archive extracts without errors.
- [ ] Expected files exist and can be parsed.

---

# P1 — Audit the first-pass normalization

The objective is to create a reviewed canonical dataset, not merely improve provisional rankings.

## P1.1 Preserve immutable raw extraction data

- [ ] Keep first-pass files unchanged as an audit layer.
- [ ] Create separate reviewed/canonical outputs rather than overwriting raw OCR results.
- [ ] Every correction must retain:
  - original value or raw OCR text;
  - corrected value;
  - correction source;
  - reviewer identity or process;
  - review timestamp;
  - reason for correction.

Suggested statuses:

```text
raw
reviewed
canonical
excluded
unresolved
```

## P1.2 Triage the 756-row review queue

Create review categories so work can be prioritized:

```text
numeric_uncertainty
ambiguous_troop_name
ambiguous_row_type
ambiguous_parent_party
battle_grouping_uncertainty
battle_context_uncertainty
duplicate_candidate
aggregation_mismatch
possible_ocr_artifact
possible_siege_engine_outlier
```

Priority order:

1. uncertain rows currently influencing primary rankings;
2. rows with uncertain `kills`, `survivors`, `deaths`, or `wounded`;
3. troop identity mismatches;
4. duplicate or cross-page grouping problems;
5. secondary columns such as `upgrade_ready` and `routed`;
6. heroes, lords, companions, and other rows excluded from troop rankings.

- [ ] Produce a review-progress report by category.
- [ ] Record how many rows can be resolved automatically.
- [ ] Record how many require image inspection.
- [ ] Never guess an unreadable value merely to complete a row.

## P1.3 Resolve battle context

Review the 5 groups currently classified as `undefined`.

Allowed values:

```text
field
siege_attack
siege_defense
undefined
```

Use the accepted evidence rules:

- fortifications, garrison, militia, gates, walls, towers, ladders, or siege engines support siege classification;
- green player party on the attacking side supports `siege_attack`;
- green player party on the defending side supports `siege_defense`;
- natural open terrain without siege evidence supports `field`;
- insufficient or conflicting evidence remains `undefined`.

When a human classification replaces an inferred value, preserve:

```text
classification_source = user_override
original_image_inference
original_confidence
review_reason
```

- [ ] Resolve all clearly classifiable groups.
- [ ] Leave genuinely ambiguous groups as `undefined` with an explanation.

## P1.4 Validate screenshot grouping and deduplication

Multiple screenshots may represent different scroll positions of the same battle.

Check grouping evidence:

- timestamps;
- matching side totals;
- matching parties, garrisons, and militias;
- same scene/context;
- overlapping troop rows;
- scroll continuity.

Check deduplication using at least:

```text
battle_id
side
parent_group
row_type
display_name_raw
survivors
kills
upgrade_ready
deaths
wounded
routed
```

- [ ] Confirm no troop row is counted twice because it appears in overlapping screenshots.
- [ ] Confirm different occurrences of the same troop in different parties remain separate.
- [ ] Confirm consolidated battle/troop rows sum valid occurrences rather than averaging occurrence-level rates.

## P1.5 Resolve troop identities against the correct track

The target is Bannerlord 1.4.x with War Sails treated as part of the vanilla baseline for this analysis.

Resolution order:

1. exact display-name match against the selected track audit;
2. normalized text match;
3. maintained alias table;
4. conservative fuzzy match;
5. manual review when more than one candidate remains.

Preserve both:

```text
display_name_raw
canonical_troop_id
```

- [ ] Build or update an explicit alias table.
- [ ] Verify every canonical troop ID exists in the selected track audit.
- [ ] Exclude player, hero, companion, and lord rows from normal troop rankings.
- [ ] Do not require exact hero identity normalization.

## P1.6 Validate numeric fields and formulas

Visible result columns, left to right:

```text
survivors
kills
upgrade_ready
deaths
wounded
routed
```

Primary deployed formula:

```text
deployed = survivors + deaths + wounded
```

Derived metrics:

```text
casualties = deaths + wounded
kills_per_deployed = kills / deployed
survival_rate = survivors / deployed
death_rate = deaths / deployed
wounded_rate = wounded / deployed
casualty_rate = casualties / deployed
routed_rate = routed / deployed
```

Rules:

- `routed` is not added to `deployed` a second time;
- `upgrade_ready` and `routed` are retained but do not enter the primary combat score;
- missing or unreadable values remain null and enter review;
- rates must be recomputed after aggregation, not averaged from child-row rates.

- [ ] Validate non-negative values.
- [ ] Validate derived formulas.
- [ ] Detect impossible or internally contradictory rows.
- [ ] Generate field-level validation errors rather than silently correcting values.

## P1.7 Validate hierarchy totals

Use aggregation checks as evidence, not as an unconditional equality rule:

```text
sum(troop rows) ≈ party total
sum(party rows) ≈ side total
```

Possible statuses:

```text
partial
consistent
inconsistent
not_applicable
```

Record:

```text
aggregation_status
aggregation_difference
```

Differences may occur because of partial scrolling, heroes, hidden rows, game behavior, or extraction mistakes.

- [ ] Identify mismatches caused by incomplete screenshots.
- [ ] Identify mismatches caused by extraction errors.
- [ ] Preserve valid partial records without inventing missing rows.

## P1.8 Review excluded and unsupported screens

First-pass exclusions currently include:

- unsupported screens: 2, 18, 49, and 54;
- keep-retreat result screen: 58;
- active in-battle scoreboard: 60.

- [ ] Verify each exclusion against the source evidence or stored extraction metadata.
- [ ] Keep excluded screens in the manifest and audit trail.
- [ ] Do not include active-combat or irrelevant phase data in primary historical rankings.

## P1.9 Calibrate the siege-engine outlier rule

Current policy:

- preserve the raw occurrence;
- mark suspected siege-engine-assisted results;
- exclude only the suspicious occurrence from primary analysis;
- retain it in a separate outlier/siege-engine analysis;
- do not exclude the entire troop or battle;
- keep normal occurrences of the same troop.

Do not freeze arbitrary thresholds before inspecting the real distribution.

Candidate evidence:

- siege defense context;
- very small deployed count;
- extreme `kills_per_deployed`;
- large deviation from other troops in the same battle;
- large deviation from the troop's own history.

- [ ] Inspect the currently suspected occurrence.
- [ ] Compare it with its battle peers.
- [ ] Compare it with the troop's other occurrences.
- [ ] Define conservative automatic-exclusion and review-only thresholds.
- [ ] Generate a separate siege-engine-assisted report.

## P1 completion criteria

- [ ] All ranking-relevant uncertain rows are reviewed or explicitly unresolved.
- [ ] Battle grouping and deduplication are validated.
- [ ] Every usable troop row has a valid canonical troop ID.
- [ ] Battle context is resolved where evidence permits.
- [ ] Numeric and hierarchical validations pass or have documented exceptions.
- [ ] Outlier treatment is calibrated and occurrence-level.

---

# P2 — Produce canonical dataset v2

Create a clean separation between source extraction, reviewed data, and analytical outputs.

Suggested layout:

```text
data/combat_observations/2026-07-23/
  raw_extraction/
  reviewed/
  canonical/
  reports/
  schemas/
```

Canonical files should include:

```text
canonical_screenshots.jsonl
canonical_battles.jsonl
canonical_occurrences.jsonl
canonical_troop_battle_consolidated.jsonl
canonical_historical_aggregates.jsonl
```

Reports should include:

```text
review_resolutions.csv
unresolved_rows.csv
duplicate_report.csv
aggregation_validation.csv
outlier_report.csv
battle_context_review.csv
canonical_validation_report.json
```

## P2.1 Finalize schemas

Define explicit JSON Schemas for:

- screenshot source record;
- battle record;
- party/group record;
- troop occurrence;
- battle/troop consolidation;
- historical aggregate;
- review correction.

- [ ] Version every schema.
- [ ] Add enums for row type, context, review status, relationship to player, and analysis status.
- [ ] Define nullable fields explicitly.
- [ ] Add semantic validation beyond JSON Schema.

## P2.2 Generate historical views

Required contexts:

```text
field
siege_attack
siege_defense
overall
```

Primary pooled metric:

```text
historical_kills_per_deployed = total_kills / total_deployed
```

Do not use the unweighted mean of per-battle rates as the primary historical metric.

The `overall` view must be marked:

```text
mixed_contexts = true
```

It must not replace context-specific analysis.

## P2.3 Apply evidence grades

The grade is the highest level for which both thresholds are met:

| Evidence grade | Valid deployed troops | Independent battles |
|---|---:|---:|
| `exploratory` | any amount | 1 |
| `low` | at least 10 | at least 2 |
| `medium` | at least 30 | at least 3 |
| `high` | at least 100 | at least 5 |

Generate:

- complete rankings containing every troop with valid observations;
- reliable rankings containing only `medium` and `high` samples.

Calculate grades independently for every battle context and for `overall`.

Excluded outlier occurrences must not increase the primary sample size.

## P2 completion criteria

- [ ] Canonical files pass schema and semantic validation.
- [ ] Every canonical record links back to source screenshot hashes.
- [ ] Complete and reliable rankings regenerate deterministically.
- [ ] No provisional review row silently enters canonical rankings.

---

# P3 — Implement a repeatable screenshot ingestion pipeline

The current normalized dataset should be reproducible from a future screenshot batch.

## P3.1 Build the command-line workflow

Suggested flow:

```text
raw screenshots
→ source manifest and SHA-256
→ screen-type detection
→ screenshot grouping
→ first-pass structured extraction
→ schema validation
→ canonical troop matching
→ arithmetic and hierarchy validation
→ reviewer pass for uncertain records
→ human review queue
→ canonical JSONL
→ historical aggregates and rankings
```

Suggested commands:

```text
manifest-images
extract-combat-screens
review-extractions
build-canonical-dataset
validate-canonical-dataset
build-empirical-rankings
```

## P3.2 Implement deterministic components

- [ ] Image inventory, dimensions, timestamps, and SHA-256.
- [ ] Battle/screenshot grouping heuristics.
- [ ] Row deduplication.
- [ ] Canonical troop matching against track audit data.
- [ ] Formula calculations.
- [ ] Aggregation checks.
- [ ] Evidence-grade calculation.
- [ ] Outlier reporting.
- [ ] Deterministic output ordering.

## P3.3 Implement model-assisted extraction

Use a two-stage architecture:

1. cost-efficient vision-capable model for first pass;
2. stronger reviewer model only for uncertain or invalid records.

Requirements:

- exact model IDs are configuration values;
- pin versions where possible;
- record model ID, prompt version, schema version, and extraction timestamp;
- use strict structured output;
- do not use standalone OCR as the source of truth;
- do not fabricate illegible values;
- route validation failures to review.

Before implementation, verify current model availability through official API documentation.

## P3.4 Add tests

Test fixtures should cover:

- clean one-page result;
- multi-page/scroll result;
- overlapping rows;
- same troop in multiple parties;
- field battle;
- siege attack;
- siege defense;
- unsupported screen;
- ambiguous troop name;
- unreadable numeric field;
- hero/player exclusion;
- aggregation mismatch;
- occurrence-level siege-engine outlier.

- [ ] Unit tests for formulas and matching.
- [ ] Integration test for one complete battle.
- [ ] Golden-file test for deterministic JSONL/CSV outputs.
- [ ] Regression tests for every corrected first-pass failure.

## P3 completion criteria

- [ ] A new screenshot directory can be processed with one documented workflow.
- [ ] The pipeline produces the same results when rerun with the same configuration.
- [ ] Uncertainty is surfaced instead of hidden.
- [ ] Tests protect accepted normalization rules.

---

# P4 — Run empirical troop analysis

Only begin after the canonical dataset is sufficiently reviewed.

## P4.1 Required outputs

Generate rankings and reports for:

- field battles;
- siege attacks;
- siege defenses;
- mixed-context overall view;
- complete samples;
- reliable samples;
- per-tier views;
- role-specific views;
- siege-engine-assisted occurrences separately.

## P4.2 Recommended metrics

Primary:

```text
kills_per_deployed
```

Secondary:

```text
survival_rate
death_rate
wounded_rate
casualty_rate
routed_rate
battle_count
total_deployed
median_battle_kills_per_deployed
best_battle
worst_battle
variation_by_battle
context_distribution
```

Do not interpret `routed_rate` as intrinsic troop weakness without battle-result and morale context.

## P4.3 Compare empirical and modeled performance

Join canonical empirical results to the current authoritative model outputs:

```text
v7.1 — general battlefield score
v7.3 — tooltip-validated throwing burst score
```

Analyze:

- rank correlation;
- score correlation;
- residuals;
- systematic overvaluation and undervaluation;
- effects by role, tier, weapon type, and battle context;
- sample reliability;
- outliers requiring qualitative inspection.

- [ ] Produce a model-vs-empirical comparison table.
- [ ] Produce residual rankings.
- [ ] Separate data-quality failures from model failures.
- [ ] Avoid changing the model because of one exploratory sample.

---

# P5 — Calibrate the combat model

Do not modify frozen model versions directly.

## P5.1 Preserve model history

- [ ] Keep v7.1 and v7.3 immutable.
- [ ] Create a new version only after documenting the hypothesis and evidence.
- [ ] Include migration notes and before/after rankings.
- [ ] Add rollback instructions.

## P5.2 Candidate calibration topics

Review only after empirical validation:

- attack speed and animation interruption;
- effective hit rate;
- AI weapon usage and reliability;
- ranged/melee transition behavior;
- ammunition constraints;
- shield interaction;
- cavalry and horse-archer behavior;
- siege-specific effectiveness;
- captain/perk sensitivity;
- difference between theoretical loadout and observed battlefield usage.

## P5.3 Validation for a new model version

- [ ] Compare against v7.1/v7.3 using the same troop universe.
- [ ] Report rank movements.
- [ ] Check control troops and known sanity cases.
- [ ] Validate each role separately.
- [ ] Test sensitivity to uncertain empirical rows.
- [ ] Freeze the new model only when evidence improves without obvious regressions.

---

# P6 — Improve storage and reproducibility

## P6.1 Decide raw screenshot storage

Current state: raw images are represented by hashes, but the approximately 85 MB ZIP is not in ordinary Git history.

Choose one:

- Git LFS;
- GitHub release asset;
- external immutable archive;
- local archive with redundant backup and committed manifests.

Required properties:

- stable download location;
- source ZIP SHA-256;
- per-image SHA-256;
- documented retrieval procedure;
- no dependence on a temporary chat attachment.

- [ ] Select a storage strategy.
- [ ] Upload the raw source archive.
- [ ] Verify its hash after upload/download.
- [ ] Update repository documentation with the retrieval location.

## P6.2 Simplify normalized bundle storage

The current Base64 chunk approach preserves the artifact but is inconvenient.

Preferred future options:

1. commit readable normalized text files directly when size permits;
2. publish the compact archive as a release asset;
3. retain chunked reconstruction only as a fallback.

- [ ] Decide the canonical distribution format.
- [ ] Add an automated reconstruction and hash-check script.
- [ ] Add CI validation for the bundle.

## P6.3 Add reproducibility metadata

Every production batch should record:

- source archive hash;
- individual image hashes;
- game version;
- selected track;
- active module/load order information;
- extractor model ID;
- reviewer model ID;
- prompt version;
- schema version;
- code commit SHA;
- execution timestamp;
- manual review log.

---

# P7 — Update documentation and handoff files

After canonical v2 is complete:

- [ ] Update `docs/handoff/PROJECT_HANDOFF_SUPER_REPORT.md`.
- [ ] Update `docs/handoff/NEW_CHAT_STARTER.md`.
- [ ] Update the screenshot normalization ADR status and consequences.
- [ ] Update `COMBAT_IMAGE_NORMALIZATION_RULES.md` with calibrated thresholds.
- [ ] Link canonical rankings from the root README.
- [ ] Document exact commands for adding a new screenshot batch.
- [ ] Record unresolved limitations honestly.

---

# Definition of done for the screenshot project

The screenshot-normalization phase is complete when:

- [ ] raw evidence is stored durably and retrievable;
- [ ] every source image has a stable hash and manifest row;
- [ ] battle grouping and deduplication have been reviewed;
- [ ] every ranking-relevant row is reviewed or explicitly unresolved;
- [ ] canonical troop IDs match the correct 1.4.x + War Sails track;
- [ ] context-specific canonical aggregates regenerate deterministically;
- [ ] evidence grades are applied correctly;
- [ ] suspected siege-engine results are separated at occurrence level;
- [ ] complete and reliable rankings are published;
- [ ] the pipeline can process a new batch reproducibly;
- [ ] model-vs-empirical validation has been produced;
- [ ] any new scoring model is versioned without altering frozen predecessors.

---

# Recommended immediate next action

Do **not** start by modifying troop scores.

Start with:

1. reconstruct and hash-verify the normalized archive;
2. inspect `review_queue.csv`;
3. classify the review queue by issue type and ranking impact;
4. resolve the 5 undefined battle contexts;
5. review the suspected siege-engine occurrence;
6. produce the first reviewed/canonical v2 files.

## Suggested continuation prompt

```text
Open the repository and read TODO.md first. Continue the Bannerlord combat screenshot project from P0. Reconstruct and verify the normalized bundle, inspect the review queue, and implement the highest-priority steps toward canonical dataset v2. Preserve raw extraction data, never guess unreadable values, keep outlier exclusion occurrence-level, and do not modify frozen model versions v7.1 or v7.3.
```
