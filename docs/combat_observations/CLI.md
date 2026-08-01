# Combat observation CLI

Run commands from the repository root with Python 3.11 or newer:

```bash
python3 -m scripts.combat_observations --help
```

The deterministic path uses only the Python standard library and does not require a network connection or API key.

## Production status

The 2026-07-23 normalized bundle is corrupt and the source screenshot ZIP is unavailable. The CLI and fixture pipeline are operational, but production canonical files and rankings must not be generated until one exact-hash source is recovered.

## Reconstruct and verify a normalized bundle

```bash
python3 -m scripts.combat_observations reconstruct-bundle \
  --bundle-dir data/combat_observations/2026-07-23/bundle \
  --archive data/combat_observations/2026-07-23/bundle/bannerlord_normalized_v1.tar.xz \
  --extract-dir data/combat_observations/2026-07-23/bundle/reconstructed \
  --report data/combat_observations/2026-07-23/reports/p0_verification_report.json \
  --forensic-report data/combat_observations/2026-07-23/reports/p0_bundle_forensics.json
```

The command:

- requires exactly parts `00` through `10`;
- streams strict Base64 decoding;
- requires SHA-256 `10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa`;
- rejects unsafe tar paths, links, and special files;
- parses every required CSV, JSON, and JSONL file;
- reconciles row counts against `validation_report.json`;
- is idempotent.

The same Python command works on macOS, Linux, and Windows. It avoids platform-specific `base64` behavior.

## Prepare a new screenshot ZIP or directory

```bash
python3 -m scripts.combat_observations manifest-images \
  --input /path/to/screenshots.zip \
  --output-dir /path/to/batch-output
```

ZIP preflight rejects traversal, absolute paths, symlinks, duplicate names, excessive member/declared sizes, suspicious compression ratios, and corrupt archives. It preserves the source ZIP, hashes every extracted file, inventories unsupported files, and identifies exact duplicate images.

For an already extracted directory, pass the directory as `--input`.

## Extraction modes

Prepare a queue without paid calls:

```bash
python3 -m scripts.combat_observations extract-combat-screens \
  --manifest /path/to/batch-output/manifest/BATCH_ID.csv \
  --output-dir /path/to/batch-output/extraction \
  --mode host-vision
```

Modes:

- `offline-existing`: verify/reprocess existing normalized records without vision calls;
- `host-vision`: queue screenshots for the current host session and record an unknown model version when the host does not expose one;
- `api-batch`: use configured extractor/reviewer model IDs.

`api-batch` requires `VISION_EXTRACTOR_MODEL`, `VISION_REVIEWER_MODEL`, and explicit `--authorize-paid-api`. Queue preparation shows which files would leave the machine. This repository does not make a live provider call merely because those variables exist.

Unreadable values remain null and enter review.

## Review and canonical build

```bash
python3 -m scripts.combat_observations triage-review-queue \
  --input /path/to/review_queue.csv \
  --output-dir /path/to/reviewed

python3 -m scripts.combat_observations build-canonical-dataset \
  --raw-occurrences /path/to/raw/troop_occurrences.jsonl \
  --corrections /path/to/reviewed/review_corrections.jsonl \
  --troop-registry /path/to/track/troops.csv \
  --aliases /path/to/reviewed/troop_aliases.csv \
  --schemas-dir data/combat_observations/schemas/v2 \
  --output-dir /path/to/batch-output

python3 -m scripts.combat_observations validate-canonical-dataset \
  --canonical-dir /path/to/batch-output/canonical \
  --schemas-dir data/combat_observations/schemas/v2 \
  --report /path/to/batch-output/reports/canonical_validation_report.json
```

The builder hashes the raw input before and after execution, applies corrections in a separate layer, validates declared original values, quarantines unresolved ranking-critical rows, and only deduplicates rows when explicit overlap identity proves they are the same visible occurrence.

## Rankings and model comparison

Context complete/reliable rankings are built with canonical data. Optional tier/role views and frozen-model comparison:

```bash
python3 -m scripts.combat_observations build-empirical-rankings \
  --aggregates /path/to/canonical/canonical_historical_aggregates.jsonl \
  --troop-metadata /path/to/track/model.csv \
  --output-dir /path/to/analysis

python3 -m scripts.combat_observations compare-models \
  --aggregates /path/to/canonical/canonical_historical_aggregates.jsonl \
  --general-model /path/to/v7.1.csv \
  --burst-model /path/to/v7.3.csv \
  --output-dir /path/to/analysis

python3 -m scripts.combat_observations calibration-decision \
  --analysis-summary /path/to/analysis/empirical_analysis_summary.json \
  --aggregates /path/to/canonical/canonical_historical_aggregates.jsonl \
  --output /path/to/analysis/calibration_decision.json
```

The comparison keeps v7.1 general and v7.3 burst separate. Missing model-universe coverage makes the report provisional. The calibration command defaults to no model change unless conservative coverage gates pass.

## Empirical display-gate status

Report, per track, whether the minimum display gate (5 independent battles and 20 deployed troops, per track/context/side/troop) is already met, from every already-committed batch under `data/combat_observations/`:

```bash
python3 -m scripts.combat_observations gate-status
python3 -m scripts.combat_observations gate-status --track nightmare_sails --format json
```

Exit code `0` means every requested track (default: all four known tracks) already meets the gate; `1` means at least one does not. Field, siege attack, and siege defense are always reported separately, and never pooled into one score. See `scripts/combat_observations/gate_status.py` for the exact aggregation rules.

## Tests

```bash
python3 -m unittest discover -v
```

Tests include bundle corruption, tar/ZIP safety, formulas, matching, review triage, deduplication, hierarchy behavior, outlier routing, schema/semantic validation, retry behavior, deterministic golden output, and resumable ZIP preflight.

## Portable skill

The repository-local skill lives at:

```text
.agents/skills/analyze-bannerlord-combat-zip/
```

Its wrapper discovers a compatible checkout and invokes this CLI. It does not
reimplement the pipeline. A direct local invocation is:

```bash
python3 .agents/skills/analyze-bannerlord-combat-zip/scripts/invoke_pipeline.py \
  --input "/absolute/path/to/input" \
  --output "/absolute/path/to/output" \
  --mode offline-existing \
  --repo "$PWD"
```

Validate the skill metadata and portable format with:

```bash
.venv/bin/python \
  /Users/andrerferrer/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  .agents/skills/analyze-bannerlord-combat-zip

.venv/bin/agentskills validate \
  .agents/skills/analyze-bannerlord-combat-zip
```

The `.venv` is local and ignored. See the skill's
`references/platform-adapters.md` for Codex, ChatGPT, Claude Code, and Cursor
discovery/invocation behavior. Preview any adapter installation with
`--dry-run`; no global installation is part of this workflow.
