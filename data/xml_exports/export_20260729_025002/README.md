# XML export snapshot `export_20260729_025002`

## SSOT

- Ordered track audits under `data/<track>/audit/` (committed).
- Per-track `data/<track>/raw_xml/manifest.csv` + `manifest_modules.csv` + `MANIFEST.md` (committed).
- Raw XML bodies remain local-only under `data/<track>/raw_xml/<Module>/` (gitignored).
- Package identity: zip SHA-256 `307d9eab533b1b83bb76545141226f86144af6712ed0b64b29e3efc3e23f3ad8` (local Downloads / machine export; not committed as loose XML).

## Track policy

| Track | Policy |
|---|---|
| vanilla | Baseline includes Native, Sandbox, SandBoxCore, StoryMode, **NavalDLC (War Sails folded)** |
| nightmare_sails | Overlay on vanilla baseline + NightmareSailsxDTAB |
| realm_of_thrones | Overlay on vanilla baseline + ROT modules |
| taom | **Promoted** overlay on vanilla baseline + TAOM modules |

Do not silently join tracks. Use separate `--track-audit` entries.

## Ordered audit counts (this rebuild)

| Track | NPC rows | Soldiers |
|---|---:|---:|
| `vanilla` | 1937 | 367 |
| `nightmare_sails` | 1989 | 371 |
| `realm_of_thrones` | 6187 | 1232 |
| `taom` | 5255 | 1237 |

