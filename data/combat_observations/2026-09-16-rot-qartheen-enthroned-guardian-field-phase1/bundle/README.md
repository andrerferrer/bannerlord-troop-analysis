# Deterministic normalized Phase 1 bundle

`rot_qartheen_enthroned_guardian_field_phase1.tar.xz.base64` reconstructs `rot_qartheen_enthroned_guardian_field_phase1.tar.xz` with **15** members. Raw PNG bytes are not included.

From this batch directory:

```bash
base64 --decode < bundle/rot_qartheen_enthroned_guardian_field_phase1.tar.xz.base64 > /tmp/rot_qartheen_enthroned_guardian_field_phase1.tar.xz
echo "ae7c7998ae73a5f9adc358550644813770280512b05f06e0b79418d3dff78f0b  /tmp/rot_qartheen_enthroned_guardian_field_phase1.tar.xz" | sha256sum -c -
OUT=$(mktemp -d)
tar -xJf /tmp/rot_qartheen_enthroned_guardian_field_phase1.tar.xz -C "$OUT"
(cd "$OUT" && sha256sum -c "$OLDPWD/bundle/rot_qartheen_enthroned_guardian_field_phase1.members.sha256")
```

PowerShell:

```powershell
$raw = [Convert]::FromBase64String((Get-Content bundle/rot_qartheen_enthroned_guardian_field_phase1.tar.xz.base64 -Raw))
[IO.File]::WriteAllBytes("$env:TEMP\rot_qartheen_enthroned_guardian_field_phase1.tar.xz", $raw)
(Get-FileHash "$env:TEMP\rot_qartheen_enthroned_guardian_field_phase1.tar.xz" -Algorithm SHA256).Hash.ToLower()
```

Expected archive SHA-256: `ae7c7998ae73a5f9adc358550644813770280512b05f06e0b79418d3dff78f0b`  
Expected archive size: `8732` bytes  
Expected Base64 text SHA-256: `d250d3caddee132d3e1fa80b03162498f77a698f78acb05a9b150c016241743c`  
Expected Base64 text size: `11798` bytes

Run the deterministic repository check:

```bash
python3 source/rebuild_phase1_bundle.py --check
```
