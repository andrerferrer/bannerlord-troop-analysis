# Reconstruct Stark Sworn Sword mixed normalized bundle

Archive SHA-256: `d94a770ddcabeb24eda965fd289dcb1d91c2a4b0ed945322cd0b825057a5bb6e`

The ordered Base64 representation is retained as
`stark_sworn_mixed_2026-08-21.tar.xz.base64.part-00`.

```bash
base64 --decode stark_sworn_mixed_2026-08-21.tar.xz.base64.part-00 > stark_sworn_mixed_2026-08-21.tar.xz
printf '%s  %s\n' 'd94a770ddcabeb24eda965fd289dcb1d91c2a4b0ed945322cd0b825057a5bb6e' 'stark_sworn_mixed_2026-08-21.tar.xz' | sha256sum --check
mkdir -p reconstructed
tar -xJf stark_sworn_mixed_2026-08-21.tar.xz -C reconstructed
```

PowerShell:

```powershell
$base64 = Get-Content 'stark_sworn_mixed_2026-08-21.tar.xz.base64.part-00' -Raw
[IO.File]::WriteAllBytes('stark_sworn_mixed_2026-08-21.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'stark_sworn_mixed_2026-08-21.tar.xz' -Algorithm SHA256
New-Item -ItemType Directory -Force 'reconstructed' | Out-Null
tar -xJf 'stark_sworn_mixed_2026-08-21.tar.xz' -C 'reconstructed'
```

After extraction, verify every file against
`stark_sworn_mixed_2026-08-21/artifact_hashes.csv`. The binary archive itself
is ignored by Git; the Base64 part is the deterministic repository-addressable
representation.
