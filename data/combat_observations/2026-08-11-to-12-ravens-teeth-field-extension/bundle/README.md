# Reconstruct normalized bundle

Archive SHA-256: `403814973c1cad3e4c5a84032806949c4fad5e613c43d2c8a9f5bcc567188fba`

```bash
cat ravens_teeth_field_extension_2026-08-11-to-12.tar.xz.base64.part-* | base64 --decode > ravens_teeth_field_extension_2026-08-11-to-12.tar.xz
sha256sum ravens_teeth_field_extension_2026-08-11-to-12.tar.xz
tar -xJf ravens_teeth_field_extension_2026-08-11-to-12.tar.xz
```

```powershell
$parts = Get-ChildItem 'ravens_teeth_field_extension_2026-08-11-to-12.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('ravens_teeth_field_extension_2026-08-11-to-12.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'ravens_teeth_field_extension_2026-08-11-to-12.tar.xz' -Algorithm SHA256
```
