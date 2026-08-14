# Source provenance

- Source: two individual screenshots supplied in the ChatGPT conversation.
- Capture range: 2026-08-13T01:47:59-03:00 through 2026-08-13T18:15:02-03:00.
- Game version family: `1.4.x`.
- Track: `realm_of_thrones`.
- Total source size: 4690340 bytes.
- Deterministic selected-source SHA-256: `763f8fb7bceb6f34514fe4686a812ec714e4ec694de1c6ddc86dc9cbb11bb1d2`.
- Source hash algorithm: for the two selected PNGs sorted by full filename, hash `filename UTF-8`, NUL, lowercase file SHA-256 ASCII, and LF for each entry.
- Raw retention: PNG files are not committed; each filename and SHA-256 is preserved in `../screenshots_manifest.csv`.
- Attachment references: `libfile_4b368ed8330c8191a266388c9bb63364` and `libfile_6e83d37aa20081918d87a9dcae1e7ede`.
- Visual re-review: possible while the original conversation/Library attachments remain available.

Recalculate the selected-source hash from a directory containing exactly the named PNGs:

```bash
python3 - <<'PY'
import csv
import hashlib
from pathlib import Path

root = Path('/path/to/the/two/pngs')
manifest = Path('data/combat_observations/2026-08-13-goldenheart-field/screenshots_manifest.csv')
names = sorted(row['image_file'] for row in csv.DictReader(manifest.open(encoding='utf-8')))
digest = hashlib.sha256()
for name in names:
    file_hash = hashlib.sha256((root / name).read_bytes()).hexdigest()
    digest.update(name.encode('utf-8'))
    digest.update(b'\0')
    digest.update(file_hash.encode('ascii'))
    digest.update(b'\n')
print(digest.hexdigest())
PY
```
