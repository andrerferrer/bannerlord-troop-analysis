# Phase 2 analytical outputs

`ranking_complete.csv` contains every observed troop/context estimate. `ranking_reliable.csv` applies the 5-battle / 20-deployed gate. `insufficient_evidence.csv` retains all rows that fail the gate. `canonical_identity_audit.csv` never treats provisional slugs as XML IDs.

The batch-level `../README.md` documents the shared batch envelope; authoritative workflow state lives in append-only protocol comments.

Reproduce from the repository root:

```bash
batch='data/combat_observations/2026-07-27-normalized-only'
work_dir=$(mktemp -d /tmp/bannerlord-analysis-20260727.XXXXXX)
archive="$work_dir/bannerlord_combat_normalized_only_2026-07-27.tar.xz"
cat "$batch"/bundle/bannerlord_combat_normalized_only_2026-07-27.tar.xz.base64.part-* \
  | base64 --decode > "$archive"
python3 - "$archive" "$work_dir/input" <<'PY'
import hashlib
import sys
from pathlib import Path
from scripts.combat_observations.bundle import inspect_tar, safe_extract_tar
archive = Path(sys.argv[1])
expected = '031a7c60d4ed239a2fcb70a81bb6edf047711c3a422ee3ba4420c4a4af534855'
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit(f'archive SHA-256 mismatch: {actual} != {expected}')
print(inspect_tar(archive))
safe_extract_tar(archive, Path(sys.argv[2]))
PY
python3 scripts/analysis/analyze_normalized_combat_batch.py \
  --input-dir "$work_dir/input/bannerlord_combat_normalized_2026-07-27" \
  --batch-dir "$batch" --repo-root . --identity-root data/rot_reference \
  --existing-identity-audit analysis/empirical/2026-07-23/canonical_identity_audit.csv \
  --normalization-commit 4e0749b84f5efc297ebcb026fa6dfbdaaed7fdf1 \
  --expected-archive-sha256 031a7c60d4ed239a2fcb70a81bb6edf047711c3a422ee3ba4420c4a4af534855 \
  --archive-path "$archive" \
  --expected-source-sha256 42d4adf2e8d9f9bce0dc90945832c673aeddf81d06044cb0e6f08a2ddb852617 \
  --expected-source-size-bytes 18596761 \
  --source-path "$PWD/$batch/source/original_screenshots.zip" \
  --batch-id combat_2026-07-27_222843_010541 --track realm_of_thrones \
  --minimum-battles 5 --minimum-deployed 20 --bootstrap-repetitions 5000
```
