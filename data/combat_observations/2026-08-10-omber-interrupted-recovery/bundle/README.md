# Reconstruct Omber interrupted recovery normalized bundle

Archive SHA-256: `03ff1f4006603b424e5c4c3fc4b3955f5464bb5ed8489819b59a8c44c1e25774`

```bash
base64 --decode omber_interrupted_recovery_2026-08-10.tar.xz.base64.part-00 > omber_interrupted_recovery_2026-08-10.tar.xz
sha256sum omber_interrupted_recovery_2026-08-10.tar.xz
tar -xJf omber_interrupted_recovery_2026-08-10.tar.xz
```

PowerShell:

```powershell
$base64 = Get-Content 'omber_interrupted_recovery_2026-08-10.tar.xz.base64.part-00' -Raw
[IO.File]::WriteAllBytes('omber_interrupted_recovery_2026-08-10.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'omber_interrupted_recovery_2026-08-10.tar.xz' -Algorithm SHA256
tar -xJf omber_interrupted_recovery_2026-08-10.tar.xz
```

The binary archive itself is ignored by Git. Its ordered Base64 representation is retained here.
