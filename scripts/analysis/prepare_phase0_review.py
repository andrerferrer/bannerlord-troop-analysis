#!/usr/bin/env python3
"""Prepare deterministic Phase 0 review, alias, and threshold-sensitivity outputs."""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from build_empirical_baseline import (
    KNOWN_CONTEXTS,
    build_rankings,
    consolidate,
    is_strict_player_row,
    read_jsonl,
)

CORE_FIELDS = ("survivors", "kills", "deaths", "wounded")


def uncertain_core_fields(row: dict[str, Any]) -> list[str]:
    extraction = row.get("field_extraction") or {}
    return [field for field in CORE_FIELDS if bool((extraction.get(field) or {}).get("uncertain"))]


def provisional_samples(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    samples: dict[str, dict[str, Any]] = defaultdict(lambda: {"battles": set(), "deployed": 0, "rows": 0})
    for row in rows:
        if row.get("analysis_status") != "included" or row.get("row_type") != "troop":
            continue
        if row.get("side") != row.get("player_side") or row.get("battle_type") not in KNOWN_CONTEXTS:
            continue
        deployed = row.get("deployed")
        if deployed is None or int(deployed) <= 0:
            continue
        sample = samples[str(row.get("canonical_name_slug") or "")]
        sample["battles"].add(str(row.get("battle_id")))
        sample["deployed"] += int(deployed)
        sample["rows"] += 1
    return samples


def classify_review_rows(
    rows: list[dict[str, Any]], minimum_battles: int, minimum_deployed: int
) -> list[dict[str, Any]]:
    samples = provisional_samples(rows)
    output: list[dict[str, Any]] = []
    for row in rows:
        if not bool(row.get("needs_review")):
            continue
        slug = str(row.get("canonical_name_slug") or "")
        sample = samples.get(slug, {"battles": set(), "deployed": 0, "rows": 0})
        uncertain = uncertain_core_fields(row)
        high_impact_shape = (
            row.get("analysis_status") == "included"
            and row.get("row_type") == "troop"
            and row.get("side") == row.get("player_side")
            and row.get("battle_type") in KNOWN_CONTEXTS
            and row.get("deployed") is not None
            and int(row.get("deployed") or 0) > 0
            and bool(uncertain)
        )
        if high_impact_shape and len(sample["battles"]) >= minimum_battles and int(sample["deployed"]) >= minimum_deployed:
            tier = "P0"
            reason = "can_change_five_battle_player_baseline"
        elif high_impact_shape:
            tier = "P1"
            reason = "player_core_uncertainty_below_display_gate"
        else:
            tier = "P2"
            reason = "enemy_undefined_secondary_or_nonranking_review"
        output.append(
            {
                "priority_tier": tier,
                "priority_reason": reason,
                "observation_id": row.get("observation_id"),
                "battle_id": row.get("battle_id"),
                "battle_type": row.get("battle_type"),
                "source_image_indices": ";".join(str(value) for value in row.get("source_image_indices") or []),
                "side": row.get("side"),
                "player_side": row.get("player_side"),
                "parent_group": row.get("parent_group"),
                "display_name_raw": row.get("display_name_raw"),
                "display_name_normalized": row.get("display_name_normalized"),
                "canonical_name_slug": slug,
                "uncertain_core_fields": ";".join(uncertain),
                "sample_battles": len(sample["battles"]),
                "sample_deployed": sample["deployed"],
                "survivors": row.get("survivors"),
                "kills": row.get("kills"),
                "deaths": row.get("deaths"),
                "wounded": row.get("wounded"),
                "routed": row.get("routed"),
                "deployed": row.get("deployed"),
                "ocr_confidence": row.get("ocr_confidence"),
            }
        )
    order = {"P0": 0, "P1": 1, "P2": 2}
    output.sort(
        key=lambda row: (
            order[row["priority_tier"]],
            -int(row["sample_battles"]),
            -int(row["sample_deployed"]),
            str(row["battle_id"]),
            str(row["observation_id"]),
        )
    )
    return output


def compact_slug(slug: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", slug.lower())


def alias_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"slugs": Counter(), "names": Counter(), "battles": set(), "rows": 0, "deployed": 0}
    )
    for row in rows:
        slug = str(row.get("canonical_name_slug") or "")
        if not slug:
            continue
        group = groups[compact_slug(slug)]
        group["slugs"][slug] += 1
        group["names"][str(row.get("display_name_normalized") or row.get("display_name_raw") or slug)] += 1
        group["battles"].add(str(row.get("battle_id")))
        group["rows"] += 1
        if row.get("deployed") is not None:
            group["deployed"] += int(row.get("deployed") or 0)
    output = []
    for key, group in groups.items():
        if len(group["slugs"]) <= 1:
            continue
        preferred_slug = group["slugs"].most_common(1)[0][0]
        output.append(
            {
                "normalization_key": key,
                "recommended_slug": preferred_slug,
                "candidate_slugs": ";".join(f"{slug}:{count}" for slug, count in group["slugs"].most_common()),
                "display_names": ";".join(f"{name}:{count}" for name, count in group["names"].most_common()),
                "row_count": group["rows"],
                "battle_count": len(group["battles"]),
                "total_deployed": group["deployed"],
                "decision": "manual_confirm_then_alias",
                "match_basis": "identical_after_removing_non_alphanumeric_characters",
            }
        )
    output.sort(key=lambda row: (-int(row["row_count"]), str(row["normalization_key"])))
    return output


