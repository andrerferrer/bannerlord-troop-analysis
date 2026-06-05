#!/usr/bin/env python3
"""Build v7.2 burst_score outputs from a v7.1 model CSV.

This script intentionally adds only burst scoring. It does not implement
boarding_score, short_engagement_score, or siege_defense_score.

Usage:
    python scripts/build_v72_burst_score.py \
      --model-csv analysis/model_versions/v7.1/bannerlord_v71_head_weighted_model_all_official_troops.csv \
      --empirical-csv analysis/empirical/screenshots_2026-05-29_2026-06-04/empirical_troop_aggregate_summary.csv \
      --outdir analysis/model_versions/v7.2_burst_score
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def clamp(values, low: float, high: float):
    return np.minimum(np.maximum(values, low), high)


def as_bool(series: pd.Series) -> pd.Series:
    return series.fillna(False).astype(bool)


def build_v72_burst_scores(model: pd.DataFrame) -> pd.DataFrame:
    df = model.copy()

    throw_type_factor = (
        df["primary_throw_damage_type"]
        .map({"Pierce": 1.10, "Blunt": 1.05, "Cut": 0.88})
        .fillna(1.0)
        .astype(float)
    )

    throw_ammo = df["primary_throw_ammo"].fillna(0).astype(float)
    throw_ammo_factor = clamp(0.55 + 0.07 * np.minimum(throw_ammo, 10), 0.55, 1.25)
    mounted_throw_bonus = np.where(as_bool(df["is_mounted"]), 1.12, 1.0)

    throw_burst_raw = (
        df["throw_pressure_v7"].fillna(0).astype(float)
        * throw_ammo_factor
        * throw_type_factor
        * mounted_throw_bonus
    )

    ranged_ammo = df["ranged_ammo_v7"].fillna(0).astype(float)
    ranged_ammo_factor = clamp(0.75 + ranged_ammo / 80.0, 0.75, 1.35)
    ranged_type_factor = np.where(
        as_bool(df["has_crossbow"]),
        1.15,
        np.where(df["category"].fillna("").eq("Horse Archer"), 1.05, 1.0),
    )
    ranged_burst_raw = df["ranged_kpm_v7"].fillna(0).astype(float) * ranged_ammo_factor * ranged_type_factor

    charge_burst_raw = df["charge_impact_score_v7"].fillna(0).astype(float) / 100.0 * 4.75
    melee_burst_raw = df["melee_kpm_eff_v7"].fillna(0).astype(float) * 0.65

    raw_matrix = np.vstack([throw_burst_raw, ranged_burst_raw, charge_burst_raw, melee_burst_raw]).T
    source_labels = np.array(["throw", "ranged", "charge", "melee"])
    source_idx = raw_matrix.argmax(axis=1)

    burst_raw = raw_matrix.max(axis=1)
    burst_source = source_labels[source_idx]
    burst_offense_score = clamp(burst_raw / 7.0 * 100.0, 0, 100)

    burst_score = clamp(
        0.70 * burst_offense_score
        + 0.20 * df["reliability_score"].fillna(0).astype(float)
        + 0.10 * df["defense_score_v71"].fillna(0).astype(float),
        0,
        100,
    )

    bucket = pd.cut(
        burst_score,
        bins=[-1, 45, 60, 75, 85, 100],
        labels=["low", "situational", "solid", "high", "elite"],
    ).astype(str)

    additions = {
        "burst_score_v72": burst_score,
        "burst_bucket_v72": bucket,
        "burst_offense_score_v72": burst_offense_score,
        "burst_raw_v72": burst_raw,
        "burst_source_v72": burst_source,
        "throw_burst_raw_v72": throw_burst_raw,
        "ranged_burst_raw_v72": ranged_burst_raw,
        "charge_burst_raw_v72": charge_burst_raw,
        "melee_burst_raw_v72": melee_burst_raw,
        "throw_ammo_factor_v72": throw_ammo_factor,
        "throw_damage_type_factor_v72": throw_type_factor,
        "mounted_throw_bonus_v72": mounted_throw_bonus,
        "ranged_ammo_factor_v72": ranged_ammo_factor,
        "ranged_type_factor_v72": ranged_type_factor,
    }

    for key, value in additions.items():
        df[key] = value

    df["burst_rank_official_v72"] = df["burst_score_v72"].rank(method="min", ascending=False).astype(int)

    regular_mask = as_bool(df["is_regular_culture_tree"])
    vanilla_regular = regular_mask & df["data_scope"].eq("Vanilla pre-War-Sails modules")
    navaldlc_regular = regular_mask & df["data_scope"].eq("War Sails / NavalDLC")

    df["burst_rank_regular_v72"] = np.nan
    df.loc[regular_mask, "burst_rank_regular_v72"] = (
        df.loc[regular_mask, "burst_score_v72"].rank(method="min", ascending=False).astype(int)
    )

    df["vanilla_regular_burst_rank_v72"] = np.nan
    df.loc[vanilla_regular, "vanilla_regular_burst_rank_v72"] = (
        df.loc[vanilla_regular, "burst_score_v72"].rank(method="min", ascending=False).astype(int)
    )

    df["navaldlc_regular_burst_rank_v72"] = np.nan
    df.loc[navaldlc_regular, "navaldlc_regular_burst_rank_v72"] = (
        df.loc[navaldlc_regular, "burst_score_v72"].rank(method="min", ascending=False).astype(int)
    )

    df["rank_delta_burst_vs_general_regular_v72"] = df["burst_rank_regular_v72"] - df["regular_rank_v71"]

    round_cols = [
        "burst_score_v72",
        "burst_offense_score_v72",
        "burst_raw_v72",
        "throw_burst_raw_v72",
        "ranged_burst_raw_v72",
        "charge_burst_raw_v72",
        "melee_burst_raw_v72",
        "throw_ammo_factor_v72",
        "throw_damage_type_factor_v72",
        "mounted_throw_bonus_v72",
        "ranged_ammo_factor_v72",
        "ranged_type_factor_v72",
        "rank_delta_burst_vs_general_regular_v72",
    ]
    for col in round_cols:
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
    "offense_score_v7",
    "defense_score_v71",
    "reliability_score",
    "burst_score_v72",
    "burst_bucket_v72",
    "burst_rank_official_v72",
    "burst_rank_regular_v72",
    "vanilla_regular_burst_rank_v72",
    "navaldlc_regular_burst_rank_v72",
    "rank_delta_burst_vs_general_regular_v72",
    "burst_offense_score_v72",
    "burst_raw_v72",
    "burst_source_v72",
    "throw_burst_raw_v72",
    "ranged_burst_raw_v72",
    "charge_burst_raw_v72",
    "melee_burst_raw_v72",
    "primary_throw_name",
    "primary_throw_damage",
    "primary_throw_damage_type",
    "primary_throw_ammo",
    "throw_pressure_v7",
    "throw_kpm",
    "throwing",
    "throw_ammo_factor_v72",
    "throw_damage_type_factor_v72",
    "mounted_throw_bonus_v72",
    "primary_ranged_name",
    "ranged_damage_v7",
    "ranged_ammo_v7",
    "ranged_kpm_v7",
    "ranged_ammo_factor_v72",
    "ranged_type_factor_v72",
    "charge_impact_score_v7",
    "melee_kpm_eff_v7",
    "has_shield",
    "shield_strength",
    "is_mounted",
    "athletics",
    "model_status_v7",
    "model_notes_v7",
    "stat_source_primary_throw",
    "stat_source_primary_ranged",
    "stat_source_primary_melee",
]


def existing(columns: list[str], df: pd.DataFrame) -> list[str]:
    return [col for col in columns if col in df.columns]


def write_outputs(df: pd.DataFrame, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    cols = existing(OUTPUT_COLUMNS, df)
    compact = df[cols].sort_values(["burst_rank_official_v72", "name"])
    compact.to_csv(outdir / "bannerlord_v72_burst_model_all_official_troops.csv", index=False)

    regular = df[df["is_regular_culture_tree"].fillna(False).astype(bool)].copy()
    regular = regular.sort_values(["burst_rank_regular_v72", "name"])
    regular[cols].to_csv(outdir / "bannerlord_v72_top_burst_units_regular_combined.csv", index=False)
    regular[cols].head(40).to_csv(outdir / "bannerlord_v72_top40_burst_units_regular_combined.csv", index=False)
    regular[cols].head(20).to_csv(outdir / "bannerlord_v72_top20_burst_units_regular_combined.csv", index=False)

    vanilla = regular[regular["data_scope"].eq("Vanilla pre-War-Sails modules")]
    naval = regular[regular["data_scope"].eq("War Sails / NavalDLC")]
    vanilla[cols].to_csv(outdir / "vanilla_v72_top_burst_units_regular.csv", index=False)
    naval[cols].to_csv(outdir / "warsails_v72_top_burst_units_regular.csv", index=False)


def write_empirical_validation(df: pd.DataFrame, empirical_csv: Path, outdir: Path) -> None:
    if not empirical_csv or not empirical_csv.exists():
        return

    empirical = pd.read_csv(empirical_csv)
    joined = empirical.merge(
        df[[
            "name",
            "burst_score_v72",
            "burst_rank_regular_v72",
            "burst_bucket_v72",
            "burst_source_v72",
            "regular_rank_v71",
            "total_score_v71",
            "data_scope",
            "category",
            "tier",
        ]],
        left_on="troop_name",
        right_on="name",
        how="left",
    )
    joined["rank_delta_burst_vs_general_regular_v72"] = joined["burst_rank_regular_v72"] - joined["regular_rank_v71"]

    def validation_note(row: pd.Series) -> str:
        if pd.isna(row.get("burst_rank_regular_v72")):
            return "no regular v7.2 burst rank matched"
        kpp = row.get("weighted_kills_per_present")
        delta = row.get("rank_delta_burst_vs_general_regular_v72")
        if pd.notna(kpp) and kpp >= 1.1 and pd.notna(delta) and delta < -10:
            return "empirical overperformance aligned with burst-score boost"
        if pd.notna(kpp) and kpp >= 1.1:
            return "empirical output strong; monitor context"
        if pd.notna(kpp) and kpp < 0.5:
            return "low empirical output in sample; likely context/casualty-sensitive"
        return "neutral / insufficient sample"

    joined["v72_burst_validation_note"] = joined.apply(validation_note, axis=1)
    cols = [
        "troop_name",
        "observations",
        "total_present",
        "total_kills",
        "weighted_kills_per_present",
        "casualty_rate",
        "total_score_v71",
        "regular_rank_v71",
        "burst_score_v72",
        "burst_rank_regular_v72",
        "rank_delta_burst_vs_general_regular_v72",
        "burst_bucket_v72",
        "burst_source_v72",
        "tier",
        "category",
        "data_scope",
        "v72_burst_validation_note",
    ]
    joined[[col for col in cols if col in joined.columns]].sort_values(
        "weighted_kills_per_present", ascending=False
    ).to_csv(outdir / "empirical_v72_burst_validation_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-csv", required=True, type=Path)
    parser.add_argument("--empirical-csv", type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    args = parser.parse_args()

    model = pd.read_csv(args.model_csv)
    scored = build_v72_burst_scores(model)
    write_outputs(scored, args.outdir)
    if args.empirical_csv:
        write_empirical_validation(scored, args.empirical_csv, args.outdir)


if __name__ == "__main__":
    main()
