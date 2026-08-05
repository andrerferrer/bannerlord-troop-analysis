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
                "ALTERNATIVE_POLICY_UNDECLARED",
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
            ("v7.1", "SOURCE_ARTIFACT_ABSENT", "general model CSV"),
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
                "analysis/model_versions/v7.3_tooltip_damage_burst/bannerlord_v73_tooltip_damage_burst_model_all_official_troops.csv",
            },
            absent_paths,
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

            with self.assertRaisesRegex(
                audit.AuditError, "refusing to rewrite"
            ):
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
