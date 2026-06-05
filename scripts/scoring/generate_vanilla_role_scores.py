from __future__ import annotations

import argparse
import numpy as np
import pandas as pd
from pathlib import Path

ROLE_COLS = [
    "ranged_role_score",
    "defensive_role_score",
    "offensive_melee_role_score",
    "skirmisher_role_score",
]

CONTROL_IDS = [
    "battanian_fian_champion",
    "khuzait_khans_guard",
    "imperial_legionary",
    "vlandian_sergeant",
    "vlandian_sharpshooter",
    "imperial_elite_cataphract",
    "vlandian_banner_knight",
    "druzhinnik_champion",
    "aserai_vanguard_faris",
    "khuzait_darkhan",
]


def norm100(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").fillna(0).astype(float)
    low = values.min()
    high = values.max()
    if high <= low:
        return values * 0
    return 100 * (values - low) / (high - low)


def boolish(value) -> bool:
    return str(value).lower() in {"true", "1", "yes"}


def crafted_class(template) -> str:
    value = str(template or "")
    if "TwoHandedPolearm" in value:
        return "two_handed_polearm"
    if "TwoHandedSword" in value:
        return "two_handed_sword"
    if "OneHandedPolearm" in value:
        return "one_handed_polearm"
    if "OneHandedSword" in value:
        return "one_handed_sword"
    if "Mace" in value:
        return "mace"
    if "Axe" in value:
        return "axe"
    if "Javelin" in value:
        return "javelin"
    if "Throwing" in value:
        return "throwing"
    return "other"


def melee_proxy(template) -> float:
    table = {
        "two_handed_polearm": 58,
        "two_handed_sword": 60,
        "one_handed_polearm": 44,
        "one_handed_sword": 44,
        "mace": 43,
        "axe": 46,
        "javelin": 36,
        "throwing": 34,
        "other": 40,
    }
    return table.get(crafted_class(template), 40)


def melee_usability(template) -> float:
    table = {
        "two_handed_polearm": 0.78,
        "two_handed_sword": 0.92,
        "one_handed_polearm": 0.70,
        "one_handed_sword": 0.95,
        "mace": 0.90,
        "axe": 0.88,
        "javelin": 0.55,
        "throwing": 0.55,
        "other": 0.75,
    }
    return table.get(crafted_class(template), 0.75)


def max_numeric(df: pd.DataFrame, column: str) -> float:
    if df.empty or column not in df.columns:
        return 0.0
    return float(pd.to_numeric(df[column], errors="coerce").fillna(0).max())


def join_unique(values) -> str:
    clean = sorted({str(v) for v in values.dropna() if str(v) != "nan" and str(v) != ""})
    return "|".join(clean)


def build_roster_features(audit: pd.DataFrame, soldiers: set[str], depths: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for (troop_id, roster_index), group in audit.groupby(["troop_id", "roster_index"], dropna=False):
        if troop_id not in soldiers:
            continue

        first = group.iloc[0]
        weapons = group[group["slot"].astype(str).str.startswith("Item", na=False)].copy()
        armor = group[group["slot"].isin(["Head", "Body", "Gloves", "Leg", "Cape"])].copy()
        horse = group[group["slot"].eq("Horse")].copy()
        harness = group[group["slot"].eq("HorseHarness")].copy()
        shield = weapons[weapons["type"].eq("Shield")].copy()
        ranged = weapons[weapons["type"].isin(["Bow", "Crossbow"])].copy()
        ammo = weapons[weapons["type"].isin(["Arrows", "Bolts"])].copy()
        direct_throw = weapons[weapons["type"].eq("Thrown")].copy()
        crafted = weapons[weapons["item_kind"].eq("CraftedItem")].copy()

        armor_head = max_numeric(armor, "head_armor") if False else pd.to_numeric(armor.get("head_armor", 0), errors="coerce").fillna(0).sum()
        armor_body = pd.to_numeric(armor.get("body_armor", 0), errors="coerce").fillna(0).sum()
        armor_arm = pd.to_numeric(armor.get("arm_armor", 0), errors="coerce").fillna(0).sum()
        armor_leg = pd.to_numeric(armor.get("leg_armor", 0), errors="coerce").fillna(0).sum()
        effective_armor = 0.20 * armor_head + 0.65 * armor_body + 0.10 * armor_arm + 0.05 * armor_leg

        shield_hp = max_numeric(shield, "hit_points")
        shield_armor = max_numeric(shield, "shield_armor")
        horse_speed = max_numeric(horse, "horse_speed")
        horse_charge = max_numeric(horse, "horse_charge_damage")
        horse_maneuver = max_numeric(horse, "horse_maneuver")
        harness_armor = max_numeric(harness, "body_armor")

        defense_raw = (
            effective_armor * 1.25
            + (shield_hp / 35 if not shield.empty else 0)
            + shield_armor * 1.1
            + harness_armor * 0.45
            + ((horse_charge * 0.25 + horse_speed * 0.06 + horse_maneuver * 0.04) if not horse.empty else 0)
        )

        best_ranged = {}
        ammo_stack = max_numeric(ammo, "stack_amount") if not ammo.empty else 0
        if not ranged.empty:
            r = ranged.copy()
            r["base_damage"] = r[["swing_damage", "thrust_damage"]].apply(pd.to_numeric, errors="coerce").fillna(0).max(axis=1)
            ammo_bonus = max_numeric(ammo, "thrust_damage") if not ammo.empty else 0
            ammo_stack = pd.to_numeric(ammo.get("stack_amount", 0), errors="coerce").fillna(0).sum()
            r["ranged_damage_real"] = r["base_damage"] + ammo_bonus
            r["ranged_raw"] = (
                r["ranged_damage_real"]
                + pd.to_numeric(r["speed_rating"], errors="coerce").fillna(0) * 0.35
                + pd.to_numeric(r["accuracy"], errors="coerce").fillna(90) * 0.15
                + pd.to_numeric(r["missile_speed"], errors="coerce").fillna(80) * 0.10
                + min(float(ammo_stack), 64) * 0.25
            )
            best_ranged = r.sort_values("ranged_raw", ascending=False).iloc[0].to_dict()

        best_crafted = {}
        best_crafted_throw = {}
        if not crafted.empty:
            c = crafted.copy()
            c["crafted_class"] = c["crafting_template"].apply(crafted_class)
            c["melee_proxy"] = c["crafting_template"].apply(melee_proxy)
            c["melee_usability"] = c["crafting_template"].apply(melee_usability)
            c["melee_raw"] = c["melee_proxy"] * c["melee_usability"]
            c["is_throwing_crafted"] = c["crafted_class"].isin(["javelin", "throwing"])
            melee_c = c[~c["is_throwing_crafted"]]
            throw_c = c[c["is_throwing_crafted"]].copy()
            if not melee_c.empty:
                best_crafted = melee_c.sort_values("melee_raw", ascending=False).iloc[0].to_dict()
            if not throw_c.empty:
                throw_c["throw_proxy_raw"] = throw_c["melee_proxy"] * 0.55
                best_crafted_throw = throw_c.sort_values("throw_proxy_raw", ascending=False).iloc[0].to_dict()

        best_direct_throw = {}
        if not direct_throw.empty:
            t = direct_throw.copy()
            t["throw_damage_real"] = t[["swing_damage", "thrust_damage"]].apply(pd.to_numeric, errors="coerce").fillna(0).max(axis=1)
            t["throw_raw"] = t["throw_damage_real"] + pd.to_numeric(t["speed_rating"], errors="coerce").fillna(0) * 0.20 + pd.to_numeric(t["stack_amount"], errors="coerce").fillna(0) * 0.50
            best_direct_throw = t.sort_values("throw_raw", ascending=False).iloc[0].to_dict()

        rows.append({
            "troop_id": troop_id,
            "troop_name": first.get("troop_name"),
            "level": first.get("level"),
            "culture": first.get("culture"),
            "default_group": first.get("default_group"),
            "roster_index": roster_index,
            "OneHanded": float(first.get("OneHanded") or 0),
            "TwoHanded": float(first.get("TwoHanded") or 0),
            "Polearm": float(first.get("Polearm") or 0),
            "Bow": float(first.get("Bow") or 0),
            "Crossbow": float(first.get("Crossbow") or 0),
            "Throwing": float(first.get("Throwing") or 0),
            "Riding": float(first.get("Riding") or 0),
            "Athletics": float(first.get("Athletics") or 0),
            "has_shield": not shield.empty,
            "has_horse": not horse.empty,
            "has_bow": bool((weapons["type"] == "Bow").any()),
            "has_crossbow": bool((weapons["type"] == "Crossbow").any()),
            "has_ranged": not ranged.empty,
            "has_throwing": (not direct_throw.empty) or bool(best_crafted_throw),
            "defense_raw": defense_raw,
            "ranged_item": best_ranged.get("item_id"),
            "ranged_raw": best_ranged.get("ranged_raw", 0),
            "ammo_stack": ammo_stack,
            "crafted_melee_item": best_crafted.get("item_id"),
            "crafted_melee_template": best_crafted.get("crafting_template"),
            "crafted_melee_class": best_crafted.get("crafted_class"),
            "crafted_melee_raw": best_crafted.get("melee_raw", 0),
            "direct_throw_item": best_direct_throw.get("item_id"),
            "direct_throw_raw": best_direct_throw.get("throw_raw", 0),
            "crafted_throw_item": best_crafted_throw.get("item_id"),
            "crafted_throw_raw": best_crafted_throw.get("throw_proxy_raw", 0),
        })

    result = pd.DataFrame(rows)
    return result.merge(depths[["troop_id", "tree_root_id", "upgrade_depth", "line_status"]], on="troop_id", how="left")


def build_role_scores(rosters: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = rosters.copy()
    df["defense_score_base"] = norm100(df["defense_raw"])
    df["ranged_score_base"] = norm100(df["ranged_raw"])
    df["crafted_melee_score_base"] = norm100(df["crafted_melee_raw"])
    df["throw_score_base"] = norm100(df[["direct_throw_raw", "crafted_throw_raw"]].max(axis=1))

    df["ranged_skill_factor"] = (df[["Bow", "Crossbow"]].max(axis=1) / 220).clip(0.25, 1.15)
    df["melee_skill_factor"] = (df[["OneHanded", "TwoHanded", "Polearm"]].max(axis=1) / 220).clip(0.25, 1.15)
    df["throw_skill_factor"] = (df["Throwing"] / 160).clip(0.25, 1.20)
    df["mobility_factor"] = (1 + np.where(df["has_horse"], 0.08, 0) + df["Riding"].fillna(0) / 1000).clip(1.0, 1.25)

    df["ranged_role_score"] = df["ranged_score_base"] * 0.78 * df["ranged_skill_factor"] * df["mobility_factor"] + df["defense_score_base"] * 0.10 + np.where(df["has_horse"], 8, 0) + np.where(df["has_shield"], 3, 0)
    df["defensive_role_score"] = df["defense_score_base"] * 0.72 + df["crafted_melee_score_base"] * 0.12 + df["throw_score_base"] * 0.04 + np.where(df["has_shield"], 12, 0) + np.where(df["has_horse"], 6, 0)
    df["offensive_melee_role_score"] = df["crafted_melee_score_base"] * 0.70 * df["melee_skill_factor"] + df["defense_score_base"] * 0.10 + np.where(df["has_horse"], 4, 0) - np.where(df["crafted_melee_class"].eq("one_handed_polearm"), 8, 0)
    df["skirmisher_role_score"] = df["throw_score_base"] * 0.65 * df["throw_skill_factor"] + df["crafted_melee_score_base"] * 0.15 + df["defense_score_base"] * 0.10 + np.where(df["has_horse"], 6, 0)

    df.loc[~df["has_ranged"], "ranged_role_score"] = np.nan
    df.loc[~(df["has_shield"] | df["has_horse"] | (df["defense_score_base"] >= 55)), "defensive_role_score"] = np.nan
    df.loc[df["crafted_melee_item"].isna(), "offensive_melee_role_score"] = np.nan
    df.loc[~df["has_throwing"], "skirmisher_role_score"] = np.nan

    for col in ROLE_COLS:
        mask = df[col].notna()
        df.loc[mask, col] = norm100(df.loc[mask, col])

    agg = df.groupby("troop_id").agg({
        "troop_name": "first",
        "level": "first",
        "upgrade_depth": "first",
        "line_status": "first",
        "culture": "first",
        "default_group": "first",
        "has_bow": "max",
        "has_crossbow": "max",
        "has_ranged": "max",
        "has_shield": "max",
        "has_horse": "max",
        "has_throwing": "max",
        "ranged_role_score": "max",
        "defensive_role_score": "max",
        "offensive_melee_role_score": "max",
        "skirmisher_role_score": "max",
        "defense_score_base": "mean",
        "ranged_score_base": "max",
        "crafted_melee_score_base": "max",
        "throw_score_base": "max",
        "ranged_item": join_unique,
        "crafted_melee_item": join_unique,
        "crafted_melee_template": join_unique,
        "direct_throw_item": join_unique,
        "crafted_throw_item": join_unique,
    }).reset_index()

    def primary(row):
        if row["has_ranged"]:
            return "Ranged Troops"
        if row["has_throwing"]:
            return "Skirmishers"
        if row["has_shield"] or row["has_horse"] or (row.get("defense_score_base") or 0) >= 55:
            return "Defensive Troops"
        return "Offensive Melee"

    agg["primary_category"] = agg.apply(primary, axis=1)
    agg["score_status"] = "role_scores_v1_conservative_not_final"
    return df, agg


def write_outputs(rosters: pd.DataFrame, troops: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rosters.to_csv(output_dir / "vanilla_roster_role_scores_v1.csv", index=False)
    troops.to_csv(output_dir / "vanilla_troop_role_scores_v1.csv", index=False)

    role_files = {
        "ranged_role_score": "ranged_troops.csv",
        "defensive_role_score": "defensive_troops.csv",
        "offensive_melee_role_score": "offensive_melee.csv",
        "skirmisher_role_score": "skirmishers.csv",
    }
    for col, filename in role_files.items():
        troops[troops[col].notna()].sort_values(col, ascending=False).to_csv(output_dir / filename, index=False)

    primary = troops.copy()
    primary["primary_category_score"] = np.select(
        [
            primary["primary_category"].eq("Ranged Troops"),
            primary["primary_category"].eq("Defensive Troops"),
            primary["primary_category"].eq("Offensive Melee"),
            primary["primary_category"].eq("Skirmishers"),
        ],
        [
            primary["ranged_role_score"],
            primary["defensive_role_score"],
            primary["offensive_melee_role_score"],
            primary["skirmisher_role_score"],
        ],
        default=np.nan,
    )
    primary.sort_values(["primary_category", "primary_category_score"], ascending=[True, False]).to_csv(output_dir / "vanilla_primary_category_rankings_v1.csv", index=False)

    troops[troops["troop_id"].isin(CONTROL_IDS)].to_csv(output_dir / "vanilla_sanity_role_scores_v1.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-dir", type=Path, default=Path("data/vanilla/audit"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/vanilla/role_scores"))
    args = parser.parse_args()

    audit = pd.read_csv(args.audit_dir / "vanilla_troop_equipment_audit.csv")
    troops = pd.read_csv(args.audit_dir / "vanilla_troops.csv")
    depths = pd.read_csv(args.audit_dir / "vanilla_tree_tiers.csv")

    soldiers = set(troops[troops["is_soldier"].astype(str).str.lower().eq("true")]["troop_id"])
    if "line_status_corrected" in depths.columns:
        depths = depths.rename(columns={"line_status_corrected": "line_status"})
    if "tree_tier" in depths.columns and "upgrade_depth" not in depths.columns:
        depths = depths.rename(columns={"tree_tier": "upgrade_depth"})

    roster_features = build_roster_features(audit, soldiers, depths)
    roster_scores, troop_scores = build_role_scores(roster_features)
    write_outputs(roster_scores, troop_scores, args.output_dir)

    print("Vanilla role scores generated.")
    print(f"rosters={len(roster_scores)}")
    print(f"troops={len(troop_scores)}")
    print(f"output={args.output_dir}")


if __name__ == "__main__":
    main()
