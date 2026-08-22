# Reconstructible normalized bundle

The six `mallister_eagle_knight_dedicated_2026-08-22.tar.xz.base64.part-*` files are the Base64 transport for the deterministic normalized archive.

Reconstruct:

```bash
cat mallister_eagle_knight_dedicated_2026-08-22.tar.xz.base64.part-* | base64 --decode > mallister_eagle_knight_dedicated_2026-08-22.tar.xz
sha256sum mallister_eagle_knight_dedicated_2026-08-22.tar.xz
tar -xJf mallister_eagle_knight_dedicated_2026-08-22.tar.xz
```

Expected archive SHA-256: `bd412e00e0033b56a0bfa4fd2b31ad185c62bafa87ec19bc5bcdd4d99c587ded`
Expected archive size: `21988` bytes

The archive contains 56 normalized, reviewed, canonical, report, analysis, and validation files. Raw PNGs are not included.
