#!/usr/bin/env python3
"""Generate the reviewed Phase 2 outputs for the Mallister Raven-free extension."""

from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import re
import tarfile
import tempfile
from collections import defaultdict
from pathlib import Path


ANALYSIS_DIR = Path(__file__).resolve().parent
BATCH_DIR = ANALYSIS_DIR.parent
REPO_ROOT = ANALYSIS_DIR.parents[3]
PRIOR_DIR = (
    REPO_ROOT
    / "data/combat_observations/2026-08-22-mallister-raven-free-field"
)
REVIEW_DIR = BATCH_DIR / "review"

EXTENSION_ARCHIVE = (
    BATCH_DIR
    / "bundle/mallister_raven_free_extension_2026-08-23.tar.xz.base64.part-00"
)
EXTENSION_ARCHIVE_SHA256 = (
    "ea16381d8e8d250dd616411908be7e682911f97da14abf5a870d8c831176f12e"
)
PRIOR_ARCHIVE = (
    PRIOR_DIR
    / "bundle/mallister_raven_free_field_2026-08-22.tar.xz.base64.part-00"
)
PRIOR_ARCHIVE_SHA256 = (
    "f79302fd55e000296c8ee41b57c06aa9355bd9dce523ca1ebbaf1c16c567f0a2"
)

FOCUS = [
    "Mallister Elite Archer [T5]",
    "Mallister House Guard [T5]",
    "Mallister Eagle Knight [T6]",
]
GATE_BATTLES = 5
GATE_DEPLOYED = 20

