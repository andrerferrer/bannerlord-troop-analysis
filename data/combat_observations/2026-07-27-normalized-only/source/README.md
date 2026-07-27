# Source evidence — 2026-07-27 combat batch

The original evidence is one ZIP archive containing 13 PNG screenshots.

## Required original file

```text
Filename:
Mount and Blade II Bannerlord - Singleplayer PID_ 6076 -  Win64_Shipping_Client Msvc14 Managed C__Program Files (x86)_Steam_steamapps_common_Mount & Blade II Bannerlord_bin_Modules_ 27_07_2026 01_05_41.zip

Size:
18,596,761 bytes

SHA-256:
42d4adf2e8d9f9bce0dc90945832c673aeddf81d06044cb0e6f08a2ddb852617
```

## Repository status

The source manifest and individual screenshot hashes are committed. The original ZIP itself still needs to be added from the local machine through Git LFS before PR #23 can leave draft state.

Expected destination:

```text
data/combat_observations/2026-07-27-normalized-only/source/original_screenshots.zip
```

Because `.gitattributes` routes ZIP and image files through Git LFS, add it with a normal Git workflow on the machine that holds the original archive:

```bash
git checkout agent/normalize-combat-batch-2026-07-27-only
git lfs install
cp '<path-to-original-zip>' \
  data/combat_observations/2026-07-27-normalized-only/source/original_screenshots.zip
sha256sum data/combat_observations/2026-07-27-normalized-only/source/original_screenshots.zip
git add .gitattributes data/combat_observations/2026-07-27-normalized-only/source/original_screenshots.zip
git commit -m 'source: archive 2026-07-27 combat screenshots'
git push
```

The calculated hash must match the value above. Do not replace the original ZIP with a recompressed or regenerated archive.

When Git LFS is unavailable, publish a chunked, repository-reconstructible copy in this directory and include per-part hashes, reconstruction commands, and the expected reconstructed ZIP hash.
