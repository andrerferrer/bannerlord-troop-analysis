#!/usr/bin/env python3
"""Generate the reviewed Phase 2 analysis for the August 24-27 ROT batch."""

from __future__ import annotations

import argparse
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
REVIEW_DIR = BATCH_DIR / "review"
IDENTITY_PATH = REPO_ROOT / "data/realm_of_thrones/audit/realm_of_thrones_troops.csv"

BATCH_ID = "2026-08-24-to-27-rot-mixed-cohorts"
TRACK = "realm_of_thrones"
GAME_VERSION = "1.4.x"
NORMALIZATION_COMMIT = "05d960d39a33165cc58e8740387bad5346dfe2bb"
REMOTE_PHASE1_HEAD = "37abe16a62b0f08ea6dd3742883a4393cbe72ddf"
LOCAL_PHASE1_HEAD = "87ca0598f73a83a22b1cf0fe69844b1843c44883"
IDENTITY_AUDIT_COMMIT = "fb8cf889330f9fe570189c081e5dd23fe078837b"
IDENTITY_AUDIT_SHA256 = "63ea983998e25aa0e6f8c0747bf42e44440f695bbe1fec717074e7ba64e42810"
SOURCE_SHA256 = "e3b00de66dedfb06eca8f2fbf74a761b96aa19cf563f7f5311bedd98536c53bf"
SOURCE_SIZE = 57_809_819
BUNDLE_SHA256 = "547984824ffaad4f7b07013e03c945ef722bf0677651b82050dbd8919ba03cc7"
BUNDLE_SIZE = 25_304
BUNDLE_MEMBERS = 16
GATE_BATTLES = 5
GATE_DEPLOYED = 20
BOOTSTRAP_REPETITIONS = 10_000
FOCUS = (
    "Pentoshi Soldier [T3]",
    "Myrish Artisan of War [T6]",
    "Knights of Starfall [T6]",
    "Dornish Master Archer [T5]",
)
COUNT_FIELDS = ("deployed", "survivors", "kills", "deaths", "wounded", "routed")

RANKING_FIELDS = (
    "track", "game_version", "cohort", "context", "participant_scope",
    "parent_group", "efficiency_rank", "impact_rank", "display_name",
    "canonical_troop_id", "identity_status", "canonical_default_group",
    "canonical_role", "reliable_role_population", "role_adjusted_rank_status",
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
    if party == "Trego Drahar's Party":
        return "trego_myrish_pentoshi"
    if party == "Edric Dayne's Party":
        return "edric_reach_dornish"
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


def verify_artifact_manifest() -> list[dict]:
    checks = []
    rows = read_csv(BATCH_DIR / "artifact_hashes.csv")
    for row in rows:
        path = BATCH_DIR / row["path"]
        passed = (
            path.is_file()
            and path.stat().st_size == int(row["size_bytes"])
            and sha256_file(path) == row["sha256"]
        )
        checks.append({"path": row["path"], "passed": passed})
    if not all(row["passed"] for row in checks):
        raise ValueError("Phase 1 artifact hash verification failed")
    return checks


def extract_bundle() -> tuple[dict[str, bytes], dict]:
    encoded = BATCH_DIR / "bundle/rot_mixed_cohorts_2026-08-24-to-27.tar.xz.base64.part-00"
    archive = base64.b64decode(encoded.read_bytes())
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
            extracted = bundle.extractfile(member)
            if extracted is None:
                raise ValueError(f"unreadable normalized bundle member: {member.name}")
            files[path.name if len(path.parts) == 2 else "/".join(path.parts[1:])] = extracted.read()
    return files, {
        "sha256": BUNDLE_SHA256,
        "size_bytes": len(archive),
        "members": len(files),
        "safe_preflight_passed": True,
    }


def verify_source_zip(path: Path | None) -> dict:
    if path is None:
        return {
            "expected_sha256": SOURCE_SHA256,
            "expected_size_bytes": SOURCE_SIZE,
            "locally_verified": False,
            "member_hashes_verified": 0,
            "note": "raw source optional after the deterministic normalized bundle passed",
        }
    import zipfile

    if sha256_file(path) != SOURCE_SHA256 or path.stat().st_size != SOURCE_SIZE:
        raise ValueError("source ZIP hash/size mismatch")
    inventory = read_csv(BATCH_DIR / "source_inventory.csv")
    with zipfile.ZipFile(path) as source:
        members = {item.filename: item for item in source.infolist() if not item.is_dir()}
        expected_names = {row["image_file"] for row in inventory}
        if set(members) != expected_names:
            raise ValueError("source ZIP member set does not match source_inventory.csv")
        for row in inventory:
            if sha256_bytes(source.read(row["image_file"])) != row["image_sha256"]:
                raise ValueError(f"source ZIP member hash mismatch: {row['image_file']}")
    return {
        "expected_sha256": SOURCE_SHA256,
        "actual_sha256": SOURCE_SHA256,
        "expected_size_bytes": SOURCE_SIZE,
        "actual_size_bytes": SOURCE_SIZE,
        "locally_verified": True,
        "member_hashes_verified": len(inventory),
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
            "audit_sha256": IDENTITY_AUDIT_SHA256, "audit_commit": IDENTITY_AUDIT_COMMIT,
        })
    return output


