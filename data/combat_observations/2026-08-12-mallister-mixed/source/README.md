# Source provenance

- Source: six individual screenshots supplied in the ChatGPT conversation.
- Capture range: 2026-08-12T10:56:03-03:00 through 2026-08-12T15:18:02-03:00.
- Game version family: `1.4.x`.
- Track: `realm_of_thrones`.
- Total source size: 13002374 bytes.
- Deterministic selected-source SHA-256: `da79e212250da1b9105f1c71b7ade09f463b4373de87c011b1a8987979e74016`.
- Source hash algorithm: for the six selected PNGs sorted by full filename, hash `filename UTF-8`, NUL, lowercase file SHA-256 ASCII, and LF for each entry.
- Raw retention: PNG files are not committed; each filename and SHA-256 is preserved in `../screenshots_manifest.csv`.
- Visual re-review: possible only while the original conversation/Library attachments remain available.

Recalculate the selected-source hash from a directory containing exactly the named PNGs:

```bash
python3 - <<'PY'
import csv
import hashlib
from pathlib import Path

root = Path('/path/to/the/six/pngs')
manifest = Path('data/combat_observations/2026-08-12-mallister-mixed/screenshots_manifest.csv')
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
