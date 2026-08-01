"""Empirical display-gate status reporter.

Scans ``data/combat_observations/**`` and reports, per track, whether the
repository's minimum empirical display gate has been reached:

    at least 5 independent battles AND at least 20 deployed troops
    for a given (track, battle context, player/enemy relationship, troop)
    combination

(see ``README.md`` "Core methodological rules" and ``AGENTS.md``
"Mandatory analytical boundaries").

This module is read-only: it never edits a batch's committed evidence or
analysis outputs. It only aggregates numbers that Phase 2 analysis agents
already computed and committed under each batch's ``analysis/`` directory,
combined the way the repository's own tooling is meant to combine them
(``docs/combat_observations/CLI.md`` describes a ``canonical_historical_aggregates.jsonl``
concept spanning batches of the same track).

Design notes / honesty caveats baked into the output:

* A troop's aggregation key is its confirmed ``canonical_troop_id`` when a
  batch resolved one, otherwise its ``provisional_slug`` (the batch's
  normalized on-screen display name). AGENTS.md says provisional labels are
  not canonical XML IDs, so this script never *reports* an unresolved row as
  though it had an audited ID -- every troop row carries an explicit
  ``identity_confirmed`` flag -- but it still counts the row's battles and
  deployed troops toward that troop's own display gate, exactly as the
  already-committed batch analyses (``ranking_reliable.csv``) do today.
  Cross-batch joins only ever happen through a matching canonical ID or an
  identically spelled provisional slug within the *same track*; they never
  merge across tracks.
* Battle counts and deployed counts are summed **across batches** for the
  same track, because each captured batch is a disjoint capture session
  (distinct battle IDs, distinct screenshot hashes) -- summing disjoint,
  already-deduplicated per-batch counts does not violate the "battle is the
  independent sampling unit" rule. Two different batches happening to reuse
  the same *local* battle label (``B01``) are still distinct battles because
  they come from different batch directories; this script never merges rows
  by bare battle id across batches.
* Battle contexts (``field``, ``siege_attack``, ``siege_defense``) are always
  kept separate, per AGENTS.md.
* Player-side and enemy-side observations must not be pooled. The current
  committed batches only carry player-side ("player_party") ordinary-troop
  rows -- none of them yet include a ``relationship_to_player`` or ``side``
  column. This script looks for such a column and, when absent, labels the
  rows ``player_party`` with an explicit ``assumed`` flag so nobody mistakes
  the assumption for observed enemy-side evidence.
* This tool does not read raw screenshots or reconstruct bundles; it only
  reads each batch's ``normalization_summary.json`` and
  ``analysis/ranking_complete.csv``. A batch missing either file (for
  example the corrupt 2026-07-23 pre-track-split batch, or a capture-plan
  scaffold with no evidence yet) is skipped and, if it is a plan scaffold,
  surfaced separately as "planned, not captured".

Stdlib only: no third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable

from .domain import DomainError, read_csv

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_ROOT = REPO_ROOT / "data" / "combat_observations"

# Minimum display gate (README.md "Core methodological rules"; AGENTS.md
# "Mandatory analytical boundaries"). Do not change without updating both
# documents and every dependent report.
MIN_INDEPENDENT_BATTLES = 5
MIN_DEPLOYED = 20

KNOWN_TRACKS = ("vanilla", "nightmare_sails", "realm_of_thrones", "taom")
KNOWN_CONTEXTS = ("field", "siege_attack", "siege_defense")

# Rows in the currently committed batches carry no relationship_to_player /
# side column; all of them are documented (batch READMEs) as player-side
# ordinary-troop occurrences. This is the explicit, honest default used only
# when neither column is present.
DEFAULT_RELATIONSHIP = "player_party"

_TRACK_LINE_RE = re.compile(r"^-?\s*Track:\s*`([a-z_]+)`", re.MULTILINE)
_NO_DATA_MARKER = "NO DATA CAPTURED YET"


class GateStatusError(Exception):
    """Raised when repository evidence cannot be interpreted safely."""


def _relationship_of(row: dict[str, str]) -> tuple[str, bool]:
    """Return (relationship_to_player, assumed) for a ranking row."""

    for key in ("relationship_to_player", "side"):
        value = (row.get(key) or "").strip()
        if value:
            return value, False
    return DEFAULT_RELATIONSHIP, True


def _int_field(row: dict[str, str], field: str, *, source: Path) -> int:
    raw = (row.get(field) or "").strip()
    if raw == "":
        raise GateStatusError(f"{source}: row for {row.get('display_name')!r} has an empty {field}")
    try:
        return int(round(float(raw)))
    except ValueError as error:
        raise GateStatusError(f"{source}: row for {row.get('display_name')!r} has a non-numeric {field}: {raw!r}") from error


def discover_batches(data_root: Path) -> list[Path]:
    """Return batch directories that have both a normalization summary and
    a committed Phase-2 ranking output, sorted for determinism."""

    if not data_root.exists():
        return []
    batches = []
    for summary_path in sorted(data_root.glob("*/normalization_summary.json")):
        batch_dir = summary_path.parent
        if (batch_dir / "analysis" / "ranking_complete.csv").exists():
            batches.append(batch_dir)
    return batches


def discover_planned_scaffolds(data_root: Path, captured_batch_dirs: Iterable[Path]) -> list[dict[str, str]]:
    """Return capture-plan scaffolds (README says NO DATA CAPTURED YET) that
    are not already counted as captured batches."""

    captured = set(captured_batch_dirs)
    planned: list[dict[str, str]] = []
    if not data_root.exists():
        return planned
    for readme_path in sorted(data_root.glob("*/README.md")):
        batch_dir = readme_path.parent
        if batch_dir in captured:
            continue
        text = readme_path.read_text(encoding="utf-8", errors="replace")
        if _NO_DATA_MARKER not in text:
            continue
        match = _TRACK_LINE_RE.search(text)
        planned.append(
            {
                "batch_dir": str(batch_dir.relative_to(REPO_ROOT)) if _is_within(batch_dir, REPO_ROOT) else str(batch_dir),
                "track": match.group(1) if match else "unknown",
            }
        )
    return planned


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def load_batch(batch_dir: Path) -> dict[str, object]:
    """Load one batch's track, per-context battle totals, and confirmed
    per-troop ranking rows."""

    summary_path = batch_dir / "normalization_summary.json"
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise GateStatusError(f"{summary_path}: unreadable normalization summary: {error}") from error

    track = summary.get("game_track")
    if not track:
        raise GateStatusError(f"{summary_path}: missing game_track; cannot attribute this batch to a track")

    context_battle_counts = summary.get("battle_context_counts") or {}
    if not isinstance(context_battle_counts, dict):
        raise GateStatusError(f"{summary_path}: battle_context_counts must be an object")

    ranking_path = batch_dir / "analysis" / "ranking_complete.csv"
    try:
        rows = read_csv(ranking_path)
    except DomainError as error:
        raise GateStatusError(str(error)) from error

    return {
        "batch_dir": batch_dir,
        "track": str(track),
        "context_battle_counts": {str(k): int(v) for k, v in context_battle_counts.items()},
        "rows": rows,
        "ranking_path": ranking_path,
    }


def aggregate(batches: list[dict[str, object]]) -> dict[str, dict]:
    """Aggregate loaded batches into a nested track -> context ->
    relationship -> troop structure, respecting AGENTS.md separations."""

    tracks: dict[str, dict] = {}

    for batch in batches:
        track = batch["track"]
        track_bucket = tracks.setdefault(
            track,
            {"batches": [], "context_battle_counts": {}, "contexts": {}},
        )
        batch_dir = batch["batch_dir"]
        track_bucket["batches"].append(
            str(batch_dir.relative_to(REPO_ROOT)) if _is_within(batch_dir, REPO_ROOT) else str(batch_dir)
        )

        for context, count in batch["context_battle_counts"].items():
            track_bucket["context_battle_counts"][context] = (
                track_bucket["context_battle_counts"].get(context, 0) + count
            )

        for row in batch["rows"]:
            context = (row.get("context") or "").strip()
            if not context:
                raise GateStatusError(f"{batch['ranking_path']}: row missing context")

            relationship, assumed = _relationship_of(row)
            context_bucket = track_bucket["contexts"].setdefault(
                context, {"relationships": {}}
            )
            relationship_bucket = context_bucket["relationships"].setdefault(
                relationship,
                {"assumed": assumed, "troops": {}},
            )
            relationship_bucket["assumed"] = relationship_bucket["assumed"] and assumed

            canonical_id = (row.get("canonical_troop_id") or "").strip()
            identity_status = (row.get("identity_status") or "").strip()
            deployed = _int_field(row, "deployed", source=batch["ranking_path"])
            battles = _int_field(row, "independent_battles", source=batch["ranking_path"])

            # Aggregation key: prefer the confirmed canonical XML ID so two
            # different display-name spellings of the same troop are joined
            # correctly; otherwise fall back to the batch's normalized
            # provisional slug (still the exact on-screen display name, just
            # not yet cross-referenced against the versioned track audit).
            # AGENTS.md: "Provisional labels are not canonical XML IDs" --
            # this script never *treats* a provisional slug as a confirmed
            # canonical ID, it only uses it as a same-track join key, and
            # every troop row still reports whether its identity is
            # confirmed so nobody mistakes it for an audited XML ID.
            provisional_slug = (row.get("provisional_slug") or "").strip()
            key = canonical_id or provisional_slug or (row.get("display_name") or "").strip()
            if not key:
                raise GateStatusError(
                    f"{batch['ranking_path']}: row has neither canonical_troop_id, provisional_slug, nor display_name"
                )

            troop_bucket = relationship_bucket["troops"].setdefault(
                key,
                {
                    "display_name": row.get("display_name") or key,
                    "canonical_troop_id": "",
                    "identity_confirmed": False,
                    "battles": 0,
                    "deployed": 0,
                },
            )
            if canonical_id and identity_status == "confirmed_id":
                troop_bucket["canonical_troop_id"] = canonical_id
                troop_bucket["identity_confirmed"] = True
            troop_bucket["battles"] += battles
            troop_bucket["deployed"] += deployed

    return tracks


def build_track_report(track: str, track_data: dict | None, planned: list[dict[str, str]]) -> dict:
    track_data = track_data or {"batches": [], "context_battle_counts": {}, "contexts": {}}
    context_reports = {}
    any_context_gate_met = False

    for context in KNOWN_CONTEXTS:
        context_data = track_data["contexts"].get(context, {"relationships": {}})
        battles_captured = track_data["context_battle_counts"].get(context, 0)
        relationship_reports = {}
        context_gate_met = False

        for relationship, bucket in sorted(context_data["relationships"].items()):
            troops = []
            reliable_count = 0
            confirmed_identity_count = 0
            for key, troop in sorted(bucket["troops"].items()):
                gate_met = (
                    troop["battles"] >= MIN_INDEPENDENT_BATTLES
                    and troop["deployed"] >= MIN_DEPLOYED
                )
                if gate_met:
                    reliable_count += 1
                    context_gate_met = True
                if troop["identity_confirmed"]:
                    confirmed_identity_count += 1
                troops.append(
                    {
                        "key": key,
                        "canonical_troop_id": troop["canonical_troop_id"],
                        "identity_confirmed": troop["identity_confirmed"],
                        "display_name": troop["display_name"],
                        "independent_battles": troop["battles"],
                        "deployed": troop["deployed"],
                        "gate_met": gate_met,
                        "battles_needed": max(0, MIN_INDEPENDENT_BATTLES - troop["battles"]),
                        "deployed_needed": max(0, MIN_DEPLOYED - troop["deployed"]),
                    }
                )
            troops.sort(key=lambda item: (-item["independent_battles"], -item["deployed"]))
            relationship_reports[relationship] = {
                "assumed": bucket["assumed"],
                "troops_observed": len(bucket["troops"]),
                "confirmed_identity_troops": confirmed_identity_count,
                "reliable_troop_count": reliable_count,
                "troops": troops,
            }

        if context_gate_met:
            any_context_gate_met = True

        context_reports[context] = {
            "independent_battles_captured": battles_captured,
            "gate_met": context_gate_met,
            "relationships": relationship_reports,
        }

    return {
        "track": track,
        "gate_met": any_context_gate_met,
        "batches": sorted(track_data["batches"]),
        "planned_batches": [p for p in planned if p["track"] == track],
        "contexts": context_reports,
    }


def build_report(data_root: Path, tracks: Iterable[str]) -> dict:
    batch_dirs = discover_batches(data_root)
    loaded = [load_batch(batch_dir) for batch_dir in batch_dirs]
    aggregated = aggregate(loaded)
    planned = discover_planned_scaffolds(data_root, batch_dirs)

    tracks = list(tracks)
    track_reports = {track: build_track_report(track, aggregated.get(track), planned) for track in tracks}
    overall_gate_met = all(report["gate_met"] for report in track_reports.values())

    return {
        "data_root": str(data_root),
        "min_independent_battles": MIN_INDEPENDENT_BATTLES,
        "min_deployed": MIN_DEPLOYED,
        "tracks": track_reports,
        "overall_gate_met": overall_gate_met,
    }


def _format_needed(context_report: dict) -> list[str]:
    needed = []
    battles_captured = context_report["independent_battles_captured"]
    if battles_captured == 0 and not context_report["relationships"]:
        return ["no battles captured yet in this context"]
    for relationship, bucket in context_report["relationships"].items():
        if bucket["reliable_troop_count"] > 0:
            continue
        closest = [t for t in bucket["troops"] if not t["gate_met"]]
        for troop in closest[:3]:
            parts = []
            if troop["battles_needed"] > 0:
                parts.append(f"{troop['battles_needed']} more independent battle(s)")
            if troop["deployed_needed"] > 0:
                parts.append(f"{troop['deployed_needed']} more deployed")
            if parts:
                needed.append(
                    f"[{relationship}] {troop['display_name']} ({troop['key']}) needs "
                    + " and ".join(parts)
                )
        if not bucket["troops"]:
            needed.append(f"[{relationship}] no troop observed yet")
    return needed


def render_text(report: dict) -> str:
    lines = []
    lines.append(
        f"Empirical display gate: >= {report['min_independent_battles']} independent battles "
        f"AND >= {report['min_deployed']} deployed troops (per track/context/relationship/troop)."
    )
    lines.append("")
    for track, track_report in report["tracks"].items():
        status = "GATE MET" if track_report["gate_met"] else "below gate"
        lines.append(f"== {track} :: {status} ==")
        if track_report["batches"]:
            lines.append(f"  captured batches: {', '.join(track_report['batches'])}")
        else:
            lines.append("  captured batches: none")
        if track_report["planned_batches"]:
            planned_dirs = ", ".join(p["batch_dir"] for p in track_report["planned_batches"])
            lines.append(f"  planned (no data yet): {planned_dirs}")

        for context, context_report in track_report["contexts"].items():
            lines.append(
                f"  [{context}] independent battles captured: {context_report['independent_battles_captured']}"
                f" -- {'gate met' if context_report['gate_met'] else 'below gate'}"
            )
            for relationship, bucket in context_report["relationships"].items():
                assumed_note = " (relationship assumed: no column in source data)" if bucket["assumed"] else ""
                lines.append(
                    f"    relationship={relationship}{assumed_note}: "
                    f"{bucket['troops_observed']} troop label(s) observed "
                    f"({bucket['confirmed_identity_troops']} with a confirmed canonical XML ID), "
                    f"{bucket['reliable_troop_count']} reaching the gate"
                )
                for troop in bucket["troops"]:
                    marker = "PASS" if troop["gate_met"] else "short"
                    identity = troop["canonical_troop_id"] if troop["identity_confirmed"] else f"{troop['key']} [unresolved id]"
                    lines.append(
                        f"      - {marker}: {troop['display_name']} ({identity}): "
                        f"{troop['independent_battles']} battles, {troop['deployed']} deployed"
                    )
            for note in _format_needed(context_report):
                lines.append(f"    needed: {note}")
        lines.append("")
    lines.append(
        "Overall: " + ("ALL requested tracks meet the gate." if report["overall_gate_met"] else "at least one requested track is below the gate.")
    )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gate_status",
        description="Report the empirical display-gate status of each Bannerlord track from committed combat-observation evidence.",
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=DEFAULT_DATA_ROOT,
        help="Root directory to scan (default: data/combat_observations).",
    )
    parser.add_argument(
        "--track",
        action="append",
        choices=KNOWN_TRACKS,
        help="Restrict the report/exit-code to this track. May be repeated. Default: all known tracks.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format (default: text).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    tracks = args.track or list(KNOWN_TRACKS)

    try:
        report = build_report(args.data_root, tracks)
    except GateStatusError as error:
        print(f"gate_status: {error}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=False))
    else:
        print(render_text(report))

    return 0 if report["overall_gate_met"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
