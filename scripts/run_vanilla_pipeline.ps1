param(
  [string]$BannerlordRoot = "C:\Program Files (x86)\Steam\steamapps\common\Mount & Blade II Bannerlord",
  [string]$ProjectRoot = ".",
  [string]$RawXmlDir = "data\vanilla\raw_xml",
  [string]$AuditOutputDir = "data\vanilla\audit",
  [string]$RoleScoreOutputDir = "data\vanilla\role_scores",
  [switch]$SkipExport,
  [switch]$SkipAudit,
  [switch]$SkipRoleScores,
  [switch]$SetupVenv,
  [switch]$ZipOutputs
)

$ErrorActionPreference = "Stop"

function Resolve-ProjectPath([string]$Path) {
  if ([System.IO.Path]::IsPathRooted($Path)) {
    return $Path
  }

  return Join-Path -Path $ProjectRoot -ChildPath $Path
}

function Find-Python {
  $candidates = @(
    ".venv\Scripts\python.exe",
    "python",
    "py"
  )

  foreach ($candidate in $candidates) {
    try {
      if ($candidate -eq "py") {
        & py -3 --version *> $null
        if ($LASTEXITCODE -eq 0) { return "py -3" }
      } else {
        & $candidate --version *> $null
        if ($LASTEXITCODE -eq 0) { return $candidate }
      }
    } catch {
      continue
    }
  }

  throw "Python 3 not found. Install Python 3.10+ and rerun."
}

function Invoke-PythonCommand([string]$PythonCommand, [string[]]$Arguments) {
  if ($PythonCommand -eq "py -3") {
    & py -3 @Arguments
  } else {
    & $PythonCommand @Arguments
  }

  if ($LASTEXITCODE -ne 0) {
    throw "Python command failed: $PythonCommand $($Arguments -join ' ')"
  }
}

$ProjectRoot = Resolve-Path $ProjectRoot
$RawXmlPath = Resolve-ProjectPath $RawXmlDir
$AuditOutputPath = Resolve-ProjectPath $AuditOutputDir
$RoleScoreOutputPath = Resolve-ProjectPath $RoleScoreOutputDir

Write-Host ""
Write-Host "===================================="
Write-Host " Bannerlord Vanilla Troop Pipeline"
Write-Host "===================================="
Write-Host "ProjectRoot: $ProjectRoot"
Write-Host "BannerlordRoot: $BannerlordRoot"
Write-Host "RawXmlDir: $RawXmlPath"
Write-Host "AuditOutputDir: $AuditOutputPath"
Write-Host "RoleScoreOutputDir: $RoleScoreOutputPath"
Write-Host ""

if (-not $SkipExport) {
  $exportScript = Join-Path $ProjectRoot "scripts\export\export_vanilla_xmls.ps1"

  if (-not (Test-Path $exportScript)) {
    throw "Missing export script: $exportScript"
  }

  Write-Host "[1/3] Exporting vanilla XMLs..."
  & $exportScript -BannerlordRoot $BannerlordRoot -Destination $RawXmlPath

  if ($LASTEXITCODE -ne 0) {
    throw "XML export failed."
  }
} else {
  Write-Host "[1/3] Skipping XML export."
}

if ($SetupVenv) {
  Write-Host "Setting up Python virtual environment..."
  $pythonBootstrap = Find-Python
  Invoke-PythonCommand $pythonBootstrap @("-m", "venv", ".venv")
  $python = ".venv\Scripts\python.exe"
  Invoke-PythonCommand $python @("-m", "pip", "install", "--upgrade", "pip")
  Invoke-PythonCommand $python @("-m", "pip", "install", "pandas", "numpy")
} else {
  $python = Find-Python
}

Write-Host "Python: $python"

if (-not $SkipAudit) {
  $auditScript = Join-Path $ProjectRoot "scripts\normalization\rebuild_vanilla_audit.py"

  if (-not (Test-Path $auditScript)) {
    throw "Missing audit script: $auditScript"
  }

  Write-Host "[2/3] Rebuilding audit datasets..."
  Invoke-PythonCommand $python @(
    $auditScript,
    "--raw-xml-root", $RawXmlPath,
    "--output-dir", $AuditOutputPath
  )
} else {
  Write-Host "[2/3] Skipping audit rebuild."
}

if (-not $SkipRoleScores) {
  $roleScoreScript = Join-Path $ProjectRoot "scripts\scoring\generate_vanilla_role_scores.py"

  if (Test-Path $roleScoreScript) {
    Write-Host "[3/3] Generating role scores..."
    Invoke-PythonCommand $python @(
      $roleScoreScript,
      "--audit-dir", $AuditOutputPath,
      "--output-dir", $RoleScoreOutputPath
    )
  } else {
    Write-Warning "Role score script not found yet: $roleScoreScript"
    Write-Warning "Audit datasets were generated. Role scores can be generated after adding scripts\scoring\generate_vanilla_role_scores.py."
  }
} else {
  Write-Host "[3/3] Skipping role scores."
}

if ($ZipOutputs) {
  Write-Host "Creating output ZIPs..."

  $auditZip = Join-Path $ProjectRoot "vanilla_audit_output.zip"
  $roleZip = Join-Path $ProjectRoot "vanilla_role_scores_output.zip"

  if (Test-Path $auditZip) { Remove-Item $auditZip -Force }
  if (Test-Path $roleZip) { Remove-Item $roleZip -Force }

  if (Test-Path $AuditOutputPath) {
    Compress-Archive -Path (Join-Path $AuditOutputPath "*") -DestinationPath $auditZip -Force
    Write-Host "Audit ZIP: $auditZip"
  }

  if (Test-Path $RoleScoreOutputPath) {
    Compress-Archive -Path (Join-Path $RoleScoreOutputPath "*") -DestinationPath $roleZip -Force
    Write-Host "Role scores ZIP: $roleZip"
  }
}

Write-Host ""
Write-Host "Pipeline complete."
Write-Host ""
Write-Host "Key outputs:"
Write-Host "  $AuditOutputPath\vanilla_sanity_check_table.csv"
Write-Host "  $AuditOutputPath\vanilla_roster_audit_summary.csv"
Write-Host "  $AuditOutputPath\vanilla_troop_equipment_audit.csv"
Write-Host ""
