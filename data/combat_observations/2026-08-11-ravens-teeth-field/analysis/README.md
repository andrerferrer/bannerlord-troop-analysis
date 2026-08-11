# Phase 2 analytical outputs

`ranking_complete.csv` contains every observed troop/context estimate. `ranking_reliable.csv` applies the 5-battle / 20-deployed gate. `insufficient_evidence.csv` retains all rows that fail the gate. `canonical_identity_audit.csv` never treats provisional slugs as XML IDs.

The batch-level `../README.md` is git-frozen at the normalization commit as Phase 1 metadata. This directory records Phase 2 outputs; authoritative workflow state lives in append-only protocol comments.

`focus_troop_contexts.csv` records each requested focus troop separately for every observed context, including explicit `not_observed` rows. Machine-readable diagnostic rates remain available with their evidence status; the report masks rates unless the full display gate passes.

Reproduce from the repository root:

```bash
batch='data/combat_observations/2026-08-11-ravens-teeth-field'
work_dir=$(mktemp -d /tmp/bannerlord-analysis.XXXXXX)
archive="$work_dir/ravens_teeth_field_2026-08-11.tar.xz"
cat "$batch"/bundle/ravens_teeth_field_2026-08-11.tar.xz.base64.part-* \
  | base64 --decode > "$archive"
python3 - "$archive" "$work_dir/input" <<'PY'
import hashlib
import sys
from pathlib import Path
from scripts.combat_observations.bundle import inspect_tar, safe_extract_tar
archive = Path(sys.argv[1])
expected = '78a6f3a80ea8351e847555b44f2e7f01c2b4db3d4b772a5af716dd5eedcebcb8'
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit(f'archive SHA-256 mismatch: {actual} != {expected}')
print(inspect_tar(archive))
safe_extract_tar(archive, Path(sys.argv[2]))
PY
python3 scripts/analysis/analyze_normalized_combat_batch.py \
  --input-dir "$work_dir/input/ravens_teeth_field_2026-08-11" \
  --batch-dir "$batch" --repo-root . --identity-root data/realm_of_thrones/audit \
  --normalization-commit 85857f608ddf6be021c66a65435e57e8ee42023a \
  --expected-archive-sha256 78a6f3a80ea8351e847555b44f2e7f01c2b4db3d4b772a5af716dd5eedcebcb8 \
  --archive-path "$archive" \
  --expected-source-sha256 78cac29a1a239a9435b83878762437057d36974fe890fc41bdd413f6a485f6f9 \
  --expected-source-size-bytes 12476029 \
  --source-path data/combat_observations/2026-08-11-ravens-teeth-field/source/original_screenshots \
  --batch-id combat_2026-08-11_ravens_teeth_field --track realm_of_thrones \
  --minimum-battles 5 --minimum-deployed 20 \
  --bootstrap-repetitions 10000 \
  --reviewer 'Codex local analysis agent (GPT-5)' \
  --focus-slug ravens_teeth
```

## Compatible combined field evidence

After reproducing the standalone analysis above, regenerate the compatible source-batch field projection with:

```bash
python3 scripts/analysis/analyze_compatible_field_evidence.py \
  --config data/combat_observations/2026-08-11-ravens-teeth-field/analysis/compatible_field_sources.json \
  --repo-root . \
  --batch-dir data/combat_observations/2026-08-11-ravens-teeth-field \
  --identity-root data/realm_of_thrones/audit
```
