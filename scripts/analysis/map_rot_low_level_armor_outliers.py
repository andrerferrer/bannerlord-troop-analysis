#!/usr/bin/env python3
"""Map low-level Realm of Thrones worn-armor outliers without a composite score."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path


ARMOR_SLOTS = {"Head", "Body", "Leg", "Gloves", "Cape"}
LEVEL_LABELS = {11: "T2", 16: "T3", 21: "T4"}
ALLOWED_GROUPS = {"Infantry", "Ranged"}
ZONE_FIELDS = {
    "body_zone_armor": "body_armor",
    "arm_zone_armor": "arm_armor",
    "head_zone_armor": "head_armor",
    "leg_zone_armor": "leg_armor",
}
OUTPUT_FIELDS = [
    "operator_tier_label",
    "level",
    "body_zone_rank",
    "body_zone_percentile",
    "body_zone_band_median",
    "body_zone_band_size",
    "troop_id",
    "troop_name",
    "culture",
    "default_group",
    "tree_tier",
    "roster_count",
    "body_slot_armor",
    "body_zone_armor",
    "arm_zone_armor",
    "head_zone_armor",
    "leg_zone_armor",
    "shield_hp",
    "shield_armor",
    "body_item_ids",
    "evidence_basis",
    "empirical",
]


def number(value: str | None) -> float:
    try:
        return float(value or 0)
    except ValueError:
        return 0.0


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def normalize(value: float) -> str:
    rounded = round(value, 2)
    return str(int(rounded)) if rounded.is_integer() else f"{rounded:.2f}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_candidates(
    path: Path, review_queue: list[dict[str, str]] | None = None
) -> list[dict[str, object]]:
    rosters: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    metadata: dict[str, dict[str, str]] = {}

    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            level = int(number(row.get("level")))
            line_status = row.get("line_status_corrected") or row.get("line_status")
            if (
                level not in LEVEL_LABELS
                or row.get("occupation") != "Soldier"
                or line_status != "main_or_minor_line"
                or row.get("default_group") not in ALLOWED_GROUPS
            ):
                continue
            troop_id = row["troop_id"]
            roster_index = int(number(row.get("roster_index")))
            rosters[(troop_id, roster_index)].append(row)
            metadata[troop_id] = {
                "troop_id": troop_id,
                "troop_name": row["troop_name"],
                "culture": row["culture"],
                "default_group": row["default_group"],
                "tree_tier": row["tree_tier"],
                "level": str(level),
            }

    by_troop: dict[str, list[dict[str, object]]] = defaultdict(list)
    unresolved_by_troop: dict[str, set[str]] = defaultdict(set)
    for (troop_id, _), equipment in rosters.items():
        armor = [
            row
            for row in equipment
            if row.get("slot") in ARMOR_SLOTS and row.get("item_found") == "True"
        ]
        unresolved_armor = [
            row
            for row in equipment
            if (
                row.get("slot") in ARMOR_SLOTS
                and row.get("item_id")
                and row.get("item_found") != "True"
            )
        ]
        if unresolved_armor:
            unresolved_by_troop[troop_id].update(row["item_id"] for row in unresolved_armor)
            continue
        shield = next(
            (
                row
                for row in equipment
                if row.get("type") == "Shield" and row.get("item_found") == "True"
            ),
            None,
        )
        roster: dict[str, object] = {
            "body_slot_armor": sum(
                number(row.get("body_armor")) for row in armor if row.get("slot") == "Body"
            ),
            "shield_hp": number(shield.get("hit_points")) if shield else 0.0,
            "shield_armor": number(shield.get("shield_armor")) if shield else 0.0,
            "body_item_ids": sorted(
                row["item_id"] for row in armor if row.get("slot") == "Body"
            ),
        }
        for output_field, source_field in ZONE_FIELDS.items():
            roster[output_field] = sum(number(row.get(source_field)) for row in armor)
        by_troop[troop_id].append(roster)

    candidates: list[dict[str, object]] = []
    for troop_id, troop_rosters in by_troop.items():
        if troop_id in unresolved_by_troop:
            continue
        row: dict[str, object] = dict(metadata[troop_id])
        level = int(row["level"])
        row["operator_tier_label"] = LEVEL_LABELS[level]
        row["roster_count"] = len(troop_rosters)
        for field in ["body_slot_armor", *ZONE_FIELDS, "shield_hp", "shield_armor"]:
            row[field] = mean([float(roster[field]) for roster in troop_rosters])
        row["body_item_ids"] = ";".join(
            sorted({item for roster in troop_rosters for item in roster["body_item_ids"]})
        )
        row["evidence_basis"] = "xml_structural"
        row["empirical"] = "false"
        candidates.append(row)

    if review_queue is not None:
        for troop_id, item_ids in sorted(unresolved_by_troop.items()):
            row = metadata[troop_id]
            review_queue.append(
                {
                    "troop_id": troop_id,
                    "troop_name": row["troop_name"],
                    "level": row["level"],
                    "reason": "unresolved_worn_armor",
                    "unresolved_item_ids": ";".join(sorted(item_ids)),
                }
            )

    for level in LEVEL_LABELS:
        band = [row for row in candidates if int(row["level"]) == level]
        if not band:
            continue
        values = [float(row["body_zone_armor"]) for row in band]
        median = statistics.median(values)
        for row in band:
            value = float(row["body_zone_armor"])
            row["body_zone_rank"] = 1 + sum(other > value for other in values)
            row["body_zone_percentile"] = 100 * sum(other <= value for other in values) / len(values)
            row["body_zone_band_median"] = median
            row["body_zone_band_size"] = len(values)
    return sorted(
        candidates,
        key=lambda row: (
            int(row["level"]),
            -float(row["body_zone_armor"]),
            -float(row["arm_zone_armor"]),
            str(row["troop_id"]),
        ),
    )


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    field: normalize(value) if isinstance(value, float) else value
                    for field, value in row.items()
                    if field in OUTPUT_FIELDS
                }
            )


def write_review_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = ["troop_id", "troop_name", "level", "reason", "unresolved_item_ids"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_meta(
    path: Path,
    audit: Path,
    output: Path,
    review_output: Path,
    row_count: int,
    review_count: int,
) -> None:
    metadata = {
        "track": "realm_of_thrones",
        "evidence_basis": "xml_structural",
        "empirical": False,
        "generator": "scripts/analysis/map_rot_low_level_armor_outliers.py",
        "methodology": "docs/methodology/009_rot_low_level_armor_outlier_screen.md",
        "source": {
            "path": audit.as_posix(),
            "sha256": sha256_file(audit),
        },
        "outputs": {
            "low_level_armor_map.csv": {
                "rows": row_count,
                "sha256": sha256_file(output),
            },
            "review_queue.csv": {
                "rows": review_count,
                "sha256": sha256_file(review_output),
            },
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit",
        type=Path,
        default=Path("analysis_pack/realm_of_thrones/realm_of_thrones_troop_equipment_audit.csv"),
    )
    parser.add_argument(
        "--meta-output",
        type=Path,
        default=Path(
            "analysis/theoretical/realm_of_thrones/low_level_armor_outliers_v1/"
            "meta.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "analysis/theoretical/realm_of_thrones/low_level_armor_outliers_v1/"
            "low_level_armor_map.csv"
        ),
    )
    parser.add_argument(
        "--review-output",
        type=Path,
        default=Path(
            "analysis/theoretical/realm_of_thrones/low_level_armor_outliers_v1/"
            "review_queue.csv"
        ),
    )
    args = parser.parse_args()
    review_queue: list[dict[str, str]] = []
    rows = load_candidates(args.audit, review_queue)
    write_csv(args.output, rows)
    write_review_csv(args.review_output, review_queue)
    write_meta(
        args.meta_output,
        args.audit,
        args.output,
        args.review_output,
        len(rows),
        len(review_queue),
    )
    print(
        f"wrote {len(rows)} rows to {args.output}; "
        f"review queue={len(review_queue)} at {args.review_output}"
    )


if __name__ == "__main__":
    main()
