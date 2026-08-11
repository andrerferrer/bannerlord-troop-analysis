from __future__ import annotations

import csv
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

    def test_identity_candidate_evidence_paths_are_repository_relative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo_root = Path(directory)
            audit_dir = repo_root / "data" / "realm_of_thrones" / "audit"
            audit_dir.mkdir(parents=True)
            audit_path = audit_dir / "troops.csv"
            with audit_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=("troop_id", "name"))
                writer.writeheader()
                writer.writerow({"troop_id": "sarnor_spider", "name": "Sarnori Spider"})

            candidates = MODULE.collect_identity_candidates(
                audit_dir,
                existing_audit=None,
                repo_root=repo_root,
            )

        self.assertEqual(
            candidates["sarnori spider"],
            [
                (
                    "sarnor_spider",
                    "data/realm_of_thrones/audit/troops.csv",
                    "versioned_track_reference",
                )
            ],
        )

    def test_historical_identity_evidence_tier_is_preserved(self) -> None:
        rows = [consolidated("b1", "field", "riverlands_ranger", 10, 20)]
        identities = MODULE.build_identity_audit(
            rows,
            {
                "riverlands ranger": [
                    (
                        "river_ranger",
                        "data/canonical_identity_recovery/pr20/realm_of_thrones_exact_matches.csv",
                        MODULE.HISTORICAL_REPORTED_EXACT,
                    )
                ]
            },
            "realm_of_thrones",
        )
        self.assertEqual(identities[0]["match_status"], "confirmed_id")
        self.assertEqual(
            identities[0]["resolution_method"],
            "historical_pr_reported_exact_name_in_versioned_source",
        )
        self.assertEqual(
            identities[0]["evidence_kind"],
            MODULE.HISTORICAL_REPORTED_EXACT,
        )

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
            with self.assertRaisesRegex(RuntimeError, "unsafe archive member path"):
                MODULE.safe_tar_preflight(archive_path)

    def test_archive_preflight_rejects_canonical_collision(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "input.tar.xz"
            with tarfile.open(archive_path, "w:xz") as archive:
                for name, payload in (("dir/file", b"one"), ("dir/./file", b"two")):
                    info = tarfile.TarInfo(name)
                    info.size = len(payload)
                    archive.addfile(info, io.BytesIO(payload))
            with self.assertRaisesRegex(RuntimeError, "duplicate archive member name"):
                MODULE.safe_tar_preflight(archive_path)

    def test_archive_member_limit_is_enforced_during_iteration(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "input.tar.xz"
            with tarfile.open(archive_path, "w:xz") as archive:
                archive.addfile(tarfile.TarInfo("one"))
                archive.addfile(tarfile.TarInfo("two"))
            with self.assertRaisesRegex(RuntimeError, "member count exceeds limit"):
                MODULE.inspect_tar(archive_path, max_members=1)

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

    def test_missing_optional_raw_source_is_not_a_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, errors = MODULE.inspect_optional_source(
                root / "not-retained.zip",
                root,
                "a" * 64,
                123,
            )
            self.assertEqual(errors, [])
            self.assertEqual(source["retention_status"], "not_retained")
            self.assertFalse(source["repository_addressable"])
            self.assertTrue(source["limits_visual_rereview"])

    def test_retained_raw_source_must_match_recorded_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "retained.zip"
            source_path.write_bytes(b"wrong")
            source, errors = MODULE.inspect_optional_source(
                source_path,
                root,
                "a" * 64,
                123,
            )
            self.assertEqual(
                errors,
                ["retained raw source does not match its recorded hash and size"],
            )
            self.assertEqual(source["retention_status"], "mismatch")

    def test_optional_source_provenance_must_match_normalized_records(self) -> None:
        checks, errors = MODULE.verify_recorded_source_identity(
            "a" * 64,
            123,
            {"source_zip_sha256": "b" * 64},
            {"source_zip_sha256": "a" * 64, "source_zip_size_bytes": 123},
        )
        self.assertEqual(
            errors,
            ["recorded source identity mismatch: normalization_summary.json:source_zip_sha256"],
        )
        self.assertFalse(checks[0]["passed"])
        self.assertTrue(checks[1]["passed"])
        self.assertTrue(checks[2]["passed"])

    def test_source_directory_provenance_uses_generic_source_fields(self) -> None:
        checks, errors = MODULE.verify_recorded_source_identity(
            "a" * 64,
            123,
            {"source_sha256": "a" * 64},
            {"source_sha256": "a" * 64, "source_size_bytes": 123},
        )
        self.assertEqual(errors, [])
        self.assertTrue(all(check["passed"] for check in checks))

    def test_symlinked_raw_source_is_never_repository_addressable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / "outside.zip"
            outside.write_bytes(b"exact")
            source_path = root / "source.zip"
            source_path.symlink_to(outside)
            source, errors = MODULE.inspect_optional_source(
                source_path,
                root,
                MODULE.sha256_file(outside),
                outside.stat().st_size,
            )
            self.assertEqual(errors, [])
            self.assertEqual(source["retention_status"], "locally_verified")
            self.assertTrue(source["locally_verified"])
            self.assertFalse(source["repository_addressable"])

    def test_git_revision_rejects_option_injection(self) -> None:
        with self.assertRaisesRegex(ValueError, "full 40-character"):
            MODULE.git_changed_paths(Path("."), "--output=/tmp/owned", ["README.md"])

    def test_csv_formula_values_are_neutralized(self) -> None:
        self.assertEqual(MODULE.escape_spreadsheet_formula("=2+2"), "'=2+2")
        self.assertEqual(MODULE.escape_spreadsheet_formula("safe"), "safe")

    def test_zero_deployment_is_rejected_before_rate_calculation(self) -> None:
        rows = [consolidated("b1", "field", "empty", 0, 0)]
        identities = MODULE.build_identity_audit(rows, {}, "realm_of_thrones")
        with self.assertRaisesRegex(ValueError, "non-positive deployed total"):
            MODULE.build_rankings(
                rows,
                identities,
                "batch",
                minimum_battles=5,
                minimum_deployed=20,
                repetitions=100,
            )

    def test_review_queue_accepts_excluded_unresolved_troop_rows(self) -> None:
        errors, summary = MODULE.validate_normalized(
            battles=[
                {
                    "battle_id": "b1",
                    "battle_context": "siege_attack",
                    "player_side": "attacker",
                }
            ],
            occurrences=[
                {
                    "observation_id": "o1",
                    "battle_id": "b1",
                    "row_type": "troop",
                    "analysis_status": "unresolved",
                    "needs_review": True,
                    "deaths": None,
                    "wounded": None,
                }
            ],
            primary=[],
            consolidated=[],
            screenshot_manifest=[],
            review_queue=[
                {
                    "observation_id": "o1",
                    "battle_id": "b1",
                    "uncertain_fields": "deaths|wounded",
                }
            ],
        )
        self.assertEqual(errors, [])
        self.assertEqual(summary["review_items"], 1)

    def test_review_decisions_preserve_queue_specific_reason(self) -> None:
        decisions = MODULE.build_review_decisions(
            review_queue=[
                {
                    "observation_id": "o1",
                    "battle_id": "b1",
                    "source_image_file": "scoreboard.png",
                    "uncertain_fields": "deaths|wounded",
                    "notes": "bottom row is clipped",
                }
            ],
            occurrences=[
                {
                    "observation_id": "o1",
                    "source_image_sha256": "a" * 64,
                    "deaths": None,
                    "wounded": None,
                }
            ],
            reviewer="test reviewer",
            raw_visual_review_available=False,
        )
        self.assertEqual([row["field"] for row in decisions], ["deaths", "wounded"])
        self.assertTrue(all("bottom row is clipped" in row["reason"] for row in decisions))
        self.assertTrue(all("level-up icon" not in row["reason"] for row in decisions))

    def test_focus_matrix_keeps_unobserved_contexts_explicit(self) -> None:
        rows = [consolidated("b1", "field", "sarnori_spider", 10, 20)]
        identities = MODULE.build_identity_audit(
            rows,
            {"sarnori spider": [("sarnor_spider", "audit.csv")]},
            "realm_of_thrones",
        )
        rankings = MODULE.build_rankings(
            rows,
            identities,
            "batch",
            minimum_battles=5,
            minimum_deployed=20,
            repetitions=100,
        )
        focus = MODULE.build_focus_context_rows(
            rankings,
            identities,
            ["sarnori_spider"],
            ["field", "siege_attack"],
        )
        self.assertEqual(len(focus), 2)
        self.assertEqual(focus[0]["reliability_status"], "insufficient_evidence")
        self.assertEqual(focus[1]["reliability_status"], "not_observed")
        self.assertEqual(focus[1]["deployed"], 0)


if __name__ == "__main__":
    unittest.main()
