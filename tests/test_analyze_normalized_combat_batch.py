from __future__ import annotations

import importlib.util
import io
import tarfile
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[1]
    / "scripts"
    / "analysis"
    / "analyze_normalized_combat_batch.py"
)
SPEC = importlib.util.spec_from_file_location("analyze_normalized_combat_batch", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def consolidated(
    battle_id: str,
    context: str,
    slug: str,
    deployed: int,
    kills: int,
) -> dict[str, object]:
    return {
        "battle_id": battle_id,
        "battle_context": context,
        "display_name_normalized": slug,
        "display_names_raw": [f"{slug.replace('_', ' ').title()} [T5]"],
        "deployed": deployed,
        "survivors": deployed,
        "kills": kills,
        "deaths": 0,
        "wounded": 0,
        "routed": 0,
        "needs_review": False,
    }


class AnalyzeNormalizedCombatBatchTests(unittest.TestCase):
    def test_name_normalization_removes_tier_without_using_slug_as_id(self) -> None:
        self.assertEqual(
            MODULE.normalize_display_name("Ravens’ Teeth [T6]"),
            "ravens' teeth",
        )

    def test_identity_requires_one_exact_versioned_candidate(self) -> None:
        rows = [consolidated("b1", "field", "ravens_teeth", 10, 20)]
        identities = MODULE.build_identity_audit(
            rows,
            {"ravens teeth": [("ravens_teeth_xml", "data/rot_reference/a.csv")]},
            "realm_of_thrones",
        )
        self.assertEqual(identities[0]["canonical_troop_id"], "ravens_teeth_xml")
        self.assertEqual(identities[0]["match_status"], "confirmed_id")

        unresolved = MODULE.build_identity_audit(rows, {}, "realm_of_thrones")
        self.assertEqual(unresolved[0]["canonical_troop_id"], "")
        self.assertEqual(unresolved[0]["match_status"], "unresolved")

    def test_reliable_gate_uses_independent_battles_and_deployed(self) -> None:
        rows = [
            consolidated(f"b{index}", "siege_attack", "ravens_teeth", 5, 10)
            for index in range(1, 6)
        ]
        identities = MODULE.build_identity_audit(rows, {}, "realm_of_thrones")
        rankings = MODULE.build_rankings(
            rows,
            identities,
            "batch",
            minimum_battles=5,
            minimum_deployed=20,
            repetitions=100,
        )
        siege = next(row for row in rankings if row["context"] == "siege_attack")
        self.assertEqual(siege["reliability_status"], "reliable")
        self.assertEqual(siege["independent_battles"], 5)
        self.assertEqual(siege["deployed"], 25)
        self.assertNotIn("overall", {row["context"] for row in rankings})

    def test_four_battles_never_pass_display_gate(self) -> None:
        rows = [
            consolidated(f"b{index}", "field", "northern_archer", 20, 10)
            for index in range(1, 5)
        ]
        identities = MODULE.build_identity_audit(rows, {}, "realm_of_thrones")
        rankings = MODULE.build_rankings(
            rows,
            identities,
            "batch",
            minimum_battles=5,
            minimum_deployed=20,
            repetitions=100,
        )
        field = next(row for row in rankings if row["context"] == "field")
        self.assertEqual(field["reliability_status"], "insufficient_evidence")
        self.assertEqual(field["ci95_low"], "")
        self.assertEqual(field["ci95_high"], "")

    def test_bootstrap_is_deterministic(self) -> None:
        rows = [
            consolidated("b1", "field", "troop", 10, 5),
            consolidated("b2", "field", "troop", 20, 30),
        ]
        first = MODULE.bootstrap_interval(rows, "batch", "field", "troop", 200)
        second = MODULE.bootstrap_interval(rows, "batch", "field", "troop", 200)
        self.assertEqual(first, second)

    def test_archive_preflight_rejects_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "input.tar.xz"
            with tarfile.open(archive_path, "w:xz") as archive:
                info = tarfile.TarInfo("../escape.jsonl")
                payload = b"{}\n"
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
            with self.assertRaisesRegex(ValueError, "unsafe archive member path"):
                MODULE.safe_tar_preflight(archive_path)

    def test_archive_preflight_rejects_canonical_collision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "input.tar.xz"
            with tarfile.open(archive_path, "w:xz") as archive:
                for name, payload in (("dir/file", b"one"), ("dir/./file", b"two")):
                    info = tarfile.TarInfo(name)
                    info.size = len(payload)
                    archive.addfile(info, io.BytesIO(payload))
            with self.assertRaisesRegex(ValueError, "duplicate canonical archive member"):
                MODULE.safe_tar_preflight(archive_path)

    def test_manifest_rejects_path_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_dir = root / "input"
            input_dir.mkdir()
            outside = root / "outside.txt"
            outside.write_text("secret", encoding="utf-8")
            manifest = root / "manifest.csv"
            manifest.write_text(
                "file,sha256,size_bytes\n../outside.txt,ignored,6\n",
                encoding="utf-8",
            )
            checks, errors = MODULE.verify_manifest(input_dir, manifest)
            self.assertEqual(checks, [])
            self.assertEqual(errors, ["unsafe artifact manifest path: ../outside.txt"])

    def test_git_revision_rejects_option_injection(self) -> None:
        with self.assertRaisesRegex(ValueError, "full 40-character"):
            MODULE.git_changed_paths(Path("."), "--output=/tmp/owned", ["README.md"])

    def test_csv_formula_values_are_neutralized(self) -> None:
        self.assertEqual(MODULE.escape_spreadsheet_formula("=2+2"), "'=2+2")
        self.assertEqual(MODULE.escape_spreadsheet_formula("safe"), "safe")


if __name__ == "__main__":
    unittest.main()
