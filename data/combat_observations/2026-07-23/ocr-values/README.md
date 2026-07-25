# Published OCR values — 2026-07-23 screenshot batch

This directory publishes the core OCR table extracted from all 60 Bannerlord screenshots.

## Coverage

- OCR/extracted rows: **1,541**
- Source screenshots: **60**
- Grouped battle/screen sets: **48**
- CSV rows include troop/party/hero/artifact rows; use `row_type`, `analysis_status`, and `needs_review` when filtering.

## Columns

`battle_id`, `screenshot_id`, `side`, `relationship_to_player`, `parent_group`, `row_type`, `display_name_raw`, `canonical_troop_id`, `survivors`, `kills`, `upgrade_ready`, `deaths`, `wounded`, `routed`, `deployed`, `analysis_status`, `exclusion_reason`, `needs_review`, `confidence`.

This compact publication contains the normalized OCR values and row-level confidence/status. The immutable first-pass JSONL with per-cell raw OCR evidence remains in the locally verified full archive and is still a follow-up publication task.

## Reconstruct

### Bash / Linux / macOS / WSL

```bash
cat ocr_values.csv.xz.part-* > ocr_values.csv.xz
sha256sum ocr_values.csv.xz
xz -dk ocr_values.csv.xz
sha256sum ocr_values.csv
```

### PowerShell

```powershell
$parts = Get-ChildItem 'ocr_values.csv.xz.part-*' | Sort-Object Name
$out = [IO.File]::Create('ocr_values.csv.xz')
try {
  foreach ($part in $parts) {
    $bytes = [IO.File]::ReadAllBytes($part.FullName)
    $out.Write($bytes, 0, $bytes.Length)
  }
} finally {
  $out.Dispose()
}
Get-FileHash 'ocr_values.csv.xz' -Algorithm SHA256
xz -dk 'ocr_values.csv.xz'
Get-FileHash 'ocr_values.csv' -Algorithm SHA256
```

Expected hashes:

```text
ocr_values.csv.xz  7c670b37aa6d04982421184a10f0002f4f46e909d7971c6fa14c455f379a3a78
ocr_values.csv     bd822556306927d35d33280fceb12933125a5300592bbcae435ff45ca0db9ae1
```

Verify individual part hashes with `OCR_VALUES_MANIFEST.sha256` before reconstruction.
