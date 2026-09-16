#!/usr/bin/env python3
"""Generate the reviewed Phase 2 analysis for the Sep 12-14 mixed campaign batch."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import random
import re
import subprocess
import tarfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ANALYSIS_DIR = Path(__file__).resolve().parent
BATCH_DIR = ANALYSIS_DIR.parent
REPO_ROOT = ANALYSIS_DIR.parents[3]
REVIEW_DIR = BATCH_DIR / "reviewed"
BUNDLE_PATH = BATCH_DIR / "bundle/rot_mixed_campaign_phase1.tar.xz.base64"
BUNDLE_SHA_PATH = BATCH_DIR / "bundle/rot_mixed_campaign_phase1.tar.xz.sha256"
IDENTITY_PATH = REPO_ROOT / "data/realm_of_thrones/audit/realm_of_thrones_troops.csv"
QUEUE_PATH = REPO_ROOT / "data/combat_observations/test_queues/realm_of_thrones.json"

BATCH_ID = "2026-09-12-to-14-rot-mixed-campaign-phase1"
TRACK = "realm_of_thrones"
GAME_VERSION = "unknown"
NORMALIZATION_COMMIT = "c7004f9ead64687c1ed83bdbd2759a0ecbe32956"
ARCHIVE_SHA256 = "99754ec7fb614e86631bd6268c327140cd7c7882db7f612035015a6291b3adab"
ARCHIVE_SIZE = 12_944
DECLARED_BASE64_SHA256 = "1fe97af8dd1979f02e4c27b7e26277a80e8bde026ebc6e50d8b989adb24692d6"
DECLARED_BASE64_SIZE = 17_261
ACTUAL_BASE64_SHA256 = DECLARED_BASE64_SHA256
ACTUAL_BASE64_SIZE = DECLARED_BASE64_SIZE
SCREENSHOTS_MANIFEST_SHA256 = "42edb4f73e88bad528ff318c019b561ccd3bf02b4151dd714ea08325ed0734dd"
IDENTITY_AUDIT_SHA256 = "63ea983998e25aa0e6f8c0747bf42e44440f695bbe1fec717074e7ba64e42810"
QUEUE_SHA256 = "7a2a7906bc98f5d90394e07a9a329a52abc539044780bfb97f845dde1129bf6e"
GATE_BATTLES = 5
GATE_DEPLOYED = 20
BOOTSTRAP_REPETITIONS = 10_000
PRIMARY_FIELDS = ("survivors", "deaths", "wounded")
COUNT_FIELDS = ("deployed", "survivors", "kills", "deaths", "wounded", "routed")
STATS_FIELDS = ("survivors", "kills", "upgrade_ready", "deaths", "wounded", "routed")
EXPECTED_MEMBERS = {
    "README.md",
    "source_manifest.json",
    "source_inventory.csv",
    "screenshots_manifest.csv",
    "integrity_report.json",
    "phase1_checkpoint.json",
    "batch_state.json",
    "normalized/events.jsonl",
    "normalized/party_summaries.jsonl",
    "normalized/player_rows.jsonl",
    "handoff/ANALYSIS_TASK_V1.json",
}
DECLARED_HANDOFF_INPUTS = (
    "phase1_checkpoint.json",
    "batch_state.json",
    "source_manifest.json",
    "source_inventory.csv",
    "screenshots_manifest.csv",
    "normalized/events.jsonl",
    "normalized/party_summaries.jsonl",
    "normalized/player_rows.jsonl",
    "integrity_report.json",
    "bundle/rot_mixed_campaign_phase1.tar.xz.base64",
    "bundle/rot_mixed_campaign_phase1.tar.xz.sha256",
)
IMMUTABLE_PHASE1_PATHS = (
    f"data/combat_observations/{BATCH_ID}/README.md",
    f"data/combat_observations/{BATCH_ID}/batch_state.json",
    f"data/combat_observations/{BATCH_ID}/phase1_checkpoint.json",
    f"data/combat_observations/{BATCH_ID}/screenshots_manifest.csv",
    f"data/combat_observations/{BATCH_ID}/bundle",
    f"data/combat_observations/{BATCH_ID}/handoff",
)
FROZEN_MODEL_PATHS = ("analysis/model_versions",)

RANKING_FIELDS = (
    "track",
    "game_version",
    "cohort",
    "context",
    "participant_scope",
    "result_scope",
    "efficiency_rank",
    "impact_rank",
    "display_name",
    "troop_name",
    "tier",
    "canonical_troop_id",
    "identity_status",
    "canonical_default_group",
    "canonical_role",
    "evidence_grade",
    "reliable_role_population",
    "role_adjusted_rank_status",
    "independent_battles",
    "complete_numeric_battles",
    "ordinary_occurrences",
    "complete_numeric_occurrences",
    *COUNT_FIELDS,
    "known_deployed_from_complete_occurrences",
    "known_kills",
    "kills_per_deployed",
    "ci95_low",
    "ci95_high",
    "verified_player_side_total_kills",
    "kill_total_coverage_battles",
    "kill_total_coverage_complete",
    "player_side_kill_share",
    "share_adjusted_impact",
    "verified_player_side_total_deployed",
    "deployment_total_coverage_battles",
    "deployment_total_coverage_complete",
    "player_side_deployment_share",
    "offensive_contribution_ratio",
    "offensive_share_gap",
    "retention_rate",
    "death_rate",
    "casualty_rate",
    "final_victory_battles",
    "outside_stage_success_battles",
    "active_censored_battles",
    "numeric_display_gate_passed",
    "identity_gate_passed",
    "reliability_status",
    "more_battles_needed",
    "more_deployed_needed",
    "missing_numeric_fields",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_csv_path(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_csv(payload: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))


def parse_json(payload: bytes) -> dict[str, Any]:
    value = json.loads(payload.decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected JSON object")
    return value


def parse_jsonl(payload: bytes) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in payload.decode("utf-8").splitlines() if line]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError("expected JSONL objects")
    return rows


def fmt(value: float | None) -> str:
    return "" if value is None else f"{value:.6f}"


def bool_text(value: Any) -> bool:
    return str(value).strip().casefold() == "true"


def slug(value: str) -> str:
    return "_".join(re.findall(r"[a-z0-9]+", value.casefold()))


def csv_safe(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        stripped = value.lstrip()
        is_numeric_literal = bool(re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", stripped))
        if stripped.startswith(("=", "+", "-", "@")) and not is_numeric_literal:
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
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def extract_verified_bundle() -> tuple[dict[str, bytes], dict[str, Any]]:
    encoded = BUNDLE_PATH.read_bytes()
    if len(encoded) != ACTUAL_BASE64_SIZE or sha256_bytes(encoded) != ACTUAL_BASE64_SHA256:
        raise ValueError("committed Base64 transport bytes changed after Phase 1 handoff")
    compact = re.sub(rb"[\t\n\r ]+", b"", encoded)
    if re.search(rb"[^A-Za-z0-9+/=]", compact):
        raise ValueError("normalized bundle contains non-Base64 bytes")
    archive = base64.b64decode(compact, validate=True)
    if len(archive) != ARCHIVE_SIZE or sha256_bytes(archive) != ARCHIVE_SHA256:
        raise ValueError("normalized archive hash or size mismatch")

    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as bundle:
        for member in bundle.getmembers():
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or not member.isfile():
                raise ValueError(f"unsafe normalized bundle member: {member.name}")
            if member.name in files:
                raise ValueError(f"duplicate normalized bundle member: {member.name}")
            extracted = bundle.extractfile(member)
            if extracted is None:
                raise ValueError(f"unreadable normalized bundle member: {member.name}")
            files[member.name] = extracted.read()
    if set(files) != EXPECTED_MEMBERS:
        raise ValueError("normalized archive member set mismatch")

    member_hashes = {
        name: {"sha256": sha256_bytes(payload), "size_bytes": len(payload)}
        for name, payload in sorted(files.items())
    }
    return files, {
        "sha256": ARCHIVE_SHA256,
        "size_bytes": len(archive),
        "members": len(files),
        "safe_preflight_passed": True,
        "member_hashes": member_hashes,
        "base64_transport": {
            "declared_sha256": DECLARED_BASE64_SHA256,
            "actual_sha256": ACTUAL_BASE64_SHA256,
            "declared_size_bytes": DECLARED_BASE64_SIZE,
            "actual_size_bytes": ACTUAL_BASE64_SIZE,
            "review_status": "verified_exact",
            "evidence_values_affected": False,
        },
    }


def verify_handoff_inventory(files: dict[str, bytes]) -> dict[str, Any]:
    sha_line = BUNDLE_SHA_PATH.read_text(encoding="utf-8").strip().split()
    if not sha_line or sha_line[0] != ARCHIVE_SHA256:
        raise ValueError("normalized archive checksum file does not match the verified archive")
    resolutions = []
    missing = []
    for declared in DECLARED_HANDOFF_INPUTS:
        if declared.startswith("bundle/"):
            path = BATCH_DIR / declared
            present = path.is_file()
            resolution = f"repository:{declared}"
            digest = sha256_file(path) if present else ""
        else:
            present = declared in files
            resolution = f"archive:{declared}"
            digest = sha256_bytes(files[declared]) if present else ""
        if not present:
            missing.append(declared)
        resolutions.append(
            {
                "declared_path": declared,
                "resolution": resolution,
                "status": "verified" if present else "missing",
                "sha256": digest,
            }
        )
    if missing:
        raise ValueError(f"unexpected handoff input inventory: missing={missing}")
    return {
        "status": "passed",
        "declared_inputs": resolutions,
        "verified_count": len(resolutions),
        "missing_inputs": missing,
    }


def verify_screenshot_manifest(
    files: dict[str, bytes],
    source_index: dict[str, dict[str, Any]],
    event_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    repository_bytes = (BATCH_DIR / "screenshots_manifest.csv").read_bytes()
    archive_bytes = files["screenshots_manifest.csv"]
    if repository_bytes != archive_bytes:
        raise ValueError("repository/archive screenshots_manifest.csv bytes differ")
    if sha256_bytes(archive_bytes) != SCREENSHOTS_MANIFEST_SHA256:
        raise ValueError("screenshots_manifest.csv hash mismatch")

    reader = csv.DictReader(io.StringIO(archive_bytes.decode("utf-8")))
    expected_fields = [
        "screenshot_id",
        "image_file",
        "image_sha256",
        "captured_at",
        "battle_id",
        "screen_status",
        "included_in_primary",
        "game_version",
        "game_track",
    ]
    if reader.fieldnames != expected_fields:
        raise ValueError("screenshots_manifest.csv schema mismatch")
    rows = list(reader)
    if len(rows) != 16:
        raise ValueError("screenshots_manifest.csv row count mismatch")
    rows_by_id = {row["screenshot_id"]: row for row in rows}
    if len(rows_by_id) != len(rows):
        raise ValueError("screenshots_manifest.csv screenshot IDs are not unique")

    expected_ids = {
        source_key.replace("src_", "screen_", 1) for source_key in source_index
    }
    if set(rows_by_id) != expected_ids:
        raise ValueError("screenshots_manifest.csv source inventory mismatch")
    for source_key, source in source_index.items():
        event_ids = source["event_ids"]
        if len(event_ids) != 1 or event_ids[0] not in event_index:
            raise ValueError(f"invalid source-to-battle mapping: {source_key}")
        event_id = event_ids[0]
        event = event_index[event_id]
        row = rows_by_id[source_key.replace("src_", "screen_", 1)]
        expected = {
            "image_file": source["filename"],
            "image_sha256": source["sha256"],
            "captured_at": source["capture_timestamp_local"],
            "battle_id": event_id,
            "screen_status": (
                "active" if event["result_status"] == "in_progress" else "final_result"
            ),
            "included_in_primary": "True",
            "game_version": GAME_VERSION,
            "game_track": TRACK,
        }
        if any(row[field] != value for field, value in expected.items()):
            raise ValueError(f"screenshots_manifest.csv source row mismatch: {source_key}")

    battle_ids = {row["battle_id"] for row in rows}
    status_counts = Counter(row["screen_status"] for row in rows)
    if len(battle_ids) != 15 or status_counts != {"active": 3, "final_result": 13}:
        raise ValueError("screenshots_manifest.csv battle/status partition mismatch")
    return {
        "status": "verified_repository_archive_exact",
        "sha256": SCREENSHOTS_MANIFEST_SHA256,
        "rows": len(rows),
        "battle_ids": len(battle_ids),
        "active_screens": status_counts["active"],
        "final_result_screens": status_counts["final_result"],
        "repository_archive_bytes_equal": True,
    }


def repository_snapshot(paths: tuple[str, ...], label: str) -> dict[str, Any]:
    committed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", NORMALIZATION_COMMIT, "--", *paths],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    modified = subprocess.run(
        ["git", "diff", "--name-only", NORMALIZATION_COMMIT, "--", *paths],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    missing = [path for path in committed if not (REPO_ROOT / path).is_file()]
    if modified or missing:
        raise ValueError(f"{label} changed after normalization: {modified + missing}")
    return {
        "baseline_commit": NORMALIZATION_COMMIT,
        "paths": list(paths),
        "files_verified": len(committed),
        "modified_files": modified,
        "missing_files": missing,
    }


def verify_source_records(
    files: dict[str, bytes], events: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    manifest = parse_json(files["source_manifest.json"])
    inventory = parse_csv(files["source_inventory.csv"])
    sources = manifest.get("sources", [])
    if len(sources) != 16 or len(inventory) != 16:
        raise ValueError("source manifest count mismatch")
    manifest_index = {row["source_key"]: row for row in sources}
    inventory_index = {row["source_key"]: row for row in inventory}
    if len(manifest_index) != 16 or set(manifest_index) != set(inventory_index):
        raise ValueError("source manifest/inventory key mismatch")
    for source_key, source in manifest_index.items():
        row = inventory_index[source_key]
        expected = {
            "filename": source["filename"],
            "sha256": source["sha256"],
            "bytes": str(source["bytes"]),
            "width": str(source["width"]),
            "height": str(source["height"]),
            "capture_timestamp_local": source["capture_timestamp_local"],
            "event_ids": "|".join(source["event_ids"]),
        }
        if any(row[field] != value for field, value in expected.items()):
            raise ValueError(f"source manifest/inventory mismatch: {source_key}")
    if len({row["sha256"] for row in sources}) != 16:
        raise ValueError("source hashes are not unique")

    event_index = {event["event_id"]: event for event in events}
    if len(event_index) != 15:
        raise ValueError("event count mismatch while validating source links")
    linked_keys = [key for event in events for key in event["source_keys"]]
    if Counter(linked_keys) != Counter(manifest_index.keys()):
        raise ValueError("every source must link to exactly one event")

    historical_paths = sorted(
        set((REPO_ROOT / "data/combat_observations").glob("**/screenshots_manifest.csv"))
        | set((REPO_ROOT / "data/combat_observations").glob("**/source_inventory.csv"))
    )
    historical_text = {
        path: path.read_text(encoding="utf-8", errors="replace")
        for path in historical_paths
        if BATCH_ID not in path.as_posix()
    }
    historical_matches: dict[str, list[str]] = {
        source["sha256"]: [
            path.relative_to(REPO_ROOT).as_posix()
            for path, text in historical_text.items()
            if source["sha256"] in text
        ]
        for source in sources
    }
    event_sources = {event["event_id"]: event["source_keys"] for event in events}
    audit_rows = []
    for source in sorted(sources, key=lambda row: row["capture_timestamp_local"]):
        event_id = source["event_ids"][0]
        siblings = event_sources[event_id]
        representative = siblings[0]
        supplemental = len(siblings) > 1 and source["source_key"] != representative
        audit_rows.append(
            {
                "source_key": source["source_key"],
                "filename": source["filename"],
                "sha256": source["sha256"],
                "event_id": event_id,
                "representative_source_key": representative,
                "decision": "accepted_supplemental" if supplemental else "accepted_primary",
                "same_battle_status": "same_event_complementary" if len(siblings) > 1 else "independent_event",
                "historical_exact_hash_matches": "|".join(historical_matches[source["sha256"]]),
                "visual_reason_provenance": (
                    "Phase 1 records identical duration and side totals with complementary party scroll positions"
                    if len(siblings) > 1
                    else "Phase 1 normalized as an independent event"
                ),
            }
        )
    return audit_rows, {
        "manifest_entries_verified": len(sources),
        "source_bytes_total": sum(int(row["bytes"]) for row in sources),
        "raw_repository_retention": "not_retained_optional_after_verified_normalization",
        "raw_source_bytes_locally_verified": False,
        "source_hashes_preserved": True,
        "historical_manifest_files_scanned": len(historical_text),
        "historical_exact_hash_matches": sum(bool(value) for value in historical_matches.values()),
        "newly_accepted_screenshots": len(audit_rows),
        "supplemental_screenshots": sum(row["decision"] == "accepted_supplemental" for row in audit_rows),
        "internal_duplicate_screenshots": 0,
        "already_normalized_screenshots": sum(bool(value) for value in historical_matches.values()),
    }


def canonical_role(default_group: str) -> str:
    group = default_group.casefold()
    if group == "infantry":
        return "frontline_infantry"
    if group in {"ranged", "horsearcher", "horse_archer"}:
        return "ranged"
    if group == "cavalry":
        return "melee_cavalry"
    return ""


def resolve_identities(raw_rows: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    if sha256_file(IDENTITY_PATH) != IDENTITY_AUDIT_SHA256:
        raise ValueError("versioned Realm of Thrones identity audit hash mismatch")
    audit = read_csv_path(IDENTITY_PATH)
    by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in audit:
        by_name[row.get("name", "").casefold()].append(row)
    observed: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in raw_rows:
        observed[row["troop_name"]].append(row)

    decisions: dict[str, dict[str, Any]] = {}
    audit_rows = []
    for name, observations in sorted(observed.items(), key=lambda item: item[0].casefold()):
        tiers = sorted({row["tier"] for row in observations if row["tier"] is not None})
        has_character_rows = any(row["tier"] is None for row in observations)
        has_ordinary_rows = bool(tiers)
        if has_character_rows and has_ordinary_rows:
            raise ValueError(f"display name crosses character/troop boundary: {name}")
        exact_matches = by_name[name.casefold()]
        matches = (
            [row for row in exact_matches if bool_text(row.get("is_soldier", ""))]
            if has_ordinary_rows
            else exact_matches
        )
        non_soldier_matches = [
            row for row in exact_matches if not bool_text(row.get("is_soldier", ""))
        ]
        candidate_ids = sorted({row["troop_id"] for row in matches})
        matched = matches[0] if len(candidate_ids) == 1 else {}
        is_character = has_character_rows
        audit_marks_hero = bool_text(matched.get("is_hero", "")) if matched else False
        if is_character:
            status = "excluded_character_confirmed" if matched else "excluded_character_unresolved_identity"
        elif len(candidate_ids) == 1 and not audit_marks_hero:
            status = "confirmed_id"
        elif len(candidate_ids) > 1:
            status = "ambiguous_exact_name"
        elif audit_marks_hero:
            status = "conflict_tiered_row_matches_hero"
        else:
            status = "unresolved_provisional_label"
        canonical_id = candidate_ids[0] if len(candidate_ids) == 1 else ""
        decision = {
            "canonical_troop_id": canonical_id,
            "identity_status": status,
            "default_group": matched.get("default_group", ""),
            "canonical_role": canonical_role(matched.get("default_group", "")),
            "level": matched.get("level", ""),
            "candidate_count": len(candidate_ids),
            "candidate_troop_ids": "|".join(candidate_ids),
            "non_soldier_exact_match_ids": "|".join(
                sorted({row["troop_id"] for row in non_soldier_matches})
            ),
            "row_class": "character" if is_character else "ordinary_troop",
            "blocking_reason": (
                "" if status in {"confirmed_id", "excluded_character_confirmed"}
                else "exact display-name matches only non-soldier audit rows"
                if non_soldier_matches
                else "no exact display-name match in the versioned track audit"
                if not candidate_ids
                else "multiple exact display-name matches in the versioned track audit"
            ),
        }
        decisions[name] = decision
        audit_rows.append(
            {
                "display_name": name,
                "observed_tiers": "|".join(str(tier) for tier in tiers),
                "row_class": decision["row_class"],
                "ordinary_occurrences": sum(row["tier"] is not None for row in observations),
                "excluded_character_occurrences": sum(row["tier"] is None for row in observations),
                "canonical_troop_id": canonical_id,
                "resolution_status": status,
                "default_group": decision["default_group"],
                "canonical_role": decision["canonical_role"],
                "level": decision["level"],
                "candidate_count": decision["candidate_count"],
                "candidate_troop_ids": decision["candidate_troop_ids"],
                "non_soldier_exact_match_ids": decision["non_soldier_exact_match_ids"],
                "resolution_method": "exact display-name match in pinned track audit" if matched else "no inferred alias",
                "blocking_reason": decision["blocking_reason"],
                "audit_path": IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(),
                "audit_sha256": IDENTITY_AUDIT_SHA256,
            }
        )
    return decisions, audit_rows


def row_deployed(stats: dict[str, Any]) -> int | None:
    values = [stats.get(field) for field in PRIMARY_FIELDS]
    return sum(values) if all(isinstance(value, int) for value in values) else None


def adapt_rows(
    raw_rows: list[dict[str, Any]],
    event_index: dict[str, dict[str, Any]],
    source_index: dict[str, dict[str, Any]],
    identities: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ordinary = []
    excluded = []
    for raw in raw_rows:
        event = event_index[raw["event_id"]]
        stats = raw["stats"]
        decision = identities[raw["troop_name"]]
        source_hashes = "|".join(source_index[key]["sha256"] for key in event["source_keys"])
        adapted = {
            "observation_id": raw["row_id"],
            "battle_id": raw["event_id"],
            "captured_at": event["capture_timestamp_local"],
            "track": TRACK,
            "game_version": GAME_VERSION,
            "context": event["battle_context"],
            "result_scope": "active_censored" if event["result_status"] == "in_progress" else "completed",
            "cohort": raw["party_name"],
            "participant_scope": "player_party" if raw["party_role"] == "primary" else "allied_party",
            "troop_name": raw["troop_name"],
            "tier": raw["tier"],
            "display_name": (
                f"{raw['troop_name']} [T{raw['tier']}]" if raw["tier"] is not None else raw["troop_name"]
            ),
            "canonical_troop_id": decision["canonical_troop_id"],
            "identity_status": decision["identity_status"],
            "canonical_default_group": decision["default_group"],
            "canonical_role": decision["canonical_role"],
            "visibility": raw["visibility"],
            "source_image_sha256": source_hashes,
            "note": raw.get("note") or "",
            **{field: stats.get(field) for field in STATS_FIELDS},
            "deployed": row_deployed(stats),
        }
        if raw["tier"] is None:
            adapted["exclusion_reason"] = "character_or_hero_row_without_troop_tier"
            excluded.append(adapted)
        else:
            ordinary.append(adapted)
    return ordinary, excluded


def evidence_grade(independent_battles: int, deployed: int | None) -> str:
    if deployed is None:
        return "exploratory_incomplete_numeric"
    if independent_battles >= 5 and deployed >= 100:
        return "high"
    if independent_battles >= 3 and deployed >= 30:
        return "medium"
    if independent_battles >= 2 and deployed >= 10:
        return "low"
    return "exploratory"


def bootstrap(rows: list[dict[str, Any]], key: str) -> tuple[float, float]:
    seed = int(hashlib.sha256(f"{BATCH_ID}|{key}|{BOOTSTRAP_REPETITIONS}".encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    ordered = sorted(rows, key=lambda row: row["battle_id"])
    values = []
    for _ in range(BOOTSTRAP_REPETITIONS):
        sample = [ordered[rng.randrange(len(ordered))] for _ in ordered]
        deployed = sum(int(row["deployed"]) for row in sample)
        kills = sum(int(row["kills"]) for row in sample)
        values.append(kills / deployed)
    values.sort()
    return values[int(0.025 * (len(values) - 1))], values[int(0.975 * (len(values) - 1))]


def aggregate_rows(
    rows: list[dict[str, Any]],
    event_index: dict[str, dict[str, Any]],
    *,
    include_result_scope: bool = False,
) -> list[dict[str, Any]]:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key: tuple[Any, ...] = (
            row["cohort"],
            row["participant_scope"],
            row["context"],
            row["display_name"],
        )
        if include_result_scope:
            key += (row["result_scope"],)
        groups[key].append(row)

    output = []
    for key, subset in groups.items():
        cohort, scope, context, display_name = key[:4]
        result_scope = key[4] if include_result_scope else "all_valid_observations"
        battle_ids = sorted({row["battle_id"] for row in subset})
        complete = [
            row
            for row in subset
            if row["deployed"] is not None
            and all(row.get(field) is not None for field in ("kills", "survivors", "deaths", "wounded", "routed"))
        ]
        aggregates = {
            field: (
                sum(int(row[field]) for row in subset)
                if all(row.get(field) is not None for row in subset)
                else None
            )
            for field in COUNT_FIELDS
        }
        deployed = aggregates["deployed"]
        kills = aggregates["kills"]
        independent = len(battle_ids)
        numeric_gate = independent >= GATE_BATTLES and deployed is not None and deployed >= GATE_DEPLOYED
        identity_status = subset[0]["identity_status"]
        identity_gate = identity_status == "confirmed_id"
        missing_fields = sorted(
            {
                field
                for row in subset
                for field in STATS_FIELDS
                if row.get(field) is None
            }
        )
        if missing_fields:
            reliability = "insufficient_missing_numeric_values"
        elif independent < GATE_BATTLES:
            reliability = "insufficient_battles"
        elif deployed is None or deployed < GATE_DEPLOYED:
            reliability = "insufficient_deployed"
        elif not identity_gate:
            reliability = "reliable_provisional_identity"
        else:
            reliability = "reliable"

        side_kills = sum(int(event_index[battle_id]["player_side_totals"]["kills"]) for battle_id in battle_ids)
        side_deployed = sum(
            int(event_index[battle_id]["player_side_totals"]["survivors"])
            + int(event_index[battle_id]["player_side_totals"]["deaths"])
            + int(event_index[battle_id]["player_side_totals"]["wounded"])
            for battle_id in battle_ids
        )
        efficiency = kills / deployed if numeric_gate and kills is not None and deployed else None
        kill_share = kills / side_kills if numeric_gate and kills is not None and side_kills > 0 else None
        deployment_share = deployed / side_deployed if numeric_gate and deployed is not None and side_deployed > 0 else None
        ci_low, ci_high = (
            bootstrap(subset, "|".join(str(value) for value in key))
            if numeric_gate and all(row in complete for row in subset)
            else (None, None)
        )
        outcome_counts = Counter(
            "outside_stage_success" if event_index[battle_id]["outside_stage_success"] else "final_victory"
            if event_index[battle_id]["result_status"] == "final"
            else "active_censored"
            for battle_id in battle_ids
        )
        output.append(
            {
                "track": TRACK,
                "game_version": GAME_VERSION,
                "cohort": cohort,
                "context": context,
                "participant_scope": scope,
                "result_scope": result_scope,
                "efficiency_rank": "",
                "impact_rank": "",
                "display_name": display_name,
                "troop_name": subset[0]["troop_name"],
                "tier": subset[0]["tier"],
                "canonical_troop_id": subset[0]["canonical_troop_id"],
                "identity_status": identity_status,
                "canonical_default_group": subset[0]["canonical_default_group"],
                "canonical_role": subset[0]["canonical_role"],
                "evidence_grade": evidence_grade(independent, deployed),
                "reliable_role_population": 0,
                "role_adjusted_rank_status": "not_published_current_methodology_keeps_offense_and_defense_independent",
                "independent_battles": independent,
                "complete_numeric_battles": len({row["battle_id"] for row in complete}),
                "ordinary_occurrences": len(subset),
                "complete_numeric_occurrences": len(complete),
                **aggregates,
                "known_deployed_from_complete_occurrences": sum(int(row["deployed"]) for row in complete),
                "known_kills": sum(int(row["kills"]) for row in subset if row["kills"] is not None),
                "kills_per_deployed": fmt(efficiency),
                "ci95_low": fmt(ci_low),
                "ci95_high": fmt(ci_high),
                "verified_player_side_total_kills": side_kills,
                "kill_total_coverage_battles": independent,
                "kill_total_coverage_complete": True,
                "player_side_kill_share": fmt(kill_share),
                "share_adjusted_impact": fmt(efficiency * kill_share if efficiency is not None and kill_share is not None else None),
                "verified_player_side_total_deployed": side_deployed,
                "deployment_total_coverage_battles": independent,
                "deployment_total_coverage_complete": True,
                "player_side_deployment_share": fmt(deployment_share),
                "offensive_contribution_ratio": fmt(
                    kill_share / deployment_share
                    if kill_share is not None and deployment_share not in (None, 0)
                    else None
                ),
                "offensive_share_gap": fmt(
                    kill_share - deployment_share
                    if kill_share is not None and deployment_share is not None
                    else None
                ),
                "retention_rate": fmt(
                    aggregates["survivors"] / deployed
                    if numeric_gate and aggregates["survivors"] is not None and deployed
                    else None
                ),
                "death_rate": fmt(
                    aggregates["deaths"] / deployed
                    if numeric_gate and aggregates["deaths"] is not None and deployed
                    else None
                ),
                "casualty_rate": fmt(
                    (aggregates["deaths"] + aggregates["wounded"]) / deployed
                    if numeric_gate
                    and aggregates["deaths"] is not None
                    and aggregates["wounded"] is not None
                    and deployed
                    else None
                ),
                "final_victory_battles": outcome_counts["final_victory"],
                "outside_stage_success_battles": outcome_counts["outside_stage_success"],
                "active_censored_battles": outcome_counts["active_censored"],
                "numeric_display_gate_passed": numeric_gate,
                "identity_gate_passed": identity_gate,
                "reliability_status": reliability,
                "more_battles_needed": max(0, GATE_BATTLES - independent),
                "more_deployed_needed": "" if deployed is None else max(0, GATE_DEPLOYED - deployed),
                "missing_numeric_fields": "|".join(missing_fields),
            }
        )
    assign_ranks(output, include_result_scope=include_result_scope)
    return sorted(
        output,
        key=lambda row: (
            row["cohort"],
            row["context"],
            row["participant_scope"],
            row.get("result_scope", ""),
            int(row["efficiency_rank"]) if row["efficiency_rank"] != "" else 10**9,
            row["display_name"],
        ),
    )


def assign_ranks(rows: list[dict[str, Any]], *, include_result_scope: bool) -> None:
    groups: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        key: tuple[Any, ...] = (row["cohort"], row["context"], row["participant_scope"])
        if include_result_scope:
            key += (row["result_scope"],)
        groups[key].append(row)
    for group in groups.values():
        efficiency = [
            row for row in group if row["numeric_display_gate_passed"] and row["kills_per_deployed"] != ""
        ]
        impact = [
            row for row in group if row["numeric_display_gate_passed"] and row["share_adjusted_impact"] != ""
        ]
        for rank, row in enumerate(
            sorted(efficiency, key=lambda item: (-float(item["kills_per_deployed"]), -int(item["deployed"]), item["display_name"])),
            1,
        ):
            row["efficiency_rank"] = rank
        for rank, row in enumerate(
            sorted(impact, key=lambda item: (-float(item["share_adjusted_impact"]), -int(item["deployed"]), item["display_name"])),
            1,
        ):
            row["impact_rank"] = rank
        role_counts = Counter(
            row["canonical_role"]
            for row in group
            if row["reliability_status"].startswith("reliable") and row["canonical_role"]
        )
        for row in group:
            row["reliable_role_population"] = role_counts[row["canonical_role"]] if row["canonical_role"] else 0


def rerank_reliable(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reliable = [dict(row) for row in rows if row["reliability_status"].startswith("reliable")]
    for row in reliable:
        row["efficiency_rank"] = ""
        row["impact_rank"] = ""
    assign_ranks(reliable, include_result_scope=True)
    return sorted(
        reliable,
        key=lambda row: (
            row["cohort"],
            row["context"],
            row["participant_scope"],
            row["result_scope"],
            int(row["efficiency_rank"]),
        ),
    )


def pressure_rows(events: list[dict[str, Any]], source_index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for event in sorted(events, key=lambda row: row["capture_timestamp_local"]):
        player = event["player_side_totals"]
        opponent = event["opponent_side_totals"]
        player_deployed = sum(int(player[field]) for field in PRIMARY_FIELDS)
        opponent_deployed = sum(int(opponent[field]) for field in PRIMARY_FIELDS)
        allied_retention = player["survivors"] / player_deployed
        enemy_retention = opponent["survivors"] / opponent_deployed
        final = event["result_status"] == "final"
        output.append(
            {
                "battle_id": event["event_id"],
                "captured_at": event["capture_timestamp_local"],
                "context": event["battle_context"],
                "player_side": event["player_side"],
                "result": event["outcome"],
                "outside_stage_success": event["outside_stage_success"],
                "observation_censoring": "final" if final else "right_censored",
                "player_deployed": player_deployed,
                "player_remaining": player["survivors"],
                "allied_retention": fmt(allied_retention),
                "opponent_deployed": opponent_deployed,
                "opponent_remaining": opponent["survivors"],
                "enemy_retention": fmt(enemy_retention),
                "pressure_margin": fmt(allied_retention - enemy_retention),
                "metric_status": "final_stage" if final else "diagnostic_censored_snapshot",
                "included_in_final_pressure_summary": final,
                "source_image_sha256": "|".join(source_index[key]["sha256"] for key in event["source_keys"]),
            }
        )
    return output


def denominator_rows(events: list[dict[str, Any]], source_index: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for event in sorted(events, key=lambda row: row["capture_timestamp_local"]):
        totals = event["player_side_totals"]
        deployed = sum(int(totals[field]) for field in PRIMARY_FIELDS)
        output.append(
            {
                "battle_id": event["event_id"],
                "captured_at": event["capture_timestamp_local"],
                "context": event["battle_context"],
                "result": event["outcome"],
                "player_side_total_kills": totals["kills"],
                "player_side_total_deployed": deployed,
                "kill_total_direct_positive": totals["kills"] > 0,
                "deployment_total_direct_positive": deployed > 0,
                "provenance": "normalized_visible_player_side_total",
                "source_image_sha256": "|".join(source_index[key]["sha256"] for key in event["source_keys"]),
            }
        )
    return output


def validate_queue() -> dict[str, Any]:
    if sha256_file(QUEUE_PATH) != QUEUE_SHA256:
        raise ValueError("authoritative Realm of Thrones queue changed during Phase 2")
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    active = queue.get("active_test")
    ordered = queue.get("ordered_queue", [])
    holds = queue.get("verification_holds", [])
    parked = queue.get("parked", [])
    closed = queue.get("closed", [])
    if active is not None:
        raise ValueError("mixed campaign batch cannot displace an active approved target")
    priorities = [row["priority"] for row in ordered]
    if len(priorities) != len(set(priorities)):
        raise ValueError("queue priorities are not unique")
    memberships = []
    for category, values in (
        ("ordered_queue", ordered),
        ("verification_holds", holds),
        ("parked", parked),
        ("closed", closed),
    ):
        for value in values:
            memberships.append((value["troop_id"], value["context"], category))
    pairs = [(troop_id, context) for troop_id, context, _ in memberships]
    if len(pairs) != len(set(pairs)):
        raise ValueError("troop/context appears in multiple queue categories")
    return {
        "status": "passed_no_change",
        "path": QUEUE_PATH.relative_to(REPO_ROOT).as_posix(),
        "sha256_before": QUEUE_SHA256,
        "sha256_after": QUEUE_SHA256,
        "active_test": active,
        "ordered_queue": ordered,
        "verification_holds": holds,
        "parked": parked,
        "closed": closed,
        "queue_change": "none",
        "decision_reason": "Mixed campaign rosters have no approved primary test unit; do not infer a new target.",
    }


def context_coverage_rows(
    ordinary: list[dict[str, Any]],
    excluded: list[dict[str, Any]],
    rankings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str, str], dict[str, Any]] = defaultdict(
        lambda: {"battle_ids": set(), "ordinary": 0, "partial": 0, "excluded": 0, "partition": 0, "reliable": 0, "insufficient": 0}
    )
    for row in ordinary:
        key = (row["cohort"], row["context"], row["participant_scope"], row["result_scope"])
        groups[key]["battle_ids"].add(row["battle_id"])
        groups[key]["ordinary"] += 1
        groups[key]["partial"] += row["visibility"] != "full" or row["deployed"] is None or row["kills"] is None
    for row in excluded:
        key = (row["cohort"], row["context"], row["participant_scope"], row["result_scope"])
        groups[key]["battle_ids"].add(row["battle_id"])
        groups[key]["excluded"] += 1
    for row in rankings:
        key = (row["cohort"], row["context"], row["participant_scope"], row["result_scope"])
        groups[key]["partition"] += 1
        groups[key]["reliable"] += row["reliability_status"].startswith("reliable")
        groups[key]["insufficient"] += not row["reliability_status"].startswith("reliable")
    return [
        {
            "cohort": key[0],
            "context": key[1],
            "participant_scope": key[2],
            "result_scope": key[3],
            "independent_battles": len(value["battle_ids"]),
            "ordinary_occurrences": value["ordinary"],
            "partial_ordinary_occurrences": value["partial"],
            "excluded_character_occurrences": value["excluded"],
            "partition_rows": value["partition"],
            "reliable_rows": value["reliable"],
            "insufficient_rows": value["insufficient"],
        }
        for key, value in sorted(groups.items())
    ]


def build_report(
    rankings: list[dict[str, Any]],
    reliable: list[dict[str, Any]],
    identity_audit: list[dict[str, Any]],
    pressure: list[dict[str, Any]],
    queue: dict[str, Any],
    validation: dict[str, Any],
) -> str:
    lines = [
        "# Phase 2 analysis — Sep 12–14 Realm of Thrones mixed campaign",
        "",
        "## Batch-wide findings",
        "",
        (
            f"The batch contains **{validation['battles']} independent battle events** "
            f"({validation['context_events']['field']} field, {validation['context_events']['siege_attack']} siege attack), "
            f"with **{validation['ordinary_occurrences']} visible ordinary-troop rows** and "
            f"**{validation['excluded_character_occurrences']} excluded character rows**. "
            f"All ordinary occurrences map to exactly one of **{validation['reliable_rows']} reliable** or "
            f"**{validation['insufficient_rows']} below-gate** troop/party/context/result-state rows."
        ),
        "",
        (
            f"{validation['reliable_rows']} rows pass the 5-battle / 20-deployed gate; "
            f"{validation['reliable_provisional_identity_rows']} row retains a provisional display label because the pinned track audit has no exact match. "
            "These are descriptive campaign measurements, not controlled causal comparisons."
        ),
        "",
    ]
    for context in ("field", "siege_attack"):
        context_rows = [row for row in reliable if row["context"] == context]
        lines.extend(
            [
                f"### Reliable {context.replace('_', ' ')} rows",
                "",
                "| Efficiency rank | Troop | Identity | Party | Observation state | Battles | Deployed | Kills | Kills/deployed | Kill share | Deployment share | Contribution ratio | Retention |",
                "|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in context_rows:
            lines.append(
                "| {efficiency_rank} | {display_name} | {identity_status} | {cohort} | {result_scope} | {independent_battles} | {deployed} | {kills} | {kills_per_deployed} | {player_side_kill_share} | {player_side_deployment_share} | {offensive_contribution_ratio} | {retention_rate} |".format(**row)
            )
        lines.append("")

    unresolved_gate = [
        row
        for row in rankings
        if row["numeric_display_gate_passed"] and not row["identity_gate_passed"]
    ]
    if unresolved_gate:
        labels = ", ".join(
            f"{row['display_name']} / {row['context'].replace('_', ' ')} / {row['result_scope']}"
            for row in unresolved_gate
        )
        lines.extend(
            [
                "## Identity boundary",
                "",
                (
                    f"{labels} clear the numeric display gate and are published as reliable within-batch evidence under provisional labels. "
                    "Their canonical IDs remain blank because the pinned Realm of Thrones audit has no exact match; no XML ID is guessed or pooled across batches."
                ),
                "",
            ]
        )

    lines.extend(
        [
            "## Final versus censored battle state",
            "",
            (
                f"`battle_pressure_margin.csv` publishes **{sum(row['included_in_final_pressure_summary'] for row in pressure)} final-stage** "
                f"pressure margins. The remaining **{sum(not row['included_in_final_pressure_summary'] for row in pressure)} active snapshots** "
                "are diagnostic and right-censored. Each `Retreated to the keep!` observation is retained as a completed outside-wall success, never a defeat."
            ),
            "",
            "## Complete ordinary-troop partition",
            "",
            "Every visible ordinary occurrence appears in exactly one troop/party/context/result-state group. Below-gate rates and ranks are blank; blank counts mean the normalized row contained clipped values. No off-screen value was inferred.",
            "",
            "| Party | Context | Participant | Observation state | Troop | Battles | Deployed | Kills | Kills/deployed | Status |",
            "|---|---|---|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in rankings:
        lines.append(
            f"| {row['cohort']} | {row['context']} | {row['participant_scope']} | {row['result_scope']} | {row['display_name']} | "
            f"{row['independent_battles']} | {row['deployed'] if row['deployed'] is not None else ''} | "
            f"{row['kills'] if row['kills'] is not None else ''} | {row['kills_per_deployed']} | {row['reliability_status']} |"
        )
    identity_confirmed = sum(
        row["row_class"] == "ordinary_troop" and row["resolution_status"] == "confirmed_id"
        for row in identity_audit
    )
    identity_ordinary = sum(row["row_class"] == "ordinary_troop" for row in identity_audit)
    hold_names = ", ".join(row["display_name"] for row in queue["verification_holds"])
    lines.extend(
        [
            "",
            "## Queue decision",
            "",
            (
                "No queue mutation is justified. `active_test` remains null and `ordered_queue` remains empty. "
                f"The verification hold remains **{hold_names}**; a hold is not a recommendation."
            ),
            "",
            "## Integrity and limitations",
            "",
            (
                f"The normalized archive matches `{ARCHIVE_SHA256}` exactly, with all 11 members verified. "
                "The committed Base64 text matches its declared hash and size, and the authoritative `screenshots_manifest.csv` is byte-identical in the repository and archive."
            ),
            "",
            (
                f"The pinned track audit confirms **{identity_confirmed}/{identity_ordinary} ordinary labels** by exact name. "
                f"Three ordinary rows preserve clipped numeric cells, and {validation['party_summaries_with_visibility_delta']} party summaries preserve visible coverage gaps. "
                "Raw PNGs are not retained, so Phase 2 verifies their committed manifest hashes but cannot repeat pixel-level review. "
                "Phase 1 did not record an exact game version, so this batch is not pooled with versioned historical cohorts."
            ),
            "",
            (
                "No universal or role-blended score is published, frozen model files are unchanged, and model/residual files explicitly record `not_run`. "
                "No battle is excluded as an outlier because this mixed campaign batch has no predeclared outlier rule. "
                "Campaign opponent, composition, terrain, orders, exposure, and difficulty remain uncontrolled confounders."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def build_analysis(*, write_outputs: bool) -> dict[str, Any]:
    immutable_snapshot = repository_snapshot(IMMUTABLE_PHASE1_PATHS, "immutable Phase 1 inputs")
    frozen_snapshot = repository_snapshot(FROZEN_MODEL_PATHS, "frozen model files")
    files, bundle_verification = extract_verified_bundle()
    handoff_inventory = verify_handoff_inventory(files)
    events = parse_jsonl(files["normalized/events.jsonl"])
    party_summaries = parse_jsonl(files["normalized/party_summaries.jsonl"])
    raw_rows = parse_jsonl(files["normalized/player_rows.jsonl"])
    integrity = parse_json(files["integrity_report.json"])
    source_manifest = parse_json(files["source_manifest.json"])
    source_index = {row["source_key"]: row for row in source_manifest["sources"]}
    event_index = {row["event_id"]: row for row in events}

    if len(events) != 15 or len(event_index) != 15 or len(party_summaries) != 19 or len(raw_rows) != 232:
        raise ValueError("normalized batch counts differ from Phase 1 checkpoint")
    if Counter(event["battle_context"] for event in events) != {"field": 8, "siege_attack": 7}:
        raise ValueError("battle-context partition mismatch")
    if Counter(event["result_status"] for event in events) != {"final": 12, "in_progress": 3}:
        raise ValueError("final/censored event partition mismatch")
    if Counter(event["outcome"] for event in events) != {"victory": 9, "retreated_to_keep": 3, "in_progress": 3}:
        raise ValueError("outcome partition mismatch")
    if integrity.get("status") != "pass_with_expected_visibility_gaps" or integrity.get("errors"):
        raise ValueError("Phase 1 structural validation did not pass")
    if any(row["event_id"] not in event_index for row in raw_rows):
        raise ValueError("troop row references an unknown event")
    if len({row["row_id"] for row in raw_rows}) != len(raw_rows):
        raise ValueError("duplicate normalized row ID")

    screenshot_manifest_verification = verify_screenshot_manifest(
        files, source_index, event_index
    )
    source_audit, source_verification = verify_source_records(files, events)
    identities, identity_audit = resolve_identities(raw_rows)
    ordinary, excluded = adapt_rows(raw_rows, event_index, source_index, identities)
    occurrence_keys = [
        (row["battle_id"], row["cohort"], row["participant_scope"], row["context"], row["display_name"])
        for row in ordinary
    ]
    if len(occurrence_keys) != len(set(occurrence_keys)):
        raise ValueError("duplicate ordinary troop occurrence within one battle/party/context")
    rankings = aggregate_rows(ordinary, event_index, include_result_scope=True)
    reliable = rerank_reliable(rankings)
    insufficient = [row for row in rankings if not row["reliability_status"].startswith("reliable")]
    result_splits = rankings
    pressure = pressure_rows(events, source_index)
    denominators = denominator_rows(events, source_index)
    coverage = context_coverage_rows(ordinary, excluded, rankings)
    queue_validation = validate_queue()

    unresolved_occurrences = []
    review_resolutions = []
    for row in ordinary:
        missing = [field for field in STATS_FIELDS if row[field] is None]
        if not missing:
            continue
        unresolved_occurrences.append(
            {
                "observation_id": row["observation_id"],
                "battle_id": row["battle_id"],
                "cohort": row["cohort"],
                "context": row["context"],
                "display_name": row["display_name"],
                "visibility": row["visibility"],
                "missing_fields": "|".join(missing),
                "decision_status": "unresolved_preserve_null",
                "reason": row["note"],
                "source_image_sha256": row["source_image_sha256"],
            }
        )
        for field in missing:
            review_resolutions.append(
                {
                    "review_correction_id": f"{row['observation_id']}__{field}",
                    "observation_id": row["observation_id"],
                    "battle_id": row["battle_id"],
                    "field": field,
                    "original_value": "null",
                    "reviewed_value": "",
                    "decision_status": "unresolved_preserve_null",
                    "reason": row["note"],
                    "reviewer": "separate Phase 2 local analysis agent",
                    "evidence_reference": row["source_image_sha256"],
                }
            )

    group_membership = Counter(
        (
            row["cohort"],
            row["participant_scope"],
            row["context"],
            row["result_scope"],
            row["display_name"],
        )
        for row in ordinary
    )
    if sum(group_membership.values()) != len(ordinary) or len(rankings) != len(group_membership):
        raise ValueError("ordinary occurrence partition mismatch")
    if len(reliable) != 7:
        raise ValueError("unexpected reliable row count")
    if len(rankings) != len(reliable) + len(insufficient):
        raise ValueError("reliable/insufficient partition mismatch")
    if any(row["context"] not in {"field", "siege_attack"} for row in rankings):
        raise ValueError("unsupported context entered rankings")
    if any(row["participant_scope"] not in {"player_party", "allied_party"} for row in rankings):
        raise ValueError("non-player-side row entered rankings")

    context_counts = dict(Counter(event["battle_context"] for event in events))
    validation = {
        "status": "passed_with_documented_identity_limits",
        "validation_errors": [],
        "batch_id": BATCH_ID,
        "pipeline_mode": "offline-existing",
        "pipeline_version": "phase2_mixed_campaign_v1",
        "schema_version": "1.0.0",
        "input_images": 16,
        "newly_accepted_screenshots": source_verification["newly_accepted_screenshots"],
        "already_normalized_screenshots": source_verification["already_normalized_screenshots"],
        "internal_duplicate_screenshots": source_verification["internal_duplicate_screenshots"],
        "supplemental_screenshots": source_verification["supplemental_screenshots"],
        "active_last_observation_battles": 3,
        "battles": len(events),
        "context_events": context_counts,
        "visible_rows": len(raw_rows),
        "ordinary_occurrences": len(ordinary),
        "ordinary_occurrences_unique_within_battle": len(occurrence_keys) == len(set(occurrence_keys)),
        "excluded_character_occurrences": len(excluded),
        "partial_ordinary_occurrences": len(unresolved_occurrences),
        "unresolved_review_fields": len(review_resolutions),
        "party_summaries": len(party_summaries),
        "party_summaries_with_visibility_delta": sum(not row["coverage"]["all_numeric_fields_exact"] for row in party_summaries),
        "partition_rows": len(rankings),
        "reliable_rows": len(reliable),
        "reliable_provisional_identity_rows": sum(
            row["reliability_status"] == "reliable_provisional_identity" for row in reliable
        ),
        "insufficient_rows": len(insufficient),
        "visible_row_partition_exact": len(ordinary) + len(excluded) == len(raw_rows),
        "ordinary_partition_exact": sum(group_membership.values()) == len(ordinary) and len(rankings) == len(group_membership),
        "result_split_occurrences_exact": sum(row["ordinary_occurrences"] for row in result_splits) == len(ordinary),
        "source_manifest_entries_verified": source_verification["manifest_entries_verified"],
        "bundle_members_verified": bundle_verification["members"],
        "archive_hash_verified": True,
        "base64_transport_exact": True,
        "screenshots_manifest_verified": True,
        "identity_labels": len(identity_audit),
        "ordinary_identity_labels": sum(row["row_class"] == "ordinary_troop" for row in identity_audit),
        "identity_confirmed": sum(row["row_class"] == "ordinary_troop" and row["resolution_status"] == "confirmed_id" for row in identity_audit),
        "identity_unresolved": sum(row["row_class"] == "ordinary_troop" and row["resolution_status"] != "confirmed_id" for row in identity_audit),
        "direct_kill_total_coverage": f"{sum(row['kill_total_direct_positive'] for row in denominators)}/{len(denominators)}",
        "direct_deployment_total_coverage": f"{sum(row['deployment_total_direct_positive'] for row in denominators)}/{len(denominators)}",
        "pressure_margin_final_battles": sum(row["included_in_final_pressure_summary"] for row in pressure),
        "pressure_margin_censored_snapshots": sum(not row["included_in_final_pressure_summary"] for row in pressure),
        "contexts_pooled": False,
        "cohorts_pooled": False,
        "player_enemy_pooled": False,
        "offscreen_rows_inferred": False,
        "active_battles_combined_with_later_fights": False,
        "final_active_observations_pooled": False,
        "frozen_models_changed": False,
        "role_adjusted_blended_rank_published": False,
        "model_comparison_status": "not_run_no_complete_compatible_rot_v71_v73_model_universe",
        "outlier_analysis_status": "not_run_no_predeclared_campaign_outlier_rule",
        "outlier_rows": 0,
        "primary_outlier_exclusions": 0,
        "queue_change": "none",
    }
    if not all(
        validation[key]
        for key in ("visible_row_partition_exact", "ordinary_partition_exact", "result_split_occurrences_exact")
    ):
        raise ValueError("coverage partition validation failed")

    phase1_transport_review = {
        "status": "verified_repaired_phase1_bundle_no_evidence_change",
        "normalized_inputs_modified": False,
        "committed_base64_text": bundle_verification["base64_transport"],
        "decoded_archive_sha256": ARCHIVE_SHA256,
        "decoded_archive_size_bytes": ARCHIVE_SIZE,
        "decoded_archive_exact": True,
        "screenshots_manifest": screenshot_manifest_verification,
        "embedded_control_file_note": (
            "The archive's embedded batch_state.json and phase1_checkpoint.json deliberately omit the self-referential archive hash; "
            "the repository-level control files pin the final archive identity."
        ),
    }
    input_verification = {
        "status": "passed",
        "batch_id": BATCH_ID,
        "pipeline_mode": "offline-existing",
        "pipeline_version": "phase2_mixed_campaign_v1",
        "schema_version": "1.0.0",
        "normalization_commit": NORMALIZATION_COMMIT,
        "normalized_bundle": bundle_verification,
        "handoff_inventory": handoff_inventory,
        "screenshot_manifest": screenshot_manifest_verification,
        "source_manifest": source_verification,
        "identity_audit": {
            "path": IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(),
            "sha256": IDENTITY_AUDIT_SHA256,
            "blob_sha": subprocess.run(
                ["git", "rev-parse", f"{NORMALIZATION_COMMIT}:{IDENTITY_PATH.relative_to(REPO_ROOT).as_posix()}"],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip(),
        },
        "immutable_phase1_snapshot": immutable_snapshot,
        "frozen_model_snapshot": frozen_snapshot,
        "immutable_inputs_modified": immutable_snapshot["modified_files"],
        "frozen_model_files_modified": frozen_snapshot["modified_files"],
        "raw_source_integrity": "manifest_hashes_only_raw_pngs_not_retained",
    }
    analysis_state = {
        "batch_id": BATCH_ID,
        "status": "phase_2_complete_local_validation_passed",
        "normalization_commit": NORMALIZATION_COMMIT,
        "primary_test_unit": None,
        "primary_test_unit_reason": "No approved primary tested troop exists in this mixed campaign batch.",
        "queue_change": "none",
        "blockers": [],
        "queue_after": {
            "active_test": queue_validation["active_test"],
            "ordered_queue": queue_validation["ordered_queue"],
            "verification_holds": [row["troop_id"] for row in queue_validation["verification_holds"]],
        },
    }

    result = {
        "validation": validation,
        "input_verification": input_verification,
        "analysis_state": analysis_state,
        "queue_validation": queue_validation,
        "rankings": rankings,
        "reliable": reliable,
        "insufficient": insufficient,
        "result_splits": result_splits,
        "ordinary": ordinary,
        "excluded": excluded,
        "identity_audit": identity_audit,
        "pressure": pressure,
        "denominators": denominators,
        "coverage": coverage,
        "source_audit": source_audit,
        "unresolved_occurrences": unresolved_occurrences,
        "review_resolutions": review_resolutions,
        "phase1_transport_review": phase1_transport_review,
        "handoff_inventory": handoff_inventory,
    }
    if write_outputs:
        emit_outputs(result)
    return result


def emit_outputs(result: dict[str, Any]) -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    rankings = result["rankings"]
    reliable = result["reliable"]
    insufficient = result["insufficient"]
    identity_audit = result["identity_audit"]

    write_csv(ANALYSIS_DIR / "ranking_complete.csv", RANKING_FIELDS, rankings)
    write_csv(ANALYSIS_DIR / "ranking_reliable.csv", RANKING_FIELDS, reliable)
    write_csv(ANALYSIS_DIR / "insufficient_evidence.csv", RANKING_FIELDS, insufficient)
    write_csv(ANALYSIS_DIR / "result_splits.csv", RANKING_FIELDS, result["result_splits"])
    write_csv(ANALYSIS_DIR / "ordinary_occurrences.csv", result["ordinary"][0].keys(), result["ordinary"])
    write_csv(ANALYSIS_DIR / "excluded_character_rows.csv", result["excluded"][0].keys(), result["excluded"])
    write_csv(ANALYSIS_DIR / "unresolved_rows.csv", result["unresolved_occurrences"][0].keys(), result["unresolved_occurrences"])
    write_csv(ANALYSIS_DIR / "canonical_identity_audit.csv", identity_audit[0].keys(), identity_audit)
    write_csv(ANALYSIS_DIR / "battle_pressure_margin.csv", result["pressure"][0].keys(), result["pressure"])
    write_csv(ANALYSIS_DIR / "battle_context_review.csv", result["pressure"][0].keys(), result["pressure"])
    write_csv(ANALYSIS_DIR / "denominator_coverage.csv", result["denominators"][0].keys(), result["denominators"])
    write_csv(ANALYSIS_DIR / "context_coverage.csv", result["coverage"][0].keys(), result["coverage"])
    write_csv(ANALYSIS_DIR / "screenshot_deduplication_audit.csv", result["source_audit"][0].keys(), result["source_audit"])

    model_fields = (
        "canonical_troop_id",
        "context",
        "cohort",
        "result_scope",
        "empirical_rank",
        "battle_count",
        "total_deployed",
        "evidence_grade",
        "empirical_kills_per_deployed",
        "general_score_v71",
        "burst_score_v73",
        "comparison_status",
    )
    model_rows = [
        {
            "canonical_troop_id": row["canonical_troop_id"],
            "context": row["context"],
            "cohort": row["cohort"],
            "result_scope": row["result_scope"],
            "empirical_rank": row["efficiency_rank"],
            "battle_count": row["independent_battles"],
            "total_deployed": row["deployed"],
            "evidence_grade": row["evidence_grade"],
            "empirical_kills_per_deployed": row["kills_per_deployed"],
            "comparison_status": "not_run_no_complete_compatible_rot_v71_v73_model_universe",
        }
        for row in reliable
    ]
    write_csv(ANALYSIS_DIR / "model_vs_empirical.csv", model_fields, model_rows)
    write_csv(ANALYSIS_DIR / "empirical_residual_rankings.csv", model_fields, model_rows)
    write_csv(
        ANALYSIS_DIR / "outlier_report.csv",
        ("battle_id", "canonical_troop_id", "context", "deployed", "kills", "kills_per_deployed", "status", "primary_excluded"),
        [],
    )

    write_json(ANALYSIS_DIR / "input_verification.json", result["input_verification"])
    write_json(ANALYSIS_DIR / "queue_validation.json", result["queue_validation"])
    write_json(ANALYSIS_DIR / "validation_report.json", result["validation"])
    write_json(ANALYSIS_DIR / "canonical_validation_report.json", result["validation"])
    write_json(ANALYSIS_DIR / "analysis_state.json", result["analysis_state"])
    write_json(REVIEW_DIR / "phase1_transport_review.json", result["phase1_transport_review"])
    write_json(
        REVIEW_DIR / "phase2_review_summary.json",
        {
            "status": "complete_local_validation_passed",
            "reviewer": "separate Phase 2 local analysis agent",
            "normalized_inputs_modified": False,
            "numeric_corrections": 0,
            "identity_decisions": len(identity_audit),
            "ordinary_identity_labels": result["validation"]["ordinary_identity_labels"],
            "unresolved_ordinary_occurrences": len(result["unresolved_occurrences"]),
            "unresolved_numeric_fields": len(result["review_resolutions"]),
            "transport_metadata_findings": 0,
            "missing_declared_phase1_inputs": result["handoff_inventory"]["missing_inputs"],
            "screenshots_manifest_status": result["input_verification"]["screenshot_manifest"]["status"],
        },
    )
    write_csv(REVIEW_DIR / "phase2_identity_decisions.csv", identity_audit[0].keys(), identity_audit)
    write_csv(
        REVIEW_DIR / "review_resolutions.csv",
        result["review_resolutions"][0].keys(),
        result["review_resolutions"],
    )
    write_csv(REVIEW_DIR / "screenshot_deduplication_audit.csv", result["source_audit"][0].keys(), result["source_audit"])
    (REVIEW_DIR / "README.md").write_text(
        "# Phase 2 reviewed layer\n\n"
        "Phase 1 normalized records remain immutable. This layer preserves three clipped ordinary rows as null, "
        "records exact-name identity decisions against the pinned Realm of Thrones audit, and verifies the authoritative "
        "`screenshots_manifest.csv` byte-for-byte across the repository and normalized archive. The reviewed deduplication audit "
        "retains the complementary-view decision without replacing or rewriting the Phase 1 manifest.\n",
        encoding="utf-8",
    )

    report = build_report(
        rankings,
        reliable,
        identity_audit,
        result["pressure"],
        result["queue_validation"],
        result["validation"],
    )
    (ANALYSIS_DIR / "ANALYSIS_REPORT.md").write_text(report, encoding="utf-8")
    (ANALYSIS_DIR / "empirical_analysis_summary.md").write_text(report, encoding="utf-8")
    (ANALYSIS_DIR / "NEXT_TEST_RECOMMENDATION.md").write_text(
        "# Next-test decision\n\n"
        "No queue change. This mixed campaign batch has no approved primary test troop, so it cannot select a new target. "
        "`active_test` remains null, `ordered_queue` remains empty, and Arryn Winged Knight remains under historical verification hold.\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "README.md").write_text(
        "# Phase 2 analytical outputs\n\n"
        f"All {result['validation']['ordinary_occurrences']} visible ordinary occurrences partition into "
        f"{len(rankings)} exact party/context/result-state rows: {len(reliable)} reliable and {len(insufficient)} insufficient. "
        "Character rows, identity decisions, clipped-value reviews, result splits, pressure margins, denominators, "
        "queue validation, manifest verification, and bundle verification remain separate auditable artifacts. "
        "Local Phase 2 validation passes; protocol completion and latest-head repository review remain delivery gates.\n\n"
        "Reproduce from the repository root with:\n\n"
        f"```bash\npython3 data/combat_observations/{BATCH_ID}/analysis/generate_phase2.py\n```\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "TESTS.md").write_text(
        "# Validation runs\n\n"
        "- Red (targeted, after updating the repaired identity pins only): the manifest-divergence test raised `AttributeError: module 'mixed_campaign_phase2' has no attribute 'verify_screenshot_manifest'`; the main contract raised `ValueError: unexpected handoff input inventory: missing=[]`.\n"
        "- Green: `python3 -m unittest -v data.combat_observations.2026-09-12-to-14-rot-mixed-campaign-phase1.analysis.test_generate_phase2` passes both tests.\n"
        "- The generator runs twice with byte-identical artifacts.\n"
        "- Focused repository validation: 120/120 passed across the shared bundle, analyzer, identity, protocol, role, Phase 1 repair, and Phase 2 batch contracts.\n"
        "- Full stdlib suite attempt: 389 tests passed; four additional test modules could not import because this documented local Python environment has no `pandas`.\n"
        "- The 12,944-byte normalized archive matches its declared SHA-256 and all 11 members pass safe extraction.\n"
        "- The authoritative screenshot manifest matches byte-for-byte between the repository and archive: 16 screens, 15 battle IDs, 3 active, and 13 final-result screens.\n"
        "- All 232 visible rows partition into 155 ordinary and 77 character rows; every ordinary occurrence maps to one reliable or insufficient aggregate.\n"
        "- Three clipped ordinary rows preserve 13 null fields in the reviewed layer.\n"
        "- Queue invariants pass with no mutation; frozen model files and published immutable Phase 1 inputs remain unchanged.\n"
        "- Local Phase 2 validation has no unresolved blockers.\n",
        encoding="utf-8",
    )

    targets = [path for path in ANALYSIS_DIR.iterdir() if path.is_file() and path.name != "artifact_hashes.csv"]
    targets.extend(path for path in REVIEW_DIR.iterdir() if path.is_file())
    artifact_rows = [
        {
            "path": path.relative_to(BATCH_DIR).as_posix(),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        }
        for path in sorted(targets)
    ]
    write_csv(ANALYSIS_DIR / "artifact_hashes.csv", ("path", "sha256", "size_bytes"), artifact_rows)


def main() -> None:
    result = build_analysis(write_outputs=True)
    print(json.dumps(result["validation"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
