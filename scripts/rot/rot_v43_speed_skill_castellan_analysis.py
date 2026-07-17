#!/usr/bin/env python3
"""
RoT/HOT V4.3 troop and Castellan package analysis.

Core model:
- weapon damage is primary;
- weapon speed is explicit;
- skill is a marginal modifier (about 0.90-1.13 combined);
- old V3c offense stabilizes existing troops;
- partial screenshot transcriptions never use contribution index;
- Castellan rosters are grouped by upgrade-tree root.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


TARGETS = {"light": 25.15, "standard": 39.85, "heavy": 50.91}
TARGET_WEIGHTS = {"light": 0.25, "standard": 0.50, "heavy": 0.25}
EXPLICIT_NEW_CASTELLAN_ROOTS = {
    "mallister_recruit",
    "westerling_recruit",
    "grafton_recruit",
}
ROOT_LABELS = {
    "arryn_recruit": "Arryn",
    "baratheon_recruit": "Baratheon",
    "blackwood_recruit": "Blackwood",
    "casterly_guard": "Casterly Rock",
    "celtigar_recruit": "Celtigar",
    "cerwyn_volunteer": "Cerwyn",
    "clegane_recruit": "Clegane",
    "crownlands_noble_recruit": "Realm Paladin line",
    "frey_recruit": "Frey",
    "grafton_recruit": "Grafton",
    "greyjoy_recruit": "Greyjoy",
    "harlaw_recruit": "Harlaw",
    "kingsguard_page": "Kingsguard",
    "mallister_recruit": "Mallister",
    "mormont_volunteer": "Mormont",
    "norvos_initiate": "Norvos",
    "pentoshi_noble_recruit": "Pentoshi Magister",
    "river_noble_recruit": "Riverlands Noble",
    "sarnor_noble_recruit": "Sarnori Noble",
    "stark_volunteer": "Stark",
    "tarly_recruit": "Tarly",
    "tarth_recruit": "Tarth",
    "umber_volunteer": "Umber",
    "volantine_noble_recruit": "Volantene Triarch",
    "westerling_recruit": "Westerling",
}
SPEED_PRIORS = {
    "onehand_sword": 94.0,
    "onehand_axe": 86.0,
    "onehand_blunt": 84.0,
    "twohand": 82.0,
    "twohand_blunt": 78.0,
    "swing_polearm": 76.0,
    "thrust_polearm": 79.0,
    "generic_melee": 84.0,
    "throwing": 88.0,
    "bow": 90.0,
    "crossbow": 65.0,
}


def bool_series(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin({"true", "1", "yes"})


def minmax100(series: pd.Series, mask: pd.Series | None = None) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").fillna(0).astype(float)
    sample = values if mask is None else values[mask]
    low, high = sample.min(), sample.max()
    if high <= low:
        return values * 0
    return 100 * (values - low) / (high - low)


def norm_name(value: object) -> str:
    text = re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()
    return re.sub(r"\s+", " ", text)


def weighted_median(values, weights) -> float:
    values = np.asarray(values, dtype=float)
    weights = np.asarray(weights, dtype=float)
    mask = np.isfinite(values) & np.isfinite(weights) & (weights > 0)
    values, weights = values[mask], weights[mask]
    if not len(values):
        return np.nan
    order = np.argsort(values)
    values, weights = values[order], weights[order]
    cumulative = np.cumsum(weights) / weights.sum()
    return float(values[np.searchsorted(cumulative, 0.5)])


def infer_family(item_id: object, weapon_class: object, damage_type: object) -> str:
    item = str(item_id or "").lower()
    weapon_class = str(weapon_class or "").lower()
    damage_type = str(damage_type or "").lower()

    if "crossbow" in weapon_class or "crossbow" in item:
        return "crossbow"
    if weapon_class == "bow" or "bow" in weapon_class or "bow" in item:
        return "bow"
    if "javelin" in weapon_class or "throw" in weapon_class or "javelin" in item or "throwing" in item:
        return "throwing"
    if "twohandedpolearm" in weapon_class or any(x in item for x in ("halberd", "glaive", "war_scythe", "polehammer")):
        return "swing_polearm"
    if "onehandedpolearm" in weapon_class or any(x in item for x in ("spear", "pike", "lance", "polearm")):
        return "thrust_polearm"
    if "twohanded" in weapon_class or any(x in item for x in ("2haxe", "twoh", "two_h", "greatsword", "great_axe")):
        if any(x in item for x in ("hammer", "mace", "maul")):
            return "twohand_blunt"
        return "twohand"
    if "mace" in weapon_class or any(x in item for x in ("hammer", "mace", "maul", "club")):
        return "onehand_blunt"
    if "axe" in weapon_class or "axe" in item:
        return "onehand_axe"
    if "sword" in weapon_class or any(x in item for x in ("sword", "sabre", "cutlass", "kopesh")):
        return "onehand_sword"
    if damage_type == "blunt":
        return "onehand_blunt"
    return "generic_melee"


def skill_speed_modifier(skill: float) -> float:
    return float(np.clip(0.95 + float(skill) / 2500.0, 0.95, 1.08))


def skill_accuracy_modifier(skill: float) -> float:
    return float(np.clip(0.95 + float(skill) / 3000.0, 0.95, 1.05))


def damage_after_armor(raw: float, damage_type: object, armor: float) -> float:
    raw = float(raw or 0)
    if raw <= 0:
        return 0.0

    blunt_factor, pierce_resistance = {
        "cut": (0.10, 0.50),
        "pierce": (0.25, 0.33),
        "blunt": (1.00, 0.00),
    }.get(str(damage_type or "").lower(), (0.15, 0.45))

    curve = raw * 100.0 / (100.0 + armor)
    return max(
        0.0,
        curve * blunt_factor
        + max(0.0, curve - armor * pierce_resistance) * (1.0 - blunt_factor),
    )


def relevant_skill(row: pd.Series, family: str) -> float:
    if family == "bow":
        return float(row.get("Bow") or row.get("ranged_skill_v3") or 0)
    if family == "crossbow":
        return float(row.get("Crossbow") or row.get("ranged_skill_v3") or 0)
    if family == "throwing":
        return float(row.get("Throwing") or row.get("throw_skill_v3") or 0)
    if family in {"onehand_sword", "onehand_axe", "onehand_blunt"}:
        return float(row.get("OneHanded") or row.get("melee_skill_v3") or 0)
    if family in {"twohand", "twohand_blunt"}:
        return float(row.get("TwoHanded") or row.get("melee_skill_v3") or 0)
    if family in {"swing_polearm", "thrust_polearm"}:
        return float(row.get("Polearm") or row.get("melee_skill_v3") or 0)
    return float(
        max(
            row.get("OneHanded") or 0,
            row.get("TwoHanded") or 0,
            row.get("Polearm") or 0,
            row.get("melee_skill_v3") or 0,
        )
    )


def melee_application(family: str, has_shield: bool, has_horse: bool) -> float:
    base = {
        "onehand_sword": 0.88,
        "onehand_axe": 0.84,
        "onehand_blunt": 0.86,
        "twohand": 0.81,
        "twohand_blunt": 0.80,
        "swing_polearm": 0.73,
        "thrust_polearm": 0.64,
        "generic_melee": 0.77,
    }.get(family, 0.77)
    if has_shield:
        base += 0.04
    if has_horse:
        base -= 0.07
    return float(np.clip(base, 0.50, 0.95))


def build_item_lookup(item_reference: pd.DataFrame) -> dict[str, dict]:
    canonical = (
        item_reference.sort_values(["item_id", "source_confidence"])
        .drop_duplicates("item_id", keep="first")
    )
    return canonical.set_index("item_id").to_dict("index")


def infer_speed(
    item_id: object,
    family: str,
    item_lookup: dict[str, dict],
    old_melee_speed_factor: float | None = None,
) -> float:
    item = item_lookup.get(str(item_id), {})
    exact = item.get("speed_rating")
    if pd.notna(exact):
        return float(exact)

    if family not in {"bow", "crossbow", "throwing"} and pd.notna(old_melee_speed_factor):
        return float(old_melee_speed_factor) * 90.0

    speed = SPEED_PRIORS.get(family, 84.0)
    length = item.get("piece_length_sum")
    weight = item.get("piece_weight_sum")

    if pd.notna(length):
        if family in {"onehand_sword", "onehand_axe", "onehand_blunt"}:
            speed -= max(0.0, float(length) - 90.0) * 0.10
        elif family in {"twohand", "twohand_blunt", "swing_polearm", "thrust_polearm"}:
            speed -= max(0.0, float(length) - 115.0) * 0.08
    if pd.notna(weight):
        speed -= max(0.0, float(weight) - 1.5) * 4.0

    return float(np.clip(speed, 55.0, 105.0))


def calculate_melee(row: pd.Series, item_lookup: dict[str, dict]) -> dict:
    raw = float(row.get("best_melee_raw_damage") or 0)
    item_id = row.get("best_melee_item")
    damage_type = row.get("best_melee_damage_type")
    item = item_lookup.get(str(item_id), {})
    family = infer_family(item_id, item.get("weapon_class"), damage_type)

    if raw <= 0 or pd.isna(item_id):
        return {"mixed_kpm": 0.0, "standard_damage": 0.0, "standard_htk": np.nan, "speed": 0.0, "skill": 0.0, "skill_modifier": 1.0, "family": "none"}

    speed = infer_speed(item_id, family, item_lookup, row.get("melee_speed_factor_v3"))
    skill = relevant_skill(row, family)
    skill_mod = skill_speed_modifier(skill)
    attacks_per_minute = 28.0 * np.clip(speed / 90.0, 0.60, 1.25) * skill_mod
    hit_application = 0.84 * skill_accuracy_modifier(skill)
    application = melee_application(family, bool(row.get("has_shield")), bool(row.get("has_horse")))

    kpms = {}
    damages = {}
    htks = {}
    for target, armor in TARGETS.items():
        damage = damage_after_armor(raw, damage_type, armor)
        htk = 100.0 / damage if damage > 0 else np.inf
        kpm = attacks_per_minute * hit_application / htk * application if np.isfinite(htk) else 0.0
        damages[target] = damage
        htks[target] = htk
        kpms[target] = kpm

    return {
        "mixed_kpm": sum(TARGET_WEIGHTS[t] * kpms[t] for t in TARGETS),
        "standard_damage": damages["standard"],
        "standard_htk": htks["standard"],
        "speed": speed,
        "skill": skill,
        "skill_modifier": skill_mod * skill_accuracy_modifier(skill),
        "family": family,
    }


def calculate_ranged(row: pd.Series, item_lookup: dict[str, dict]) -> dict:
    raw = float(row.get("best_ranged_raw_damage") or 0)
    item_id = row.get("best_ranged_item")
    damage_type = row.get("best_ranged_damage_type")
    item = item_lookup.get(str(item_id), {})
    family = infer_family(item_id, item.get("weapon_class"), damage_type)

    if raw <= 0 or pd.isna(item_id):
        return {"mixed_kpm": 0.0, "battle_output": 0.0, "capacity_kills": 0.0, "standard_damage": 0.0, "standard_htk": np.nan, "speed": 0.0, "skill": 0.0, "skill_modifier": 1.0, "family": "none", "ammo": 0.0}

    speed = infer_speed(item_id, family, item_lookup)
    skill = relevant_skill(row, family)
    ammo = float(row.get("ammo_stack") or item.get("stack_amount") or row.get("ranged_ammo_v3") or 24)
    speed_mod = skill_speed_modifier(skill)
    accuracy_mod = skill_accuracy_modifier(skill)

    if family == "bow":
        shots_per_minute = 16.0 * np.clip(speed / 90.0, 0.65, 1.35) * speed_mod
        base_hit = 0.69
        application = 1.60
    else:
        shots_per_minute = 6.5 * np.clip(speed / 65.0, 0.55, 1.35) * speed_mod
        base_hit = 0.80
        application = 1.28

    if bool(row.get("has_horse")):
        application += 0.06

    hit_probability = float(np.clip(base_hit * accuracy_mod, 0.35, 0.95))
    uptime_minutes = 3.0

    kpms = {}
    capacities = {}
    battle_outputs = {}
    damages = {}
    htks = {}

    for target, armor in TARGETS.items():
        damage = damage_after_armor(raw, damage_type, armor)
        htk = 100.0 / damage if damage > 0 else np.inf
        kpm = shots_per_minute * hit_probability / htk * application if np.isfinite(htk) else 0.0
        capacity = ammo * hit_probability / htk if np.isfinite(htk) else 0.0
        battle_output = min(kpm * uptime_minutes, capacity)

        damages[target] = damage
        htks[target] = htk
        kpms[target] = kpm
        capacities[target] = capacity
        battle_outputs[target] = battle_output

    return {
        "mixed_kpm": sum(TARGET_WEIGHTS[t] * kpms[t] for t in TARGETS),
        "battle_output": sum(TARGET_WEIGHTS[t] * battle_outputs[t] for t in TARGETS),
        "capacity_kills": sum(TARGET_WEIGHTS[t] * capacities[t] for t in TARGETS),
        "standard_damage": damages["standard"],
        "standard_htk": htks["standard"],
        "speed": speed,
        "skill": skill,
        "skill_modifier": speed_mod * accuracy_mod,
        "family": family,
        "ammo": ammo,
    }


def calculate_throwing(row: pd.Series, item_lookup: dict[str, dict]) -> dict:
    raw = float(row.get("best_throw_raw_damage") or 0)
    item_id = row.get("best_throw_item")
    damage_type = row.get("best_throw_damage_type")

    if raw <= 0 or pd.isna(item_id):
        return {"mixed_kpm": 0.0, "battle_output": 0.0, "capacity_kills": 0.0, "standard_damage": 0.0, "standard_htk": np.nan, "speed": 0.0, "skill": 0.0, "skill_modifier": 1.0, "family": "none"}

    family = "throwing"
    speed = infer_speed(item_id, family, item_lookup)
    skill = relevant_skill(row, family)
    speed_mod = skill_speed_modifier(skill)
    accuracy_mod = skill_accuracy_modifier(skill)
    attacks_per_minute = 12.0 * (speed / 90.0) * speed_mod
    hit_probability = float(np.clip(0.64 * accuracy_mod, 0.35, 0.88))
    application = 0.76
    ammo = 4.0

    kpms = {}
    capacities = {}
    battle_outputs = {}
    damages = {}
    htks = {}

    for target, armor in TARGETS.items():
        damage = damage_after_armor(raw, damage_type, armor)
        htk = 100.0 / damage if damage > 0 else np.inf
        kpm = attacks_per_minute * hit_probability / htk * application if np.isfinite(htk) else 0.0
        capacity = ammo * hit_probability / htk if np.isfinite(htk) else 0.0
        battle_output = min(kpm * 0.75, capacity)

        damages[target] = damage
        htks[target] = htk
        kpms[target] = kpm
        capacities[target] = capacity
        battle_outputs[target] = battle_output

    return {
        "mixed_kpm": sum(TARGET_WEIGHTS[t] * kpms[t] for t in TARGETS),
        "battle_output": sum(TARGET_WEIGHTS[t] * battle_outputs[t] for t in TARGETS),
        "capacity_kills": sum(TARGET_WEIGHTS[t] * capacities[t] for t in TARGETS),
        "standard_damage": damages["standard"],
        "standard_htk": htks["standard"],
        "speed": speed,
        "skill": skill,
        "skill_modifier": speed_mod * accuracy_mod,
        "family": family,
    }


def robust_empirical(empirical: pd.DataFrame, theoretical: pd.DataFrame) -> pd.DataFrame:
    clean = empirical[
        (~bool_series(empirical["is_hero_or_companion"]))
        & (~bool_series(empirical["is_garrison_party"]))
        & (~bool_series(empirical["is_militia_troop"]))
        & empirical["confidence_level"].isin(["high", "medium", "unknown"])
    ].copy()

    clean["verified_full_side"] = clean["side_total_kills"].notna() & clean["side_total_present"].notna()
    clean["kpp_raw"] = clean["kills"] / clean["estimated_present"].replace(0, np.nan)
    cap = float(clean["kpp_raw"].quantile(0.95))
    clean["kpp_winsor"] = clean["kpp_raw"].clip(upper=cap)
    clean["survival_factor"] = (
        1 - clean["death_rate"].fillna(0) - 0.35 * clean["wounded_rate"].fillna(0)
    ).clip(lower=0)
    clean["survival_kpp_winsor"] = clean["kpp_winsor"] * clean["survival_factor"]

    global_kpp = float(np.average(clean["kpp_winsor"], weights=clean["estimated_present"]))
    global_survival = float(np.average(clean["survival_kpp_winsor"], weights=clean["estimated_present"]))

    rows = []
    prior_exposure = 20

    for troop_name, group in clean.groupby("troop_name"):
        total_present = float(group["estimated_present"].sum())
        winsor_equivalent = float((group["kpp_winsor"] * group["estimated_present"]).sum())
        survival_equivalent = float((group["survival_kpp_winsor"] * group["estimated_present"]).sum())
        full = group[group["verified_full_side"] & (group["estimated_present"] >= 3)]

        rows.append({
            "troop_name": troop_name,
            "rows": len(group),
            "battles": group["battle_id"].nunique(),
            "total_present": total_present,
            "total_kills": float(group["kills"].sum()),
            "raw_overall_kpp": float(group["kills"].sum() / total_present),
            "winsorized_overall_kpp": float(winsor_equivalent / total_present),
            "shrunk_kpp": float((winsor_equivalent + prior_exposure * global_kpp) / (total_present + prior_exposure)),
            "shrunk_survival_kpp": float((survival_equivalent + prior_exposure * global_survival) / (total_present + prior_exposure)),
            "median_kpp": float(group["kpp_raw"].median()),
            "full_side_battles": full["battle_id"].nunique(),
            "full_side_ci_median": float(full["contribution_index"].median()) if len(full) else np.nan,
            "full_side_ci_weighted_median": weighted_median(
                full["contribution_index"], np.minimum(full["estimated_present"], 12)
            ) if len(full) else np.nan,
            "full_side_campaign_ci_median": float(full["campaign_contribution"].median()) if len(full) else np.nan,
            "mean_death_rate": float(group["death_rate"].fillna(0).mean()),
            "mean_wounded_rate": float(group["wounded_rate"].fillna(0).mean()),
            "empirical_confidence": (
                0.5 * min(1, total_present / 80)
                + 0.3 * min(1, group["battle_id"].nunique() / 6)
                + 0.2 * min(1, full["battle_id"].nunique() / 3)
            ),
            "outlier_rows_over_cap": int((group["kpp_raw"] > cap).sum()),
            "tiny_rows_present_le2": int((group["estimated_present"] <= 2).sum()),
        })

    result = pd.DataFrame(rows)
    result["join_name"] = result["troop_name"].map(norm_name)
    result = result.merge(
        theoretical[["troop_id", "name", "v43_total", "join_name", "baseline_status"]],
        on="join_name",
        how="left",
    )

    matched = result["troop_id"].notna()
    for column in ("shrunk_kpp", "shrunk_survival_kpp", "median_kpp"):
        result.loc[matched, f"{column}_pct"] = result.loc[matched, column].rank(pct=True)

    result["full_ci_pct"] = 0.5
    available = matched & result["full_side_ci_weighted_median"].notna()
    result.loc[available, "full_ci_pct"] = result.loc[available, "full_side_ci_weighted_median"].rank(pct=True)

    result["empirical_score_robust"] = 100 * (
        0.45 * result["shrunk_kpp_pct"].fillna(0.5)
        + 0.35 * result["shrunk_survival_kpp_pct"].fillna(0.5)
        + 0.15 * result["full_ci_pct"].fillna(0.5)
        + 0.05 * result["median_kpp_pct"].fillna(0.5)
    )

    delta = result["empirical_score_robust"] - result["v43_total"]
    confidence = result["empirical_confidence"] * (
        0.75 + 0.25 * np.minimum(1, result["full_side_battles"] / 2)
    )
    adjustment = (delta * 0.18 * confidence).clip(-8, 8)

    positive_eligible = (result["battles"] >= 4) & (result["total_present"] >= 30)
    negative_eligible = (
        ((result["full_side_battles"] >= 2) | (result["total_present"] >= 80))
        & (result["battles"] >= 4)
    )
    adjustment = np.where((adjustment > 0) & (~positive_eligible), 0, adjustment)
    adjustment = np.where((adjustment < 0) & (~negative_eligible), 0, adjustment)

    outlier_fraction = result["outlier_rows_over_cap"] / result["rows"].replace(0, np.nan)
    adjustment = np.where(adjustment > 0, adjustment * (1 - 0.5 * outlier_fraction.fillna(0)), adjustment)
    adjustment = np.where(result["troop_name"].eq("Ravens' Teeth"), 0, adjustment)
    adjustment = np.where(result["troop_name"].eq("Lyseni Enforcer"), np.maximum(adjustment, -5), adjustment)

    result["robust_empirical_adjustment"] = adjustment
    result.attrs["kpp_cap"] = cap
    return result


def practical_branch_score(
    theory_score: float,
    empirical_score: float | None,
    confidence: float,
    full_side_battles: int,
    total_present: float,
    battles: int,
) -> float:
    """Apply cautious empirical upside/downside to one castle role branch."""
    theory = float(theory_score or 0)
    if pd.isna(empirical_score) or battles < 3 or total_present < 10:
        return theory

    delta = float(empirical_score) - theory
    confidence = float(np.clip(confidence or 0, 0, 1))

    if delta > 0:
        return theory + min(15.0, 0.35 * delta * confidence)

    # Negative package adjustments require either verified full-side samples
    # or substantial exposure. This avoids punishing troops from partial tables.
    if full_side_battles >= 2 or total_present >= 80:
        return max(0.0, theory + max(-10.0, 0.20 * delta * confidence))

    return theory


def graph_roots_and_descendants(
    troops_all: pd.DataFrame,
    upgrade_edges: pd.DataFrame,
    terminal_audit: pd.DataFrame,
    castellan_troop_ids: set[str],
):
    rot_ids = set(troops_all.loc[troops_all["source_module"].eq("ROT-Content"), "troop_id"])
    edges = upgrade_edges[
        upgrade_edges["source_troop_id"].isin(rot_ids)
        & upgrade_edges["target_troop_id"].isin(rot_ids)
    ]

    parents = defaultdict(set)
    children = defaultdict(set)
    for row in edges.itertuples():
        parents[row.target_troop_id].add(row.source_troop_id)
        children[row.source_troop_id].add(row.target_troop_id)

    terminal_ids = set(terminal_audit["troop_id"])

    def roots_for(troop_id: str) -> set[str]:
        roots = set()
        stack = [troop_id]
        seen = set()
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            current_parents = parents.get(current, set())
            if not current_parents:
                roots.add(current)
            else:
                stack.extend(current_parents)
        return roots

    def descendants(root_id: str) -> set[str]:
        output = set()
        stack = [root_id]
        seen = set()
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            if current in terminal_ids:
                output.add(current)
            stack.extend(children.get(current, set()))
        return output

    roots = set(EXPLICIT_NEW_CASTELLAN_ROOTS)
    for troop_id in castellan_troop_ids:
        roots |= roots_for(troop_id)

    return roots, descendants


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--weapon-summary", type=Path, required=True)
    parser.add_argument("--item-reference", type=Path, required=True)
    parser.add_argument("--troop-audit", type=Path, required=True)
    parser.add_argument("--v41", type=Path, required=True)
    parser.add_argument("--v3c", type=Path, required=True)
    parser.add_argument("--troops-all", type=Path, required=True)
    parser.add_argument("--upgrade-edges", type=Path, required=True)
    parser.add_argument("--terminal-audit", type=Path, required=True)
    parser.add_argument("--empirical-segmented", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("data/rot_reference/hot_v43"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    weapon = pd.read_csv(args.weapon_summary)
    item_reference = pd.read_csv(args.item_reference)
    troop_audit = pd.read_csv(args.troop_audit)
    v41 = pd.read_csv(args.v41)
    v3c = pd.read_csv(args.v3c)
    troops_all = pd.read_csv(args.troops_all)
    upgrade_edges = pd.read_csv(args.upgrade_edges)
    terminal_audit = pd.read_csv(args.terminal_audit)

    item_lookup = build_item_lookup(item_reference)

    merged = (
        weapon.merge(
            troop_audit[[
                "troop_id", "OneHanded", "TwoHanded", "Polearm", "Bow", "Crossbow",
                "Throwing", "Athletics", "Riding", "has_horse", "has_shield",
                "default_group", "audit_category", "baseline_status",
            ]],
            on="troop_id",
            how="left",
            suffixes=("", "_troop"),
        )
        .merge(
            v41[[
                "troop_id", "total_v41_integrated", "offense_v41_integrated",
                "defense_score_v41", "reliability_score_v41", "castellan",
                "possible_special_access", "excluded_from_likely_campaign",
                "is_likely_new_hot", "is_militia",
            ]],
            on="troop_id",
            how="left",
        )
        .merge(
            v3c[[
                "troop_id", "total_v3c", "offense_v3c_norm", "defense_norm",
                "reliability_v3", "v3c_best_mode", "melee_speed_factor_v3",
                "melee_skill_v3", "ranged_speed_v3", "ranged_skill_v3",
                "ranged_accuracy_v3", "ranged_ammo_v3", "throw_skill_v3",
            ]],
            on="troop_id",
            how="left",
        )
    )

    melee = merged.apply(lambda row: calculate_melee(row, item_lookup), axis=1, result_type="expand").add_prefix("v43_melee_")
    ranged = merged.apply(lambda row: calculate_ranged(row, item_lookup), axis=1, result_type="expand").add_prefix("v43_ranged_")
    throwing = merged.apply(lambda row: calculate_throwing(row, item_lookup), axis=1, result_type="expand").add_prefix("v43_throw_")
    result = merged.join(melee).join(ranged).join(throwing)

    rank_mask = ~bool_series(result["is_giant"])
    result["v43_melee_kpm_score"] = minmax100(result["v43_melee_mixed_kpm"], rank_mask)
    result["v43_ranged_kpm_score"] = minmax100(result["v43_ranged_mixed_kpm"], rank_mask)
    result["v43_ranged_battle_score"] = minmax100(result["v43_ranged_battle_output"], rank_mask)
    result["v43_ranged_capacity_score"] = minmax100(result["v43_ranged_capacity_kills"], rank_mask)
    result["v43_throw_kpm_score"] = minmax100(result["v43_throw_mixed_kpm"], rank_mask)
    result["v43_throw_battle_score"] = minmax100(result["v43_throw_battle_output"], rank_mask)

    result["v43_ranged_carry_score"] = (
        0.50 * result["v43_ranged_kpm_score"]
        + 0.35 * result["v43_ranged_battle_score"]
        + 0.15 * result["v43_ranged_capacity_score"]
    )
    result["v43_melee_carry_score"] = result["v43_melee_kpm_score"]
    result["v43_throw_carry_score"] = (
        0.45 * result["v43_throw_kpm_score"]
        + 0.55 * result["v43_throw_battle_score"]
    )
    result["v43_meaningful_throwing"] = result["v43_throw_standard_damage"] >= 25

    has_ranged = result["v43_ranged_mixed_kpm"] > 0
    has_throwing = result["v43_meaningful_throwing"]
    result["v43_weapon_offense_score"] = np.select(
        [has_ranged, has_throwing],
        [
            0.82 * result["v43_ranged_carry_score"] + 0.18 * result["v43_melee_carry_score"],
            0.35 * result["v43_throw_carry_score"] + 0.65 * result["v43_melee_carry_score"],
        ],
        default=result["v43_melee_carry_score"],
    )
    result["v43_weapon_mode"] = np.select(
        [has_ranged, has_throwing],
        ["ranged+fallback", "throw+melee"],
        default="melee",
    )

    old_offense = pd.to_numeric(result["offense_v3c_norm"], errors="coerce")
    result["v43_offense_pre"] = np.where(
        old_offense.notna(),
        0.60 * old_offense.fillna(0) + 0.40 * result["v43_weapon_offense_score"],
        result["v43_weapon_offense_score"],
    )
    result["v43_offense_integrated"] = minmax100(result["v43_offense_pre"], rank_mask)

    fallback_defense = minmax100(
        pd.to_numeric(result["armor_total"], errors="coerce").fillna(0) * 0.75
        + pd.to_numeric(result["shield_hp_max"], errors="coerce").fillna(0) / 8,
        rank_mask,
    )
    result["v43_defense"] = pd.to_numeric(result["defense_score_v41"], errors="coerce").fillna(fallback_defense)
    result["v43_reliability"] = pd.to_numeric(result["reliability_score_v41"], errors="coerce").fillna(70)
    result["v43_total_raw"] = (
        0.70 * result["v43_offense_integrated"]
        + 0.18 * result["v43_defense"]
        + 0.12 * result["v43_reliability"]
    )
    result["v43_total"] = minmax100(result["v43_total_raw"], rank_mask)
    result["join_name"] = result["name"].map(norm_name)

    empirical_audit = None
    if args.empirical_segmented:
        empirical = pd.read_csv(args.empirical_segmented)
        empirical_audit = robust_empirical(empirical, result)
        adjustment_map = empirical_audit.dropna(subset=["troop_id"]).set_index("troop_id")["robust_empirical_adjustment"]
        result["v43_emp_adjustment_robust"] = result["troop_id"].map(adjustment_map).fillna(0)
    else:
        result["v43_emp_adjustment_robust"] = 0.0

    result["v43_robust_raw"] = result["v43_total"] + result["v43_emp_adjustment_robust"]
    result["v43_robust_total"] = (
        100 * result["v43_robust_raw"] / result.loc[rank_mask, "v43_robust_raw"].max()
    )

    ranked = result[rank_mask].sort_values("v43_robust_total", ascending=False).copy()
    ranked.insert(0, "rank_v43", range(1, len(ranked) + 1))
    ranked.to_csv(args.output_dir / "rot_hot_v43_all_humanoid_ranked.csv", index=False)
    ranked.head(20).to_csv(args.output_dir / "rot_hot_v43_top20_overall.csv", index=False)

    likely = ranked[
        (~bool_series(ranked["castellan"]))
        & (~bool_series(ranked["possible_special_access"]))
        & (~bool_series(ranked["is_militia_y"] if "is_militia_y" in ranked else ranked["is_militia"]))
    ].copy()
    likely.insert(0, "rank_likely_campaign", range(1, len(likely) + 1))
    likely.to_csv(args.output_dir / "rot_hot_v43_likely_campaign_ranked.csv", index=False)

    if empirical_audit is not None:
        empirical_audit.to_csv(args.output_dir / "rot_empirical_robust_metric_audit.csv", index=False)

    castellan_ids = set(ranked.loc[bool_series(ranked["castellan"]), "troop_id"])
    roots, descendants = graph_roots_and_descendants(
        troops_all, upgrade_edges, terminal_audit, castellan_ids
    )

    name_lookup = troops_all.set_index("troop_id")["name"].to_dict()
    ranked_lookup = ranked.set_index("troop_id")
    empirical_lookup = (
        empirical_audit.dropna(subset=["troop_id"]).set_index("troop_id").to_dict("index")
        if empirical_audit is not None
        else {}
    )
    troop_rows = []

    for root in sorted(roots):
        house = ROOT_LABELS.get(root, name_lookup.get(root, root))
        for troop_id in sorted(descendants(root)):
            if troop_id not in ranked_lookup.index:
                continue
            row = ranked_lookup.loc[troop_id]
            has_ranged = row.get("v43_ranged_mixed_kpm", 0) > 0
            has_horse = bool(row.get("has_horse"))
            role = "ranged" if has_ranged else ("cavalry" if has_horse else "infantry")

            ranged_score = (
                0.75 * row.get("v43_ranged_carry_score", 0)
                + 0.15 * row.get("v43_melee_carry_score", 0)
                + 0.10 * row.get("v43_defense", 0)
            ) if role == "ranged" else 0
            infantry_score = (
                0.55 * row.get("v43_melee_carry_score", 0)
                + 0.35 * row.get("v43_defense", 0)
                + 0.10 * row.get("v43_reliability", 0)
            ) if role == "infantry" else 0
            cavalry_score = (
                0.45 * row.get("v43_melee_carry_score", 0)
                + 0.30 * row.get("v43_defense", 0)
                + 0.10 * row.get("v43_reliability", 0)
                + 0.15 * row.get("v43_ranged_carry_score", 0)
            ) * 0.85 if role == "cavalry" else 0

            branch_theory = {
                "ranged": ranged_score,
                "infantry": infantry_score,
                "cavalry": cavalry_score,
            }[role]
            empirical_row = empirical_lookup.get(troop_id, {})
            branch_practical = practical_branch_score(
                branch_theory,
                empirical_row.get("empirical_score_robust", np.nan),
                empirical_row.get("empirical_confidence", 0),
                int(empirical_row.get("full_side_battles", 0) or 0),
                float(empirical_row.get("total_present", 0) or 0),
                int(empirical_row.get("battles", 0) or 0),
            )

            troop_rows.append({
                "castle_root_id": root,
                "castle_house": house,
                "troop_id": troop_id,
                "troop_name": row["name"],
                "role": role,
                "v43_total_theory": row["v43_total"],
                "v43_emp_adjustment": row["v43_emp_adjustment_robust"],
                "v43_total_robust": row["v43_robust_total"],
                "ranged_branch_score": ranged_score,
                "infantry_branch_score": infantry_score,
                "cavalry_branch_score": cavalry_score,
                "v43_ranged_carry_score": row.get("v43_ranged_carry_score", 0),
                "v43_melee_carry_score": row.get("v43_melee_carry_score", 0),
                "v43_defense": row.get("v43_defense", 0),
                "v43_reliability": row.get("v43_reliability", 0),
                "best_weapon_item": row.get("best_weapon_item"),
                "best_mode": row.get("v43_weapon_mode"),
                "empirical_score_robust": empirical_row.get("empirical_score_robust", np.nan),
                "empirical_confidence": empirical_row.get("empirical_confidence", 0),
                "emp_full_side_battles": empirical_row.get("full_side_battles", 0),
                "emp_total_present": empirical_row.get("total_present", 0),
                "emp_battles": empirical_row.get("battles", 0),
                "practical_branch_score": branch_practical,
            })

    castle_troops = pd.DataFrame(troop_rows)
    castle_troops.to_csv(args.output_dir / "rot_castellan_terminal_troops_v43.csv", index=False)

    house_rows = []
    for root, group in castle_troops.groupby("castle_root_id"):
        scores = sorted(group["v43_total_robust"], reverse=True)
        peak_row = group.sort_values("v43_total_robust", ascending=False).iloc[0]
        peak = scores[0] if scores else 0
        second = scores[1] if len(scores) > 1 else 0
        third = scores[2] if len(scores) > 2 else 0

        def best_role(role_name: str, score_column: str):
            subset = group[group["role"].eq(role_name)]
            if subset.empty:
                return 0.0, ""
            best = subset.sort_values(score_column, ascending=False).iloc[0]
            return float(best[score_column]), str(best["troop_name"])

        ranged_theory, ranged_troop = best_role("ranged", "ranged_branch_score")
        infantry_theory, infantry_troop = best_role("infantry", "infantry_branch_score")
        cavalry_theory, cavalry_troop = best_role("cavalry", "cavalry_branch_score")
        ranged_practical, _ = best_role("ranged", "practical_branch_score")
        infantry_practical, _ = best_role("infantry", "practical_branch_score")
        cavalry_practical, _ = best_role("cavalry", "practical_branch_score")

        coverage = 100 * sum(x > 0 for x in (ranged_theory, infantry_theory, cavalry_theory)) / 3
        package_theory = (
            0.32 * ranged_theory
            + 0.32 * infantry_theory
            + 0.10 * cavalry_theory
            + 0.16 * peak
            + 0.05 * second
            + 0.05 * coverage
        )
        package_practical = (
            0.32 * ranged_practical
            + 0.32 * infantry_practical
            + 0.10 * cavalry_practical
            + 0.16 * peak
            + 0.05 * second
            + 0.05 * coverage
        )
        house_rows.append({
            "castle_root_id": root,
            "castle_house": group["castle_house"].iloc[0],
            "terminal_count": len(group),
            "ranged_branch_theory": ranged_theory,
            "infantry_branch_theory": infantry_theory,
            "cavalry_branch_theory": cavalry_theory,
            "ranged_branch_practical": ranged_practical,
            "infantry_branch_practical": infantry_practical,
            "cavalry_branch_practical": cavalry_practical,
            "peak_troop": peak_row["troop_name"],
            "peak_score": peak,
            "second_score": second,
            "third_score": third,
            "role_coverage": coverage,
            "castle_package_theory_raw": package_theory,
            "castle_package_practical_raw": package_practical,
            "ranged_troop": ranged_troop,
            "infantry_troop": infantry_troop,
            "cavalry_troop": cavalry_troop,
        })

    houses = pd.DataFrame(house_rows)
    full_houses = houses[houses["terminal_count"] >= 3].copy()
    full_houses["castle_package_theory"] = (
        100 * full_houses["castle_package_theory_raw"] / full_houses["castle_package_theory_raw"].max()
    )
    full_houses["castle_package_practical"] = (
        100 * full_houses["castle_package_practical_raw"] / full_houses["castle_package_practical_raw"].max()
    )
    full_houses = full_houses.sort_values("castle_package_practical", ascending=False)
    full_houses.insert(0, "rank_castle_package", range(1, len(full_houses) + 1))
    full_houses.to_csv(args.output_dir / "rot_castellan_house_package_ranking_v43.csv", index=False)

    single_line = houses[houses["terminal_count"] < 3].copy()
    single_line = single_line.sort_values("peak_score", ascending=False)
    single_line.to_csv(args.output_dir / "rot_castellan_single_line_elites_v43.csv", index=False)

    summary = {
        "humanoid_ranked": len(ranked),
        "likely_campaign": len(likely),
        "castellan_full_trees": len(full_houses),
        "top_overall": ranked[["rank_v43", "name", "v43_robust_total"]].head(10).to_dict("records"),
        "top_castellan_packages": full_houses[["rank_castle_package", "castle_house", "castle_package_practical"]].head(10).to_dict("records"),
    }
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("RoT/HOT V4.3 analysis complete.")
    print(f"Humanoid troops: {len(ranked)}")
    print(f"Full Castellan trees: {len(full_houses)}")
    print(f"Output: {args.output_dir}")


if __name__ == "__main__":
    main()
