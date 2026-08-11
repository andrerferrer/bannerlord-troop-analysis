# Phase 2 analytical outputs

`ranking_complete.csv` contains every observed troop/context estimate. `ranking_reliable.csv` applies the 5-battle / 20-deployed gate. `insufficient_evidence.csv` retains all rows that fail the gate. `canonical_identity_audit.csv` never treats provisional slugs as XML IDs.

The batch-level `../README.md` is preserved byte-for-byte as the immutable Phase 1 snapshot. This directory records Phase 2 outputs; authoritative workflow state lives in append-only protocol comments.

`focus_troop_contexts.csv` records each requested focus troop separately for every observed context, including explicit `not_observed` rows.

Reproduce from the repository root:

```bash
batch='data/combat_observations/2026-08-08-to-10-sarnori-mixed'
work_dir=$(mktemp -d /tmp/bannerlord-analysis.XXXXXX)
archive="$work_dir/sarnori_combat_2026-08-08_to_10.tar.xz"
cat "$batch"/bundle/sarnori_combat_2026-08-08_to_10.tar.xz.base64.part-* \
  | base64 --decode > "$archive"
python3 - "$archive" "$work_dir/input" <<'PY'
import hashlib
import sys
from pathlib import Path
from scripts.combat_observations.bundle import inspect_tar, safe_extract_tar
archive = Path(sys.argv[1])
expected = '54c5ed631540a13a59af5f799910b7253ad09d873b414e0776b1e64f25947bc1'
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit(f'archive SHA-256 mismatch: {actual} != {expected}')
print(inspect_tar(archive))
safe_extract_tar(archive, Path(sys.argv[2]))
PY
python3 scripts/analysis/analyze_normalized_combat_batch.py \
  --input-dir "$work_dir/input/sarnori_combat_2026-08-08_to_10" \
  --batch-dir "$batch" --repo-root . --identity-root data/realm_of_thrones/audit \
  --normalization-commit 0f42832bc22b20cc83d2e61da026dd049e2bc24e \
  --expected-archive-sha256 54c5ed631540a13a59af5f799910b7253ad09d873b414e0776b1e64f25947bc1 \
  --archive-path "$archive" \
  --expected-source-sha256 adcb2b9f8545c042f57b5ced51374d919b2829e0d81500aba353507b3dff88bc \
  --expected-source-size-bytes 14829018 \
  --source-path "$PWD/data/combat_observations/2026-08-08-to-10-sarnori-mixed/source/original_screenshots" \
  --batch-id combat_2026-08-08_to_10_sarnori_mixed --track realm_of_thrones \
  --minimum-battles 5 --minimum-deployed 20 \
  --bootstrap-repetitions 10000 \
  --reviewer 'Codex local analysis agent (GPT-5)' \
  --focus-slug sarnori_spider \
  --focus-slug sarnori_master_javelinier \
  --focus-slug sarnori_master_spearman \
  --focus-slug sarnori_javelineer \
  --focus-slug sarnori_elite_javelinier \
  --focus-slug sarnori_archer \
  --focus-slug sarnori_elite_archer \
  --focus-slug sarnori_longbowman
```
