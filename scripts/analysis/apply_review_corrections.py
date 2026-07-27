#!/usr/bin/env python3
"""Apply auditable review-correction CSV files to normalized troop JSONL."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable

CORE_FIELDS = ("survivors", "kills", "deaths", "wounded")
OPTIONAL_FIELDS = ("upgrade_ready", "routed")
ALL_FIELDS = CORE_FIELDS + OPTIONAL_FIELDS


def parse_optional_int(value: str | None) -> int | None:
    if value is None or value == "":
        return None
    return int(value)


def load_corrections(paths: Iterable[Path]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                observation_id = row["observation_id"]
                if observation_id in result:
                    raise ValueError(f"Duplicate correction: {observation_id}")
                result[observation_id] = row
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="raw primary troop-occurrence JSONL")
    parser.add_argument("output", type=Path, help="reviewed output JSONL")
    parser.add_argument(
        "--corrections",
        type=Path,
        nargs="+",
        required=True,
        help="one or more correction CSV files; shell globs are supported",
    )
    args = parser.parse_args()

    corrections = load_corrections(args.corrections)
    seen: set[str] = set()
    output_rows: list[dict[str, Any]] = []

    with args.input.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on {args.input}:{line_number}: {exc}") from exc

            observation_id = row.get("observation_id")
            correction = corrections.get(observation_id)
            if correction:
                seen.add(str(observation_id))
                before = {field: row.get(field) for field in ALL_FIELDS}

                for field in CORE_FIELDS:
                    expected = parse_optional_int(correction[f"original_{field}"])
                    if row.get(field) != expected:
                        raise ValueError(
                            f"{observation_id}: original {field} mismatch "
                            f"{row.get(field)} != {expected}"
                        )
                    row[field] = int(correction[f"reviewed_{field}"])

                for field in OPTIONAL_FIELDS:
                    expected = parse_optional_int(correction[f"original_{field}"])
                    if row.get(field) != expected:
                        raise ValueError(
                            f"{observation_id}: original {field} mismatch "
                            f"{row.get(field)} != {expected}"
                        )
                    reviewed = parse_optional_int(correction[f"reviewed_{field}"])
                    if reviewed is not None:
                        row[field] = reviewed

                row["deployed"] = int(row["survivors"]) + int(row["deaths"]) + int(row["wounded"])
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
                reviewed_fields = list(CORE_FIELDS)
                for field in OPTIONAL_FIELDS:
                    if correction[f"reviewed_{field}"] != "":
                        reviewed_fields.append(field)
                for field in reviewed_fields:
                    detail = extraction.setdefault(field, {})
                    detail["confidence"] = 1.0
                    detail["source"] = "manual_visual_review"
                    detail["uncertain"] = False
                    detail["reviewed_value"] = row[field]

                row.setdefault("review_history", []).append(
                    {
                        "reviewed_at": correction["reviewed_at"],
                        "reviewer": correction["reviewer"],
                        "review_source": correction["review_source"],
                        "review_status": correction["review_status"],
                        "changed_fields": [
                            value for value in correction["changed_fields"].split(";") if value
                        ],
                        "before": before,
                        "after": {field: row.get(field) for field in ALL_FIELDS},
                        "note": correction["review_note"],
                        "source_image_indices": [
                            int(value)
                            for value in correction["source_image_indices"].split(";")
                            if value
                        ],
                    }
                )
                row["needs_review"] = any(
                    bool((value or {}).get("uncertain")) for value in extraction.values()
                )
                row["review_status"] = (
                    "reviewed" if not row["needs_review"] else "partially_reviewed"
                )

            output_rows.append(row)

    missing = set(corrections) - seen
    if missing:
        raise ValueError(f"Corrections not found in input: {sorted(missing)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in output_rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    print(
        json.dumps(
            {
                "input_rows": len(output_rows),
                "corrections_applied": len(seen),
                "remaining_needs_review": sum(
                    bool(row.get("needs_review")) for row in output_rows
                ),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
