# PC crafting-piece export prompt — unblock crafted melee/thrown damage

Use this checklist on the Windows PC that runs Mount & Blade II: Bannerlord. It is
self-contained. **Do not fill gaps from memory, do not rename attributes to what you
think they should be, and do not invent a number.** An empty cell is a correct answer;
a guessed cell is not.

## Why this export exists

In `export_20260731_150800`, every crafted weapon in every troop roster has blank
`swing_damage` and `thrust_damage`:

| track | hollow crafted weapon rows | direct (non-crafted) melee rows |
|---|---:|---:|
| `vanilla` | 3,619 | **0** |
| `nightmare_sails` | 3,723 | **0** |
| `realm_of_thrones` | 9,648 | **0** |
| `taom` | 6,663 | **0** |

There are zero `<Item>`-defined melee weapons in any roster, so **all** melee damage in
the analysis is currently a substring match on the crafting-template name, collapsed
onto six distinct values. Full quantification:
[`analysis/item_validation/CRAFTED_DAMAGE_COVERAGE_export_20260731_150800.md`](../../analysis/item_validation/CRAFTED_DAMAGE_COVERAGE_export_20260731_150800.md).

The repository already has the crafted-item **composition** — `item_id → piece_id,
piece_type, scale_factor`, covering 100 % of the crafted items troops actually use,
2,171 distinct pieces across the four tracks. What it does not have, anywhere, is the
**per-piece stats** and the **per-template base stats**. Those exist only in
`crafting_pieces*.xml` and `crafting_templates*.xml` inside the installed modules.

This export closes exactly that gap and nothing else. It does not need troop XML, item
XML, or screenshots.

## What is consumed on the repository side

`scripts/normalization/reconstruct_crafted_weapon_stats.py`. It joins your catalogs to
the repo's `data/<track>/audit/<track>_crafted_item_pieces.csv` and writes
`data/<track>/audit/<track>_crafted_weapon_stats.csv`. It **exits 2 with a
`blocked: missing crafting piece catalog (...)` message** if any required column below is
absent, and it never zero-fills a stat it could not compute. The column names in this
document are the contract — do not rename them.

## Source paths and globs

Default modules root (adjust to your install; Game Pass and Epic differ):

```text
C:\Program Files (x86)\Steam\steamapps\common\Mount & Blade II Bannerlord\Modules
```

Inside each module, collect every `*.xml` whose **file name** matches:

```text
crafting_piece*.xml
crafting_template*.xml
weapon_description*.xml
```

