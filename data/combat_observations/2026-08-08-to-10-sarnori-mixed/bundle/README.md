# Reconstruct normalized Sarnori combat evidence

The deterministic tar.xz archive is stored as ordered Base64 parts.

Archive SHA-256: `54c5ed631540a13a59af5f799910b7253ad09d873b414e0776b1e64f25947bc1`

```bash
cat sarnori_combat_2026-08-08_to_10.tar.xz.base64.part-* | base64 --decode > sarnori_combat_2026-08-08_to_10.tar.xz
sha256sum sarnori_combat_2026-08-08_to_10.tar.xz
tar -xJf sarnori_combat_2026-08-08_to_10.tar.xz
```

```powershell
$parts = Get-ChildItem 'sarnori_combat_2026-08-08_to_10.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('sarnori_combat_2026-08-08_to_10.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'sarnori_combat_2026-08-08_to_10.tar.xz' -Algorithm SHA256
```
