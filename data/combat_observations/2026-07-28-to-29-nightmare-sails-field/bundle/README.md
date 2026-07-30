# Reconstruct Nightmare Sails field batch — 2026-07-28 to 2026-07-29 normalized bundle

The deterministic normalized evidence archive is stored as ordered Base64 chunks. Raw screenshots are not retained in Git history; their filenames and SHA-256 hashes are recorded in `screenshots_manifest.csv`.

```bash
cat bannerlord_combat_normalized_nightmare_sails_b03_b11.tar.xz.base64.part-* | base64 --decode > bannerlord_combat_normalized_nightmare_sails_b03_b11.tar.xz
sha256sum bannerlord_combat_normalized_nightmare_sails_b03_b11.tar.xz
# expected: 67faffdb8dd882299c97d289136338d9c79fd33ce07c0b11db261514454facde
tar -xJf bannerlord_combat_normalized_nightmare_sails_b03_b11.tar.xz
```

PowerShell:

```powershell
$parts = Get-ChildItem 'bannerlord_combat_normalized_nightmare_sails_b03_b11.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('bannerlord_combat_normalized_nightmare_sails_b03_b11.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'bannerlord_combat_normalized_nightmare_sails_b03_b11.tar.xz' -Algorithm SHA256
```
