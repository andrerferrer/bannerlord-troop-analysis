"""Inventory pinned weapon sources; diagnostic only, never a performance score."""
from __future__ import annotations
import csv
import hashlib
import io
import json
import subprocess
from pathlib import Path

BASE = '9311f5596aabc04974d5fe4d7113f1088454143f'
OUT = Path('analysis/weapon_first/2026-09-17')
TARGETS = {'yiti_samurai', 'yiti_sword', 'mounted_kingsguard', 'vlandia_2hsword_1_t5', 'stormlands_thunderknight', 'western_2hsword_t4', 'mounted_priest', 'norvoshi_long_axe', 'sarnor_spider', 'khuzait_polearm_1_t4'}

def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args])

def main() -> None:
    paths = git('ls-tree', '-r', '--name-only', BASE).decode().splitlines()
    audit_names = {'realm_of_thrones_troops.csv', 'realm_of_thrones_items_direct.csv', 'realm_of_thrones_items_crafted.csv', 'realm_of_thrones_equipment_rosters.csv', 'realm_of_thrones_roster_audit_summary.csv', 'realm_of_thrones_tree_tiers.csv'}
    sources = [p for p in paths if p.startswith('data/realm_of_thrones/audit/') and Path(p).name in audit_names]
    sources += [p for p in paths if p.startswith('data/rot_reference/hot_20260717/hot_v44_kinetic_melee/extracted/') and p.endswith('.csv')]
    report = {'source_commit': BASE, 'purpose': 'source inspection only; no recommendation or scoring', 'sources': []}
    for path in sorted(sources):
        payload = git('show', f'{BASE}:{path}')
        reader = csv.DictReader(io.StringIO(payload.decode('utf-8-sig')))
        matches, count, hits = [], 0, 0
        for index, row in enumerate(reader, 2):
            count += 1
            if any(str(v) in TARGETS for v in row.values()):
                hits += 1
                if len(matches) < 60:
                    matches.append({'csv_row': index, 'values': row})
        report['sources'].append({'path': path, 'git_blob_sha': git('rev-parse', f'{BASE}:{path}').decode().strip(), 'sha256': hashlib.sha256(payload).hexdigest(), 'size_bytes': len(payload), 'row_count': count, 'columns': reader.fieldnames, 'matched_rows': hits, 'displayed_rows': len(matches), 'rows': matches})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'source_inventory.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'source_files': len(report['sources']), 'rows_scanned': sum(s['row_count'] for s in report['sources']), 'output': str(OUT / 'source_inventory.json')}))

if __name__ == '__main__':
    main()
