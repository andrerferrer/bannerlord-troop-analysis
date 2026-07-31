"""Write theoretical OVERVIEW.md files (mod troops only; no name/specials filters)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

EXPORT_ID = "export_20260729_025002"
TRACKS = ("nightmare_sails", "taom", "realm_of_thrones")
ROLE_COLS = [
    ("ranged_role_score", "Ranged"),
    ("defensive_role_score", "Defensive"),
    ("offensive_melee_role_score", "Offensive melee"),
    ("skirmisher_role_score", "Skirmisher"),
]
# Drivers + raw when present (melee crafted has no real weapon damage — template proxy only).
ROLE_WHY_COLS: dict[str, list[str]] = {
    "ranged_role_score": [
        "ranged_score_base",
        "ranged_damage",
        "ranged_item",
        "has_horse",
        "has_shield",
    ],
    "defensive_role_score": [
        "defense_score_base",
        "armor_total",
        "effective_armor",
        "has_shield",
        "has_horse",
    ],
    "offensive_melee_role_score": [
        "crafted_melee_score_base",
        "crafted_melee_template",
        "crafted_melee_item",
        "defense_score_base",
        "has_horse",
    ],
    "skirmisher_role_score": [
        "throw_score_base",
        "throw_damage",
        "direct_throw_item",
        "crafted_throw_item",
        "has_horse",
    ],
}
LATEST_REPORT_START = "<!-- latest-theoretical-report:start -->"
LATEST_REPORT_END = "<!-- latest-theoretical-report:end -->"

# Giants / mammoths sit outside normal troop scale — listed as S+ outliers, not S–D.
_SPECTACLE_RE = re.compile(r"(?i)\bgiants?\b|\bmammoths?\b|(^|_)giant(_|$)|(^|_)mammoth(_|$)")


def is_spectacle_outlier(troop_id: object, troop_name: object) -> bool:
    blob = f"{troop_id or ''} {troop_name or ''}"
    return bool(_SPECTACLE_RE.search(blob))


def tier_letter_from_top_fraction(frac: float) -> str:
    """Map 1.0=best … 0.0=worst within a role (non-outlier) list to S–D."""
    if frac >= 0.90:
        return "S"
    if frac >= 0.70:
        return "A"
    if frac >= 0.40:
        return "B"
    if frac >= 0.20:
        return "C"
    return "D"


def assign_tiers_by_scores(scores: list[float]) -> list[str]:
    """Tier by score vs the best non-outlier in this role list (1.0 = leader)."""
    if not scores:
        return []
    top = max(float(s) for s in scores)
    if top <= 0:
        return ["D"] * len(scores)
    return [tier_letter_from_top_fraction(float(s) / top) for s in scores]


def filter_mod_troops(df: Any, overrides: Any | None = None) -> Any:
    """Keep mod-added/overridden troops; drop untouched vanilla baseline only."""
    out = df.copy()
    if overrides is not None and not overrides.empty and "troop_id" in out.columns:
        keep = overrides.loc[
            ~overrides["change_type"].astype(str).eq("inalterado"),
            "troop_id",
        ]
        out = out[out["troop_id"].isin(set(keep))]
    return out


def split_spectacle_outliers(df: Any) -> tuple[Any, Any]:
    """Return (standard troops, giant/mammoth outliers)."""
    if df is None or len(df) == 0:
        return df, df

    def _flag(row: Any) -> bool:
        if hasattr(row, "get"):
            return is_spectacle_outlier(row.get("troop_id"), row.get("troop_name"))
        return is_spectacle_outlier(row["troop_id"], row["troop_name"])

    if hasattr(df, "apply"):
        mask = df.apply(_flag, axis=1)
        return df.loc[~mask].copy(), df.loc[mask].copy()
    # List-backed test frame
    standard_rows = [r for r in df._rows if not _flag(r)]
    outlier_rows = [r for r in df._rows if _flag(r)]
    return type(df)(standard_rows), type(df)(outlier_rows)


def rank_table(df: Any, col: str, *, tier: str | None = None) -> Any:
    ranked = df.dropna(subset=[col]).sort_values(col, ascending=False).reset_index(drop=True)
    ranked.insert(0, "rank", range(1, len(ranked) + 1))
    if tier is not None:
        ranked.insert(1, "tier", [tier] * len(ranked))
    else:
        if hasattr(ranked, "_rows"):
            scores = [float(r[col]) for r in ranked._rows]
        else:
            scores = [float(v) for v in list(ranked[col])]
        ranked.insert(1, "tier", assign_tiers_by_scores(scores))
    why = [c for c in ROLE_WHY_COLS.get(col, []) if c in ranked.columns]
    cols = [
        "rank",
        "tier",
        "troop_name",
        "troop_id",
        col,
        *why,
        "primary_category",
        "culture",
        "level",
        "line_status",
    ]
    return ranked[[c for c in cols if c in ranked.columns]]


def md_table(frame: Any) -> str:
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
    import pandas as pd

    out_dir = repo / "analysis" / "theoretical" / track / EXPORT_ID
    scores_path = out_dir / f"{track}_troop_role_scores_v1.csv"
    df = pd.read_csv(scores_path)
    override_path = repo / "data" / track / "audit" / f"{track}_override_report.csv"
    overrides = pd.read_csv(override_path) if override_path.is_file() else None
    filtered = filter_mod_troops(df, overrides=overrides)
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
        f"(excluded {excluded}: untouched vanilla `change_type=inalterado` only)",
        "",
        "## Tiers",
        "",
        "- Main tables: `rank` + `tier` in **S / A / B / C / D** vs the best "
        "non-outlier score in that role (~within 10% of the leader → S; then "
        "A/B/C/D)",
        "- **S+** = spectacle-scale outliers (giants / mammoths): listed in a "
        "separate section and **excluded** from the main S–D ladder so they do "
        "not crowd ordinary troop tiers",
        "",
        "## Why columns",
        "",
        "- **Defensive:** `defense_score_base` (driver) + `armor_total` / `effective_armor` "
        "(raw) + shield/horse flags",
        "- **Ranged:** `ranged_score_base` (driver) + `ranged_damage` (weapon+ammo thrust) "
        "+ item + horse/shield",
        "- **Offensive melee:** `crafted_melee_score_base` + template/item "
        "(**no real weapon damage** — template proxy only)",
        "- **Skirmisher:** `throw_score_base` + `throw_damage` when the throw item is a "
        "direct `Thrown` weapon (crafted javelins stay proxy-only)",
        "",
        "## Filters",
        "",
        "- Drop `change_type=inalterado` from the track override report "
        "(vanilla baseline troops the mod did not add/override)",
        "- No name filters on Greyjoy / specials; giants/mammoths → S+ outliers section",
        "- Full ranked lists below — filter locally as needed",
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
    standard, outliers = split_spectacle_outliers(filtered)
    for col, label in ROLE_COLS:
        table = rank_table(standard, col)
        lines.append(f"## Ranked — {label} ({len(table)} troops)")
        lines.append("")
        lines.append(md_table(table))
        lines.append("")
        outlier_table = rank_table(outliers, col, tier="S+")
        if len(outlier_table) > 0:
            lines.append(
                f"## Outliers S+ — {label} ({len(outlier_table)} giants/mammoths)"
            )
            lines.append("")
            lines.append(
                "Spectacle-scale units; excluded from the S–D ladder above."
            )
            lines.append("")
            lines.append(md_table(outlier_table))
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
        f"| `nightmare_sails` | [OVERVIEW.md](nightmare_sails/{EXPORT_ID}/OVERVIEW.md) | 9 battles; **7 reliable** rows (see combat batch analysis) |",
        f"| `realm_of_thrones` | [OVERVIEW.md](realm_of_thrones/{EXPORT_ID}/OVERVIEW.md) | Follow-up 2 battles; **below** 5/20 display gate |",
        f"| `taom` | [OVERVIEW.md](taom/{EXPORT_ID}/OVERVIEW.md) | No field batch yet; item XML mostly absent in export |",
        "",
        "Human blockers: [HUMAN_INPUT.md](HUMAN_INPUT.md).",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def latest_report_readme_block(package_sha: str, *, link_prefix: str) -> str:
    """Build the marked latest-report section with links under ``link_prefix``."""
    short = package_sha[:12] if package_sha else "unknown"
    prefix = link_prefix.rstrip("/")
    if prefix:
        prefix = prefix + "/"

    def href(rel: str) -> str:
        return f"{prefix}{rel}"

    index_rel = "OVERVIEW_INDEX.md"
    human_rel = "HUMAN_INPUT.md"
    ns_rel = f"nightmare_sails/{EXPORT_ID}/OVERVIEW.md"
    rot_rel = f"realm_of_thrones/{EXPORT_ID}/OVERVIEW.md"
    taom_rel = f"taom/{EXPORT_ID}/OVERVIEW.md"
    return "\n".join(
        [
            LATEST_REPORT_START,
            "## Latest theoretical report",
            "",
            f"Export `{EXPORT_ID}` · package `{short}…` · model `role_scores_v1` "
            "(XML-structural; not empiria).",
            "",
            f"- Index: [`{href(index_rel)}`]({href(index_rel)})",
            f"- Nightmare Sails: [`OVERVIEW.md`]({href(ns_rel)})",
            f"- Realm of Thrones: [`OVERVIEW.md`]({href(rot_rel)})",
            f"- TAOM: [`OVERVIEW.md`]({href(taom_rel)})",
            f"- Human blockers: [`HUMAN_INPUT.md`]({href(human_rel)})",
            "",
            "Regenerated by `python3 scripts/scoring/write_theoretical_overview.py`.",
            LATEST_REPORT_END,
        ]
    )


def _rewrite_latest_report_block(
    path: Path,
    package_sha: str,
    *,
    link_prefix: str,
    insert_before: str | None,
) -> Path:
    text = path.read_text(encoding="utf-8")
    block = latest_report_readme_block(package_sha, link_prefix=link_prefix)
    pattern = re.compile(
        re.escape(LATEST_REPORT_START) + r".*?" + re.escape(LATEST_REPORT_END),
        re.DOTALL,
    )
    if pattern.search(text):
        text = pattern.sub(block, text, count=1)
    elif insert_before and insert_before in text:
        text = text.replace(insert_before, block + "\n\n" + insert_before, 1)
    else:
        text = text.rstrip() + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8")
    return path


def update_root_readme_latest_report(repo: Path, package_sha: str) -> Path:
    """Keep root README pointed at the current theoretical OVERVIEW export."""
    return _rewrite_latest_report_block(
        repo / "README.md",
        package_sha,
        link_prefix="analysis/theoretical",
        insert_before="## Batch workflow",
    )


def update_theoretical_readme_latest_report(repo: Path, package_sha: str) -> Path:
    """Mirror the latest-report block into analysis/theoretical/README.md."""
    return _rewrite_latest_report_block(
        repo / "analysis" / "theoretical" / "README.md",
        package_sha,
        link_prefix="",
        insert_before=None,
    )


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
    print(f"wrote {update_root_readme_latest_report(repo, package_sha)}")
    print(f"wrote {update_theoretical_readme_latest_report(repo, package_sha)}")


if __name__ == "__main__":
    main()
