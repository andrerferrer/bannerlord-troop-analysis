# Phase 2 analytical outputs

`ranking_complete.csv` contains every observed troop/context estimate. `ranking_reliable.csv` applies the 5-battle / 20-deployed gate. `insufficient_evidence.csv` retains all rows that fail the gate. `canonical_identity_audit.csv` never treats provisional slugs as XML IDs.

The batch-level `../README.md` is git-frozen at the normalization commit as Phase 1 metadata. This directory records Phase 2 outputs; authoritative workflow state lives in append-only protocol comments.

`focus_troop_contexts.csv` records each requested focus troop separately for every observed context, including explicit `not_observed` rows. Machine-readable diagnostic rates remain available with their evidence status; the report masks rates unless the full display gate passes.

Reproduce from the repository root:

```bash
batch='data/combat_observations/2026-08-11-to-12-ravens-teeth-field-extension'
work_dir=$(mktemp -d /tmp/bannerlord-analysis.XXXXXX)
archive="$work_dir/ravens_teeth_field_extension_2026-08-11-to-12.tar.xz"
cat "$batch"/bundle/ravens_teeth_field_extension_2026-08-11-to-12.tar.xz.base64.part-* \
  | base64 --decode > "$archive"
python3 - "$archive" "$work_dir/input" <<'PY'
import hashlib
import sys
from pathlib import Path
from scripts.combat_observations.bundle import inspect_tar, safe_extract_tar
archive = Path(sys.argv[1])
expected = '403814973c1cad3e4c5a84032806949c4fad5e613c43d2c8a9f5bcc567188fba'
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit(f'archive SHA-256 mismatch: {actual} != {expected}')
print(inspect_tar(archive))
safe_extract_tar(archive, Path(sys.argv[2]))
PY
python3 scripts/analysis/analyze_normalized_combat_batch.py \
  --input-dir "$work_dir/input/ravens_teeth_field_extension_2026-08-11-to-12" \
  --batch-dir "$batch" --repo-root . --identity-root data/realm_of_thrones/audit \
  --normalization-commit 11c84fed5420acc23b930ffa729bcb978256e8e3 \
  --expected-archive-sha256 403814973c1cad3e4c5a84032806949c4fad5e613c43d2c8a9f5bcc567188fba \
  --archive-path "$archive" \
  --expected-source-sha256 60e861aa3e0e3da7f60beb71f17813b8a25367e3975358e8385f67c972a19047 \
  --expected-source-size-bytes 16772247 \
  --source-path data/combat_observations/2026-08-11-to-12-ravens-teeth-field-extension/source/original_screenshots \
  --batch-id combat_2026-08-11_to_12_ravens_teeth_field_extension --track realm_of_thrones \
  --minimum-battles 5 --minimum-deployed 20 \
  --bootstrap-repetitions 10000 \
  --reviewer 'Phase 2 local review' \
  --focus-slug ravens_teeth
```

## Compatible combined field evidence

After reproducing the standalone analysis above, regenerate the compatible source-batch field projection with:

```bash
python3 scripts/analysis/analyze_compatible_field_evidence.py \
  --config data/combat_observations/2026-08-11-to-12-ravens-teeth-field-extension/analysis/compatible_field_sources.json \
  --repo-root . \
  --batch-dir data/combat_observations/2026-08-11-to-12-ravens-teeth-field-extension \
  --identity-root data/realm_of_thrones/audit
```
