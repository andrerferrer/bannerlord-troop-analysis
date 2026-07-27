#!/usr/bin/env python3
"""Apply approved provisional troop aliases without overwriting raw OCR names."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="reviewed troop-occurrence JSONL")
    parser.add_argument("aliases", type=Path, help="alias CSV")
    parser.add_argument("output", type=Path, help="canonicalized output JSONL")
    args = parser.parse_args()

    aliases: dict[str, str] = {}
    with args.aliases.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["status"] == "approved":
                aliases[row["alias_slug"]] = row["canonical_slug"]

    output_rows: list[dict[str, object]] = []
    changed = 0
    with args.input.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on {args.input}:{line_number}: {exc}") from exc

            old_slug = row.get("canonical_name_slug")
            if old_slug in aliases:
                row["canonical_name_slug_original"] = old_slug
                row["canonical_name_slug"] = aliases[str(old_slug)]
                row["alias_resolution_source"] = "approved_alias_table"
                changed += 1
            output_rows.append(row)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in output_rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    print(
        json.dumps(
            {
                "rows": len(output_rows),
                "aliases": len(aliases),
                "rows_changed": changed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
