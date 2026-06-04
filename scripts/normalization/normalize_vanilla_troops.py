from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

SKILL_COLUMNS = [
    'OneHanded',
    'TwoHanded',
    'Polearm',
    'Bow',
    'Crossbow',
    'Throwing',
    'Riding',
    'Athletics',
]


def strip_ns(tag: str) -> str:
    return tag.split('}', 1)[-1] if '}' in tag else tag


def level_to_tier(level):
    if pd.isna(level):
        return None

    level = int(level)
    mapping = {1:1,6:2,11:3,16:4,21:5,26:6,31:7}
    return mapping.get(level)


def extract_troops(spnpccharacters_path: Path) -> pd.DataFrame:
    tree = ET.parse(spnpccharacters_path)
    root = tree.getroot()

    rows = []

    for npc in root.iter():
        if strip_ns(npc.tag) != 'NPCCharacter':
            continue

        attrs = dict(npc.attrib)

        row = {
            'id': attrs.get('id'),
            'name_raw': attrs.get('name'),
            'level': attrs.get('level'),
            'occupation': attrs.get('occupation'),
            'culture': attrs.get('culture'),
            'default_group': attrs.get('default_group'),
            'is_basic_troop': attrs.get('is_basic_troop'),
            'is_hero': attrs.get('is_hero'),
            'upgrade_targets': '',
            'equipment_items': '',
        }

        skills = {}
        upgrade_targets = []

        for child in npc:
            tag = strip_ns(child.tag)

            if tag == 'skills':
                for skill in child:
                    if strip_ns(skill.tag) == 'skill':
                        sid = skill.attrib.get('id')
                        val = skill.attrib.get('value')
                        if sid:
                            skills[sid] = val

            elif tag == 'upgrade_targets':
                for up in child:
                    if strip_ns(up.tag) == 'upgrade_target':
                        upgrade_targets.append(up.attrib.get('id', ''))

        for skill_name in SKILL_COLUMNS:
            row[skill_name] = skills.get(skill_name)

        row['upgrade_targets'] = '|'.join([x for x in upgrade_targets if x])

        rows.append(row)

    df = pd.DataFrame(rows)

    for col in ['level', *SKILL_COLUMNS]:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--raw-xml-root', type=Path, default=Path('data/vanilla/raw_xml'))
    parser.add_argument('--output-dir', type=Path, default=Path('data/vanilla/normalized'))
    args = parser.parse_args()

    troop_xml = args.raw_xml_root / 'SandboxCore' / 'ModuleData' / 'spnpccharacters.xml'

    troops = extract_troops(troop_xml)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    troops.to_csv(args.output_dir / 'vanilla_troops_raw_extracted.csv', index=False)

    combat = troops[(troops['occupation'] == 'Soldier') & (troops['level'].notna())].copy()

    combat['tier_estimated'] = combat['level'].apply(level_to_tier)
    combat['is_terminal'] = combat['upgrade_targets'].fillna('').eq('')

    combat.to_csv(args.output_dir / 'vanilla_combat_troops_raw.csv', index=False)

    summary = combat.groupby(['level', 'tier_estimated']).size().reset_index(name='count')
    summary.to_csv(args.output_dir / 'vanilla_combat_troop_level_summary.csv', index=False)


if __name__ == '__main__':
    main()
