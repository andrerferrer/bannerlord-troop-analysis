# Immutable Phase 2 bundle

Reconstruct and verify:

```bash
cat cerwyn_mixed_phase2.tar.xz.base64.part-* | base64 -d > /tmp/cerwyn_mixed_phase2.tar.xz
echo "43b206dd20c71fc528743d7fa2be179a2537e368912c58413363e18fb56c6262  /tmp/cerwyn_mixed_phase2.tar.xz" | sha256sum -c -
mkdir -p /tmp/cerwyn-phase2
tar -xJf /tmp/cerwyn_mixed_phase2.tar.xz -C /tmp/cerwyn-phase2
```

Archive SHA-256: `43b206dd20c71fc528743d7fa2be179a2537e368912c58413363e18fb56c6262`  
Archive bytes: `23636`  
Members: `30`

The bundle contains the reproducible generator, all Phase 2 outputs, and the validated queue transition.
