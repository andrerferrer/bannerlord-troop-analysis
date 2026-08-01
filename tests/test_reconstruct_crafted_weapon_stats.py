"""reconstruct_crafted_weapon_stats: formula path + blocked paths.

The formula path runs against a small synthetic piece/template catalog so the arithmetic
is checkable by hand. The blocked paths assert the honesty contract: a missing or
structurally insufficient catalog must exit non-zero and must NOT leave an output file
behind, and no stat may ever be zero-filled.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "normalization" / "reconstruct_crafted_weapon_stats.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("reconstruct_crafted_weapon_stats", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


rcws = _load_module()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


PIECE_FIELDS = list(rcws.PIECE_REQUIRED_COLUMNS)
TEMPLATE_FIELDS = list(rcws.TEMPLATE_REQUIRED_COLUMNS)


def piece(piece_id, piece_type, **kwargs) -> dict:
    row = {name: "" for name in PIECE_FIELDS}
    row["piece_id"] = piece_id
    row["piece_type"] = piece_type
    row["source_xml"] = "Native/ModuleData/crafting_pieces.xml"
    row["source_module"] = "Native"
    row.update(kwargs)
    return row


def template(template_id, **kwargs) -> dict:
    row = {name: "" for name in TEMPLATE_FIELDS}
    row["template_id"] = template_id
    row["source_xml"] = "Native/ModuleData/crafting_templates.xml"
    row["source_module"] = "Native"
    row.update(kwargs)
    return row


class Fixture:
    """A synthetic track audit directory plus synthetic catalogs."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.audit_dir = root / "audit"
        self.piece_catalog = root / "crafting_pieces_stats.csv"
        self.template_catalog = root / "crafting_templates_stats.csv"
        self.output = root / "out.csv"

    def write_composition(self, rows: list[dict]) -> None:
        write_csv(
            self.audit_dir / "vanilla_crafted_item_pieces.csv",
            list(rcws.PIECES_JOIN_COLUMNS),
            rows,
        )

    def write_items(self, rows: list[dict]) -> None:
        write_csv(
            self.audit_dir / "vanilla_items_crafted.csv",
            ["item_id", "name", "crafting_template"],
            rows,
        )

    def write_pieces(self, rows: list[dict], fieldnames: list[str] | None = None) -> None:
        write_csv(self.piece_catalog, fieldnames or PIECE_FIELDS, rows)

    def write_templates(self, rows: list[dict], fieldnames: list[str] | None = None) -> None:
        write_csv(self.template_catalog, fieldnames or TEMPLATE_FIELDS, rows)

    def run(self, *extra: str, with_template: bool = True) -> tuple[int, str, str]:
        argv = [
            "--track",
            "vanilla",
            "--audit-dir",
            str(self.audit_dir),
            "--piece-catalog",
            str(self.piece_catalog),
            "--output",
            str(self.output),
        ]
        if with_template:
            argv += ["--template-catalog", str(self.template_catalog)]
        argv += list(extra)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = rcws.main(argv)
        return code, out.getvalue(), err.getvalue()