Then, mirroring ADR-003 decision 5 (mods put definitions outside the canonical
filenames), also collect any `*.xml` under a `ModuleData\` path whose first 400 lines
contain one of:

```text
<CraftingPiece
<CraftingTemplate
<WeaponDescription
```

`weapon_description*.xml` matters because crafting templates reference weapon
descriptions for `weapon_class` and the base damage/speed figures; without them the
template catalog cannot be filled.

## Load order per track

Apply load order **per track, in this exact order, later module wins**. These are the
orders pinned in `data/<track>/raw_xml/manifest_modules.csv` for
`export_20260731_150800`. Never merge tracks into one catalog.

| track | load order |
|---|---|
| `vanilla` | `Native`, `Sandbox`, `SandBoxCore`, `StoryMode`, `NavalDLC` |
| `nightmare_sails` | the vanilla five, then `NightmareSailsxDTAB` |
| `realm_of_thrones` | the vanilla five, then `ROT-Core`, `ROT-Content`, `ROT-Dragon`, `ROT_Map` |
| `taom` | the vanilla five, then `TAOM.Dependencies`, `Alliance.Wargs`, `LOTRLOME_Armory`, `TAOM`, `TAOM_Map` |

`NavalDLC` (War Sails) is part of every baseline, not a separate track.

**TAOM caveat, already burned us once.** `Modules\Alliance.Wargs` and
`Modules\LOTRLOME_Armory` are unreadable symlinks; every earlier export walked them as
empty folders. Extract those two module folders from `TAOM_2_0_12.zip` to a scratch
directory and point the script's TAOM load order at the extracted copies. If they come
back empty again, **stop and report it** rather than shipping a TAOM catalog with 0
mod pieces.

Resolution rule inside a track: process modules in load-order index order and let a
later module's definition of the same `piece_id` / `template_id` replace an earlier one.
Record the winning `source_module` and `source_xml` on the row.

## Two files per track, both required

### 1. Long-form verbatim dump — the evidence

`crafting_attributes_<track>.csv`. One row per attribute of every element under a
`<CraftingPiece>`, `<CraftingTemplate>`, or `<WeaponDescription>`, including nested
children. **Do not filter, rename, or normalize anything here.**

```csv
track,load_order_index,module,source_xml,entity_kind,entity_id,element_path,attribute,value
```

- `entity_kind`: `CraftingPiece`, `CraftingTemplate`, or `WeaponDescription`.
- `entity_id`: the `id` attribute of that top-level element.
- `element_path`: element names joined by `/` from the top-level element down, e.g.
  `CraftingPiece/BladeData`.
- `attribute` / `value`: exactly as written in the XML.

This file is what lets us fix the wide mapping in the repository without asking you to
export again. It is not optional.

### 2. Wide contract dumps — what the script reads

Attribute names differ between game versions and mods, so the wide files are a
best-effort mapping over candidate names. **If a field is absent under every candidate,
leave the cell empty.** The long-form file is the authority.

#### `crafting_pieces_stats_<track>.csv`

Required columns, exact names and order:

```csv
piece_id,piece_type,length,weight,swing_damage_factor,thrust_damage_factor,swing_damage_type,thrust_damage_type,swing_speed_factor,source_xml,source_module
```

Optional extra columns are allowed and will be ignored: `tier`, `culture`, `track`,
`load_order_index`, `is_hidden`, `physics_material`.

Candidate attribute names, first non-empty match wins, searched across the
`<CraftingPiece>` element and all of its descendants:

| contract column | candidate XML attribute names |
|---|---|
| `piece_id` | `id` |
| `piece_type` | `piece_type`, `Type` |
| `length` | `length`, `blade_length`, `piece_length` |
| `weight` | `weight`, `piece_weight` |
| `swing_damage_factor` | `swing_damage_factor`, `swing_damage` |
| `thrust_damage_factor` | `thrust_damage_factor`, `thrust_damage` |
| `swing_damage_type` | `swing_damage_type` |
| `thrust_damage_type` | `thrust_damage_type` |
| `swing_speed_factor` | `swing_speed_factor`, `swing_speed`, `speed_factor`, `handling` |

Expected piece types are `Blade`, `Handle`, `Guard`, `Pommel` — the only four present in
the repository's composition file. Export **every** piece you find regardless of type;
do not pre-filter to those four.

Expected row counts (pieces referenced by troop rosters; your file will normally be a
superset because it includes unused pieces too):

| track | distinct piece_ids referenced |
|---|---:|
| `vanilla` | 1,064 |
| `nightmare_sails` | 1,111 |
| `realm_of_thrones` | 1,469 |
| `taom` | 1,719 |

#### `crafting_templates_stats_<track>.csv`

Required columns, exact names and order:

```csv
template_id,weapon_class,swing_damage_base,thrust_damage_base,speed_rating_base,swing_damage_type,thrust_damage_type,source_xml,source_module
```

One row per `(template_id, weapon_class)` pair. If a template exposes no weapon class,
emit one row with `weapon_class` empty.

| contract column | candidate XML attribute names |
|---|---|
| `template_id` | `id` |
| `weapon_class` | `weapon_class`, `WeaponClass` |
| `swing_damage_base` | `swing_damage`, `swing_damage_base`, `SwingDamage` |
| `thrust_damage_base` | `thrust_damage`, `thrust_damage_base`, `ThrustDamage` |
| `speed_rating_base` | `speed_rating`, `swing_speed`, `SpeedRating` |
| `swing_damage_type` | `swing_damage_type` |
| `thrust_damage_type` | `thrust_damage_type` |

These 13 template ids are referenced by troop equipment across the four tracks and must
all appear (`ROT_ThrowingAxe` only in `realm_of_thrones`):

```text
Dagger, Javelin, Mace, OneHandedAxe, OneHandedSword, Pike, ROT_ThrowingAxe,
ThrowingAxe, ThrowingKnife, TwoHandedAxe, TwoHandedMace, TwoHandedPolearm,
TwoHandedSword
```

A template catalog that resolves fewer than 13 rows is incomplete — say so in the report
rather than padding it.

## Export script

PowerShell 5.1 or later. Save as `Export-CraftingCatalogs.ps1`, edit the two paths at
the top, run from an ordinary (non-elevated) prompt.

```powershell
$ErrorActionPreference = 'Stop'

