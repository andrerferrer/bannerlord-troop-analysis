# Reconstruct Goldenheart Warrior field normalized bundle

Archive SHA-256: `b9b59cdd6547637b7dbf73ff66bef8370654df1dd3ecf7dd62cc48fe37577829`

```bash
cat goldenheart_field_2026-08-13.tar.xz.base64.part-* | base64 --decode > goldenheart_field_2026-08-13.tar.xz
sha256sum goldenheart_field_2026-08-13.tar.xz
tar -xJf goldenheart_field_2026-08-13.tar.xz
```

PowerShell:

```powershell
$parts = Get-ChildItem 'goldenheart_field_2026-08-13.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('goldenheart_field_2026-08-13.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'goldenheart_field_2026-08-13.tar.xz' -Algorithm SHA256
tar -xJf goldenheart_field_2026-08-13.tar.xz
```

The archive itself is ignored by Git. Its ordered Base64 representation is retained in this directory.
