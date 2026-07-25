# ADR-001: Combat Screenshot Normalization Pipeline

- **Status:** Implemented for deterministic/offline tooling; production extraction blocked
- **Date:** 2026-07-24
- **Scope:** Empirical Bannerlord battle-result screenshots
- **Repository:** `andrerferrer/bannerlord-troop-analysis`

## Context

The project currently uses screenshots as empirical evidence for troop performance. Manual transcription is slow, difficult to reproduce, and vulnerable to inconsistent naming, missed rows, and transcription mistakes.

Implementation note (2026-07-24): the CLI, schemas, review/canonical layers, mockable extraction contract, ZIP safety, and offline tests exist under `scripts/combat_observations/`. No live provider call or paid upload was performed. Current model IDs remain environment configuration because production inputs are unavailable and model selection must be revalidated against official documentation at execution time.

The goal is to convert combat screenshots into structured, auditable observations that can be committed to the repository and analyzed alongside XML-derived troop data.

This decision covers the extraction architecture and storage format. It does not yet freeze every field in the final normalization schema.

## Decision

Use a two-stage vision pipeline:

1. A cost-efficient vision-capable model performs the first structured extraction for every screenshot.
2. A stronger vision-capable model reviews only low-confidence, contradictory, or validation-failing observations.
3. Responses must use Structured Outputs with a strict JSON Schema.
4. The exact API model IDs are configuration values, not part of the data schema.
5. Model aliases must be revalidated against the current OpenAI API model catalog before implementation and should be pinned for reproducible production runs.

Initial configuration concept:

```text
VISION_EXTRACTOR_MODEL=<current cost-efficient vision-capable model>
VISION_REVIEWER_MODEL=<current strongest suitable vision-capable model>
IMAGE_DETAIL=high
```

Do not make OCR the source of truth. OCR may be used as an auxiliary signal, but the primary extractor must interpret the full screen structure, including rows, columns, faction sides, troop names, and surrounding battle context.

## Why model IDs are not frozen here

OpenAI model availability and aliases change over time. The durable decision is the routing strategy, validation rules, and output contract.

Before implementing or rerunning a production batch:

- verify the available vision-capable models;
- pin the selected versions where possible;
- run a small evaluation set before processing the full dataset;
- record the exact model ID in each extracted observation.

## Data format

Use JSON Lines (`.jsonl`) as the canonical append-friendly dataset format.

Each line represents one normalized troop observation from one battle screenshot. Shared battle metadata may be repeated intentionally to keep each record independently processable.

Suggested repository layout:

```text
data/
  combat_observations/
    raw_images/
      YYYY-MM-DD/
    extracted/
      combat_observations.jsonl
    reviewed/
      combat_observations_reviewed.jsonl
    schemas/
      combat_observation.schema.json
    reports/
      extraction_errors.csv
      low_confidence.csv
      duplicate_images.csv
```

Large raw images should not be committed to normal Git history without a deliberate storage decision. Candidate approaches are Git LFS, release assets, or local/archive storage with committed SHA-256 hashes and manifests.

## Minimum observation contract

```json
{
  "schema_version": "1.0",
  "observation_id": "battle_20260724_001_battanian_fian_champion",
  "source": {
    "image_file": "battle_001_result.png",
    "image_sha256": "<sha256>",
    "captured_at": "2026-07-24T18:30:00-03:00"
  },
  "game": {
    "version": "1.4.x",
    "track": "vanilla_current",
    "campaign": null,
    "active_modules": []
  },
  "battle": {
    "battle_id": "battle_20260724_001",
    "battle_type": "field_battle",
    "result": "victory",
    "duration_seconds": null,
    "player_side_total": null,
    "enemy_side_total": null
  },
  "troop": {
    "display_name_raw": "Battanian Fian Champion",
    "canonical_troop_id": "battanian_fian_champion",
    "side": "player",
    "deployed": null,
    "kills": 34,
    "wounded": 2,
    "dead": 1,
    "survived": null
  },
  "extraction": {
    "model": "<exact-model-id>",
    "confidence": 0.97,
    "needs_review": false,
    "uncertain_fields": [],
    "notes": null
  }
}
```

## Null and uncertainty policy

