# Reconstruct the normalized dataset bundle

The complete normalized dataset is stored as 11 ordered Base64 chunks because the connector could not upload the binary archive directly.

From this directory on Linux/macOS/WSL:

```bash
cat bannerlord_normalized_v1.tar.xz.base64.part-* \
  | base64 --decode \
  > bannerlord_normalized_v1.tar.xz

sha256sum bannerlord_normalized_v1.tar.xz
# expected: 10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa

tar -xJf bannerlord_normalized_v1.tar.xz
```

PowerShell:

```powershell
$parts = Get-ChildItem 'bannerlord_normalized_v1.tar.xz.base64.part-*' | Sort-Object Name
$base64 = ($parts | ForEach-Object { Get-Content $_ -Raw }) -join ''
[IO.File]::WriteAllBytes('bannerlord_normalized_v1.tar.xz', [Convert]::FromBase64String($base64))
Get-FileHash 'bannerlord_normalized_v1.tar.xz' -Algorithm SHA256
```

The archive contains the readable JSONL, CSV, JSON, schema, rankings, manifest, and review queue produced by the first-pass normalization.

The original 85 MB screenshot ZIP is not stored in normal Git history. Its SHA-256 and every individual screenshot hash are present in the normalized manifest.