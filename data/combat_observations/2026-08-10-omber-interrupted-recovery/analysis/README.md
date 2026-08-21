# Phase 2 analytical outputs

`ranking_complete.csv` contains every observed troop/context estimate. `ranking_reliable.csv` applies the 5-battle / 20-deployed gate. `insufficient_evidence.csv` retains all rows that fail the gate. `ANALYSIS_REPORT.md` renders every row as either a reliable rate or explicit below-gate coverage. `canonical_identity_audit.csv` never treats provisional slugs as XML IDs.

The batch-level `../README.md` is git-frozen at the normalization commit as Phase 1 metadata. This directory records Phase 2 outputs; authoritative workflow state lives in append-only protocol comments.

`battle_observation_uncertainty.json` and `battle_provenance.csv` preserve the
active/right-censored result and explicitly prevent combination with Casat or a
cleanup fight. Exact-image decisions are recorded additively under
`../review/review_decisions.csv` and `../review/VISUAL_REVIEW.md`.

Rebuild the deterministic machine-generated baseline from the repository root in
a disposable checkout. The generic generator writes review metadata; the committed
Phase 2 reviewed layer then records the separate exact-image visual decision and
active-battle uncertainty without changing Phase 1 inputs.

```bash
batch='data/combat_observations/2026-08-10-omber-interrupted-recovery'
work_dir=$(mktemp -d /tmp/bannerlord-analysis.XXXXXX)
archive="$work_dir/omber_interrupted_recovery_2026-08-10.tar.xz"
cat "$batch"/bundle/omber_interrupted_recovery_2026-08-10.tar.xz.base64.part-* \
  | base64 --decode > "$archive"
python3 - "$archive" "$work_dir/input" <<'PY'
import hashlib
import sys
from pathlib import Path
from scripts.combat_observations.bundle import inspect_tar, safe_extract_tar
archive = Path(sys.argv[1])
expected = '03ff1f4006603b424e5c4c3fc4b3955f5464bb5ed8489819b59a8c44c1e25774'
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit(f'archive SHA-256 mismatch: {actual} != {expected}')
print(inspect_tar(archive))
safe_extract_tar(archive, Path(sys.argv[2]))
PY
python3 scripts/analysis/analyze_normalized_combat_batch.py \
  --input-dir "$work_dir/input/omber_interrupted_recovery_2026-08-10" \
  --batch-dir "$batch" --repo-root . --identity-root data/realm_of_thrones/audit \
  --normalization-commit f0b0019e0f6915d8195e7d7d2b65beb646c5dd05 \
  --expected-archive-sha256 03ff1f4006603b424e5c4c3fc4b3955f5464bb5ed8489819b59a8c44c1e25774 \
  --archive-path "$archive" \
  --expected-source-sha256 f8fad8a43801f885d7428ca15558a78ac54e827a4dd186fd92d59132709ef1d3 \
  --expected-source-size-bytes 2280636 \
  --source-path data/combat_observations/2026-08-10-omber-interrupted-recovery/source/original_screenshot.png \
  --batch-id combat_2026-08-10_omber_interrupted_recovery --track realm_of_thrones \
  --minimum-battles 5 --minimum-deployed 20 \
  --bootstrap-repetitions 10000 \
  --reviewer 'Codex Phase 2 analysis agent (GPT-5.6)'
```
