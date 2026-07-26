#!/usr/bin/env python3
"""Join empirical rankings to an explicit multi-track canonical identity audit."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

REQUIRED_ID_STATUS = "confirmed_id"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("identity_audit", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--require-complete",
        action="store_true",
        help="Fail unless every baseline troop has a confirmed canonical ID.",
    )
    args = parser.parse_args()

    baseline = read_rows(args.baseline)
    identity_rows = read_rows(args.identity_audit)
    identity = {row["provisional_slug"]: row for row in identity_rows}
    if len(identity) != len(identity_rows):
        raise ValueError("Duplicate provisional_slug in identity audit")

    output: list[dict[str, str]] = []
    unresolved: set[str] = set()
    for row in baseline:
        slug = row["canonical_name_slug"]
        match = identity.get(slug)
        if match is None:
            unresolved.add(slug)
            match = {
                "observed_track": "unresolved",
                "canonical_troop_id": "",
                "match_status": "missing_audit_row",
                "evidence_path": "",
            }
        elif match["match_status"] != REQUIRED_ID_STATUS:
            unresolved.add(slug)

        output.append(
            {
                **row,
                "observed_track": match["observed_track"],
                "canonical_troop_id": match["canonical_troop_id"],
                "identity_match_status": match["match_status"],
                "identity_evidence_path": match["evidence_path"],
            }
        )

    if args.require_complete and unresolved:
        raise ValueError(
            "Canonical identity gate failed; unresolved slugs: "
            + ", ".join(sorted(unresolved))
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(output[0]) if output else []
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)

    print(
        f"rows={len(output)} confirmed_ids={len(output) - len(unresolved)} "
        f"unresolved={len(unresolved)}"
    )


if __name__ == "__main__":
    main()
