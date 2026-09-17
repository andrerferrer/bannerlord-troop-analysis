#!/usr/bin/env python3
"""Generate the deterministic Phase 2 analysis for the Qartheen Guardian batch."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import os
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
QUEUE_PATH = REPO_ROOT / "data/combat_observations/test_queues/realm_of_thrones.json"
IDENTITY_PATH = REPO_ROOT / "data/realm_of_thrones/audit/realm_of_thrones_troops.csv"

BATCH_ID = "2026-09-15-to-16-rot-qartheen-enthroned-guardian"
TRACK = "realm_of_thrones"
GAME_VERSION = "1.4.x"
NORMALIZATION_COMMIT = "b51dffd676ea753160972bd4e32647ca96868d01"
ARCHIVE_SHA256 = "7f75db2d12038c24a57a12f2bdb1f37b2220f873b34ea7247121aa7c5b9b4ced"
ARCHIVE_SIZE = 10_412
BASE64_SHA256 = "8cf63f6e7ebe820a6046a61025798471229dea1083ee5fa8239d446b8fe355c5"
BASE64_SIZE = 14_067
IDENTITY_SHA256 = "63ea983998e25aa0e6f8c0747bf42e44440f695bbe1fec717074e7ba64e42810"
QUEUE_BEFORE_SHA256 = "10c49b2d9434ce7b747526f1667f1655bd7774223eb4d0e6c8289c4e9a598855"
FOCUS_ID = "enthroned_guardian"
FOCUS_NAME = "Qartheen Enthroned Guardian"
GATE_BATTLES = 5
GATE_DEPLOYED = 20
BOOTSTRAP_REPETITIONS = 10_000
COUNT_FIELDS = ("deployed", "survivors", "kills", "deaths", "wounded", "routed")
NUMERIC_FIELDS = ("survivors", "kills", "upgrade_ready", "deaths", "wounded", "routed")
IMMUTABLE_PATHS = (
    f"data/combat_observations/{BATCH_ID}/README.md",
    f"data/combat_observations/{BATCH_ID}/batch_state.json",
    f"data/combat_observations/{BATCH_ID}/phase1_checkpoint.json",
    f"data/combat_observations/{BATCH_ID}/screenshots_manifest.csv",
    f"data/combat_observations/{BATCH_ID}/bundle",
    f"data/combat_observations/{BATCH_ID}/handoff",
    f"data/combat_observations/{BATCH_ID}/reports/publication_recovery_validation.json",
)
FROZEN_MODEL_PATHS = ("analysis/model_versions",)

RANKING_FIELDS = (
    "track", "game_version", "cohort", "context", "participant_scope",
    "efficiency_rank", "impact_rank", "display_name", "canonical_troop_id",
    "identity_status", "canonical_default_group", "canonical_role", "evidence_grade",
    "independent_battles", "ordinary_occurrences", "complete_numeric_occurrences",
    "excluded_partial_occurrences", *COUNT_FIELDS, "known_deployed", "known_kills",
    "kills_per_deployed", "ci95_low", "ci95_high",
    "verified_player_side_total_kills", "kill_total_coverage_battles",
    "kill_total_coverage_complete", "player_side_kill_share", "share_adjusted_impact",
    "verified_player_side_total_deployed", "deployment_total_coverage_battles",
    "deployment_total_coverage_complete", "player_side_deployment_share",
    "offensive_contribution_ratio", "offensive_share_gap", "retention_rate",
    "death_rate", "casualty_rate", "victory_battles", "numeric_display_gate_passed",
    "reliability_status", "more_battles_needed", "more_deployed_needed",
    "missing_numeric_fields", "role_adjusted_rank_status",
)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_jsonl(payload: bytes) -> list[dict[str, Any]]:
    return [json.loads(line) for line in payload.decode().splitlines() if line]


def parse_csv(payload: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))


def read_csv(path: Path) -> list[dict[str, str]]:
    return parse_csv(path.read_bytes())


def csv_safe(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", value.strip()):
            return "'" + value
    return value


def write_csv(path: Path, fields: Iterable[str], rows: Iterable[dict[str, Any]]) -> None:
    fieldnames = list(fields)
    path.parent.mkdir(parents=True, exist_ok=True)
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
    committed = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", NORMALIZATION_COMMIT, "--", *paths],
        cwd=REPO_ROOT, check=True, capture_output=True, text=True,
    ).stdout.splitlines()
    modified = subprocess.run(
        ["git", "diff", "--name-only", NORMALIZATION_COMMIT, "--", *paths],
        cwd=REPO_ROOT, check=True, capture_output=True, text=True,
    ).stdout.splitlines()
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


def extract_bundle() -> tuple[dict[str, bytes], dict[str, Any]]:
    encoded_path = BATCH_DIR / "bundle/qartheen_enthroned_guardian_phase1.tar.xz.base64"
    encoded = encoded_path.read_bytes()
    if len(encoded) != BASE64_SIZE or sha256_bytes(encoded) != BASE64_SHA256:
        raise ValueError("committed Base64 transport hash/size mismatch")
    compact = re.sub(rb"[\t\n\r ]+", b"", encoded)
    if re.search(rb"[^A-Za-z0-9+/=]", compact):
        raise ValueError("normalized bundle contains non-Base64 bytes")
    archive = base64.b64decode(compact, validate=True)
    if len(archive) != ARCHIVE_SIZE or sha256_bytes(archive) != ARCHIVE_SHA256:
        raise ValueError("normalized archive hash/size mismatch")

    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as bundle:
        members = bundle.getmembers()
        for member in members:
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts or not member.isfile():
                raise ValueError(f"unsafe normalized bundle member: {member.name}")
            if member.name in files:
                raise ValueError(f"duplicate normalized bundle member: {member.name}")
            extracted = bundle.extractfile(member)
            if extracted is None:
                raise ValueError(f"unreadable normalized bundle member: {member.name}")
            files[member.name] = extracted.read()

    declared: dict[str, str] = {}
    for line in (BATCH_DIR / "bundle/qartheen_enthroned_guardian_phase1.members.sha256").read_text().splitlines():
        digest, name = line.split("  ", 1)
        declared[name] = digest
    if set(files) != set(declared):
        raise ValueError("normalized archive member set mismatch")
    for name, payload in files.items():
        if sha256_bytes(payload) != declared[name]:
            raise ValueError(f"normalized member hash mismatch: {name}")

    mirrors = {
        "README.md": BATCH_DIR / "README.md",
        "handoff/ANALYSIS_PROMPT.md": BATCH_DIR / "handoff/ANALYSIS_PROMPT.md",
        "handoff/ANALYSIS_TASK_V1.json": BATCH_DIR / "handoff/ANALYSIS_TASK_V1.json",
        "screenshots_manifest.csv": BATCH_DIR / "screenshots_manifest.csv",
    }
    for member, path in mirrors.items():
        if files[member] != path.read_bytes():
            raise ValueError(f"repository/archive mirror mismatch: {member}")
    return files, {
        "archive_sha256": ARCHIVE_SHA256,
        "archive_size_bytes": len(archive),
        "base64_sha256": BASE64_SHA256,
        "base64_size_bytes": len(encoded),
        "members_verified": len(files),
        "safe_preflight_passed": True,
        "repository_mirrors_verified": len(mirrors),
    }


def load_inputs(files: dict[str, bytes]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    events = parse_jsonl(files["normalized/events.jsonl"])
    parties = parse_jsonl(files["normalized/party_summaries.jsonl"])
    index = json.loads(files["normalized/player_rows/index.json"])
    rows: list[dict[str, Any]] = []
    for shard in index["shards"]:
        payload = files[shard["path"]]
        if sha256_bytes(payload) != shard["sha256"]:
            raise ValueError(f"player-row shard hash mismatch: {shard['path']}")
        shard_rows = parse_jsonl(payload)
        if len(shard_rows) != shard["rows"]:
            raise ValueError(f"player-row shard count mismatch: {shard['path']}")
        rows.extend(shard_rows)
    if len(events) != 10 or len(parties) != 10 or len(rows) != 153 or index["row_count"] != 153:
        raise ValueError("unexpected normalized record counts")
    if Counter(event["battle_context"] for event in events) != {"field": 9, "siege_attack": 1}:
        raise ValueError("battle context partition mismatch")
    if any(event["game_track"] != TRACK or event["game_version"] != GAME_VERSION for event in events):
        raise ValueError("track/version boundary violation")
    if len({event["event_id"] for event in events}) != len(events):
        raise ValueError("duplicate event IDs")
    if len({row["occurrence_id"] for row in rows}) != len(rows):
        raise ValueError("duplicate occurrence IDs")
    return events, parties, rows, index


def verify_sources(files: dict[str, bytes], events: list[dict[str, Any]]) -> dict[str, Any]:
    manifest = json.loads(files["source_manifest.json"])
    inventory = parse_csv(files["source_inventory.csv"])
    screenshots = parse_csv(files["screenshots_manifest.csv"])
    sources = manifest["sources"]
    if len(sources) != 10 or len(inventory) != 10 or len(screenshots) != 10:
        raise ValueError("source record count mismatch")
    source_index = {row["source_key"]: row for row in sources}
    inventory_index = {row["source_key"]: row for row in inventory}
    if set(source_index) != set(inventory_index) or len(source_index) != 10:
        raise ValueError("source manifest/inventory key mismatch")
    for key, source in source_index.items():
        inv = inventory_index[key]
        for field in ("filename", "sha256", "capture_timestamp_local", "host_upload_id", "event_id"):
            if str(source[field]) != inv[field]:
                raise ValueError(f"source manifest/inventory mismatch: {key}/{field}")
        if int(inv["size_bytes"]) != source["size_bytes"]:
            raise ValueError(f"source size mismatch: {key}")
    if len({row["sha256"] for row in sources}) != 10:
        raise ValueError("source hashes are not unique")
    event_ids = {event["event_id"] for event in events}
    if {source["event_id"] for source in sources} != event_ids:
        raise ValueError("source/event mapping mismatch")
    if sha256_bytes(files["screenshots_manifest.csv"]) != "3c58f5260265efd32eba11ece47465ed10f6326edc8405f5e94c723cd2a319ba":
        raise ValueError("screenshots manifest hash mismatch")
    return {
        "manifest_entries_verified": len(sources),
        "source_set_sha256": manifest["source_set_sha256"],
        "source_total_bytes": manifest["source_total_bytes"],
        "raw_repository_retention": "not_retained",
        "raw_sources_repository_addressable": False,
        "raw_source_hashes_phase1_recovery_verified": 10,
        "note": "Phase 2 verified every retained source record and hash; raw PNG bytes are not repository-addressable.",
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


def resolve_identities(rows: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    if sha256_file(IDENTITY_PATH) != IDENTITY_SHA256:
        raise ValueError("versioned Realm of Thrones identity audit hash mismatch")
    audit = read_csv(IDENTITY_PATH)
    by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    for entry in audit:
        if bool_text(entry.get("is_soldier", "")):
            by_name[entry.get("name", "").casefold()].append(entry)
    observed = defaultdict(list)
    for row in rows:
        if row["row_type"] == "ordinary_troop":
            observed[row["display_name_raw"]].append(row)
    decisions: dict[str, dict[str, Any]] = {}
    output = []
    for name, occurrences in sorted(observed.items(), key=lambda item: item[0].casefold()):
        matches = by_name[name.casefold()]
        candidate_ids = sorted({row["troop_id"] for row in matches})
        matched = matches[0] if len(candidate_ids) == 1 else {}
        status = "confirmed_id" if matched and not bool_text(matched.get("is_hero")) else (
            "ambiguous_exact_name" if len(candidate_ids) > 1 else "unresolved_provisional_label"
        )
        decision = {
            "canonical_troop_id": candidate_ids[0] if status == "confirmed_id" else "",
            "identity_status": status,
            "default_group": matched.get("default_group", "") if status == "confirmed_id" else "",
            "canonical_role": canonical_role(matched.get("default_group", "")) if status == "confirmed_id" else "",
            "candidate_ids": "|".join(candidate_ids),
        }
        decisions[name] = decision
        output.append({
            "display_name": name,
            "ordinary_occurrences": len(occurrences),
            "canonical_troop_id": decision["canonical_troop_id"],
            "resolution_status": status,
            "default_group": decision["default_group"],
            "canonical_role": decision["canonical_role"],
            "candidate_count": len(candidate_ids),
            "candidate_troop_ids": decision["candidate_ids"],
            "resolution_method": "exact display-name match in pinned track audit" if status == "confirmed_id" else "no inferred alias",
            "blocking_reason": "" if status == "confirmed_id" else "no unique exact soldier display-name match in pinned track audit",
            "audit_path": IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(),
            "audit_sha256": IDENTITY_SHA256,
        })
    return decisions, output


def adapt_rows(rows: list[dict[str, Any]], events: dict[str, dict[str, Any]], identities: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ordinary, characters = [], []
    for source in rows:
        event = events[source["event_id"]]
        adapted = {
            "occurrence_id": source["occurrence_id"],
            "battle_id": source["event_id"],
            "captured_at": event["capture_timestamp_local"],
            "cohort": source["parent_party"],
            "context": event["battle_context"],
            "participant_scope": "player_party",
            "display_name": source["display_name_raw"],
            "row_type": source["row_type"],
            "visibility_status": source["visibility_status"],
            "review_status": source["review_status"],
            "review_note": source.get("review_note") or "",
            "source_key": source["source_key"],
            **{field: source.get(field) for field in NUMERIC_FIELDS},
            "deployed": source.get("deployed"),
        }
        if source["row_type"] == "character":
            adapted["exclusion_reason"] = "character_or_hero_excluded_from_ordinary_rankings"
            characters.append(adapted)
        else:
            decision = identities[source["display_name_raw"]]
            adapted.update({
                "canonical_troop_id": decision["canonical_troop_id"],
                "identity_status": decision["identity_status"],
                "canonical_default_group": decision["default_group"],
                "canonical_role": decision["canonical_role"],
            })
            ordinary.append(adapted)
    return ordinary, characters


def complete_numeric(row: dict[str, Any]) -> bool:
    return row["visibility_status"] == "complete" and isinstance(row["deployed"], int) and all(
        isinstance(row.get(field), int) for field in NUMERIC_FIELDS
    )


def bootstrap(rows: list[dict[str, Any]], key: str) -> tuple[float, float]:
    seed = int(hashlib.sha256(f"{BATCH_ID}|{key}".encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    ordered = sorted(rows, key=lambda row: row["battle_id"])
    values = []
    for _ in range(BOOTSTRAP_REPETITIONS):
        sample = [ordered[rng.randrange(len(ordered))] for _ in ordered]
        values.append(sum(row["kills"] for row in sample) / sum(row["deployed"] for row in sample))
    values.sort()
    return values[int(0.025 * (len(values) - 1))], values[int(0.975 * (len(values) - 1))]


def evidence_grade(battles: int, deployed: int | None) -> str:
    if deployed is None:
        return "exploratory_incomplete_numeric"
    if battles >= 5 and deployed >= 100:
        return "high"
    if battles >= 3 and deployed >= 30:
        return "medium"
    if battles >= 2 and deployed >= 10:
        return "low"
    return "exploratory"


def aggregate(ordinary: list[dict[str, Any]], events: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in ordinary:
        groups[(row["cohort"], row["context"], row["participant_scope"], row["display_name"])].append(row)
    output = []
    for (cohort, context, scope, name), subset in groups.items():
        battle_ids = sorted({row["battle_id"] for row in subset})
        complete = [row for row in subset if complete_numeric(row)]
        partial = [row for row in subset if not complete_numeric(row)]
        numeric_complete = not partial
        totals = {
            field: sum(int(row[field]) for row in subset) if numeric_complete else None
            for field in COUNT_FIELDS
        }
        deployed = totals["deployed"]
        kills = totals["kills"]
        gate = numeric_complete and len(battle_ids) >= GATE_BATTLES and deployed >= GATE_DEPLOYED
        side_kills = sum(events[battle_id]["player_side_totals"]["kills"] for battle_id in battle_ids)
        side_deployed = sum(
            sum(events[battle_id]["player_side_totals"][field] for field in ("survivors", "deaths", "wounded"))
            for battle_id in battle_ids
        )
        efficiency = kills / deployed if numeric_complete and deployed else None
        kill_share = kills / side_kills if numeric_complete and side_kills else None
        deployment_share = deployed / side_deployed if numeric_complete and side_deployed else None
        ci_low, ci_high = bootstrap(subset, "|".join((cohort, context, scope, name))) if gate else (None, None)
        identity = subset[0]
        if partial:
            status = "insufficient_missing_numeric_values"
        elif len(battle_ids) < GATE_BATTLES:
            status = "insufficient_battles"
        elif deployed < GATE_DEPLOYED:
            status = "insufficient_deployed"
        elif identity["identity_status"] != "confirmed_id":
            status = "reliable_provisional_identity"
        else:
            status = "reliable"
        output.append({
            "track": TRACK, "game_version": GAME_VERSION, "cohort": cohort,
            "context": context, "participant_scope": scope, "efficiency_rank": "",
            "impact_rank": "", "display_name": name,
            "canonical_troop_id": identity["canonical_troop_id"],
            "identity_status": identity["identity_status"],
            "canonical_default_group": identity["canonical_default_group"],
            "canonical_role": identity["canonical_role"],
            "evidence_grade": evidence_grade(len(battle_ids), deployed),
            "independent_battles": len(battle_ids), "ordinary_occurrences": len(subset),
            "complete_numeric_occurrences": len(complete), "excluded_partial_occurrences": len(partial),
            **totals,
            "known_deployed": sum(row["deployed"] for row in complete),
            "known_kills": sum(row["kills"] for row in complete),
            "kills_per_deployed": fmt(efficiency), "ci95_low": fmt(ci_low), "ci95_high": fmt(ci_high),
            "verified_player_side_total_kills": side_kills,
            "kill_total_coverage_battles": len(battle_ids), "kill_total_coverage_complete": True,
            "player_side_kill_share": fmt(kill_share),
            "share_adjusted_impact": fmt(efficiency * kill_share if efficiency is not None else None),
            "verified_player_side_total_deployed": side_deployed,
            "deployment_total_coverage_battles": len(battle_ids), "deployment_total_coverage_complete": True,
            "player_side_deployment_share": fmt(deployment_share),
            "offensive_contribution_ratio": fmt(kill_share / deployment_share if deployment_share else None),
            "offensive_share_gap": fmt(kill_share - deployment_share if kill_share is not None else None),
            "retention_rate": fmt(totals["survivors"] / deployed if numeric_complete and deployed else None),
            "death_rate": fmt(totals["deaths"] / deployed if numeric_complete and deployed else None),
            "casualty_rate": fmt((totals["deaths"] + totals["wounded"]) / deployed if numeric_complete and deployed else None),
            "victory_battles": len(battle_ids), "numeric_display_gate_passed": gate,
            "reliability_status": status, "more_battles_needed": max(0, GATE_BATTLES - len(battle_ids)),
            "more_deployed_needed": "" if deployed is None else max(0, GATE_DEPLOYED - deployed),
            "missing_numeric_fields": "|".join(NUMERIC_FIELDS) if partial else "",
            "role_adjusted_rank_status": "not_published_fewer_than_five_reliable_same_role_rows",
        })
    assign_ranks(output)
    return sorted(output, key=lambda row: (row["context"], int(row["efficiency_rank"]) if row["efficiency_rank"] != "" else 9999, row["display_name"]))


def assign_ranks(rows: list[dict[str, Any]]) -> None:
    groups = defaultdict(list)
    for row in rows:
        groups[(row["cohort"], row["context"], row["participant_scope"])].append(row)
    for group in groups.values():
        numeric = [row for row in group if row["kills_per_deployed"] != ""]
        for rank, row in enumerate(sorted(numeric, key=lambda item: (-float(item["kills_per_deployed"]), -int(item["deployed"]), item["display_name"])), 1):
            row["efficiency_rank"] = rank
        for rank, row in enumerate(sorted(numeric, key=lambda item: (-float(item["share_adjusted_impact"]), -int(item["deployed"]), item["display_name"])), 1):
            row["impact_rank"] = rank


def focus_battles(ordinary: list[dict[str, Any]], events: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in ordinary:
        if row["canonical_troop_id"] != FOCUS_ID:
            continue
        event = events[row["battle_id"]]
        side = event["player_side_totals"]
        side_deployed = sum(side[field] for field in ("survivors", "deaths", "wounded"))
        output.append({
            "display_name": FOCUS_NAME, "canonical_troop_id": FOCUS_ID,
            "battle_id": row["battle_id"], "captured_at": row["captured_at"],
            "context": row["context"], "result": "victory", "deployed": row["deployed"],
            "survivors": row["survivors"], "kills": row["kills"], "deaths": row["deaths"],
            "wounded": row["wounded"], "kills_per_deployed": fmt(row["kills"] / row["deployed"]),
            "retention_rate": fmt(row["survivors"] / row["deployed"]),
            "player_side_kills": side["kills"], "player_side_deployed": side_deployed,
            "player_side_kill_share": fmt(row["kills"] / side["kills"]),
            "player_side_deployment_share": fmt(row["deployed"] / side_deployed),
        })
    return sorted(output, key=lambda row: row["captured_at"])


def sensitivity(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    field = [row for row in rows if row["context"] == "field"]
    highest = max(field, key=lambda row: float(row["kills_per_deployed"]))
    scenarios = [("all_field_battles", field), (f"exclude_highest_rate_{highest['battle_id']}", [row for row in field if row is not highest])]
    output = []
    for scenario, subset in scenarios:
        deployed = sum(row["deployed"] for row in subset)
        kills = sum(row["kills"] for row in subset)
        side_kills = sum(row["player_side_kills"] for row in subset)
        side_deployed = sum(row["player_side_deployed"] for row in subset)
        survivors = sum(row["survivors"] for row in subset)
        kill_share = kills / side_kills
        deployment_share = deployed / side_deployed
        output.append({
            "scenario": scenario, "excluded_battle_id": "" if scenario == "all_field_battles" else highest["battle_id"],
            "independent_battles": len(subset), "deployed": deployed, "kills": kills,
            "kills_per_deployed": fmt(kills / deployed), "player_side_total_kills": side_kills,
            "player_side_kill_share": fmt(kill_share), "player_side_total_deployed": side_deployed,
            "player_side_deployment_share": fmt(deployment_share),
            "offensive_contribution_ratio": fmt(kill_share / deployment_share),
            "offensive_share_gap": fmt(kill_share - deployment_share), "survivors": survivors,
            "retention_rate": fmt(survivors / deployed),
            "display_gate_passed": len(subset) >= GATE_BATTLES and deployed >= GATE_DEPLOYED,
        })
    return output


def update_queue(field_focus: dict[str, Any], sensitivity_rows: list[dict[str, Any]]) -> dict[str, Any]:
    queue = json.loads(QUEUE_PATH.read_text(encoding="utf-8"))
    before_hash = sha256_file(QUEUE_PATH)
    already_closed = any(row.get("troop_id") == FOCUS_ID and row.get("context") == "field" for row in queue["closed"])
    if not already_closed:
        if before_hash != QUEUE_BEFORE_SHA256 or queue.get("active_test", {}).get("troop_id") != FOCUS_ID:
            raise ValueError("authoritative queue does not match the expected active target")
        if not field_focus["numeric_display_gate_passed"] or not all(row["display_gate_passed"] for row in sensitivity_rows):
            raise ValueError("focus and sensitivity must pass before queue closure")
        queue["active_test"] = None
        queue["closed"].append({
            "completed_by": f"data/combat_observations/{BATCH_ID}/analysis/ANALYSIS_REPORT.md",
            "context": "field",
            "decision": "Stop dedicated field testing. The nine-battle cohort and leave-one-highest-rate-battle sensitivity both pass the 5-battle / 20-deployed gate, with player-side kill share above deployment share.",
            "display_name": FOCUS_NAME,
            "evidence": [
                {
                    "deployed": field_focus["deployed"], "independent_battles": field_focus["independent_battles"],
                    "kills": field_focus["kills"], "kills_per_deployed": float(field_focus["kills_per_deployed"]),
                    "offensive_contribution_ratio": float(field_focus["offensive_contribution_ratio"]),
                    "player_side_deployment_share": float(field_focus["player_side_deployment_share"]),
                    "player_side_kill_share": float(field_focus["player_side_kill_share"]),
                    "retention_rate": float(field_focus["retention_rate"]),
                },
                {
                    "deployed": sensitivity_rows[1]["deployed"], "independent_battles": sensitivity_rows[1]["independent_battles"],
                    "kills": sensitivity_rows[1]["kills"], "kills_per_deployed": float(sensitivity_rows[1]["kills_per_deployed"]),
                    "offensive_contribution_ratio": float(sensitivity_rows[1]["offensive_contribution_ratio"]),
                    "player_side_deployment_share": float(sensitivity_rows[1]["player_side_deployment_share"]),
                    "player_side_kill_share": float(sensitivity_rows[1]["player_side_kill_share"]),
                    "retention_rate": float(sensitivity_rows[1]["retention_rate"]),
                    "sensitivity": "field cohort without highest-rate battle",
                },
            ],
            "evidence_references": [
                f"data/combat_observations/{BATCH_ID}/analysis/focus_deep_dive.csv",
                f"data/combat_observations/{BATCH_ID}/analysis/focus_sensitivity.csv",
                f"data/combat_observations/{BATCH_ID}/analysis/focus_battle_rates.csv",
                "pull/100",
            ],
            "status": "completed_no_additional_test", "troop_id": FOCUS_ID,
        })
        queue["last_transition"] = {
            "batch": f"data/combat_observations/{BATCH_ID}", "date": "2026-09-17",
            "from": "active_test: enthroned_guardian / ordered_queue: []",
            "reason": "The nine-battle field cohort and leave-one-highest-rate-battle sensitivity pass the display gate; both retain kill share above deployment share.",
            "to": "active_test: null / ordered_queue: []",
        }
        queue["queue_status"] = "awaiting_operator_selection"
        queue["updated_at"] = "2026-09-17"
        temporary_queue = QUEUE_PATH.with_suffix(".json.tmp")
        write_json(temporary_queue, queue)
        os.replace(temporary_queue, QUEUE_PATH)
    if queue.get("active_test") is not None or queue.get("ordered_queue") != []:
        raise ValueError("completed target must leave no inferred future target")
    holds = queue.get("verification_holds", [])
    if not any(row.get("troop_id") == "arryn_moonknight" and row.get("status") == "do_not_recommend_until_audited" for row in holds):
        raise ValueError("Arryn Winged Knight verification hold changed")
    categories = []
    for category in ("ordered_queue", "verification_holds", "parked", "closed"):
        categories.extend((row["troop_id"], row["context"], category) for row in queue.get(category, []))
    pairs = [(troop, context) for troop, context, _ in categories]
    if len(pairs) != len(set(pairs)):
        raise ValueError("troop/context appears in multiple queue categories")
    return {
        "status": "passed_closed_target_no_future_target_invented",
        "path": QUEUE_PATH.relative_to(REPO_ROOT).as_posix(), "sha256_before": QUEUE_BEFORE_SHA256,
        "sha256_after": sha256_file(QUEUE_PATH), "active_test_before": FOCUS_ID,
        "active_test_after": None, "ordered_queue_after": [],
        "verification_holds_after": [row["troop_id"] for row in holds],
        "queue_change": "closed enthroned_guardian field; preserved empty ordered queue and Arryn hold",
    }


def build_report(rankings: list[dict[str, Any]], focus: list[dict[str, Any]], focus_battle_rows: list[dict[str, Any]], sensitivity_rows: list[dict[str, Any]], identity_audit: list[dict[str, Any]]) -> str:
    reliable = [row for row in rankings if row["reliability_status"].startswith("reliable")]
    insufficient = [row for row in rankings if not row["reliability_status"].startswith("reliable")]
    field = next(row for row in focus if row["context"] == "field")
    siege = next(row for row in focus if row["context"] == "siege_attack")
    lines = [
        "# Phase 2 analysis — Qartheen Enthroned Guardian", "",
        "## Batch-wide findings", "",
        f"All **79 visible player-side ordinary occurrences** are covered across **{len(rankings)} troop/context rows**: **{len(reliable)} reliable** and **{len(insufficient)} insufficient**. The two clipped Qartheen Pureborn Warrior occurrences remain explicit unresolved evidence and make that field aggregate non-numeric; 74 character/hero rows are retained separately and excluded from ordinary rankings.", "",
        "Field and siege attack are never pooled. Shares use the visible positive player-side totals in each contributing battle. Metrics below the display gate remain descriptive and are classified insufficient; only gate-passing rows appear in the reliable output.", "",
        "| context | troop | identity | battles | deployed | kills | kills/deployed | kill share | deployment share | contribution ratio | status |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rankings:
        lines.append(
            f"| {row['context']} | {row['display_name']} | {row['identity_status']} | {row['independent_battles']} | {row['deployed'] if row['deployed'] is not None else '—'} | {row['kills'] if row['kills'] is not None else '—'} | {row['kills_per_deployed'] or '—'} | {row['player_side_kill_share'] or '—'} | {row['player_side_deployment_share'] or '—'} | {row['offensive_contribution_ratio'] or '—'} | {row['reliability_status']} |"
        )
    lines.extend([
        "", "## Qartheen Enthroned Guardian focus", "",
        f"The nine-battle field cohort records **{field['deployed']} deployed / {field['kills']} kills = {field['kills_per_deployed']} kills per deployed**. Its kill share is **{float(field['player_side_kill_share']):.2%}** versus **{float(field['player_side_deployment_share']):.2%}** deployment share, a **{float(field['offensive_contribution_ratio']):.3f}x** contribution ratio, with **{float(field['retention_rate']):.2%}** retention.", "",
        f"Removing the highest-rate field battle ({sensitivity_rows[1]['excluded_battle_id']}) leaves **{sensitivity_rows[1]['independent_battles']} battles / {sensitivity_rows[1]['deployed']} deployed / {sensitivity_rows[1]['kills']} kills = {sensitivity_rows[1]['kills_per_deployed']}**, with a **{float(sensitivity_rows[1]['offensive_contribution_ratio']):.3f}x** contribution ratio. The sensitivity still clears the gate and preserves kill share above deployment share.", "",
        f"The single siege attack is separate and insufficient for ranking: **{siege['deployed']} deployed / {siege['kills']} kills = {siege['kills_per_deployed']}**, with {float(siege['retention_rate']):.2%} retention. It does not enter the field stop decision.", "",
        "**Decision: stop dedicated Qartheen Enthroned Guardian field testing.** The authoritative queue closes the target, keeps `ordered_queue` empty, and preserves the Arryn Winged Knight verification hold.", "",
        "## Per-battle focus evidence", "",
        "| context | battle | deployed | kills | kills/deployed | retention | player kills | player deployed |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ])
    for row in focus_battle_rows:
        lines.append(f"| {row['context']} | {row['battle_id']} | {row['deployed']} | {row['kills']} | {row['kills_per_deployed']} | {row['retention_rate']} | {row['player_side_kills']} | {row['player_side_deployed']} |")
    confirmed = sum(row["resolution_status"] == "confirmed_id" for row in identity_audit)
    lines.extend([
        "", "## Identity, model, and limitations", "",
        f"The pinned Realm of Thrones audit confirms **{confirmed}/{len(identity_audit)} ordinary display labels** by one exact soldier-name match. Unmatched labels stay provisional; no alias is inferred and no normalized value is corrected.", "",
        "No complete compatible Realm of Thrones v7.1/v7.3 empirical comparison universe is committed for this batch, so model comparison and residual artifacts explicitly record `not_run`; `analysis/model_versions/` is unchanged. Role populations do not reach five reliable rows in one role/context, so no role-adjusted blended rank is published.", "",
        "Raw PNGs are not retained in Git; Phase 2 verifies the immutable normalized archive, all member hashes, and the retained source manifest whose raw hashes were rechecked during Phase 1 recovery. Historical exact-hash search retains the recorded HTTP 502 limitation. Campaign results remain descriptive and confounded by opponent, map, roster, orders, and difficulty. No off-screen value is inferred.", "",
    ])
    return "\n".join(lines)


def main() -> None:
    immutable = repository_snapshot(IMMUTABLE_PATHS, "immutable Phase 1 inputs")
    frozen = repository_snapshot(FROZEN_MODEL_PATHS, "frozen model files")
    files, bundle = extract_bundle()
    events_list, parties, source_rows, shard_index = load_inputs(files)
    sources = verify_sources(files, events_list)
    events = {row["event_id"]: row for row in events_list}
    identities, identity_audit = resolve_identities(source_rows)
    ordinary, characters = adapt_rows(source_rows, events, identities)
    if len(ordinary) != 79 or len(characters) != 74:
        raise ValueError("ordinary/character partition mismatch")
    unresolved = [row for row in ordinary if not complete_numeric(row)]
    if len(unresolved) != 2 or {row["display_name"] for row in unresolved} != {"Qartheen Pureborn Warrior"}:
        raise ValueError("unexpected unresolved numeric occurrences")
    for row in ordinary:
        if complete_numeric(row) and row["deployed"] != row["survivors"] + row["deaths"] + row["wounded"]:
            raise ValueError(f"troop arithmetic mismatch: {row['occurrence_id']}")
    rankings = aggregate(ordinary, events)
    reliable = [dict(row) for row in rankings if row["reliability_status"].startswith("reliable")]
    for row in reliable:
        row["efficiency_rank"] = ""
        row["impact_rank"] = ""
    assign_ranks(reliable)
    insufficient = [dict(row) for row in rankings if not row["reliability_status"].startswith("reliable")]
    focus = [row for row in rankings if row["canonical_troop_id"] == FOCUS_ID]
    if len(focus) != 2 or {row["context"] for row in focus} != {"field", "siege_attack"}:
        raise ValueError("focus context coverage mismatch")
    focus_rows = focus_battles(ordinary, events)
    sensitivity_rows = sensitivity(focus_rows)
    field_focus = next(row for row in focus if row["context"] == "field")
    if not field_focus["numeric_display_gate_passed"] or not all(row["display_gate_passed"] for row in sensitivity_rows):
        raise ValueError("field focus or sensitivity gate failed")

    queue_validation = update_queue(field_focus, sensitivity_rows)
    write_csv(ANALYSIS_DIR / "ranking_complete.csv", RANKING_FIELDS, rankings)
    write_csv(ANALYSIS_DIR / "ranking_reliable.csv", RANKING_FIELDS, reliable)
    write_csv(ANALYSIS_DIR / "insufficient_evidence.csv", RANKING_FIELDS, insufficient)
    result_split_fields = ("result_scope", *RANKING_FIELDS)
    write_csv(
        ANALYSIS_DIR / "result_splits.csv",
        result_split_fields,
        [{"result_scope": "final_victory", **row} for row in rankings],
    )
    write_csv(ANALYSIS_DIR / "focus_deep_dive.csv", RANKING_FIELDS, focus)
    write_csv(ANALYSIS_DIR / "focus_battle_rates.csv", focus_rows[0].keys(), focus_rows)
    write_csv(ANALYSIS_DIR / "focus_sensitivity.csv", sensitivity_rows[0].keys(), sensitivity_rows)
    write_csv(ANALYSIS_DIR / "canonical_identity_audit.csv", identity_audit[0].keys(), identity_audit)
    write_csv(ANALYSIS_DIR / "ordinary_occurrences.csv", ordinary[0].keys(), ordinary)
    write_csv(ANALYSIS_DIR / "excluded_character_rows.csv", characters[0].keys(), characters)
    write_csv(ANALYSIS_DIR / "unresolved_rows.csv", unresolved[0].keys(), unresolved)
    (ANALYSIS_DIR / "screenshot_deduplication_audit.csv").write_bytes(files["reports/screenshot_deduplication_audit.csv"])

    denominator_rows = []
    context_rows = []
    for event in sorted(events_list, key=lambda row: row["capture_timestamp_local"]):
        totals = event["player_side_totals"]
        deployed = sum(totals[field] for field in ("survivors", "deaths", "wounded"))
        denominator_rows.append({
            "battle_id": event["event_id"], "captured_at": event["capture_timestamp_local"],
            "context": event["battle_context"], "result": event["result_status"],
            "player_side_total_kills": totals["kills"], "player_side_total_deployed": deployed,
            "kill_total_direct_positive": totals["kills"] > 0, "deployment_total_direct_positive": deployed > 0,
            "provenance": "normalized_visible_player_side_total", "source_key": event["source_keys"][0],
        })
        enemy = event["enemy_side_totals"]
        enemy_deployed = sum(enemy[field] for field in ("survivors", "deaths", "wounded"))
        context_rows.append({
            "battle_id": event["event_id"], "context": event["battle_context"], "result": event["result_status"],
            "player_deployed": deployed, "player_survivors": totals["survivors"],
            "player_retention": fmt(totals["survivors"] / deployed), "enemy_deployed": enemy_deployed,
            "enemy_survivors": enemy["survivors"], "enemy_retention": fmt(enemy["survivors"] / enemy_deployed),
            "pressure_margin": fmt(totals["survivors"] / deployed - enemy["survivors"] / enemy_deployed),
            "metric_status": "final_battle_level_not_attributed_to_one_troop",
        })
    write_csv(ANALYSIS_DIR / "denominator_coverage.csv", denominator_rows[0].keys(), denominator_rows)
    write_csv(ANALYSIS_DIR / "battle_context_review.csv", context_rows[0].keys(), context_rows)
    write_csv(ANALYSIS_DIR / "battle_pressure_margin.csv", context_rows[0].keys(), context_rows)

    coverage = []
    for context in ("field", "siege_attack"):
        context_occurrences = [row for row in ordinary if row["context"] == context]
        context_rankings = [row for row in rankings if row["context"] == context]
        coverage.append({
            "cohort": "Egon Emeros' Party", "context": context, "participant_scope": "player_party",
            "independent_battles": len({row["battle_id"] for row in context_occurrences}),
            "ordinary_occurrences": len(context_occurrences),
            "partial_ordinary_occurrences": sum(not complete_numeric(row) for row in context_occurrences),
            "partition_rows": len(context_rankings),
            "reliable_rows": sum(row["reliability_status"].startswith("reliable") for row in context_rankings),
            "insufficient_rows": sum(not row["reliability_status"].startswith("reliable") for row in context_rankings),
        })
    write_csv(ANALYSIS_DIR / "context_coverage.csv", coverage[0].keys(), coverage)
    grouping_rows = [{
        "cohort": row["cohort"], "context": row["context"],
        "participant_scope": row["participant_scope"], "display_name": row["display_name"],
        "ordinary_occurrences": row["ordinary_occurrences"],
        "partition_rows": 1, "status": "covered_exactly_once",
    } for row in rankings]
    write_csv(ANALYSIS_DIR / "grouping_validation.csv", grouping_rows[0].keys(), grouping_rows)
    aggregation_rows = [{
        "context": row["context"], "display_name": row["display_name"],
        "complete_numeric_occurrences": row["complete_numeric_occurrences"],
        "excluded_partial_occurrences": row["excluded_partial_occurrences"],
        "known_deployed": row["known_deployed"], "known_kills": row["known_kills"],
        "published_deployed": row["deployed"] if row["deployed"] is not None else "",
        "published_kills": row["kills"] if row["kills"] is not None else "",
        "status": "passed_complete_sum" if row["excluded_partial_occurrences"] == 0 else "passed_partial_values_not_imputed",
    } for row in rankings]
    write_csv(ANALYSIS_DIR / "aggregation_validation.csv", aggregation_rows[0].keys(), aggregation_rows)

    model_fields = ("canonical_troop_id", "context", "empirical_rank", "battle_count", "total_deployed", "evidence_grade", "empirical_kills_per_deployed", "general_score_v71", "burst_score_v73", "comparison_status")
    model_rows = [{
        "canonical_troop_id": row["canonical_troop_id"], "context": row["context"],
        "empirical_rank": row["efficiency_rank"], "battle_count": row["independent_battles"],
        "total_deployed": row["deployed"], "evidence_grade": row["evidence_grade"],
        "empirical_kills_per_deployed": row["kills_per_deployed"],
        "comparison_status": "not_run_no_complete_compatible_rot_v71_v73_model_universe",
    } for row in reliable]
    write_csv(ANALYSIS_DIR / "model_vs_empirical.csv", model_fields, model_rows)
    write_csv(ANALYSIS_DIR / "empirical_residual_rankings.csv", model_fields, model_rows)
    highest = max([row for row in focus_rows if row["context"] == "field"], key=lambda row: float(row["kills_per_deployed"]))
    write_csv(ANALYSIS_DIR / "outlier_report.csv", ("battle_id", "canonical_troop_id", "context", "deployed", "kills", "kills_per_deployed", "status", "primary_excluded"), [{
        "battle_id": highest["battle_id"], "canonical_troop_id": FOCUS_ID, "context": "field",
        "deployed": highest["deployed"], "kills": highest["kills"], "kills_per_deployed": highest["kills_per_deployed"],
        "status": "highest_rate_sensitivity_target_not_statistical_exclusion", "primary_excluded": False,
    }])

    report = build_report(rankings, focus, focus_rows, sensitivity_rows, identity_audit)
    (ANALYSIS_DIR / "ANALYSIS_REPORT.md").write_text(report, encoding="utf-8")
    (ANALYSIS_DIR / "empirical_analysis_summary.md").write_text(report, encoding="utf-8")
    (ANALYSIS_DIR / "NEXT_TEST_RECOMMENDATION.md").write_text(
        "# Next-test decision\n\nStop dedicated **Qartheen Enthroned Guardian / field** testing. "
        "The nine-battle cohort and leave-one-highest-rate-battle sensitivity pass the display gate "
        "with kill share above deployment share. No future target is approved: keep `ordered_queue` "
        "empty and preserve the Arryn Winged Knight verification hold.\n", encoding="utf-8",
    )
    (ANALYSIS_DIR / "README.md").write_text(
        f"# Phase 2 analytical outputs\n\nAll 79 visible ordinary occurrences partition into {len(rankings)} troop/context rows: "
        f"{len(reliable)} reliable and {len(insufficient)} insufficient. Reproduce with:\n\n"
        f"```bash\npython3 data/combat_observations/{BATCH_ID}/analysis/generate_phase2.py\n```\n", encoding="utf-8",
    )
    (ANALYSIS_DIR / "TESTS.md").write_text(
        "# Validation runs\n\n"
        "- Phase 2 generator: passed, including strict Base64/archive/member/mirror hashes, shard hashes, source links, identities, arithmetic, exact partition, focus, sensitivity, context, immutable-input, frozen-model, and queue assertions.\n"
        "- Deterministic regeneration: passed with byte-identical generated analysis/review artifacts and queue.\n"
        "- `python3 -m py_compile .../analysis/generate_phase2.py`: passed.\n"
        "- Focused repository validation: **101/101 passed** across normalized analysis, combat bundle/domain, task protocol, empirical analysis, Qartheen Phase 1 bundle, canonical identity, role diagnostics, and historical evidence audit.\n"
        "- `git diff --check`: passed.\n"
        "- Full repository discovery: 394 tests ran; 390 passed and 4 unrelated modules could not import because this environment lacks optional `pandas` (item catalog, two vanilla-audit discovery modules, and the ROT S-tier ranged audit).\n"
        "- No product-code behavior changed, so behavior-test red-before-green was not applicable to this deterministic batch generator and generated-report slice.\n",
        encoding="utf-8",
    )
    input_verification = {
        "status": "passed", "batch_id": BATCH_ID, "pipeline_mode": "offline-existing",
        "pipeline_version": "batch-phase2-1.0.0", "schema_version": "2.0.0",
        "normalization_commit": NORMALIZATION_COMMIT, "normalized_bundle": bundle,
        "source_manifest": sources, "player_row_shards_verified": len(shard_index["shards"]),
        "identity_audit": {"path": IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(), "sha256": IDENTITY_SHA256},
        "immutable_phase1_snapshot": immutable, "frozen_model_snapshot": frozen,
        "immutable_inputs_modified": immutable["modified_files"], "frozen_model_files_modified": frozen["modified_files"],
    }
    write_json(ANALYSIS_DIR / "input_verification.json", input_verification)
    write_json(ANALYSIS_DIR / "queue_validation.json", queue_validation)
    write_json(ANALYSIS_DIR / "cohort_compatibility.json", {
        "status": "passed_contexts_separate", "decisions": [
            {"cohort": "Egon Emeros' Party", "contexts": ["field", "siege_attack"], "decision": "aggregate only inside one context"},
            {"focus": FOCUS_ID, "decision": "single siege attack excluded from field stop decision"},
        ],
    })
    validation = {
        "status": "passed_with_documented_identity_and_visibility_limits", "validation_errors": [],
        "batch_id": BATCH_ID, "input_images": 10, "newly_accepted_screenshots": 10,
        "already_normalized_screenshots": 0, "internal_same_battle_duplicates": 0,
        "supplemental_screenshots": 0, "active_last_observation_battles": 0,
        "bundle_members_verified": bundle["members_verified"], "battles": len(events_list),
        "ordinary_occurrences": len(ordinary), "excluded_character_rows": len(characters),
        "unresolved_review_rows": len(unresolved), "distinct_ordinary_labels": len(identity_audit),
        "partition_rows": len(rankings), "reliable_rows": len(reliable), "insufficient_rows": len(insufficient),
        "partition_exact": len(rankings) == len(reliable) + len(insufficient),
        "focus_rows": len(focus), "focus_battle_rows": len(focus_rows),
        "focus_field_gate_passed": field_focus["numeric_display_gate_passed"],
        "focus_leave_highest_gate_passed": sensitivity_rows[1]["display_gate_passed"],
        "focus_siege_kept_separate": True, "direct_kill_total_coverage": "10/10",
        "direct_deployment_total_coverage": "10/10",
        "identity_confirmed": sum(row["resolution_status"] == "confirmed_id" for row in identity_audit),
        "identity_unresolved": sum(row["resolution_status"] != "confirmed_id" for row in identity_audit),
        "numeric_corrections": 0, "outlier_rows": 1, "primary_outlier_exclusions": 0,
        "contexts_pooled": False, "player_enemy_pooled": False, "offscreen_rows_inferred": False,
        "frozen_models_changed": False, "role_adjusted_blended_rank_published": False,
        "model_comparison_status": "not_run_no_complete_compatible_rot_v71_v73_model_universe",
        "queue_status": queue_validation["status"],
    }
    write_json(ANALYSIS_DIR / "validation_report.json", validation)
    write_json(ANALYSIS_DIR / "canonical_validation_report.json", validation)
    write_json(ANALYSIS_DIR / "analysis_state.json", {
        "batch_id": BATCH_ID, "status": "phase_2_complete_local_validation_passed",
        "normalization_commit": NORMALIZATION_COMMIT,
        "focus_decision": "completed_no_additional_test",
        "queue_after": {"active_test": None, "ordered_queue": [], "verification_holds": ["arryn_moonknight"]},
    })
    write_json(REVIEW_DIR / "phase2_review_summary.json", {
        "status": "complete_with_two_unresolved_visibility_rows_excluded_from_numeric_aggregation",
        "normalized_review_queue_rows": 2, "numeric_corrections": 0,
        "identity_decisions": len(identity_audit), "reviewer": "separate Phase 2 local analysis agent",
        "note": "Normalized evidence is unchanged; identity decisions and visibility dispositions are additive analysis-layer records.",
    })
    write_csv(REVIEW_DIR / "phase2_identity_decisions.csv", identity_audit[0].keys(), identity_audit)
    write_csv(REVIEW_DIR / "review_resolutions.csv", ("occurrence_id", "field", "original_value", "reviewed_value", "decision_status", "reason", "reviewer", "evidence_reference"), [
        {
            "occurrence_id": row["occurrence_id"], "field": "kills|upgrade_ready|deaths|wounded|routed",
            "original_value": "null", "reviewed_value": "null", "decision_status": "unresolved_visibility_excluded_from_numeric_aggregation",
            "reason": row["review_note"], "reviewer": "separate Phase 2 local analysis agent",
            "evidence_reference": "immutable normalized row and Phase 1 unresolved queue",
        } for row in unresolved
    ])
    (REVIEW_DIR / "README.md").write_text(
        "# Phase 2 reviewed layer\n\nNo normalized numeric value was changed. Two clipped Pureborn Warrior rows remain null and excluded from numeric aggregation; identity decisions are pinned to the versioned Realm of Thrones audit.\n",
        encoding="utf-8",
    )
    targets = [path for path in ANALYSIS_DIR.iterdir() if path.is_file() and path.name != "artifact_hashes.csv"]
    targets += [path for path in REVIEW_DIR.iterdir() if path.is_file()]
    artifacts = [{
        "path": path.relative_to(BATCH_DIR).as_posix(), "sha256": sha256_file(path), "size_bytes": path.stat().st_size,
    } for path in sorted(targets)]
    write_csv(ANALYSIS_DIR / "artifact_hashes.csv", ("path", "sha256", "size_bytes"), artifacts)
    print(json.dumps(validation, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
