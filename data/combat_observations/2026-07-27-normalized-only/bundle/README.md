# Reconstruct the normalized-only 2026-07-27 combat batch

The complete normalized evidence bundle is stored as ordered Base64 chunks because the GitHub connector cannot upload the binary archive directly.

This archive contains normalized records only. It intentionally excludes rankings, historical aggregates, model comparisons, and analytical conclusions.

## Linux, macOS, or WSL

```bash
cat bannerlord_combat_normalized_only_2026-07-27.tar.xz.base64.part-* \
  | base64 --decode \
  > bannerlord_combat_normalized_only_2026-07-27.tar.xz

sha256sum bannerlord_combat_normalized_only_2026-07-27.tar.xz
# expected: 031a7c60d4ed239a2fcb70a81bb6edf047711c3a422ee3ba4420c4a4af534855

tar -xJf bannerlord_combat_normalized_only_2026-07-27.tar.xz
```

## PowerShell

```powershell
$parts = Get-ChildItem 'bannerlord_combat_normalized_only_2026-07-27.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes(
  'bannerlord_combat_normalized_only_2026-07-27.tar.xz',
  [Convert]::FromBase64String($base64)
)
Get-FileHash 'bannerlord_combat_normalized_only_2026-07-27.tar.xz' -Algorithm SHA256
```

The source screenshots are not present in this archive. Their individual SHA-256 hashes are retained in `screenshots_manifest.csv`.
