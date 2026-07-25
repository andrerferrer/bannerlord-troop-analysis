from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Mapping

from .bundle import atomic_write_json
from .domain import RANKING_CRITICAL_FIELDS, read_csv, stable_id, write_csv


REVIEW_CATEGORIES = (
    "numeric_uncertainty",
    "ambiguous_troop_name",
    "ambiguous_row_type",
    "ambiguous_parent_party",
    "battle_grouping_uncertainty",
    "battle_context_uncertainty",
    "duplicate_candidate",
    "aggregation_mismatch",
    "possible_ocr_artifact",
    "possible_siege_engine_outlier",
)

CATEGORIZED_FIELDS = (
    "review_id",
    "observation_id",
    "categories",
    "ranking_impact",
    "priority",
    "fields_needing_review",
    "automatic_resolution_eligible",
    "image_inspection_required",
    "current_status",
    "resolution_reference",
)


def _truthy(value: object) -> bool:
    return str(value or "").strip().casefold() in {"1", "true", "yes", "y"}


def _list_value(value: object) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    text = str(value)
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    separator = "|" if "|" in text else ","
    return [item.strip() for item in text.split(separator) if item.strip()]


def categorize_review_row(row: Mapping[str, object]) -> dict[str, object]:
    observation_id = str(row.get("observation_id") or row.get("source_observation_id") or "")
    uncertain = sorted(set(_list_value(row.get("uncertain_fields") or row.get("fields_needing_review"))))
    categories: set[str] = set(_list_value(row.get("categories")))
    numeric_fields = {"survivors", "kills", "upgrade_ready", "deaths", "wounded", "routed"}
    if numeric_fields.intersection(field.rsplit(".", 1)[-1] for field in uncertain):
        categories.add("numeric_uncertainty")
    if any("name" in field or "troop_id" in field for field in uncertain) or not row.get("canonical_troop_id"):
        categories.add("ambiguous_troop_name")
    if any("row_type" in field for field in uncertain) or row.get("row_type") in {"", None, "artifact"}:
        categories.add("ambiguous_row_type")
    if any("parent" in field for field in uncertain) or _truthy(row.get("ambiguous_parent_party")):
        categories.add("ambiguous_parent_party")
    if _truthy(row.get("battle_grouping_uncertainty")):
        categories.add("battle_grouping_uncertainty")
    if row.get("battle_context") == "undefined" or any("battle_context" in field for field in uncertain):
        categories.add("battle_context_uncertainty")
    flag_mapping = {
        "duplicate_candidate": "duplicate_candidate",
        "aggregation_mismatch": "aggregation_mismatch",
        "possible_ocr_artifact": "possible_ocr_artifact",
        "possible_siege_engine_outlier": "possible_siege_engine_outlier",
        "suspected_siege_engine_outlier": "possible_siege_engine_outlier",
    }
    for field, category in flag_mapping.items():
        if _truthy(row.get(field)):
            categories.add(category)

    row_type = str(row.get("row_type") or "")
    ranking_row = row_type == "troop" and str(row.get("analysis_status") or "primary") not in {
        "excluded",
        "non_ranking",
    }
    critical = sorted(
        field
        for field in uncertain
        if field.rsplit(".", 1)[-1] in RANKING_CRITICAL_FIELDS
    )
    ranking_impact = ranking_row and bool(
        critical
        or "ambiguous_troop_name" in categories
        or "duplicate_candidate" in categories
        or "aggregation_mismatch" in categories
    )
    if ranking_impact and any(field.rsplit(".", 1)[-1] in {"kills", "survivors", "deaths", "wounded"} for field in critical):
        priority = 1
    elif ranking_row and "ambiguous_troop_name" in categories:
        priority = 2
    elif categories.intersection({"duplicate_candidate", "battle_grouping_uncertainty", "aggregation_mismatch"}):
        priority = 3
    elif "battle_context_uncertainty" in categories:
        priority = 4
    elif row_type in {"hero", "player", "party", "side_total", "artifact"}:
        priority = 6
    else:
        priority = 5

    categories_sorted = sorted(categories)
    review_id = str(row.get("review_id") or stable_id("review", observation_id, uncertain, categories_sorted))
    deterministic_evidence = _truthy(row.get("deterministic_resolution_proven"))
    return {
        "review_id": review_id,
        "observation_id": observation_id,
        "categories": categories_sorted,
        "ranking_impact": ranking_impact,
        "priority": priority,
        "fields_needing_review": uncertain,
        "automatic_resolution_eligible": deterministic_evidence,
        "image_inspection_required": not deterministic_evidence,
        "current_status": row.get("current_status") or row.get("resolution_status") or "unresolved",
        "resolution_reference": row.get("resolution_reference") or "",
    }


def triage_review_queue(input_csv: Path, output_dir: Path) -> dict[str, object]:
    source_rows = read_csv(input_csv)
    categorized = sorted(
        (categorize_review_row(row) for row in source_rows),
        key=lambda row: (int(row["priority"]), str(row["review_id"])),
    )
    write_csv(output_dir / "review_queue_categorized.csv", categorized, CATEGORIZED_FIELDS)
    counts = Counter(category for row in categorized for category in row["categories"])
    summary_rows = [
        {"category": category, "row_count": counts.get(category, 0)}
        for category in REVIEW_CATEGORIES
    ]
    write_csv(output_dir / "review_category_summary.csv", summary_rows, ("category", "row_count"))
    progress = {
        "schema_version": "1.0.0",
        "total_rows": len(categorized),
        "ranking_impact_rows": sum(bool(row["ranking_impact"]) for row in categorized),
        "automatic_resolution_eligible": sum(bool(row["automatic_resolution_eligible"]) for row in categorized),
        "image_inspection_required": sum(bool(row["image_inspection_required"]) for row in categorized),
        "status_counts": dict(sorted(Counter(str(row["current_status"]) for row in categorized).items())),
        "category_counts": dict(sorted(counts.items())),
    }
    atomic_write_json(output_dir / "review_progress.json", progress)
    return progress
