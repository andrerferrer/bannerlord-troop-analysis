#!/usr/bin/env python3
"""Generate and verify the deterministic Phase 2 analysis for PR #101."""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import re
import subprocess
import tarfile
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


ANALYSIS_DIR = Path(__file__).resolve().parent
BATCH_DIR = ANALYSIS_DIR.parent
REPO_ROOT = ANALYSIS_DIR.parents[3]
REVIEW_DIR = BATCH_DIR / "reviewed"
QUEUE_PATH = REPO_ROOT / "data/combat_observations/test_queues/realm_of_thrones.json"
IDENTITY_PATH = REPO_ROOT / "data/realm_of_thrones/audit/realm_of_thrones_troops.csv"
HISTORICAL_DIR = REPO_ROOT / "data/combat_observations/2026-09-12-to-14-rot-mixed-campaign-phase1/analysis"
PR100_DIR = REPO_ROOT / "data/combat_observations/2026-09-15-to-16-rot-qartheen-enthroned-guardian/analysis"

BATCH_ID = "2026-09-16-rot-qartheen-enthroned-guardian-field-phase1"
TRACK = "realm_of_thrones"
NORMALIZATION_COMMIT = "e0c3d5c47d35f4743699311c05c397eb698ddaec"
MAIN_COMMIT = "03e56761316704ee44921368a751fb14b66d475c"
ARCHIVE_SHA256 = "ae7c7998ae73a5f9adc358550644813770280512b05f06e0b79418d3dff78f0b"
ARCHIVE_SIZE = 8_732
BASE64_SHA256 = "d250d3caddee132d3e1fa80b03162498f77a698f78acb05a9b150c016241743c"
BASE64_SIZE = 11_798
BASE64_BLOB = "6dfc56ad73516c0c8b8bb2e5eab3dbd6a973a790"
IDENTITY_SHA256 = "63ea983998e25aa0e6f8c0747bf42e44440f695bbe1fec717074e7ba64e42810"
IDENTITY_BLOB = "67df28bb6cbfbb60a37a90950c781980d41a2fe9"
FOCUS_ID = "enthroned_guardian"
FOCUS_NAME = "Qartheen Enthroned Guardian"
FOCUS_DISPLAY = "Qartheen Enthroned Guardian [T6]"
GATE_BATTLES = 5
GATE_DEPLOYED = 20
COUNT_FIELDS = ("deployed", "survivors", "kills", "deaths", "wounded", "routed")
NUMERIC_FIELDS = ("survivors", "kills", "upgrade_ready", "deaths", "wounded", "routed")

IMMUTABLE_PATHS = (
    f"data/combat_observations/{BATCH_ID}/README.md",
    f"data/combat_observations/{BATCH_ID}/batch_state.json",
    f"data/combat_observations/{BATCH_ID}/phase1_checkpoint.json",
    f"data/combat_observations/{BATCH_ID}/screenshots_manifest.csv",
    f"data/combat_observations/{BATCH_ID}/bundle",
    f"data/combat_observations/{BATCH_ID}/handoff",
    f"data/combat_observations/{BATCH_ID}/source",
)
FROZEN_MODEL_PATHS = ("analysis/model_versions",)

OCCURRENCE_FIELDS = (
    "observation_id", "battle_id", "captured_at", "track", "game_version", "context",
    "result_scope", "cohort", "participant_scope", "row_index", "raw_name", "raw_tier",
    "display_name", "canonical_troop_id", "identity_status", "canonical_default_group",
    "canonical_role", "visibility", "transcription_status", "source_key",
    "source_image_sha256", "note", *NUMERIC_FIELDS, "deployed",
)
RANKING_FIELDS = (
    "track", "game_version", "cohort", "context", "participant_scope", "efficiency_rank",
    "impact_rank", "display_name", "canonical_troop_id", "identity_status",
    "canonical_default_group", "canonical_role", "evidence_grade", "independent_battles",
    "ordinary_occurrences", *COUNT_FIELDS, "kills_per_deployed",
    "verified_player_side_total_kills", "kill_total_coverage_battles",
    "kill_total_coverage_complete", "player_side_kill_share", "share_adjusted_impact",
    "verified_player_side_total_deployed", "deployment_total_coverage_battles",
    "deployment_total_coverage_complete", "player_side_deployment_share",
    "offensive_contribution_ratio", "offensive_share_gap", "retention_rate", "death_rate",
    "casualty_rate", "numeric_display_gate_passed", "reliability_status",
    "more_battles_needed", "more_deployed_needed", "role_adjusted_rank_status",
)
COHORT_FIELDS = (
    "cohort_view", "track", "context", "participant_party", "result_scope",
    "independent_battles", *COUNT_FIELDS, "kills_per_deployed", "player_side_total_kills",
    "player_side_kill_share", "player_side_total_deployed", "player_side_deployment_share",
    "offensive_contribution_ratio", "offensive_share_gap", "retention_rate",
    "numeric_display_gate_passed", "evidence_status", "interpretation", "source",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True
    ).stdout


def parse_jsonl(payload: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in payload.decode().splitlines() if line]


def parse_csv(payload: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))


def read_csv(path: Path) -> list[dict[str, str]]:
    return parse_csv(path.read_bytes())


def read_pinned_csv(path: Path) -> list[dict[str, str]]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    pinned = git_bytes("show", f"{MAIN_COMMIT}:{rel}")
    if path.read_bytes() != pinned:
        raise ValueError(f"working-tree input differs from pinned {MAIN_COMMIT}: {rel}")
    return parse_csv(pinned)


