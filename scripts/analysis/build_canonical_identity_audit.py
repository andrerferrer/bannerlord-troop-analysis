#!/usr/bin/env python3
"""Build a conservative multi-track canonical troop identity audit.

The resolver accepts one or more track-level ``<track>_troops.csv`` files created by
``rebuild_vanilla_audit.py``. It only accepts exact normalized display-name matches;
it never treats a provisional slug as a game/XML troop ID.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

CONFIRMED = "confirmed_id"
OUTPUT_COLUMNS = [
    "provisional_slug",
    "display_name",
    "observed_track",
    "canonical_troop_id",
    "match_status",
    "resolution_method",
    "evidence_path",
    "evidence_detail",
    "candidate_count",
    "candidate_tracks",
    "candidate_troop_ids",
    "blocking_reason",
]


@dataclass(frozen=True)
class Candidate:
    track: str
    troop_id: str
    source_name: str
    source_path: str


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_display_name(value: str) -> str:
    """Normalize formatting noise without fuzzy matching or token substitution."""
    text = unicodedata.normalize("NFKC", value or "")
    text = text.replace("’", "'").replace("‘", "'").replace("`", "'")
    text = re.sub(r"^\s*>\s*", "", text)
    # Result tables append tier labels that are not part of XML display names.
    text = re.sub(r"\s*\[(?:\s*(?:t|tier)?\s*[0-9s]{1,2}|ts|t5|t6)\s*\]\s*$", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" .")
    return text.casefold()


def parse_track_audit(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("--track-audit must use TRACK=PATH")
    track, raw_path = value.split("=", 1)
    track = track.strip()
    path = Path(raw_path.strip())
    if not track or not raw_path.strip():
        raise argparse.ArgumentTypeError("--track-audit must use non-empty TRACK=PATH")
    return track, path


def load_candidates(specs: list[tuple[str, Path]]) -> dict[str, list[Candidate]]:
    seen_tracks: set[str] = set()
    by_name: dict[str, list[Candidate]] = defaultdict(list)
    for track, path in specs:
        if track in seen_tracks:
            raise ValueError(f"Duplicate --track-audit track: {track}")
        seen_tracks.add(track)
        rows = read_rows(path)
        if rows and not {"troop_id", "name"}.issubset(rows[0]):
            raise ValueError(f"{path}: expected troop_id and name columns")
        for row in rows:
            troop_id = (row.get("troop_id") or "").strip()
            source_name = (row.get("name") or "").strip()
            if not troop_id or not source_name:
                continue
            candidate = Candidate(track, troop_id, source_name, str(path))
            key = normalize_display_name(source_name)
            if candidate not in by_name[key]:
                by_name[key].append(candidate)
    return by_name


def unique_candidates(candidates: list[Candidate]) -> list[Candidate]:
    result: list[Candidate] = []
    seen: set[tuple[str, str]] = set()
    for candidate in candidates:
        key = (candidate.track, candidate.troop_id)
        if key not in seen:
            seen.add(key)
            result.append(candidate)
    return result


def resolve_row(
    baseline_row: dict[str, str],
    existing: dict[str, str] | None,
    candidates_by_name: dict[str, list[Candidate]],
) -> dict[str, str]:
    slug = baseline_row["canonical_name_slug"].strip()
    display_name = (baseline_row.get("display_name") or baseline_row.get("display_name_raw") or slug).strip()
    existing = existing or {}
    track_hint = (existing.get("observed_track") or "").strip()
    if track_hint == "unresolved":
        track_hint = ""

    candidates = unique_candidates(candidates_by_name.get(normalize_display_name(display_name), []))
    if track_hint:
        hinted = [candidate for candidate in candidates if candidate.track == track_hint]
        # A verified track hint is a hard boundary: never silently cross tracks.
        candidates = hinted

    candidate_tracks = sorted({candidate.track for candidate in candidates})
    candidate_ids = sorted({candidate.troop_id for candidate in candidates})
    base = {
        "provisional_slug": slug,
        "display_name": display_name,
        "observed_track": track_hint or (candidate_tracks[0] if len(candidate_tracks) == 1 else "unresolved"),
        "canonical_troop_id": "",
        "match_status": "unresolved",
        "resolution_method": "",
        "evidence_path": "",
        "evidence_detail": "",
        "candidate_count": str(len(candidates)),
        "candidate_tracks": "|".join(candidate_tracks),
        "candidate_troop_ids": "|".join(candidate_ids),
        "blocking_reason": "No unique exact name-to-ID match in supplied track audits",
    }

    existing_status = (existing.get("match_status") or "").strip()
    existing_id = (existing.get("canonical_troop_id") or "").strip()

    if existing_status == CONFIRMED and existing_id:
        if not candidates:
            return {
                **base,
                **{column: existing.get(column, base.get(column, "")) for column in OUTPUT_COLUMNS},
                "provisional_slug": slug,
                "display_name": display_name,
                "match_status": CONFIRMED,
                "canonical_troop_id": existing_id,
                "resolution_method": existing.get("resolution_method") or "preserved_manual_confirmation",
                "candidate_count": "0",
                "candidate_tracks": "",
                "candidate_troop_ids": "",
                "blocking_reason": "",
            }
        if len(candidates) == 1 and candidates[0].troop_id == existing_id:
            candidate = candidates[0]
            return {
                **base,
                "observed_track": candidate.track,
                "canonical_troop_id": candidate.troop_id,
                "match_status": CONFIRMED,
                "resolution_method": "exact_normalized_name_verified_existing",
                "evidence_path": candidate.source_path,
                "evidence_detail": f"Exact normalized display-name match: {candidate.source_name}",
                "blocking_reason": "",
            }
        return {
            **base,
            "observed_track": track_hint or "unresolved",
            "match_status": "conflict_existing_vs_track_audit",
            "resolution_method": "manual_confirmation_conflict",
            "evidence_path": existing.get("evidence_path", ""),
            "evidence_detail": f"Existing confirmed ID {existing_id} conflicts with supplied audit candidate(s)",
            "blocking_reason": "Resolve conflict before canonical joins",
        }

    if len(candidates) == 1:
        candidate = candidates[0]
        return {
            **base,
            "observed_track": candidate.track,
            "canonical_troop_id": candidate.troop_id,
            "match_status": CONFIRMED,
            "resolution_method": "exact_normalized_name",
            "evidence_path": candidate.source_path,
            "evidence_detail": f"Exact normalized display-name match: {candidate.source_name}",
            "blocking_reason": "",
        }

    if len(candidates) > 1:
        return {
            **base,
            "match_status": "ambiguous_exact_name",
            "resolution_method": "exact_name_multiple_candidates",
            "evidence_path": "|".join(sorted({candidate.source_path for candidate in candidates})),
            "evidence_detail": "Multiple exact normalized name matches",
            "blocking_reason": "Select the correct track/troop ID explicitly",
        }

    if existing:
        preserved = {column: existing.get(column, base.get(column, "")) for column in OUTPUT_COLUMNS}
        return {
            **base,
            **preserved,
            "provisional_slug": slug,
            "display_name": display_name,
            "candidate_count": "0",
            "candidate_tracks": "",
            "candidate_troop_ids": "",
        }
    return base


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path, help="reviewed ranking/baseline CSV")
    parser.add_argument("output", type=Path, help="canonical identity audit CSV")
    parser.add_argument("--existing-audit", type=Path)
    parser.add_argument(
        "--track-audit",
        type=parse_track_audit,
        action="append",
        default=[],
        metavar="TRACK=PATH",
        help="track-level <track>_troops.csv; repeat for multiple tracks",
    )
    parser.add_argument("--report", type=Path, help="optional JSON resolution report")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    baseline = read_rows(args.baseline)
    if baseline and "canonical_name_slug" not in baseline[0]:
        raise ValueError(f"{args.baseline}: expected canonical_name_slug column")

    existing_rows = read_rows(args.existing_audit) if args.existing_audit else []
    existing_by_slug = {row["provisional_slug"]: row for row in existing_rows}
    if len(existing_by_slug) != len(existing_rows):
        raise ValueError("Duplicate provisional_slug in existing identity audit")

    candidates_by_name = load_candidates(args.track_audit)
    resolved_by_slug: dict[str, dict[str, str]] = {}
    for row in baseline:
        slug = row["canonical_name_slug"].strip()
        if slug not in resolved_by_slug:
            resolved_by_slug[slug] = resolve_row(row, existing_by_slug.get(slug), candidates_by_name)

    output_rows = list(resolved_by_slug.values())
    unresolved = [row for row in output_rows if row["match_status"] != CONFIRMED]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(output_rows)

    report = {
        "baseline_labels": len(output_rows),
        "confirmed_ids": len(output_rows) - len(unresolved),
        "unresolved": len(unresolved),
        "status_counts": {},
        "track_audits": [{"track": track, "path": str(path)} for track, path in args.track_audit],
        "unresolved_slugs": [row["provisional_slug"] for row in unresolved],
    }
    for row in output_rows:
        status = row["match_status"]
        report["status_counts"][status] = report["status_counts"].get(status, 0) + 1

    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, sort_keys=True))
    if args.require_complete and unresolved:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
