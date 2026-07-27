from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable, Mapping

from .bundle import atomic_write_json
from .domain import DomainError, normalize_name, read_csv, read_jsonl, write_csv


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2 or len(xs) != len(ys):
        return None
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    denominator = math.sqrt(
        sum((x - mean_x) ** 2 for x in xs) * sum((y - mean_y) ** 2 for y in ys)
    )
    return numerator / denominator if denominator else None


def _rank(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: (-item[1], item[0]))
    result = [0.0] * len(values)
    position = 0
    while position < len(indexed):
        end = position + 1
        while end < len(indexed) and indexed[end][1] == indexed[position][1]:
            end += 1
        average_rank = (position + 1 + end) / 2
        for original_index, _ in indexed[position:end]:
            result[original_index] = average_rank
        position = end
    return result


def _model_index(rows: Iterable[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    result = {}
    for row in rows:
        keys = [
            row.get("troop_id"),
            row.get("canonical_troop_id"),
            normalize_name(row.get("name") or row.get("troop_name") or ""),
        ]
        for key in keys:
            if key:
                result[str(key)] = row
    return result


def _first_numeric(row: Mapping[str, str], columns: Iterable[str]) -> float | None:
    for column in columns:
        value = row.get(column)
        if value not in {None, ""}:
            try:
                return float(value)
            except ValueError:
                continue
    return None


def compare_models(
    aggregates_jsonl: Path,
    general_model_csv: Path,
    burst_model_csv: Path,
    output_dir: Path,
) -> dict[str, object]:
    aggregates = [
        row for row in read_jsonl(aggregates_jsonl)
        if (
            row.get("battle_context") == "overall"
            and row.get("historical_kills_per_deployed") is not None
        )
    ]
    general_rows = read_csv(general_model_csv)
    burst_rows = read_csv(burst_model_csv)
    general = _model_index(general_rows)
    burst = _model_index(burst_rows)
    joined = []
    for row in aggregates:
        troop_id = str(row["canonical_troop_id"])
        general_row = general.get(troop_id) or general.get(normalize_name(troop_id.replace("_", " ")))
        burst_row = burst.get(troop_id) or burst.get(normalize_name(troop_id.replace("_", " ")))
        empirical = float(row["historical_kills_per_deployed"]) if row.get("historical_kills_per_deployed") else None
        general_score = _first_numeric(general_row or {}, ("total_score_v71", "general_score_v71", "total_score"))
        burst_score = _first_numeric(burst_row or {}, ("burst_score_v73", "burst_score"))
        joined.append(
            {
                "canonical_troop_id": troop_id,
                "battle_count": row["battle_count"],
                "total_deployed": row["total_deployed"],
                "evidence_grade": row["evidence_grade"],
                "empirical_kills_per_deployed": row["historical_kills_per_deployed"],
                "general_score_v71": general_score,
                "burst_score_v73": burst_score,
                "general_model_matched": general_row is not None and general_score is not None,
                "burst_model_matched": burst_row is not None and burst_score is not None,
            }
        )
    empirical_values = [float(row["empirical_kills_per_deployed"]) for row in joined]
    empirical_ranks = _rank(empirical_values) if empirical_values else []
    for row, rank in zip(joined, empirical_ranks):
        row["empirical_rank"] = rank

    def correlations(score_field: str) -> dict[str, object]:
        subset = [
            row for row in joined
            if row[score_field] is not None and row["empirical_kills_per_deployed"] is not None
        ]
        empirical = [float(row["empirical_kills_per_deployed"]) for row in subset]
        scores = [float(row[score_field]) for row in subset]
        empirical_rank = _rank(empirical)
        score_rank = _rank(scores)
        for row, model_rank, observed_rank in zip(subset, score_rank, empirical_rank):
            row[f"{score_field}_rank"] = model_rank
            row[f"{score_field}_rank_residual"] = observed_rank - model_rank
        return {
            "matched_troops": len(subset),
            "score_correlation": _pearson(empirical, scores),
            "rank_correlation": _pearson(empirical_rank, score_rank),
        }

    general_stats = correlations("general_score_v71")
    burst_stats = correlations("burst_score_v73")
    fields = (
        "canonical_troop_id", "empirical_rank", "battle_count", "total_deployed", "evidence_grade",
        "empirical_kills_per_deployed", "general_score_v71", "general_score_v71_rank",
        "general_score_v71_rank_residual", "burst_score_v73", "burst_score_v73_rank",
        "burst_score_v73_rank_residual", "general_model_matched", "burst_model_matched",
    )
    joined.sort(key=lambda row: (float(row["empirical_rank"]), str(row["canonical_troop_id"])))
    write_csv(output_dir / "model_vs_empirical.csv", joined, fields)
    residuals = sorted(
        joined,
        key=lambda row: (
            -abs(float(row.get("general_score_v71_rank_residual") or 0)),
            str(row["canonical_troop_id"]),
        ),
    )
    write_csv(output_dir / "empirical_residual_rankings.csv", residuals, fields)
    full_coverage = (
        len(joined) > 0
        and general_stats["matched_troops"] == len(joined)
        and burst_stats["matched_troops"] == len(joined)
    )
    summary = {
        "schema_version": "1.0.0",
        "status": "authoritative" if full_coverage else "provisional_incomplete_model_universe",
        "canonical_overall_troops": len(joined),
        "general_v71": general_stats,
        "burst_v73": burst_stats,
        "limitations": [
            "Correlation is descriptive and does not prove model causality.",
            "Evidence grade and battle context must be considered with each residual.",
            *(
                []
                if full_coverage
                else ["Committed model snapshots do not cover every canonical troop ID."]
            ),
        ],
    }
    atomic_write_json(output_dir / "empirical_analysis_summary.json", summary)
    markdown = [
        "# Empirical analysis summary",
        "",
        f"- Status: `{summary['status']}`",
        f"- Canonical overall troops: {len(joined)}",
        f"- v7.1 matched troops: {general_stats['matched_troops']}",
        f"- v7.3 matched troops: {burst_stats['matched_troops']}",
        "",
        "This comparison keeps general and burst scores separate. Residuals are hypotheses, not automatic model changes.",
        "",
    ]
    (output_dir / "empirical_analysis_summary.md").write_text("\n".join(markdown), encoding="utf-8", newline="\n")
    return summary


def build_tier_role_views(
    aggregates_jsonl: Path,
    troop_metadata_csv: Path,
    output_dir: Path,
) -> dict[str, object]:
    aggregates = read_jsonl(aggregates_jsonl)
    metadata_rows = read_csv(troop_metadata_csv)
    metadata = _model_index(metadata_rows)
    joined = []
    unmatched = []
    for row in aggregates:
        troop_id = str(row["canonical_troop_id"])
        details = metadata.get(troop_id)
        if details is None:
            unmatched.append(troop_id)
            continue
        joined.append(
            {
                **row,
                "tier": details.get("tier") or details.get("tree_tier") or details.get("level"),
                "role": details.get("category") or details.get("primary_category") or details.get("default_group"),
            }
        )
    fields = (
        "rank", "canonical_troop_id", "battle_context", "tier", "role", "evidence_grade",
        "battle_count", "total_deployed", "total_kills", "historical_kills_per_deployed",
    )
    generated = []
    for label, key in (("tier", "tier"), ("role", "role")):
        values = sorted({str(row[key]) for row in joined if row.get(key)})
        for value in values:
            subset = [row.copy() for row in joined if str(row.get(key)) == value]
            subset.sort(key=lambda row: (-float(row["historical_kills_per_deployed"] or 0), str(row["canonical_troop_id"])))
            for index, row in enumerate(subset, 1):
                row["rank"] = index
            safe = "".join(char if char.isalnum() else "_" for char in value.casefold()).strip("_")
            path = output_dir / f"ranking_{label}_{safe}.csv"
            write_csv(path, subset, fields)
            generated.append(path.name)
    report = {
        "schema_version": "1.0.0",
        "status": "complete" if not unmatched else "partial",
        "generated_views": sorted(generated),
        "unmatched_canonical_troop_ids": sorted(set(unmatched)),
    }
    atomic_write_json(output_dir / "tier_role_view_report.json", report)
    return report


def calibration_decision(
    analysis_summary_path: Path,
    aggregates_jsonl: Path,
    output_path: Path,
) -> dict[str, object]:
    import json

    summary = json.loads(analysis_summary_path.read_text(encoding="utf-8"))
    aggregates = [
        row for row in read_jsonl(aggregates_jsonl)
        if row.get("battle_context") != "overall"
    ]
    reliable = [row for row in aggregates if row.get("evidence_grade") in {"medium", "high"}]
    contexts = sorted({str(row["battle_context"]) for row in reliable})
    sufficient = (
        summary.get("status") == "authoritative"
        and len(reliable) >= 10
        and len(contexts) >= 2
    )
    decision = {
        "schema_version": "1.0.0",
        "decision": "evaluate_new_version" if sufficient else "no_model_change",
        "canonical_coverage_sufficient": sufficient,
        "reliable_context_rows": len(reliable),
        "reliable_contexts": contexts,
        "frozen_models": ["v7.1", "v7.3"],
        "reason": (
            "Coverage passes the conservative design gate; candidate hypotheses may be evaluated in a new version."
            if sufficient
            else "Coverage/model-universe evidence is insufficient for calibration; preserve v7.1 and v7.3."
        ),
        "additional_evidence_required": (
            []
            if sufficient
            else [
                "Recover and review the production screenshot batch.",
                "Obtain at least ten medium/high context-specific troop samples across at least two contexts.",
                "Match the complete canonical troop universe to committed v7.1 and v7.3 inputs.",
                "Confirm stable residuals across independent battles before changing a formula.",
            ]
        ),
    }
    atomic_write_json(output_path, decision)
    return decision
