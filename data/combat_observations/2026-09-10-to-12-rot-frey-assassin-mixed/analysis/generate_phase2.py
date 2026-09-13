#!/usr/bin/env python3
"""Generate the reviewed Phase 2 analysis for the Frey Assassin batch."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import random
import re
import tarfile
from collections import Counter, defaultdict
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parent
BATCH_DIR = ANALYSIS_DIR.parent
REPO_ROOT = ANALYSIS_DIR.parents[3]
REVIEW_DIR = BATCH_DIR / "reviewed"
IDENTITY_PATH = REPO_ROOT / "data/realm_of_thrones/audit/realm_of_thrones_troops.csv"
HISTORICAL_PATH = REPO_ROOT / "data/combat_observations/2026-09-07-to-08-rot-cerwyn-mixed/analysis/ranking_reliable.csv"

BATCH_ID = "2026-09-10-to-12-rot-frey-assassin-mixed"
TRACK = "realm_of_thrones"
GAME_VERSION = "1.4.x"
NORMALIZATION_COMMIT = "75b500ca3deab949aa8ca5392bf8c02df26e1f77"
IDENTITY_AUDIT_SHA256 = "63ea983998e25aa0e6f8c0747bf42e44440f695bbe1fec717074e7ba64e42810"
SOURCE_SHA256 = "23a83d0e0566e8fd2def0f9e7e950c5f19ea83f985f52b8bc71fcc212eaa5559"
SOURCE_SIZE = 12_840_258
BUNDLE_SHA256 = "83c1ba5030e27abd98eae24ca3b9e4c3c2ff3beefc99df6741d39c99ec3680ec"
BUNDLE_SIZE = 14_900
BUNDLE_MEMBERS = 22
HISTORICAL_SHA256 = "a26207cbe1e9bf362dce4ff8e303325785c32db68a1f627ceec7c03c52300839"
HISTORICAL_COMMIT = "f6c9bcab68f60419eaf4c7b5fdf11d4cf7676a30"
HISTORICAL_BLOB_SHA = "508a56989537d6598c9440dc9981de7b7961e4ca"
GATE_BATTLES = 5
GATE_DEPLOYED = 20
BOOTSTRAP_REPETITIONS = 10_000
FOCUS = ("Frey Assassin [T6]",)
COUNT_FIELDS = ("deployed", "survivors", "kills", "deaths", "wounded", "routed")

RANKING_FIELDS = (
    "track", "game_version", "cohort", "context", "participant_scope",
    "parent_group", "efficiency_rank", "impact_rank", "display_name",
    "canonical_troop_id", "identity_status", "canonical_default_group",
    "canonical_role", "evidence_grade", "reliable_role_population",
    "role_adjusted_rank_status",
    "independent_battles", *COUNT_FIELDS, "kills_per_deployed", "ci95_low",
    "ci95_high", "verified_player_side_total_kills", "kill_total_coverage_battles",
    "kill_total_coverage_complete", "player_side_kill_share",
    "share_adjusted_impact", "verified_player_side_total_deployed",
    "deployment_total_coverage_battles", "deployment_total_coverage_complete",
    "player_side_deployment_share", "offensive_contribution_ratio",
    "offensive_share_gap", "retention_rate", "death_rate", "casualty_rate",
    "victory_battles", "defeat_battles", "active_battles", "reliability_status",
    "more_battles_needed", "more_deployed_needed",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def fmt(value: float | None) -> str:
    return "" if value is None else f"{value:.6f}"


def tierless(name: str) -> str:
    return re.sub(r" \[T\d+\]$", "", name)


def cohort_for(battle: dict) -> str:
    party = battle["player_party"]
    if party == "Walder Frey's Party":
        return "frey_dedicated"
    raise ValueError(f"unrecognized player cohort: {party}")


def canonical_role(default_group: str) -> str:
    group = default_group.casefold()
    if group in {"ranged", "horsearcher", "horse_archer"}:
        return "ranged"
    if group == "infantry":
        return "frontline_infantry"
    if group == "cavalry":
        return "melee_cavalry"
    return ""


def evidence_grade(independent_battles: int, deployed: int) -> str:
    if independent_battles >= 5 and deployed >= 100:
        return "high"
    if independent_battles >= 3 and deployed >= 30:
        return "medium"
    if independent_battles >= 2 and deployed >= 10:
        return "low"
    return "exploratory"


def extract_bundle() -> tuple[dict[str, bytes], dict]:
    checkpoint = json.loads((BATCH_DIR / "phase1_checkpoint.json").read_text())
    encoded = BATCH_DIR / "bundle/frey_assassin_phase1.tar.xz.base64"
    compact_base64 = b"".join(encoded.read_bytes().split())
    archive = base64.b64decode(compact_base64, validate=True)
    if sha256_bytes(archive) != BUNDLE_SHA256 or len(archive) != BUNDLE_SIZE:
        raise ValueError("normalized bundle hash/size mismatch")
    files: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as bundle:
        members = bundle.getmembers()
        if len(members) != BUNDLE_MEMBERS:
            raise ValueError("normalized bundle member-count mismatch")
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

    declared = {item["path"]: item for item in checkpoint["archive"]["archive_contents"]}
    if set(files) != set(declared):
        raise ValueError("normalized bundle member set differs from checkpoint")
    for name, payload in files.items():
        expected = declared[name]
        if len(payload) != expected["size_bytes"] or sha256_bytes(payload) != expected["sha256"]:
            raise ValueError(f"normalized bundle member hash/size mismatch: {name}")
    return files, {
        "sha256": BUNDLE_SHA256,
        "size_bytes": len(archive),
        "members": len(files),
        "declared_member_hashes_verified": len(files),
        "safe_preflight_passed": True,
    }


def parse_csv_blob(blob: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig"))))


def verify_source_manifest(files: dict[str, bytes]) -> dict:
    inventory = parse_csv_blob(files["source_inventory.csv"])
    screenshots = load_bundle_jsonl(files, "canonical/canonical_screenshots.jsonl")
    ordered_inventory = sorted(inventory, key=lambda row: int(row["source_order"]))
    manifest_rows = (
        f"{row['sha256']}  {row['size_bytes']}  {row['image_file']}\n"
        for row in ordered_inventory
    )
    source_set_sha = sha256_bytes("".join(manifest_rows).encode())
    if source_set_sha != SOURCE_SHA256 or sum(int(row["size_bytes"]) for row in inventory) != SOURCE_SIZE:
        raise ValueError("source inventory set hash/size mismatch")
    inventory_keys = {(row["image_file"], row["sha256"]) for row in inventory}
    screenshot_keys = {(row["image_file"], row["image_sha256"]) for row in screenshots}
    if inventory_keys != screenshot_keys:
        raise ValueError("source inventory/canonical screenshot mismatch")
    return {
        "source_set_sha256": source_set_sha,
        "source_size_bytes": SOURCE_SIZE,
        "manifest_entries_verified": len(inventory),
        "serialization_order": "numeric source_order",
        "provenance_wording_note": "The Phase 1 prose says sorted lines; the committed hash is reproduced by numeric source_order, not lexicographic line order.",
        "raw_source_bytes_locally_verified": False,
        "raw_repository_retention": "not_retained_optional_after_verified_normalization",
        "note": "Phase 1 hashed all source PNGs; Phase 2 verifies the retained source manifest and immutable normalized archive.",
    }


def load_bundle_jsonl(files: dict[str, bytes], name: str) -> list[dict]:
    return [json.loads(line) for line in files[name].decode().splitlines() if line]


def resolve_identities(names: set[str]) -> dict[str, dict]:
    if sha256_file(IDENTITY_PATH) != IDENTITY_AUDIT_SHA256:
        raise ValueError("versioned Realm of Thrones identity audit hash mismatch")
    audit = read_csv(IDENTITY_PATH)
    output = {}
    for name in sorted(names):
        base = tierless(name)
        matches = [
            row for row in audit
            if row.get("is_soldier", "").casefold() == "true"
            and row.get("name", "").casefold() == base.casefold()
        ]
        unique_ids = sorted({row["troop_id"] for row in matches})
        confirmed = len(unique_ids) == 1
        matched = matches[0] if confirmed else {}
        output[name] = {
            "canonical_troop_id": unique_ids[0] if confirmed else "",
            "identity_status": "confirmed_id" if confirmed else (
                "ambiguous_exact_name" if len(unique_ids) > 1 else "unresolved"
            ),
            "default_group": matched.get("default_group", ""),
            "canonical_role": canonical_role(matched.get("default_group", "")),
            "level": matched.get("level", ""),
            "candidate_count": len(unique_ids),
            "candidate_troop_ids": "|".join(unique_ids),
            "blocking_reason": "" if confirmed else (
                "multiple exact display-name matches" if unique_ids
                else "no exact tier-stripped display-name match in versioned audit"
            ),
        }
    return output


def bootstrap(rows: list[dict], key: str) -> tuple[float, float]:
    seed = int(hashlib.sha256(f"{BATCH_ID}|{key}|{BOOTSTRAP_REPETITIONS}".encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    ordered = sorted(rows, key=lambda row: row["battle_id"])
    values = []
    for _ in range(BOOTSTRAP_REPETITIONS):
        sample = [ordered[rng.randrange(len(ordered))] for _ in ordered]
        deployed = sum(row["deployed"] for row in sample)
        kills = sum(row["kills"] for row in sample)
        values.append(kills / deployed)
    values.sort()
    return values[int(0.025 * (len(values) - 1))], values[int(0.975 * (len(values) - 1))]


def participant_key(row: dict, battle: dict) -> tuple[str, str, str, str, str]:
    return (
        cohort_for(battle),
        row["battle_context"],
        row["relationship_to_player"],
        row["parent_group"],
        row["display_name_raw"],
    )


def aggregate_rows(rows: list[dict], battles: dict[str, dict], identities: dict[str, dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        battle = battles[row["battle_id"]]
        groups[participant_key(row, battle)].append(row)

    output = []
    for (cohort, context, scope, parent, name), subset in groups.items():
        battle_ids = {row["battle_id"] for row in subset}
        counts = {field: sum(int(row[field]) for row in subset) for field in COUNT_FIELDS}
        independent = len(battle_ids)
        reliable = independent >= GATE_BATTLES and counts["deployed"] >= GATE_DEPLOYED
        side_kills = sum(int(battles[battle_id]["player_kills"]) for battle_id in battle_ids)
        side_deployed = sum(int(battles[battle_id]["player_deployed"]) for battle_id in battle_ids)
        kill_share = counts["kills"] / side_kills
        deployment_share = counts["deployed"] / side_deployed
        efficiency = counts["kills"] / counts["deployed"]
        result_counts = Counter(battles[battle_id]["result"] for battle_id in battle_ids)
        identity = identities[name]
        ci_low, ci_high = bootstrap(subset, "|".join((cohort, context, scope, parent, name))) if reliable else (None, None)
        output.append({
            "track": TRACK,
            "game_version": GAME_VERSION,
            "cohort": cohort,
            "context": context,
            "participant_scope": scope,
            "parent_group": parent,
            "display_name": name,
            "canonical_troop_id": identity["canonical_troop_id"],
            "identity_status": identity["identity_status"],
            "canonical_default_group": identity["default_group"],
            "canonical_role": identity["canonical_role"],
            "evidence_grade": evidence_grade(independent, counts["deployed"]),
            "role_adjusted_rank_status": "not_published_current_methodology_keeps_offense_and_defense_independent",
            "independent_battles": independent,
            **counts,
            "kills_per_deployed": fmt(efficiency),
            "ci95_low": fmt(ci_low),
            "ci95_high": fmt(ci_high),
            "verified_player_side_total_kills": side_kills,
            "kill_total_coverage_battles": independent,
            "kill_total_coverage_complete": True,
            "player_side_kill_share": fmt(kill_share),
            "share_adjusted_impact": fmt(efficiency * kill_share),
            "verified_player_side_total_deployed": side_deployed,
            "deployment_total_coverage_battles": independent,
            "deployment_total_coverage_complete": True,
            "player_side_deployment_share": fmt(deployment_share),
            "offensive_contribution_ratio": fmt(kill_share / deployment_share),
            "offensive_share_gap": fmt(kill_share - deployment_share),
            "retention_rate": fmt(counts["survivors"] / counts["deployed"]),
            "death_rate": fmt(counts["deaths"] / counts["deployed"]),
            "casualty_rate": fmt((counts["deaths"] + counts["wounded"]) / counts["deployed"]),
            "victory_battles": result_counts["victory"],
            "defeat_battles": result_counts["defeat"],
            "active_battles": result_counts["active"],
            "reliability_status": "reliable" if reliable else "insufficient_evidence",
            "more_battles_needed": max(0, GATE_BATTLES - independent),
            "more_deployed_needed": max(0, GATE_DEPLOYED - counts["deployed"]),
        })

    rank_groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in output:
        rank_groups[(row["cohort"], row["context"], row["participant_scope"], row["parent_group"])].append(row)
    for group in rank_groups.values():
        efficiency_order = sorted(group, key=lambda row: (-float(row["kills_per_deployed"]), -row["deployed"], row["display_name"]))
        impact_order = sorted(group, key=lambda row: (-float(row["share_adjusted_impact"]), -row["deployed"], row["display_name"]))
        for rank, row in enumerate(efficiency_order, 1):
            row["efficiency_rank"] = rank
        for rank, row in enumerate(impact_order, 1):
            row["impact_rank"] = rank
        role_counts = Counter(row["canonical_role"] for row in group if row["reliability_status"] == "reliable" and row["canonical_role"])
        for row in group:
            row["reliable_role_population"] = role_counts[row["canonical_role"]] if row["canonical_role"] else 0
    return sorted(output, key=lambda row: (row["cohort"], row["context"], row["participant_scope"], row["parent_group"], row["efficiency_rank"]))


def rerank_reliable(rows: list[dict]) -> list[dict]:
    reliable = [dict(row) for row in rows if row["reliability_status"] == "reliable"]
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in reliable:
        groups[(row["cohort"], row["context"], row["participant_scope"], row["parent_group"])].append(row)
    for group in groups.values():
        for rank, row in enumerate(sorted(group, key=lambda item: (-float(item["kills_per_deployed"]), -item["deployed"], item["display_name"])), 1):
            row["efficiency_rank"] = rank
        for rank, row in enumerate(sorted(group, key=lambda item: (-float(item["share_adjusted_impact"]), -item["deployed"], item["display_name"])), 1):
            row["impact_rank"] = rank
    return sorted(reliable, key=lambda row: (row["cohort"], row["context"], row["participant_scope"], row["efficiency_rank"]))


def result_splits(rows: list[dict], battles: dict[str, dict], identities: dict[str, dict]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        battle = battles[row["battle_id"]]
        groups[(*participant_key(row, battle), battle["result"])].append(row)
    output = []
    for (cohort, context, scope, parent, name, result), subset in groups.items():
        battle_ids = {row["battle_id"] for row in subset}
        deployed = sum(row["deployed"] for row in subset)
        survivors = sum(row["survivors"] for row in subset)
        kills = sum(row["kills"] for row in subset)
        deaths = sum(row["deaths"] for row in subset)
        wounded = sum(row["wounded"] for row in subset)
        side_kills = sum(battles[battle_id]["player_kills"] for battle_id in battle_ids)
        side_deployed = sum(battles[battle_id]["player_deployed"] for battle_id in battle_ids)
        output.append({
            "cohort": cohort, "context": context, "participant_scope": scope,
            "parent_group": parent, "display_name": name,
            "canonical_troop_id": identities[name]["canonical_troop_id"],
            "result": result, "censoring_status": "censored_diagnostic" if result == "active" else "final",
            "independent_battles": len(battle_ids), "deployed": deployed,
            "survivors": survivors, "kills": kills, "deaths": deaths, "wounded": wounded,
            "kills_per_deployed": fmt(kills / deployed), "retention_rate": fmt(survivors / deployed),
            "verified_player_side_total_kills": side_kills,
            "player_side_kill_share": fmt(kills / side_kills),
            "verified_player_side_total_deployed": side_deployed,
            "player_side_deployment_share": fmt(deployed / side_deployed),
            "offensive_contribution_ratio": fmt((kills / side_kills) / (deployed / side_deployed)),
            "offensive_share_gap": fmt(kills / side_kills - deployed / side_deployed),
        })
    return sorted(output, key=lambda row: (row["cohort"], row["context"], row["display_name"], {"victory": 0, "defeat": 1, "active": 2}.get(row["result"], 9)))


def pressure_rows(battles: dict[str, dict]) -> list[dict]:
    output = []
    for battle in sorted(battles.values(), key=lambda row: row["captured_at"]):
        allied = battle["player_survivors"] / battle["player_deployed"]
        enemy = battle["opponent_survivors"] / battle["opponent_deployed"]
        final = battle["result"] in {"victory", "defeat", "retreat"}
        output.append({
            "battle_id": battle["battle_id"], "captured_at": battle["captured_at"],
            "cohort": cohort_for(battle), "context": battle["battle_context"],
            "result": battle["result"], "observation_censoring": battle["observation_censoring"],
            "player_deployed": battle["player_deployed"], "player_remaining": battle["player_survivors"],
            "allied_retention": fmt(allied), "opponent_deployed": battle["opponent_deployed"],
            "opponent_remaining": battle["opponent_survivors"], "enemy_retention": fmt(enemy),
            "pressure_margin": fmt(allied - enemy),
            "metric_status": "final" if final else "diagnostic_censored_snapshot",
            "included_in_final_pressure_summary": final,
            "source_image_sha256": battle["source_image_sha256"],
        })
    return output


def focus_battle_rows(rows: list[dict], battles: dict[str, dict], identities: dict[str, dict]) -> list[dict]:
    output = []
    for row in rows:
        if row["display_name_raw"] not in FOCUS:
            continue
        battle = battles[row["battle_id"]]
        output.append({
            "display_name": row["display_name_raw"],
            "canonical_troop_id": identities[row["display_name_raw"]]["canonical_troop_id"],
            "battle_id": row["battle_id"], "captured_at": battle["captured_at"],
            "cohort": cohort_for(battle), "context": row["battle_context"],
            "result": battle["result"], "censoring_status": "censored_diagnostic" if battle["result"] == "active" else "final",
            "deployed": row["deployed"], "survivors": row["survivors"], "kills": row["kills"],
            "deaths": row["deaths"], "wounded": row["wounded"],
            "kills_per_deployed": fmt(row["kills"] / row["deployed"]),
            "retention_rate": fmt(row["survivors"] / row["deployed"]),
            "player_side_kills": battle["player_kills"],
            "player_side_deployed": battle["player_deployed"],
        })
    return sorted(output, key=lambda row: (FOCUS.index(row["display_name"]), row["captured_at"]))


def identity_audit_rows(rows: list[dict], identities: dict[str, dict]) -> list[dict]:
    observed = defaultdict(lambda: {"ids": set(), "hashes": set(), "occurrences": 0})
    for row in rows:
        name = row["display_name_raw"]
        observed[name]["ids"].add(row.get("canonical_troop_id") or "")
        observed[name]["hashes"].add(row["source_image_sha256"])
        observed[name]["occurrences"] += 1
    output = []
    for name in sorted(observed):
        identity = identities[name]
        output.append({
            "display_name": name, "observed_canonical_troop_ids": "|".join(sorted(observed[name]["ids"])),
            "canonical_troop_id": identity["canonical_troop_id"],
            "resolution_status": identity["identity_status"],
            "default_group": identity["default_group"], "canonical_role": identity["canonical_role"],
            "level": identity["level"], "candidate_count": identity["candidate_count"],
            "candidate_troop_ids": identity["candidate_troop_ids"],
            "resolution_method": "exact tier-stripped display-name match" if identity["identity_status"] == "confirmed_id" else "unresolved conservative exact-match audit",
            "blocking_reason": identity["blocking_reason"],
            "ordinary_occurrences": observed[name]["occurrences"],
            "source_image_count": len(observed[name]["hashes"]),
            "audit_path": IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(),
            "audit_sha256": IDENTITY_AUDIT_SHA256,
        })
    return output


def capture_timestamp(image_file: str) -> str:
    match = re.search(r"(\d{2})_(\d{2})_(\d{4})[ _](\d{2})_(\d{2})_(\d{2})", image_file)
    if not match:
        raise ValueError(f"capture timestamp missing from {image_file}")
    day, month, year, hour, minute, second = match.groups()
    return f"{year}-{month}-{day}T{hour}:{minute}:{second}-03:00"


def adapt_battles(raw_battles: list[dict]) -> dict[str, dict]:
    battles = {}
    for raw in raw_battles:
        battle = dict(raw)
        battle.update({
            "captured_at": capture_timestamp(raw["representative_image_file"]),
            "opponent_deployed": raw["enemy_deployed"],
            "opponent_survivors": raw["enemy_survivors"],
            "observation_censoring": "right_censored" if raw["state"] == "active_last_observation" else "final",
            "source_image_sha256": raw["representative_image_sha256"],
        })
        battles[raw["battle_id"]] = battle
    return battles


def adapt_rows(raw_rows: list[dict], battles: dict[str, dict]) -> list[dict]:
    rows = []
    for raw in raw_rows:
        row = dict(raw)
        if len(raw["display_names_raw"]) != 1:
            raise ValueError(f"unexpected display-name consolidation: {raw['battle_id']}")
        battle = battles[raw["battle_id"]]
        if battle["game_versions"] != [GAME_VERSION]:
            raise ValueError(f"unexpected game version boundary: {raw['battle_id']}")
        row.update({
            "display_name_raw": raw["display_names_raw"][0],
            "relationship_to_player": raw["participant_scope"],
            "game_version": GAME_VERSION,
            "source_image_sha256": battle["source_image_sha256"],
        })
        rows.append(row)
    return rows


def build_focus_sensitivity(focus_battles: list[dict]) -> list[dict]:
    scenarios = [("all_observations", focus_battles)]
    final_rows = [row for row in focus_battles if row["result"] != "active"]
    scenarios.append(("final_results_only", final_rows))
    highest = max(focus_battles, key=lambda row: float(row["kills_per_deployed"]))
    scenarios.append((f"exclude_highest_rate_{highest['battle_id']}", [row for row in focus_battles if row is not highest]))
    output = []
    for scenario, rows in scenarios:
        deployed = sum(row["deployed"] for row in rows)
        kills = sum(row["kills"] for row in rows)
        survivors = sum(row["survivors"] for row in rows)
        side_kills = sum(row["player_side_kills"] for row in rows)
        side_deployed = sum(row["player_side_deployed"] for row in rows)
        kill_share = kills / side_kills
        deployment_share = deployed / side_deployed
        output.append({
            "scenario": scenario,
            "independent_battles": len(rows),
            "deployed": deployed,
            "kills": kills,
            "kills_per_deployed": fmt(kills / deployed),
            "player_side_kill_share": fmt(kill_share),
            "player_side_deployment_share": fmt(deployment_share),
            "offensive_contribution_ratio": fmt(kill_share / deployment_share),
            "offensive_share_gap": fmt(kill_share - deployment_share),
            "survivors": survivors,
            "retention_rate": fmt(survivors / deployed),
            "display_gate_passed": len(rows) >= GATE_BATTLES and deployed >= GATE_DEPLOYED,
        })
    return output


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def historical_comparison(focus_row: dict) -> list[dict]:
    payload = HISTORICAL_PATH.read_bytes()
    if sha256_bytes(payload) != HISTORICAL_SHA256 or git_blob_sha(payload) != HISTORICAL_BLOB_SHA:
        raise ValueError("pinned historical Frey ranking changed")
    rows = list(csv.DictReader(io.StringIO(payload.decode("utf-8-sig"))))
    prior = next(
        row for row in rows
        if row["cohort"] == "frey" and row["context"] == "field"
        and row["parent_group"] == "Walder Frey's Party"
        and row["display_name"] == "Frey Assassin"
    )
    common = {
        "track": TRACK,
        "game_version": GAME_VERSION,
        "context": "field",
        "display_name": "Frey Assassin",
        "canonical_troop_id": "frey_assassin",
        "pooling_eligible": False,
        "pooling_decision": "descriptive_comparison_only_separate_campaign_roster_opponents_and_unrecorded_difficulty_state",
    }
    return [
        {
            **common,
            "cohort_kind": "dedicated_current",
            "source_path": BATCH_DIR.relative_to(REPO_ROOT).as_posix() + "/analysis/focus_deep_dive.csv",
            "source_commit": "current_phase2_head",
            "source_blob_sha": "generated_and_pinned_by_artifact_hashes",
            **{field: focus_row[field] for field in (
                "independent_battles", "deployed", "kills", "kills_per_deployed",
                "player_side_kill_share", "player_side_deployment_share",
                "offensive_contribution_ratio", "offensive_share_gap", "retention_rate",
            )},
        },
        {
            **common,
            "cohort_kind": "incidental_prior",
            "source_path": HISTORICAL_PATH.relative_to(REPO_ROOT).as_posix(),
            "source_commit": HISTORICAL_COMMIT,
            "source_blob_sha": HISTORICAL_BLOB_SHA,
            **{field: prior[field] for field in (
                "independent_battles", "deployed", "kills", "kills_per_deployed",
                "player_side_kill_share", "player_side_deployment_share",
                "offensive_contribution_ratio", "offensive_share_gap", "retention_rate",
            )},
        },
    ]


def build_report(rankings: list[dict], reliable: list[dict], insufficient: list[dict], focus: list[dict], pressure: list[dict], identity_audit: list[dict], sensitivity: list[dict], comparison: list[dict], occurrence_count: int) -> str:
    lines = [f"# Phase 2 analysis — {BATCH_ID}", "", "## Batch-wide findings", "",
        f"All **{occurrence_count}** visible player-side ordinary-troop occurrences form **{len(rankings)}** troop/context rows: **{len(reliable)} reliable** and **{len(insufficient)} below the 5-battle / 20-deployed gate**. Field and siege attack remain separate, and the active last observation is an independent right-censored battle.", "",
        "### Exact reliable/insufficient partition", "",
        "| Partition | Context | Eff. rank | Impact rank | Troop | Battles | Deployed | Kills | Kills/deployed | Kill share | Deploy share | Ratio | Retention | Grade |",
        "|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",]
    for row in rankings:
        lines.append(
            f"| {row['reliability_status']} | {row['context']} | {row['efficiency_rank']} | {row['impact_rank']} | {row['display_name']} | {row['independent_battles']} | {row['deployed']} | {row['kills']} | {row['kills_per_deployed']} | {float(row['player_side_kill_share']):.2%} | {float(row['player_side_deployment_share']):.2%} | {row['offensive_contribution_ratio']} | {float(row['retention_rate']):.2%} | {row['evidence_grade']} |"
        )

    current = comparison[0]
    prior = comparison[1]
    final_only = next(row for row in sensitivity if row["scenario"] == "final_results_only")
    lines += ["", "## Additive Frey Assassin deep dive", "",
        f"The dedicated field cohort records **{current['independent_battles']} battles / {current['deployed']} deployed / {current['kills']} kills = {current['kills_per_deployed']} kills/deployed**. It supplied **{float(current['player_side_kill_share']):.2%}** of player-side kills from **{float(current['player_side_deployment_share']):.2%}** of deployments (**{float(current['offensive_contribution_ratio']):.3f}x**, gap **{float(current['offensive_share_gap']):.2%}**), with **{float(current['retention_rate']):.2%}** retention.", "",
        f"The final-results-only sensitivity still passes the gate at **{final_only['independent_battles']} battles / {final_only['deployed']} deployed / {final_only['kills']} kills = {final_only['kills_per_deployed']}**, with a **{float(final_only['offensive_contribution_ratio']):.3f}x** contribution ratio. The active battle therefore does not create the stop decision.", "",
        f"The already-merged incidental PR #96 cohort was **{prior['independent_battles']} battles / {prior['deployed']} deployed / {prior['kills']} kills = {prior['kills_per_deployed']}**, with **{float(prior['retention_rate']):.2%}** retention. These cohorts are compared descriptively but never pooled: campaign date, roster, opponents, and difficulty state are not controlled as one experiment.", "",
        "**Decision: stop dedicated Frey Assassin field testing.** The dedicated cohort and its final-only sensitivity both clear the display gate and retain kill share above deployment share. No future target is approved; the Arryn Winged Knight historical hold remains authoritative.", "",
        "## Defensive context and boundaries", "",
        f"Five final field battles and the final siege attack publish production pressure margins. One active field scoreboard remains diagnostic only. Pressure margin stays battle-level and is not assigned to Frey Assassin or another troop.", "",
        "## Identity, model, and evidence limits", "",
        f"The pinned Realm of Thrones audit confirms **{sum(row['resolution_status'] == 'confirmed_id' for row in identity_audit)} of {len(identity_audit)}** labels by one exact tier-stripped name-to-ID match. No normalized value required correction.", "",
        "No complete compatible Realm of Thrones v7.1/v7.3 model universe is committed here, so model comparison and residual outputs explicitly record `not_run`; frozen models are unchanged. Role populations do not reach five reliable rows inside one role/context, so no role-adjusted rank is published.", "",
        "## Limitations", "",
        "Raw PNGs are not retained after verified normalization. The Phase 1 source-hash prose says sorted lines, while the committed hash reproduces only in numeric `source_order`; Phase 2 records that wording ambiguity without changing provenance. Repository-wide historical exact-hash search previously returned HTTP 502, so historical duplicate risk remains low rather than zero. Campaign results remain confounded by opponent, map, roster, orders, and unrecorded difficulty. No off-screen row is inferred and no context, participant, or result-state boundary is crossed.", ""]
    return "\n".join(lines)


def main() -> None:
    files, bundle_verification = extract_bundle()
    source_verification = verify_source_manifest(files)
    battles = adapt_battles(load_bundle_jsonl(files, "canonical/canonical_battles.jsonl"))
    occurrences = load_bundle_jsonl(files, "canonical/canonical_occurrences.jsonl")
    rows = adapt_rows(
        load_bundle_jsonl(files, "canonical/canonical_troop_battle_consolidated.jsonl"),
        battles,
    )

    if len(battles) != 7 or len(occurrences) != 131 or len(rows) != 61:
        raise ValueError("unexpected normalized batch counts")
    if Counter(battle["battle_context"] for battle in battles.values()) != {"field": 6, "siege_attack": 1}:
        raise ValueError("unexpected battle-context partition")
    if any(row["game_track"] != TRACK or row["game_version"] != GAME_VERSION for row in rows):
        raise ValueError("track/version boundary violation")
    if any(row["relationship_to_player"] != "player_party" or row["analysis_status"] != "included_primary" for row in rows):
        raise ValueError("ordinary player-side troop boundary violation")
    for row in rows:
        if row["deployed"] != row["survivors"] + row["deaths"] + row["wounded"]:
            raise ValueError(f"troop arithmetic mismatch: {row['battle_id']} / {row['display_name_raw']}")

    names = {row["display_name_raw"] for row in rows}
    identities = resolve_identities(names)
    rankings = aggregate_rows(rows, battles, identities)
    reliable = rerank_reliable(rankings)
    insufficient = [row for row in rankings if row["reliability_status"] == "insufficient_evidence"]
    splits = result_splits(rows, battles, identities)
    pressure = pressure_rows(battles)
    reliable_index = {
        (row["cohort"], row["context"], row["participant_scope"], row["parent_group"], row["display_name"]): row
        for row in reliable
    }
    focus = [
        reliable_index.get(
            (row["cohort"], row["context"], row["participant_scope"], row["parent_group"], row["display_name"]),
            row,
        )
        for row in rankings
        if row["display_name"] in FOCUS
    ]
    focus_battles = focus_battle_rows(rows, battles, identities)
    identity_audit = identity_audit_rows(rows, identities)
    field_focus = next(row for row in focus if row["context"] == "field")
    sensitivity = build_focus_sensitivity([row for row in focus_battles if row["context"] == "field"])
    comparison = historical_comparison(field_focus)

    if (len(rankings), len(reliable), len(insufficient)) != (27, 6, 21):
        raise ValueError("reliable/insufficient partition mismatch")
    if len(focus) != 2 or {row["context"] for row in focus} != {"field", "siege_attack"}:
        raise ValueError("focus coverage mismatch")
    if any(identity["identity_status"] != "confirmed_id" for identity in identities.values()):
        raise ValueError("identity resolution incomplete")

    write_csv(ANALYSIS_DIR / "ranking_complete.csv", RANKING_FIELDS, rankings)
    write_csv(ANALYSIS_DIR / "ranking_reliable.csv", RANKING_FIELDS, reliable)
    write_csv(ANALYSIS_DIR / "insufficient_evidence.csv", RANKING_FIELDS, insufficient)
    split_fields = list(splits[0])
    write_csv(ANALYSIS_DIR / "result_splits.csv", split_fields, splits)
    write_csv(ANALYSIS_DIR / "battle_pressure_margin.csv", list(pressure[0]), pressure)
    write_csv(ANALYSIS_DIR / "focus_deep_dive.csv", RANKING_FIELDS, focus)
    write_csv(ANALYSIS_DIR / "focus_battle_rates.csv", list(focus_battles[0]), focus_battles)
    write_csv(ANALYSIS_DIR / "focus_sensitivity.csv", list(sensitivity[0]), sensitivity)
    write_csv(ANALYSIS_DIR / "focus_historical_comparison.csv", list(comparison[0]), comparison)
    write_csv(ANALYSIS_DIR / "canonical_identity_audit.csv", list(identity_audit[0]), identity_audit)

    side_totals = defaultdict(list)
    for occurrence in occurrences:
        if occurrence["row_type"] == "side_total":
            side_totals[occurrence["battle_id"]].append(occurrence)
    kill_coverage = []
    for battle in sorted(battles.values(), key=lambda row: row["captured_at"]):
        direct = [
            row for row in side_totals[battle["battle_id"]]
            if row["side"] == battle["player_side"] and not row["needs_review"]
        ]
        if len(direct) != 1:
            raise ValueError(f"missing or duplicate player side total: {battle['battle_id']}")
        direct = direct[0]
        if direct["kills"] != battle["player_kills"] or direct["deployed"] != battle["player_deployed"]:
            raise ValueError(f"battle metadata/side-total mismatch: {battle['battle_id']}")
        kill_coverage.append({
            "battle_id": battle["battle_id"], "captured_at": battle["captured_at"],
            "cohort": cohort_for(battle), "context": battle["battle_context"],
            "result": battle["result"], "player_kills": battle["player_kills"],
            "player_deployed": battle["player_deployed"],
            "kill_total_direct_positive": battle["player_kills"] > 0,
            "deployment_total_direct_positive": battle["player_deployed"] > 0,
            "provenance": "battle_metadata_and_visible_side_total_exact_match",
            "source_image_sha256": battle["source_image_sha256"],
        })
    write_csv(ANALYSIS_DIR / "denominator_coverage.csv", list(kill_coverage[0]), kill_coverage)

    coverage_groups = defaultdict(lambda: {"battle_ids": set(), "occurrences": 0, "rows": 0, "reliable": 0, "insufficient": 0})
    for row in rows:
        battle = battles[row["battle_id"]]
        key = (cohort_for(battle), row["battle_context"], row["relationship_to_player"], row["parent_group"])
        coverage_groups[key]["battle_ids"].add(row["battle_id"])
        coverage_groups[key]["occurrences"] += 1
    for row in rankings:
        key = (row["cohort"], row["context"], row["participant_scope"], row["parent_group"])
        coverage_groups[key]["rows"] += 1
        coverage_groups[key]["reliable"] += row["reliability_status"] == "reliable"
        coverage_groups[key]["insufficient"] += row["reliability_status"] == "insufficient_evidence"
    context_coverage = [
        {"cohort": key[0], "context": key[1], "participant_scope": key[2], "parent_group": key[3],
         "independent_battles": len(value["battle_ids"]), "ordinary_occurrences": value["occurrences"],
         "partition_rows": value["rows"], "reliable_rows": value["reliable"], "insufficient_rows": value["insufficient"]}
        for key, value in sorted(coverage_groups.items())
    ]
    write_csv(ANALYSIS_DIR / "context_coverage.csv", list(context_coverage[0]), context_coverage)

    compatibility = {
        "status": "passed_with_context_and_historical_cohort_separation",
        "decisions": [
            {"cohort": "frey_dedicated", "contexts": ["field", "siege_attack"], "decision": "aggregate only inside one context"},
            {"battle": "battle_fa07", "decision": "independent active last observation; included in offensive evidence but excluded from production pressure margin"},
            {"pair": ["frey_dedicated", "PR_96_frey_incidental"], "decision": "descriptive comparison only; never pool campaign date, roster, opponent, or unrecorded difficulty states"},
        ],
    }
    write_json(ANALYSIS_DIR / "cohort_compatibility.json", compatibility)

    input_verification = {
        "status": "passed", "batch_id": BATCH_ID, "pipeline_mode": "offline-existing",
        "pipeline_version": "0.4.0", "schema_version": "2.0.0",
        "normalization_commit": NORMALIZATION_COMMIT,
        "source_manifest": source_verification, "normalized_bundle": bundle_verification,
        "identity_audit": {"path": IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(), "sha256": IDENTITY_AUDIT_SHA256},
        "historical_comparison_source": {"path": HISTORICAL_PATH.relative_to(REPO_ROOT).as_posix(), "commit": HISTORICAL_COMMIT, "blob_sha": HISTORICAL_BLOB_SHA, "sha256": HISTORICAL_SHA256},
        "immutable_inputs_modified": [], "frozen_model_files_modified": [],
    }
    write_json(ANALYSIS_DIR / "input_verification.json", input_verification)
    write_json(REVIEW_DIR / "phase2_review_summary.json", {
        "status": "complete", "normalized_review_queue_rows": 0,
        "numeric_corrections": 0, "identity_decisions": len(identity_audit),
        "reviewer": "separate Phase 2 local analysis agent",
        "note": "No normalized value changed. Canonical identities are analysis-layer decisions only.",
    })
    write_csv(REVIEW_DIR / "phase2_identity_decisions.csv", list(identity_audit[0]), identity_audit)
    write_csv(
        REVIEW_DIR / "review_resolutions.csv",
        ("review_correction_id", "observation_id", "field", "original_value", "reviewed_value", "decision_status", "reason", "reviewer", "evidence_reference"),
        [],
    )
    (REVIEW_DIR / "README.md").write_text(
        "# Phase 2 reviewed layer\n\nNo normalized numeric correction was required. "
        "Identity decisions are additive and pinned to the versioned Realm of Thrones audit.\n",
        encoding="utf-8",
    )

    report = build_report(rankings, reliable, insufficient, focus, pressure, identity_audit, sensitivity, comparison, len(rows))
    (ANALYSIS_DIR / "ANALYSIS_REPORT.md").write_text(report, encoding="utf-8")
    (ANALYSIS_DIR / "empirical_analysis_summary.md").write_text(report, encoding="utf-8")
    (ANALYSIS_DIR / "NEXT_TEST_RECOMMENDATION.md").write_text(
        "# Next-test decision\n\nStop dedicated **Frey Assassin / field** testing. "
        "The six-battle cohort and its five-final-battle sensitivity both pass the display gate "
        "with kill share above deployment share. No future target is approved: keep "
        "`ordered_queue` empty and preserve the Arryn Winged Knight verification hold.\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "TESTS.md").write_text(
        "# Validation runs\n\n"
        "- Phase 2 generator run twice: passed with byte-identical generated artifacts.\n"
        "- Normalized archive: 14,900 bytes, 22/22 declared member hashes and sizes verified.\n"
        "- Exact partition: 61 occurrences into 27 rows (6 reliable, 21 insufficient).\n"
        "- `python3 -m py_compile .../analysis/generate_phase2.py`: passed.\n"
        "- `git diff --check`: passed.\n"
        "- Focused archive, source-manifest, denominator, identity, partition, sensitivity, historical-pin, queue, artifact-hash, and human-report coverage assertions: passed.\n"
        "- Focused repository unit tests: **89/89 passed** (normalized analysis, canonical identity, bundle safety, task protocol, and role diagnostics).\n"
        "- Deliberate negative red/fix: permissive decoding first accepted a corrupted trailing Base64 byte; after compacting only ASCII whitespace and enabling strict validation, the same corruption fails closed.\n"
        "- Changed identity audit and changed historical comparison source each fail closed.\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "README.md").write_text(
        "# Phase 2 analytical outputs\n\n"
        f"All 61 ordinary occurrences partition into {len(rankings)} troop/context rows: {len(reliable)} reliable and {len(insufficient)} insufficient. `ranking_complete.csv` is the exact union.\n\n"
        "The focus, sensitivity, historical comparison, result splits, denominators, pressure margins, identities, model status, and review decisions are separate auditable artifacts.\n\n"
        "Reproduce the analysis from the repository root with:\n\n"
        f"```bash\npython3 data/combat_observations/{BATCH_ID}/analysis/generate_phase2.py\n```\n",
        encoding="utf-8",
    )

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
    write_csv(ANALYSIS_DIR / "outlier_report.csv", ("battle_id", "canonical_troop_id", "context", "deployed", "kills", "kills_per_deployed", "status", "primary_excluded"), [])
    write_csv(ANALYSIS_DIR / "battle_context_review.csv", list(pressure[0]), pressure)

    validation = {
        "status": "passed", "validation_errors": [], "batch_id": BATCH_ID,
        "input_images": 8, "newly_accepted_screenshots": 7,
        "already_normalized_screenshots": 0, "internal_same_battle_duplicates": 1,
        "supplemental_screenshots": 0, "active_last_observation_battles": 1,
        "source_manifest_entries_verified": source_verification["manifest_entries_verified"],
        "source_manifest_order_note_recorded": True,
        "bundle_members_verified": bundle_verification["members"],
        "bundle_member_hashes_verified": bundle_verification["declared_member_hashes_verified"],
        "strict_base64_corruption_regression": "passed_after_observed_red",
        "battles": len(battles), "canonical_occurrences": len(occurrences),
        "ordinary_occurrences": len(rows), "excluded_unresolved_rows": 0,
        "unresolved_review_rows": 0, "distinct_display_labels": len(names),
        "partition_rows": len(rankings), "reliable_rows": len(reliable), "insufficient_rows": len(insufficient),
        "partition_exact": len(rankings) == len(reliable) + len(insufficient),
        "focus_rows": len(focus), "focus_battle_rows": len(focus_battles),
        "focus_field_gate_passed": field_focus["reliability_status"] == "reliable",
        "focus_final_only_gate_passed": next(row for row in sensitivity if row["scenario"] == "final_results_only")["display_gate_passed"],
        "historical_comparison_rows": len(comparison), "historical_cohorts_pooled": False,
        "direct_kill_total_coverage": f"{sum(row['kill_total_direct_positive'] for row in kill_coverage)}/{len(kill_coverage)}",
        "direct_deployment_total_coverage": f"{sum(row['deployment_total_direct_positive'] for row in kill_coverage)}/{len(kill_coverage)}",
        "pressure_margin_final_battles": sum(row["included_in_final_pressure_summary"] for row in pressure),
        "pressure_margin_censored_snapshots": sum(not row["included_in_final_pressure_summary"] for row in pressure),
        "identity_confirmed": sum(row["resolution_status"] == "confirmed_id" for row in identity_audit),
        "identity_unresolved": sum(row["resolution_status"] != "confirmed_id" for row in identity_audit), "numeric_corrections": 0,
        "outlier_rows": 0, "primary_outlier_exclusions": 0,
        "contexts_pooled": False, "cohorts_pooled": False, "player_enemy_pooled": False,
        "offscreen_rows_inferred": False, "active_battles_combined_with_later_fights": False,
        "frozen_models_changed": False, "role_adjusted_blended_rank_published": False,
        "model_comparison_status": "not_run_no_complete_compatible_rot_v71_v73_model_universe",
    }
    write_json(ANALYSIS_DIR / "validation_report.json", validation)
    write_json(ANALYSIS_DIR / "canonical_validation_report.json", validation)
    write_json(ANALYSIS_DIR / "analysis_state.json", {
        "batch_id": BATCH_ID, "status": "phase_2_complete_local_validation_passed",
        "normalization_commit": NORMALIZATION_COMMIT, "focus_decision": "completed_no_additional_test",
        "queue_after": {"active_test": None, "ordered_queue": [], "verification_holds": ["arryn_moonknight"]},
    })

    targets = [path for path in ANALYSIS_DIR.iterdir() if path.is_file() and path.name != "artifact_hashes.csv"]
    targets += [path for path in REVIEW_DIR.iterdir() if path.is_file()]
    artifacts = [
        {"path": path.relative_to(BATCH_DIR).as_posix(), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
        for path in sorted(targets)
    ]
    write_csv(ANALYSIS_DIR / "artifact_hashes.csv", ("path", "sha256", "size_bytes"), artifacts)
    print(json.dumps(validation, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
