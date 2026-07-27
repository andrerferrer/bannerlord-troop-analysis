# Reconstruct the 2026-07-27 normalized combat batch

The complete normalized dataset is stored as ordered Base64 chunks because the GitHub connector cannot upload the binary archive directly.

## Linux, macOS, or WSL

```bash
cat bannerlord_combat_normalized_2026-07-27.tar.xz.base64.part-* \
  | base64 --decode \
  > bannerlord_combat_normalized_2026-07-27.tar.xz

sha256sum bannerlord_combat_normalized_2026-07-27.tar.xz
# expected: 1beafb3568fd2fb78d22ef9b9a27b20031019f4f8c2f02aa612f0c72f8e03fc1

tar -xJf bannerlord_combat_normalized_2026-07-27.tar.xz
```

## PowerShell

```powershell
$parts = Get-ChildItem 'bannerlord_combat_normalized_2026-07-27.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes(
  'bannerlord_combat_normalized_2026-07-27.tar.xz',
  [Convert]::FromBase64String($base64)
)
Get-FileHash 'bannerlord_combat_normalized_2026-07-27.tar.xz' -Algorithm SHA256
```

The archive contains the readable JSONL, CSV, JSON, reports, source manifest, review queue, and artifact hashes for this batch. Raw screenshots are intentionally excluded from ordinary Git history; their SHA-256 values are preserved in `screenshots_manifest.csv`.