def default_fixture(root: Path) -> Fixture:
    """Two crafted items with hand-checkable arithmetic.

    good_sword: Blade(scale 110) + Handle(scale 100) + Guard(blank scale)
        weapon_length = 80*1.10 + 30*1.00 + 6*1.00 = 88 + 30 + 6 = 124
        weight        = 1.5*1.10 + 0.6 + 0.2       = 1.65 + 0.8   = 2.45
        swing_damage  = floor(100 * 0.90 * 1.10) = floor(99.0)  = 99
        thrust_damage = floor( 80 * 0.50 * 1.10) = floor(44.0)  = 44
        speed_rating  = round( 95 * 0.95 * 1.10) = round(99.275) = 99

    orphan_axe: its only piece is absent from the piece catalog.
    """
    fixture = Fixture(root)
    fixture.write_composition(
        [
            {
                "item_id": "good_sword",
                "piece_id": "blade_a",
                "piece_type": "Blade",
                "scale_factor": "110",
            },
            {
                "item_id": "good_sword",
                "piece_id": "handle_a",
                "piece_type": "Handle",
                "scale_factor": "100",
            },
            {
                "item_id": "good_sword",
                "piece_id": "guard_a",
                "piece_type": "Guard",
                "scale_factor": "",
            },
            {
                "item_id": "orphan_axe",
                "piece_id": "blade_missing",
                "piece_type": "Blade",
                "scale_factor": "100",
            },
        ]
    )
    fixture.write_items(
        [
            {
                "item_id": "good_sword",
                "name": "Good Sword",
                "crafting_template": "OneHandedSword",
            },
            {
                "item_id": "orphan_axe",
                "name": "Orphan Axe",
                "crafting_template": "OneHandedAxe",
            },
        ]
    )
    fixture.write_pieces(
        [
            piece(
                "blade_a",
                "Blade",
                length="80",
                weight="1.5",
                swing_damage_factor="0.90",
                thrust_damage_factor="0.50",
                swing_damage_type="Cut",
                thrust_damage_type="Pierce",
                swing_speed_factor="0.95",
            ),
            piece("handle_a", "Handle", length="30", weight="0.6"),
            piece("guard_a", "Guard", length="6", weight="0.2"),
        ]
    )
    fixture.write_templates(
        [
            template(
                "OneHandedSword",
                weapon_class="OneHandedSword",
                swing_damage_base="100",
                thrust_damage_base="80",
                speed_rating_base="95",
                swing_damage_type="Cut",
                thrust_damage_type="Pierce",
            ),
            template(
                "OneHandedAxe",
                weapon_class="OneHandedAxe",
                swing_damage_base="90",
                thrust_damage_base="0",
                speed_rating_base="88",
            ),
        ]
    )
    return fixture


class FormulaPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.fixture = default_fixture(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _rows(self) -> dict[str, dict[str, str]]:
        code, stdout, stderr = self.fixture.run()
        self.assertEqual(code, 0, f"expected success; stderr={stderr}")
        self.assertTrue(self.fixture.output.is_file())
        return {row["item_id"]: row for row in read_csv(self.fixture.output)}

    def test_computes_damage_length_weight_and_speed(self) -> None:
        row = self._rows()["good_sword"]
        self.assertEqual(row["swing_damage"], "99")
        self.assertEqual(row["thrust_damage"], "44")
        self.assertEqual(row["speed_rating"], "99")
        self.assertEqual(row["weapon_length"], "124")
        self.assertEqual(float(row["weight"]), 2.45)
        self.assertEqual(row["swing_damage_type"], "Cut")
        self.assertEqual(row["thrust_damage_type"], "Pierce")
        self.assertEqual(row["weapon_class"], "OneHandedSword")
        self.assertEqual(row["blade_piece_id"], "blade_a")

    def test_marks_reconstructed_only_for_computed_rows(self) -> None:
        rows = self._rows()
        self.assertEqual(rows["good_sword"]["crafted_stats_reconstructed"], "True")
        self.assertEqual(rows["good_sword"]["stat_source"], rcws.SRC_FULL)
        self.assertEqual(rows["orphan_axe"]["crafted_stats_reconstructed"], "False")
        self.assertEqual(rows["orphan_axe"]["stat_source"], rcws.SRC_UNRESOLVED_PIECES)

    def test_unresolved_item_is_blank_never_zero(self) -> None:
        row = self._rows()["orphan_axe"]
        for column in (
            "swing_damage",
            "thrust_damage",
            "speed_rating",
            "weapon_length",
            "weight",
        ):
            self.assertEqual(row[column], "", f"{column} must be blank, not zero-filled")
        self.assertTrue(row["blocked_reason"])

    def test_provenance_columns_are_populated(self) -> None:
        expected_sha = hashlib.sha256(self.fixture.piece_catalog.read_bytes()).hexdigest()
        for row in self._rows().values():
            self.assertEqual(row["formula_version"], "piece_composition_v1")
            self.assertEqual(row["piece_catalog_sha256"], expected_sha)
            self.assertEqual(len(row["template_catalog_sha256"]), 64)
            self.assertEqual(row["track"], "vanilla")
            self.assertEqual(row["export_id"], rcws.DEFAULT_EXPORT_ID)
            self.assertTrue(row["stat_source"])

    def test_scale_factor_is_applied_and_blank_defaults_to_100(self) -> None:
        self.assertEqual(rcws.scale_of({"scale_factor": "110"}), 1.10)
        self.assertEqual(rcws.scale_of({"scale_factor": ""}), 1.0)
        self.assertEqual(rcws.scale_of({}), 1.0)
        self.assertEqual(rcws.scale_of({"scale_factor": "0"}), 1.0)

    def test_blade_choice_is_deterministic(self) -> None:
        """Two blades: the higher swing_damage_factor wins regardless of row order."""
        self.fixture.write_composition(
            [
                {
                    "item_id": "good_sword",
                    "piece_id": "blade_weak",
                    "piece_type": "Blade",
                    "scale_factor": "100",
                },
                {
                    "item_id": "good_sword",
                    "piece_id": "blade_a",
                    "piece_type": "Blade",
                    "scale_factor": "100",
                },
            ]
        )
        self.fixture.write_pieces(
            [
                piece(
                    "blade_weak",
                    "Blade",
                    length="10",
                    weight="0.1",
                    swing_damage_factor="0.10",
                    thrust_damage_factor="0.10",
                    swing_speed_factor="0.10",
                ),
                piece(
                    "blade_a",
                    "Blade",
                    length="80",
                    weight="1.5",
                    swing_damage_factor="0.90",
                    thrust_damage_factor="0.50",
                    swing_damage_type="Cut",
                    thrust_damage_type="Pierce",
                    swing_speed_factor="0.95",
                ),
            ]
        )
        row = self._rows()["good_sword"]
        self.assertEqual(row["blade_piece_id"], "blade_a")
        self.assertEqual(row["swing_damage"], "90")

    def test_output_is_deterministic(self) -> None:
        code, _, _ = self.fixture.run()
        self.assertEqual(code, 0)
        first = self.fixture.output.read_bytes()
        code, _, _ = self.fixture.run()
        self.assertEqual(code, 0)
        self.assertEqual(first, self.fixture.output.read_bytes())

    def test_rows_are_sorted_by_item_id(self) -> None:
        code, _, _ = self.fixture.run()
        self.assertEqual(code, 0)
        ids = [row["item_id"] for row in read_csv(self.fixture.output)]
        self.assertEqual(ids, sorted(ids))

    def test_output_header_matches_declared_contract(self) -> None:
        code, _, _ = self.fixture.run()
        self.assertEqual(code, 0)
        with self.fixture.output.open(newline="", encoding="utf-8") as handle:
            header = next(csv.reader(handle))
        self.assertEqual(header, list(rcws.OUTPUT_COLUMNS))


class TemplateDegradationTests(unittest.TestCase):
    """Without template base stats, damage is not derivable -- and must stay blank."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.fixture = default_fixture(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_piece_only_run_reports_not_reconstructed(self) -> None:
        code, stdout, stderr = self.fixture.run(with_template=False)
        self.assertEqual(code, 0, stderr)
        rows = {row["item_id"]: row for row in read_csv(self.fixture.output)}
        row = rows["good_sword"]
        self.assertEqual(row["crafted_stats_reconstructed"], "False")
        self.assertEqual(row["stat_source"], rcws.SRC_NO_TEMPLATE)
        self.assertEqual(row["swing_damage"], "")
        self.assertEqual(row["thrust_damage"], "")
        self.assertEqual(row["speed_rating"], "")
        # Geometry is still real and still published.
        self.assertEqual(row["weapon_length"], "124")
        self.assertIn("reconstructed=0", stdout)

    def test_template_row_absent_for_this_item_only(self) -> None:
        self.fixture.write_templates(
            [
                template(
                    "SomeOtherTemplate",
                    weapon_class="Dagger",
                    swing_damage_base="10",
                    thrust_damage_base="10",
                    speed_rating_base="10",
                )
            ]
        )
        code, _, stderr = self.fixture.run()
        self.assertEqual(code, 0, stderr)
        rows = {row["item_id"]: row for row in read_csv(self.fixture.output)}
        self.assertEqual(rows["good_sword"]["stat_source"], rcws.SRC_PIECE_ONLY)
        self.assertEqual(rows["good_sword"]["swing_damage"], "")
        self.assertIn("OneHandedSword", rows["good_sword"]["blocked_reason"])

    def test_no_blade_piece_blocks_damage(self) -> None:
        self.fixture.write_composition(
            [
                {
                    "item_id": "handle_only",
                    "piece_id": "handle_a",
                    "piece_type": "Handle",
                    "scale_factor": "100",
                }
            ]
        )
        code, _, stderr = self.fixture.run()
        self.assertEqual(code, 0, stderr)
        row = read_csv(self.fixture.output)[0]
        self.assertEqual(row["stat_source"], rcws.SRC_NO_BLADE)
        self.assertEqual(row["swing_damage"], "")
        self.assertEqual(row["crafted_stats_reconstructed"], "False")

    def test_blade_without_numeric_factors_leaves_damage_blank(self) -> None:
        self.fixture.write_pieces(
            [
                piece(
                    "blade_a",
                    "Blade",
                    length="80",
                    weight="1.5",
                    swing_damage_factor="0.90",
                    thrust_damage_factor="",  # absent in the source XML
                    swing_speed_factor="0.95",
                ),
                piece("handle_a", "Handle", length="30", weight="0.6"),
                piece("guard_a", "Guard", length="6", weight="0.2"),
            ]
        )
        code, _, stderr = self.fixture.run()
        self.assertEqual(code, 0, stderr)
        rows = {row["item_id"]: row for row in read_csv(self.fixture.output)}
        row = rows["good_sword"]
        self.assertEqual(row["swing_damage"], "99")
        self.assertEqual(row["thrust_damage"], "")
        self.assertEqual(row["crafted_stats_reconstructed"], "False")
        self.assertEqual(row["stat_source"], rcws.SRC_PIECE_ONLY)
        self.assertIn("thrust_damage", row["blocked_reason"])


class BlockedPathTests(unittest.TestCase):
    """A missing or insufficient catalog must exit non-zero and write nothing."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.fixture = default_fixture(Path(self._tmp.name))

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _assert_blocked(self, code: int, stderr: str) -> None:
        self.assertEqual(code, 2, f"expected exit 2, got {code}; stderr={stderr}")
        self.assertTrue(
            stderr.startswith("blocked: missing crafting piece catalog"),
            f"unexpected message: {stderr!r}",
        )
        self.assertFalse(
            self.fixture.output.exists(),
            "a blocked run must not leave an output file behind",
        )

    def test_absent_piece_catalog_blocks(self) -> None:
        self.fixture.piece_catalog.unlink()
        code, _, stderr = self.fixture.run()
        self._assert_blocked(code, stderr)

    def test_piece_catalog_missing_required_column_blocks(self) -> None:
        trimmed = [name for name in PIECE_FIELDS if name != "swing_damage_factor"]
        rows = [
            {key: value for key, value in row.items() if key in trimmed}
            for row in read_csv(self.fixture.piece_catalog)
        ]
        self.fixture.write_pieces(rows, fieldnames=trimmed)
        code, _, stderr = self.fixture.run()
        self._assert_blocked(code, stderr)
        self.assertIn("swing_damage_factor", stderr)

    def test_header_only_piece_catalog_blocks(self) -> None:
        self.fixture.write_pieces([])
        code, _, stderr = self.fixture.run()
        self._assert_blocked(code, stderr)
        self.assertIn("no data rows", stderr)

    def test_piece_catalog_without_a_usable_blade_blocks(self) -> None:
        """Rows present but every Blade lacks a numeric swing_damage_factor."""
        self.fixture.write_pieces(
            [
                piece("blade_a", "Blade", length="80", weight="1.5"),
                piece("handle_a", "Handle", length="30", weight="0.6"),
            ]
        )
        code, _, stderr = self.fixture.run()
        self._assert_blocked(code, stderr)
        self.assertIn("swing_damage_factor", stderr)

    def test_template_catalog_missing_required_column_blocks(self) -> None:
        trimmed = [name for name in TEMPLATE_FIELDS if name != "swing_damage_base"]
        rows = [
            {key: value for key, value in row.items() if key in trimmed}
            for row in read_csv(self.fixture.template_catalog)
        ]
        self.fixture.write_templates(rows, fieldnames=trimmed)
        code, _, stderr = self.fixture.run()
        self._assert_blocked(code, stderr)
        self.assertIn("swing_damage_base", stderr)

    def test_absent_template_catalog_path_blocks(self) -> None:
        self.fixture.template_catalog.unlink()
        code, _, stderr = self.fixture.run()
        self._assert_blocked(code, stderr)

    def test_absent_track_composition_blocks(self) -> None:
        (self.fixture.audit_dir / "vanilla_crafted_item_pieces.csv").unlink()
        code, _, stderr = self.fixture.run()
        self._assert_blocked(code, stderr)

    def test_real_repo_run_is_blocked_today(self) -> None:
        """The repository genuinely has no piece stats catalog: the tool must refuse."""
        out, err = io.StringIO(), io.StringIO()
        absent = self.fixture.root / "does_not_exist.csv"
        with redirect_stdout(out), redirect_stderr(err):
            code = rcws.main(
                [
                    "--track",
                    "vanilla",
                    "--piece-catalog",
                    str(absent),
                    "--output",
                    str(self.fixture.output),
                ]
            )
        self.assertEqual(code, 2)
        self.assertIn("blocked: missing crafting piece catalog", err.getvalue())
        self.assertFalse(self.fixture.output.exists())


class TooltipValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.fixture = default_fixture(Path(self._tmp.name))
        self.tooltips = Path(self._tmp.name) / "tooltips.csv"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write_tooltips(self, swing: str, thrust: str) -> None:
        write_csv(
            self.tooltips,
            ["item_id", "observed_swing_damage", "observed_thrust_damage"],
            [
                {
                    "item_id": "good_sword",
                    "observed_swing_damage": swing,
                    "observed_thrust_damage": thrust,
                }
            ],
        )

    def test_matching_tooltips_pass(self) -> None:
        self._write_tooltips("99", "44")
        code, stdout, stderr = self.fixture.run(
            "--tooltip-validation",
            str(self.tooltips),
            "--require-tooltip-validation",
        )
        self.assertEqual(code, 0, stderr)
        self.assertIn("tooltip_validation: compared=2 failures=0", stdout)

    def test_mismatching_tooltips_refuse_to_publish(self) -> None:
        self._write_tooltips("140", "44")
        code, _, stderr = self.fixture.run(
            "--tooltip-validation",
            str(self.tooltips),
            "--require-tooltip-validation",
        )
        self.assertEqual(code, 3)
        self.assertIn("tooltip mismatch", stderr)
        self.assertFalse(
            self.fixture.output.exists(),
            "a failed validation gate must not publish stats",
        )

    def test_mismatch_without_gate_still_publishes_but_reports(self) -> None:
        self._write_tooltips("140", "44")
        code, stdout, stderr = self.fixture.run(
            "--tooltip-validation", str(self.tooltips)
        )
        self.assertEqual(code, 0, stderr)
        self.assertIn("failures=1", stdout)
        self.assertTrue(self.fixture.output.is_file())


class CoverageQuantifierTests(unittest.TestCase):
    """The published coverage numbers must stay reproducible from the committed audits."""

    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location(
            "quantify_crafted_damage_coverage",
            REPO / "scripts" / "analysis" / "quantify_crafted_damage_coverage.py",
        )
        cls.module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(cls.module)

    def test_every_crafted_row_is_still_hollow(self) -> None:
        expected = {
            "vanilla": 3619,
            "nightmare_sails": 3723,
            "realm_of_thrones": 9648,
            "taom": 6663,
        }
        for track, hollow in expected.items():
            stats = self.module.analyse_track(REPO, track)
            self.assertEqual(stats["crafted_weapon_rows"], hollow, track)
            self.assertEqual(stats["hollow_weapon_rows"], hollow, track)
            self.assertEqual(
                stats["direct_melee_weapon_rows"],
                0,
                f"{track}: a direct melee item appeared; the report needs updating",
            )

    def test_crafted_class_matches_the_scorer(self) -> None:
        """Documented mis-classifications in the coverage report must stay documented."""
        self.assertEqual(self.module.crafted_class("ThrowingAxe"), "axe")
        self.assertEqual(self.module.crafted_class("ROT_ThrowingAxe"), "axe")
        self.assertEqual(self.module.crafted_class("Pike"), "other")
        self.assertEqual(self.module.crafted_class("Dagger"), "other")
        self.assertEqual(self.module.crafted_class("TwoHandedPolearm"), "two_handed_polearm")


if __name__ == "__main__":
    unittest.main()