# ---- edit these two ----
$ModulesRoot = 'C:\Program Files (x86)\Steam\steamapps\common\Mount & Blade II Bannerlord\Modules'
$OutRoot     = "$HOME\Desktop\crafting_export"
# TAOM only: folders extracted from TAOM_2_0_12.zip, because the installed
# Alliance.Wargs / LOTRLOME_Armory are unreadable symlinks. Leave as $null if the
# installed copies genuinely read as populated directories.
$TaomZipExtractRoot = "$HOME\Desktop\TAOM_2_0_12_extracted\Modules"
# ------------------------

$Baseline = @('Native','Sandbox','SandBoxCore','StoryMode','NavalDLC')
$Tracks = [ordered]@{
  'vanilla'          = $Baseline
  'nightmare_sails'  = $Baseline + @('NightmareSailsxDTAB')
  'realm_of_thrones' = $Baseline + @('ROT-Core','ROT-Content','ROT-Dragon','ROT_Map')
  'taom'             = $Baseline + @('TAOM.Dependencies','Alliance.Wargs','LOTRLOME_Armory','TAOM','TAOM_Map')
}
$FromZip = @('Alliance.Wargs','LOTRLOME_Armory')

New-Item -ItemType Directory -Force -Path $OutRoot | Out-Null

function Resolve-ModuleDir([string]$Module) {
  if ($TaomZipExtractRoot -and ($FromZip -contains $Module)) {
    $candidate = Join-Path $TaomZipExtractRoot $Module
    if (Test-Path -LiteralPath $candidate) { return $candidate }
  }
  $installed = Join-Path $ModulesRoot $Module
  if (Test-Path -LiteralPath $installed) { return $installed }
  return $null
}

function Get-CraftingXml([string]$ModuleDir) {
  Get-ChildItem -LiteralPath $ModuleDir -Recurse -Filter *.xml -File -ErrorAction SilentlyContinue |
    Where-Object {
      $name = $_.Name.ToLowerInvariant()
      if ($name -like 'crafting_piece*' -or $name -like 'crafting_template*' -or $name -like 'weapon_description*') {
        return $true
      }
      if ($_.FullName -notmatch '\\ModuleData\\') { return $false }
      $head = Get-Content -LiteralPath $_.FullName -TotalCount 400 -ErrorAction SilentlyContinue
      if (-not $head) { return $false }
      $joined = $head -join "`n"
      return ($joined -match '<CraftingPiece[\s>]' -or $joined -match '<CraftingTemplate[\s>]' -or $joined -match '<WeaponDescription[\s>]')
    }
}

