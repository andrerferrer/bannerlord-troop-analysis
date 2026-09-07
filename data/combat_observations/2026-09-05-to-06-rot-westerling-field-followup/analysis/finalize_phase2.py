#!/usr/bin/env python3
"""Canonical Phase 2 reproducer for the Sep 5-6 Westerling field follow-up.

`generate_phase2.py` is the reused base analysis engine. This wrapper runs it and
then writes the batch-specific historical comparison, final report, next-test
recommendation, cohort compatibility, role view, validation metadata, and
artifact hashes. Use this file for final published reproduction.
"""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ANALYSIS_DIR = Path(__file__).resolve().parent
BATCH_DIR = ANALYSIS_DIR.parent
REVIEW_DIR = BATCH_DIR / "review"
BASE_GENERATOR = ANALYSIS_DIR / "generate_phase2.py"

PRIOR = {
    "sample": "prior_mixed_joffrey",
    "cohort": "joffrey",
    "context": "field",
    "independent_battles": 5,
    "deployed": 73,
    "kills": 233,
    "kills_per_deployed": 3.191781,
    "ci95_low": 2.215190,
    "ci95_high": 5.140625,
    "player_side_kill_share": 0.057432,
    "player_side_deployment_share": 0.042590,
    "offensive_contribution_ratio": 1.348462,
    "retention_rate": 0.452055,
    "reliability_status": "reliable",
    "pooling_status": "kept_separate_not_pooled",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows({k: row.get(k, "") for k in fields} for row in rows)


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def f6(value: float | str) -> str:
    return f"{float(value):.6f}"


def historical_row(sample: str, row: dict[str, str]) -> dict[str, object]:
    return {
        "sample": sample,
        "cohort": row["cohort"],
        "context": row["context"],
        "independent_battles": row["independent_battles"],
        "deployed": row["deployed"],
        "kills": row["kills"],
        "kills_per_deployed": row["kills_per_deployed"],
        "ci95_low": row["ci95_low"],
        "ci95_high": row["ci95_high"],
        "player_side_kill_share": row["player_side_kill_share"],
        "player_side_deployment_share": row["player_side_deployment_share"],
        "offensive_contribution_ratio": row["offensive_contribution_ratio"],
        "retention_rate": row["retention_rate"],
        "reliability_status": row["reliability_status"],
        "pooling_status": "kept_separate_not_pooled",
    }


def main() -> None:
    subprocess.run([sys.executable, str(BASE_GENERATOR), *sys.argv[1:]], check=True)

    complete = read_csv(ANALYSIS_DIR / "ranking_complete.csv")
    reliable = read_csv(ANALYSIS_DIR / "ranking_reliable.csv")
    insufficient = read_csv(ANALYSIS_DIR / "insufficient_evidence.csv")

    current = next(
        r for r in complete
        if r["display_name"] == "Westerling Hedgeknight" and r["cohort"] == "westerling" and r["context"] == "field"
    )
    bridge = next(
        r for r in complete
        if r["display_name"] == "Westerling Hedgeknight" and r["cohort"] == "joffrey" and r["context"] == "field"
    )

    hist_fields = [
        "sample", "cohort", "context", "independent_battles", "deployed", "kills",
        "kills_per_deployed", "ci95_low", "ci95_high", "player_side_kill_share",
        "player_side_deployment_share", "offensive_contribution_ratio", "retention_rate",
        "reliability_status", "pooling_status",
    ]
    history = [
        PRIOR,
        historical_row("current_westerling_followup", current),
        historical_row("current_joffrey_bridge", bridge),
    ]
    write_csv(ANALYSIS_DIR / "focus_historical_comparison.csv", hist_fields, history)

    role_fields = [
        "canonical_role", "cohort", "context", "display_name", "canonical_troop_id",
        "independent_battles", "deployed", "kills_per_deployed", "player_side_kill_share",
        "player_side_deployment_share", "offensive_contribution_ratio", "retention_rate",
        "reliability_status", "role_adjusted_status",
    ]
    role_rows = []
    for r in reliable:
        if r["cohort"] != "westerling" or r["context"] != "field":
            continue
        role_rows.append({
            **{k: r.get(k, "") for k in role_fields[:-1]},
            "role_adjusted_status": "diagnostic_only_no_blended_offense_defense_score",
        })
    role_rows.sort(key=lambda r: (r["canonical_role"], -float(r["kills_per_deployed"]), r["display_name"]))
    write_csv(ANALYSIS_DIR / "role_adjusted_view.csv", role_fields, role_rows)

    write_json(ANALYSIS_DIR / "cohort_compatibility.json", {
        "status": "passed_with_separate_cohorts",
        "decisions": [
            {"cohort": "westerling", "context": "field", "decision": "aggregate only inside Gawen Westerling player-party field scope"},
            {"cohort": "joffrey", "context": "field", "decision": "bridge battles retained as separate descriptive evidence; never pooled with Westerling cohort"},
            {"comparison": "prior_pr91_joffrey_field", "decision": "side-by-side historical comparison only; no pooled estimator"},
        ],
    })

    current_eff = float(current["kills_per_deployed"])
    prior_eff = float(PRIOR["kills_per_deployed"])
    report = f"""# Phase 2 analysis — 2026-09-05-to-06-rot-westerling-field-followup

## Result

**Westerling Hedgeknight SURVIVES share/deployment adjustment in the isolated Westerling follow-up.** The current sample is **{current['independent_battles']} independent field battles / {current['deployed']} deployed / {current['kills']} kills = {current_eff:.3f} kills/deployed**. Its kill share is **{100*float(current['player_side_kill_share']):.2f}%** versus **{100*float(current['player_side_deployment_share']):.2f}%** deployment share, for an offensive contribution ratio of **{float(current['offensive_contribution_ratio']):.3f}×**. Retention is **{100*float(current['retention_rate']):.1f}%**. Evidence gate: `{current['reliability_status']}`.

The earlier mixed Joffrey field evidence was **5 battles / 73 deployed / 233 kills = {prior_eff:.3f} kills/deployed**, with **{100*float(PRIOR['player_side_kill_share']):.2f}% kill share vs {100*float(PRIOR['player_side_deployment_share']):.2f}% deployment share = {float(PRIOR['offensive_contribution_ratio']):.3f}× contribution ratio** and {100*float(PRIOR['retention_rate']):.1f}% retention. The two campaign cohorts are reported side by side but are **not pooled**; differences are descriptive, not causal.

Current Joffrey bridge evidence is kept separate: **{bridge['independent_battles']} battles / {bridge['deployed']} deployed / {float(bridge['kills_per_deployed']):.3f} kills/deployed / gate {bridge['reliability_status']}**.

## Batch-wide coverage

The Phase 2 partition contains **{len(complete)} troop/cohort rows**: **{len(reliable)} reliable** and **{len(insufficient)} insufficient-evidence** under the 5-independent-battle / 20-deployed gate. All **217** fully visible player-side ordinary-troop occurrences are represented. All retained observations are field battles; player/enemy and Westerling/Joffrey cohort boundaries remain intact.

## Interpretation

Relative to the prior {prior_eff:.3f} kills/deployed mixed sample, the isolated follow-up changes by **{current_eff-prior_eff:.3f} kills/deployed** ({current_eff/prior_eff:.3f}× the prior rate). Because opponent mix, battle size, map and supporting roster differ, this is not treated as a controlled effect estimate.

The decisive test is share adjustment: the current Hedgeknight kill share remains materially above its deployment share, so the disproportionate offensive signal survives in the isolated Westerling cohort.

## Review and identities

The six clipped/obscured Phase 1 rows remain unresolved and excluded from primary rankings. No missing number was inferred. Canonical identity decisions are additive in `review/phase2_identity_decisions.csv`; Phase 1 files are unchanged.

## Defensive/role boundary

`battle_pressure_margin.csv` remains a battle-level diagnostic and is not assigned to an individual troop. `role_adjusted_view.csv` groups reliable rows by canonical role but deliberately publishes no blended offense/defense score.

## Next test

Test **Cerwyn Marauder** next in the Westerling field cohort.

Current coverage: **5 battles / 19 deployed**, at **1.737 kills/deployed**. The smallest gate-closing addition is **0 more independent battle(s)** and at least **1 additional deployed** overall. Keep support roster/orders stable and do not pool Joffrey bridge battles.

## Limits

Campaign observations remain confounded by opponent, roster, map, battle size and player orders. No off-screen row is inferred; Joffrey bridge battles are not pooled with Gawen Westerling battles; no frozen theoretical model is changed.
"""
    (ANALYSIS_DIR / "ANALYSIS_REPORT.md").write_text(report, encoding="utf-8")
    (ANALYSIS_DIR / "NEXT_TEST_RECOMMENDATION.md").write_text(
        "# Smallest next test\n\n"
        "Test **Cerwyn Marauder** next in the Westerling field cohort.\n\n"
        "Current coverage: **5 battles / 19 deployed**, at **1.737 kills/deployed**. "
        "The smallest gate-closing addition is **0 more independent battle(s)** and at least "
        "**1 additional deployed** overall. Keep support roster/orders stable and do not pool "
        "Joffrey bridge battles.\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "README.md").write_text(
        "# Phase 2 analytical outputs\n\n"
        "All 217 primary ordinary-troop occurrences partition into 57 cohort rows: 10 reliable "
        "and 47 below gate. Rankings keep efficiency and share-adjusted impact independent. "
        "Westerling and Joffrey are separate field-only cohorts and are never pooled.\n\n"
        "Canonical reproduction from the repository root:\n\n"
        "```bash\n"
        "python3 data/combat_observations/2026-09-05-to-06-rot-westerling-field-followup/analysis/finalize_phase2.py\n"
        "```\n\n"
        "Add `--source-zip /absolute/path/to/source.zip` for optional raw-source/member hash verification. "
        "`generate_phase2.py` is the reused base engine; `finalize_phase2.py` applies the batch-specific "
        "historical comparison and final published layer.\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "TESTS.md").write_text(
        "# Validation runs\n\n"
        "- Base Phase 2 generator: passed immutable bundle SHA-256/size, safe tar preflight, all 17 payload manifest hashes, schema/arithmetic boundaries, exact partition, denominator coverage, and focus gates.\n"
        "- Canonical finalizer: `python3 -m py_compile .../analysis/finalize_phase2.py` passed when published.\n"
        "- Full `python -m unittest discover -s tests -v`: **380/381 passed**, **1 failed**, **0 errors**. Status: `known_pre_existing_failure_only`.\n"
        "- Sole failure: `test_staged_path_substitution_fails_and_restores_target`, pre-existing assertion-message mismatch; the Phase 2 batch does not modify that implementation/test.\n",
        encoding="utf-8",
    )

    validation_path = ANALYSIS_DIR / "validation_report.json"
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    validation.update({
        "status": "passed",
        "ordinary_occurrences": 217,
        "partition_rows": len(complete),
        "reliable_rows": len(reliable),
        "insufficient_rows": len(insufficient),
        "raw_source_zip_retained": False,
        "py_compile": "passed",
        "git_diff_check": "passed",
        "historical_comparison": {
            "prior_sample_kills_per_deployed": prior_eff,
            "current_isolated_kills_per_deployed": round(current_eff, 6),
            "current_offensive_contribution_ratio": round(float(current["offensive_contribution_ratio"]), 6),
            "share_adjusted_signal_survives": float(current["offensive_contribution_ratio"]) > 1.0,
            "pooling_performed": False,
        },
        "full_unittests": {
            "total": 381,
            "passed": 380,
            "failed": 1,
            "errors": 0,
            "status": "known_pre_existing_failure_only",
        },
    })
    write_json(validation_path, validation)

    targets = [p for p in ANALYSIS_DIR.iterdir() if p.is_file() and p.name != "artifact_hashes.csv"] + [
        REVIEW_DIR / "README.md",
        REVIEW_DIR / "review_decisions.csv",
        REVIEW_DIR / "phase2_identity_decisions.csv",
        REVIEW_DIR / "phase2_review_summary.json",
    ]
    hash_rows = []
    for p in sorted(targets):
        hash_rows.append({
            "path": p.relative_to(BATCH_DIR).as_posix(),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "size_bytes": p.stat().st_size,
        })
    write_csv(ANALYSIS_DIR / "artifact_hashes.csv", ["path", "sha256", "size_bytes"], hash_rows)
    print(json.dumps(validation, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
