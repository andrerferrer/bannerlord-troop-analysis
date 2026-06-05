"""Build Bannerlord v7.2 context scores.

Inputs:
  - v7.1 model CSV
  - optional empirical aggregate CSV

Outputs:
  - context-scored compact model
  - top burst / short engagement / siege defense CSVs
  - empirical validation join

Important: v7.2 keeps v7.1 general_score unchanged and does not include boarding_score.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import numpy as np
import pandas as pd


def num(series, default: float = 0.0) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(default).astype(float)


def clip(x, lo: float = 0.0, hi: float = 100.0):
    return np.minimum(np.maximum(x, lo), hi)


def boolish(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["true", "1", "yes"]) | (
        pd.to_numeric(series, errors="coerce").fillna(0) > 0
    )


def build_context_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # v7.2 does not replace the v7.1 general ranking.
    df["general_score_v72"] = num(df["total_score_v71"])

    throw_pressure = num(df.get("throw_pressure_v7", 0))
    throw_pressure_eff = num(df.get("throw_pressure_eff_v6", 0))
    throw_pressure_best = np.maximum(throw_pressure, throw_pressure_eff * 0.85)
    throw_ammo = np.maximum.reduce([
        num(df.get("throw_ammo_v6", 0)).values,
        num(df.get("primary_throw_ammo", 0)).values,
        num(df.get("raw_xml_throw_stack_amount", 0)).values,
    ])
    throw_damage = num(df.get("primary_throw_damage", 0))
    throw_skill = num(df.get("throwing", 0))
    throw_type = df.get("primary_throw_damage_type", pd.Series([""] * len(df))).fillna("").astype(str).str.lower()
    throw_type_mod = np.select(
        [throw_type.str.contains("pierce"), throw_type.str.contains("blunt"), throw_type.str.contains("cut")],
        [1.00, 0.92, 0.78],
        default=0.85,
    )
    throw_pressure_norm = clip(throw_pressure_best / 6.0 * 100)
    throw_ammo_norm = clip(np.log1p(throw_ammo) / np.log1p(10) * 100)
    throw_damage_norm = clip((throw_damage * throw_type_mod) / 60.0 * 100)
    throw_skill_norm = clip(throw_skill / 160.0 * 100)
    throw_mounted_bonus = np.where(
        boolish(df.get("is_mounted", pd.Series(False, index=df.index)))
        & (throw_pressure_best > 0)
        & throw_type.str.contains("pierce"),
        4.0,
        0.0,
    )
    throw_burst = clip(
        0.45 * throw_pressure_norm
        + 0.25 * throw_ammo_norm
        + 0.20 * throw_skill_norm
        + 0.10 * throw_damage_norm
        + throw_mounted_bonus
    )
    throw_burst = np.where(throw_ammo > 0, throw_burst, 0.0)

    ranged_kpm = num(df.get("ranged_kpm_v7", df.get("ranged_kpm", 0)))
    ranged_damage = num(df.get("ranged_damage_v7", df.get("primary_ranged_damage", 0)))
    ranged_ammo = num(df.get("ranged_ammo_v7", df.get("primary_ranged_ammo", 0)))
    expected_kill_capacity = num(df.get("expected_kill_capacity_v6", df.get("expected_kill_capacity", 0)))
    ranged_class = df.get("primary_ranged_class", pd.Series([""] * len(df))).fillna("").astype(str).str.lower()
    ranged_pressure_norm = clip(ranged_kpm / 4.9 * 100)
    ranged_ammo_norm = clip(np.log1p(ranged_ammo) / np.log1p(48) * 100)
    ranged_damage_norm = clip(ranged_damage / 105.0 * 100)
    ranged_capacity_norm = clip(expected_kill_capacity / 16.0 * 100)
    crossbow_alpha_bonus = np.where(ranged_class.str.contains("crossbow"), 8.0, 0.0)
    bow_sustained_bonus = np.where(ranged_class.str.contains("bow") & ~ranged_class.str.contains("crossbow"), 4.0, 0.0)
    ranged_burst = clip(
        0.42 * ranged_pressure_norm
        + 0.20 * ranged_ammo_norm
        + 0.20 * ranged_damage_norm
        + 0.12 * ranged_capacity_norm
        + 0.06 * num(df["reliability_score"])
        + crossbow_alpha_bonus
        + bow_sustained_bonus
    )
    ranged_burst = np.where(ranged_ammo > 0, ranged_burst, 0.0)

    melee_kpm = num(df.get("melee_kpm_eff_v7", df.get("melee_kpm", 0)))
    melee_damage = num(df.get("primary_melee_damage", 0))
    melee_reach = num(df.get("primary_melee_reach", 0))
    melee_class = df.get("primary_melee_class", pd.Series([""] * len(df))).fillna("").astype(str).str.lower()
    melee_type = df.get("primary_melee_damage_type", pd.Series([""] * len(df))).fillna("").astype(str).str.lower()
    has_shield = boolish(df.get("has_shield", pd.Series(False, index=df.index)))
    melee_shock = clip(
        0.58 * clip(melee_kpm / 6.5 * 100)
        + 0.30 * clip(melee_damage / 105.0 * 100)
        + 0.12 * clip(melee_reach / 155.0 * 100)
        + np.where(melee_class.str.contains("twohand"), 8.0, 0.0)
        + np.where(melee_class.str.contains("polearm") & ~has_shield, 6.0, 0.0)
        + np.where(melee_type.str.contains("blunt"), 4.0, 0.0)
        + np.where(melee_class.str.contains("polearm") & has_shield & melee_type.str.contains("pierce"), -15.0, 0.0)
    )

    charge = np.where(boolish(df.get("is_mounted", pd.Series(False, index=df.index))), clip(num(df.get("charge_impact_score_v7", 0))), 0.0)
    burst_core = np.maximum.reduce([throw_burst, ranged_burst, melee_shock, charge])

    df["throw_burst_component_v72"] = throw_burst
    df["ranged_burst_component_v72"] = ranged_burst
    df["melee_shock_component_v72"] = melee_shock
    df["charge_burst_component_v72"] = charge
    df["burst_score_v72"] = clip(0.82 * burst_core + 0.13 * num(df["reliability_score"]) + 0.05 * num(df["defense_score_v71"]))
    df["short_engagement_score_v72"] = clip(
        0.45 * df["burst_score_v72"]
        + 0.30 * num(df["offense_score_v7"])
        + 0.15 * num(df["reliability_score"])
        + 0.10 * num(df["defense_score_v71"])
    )

    ranged_siege = clip(
        0.50 * ranged_pressure_norm
        + 0.25 * ranged_ammo_norm
        + 0.15 * ranged_capacity_norm
        + 0.10 * ranged_damage_norm
        + crossbow_alpha_bonus / 2
        + bow_sustained_bonus / 2
    )
    throw_siege = clip(0.75 * throw_burst)
    siege = clip(0.55 * np.maximum(ranged_siege, throw_siege) + 0.20 * num(df["defense_score_v71"]) + 0.15 * num(df["reliability_score"]) + 0.10 * ranged_ammo_norm)
    formation_floor = np.where(
        df["category"].astype(str).str.contains("Defensive"),
        clip(0.45 * num(df["defense_score_v71"]) + 0.35 * num(df["reliability_score"]) + 0.20 * num(df["offense_score_v7"])),
        0,
    )
    df["ranged_siege_component_v72"] = ranged_siege
    df["throw_siege_component_v72"] = throw_siege
    df["siege_defense_score_v72"] = np.maximum(siege, formation_floor)

    labels = np.array(["throwing", "ranged", "charge", "melee"])
    values = np.vstack([throw_burst, ranged_burst, charge, melee_shock]).T
    df["burst_primary_driver_v72"] = labels[np.nanargmax(values, axis=1)]
    return df


def rank_outputs(df: pd.DataFrame) -> pd.DataFrame:
    def rank_desc(mask, col):
        out = pd.Series(np.nan, index=df.index)
        out.loc[mask] = df.loc[mask, col].rank(method="first", ascending=False).astype(int)
        return out

    reg = df["is_regular_culture_tree"].astype(str).str.lower().isin(["true", "1"])
    df["burst_rank_regular_v72"] = rank_desc(reg, "burst_score_v72")
    df["short_engagement_rank_regular_v72"] = rank_desc(reg, "short_engagement_score_v72")
    df["siege_defense_rank_regular_v72"] = rank_desc(reg, "siege_defense_score_v72")
    df["throwing_burst_component_rank_regular_v72"] = rank_desc(reg & (df["throw_burst_component_v72"] > 0), "throw_burst_component_v72")
    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="v7.1 model CSV")
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--empirical", default=None, help="optional empirical aggregate CSV")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    df = rank_outputs(build_context_scores(pd.read_csv(args.input)))
    reg = df["is_regular_culture_tree"].astype(str).str.lower().isin(["true", "1"])

    compact_cols = [
        "troop_id", "name", "culture_name", "data_scope", "tier", "category", "is_regular_culture_tree",
        "general_score_v72", "regular_rank_v71", "burst_score_v72", "burst_rank_regular_v72",
        "short_engagement_score_v72", "short_engagement_rank_regular_v72",
        "siege_defense_score_v72", "siege_defense_rank_regular_v72",
        "throwing_burst_component_rank_regular_v72", "burst_primary_driver_v72",
        "throw_burst_component_v72", "ranged_burst_component_v72", "melee_shock_component_v72", "charge_burst_component_v72",
        "offense_score_v7", "defense_score_v71", "reliability_score",
    ]
    compact_cols = [c for c in compact_cols if c in df.columns]
    compact = df[compact_cols].copy()
    for col in compact.select_dtypes(include=["number"]).columns:
        compact[col] = compact[col].round(3)

    compact.to_csv(outdir / "bannerlord_v72_context_scores_all_official_troops.csv", index=False)
    compact[reg].sort_values("burst_score_v72", ascending=False).head(40).to_csv(outdir / "bannerlord_v72_top40_burst_regular.csv", index=False)
    compact[reg].sort_values("short_engagement_score_v72", ascending=False).head(40).to_csv(outdir / "bannerlord_v72_top40_short_engagement_regular.csv", index=False)
    compact[reg].sort_values("siege_defense_score_v72", ascending=False).head(40).to_csv(outdir / "bannerlord_v72_top40_siege_defense_regular.csv", index=False)
    compact[reg & (compact["throw_burst_component_v72"] > 0)].sort_values("throw_burst_component_v72", ascending=False).head(40).to_csv(outdir / "bannerlord_v72_top40_throwing_burst_regular.csv", index=False)

    if args.empirical:
        emp = pd.read_csv(args.empirical)
        join_cols = ["name", "general_score_v72", "burst_score_v72", "short_engagement_score_v72", "siege_defense_score_v72", "burst_primary_driver_v72"]
        emp.merge(compact[join_cols], left_on="troop_name", right_on="name", how="left").to_csv(outdir / "empirical_v72_context_validation.csv", index=False)


if __name__ == "__main__":
    main()
