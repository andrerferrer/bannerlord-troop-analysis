param(
  [string]$Baseline = ".\analysis\empirical\2026-07-23\baseline_strict_player_side.csv",
  [string]$ExistingAudit = ".\analysis\empirical\2026-07-23\canonical_identity_audit.csv",
  [string]$Output = ".\analysis\empirical\2026-07-23\canonical_identity_audit.generated.csv",
  [string]$Report = ".\analysis\empirical\2026-07-23\canonical_identity_resolution_report.json",
  [string[]]$TrackAudits = @(),
  [switch]$RequireComplete
)

$ErrorActionPreference = "Stop"

function Find-Python {
  foreach ($candidate in @(".venv\Scripts\python.exe", "python", "py")) {
    try {
      if ($candidate -eq "py") {
        & py -3 --version *> $null
        if ($LASTEXITCODE -eq 0) { return "py -3" }
      } else {
        & $candidate --version *> $null
        if ($LASTEXITCODE -eq 0) { return $candidate }
      }
    } catch { continue }
  }
  throw "Python 3 not found."
}

function Invoke-Python([string]$PythonCommand, [string[]]$Arguments) {
  if ($PythonCommand -eq "py -3") { & py -3 @Arguments } else { & $PythonCommand @Arguments }
  if ($LASTEXITCODE -ne 0) { throw "Canonical identity command failed with exit code $LASTEXITCODE." }
}

$script = Join-Path $PSScriptRoot "analysis\build_canonical_identity_audit.py"
if (-not (Test-Path -LiteralPath $script)) { throw "Missing script: $script" }
if (-not (Test-Path -LiteralPath $Baseline)) { throw "Missing baseline: $Baseline" }

$argsList = @($script, $Baseline, $Output, "--report", $Report)
if (-not [string]::IsNullOrWhiteSpace($ExistingAudit) -and (Test-Path -LiteralPath $ExistingAudit)) {
  $argsList += @("--existing-audit", $ExistingAudit)
}
foreach ($spec in $TrackAudits) { $argsList += @("--track-audit", $spec) }
if ($RequireComplete) { $argsList += "--require-complete" }

$python = Find-Python
Invoke-Python $python $argsList
Write-Host "Canonical identity audit: $Output"
Write-Host "Resolution report: $Report"