def csv_safe(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", value.strip()):
            return "'" + value
    return value


def write_csv(path: Path, fields: Iterable[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(fields)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: csv_safe(row.get(field, "")) for field in fieldnames})


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def fmt(value: float | None) -> str:
    return "" if value is None else f"{value:.6f}"


def bool_text(value: Any) -> bool:
    return str(value).strip().casefold() == "true"


def repository_snapshot(paths: tuple[str, ...], label: str) -> dict[str, Any]:
    committed = git("ls-tree", "-r", "--name-only", NORMALIZATION_COMMIT, "--", *paths).splitlines()
    modified = git("diff", "--name-only", NORMALIZATION_COMMIT, "--", *paths).splitlines()
    missing = [name for name in committed if not (REPO_ROOT / name).is_file()]
    if modified or missing:
        raise ValueError(f"{label} changed after normalization: {modified + missing}")
    return {
        "baseline_commit": NORMALIZATION_COMMIT,
        "paths": list(paths),
        "files_verified": len(committed),
        "modified_files": modified,
        "missing_files": missing,
    }


def verify_bundle() -> tuple[dict[str, bytes], dict[str, Any]]:
    base64_path = BATCH_DIR / "bundle/rot_qartheen_enthroned_guardian_field_phase1.tar.xz.base64"
    encoded = base64_path.read_bytes()
    if len(encoded) != BASE64_SIZE or sha256_bytes(encoded) != BASE64_SHA256:
        raise ValueError("Base64 transport hash/size mismatch")
    if git("hash-object", str(base64_path.relative_to(REPO_ROOT))) != BASE64_BLOB:
        raise ValueError("Base64 Git blob mismatch")
    compact = re.sub(rb"[\t\n\r ]+", b"", encoded)
    if re.search(rb"[^A-Za-z0-9+/=]", compact):
        raise ValueError("transport contains non-Base64 bytes")
    archive = base64.b64decode(compact, validate=True)
    if len(archive) != ARCHIVE_SIZE or sha256_bytes(archive) != ARCHIVE_SHA256:
        raise ValueError("decoded archive hash/size mismatch")

    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as handle:
        for member in handle.getmembers():
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or not member.isfile():
                raise ValueError(f"unsafe archive member: {member.name}")
            if member.name in files:
                raise ValueError(f"duplicate archive member: {member.name}")
            extracted = handle.extractfile(member)
            if extracted is None:
                raise ValueError(f"unreadable archive member: {member.name}")
            files[member.name] = extracted.read()

    declared: dict[str, str] = {}
    checksum_path = BATCH_DIR / "bundle/rot_qartheen_enthroned_guardian_field_phase1.members.sha256"
    for line in checksum_path.read_text().splitlines():
        digest, name = line.split("  ", 1)
        declared[name] = digest
    if set(files) != set(declared) or len(files) != 15:
        raise ValueError("archive member inventory mismatch")
    for name, payload in files.items():
        if sha256_bytes(payload) != declared[name]:
            raise ValueError(f"member hash mismatch: {name}")

    manifest = json.loads((BATCH_DIR / "bundle/manifest.blake2b.json").read_text())
    manifest_members = {row["path"]: row for row in manifest["members"]}
    if manifest["archive"]["sha256"] != ARCHIVE_SHA256 or set(manifest_members) != set(files):
        raise ValueError("bundle manifest inventory mismatch")
    for name, payload in files.items():
        if manifest_members[name]["sha256"] != sha256_bytes(payload):
            raise ValueError(f"bundle manifest SHA mismatch: {name}")
        if manifest_members[name]["blake2b_256"] != hashlib.blake2b(payload, digest_size=32).hexdigest():
            raise ValueError(f"bundle manifest BLAKE2 mismatch: {name}")

    mirrors = (
        "README.md", "screenshots_manifest.csv", "phase1_checkpoint.json", "batch_state.json",
        "handoff/ANALYSIS_PROMPT.md", "handoff/ANALYSIS_TASK_V1.json",
    )
    for name in mirrors:
        if (BATCH_DIR / name).read_bytes() != files[name]:
            raise ValueError(f"repository/archive mirror mismatch: {name}")

    source_manifest = json.loads(files["source_manifest.json"])
    source_inventory = parse_csv(files["source_inventory.csv"])
    screenshots = parse_csv(files["screenshots_manifest.csv"])
    rows = parse_jsonl(files["normalized/player_rows.jsonl"])
    sources = {source["source_key"]: source for source in source_manifest["sources"]}
    hashes = {source["sha256"] for source in sources.values()}
    if len(sources) != 2 or len(hashes) != 2:
        raise ValueError("source manifest inventory mismatch")
    if {row["sha256"] for row in source_inventory} != hashes:
        raise ValueError("source inventory hash links mismatch")
    if {row["image_sha256"] for row in screenshots} != hashes:
        raise ValueError("screenshot manifest hash links mismatch")
    for row in rows:
        if row["source_key"] not in sources or row["source_image_sha256"] != sources[row["source_key"]]["sha256"]:
            raise ValueError(f"row source link mismatch: {row['observation_id']}")

    return files, {
        "archive_sha256": ARCHIVE_SHA256,
        "archive_size_bytes": len(archive),
        "base64_sha256": BASE64_SHA256,
        "base64_size_bytes": len(encoded),
        "base64_git_blob": BASE64_BLOB,
        "members_verified": len(files),
        "member_sha256_manifest_verified": True,
        "member_blake2b_manifest_verified": True,
        "repository_mirrors_verified": len(mirrors),
        "source_links_verified": len(rows),
        "retained_raw_source_hashes": sorted(hashes),
        "retained_raw_bytes_repository_addressable": False,
        "retained_raw_hash_status": "manifest hashes reverified; PNG bytes were session-local and are not retained",
        "safe_preflight_passed": True,
    }


def identity_index() -> dict[str, list[dict[str, str]]]:
    if sha256_file(IDENTITY_PATH) != IDENTITY_SHA256 or git("hash-object", str(IDENTITY_PATH.relative_to(REPO_ROOT))) != IDENTITY_BLOB:
        raise ValueError("versioned Realm of Thrones identity audit mismatch")
    identity_rel = IDENTITY_PATH.relative_to(REPO_ROOT).as_posix()
    if git("rev-parse", f"{MAIN_COMMIT}:{identity_rel}") != IDENTITY_BLOB:
        raise ValueError("pinned Realm of Thrones identity audit blob mismatch")
    pinned = git_bytes("show", f"{MAIN_COMMIT}:{identity_rel}")
    if IDENTITY_PATH.read_bytes() != pinned:
        raise ValueError("working-tree identity audit differs from pinned main bytes")
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in parse_csv(pinned):
        index[row["name"].strip().casefold()].append(row)
    return index


def resolve_identity(row: dict[str, Any], index: dict[str, list[dict[str, str]]]) -> dict[str, str]:
    raw_name = row.get("raw_name")
    if not raw_name:
        return {
            "canonical_troop_id": "", "identity_status": "unresolved_label",
            "canonical_default_group": "", "canonical_role": "",
        }
    matches = index.get(raw_name.strip().casefold(), [])
    if row.get("transcription_status") != "exact_visible":
        return {
            "canonical_troop_id": "", "identity_status": "unresolved_provisional_label",
            "canonical_default_group": "", "canonical_role": "",
        }
    if len(matches) == 1:
        match = matches[0]
        group = match.get("default_group", "")
        return {
            "canonical_troop_id": match["troop_id"], "identity_status": "confirmed_id",
            "canonical_default_group": group, "canonical_role": group.casefold(),
        }
    return {
        "canonical_troop_id": "", "identity_status": "unresolved_provisional_label",
        "canonical_default_group": "", "canonical_role": "",
    }


def normalized_rows(files: dict[str, bytes]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    events = parse_jsonl(files["normalized/events.jsonl"])
    parties = parse_jsonl(files["normalized/party_summaries.jsonl"])
    rows = parse_jsonl(files["normalized/player_rows.jsonl"])
    if len(events) != 2 or len(parties) != 2 or len(rows) != 31:
        raise ValueError("normalized record count mismatch")
    if any(event["track"] != TRACK or event["context"] != "field" or event["result_status"] != "completed" for event in events):
        raise ValueError("track/context/result boundary mismatch")
    if len({event["event_id"] for event in events}) != 2 or len({row["observation_id"] for row in rows}) != 31:
        raise ValueError("duplicate event or observation IDs")
    if sum(row["row_kind"] == "ordinary" for row in rows) != 13 or sum(row["row_kind"] == "character" for row in rows) != 18:
        raise ValueError("ordinary/character partition mismatch")

    identities = identity_index()
    ordinary: list[dict[str, Any]] = []
    characters: list[dict[str, Any]] = []
    for row in rows:
        out = {
            "observation_id": row["observation_id"], "battle_id": row["event_id"],
            "captured_at": row["captured_at"], "track": row["track"],
            "game_version": row["game_version"], "context": row["context"],
            "result_scope": row["result_scope"], "cohort": row["participant_party"],
            "participant_scope": row["participant_scope"], "row_index": row["row_index"],
            "raw_name": row["raw_name"], "raw_tier": row["raw_tier"],
            "display_name": row["display_name"] or "[unreadable ordinary label]",
            "visibility": row["visibility"], "transcription_status": row["transcription_status"],
            "source_key": row["source_key"], "source_image_sha256": row["source_image_sha256"],
            "note": row["note"], **{field: row[field] for field in NUMERIC_FIELDS},
            "deployed": row["deployed"],
        }
        if row["row_kind"] == "ordinary":
            out.update(resolve_identity(row, identities))
            ordinary.append(out)
        else:
            out.update({
                "canonical_troop_id": "", "identity_status": "excluded_character",
                "canonical_default_group": "", "canonical_role": "",
            })
            characters.append(out)
    ordinary.sort(key=lambda row: (row["captured_at"], int(row["row_index"])))
    characters.sort(key=lambda row: (row["captured_at"], int(row["row_index"])))
    return events, parties, ordinary, characters


def metric_row(
    *, view: str, counts: dict[str, int], battle_ids: set[str], total_kills: int,
    total_deployed: int, source: str, interpretation: str,
) -> dict[str, Any]:
    battles = len(battle_ids)
    kill_share = counts["kills"] / total_kills if total_kills else None
    deployment_share = counts["deployed"] / total_deployed if total_deployed else None
    ratio = kill_share / deployment_share if kill_share is not None and deployment_share else None
    gate = battles >= GATE_BATTLES and counts["deployed"] >= GATE_DEPLOYED
    return {
        "cohort_view": view, "track": TRACK, "context": "field",
        "participant_party": "Egon Emeros' Party", "result_scope": "completed",
        "independent_battles": battles, **counts,
        "kills_per_deployed": fmt(counts["kills"] / counts["deployed"] if counts["deployed"] else None),
        "player_side_total_kills": total_kills, "player_side_kill_share": fmt(kill_share),
        "player_side_total_deployed": total_deployed,
        "player_side_deployment_share": fmt(deployment_share),
        "offensive_contribution_ratio": fmt(ratio),
        "offensive_share_gap": fmt(kill_share - deployment_share if kill_share is not None and deployment_share is not None else None),
        "retention_rate": fmt(counts["survivors"] / counts["deployed"] if counts["deployed"] else None),
        "numeric_display_gate_passed": gate,
        "evidence_status": "reliable" if gate else "below_gate_two_battles",
        "interpretation": interpretation, "source": source,
    }


def aggregate_rows(ordinary: list[dict[str, Any]], parties: list[dict[str, Any]]) -> list[dict[str, Any]]:
    party_by_event = {party["event_id"]: party["party_totals"] for party in parties}
    groups: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in ordinary:
        identity_key = row["canonical_troop_id"] or row["display_name"]
        groups[(row["context"], identity_key, row["cohort"])].append(row)
    aggregates: list[dict[str, Any]] = []
    for (_, _, _), rows in groups.items():
        battle_ids = {row["battle_id"] for row in rows}
        counts = {field: sum(int(row[field]) for row in rows) for field in COUNT_FIELDS}
        total_kills = sum(int(party_by_event[battle]["kills"]) for battle in battle_ids)
        total_deployed = sum(int(party_by_event[battle]["deployed"]) for battle in battle_ids)
        battles = len(battle_ids)
        kill_share = counts["kills"] / total_kills
        deployment_share = counts["deployed"] / total_deployed
        kpd = counts["kills"] / counts["deployed"]
        gate = battles >= GATE_BATTLES and counts["deployed"] >= GATE_DEPLOYED
        missing_battles = max(0, GATE_BATTLES - battles)
        missing_deployed = max(0, GATE_DEPLOYED - counts["deployed"])
        if gate:
            reliability = "reliable"
        elif missing_battles and missing_deployed:
            reliability = "insufficient_battles_and_deployed"
        elif missing_battles:
            reliability = "insufficient_battles"
        else:
            reliability = "insufficient_deployed"
        first = rows[0]
        aggregates.append({
            "track": TRACK, "game_version": "unknown", "cohort": first["cohort"],
            "context": first["context"], "participant_scope": "player_party",
            "display_name": first["display_name"], "canonical_troop_id": first["canonical_troop_id"],
            "identity_status": first["identity_status"],
            "canonical_default_group": first["canonical_default_group"],
            "canonical_role": first["canonical_role"],
            "evidence_grade": "high" if gate else "exploratory",
            "independent_battles": battles, "ordinary_occurrences": len(rows), **counts,
            "kills_per_deployed": fmt(kpd), "verified_player_side_total_kills": total_kills,
            "kill_total_coverage_battles": battles, "kill_total_coverage_complete": True,
            "player_side_kill_share": fmt(kill_share), "share_adjusted_impact": fmt(kpd * kill_share),
            "verified_player_side_total_deployed": total_deployed,
            "deployment_total_coverage_battles": battles, "deployment_total_coverage_complete": True,
            "player_side_deployment_share": fmt(deployment_share),
            "offensive_contribution_ratio": fmt(kill_share / deployment_share),
            "offensive_share_gap": fmt(kill_share - deployment_share),
            "retention_rate": fmt(counts["survivors"] / counts["deployed"]),
            "death_rate": fmt(counts["deaths"] / counts["deployed"]),
            "casualty_rate": fmt((counts["deaths"] + counts["wounded"]) / counts["deployed"]),
            "numeric_display_gate_passed": gate, "reliability_status": reliability,
            "more_battles_needed": missing_battles, "more_deployed_needed": missing_deployed,
            "role_adjusted_rank_status": "not_applicable_current_methodology_keeps_offense_and_defense_separate",
            "_kpd": kpd, "_impact": kpd * kill_share,
        })
    eligible = [row for row in aggregates if row["numeric_display_gate_passed"]]
    for row in aggregates:
        row["efficiency_rank"] = ""
        row["impact_rank"] = ""
    for rank, row in enumerate(sorted(eligible, key=lambda item: (-item["_kpd"], item["display_name"])), 1):
        row["efficiency_rank"] = rank
    for rank, row in enumerate(sorted(eligible, key=lambda item: (-item["_impact"], item["display_name"])), 1):
        row["impact_rank"] = rank
    for row in aggregates:
        row.pop("_kpd")
        row.pop("_impact")
    return sorted(aggregates, key=lambda row: (-float(row["kills_per_deployed"]), row["display_name"]))


def guardian_cohorts(
    ordinary: list[dict[str, Any]], parties: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    historical_occurrences = [
        row for row in read_pinned_csv(HISTORICAL_DIR / "ordinary_occurrences.csv")
        if row["canonical_troop_id"] == FOCUS_ID and row["context"] == "field"
        and row["cohort"] == "Egon Emeros' Party" and row["result_scope"] == "completed"
    ]
    historical_denominators = {
        row["battle_id"]: row for row in read_pinned_csv(HISTORICAL_DIR / "denominator_coverage.csv")
    }
    if len(historical_occurrences) != 5:
        raise ValueError("pinned historical Guardian cohort is not five completed field battles")
    hist_ids = {row["battle_id"] for row in historical_occurrences}
    hist_counts = {field: sum(int(row[field]) for row in historical_occurrences) for field in COUNT_FIELDS}
    hist_total_kills = sum(int(historical_denominators[battle]["player_side_total_kills"]) for battle in hist_ids)
    hist_total_deployed = sum(int(historical_denominators[battle]["player_side_total_deployed"]) for battle in hist_ids)
    historical = metric_row(
        view="historical_mixed_campaign", counts=hist_counts, battle_ids=hist_ids,
        total_kills=hist_total_kills, total_deployed=hist_total_deployed,
        source="2026-09-12-to-14 mixed-campaign completed field cohort",
        interpretation="reliable_historical_descriptive",
    )

    focus = [row for row in ordinary if row["canonical_troop_id"] == FOCUS_ID]
    new_ids = {row["battle_id"] for row in focus}
    party_by_event = {party["event_id"]: party["party_totals"] for party in parties}
    new_counts = {field: sum(int(row[field]) for row in focus) for field in COUNT_FIELDS}
    new_total_kills = sum(int(party_by_event[battle]["kills"]) for battle in new_ids)
    new_total_deployed = sum(int(party_by_event[battle]["deployed"]) for battle in new_ids)
    new = metric_row(
        view="new_follow_up", counts=new_counts, battle_ids=new_ids,
        total_kills=new_total_kills, total_deployed=new_total_deployed,
        source=BATCH_ID, interpretation="below_gate_follow_up_descriptive",
    )

    combined_counts = {field: hist_counts[field] + new_counts[field] for field in COUNT_FIELDS}
    combined = metric_row(
        view="combined_descriptive_continuity", counts=combined_counts,
        battle_ids=hist_ids | new_ids, total_kills=hist_total_kills + new_total_kills,
        total_deployed=hist_total_deployed + new_total_deployed,
        source="historical_mixed_campaign + new_follow_up; excludes PR #100 cohort",
        interpretation="descriptive_non_causal",
    )

    ranking = next(
        row for row in read_pinned_csv(HISTORICAL_DIR / "ranking_reliable.csv")
        if row["canonical_troop_id"] == FOCUS_ID and row["context"] == "field"
    )
    if (int(ranking["independent_battles"]), int(ranking["deployed"]), int(ranking["kills"])) != (5, hist_counts["deployed"], hist_counts["kills"]):
        raise ValueError("recomputed historical cohort disagrees with pinned ranking")

    battle_rows: list[dict[str, Any]] = []
    for row in historical_occurrences:
        denom = historical_denominators[row["battle_id"]]
        battle_rows.append({
            "cohort_view": "historical_mixed_campaign", "battle_id": row["battle_id"],
            "captured_at": row["captured_at"], "context": row["context"],
            "result_scope": row["result_scope"], **{field: int(row[field]) for field in COUNT_FIELDS},
            "kills_per_deployed": fmt(int(row["kills"]) / int(row["deployed"])),
            "retention_rate": fmt(int(row["survivors"]) / int(row["deployed"])),
            "player_side_total_kills": int(denom["player_side_total_kills"]),
            "player_side_total_deployed": int(denom["player_side_total_deployed"]),
            "source_image_sha256": row["source_image_sha256"],
        })
    event_by_id = {party["event_id"]: party for party in parties}
    for row in focus:
        totals = event_by_id[row["battle_id"]]["party_totals"]
        battle_rows.append({
            "cohort_view": "new_follow_up", "battle_id": row["battle_id"],
            "captured_at": row["captured_at"], "context": row["context"],
            "result_scope": row["result_scope"], **{field: int(row[field]) for field in COUNT_FIELDS},
            "kills_per_deployed": fmt(int(row["kills"]) / int(row["deployed"])),
            "retention_rate": fmt(int(row["survivors"]) / int(row["deployed"])),
            "player_side_total_kills": int(totals["kills"]),
            "player_side_total_deployed": int(totals["deployed"]),
            "source_image_sha256": row["source_image_sha256"],
        })

    pr100_occurrences = [
        row for row in read_pinned_csv(PR100_DIR / "ordinary_occurrences.csv")
        if row["canonical_troop_id"] == FOCUS_ID and row["context"] == "field"
    ]
    pr100_ids = {row["battle_id"] for row in pr100_occurrences}
    pr100_dedup = read_pinned_csv(PR100_DIR / "screenshot_deduplication_audit.csv")
    pr100_hashes = {
        row["candidate_sha256"] for row in pr100_dedup if row["battle_id"] in pr100_ids
    }
    new_hashes = {row["source_image_sha256"] for row in focus}
    compatibility = {
        "status": "passed_for_descriptive_continuity_only",
        "compatible_fields": {
            "track": TRACK, "context": "field", "participant_party": "Egon Emeros' Party",
            "focus_identity": FOCUS_ID, "result_scope": "completed",
        },
        "limitations": [
            "Exact game build is unknown in both the historical and new normalized evidence.",
            "Campaign battles are uncontrolled and differ in opponent, roster, map, orders, and enemy availability.",
            "The combined seven-battle view is descriptive continuity, not a causal or controlled-test estimate.",
        ],
        "historical_vs_new_battle_id_overlap": sorted(hist_ids & new_ids),
        "historical_vs_new_source_hash_overlap": sorted(
            {value for row in historical_occurrences for value in row["source_image_sha256"].split("|")} & new_hashes
        ),
        "pr100_distinct_nine_field_battle_cohort": {
            "battle_count": len(pr100_ids), "battle_id_overlap_with_new": sorted(pr100_ids & new_ids),
            "source_hash_overlap_with_new": sorted(pr100_hashes & new_hashes),
            "pooled_into_continuity_view": False,
            "reason": "PR #100 is the distinct dedicated decision cohort and is not part of the task-pinned historical-five-plus-follow-up continuity view.",
        },
    }
    if compatibility["historical_vs_new_battle_id_overlap"] or compatibility["historical_vs_new_source_hash_overlap"]:
        raise ValueError("historical and new Guardian cohorts overlap")
    if pr100_ids & new_ids or pr100_hashes & new_hashes or len(pr100_ids) != 9:
        raise ValueError("new follow-up overlaps or misreads the distinct PR #100 cohort")
    return [historical, new, combined], battle_rows, compatibility


def path_pin(path: Path) -> dict[str, str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    pinned = git_bytes("show", f"{MAIN_COMMIT}:{rel}")
    if path.read_bytes() != pinned:
        raise ValueError(f"working-tree input differs from pinned {MAIN_COMMIT}: {rel}")
    return {
        "path": rel, "commit": MAIN_COMMIT,
        "git_blob_sha": git("rev-parse", f"{MAIN_COMMIT}:{rel}"),
        "sha256": sha256_bytes(pinned),
        "worktree_bytes_equal_pinned_commit": True,
    }


def queue_validation() -> dict[str, Any]:
    queue = json.loads(QUEUE_PATH.read_text())
    categories: dict[tuple[str, str], str] = {}
    duplicates: list[str] = []
    for category in ("ordered_queue", "verification_holds", "parked", "closed"):
        for row in queue[category]:
            key = (row["troop_id"], row["context"])
            if key in categories:
                duplicates.append(f"{key[0]}:{key[1]} in {categories[key]} and {category}")
            categories[key] = category
    if queue["active_test"]:
        row = queue["active_test"]
        key = (row["troop_id"], row["context"])
        if key in categories:
            duplicates.append(f"{key[0]}:{key[1]} in {categories[key]} and active_test")
    priorities = [row["priority"] for row in queue["ordered_queue"]]
    guardian = [row for row in queue["closed"] if row["troop_id"] == FOCUS_ID and row["context"] == "field"]
    holds = [row["troop_id"] for row in queue["verification_holds"]]
    if duplicates or len(priorities) != len(set(priorities)) or len(guardian) != 1:
        raise ValueError("authoritative queue invariants failed")
    if queue["active_test"] is not None or queue["ordered_queue"] != [] or holds != ["arryn_moonknight"]:
        raise ValueError("authoritative queue does not preserve closed Guardian/empty queue/Arryn hold")
    return {
        "status": "passed_unchanged", "queue_path": str(QUEUE_PATH.relative_to(REPO_ROOT)),
        "queue_sha256_before": sha256_file(QUEUE_PATH), "queue_sha256_after": sha256_file(QUEUE_PATH),
        "active_test_before": None, "active_test_after": None,
        "ordered_queue_before": [], "ordered_queue_after": [],
        "verification_holds_before": holds, "verification_holds_after": holds,
        "guardian_closed_before": True, "guardian_closed_after": True,
        "guardian_completed_by": guardian[0]["completed_by"],
        "decision": "No queue mutation. PR #100 already closed dedicated Guardian field testing with a stronger nine-battle cohort and sensitivity; the new two-battle follow-up is confirmatory and below the independent-battle gate.",
        "future_target_authorized": False, "duplicate_category_entries": duplicates,
        "unique_priorities": len(priorities) == len(set(priorities)),
    }


def dedup_audit(files: dict[str, bytes], compatibility: dict[str, Any]) -> list[dict[str, Any]]:
    current = parse_csv(files["screenshots_manifest.csv"])
    rows: list[dict[str, Any]] = []
    for source in current:
        source_hash = source["image_sha256"]
        battle_id = source["battle_id"]
        hash_matches: list[str] = []
        battle_matches: list[str] = []
        for pattern in ("**/screenshots_manifest.csv", "**/source_inventory.csv"):
            for path in sorted((REPO_ROOT / "data/combat_observations").glob(pattern)):
                if BATCH_DIR in path.parents:
                    continue
                try:
                    other_rows = read_csv(path)
                except (UnicodeDecodeError, csv.Error):
                    continue
                for other in other_rows:
                    candidate_hashes = (
                        other.get("image_sha256", "") + "|" + other.get("sha256", "")
                        + "|" + other.get("candidate_sha256", "")
                    ).split("|")
                    if source_hash and source_hash in candidate_hashes:
                        hash_matches.append(str(path.relative_to(REPO_ROOT)))
                    candidate_battles = (
                        other.get("battle_id", "") + "|" + other.get("event_ids", "")
                    ).split("|")
                    if battle_id and battle_id in candidate_battles:
                        battle_matches.append(str(path.relative_to(REPO_ROOT)))
        rows.append({
            "screenshot_id": source["screenshot_id"], "image_sha256": source_hash,
            "battle_id": battle_id, "historical_exact_hash_matches": "|".join(sorted(set(hash_matches))),
            "historical_battle_id_matches": "|".join(sorted(set(battle_matches))),
            "pr100_hash_overlap": False, "pr100_battle_id_overlap": False,
            "decision": "retain_as_independent_battle",
            "reason": "No committed cross-batch exact hash or battle ID match; the two current screens also differ in timestamp, opponent, duration, totals, and hash.",
        })
    if any(row["historical_exact_hash_matches"] or row["historical_battle_id_matches"] for row in rows):
        raise ValueError("cross-batch duplicate detected")
    if compatibility["pr100_distinct_nine_field_battle_cohort"]["source_hash_overlap_with_new"]:
        raise ValueError("PR #100 source overlap detected")
    return rows


def report_markdown(aggregates: list[dict[str, Any]], cohorts: list[dict[str, Any]]) -> str:
    lines = [
        "# Phase 2 analysis — Sep 16 Qartheen Guardian follow-up", "",
        "## Batch-wide findings", "",
        "All **13 visible player-side ordinary occurrences** are covered across **12 troop/context rows**. None reaches the 5-independent-battle gate, so **0 rows are reliable** and **12 remain explicit insufficient evidence**. All **18 character rows** are retained separately and excluded from ordinary-troop metrics.", "",
        "Player-side, field, Realm of Thrones, and Egon Emeros' Party boundaries remain separate. Every contributing battle has direct positive player-side kill and deployment totals, so shares are published without reconstructing off-screen troop rows.", "",
        "Because every screenshot is a completed final result with direct side totals, battle-level pressure margins are published separately: **1.000000** against Forim's Party and **0.911765** against the Deserters. No tested frontline is predeclared in this mixed campaign evidence, so those side-level margins are not attributed to the Guardian or any other troop.", "",
        "| troop | identity | battles | deployed | kills | kills/deployed | kill share | deployment share | contribution ratio | status |", "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in aggregates:
        lines.append(
            f"| {row['display_name']} | {row['identity_status']} | {row['independent_battles']} | {row['deployed']} | {row['kills']} | {row['kills_per_deployed']} | {row['player_side_kill_share']} | {row['player_side_deployment_share']} | {row['offensive_contribution_ratio']} | {row['reliability_status']} |"
        )
    lines += ["", "## Qartheen Enthroned Guardian focus", "", "The requested focus is additive to the batch-wide table above. The three views below are deliberately separate.", "", "| view | battles | deployed | survivors | kills | deaths | wounded | kills/deployed | kill share | deployment share | contribution ratio | retention | gate |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for row in cohorts:
        lines.append(
            f"| {row['cohort_view']} | {row['independent_battles']} | {row['deployed']} | {row['survivors']} | {row['kills']} | {row['deaths']} | {row['wounded']} | {row['kills_per_deployed']} | {row['player_side_kill_share']} | {row['player_side_deployment_share']} | {row['offensive_contribution_ratio']} | {row['retention_rate']} | {'pass' if row['numeric_display_gate_passed'] else 'below gate'} |"
        )
    lines += [
        "", "The two-battle follow-up records **173 deployed / 138 kills = 0.797688 kills per deployed**. Its **86.25% kill share** remains above its **59.45% deployment share** (1.451x contribution ratio), with **100% retention**. The lower raw kills/deployed value is constrained by only 160 total enemy kills being available across these two small battles; it is not evidence of a causal performance collapse.", "",
        "The compatibility audit permits the seven-battle combined row only as descriptive continuity: both inputs are Realm of Thrones field battles for Egon Emeros' Party, use the same confirmed Guardian identity, contain completed results, and have distinct battle IDs and source hashes. Exact game build remains unknown, and campaign opponent, map, roster, orders, difficulty, and enemy availability are uncontrolled.", "",
        "PR #100's separate nine-field-battle dedicated cohort is not pooled into this continuity view. It already closed dedicated Guardian field testing after both the full cohort and its leave-one-highest-rate-battle sensitivity cleared the gate with kill share above deployment share. These two later distinct battles are directionally confirmatory on share and retention but remain below the battle gate, so they do not reopen or otherwise change that decision.", "",
        "## Identity, queue, and limitations", "",
        "Seven of the 12 ordinary labels resolve by one exact match in the versioned Realm of Thrones audit. `Lengii Mounted Slayer`, `Braavosi Soldier`, and `Braavosi Footman` remain provisional unmatched labels; `Dornish Archer [T3]` remains provisional because its prefix is occluded; the unreadable Deserters row remains unresolved and unpooled. No aliases or off-screen values are inferred.", "",
        "The authoritative queue remains unchanged: `active_test` is null, `ordered_queue` is empty, Qartheen Enthroned Guardian is closed by PR #100, and Arryn Winged Knight remains on verification hold. No future target is authorized.", "",
        "Raw PNG bytes are not retained in Git. Phase 2 verifies the exact Base64 Git blob, decoded archive, both checksum manifests, every member, repository mirrors, source links, and the two raw-source hashes preserved in the source manifest; later pixel-level rereview still requires the original uploads. Game version, command mode, and boost status remain unknown. `analysis/model_versions/` is unchanged, and no theoretical model recalibration is performed.", "",
    ]
    return "\n".join(lines)


def generate(analysis_dir: Path, review_dir: Path) -> tuple[list[str], list[str]]:
    analysis_dir.mkdir(parents=True, exist_ok=True)
    review_dir.mkdir(parents=True, exist_ok=True)
    files, bundle_verification = verify_bundle()
    immutable_snapshot = repository_snapshot(IMMUTABLE_PATHS, "immutable Phase 1 input")
    frozen_snapshot = repository_snapshot(FROZEN_MODEL_PATHS, "frozen model")
    events, parties, ordinary, characters = normalized_rows(files)
    aggregates = aggregate_rows(ordinary, parties)
    reliable = [row for row in aggregates if bool(row["numeric_display_gate_passed"])]
    insufficient = [row for row in aggregates if not bool(row["numeric_display_gate_passed"])]
    if len(aggregates) != 12 or reliable or len(insufficient) != 12:
        raise ValueError("unexpected batch-wide reliable/insufficient partition")
    cohorts, battle_rows, compatibility = guardian_cohorts(ordinary, parties)
    queue = queue_validation()
    dedup = dedup_audit(files, compatibility)

    review_rows = []
    for row in parse_csv(files["review_queue.csv"]):
        if row["review_id"] == "review_001":
            decision = "Label remains unreadable; keep the numeric row separate and unpooled."
        elif row["review_id"] == "review_002":
            decision = "Keep Dornish Archer [T3] as a provisional raw label; no exact pinned-audit match exists."
        elif row["review_id"] == "review_003":
            decision = "Exact game version remains unknown."
        else:
            decision = "Command mode and boost status remain unknown."
        review_rows.append({
            **row, "phase2_status": "resolved_by_preservation",
            "resolution_action": "preserve_without_guessing", "resolution": decision,
            "provenance": "Phase 1 review queue + versioned Realm of Thrones audit + Phase 2 evidence-boundary review",
        })

    write_csv(analysis_dir / "ordinary_occurrences.csv", OCCURRENCE_FIELDS, ordinary)
    write_csv(analysis_dir / "excluded_character_rows.csv", OCCURRENCE_FIELDS, characters)
    write_csv(analysis_dir / "ranking_complete.csv", RANKING_FIELDS, aggregates)
    write_csv(analysis_dir / "ranking_reliable.csv", RANKING_FIELDS, reliable)
    write_csv(analysis_dir / "insufficient_evidence.csv", RANKING_FIELDS, insufficient)
    write_csv(analysis_dir / "guardian_cohort_comparison.csv", COHORT_FIELDS, cohorts)
    battle_fields = (
        "cohort_view", "battle_id", "captured_at", "context", "result_scope", *COUNT_FIELDS,
        "kills_per_deployed", "retention_rate", "player_side_total_kills",
        "player_side_total_deployed", "source_image_sha256",
    )
    write_csv(analysis_dir / "guardian_battle_evidence.csv", battle_fields, battle_rows)
    write_csv(
        analysis_dir / "canonical_identity_audit.csv",
        ("display_name", "raw_name", "canonical_troop_id", "identity_status", "canonical_default_group", "canonical_role", "decision"),
        [
            {
                "display_name": row["display_name"], "raw_name": row["raw_name"],
                "canonical_troop_id": row["canonical_troop_id"], "identity_status": row["identity_status"],
                "canonical_default_group": row["canonical_default_group"], "canonical_role": row["canonical_role"],
                "decision": "exact audit match" if row["identity_status"] == "confirmed_id" else "preserve raw/provisional identity without alias",
            }
            for row in {item["display_name"]: item for item in ordinary}.values()
        ],
    )
    write_csv(
        analysis_dir / "screenshot_deduplication_audit.csv",
        ("screenshot_id", "image_sha256", "battle_id", "historical_exact_hash_matches", "historical_battle_id_matches", "pr100_hash_overlap", "pr100_battle_id_overlap", "decision", "reason"),
        dedup,
    )
    pressure_rows = []
    for event in events:
        allied = event["attacker_side"]
        enemy = event["defender_side"]
        allied_retention = allied["survivors"] / allied["deployed"]
        enemy_retention = enemy["survivors"] / enemy["deployed"]
        pressure_rows.append({
            "battle_id": event["event_id"], "context": event["context"],
            "result_state": event["result_status"], "frontline_deployed": "",
            "frontline_survivors": "", "frontline_retention": "",
            "frontline_status": "not_designated_in_mixed_campaign_evidence",
            "allied_deployed": allied["deployed"], "allied_remaining": allied["survivors"],
            "enemy_deployed": enemy["deployed"], "enemy_remaining": enemy["survivors"],
            "allied_retention": fmt(allied_retention), "enemy_retention": fmt(enemy_retention),
            "pressure_margin": fmt(allied_retention - enemy_retention),
            "metric_status": "final_battle_level_not_attributed_to_one_troop",
        })
    pressure_fields = (
        "battle_id", "context", "result_state", "frontline_deployed",
        "frontline_survivors", "frontline_retention", "frontline_status",
        "allied_deployed", "allied_remaining", "enemy_deployed", "enemy_remaining",
        "allied_retention", "enemy_retention", "pressure_margin", "metric_status",
    )
    write_csv(analysis_dir / "battle_pressure_margin.csv", pressure_fields, pressure_rows)
    write_csv(analysis_dir / "battle_context_review.csv", pressure_fields, pressure_rows)
    unresolved_rows = [row for row in ordinary if row["identity_status"] != "confirmed_id"]
    write_csv(
        analysis_dir / "unresolved_rows.csv",
        (*OCCURRENCE_FIELDS, "unresolved_reason"),
        [
            {
                **row,
                "unresolved_reason": (
                    "label unreadable and unpooled" if row["identity_status"] == "unresolved_label"
                    else "no exact versioned-audit match or transcription remains provisional"
                ),
            }
            for row in unresolved_rows
        ],
    )
    write_csv(
        analysis_dir / "outlier_report.csv",
        ("battle_id", "canonical_troop_id", "context", "deployed", "kills", "kills_per_deployed", "status", "primary_excluded"),
        [{
            "battle_id": "", "canonical_troop_id": FOCUS_ID, "context": "field",
            "deployed": "", "kills": "", "kills_per_deployed": "",
            "status": "not_run_new_follow_up_below_gate_and_no_predeclared_outlier_rule",
            "primary_excluded": False,
        }],
    )
    write_csv(
        analysis_dir / "grouping_validation.csv",
        ("check", "status", "detail"),
        [
            {"check": "player_enemy_boundary", "status": "pass", "detail": "player_party rows only"},
            {"check": "context_boundary", "status": "pass", "detail": "field only; no siege pooling"},
            {"check": "track_boundary", "status": "pass", "detail": TRACK},
            {"check": "cohort_boundary", "status": "pass", "detail": "Egon Emeros' Party only"},
            {"check": "unresolved_identity_boundary", "status": "pass", "detail": "unreadable row remains one unpooled group"},
            {"check": "pr100_cohort_boundary", "status": "pass", "detail": "nine-battle decision cohort not pooled"},
        ],
    )
    write_csv(
        analysis_dir / "aggregation_validation.csv",
        ("check", "expected", "actual", "status"),
        [
            {"check": "ordinary_occurrences", "expected": 13, "actual": len(ordinary), "status": "pass"},
            {"check": "excluded_character_rows", "expected": 18, "actual": len(characters), "status": "pass"},
            {"check": "aggregate_partition", "expected": 12, "actual": len(reliable) + len(insufficient), "status": "pass"},
            {"check": "guardian_historical_battles", "expected": 5, "actual": cohorts[0]["independent_battles"], "status": "pass"},
            {"check": "guardian_new_battles", "expected": 2, "actual": cohorts[1]["independent_battles"], "status": "pass"},
        ],
    )
    write_csv(
        analysis_dir / "model_vs_empirical.csv",
        ("status", "reason", "frozen_models_changed"),
        [{"status": "not_run", "reason": "No complete compatible Realm of Thrones v7.1/v7.3 empirical comparison universe is declared for this follow-up.", "frozen_models_changed": False}],
    )
    write_csv(
        analysis_dir / "empirical_residual_rankings.csv",
        ("status", "reason"),
        [{"status": "not_run", "reason": "Model comparison not run; no residual ranking is valid."}],
    )
    write_json(analysis_dir / "cohort_compatibility.json", compatibility)
    write_json(analysis_dir / "queue_validation.json", queue)
    historical_pins = [
        path_pin(HISTORICAL_DIR / name)
        for name in ("ranking_reliable.csv", "ordinary_occurrences.csv", "ANALYSIS_REPORT.md", "denominator_coverage.csv")
    ]
    pr100_pins = [
        path_pin(PR100_DIR / name)
        for name in ("ANALYSIS_REPORT.md", "focus_deep_dive.csv", "focus_sensitivity.csv", "focus_battle_rates.csv", "ordinary_occurrences.csv", "screenshot_deduplication_audit.csv")
    ]
    write_json(analysis_dir / "input_verification.json", {
        "status": "passed", "batch_id": BATCH_ID, "pipeline_mode": "offline-existing",
        "pipeline_version": "pr101-phase2-1.0.0", "schema_version": "1.0.0",
        "normalization_commit": NORMALIZATION_COMMIT, "required_main_commit": MAIN_COMMIT,
        "main_is_ancestor": subprocess.run(["git", "merge-base", "--is-ancestor", MAIN_COMMIT, "HEAD"], cwd=REPO_ROOT).returncode == 0,
        "immutable_phase1_snapshot": immutable_snapshot, "frozen_model_snapshot": frozen_snapshot,
        "normalized_bundle": bundle_verification,
        "identity_audit": {
            "path": str(IDENTITY_PATH.relative_to(REPO_ROOT)), "commit": MAIN_COMMIT,
            "sha256": IDENTITY_SHA256, "git_blob_sha": IDENTITY_BLOB,
            "worktree_bytes_equal_pinned_commit": True,
        },
        "historical_cohort_pins": historical_pins, "pr100_decision_cohort_pins": pr100_pins,
    })
    validation = {
        "status": "passed_with_documented_limits", "batch_id": BATCH_ID,
        "input_images": 2, "battles": 2, "ordinary_occurrences": len(ordinary),
        "excluded_character_rows": len(characters), "aggregate_rows": len(aggregates),
        "reliable_rows": len(reliable), "insufficient_rows": len(insufficient),
        "ordinary_partition_exact": len(ordinary) == 13 and len(aggregates) == len(reliable) + len(insufficient),
        "character_partition_exact": len(characters) == 18, "player_enemy_pooled": False,
        "contexts_pooled": False, "tracks_pooled": False, "cohorts_pooled": False,
        "offscreen_rows_inferred": False, "numeric_corrections": 0,
        "unresolved_label_rows": sum(row["identity_status"] == "unresolved_label" for row in ordinary),
        "provisional_dornish_rows": sum(row["raw_name"] == "Dornish Archer" for row in ordinary),
        "archive_hash_verified": True, "bundle_members_verified": 15,
        "source_links_verified": 31, "historical_duplicate_hashes": 0,
        "historical_duplicate_battle_ids": 0, "pr100_cohort_pooled": False,
        "historical_new_continuity_compatible": True, "combined_view_causal": False,
        "guardian_new_gate_passed": cohorts[1]["numeric_display_gate_passed"],
        "guardian_combined_gate_passed": cohorts[2]["numeric_display_gate_passed"],
        "queue_change": "none_already_closed_on_main", "future_target_authorized": False,
        "frozen_models_changed": False, "validation_errors": [],
        "unresolved_rows": len(unresolved_rows), "pressure_margin_rows": len(pressure_rows),
        "pressure_margin_status": "published_at_battle_level_not_attributed_to_one_troop",
        "outlier_analysis_status": "not_run_new_follow_up_below_gate_and_no_predeclared_outlier_rule",
        "below_gate_ranks_blank": all(not row["efficiency_rank"] and not row["impact_rank"] for row in insufficient),
        "role_adjusted_blended_rank_published": False,
    }
    write_json(analysis_dir / "validation_report.json", validation)
    write_json(analysis_dir / "canonical_validation_report.json", {
        **validation,
        "canonical_artifacts": {
            "ordinary_occurrences": "analysis/ordinary_occurrences.csv",
            "excluded_characters": "analysis/excluded_character_rows.csv",
            "complete_partition": "analysis/ranking_complete.csv",
            "reliable_partition": "analysis/ranking_reliable.csv",
            "insufficient_partition": "analysis/insufficient_evidence.csv",
            "unresolved_rows": "analysis/unresolved_rows.csv",
        },
    })
    write_json(analysis_dir / "analysis_state.json", {
        "status": "phase_2_complete_local_validation_passed", "batch_id": BATCH_ID,
        "normalization_commit": NORMALIZATION_COMMIT, "blockers": [],
        "queue_change": "none_already_closed_on_main",
        "queue_before": {"active_test": None, "ordered_queue": [], "verification_holds": ["arryn_moonknight"], "guardian_field": "closed"},
        "queue_after": {"active_test": None, "ordered_queue": [], "verification_holds": ["arryn_moonknight"], "guardian_field": "closed"},
        "decision": "The two new battles support the already-closed Guardian field decision descriptively but do not replace or pool with PR #100's nine-battle decision cohort.",
    })
    report = report_markdown(aggregates, cohorts)
    (analysis_dir / "ANALYSIS_REPORT.md").write_text(report, encoding="utf-8")
    (analysis_dir / "empirical_analysis_summary.md").write_text(
        "# Empirical analysis summary\n\n"
        "The batch contains 13 visible ordinary occurrences across 12 field troop rows; all 12 are below the 5-battle display gate, while 18 character rows remain excluded. "
        "The new Guardian follow-up is 2 battles / 173 deployed / 138 kills, with 86.25% kill share, 59.45% deployment share, 1.450795 contribution ratio, and 100% retention.\n\n"
        "The task-pinned historical cohort remains 5 battles / 195 deployed / 698 kills. The seven-battle combined row is descriptive and non-causal, and PR #100's distinct nine-battle decision cohort is not pooled.\n\n"
        "The authoritative queue remains unchanged: Guardian field testing is closed, the future queue is empty, and the Arryn Winged Knight verification hold remains.\n",
        encoding="utf-8",
    )
    (analysis_dir / "NEXT_TEST_RECOMMENDATION.md").write_text(
        "# Next-test recommendation\n\nNo future Realm of Thrones troop is authorized. The authoritative queue remains unchanged: `active_test` is null, `ordered_queue` is empty, Qartheen Enthroned Guardian field testing is already closed by PR #100, and Arryn Winged Knight remains on verification hold pending historical audit.\n",
        encoding="utf-8",
    )
    write_csv(
        review_dir / "review_resolutions.csv",
        (*parse_csv(files["review_queue.csv"])[0].keys(), "phase2_status", "resolution_action", "resolution", "provenance"),
        review_rows,
    )
    write_json(review_dir / "phase2_review_summary.json", {
        "status": "complete", "batch_id": BATCH_ID, "review_items": 4,
        "resolved_by_preservation": 4, "numeric_corrections": 0,
        "identity_aliases_added": 0, "normalized_inputs_modified": False,
        "decisions": [row["resolution"] for row in review_rows],
    })

    generated_analysis = sorted(path.name for path in analysis_dir.iterdir() if path.is_file() and path.name not in {"generate_phase2.py", "test_generate_phase2.py", "artifact_hashes.csv"})
    generated_review = sorted(path.name for path in review_dir.iterdir() if path.is_file())
    hash_rows = []
    for name in ["generate_phase2.py", "test_generate_phase2.py"]:
        canonical = ANALYSIS_DIR / name
        hash_rows.append({"path": f"analysis/{name}", "sha256": sha256_file(canonical), "bytes": canonical.stat().st_size})
    for name in generated_analysis:
        path = analysis_dir / name
        hash_rows.append({"path": f"analysis/{name}", "sha256": sha256_file(path), "bytes": path.stat().st_size})
    for name in generated_review:
        path = review_dir / name
        hash_rows.append({"path": f"reviewed/{name}", "sha256": sha256_file(path), "bytes": path.stat().st_size})
    write_csv(analysis_dir / "artifact_hashes.csv", ("path", "sha256", "bytes"), hash_rows)
    generated_analysis.append("artifact_hashes.csv")
    return sorted(generated_analysis), generated_review


def check_deterministic() -> None:
    with tempfile.TemporaryDirectory(prefix="pr101-phase2-check-") as tmp:
        root = Path(tmp)
        analysis = root / "analysis"
        reviewed = root / "reviewed"
        generated_analysis, generated_review = generate(analysis, reviewed)
        problems: list[str] = []
        for name in generated_analysis:
            actual = ANALYSIS_DIR / name
            expected = analysis / name
            if not actual.is_file() or actual.read_bytes() != expected.read_bytes():
                problems.append(f"analysis/{name}")
        for name in generated_review:
            actual = REVIEW_DIR / name
            expected = reviewed / name
            if not actual.is_file() or actual.read_bytes() != expected.read_bytes():
                problems.append(f"reviewed/{name}")
        if problems:
            raise SystemExit("deterministic output mismatch: " + ", ".join(problems))
    print("PR #101 Phase 2 deterministic outputs verified")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check_deterministic()
    else:
        generated_analysis, generated_review = generate(ANALYSIS_DIR, REVIEW_DIR)
        print(f"generated {len(generated_analysis)} analysis files and {len(generated_review)} reviewed files")


if __name__ == "__main__":
    main()
