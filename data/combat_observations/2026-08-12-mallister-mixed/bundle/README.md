# Reconstruct Mallister mixed-context normalized bundle

Archive SHA-256: `97db4b82f1d1b146d43c3f3afc421cb4594c2960bd418a045f70c2a0685758e7`

```bash
cat mallister_combat_2026-08-12.tar.xz.base64.part-* | base64 --decode > mallister_combat_2026-08-12.tar.xz
sha256sum mallister_combat_2026-08-12.tar.xz
tar -xJf mallister_combat_2026-08-12.tar.xz
```

PowerShell:

```powershell
$parts = Get-ChildItem 'mallister_combat_2026-08-12.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('mallister_combat_2026-08-12.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'mallister_combat_2026-08-12.tar.xz' -Algorithm SHA256
tar -xJf mallister_combat_2026-08-12.tar.xz
```

The archive itself is ignored by Git. Its ordered Base64 representation is retained in this directory.
