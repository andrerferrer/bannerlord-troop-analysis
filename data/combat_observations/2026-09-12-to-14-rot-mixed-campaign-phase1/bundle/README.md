# Deterministic normalized Phase 1 bundle

The Base64 file reconstructs `rot_mixed_campaign_phase1.tar.xz` with 11 members. Raw PNG bytes are not included.

From this batch directory:

```bash
BATCH_DIR=$PWD
OUT=$(mktemp -d)
base64 --decode < bundle/rot_mixed_campaign_phase1.tar.xz.base64 > /tmp/rot_mixed_campaign_phase1.tar.xz
echo '99754ec7fb614e86631bd6268c327140cd7c7882db7f612035015a6291b3adab  /tmp/rot_mixed_campaign_phase1.tar.xz' | sha256sum -c -
tar -xJf /tmp/rot_mixed_campaign_phase1.tar.xz -C "$OUT"
(cd "$OUT" && sha256sum -c "$BATCH_DIR/bundle/rot_mixed_campaign_phase1.members.sha256")
```

- Archive SHA-256: `99754ec7fb614e86631bd6268c327140cd7c7882db7f612035015a6291b3adab`
- Archive size: `12944` bytes
- Base64 text SHA-256: `1fe97af8dd1979f02e4c27b7e26277a80e8bde026ebc6e50d8b989adb24692d6`
- Base64 text size: `17261` bytes
- Archive member count: `11`

To verify that the checked-in archive is a deterministic rebuild of the retained Phase 1 evidence and metadata:

```bash
python3 source/rebuild_phase1_bundle.py --check
```
