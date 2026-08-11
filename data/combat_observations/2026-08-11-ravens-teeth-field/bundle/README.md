# Reconstruct Ravens' Teeth field normalized bundle

Archive SHA-256: `78a6f3a80ea8351e847555b44f2e7f01c2b4db3d4b772a5af716dd5eedcebcb8`

```bash
cat ravens_teeth_field_2026-08-11.tar.xz.base64.part-* | base64 --decode > ravens_teeth_field_2026-08-11.tar.xz
sha256sum ravens_teeth_field_2026-08-11.tar.xz
tar -xJf ravens_teeth_field_2026-08-11.tar.xz
```

PowerShell:

```powershell
$parts = Get-ChildItem 'ravens_teeth_field_2026-08-11.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('ravens_teeth_field_2026-08-11.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'ravens_teeth_field_2026-08-11.tar.xz' -Algorithm SHA256
```
