# Reconstruction — xml_ssot_package `export_20260729_025002`

This directory is an **XML audit SSOT package** (`package_kind=xml_ssot_package`).
It is **not** an ADR-002 combat evidence / “normalized batch” package. No
`bannerlord-analysis-task:v1` protocol comment applies.

## Source zip (local-only)

| Field | Value |
|---|---|
| Filename | `bannerlord_xml_export_20260729_025002.zip` |
| SHA-256 | `307d9eab533b1b83bb76545141226f86144af6712ed0b64b29e3efc3e23f3ad8` |
| Size | `22862973` bytes (when present on builder machine) |
| Retention | **local_only** — LFS declined, plain Git declined (public repo; third-party XML) |

Local path convention: `$BANNERLORD_XML_EXPORT_ZIP` or `~/Downloads/bannerlord_xml_export_20260729_025002.zip`.

Preflight: if the zip is missing or the SHA mismatches, **stop** — do not rebuild audits from another dump.

## Rebuild audits (requires extracted raw XML)

Raw XML bodies stay gitignored under `data/<track>/raw_xml/<Module>/`. Allowlisted
manifests are committed. After extracting the zip into each track’s `raw_xml`:

```bash
PY=python3
AUD=scripts/normalization/rebuild_vanilla_audit.py
BASE="Native,Sandbox,SandBoxCore,StoryMode,NavalDLC"

$PY "$AUD" --raw-xml-root data/vanilla/raw_xml --output-dir data/vanilla/audit \
  --track vanilla --load-order "$BASE" --baseline-modules "$BASE"

$PY "$AUD" --raw-xml-root data/nightmare_sails/raw_xml --output-dir data/nightmare_sails/audit \
  --track nightmare_sails --load-order "$BASE,NightmareSailsxDTAB" --baseline-modules "$BASE"

$PY "$AUD" --raw-xml-root data/realm_of_thrones/raw_xml --output-dir data/realm_of_thrones/audit \
  --track realm_of_thrones --load-order "$BASE,ROT-Core,ROT-Content,ROT-Dragon,ROT_Map" --baseline-modules "$BASE" \
  --unknown-items-allowlist data/realm_of_thrones/audit/realm_of_thrones_unknown_items_allowlist.csv

$PY "$AUD" --raw-xml-root data/taom/raw_xml --output-dir data/taom/audit \
  --track taom --load-order "$BASE,TAOM.Dependencies,TAOM,TAOM_Map" --baseline-modules "$BASE" \
  --unknown-items-allowlist data/taom/audit/taom_unknown_items_allowlist.csv
```

Outputs also include `<track>_items_catalog.csv` and
`<track>_unknown_items_review_queue.csv`. Rebuild exits **2** if any soldier
equipment ID is unresolved and not allowlisted. Do **not** finalize with
`--allow-unknown-items`.

Note: this export’s TAOM modules ship almost no item definition XML, so many
TAOM equipment IDs are allowlisted as absent-from-export (see allowlist reason).

## Refresh package hashes

```bash
python3 scripts/normalization/build_xml_ssot_package_hashes.py \
  --export-id export_20260729_025002 \
  --source-zip ~/Downloads/bannerlord_xml_export_20260729_025002.zip
```

Verify:

```bash
python3 -m unittest discover -s tests -p 'test_xml_ssot_package_hashes.py'
```

`expected_package_sha256` in `PACKAGE.json` must match the digest algorithm
documented there (sorted `path,bytes,sha256` rows; hashes file itself excluded).

## Unresolved without raw XML

Fields that require re-opening XML bodies (or visual review of module content not
captured in audits) stay **unresolved** — do not guess them into the SSOT.
