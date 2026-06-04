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

New-Item -ItemType Directory -Force -Path $Destination | Out-Null

foreach ($module in $modules) {
  $modulePath = Join-Path $BannerlordRoot "Modules\$module"

  if (-not (Test-Path $modulePath)) {
    Write-Warning "Module not found: $modulePath"
    continue
  }

  $targetModulePath = Join-Path $Destination $module
  New-Item -ItemType Directory -Force -Path $targetModulePath | Out-Null

  Get-ChildItem -Path $modulePath -Recurse -Filter "*.xml" | ForEach-Object {
    $relativePath = $_.FullName.Substring($modulePath.Length).TrimStart("\")
    $targetPath = Join-Path $targetModulePath $relativePath
    $targetDir = Split-Path $targetPath -Parent

    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    Copy-Item $_.FullName $targetPath -Force
  }
}

Write-Host "Vanilla XML export complete."
Write-Host "Destination: $Destination"
