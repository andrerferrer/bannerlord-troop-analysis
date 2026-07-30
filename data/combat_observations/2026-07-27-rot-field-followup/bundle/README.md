# Reconstruct Realm of Thrones field follow-up — 2026-07-27 normalized bundle

The deterministic normalized evidence archive is stored as ordered Base64 chunks. Raw screenshots are not retained in Git history; their filenames and SHA-256 hashes are recorded in `screenshots_manifest.csv`.

```bash
cat bannerlord_combat_normalized_rot_b01_b02.tar.xz.base64.part-* | base64 --decode > bannerlord_combat_normalized_rot_b01_b02.tar.xz
sha256sum bannerlord_combat_normalized_rot_b01_b02.tar.xz
# expected: 70abe0385130a6d96aa9c594b08edc9bfa528bfdddeedd94c92dcf1d9de940ce
tar -xJf bannerlord_combat_normalized_rot_b01_b02.tar.xz
```

PowerShell:

```powershell
$parts = Get-ChildItem 'bannerlord_combat_normalized_rot_b01_b02.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('bannerlord_combat_normalized_rot_b01_b02.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'bannerlord_combat_normalized_rot_b01_b02.tar.xz' -Algorithm SHA256
```
