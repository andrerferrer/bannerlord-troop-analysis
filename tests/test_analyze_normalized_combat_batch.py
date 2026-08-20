from __future__ import annotations

import csv
import hashlib
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
    def test_routed_is_not_added_to_deployed_arithmetic(self) -> None:
        battle = {
            "battle_id": "b1",
            "battle_context": "field",
            "player_side": "attacker",
        }
        occurrence = {
            "observation_id": "o1",
            "battle_id": "b1",
            "battle_context": "field",
            "display_name_normalized": "troop",
            "display_name_raw": "Troop [T1]",
            "game_track": "realm_of_thrones",
            "row_type": "troop",
            "analysis_status": "included_primary",
            "needs_review": False,
            "side": "attacker",
            "source_image_sha256": "image-hash",
            "deployed": 1,
            "survivors": 1,
            "kills": 0,
            "deaths": 0,
            "wounded": 0,
            "routed": 1,
        }
        consolidated_row = {
            "battle_id": "b1",
            "battle_context": "field",
            "display_name_normalized": "troop",
            "display_names_raw": ["Troop [T1]"],
            "game_track": "realm_of_thrones",
            "observation_ids": ["o1"],
            "needs_review": False,
            "deployed": 1,
            "survivors": 1,
            "kills": 0,
            "deaths": 0,
            "wounded": 0,
            "routed": 1,
        }

        errors, _ = MODULE.validate_normalized(
            [battle],
            [occurrence],
            [occurrence],
            [consolidated_row],
            [{"image_sha256": "image-hash"}],
            [],
        )

        self.assertEqual(errors, [])

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

    def test_kill_share_impact_can_reverse_efficiency_order(self) -> None:
        rows = [
            consolidated("b1", "field", "majority", 9, 18),
            consolidated("b2", "field", "burst", 5, 20),
        ]
        identities = MODULE.build_identity_audit(rows, {}, "realm_of_thrones")
        rankings = MODULE.build_rankings(
            rows,
            identities,
            "batch",
            minimum_battles=5,
            minimum_deployed=20,
            repetitions=100,
            player_side_kill_totals={
                ("b1", "field"): {
                    "kills": 20,
                    "provenance": "battle_metadata_direct",
                },
                ("b2", "field"): {
                    "kills": 80,
                    "provenance": "battle_metadata_direct",
                },
            },
        )
        by_slug = {str(row["provisional_slug"]): row for row in rankings}

        self.assertEqual(by_slug["majority"]["kills_per_deployed"], 2.0)
        self.assertEqual(by_slug["majority"]["player_side_kill_share"], 0.9)
        self.assertEqual(by_slug["majority"]["share_adjusted_impact"], 1.8)
        self.assertEqual(by_slug["majority"]["rank"], 2)
        self.assertEqual(by_slug["majority"]["impact_rank"], 1)
        self.assertEqual(by_slug["burst"]["kills_per_deployed"], 4.0)
        self.assertEqual(by_slug["burst"]["player_side_kill_share"], 0.25)
        self.assertEqual(by_slug["burst"]["share_adjusted_impact"], 1.0)
        self.assertEqual(by_slug["burst"]["rank"], 1)
        self.assertEqual(by_slug["burst"]["impact_rank"], 2)

    def test_verified_player_side_totals_reject_conflicts(self) -> None:
        battles = [
            {
                "battle_id": "b1",
                "battle_context": "field",
                "player_side": "attacker",
                "player_kills": 20,
            },
            {
                "battle_id": "b2",
                "battle_context": "field",
                "player_side": "defender",
                "player_kills": 30,
            },
        ]
        occurrences = [
            {
                "battle_id": "b1",
                "battle_context": "field",
                "side": "attacker",
                "row_type": "side_total",
                "kills": 20,
                "needs_review": False,
            },
            {
                "battle_id": "b2",
                "battle_context": "field",
                "side": "defender",
                "row_type": "side_total",
                "kills": 31,
                "needs_review": False,
            },
        ]

        totals = MODULE.verified_player_side_kill_totals(battles, occurrences)

        self.assertEqual(totals[("b1", "field")]["kills"], 20)
        self.assertEqual(
            totals[("b1", "field")]["provenance"],
            "battle_metadata_and_side_total",
        )
        self.assertNotIn(("b2", "field"), totals)

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

    def test_manifest_requires_complete_unique_file_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_dir = root / "input"
            input_dir.mkdir()
            included = input_dir / "included.txt"
            included.write_text("included", encoding="utf-8")
            (input_dir / "unlisted.txt").write_text("unlisted", encoding="utf-8")
            (input_dir / "artifact_hashes.csv").write_text("self", encoding="utf-8")
            digest = hashlib.sha256(included.read_bytes()).hexdigest()
            manifest = root / "artifact_hashes.csv"
            manifest.write_text(
                "file,sha256,size_bytes\n"
                f"included.txt,{digest},{included.stat().st_size}\n"
                f"included.txt,{digest},{included.stat().st_size}\n",
                encoding="utf-8",
            )

            _, errors = MODULE.verify_manifest(input_dir, manifest)

            self.assertIn("duplicate artifact manifest path: included.txt", errors)
            self.assertIn("unlisted artifact file: unlisted.txt", errors)

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

    def test_retained_source_directory_is_verified_per_manifest_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source_path = root / "screenshots"
            source_path.mkdir()
            first = source_path / "one.png"
            second = source_path / "two.png"
            first.write_bytes(b"one")
            second.write_bytes(b"two")
            source_manifest = [
                {"image_file": first.name, "image_sha256": MODULE.sha256_file(first)},
                {"image_file": second.name, "image_sha256": MODULE.sha256_file(second)},
            ]

            source, errors = MODULE.inspect_optional_source(
                source_path,
                root,
                "a" * 64,
                first.stat().st_size + second.stat().st_size,
                source_manifest,
            )

            self.assertEqual(errors, [])
            self.assertTrue(source["locally_verified"])
            self.assertEqual(source["verification_method"], "manifest_files_sha256_and_total_size")
            self.assertEqual(source["actual_sha256"], "")

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

    def test_normalized_schema_versions_must_agree(self) -> None:
        version, errors = MODULE.verify_normalized_schema_version(
            {"schema_version": "2.0.0"},
            {"schema_version": "1.1.0"},
        )
        self.assertEqual(version, "")
        self.assertEqual(errors, ["normalized schema version mismatch"])

    def test_normalized_schema_version_must_be_supported(self) -> None:
        version, errors = MODULE.verify_normalized_schema_version(
            {"schema_version": "99.0.0"},
            {"schema_version": "99.0.0"},
        )
        self.assertEqual(version, "")
        self.assertEqual(errors, ["unsupported normalized schema version: 99.0.0"])

    def test_reproduction_path_accepts_source_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo_root = Path(directory) / "repo"
            repo_root.mkdir()
            outside = Path(directory) / "raw screenshots"
            self.assertEqual(
                MODULE.format_reproduction_path(outside, repo_root),
                "'" + str(outside) + "'",
            )

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

    def test_consolidated_rows_must_come_only_from_primary_and_exclude_queue(self) -> None:
        primary = {
            "observation_id": "o1",
            "battle_id": "b1",
            "battle_context": "field",
            "row_type": "troop",
            "analysis_status": "included_primary",
            "needs_review": False,
            "side": "attacker",
            "source_image_sha256": "a" * 64,
            "deployed": 1,
            "survivors": 1,
            "kills": 0,
            "deaths": 0,
            "wounded": 0,
            "routed": 0,
        }
        consolidated_row = consolidated("b1", "field", "troop", 1, 0)
        consolidated_row["observation_ids"] = ["queued", "not-primary"]
        errors, summary = MODULE.validate_normalized(
            battles=[{"battle_id": "b1", "battle_context": "field", "player_side": "attacker"}],
            occurrences=[
                primary,
                {
                    "observation_id": "queued",
                    "battle_id": "b1",
                    "row_type": "troop",
                    "analysis_status": "unresolved",
                    "needs_review": True,
                    "deaths": None,
                },
            ],
            primary=[primary],
            consolidated=[consolidated_row],
            screenshot_manifest=[{"image_sha256": "a" * 64}],
            review_queue=[
                {
                    "observation_id": "queued",
                    "battle_id": "b1",
                    "uncertain_fields": "deaths",
                }
            ],
        )
        self.assertIn("non-primary observation entered consolidated rows: not-primary", errors)
        self.assertIn("review item leaked into consolidated rows: queued", errors)
        self.assertIn("primary observation missing from consolidated rows: o1", errors)
        self.assertFalse(summary["queued_rows_excluded_from_rankings"])
        self.assertFalse(summary["primary_rows_fully_consolidated"])

    def test_consolidated_identity_and_counts_must_match_primary_rows(self) -> None:
        primary = {
            "observation_id": "o1",
            "battle_id": "b1",
            "battle_context": "field",
            "display_name_normalized": "right_troop",
            "display_name_raw": "Right Troop [T3]",
            "game_track": "realm_of_thrones",
            "row_type": "troop",
            "analysis_status": "included_primary",
            "needs_review": False,
            "side": "attacker",
            "source_image_sha256": "a" * 64,
            "deployed": 10,
            "survivors": 9,
            "kills": 1,
            "deaths": 1,
            "wounded": 0,
            "routed": 0,
        }
        consolidated_row = consolidated("b1", "field", "wrong_troop", 999, 999)
        consolidated_row.update(
            {
                "observation_ids": ["o1"],
                "display_names_raw": ["Wrong Troop [T6]"],
                "game_track": "wrong_track",
            }
        )

        errors, summary = MODULE.validate_normalized(
            battles=[{"battle_id": "b1", "battle_context": "field", "player_side": "attacker"}],
            occurrences=[primary],
            primary=[primary],
            consolidated=[consolidated_row],
            screenshot_manifest=[{"image_sha256": "a" * 64}],
            review_queue=[],
        )

        self.assertTrue(any(error.startswith("consolidated key missing from primary rows:") for error in errors))
        self.assertTrue(any(error.startswith("primary group missing from consolidated rows:") for error in errors))
        self.assertFalse(summary["primary_rows_fully_consolidated"])

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

    def test_unknown_focus_slug_fails_instead_of_reporting_not_observed(self) -> None:
        rows = [consolidated("b1", "field", "sarnori_spider", 10, 20)]
        identities = MODULE.build_identity_audit(rows, {}, "realm_of_thrones")
        rankings = MODULE.build_rankings(rows, identities, "batch", 5, 20, 100)
        with self.assertRaisesRegex(ValueError, "unknown focus slug: typo"):
            MODULE.build_focus_context_rows(
                rankings,
                identities,
                ["typo"],
                ["field"],
            )

    def test_focus_rate_display_requires_the_full_evidence_gate(self) -> None:
        row = {
            "independent_battles": 3,
            "deployed": 100,
            "kills_per_deployed": 2.5,
        }
        self.assertEqual(
            MODULE.format_focus_rate(row, "kills_per_deployed", 5, 20),
            "—",
        )
        row["independent_battles"] = 5
        self.assertEqual(
            MODULE.format_focus_rate(row, "kills_per_deployed", 5, 20),
            "2.500",
        )

    def test_batch_wide_report_includes_every_reliable_and_insufficient_row(self) -> None:
        rankings = []
        for index in range(1, 7):
            rankings.append(
                {
                    "context": "field",
                    "provisional_slug": f"reliable_{index}",
                    "canonical_troop_id": f"reliable_{index}",
                    "independent_battles": 5,
                    "deployed": 20,
                    "kills_per_deployed": 1.0,
                    "casualty_rate": 0.1,
                    "ci95_low": 0.5,
                    "ci95_high": 1.5,
                    "reliability_status": "reliable",
                }
            )
        rankings.append(
            {
                "context": "field",
                "provisional_slug": "below_gate",
                "canonical_troop_id": "",
                "independent_battles": 3,
                "deployed": 12,
                "kills_per_deployed": 9.0,
                "casualty_rate": 0.0,
                "ci95_low": "",
                "ci95_high": "",
                "reliability_status": "insufficient_evidence",
            }
        )

        report = "\n".join(
            MODULE.build_batch_wide_report_sections(rankings, ["field"], 5, 20)
        )

        for index in range(1, 7):
            self.assertIn(f"`reliable_{index}`", report)
        self.assertIn("`below_gate (provisional)`", report)
        self.assertIn("| 3 | 12 | 2 | 8 |", report)
        self.assertNotIn("9.000", report)
        self.assertLess(report.index("Batch-wide roster analysis"), report.index("below_gate"))


if __name__ == "__main__":
    unittest.main()
