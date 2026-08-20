#!/usr/bin/env python3
"""Re-audit committed combat batches under normalization pipeline v0.4 rules."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import re
import tarfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

try:
    from scripts.analysis.analyze_normalized_combat_batch import (
        verified_player_side_kill_totals,
    )
except ModuleNotFoundError:  # Direct execution from scripts/analysis.
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.analysis.analyze_normalized_combat_batch import (
        verified_player_side_kill_totals,
    )


METRIC_FIELDS = (
    "batch",
    "track",
    "context",
    "efficiency_rank",
    "impact_rank",
    "rank_delta",
    "display_name",
    "provisional_slug",
    "canonical_troop_id",
    "identity_status",
    "independent_battles",
    "deployed",
    "kills",
    "kills_per_deployed",
    "verified_player_side_total_kills",
    "player_side_kill_share",
    "share_adjusted_impact",
    "kill_share_coverage_battles",
    "kill_share_coverage_complete",
    "kill_share_status",
    "kill_share_denominator_provenance",
    "reliability_status",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def write_csv(path: Path, fields: Iterable[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def normalized_capture_name(value: str) -> str:
    name = Path(value).name.casefold()
    return re.sub(r"\s*\(\d+\)(?=\.[^.]+$)", "", name)


def screenshot_audit_rows(data_root: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for batch in sorted(path for path in data_root.iterdir() if path.is_dir()):
        inventory = batch / "source_inventory.csv"
        manifest = batch / "screenshots_manifest.csv"
        source = inventory if inventory.is_file() else manifest
        if not source.is_file():
            continue
        for row in read_csv(source):
            candidates.append(
                {
                    "batch": batch.name,
                    "source_file": source.name,
                    "screenshot_id": row.get("screenshot_id") or row.get("source_id") or "",
                    "image_file": row.get("image_file", ""),
                    "image_sha256": row.get("image_sha256", ""),
                    "captured_at": row.get("captured_at", ""),
                    "battle_id": row.get("battle_id") or row.get("battle_or_batch_id") or "",
                    "screen_status": row.get("screen_status", ""),
                    "included_in_primary": row.get("included_in_primary", ""),
                    "selection_reason": row.get("selection_reason", ""),
                }
            )

    included_by_battle: Counter[tuple[str, str]] = Counter(
        (str(row["batch"]), str(row["battle_id"]))
        for row in candidates
        if str(row["included_in_primary"]).casefold() == "true" and row["battle_id"]
    )
    first_by_hash: dict[str, dict[str, Any]] = {}
    first_by_capture: dict[tuple[str, str], dict[str, Any]] = {}
    output: list[dict[str, Any]] = []
    for row in candidates:
        image_hash = str(row["image_sha256"])
        capture_key = (
            str(row["captured_at"]),
            normalized_capture_name(str(row["image_file"])),
        )
        prior = first_by_hash.get(image_hash) if image_hash else None
        match_kind = "exact_sha256" if prior else ""
        if prior is None and all(capture_key):
            prior = first_by_capture.get(capture_key)
            match_kind = "capture_identity_and_filename" if prior else ""

        included = str(row["included_in_primary"]).casefold() == "true"
        status = str(row["screen_status"]).casefold()
        multi_primary = included_by_battle[(str(row["batch"]), str(row["battle_id"]))] > 1
        if prior and str(prior["batch"]) != str(row["batch"]):
            decision = "skip_already_normalized"
            representative = f"{prior['batch']}:{prior['screenshot_id']}"
            reason = f"Historical {match_kind} match."
            visual_status = "not_required_exact_history_match"
        elif not included and "duplicate" in status:
            decision = "skip_internal_duplicate"
            representative = str(row.get("selection_reason", ""))
            reason = str(row.get("selection_reason") or row["screen_status"])
            visual_status = "documented_existing_decision"
        elif not included and any(token in status for token in ("active", "progress", "superseded")):
            decision = "skip_nonfinal_or_superseded"
            representative = str(row.get("selection_reason", ""))
            reason = str(row.get("selection_reason") or row["screen_status"])
            visual_status = "documented_existing_decision"
        elif not included:
            decision = "skip_existing_excluded"
            representative = str(row.get("selection_reason", ""))
            reason = str(row.get("selection_reason") or row["screen_status"])
            visual_status = "documented_existing_decision"
        elif multi_primary:
            decision = "keep_grouped_pending_visual_representative_audit"
            representative = str(row["battle_id"])
            reason = (
                "Multiple primary screens share one battle ID, so independence is preserved; "
                "raw pixels are unavailable here to choose representative versus supplemental."
            )
            visual_status = "blocked_raw_screenshot_not_retained"
        else:
            decision = "keep_existing_representative"
            representative = str(row["screenshot_id"])
            reason = "Single committed primary screen for this battle."
            visual_status = "manifest_only_no_new_visual_claim"

        output.append(
            {
                **row,
                "decision": decision,
                "representative_or_prior": representative,
                "same_battle_group": bool(row["battle_id"]),
                "visual_audit_status": visual_status,
                "reason": reason,
            }
        )
        if image_hash and image_hash not in first_by_hash:
            first_by_hash[image_hash] = row
        if all(capture_key) and capture_key not in first_by_capture:
            first_by_capture[capture_key] = row
    return output


def _safe_member_name(name: str) -> bool:
    path = PurePosixPath(name)
    return not path.is_absolute() and ".." not in path.parts and bool(path.parts)


def load_normalized_archive(batch: Path) -> dict[str, Any]:
    verification_path = batch / "analysis" / "input_verification.json"
    verification = read_json(verification_path) if verification_path.is_file() else {}
    normalized_archive = verification.get("normalized_archive")
    expected = str(
        verification.get("normalized_archive_sha256")
        or (
            normalized_archive.get("expected_sha256")
            if isinstance(normalized_archive, dict)
            else ""
        )
        or ""
    )
    parts = sorted((batch / "bundle").glob("*.base64.part-*"))
    if not parts:
        return {"status": "missing_bundle_parts", "expected_sha256": expected}
    try:
        encoded = b"".join(b"".join(part.read_bytes().split()) for part in parts)
        archive = base64.b64decode(encoded, validate=True)
    except (OSError, ValueError) as error:
        return {
            "status": "base64_decode_failed",
            "expected_sha256": expected,
            "error": str(error),
        }
    actual = hashlib.sha256(archive).hexdigest()
    if not expected:
        return {
            "status": "missing_expected_archive_hash",
            "actual_sha256": actual,
            "expected_sha256": "",
        }
    if actual != expected:
        return {
            "status": "archive_hash_mismatch",
            "actual_sha256": actual,
            "expected_sha256": expected,
        }
    try:
        with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as handle:
            files = [member for member in handle.getmembers() if member.isfile()]
            if any(not _safe_member_name(member.name) for member in files):
                return {
                    "status": "unsafe_archive_member",
                    "actual_sha256": actual,
                    "expected_sha256": expected,
                }

            def jsonl(suffix: str) -> list[dict[str, Any]]:
                matches = [
                    member
                    for member in files
                    if PurePosixPath(member.name).name == suffix
                ]
                if len(matches) != 1:
                    raise ValueError(f"expected one {suffix}, found {len(matches)}")
                extracted = handle.extractfile(matches[0])
                if extracted is None:
                    raise ValueError(f"cannot read {matches[0].name}")
                return [
                    json.loads(line)
                    for line in extracted.read().decode("utf-8").splitlines()
                    if line.strip()
                ]

            return {
                "status": "verified",
                "actual_sha256": actual,
                "expected_sha256": expected,
                "battles": jsonl("battles.jsonl"),
                "occurrences": jsonl("troop_occurrences.jsonl"),
                "consolidated": jsonl("troop_battle_consolidated.jsonl"),
            }
    except (tarfile.TarError, OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
        return {
            "status": "archive_parse_failed",
            "actual_sha256": actual,
            "expected_sha256": expected,
            "error": str(error),
        }


def augment_rankings(
    batch_name: str,
    track: str,
    ranking_rows: list[dict[str, str]],
    consolidated: list[dict[str, Any]],
    totals: dict[tuple[str, str], dict[str, Any]],
    archive_status: str,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in consolidated:
        grouped[(str(row.get("battle_context")), str(row.get("display_name_normalized")))].append(row)

    output: list[dict[str, Any]] = []
    for ranking in ranking_rows:
        context = str(ranking.get("context", ""))
        slug = str(ranking.get("provisional_slug", ""))
        rows = grouped.get((context, slug), [])
        efficiency_rank = int(ranking["rank"])
        independent_battles = int(ranking["independent_battles"])
        deployed = int(ranking["deployed"])
        kills = int(ranking["kills"])
        kills_per_deployed = float(ranking["kills_per_deployed"])
        grouping_valid = (
            len({str(row.get("battle_id")) for row in rows}) == independent_battles
            and sum(int(row.get("deployed", 0)) for row in rows) == deployed
            and sum(int(row.get("kills", 0)) for row in rows) == kills
        )
        battle_keys = {(str(row.get("battle_id")), context) for row in rows}
        covered = {key: totals[key] for key in battle_keys if key in totals}
        coverage_complete = grouping_valid and len(covered) == independent_battles
        verified_total = (
            sum(int(value["kills"]) for value in covered.values())
            if coverage_complete
            else None
        )
        if verified_total is not None and kills > verified_total:
            coverage_complete = False
            verified_total = None
            status = "invalid_troop_kills_exceed_side_total"
        elif archive_status != "verified":
            status = archive_status
        elif not grouping_valid:
            status = "ranking_consolidation_mismatch"
        elif not coverage_complete:
            status = "missing_player_side_total"
        else:
            status = "complete"
        kill_share = kills / verified_total if verified_total else None
        impact = kills_per_deployed * kill_share if kill_share is not None else None
        output.append(
            {
                "batch": batch_name,
                "track": track,
                "context": context,
                "efficiency_rank": efficiency_rank,
                "impact_rank": "",
                "rank_delta": "",
                "display_name": ranking.get("display_name", ""),
                "provisional_slug": slug,
                "canonical_troop_id": ranking.get("canonical_troop_id", ""),
                "identity_status": ranking.get("identity_status", ""),
                "independent_battles": independent_battles,
                "deployed": deployed,
                "kills": kills,
                "kills_per_deployed": f"{kills_per_deployed:.6f}",
                "verified_player_side_total_kills": verified_total if verified_total is not None else "",
                "player_side_kill_share": f"{kill_share:.6f}" if kill_share is not None else "",
                "share_adjusted_impact": f"{impact:.6f}" if impact is not None else "",
                "kill_share_coverage_battles": len(covered),
                "kill_share_coverage_complete": coverage_complete,
                "kill_share_status": status,
                "kill_share_denominator_provenance": (
                    "|".join(sorted({str(value["provenance"]) for value in covered.values()}))
                    if coverage_complete
                    else ""
                ),
                "reliability_status": ranking.get("reliability_status", ""),
            }
        )

    by_context: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in output:
        if row["share_adjusted_impact"] != "":
            by_context[str(row["context"])].append(row)
    for rows in by_context.values():
        rows.sort(
            key=lambda row: (
                -float(row["share_adjusted_impact"]),
                -int(row["deployed"]),
                str(row["provisional_slug"]),
            )
        )
        for impact_rank, row in enumerate(rows, start=1):
            row["impact_rank"] = impact_rank
            row["rank_delta"] = impact_rank - int(row["efficiency_rank"])
    return output


def build_report(
    batch_rows: list[dict[str, Any]],
    screenshot_rows: list[dict[str, Any]],
    metric_rows: list[dict[str, Any]],
) -> str:
    verified_batches = sum(row["archive_status"] == "verified" for row in batch_rows)
    complete_metrics = [row for row in metric_rows if row["kill_share_status"] == "complete"]
    reliable_metrics = [
        row for row in complete_metrics if row["reliability_status"] == "reliable"
    ]
    historical_matches = sum(
        row["decision"] == "skip_already_normalized" for row in screenshot_rows
    )
    pending_visual = sum(
        row["visual_audit_status"] == "blocked_raw_screenshot_not_retained"
        for row in screenshot_rows
    )
    lines = [
        "# Historical combat evidence reanalysis — pipeline v0.4",
        "",
        "This reanalysis treats committed normalized bundles as immutable inputs. It does not "
        "infer player-side totals from partial troop rows and does not promote below-gate rates "
        "into the human-readable ranking.",
        "",
        "## Status",
        "",
        "**COMPLETE_WITH_EXTERNAL_BLOCKERS** — every reconstructible committed Phase 2 bundle "
        "was reprocessed locally in `offline-existing` mode. The remaining gaps require a valid "
        "historical archive or retained raw screenshot; they are not replaced with inferred data.",
        "",
        "## Coverage",
        "",
        f"- Historical batches inventoried: **{len(batch_rows)}**",
        f"- Historical screenshots inventoried: **{len(screenshot_rows)}**",
        f"- Normalized archives verified and parsed: **{verified_batches}**",
        f"- Troop/context rows audited: **{len(metric_rows)}**",
        f"- Troop/context rows with complete kill-share coverage: **{len(complete_metrics)}**",
        f"- Cross-batch screenshots already normalized: **{historical_matches}**",
        f"- Existing same-battle primary screens needing raw visual representative review: **{pending_visual}**",
        "",
        "## Reliable rows under the new impact rule",
        "",
    ]
    if reliable_metrics:
        lines.extend(
            [
                "| Batch | Context | Efficiency rank | Impact rank | Troop | Battles | Deployed | Kills/deployed | Player kill share | Share-adjusted impact |",
                "|---|---|---:|---:|---|---:|---:|---:|---:|---:|",
            ]
        )
        for row in sorted(
            reliable_metrics,
            key=lambda value: (
                str(value["batch"]),
                str(value["context"]),
                int(value["impact_rank"]),
            ),
        ):
            lines.append(
                f"| {row['batch']} | {row['context']} | {row['efficiency_rank']} | "
                f"{row['impact_rank']} | {row['display_name']} | {row['independent_battles']} | "
                f"{row['deployed']} | {float(row['kills_per_deployed']):.3f} | "
                f"{float(row['player_side_kill_share']):.1%} | "
                f"{float(row['share_adjusted_impact']):.3f} |"
            )
    else:
        lines.append("No row with complete kill-share coverage also reaches the 5-battle / 20-deployed display gate.")

    lines.extend(
        [
            "",
            "## Explicit blockers",
            "",
        ]
    )
    blockers = Counter(
        row["kill_share_status"]
        for row in metric_rows
        if row["kill_share_status"] != "complete"
    )
    for status, count in sorted(blockers.items()):
        lines.append(f"- `{status}`: {count} troop/context row(s).")
    lines.extend(
        [
            "",
            "Machine-readable diagnostics, including below-gate rates, are in "
            "`historical_kill_share_rankings.csv`. Screenshot decisions are in "
            "`historical_screenshot_deduplication_audit.csv`.",
            "",
            "## Reproduce",
            "",
            "```bash",
            "python scripts/analysis/audit_historical_combat_evidence_v04.py \\",
            "  --data-root data/combat_observations \\",
            "  --output-dir analysis/historical_reanalysis_v04",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("data/combat_observations"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("analysis/historical_reanalysis_v04"),
    )
    args = parser.parse_args()
    data_root = args.data_root.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    screenshot_rows = screenshot_audit_rows(data_root)
    batch_rows: list[dict[str, Any]] = []
    metric_rows: list[dict[str, Any]] = []
    for batch in sorted(path for path in data_root.iterdir() if path.is_dir()):
        summary_path = batch / "normalization_summary.json"
        ranking_path = batch / "analysis" / "ranking_complete.csv"
        if not summary_path.is_file() or not (batch / "bundle").is_dir():
            continue
        summary = read_json(summary_path)
        if not ranking_path.is_file():
            batch_rows.append(
                {
                    "batch": batch.name,
                    "batch_id": summary.get("batch_id", ""),
                    "track": summary.get("game_track", ""),
                    "schema_version": summary.get("schema_version", ""),
                    "screenshots": summary.get("screenshots", summary.get("images_total", "")),
                    "battles": summary.get("battles", summary.get("primary_victory_battles", "")),
                    "archive_status": "legacy_without_phase2_ranking",
                    "expected_archive_sha256": "",
                    "actual_archive_sha256": "",
                    "ranking_rows": 0,
                    "complete_kill_share_rows": 0,
                }
            )
            continue

        archive = load_normalized_archive(batch)
        rankings = read_csv(ranking_path)
        rows: list[dict[str, Any]] = []
        totals: dict[tuple[str, str], dict[str, Any]] = {}
        if archive["status"] == "verified":
            totals = verified_player_side_kill_totals(
                archive["battles"],
                archive["occurrences"],
            )
            rows = augment_rankings(
                batch.name,
                str(summary.get("game_track", "")),
                rankings,
                archive["consolidated"],
                totals,
                str(archive["status"]),
            )
        else:
            rows = augment_rankings(
                batch.name,
                str(summary.get("game_track", "")),
                rankings,
                [],
                {},
                str(archive["status"]),
            )
        metric_rows.extend(rows)
        batch_rows.append(
            {
                "batch": batch.name,
                "batch_id": summary.get("batch_id", ""),
                "track": summary.get("game_track", ""),
                "schema_version": summary.get("schema_version", ""),
                "screenshots": summary.get("screenshots", summary.get("selected_screenshots", "")),
                "battles": summary.get("battles", ""),
                "archive_status": archive["status"],
                "expected_archive_sha256": archive.get("expected_sha256", ""),
                "actual_archive_sha256": archive.get("actual_sha256", ""),
                "ranking_rows": len(rankings),
                "verified_player_side_battles": len(totals),
                "complete_kill_share_rows": sum(
                    row["kill_share_status"] == "complete" for row in rows
                ),
            }
        )

    write_csv(
        output_dir / "historical_batch_audit.csv",
        (
            "batch",
            "batch_id",
            "track",
            "schema_version",
            "screenshots",
            "battles",
            "archive_status",
            "expected_archive_sha256",
            "actual_archive_sha256",
            "ranking_rows",
            "verified_player_side_battles",
            "complete_kill_share_rows",
        ),
        batch_rows,
    )
    write_csv(
        output_dir / "historical_screenshot_deduplication_audit.csv",
        (
            "batch",
            "source_file",
            "screenshot_id",
            "image_file",
            "image_sha256",
            "captured_at",
            "battle_id",
            "screen_status",
            "included_in_primary",
            "decision",
            "representative_or_prior",
            "same_battle_group",
            "visual_audit_status",
            "reason",
        ),
        screenshot_rows,
    )
    write_csv(output_dir / "historical_kill_share_rankings.csv", METRIC_FIELDS, metric_rows)
    (output_dir / "REPORT.md").write_text(
        build_report(batch_rows, screenshot_rows, metric_rows),
        encoding="utf-8",
    )
    validation = {
        "analysis_version": "0.4.0",
        "status": "pass_with_explicit_historical_blockers",
        "batch_count": len(batch_rows),
        "screenshot_count": len(screenshot_rows),
        "metric_row_count": len(metric_rows),
        "complete_kill_share_rows": sum(
            row["kill_share_status"] == "complete" for row in metric_rows
        ),
        "reliable_complete_kill_share_rows": sum(
            row["kill_share_status"] == "complete"
            and row["reliability_status"] == "reliable"
            for row in metric_rows
        ),
        "archive_status_counts": dict(
            sorted(Counter(str(row["archive_status"]) for row in batch_rows).items())
        ),
        "screenshot_decision_counts": dict(
            sorted(Counter(str(row["decision"]) for row in screenshot_rows).items())
        ),
        "kill_share_status_counts": dict(
            sorted(Counter(str(row["kill_share_status"]) for row in metric_rows).items())
        ),
    }
    (output_dir / "validation_report.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    artifacts = [
        path
        for path in sorted(output_dir.iterdir())
        if path.is_file() and path.name != "artifact_hashes.csv"
    ]
    write_csv(
        output_dir / "artifact_hashes.csv",
        ("artifact", "sha256", "size_bytes"),
        (
            {
                "artifact": path.name,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
            for path in artifacts
        ),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
