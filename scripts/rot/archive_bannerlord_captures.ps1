param(
  [string[]]$SourceDirs = @(
    "$HOME\Pictures",
    "$HOME\Videos",
    "$HOME\Documents"
  ),
  [string]$DestinationRoot = "$HOME\Documents\bannerlord-capture-backups",
  [int]$DaysBack = 30,
  [switch]$IncludeAllMedia
)

$ErrorActionPreference = "Stop"

$extensions = @(
  ".png",
  ".jpg",
  ".jpeg",
  ".webp",
  ".mp4",
  ".mov",
  ".mkv"
)

$bannerlordPattern = "(?i)(Mount and Blade II Bannerlord|Armoury Crate SE|Bannerlord)"
$cutoff = (Get-Date).AddDays(-[Math]::Abs($DaysBack))
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$archiveName = "bannerlord_captures_$timestamp"
$archiveDir = Join-Path -Path $DestinationRoot -ChildPath $archiveName
$filesDir = Join-Path -Path $archiveDir -ChildPath "files"
$manifestPath = Join-Path -Path $archiveDir -ChildPath "capture_manifest.csv"
$summaryPath = Join-Path -Path $archiveDir -ChildPath "README_CAPTURE_ARCHIVE.txt"
$zipPath = Join-Path -Path $DestinationRoot -ChildPath "$archiveName.zip"

New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

Write-Host ""
Write-Host "===================================="
Write-Host " Bannerlord Capture Archive"
Write-Host "===================================="
Write-Host "Cutoff: $($cutoff.ToString('s'))"
Write-Host "Destination: $archiveDir"
Write-Host ""

$manifestRows = @()
$seenSources = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)

foreach ($sourceDirInput in $SourceDirs) {
  if ([string]::IsNullOrWhiteSpace($sourceDirInput)) {
    continue
  }

  $expandedSourceDir = [Environment]::ExpandEnvironmentVariables($sourceDirInput)

  if (-not (Test-Path -LiteralPath $expandedSourceDir)) {
    Write-Warning "Source directory not found, skipping: $expandedSourceDir"
    continue
  }

  $sourceDir = (Resolve-Path -LiteralPath $expandedSourceDir).Path.TrimEnd("\")
  $sourceLabel = Split-Path -Path $sourceDir -Leaf

  Write-Host "Scanning: $sourceDir"

  $candidates = Get-ChildItem -LiteralPath $sourceDir -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
      $extensions -contains $_.Extension.ToLowerInvariant() -and
      $_.LastWriteTime -ge $cutoff -and
      ($IncludeAllMedia -or $_.Name -match $bannerlordPattern)
    }

  foreach ($file in $candidates) {
    if (-not $seenSources.Add($file.FullName)) {
      continue
    }

    $relativePath = $file.FullName.Substring($sourceDir.Length).TrimStart("\")
    $targetPath = Join-Path -Path $filesDir -ChildPath (Join-Path -Path $sourceLabel -ChildPath $relativePath)
    $targetDir = Split-Path -Path $targetPath -Parent

    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    Copy-Item -LiteralPath $file.FullName -Destination $targetPath -Force

    $hash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash

    $manifestRows += [PSCustomObject]@{
      source_root = $sourceDir
      source_path = $file.FullName
      archive_relative_path = $targetPath.Substring($archiveDir.Length).TrimStart("\")
      extension = $file.Extension.ToLowerInvariant()
      bytes = $file.Length
      last_write_time = $file.LastWriteTime.ToString("s")
      sha256 = $hash
    }
  }
}

if ($manifestRows.Count -eq 0) {
  Remove-Item -LiteralPath $archiveDir -Recurse -Force
  throw "No matching Bannerlord captures found. Pass the exact folder with -SourceDirs or use -IncludeAllMedia."
}

$manifestRows |
  Sort-Object last_write_time, source_path |
  Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding UTF8

$imageCount = ($manifestRows | Where-Object { $_.extension -in @('.png', '.jpg', '.jpeg', '.webp') } | Measure-Object).Count
$videoCount = ($manifestRows | Where-Object { $_.extension -in @('.mp4', '.mov', '.mkv') } | Measure-Object).Count
$totalBytes = ($manifestRows | Measure-Object -Property bytes -Sum).Sum

$summary = @"
Bannerlord capture archive
Generated: $(Get-Date -Format s)
Cutoff: $($cutoff.ToString('s'))
Files: $($manifestRows.Count)
Images: $imageCount
Videos: $videoCount
Total bytes: $totalBytes

Source directories:
$($SourceDirs -join "`r`n")

This archive is copy-only. Original files were not deleted or moved.
Upload the generated ZIP to the RoT analysis chat before deleting local captures.
"@

$summary | Out-File -LiteralPath $summaryPath -Encoding UTF8

if (Test-Path -LiteralPath $zipPath) {
  Remove-Item -LiteralPath $zipPath -Force
}

Compress-Archive -Path (Join-Path -Path $archiveDir -ChildPath "*") -DestinationPath $zipPath -Force

if (-not (Test-Path -LiteralPath $zipPath)) {
  throw "ZIP creation failed: $zipPath"
}

$zipSize = (Get-Item -LiteralPath $zipPath).Length

Write-Host ""
Write-Host "Archive complete."
Write-Host "Files: $($manifestRows.Count)"
Write-Host "Images: $imageCount"
Write-Host "Videos: $videoCount"
Write-Host "ZIP size: $zipSize bytes"
Write-Host "ZIP: $zipPath"
Write-Host ""
Write-Host "Original captures were not deleted."
