"""Mod-track OVERVIEW lists: full mod-owned ranks; no name/specials filters."""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT_ID = "export_20260731_150800"
sys.path.insert(0, str(REPO / "scripts" / "scoring"))

import write_theoretical_overview  # noqa: E402
from write_theoretical_overview import (  # noqa: E402
    HOLLOW_CRAFTED_COUNTS,
    LATEST_REPORT_END,
    LATEST_REPORT_START,
    assign_tiers_by_scores,
    count_hollow_crafted_rows,
    hollow_damage_banner,
    is_spectacle_outlier,
    rank_table,
    tier_letter_from_top_fraction,
    update_root_readme_latest_report,
    update_theoretical_readme_latest_report,
)


class _FakeFrame:
    """Minimal stand-in so rank_table tests run without pandas."""

    def __init__(self, rows: list[dict]):
        self._rows = rows
        self.columns = list(rows[0].keys()) if rows else []

    def __len__(self) -> int:
        return len(self._rows)

    def dropna(self, subset: list[str]) -> "_FakeFrame":
        col = subset[0]
        return _FakeFrame([r for r in self._rows if r.get(col) is not None])

    def sort_values(self, col: str, ascending: bool = True) -> "_FakeFrame":
        return _FakeFrame(
            sorted(self._rows, key=lambda r: r[col], reverse=not ascending)
        )

    def reset_index(self, drop: bool = True) -> "_FakeFrame":
        return self

    def insert(self, loc: int, column: str, value) -> None:
        for i, row in enumerate(self._rows):
            items = list(row.items())
            items.insert(loc, (column, value[i]))
            self._rows[i] = dict(items)
        if column not in self.columns:
            self.columns.insert(loc, column)

    def __getitem__(self, cols: list[str]) -> "_FakeFrame":
        return _FakeFrame([{c: r.get(c) for c in cols} for r in self._rows])


