#!/usr/bin/env python3
"""Apply the Wavey v2.9 kinetic melee layer to frozen RoT V4.3 outputs.

Canonical mode requires exact one-handed-sword profiles and a complete V4.3
all-humanoid output. Sensitivity mode accepts the preserved V4.3 top 20 and
uses explicit low-confidence family priors; it must not be published as a
canonical ranking.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from melee_engine import ROT_V44, WeaponProfile, kinetic_application_factor


EXACT_SUPPORTED_FAMILIES = {"onehand_sword"}
FAMILY_PRIORS = {
    "onehand_sword": {
        "handling": 90.0,
        "reach": 100.0,
        "weight": 1.30,
        "has_thrust": True,
        "thrust_damage_ratio": 0.75,
        "thrust_speed_ratio": 0.90,
    },
    "onehand_axe": {
        "handling": 78.0,
        "reach": 78.0,
        "weight": 1.70,
        "has_thrust": False,
    },
    "onehand_blunt": {
        "handling": 75.0,
        "reach": 75.0,
        "weight": 1.90,
        "has_thrust": False,
    },
    "twohand": {
        "handling": 75.0,
        "reach": 115.0,
        "weight": 2.20,
        "has_thrust": False,
    },
    "twohand_blunt": {
        "handling": 70.0,
        "reach": 105.0,
        "weight": 2.70,
        "has_thrust": False,
    },
    "swing_polearm": {
        "handling": 70.0,
        "reach": 135.0,
        "weight": 2.30,
        "has_thrust": False,
    },
    "thrust_polearm": {
        "handling": 75.0,
        "reach": 180.0,
        "weight": 2.20,
        "has_thrust": True,
        "thrust_damage_ratio": 0.90,
        "thrust_speed_ratio": 0.90,
    },
    "generic_melee": {
        "handling": 80.0,
        "reach": 95.0,
        "weight": 1.50,
        "has_thrust": False,
    },
}


@dataclass(frozen=True)
class ProfileResolution:
    item_id: str
    family: str
    status: str
    source: str
    missing_fields: tuple[str, ...]
    profile: WeaponProfile | None


def as_float(value: object, default: float = math.nan) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return default
    return result if math.isfinite(result) else default


def as_bool(value: object) -> bool | None:
    text = str(value or "").strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no"}:
        return False
    return None


def first_value(row: dict[str, object], aliases: Iterable[str]) -> object:
    for alias in aliases:
        value = row.get(alias)
        if value is not None and str(value).strip() != "":
            return value
    return ""


def infer_family(
    item_id: object,
    weapon_class: object = "",
    damage_type: object = "",
) -> str:
    item = str(item_id or "").lower()
    weapon_class = str(weapon_class or "").lower()
    damage_type = str(damage_type or "").lower()

    if (
        "twohandedpolearm" in weapon_class
        or any(x in item for x in ("halberd", "glaive", "war_scythe", "polehammer"))
    ):
        return "swing_polearm"
    if (
        "onehandedpolearm" in weapon_class
        or any(x in item for x in ("spear", "pike", "lance", "polearm"))
    ):
        return "thrust_polearm"
    if (
        "twohanded" in weapon_class
        or any(x in item for x in ("2hsword", "2haxe", "twoh", "two_h", "greatsword", "great_axe"))
    ):
        if any(x in item for x in ("hammer", "mace", "maul")):
            return "twohand_blunt"
        return "twohand"
    if "mace" in weapon_class or any(
        x in item for x in ("hammer", "mace", "maul", "club")
    ):
        return "onehand_blunt"
    if "axe" in weapon_class or "axe" in item:
        return "onehand_axe"
    if "sword" in weapon_class or any(
        x in item for x in ("sword", "sabre", "cutlass", "kopesh")
    ):
        return "onehand_sword"
    if damage_type == "blunt":
        return "onehand_blunt"
    return "generic_melee"


def build_item_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    lookup: dict[str, dict[str, str]] = {}
    profile_aliases = {
        "swing_speed",
        "speed_rating",
        "handling",
        "handling_rating",
        "reach",
        "weapon_length",
        "weight",
        "piece_weight_sum",
        "has_thrust",
        "thrust_damage",
        "thrust_speed",
    }
    for row in rows:
        item_id = str(row.get("item_id") or "").strip()
        if not item_id:
            continue
        completeness = sum(bool(str(row.get(key) or "").strip()) for key in profile_aliases)
        current = lookup.get(item_id)
        current_completeness = (
            sum(bool(str(current.get(key) or "").strip()) for key in profile_aliases)
            if current
            else -1
        )
        if completeness > current_completeness:
            lookup[item_id] = row
    return lookup


def melee_damage(row: dict[str, object]) -> float:
    direct = as_float(row.get("best_melee_raw_damage"))
    if math.isfinite(direct):
        return direct
    if (
        str(row.get("v43_weapon_mode") or "") == "melee"
        and str(row.get("best_weapon_item") or "")
        == str(row.get("best_melee_item") or "")
    ):
        return as_float(row.get("best_weapon_raw_damage"))
    return math.nan


def resolve_exact_profile(
    row: dict[str, object],
    item_lookup: dict[str, dict[str, str]],
) -> ProfileResolution:
    item_id = str(row.get("best_melee_item") or "").strip()
    if not item_id:
        return ProfileResolution("", "none", "no_melee_weapon", "none", (), None)

    item = item_lookup.get(item_id, {})
    combined: dict[str, object] = {**row, **item}
    family = infer_family(
        item_id,
        first_value(combined, ("weapon_class", "best_melee_weapon_class")),
        first_value(combined, ("damage_type", "best_melee_damage_type", "best_weapon_damage_type")),
    )
    if family not in EXACT_SUPPORTED_FAMILIES:
        return ProfileResolution(
            item_id,
            family,
            "unsupported_family",
            "unchanged_v43",
            (),
            None,
        )

    values = {
        "swing_damage": melee_damage(row),
        "swing_speed": as_float(
            first_value(combined, ("swing_speed", "speed_rating", "weapon_speed", "best_melee_swing_speed"))
        ),
        "handling": as_float(
            first_value(combined, ("handling", "handling_rating", "best_melee_handling"))
        ),
        "reach": as_float(
            first_value(combined, ("reach", "weapon_length", "piece_length_sum", "best_melee_reach"))
        ),
        "weight": as_float(
            first_value(combined, ("weight", "weapon_weight", "piece_weight_sum", "best_melee_weight"))
        ),
    }
    has_thrust = as_bool(
        first_value(combined, ("has_thrust", "best_melee_has_thrust"))
    )
    missing = [key for key, value in values.items() if not math.isfinite(value)]
    if has_thrust is None:
        missing.append("has_thrust")

    thrust_damage = as_float(
        first_value(combined, ("thrust_damage", "best_melee_thrust_damage")), 0.0
    )
    thrust_speed = as_float(
        first_value(combined, ("thrust_speed", "best_melee_thrust_speed")), 0.0
    )
    if has_thrust:
        if thrust_damage <= 0:
            missing.append("thrust_damage")
        if thrust_speed <= 0:
            missing.append("thrust_speed")

    if missing:
        return ProfileResolution(
            item_id,
            family,
            "missing_exact_profile",
            "unchanged_v43",
            tuple(sorted(set(missing))),
            None,
        )

    return ProfileResolution(
        item_id,
        family,
        "applied_exact",
        "item_reference",
        (),
        WeaponProfile(
            **values,
            has_thrust=bool(has_thrust),
            thrust_damage=thrust_damage,
            thrust_speed=thrust_speed,
        ),
    )


def resolve_prior_profile(row: dict[str, object]) -> ProfileResolution:
    item_id = str(row.get("best_melee_item") or "").strip()
    if not item_id:
        return ProfileResolution("", "none", "no_melee_weapon", "none", (), None)
    damage = melee_damage(row)
    speed = as_float(row.get("v43_melee_speed"))
    family = infer_family(item_id, "", row.get("best_weapon_damage_type"))
    if not math.isfinite(damage) or not math.isfinite(speed):
        missing = []
        if not math.isfinite(damage):
            missing.append("swing_damage")
        if not math.isfinite(speed):
            missing.append("swing_speed")
        return ProfileResolution(
            item_id,
            family,
            "missing_sensitivity_input",
            "unchanged_v43",
            tuple(missing),
            None,
        )

    prior = FAMILY_PRIORS[family]
    has_thrust = bool(prior["has_thrust"])
    return ProfileResolution(
        item_id,
        family,
        "applied_family_prior",
        "low_confidence_family_prior",
        (),
        WeaponProfile(
            swing_damage=damage,
            swing_speed=speed,
            handling=float(prior["handling"]),
            reach=float(prior["reach"]),
            weight=float(prior["weight"]),
            has_thrust=has_thrust,
            thrust_damage=(
                damage * float(prior.get("thrust_damage_ratio", 0.0))
                if has_thrust
                else 0.0
            ),
            thrust_speed=(
                speed * float(prior.get("thrust_speed_ratio", 0.0))
                if has_thrust
                else 0.0
            ),
        ),
    )


def minmax100(values: list[float], mask: list[bool]) -> list[float]:
    sample = [value for value, include in zip(values, mask) if include]
    low, high = min(sample), max(sample)
    if high <= low:
        return [0.0 for _ in values]
    return [100.0 * (value - low) / (high - low) for value in values]


def weapon_offense(row: dict[str, object], melee_score: float) -> float:
    ranged = as_float(row.get("v43_ranged_carry_score"), 0.0)
    throwing = as_float(row.get("v43_throw_carry_score"), 0.0)
    mode = str(row.get("v43_weapon_mode") or "melee")
    if mode == "ranged+fallback":
        return 0.82 * ranged + 0.18 * melee_score
    if mode == "throw+melee":
        return 0.35 * throwing + 0.65 * melee_score
    return melee_score


def audit_row(
    row: dict[str, object],
    resolution: ProfileResolution,
    factor: float,
) -> dict[str, object]:
    profile = asdict(resolution.profile) if resolution.profile else {}
    return {
        "troop_id": row.get("troop_id", ""),
        "name": row.get("name", ""),
        "best_melee_item": resolution.item_id,
        "family": resolution.family,
        "kinetic_status": resolution.status,
        "profile_source": resolution.source,
        "missing_fields": "|".join(resolution.missing_fields),
        "kinetic_application_factor": round(factor, 6),
        **{f"profile_{key}": value for key, value in profile.items()},
    }


def apply_canonical(
    rows: list[dict[str, str]],
    item_lookup: dict[str, dict[str, str]],
    minimum_coverage: float,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    required = {
        "troop_id",
        "name",
        "v43_melee_mixed_kpm",
        "v43_ranged_carry_score",
        "v43_throw_carry_score",
        "v43_weapon_mode",
        "offense_v3c_norm",
        "v43_defense",
        "v43_reliability",
        "v43_emp_adjustment_robust",
        "best_melee_item",
        "best_melee_raw_damage",
    }
    missing_columns = sorted(required - set(rows[0]))
    if missing_columns:
        raise ValueError(
            "canonical mode requires the complete V4.3 output; missing columns: "
            + ", ".join(missing_columns)
        )

    resolutions = [resolve_exact_profile(row, item_lookup) for row in rows]
    eligible = [resolution.family in EXACT_SUPPORTED_FAMILIES for resolution in resolutions]
    eligible_count = sum(eligible)
    applied_count = sum(
        resolution.status == "applied_exact" for resolution in resolutions
    )
    coverage = applied_count / eligible_count if eligible_count else 1.0
    if coverage < minimum_coverage:
        raise ValueError(
            f"exact one-handed-sword profile coverage {coverage:.1%} is below "
            f"the required {minimum_coverage:.1%}"
        )

    factors = [
        kinetic_application_factor(resolution.profile, ROT_V44)
        if resolution.profile
        else 1.0
        for resolution in resolutions
    ]
    mask = [not bool(as_bool(row.get("is_giant"))) for row in rows]
    adjusted_kpm = [
        as_float(row["v43_melee_mixed_kpm"], 0.0) * factor
        for row, factor in zip(rows, factors)
    ]
    melee_scores = minmax100(adjusted_kpm, mask)
    new_weapon_offense = [
        weapon_offense(row, score) for row, score in zip(rows, melee_scores)
    ]
    offense_pre = []
    for row, score in zip(rows, new_weapon_offense):
        old_offense = as_float(row.get("offense_v3c_norm"))
        offense_pre.append(
            0.60 * old_offense + 0.40 * score
            if math.isfinite(old_offense)
            else score
        )
    integrated_offense = minmax100(offense_pre, mask)
    total_raw = [
        0.70 * offense
        + 0.18 * as_float(row.get("v43_defense"), 0.0)
        + 0.12 * as_float(row.get("v43_reliability"), 70.0)
        for row, offense in zip(rows, integrated_offense)
    ]
    totals = minmax100(total_raw, mask)
    robust_raw = [
        total + as_float(row.get("v43_emp_adjustment_robust"), 0.0)
        for row, total in zip(rows, totals)
    ]
    robust_max = max(value for value, include in zip(robust_raw, mask) if include)
    robust_totals = [100.0 * value / robust_max for value in robust_raw]

    output = []
    audit = []
    for row, resolution, factor, kpm, melee, offense, total, robust in zip(
        rows,
        resolutions,
        factors,
        adjusted_kpm,
        melee_scores,
        new_weapon_offense,
        totals,
        robust_totals,
    ):
        enriched: dict[str, object] = dict(row)
        enriched.update(
            {
                "v44_kinetic_status": resolution.status,
                "v44_kinetic_profile_source": resolution.source,
                "v44_kinetic_application_factor": round(factor, 6),
                "v44_melee_mixed_kpm": round(kpm, 6),
                "v44_melee_carry_score": round(melee, 6),
                "v44_weapon_offense_score": round(offense, 6),
                "v44_total": round(total, 6),
                "v44_robust_total": round(robust, 6),
                "v44_delta_vs_v43": round(
                    robust - as_float(row.get("v43_robust_total"), 0.0), 6
                ),
            }
        )
        output.append(enriched)
        audit.append(audit_row(row, resolution, factor))

    ranked = sorted(
        (row for row, include in zip(output, mask) if include),
        key=lambda row: (-float(row["v44_robust_total"]), str(row["troop_id"])),
    )
    for rank, row in enumerate(ranked, 1):
        row["rank_v44"] = rank
        old_rank = as_float(row.get("rank_v43"))
        row["v44_rank_change"] = (
            int(old_rank - rank) if math.isfinite(old_rank) else ""
        )

    summary = {
        "mode": "canonical",
        "rows": len(ranked),
        "eligible_exact_onehand_swords": eligible_count,
        "applied_exact_profiles": applied_count,
        "exact_profile_coverage": coverage,
        "minimum_coverage": minimum_coverage,
        "unsupported_families_remain_v43": sum(
            resolution.status == "unsupported_family"
            for resolution in resolutions
        ),
        "top_10": [
            {
                "rank_v44": row["rank_v44"],
                "name": row["name"],
                "v44_robust_total": row["v44_robust_total"],
                "rank_change": row["v44_rank_change"],
            }
            for row in ranked[:10]
        ],
    }
    return ranked, audit, summary


def apply_sensitivity(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    resolutions = [resolve_prior_profile(row) for row in rows]
    factors = [
        kinetic_application_factor(resolution.profile, ROT_V44)
        if resolution.profile
        else 1.0
        for resolution in resolutions
    ]
    adjusted_melee_raw = [
        as_float(row.get("v43_melee_carry_score"), 0.0) * factor
        for row, factor in zip(rows, factors)
    ]
    # V4.3 normalizes melee on a domain that includes zero-melee troops. The
    # preserved top 20 is incomplete, so use a zero floor and the maximum
    # visible adjusted melee value. This is directional, not canonical.
    adjusted_melee_max = max(adjusted_melee_raw) or 1.0
    adjusted_melee_scores = [
        100.0 * value / adjusted_melee_max for value in adjusted_melee_raw
    ]
    output = []
    audit = []
    for row, resolution, factor, adjusted_melee in zip(
        rows,
        resolutions,
        factors,
        adjusted_melee_scores,
    ):
        old_weapon = as_float(row.get("v43_weapon_offense_score"), 0.0)
        adjusted_weapon = weapon_offense(row, adjusted_melee)
        has_old_baseline = math.isfinite(as_float(row.get("total_v3c")))
        integration_weight = 0.40 if has_old_baseline else 1.0
        directional_delta = 0.70 * integration_weight * (adjusted_weapon - old_weapon)
        proxy = as_float(row.get("v43_robust_total"), 0.0) + directional_delta
        enriched: dict[str, object] = dict(row)
        enriched.update(
            {
                "v44_sensitivity_status": resolution.status,
                "v44_sensitivity_profile_source": resolution.source,
                "v44_kinetic_application_factor": round(factor, 6),
                "v44_melee_carry_sensitivity": round(adjusted_melee, 6),
                "v44_weapon_offense_sensitivity": round(adjusted_weapon, 6),
                "v44_directional_delta": round(directional_delta, 6),
                "v44_directional_total_proxy": round(proxy, 6),
            }
        )
        output.append(enriched)
        audit.append(audit_row(row, resolution, factor))

    proxy_max = max(float(row["v44_directional_total_proxy"]) for row in output)
    for row in output:
        row["v44_directional_total_sensitivity"] = round(
            100.0 * float(row["v44_directional_total_proxy"]) / proxy_max, 6
        )
    output.sort(
        key=lambda row: (
            -float(row["v44_directional_total_sensitivity"]),
            str(row.get("troop_id", "")),
        )
    )
    for rank, row in enumerate(output, 1):
        row["rank_v44_sensitivity_within_input"] = rank
        old_rank = as_float(row.get("rank_v43"))
        row["rank_change_within_input"] = (
            int(old_rank - rank) if math.isfinite(old_rank) else ""
        )

    summary = {
        "mode": "sensitivity_noncanonical",
        "rows": len(output),
        "profiles_from_low_confidence_family_priors": sum(
            resolution.status == "applied_family_prior"
            for resolution in resolutions
        ),
        "warning": (
            "Directional sensitivity only. Family priors and an incomplete "
            "ranking domain cannot produce a canonical V4.4 ranking."
        ),
        "top_10_within_preserved_input": [
            {
                "rank": row["rank_v44_sensitivity_within_input"],
                "name": row["name"],
                "directional_total": row["v44_directional_total_sensitivity"],
                "rank_change": row["rank_change_within_input"],
            }
            for row in output[:10]
        ],
        "largest_rank_gains_within_preserved_input": [
            {
                "name": row["name"],
                "rank_change": row["rank_change_within_input"],
            }
            for row in sorted(
                output,
                key=lambda row: -int(row["rank_change_within_input"] or 0),
            )[:5]
        ],
        "largest_rank_drops_within_preserved_input": [
            {
                "name": row["name"],
                "rank_change": row["rank_change_within_input"],
            }
            for row in sorted(
                output,
                key=lambda row: int(row["rank_change_within_input"] or 0),
            )[:5]
        ],
    }
    return output, audit, summary


def read_csv(
    path: Path,
    *,
    require_rows: bool = True,
) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if require_rows and not rows:
        raise ValueError(f"empty CSV: {path}")
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--item-reference", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path, required=True)
    parser.add_argument("--summary-output", type=Path, required=True)
    parser.add_argument(
        "--mode",
        choices=("canonical", "sensitivity"),
        default="canonical",
    )
    parser.add_argument("--minimum-exact-coverage", type=float, default=1.0)
    args = parser.parse_args()

    try:
        rows = read_csv(args.input)
        if args.mode == "canonical":
            if not args.item_reference:
                parser.error("--item-reference is required in canonical mode")
            item_lookup = build_item_lookup(
                read_csv(args.item_reference, require_rows=False)
            )
            output, audit, summary = apply_canonical(
                rows,
                item_lookup,
                args.minimum_exact_coverage,
            )
        else:
            output, audit, summary = apply_sensitivity(rows)
    except (OSError, ValueError) as error:
        parser.error(str(error))

    write_csv(args.output, output)
    write_csv(args.audit_output, audit)
    args.summary_output.parent.mkdir(parents=True, exist_ok=True)
    args.summary_output.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
