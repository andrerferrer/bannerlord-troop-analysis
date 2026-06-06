#!/usr/bin/env python3
"""Build v7.3 tooltip-validated throwing burst score outputs.

v7.3 changes only burst context scoring. It does not replace v7.1 general_score.

Inputs expected:
- v7.2.1 tooltip-validated model CSV, with tooltip_throw_* columns.

Example:
    python scripts/build_v73_tooltip_damage_burst.py \
      --model-csv analysis/model_versions/v7.2.1_tooltip_throw_validation/bannerlord_v721_tooltip_throw_model_all_official_troops.csv \
      --outdir analysis/model_versions/v7.3_tooltip_damage_burst
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def clamp(values, low: float, high: float):
    return np.minimum(np.maximum(values, low), high)


def bool_series(s: pd.Series) -> pd.Series:
    return s.fillna(False).astype(bool)


def markdown_table(frame: pd.DataFrame, cols: list[str]) -> str:
    x = frame[cols].copy()
    for col in x.select_dtypes(include=[float]).columns:
        x[col] = x[col].map(
            lambda v: "" if pd.isna(v) else f"{v:.3f}" if abs(v - round(v)) > 1e-6 else str(int(v))
        )
    return x.to_markdown(index=False)


def build_v73(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    tooltip_available = df["tooltip_throw_damage"].notna() & (df["tooltip_throw_damage"].fillna(0) > 0)

    df["throw_damage_used_v73"] = np.where(
        tooltip_available,
        df["tooltip_throw_damage"],
        df["primary_throw_damage"],
    ).astype(float)

    df["throw_damage_source_v73"] = np.where(
        tooltip_available,
        "tooltip_validated",
        np.where(df["primary_throw_damage"].notna(), "model_proxy", "none"),
    )

    df["throw_damage_ratio_tooltip_v73"] = np.where(
        tooltip_available & df["primary_throw_damage"].notna() & (df["primary_throw_damage"] > 0),
        df["tooltip_throw_damage"] / df["primary_throw_damage"],
        np.nan,
    )

    df["throw_ammo_used_v73"] = np.where(
        df["tooltip_throw_total_ammo"].notna() & (df["tooltip_throw_total_ammo"].fillna(0) > 0),
        df["tooltip_throw_total_ammo"],
        df["primary_throw_ammo"].fillna(0),
    ).astype(float)

    df["throw_damage_type_used_v73"] = np.where(
        df["tooltip_throw_damage_type"].notna() & (df["tooltip_throw_damage_type"].astype(str).str.len() > 0),
        df["tooltip_throw_damage_type"],
        df["primary_throw_damage_type"],
    )

    throw_damage = pd.Series(df["throw_damage_used_v73"]).fillna(0).astype(float)
    throwing = pd.Series(df["throwing"]).fillna(0).astype(float)
    ammo = pd.Series(df["throw_ammo_used_v73"]).fillna(0).astype(float)

    df["throw_damage_factor_v73"] = clamp(throw_damage / 110.0, 0.70, 1.10)
    df["throw_skill_factor_v73"] = clamp(0.75 + throwing / 400.0, 0.75, 1.20)

    df["throw_ammo_factor_v73"] = clamp(
        0.70 + 0.08 * np.minimum(ammo, 5) + 0.04 * np.maximum(np.minimum(ammo - 5, 5), 0),
        0.70,
        1.30,
    )

    df["mounted_throw_bonus_v73"] = np.where(bool_series(df["is_mounted"]), 1.12, 1.0)

    type_map = {"Pierce": 1.00, "Blunt": 0.96, "Cut": 0.88}
    df["throw_damage_type_factor_v73"] = (
        pd.Series(df["throw_damage_type_used_v73"]).map(type_map).fillna(1.0).astype(float)
    )

    reference_throw_factor_v73 = 1.10 * (0.75 + 140 / 400.0) * (0.70 + 0.08 * 5) * 1.12

    throw_has_weapon = df["throw_damage_used_v73"].fillna(0).astype(float) > 0
    df["throw_burst_raw_v73"] = np.where(
        throw_has_weapon,
        df["throw_damage_factor_v73"]
        * df["throw_skill_factor_v73"]
        * df["throw_ammo_factor_v73"]
        * df["mounted_throw_bonus_v73"]
        * df["throw_damage_type_factor_v73"],
        0.0,
    )

    df["throw_burst_offense_score_v73"] = clamp(
        df["throw_burst_raw_v73"] / reference_throw_factor_v73 * 100.0,
        0,
        100,
    )

    df["ranged_burst_offense_score_v73"] = clamp(
        df["ranged_burst_raw_v72"].fillna(0).astype(float) / 7.0 * 100.0,
        0,
        100,
    )
    df["charge_burst_offense_score_v73"] = clamp(
        df["charge_burst_raw_v72"].fillna(0).astype(float) / 7.0 * 100.0,
        0,
        100,
    )
    df["melee_burst_offense_score_v73"] = clamp(
        df["melee_burst_raw_v72"].fillna(0).astype(float) / 7.0 * 100.0,
        0,
        100,
    )

    score_matrix = np.vstack([
        df["throw_burst_offense_score_v73"].to_numpy(),
        df["ranged_burst_offense_score_v73"].to_numpy(),
        df["charge_burst_offense_score_v73"].to_numpy(),
        df["melee_burst_offense_score_v73"].to_numpy(),
    ]).T
    source_labels = np.array(["throw", "ranged", "charge", "melee"])
    idx = score_matrix.argmax(axis=1)

    df["burst_source_v73"] = source_labels[idx]
    df["burst_offense_score_v73"] = score_matrix.max(axis=1)

    df["burst_score_v73"] = clamp(
        0.70 * df["burst_offense_score_v73"]
        + 0.20 * df["reliability_score"].fillna(0).astype(float)
        + 0.10 * df["defense_score_v71"].fillna(0).astype(float),
        0,
        100,
    )

    df["burst_bucket_v73"] = pd.cut(
        df["burst_score_v73"],
        [-1, 45, 60, 75, 85, 100],
        labels=["low", "situational", "solid", "high", "elite"],
    ).astype(str)

    df["burst_rank_official_v73"] = df["burst_score_v73"].rank(method="min", ascending=False).astype(int)

    regular = df["is_regular_culture_tree"].fillna(False).astype(bool)
    vanilla = regular & df["data_scope"].eq("Vanilla pre-War-Sails modules")
    naval = regular & df["data_scope"].eq("War Sails / NavalDLC")

    df["burst_rank_regular_v73"] = np.nan
    df.loc[regular, "burst_rank_regular_v73"] = (
        df.loc[regular, "burst_score_v73"].rank(method="min", ascending=False).astype(int)
    )

    df["vanilla_regular_burst_rank_v73"] = np.nan
    df.loc[vanilla, "vanilla_regular_burst_rank_v73"] = (
        df.loc[vanilla, "burst_score_v73"].rank(method="min", ascending=False).astype(int)
    )

    df["navaldlc_regular_burst_rank_v73"] = np.nan
    df.loc[naval, "navaldlc_regular_burst_rank_v73"] = (
        df.loc[naval, "burst_score_v73"].rank(method="min", ascending=False).astype(int)
    )

    if "burst_rank_regular_v721" in df:
        df["rank_delta_v73_vs_v72_burst_regular"] = df["burst_rank_regular_v73"] - df["burst_rank_regular_v721"]
    else:
        df["rank_delta_v73_vs_v72_burst_regular"] = np.nan

    df["rank_delta_burst_vs_general_regular_v73"] = df["burst_rank_regular_v73"] - df["regular_rank_v71"]

    for col in df.select_dtypes(include=[float]).columns:
        if any(key in col for key in ["score", "raw", "factor", "bonus", "ratio", "rank_delta", "damage_used", "ammo_used"]):
            df[col] = df[col].round(3)

    return df


OUTPUT_COLUMNS = [
    "troop_id",
    "name",
    "data_scope",
    "culture_name",
    "tier",
    "is_regular_culture_tree",
    "category",
    "total_score_v71",
    "regular_rank_v71",
    "vanilla_regular_rank_v71",
    "navaldlc_regular_rank_v71",
    "burst_score_v72",
    "burst_rank_regular_v721",
    "burst_source_v72",
    "burst_score_v73",
    "burst_bucket_v73",
    "burst_rank_official_v73",
    "burst_rank_regular_v73",
    "vanilla_regular_burst_rank_v73",
    "navaldlc_regular_burst_rank_v73",
    "rank_delta_v73_vs_v72_burst_regular",
    "rank_delta_burst_vs_general_regular_v73",
    "burst_source_v73",
    "burst_offense_score_v73",
    "throw_burst_offense_score_v73",
    "ranged_burst_offense_score_v73",
    "charge_burst_offense_score_v73",
    "melee_burst_offense_score_v73",
    "throw_burst_raw_v73",
    "throw_damage_source_v73",
    "throw_damage_used_v73",
    "throw_damage_ratio_tooltip_v73",
    "throw_damage_type_used_v73",
    "throw_ammo_used_v73",
    "throw_damage_factor_v73",
    "throw_skill_factor_v73",
    "throw_ammo_factor_v73",
    "mounted_throw_bonus_v73",
    "throw_damage_type_factor_v73",
    "primary_throw_name",
    "primary_throw_damage",
    "primary_throw_damage_type",
    "primary_throw_ammo",
    "tooltip_throw_name",
    "tooltip_throw_damage",
    "tooltip_throw_damage_type",
    "tooltip_throw_stack_amount",
    "tooltip_throw_visible_stacks",
    "tooltip_throw_total_ammo",
    "tooltip_throw_validation_result",
    "primary_ranged_name",
    "ranged_damage_v7",
    "ranged_ammo_v7",
    "ranged_kpm_v7",
    "ranged_burst_raw_v72",
    "charge_impact_score_v7",
    "melee_kpm_eff_v7",
    "has_shield",
    "shield_strength",
    "is_mounted",
    "athletics",
    "offense_score_v7",
    "defense_score_v71",
    "reliability_score",
    "model_status_v7",
    "model_notes_v7",
]


def existing(cols: list[str], df: pd.DataFrame) -> list[str]:
    return [c for c in cols if c in df.columns]


def write_outputs(df: pd.DataFrame, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    cols = existing(OUTPUT_COLUMNS, df)

    full = df[cols].sort_values(["burst_rank_official_v73", "name"])
    full.to_csv(outdir / "bannerlord_v73_tooltip_damage_burst_model_all_official_troops.csv", index=False)

    regular = df[df["is_regular_culture_tree"].fillna(False).astype(bool)].sort_values(["burst_rank_regular_v73", "name"])
    regular[cols].to_csv(outdir / "bannerlord_v73_top_burst_units_regular_combined.csv", index=False)
    regular[cols].head(40).to_csv(outdir / "bannerlord_v73_top40_burst_units_regular_combined.csv", index=False)
    regular[cols].head(20).to_csv(outdir / "bannerlord_v73_top20_burst_units_regular_combined.csv", index=False)

    vanilla = regular[regular["data_scope"].eq("Vanilla pre-War-Sails modules")]
    naval = regular[regular["data_scope"].eq("War Sails / NavalDLC")]
    vanilla[cols].to_csv(outdir / "vanilla_v73_top_burst_units_regular.csv", index=False)
    naval[cols].to_csv(outdir / "warsails_v73_top_burst_units_regular.csv", index=False)

    key_names = [
        "Aserai Vanguard Faris",
        "Battanian Skipari",
        "Imperial Naute",
        "Battanian River Raider",
        "Imperial Coast Guard",
        "Battanian Fian Champion",
        "Khuzait Khan's Guard",
        "Battanian Fian",
        "Vlandian Banner Knight",
        "Imperial Elite Menavliaton",
        "Imperial Sergeant Crossbowman",
        "Vlandian Sharpshooter",
        "Nord Huscarl",
        "Nord Skjaldbrestir",
    ]
    key = df[df["name"].isin(key_names)].copy().sort_values("burst_rank_regular_v73", na_position="last")
    key[cols].to_csv(outdir / "bannerlord_v73_key_burst_cases.csv", index=False)

    comp_cols = existing([
        "name",
        "tier",
        "category",
        "data_scope",
        "regular_rank_v71",
        "burst_rank_regular_v721",
        "burst_rank_regular_v73",
        "rank_delta_v73_vs_v72_burst_regular",
        "burst_score_v72",
        "burst_score_v73",
        "burst_source_v72",
        "burst_source_v73",
        "throw_damage_source_v73",
        "throw_damage_used_v73",
        "tooltip_throw_damage",
        "primary_throw_damage",
        "throw_ammo_used_v73",
        "tooltip_throw_total_ammo",
    ], df)
    regular[comp_cols].to_csv(outdir / "bannerlord_v73_comparison_v72_vs_v73_burst_regular.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-csv", required=True, type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()

    model = pd.read_csv(args.model_csv)
    scored = build_v73(model)
    write_outputs(scored, args.outdir)


if __name__ == "__main__":
    main()