function Emit-Attributes {
  param(
    [System.Xml.XmlElement]$Node,
    [string]$Path,
    [hashtable]$Ctx,
    [System.Collections.Generic.List[object]]$Sink,
    [hashtable]$Bag
  )
  foreach ($attr in $Node.Attributes) {
    $Sink.Add([PSCustomObject]@{
      track            = $Ctx.track
      load_order_index = $Ctx.rank
      module           = $Ctx.module
      source_xml       = $Ctx.rel
      entity_kind      = $Ctx.kind
      entity_id        = $Ctx.id
      element_path     = $Path
      attribute        = $attr.Name
      value            = $attr.Value
    })
    $key = $attr.Name.ToLowerInvariant()
    if (-not $Bag.ContainsKey($key) -and $attr.Value -ne '') { $Bag[$key] = $attr.Value }
    if ($Path -ne $Ctx.kind) {
      $scoped = ($Path -replace '.*/', '').ToLowerInvariant() + '.' + $key
      if (-not $Bag.ContainsKey($scoped) -and $attr.Value -ne '') { $Bag[$scoped] = $attr.Value }
    }
  }
  foreach ($child in $Node.ChildNodes) {
    if ($child.NodeType -eq [System.Xml.XmlNodeType]::Element) {
      Emit-Attributes -Node $child -Path "$Path/$($child.Name)" -Ctx $Ctx -Sink $Sink -Bag $Bag
    }
  }
}

function First-Value([hashtable]$Bag, [string[]]$Candidates) {
  foreach ($candidate in $Candidates) {
    $key = $candidate.ToLowerInvariant()
    if ($Bag.ContainsKey($key)) { return $Bag[$key] }
  }
  return ''
}

