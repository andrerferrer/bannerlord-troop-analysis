param(
  [string]$BannerlordRoot = "C:\Program Files (x86)\Steam\steamapps\common\Mount & Blade II Bannerlord",
  [string]$Track = "vanilla",
  [string]$Destination = "",
  [string[]]$Modules = @("Native", "Sandbox", "SandboxCore", "StoryMode"),
  [string[]]$ExtraModules = @(),
  [string]$LauncherData = "$env:USERPROFILE\Documents\Mount and Blade II Bannerlord\Configs\LauncherData.xml"
)

$ErrorActionPreference = "Stop"

function Add-Unique([System.Collections.Generic.List[string]]$List, [string]$Value) {
  if (-not [string]::IsNullOrWhiteSpace($Value) -and -not $List.Contains($Value)) {
    [void]$List.Add($Value)
  }
}

function Get-XmlFieldValue($Node, [string[]]$Names) {
  foreach ($name in $Names) {
    foreach ($attribute in $Node.Attributes) {
      if ($attribute.Name -ieq $name) {
        return [string]$attribute.Value
      }
    }

    foreach ($child in $Node.ChildNodes) {
      if ($child.LocalName -ieq $name) {
        $childValue = [string]$child.InnerText
        if ([string]::IsNullOrWhiteSpace($childValue)) {
          foreach ($attribute in $child.Attributes) {
            if ($attribute.Name -ieq "value") {
              $childValue = [string]$attribute.Value
              break
            }
          }
        }
        return $childValue
      }
    }
  }

  return $null
}

function Get-ModuleVersion([string]$ModulePath) {
  $subModulePath = Join-Path -Path $ModulePath -ChildPath "SubModule.xml"
  if (-not (Test-Path -LiteralPath $subModulePath)) {
    return ""
  }

  try {
    [xml]$subModuleXml = Get-Content -LiteralPath $subModulePath -Raw
    $versionNode = $subModuleXml.SelectSingleNode("//*[local-name()='Version']")
    if ($null -eq $versionNode) {
      return ""
    }

    $version = Get-XmlFieldValue $versionNode @("value", "Value")
    if ([string]::IsNullOrWhiteSpace($version)) {
      $version = [string]$versionNode.InnerText
    }
    return $version.Trim()
  } catch {
    Write-Warning "Could not read module version from $subModulePath`: $($_.Exception.Message)"
    return ""
  }
}

function Get-SelectedLauncherModules([string]$Path) {
  $selected = [System.Collections.Generic.List[string]]::new()
  if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) {
    return $selected
  }

  try {
    [xml]$launcherXml = Get-Content -LiteralPath $Path -Raw
    $nodes = $launcherXml.SelectNodes("//*[local-name()='UserModData']")
    foreach ($node in $nodes) {
      $isSelected = Get-XmlFieldValue $node @("IsSelected", "Selected")
      if ($isSelected -notmatch '^(?i:true|1)$') {
        continue
      }

      $moduleId = Get-XmlFieldValue $node @("Id", "ModuleId", "Name")
      Add-Unique $selected $moduleId
    }
  } catch {
    Write-Warning "Could not parse LauncherData.xml at $Path`: $($_.Exception.Message)"
  }

  return $selected
}

if ([string]::IsNullOrWhiteSpace($Track)) {
  throw "Track cannot be empty."
}

if ([string]::IsNullOrWhiteSpace($Destination)) {
  $Destination = Join-Path -Path ".\data" -ChildPath (Join-Path -Path $Track -ChildPath "raw_xml")
}

if (-not (Test-Path -LiteralPath $BannerlordRoot)) {
  throw "Bannerlord root not found: $BannerlordRoot"
}

$modulesRoot = Join-Path -Path $BannerlordRoot -ChildPath "Modules"
if (-not (Test-Path -LiteralPath $modulesRoot)) {
  throw "Bannerlord Modules folder not found: $modulesRoot"
}

$exportModules = [System.Collections.Generic.List[string]]::new()
foreach ($module in $Modules) { Add-Unique $exportModules $module }

$dlcCandidates = @("NavalDLC")
foreach ($candidate in $dlcCandidates) {
  $candidatePath = Join-Path -Path $modulesRoot -ChildPath $candidate
  if (Test-Path -LiteralPath $candidatePath) {
    Add-Unique $exportModules $candidate
  }
}
foreach ($module in $ExtraModules) { Add-Unique $exportModules $module }

$launcherModules = Get-SelectedLauncherModules $LauncherData
$effectiveLoadOrder = [System.Collections.Generic.List[string]]::new()
foreach ($module in $launcherModules) {
  if ($exportModules.Contains($module)) { Add-Unique $effectiveLoadOrder $module }
}
foreach ($module in $exportModules) { Add-Unique $effectiveLoadOrder $module }

New-Item -ItemType Directory -Force -Path $Destination | Out-Null
$exportedAt = [DateTime]::UtcNow.ToString("o")
$gameVersion = Get-ModuleVersion (Join-Path -Path $modulesRoot -ChildPath "Native")
$manifestRows = [System.Collections.Generic.List[object]]::new()
$moduleRows = [System.Collections.Generic.List[object]]::new()

