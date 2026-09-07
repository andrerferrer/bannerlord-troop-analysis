# Deterministic normalized Phase 1 bundle

Payload SHA-256: `9cc8482caf6d37356b186c0a68dfa9e6f50303fb715f6ddfc3a49e2593b59c9d`

From this batch directory:

```bash
ARCHIVE=/tmp/2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts-normalized-phase1.tar.xz
OUT=/tmp/2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts-normalized-phase1
cat bundle/2026-08-29-to-09-05-rot-white-harbor-and-joffrey-cohorts-normalized-phase1.tar.xz.base64.part-* \
  | base64 -d > "$ARCHIVE"
echo '9cc8482caf6d37356b186c0a68dfa9e6f50303fb715f6ddfc3a49e2593b59c9d  '"$ARCHIVE" \
  | sha256sum -c -
mkdir -p "$OUT"
tar -xJf "$ARCHIVE" -C "$OUT"
```

The archive contains the normalization records, direct manifests, review queues, validation report, and the original Phase 1 handoff snapshot. The repository-level `handoff/ANALYSIS_PROMPT.md` is the authoritative current handoff.
