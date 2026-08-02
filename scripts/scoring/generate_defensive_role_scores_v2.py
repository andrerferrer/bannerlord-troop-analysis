#!/usr/bin/env python3
"""Build the XML-structural defensive role model v2 candidate.

The candidate keeps infantry and cavalry on separate scales, averages alternative
equipment rosters, and separates physical protection from defensive utility.
Spectacle-scale units remain in each lane's normalization population by design.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from outliers import ALL_CRITERIA, spectacle_reason

MODEL_VERSION = "defensive_role_scores_v2_candidate"
EXPORT_ID = "export_20260731_150800"
TRACKS = ("vanilla", "nightmare_sails", "realm_of_thrones", "taom")
BASE_TRACK = "vanilla"
PUBLISHED_SCORE_DECIMALS = 6

ARMOR_SLOTS = {"Head", "Body", "Gloves", "Leg", "Cape"}
MELEE_SKILLS = ("OneHanded", "TwoHanded", "Polearm")

INFANTRY_PROTECTION_WEIGHTS = {
    "armor_component_v2": 0.70,
    "shield_hp_component_v2": 0.20,
    "shield_armor_component_v2": 0.10,
}
CAVALRY_PROTECTION_WEIGHTS = {
    "armor_component_v2": 0.50,
    "shield_hp_component_v2": 0.15,
    "shield_armor_component_v2": 0.05,
    "harness_component_v2": 0.20,
    "mount_health_component_v2": 0.10,
}
UTILITY_WEIGHTS = {
    "protection_score_v2": 0.80,
    "mobility_component_v2": 0.10,
    "counterpressure_component_v2": 0.10,
}

ROSTER_FIELDS = (
    "troop_id",
    "troop_name",
    "roster_index",
    "armor_total",
    "survivability_armor_v71",
    "shield_hp",
    "shield_armor",
    "has_shield",
    "has_horse",
    "harness_armor",
    "horse_extra_health",
    "horse_speed",
    "horse_maneuver",
    "horse_charge_damage_audit_only",
    "horse_charge_damage_max_audit_only",
    "horse_item_ids_audit_only",
    "shield_probability",
    "horse_probability",
)

TROOP_FIELDS = (
    "troop_id",
    "troop_name",
    "culture",
    "level",
    "default_group",
    "defensive_lane",
    "roster_count",
    "shield_share",
    "horse_share",
    "armor_total_mean",
    "survivability_armor_v71_mean",
    "shield_hp_mean",
    "shield_armor_mean",
    "harness_armor_mean",
    "horse_extra_health_mean",
    "horse_speed_mean",
    "horse_maneuver_mean",
    "horse_charge_damage_audit_only_mean",
    "horse_charge_damage_max_audit_only",
    "mount_ids_audit_only",
    "spectacle_reason",
    "athletics",
    "riding",
    "melee_skill",
    "armor_component_v2",
    "shield_hp_component_v2",
    "shield_armor_component_v2",
    "harness_component_v2",
    "mount_health_component_v2",
    "mobility_component_v2",
    "counterpressure_component_v2",
    "protection_score_v2",
    "defensive_utility_score_v2",
    "protection_rank_v2",
    "defensive_utility_rank_v2",
    "normalization_includes_outliers",
    "roster_aggregation",
    "evidence_basis",
    "empirical",
    "score_status",
)


def number(value: object, default: float = 0.0) -> float:
    try:
        text = str(value).strip()
        parsed = float(text) if text else default
        return parsed if math.isfinite(parsed) else default
    except (TypeError, ValueError):
        return default


def truthy(value: object) -> bool:
    return str(value).strip().casefold() in {"1", "true", "yes"}


def survivability_armor_v71(
    head_armor: float,
    body_armor: float,
    arm_armor: float,
    leg_armor: float,
) -> float:
    """Return the accepted v7.1 lethality-weighted armor proxy."""
    return (
        0.35 * head_armor
        + 0.55 * body_armor
        + 0.05 * arm_armor
        + 0.05 * leg_armor
    )


def mean(values: Iterable[float]) -> float:
    collected = list(values)
    return sum(collected) / len(collected) if collected else 0.0


def max_value(rows: Sequence[Mapping[str, object]], field: str) -> float:
    return max((number(row.get(field)) for row in rows), default=0.0)


def published_score(value: object) -> float:
    return float(f"{number(value):.{PUBLISHED_SCORE_DECIMALS}f}")


def minmax(values: Sequence[float]) -> list[float]:
    if not values:
        return []
    low = min(values)
    high = max(values)
    if high <= low:
        return [0.0] * len(values)
    return [100.0 * (value - low) / (high - low) for value in values]


def weighted_score(row: Mapping[str, object], weights: Mapping[str, float]) -> float:
    return sum(number(row.get(field)) * weight for field, weight in weights.items())


def eligible_troops(
    troops: Sequence[Mapping[str, object]],
    overrides: Sequence[Mapping[str, object]] | None,
) -> list[Mapping[str, object]]:
    changes = {
        str(row.get("troop_id", "")): str(row.get("change_type", ""))
        for row in (overrides or [])
    }
    eligible = []
    for row in troops:
        troop_id = str(row.get("troop_id", ""))
        if not truthy(row.get("is_soldier")) or truthy(row.get("is_hero")):
            continue
        if troop_id.startswith("mp_"):
            continue
        if changes.get(troop_id) == "inalterado":
            continue
        eligible.append(row)
    return eligible


def rows_by_slot(
    rows: Sequence[Mapping[str, object]],
) -> dict[str, list[Mapping[str, object]]]:
    grouped: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("slot", ""))].append(row)
    return grouped


def expected_value(
    rows: Sequence[Mapping[str, object]],
    field: str,
    *,
    required_type: str | None = None,
) -> float:
    def value(row: Mapping[str, object]) -> float:
        if not truthy(row.get("item_found", "True")):
            return 0.0
        if required_type is not None and row.get("type") != required_type:
            return 0.0
        return number(row.get(field))

    return mean(value(row) for row in rows)


def armor_totals(rows: Sequence[Mapping[str, object]]) -> tuple[float, ...]:
    armor_slots = [
        alternatives
        for slot, alternatives in rows_by_slot(rows).items()
        if slot in ARMOR_SLOTS
    ]
    return tuple(
        sum(expected_value(alternatives, field) for alternatives in armor_slots)
        for field in ("head_armor", "body_armor", "arm_armor", "leg_armor")
    )


def shield_probability(
    item_slots: Sequence[Sequence[Mapping[str, object]]],
) -> float:
    no_shield_probability = 1.0
    for alternatives in item_slots:
        slot_probability = mean(
            float(
                truthy(row.get("item_found", "True"))
                and row.get("type") == "Shield"
            )
            for row in alternatives
        )
        no_shield_probability *= 1.0 - slot_probability
    return 1.0 - no_shield_probability


def roster_features(
    troop: Mapping[str, object],
    roster_index: str,
    rows: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    slots = rows_by_slot(rows)
    item_slots = [
        alternatives
        for slot, alternatives in slots.items()
        if slot.startswith("Item")
    ]
    horses = slots.get("Horse", [])
    harnesses = slots.get("HorseHarness", [])
    probability_of_shield = shield_probability(item_slots)
    horse_ids = sorted(
        {
            str(row.get("item_id", ""))
            for row in horses
            if str(row.get("item_id", ""))
        }
    )
    head, body, arm, leg = armor_totals(rows)
    return {
        "troop_id": str(troop.get("troop_id", "")),
        "troop_name": str(troop.get("name") or troop.get("name_raw") or ""),
        "roster_index": roster_index,
        "armor_total": head + body + arm + leg,
        "survivability_armor_v71": survivability_armor_v71(head, body, arm, leg),
        "shield_hp": max(
            (
                expected_value(
                    alternatives,
                    "hit_points",
                    required_type="Shield",
                )
                for alternatives in item_slots
            ),
            default=0.0,
        ),
        "shield_armor": max(
            (
                expected_value(
                    alternatives,
                    "shield_armor",
                    required_type="Shield",
                )
                for alternatives in item_slots
            ),
            default=0.0,
        ),
        "has_shield": probability_of_shield > 0,
        "has_horse": bool(horses),
        "harness_armor": expected_value(harnesses, "body_armor"),
        "horse_extra_health": expected_value(horses, "horse_extra_health"),
        "horse_speed": expected_value(horses, "horse_speed"),
        "horse_maneuver": expected_value(horses, "horse_maneuver"),
        "horse_charge_damage_audit_only": expected_value(
            horses,
            "horse_charge_damage",
        ),
        "horse_charge_damage_max_audit_only": max_value(
            [row for row in horses if truthy(row.get("item_found", "True"))],
            "horse_charge_damage",
        ),
        "horse_item_ids_audit_only": "|".join(horse_ids),
        "shield_probability": probability_of_shield,
        "horse_probability": float(bool(horses)),
    }


def build_roster_features(
    troops: Sequence[Mapping[str, object]],
    audit: Sequence[Mapping[str, object]],
    overrides: Sequence[Mapping[str, object]] | None = None,
) -> tuple[list[dict[str, object]], dict[str, Mapping[str, object]]]:
    selected = eligible_troops(troops, overrides)
    troop_by_id = {str(row.get("troop_id", "")): row for row in selected}
    grouped: dict[tuple[str, str], list[Mapping[str, object]]] = defaultdict(list)
    for row in audit:
        troop_id = str(row.get("troop_id", ""))
        if troop_id in troop_by_id:
            grouped[(troop_id, str(row.get("roster_index", "0")))].append(row)
    troops_with_rosters = {troop_id for troop_id, _ in grouped}
    missing = sorted(set(troop_by_id) - troops_with_rosters)
    if missing:
        raise ValueError(
            "eligible troops missing equipment audit rosters: "
            + ", ".join(missing)
        )
    rosters = [
        roster_features(troop_by_id[troop_id], roster_index, rows)
        for (troop_id, roster_index), rows in sorted(grouped.items())
    ]
    return rosters, troop_by_id


def aggregate_rosters(
    rosters: Sequence[Mapping[str, object]],
    troop_by_id: Mapping[str, Mapping[str, object]],
) -> list[dict[str, object]]:
    grouped: dict[str, list[Mapping[str, object]]] = defaultdict(list)
    for row in rosters:
        grouped[str(row["troop_id"])].append(row)
    aggregated = []
    for troop_id, troop in sorted(troop_by_id.items()):
        loadouts = grouped.get(troop_id, [])
        if not loadouts:
            continue
        horse_share = mean(number(row["horse_probability"]) for row in loadouts)
        mount_ids = sorted(
            {
                mount_id
                for row in loadouts
                for mount_id in str(row["horse_item_ids_audit_only"]).split("|")
                if mount_id
            }
        )
        max_mount_charge = max(
            (
                number(row["horse_charge_damage_max_audit_only"])
                for row in loadouts
            ),
            default=0.0,
        )
        melee_skill = max(number(troop.get(skill)) for skill in MELEE_SKILLS)
        troop_name = str(troop.get("name") or troop.get("name_raw") or "")
        aggregated.append(
            {
                "troop_id": troop_id,
                "troop_name": troop_name,
                "culture": str(troop.get("culture", "")),
                "level": number(troop.get("level")),
                "default_group": str(troop.get("default_group", "")),
                "defensive_lane": "cavalry" if horse_share >= 0.5 else "infantry",
                "roster_count": len(loadouts),
                "shield_share": mean(
                    number(row["shield_probability"]) for row in loadouts
                ),
                "horse_share": horse_share,
                "armor_total_mean": mean(number(row["armor_total"]) for row in loadouts),
                "survivability_armor_v71_mean": mean(
                    number(row["survivability_armor_v71"]) for row in loadouts
                ),
                "shield_hp_mean": mean(number(row["shield_hp"]) for row in loadouts),
                "shield_armor_mean": mean(
                    number(row["shield_armor"]) for row in loadouts
                ),
                "harness_armor_mean": mean(
                    number(row["harness_armor"]) for row in loadouts
                ),
                "horse_extra_health_mean": mean(
                    number(row["horse_extra_health"]) for row in loadouts
                ),
                "horse_speed_mean": mean(
                    number(row["horse_speed"]) for row in loadouts
                ),
                "horse_maneuver_mean": mean(
                    number(row["horse_maneuver"]) for row in loadouts
                ),
                "horse_charge_damage_audit_only_mean": mean(
                    number(row["horse_charge_damage_audit_only"])
                    for row in loadouts
                ),
                "horse_charge_damage_max_audit_only": max_mount_charge,
                "mount_ids_audit_only": "|".join(mount_ids),
                "spectacle_reason": spectacle_reason(
                    troop_id,
                    troop_name,
                    mount_ids=mount_ids,
                    mount_charge_damage=max_mount_charge,
                    criteria=ALL_CRITERIA,
                )
                or "",
                "athletics": number(troop.get("Athletics")),
                "riding": number(troop.get("Riding")),
                "melee_skill": melee_skill,
            }
        )
    return aggregated


def add_component(
    lane: list[dict[str, object]],
    source_field: str,
    component_field: str,
) -> None:
    normalized = minmax([number(row[source_field]) for row in lane])
    for row, value in zip(lane, normalized, strict=True):
        row[component_field] = value


def add_lane_scores(lane: list[dict[str, object]], lane_name: str) -> None:
    components = {
        "survivability_armor_v71_mean": "armor_component_v2",
        "shield_hp_mean": "shield_hp_component_v2",
        "shield_armor_mean": "shield_armor_component_v2",
        "harness_armor_mean": "harness_component_v2",
        "horse_extra_health_mean": "mount_health_component_v2",
        "athletics": "athletics_component_v2",
        "riding": "riding_component_v2",
        "horse_speed_mean": "horse_speed_component_v2",
        "horse_maneuver_mean": "horse_maneuver_component_v2",
        "melee_skill": "counterpressure_component_v2",
    }
    for source, target in components.items():
        add_component(lane, source, target)

    protection_weights = (
        CAVALRY_PROTECTION_WEIGHTS
        if lane_name == "cavalry"
        else INFANTRY_PROTECTION_WEIGHTS
    )
    for row in lane:
        if lane_name == "cavalry":
            row["mobility_component_v2"] = mean(
                number(row[field])
                for field in (
                    "riding_component_v2",
                    "horse_speed_component_v2",
                    "horse_maneuver_component_v2",
                )
            )
        else:
            row["mobility_component_v2"] = number(
                row["athletics_component_v2"]
            )
        row["protection_score_v2"] = published_score(
            weighted_score(row, protection_weights)
        )
        row["defensive_utility_score_v2"] = published_score(
            weighted_score(row, UTILITY_WEIGHTS)
        )
        row["normalization_includes_outliers"] = True
        row["roster_aggregation"] = (
            "arithmetic_mean_across_rosters_and_within_slot_alternatives"
        )
        row["evidence_basis"] = "xml_structural"
        row["empirical"] = False
        row["score_status"] = MODEL_VERSION
        for field in (
            "harness_component_v2",
            "mount_health_component_v2",
        ):
            row.setdefault(field, 0.0)
    add_ranks(lane, "protection_score_v2", "protection_rank_v2")
    add_ranks(
        lane,
        "defensive_utility_score_v2",
        "defensive_utility_rank_v2",
    )


def add_ranks(
    rows: list[dict[str, object]],
    score_field: str,
    rank_field: str,
) -> None:
    ordered = sorted(
        rows,
        key=lambda row: (-published_score(row[score_field]), str(row["troop_id"])),
    )
    previous_score: float | None = None
    previous_rank = 0
    for position, row in enumerate(ordered, 1):
        score = published_score(row[score_field])
        if previous_score is None or score != previous_score:
            previous_rank = position
            previous_score = score
        row[rank_field] = previous_rank


def build_candidate_model(
    troops: Sequence[Mapping[str, object]],
    audit: Sequence[Mapping[str, object]],
    overrides: Sequence[Mapping[str, object]] | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rosters, troop_by_id = build_roster_features(troops, audit, overrides)
    scores = aggregate_rosters(rosters, troop_by_id)
    for lane_name in ("infantry", "cavalry"):
        lane = [row for row in scores if row["defensive_lane"] == lane_name]
        add_lane_scores(lane, lane_name)
    return rosters, scores


def build_candidate_scores(
    troops: Sequence[Mapping[str, object]],
    audit: Sequence[Mapping[str, object]],
    overrides: Sequence[Mapping[str, object]] | None = None,
) -> list[dict[str, object]]:
    """Return troop-level scores; used by tests and programmatic callers."""
    _, scores = build_candidate_model(troops, audit, overrides)
    return scores


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def serialized(value: object) -> object:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f"{value:.{PUBLISHED_SCORE_DECIMALS}f}"
    return value


def write_csv(
    path: Path,
    rows: Sequence[Mapping[str, object]],
    fieldnames: Sequence[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({field: serialized(row.get(field, "")) for field in fieldnames})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ranked(
    rows: Sequence[Mapping[str, object]],
    lane: str,
    score_field: str,
) -> list[Mapping[str, object]]:
    return sorted(
        (row for row in rows if row["defensive_lane"] == lane),
        key=lambda row: (-published_score(row[score_field]), str(row["troop_id"])),
    )


def write_track(
    repo: Path,
    output_root: Path,
    track: str,
) -> list[Path]:
    audit_dir = repo / "data" / track / "audit"
    audit_path = audit_dir / f"{track}_troop_equipment_audit.csv"
    troops_path = audit_dir / f"{track}_troops.csv"
    override_path = audit_dir / f"{track}_override_report.csv"
    overrides = None if track == BASE_TRACK else read_csv(override_path)
    rosters, scores = build_candidate_model(
        read_csv(troops_path),
        read_csv(audit_path),
        overrides,
    )
    track_dir = output_root / track
    outputs = []
    roster_path = track_dir / f"{track}_defensive_roster_features_v2.csv"
    score_path = track_dir / f"{track}_defensive_troop_scores_v2.csv"
    write_csv(roster_path, rosters, ROSTER_FIELDS)
    write_csv(score_path, sorted(scores, key=lambda row: str(row["troop_id"])), TROOP_FIELDS)
    outputs.extend((roster_path, score_path))
    for lane in ("infantry", "cavalry"):
        for score_field, label in (
            ("protection_score_v2", "protection"),
            ("defensive_utility_score_v2", "utility"),
        ):
            path = track_dir / f"{lane}_{label}_v2.csv"
            write_csv(path, ranked(scores, lane, score_field), TROOP_FIELDS)
            outputs.append(path)
    meta_path = track_dir / "meta.json"
    meta = {
        "model": MODEL_VERSION,
        "canonical": False,
        "export_id": EXPORT_ID,
        "track": track,
        "evidence_basis": "xml_structural",
        "empirical": False,
        "normalization": "per_track_per_lane_minmax_including_outliers",
        "roster_aggregation": (
            "arithmetic_mean_across_rosters_and_within_slot_alternatives"
        ),
        "inputs": {
            audit_path.relative_to(repo).as_posix(): sha256_file(audit_path),
            troops_path.relative_to(repo).as_posix(): sha256_file(troops_path),
            **(
                {override_path.relative_to(repo).as_posix(): sha256_file(override_path)}
                if overrides is not None
                else {}
            ),
        },
        "counts": {
            "rosters": len(rosters),
            "troops": len(scores),
            "infantry": sum(row["defensive_lane"] == "infantry" for row in scores),
            "cavalry": sum(row["defensive_lane"] == "cavalry" for row in scores),
        },
        "weights": {
            "infantry_protection": INFANTRY_PROTECTION_WEIGHTS,
            "cavalry_protection": CAVALRY_PROTECTION_WEIGHTS,
            "defensive_utility": UTILITY_WEIGHTS,
        },
    }
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    outputs.append(meta_path)
    return outputs


def write_manifest(output_root: Path, paths: Sequence[Path]) -> None:
    existing_artifacts = {
        path
        for path in output_root.rglob("*")
        if path.is_file()
        and path.name != "artifact_hashes.csv"
        and path.suffix in {".csv", ".json"}
    }
    rows = [
        {
            "path": path.relative_to(output_root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in sorted(set(paths) | existing_artifacts)
    ]
    write_csv(output_root / "artifact_hashes.csv", rows, ("path", "bytes", "sha256"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("analysis/model_candidates/role_scores_v2_defense"),
    )
    parser.add_argument("--tracks", nargs="+", choices=TRACKS, default=list(TRACKS))
    args = parser.parse_args()
    repo = args.repo.resolve()
    output_root = args.output_dir
    if not output_root.is_absolute():
        output_root = repo / output_root
    generated = []
    for track in args.tracks:
        generated.extend(write_track(repo, output_root, track))
    write_manifest(output_root, generated)
    print(f"model={MODEL_VERSION}")
    print(f"tracks={','.join(args.tracks)}")
    print(f"output={output_root}")


if __name__ == "__main__":
    main()
