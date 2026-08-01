#!/usr/bin/env python3
"""Quantify the hollow crafted-weapon damage hole per track (stdlib only).

Reproduces every number in
`analysis/item_validation/CRAFTED_DAMAGE_COVERAGE_export_20260731_150800.md`.

A weapon slot is **hollow** when it resolves to `item_kind == "CraftedItem"` and both
`swing_damage` and `thrust_damage` are blank. No score can read a real melee or thrown
damage number out of such a row.

Tracks are never pooled.

    python3 scripts/analysis/quantify_crafted_damage_coverage.py
    python3 scripts/analysis/quantify_crafted_damage_coverage.py --json
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
from pathlib import Path

TRACKS = ("vanilla", "nightmare_sails", "realm_of_thrones", "taom")
EXPORT_ID = "export_20260731_150800"

# Mirrors scripts/scoring/generate_vanilla_role_scores.py:crafted_class (read-only).
CLASS_TOKENS = (
    ("TwoHandedPolearm", "two_handed_polearm"),
    ("TwoHandedSword", "two_handed_sword"),
    ("OneHandedPolearm", "one_handed_polearm"),
    ("OneHandedSword", "one_handed_sword"),
    ("Mace", "mace"),
    ("Axe", "axe"),
    ("Javelin", "javelin"),
    ("Throwing", "throwing"),
)
THROWN_CLASSES = {"javelin", "throwing"}


def crafted_class(template: str | None) -> str:
    value = str(template or "")
    for token, name in CLASS_TOKENS:
        if token in value:
            return name
    return "other"


def analyse_track(repo: Path, track: str) -> dict:
    audit_path = repo / "data" / track / "audit" / f"{track}_troop_equipment_audit.csv"
    troops_path = repo / "data" / track / "audit" / f"{track}_troops.csv"

    with troops_path.open(newline="", encoding="utf-8") as handle:
        soldiers = {
            row["troop_id"]
            for row in csv.DictReader(handle)
            if str(row.get("is_soldier", "")).strip().lower() == "true"
        }

    weapon_rows = 0
    crafted_rows = 0
    hollow_rows = 0
    hollow_troops: set[str] = set()
    hollow_melee_troops: set[str] = set()
    hollow_thrown_troops: set[str] = set()
    real_thrown_troops: set[str] = set()
    direct_melee_rows = 0
    class_rows: dict[str, int] = {}
    crafted_item_ids: set[str] = set()
    templates: set[str] = set()

    with audit_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if not str(row.get("slot", "")).startswith("Item"):
                continue
            weapon_rows += 1
            troop_id = row["troop_id"]
            if row.get("item_kind") == "CraftedItem":
                crafted_rows += 1
                crafted_item_ids.add(row.get("item_id", ""))
                template = row.get("crafting_template") or ""
                templates.add(template)
                name = crafted_class(template)
                class_rows[name] = class_rows.get(name, 0) + 1
                hollow = not (row.get("swing_damage") or "").strip() and not (
                    row.get("thrust_damage") or ""
                ).strip()
                if hollow:
                    hollow_rows += 1
                    hollow_troops.add(troop_id)
                    (hollow_thrown_troops if name in THROWN_CLASSES else hollow_melee_troops).add(
                        troop_id
                    )
            elif row.get("type") in {"OneHandedWeapon", "TwoHandedWeapon", "Polearm"}:
                direct_melee_rows += 1
            elif row.get("type") == "Thrown":
                if (row.get("swing_damage") or "").strip() or (
                    row.get("thrust_damage") or ""
                ).strip():
                    real_thrown_troops.add(troop_id)

    return {
        "track": track,
        "soldiers": len(soldiers),
        "weapon_slot_rows": weapon_rows,
        "crafted_weapon_rows": crafted_rows,
        "hollow_weapon_rows": hollow_rows,
        "direct_melee_weapon_rows": direct_melee_rows,
        "distinct_crafted_items": len(crafted_item_ids - {""}),
        "distinct_crafting_templates": len(templates - {""}),
        "soldiers_with_hollow_slot": len(hollow_troops & soldiers),
        "soldiers_with_hollow_melee": len(hollow_melee_troops & soldiers),
        "soldiers_with_hollow_thrown": len(hollow_thrown_troops & soldiers),
        "soldiers_with_real_thrown": len(real_thrown_troops & soldiers),
        "hollow_rows_by_class": dict(sorted(class_rows.items())),
        "_hollow_troop_ids": hollow_troops,
    }


def analyse_ladders(repo: Path, track: str, hollow_troops: set[str]) -> dict:
    ladder_dir = repo / "analysis" / "theoretical" / track / EXPORT_ID
    result: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(str(ladder_dir), "role_report_*.csv"))):
        name = Path(path).name[len("role_report_") : -len(".csv")]
        with open(path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        top = rows[:50]
        result[name] = {
            "entries": len(rows),
            "entries_with_hollow_weapon": sum(
                1 for row in rows if row.get("troop_id") in hollow_troops
            ),
            "top_n": len(top),
            "top_n_with_hollow_weapon": sum(
                1 for row in top if row.get("troop_id") in hollow_troops
            ),
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()

    report: dict[str, dict] = {"export_id": EXPORT_ID, "tracks": {}}
    for track in TRACKS:
        stats = analyse_track(repo, track)
        hollow_ids = stats.pop("_hollow_troop_ids")
        stats["role_ladders"] = analyse_ladders(repo, track, hollow_ids)
        report["tracks"][track] = stats

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    for track, stats in report["tracks"].items():
        print(f"== {track}")
        for key, value in stats.items():
            if key in {"role_ladders", "hollow_rows_by_class"}:
                continue
            print(f"   {key}: {value}")
        print(f"   hollow_rows_by_class: {stats['hollow_rows_by_class']}")
        for role, ladder in stats["role_ladders"].items():
            share = (
                100.0 * ladder["entries_with_hollow_weapon"] / ladder["entries"]
                if ladder["entries"]
                else 0.0
            )
            print(
                f"   ladder {role:16s} entries={ladder['entries']:4d} "
                f"hollow={ladder['entries_with_hollow_weapon']:4d} ({share:5.1f}%) "
                f"top{ladder['top_n']}_hollow={ladder['top_n_with_hollow_weapon']}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
