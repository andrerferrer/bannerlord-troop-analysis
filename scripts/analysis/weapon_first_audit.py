#!/usr/bin/env python3
"""Source-pinned ROT weapon audit. No damage proxies, DPS, or skill-led ranking.

The comparator is a partial order of verified, usage-compatible damage/speed
pairs, not a scalar score. Current missing pairs stay missing. Run from any cwd.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import json
import math
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

BASE = '9311f5596aabc04974d5fe4d7113f1088454143f'
TRACK = 'realm_of_thrones'
EXPORT = 'export_20260731_150800'
PREFIX = f'data/{TRACK}/audit/{TRACK}_'
QUEUE = 'data/combat_observations/test_queues/realm_of_thrones.json'
OUT_PATH = 'analysis/weapon_first/2026-09-17'
FOCUS = ('yiti_samurai', 'mounted_kingsguard', 'stormlands_thunderknight', 'mounted_priest', 'sarnor_spider')
MELEE = frozenset({'OneHandedSword', 'TwoHandedSword', 'OneHandedAxe', 'TwoHandedAxe', 'OneHandedPolearm', 'TwoHandedPolearm', 'Mace', 'TwoHandedMace', 'Pike', 'Dagger'})
THROWN = frozenset({'Javelin', 'ThrowingKnife', 'ThrowingAxe', 'ROT_ThrowingAxe'})
DIRECT_MELEE = frozenset({'OneHandedWeapon', 'TwoHandedWeapon', 'Polearm'})
NUMERIC = ('swing_damage', 'thrust_damage', 'swing_speed', 'thrust_speed', 'speed_rating')


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n').encode()


def number(value: object) -> float | None:
    if value is None or isinstance(value, bool) or str(value).strip() == '':
        return None
    try:
        result = float(value)
    except (ValueError, TypeError):
        return None
    return result if math.isfinite(result) and result >= 0 else None


def family(row: dict) -> str:
    if str(row.get('item_found', '')).lower() != 'true':
        return 'unresolved_item'
    if row.get('item_kind') == 'CraftedItem':
        template = row.get('crafting_template', '')
        if template in THROWN:
            return 'thrown'
        if template in MELEE:
            return 'melee'
        return 'unresolved_template'
    if row.get('type') in DIRECT_MELEE:
        return 'melee'
    return 'non_melee'


def eligible_pair(row: dict) -> bool:
    return (row.get('evidence_grade') in {'direct_usage_verified', 'validated_reconstruction'}
            and row.get('attack_usage') in {'swing', 'thrust'}
            and row.get('mount_state') in {'mounted', 'dismounted'}
            and row.get('context') in {'field', 'siege_attack', 'siege_defense'}
            and row.get('damage_type') in {'Cut', 'Pierce', 'Blunt'}
            and row.get('usage_verified') is True
            and row.get('context_usable') is True
            and number(row.get('damage')) not in (None, 0)
            and number(row.get('attack_speed')) not in (None, 0)
            and all(row.get(k) for k in ('source_reference', 'profile', 'track', 'context', 'mount_state', 'weapon_class', 'damage_type')))


def compare_pair(a: dict, b: dict) -> str:
    """Only dominance in the two raw dimensions; skills are deliberately ignored."""
    keys = ('track', 'profile', 'context', 'mount_state', 'attack_usage', 'damage_type', 'weapon_class')
    if not eligible_pair(a) or not eligible_pair(b) or any(a.get(k) != b.get(k) for k in keys):
        return 'incomparable'
    av, bv = (number(a['damage']), number(a['attack_speed'])), (number(b['damage']), number(b['attack_speed']))
    if av == bv:
        return 'equal'
    if all(x >= y for x, y in zip(av, bv)):
        return 'a_dominates_on_damage_and_speed'
    if all(x <= y for x, y in zip(av, bv)):
        return 'b_dominates_on_damage_and_speed'
    return 'tradeoff_no_total_order'


def operator_queue(base: dict) -> dict:
    """Build the declared operator override, without promoting weapon evidence."""
    result = copy.deepcopy(base)
    if base.get('track') != TRACK or base.get('active_test') is not None or base.get('ordered_queue'):
        raise ValueError('operator snapshot no longer matches the pinned unassigned queue')
    if any(r['troop_id'] == 'yiti_samurai' for r in base['closed'] + base['verification_holds']):
        raise ValueError('operator target conflicts with a closed or historically held identity')
    parked = [r for r in base['parked'] if r['troop_id'] == 'yiti_samurai']
    if len(parked) != 1 or parked[0]['status'] != 'parked_pending_weapon_evidence':
        raise ValueError('expected exactly one evidence-parked Yi Ti entry')
    result['parked'] = [r for r in base['parked'] if r['troop_id'] != 'yiti_samurai']
    result['active_test'] = {
        'troop_id': 'yiti_samurai', 'display_name': 'Yi Ti Mounted Shi', 'context': 'field',
        'status': 'operator_selected_test_in_progress', 'selection_source': 'explicit_operator_decision',
        'reason': 'Operator explicitly chose to test this troop while the weapon-first audit proceeds. This scheduling override is not a weapon-stat validation or an effectiveness verdict.',
        'weapon_evidence_status': 'damage_and_usage_speed_pending',
        'evidence_references': [f'{OUT_PATH}/OPERATOR_DECISION.json', f'{OUT_PATH}/REPORT.md', 'pull/105'],
    }
    result['queue_status'] = 'operator_selected_test_active'
    result['last_transition'] = {
        'date': '2026-09-17', 'decision_path': f'{OUT_PATH}/OPERATOR_DECISION.json',
        'from': 'active_test: null / parked: yiti_samurai pending weapon evidence',
        'to': 'active_test: yiti_samurai / ordered_queue: []',
        'reason': 'Explicit operator choice; retain the weapon-first evidence gate for analytical conclusions and future recommendations.'}
    result['updated_at'] = '2026-09-17'
    return result


class Source:
    def __init__(self, repo: Path):
        self.repo = repo
        self.sources: dict[str, dict] = {}

    def git(self, *args: str) -> bytes:
        return subprocess.check_output(['git', '-C', str(self.repo), *args])

    def read(self, path: str) -> bytes:
        data = self.git('show', f'{BASE}:{path}')
        self.sources[path] = {'path': path, 'ref': BASE,
                              'git_blob_sha': self.git('rev-parse', f'{BASE}:{path}').decode().strip(),
                              'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        return data

    def csv(self, path: str) -> list[dict]:
        return list(csv.DictReader(io.StringIO(self.read(path).decode('utf-8-sig'))))


def unique_index(rows: list[dict], key: str) -> dict[str, dict]:
    out = {}
    for row in rows:
        if not row.get(key) or row[key] in out:
            raise ValueError(f'empty or duplicate {key}')
        out[row[key]] = row
    return out


def csv_bytes(rows: list[dict], fields: list[str]) -> bytes:
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def generate(repo: Path) -> dict[str, bytes]:
    source = Source(repo)
    package = json.loads(source.read(f'data/xml_exports/{EXPORT}/PACKAGE.json'))
    declared = unique_index(source.csv(f'data/xml_exports/{EXPORT}/artifact_hashes.csv'), 'path')
    troops = unique_index(source.csv(PREFIX + 'troops.csv'), 'troop_id')
    overrides = unique_index(source.csv(PREFIX + 'override_report.csv'), 'troop_id')
    tiers = unique_index(source.csv(PREFIX + 'tree_tiers.csv'), 'troop_id')
    equipment = source.csv(PREFIX + 'troop_equipment_audit.csv')
    base_queue = json.loads(source.read(QUEUE))
    source.csv(PREFIX + 'crafted_item_pieces.csv')
    legacy_path = 'data/rot_reference/hot_20260717/v44_kinetic_profile_audit.csv'
    legacy = source.csv(legacy_path)
    template = source.csv('data/rot_reference/hot_20260717/v44_exact_item_profile_template.csv')
    for path in ('docs/rot_reference/HOT_V44_KINETIC_MELEE_INTEGRATION.md',
                 'docs/handoff/PC_CRAFTING_PIECES_EXPORT_PROMPT.md',
                 'scripts/normalization/reconstruct_crafted_weapon_stats.py',
                 'scripts/normalization/rebuild_vanilla_audit.py',
                 f'data/xml_exports/{EXPORT}/RECONSTRUCTION.md'):
        source.read(path)
    # Enforce actual package hashes and byte-identical audit/analysis_pack mirrors.
    for suffix in ('troops', 'override_report', 'tree_tiers', 'troop_equipment_audit'):
        path = PREFIX + suffix + '.csv'
        mirror = f'analysis_pack/{TRACK}/{TRACK}_{suffix}.csv'
        mirror_data = source.read(mirror)
        if hashlib.sha256(mirror_data).hexdigest() != source.sources[path]['sha256']:
            raise ValueError('audit and analysis_pack diverge: ' + path)
        if source.sources[mirror]['sha256'] != declared[mirror]['sha256']:
            raise ValueError('pinned package hash mismatch: ' + mirror)
    soldiers = {k for k, v in troops.items() if v['is_soldier'].lower() == 'true'}
    selected = {k for k in soldiers if overrides[k]['change_type'] != 'inalterado'}
    by_roster = defaultdict(list)
    for index, row in enumerate(equipment, 2):
        if row['troop_id'] in selected:
            by_roster[(row['troop_id'], row['roster_index'])].append((index, row))
    weapon_rows, all_slots, candidates = [], [], []
    profile = f'{TRACK}/{EXPORT}/package:{package["expected_package_sha256"]}'
    for (troop_id, roster_index), rows in sorted(by_roster.items()):
        # A missing/unresolved horse slot is not silently converted to dismounted.
        horse_rows = [r for _, r in rows if r['slot'] == 'Horse']
        mount = 'mounted' if any(r['item_found'].lower() == 'true' and r['type'] == 'Horse' for r in horse_rows) else ('unknown' if horse_rows else 'dismounted')
        slot_counts = Counter(r['slot'] for _, r in rows)
        for index, row in rows:
            if not re.fullmatch(r'Item\d+', row['slot']):
                continue
            rec = {'troop_id': troop_id, 'troop_name': troops[troop_id]['name'],
                   'roster_index': roster_index, 'slot': row['slot'], 'item_id': row['item_id'],
                   'item_name': row['item_name'], 'family': family(row), 'item_kind': row['item_kind'],
                   'crafting_template': row['crafting_template'], 'mount_state': mount,
                   'source_row': index, 'source_reference': PREFIX + f'troop_equipment_audit.csv#row={index}',
                   'swing_damage': number(row.get('swing_damage')), 'swing_speed': number(row.get('swing_speed')),
                   'thrust_damage': number(row.get('thrust_damage')), 'thrust_speed': number(row.get('thrust_speed')),
                   'raw_speed_rating': number(row.get('speed_rating')), 'stack_amount': number(row.get('stack_amount')),
                   'evidence_grade': 'unresolved', 'eligible_usage_pairs': 0}
            if slot_counts[row['slot']] > 1:
                rec['evidence_grade'] = 'ambiguous_slot'
            elif rec['family'] == 'melee':
                rec['evidence_grade'] = ('crafted_unvalidated' if row['item_kind'] == 'CraftedItem' else 'direct_usage_incomplete')
                for usage in ('swing', 'thrust'):
                    pair = {'troop_id': troop_id, 'roster_index': roster_index, 'slot': row['slot'],
                            'item_id': row['item_id'], 'track': TRACK, 'profile': profile, 'context': 'field',
                            'mount_state': mount, 'weapon_class': row['weapon_class'], 'attack_usage': usage,
                            'damage_type': row.get(usage + '_damage_type'), 'damage': rec[usage + '_damage'],
                            'attack_speed': rec[usage + '_speed'], 'source_reference': rec['source_reference'],
                            'usage_verified': row.get('usage_verified', '').lower() == 'true',
                            'context_usable': row.get('context_usable', '').lower() == 'true',
                            'evidence_grade': 'direct_usage_verified' if row['item_kind'] == 'Item' else 'crafted_unvalidated'}
                    if mount != 'unknown' and eligible_pair(pair):
                        candidates.append(pair)
                        rec['eligible_usage_pairs'] += 1
                if rec['eligible_usage_pairs']:
                    rec['evidence_grade'] = 'direct_usage_verified'
            elif rec['family'] == 'thrown':
                rec['evidence_grade'] = 'crafted_thrown_unvalidated' if row['item_kind'] == 'CraftedItem' else 'direct_non_melee'
            elif rec['family'] == 'non_melee':
                rec['evidence_grade'] = 'not_a_melee_candidate'
            all_slots.append(rec)
            if rec['family'] in {'melee', 'unresolved_item', 'unresolved_template'}:
                weapon_rows.append(rec)
    if not all_slots or not selected:
        raise ValueError('empty production scope')
    per_troop = defaultdict(list)
    for row in weapon_rows:
        per_troop[row['troop_id']].append(row)
    coverage = []
    for troop_id in sorted(selected):
        rows = per_troop[troop_id]
        coverage.append({'troop_id': troop_id, 'troop_name': troops[troop_id]['name'],
                         'level': troops[troop_id]['level'], 'tree_depth_not_ui_tier': tiers[troop_id]['tree_tier'],
                         'rosters': sum(k[0] == troop_id for k in by_roster), 'melee_or_unresolved_slots': len(rows),
                         'complete_usage_pairs': sum(r['eligible_usage_pairs'] for r in rows),
                         'status': 'usage_pairs_available_not_troop_rank' if any(r['eligible_usage_pairs'] for r in rows) else 'withheld_missing_weapon_pair'})
    focus = [row for row in all_slots if row['troop_id'] in FOCUS]
    request_groups = defaultdict(list)
    for row in weapon_rows:
        if not row['eligible_usage_pairs']:
            request_groups[row['item_id']].append(row)
    requests = [{'item_id': item, 'item_name': rows[0]['item_name'], 'crafting_template': rows[0]['crafting_template'],
                 'affected_troops': len({r['troop_id'] for r in rows}), 'affected_slots': len(rows),
                 'active_test_weapon': any(r['troop_id'] == 'yiti_samurai' for r in rows),
                 'missing_contract': 'mode-specific damage, speed, damage type, mounted usability, verified version/source',
                 'no_skill_fallback': True} for item, rows in sorted(request_groups.items())]
    legacy_audit = [{'troop_id': r['troop_id'], 'item_id': r['best_melee_item'], 'profile_source': r['profile_source'],
                     'raw_prior_damage': number(r['profile_swing_damage']), 'raw_prior_speed': number(r['profile_swing_speed']),
                     'admitted_to_current_comparison': False,
                     'reason': 'legacy sensitivity priors or missing input; not an exact current-profile weapon measurement'} for r in legacy]
    tracked = source.git('ls-tree', '-r', '--name-only', BASE).decode().splitlines()
    search = {'base_commit': BASE, 'tracked_paths_scanned': len(tracked),
              'raw_xml_tracked': [p for p in tracked if p.endswith('.xml')],
              'weapon_evidence_related_paths': [p for p in tracked if any(x in p.lower() for x in ('crafted_weapon_stats', 'crafting_piece', 'crafting_template', 'tooltip', 'exact_item_profile'))],
              'v44_exact_profile_template_data_rows': len(template),
              'boundary': 'Search covers this pinned Git snapshot; not local-only exports, other commits, or the running game.'}
    summary = {'base_commit': BASE, 'track': TRACK, 'export_id': EXPORT, 'game_version_from_package': package['game_version'],
               'live_installation_equivalence': 'unverified', 'scope': 'all added/overridden ROT soldiers; untouched vanilla excluded',
               'raw_soldiers': len(soldiers), 'selected_troops': len(selected), 'rosters': len(by_roster),
               'weapon_slot_rows': len(all_slots), 'melee_or_unresolved_slot_rows': len(weapon_rows),
               'families': dict(sorted(Counter(r['family'] for r in all_slots).items())),
               'evidence_grades': dict(sorted(Counter(r['evidence_grade'] for r in weapon_rows).items())),
               'complete_usage_pairs': len(candidates), 'distinct_items_needing_evidence': len(requests),
               'legacy_rows_rejected': len(legacy), 'rank_generated': False, 'skill_used_for_priority': False,
               'roster_policy': 'alternatives kept separate; no favorable-roster pick, cross-roster sum or partial mean',
               'gate_outcome': 'comparison_withheld' if not candidates else 'verified_usage_partial_order_only'}
    decision = {'date': '2026-09-17', 'request': 'Execute the weapon-first gauntlet to completion; operator will test this troop meanwhile.',
                'troop_id': 'yiti_samurai', 'display_name': 'Yi Ti Mounted Shi', 'context': 'field',
                'source': 'explicit_operator_choice', 'weapon_evidence_validated': False,
                'prior_decision_preserved': 'data/combat_observations/test_queues/decisions/2026-09-17-weapon-first-correction.json',
                'meaning': 'Scheduling override only. No analytical promotion, no new battle result, no replacement future target.',
                'queue_source_commit': BASE}
    outputs = {'summary.json': canonical_json(summary), 'source_hashes.json': canonical_json(sorted(source.sources.values(), key=lambda r: r['path'])),
               'repository_evidence_search.json': canonical_json(search), 'OPERATOR_DECISION.json': canonical_json(decision),
               'operator_queue_projection.json': canonical_json(operator_queue(base_queue)),
               'focus_loadouts.json': canonical_json(focus), 'legacy_rejected_profiles.json': canonical_json(legacy_audit)}
    for name, rows, fields in (
        ('melee_weapon_audit.csv', weapon_rows, list(all_slots[0])),
        ('troop_coverage.csv', coverage, list(coverage[0])),
        ('weapon_evidence_requests.csv', requests, list(requests[0]) if requests else ['item_id']),
        ('verified_usage_pairs.csv', candidates, ['troop_id', 'roster_index', 'slot', 'item_id', 'track', 'profile', 'context', 'mount_state', 'weapon_class', 'attack_usage', 'damage_type', 'damage', 'attack_speed', 'source_reference', 'usage_verified', 'context_usable', 'evidence_grade'])):
        outputs[name] = csv_bytes(rows, fields)
    lines = ['# Weapon-first audit — 2026-09-17', '',
             '## Outcome', '',
             f'Full pinned ROT scope: **{len(selected)} troops**, **{len(by_roster)} alternative rosters**, **{len(weapon_rows)} melee/unresolved slots**.',
             f'**{len(candidates)} verified usage-specific damage/speed pairs**. No skill-based or template-based ranking was substituted.', '',
             'The operator-selected active test is **Yi Ti Mounted Shi**. Testing may proceed; its selection is explicit, not a claim that the missing weapon data was validated.', '',
             '## Carried weapons — not a performance order', '',
             '| Troop | Roster / slot | Item | Family | Damage / matching speed |', '|---|---|---|---|---|']
    for r in focus:
        lines.append(f'| {r["troop_name"]} | {r["roster_index"]} / {r["slot"]} | `{r["item_id"]}` | {r["family"]} | ' + ('unavailable / unavailable' if r['family'] in {'melee', 'thrown'} and r['swing_damage'] is None and r['thrust_damage'] is None else 'see raw source row; no melee inference') + ' |')
    lines += ['', 'Yi Ti carries **two distinct melee weapons** (`yiti_sword` and `yiti_qinglongji`) and **two throwing-knife slots**. Two slots do not establish ammunition quantity, firing frequency, or which weapon the AI used. Its battle kills must not be attributed to the sword alone.', '',
              '## Evidence and source limits', '',
              f'- Snapshot `{BASE}`, package `{EXPORT}`, game version `{package["game_version"]}`. Compatibility with the currently running installation is not independently verified.',
              '- The normalized roster audit and analysis_pack mirrors were checked against the package hashes.',
              '- Crafted composition is available, but no exact weapon physics/profile is supplied by those rows. The existing reconstruction script calls its formula an approximation and requires tooltip validation.',
              f'- All {len(legacy)} preserved V4.4 sensitivity rows were kept outside this comparison; the exact-profile template contains {len(template)} data rows.',
              '- The direct audit retains a generic speed_rating, not separate swing/thrust speed or a full weapon-usage record. It is not copied into both modes.',
              '- Untouched vanilla entries are excluded from the ROT candidate domain. Weapon slots and roster alternatives are retained, never added into a fictional combined loadout.', '',
              '## Comparator', '',
              'Verified compatible pairs are compared on damage and matching attack speed together. Improvement in both dimensions gives pairwise dominance; a damage/speed trade-off remains unordered. Different damage types, weapon classes, attack usages, mount states, contexts or profiles remain incomparable. This is not DPS and does not choose a universal troop winner. Skills never repair a missing primary input.', '',
              '## Reproduce', '',
              '```bash', 'python3 -m unittest discover -s tests -p "test_weapon_first_*.py" -v',
              f'python3 scripts/analysis/weapon_first_audit.py --repo . --output {OUT_PATH}', '```', '',
              'The output includes every scoped troop, explicit missing-data requests per weapon, retained legacy priors with rejection reasons, and source hashes. The battle evidence and frozen models remain unchanged.']
    outputs['REPORT.md'] = ('\n'.join(lines) + '\n').encode()
    outputs['artifact_hashes.json'] = canonical_json({k: hashlib.sha256(v).hexdigest() for k, v in sorted(outputs.items())})
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--apply-operator-selection', action='store_true', help='Apply only the exact declared one-shot queue override; refuses intervening changes.')
    args = parser.parse_args()
    repo = args.repo.resolve()
    first, second = generate(repo), generate(repo)
    if first != second:
        raise ValueError('non-deterministic production regeneration')
    args.output.mkdir(parents=True, exist_ok=True)
    for name, data in first.items():
        (args.output / name).write_bytes(data)
    if args.apply_operator_selection:
        current = json.loads((repo / QUEUE).read_text())
        base = json.loads(Source(repo).read(QUEUE))
        desired = json.loads(first['operator_queue_projection.json'])
        if current not in (base, desired):
            raise ValueError('refusing to overwrite intervening queue decision')
        (repo / QUEUE).write_bytes(first['operator_queue_projection.json'])
    print(first['summary.json'].decode())
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
