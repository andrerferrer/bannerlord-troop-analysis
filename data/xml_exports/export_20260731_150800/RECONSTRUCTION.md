# Reconstruction — xml_ssot_package `export_20260731_150800`

## Source zip (local-only)

| Field | Value |
|---|---|
| Filename | `bannerlord_analysis_pack_20260731.zip` |
| Retention | **local_only** — normalized audits + `analysis_pack/`; no raw module XML |
| Typical path | `~/Downloads/bannerlord_analysis_pack_20260731.zip` |

This package pins **already-normalized** audits. Rebuilding from raw XML on the
Bannerlord PC remains possible, but day-to-day analysis should use `analysis_pack/`
and `data/<track>/audit/` hashes — do not re-hunt XML.

## Refresh hashes + scores

```bash
python3 scripts/normalization/build_xml_ssot_package_hashes.py \
  --export-id export_20260731_150800 \
  --source-zip ~/Downloads/bannerlord_analysis_pack_20260731.zip

python3 scripts/scoring/run_theoretical_role_scores.py
python3 scripts/scoring/write_theoretical_overview.py
```

## Obsolete

`analysis/theoretical/*/export_20260729_025002/` for **TAOM** was scored on a hollow
item catalog — superseded by this export.
