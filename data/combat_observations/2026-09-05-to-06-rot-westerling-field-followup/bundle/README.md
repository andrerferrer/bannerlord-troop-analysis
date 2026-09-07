# Deterministic normalized Phase 1 bundle

Payload SHA-256: `1ba4c3c28db029bda23f57a6c830c0d57107b9a6e89dd1b1258a70514f56222a`

From this batch directory:

```bash
ARCHIVE=/tmp/2026-09-05-to-06-rot-westerling-field-followup-normalized-phase1.tar.xz
OUT=/tmp/2026-09-05-to-06-rot-westerling-field-followup-normalized-phase1
cat bundle/2026-09-05-to-06-rot-westerling-field-followup-normalized-phase1.tar.xz.base64.part-* \
  | base64 -d > "$ARCHIVE"
echo '1ba4c3c28db029bda23f57a6c830c0d57107b9a6e89dd1b1258a70514f56222a  '"$ARCHIVE" \
  | sha256sum -c -
mkdir -p "$OUT"
tar -xJf "$ARCHIVE" -C "$OUT"
```

The archive contains the normalization records, direct manifests, review queues, validation report, and the original Phase 1 handoff snapshot. The repository-level `handoff/ANALYSIS_PROMPT.md` is the authoritative current handoff.
