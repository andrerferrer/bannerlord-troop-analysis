# XML SSOT package `export_20260731_150800`

**Package kind:** `xml_ssot_package` (normalized audit SSOT). **Not** an ADR-002 combat evidence package.

## What changed vs `export_20260729_025002`

- TAOM item defs resolved from `LOTRLOME_Armory` + `Alliance.Wargs` inside `TAOM_2_0_12.zip` (install symlinks were empty).
- TAOM catalog: **4 → 3,538** mod items; unknown allowlist **~18k → 13** (`orc_rider_*` MP test stubs).
- Transfer artifact is the **normalized analysis pack** zip (raw XML stays local-only).

## Pin

See `PACKAGE.json` for `expected_package_sha256` and source zip digest.

Repo entry point for agents: [`analysis_pack/README.md`](../../../analysis_pack/README.md).
