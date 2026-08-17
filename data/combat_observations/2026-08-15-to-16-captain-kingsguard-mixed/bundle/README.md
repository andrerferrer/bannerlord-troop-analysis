# Reconstruct Captain of the Kingsguard mixed normalized bundle

Archive SHA-256: `6b16d78d32ca70ea5093431874d8a73b00e6a3b961fa2686ec8701659decbc4d`

```bash
cat captain_kingsguard_mixed_2026-08-15_to_16.tar.xz.base64.part-* | base64 --decode > captain_kingsguard_mixed_2026-08-15_to_16.tar.xz
sha256sum captain_kingsguard_mixed_2026-08-15_to_16.tar.xz
tar -xJf captain_kingsguard_mixed_2026-08-15_to_16.tar.xz
```

PowerShell:

```powershell
$parts = Get-ChildItem 'captain_kingsguard_mixed_2026-08-15_to_16.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('captain_kingsguard_mixed_2026-08-15_to_16.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'captain_kingsguard_mixed_2026-08-15_to_16.tar.xz' -Algorithm SHA256
tar -xJf captain_kingsguard_mixed_2026-08-15_to_16.tar.xz
```

The binary archive itself is ignored by Git. Its ordered Base64 representation is retained in this directory.
