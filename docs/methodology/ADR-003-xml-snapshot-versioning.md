# ADR-003 — XML snapshot versioning (ordered audits as SSOT)

## Context

A multi-track Bannerlord XML export (`export_20260729_025002`, game v1.4.7) needs a
repository-addressable SSOT. Raw XML is large and already gitignored under
`data/*/raw_xml/*`. Publishing loose XML on a public repo also redistributes
TaleWorlds and third-party content.

## Decision

1. **Version the ordered derived form**: per-track audit CSVs under
   `data/<track>/audit/` plus allowlisted `manifest.csv` /
   `manifest_modules.csv` / `MANIFEST.md`.
2. **Keep XML bodies local-only** (gitignored). The zip remains a local package
   pinned by SHA-256 in the snapshot README / manifests.
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
