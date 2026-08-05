from __future__ import annotations

import csv
import hashlib
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCORING_DIR = REPO_ROOT / "scripts" / "scoring"
if str(SCORING_DIR) not in sys.path:
    sys.path.insert(0, str(SCORING_DIR))

import audit_context_first_candidates as audit  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ContextFirstCandidateAuditTests(unittest.TestCase):
    def test_required_departures_and_absent_artifacts_are_explicit(self) -> None:
        findings = audit.build_findings(REPO_ROOT)
        observed = {
            (finding.model_or_candidate, finding.departure_code, finding.field_or_formula)
            for finding in findings
        }

        required = {
            ("role_scores_v1", "CONTEXT_UNDECLARED", "candidate declaration"),
            ("role_scores_v1", "QUESTION_MIXED", "defensive_role_score"),
            ("role_scores_v1", "TEMPLATE_PROXY_USED", "melee_proxy(crafting_template)"),
            (
                "role_scores_v1",
                "TEMPLATE_PROXY_USED",
                "melee_usability(crafting_template)",
            ),
            ("role_scores_v1", "MISSING_VALUE_ZERO_FILLED", "numeric coercion"),
            ("role_scores_v1", "AMMUNITION_POLICY_UNDECLARED", "ranged_raw"),
            ("role_scores_v1", "IRRELEVANT_DRIVER_INCLUDED", "direct_throw_raw"),
            (
                "role_scores_v1",
                "TEMPLATE_PROXY_USED",
                "throw_proxy_raw(crafting_template)",
            ),
            (
                "role_scores_v1",
                "IRRELEVANT_DRIVER_INCLUDED",
                "best item and roster aggregation",
            ),
            (
                "role_scores_v1",
                "IRRELEVANT_DRIVER_INCLUDED",
                "role eligibility and primary_category",
            ),
            (
                "defensive_role_scores_v2_candidate",
                "IRRELEVANT_DRIVER_INCLUDED",
                "shield_hp_component_v2",
            ),
            (
                "defensive_role_scores_v2_candidate",
                "IRRELEVANT_DRIVER_INCLUDED",
                "mobility_component_v2",
            ),
            (
                "defensive_role_scores_v2_candidate",
                "MISSING_VALUE_ZERO_FILLED",
                "unresolved non-mount item evidence",
            ),
            ("v7.1", "SOURCE_ARTIFACT_ABSENT", "general model CSV"),
            ("v7.2", "SOURCE_ARTIFACT_ABSENT", "full burst model CSV"),
            (
                "v7.2_context_scores",
                "QUESTION_MIXED",
                "siege_defense_score_v72",
            ),
            ("v7.2", "QUESTION_MIXED", "burst_score_v72"),
            (
                "v7.2",
                "IRRELEVANT_DRIVER_INCLUDED",
                "throw_pressure_v7/ranged_kpm_v7/charge_impact_score_v7/melee_kpm_eff_v7",
            ),
            (
                "v7.2",
                "IRRELEVANT_DRIVER_INCLUDED",
                "primary_throw_damage_type/category/has_crossbow",
            ),
            ("v7.3", "TEMPLATE_PROXY_USED", "throw_damage_source_v73=model_proxy"),
            ("v7.3", "MOUNTED_INPUT_NON_APPLICABLE", "mounted_throw_bonus_v73"),
        }
        self.assertTrue(required.issubset(observed), required - observed)

        absent_paths = {
            finding.source_path
            for finding in findings
            if finding.departure_code == "SOURCE_ARTIFACT_ABSENT"
        }
        self.assertEqual(
            {
                "analysis/model_versions/v7.1/bannerlord_v71_head_weighted_model_all_official_troops.csv",
                "analysis/model_versions/v7.2_burst_score/bannerlord_v72_burst_model_all_official_troops.csv",
                "analysis/model_versions/v7.2_burst_score/bannerlord_v72_top_burst_units_regular_combined.csv",
                "analysis/model_versions/v7.2_burst_score/bannerlord_v72_top40_burst_units_regular_combined.csv",
                "analysis/model_versions/v7.2_burst_score/vanilla_v72_top_burst_units_regular.csv",
                "analysis/model_versions/v7.2_burst_score/warsails_v72_top_burst_units_regular.csv",
                "analysis/model_versions/v7.2.1_tooltip_throw_validation/bannerlord_v721_tooltip_throw_model_all_official_troops.csv",
                "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_tooltip_damage_burst_model_all_official_troops.csv",
                "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top_burst_units_regular_combined.csv",
                "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top40_burst_units_regular_combined.csv",
                "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_top20_burst_units_regular_combined.csv",
                "analysis/model_versions/v7.3_tooltip_damage_burst/vanilla_v73_top_burst_units_regular.csv",
                "analysis/model_versions/v7.3_tooltip_damage_burst/warsails_v73_top_burst_units_regular.csv",
                "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_key_burst_cases.csv",
                "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_comparison_v72_vs_v73_burst_regular.csv",
                "analysis/model/v7_2_context_scoring/bannerlord_v72_context_scores_all_official_troops.csv",
                "analysis/model/v7_2_context_scoring/bannerlord_v72_top40_burst_regular.csv",
                "analysis/model/v7_2_context_scoring/bannerlord_v72_top40_short_engagement_regular.csv",
                "analysis/model/v7_2_context_scoring/bannerlord_v72_top40_siege_defense_regular.csv",
                "analysis/model/v7_2_context_scoring/bannerlord_v72_top40_throwing_burst_regular.csv",
                "analysis/model/v7_2_context_scoring/empirical_v72_context_validation.csv",
            },
            absent_paths,
        )

        allowed_codes = {
            "SOURCE_ARTIFACT_ABSENT",
            "CONTEXT_UNDECLARED",
            "QUESTION_MIXED",
            "ATTACK_MODE_UNDECLARED",
            "MOUNT_STATE_UNDECLARED",
            "IRRELEVANT_DRIVER_INCLUDED",
            "TEMPLATE_PROXY_USED",
            "MISSING_VALUE_ZERO_FILLED",
            "AMMUNITION_POLICY_UNDECLARED",
            "MOUNTED_INPUT_NON_APPLICABLE",
        }
        self.assertEqual(
            set(),
            {finding.departure_code for finding in findings} - allowed_codes,
        )

        defensive_v2 = [
            finding
            for finding in findings
            if finding.model_or_candidate == "defensive_role_scores_v2_candidate"
        ]
        self.assertTrue(defensive_v2)
        self.assertEqual({"false"}, {row.question_declared for row in defensive_v2})

        for finding in findings:
            if finding.departure_code == "SOURCE_ARTIFACT_ABSENT":
                self.assertEqual("", finding.source_sha256)
            else:
                source = REPO_ROOT / finding.source_path
                self.assertTrue(source.is_file(), finding.source_path)
                self.assertEqual(sha256(source), finding.source_sha256)

    def test_historical_baseline_is_complete_sorted_and_hash_verified(self) -> None:
        rows = audit.build_historical_baseline(REPO_ROOT)
        paths = [row.path for row in rows]

        self.assertEqual(sorted(paths), paths)
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn(
            "analysis/model_candidates/role_scores_v2_defense/README.md", paths
        )
        self.assertIn(
            "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_burst_summary.md",
            paths,
        )
        self.assertIn(
            "analysis/theoretical/realm_of_thrones/export_20260731_150800/realm_of_thrones_troop_role_scores_v1.csv",
            paths,
        )
        self.assertIn("scripts/scoring/generate_vanilla_role_scores.py", paths)
        self.assertIn("scripts/build_v73_tooltip_damage_burst.py", paths)
        self.assertIn(
            "analysis/model/v7_2_context_scoring/build_v72_context_scores.py",
            paths,
        )
        self.assertIn(
            "data/vanilla/role_scores/vanilla_sanity_role_scores_v1.csv", paths
        )

        tracked = set(
            subprocess.run(
                ["git", "-C", str(REPO_ROOT), "ls-files", "-z"],
                check=True,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .rstrip("\0")
            .split("\0")
        )
        self.assertTrue(set(paths).issubset(tracked), set(paths) - tracked)

        for row in rows:
            source = REPO_ROOT / row.path
            self.assertEqual(source.stat().st_size, row.bytes)
            self.assertEqual(sha256(source), row.sha256)

        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        verified = audit.verify_historical_baseline(REPO_ROOT, committed)
        self.assertEqual(rows, verified)

    def test_baseline_verification_allows_only_one_declared_new_model_version(
        self,
    ) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        rows = audit.build_historical_baseline(REPO_ROOT)
        promoted = audit.BaselineRow(
            path="analysis/model_versions/v8_context_first/model.csv",
            bytes=3,
            sha256=hashlib.sha256(b"new").hexdigest(),
            immutability_class="frozen_model",
        )
        unrelated = audit.BaselineRow(
            path="analysis/model_candidates/role_scores_v2_defense/changed.csv",
            bytes=3,
            sha256=hashlib.sha256(b"new").hexdigest(),
            immutability_class="historical_candidate",
        )

        with mock.patch.object(
            audit, "build_historical_baseline", return_value=rows + (promoted,)
        ):
            verified = audit.verify_historical_baseline(
                REPO_ROOT,
                committed,
                allowed_new_version="v8_context_first",
            )
        self.assertEqual(
            tuple(sorted(rows + (promoted,), key=lambda row: row.path)), verified
        )

        with mock.patch.object(
            audit, "build_historical_baseline", return_value=rows + (promoted,)
        ), self.assertRaisesRegex(audit.AuditError, "unexpected protected path"):
            audit.verify_historical_baseline(REPO_ROOT, committed)

        with mock.patch.object(
            audit, "build_historical_baseline", return_value=rows + (unrelated,)
        ), self.assertRaisesRegex(audit.AuditError, "unexpected protected path"):
            audit.verify_historical_baseline(
                REPO_ROOT,
                committed,
                allowed_new_version="v8_context_first",
            )

        with mock.patch.object(
            audit, "build_historical_baseline", return_value=rows + (promoted,)
        ), self.assertRaisesRegex(
            audit.AuditError, "already exists|historical namespace"
        ):
            audit.verify_historical_baseline(
                REPO_ROOT,
                committed,
                allowed_new_version="v7.3_tooltip_damage_burst",
            )

        for reserved_version in ("v7.1", "v7.2.1_tooltip_throw_validation"):
            with mock.patch.object(
                audit, "build_historical_baseline", return_value=rows
            ), self.assertRaisesRegex(audit.AuditError, "historical namespace"):
                audit.verify_historical_baseline(
                    REPO_ROOT,
                    committed,
                    allowed_new_version=reserved_version,
                )

    def test_untracked_protected_additions_are_visible_to_promotion_verification(
        self,
    ) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            candidate_root = (
                temp_repo / "analysis/model_candidates/context_first_scores_v1"
            )
            candidate_root.mkdir(parents=True)
            temp_baseline = candidate_root / "historical_baseline_hashes.csv"
            temp_baseline.write_bytes(committed.read_bytes())
            rows = audit._parse_baseline(committed.read_bytes())
            findings = audit.build_findings(REPO_ROOT)
            version_name = "v8_context_first"
            addition = (
                temp_repo
                / "analysis/model_versions"
                / version_name
                / "model.csv"
            )
            addition.parent.mkdir(parents=True)
            addition.write_bytes(b"new model\n")

            with mock.patch.object(
                audit, "build_historical_baseline", return_value=rows
            ), mock.patch.object(audit, "_tracked_files", return_value=()):
                with self.assertRaisesRegex(
                    audit.AuditError, "unexpected protected path"
                ):
                    audit.verify_historical_baseline(temp_repo, temp_baseline)

                verified = audit.verify_historical_baseline(
                    temp_repo,
                    temp_baseline,
                    allowed_new_version=version_name,
                )
                self.assertIn(
                    addition.relative_to(temp_repo).as_posix(),
                    {row.path for row in verified},
                )

                with mock.patch.object(
                    audit, "build_findings", return_value=findings
                ):
                    report = candidate_root / "CURRENT_CANDIDATE_AUDIT.md"
                    _, published_rows = audit.write_audit(
                        temp_repo,
                        report,
                        temp_baseline,
                        allowed_new_version=version_name,
                    )
                self.assertEqual(verified, published_rows)

    def test_entirely_untracked_theoretical_export_root_is_rejected(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        rows = audit._parse_baseline(committed.read_bytes())
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            temp_baseline = (
                temp_repo
                / "analysis/model_candidates/context_first_scores_v1/"
                "historical_baseline_hashes.csv"
            )
            temp_baseline.parent.mkdir(parents=True)
            temp_baseline.write_bytes(committed.read_bytes())
            addition = (
                temp_repo
                / "analysis/theoretical/new_track/export_20260731_150800/"
                "untracked.csv"
            )
            addition.parent.mkdir(parents=True)
            addition.write_bytes(b"historical output\n")
            with mock.patch.object(
                audit, "build_historical_baseline", return_value=rows
            ), mock.patch.object(
                audit, "_tracked_files", return_value=()
            ), self.assertRaisesRegex(audit.AuditError, "unexpected protected path"):
                audit.verify_historical_baseline(temp_repo, temp_baseline)

    def test_untracked_v72_context_output_is_rejected(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        rows = audit._parse_baseline(committed.read_bytes())
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            temp_baseline = (
                temp_repo
                / "analysis/model_candidates/context_first_scores_v1/"
                "historical_baseline_hashes.csv"
            )
            temp_baseline.parent.mkdir(parents=True)
            temp_baseline.write_bytes(committed.read_bytes())
            addition = (
                temp_repo
                / "analysis/model/v7_2_context_scoring/"
                "bannerlord_v72_context_scores_all_official_troops.csv"
            )
            addition.parent.mkdir(parents=True)
            addition.write_bytes(b"historical output\n")
            with mock.patch.object(
                audit, "build_historical_baseline", return_value=rows
            ), mock.patch.object(
                audit, "_tracked_files", return_value=()
            ), self.assertRaisesRegex(audit.AuditError, "unexpected protected path"):
                audit.verify_historical_baseline(temp_repo, temp_baseline)

    def test_symlinked_theoretical_track_is_rejected(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        rows = audit._parse_baseline(committed.read_bytes())
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            temp_repo = temp / "repo"
            temp_baseline = (
                temp_repo
                / "analysis/model_candidates/context_first_scores_v1/"
                "historical_baseline_hashes.csv"
            )
            temp_baseline.parent.mkdir(parents=True)
            temp_baseline.write_bytes(committed.read_bytes())
            hidden = temp / "hidden/export_20260731_150800"
            hidden.mkdir(parents=True)
            (hidden / "untracked.csv").write_bytes(b"historical output\n")
            theoretical = temp_repo / "analysis/theoretical"
            theoretical.mkdir(parents=True)
            (theoretical / "new_track").symlink_to(
                hidden.parent, target_is_directory=True
            )

            with mock.patch.object(
                audit, "build_historical_baseline", return_value=rows
            ), mock.patch.object(
                audit, "_tracked_files", return_value=()
            ), self.assertRaisesRegex(audit.AuditError, "symlink"):
                audit.verify_historical_baseline(temp_repo, temp_baseline)

    def test_unreadable_theoretical_subtree_is_rejected(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        rows = audit._parse_baseline(committed.read_bytes())
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            temp_baseline = (
                temp_repo
                / "analysis/model_candidates/context_first_scores_v1/"
                "historical_baseline_hashes.csv"
            )
            temp_baseline.parent.mkdir(parents=True)
            temp_baseline.write_bytes(committed.read_bytes())
            hidden = (
                temp_repo
                / "analysis/theoretical/new_track/private/"
                "export_20260731_150800"
            )
            hidden.mkdir(parents=True)
            (hidden / "untracked.csv").write_bytes(b"historical output\n")
            unreadable = hidden.parent
            unreadable.chmod(0)
            try:
                with mock.patch.object(
                    audit, "build_historical_baseline", return_value=rows
                ), mock.patch.object(
                    audit, "_tracked_files", return_value=()
                ), self.assertRaisesRegex(audit.AuditError, "cannot scan"):
                    audit.verify_historical_baseline(temp_repo, temp_baseline)
            finally:
                unreadable.chmod(0o700)

    def test_protected_root_ancestor_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            temp_repo = temp / "repo"
            temp_repo.mkdir()
            outside = temp / "outside/model/v7_2_context_scoring"
            outside.mkdir(parents=True)
            (outside / "hidden.csv").write_bytes(b"external bytes\n")
            (temp_repo / "analysis").symlink_to(
                outside.parents[1], target_is_directory=True
            )

            with self.assertRaisesRegex(audit.AuditError, "ancestor.*symlink"):
                audit._scan_tree_fail_closed(
                    temp_repo,
                    temp_repo / "analysis/model/v7_2_context_scoring",
                )

    def test_unstatable_protected_root_is_not_treated_as_absent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            root = temp_repo / "analysis/model_versions"
            root.mkdir(parents=True)
            (root / "hidden.csv").write_bytes(b"historical output\n")
            unreadable = root.parent
            unreadable.chmod(0)
            try:
                with self.assertRaisesRegex(audit.AuditError, "cannot scan"):
                    audit._scan_tree_fail_closed(temp_repo, root)
            finally:
                unreadable.chmod(0o700)

    def test_lstat_helper_rejects_repository_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            with self.assertRaisesRegex(audit.AuditError, "repository root"):
                audit._lstat_repository_path(temp_repo, temp_repo)

    def test_seeded_historical_rows_are_revalidated_after_discovery(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        rows = audit._parse_baseline(committed.read_bytes())
        changed = audit.BaselineRow(
            path=rows[0].path,
            bytes=rows[0].bytes,
            sha256="0" * 64,
            immutability_class=rows[0].immutability_class,
        )
        changed_rows = (changed,) + rows[1:]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            for second_snapshot in (changed_rows, rows[1:]):
                with self.subTest(second_snapshot_size=len(second_snapshot)), mock.patch.object(
                    audit,
                    "build_historical_baseline",
                    side_effect=(rows, second_snapshot),
                ), mock.patch.object(
                    audit, "_tracked_files", return_value=()
                ), self.assertRaisesRegex(
                    audit.AuditError, "changed during working-tree scan"
                ):
                    audit.build_working_tree_baseline(temp_repo)

    def test_complete_working_tree_snapshot_is_revalidated(self) -> None:
        rows = audit.build_historical_baseline(REPO_ROOT)
        promoted = audit.BaselineRow(
            path="analysis/model_versions/v8_context_first/model.csv",
            bytes=3,
            sha256=hashlib.sha256(b"new").hexdigest(),
            immutability_class="frozen_model",
        )
        changed = rows + (promoted,)

        with mock.patch.object(
            audit,
            "_build_working_tree_snapshot",
            side_effect=(rows, changed),
        ), self.assertRaisesRegex(
            audit.AuditError, "protected tree changed during working-tree scan"
        ):
            audit.build_working_tree_baseline(REPO_ROOT)

    def test_untracked_file_mutated_between_complete_snapshots_is_rejected(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            promoted = (
                temp_repo
                / "analysis/model_versions/v8_context_first/model.csv"
            )
            promoted.parent.mkdir(parents=True)
            promoted.write_bytes(b"old")
            real_snapshot = audit._build_working_tree_snapshot
            snapshot_count = 0

            def snapshot_then_mutate(repo: Path) -> tuple[audit.BaselineRow, ...]:
                nonlocal snapshot_count
                result = real_snapshot(repo)
                snapshot_count += 1
                if snapshot_count == 1:
                    promoted.write_bytes(b"new")
                return result

            with mock.patch.object(
                audit, "build_historical_baseline", return_value=()
            ), mock.patch.object(
                audit, "_tracked_files", return_value=()
            ), mock.patch.object(
                audit,
                "_build_working_tree_snapshot",
                side_effect=snapshot_then_mutate,
            ), self.assertRaisesRegex(
                audit.AuditError, "protected tree changed during working-tree scan"
            ):
                audit.build_working_tree_baseline(temp_repo)

            self.assertEqual(2, snapshot_count)

    def test_repository_file_reader_rejects_symlink_leaf(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            repo = temp / "repo"
            repo.mkdir()
            outside = temp / "outside.csv"
            outside.write_bytes(b"outside\n")
            link = repo / "protected.csv"
            link.symlink_to(outside)

            with self.assertRaisesRegex(audit.AuditError, "symlink|regular file"):
                audit._read_repository_file(repo, link)

    def test_repository_file_reader_rejects_fifo_swap_without_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            protected = repo / "protected.csv"
            protected.write_bytes(b"regular\n")
            real_open = audit.os.open

            def swap_leaf_before_open(
                path: object, flags: int, *args: object, **kwargs: object
            ) -> int:
                if path == protected.name and kwargs.get("dir_fd") is not None:
                    self.assertTrue(flags & audit.os.O_NONBLOCK)
                    protected.unlink()
                    audit.os.mkfifo(protected)
                return real_open(path, flags, *args, **kwargs)

            with mock.patch.object(
                audit.os, "open", side_effect=swap_leaf_before_open
            ), self.assertRaisesRegex(audit.AuditError, "not a regular file"):
                audit._read_repository_file(repo, protected)

    def test_reserved_theoretical_export_name_must_be_directory(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        rows = audit._parse_baseline(committed.read_bytes())
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_repo = Path(temp_dir)
            temp_baseline = (
                temp_repo
                / "analysis/model_candidates/context_first_scores_v1/"
                "historical_baseline_hashes.csv"
            )
            temp_baseline.parent.mkdir(parents=True)
            temp_baseline.write_bytes(committed.read_bytes())
            reserved = (
                temp_repo
                / "analysis/theoretical/new_track/export_20260731_150800"
            )
            reserved.parent.mkdir(parents=True)
            audit.os.mkfifo(reserved)

            with mock.patch.object(
                audit, "build_historical_baseline", return_value=rows
            ), mock.patch.object(
                audit, "_tracked_files", return_value=()
            ), self.assertRaisesRegex(audit.AuditError, "reserved.*not a directory"):
                audit.verify_historical_baseline(temp_repo, temp_baseline)

    def test_generation_is_deterministic_and_does_not_mutate_history(self) -> None:
        protected_before = {
            row.path: row.sha256
            for row in audit.build_historical_baseline(REPO_ROOT)
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            report = temp / "CURRENT_CANDIDATE_AUDIT.md"
            baseline = temp / "historical_baseline_hashes.csv"

            audit.write_audit(
                REPO_ROOT,
                report,
                baseline,
                initialize_baseline=True,
            )
            first_report = report.read_bytes()
            first_baseline = baseline.read_bytes()
            audit.write_audit(REPO_ROOT, report, baseline)

            self.assertEqual(first_report, report.read_bytes())
            self.assertEqual(first_baseline, baseline.read_bytes())
            self.assertIn(b"No rankings are published by this audit", first_report)

            committed_report = (
                REPO_ROOT
                / "analysis/model_candidates/context_first_scores_v1/CURRENT_CANDIDATE_AUDIT.md"
            )
            self.assertEqual(first_report, committed_report.read_bytes())
            audit.verify_committed_report(REPO_ROOT, committed_report, baseline)

            stale_report = temp / "stale-report.md"
            stale_report.write_text("stale\n", encoding="utf-8")
            with self.assertRaisesRegex(audit.AuditError, "audit report differs"):
                audit.verify_committed_report(REPO_ROOT, stale_report, baseline)

            with baseline.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(
                ["path", "bytes", "sha256", "immutability_class"],
                list(rows[0]),
            )

        protected_after = {
            row.path: row.sha256
            for row in audit.build_historical_baseline(REPO_ROOT)
        }
        self.assertEqual(protected_before, protected_after)

    def test_existing_baseline_drift_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            report = temp / "CURRENT_CANDIDATE_AUDIT.md"
            baseline = temp / "historical_baseline_hashes.csv"
            baseline.write_text(
                "path,bytes,sha256,immutability_class\n"
                "changed,1,not-the-current-hash,frozen_model\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(audit.AuditError, "differs"):
                audit.write_audit(REPO_ROOT, report, baseline)

            self.assertFalse(report.exists())
            self.assertIn("not-the-current-hash", baseline.read_text(encoding="utf-8"))

            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = audit.main(
                    [
                        "--repo",
                        str(REPO_ROOT),
                        "--output",
                        str(report),
                        "--baseline-output",
                        str(baseline),
                    ]
                )

            self.assertEqual(2, exit_code)
            self.assertEqual("", stdout.getvalue())
            self.assertIn("error_code=AUDIT_INTEGRITY_FAILURE", stderr.getvalue())

    def test_concurrent_history_drift_restores_previous_publication(self) -> None:
        rows = audit.build_historical_baseline(REPO_ROOT)
        changed = audit.BaselineRow(
            path=rows[0].path,
            bytes=rows[0].bytes,
            sha256="0" * 64,
            immutability_class=rows[0].immutability_class,
        )
        drifted = (changed,) + rows[1:]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            report = temp / "CURRENT_CANDIDATE_AUDIT.md"
            baseline = temp / "historical_baseline_hashes.csv"
            report.write_bytes(b"previous report\n")
            baseline.write_bytes(audit._baseline_bytes(rows))

            with mock.patch.object(
                audit,
                "build_historical_baseline",
                side_effect=(rows, rows, rows, rows, drifted, drifted),
            ) as snapshots, self.assertRaisesRegex(
                audit.AuditError, "changed while publishing"
            ):
                audit.write_audit(REPO_ROOT, report, baseline)

            self.assertEqual(6, snapshots.call_count)
            self.assertEqual(b"previous report\n", report.read_bytes())
            self.assertEqual(audit._baseline_bytes(rows), baseline.read_bytes())

    def test_malformed_csv_error_is_normalized(self) -> None:
        oversized = "x" * 140_000
        content = (
            "path,bytes,sha256,immutability_class\n"
            f'"{oversized}",1,{"0" * 64},frozen_model\n'
        ).encode("utf-8")

        with self.assertRaisesRegex(audit.AuditError, "invalid row"):
            audit._parse_baseline(content)

    def test_consumed_temporary_names_are_not_cleaned_up(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            atomic_output = temp / "atomic.md"
            transaction_output = temp / "transaction.md"

            with mock.patch.object(
                audit.Path,
                "unlink",
                side_effect=PermissionError("directory search denied"),
            ) as unlink:
                audit._atomic_write(atomic_output, b"published\n")
                audit._publish_transaction(
                    [(transaction_output, b"published\n")], lambda: None
                )

            unlink.assert_not_called()
            self.assertEqual(b"published\n", atomic_output.read_bytes())
            self.assertEqual(b"published\n", transaction_output.read_bytes())

    def test_concurrent_finding_drift_restores_previous_publication(self) -> None:
        findings = audit.build_findings(REPO_ROOT)
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            report = temp / "CURRENT_CANDIDATE_AUDIT.md"
            baseline = temp / "historical_baseline_hashes.csv"
            report.write_bytes(b"previous report\n")
            baseline.write_bytes(committed.read_bytes())

            with mock.patch.object(
                audit,
                "build_findings",
                side_effect=(findings, findings[:-1]),
            ), self.assertRaisesRegex(audit.AuditError, "evidence changed"):
                audit.write_audit(REPO_ROOT, report, baseline)

            self.assertEqual(b"previous report\n", report.read_bytes())
            self.assertEqual(committed.read_bytes(), baseline.read_bytes())

    def test_noncanonical_baseline_is_rejected_before_publication(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            report = temp / "CURRENT_CANDIDATE_AUDIT.md"
            baseline = temp / "historical_baseline_hashes.csv"
            baseline.write_bytes(committed.read_bytes().replace(b"\n", b"\r\n"))

            with self.assertRaisesRegex(audit.AuditError, "canonical"):
                audit.write_audit(REPO_ROOT, report, baseline)

            self.assertFalse(report.exists())

    def test_committed_report_verification_allows_declared_new_version(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        baseline = committed.read_bytes()
        rows = audit._parse_baseline(baseline)
        promoted = audit.BaselineRow(
            path="analysis/model_versions/v8_context_first/model.csv",
            bytes=3,
            sha256=hashlib.sha256(b"new").hexdigest(),
            immutability_class="frozen_model",
        )
        findings = audit.build_findings(REPO_ROOT)

        with tempfile.TemporaryDirectory() as temp_dir:
            report = Path(temp_dir) / "CURRENT_CANDIDATE_AUDIT.md"
            report.write_bytes(audit._report_bytes(findings, rows, baseline))
            with mock.patch.object(
                audit,
                "build_working_tree_baseline",
                return_value=tuple(sorted(rows + (promoted,), key=lambda row: row.path)),
            ):
                audit.verify_committed_report(
                    REPO_ROOT,
                    report,
                    committed,
                    allowed_new_version="v8_context_first",
                )

    def test_cli_normalizes_filesystem_failures(self) -> None:
        committed = (
            REPO_ROOT
            / "analysis/model_candidates/context_first_scores_v1/historical_baseline_hashes.csv"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            parent_file = temp / "not-a-directory"
            parent_file.write_bytes(b"occupied\n")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = audit.main(
                    [
                        "--repo",
                        str(REPO_ROOT),
                        "--output",
                        str(parent_file / "report.md"),
                        "--baseline-output",
                        str(committed),
                    ]
                )

            self.assertEqual(2, exit_code)
            self.assertEqual("", stdout.getvalue())
            self.assertIn("error_code=AUDIT_INTEGRITY_FAILURE", stderr.getvalue())

    def test_interrupt_between_output_swaps_restores_both_snapshots(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            report = temp / "report.md"
            baseline = temp / "baseline.csv"
            report.write_bytes(b"old report\n")
            baseline.write_bytes(b"old baseline\n")
            real_replace = audit.os.replace
            replace_count = 0

            def interrupt_second_replace(source: Path, destination: Path) -> None:
                nonlocal replace_count
                replace_count += 1
                if replace_count == 2:
                    raise KeyboardInterrupt
                real_replace(source, destination)

            with mock.patch.object(
                audit.os, "replace", side_effect=interrupt_second_replace
            ), self.assertRaises(KeyboardInterrupt):
                audit._publish_transaction(
                    [(report, b"new report\n"), (baseline, b"new baseline\n")],
                    lambda: None,
                )

            self.assertEqual(b"old report\n", report.read_bytes())
            self.assertEqual(b"old baseline\n", baseline.read_bytes())

    def test_staging_write_failure_removes_partial_temporary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            output = temp / "report.md"
            output.write_bytes(b"old report\n")
            real_fdopen = audit.os.fdopen

            class FailingWrite:
                def __init__(self, descriptor: int) -> None:
                    self.handle = real_fdopen(descriptor, "wb")

                def __enter__(self) -> "FailingWrite":
                    return self

                def write(self, content: bytes) -> int:
                    raise OSError("disk full")

                def __exit__(self, *args: object) -> None:
                    self.handle.close()

            with mock.patch.object(
                audit.os,
                "fdopen",
                side_effect=lambda descriptor, mode: FailingWrite(descriptor),
            ), self.assertRaisesRegex(audit.AuditError, "disk full"):
                audit._publish_transaction(
                    [(output, b"new report\n")], lambda: None
                )

            self.assertEqual(b"old report\n", output.read_bytes())
            self.assertEqual([], list(temp.glob(".report.md.*.tmp")))

    def test_prepublication_failure_does_not_restore_untouched_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")

            def concurrent_update_then_fail() -> None:
                output.write_bytes(b"concurrent report\n")
                raise OSError("prepublication failure")

            with self.assertRaisesRegex(
                audit.AuditError, "prepublication failure"
            ):
                audit._publish_transaction(
                    [(output, b"new report\n")], concurrent_update_then_fail
                )

            self.assertEqual(b"concurrent report\n", output.read_bytes())

    def test_rollback_continues_after_second_interrupt(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            outputs = [temp / f"output-{index}.txt" for index in range(3)]
            for index, output in enumerate(outputs):
                output.write_bytes(f"old-{index}\n".encode("utf-8"))
            real_replace = audit.os.replace
            replace_count = 0

            def interrupt_publication_and_first_restore(
                source: Path, destination: Path
            ) -> None:
                nonlocal replace_count
                replace_count += 1
                if replace_count in {3, 4}:
                    raise KeyboardInterrupt
                real_replace(source, destination)

            with mock.patch.object(
                audit.os,
                "replace",
                side_effect=interrupt_publication_and_first_restore,
            ), self.assertRaisesRegex(
                audit.AuditError, "rollback also failed.*KeyboardInterrupt"
            ):
                audit._publish_transaction(
                    [
                        (output, f"new-{index}\n".encode("utf-8"))
                        for index, output in enumerate(outputs)
                    ],
                    lambda: None,
                )

            self.assertEqual(b"old-0\n", outputs[0].read_bytes())
            self.assertEqual(b"new-1\n", outputs[1].read_bytes())
            self.assertEqual(b"old-2\n", outputs[2].read_bytes())

    def test_replace_then_interrupt_is_reconciled_and_rolled_back(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")
            real_replace = audit.os.replace
            replace_count = 0

            def replace_then_interrupt(source: Path, destination: Path) -> None:
                nonlocal replace_count
                replace_count += 1
                real_replace(source, destination)
                if replace_count == 1:
                    raise KeyboardInterrupt

            with mock.patch.object(
                audit.os, "replace", side_effect=replace_then_interrupt
            ), self.assertRaises(KeyboardInterrupt):
                audit._publish_transaction(
                    [(output, b"new report\n")], lambda: None
                )

            self.assertEqual(2, replace_count)
            self.assertEqual(b"old report\n", output.read_bytes())

    def test_cleanup_interrupt_preserves_primary_error_and_continues(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            outputs = [temp / "report.md", temp / "baseline.csv"]
            for output in outputs:
                output.write_bytes(b"old\n")
            real_unlink = audit.Path.unlink
            unlink_count = 0

            def interrupt_first_cleanup(
                path: Path, missing_ok: bool = False
            ) -> None:
                nonlocal unlink_count
                unlink_count += 1
                if unlink_count == 1:
                    raise KeyboardInterrupt
                real_unlink(path, missing_ok=missing_ok)

            def primary_failure() -> None:
                raise ValueError("primary integrity failure")

            with mock.patch.object(
                audit.Path, "unlink", autospec=True, side_effect=interrupt_first_cleanup
            ), self.assertRaisesRegex(ValueError, "primary integrity failure"):
                audit._publish_transaction(
                    [(output, b"new\n") for output in outputs], primary_failure
                )

            self.assertEqual(3, unlink_count)
            self.assertEqual([], list(temp.glob(".*.tmp")))
            self.assertEqual([b"old\n", b"old\n"], [path.read_bytes() for path in outputs])

    def test_unstatable_destination_is_not_restored_without_identity_proof(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")
            real_replace = audit.os.replace
            real_lstat = audit.os.lstat
            replacement_committed = False
            destination_failure_injected = False
            replace_count = 0

            def replace_then_interrupt(source: Path, destination: Path) -> None:
                nonlocal replace_count, replacement_committed
                replace_count += 1
                real_replace(source, destination)
                if replace_count == 1:
                    replacement_committed = True
                    raise KeyboardInterrupt

            def fail_destination_lstat_once(path: Path) -> object:
                nonlocal destination_failure_injected
                if (
                    replacement_committed
                    and not destination_failure_injected
                    and Path(path) == output
                ):
                    destination_failure_injected = True
                    raise PermissionError("destination hidden")
                return real_lstat(path)

            with mock.patch.object(
                audit.os, "replace", side_effect=replace_then_interrupt
            ), mock.patch.object(
                audit.os, "lstat", side_effect=fail_destination_lstat_once
            ), self.assertRaises(KeyboardInterrupt) as raised:
                audit._publish_transaction(
                    [(output, b"new report\n")], lambda: None
                )

            self.assertTrue(destination_failure_injected)
            notes = getattr(raised.exception, "__notes__", [])
            self.assertTrue(any("destination hidden" in note for note in notes), notes)
            self.assertEqual(b"new report\n", output.read_bytes())

    def test_staged_path_substitution_fails_and_restores_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")
            real_replace = audit.os.replace
            replace_count = 0

            def substitute_first_stage(source: Path, destination: Path) -> None:
                nonlocal replace_count
                replace_count += 1
                if replace_count == 1:
                    source.unlink()
                    source.write_bytes(b"substituted bytes\n")
                real_replace(source, destination)

            with mock.patch.object(
                audit.os, "replace", side_effect=substitute_first_stage
            ), self.assertRaisesRegex(
                audit.AuditError, "staged|identity|replacement"
            ):
                audit._publish_transaction(
                    [(output, b"requested bytes\n")], lambda: None
                )

            self.assertEqual(b"old report\n", output.read_bytes())

    def test_atomic_write_accepts_interrupt_after_committed_replace(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")
            real_replace = audit.os.replace

            def replace_then_interrupt(source: Path, destination: Path) -> None:
                real_replace(source, destination)
                raise KeyboardInterrupt

            with mock.patch.object(
                audit.os, "replace", side_effect=replace_then_interrupt
            ):
                audit._atomic_write(output, b"restored report\n")

            self.assertEqual(b"restored report\n", output.read_bytes())

    def test_persistent_cleanup_failure_is_noted_on_primary_error(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")

            def primary_failure() -> None:
                raise ValueError("primary integrity failure")

            with mock.patch.object(
                audit.Path,
                "unlink",
                side_effect=PermissionError("cleanup denied"),
            ), self.assertRaisesRegex(
                ValueError, "primary integrity failure"
            ) as raised:
                audit._publish_transaction(
                    [(output, b"new report\n")], primary_failure
                )

            notes = getattr(raised.exception, "__notes__", [])
            self.assertTrue(any("cleanup denied" in note for note in notes), notes)

    def test_in_place_staged_content_substitution_fails_and_restores(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")
            real_replace = audit.os.replace
            replace_count = 0

            def overwrite_first_stage(source: Path, destination: Path) -> None:
                nonlocal replace_count
                replace_count += 1
                if replace_count == 1:
                    source.write_bytes(b"same inode, different bytes\n")
                real_replace(source, destination)

            with mock.patch.object(
                audit.os, "replace", side_effect=overwrite_first_stage
            ), self.assertRaisesRegex(
                audit.AuditError, "content|hash|replacement"
            ):
                audit._publish_transaction(
                    [(output, b"requested bytes\n")], lambda: None
                )

            self.assertEqual(b"old report\n", output.read_bytes())

    def test_hard_link_alias_is_not_accepted_as_consumed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            source = temp / "stage.tmp"
            destination = temp / "report.md"
            source.write_bytes(b"requested bytes\n")
            destination.hardlink_to(source)
            identity = audit._file_identity(audit.os.lstat(source))

            rollback_owned, source_consumed, errors = audit._replacement_state(
                source,
                destination,
                identity,
                hashlib.sha256(b"requested bytes\n").hexdigest(),
                len(b"requested bytes\n"),
                replacement_attempted=True,
                replacement_returned=False,
            )

            self.assertTrue(rollback_owned)
            self.assertFalse(source_consumed)
            self.assertTrue(any("source" in str(error) for error in errors), errors)

    def test_fstat_interrupt_closes_descriptor_and_removes_temporary(self) -> None:
        for operation in ("transaction", "atomic"):
            with self.subTest(operation=operation), tempfile.TemporaryDirectory() as temp_dir:
                temp = Path(temp_dir)
                output = temp / "report.md"
                output.write_bytes(b"old report\n")
                real_mkstemp = audit.tempfile.mkstemp
                descriptors: list[int] = []

                def recording_mkstemp(*args: object, **kwargs: object) -> tuple[int, str]:
                    descriptor, name = real_mkstemp(*args, **kwargs)
                    descriptors.append(descriptor)
                    return descriptor, name

                with mock.patch.object(
                    audit.tempfile, "mkstemp", side_effect=recording_mkstemp
                ), mock.patch.object(
                    audit.os, "fstat", side_effect=KeyboardInterrupt
                ), self.assertRaises(KeyboardInterrupt):
                    if operation == "transaction":
                        audit._publish_transaction(
                            [(output, b"new report\n")], lambda: None
                        )
                    else:
                        audit._atomic_write(output, b"new report\n")

                self.assertEqual(1, len(descriptors))
                with self.assertRaises(OSError):
                    audit.os.close(descriptors[0])
                self.assertEqual([], list(temp.glob(".report.md.*.tmp")))
                self.assertEqual(b"old report\n", output.read_bytes())

    def test_cli_serializes_exception_notes(self) -> None:
        failure = audit.AuditError("primary failure")
        failure.add_note("staged audit cleanup failed: PermissionError: cleanup denied")
        stdout = io.StringIO()
        stderr = io.StringIO()

        with mock.patch.object(
            audit, "write_audit", side_effect=failure
        ), redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = audit.main(["--repo", str(REPO_ROOT)])

        self.assertEqual(2, exit_code)
        self.assertEqual("", stdout.getvalue())
        self.assertIn("primary failure", stderr.getvalue())
        self.assertIn("cleanup denied", stderr.getvalue())

    def test_stage_loss_before_replace_does_not_restore_untouched_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")

            def remove_stage_before_attempt(
                temporary: Path, *args: object, **kwargs: object
            ) -> None:
                temporary.unlink()
                output.write_bytes(b"concurrent report\n")
                raise audit.AuditError("stage disappeared before replace")

            with mock.patch.object(
                audit,
                "_validate_staged_source",
                side_effect=remove_stage_before_attempt,
            ), mock.patch.object(
                audit, "_atomic_write", wraps=audit._atomic_write
            ) as restore, self.assertRaisesRegex(
                audit.AuditError, "stage disappeared"
            ):
                audit._publish_transaction(
                    [(output, b"new report\n")], lambda: None
                )

            restore.assert_not_called()
            self.assertEqual(b"concurrent report\n", output.read_bytes())

    def test_stage_loss_inside_failed_replace_preserves_concurrent_target(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")

            def lose_stage_without_rename(source: Path, destination: Path) -> None:
                source.unlink()
                destination.write_bytes(b"concurrent report\n")
                raise OSError("replace did not run")

            with mock.patch.object(
                audit.os, "replace", side_effect=lose_stage_without_rename
            ), mock.patch.object(
                audit, "_atomic_write", wraps=audit._atomic_write
            ) as restore, self.assertRaisesRegex(
                audit.AuditError, "replace did not run"
            ):
                audit._publish_transaction(
                    [(output, b"new report\n")], lambda: None
                )

            restore.assert_not_called()
            self.assertEqual(b"concurrent report\n", output.read_bytes())

    def test_recreated_stage_alias_does_not_hide_rollback_ownership(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            output = temp / "report.md"
            output.write_bytes(b"old report\n")
            real_replace = audit.os.replace
            replace_count = 0

            def replace_recreate_alias_then_interrupt(
                source: Path, destination: Path
            ) -> None:
                nonlocal replace_count
                replace_count += 1
                real_replace(source, destination)
                if replace_count == 1:
                    source.hardlink_to(destination)
                    raise KeyboardInterrupt

            with mock.patch.object(
                audit.os,
                "replace",
                side_effect=replace_recreate_alias_then_interrupt,
            ), self.assertRaises(KeyboardInterrupt):
                audit._publish_transaction(
                    [(output, b"new report\n")], lambda: None
                )

            self.assertEqual(b"old report\n", output.read_bytes())
            self.assertEqual([], list(temp.glob(".report.md.*.tmp")))

    def test_descriptor_close_interrupts_are_contained(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            descriptor = audit.os.open(Path(temp_dir), audit.os.O_RDONLY)
            with mock.patch.object(
                audit.os,
                "close",
                side_effect=(KeyboardInterrupt(), KeyboardInterrupt()),
            ):
                failures = audit._close_descriptor_resilient(descriptor)

            self.assertEqual(2, len(failures))
            audit.os.close(descriptor)

    def test_cli_serializes_notes_from_chained_cause(self) -> None:
        cause = PermissionError("publication denied")
        cause.add_note("audit replacement reconciliation: stage lost")
        failure = audit.AuditError("publication filesystem failure")
        failure.__cause__ = cause
        stdout = io.StringIO()
        stderr = io.StringIO()

        with mock.patch.object(
            audit, "write_audit", side_effect=failure
        ), redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = audit.main(["--repo", str(REPO_ROOT)])

        self.assertEqual(2, exit_code)
        self.assertEqual("", stdout.getvalue())
        self.assertIn("stage lost", stderr.getvalue())

    def test_publication_does_not_report_already_absent_target_as_rollback_failure(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            parent_file = Path(temp_dir) / "not-a-directory"
            parent_file.write_bytes(b"occupied\n")
            output = parent_file / "report.md"

            with self.assertRaisesRegex(
                audit.AuditError, "publication filesystem failure"
            ) as raised:
                audit._publish_transaction([(output, b"report\n")], lambda: None)

            self.assertIsInstance(raised.exception.__cause__, FileExistsError)
            self.assertNotIn("rollback also failed", str(raised.exception))

    def test_publication_reports_genuine_rollback_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "report.md"
            output.write_bytes(b"old report\n")

            integrity_checks = 0

            def postpublication_failure() -> None:
                nonlocal integrity_checks
                integrity_checks += 1
                if integrity_checks == 2:
                    raise FileExistsError("publication failed")

            with mock.patch.object(
                audit,
                "_atomic_write",
                side_effect=PermissionError("restore denied"),
            ), self.assertRaisesRegex(
                audit.AuditError,
                "publication failed.*rollback also failed.*restore denied",
            ) as raised:
                audit._publish_transaction(
                    [(output, b"new report\n")], postpublication_failure
                )

            self.assertIsInstance(raised.exception.__cause__, FileExistsError)

    def test_baseline_initialization_is_explicit_and_one_time(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            report = temp / "CURRENT_CANDIDATE_AUDIT.md"
            baseline = temp / "historical_baseline_hashes.csv"

            with self.assertRaisesRegex(audit.AuditError, "baseline missing"):
                audit.write_audit(REPO_ROOT, report, baseline)
            self.assertFalse(report.exists())
            self.assertFalse(baseline.exists())

            audit.write_audit(
                REPO_ROOT,
                report,
                baseline,
                initialize_baseline=True,
            )
            with self.assertRaisesRegex(audit.AuditError, "already exists"):
                audit.write_audit(
                    REPO_ROOT,
                    report,
                    baseline,
                    initialize_baseline=True,
                )

    def test_output_paths_cannot_alias_or_target_protected_history(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp = Path(temp_dir)
            same_output = temp / "same-output"
            with self.assertRaisesRegex(audit.AuditError, "must be distinct"):
                audit.write_audit(
                    REPO_ROOT,
                    same_output,
                    same_output,
                    initialize_baseline=True,
                )
            self.assertFalse(same_output.exists())

            protected_output = (
                REPO_ROOT / "analysis/model_versions/D1_MUST_NOT_WRITE.md"
            )
            self.assertFalse(protected_output.exists())
            with self.assertRaisesRegex(audit.AuditError, "protected output"):
                audit.write_audit(
                    REPO_ROOT,
                    protected_output,
                    temp / "baseline.csv",
                    initialize_baseline=True,
                )
            self.assertFalse(protected_output.exists())

            unowned_output = REPO_ROOT / "D1_MUST_NOT_WRITE.md"
            self.assertFalse(unowned_output.exists())
            with self.assertRaisesRegex(audit.AuditError, "D1-owned output"):
                audit.write_audit(
                    REPO_ROOT,
                    unowned_output,
                    temp / "second-baseline.csv",
                    initialize_baseline=True,
                )
            self.assertFalse(unowned_output.exists())


if __name__ == "__main__":
    unittest.main()