foreach ($module in $exportModules) {
  $modulePath = Join-Path -Path $modulesRoot -ChildPath $module
  if (-not (Test-Path -LiteralPath $modulePath)) {
    Write-Warning "Module not found: $modulePath"
    continue
  }

  $targetModulePath = Join-Path -Path $Destination -ChildPath $module
  New-Item -ItemType Directory -Force -Path $targetModulePath | Out-Null

  $moduleXmlCount = 0
  Get-ChildItem -LiteralPath $modulePath -Recurse -File |
    Where-Object { @(".xml", ".xslt") -contains $_.Extension.ToLowerInvariant() } |
    Sort-Object FullName |
    ForEach-Object {
      $relativePath = $_.FullName.Substring($modulePath.Length).TrimStart([char[]]@([char]"\", [char]"/"))
      $targetPath = Join-Path -Path $targetModulePath -ChildPath $relativePath
      $targetDir = Split-Path -Path $targetPath -Parent

      New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
      Copy-Item -LiteralPath $_.FullName -Destination $targetPath -Force
      $copied = Get-Item -LiteralPath $targetPath
      $hash = Get-FileHash -LiteralPath $targetPath -Algorithm SHA256
      [void]$manifestRows.Add([pscustomobject]@{
        track = $Track
        exported_at = $exportedAt
        game_version = $gameVersion
        module = $module
        relative_path = $relativePath.Replace("\", "/")
        size_bytes = $copied.Length
        sha256 = $hash.Hash.ToLowerInvariant()
      })
      if ($_.Extension -ieq ".xml") {
        $moduleXmlCount++
      }
    }

  [void]$moduleRows.Add([pscustomobject]@{
    module = $module
    version = Get-ModuleVersion $modulePath
    load_order_index = $effectiveLoadOrder.IndexOf($module)
    xml_count = $moduleXmlCount
  })
}

$manifestPath = Join-Path -Path $Destination -ChildPath "manifest.csv"
$moduleManifestPath = Join-Path -Path $Destination -ChildPath "manifest_modules.csv"
$humanManifestPath = Join-Path -Path $Destination -ChildPath "MANIFEST.md"

$manifestRows | Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding UTF8
$moduleRows | Select-Object module, version, load_order_index | Export-Csv -LiteralPath $moduleManifestPath -NoTypeInformation -Encoding UTF8

$xmlFileCount = @($manifestRows | Where-Object { [System.IO.Path]::GetExtension($_.relative_path) -ieq ".xml" }).Count
$xsltFileCount = @($manifestRows | Where-Object { [System.IO.Path]::GetExtension($_.relative_path) -ieq ".xslt" }).Count
$loadOrderSource = if (-not [string]::IsNullOrWhiteSpace($LauncherData) -and (Test-Path -LiteralPath $LauncherData)) {
  $LauncherData
} else {
  "export module order (LauncherData.xml unavailable)"
}

$manifestLines = [System.Collections.Generic.List[string]]::new()
[void]$manifestLines.Add("# Bannerlord XML Snapshot")
[void]$manifestLines.Add("")
[void]$manifestLines.Add("- **Track:** ``$Track``")
[void]$manifestLines.Add("- **Exported at (UTC):** ``$exportedAt``")
[void]$manifestLines.Add("- **Game version:** ``$gameVersion``")
[void]$manifestLines.Add("- **Load-order source:** ``$loadOrderSource``")
[void]$manifestLines.Add("- **XML files:** $xmlFileCount")
[void]$manifestLines.Add("- **XSLT files:** $xsltFileCount")
[void]$manifestLines.Add("")
[void]$manifestLines.Add("| Load order | Module | Version | XML files |")
[void]$manifestLines.Add("|---:|---|---|---:|")
foreach ($row in ($moduleRows | Sort-Object load_order_index, module)) {
  [void]$manifestLines.Add("| $($row.load_order_index) | ``$($row.module)`` | ``$($row.version)`` | $($row.xml_count) |")
}
[void]$manifestLines.Add("")
[void]$manifestLines.Add("Raw XML/XSLT files are local-only. ``manifest.csv`` records file sizes and SHA-256 hashes for reproducibility.")
$manifestLines | Set-Content -LiteralPath $humanManifestPath -Encoding UTF8

$requiredManifests = @($humanManifestPath, $manifestPath, $moduleManifestPath)
$missingManifests = @($requiredManifests | Where-Object { -not (Test-Path -LiteralPath $_) })
if ($missingManifests.Count -gt 0) {
  throw "Snapshot is invalid because manifest generation failed: $($missingManifests -join ', ')"
}

Write-Host ""
Write-Host "Bannerlord XML Export Complete"
Write-Host "Track: $Track"
Write-Host "Destination: $Destination"
Write-Host "Modules: $($moduleRows.module -join ', ')"
Write-Host "XML files copied: $xmlFileCount"
Write-Host "XSLT files copied: $xsltFileCount"
Write-Host "Manifest: $humanManifestPath"