class TheoreticalOverviewTests(unittest.TestCase):
    def test_spectacle_outlier_detects_giants_not_dragonstone(self) -> None:
        self.assertTrue(is_spectacle_outlier("giant_rider", "Mammoth Riding Giant"))
        self.assertTrue(is_spectacle_outlier("elder_giant", "Elder Giant"))
        self.assertFalse(
            is_spectacle_outlier("dragonstone_elite_archer", "Dragonstone Elite Archer")
        )
        self.assertFalse(is_spectacle_outlier("greyjoy_sniper", "Greyjoy Sniper"))

    def test_spectacle_predicate_comes_from_the_owner_module(self) -> None:
        # ADR-005: zero duplicated regex left in the generator.
        source = Path(write_theoretical_overview.__file__).read_text(encoding="utf-8")
        self.assertNotIn("_SPECTACLE_RE", source)
        self.assertNotIn(r"\bgiants?\b", source)  # the pattern itself lives in outliers.py
        self.assertIn("from outliers import", source)
        import outliers

        self.assertIs(is_spectacle_outlier, outliers.is_spectacle_outlier)

    def test_hollow_damage_banner_counts_crafted_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            pack = repo / "analysis_pack" / "demo"
            pack.mkdir(parents=True)
            with (pack / "demo_troop_equipment_audit.csv").open(
                "w", newline="", encoding="utf-8"
            ) as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=["item_kind", "swing_damage", "thrust_damage"],
                )
                writer.writeheader()
                writer.writerow(
                    {"item_kind": "CraftedItem", "swing_damage": "", "thrust_damage": ""}
                )
                writer.writerow(
                    {"item_kind": "CraftedItem", "swing_damage": "", "thrust_damage": ""}
                )
                writer.writerow(
                    {"item_kind": "CraftedItem", "swing_damage": "70", "thrust_damage": ""}
                )
                writer.writerow(
                    {"item_kind": "Item", "swing_damage": "", "thrust_damage": "80"}
                )
            self.assertEqual(count_hollow_crafted_rows(repo, "demo"), (3, 2))
            banner = "\n".join(hollow_damage_banner(repo, "demo"))
            self.assertIn("Provenance limits", banner)
            self.assertIn("**2 of 3**", banner)
            self.assertIn("CraftedItem", banner)
            self.assertIn("template-name proxy", banner)

    def test_hollow_damage_banner_falls_back_to_documented_counts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.assertEqual(
                count_hollow_crafted_rows(repo, "taom"),
                (HOLLOW_CRAFTED_COUNTS["taom"], HOLLOW_CRAFTED_COUNTS["taom"]),
            )
            banner = "\n".join(hollow_damage_banner(repo, "taom"))
            for track, count in HOLLOW_CRAFTED_COUNTS.items():
                self.assertIn(f"{track} {count}", banner)

    def test_documented_hollow_counts_match_the_analysis_pack(self) -> None:
        for track, expected in HOLLOW_CRAFTED_COUNTS.items():
            path = (
                REPO
                / "analysis_pack"
                / track
                / f"{track}_troop_equipment_audit.csv"
            )
            if not path.is_file():
                self.skipTest(f"analysis_pack missing for {track}")
            crafted, hollow = count_hollow_crafted_rows(REPO, track)
            self.assertEqual(crafted, expected, track)
            self.assertEqual(hollow, expected, track)

    def test_tier_ladder_from_position(self) -> None:
        self.assertEqual(tier_letter_from_top_fraction(1.0), "S")
        self.assertEqual(tier_letter_from_top_fraction(0.90), "S")
        self.assertEqual(tier_letter_from_top_fraction(0.89), "A")
        self.assertEqual(tier_letter_from_top_fraction(0.70), "A")
        self.assertEqual(tier_letter_from_top_fraction(0.40), "B")
        self.assertEqual(tier_letter_from_top_fraction(0.20), "C")
        self.assertEqual(tier_letter_from_top_fraction(0.19), "D")
        self.assertEqual(assign_tiers_by_scores([88.0]), ["S"])
        self.assertEqual(assign_tiers_by_scores([88.0, 80.0])[0], "S")
        # 80/88 ≈ 0.91 → still S; 75/88 ≈ 0.85 → A
        self.assertEqual(assign_tiers_by_scores([88.0, 80.0])[1], "S")
        self.assertEqual(assign_tiers_by_scores([88.0, 75.0])[1], "A")
        # 50/88 ≈ 0.57 → B
        self.assertEqual(assign_tiers_by_scores([88.0, 50.0])[1], "B")

    def test_rank_table_includes_why_columns_when_present(self) -> None:
        frame = _FakeFrame(
            [
                {
                    "troop_name": "A",
                    "troop_id": "a",
                    "defensive_role_score": 90.0,
                    "defense_score_base": 80.0,
                    "armor_total": 120.0,
                    "effective_armor": 70.0,
                    "has_shield": True,
                    "has_horse": False,
                    "primary_category": "Defensive Troops",
                    "culture": "x",
                    "level": 21,
                    "line_status": "main_or_minor_line",
                }
            ]
        )
        out = rank_table(frame, "defensive_role_score")
        self.assertIn("armor_total", out.columns)
        self.assertIn("effective_armor", out.columns)
        self.assertIn("defense_score_base", out.columns)
        self.assertIn("tier", out.columns)
        self.assertEqual(out._rows[0]["tier"], "S")

    def test_rank_table_forced_splus_tier(self) -> None:
        frame = _FakeFrame(
            [
                {
                    "troop_name": "Mammoth Riding Giant",
                    "troop_id": "giant_rider",
                    "ranged_role_score": 100.0,
                    "primary_category": "Ranged Troops",
                    "culture": "freefolk",
                    "level": 31,
                    "line_status": "main_or_minor_line",
                }
            ]
        )
        out = rank_table(frame, "ranged_role_score", tier="S+")
        self.assertEqual(out._rows[0]["tier"], "S+")

    def test_rot_overview_keeps_mod_troops_drops_vanilla_baseline(self) -> None:
        path = (
            REPO
            / "analysis"
            / "theoretical"
            / "realm_of_thrones"
            / EXPORT_ID
            / "OVERVIEW.md"
        )
        self.assertTrue(path.is_file(), "run write_theoretical_overview.py first")
        text = path.read_text(encoding="utf-8")
        ranged_block = text.split("## Ranked — Ranged", 1)[1]
        if "## Outliers S+ — Ranged" in ranged_block:
            ranged = ranged_block.split("## Outliers S+ — Ranged", 1)[0]
        else:
            ranged = ranged_block.split("## Ranked —", 1)[0]
        self.assertIn("Myrish Artisan of War", ranged)
        self.assertIn("Ravens' Teeth", ranged)
        self.assertIn("Goldenheart Warrior", ranged)
        self.assertNotIn("Mammoth Riding Giant", ranged)
        self.assertNotIn("Khuzait Khan's Guard", ranged)
        self.assertNotIn("Battanian Fian Champion", ranged)
        self.assertIn("change_type=inalterado", text)
        self.assertNotIn("Drop troop names matching", text)

    def test_rot_overview_tiers_and_giant_outliers(self) -> None:
        path = (
            REPO
            / "analysis"
            / "theoretical"
            / "realm_of_thrones"
            / EXPORT_ID
            / "OVERVIEW.md"
        )
        text = path.read_text(encoding="utf-8")
        self.assertIn("## Tiers", text)
        ranged_block = text.split("## Ranked — Ranged", 1)[1]
        ranged_main = ranged_block.split("## Outliers S+ — Ranged", 1)[0]
        self.assertIn("| rank | tier |", ranged_main)
        self.assertIn("| S |", ranged_main)
        outliers = ranged_block.split("## Outliers S+ — Ranged", 1)[1].split(
            "## Ranked —", 1
        )[0]
        self.assertIn("Mammoth Riding Giant", outliers)
        self.assertIn("| S+ |", outliers)

    def test_rot_overview_includes_why_columns(self) -> None:
        path = (
            REPO
            / "analysis"
            / "theoretical"
            / "realm_of_thrones"
            / EXPORT_ID
            / "OVERVIEW.md"
        )
        text = path.read_text(encoding="utf-8")
        self.assertIn("## Why columns", text)
        defensive_block = text.split("## Ranked — Defensive", 1)[1]
        if "## Outliers S+ — Defensive" in defensive_block:
            defensive = defensive_block.split("## Outliers S+ — Defensive", 1)[0]
        else:
            defensive = defensive_block.split("## Ranked —", 1)[0]
        self.assertIn("armor_total", defensive)
        self.assertIn("effective_armor", defensive)
        self.assertIn("defense_score_base", defensive)
        ranged_block = text.split("## Ranked — Ranged", 1)[1]
        if "## Outliers S+ — Ranged" in ranged_block:
            ranged = ranged_block.split("## Outliers S+ — Ranged", 1)[0]
        else:
            ranged = ranged_block.split("## Ranked —", 1)[0]
        self.assertIn("ranged_damage", ranged)
        offensive_block = text.split("## Ranked — Offensive melee", 1)[1]
        if "## Outliers S+ — Offensive" in offensive_block:
            offensive = offensive_block.split("## Outliers S+ — Offensive", 1)[0]
        else:
            offensive = offensive_block.split("## Ranked —", 1)[0]
        self.assertIn("crafted_melee_template", offensive)

    def test_troop_scores_export_raw_why_fields(self) -> None:
        path = (
            REPO
            / "analysis"
            / "theoretical"
            / "realm_of_thrones"
            / EXPORT_ID
            / "realm_of_thrones_troop_role_scores_v1.csv"
        )
        self.assertTrue(path.is_file(), "run run_theoretical_role_scores.py first")
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertIn("armor_total", rows[0])
        self.assertIn("effective_armor", rows[0])
        self.assertIn("ranged_damage", rows[0])
        self.assertIn("throw_damage", rows[0])

    def test_human_input_doc_exists(self) -> None:
        path = REPO / "analysis" / "theoretical" / "HUMAN_INPUT.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("RoT field empiria", text)
        self.assertIn("TAOM item XML", text)
        self.assertIn("Resolved", text)

    def test_update_root_readme_rewrites_latest_report_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            readme = repo / "README.md"
            readme.write_text(
                "\n".join(
                    [
                        "# Bannerlord Troop Analysis",
                        "",
                        "## Start here",
                        "",
                        "- older link",
                        "",
                        LATEST_REPORT_START,
                        "stale content",
                        LATEST_REPORT_END,
                        "",
                        "## Batch workflow",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            update_root_readme_latest_report(repo, package_sha="abc123")
            text = readme.read_text(encoding="utf-8")
            self.assertIn(LATEST_REPORT_START, text)
            self.assertIn(LATEST_REPORT_END, text)
            self.assertNotIn("stale content", text)
            self.assertIn("analysis/theoretical/OVERVIEW_INDEX.md", text)
            self.assertIn(EXPORT_ID, text)
            self.assertIn(
                f"analysis/theoretical/realm_of_thrones/{EXPORT_ID}/OVERVIEW.md",
                text,
            )
            self.assertIn("Batch workflow", text)

    def test_root_readme_has_latest_report_markers(self) -> None:
        text = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertIn(LATEST_REPORT_START, text)
        self.assertIn(LATEST_REPORT_END, text)
        self.assertIn("analysis/theoretical/OVERVIEW_INDEX.md", text)

    def test_update_theoretical_readme_rewrites_latest_report_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = repo / "analysis" / "theoretical" / "README.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "\n".join(
                    [
                        "# Theoretical outputs",
                        "",
                        "- layout note",
                        "",
                        LATEST_REPORT_START,
                        "stale theoretical",
                        LATEST_REPORT_END,
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            update_theoretical_readme_latest_report(repo, package_sha="abc123")
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("stale theoretical", text)
            self.assertIn("[`OVERVIEW_INDEX.md`](OVERVIEW_INDEX.md)", text)
            self.assertIn(
                f"[`OVERVIEW.md`](realm_of_thrones/{EXPORT_ID}/OVERVIEW.md)",
                text,
            )
            self.assertNotIn("analysis/theoretical/OVERVIEW_INDEX.md", text)

    def test_theoretical_readme_has_latest_report_markers(self) -> None:
        text = (REPO / "analysis" / "theoretical" / "README.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(LATEST_REPORT_START, text)
        self.assertIn(LATEST_REPORT_END, text)
        self.assertIn("[`OVERVIEW_INDEX.md`](OVERVIEW_INDEX.md)", text)


if __name__ == "__main__":
    unittest.main()
