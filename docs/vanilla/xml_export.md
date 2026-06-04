# Vanilla XML Export

This document describes how to export the vanilla Bannerlord XML files needed for troop analysis.

## Goal

Copy the relevant vanilla XML files from the Bannerlord installation into the repository so they can be normalized and scored.

## Expected game path

Steam default path on Windows:

```powershell
C:\Program Files (x86)\Steam\steamapps\common\Mount & Blade II Bannerlord
```

If the game is installed elsewhere, update `$BannerlordRoot` in the script.

## Relevant vanilla modules

The main vanilla data comes from:

```txt
Modules/Native
Modules/Sandbox
Modules/SandboxCore
Modules/StoryMode
```

For troop analysis, the most important XML files are usually under `ModuleData`.

Expected high-value files:

```txt
spnpccharacters.xml
spitems.xml
crafting_pieces.xml
mpitems.xml
skins.xml
monsters.xml
```

Some names vary by version, so the export script copies all XML files from the relevant modules.

## Recommended repo destination

```txt
data/vanilla/raw_xml/
```

The export should preserve module folders:

```txt
data/vanilla/raw_xml/Native/ModuleData/...
data/vanilla/raw_xml/Sandbox/ModuleData/...
data/vanilla/raw_xml/SandboxCore/ModuleData/...
data/vanilla/raw_xml/StoryMode/ModuleData/...
```

## PowerShell export

Use the script in:

```txt
scripts/export/export_vanilla_xmls.ps1
```

Example:

```powershell
.\scripts\export\export_vanilla_xmls.ps1 `
  -BannerlordRoot "C:\Program Files (x86)\Steam\steamapps\common\Mount & Blade II Bannerlord" `
  -Destination ".\data\vanilla\raw_xml"
```

## After export

Commit the XMLs only if we want this repo to contain raw game data.

Alternative workflow:

1. Keep raw XMLs local.
2. Commit only normalized CSVs.
3. Commit scripts and docs.

For reproducibility, normalized outputs should include:

```txt
source_game_version
source_module
source_xml_file
source_record_id
```
