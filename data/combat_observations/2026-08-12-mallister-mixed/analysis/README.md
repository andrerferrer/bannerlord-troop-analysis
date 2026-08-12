# Phase 2 analytical outputs

`ranking_complete.csv` contains every observed troop/context estimate. `ranking_reliable.csv` applies the 5-battle / 20-deployed gate. `insufficient_evidence.csv` retains all rows that fail the gate. `canonical_identity_audit.csv` never treats provisional slugs as XML IDs.

The batch-level `../README.md` is git-frozen at the normalization commit as Phase 1 metadata. This directory records Phase 2 outputs; authoritative workflow state lives in append-only protocol comments.

`focus_troop_contexts.csv` records each requested focus troop separately for every observed context, including explicit `not_observed` rows. Machine-readable diagnostic rates remain available with their evidence status; the report masks rates unless the full display gate passes.

Reproduce from the repository root:

```bash
batch='data/combat_observations/2026-08-12-mallister-mixed'
work_dir=$(mktemp -d /tmp/bannerlord-analysis.XXXXXX)
archive="$work_dir/mallister_combat_2026-08-12.tar.xz"
cat "$batch"/bundle/mallister_combat_2026-08-12.tar.xz.base64.part-* \
  | base64 --decode > "$archive"
python3 - "$archive" "$work_dir/input" <<'PY'
import hashlib
import sys
from pathlib import Path
from scripts.combat_observations.bundle import inspect_tar, safe_extract_tar
archive = Path(sys.argv[1])
expected = '97db4b82f1d1b146d43c3f3afc421cb4594c2960bd418a045f70c2a0685758e7'
actual = hashlib.sha256(archive.read_bytes()).hexdigest()
if actual != expected:
    raise SystemExit(f'archive SHA-256 mismatch: {actual} != {expected}')
print(inspect_tar(archive))
safe_extract_tar(archive, Path(sys.argv[2]))
PY
python3 scripts/analysis/analyze_normalized_combat_batch.py \
  --input-dir "$work_dir/input/mallister_combat_2026-08-12" \
  --batch-dir "$batch" --repo-root . --identity-root data/realm_of_thrones/audit \
  --normalization-commit 62e389f9621df6d353b60541bcc96f222fb20520 \
  --expected-archive-sha256 97db4b82f1d1b146d43c3f3afc421cb4594c2960bd418a045f70c2a0685758e7 \
  --archive-path "$archive" \
  --expected-source-sha256 da79e212250da1b9105f1c71b7ade09f463b4373de87c011b1a8987979e74016 \
  --expected-source-size-bytes 13002374 \
  --source-path data/combat_observations/2026-08-12-mallister-mixed/source/original_screenshots \
  --batch-id combat_2026-08-12_mallister_mixed --track realm_of_thrones \
  --minimum-battles 5 --minimum-deployed 20 \
  --bootstrap-repetitions 10000 \
  --reviewer 'Codex local analysis agent (GPT-5)' \
  --focus-slug mallister_elite_archer \
  --focus-slug mallister_house_guard \
  --focus-slug mallister_eagle_knight \
  --focus-slug mallister_archer \
  --focus-slug mallister_footman \
  --focus-slug mallister_horseman \
  --focus-slug mallister_knight \
  --focus-slug mallister_man_at_arms
```

## Compatible combined field evidence

After reproducing the standalone analysis above, regenerate the compatible source-batch field projection with:

```bash
python3 scripts/analysis/analyze_compatible_field_evidence.py \
  --config data/combat_observations/2026-08-12-mallister-mixed/analysis/compatible_field_sources.json \
  --repo-root . \
  --batch-dir data/combat_observations/2026-08-12-mallister-mixed \
  --identity-root data/realm_of_thrones/audit
```

## Compatible combined siege attack evidence

After reproducing the standalone analysis above, regenerate the compatible source-batch siege attack projection with:

```bash
python3 scripts/analysis/analyze_compatible_field_evidence.py \
  --config data/combat_observations/2026-08-12-mallister-mixed/analysis/compatible_siege_attack_sources.json \
  --repo-root . \
  --batch-dir data/combat_observations/2026-08-12-mallister-mixed \
  --identity-root data/realm_of_thrones/audit
```
