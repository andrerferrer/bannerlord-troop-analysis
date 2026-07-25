# Reconstruct the normalized dataset bundle

The complete normalized dataset is stored as 11 ordered Base64 chunks because the connector could not upload the binary archive directly.

The historical shell command below is retained only to explain the original format. **Do not use successful decoding or tar opening as the integrity gate.** The current committed parts are corrupt and include intermediate padding/overlap.

Use the repository CLI from the repository root on macOS, Linux, or Windows:

```bash
python3 -m scripts.combat_observations reconstruct-bundle \
  --bundle-dir data/combat_observations/2026-07-23/bundle \
  --archive data/combat_observations/2026-07-23/bundle/bannerlord_normalized_v1.tar.xz \
  --extract-dir data/combat_observations/2026-07-23/bundle/reconstructed \
  --report data/combat_observations/2026-07-23/reports/p0_verification_report.json \
  --forensic-report data/combat_observations/2026-07-23/reports/p0_bundle_forensics.json
```

It requires the exact SHA-256, inspects the tar safely before extraction, rejects traversal/links, parses every required data file, and reconciles recorded counts.

Historical Linux/macOS/WSL command (known to fail on the current parts):

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
