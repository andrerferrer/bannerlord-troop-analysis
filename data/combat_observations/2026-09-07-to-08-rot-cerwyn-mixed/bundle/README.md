# Immutable Phase 1 normalized bundle

Reconstruct and verify:

```bash
cat cerwyn_mixed_phase1.tar.xz.base64.part-* | base64 -d > /tmp/cerwyn_mixed_phase1.tar.xz
echo "d780a64dbfbcde1ac8e82428b2a86fceea2922f0584c42ef64a8eddd309f3439  /tmp/cerwyn_mixed_phase1.tar.xz" | sha256sum -c -
mkdir -p /tmp/cerwyn-phase1
tar -xJf /tmp/cerwyn_mixed_phase1.tar.xz -C /tmp/cerwyn-phase1
```

Archive SHA-256: `d780a64dbfbcde1ac8e82428b2a86fceea2922f0584c42ef64a8eddd309f3439`  
Archive bytes: `25272`  
Members: `22`

The archive is the immutable Phase 1 analysis input. It contains normalized canonical records, reviewed decisions, validation reports, source inventory/provenance, and the Phase 2 handoff. It intentionally excludes the raw 48 MB screenshot ZIP.
