# Reconstruct Lannister Prideknight mixed normalized bundle

Archive SHA-256: `1ff30bba3440c89a338cbbdbe9a78c76f0eaf912bae2d5504ee9f05f42d82456`

The ordered Base64 representation is retained as `lannister_prideknight_mixed_2026-08-21.tar.xz.base64.part-00`.

```bash
base64 --decode lannister_prideknight_mixed_2026-08-21.tar.xz.base64.part-00 > lannister_prideknight_mixed_2026-08-21.tar.xz
printf '%s  %s\n' '1ff30bba3440c89a338cbbdbe9a78c76f0eaf912bae2d5504ee9f05f42d82456' 'lannister_prideknight_mixed_2026-08-21.tar.xz' | sha256sum --check
mkdir -p reconstructed
tar -xJf lannister_prideknight_mixed_2026-08-21.tar.xz -C reconstructed
```

After extraction, verify every file against `lannister_prideknight_mixed_2026-08-21/artifact_hashes.csv`.