foreach ($track in $Tracks.Keys) {
  $long     = New-Object System.Collections.Generic.List[object]
  $pieces   = [ordered]@{}
  $templates = [ordered]@{}
  $files    = New-Object System.Collections.Generic.List[object]
  $modules  = New-Object System.Collections.Generic.List[object]
  $rank     = -1

  foreach ($module in $Tracks[$track]) {
    $rank++
    $moduleDir = Resolve-ModuleDir $module
    if (-not $moduleDir) {
      Write-Warning "$track : module not found: $module"
      $modules.Add([PSCustomObject]@{ track=$track; module=$module; load_order_index=$rank; is_baseline=($Baseline -contains $module); module_dir=''; file_count=0; bytes=0 })
      continue
    }
    $found = @(Get-CraftingXml $moduleDir)
    $bytes = 0
    foreach ($file in $found) { $bytes += $file.Length }
    $modules.Add([PSCustomObject]@{ track=$track; module=$module; load_order_index=$rank; is_baseline=($Baseline -contains $module); module_dir=$moduleDir; file_count=$found.Count; bytes=$bytes })

    foreach ($file in $found) {
      $rel = $file.FullName.Substring($moduleDir.Length).TrimStart('\')
      $rel = ($module + '/' + $rel) -replace '\\', '/'
      $files.Add([PSCustomObject]@{
        track  = $track
        module = $module
        path   = $rel
        bytes  = $file.Length
        sha256 = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
      })

      try { $doc = [xml](Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8) }
      catch { Write-Warning "unparseable: $rel"; continue }

      foreach ($kind in @('CraftingPiece','CraftingTemplate','WeaponDescription')) {
        foreach ($node in $doc.GetElementsByTagName($kind)) {
          $id = $node.GetAttribute('id')
          if (-not $id) { continue }
          $bag = @{}
          $ctx = @{ track=$track; rank=$rank; module=$module; rel=$rel; kind=$kind; id=$id }
          Emit-Attributes -Node $node -Path $kind -Ctx $ctx -Sink $long -Bag $bag

          if ($kind -eq 'CraftingPiece') {
            $pieces[$id] = [PSCustomObject]@{
              piece_id             = $id
              piece_type           = (First-Value $bag @('piece_type','Type'))
              length               = (First-Value $bag @('length','blade_length','piece_length'))
              weight               = (First-Value $bag @('weight','piece_weight'))
              swing_damage_factor  = (First-Value $bag @('swing_damage_factor','swing_damage'))
              thrust_damage_factor = (First-Value $bag @('thrust_damage_factor','thrust_damage'))
              swing_damage_type    = (First-Value $bag @('swing_damage_type'))
              thrust_damage_type   = (First-Value $bag @('thrust_damage_type'))
              swing_speed_factor   = (First-Value $bag @('swing_speed_factor','swing_speed','speed_factor','handling'))
              source_xml           = $rel
              source_module        = $module
              tier                 = (First-Value $bag @('tier','piece_tier'))
              culture              = (First-Value $bag @('culture'))
              track                = $track
              load_order_index     = $rank
            }
          }
          else {
            $classes = @()
            foreach ($attrName in @('weapon_class','WeaponClass')) {
              foreach ($n in $node.SelectNodes(".//*[@$attrName]")) { $classes += $n.GetAttribute($attrName) }
              if ($node.HasAttribute($attrName)) { $classes += $node.GetAttribute($attrName) }
            }
            $classes = @($classes | Where-Object { $_ } | Select-Object -Unique)
            if ($classes.Count -eq 0) { $classes = @('') }
            foreach ($cls in $classes) {
              $templates["$id|$cls"] = [PSCustomObject]@{
                template_id        = $id
                weapon_class       = $cls
                swing_damage_base  = (First-Value $bag @('swing_damage','swing_damage_base','SwingDamage'))
                thrust_damage_base = (First-Value $bag @('thrust_damage','thrust_damage_base','ThrustDamage'))
                speed_rating_base  = (First-Value $bag @('speed_rating','swing_speed','SpeedRating'))
                swing_damage_type  = (First-Value $bag @('swing_damage_type'))
                thrust_damage_type = (First-Value $bag @('thrust_damage_type'))
                source_xml         = $rel
                source_module      = $module
                entity_kind        = $kind
                track              = $track
                load_order_index   = $rank
              }
            }
          }
        }
      }
    }
  }

  $enc = 'utf8'
  $long   | Export-Csv (Join-Path $OutRoot "crafting_attributes_$track.csv")     -NoTypeInformation -Encoding $enc
  $pieces.Values    | Select-Object piece_id,piece_type,length,weight,swing_damage_factor,thrust_damage_factor,swing_damage_type,thrust_damage_type,swing_speed_factor,source_xml,source_module,tier,culture,track,load_order_index |
    Export-Csv (Join-Path $OutRoot "crafting_pieces_stats_$track.csv") -NoTypeInformation -Encoding $enc
  $templates.Values | Select-Object template_id,weapon_class,swing_damage_base,thrust_damage_base,speed_rating_base,swing_damage_type,thrust_damage_type,source_xml,source_module,entity_kind,track,load_order_index |
    Export-Csv (Join-Path $OutRoot "crafting_templates_stats_$track.csv") -NoTypeInformation -Encoding $enc
  $files   | Export-Csv (Join-Path $OutRoot "manifest_$track.csv")         -NoTypeInformation -Encoding $enc
  $modules | Export-Csv (Join-Path $OutRoot "manifest_modules_$track.csv") -NoTypeInformation -Encoding $enc

  $blades = @($pieces.Values | Where-Object { $_.piece_type -eq 'Blade' })
  $bladesWithSwing = @($blades | Where-Object { $_.swing_damage_factor -ne '' })
  Write-Host ("{0,-18} xml={1,-4} pieces={2,-5} blades={3,-5} blades_with_swing_factor={4,-5} templates={5}" -f `
    $track, $files.Count, $pieces.Count, $blades.Count, $bladesWithSwing.Count, $templates.Count)
}
```

## Read the summary line before you ship

For each track the script prints `xml`, `pieces`, `blades`,
`blades_with_swing_factor`, `templates`. Sanity expectations:

- `pieces` at least the referenced count in the table above.
- `blades_with_swing_factor` greater than zero. If it is **0**, the candidate attribute
  names did not match this game version — that is exactly the case the long-form dump
  exists for. Ship both files and say so in the report; do not hand-edit values in.
- `templates` at least 13 for `vanilla` and at least 14 for `realm_of_thrones`.
- `taom` `pieces` must be clearly larger than the vanilla count. If TAOM equals vanilla,
  `Alliance.Wargs` / `LOTRLOME_Armory` were empty again.

## Optional but strongly recommended: tooltip validation sample

`piece_composition_v1` is an approximation of TaleWorlds' internal `WeaponDesign` math.
It must be validated against in-game values before any ranking consumes it. Precedent:
`analysis/item_validation/2026-06-05_throwing_tooltips/`.

Record the in-game encyclopedia tooltip for these crafted items — one per crafting
template per track — into `tooltip_validation_<track>.csv`:

```csv
item_id,item_name,observed_swing_damage,observed_thrust_damage,observed_speed,observed_weapon_length,observed_damage_type,source_screenshot,notes
```

Leave a cell empty when the tooltip does not show that stat. Do not derive one stat from
another.

`vanilla`

| template | item_id | display name |
|---|---|---|
| `Dagger` | `pugio` | Pugio |
| `Javelin` | `northern_javelin_1_t2` | Fish Harpoon |
| `Mace` | `empire_mace_1_t2` | Spiked Club |
| `OneHandedAxe` | `peasant_sickle_1_t1` | Sickle |
| `OneHandedSword` | `short_sword_t3` | Short Sword |
| `Pike` | `fine_pike_t4` | Fine Pike |
| `ThrowingAxe` | `highland_throwing_axe_1_t2` | Highland Throwing Axe |
| `ThrowingKnife` | `lowland_throwing_knife` | Lowland Throwing Knife |
| `TwoHandedAxe` | `peasant_2haxe_1_t1` | Hoe |
| `TwoHandedMace` | `aserai_mace_5_t4` | Southern Two Handed Mace |
| `TwoHandedPolearm` | `western_spear_3_t3` | Tall Tipped Long Spear |
| `TwoHandedSword` | `battania_2hsword_1_t2_blunt` | Sparring Twohander |

`realm_of_thrones` adds `thenn_throwing_axe` (Thenn Throwing Axe, `ROT_ThrowingAxe`) and
replaces the sword/mace/pike entries with `vlandia_sword_2_t3` (Ridged Tipped Arming
Sword), `vlandia_mace_1_t2` (Spiked Mace), `vlandia_pike_1_t5` (Pike).

`taom` replaces the mace/two-handed entries with `wm_gundabad_mace_a02`
(`[Gundabad] Mace II`), `wm_dol_goldur_2h_mace_a04`
(`[Dol Guldur] Dol Guldur Two-Handed Mace IV`), `he_sword`
(`[Noldor] Two-Handed Sword I`), and uses `eastern_javelin_3_t4` (Jereed) for `Javelin`.

`nightmare_sails` uses the vanilla list with `eastern_javelin_1_t2` (Tribal Javelin),
`battania_mace_2_t2` (Highland Spiked Club) and `sturgia_mace_2_t4` (Northern Reinforced
Two Handed Mace).

## Hash and manifest steps (ADR-003)

ADR-003 keeps XML bodies **local-only and gitignored**; the manifest is the versioned
identity, and nothing that ends in `.xml` may be hash-pinned into the package
(`build_xml_ssot_package_hashes.py` raises `refusing to hash XML body`). So:

1. The script already wrote `manifest_<track>.csv` (`track,module,path,bytes,sha256`,
   one row per scanned XML) and `manifest_modules_<track>.csv`
   (`track,module,load_order_index,is_baseline,module_dir,file_count,bytes`). These are
   the versioned identity of the sources. **Do not ship the XML files themselves.**
2. Record the game version and the exact launcher load order you had selected.
3. Hash the deliverable CSVs after they are final, and never edit or rename a file after
   hashing it:

   ```powershell
   Get-ChildItem $OutRoot -Filter *.csv | Sort-Object Name | ForEach-Object {
     [PSCustomObject]@{
       file   = $_.Name
       bytes  = $_.Length
       sha256 = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
     }
   } | Export-Csv (Join-Path $OutRoot 'artifact_hashes.csv') -NoTypeInformation -Encoding utf8
   ```

4. Zip the whole `$OutRoot` as `bannerlord_crafting_pieces_<YYYYMMDD>.zip` and hash the
   zip:

   ```powershell
   Compress-Archive -Path "$OutRoot\*" -DestinationPath "$HOME\Desktop\bannerlord_crafting_pieces_20260801.zip"
   (Get-FileHash "$HOME\Desktop\bannerlord_crafting_pieces_20260801.zip" -Algorithm SHA256).Hash.ToLowerInvariant()
   ```

5. Deliver the zip plus its SHA-256 to the repository operator. Retention is
   `local_only` for the zip, exactly like `bannerlord_analysis_pack_20260731.zip` in
   `data/xml_exports/export_20260731_150800/PACKAGE.json`.

## CSV encoding rules

Same contract as `PC_BATTLE_CAPTURE_PROMPT.md`:

- UTF-8, comma delimiter, one header row, RFC 4180 quoting.
- Empty/unknown scalar values are **empty cells**, not `0`, not `N/A`, not `null`.
- Boolean values are lowercase `true`/`false`.
- Do not reorder or rename the required columns; extra trailing columns are fine.
- `Export-Csv -Encoding utf8` on PowerShell 5.1 writes a BOM; that is fine, the reader
  uses `utf-8-sig`.

## Repository-side steps after the zip lands

For the operator, not the PC. New export id follows the `export_YYYYMMDD_HHMMSS`
convention.

```bash
unzip -d /tmp/crafting_export ~/Downloads/bannerlord_crafting_pieces_20260801.zip

# 1. Reconstruct, per track. Exits 2 with "blocked: ..." if an input is insufficient.
for track in vanilla nightmare_sails realm_of_thrones taom; do
  python3 scripts/normalization/reconstruct_crafted_weapon_stats.py \
    --track "$track" \
    --piece-catalog    "/tmp/crafting_export/crafting_pieces_stats_${track}.csv" \
    --template-catalog "/tmp/crafting_export/crafting_templates_stats_${track}.csv"
done

# 2. Gate on the tooltip sample before letting any score read the numbers.
python3 scripts/normalization/reconstruct_crafted_weapon_stats.py \
  --track vanilla \
  --piece-catalog    /tmp/crafting_export/crafting_pieces_stats_vanilla.csv \
  --template-catalog /tmp/crafting_export/crafting_templates_stats_vanilla.csv \
  --tooltip-validation /tmp/crafting_export/tooltip_validation_vanilla.csv \
  --require-tooltip-validation

# 3. MANDATORY. data/<track>/audit/*.csv is hash-pinned and the new file breaks the
#    scoring preflight until the manifest is rebuilt.
python3 scripts/normalization/build_xml_ssot_package_hashes.py \
  --export-id <new_export_id> \
  --source-zip ~/Downloads/bannerlord_crafting_pieces_20260801.zip

# 4. Only then rescore.
python3 scripts/scoring/run_theoretical_role_scores.py
python3 scripts/scoring/write_theoretical_overview.py
```

Step 3 is not optional: `run_theoretical_role_scores.py` globs
`data/<track>/audit/*.csv` and raises
`audit missing from artifact_hashes.csv: ...` for any file not in the manifest.

Until the tooltip gate in step 2 passes, keep labelling melee and thrown rankings as
template-name proxies. `piece_composition_v1` being runnable is not the same as
`piece_composition_v1` being validated.
