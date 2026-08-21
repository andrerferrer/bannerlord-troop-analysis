# Phase 2 analytical outputs

`ranking_complete.csv` contains every observed troop/context estimate. `ranking_reliable.csv` applies the 5-battle / 20-deployed gate. `insufficient_evidence.csv` retains all rows that fail the gate. `ANALYSIS_REPORT.md` renders every row as either a reliable rate or explicit below-gate coverage. `canonical_identity_audit.csv` never treats provisional slugs as XML IDs.

The batch-level `../README.md` is git-frozen at the normalization commit as Phase 1 metadata. This directory records Phase 2 outputs; authoritative workflow state lives in append-only protocol comments.

`focus_troop_contexts.csv` records each requested focus troop separately for every observed context, including explicit `not_observed` rows. Machine-readable diagnostic rates remain available with their evidence status; the report masks rates unless the full display gate passes.

`focus_battle_rates.csv`, `battle_provenance.csv`, and
`battle_observation_uncertainty.json` retain the focus/battle detail without
pooling contexts. `../review/review_decisions.csv` and
`../review/VISUAL_REVIEW.md` are the additive exact-image reviewed layer.
`NEXT_TEST_RECOMMENDATION.md` records the next field target and exact gate deficit.

Rebuild the deterministic generated baseline from the repository root in a
disposable checkout. The committed exact-image decisions and recommendation are
reviewed Phase 2 additions and must not be replaced by the generic baseline:

```bash
batch='data/combat_observations/2026-08-21-stark-sworn-mixed'
work_dir=$(mktemp -d /tmp/bannerlord-analysis.XXXXXX)
archive="$work_dir/stark_sworn_mixed_2026-08-21.tar.xz"
cat "$batch"/bundle/stark_sworn_mixed_2026-08-21.tar.xz.base64.part-* \
  | base64 --decode > "$archive"
python3 - "$archive" "$work_dir/input" <<'PY'
import hashlib
import sys
from pathlib import Path
from scripts.combat_observations.bundle import inspect_tar, safe_extract_tar
archive = Path(sys.argv[1])
expected = 'd94a770ddcabeb24eda965fd289dcb1d91c2a4b0ed945322cd0b825057a5bb6e'
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit(f'archive SHA-256 mismatch: {actual} != {expected}')
print(inspect_tar(archive))
safe_extract_tar(archive, Path(sys.argv[2]))
PY
python3 scripts/analysis/analyze_normalized_combat_batch.py \
  --input-dir "$work_dir/input/stark_sworn_mixed_2026-08-21" \
  --batch-dir "$batch" --repo-root . --identity-root data/realm_of_thrones/audit \
  --normalization-commit 0da412b0ed74a1ad7de89fdf53ee2ce6d1947cbc \
  --expected-archive-sha256 d94a770ddcabeb24eda965fd289dcb1d91c2a4b0ed945322cd0b825057a5bb6e \
  --archive-path "$archive" \
  --expected-source-sha256 10b4e2e5e17116df7b8dd1beb8a8c679f6e119b0f7411a0c3ea6040898855498 \
  --expected-source-size-bytes 18907345 \
  --source-path "$batch/source/raw_not_retained" \
  --batch-id combat_2026-08-21_stark_sworn_mixed --track realm_of_thrones \
  --minimum-battles 5 --minimum-deployed 20 \
  --bootstrap-repetitions 10000 \
  --reviewer 'Codex Phase 2 analysis agent (GPT-5.6)' \
  --focus-slug stark_sworn_sword
```