def threshold_comparison(rows: list[dict[str, Any]], minimum_deployed: int, repetitions: int) -> list[dict[str, Any]]:
    strict = [row for row in rows if is_strict_player_row(row)]
    battle_rows = consolidate(strict)
    rankings3 = build_rankings(battle_rows, 3, minimum_deployed, repetitions)
    rankings5 = build_rankings(battle_rows, 5, minimum_deployed, repetitions)
    index3 = {(row["context"], row["canonical_name_slug"]): row for row in rankings3}
    index5 = {(row["context"], row["canonical_name_slug"]): row for row in rankings5}
    output = []
    for key in sorted(set(index3) | set(index5)):
        r3 = index3.get(key)
        r5 = index5.get(key)
        source = r5 or r3
        output.append(
            {
                "context": key[0],
                "display_name": source["display_name"],
                "canonical_name_slug": key[1],
                "eligible_min3": bool(r3),
                "eligible_min5": bool(r5),
                "battle_count": source["battle_count"],
                "total_deployed": source["total_deployed"],
                "kills_per_deployed": round(float(source["kills_per_deployed"]), 6),
                "rank_min3": r3["rank"] if r3 else "",
                "rank_min5": r5["rank"] if r5 else "",
                "rank_change_min5_minus_min3": (int(r5["rank"]) - int(r3["rank"])) if r3 and r5 else "",
                "status": "retained" if r3 and r5 else "removed_by_five_battle_gate" if r3 else "new_at_five",
            }
        )
    return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="primary_troop_occurrences.jsonl")
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--minimum-battles", type=int, default=5)
    parser.add_argument("--minimum-deployed", type=int, default=20)
    parser.add_argument("--bootstrap-repetitions", type=int, default=5000)
    args = parser.parse_args()
    rows = read_jsonl(args.input)
    review = classify_review_rows(rows, args.minimum_battles, args.minimum_deployed)
    aliases = alias_candidates(rows)
    sensitivity = threshold_comparison(rows, args.minimum_deployed, args.bootstrap_repetitions)
    write_csv(args.output_dir / "review_priority.csv", review)
    write_csv(args.output_dir / "alias_candidates_exact_normalization.csv", aliases)
    write_csv(args.output_dir / "threshold_sensitivity_3_vs_5.csv", sensitivity)
    print(
        json.dumps(
            {
                "review_rows": len(review),
                "review_by_tier": dict(Counter(row["priority_tier"] for row in review)),
                "exact_alias_candidate_groups": len(aliases),
                "threshold_rows": len(sensitivity),
                "minimum_battles": args.minimum_battles,
                "minimum_deployed": args.minimum_deployed,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
