#!/usr/bin/env python3
"""Verify every original delivery file without extracting or overwriting files."""
from __future__ import annotations
import hashlib
import io
import json
import subprocess
import tarfile
from pathlib import Path
from typing import Callable

SOURCE_COMMIT = 'e79827d9fd61834479bcbad2d7a2f2fd6f7ce26d'
ARCHIVE_SHA256 = 'f1076c2618db989b33d3379e015d7ed5d1cd7888d0849fa6dc4b4b9174758065'
MANIFEST_SHA256 = '94c48ec80afb94895c84a2559e6acdc80deca2beda1a20cebc6009d1bb0c8be6'
ROOT = 'analysis/weapon_first/2026-09-17/'
LOGS = {'execution_logs/' + name for name in (
    'weapon-first-targeted.log', 'weapon-first-adversarial-red.log',
    'weapon-first-targeted-green.log', 'weapon-first-full-final.log',
    'weapon-first-baseline-failures.log')}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify(archive: bytes, read_source: Callable[[str], bytes]) -> dict:
    require(hashlib.sha256(archive).hexdigest() == ARCHIVE_SHA256, 'archive hash mismatch')
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:xz') as tar:
        members = tar.getmembers()
        expected = LOGS | {'LEIA-ME.md', 'delivery_hashes.json'}
        require(len(members) == 7 and {m.name for m in members} == expected, 'unexpected archive members')
        require(all(m.isfile() and m.size < 1_000_000 for m in members), 'invalid archive member type/size')
        payloads = {m.name: tar.extractfile(m).read() for m in members}
    raw_manifest = payloads['delivery_hashes.json']
    require(hashlib.sha256(raw_manifest).hexdigest() == MANIFEST_SHA256, 'manifest hash mismatch')
    manifest = json.loads(raw_manifest)
    require(len(manifest) == 28, 'original delivery index is incomplete')
    require(set(payloads) - {'delivery_hashes.json'} <= set(manifest), 'unindexed supplement file')
    for path, expected_hash in manifest.items():
        data = payloads[path] if path in payloads else read_source(path)
        require(hashlib.sha256(data).hexdigest() == expected_hash, 'file hash mismatch: ' + path)
    report = json.loads(read_source(ROOT + 'validation_report.json'))
    require({'execution_logs/' + r['name'] for r in report['original_execution_logs']} == LOGS, 'original log index differs')
    for row in report['original_execution_logs']:
        data = payloads['execution_logs/' + row['name']]
        require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], 'original log bytes differ')
    return {'source_commit': SOURCE_COMMIT, 'original_file_payloads_verified': len(manifest) + 1,
            'already_versioned_files': 22, 'supplement_files': len(payloads), 'original_logs': len(LOGS),
            'archive_sha256': ARCHIVE_SHA256, 'original_zip_container_retained': False}


def main() -> None:
    here = Path(__file__).resolve().parent
    repo = here.parents[3]
    def read_source(path: str) -> bytes:
        return subprocess.check_output(['git', '-C', str(repo), 'show', SOURCE_COMMIT + ':' + path])
    result = verify((here / 'delivery_supplement.tar.xz').read_bytes(), read_source)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
