#!/usr/bin/env python3
"""Run role_scores_v1 into analysis/theoretical/ (I/O only; no scoring changes).

Verifies xml_ssot audit hashes, invokes generate_vanilla_role_scores.py unchanged,
then stamps ADR-004 evidence labels onto CSV outputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

TRACKS = ("nightmare_sails", "taom", "realm_of_thrones")
EXPORT_ID = "export_20260729_025002"
SCORER = Path("scripts/scoring/generate_vanilla_role_scores.py")

ROT_PRIORITY_ANCHORS = [
    "Ravens' Teeth",
    "Goldenheart Warrior",
    "Celtigar Banneret",
    "Lyseni Enforcer",
    "Myrish Artisan of War",
    "Golden Company Mahout",
    "Sarnori Spider",
    "Baratheon Hammerknight",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_hashes(repo: Path) -> dict[str, tuple[str, int]]:
    path = repo / "data" / "xml_exports" / EXPORT_ID / "artifact_hashes.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["path"]: (row["sha256"], int(row["bytes"])) for row in rows}


def verify_track_audits(repo: Path, track: str, hashes: dict[str, tuple[str, int]]) -> list[str]:
    audit_dir = repo / "data" / track / "audit"
    verified: list[str] = []
    for path in sorted(audit_dir.glob("*.csv")):
        rel = path.relative_to(repo).as_posix()
        if rel not in hashes:
            raise SystemExit(f"audit missing from artifact_hashes.csv: {rel}")
        expected_sha, expected_bytes = hashes[rel]
        actual_sha = sha256_file(path)
        actual_bytes = path.stat().st_size
        if actual_sha != expected_sha or actual_bytes != expected_bytes:
            raise SystemExit(
                f"hash preflight failed for {rel}: "
                f"expected sha={expected_sha} bytes={expected_bytes}, "
                f"got sha={actual_sha} bytes={actual_bytes}"
            )
        verified.append(rel)
    return verified


def stamp_evidence_basis(output_dir: Path) -> None:
    for path in sorted(output_dir.glob("*.csv")):
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
        if not rows:
            continue
        for key in ("evidence_basis", "empirical"):
            if key not in fieldnames:
                fieldnames.append(key)
        for row in rows:
            row["evidence_basis"] = "xml_structural"
            row["empirical"] = "false"
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


def write_readme(path: Path, track: str) -> None:
    path.write_text(
        "\n".join(
            [
                f"# Theoretical role_scores_v1 — `{track}`",
                "",
                "- `evidence_basis=xml_structural`",
                "- `empirical=false`",
                "- Governed by ADR-004; outside `bannerlord-analysis-task:v1`.",
                "- Model: `role_scores_v1` conservative (docs/methodology/003 + 004_role_scoring_v1).",
                "- Do not join these rows into empirical rankings.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_report(
    path: Path,
    track: str,
    verified: list[str],
    troop_count: int,
    package_sha: str,
) -> None:
    anchors = (
        ROT_PRIORITY_ANCHORS
        if track == "realm_of_thrones"
        else []
    )
    lines = [
        f"# Theoretical analysis — `{track}` / `{EXPORT_ID}`",
        "",
        "## Labels",
        "",
        "- Evidence basis: `xml_structural` (ADR-004)",
        "- Empirical: `false`",
        "- Model: `role_scores_v1` conservative proxy (not HTK/V4.x/V7.x)",
        "- Combat display gate (≥5 battles / ≥20 troops): applies to empirical",
        "  combat outputs only (ADR-004); this package has zero battle-derived quantities.",
        "",
        "## Inputs",
        "",
        f"- Export: `{EXPORT_ID}`",
        f"- Package digest: `{package_sha}`",
        f"- Track audit files verified against `artifact_hashes.csv`: {len(verified)}",
        "",
        "## Outputs",
        "",
        f"- Soldier/troop role rows scored: **{troop_count}**",
        "- Entrypoint: `scripts/scoring/generate_vanilla_role_scores.py` (unchanged scoring logic)",
        "",
        "## Sanity / anchors",
        "",
    ]
    if anchors:
        lines.append(
            "Priority empirical validation targets for this track "
            "(not cross-track controls):"
        )
        lines.append("")
        for name in anchors:
            lines.append(f"- {name}")
        lines.append("")
        lines.append(
            "Vanilla `CONTROL_IDS` do not transfer. Sanity CSV may be empty or sparse."
        )
    else:
        lines.append(
            "No canonical mod-track control set yet — treat rankings as "
            "**proxy-only**. Vanilla CONTROL_IDS do not transfer."
        )
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- Crafted melee uses conservative template proxy; no reconstructed HTK.",
            "- Heroes excluded from ordinary soldier scoring inputs via `is_soldier`.",
            "- Intra-track only; do not compare rankings across tracks.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def run_track(repo: Path, track: str, python: Path, hashes: dict[str, tuple[str, int]], package_sha: str) -> None:
    verified = verify_track_audits(repo, track, hashes)
    out = repo / "analysis" / "theoretical" / track / EXPORT_ID
    if out.exists():
        for child in out.iterdir():
            if child.is_file():
                child.unlink()
    out.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(python),
        str(repo / SCORER),
        "--audit-dir",
        str(repo / "data" / track / "audit"),
        "--output-dir",
        str(out),
        "--track",
        track,
    ]
    subprocess.run(cmd, check=True, cwd=repo)
    stamp_evidence_basis(out)
    troop_csv = out / f"{track}_troop_role_scores_v1.csv"
    with troop_csv.open(newline="", encoding="utf-8") as handle:
        troop_count = sum(1 for _ in csv.DictReader(handle))
    write_readme(out / "README.md", track)
    write_report(out / "REPORT.md", track, verified, troop_count, package_sha)
    meta = {
        "export_id": EXPORT_ID,
        "track": track,
        "package_kind_source": "xml_ssot_package",
        "expected_package_sha256": package_sha,
        "model": "role_scores_v1",
        "evidence_basis": "xml_structural",
        "empirical": False,
        "adr": "ADR-004",
        "verified_audit_files": verified,
        "troop_rows": troop_count,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"OK {track}: troops={troop_count} out={out}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--python", type=Path, default=Path(sys.executable))
    parser.add_argument(
        "--tracks",
        nargs="+",
        default=list(TRACKS),
        choices=list(TRACKS),
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    package = json.loads(
        (repo / "data" / "xml_exports" / EXPORT_ID / "PACKAGE.json").read_text(
            encoding="utf-8"
        )
    )
    package_sha = package["expected_package_sha256"]
    hashes = load_hashes(repo)
    for track in args.tracks:
        run_track(repo, track, args.python, hashes, package_sha)


if __name__ == "__main__":
    main()
