"""Write filtered theoretical OVERVIEW.md files (no giants/specials noise)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd

EXPORT_ID = "export_20260729_025002"
TRACKS = ("nightmare_sails", "taom", "realm_of_thrones")
ROLE_COLS = [
    ("ranged_role_score", "Ranged"),
    ("defensive_role_score", "Defensive"),
    ("offensive_melee_role_score", "Offensive melee"),
    ("skirmisher_role_score", "Skirmisher"),
]
SPECTACLE_NAME = re.compile(
    r"(?:Giant|Mammoth|Dragon|Direwolf|Kraken)",
    re.IGNORECASE,
)


def filter_playable(df: pd.DataFrame, overrides: pd.DataFrame | None = None) -> pd.DataFrame:
    out = df.copy()
    if "line_status" in out.columns:
        out = out[~out["line_status"].astype(str).eq("special_or_unlinked")]
    if "troop_name" in out.columns:
        out = out[
            ~out["troop_name"].astype(str).map(lambda name: bool(SPECTACLE_NAME.search(name)))
        ]
    # Mod-track overviews should not list untouched vanilla baseline troops
    # (e.g. Khan's Guard / Fian on the RoT track).
    if overrides is not None and not overrides.empty and "troop_id" in out.columns:
        keep = overrides.loc[
            ~overrides["change_type"].astype(str).eq("inalterado"),
            "troop_id",
        ]
        out = out[out["troop_id"].isin(set(keep))]
    return out


def top_table(df: pd.DataFrame, col: str, n: int = 20) -> pd.DataFrame:
    ranked = df.dropna(subset=[col]).sort_values(col, ascending=False).head(n)
    ranked = ranked.reset_index(drop=True)
    ranked.insert(0, "rank", range(1, len(ranked) + 1))
    cols = ["rank", "troop_name", "troop_id", col, "primary_category", "culture", "level"]
    return ranked[[c for c in cols if c in ranked.columns]]


def md_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No rows._\n"
    cols = list(frame.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join("---" for _ in cols) + " |",
    ]
    for row in frame.itertuples(index=False):
        cells = []
        for value in row:
            if isinstance(value, float):
                cells.append(f"{value:.1f}")
            else:
                cells.append(str(value))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def write_track_overview(repo: Path, track: str, package_sha: str) -> Path:
    out_dir = repo / "analysis" / "theoretical" / track / EXPORT_ID
    scores_path = out_dir / f"{track}_troop_role_scores_v1.csv"
    df = pd.read_csv(scores_path)
    override_path = repo / "data" / track / "audit" / f"{track}_override_report.csv"
    overrides = pd.read_csv(override_path) if override_path.is_file() else None
    filtered = filter_playable(df, overrides=overrides)
    excluded = len(df) - len(filtered)

    lines = [
        f"# Troop overview — `{track}` / `{EXPORT_ID}`",
        "",
        "## Labels",
        "",
        "- `evidence_basis=xml_structural`, `empirical=false` (ADR-004)",
        "- Model: `role_scores_v1` conservative (crafted melee = proxy, not HTK)",
        f"- Package digest: `{package_sha}`",
        f"- Rows scored: **{len(df)}**; after filters: **{len(filtered)}** "
        f"(excluded {excluded}: specials, spectacle names, and untouched vanilla "
        f"`change_type=inalterado`)",
        "",
        "## Filters",
        "",
        "- Drop `line_status=special_or_unlinked`",
        "- Drop troop names matching Giant / Mammoth / Dragon / Direwolf / Kraken",
        "- Drop `change_type=inalterado` from the track override report "
        "(vanilla baseline troops that the mod did not add/override)",
        "- Intra-track only; do not compare ranks across tracks",
        "",
    ]
    if track == "nightmare_sails":
        empiria = (
            repo
            / "data/combat_observations/2026-07-28-to-29-nightmare-sails-field/analysis"
            / "ranking_reliable.csv"
        )
        if empiria.is_file():
            rel = pd.read_csv(empiria)
            lines.extend(
                [
                    "## Field empiria (reliable rows only)",
                    "",
                    "From `2026-07-28-to-29-nightmare-sails-field` — descriptive "
                    "kills/deployed, not the same as role_scores_v1.",
                    "",
                    md_table(rel.head(20)),
                    "",
                ]
            )
    for col, label in ROLE_COLS:
        lines.append(f"## Top 20 — {label}")
        lines.append("")
        lines.append(md_table(top_table(filtered, col, 20)))
        lines.append("")

    path = out_dir / "OVERVIEW.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_index(repo: Path, package_sha: str) -> Path:
    path = repo / "analysis" / "theoretical" / "OVERVIEW_INDEX.md"
    lines = [
        "# Theoretical troop overview index",
        "",
        f"Export `{EXPORT_ID}` · package `{package_sha}` · model `role_scores_v1`.",
        "",
        "| Track | Overview | Empiria field status |",
        "|---|---|---|",
        "| `nightmare_sails` | [OVERVIEW.md](nightmare_sails/export_20260729_025002/OVERVIEW.md) | 9 battles; **7 reliable** rows (see combat batch analysis) |",
        "| `realm_of_thrones` | [OVERVIEW.md](realm_of_thrones/export_20260729_025002/OVERVIEW.md) | Follow-up 2 battles; **below** 5/20 display gate |",
        "| `taom` | [OVERVIEW.md](taom/export_20260729_025002/OVERVIEW.md) | No field batch yet; item XML mostly absent in export |",
        "",
        "Human blockers: [HUMAN_INPUT.md](HUMAN_INPUT.md).",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_human_input(repo: Path) -> Path:
    path = repo / "analysis" / "theoretical" / "HUMAN_INPUT.md"
    path.write_text(
        "\n".join(
            [
                "# Human input required",
                "",
                "Agent can keep shipping theoretical overviews and gates without these.",
                "The items below are blocked on Andre (or new PC exports / battles).",
                "",
                "## Blockers",
                "",
                "1. **TAOM item XML export** — current zip has almost no TAOM `Item`/`CraftedItem`",
                "   definitions, so melee/armor overview is hollow (2243 allowlisted IDs).",
                "   Need a new export that includes TAOM item modules/files.",
                "2. **RoT field empiria to display gate** — need ≥5 independent field battles",
                "   and ≥20 deployed for the priority S-tier set (Ravens, Goldenheart, Myrish,",
                "   Celtigar, Lyseni Enforcer, Mahout, Sarnori Spider, Hammerknight).",
                "   Current follow-up is only 2 battles / 0 reliable rows.",
                "3. **NS empiria expansion (optional)** — 7 reliable rows exist; more battles",
                "   improve intervals and cover naval/marine lines if those are the goal.",
                "4. **V4.4 / exact-item profiles** — dedicated model-change PR + profiles;",
                "   not required for role_scores_v1 overview.",
                "",
                "## Not blocked (agent can do)",
                "",
                "- Refresh filtered `OVERVIEW.md` after audit/score rebuilds",
                "- Unknown-item gate / catalog maintenance when XML is present",
                "- NS theory↔field join notes when names match reliable empiria rows",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    repo = args.repo.resolve()
    package = json.loads(
        (repo / "data" / "xml_exports" / EXPORT_ID / "PACKAGE.json").read_text(
            encoding="utf-8"
        )
    )
    package_sha = package["expected_package_sha256"]
    for track in TRACKS:
        path = write_track_overview(repo, track, package_sha)
        print(f"wrote {path}")
    print(f"wrote {write_index(repo, package_sha)}")
    print(f"wrote {write_human_input(repo)}")


if __name__ == "__main__":
    main()
