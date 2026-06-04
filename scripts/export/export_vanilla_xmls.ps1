param(
  [string]$BannerlordRoot = "C:\Program Files (x86)\Steam\steamapps\common\Mount & Blade II Bannerlord",
  [string]$Destination = ".\data\vanilla\raw_xml"
)

$ErrorActionPreference = "Stop"

$modules = @(
  "Native",
  "Sandbox",
  "SandboxCore",
  "StoryMode"
)

if (-not (Test-Path $BannerlordRoot)) {
  throw "Bannerlord root not found: $BannerlordRoot"
}

$modulesRoot = Join-Path -Path $BannerlordRoot -ChildPath "Modules"

if (-not (Test-Path $modulesRoot)) {
  throw "Bannerlord Modules folder not found: $modulesRoot"
}

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

foreach ($module in $modules) {
  $modulePath = Join-Path -Path $modulesRoot -ChildPath $module

  if (-not (Test-Path $modulePath)) {
    Write-Warning "Module not found: $modulePath"
    continue
  }

  $targetModulePath = Join-Path -Path $Destination -ChildPath $module
  New-Item -ItemType Directory -Force -Path $targetModulePath | Out-Null

  Get-ChildItem -Path $modulePath -Recurse -Filter "*.xml" | ForEach-Object {
    $relativePath = $_.FullName.Substring($modulePath.Length).TrimStart("\")
    $targetPath = Join-Path -Path $targetModulePath -ChildPath $relativePath
    $targetDir = Split-Path -Path $targetPath -Parent

    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    Copy-Item -Path $_.FullName -Destination $targetPath -Force
  }
}

Write-Host ""
Write-Host "Vanilla XML Export Complete"
Write-Host "Destination: $Destination"

$count = Get-ChildItem $Destination -Recurse -Filter "*.xml" | Measure-Object
Write-Host "XML files copied: $($count.Count)"
