#!/usr/bin/env python3
"""Apply compact P1 review decisions to a P0-reviewed troop JSONL."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

FIELDS = ("survivors", "kills", "upgrade_ready", "deaths", "wounded", "routed")
REVIEW_METADATA = {
    "reviewed_at": "2026-07-26",
    "reviewer": "OpenAI GPT-5.6 Thinking with user-authorized repository workflow",
    "review_source": "manual_visual_review_exact_hash_source_screenshot",
}


def parse_optional_int(value: str | None) -> int | None:
    return None if value in (None, "") else int(value)


def source_fingerprint(row: dict[str, Any]) -> str:
    payload = [row.get("analysis_status"), *[row.get(field) for field in FIELDS]]
    serialized = json.dumps(payload, separators=(",", ":"))
    return hashlib.sha256(serialized.encode()).hexdigest()


def load_decisions(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    result = {row["observation_id"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError("Duplicate observation_id in decision file")
    return result


def apply_decision(row: dict[str, Any], decision: dict[str, str]) -> None:
    observation_id = str(row["observation_id"])
    actual_fingerprint = source_fingerprint(row)
    expected_fingerprint = decision["source_fingerprint_sha256"]
    if actual_fingerprint != expected_fingerprint:
        raise ValueError(
            f"{observation_id}: source fingerprint mismatch "
            f"{actual_fingerprint} != {expected_fingerprint}"
        )

    status = decision["review_status"]
    before = {field: row.get(field) for field in FIELDS}

    if status == "excluded":
        row.update(
            analysis_status="excluded",
            exclusion_reason=decision["exclusion_reason"],
            needs_review=False,
            review_status="excluded",
        )
    elif status in {"corrected", "confirmed"}:
        for field in FIELDS:
            reviewed = parse_optional_int(decision[f"reviewed_{field}"])
            if reviewed is not None:
                row[field] = reviewed

        row["deployed"] = (
            int(row["survivors"]) + int(row["deaths"]) + int(row["wounded"])
        )
        row["kills_per_deployed"] = (
            round(int(row["kills"]) / int(row["deployed"]), 6)
            if row["deployed"]
            else None
        )
        row["routed_rate"] = (
            round(int(row["routed"]) / int(row["deployed"]), 6)
            if row["deployed"]
            else None
        )

        extraction = row.setdefault("field_extraction", {})
        for field in FIELDS:
            extraction.setdefault(field, {}).update(
                confidence=1.0,
                source="manual_visual_review",
                uncertain=False,
                reviewed_value=row[field],
            )
        row.update(needs_review=False, review_status="reviewed")
    else:
        raise ValueError(f"{observation_id}: unsupported review status {status}")

    row.setdefault("review_history", []).append(
        {
            **REVIEW_METADATA,
            "review_status": status,
            "changed_fields": [
                value for value in decision["changed_fields"].split(";") if value
            ],
            "before": before,
            "after": {field: row.get(field) for field in FIELDS},
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="P0-reviewed troop JSONL")
    parser.add_argument("decisions", type=Path, help="compact P1 decision CSV")
    parser.add_argument("output", type=Path, help="P1-reviewed output JSONL")
    args = parser.parse_args()

    decisions = load_decisions(args.decisions)
    seen: set[str] = set()
    counts = {"corrected": 0, "confirmed": 0, "excluded": 0}
    output_rows: list[dict[str, Any]] = []

    with args.input.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON on {args.input}:{line_number}: {exc}"
                ) from exc

            observation_id = str(row.get("observation_id"))
            decision = decisions.get(observation_id)
            if decision:
                apply_decision(row, decision)
                seen.add(observation_id)
                counts[decision["review_status"]] += 1
            output_rows.append(row)

    missing = set(decisions) - seen
    if missing:
        raise ValueError(f"Decisions not found in input: {sorted(missing)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in output_rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    print(
        json.dumps(
            {
                "input_rows": len(output_rows),
                "decisions_applied": len(seen),
                "counts": counts,
                "remaining_needs_review": sum(
                    bool(row.get("needs_review")) for row in output_rows
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
