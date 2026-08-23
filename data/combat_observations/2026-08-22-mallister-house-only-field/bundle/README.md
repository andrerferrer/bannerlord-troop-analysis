# Reconstructible normalized Phase 1 archive

`mallister_house_only_2026-08-22.tar.xz.base64.part-00` is the Base64 transport for the immutable normalized Phase 1 archive.

```bash
base64 --decode mallister_house_only_2026-08-22.tar.xz.base64.part-00 > mallister_house_only_2026-08-22.tar.xz
sha256sum mallister_house_only_2026-08-22.tar.xz
tar -xJf mallister_house_only_2026-08-22.tar.xz
```

Expected archive SHA-256: `6daf5fd4ca2aae1b0ed77da4c8e4bf8e5603a16929827dea0b7c4ed0b32d02a1`
Expected archive size: `8264` bytes

The archive contains 19 files: the manifest plus every normalized Phase 1 artifact. Raw PNGs are not included.
