# ADR-003 — XML snapshot versioning (ordered audits as SSOT)

## Context

A multi-track Bannerlord XML export (`export_20260729_025002`, game v1.4.7) needs a
repository-addressable SSOT. Raw XML is large and already gitignored under
`data/*/raw_xml/*`. Publishing loose XML on a public repo also redistributes
TaleWorlds and third-party content.

## Decision

1. **Version the ordered derived form** as an **`xml_ssot_package`** (not an
   ADR-002 combat “normalized” package): per-track audit CSVs under
   `data/<track>/audit/` plus allowlisted `manifest.csv` /
   `manifest_modules.csv` / `MANIFEST.md`, with package metadata under
   `data/xml_exports/<export_id>/` (`PACKAGE.json`, `artifact_hashes.csv`,
   `RECONSTRUCTION.md`).
2. **Keep XML bodies local-only** (gitignored). The zip remains local-only
   (LFS/Git declined for this public repo), pinned by filename + size + SHA-256
   in `PACKAGE.json` / `RECONSTRUCTION.md`.
3. **Track policy for this snapshot**
   - `vanilla`: Native + Sandbox + SandBoxCore + StoryMode + **NavalDLC**
     (War Sails folded into the vanilla baseline).
   - `nightmare_sails`: baselines + `NightmareSailsxDTAB`.
   - `realm_of_thrones`: baselines + ROT modules.
   - `taom`: **promoted** baselines + TAOM modules.
4. Troop XML discovery reads every module `*.xml` for `NPCCharacter`, not only
   `spnpccharacters.xml`, so RoT/TAOM troop files participate.

## Consequences

- Clones get reproducible troop/item audits without LFS for this snapshot.
- Rebuilding audits requires the local raw XML extract (or regenerating from the
  pinned zip).
- Tracks must not be concatenated; join only via explicit multi-track tools.