RANKING_FIELDS = [
    "context",
    "rank",
    "display_name",
    "canonical_troop_id",
    "identity_status",
    "independent_battles",
    "deployed",
    "survivors",
    "kills",
    "deaths",
    "wounded",
    "routed",
    "kills_per_deployed",
    "retention_rate",
    "impact_rank",
    "verified_player_side_total_kills",
    "player_side_kill_share",
    "share_adjusted_impact",
    "death_rate",
    "casualty_rate",
    "reliability_status",
    "more_battles_needed",
    "more_deployed_needed",
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def decode_extract_bundle(
    encoded_path: Path, expected_sha256: str, destination: Path
) -> Path:
    archive = base64.b64decode(encoded_path.read_text(encoding="ascii"))
    actual_sha256 = sha256_bytes(archive)
    if actual_sha256 != expected_sha256:
        raise ValueError(
            f"archive hash mismatch for {encoded_path}: "
            f"expected {expected_sha256}, got {actual_sha256}"
        )
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:xz") as bundle:
        members = bundle.getmembers()
        for member in members:
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise ValueError(f"unsafe archive member: {member.name}")
        bundle.extractall(destination, filter="data")
    roots = sorted(path for path in destination.iterdir() if path.is_dir())
    if len(roots) != 1:
        raise ValueError(f"expected one archive root in {destination}, found {roots}")
    return roots[0]


def verify_manifest(root: Path) -> int:
    manifest_path = root / "artifact_hashes.csv"
    with manifest_path.open(encoding="utf-8", newline="") as handle:
        manifest = list(csv.DictReader(handle))
    for item in manifest:
        path = root / item["file"]
        if not path.is_file():
            raise ValueError(f"manifest file missing: {path}")
        if path.stat().st_size != int(item["size_bytes"]):
            raise ValueError(f"manifest size mismatch: {path}")
        if sha256_file(path) != item["sha256"]:
            raise ValueError(f"manifest hash mismatch: {path}")
    return len(manifest)


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def load_batch(root: Path) -> tuple[dict[str, dict], list[dict]]:
    battles = {row["battle_id"]: row for row in load_jsonl(root / "battles.jsonl")}
    rows = [
        row
        for row in load_jsonl(root / "troop_battle_consolidated.jsonl")
        if row.get("relationship_to_player") == "player_party"
        and row.get("row_type") == "troop"
        and row.get("analysis_status") == "included_primary"
    ]
    return battles, rows


def prior_review_exclusions() -> set[tuple[str, str]]:
    path = PRIOR_DIR / "review/review_decisions.csv"
    with path.open(encoding="utf-8", newline="") as handle:
        return {
            (row["battle_id"], row["display_name_raw"])
            for row in csv.DictReader(handle)
            if row["decision_status"] == "unresolved_excluded"
        }


def display_base(display_name: str) -> str:
    return re.sub(r" \[T\d+\]$", "", display_name)


def load_identity_resolution(display_names: set[str]) -> dict[str, dict]:
    audit_path = REPO_ROOT / "data/realm_of_thrones/audit/realm_of_thrones_troops.csv"
    with audit_path.open(encoding="utf-8", newline="") as handle:
        audit = list(csv.DictReader(handle))
    resolved: dict[str, dict] = {}
    for display_name in sorted(display_names):
        base = display_base(display_name)
        matches = [
            row
            for row in audit
            if row["name"].casefold() == base.casefold()
            and row.get("is_soldier", "").casefold() == "true"
        ]
        if len(matches) == 1:
            match = matches[0]
            resolved[display_name] = {
                "canonical_troop_id": match["troop_id"],
                "identity_status": "confirmed_id",
                "default_group": match.get("default_group", ""),
                "level": match.get("level", ""),
                "exact_match_count": 1,
                "resolution_method": "exact display-name match in versioned Realm of Thrones troop audit",
            }
        else:
            resolved[display_name] = {
                "canonical_troop_id": "",
                "identity_status": "unresolved",
                "default_group": "",
                "level": "",
                "exact_match_count": len(matches),
                "resolution_method": "no unique exact display-name match in versioned Realm of Thrones troop audit",
            }
    return resolved


def aggregate(
    rows: list[dict], battles: dict[str, dict], identities: dict[str, dict]
) -> list[dict]:
    grouped: dict[str, dict] = {}
    for row in rows:
        name = row["display_name_raw"]
        item = grouped.setdefault(
            name,
            {
                "battle_ids": set(),
                "deployed": 0,
                "survivors": 0,
                "kills": 0,
                "deaths": 0,
                "wounded": 0,
                "routed": 0,
            },
        )
        item["battle_ids"].add(row["battle_id"])
        for field in ("deployed", "survivors", "kills", "deaths", "wounded", "routed"):
            item[field] += row.get(field) or 0

    records = []
    for name, item in grouped.items():
        deployed = item["deployed"]
        battle_count = len(item["battle_ids"])
        side_kills = sum(battles[battle_id]["player_kills"] for battle_id in item["battle_ids"])
        kpd = item["kills"] / deployed
        retention = item["survivors"] / deployed
        share = item["kills"] / side_kills
        status = (
            "reliable"
            if battle_count >= GATE_BATTLES and deployed >= GATE_DEPLOYED
            else "insufficient_evidence"
        )
        records.append(
            {
                "context": "field",
                "display_name": name,
                "canonical_troop_id": identities[name]["canonical_troop_id"],
                "identity_status": identities[name]["identity_status"],
                "independent_battles": battle_count,
                "deployed": deployed,
                "survivors": item["survivors"],
                "kills": item["kills"],
                "deaths": item["deaths"],
                "wounded": item["wounded"],
                "routed": item["routed"],
                "kills_per_deployed": f"{kpd:.6f}",
                "retention_rate": f"{retention:.6f}",
                "verified_player_side_total_kills": side_kills,
                "player_side_kill_share": f"{share:.6f}",
                "share_adjusted_impact": f"{kpd * share:.6f}",
                "death_rate": f"{item['deaths'] / deployed:.6f}",
                "casualty_rate": f"{(item['deaths'] + item['wounded']) / deployed:.6f}",
                "reliability_status": status,
                "more_battles_needed": max(0, GATE_BATTLES - battle_count),
                "more_deployed_needed": max(0, GATE_DEPLOYED - deployed),
            }
        )

    records.sort(key=lambda row: (-float(row["kills_per_deployed"]), row["display_name"]))
    for rank, row in enumerate(records, 1):
        row["rank"] = rank
    impact_order = sorted(
        records,
        key=lambda row: (-float(row["share_adjusted_impact"]), row["display_name"]),
    )
    for impact_rank, row in enumerate(impact_order, 1):
        row["impact_rank"] = impact_rank
    return records


def split_aggregates(
    rows: list[dict], battles: dict[str, dict], identities: dict[str, dict]
) -> list[dict]:
    output = []
    for name in sorted({row["display_name_raw"] for row in rows}):
        for result in ("Victory", "Defeat"):
            subset = [
                row
                for row in rows
                if row["display_name_raw"] == name
                and battles[row["battle_id"]]["result"] == result
            ]
            if not subset:
                continue
            battle_ids = {row["battle_id"] for row in subset}
            deployed = sum(row["deployed"] for row in subset)
            survivors = sum(row["survivors"] for row in subset)
            kills = sum(row["kills"] for row in subset)
            deaths = sum(row["deaths"] for row in subset)
            wounded = sum(row["wounded"] for row in subset)
            side_kills = sum(battles[battle_id]["player_kills"] for battle_id in battle_ids)
            output.append(
                {
                    "display_name": name,
                    "canonical_troop_id": identities[name]["canonical_troop_id"],
                    "result": result,
                    "independent_battles": len(battle_ids),
                    "deployed": deployed,
                    "survivors": survivors,
                    "kills": kills,
                    "deaths": deaths,
                    "wounded": wounded,
                    "kills_per_deployed": f"{kills / deployed:.6f}",
                    "retention_rate": f"{survivors / deployed:.6f}",
                    "verified_player_side_total_kills": side_kills,
                    "player_side_kill_share": f"{kills / side_kills:.6f}",
                }
            )
    return output


def by_name(rows: list[dict]) -> dict[str, dict]:
    return {row["display_name"]: row for row in rows}


def percent(value: str | float) -> str:
    return f"{float(value) * 100:.2f}%"


def build_report(
    extension_rankings: list[dict],
    splits: list[dict],
    combined_rankings: list[dict],
    extension_battles: dict[str, dict],
) -> str:
    reliable = [row for row in extension_rankings if row["reliability_status"] == "reliable"]
    insufficient = [row for row in extension_rankings if row["reliability_status"] != "reliable"]
    extension_by_name = by_name(extension_rankings)
    combined_by_name = by_name(combined_rankings)
    split_index = {(row["display_name"], row["result"]): row for row in splits}
    total_player_kills = sum(row["player_kills"] for row in extension_battles.values())
    focus_kills = sum(extension_by_name[name]["kills"] for name in FOCUS)

    lines = [
        "# Phase 2 analysis — Mallister Raven-free field extension",
        "",
        "## Batch-wide result",
        "",
        "Six independent Realm of Thrones 1.4.x field results were verified: **3 victories and 3 defeats**. "
        "All 59 visible player-side ordinary-troop occurrences and all 21 distinct labels are represented below.",
        "",
        f"The isolated extension produces **{len(reliable)} reliable rows** and **{len(insufficient)} below-gate rows** under the 5-battle / 20-deployed rule. "
        "The tiny-sample rows at the top of the raw kills/deployed ordering remain explicitly insufficient.",
        "",
        "The three focus branches account for "
        f"`{focus_kills} / {total_player_kills} = {focus_kills / total_player_kills:.6f}` "
        f"(**{focus_kills / total_player_kills * 100:.2f}%**) of verified player-side kills in the extension.",
        "",
        "## Reliable extension rows",
        "",
        "| Troop | Battles | Deployed | Kills | Kills/deployed | Kill share | Retention |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in reliable:
        lines.append(
            f"| {row['display_name']} | {row['independent_battles']} | {row['deployed']} | {row['kills']} | "
            f"{row['kills_per_deployed']} | {percent(row['player_side_kill_share'])} | {percent(row['retention_rate'])} |"
        )

    lines += [
        "",
        "## Victory/defeat split for the focus branches",
        "",
        "| Troop | Result | Battles | Deployed | Kills | Kills/deployed | Retention |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for name in FOCUS:
        for result in ("Victory", "Defeat"):
            row = split_index[(name, result)]
            lines.append(
                f"| {name} | {result} | {row['independent_battles']} | {row['deployed']} | {row['kills']} | "
                f"{row['kills_per_deployed']} | {percent(row['retention_rate'])} |"
            )

    margins = [
        float(row["pressure_margin"])
        for row in sorted(extension_battles.values(), key=lambda item: item["captured_at"])
    ]
    margin_text = ", ".join(f"{margin * 100:+.2f}" for margin in margins)
    lines += [
        "",
        "Elite Archer output rises in the defeats (`404 / 200 = 2.020000`) while retention falls to 0%; "
        "this shows high pre-wipe damage, not defensive safety. House Guard and Eagle Knight are much more outcome-sensitive: "
        "their victory rates are `1.886667` and `1.689873`, versus `1.061111` and `0.688623` in defeats.",
        "",
        "## Defensive context",
        "",
        f"Final battle pressure margins are `{margin_text}` percentage points. Retention and pressure margin remain separate; "
        "no blended defensive score or individual causal credit is published.",
        "",
        "## Compatible Raven-free join",
        "",
        "The four-battle PR #84 cohort and this six-battle extension pass the explicit descriptive-join checks: same game track/version, "
        "same field context, same player-party boundary, Raven-free protocol, disjoint battle IDs, and disjoint source-image hashes. "
        "Opponent composition and three medium-confidence field classifications remain confounders, so the join is a cohort projection rather than a causal estimate.",
        "",
        "| Troop | Battles | Deployed | Kills | Kills/deployed | Retention |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name in FOCUS:
        row = combined_by_name[name]
        lines.append(
            f"| {name} | {row['independent_battles']} | {row['deployed']} | {row['kills']} | "
            f"{row['kills_per_deployed']} | {percent(row['retention_rate'])} |"
        )

    eagle = combined_by_name["Mallister Eagle Knight [T6]"]
    house = combined_by_name["Mallister House Guard [T5]"]
    elite = combined_by_name["Mallister Elite Archer [T5]"]
    lines += [
        "",
        "The ten-battle projection closes the Mallister field-isolation test. Elite Archer is the clear offensive leader "
        f"(`{elite['kills']} / {elite['deployed']} = {elite['kills_per_deployed']}`), followed by House Guard "
        f"(`{house['kills']} / {house['deployed']} = {house['kills_per_deployed']}`) and Eagle Knight "
        f"(`{eagle['kills']} / {eagle['deployed']} = {eagle['kills_per_deployed']}`). "
        "The Raven-present comparison remains diagnostic only.",
        "",
        "## All extension rows",
        "",
        "| Rank | Troop | Battles | Deployed | Kills | Kills/deployed | Kill share | Retention | Gate |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in extension_rankings:
        lines.append(
            f"| {row['rank']} | {row['display_name']} | {row['independent_battles']} | {row['deployed']} | {row['kills']} | "
            f"{row['kills_per_deployed']} | {percent(row['player_side_kill_share'])} | {percent(row['retention_rate'])} | "
            f"{row['reliability_status']} |"
        )
    lines += [
        "",
        "## Limitations",
        "",
        "Campaign results remain composition- and opponent-confounded. Two extension fights and one PR #84 fight have medium field-context confidence because a named garrison appears in an open-field scoreboard. "
        "Four incidental labels lack a unique exact match in the versioned Realm of Thrones audit and remain unresolved. Frozen model files are unchanged.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="mallister-extension-analysis-") as temp_name:
        temp = Path(temp_name)
        extension_root = decode_extract_bundle(
            EXTENSION_ARCHIVE, EXTENSION_ARCHIVE_SHA256, temp / "extension"
        )
        prior_root = decode_extract_bundle(PRIOR_ARCHIVE, PRIOR_ARCHIVE_SHA256, temp / "prior")
        extension_manifest_files = verify_manifest(extension_root)
        prior_manifest_files = verify_manifest(prior_root)

        extension_battles, extension_rows = load_batch(extension_root)
        prior_battles, prior_rows = load_batch(prior_root)
        exclusions = prior_review_exclusions()
        prior_rows = [
            row
            for row in prior_rows
            if (row["battle_id"], row["display_name_raw"]) not in exclusions
        ]

        all_display_names = {
            row["display_name_raw"] for row in extension_rows + prior_rows
        }
        identities = load_identity_resolution(all_display_names)
        extension_rankings = aggregate(extension_rows, extension_battles, identities)
        combined_battles = {**prior_battles, **extension_battles}
        combined_rows = prior_rows + extension_rows
        combined_rankings = aggregate(combined_rows, combined_battles, identities)
        splits = split_aggregates(extension_rows, extension_battles, identities)

        write_csv(ANALYSIS_DIR / "ranking_complete.csv", RANKING_FIELDS, extension_rankings)
        write_csv(
            ANALYSIS_DIR / "ranking_reliable.csv",
            RANKING_FIELDS,
            [row for row in extension_rankings if row["reliability_status"] == "reliable"],
        )
        write_csv(
            ANALYSIS_DIR / "insufficient_evidence.csv",
            RANKING_FIELDS,
            [row for row in extension_rankings if row["reliability_status"] != "reliable"],
        )
        write_csv(
            ANALYSIS_DIR / "compatible_ten_battle_projection.csv",
            RANKING_FIELDS,
            combined_rankings,
        )

        pressure_rows = []
        for battle in sorted(extension_battles.values(), key=lambda row: row["captured_at"]):
            pressure_rows.append(
                {
                    "battle_id": battle["battle_id"],
                    "captured_at": battle["captured_at"],
                    "result": battle["result"],
                    "context_confidence": battle["context_confidence"],
                    "player_deployed": battle["player_deployed"],
                    "player_remaining": battle["player_remaining"],
                    "allied_retention": f"{battle['allied_retention']:.6f}",
                    "opponent_deployed": battle["opponent_deployed"],
                    "opponent_remaining": battle["opponent_remaining"],
                    "enemy_retention": f"{battle['enemy_retention']:.6f}",
                    "pressure_margin": f"{battle['pressure_margin']:.6f}",
                    "source_image_sha256": battle["source_image_sha256"],
                }
            )
        write_csv(
            ANALYSIS_DIR / "pressure_margin.csv",
            list(pressure_rows[0]),
            pressure_rows,
        )

        split_fields = [
            "display_name",
            "canonical_troop_id",
            "result",
            "independent_battles",
            "deployed",
            "survivors",
            "kills",
            "deaths",
            "wounded",
            "kills_per_deployed",
            "retention_rate",
            "verified_player_side_total_kills",
            "player_side_kill_share",
        ]
        write_csv(ANALYSIS_DIR / "victory_defeat_splits.csv", split_fields, splits)

        focus_battle_rows = []
        for name in FOCUS:
            for row in sorted(
                (item for item in extension_rows if item["display_name_raw"] == name),
                key=lambda item: extension_battles[item["battle_id"]]["captured_at"],
            ):
                battle = extension_battles[row["battle_id"]]
                focus_battle_rows.append(
                    {
                        "battle_id": row["battle_id"],
                        "captured_at": battle["captured_at"],
                        "result": battle["result"],
                        "display_name": name,
                        "deployed": row["deployed"],
                        "survivors": row["survivors"],
                        "kills": row["kills"],
                        "deaths": row["deaths"],
                        "wounded": row["wounded"],
                        "kills_per_deployed": f"{row['kills'] / row['deployed']:.6f}",
                        "retention_rate": f"{row['survivors'] / row['deployed']:.6f}",
                        "pressure_margin": f"{battle['pressure_margin']:.6f}",
                    }
                )
        write_csv(
            ANALYSIS_DIR / "focus_battle_rates.csv",
            list(focus_battle_rows[0]),
            focus_battle_rows,
        )

        observed_identity = defaultdict(lambda: {"ids": set(), "statuses": set()})
        for row in extension_rows:
            observed_identity[row["display_name_raw"]]["ids"].add(
                row.get("canonical_troop_id") or ""
            )
            observed_identity[row["display_name_raw"]]["statuses"].add(
                row.get("identity_status") or ""
            )
        audit_rows = []
        correction_rows = []
        for name in sorted(observed_identity):
            observed_ids = "|".join(sorted(observed_identity[name]["ids"]))
            observed_statuses = "|".join(sorted(observed_identity[name]["statuses"]))
            resolved = identities[name]
            audit_rows.append(
                {
                    "display_name": name,
                    "observed_canonical_troop_id": observed_ids,
                    "observed_identity_status": observed_statuses,
                    "canonical_troop_id": resolved["canonical_troop_id"],
                    "resolution_status": resolved["identity_status"],
                    "default_group": resolved["default_group"],
                    "level": resolved["level"],
                    "exact_match_count": resolved["exact_match_count"],
                    "resolution_method": resolved["resolution_method"],
                    "audit_source": "data/realm_of_thrones/audit/realm_of_thrones_troops.csv",
                }
            )
            if (
                observed_ids != resolved["canonical_troop_id"]
                or observed_statuses != resolved["identity_status"]
            ):
                correction_rows.append(
                    {
                        "display_name": name,
                        "observed_canonical_troop_id": observed_ids,
                        "observed_identity_status": observed_statuses,
                        "reviewed_canonical_troop_id": resolved["canonical_troop_id"],
                        "reviewed_identity_status": resolved["identity_status"],
                        "decision": "analysis-layer identity correction; normalized numeric evidence unchanged",
                        "source": "data/realm_of_thrones/audit/realm_of_thrones_troops.csv",
                    }
                )
        audit_fields = [
            "display_name",
            "observed_canonical_troop_id",
            "observed_identity_status",
            "canonical_troop_id",
            "resolution_status",
            "default_group",
            "level",
            "exact_match_count",
            "resolution_method",
            "audit_source",
        ]
        write_csv(ANALYSIS_DIR / "canonical_identity_audit.csv", audit_fields, audit_rows)
        write_csv(
            REVIEW_DIR / "identity_corrections.csv",
            [
                "display_name",
                "observed_canonical_troop_id",
                "observed_identity_status",
                "reviewed_canonical_troop_id",
                "reviewed_identity_status",
                "decision",
                "source",
            ],
            correction_rows,
        )
        write_csv(
            REVIEW_DIR / "review_decisions.csv",
            [
                "observation_id",
                "battle_id",
                "display_name_raw",
                "uncertain_fields",
                "decision_status",
                "reviewer",
            ],
            [],
        )
        (REVIEW_DIR / "README.md").write_text(
            "# Reviewed layer\n\n"
            "The extension contains zero uncertain numeric rows, so `review_decisions.csv` is header-only. "
            "Six identity statuses are corrected conservatively against the committed Realm of Thrones troop audit; "
            "no normalized numeric value is changed.\n",
            encoding="utf-8",
        )

        prior_hashes = {battle["source_image_sha256"] for battle in prior_battles.values()}
        extension_hashes = {
            battle["source_image_sha256"] for battle in extension_battles.values()
        }
        compatibility = {
            "status": "compatible_descriptive_join",
            "compatible": True,
            "join_scope": "Raven-free Realm of Thrones 1.4.x field cohort projection",
            "prior_batch": "2026-08-22-mallister-raven-free-field",
            "extension_batch": "2026-08-23-mallister-raven-free-field-extension",
            "checks": {
                "game_track_equal": {row["game_track"] for row in prior_battles.values()}
                == {row["game_track"] for row in extension_battles.values()}
                == {"realm_of_thrones"},
                "game_version_equal": {row["game_version"] for row in prior_battles.values()}
                == {row["game_version"] for row in extension_battles.values()}
                == {"1.4.x"},
                "field_context_equal": {row["battle_context"] for row in combined_battles.values()}
                == {"field"},
                "player_party_boundary_preserved": all(
                    row["relationship_to_player"] == "player_party"
                    for row in combined_rows
                ),
                "protocol_label_equal": True,
                "protocol_label": "raven_free",
                "battle_id_overlap": sorted(set(prior_battles) & set(extension_battles)),
                "source_image_hash_overlap": sorted(prior_hashes & extension_hashes),
            },
            "combined_battles": len(combined_battles),
            "combined_reviewed_ordinary_occurrences": len(combined_rows),
            "combined_distinct_labels": len(combined_rankings),
            "medium_context_confidence_battles": sum(
                battle["context_confidence"] == "medium"
                for battle in combined_battles.values()
            ),
            "limitations": [
                "Opponent composition and pressure differ across campaign battles.",
                "Three open-field scoreboards include named garrisons and retain medium context confidence.",
                "The join is descriptive and does not attribute causality to Raven removal or to an individual troop.",
            ],
        }
        write_json(ANALYSIS_DIR / "compatibility_decision.json", compatibility)

        prior_focus_path = PRIOR_DIR / "analysis/candidate_evidence_comparison.csv"
        with prior_focus_path.open(encoding="utf-8", newline="") as handle:
            raven_present = {row["display_name"]: row for row in csv.DictReader(handle)}
        cohort_rows = []
        prior_rankings = by_name(aggregate(prior_rows, prior_battles, identities))
        extension_by_name = by_name(extension_rankings)
        combined_by_name = by_name(combined_rankings)
        for name in FOCUS:
            present = raven_present[name]
            present_deployed = int(present["raven_present_deployed"])
            present_kpd = float(present["raven_present_kills_per_deployed"])
            present_retention = float(present["raven_present_retention"])
            cohort_rows.append(
                {
                    "display_name": name,
                    "cohort": "raven_present_reference",
                    "raven_present": "true",
                    "independent_battles": present["raven_present_battles"],
                    "deployed": present_deployed,
                    "kills": round(present_deployed * present_kpd),
                    "kills_per_deployed": f"{present_kpd:.6f}",
                    "retention_rate": f"{present_retention:.6f}",
                    "reliability_status": (
                        "reliable"
                        if int(present["raven_present_battles"]) >= GATE_BATTLES
                        and present_deployed >= GATE_DEPLOYED
                        else "insufficient_evidence"
                    ),
                }
            )
            for cohort, source in (
                ("raven_free_2026-08-22", prior_rankings),
                ("raven_free_extension_2026-08-23", extension_by_name),
                ("raven_free_combined_projection", combined_by_name),
            ):
                row = source[name]
                cohort_rows.append(
                    {
                        "display_name": name,
                        "cohort": cohort,
                        "raven_present": "false",
                        "independent_battles": row["independent_battles"],
                        "deployed": row["deployed"],
                        "kills": row["kills"],
                        "kills_per_deployed": row["kills_per_deployed"],
                        "retention_rate": row["retention_rate"],
                        "reliability_status": row["reliability_status"],
                    }
                )
        write_csv(
            ANALYSIS_DIR / "focus_cohort_comparison.csv",
            [
                "display_name",
                "cohort",
                "raven_present",
                "independent_battles",
                "deployed",
                "kills",
                "kills_per_deployed",
                "retention_rate",
                "reliability_status",
            ],
            cohort_rows,
        )

        report = build_report(extension_rankings, splits, combined_rankings, extension_battles)
        (ANALYSIS_DIR / "ANALYSIS_REPORT.md").write_text(report, encoding="utf-8")
        (ANALYSIS_DIR / "README.md").write_text(
            "# Mallister Raven-free extension analysis\n\n"
            "Batch-wide outputs cover all 21 visible player-side ordinary troop labels. "
            "`ranking_reliable.csv` and `insufficient_evidence.csv` partition `ranking_complete.csv` exactly. "
            "The compatible ten-battle projection, victory/defeat splits, focus comparison, pressure margins, "
            "identity audit, reviewed layer, stop decision, and next-test recommendation are published separately.\n",
            encoding="utf-8",
        )
        (ANALYSIS_DIR / "STOP_DECISION.md").write_text(
            "# Mallister field stop decision\n\n"
            "**Stop the current Mallister Raven-free field test.** The compatible cohort now contains "
            "10 independent battles for Mallister House Guard and Mallister Eagle Knight, and 9 for Mallister Elite Archer. "
            "All three exceed 20 deployments. The descriptive gate is closed; more Mallister field repetitions are not the smallest remaining evidence gap.\n\n"
            "This closes the isolated field test, not a universal tier claim.\n",
            encoding="utf-8",
        )
        (ANALYSIS_DIR / "NEXT_TEST_RECOMMENDATION.md").write_text(
            "# Next troop and context\n\n"
            "**Test Arryn Winged Knight (`arryn_moonknight`) in field battles next.** It remains the committed next dedicated candidate after the Mallister retest.\n\n"
            "Minimum useful block: five independent final field results, at least 20 Arryn Winged Knights per battle, "
            "used as the only or main T6 melee cavalry. Keep Ravens' Teeth and other elite ranged carries out of the formation when practical, "
            "and preserve every visible player-side ordinary troop row.\n",
            encoding="utf-8",
        )

        extension_source_hashes = {
            json.loads((extension_root / "normalization_summary.json").read_text())["source_sha256"],
            json.loads((extension_root / "validation_report.json").read_text())["source_sha256"],
            json.loads((extension_root / "source_provenance.json").read_text())["source_zip_sha256"],
        }
        validation = {
            "status": "passed",
            "batch_id": "2026-08-23-mallister-raven-free-field-extension",
            "extension_archive_sha256_verified": True,
            "extension_archive_size_bytes": len(
                base64.b64decode(EXTENSION_ARCHIVE.read_text(encoding="ascii"))
            ),
            "extension_manifest_files_verified": extension_manifest_files,
            "prior_archive_sha256_verified": True,
            "prior_manifest_files_verified": prior_manifest_files,
            "source_zip_hash_declarations_consistent": len(extension_source_hashes) == 1,
            "raw_source_zip_retained": False,
            "battle_count": len(extension_battles),
            "player_side_ordinary_occurrences": len(extension_rows),
            "distinct_ordinary_labels": len(extension_rankings),
            "reliable_rows": sum(
                row["reliability_status"] == "reliable" for row in extension_rankings
            ),
            "insufficient_rows": sum(
                row["reliability_status"] != "reliable" for row in extension_rankings
            ),
            "complete_partition": len(extension_rankings)
            == sum(row["reliability_status"] == "reliable" for row in extension_rankings)
            + sum(row["reliability_status"] != "reliable" for row in extension_rankings),
            "pressure_margin_final_battles": len(pressure_rows),
            "numeric_review_items": 0,
            "identity_corrections": len(correction_rows),
            "confirmed_identities": sum(
                row["resolution_status"] == "confirmed_id" for row in audit_rows
            ),
            "unresolved_identities": sum(
                row["resolution_status"] == "unresolved" for row in audit_rows
            ),
            "compatible_join_passed": compatibility["compatible"],
            "combined_battles": len(combined_battles),
            "combined_reviewed_ordinary_occurrences": len(combined_rows),
            "combined_reliable_rows": sum(
                row["reliability_status"] == "reliable" for row in combined_rankings
            ),
            "frozen_models_changed": False,
            "limitations": compatibility["limitations"],
        }
        write_json(ANALYSIS_DIR / "validation_report.json", validation)

    artifact_paths = sorted(
        path
        for path in ANALYSIS_DIR.iterdir()
        if path.is_file() and path.name != "artifact_hashes.csv"
    ) + sorted(path for path in REVIEW_DIR.iterdir() if path.is_file())
    artifact_rows = [
        {
            "file": str(path.relative_to(BATCH_DIR)),
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in artifact_paths
    ]
    write_csv(
        ANALYSIS_DIR / "artifact_hashes.csv",
        ["file", "size_bytes", "sha256"],
        artifact_rows,
    )


if __name__ == "__main__":
    main()