The model must not infer illegible numbers merely because a value seems plausible.

When a field cannot be read reliably:

```json
{
  "kills": null,
  "uncertain_fields": ["troop.kills"],
  "needs_review": true
}
```

A missing value is preferable to fabricated precision.

## Canonical troop matching

Keep the screen text and normalized identifier separate:

```text
display_name_raw
canonical_troop_id
```

Resolution order:

1. exact match against names from the selected track audit;
2. normalized text match;
3. explicitly maintained aliases;
4. fuzzy match with a conservative threshold;
5. human or reviewer-model resolution when multiple candidates remain.

The extractor may propose a canonical ID, but deterministic repository data should be the final authority.

## Validation requirements

A Python validation layer must check at least:

- non-negative numeric values;
- `dead + wounded + survived <= deployed` when all relevant fields exist;
- `canonical_troop_id` exists in the audit for the specified track;
- referenced track and battle IDs exist or follow the accepted naming convention;
- the image SHA-256 is present and not accidentally duplicated;
- required source and extraction metadata is present;
- values from multiple screenshots of the same battle do not contradict one another.

Validation failures must route the record to review rather than silently correcting it.

## Confidence policy

Do not rely solely on a confidence number generated by the model.

Review routing should combine:

- model-reported uncertainty;
- schema validity;
- arithmetic consistency;
- exact or ambiguous troop-name matching;
- agreement between screenshots of the same battle;
- image quality and crop completeness.

Initial categories:

```text
high: legible data, deterministic troop match, no validation failure
medium: one or more uncertain fields, but usable context
low: cropped rows, unreadable values, ambiguous troop identity, or contradictions
```

Only high-confidence records should enter the canonical dataset without a second pass.

## Batch processing flow

```text
raw screenshot
  -> SHA-256 and source manifest
  -> first-pass vision extraction
  -> strict schema validation
  -> deterministic troop-ID resolution
  -> semantic and arithmetic validation
  -> high confidence: canonical JSONL
  -> otherwise: reviewer-model pass
  -> unresolved: human review queue
```

## Required provenance

Every record must retain:

- original image filename;
- original image SHA-256;
- exact extraction model ID;
- prompt/schema version;
- extraction timestamp;
- review status;
- reviewer model or human reviewer when applicable;
- track and active-module context.

This makes future reprocessing and comparison possible when prompts, models, or schemas change.

## Consequences

### Benefits

- append-friendly, diffable empirical data;
- reproducible linkage between screenshot and normalized observation;
- lower cost through selective escalation;
- deterministic validation against exported troop tracks;
- explicit handling of uncertainty instead of guessed values;
- future reprocessing without losing the original evidence trail.

### Costs and risks

- requires a maintained JSON Schema and validation script;
- raw screenshot storage may require Git LFS or external archives;
- vision extraction still needs an evaluation set and periodic review;
- ambiguous localized troop names may require alias maintenance;
- model upgrades can change extraction behavior unless versions are pinned.

## Parameters intentionally left open

These must be specified using representative screenshots before implementation:

1. exact screen types to support;
2. exact visible columns and their semantic meaning;
3. whether one image can contain multiple pages or scroll states;
4. battle-level metadata available outside the result table;
5. casualty definitions for each screen;
6. handling of reinforcement waves and repeated troop rows;
7. treatment of player, companion, hero, and summoned-unit rows;
8. localized troop-name aliases;
9. confidence and fuzzy-match thresholds;
10. raw-image storage policy;
11. evaluation dataset and acceptance metrics;
12. whether the canonical unit is one battle, one screenshot, or one troop row.

## Next decision

Collect three to five representative screenshots:

- one clean and high-resolution example;
- one difficult or partially obscured example;
- one with many troop rows;
- one where the same battle is represented by multiple screens, when available.

Use these images to finalize `combat_observation.schema.json`, the extraction prompt, normalization rules, and validation thresholds.

## Official API references

- Models: https://platform.openai.com/docs/models
- Image inputs: https://platform.openai.com/docs/guides/images-vision
- Structured Outputs: https://platform.openai.com/docs/guides/structured-outputs
- API backward compatibility and pinned versions: https://platform.openai.com/docs/api-reference/backward-compatibility