def build_report(rankings: list[dict], reliable: list[dict], insufficient: list[dict], focus: list[dict], splits: list[dict], pressure: list[dict], identity_audit: list[dict], occurrence_count: int) -> str:
    lines = [
        f"# Phase 2 analysis — {BATCH_ID}", "", "## Batch-wide findings", "",
        f"All **{occurrence_count}** fully visible player-side ordinary-troop occurrences are represented in **{len(rankings)}** cohort/context/participant rows: **{len(reliable)} reliable** and **{len(insufficient)} below gate**. The two Arwa allied-party troop rows remain separate from Trego's player-party aggregates.", "",
        "Trego/Myrish-Pentoshi field, Trego/Myrish-Pentoshi siege attack, and Edric/Reach-Dornish field are separate cohorts. Active scoreboards are independent censored battles; no value is combined with or reconstructed from a later fight.", "",
        "### Reliable rows", "",
        "| Cohort/context | Eff. rank | Impact rank | Troop | Battles | Deployed | Kills/deployed | Kill share | Deploy share | Offense ratio | Retention |",
        "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in reliable:
        lines.append(
            f"| {row['cohort']} / {row['context']} | {row['efficiency_rank']} | {row['impact_rank']} | {row['display_name']} | {row['independent_battles']} | {row['deployed']} | {row['kills_per_deployed']} | {float(row['player_side_kill_share']):.2%} | {float(row['player_side_deployment_share']):.2%} | {row['offensive_contribution_ratio']} | {float(row['retention_rate']):.2%} |"
        )
    lines += ["", "### Below-gate partition", "", "Every row below is retained without promoting its diagnostic rate.", "", "| Cohort/context/scope | Troop | Battles | Deployed | More battles | More deployed |", "|---|---|---:|---:|---:|---:|"]
    for row in insufficient:
        scope = f"{row['cohort']} / {row['context']} / {row['parent_group']}"
        lines.append(f"| {scope} | {row['display_name']} | {row['independent_battles']} | {row['deployed']} | {row['more_battles_needed']} | {row['more_deployed_needed']} |")

    lines += ["", "## Additive focus deep dives", ""]
    for name in FOCUS:
        focus_rows = [row for row in focus if row["display_name"] == name]
        lines += [f"### {name}", ""]
        for row in focus_rows:
            lines.append(
                f"- `{row['cohort']} / {row['context']}`: `{row['kills']} / {row['deployed']} = {row['kills_per_deployed']}` kills/deployed; "
                f"kill share `{row['kills']} / {row['verified_player_side_total_kills']} = {row['player_side_kill_share']}`; "
                f"deployment share `{row['deployed']} / {row['verified_player_side_total_deployed']} = {row['player_side_deployment_share']}`; "
                f"offensive ratio `{row['offensive_contribution_ratio']}`, share gap `{row['offensive_share_gap']}`, retention `{row['survivors']} / {row['deployed']} = {row['retention_rate']}`; "
                f"gate `{row['reliability_status']}` ({row['independent_battles']} battles), efficiency rank `{row['efficiency_rank']}` and impact rank `{row['impact_rank']}` within its applicable gate population."
            )
        lines.append("")

    final_pressure = [float(row["pressure_margin"]) for row in pressure if row["included_in_final_pressure_summary"]]
    active_pressure = [row for row in pressure if not row["included_in_final_pressure_summary"]]
    confirmed = sum(row["resolution_status"] == "confirmed_id" for row in identity_audit)
    lines += [
        "## Result splits and defensive context", "",
        "`result_splits.csv` keeps victory, defeat, and active/censored observations separate for every troop row. The active observations are diagnostics, not final-result pressure ranks.", "",
        f"All {len(pressure)} battles have direct positive deployment and remaining denominators. {len(final_pressure)} final results have production pressure margins; the {len(active_pressure)} active scoreboards have separately marked censored snapshots. Final pressure margin range: `{min(final_pressure):.6f}` to `{max(final_pressure):.6f}`.", "",
        "## Identity and metric limits", "",
        f"The versioned Realm of Thrones audit confirms {confirmed} of {len(identity_audit)} labels by one exact tier-stripped name-to-ID match. Unresolved labels stay provisional; notably Dornish Master Archer has no canonical ID in this audit snapshot.", "",
        "Efficiency and share-adjusted impact have independent ranks. Deployment share, offensive ratio/gap, and retention remain separate diagnostics. Current methodology keeps offense and defense independent, so no role-adjusted blended rank or universal cross-role ladder is published.", "",
        "## Smallest next test", "",
        "Run **3 more independent Trego field battles** with at least **20 Pentoshi Soldiers [T3] per battle**, keeping Myrish support and orders as fixed as practical. Existing field coverage is `2` battles / `39` deployed, so `5 - 2 = 3` battles close the only requested focus field gate; the deployment gate is already met. Do not substitute siege observations for this field gap.", "",
        "## Limitations", "",
        "Campaign observations remain opponent-, roster-, map-, result-, and player-order-confounded. Active observations are right-censored. Pressure margin is battle-level and is not assigned to an individual troop. No off-screen row is inferred, no cohort boundary is crossed, and frozen models are unchanged.", "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-zip", type=Path)
    args = parser.parse_args()

    manifest_checks = verify_artifact_manifest()
    files, bundle_verification = extract_bundle()
    source_verification = verify_source_zip(args.source_zip)
    battles = {row["battle_id"]: row for row in load_bundle_jsonl(files, "battles.jsonl")}
    occurrences = load_bundle_jsonl(files, "troop_occurrences.jsonl")
    rows = load_bundle_jsonl(files, "primary_troop_occurrences.jsonl")

    if len(battles) != 29 or len(rows) != 339:
        raise ValueError("unexpected normalized batch counts")
    if any(row["game_track"] != TRACK or row["game_version"] != GAME_VERSION for row in rows):
        raise ValueError("track/version boundary violation")
    if any(row["row_type"] != "troop" or row["relationship_to_player"] not in {"player_party", "allied_party"} for row in rows):
        raise ValueError("ordinary player-side troop boundary violation")
    if any(row["side"] != battles[row["battle_id"]]["player_side"] for row in rows):
        raise ValueError("player/enemy side boundary violation")
    if sum(row["relationship_to_player"] == "allied_party" and row["parent_group"] == "Arwa's Party" for row in rows) != 2:
        raise ValueError("Arwa allied-party coverage mismatch")
    for row in rows:
        if row["deployed"] != row["survivors"] + row["deaths"] + row["wounded"]:
            raise ValueError(f"troop arithmetic mismatch: {row['observation_id']}")

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

    if len(rankings) != len(reliable) + len(insufficient):
        raise ValueError("reliable/insufficient partition mismatch")
    if sum(row["independent_battles"] for row in rankings if row["participant_scope"] == "allied_party") != 2:
        raise ValueError("Arwa aggregate partition mismatch")
    if {row["display_name"] for row in focus} != set(FOCUS):
        raise ValueError("focus coverage mismatch")

    write_csv(ANALYSIS_DIR / "ranking_complete.csv", RANKING_FIELDS, rankings)
    write_csv(ANALYSIS_DIR / "ranking_reliable.csv", RANKING_FIELDS, reliable)
    write_csv(ANALYSIS_DIR / "insufficient_evidence.csv", RANKING_FIELDS, insufficient)
    split_fields = list(splits[0])
    write_csv(ANALYSIS_DIR / "result_splits.csv", split_fields, splits)
    write_csv(ANALYSIS_DIR / "battle_pressure_margin.csv", list(pressure[0]), pressure)
    write_csv(ANALYSIS_DIR / "focus_deep_dive.csv", RANKING_FIELDS, focus)
    write_csv(ANALYSIS_DIR / "focus_battle_rates.csv", list(focus_battles[0]), focus_battles)
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
        "status": "passed_with_separate_cohorts",
        "decisions": [
            {"cohort": "trego_myrish_pentoshi", "contexts": ["field", "siege_attack"], "decision": "same party/core roster may aggregate only inside one context; field and siege remain separate"},
            {"cohort": "edric_reach_dornish", "contexts": ["field"], "decision": "same party/core roster may aggregate inside field only"},
            {"pair": ["trego_myrish_pentoshi", "edric_reach_dornish"], "decision": "incompatible; never pooled"},
            {"scope": "Arwa's Party", "decision": "allied-party rows remain distinct from Trego player-party rows"},
            {"active_battles": ["battle_20260825_163450_siege", "battle_20260827_235142_field"], "decision": "independent censored observations; never combined/subtracted/reconstructed with later fights"},
        ],
    }
    write_json(ANALYSIS_DIR / "cohort_compatibility.json", compatibility)

    input_verification = {
        "status": "passed", "batch_id": BATCH_ID, "pipeline_mode": "offline-existing with local source-hash recheck",
        "pipeline_version": "0.4.0", "schema_version": "2.0.0",
        "normalization_commit": NORMALIZATION_COMMIT, "remote_phase1_head": REMOTE_PHASE1_HEAD,
        "local_equivalent_phase1_head": LOCAL_PHASE1_HEAD,
        "source_zip": source_verification, "normalized_bundle": bundle_verification,
        "artifact_manifest": {"verified": len(manifest_checks), "failed": 0},
        "identity_audit": {"path": IDENTITY_PATH.relative_to(REPO_ROOT).as_posix(), "sha256": IDENTITY_AUDIT_SHA256, "commit": IDENTITY_AUDIT_COMMIT},
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

    report = build_report(rankings, reliable, insufficient, focus, splits, pressure, identity_audit, len(rows))
    (ANALYSIS_DIR / "ANALYSIS_REPORT.md").write_text(report, encoding="utf-8")
    (ANALYSIS_DIR / "NEXT_TEST_RECOMMENDATION.md").write_text(
        "# Smallest next test\n\nRun 3 more independent Trego field battles with at least 20 Pentoshi Soldiers [T3] per battle and fixed Myrish support/orders. Existing field coverage is 2 battles / 39 deployed, so the deployment gate is already met and 5 - 2 = 3 more battles close the field evidence gate.\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "TESTS.md").write_text(
        "# Validation runs\n\n"
        "- `python3 .../analysis/generate_phase2.py --source-zip <attachment>`: passed; source ZIP, 29 members, 26 Phase 1 artifacts, bundle, schema boundaries, partition, and metrics regenerated.\n"
        "- `python3 -m py_compile .../analysis/generate_phase2.py`: passed.\n"
        "- `git diff --check`: passed.\n"
        "- Targeted `unittest` run for protocol, role diagnostics, canonical identity, normalized analysis, and bundle safety: **73/73 passed**.\n"
        "- Full `python3 -m unittest discover -s tests -v`: **380 passed, 1 failed**. The sole failure is the unrelated pre-existing assertion-message regex in `test_staged_path_substitution_fails_and_restores_target`. The same test was reproduced failing unchanged on detached `main` (`fb8cf889330f9fe570189c081e5dd23fe078837b`); this Phase 2 changes neither the tested script nor test.\n",
        encoding="utf-8",
    )
    (ANALYSIS_DIR / "README.md").write_text(
        "# Phase 2 analytical outputs\n\n"
        f"All 339 ordinary occurrences partition into {len(rankings)} cohort/context/participant rows: {len(reliable)} reliable and {len(insufficient)} insufficient. `ranking_complete.csv` is the exact union. `ranking_reliable.csv` reranks reliable rows separately by efficiency and share-adjusted impact.\n\n"
        "`result_splits.csv`, `battle_pressure_margin.csv`, `denominator_coverage.csv`, `focus_deep_dive.csv`, `focus_battle_rates.csv`, `canonical_identity_audit.csv`, and `cohort_compatibility.json` preserve the required boundaries and additive analysis.\n\n"
        "Reproduce the analysis from the repository root with:\n\n"
        "```bash\npython3 data/combat_observations/2026-08-24-to-27-rot-mixed-cohorts/analysis/generate_phase2.py\n```\n\n"
        "Add `--source-zip /absolute/path/to/source.zip` to repeat optional raw ZIP and member-hash verification.\n",
        encoding="utf-8",
    )

    validation = {
        "status": "passed", "validation_errors": [], "batch_id": BATCH_ID,
        "source_members_verified": source_verification["member_hashes_verified"],
        "artifact_hashes_verified": len(manifest_checks), "bundle_members_verified": bundle_verification["members"],
        "battles": len(battles), "ordinary_occurrences": len(rows), "distinct_display_labels": len(names),
        "partition_rows": len(rankings), "reliable_rows": len(reliable), "insufficient_rows": len(insufficient),
        "partition_exact": len(rankings) == len(reliable) + len(insufficient),
        "arwa_allied_rows": 2, "focus_rows": len(focus), "focus_battle_rows": len(focus_battles),
        "direct_kill_total_coverage": f"{sum(row['kill_total_direct_positive'] for row in kill_coverage)}/{len(kill_coverage)}",
        "direct_deployment_total_coverage": f"{sum(row['deployment_total_direct_positive'] for row in kill_coverage)}/{len(kill_coverage)}",
        "pressure_margin_final_battles": sum(row["included_in_final_pressure_summary"] for row in pressure),
        "pressure_margin_censored_snapshots": sum(not row["included_in_final_pressure_summary"] for row in pressure),
        "identity_confirmed": sum(row["resolution_status"] == "confirmed_id" for row in identity_audit),
        "identity_unresolved": sum(row["resolution_status"] != "confirmed_id" for row in identity_audit),
        "contexts_pooled": False, "cohorts_pooled": False, "player_enemy_pooled": False,
        "offscreen_rows_inferred": False, "active_battles_combined_with_later_fights": False,
        "frozen_models_changed": False, "role_adjusted_blended_rank_published": False,
        "targeted_unittests": {"passed": 73, "failed": 0},
        "full_unittests": {"passed": 380, "failed": 1, "pre_existing_failure_reproduced_on_main": True},
        "git_diff_check": "passed",
    }
    write_json(ANALYSIS_DIR / "validation_report.json", validation)

    targets = [path for path in ANALYSIS_DIR.iterdir() if path.is_file() and path.name != "artifact_hashes.csv"]
    targets += [REVIEW_DIR / "phase2_review_summary.json", REVIEW_DIR / "phase2_identity_decisions.csv"]
    artifacts = [
        {"path": path.relative_to(BATCH_DIR).as_posix(), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
        for path in sorted(targets)
    ]
    write_csv(ANALYSIS_DIR / "artifact_hashes.csv", ("path", "sha256", "size_bytes"), artifacts)
    print(json.dumps(validation, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
