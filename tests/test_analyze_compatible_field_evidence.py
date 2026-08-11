import base64
import csv
import hashlib
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts.analysis import analyze_compatible_field_evidence as module


class CompatibleFieldEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.batch_dir = self.root / "data" / "output"
        analysis_dir = self.batch_dir / "analysis"
        analysis_dir.mkdir(parents=True)
        (self.batch_dir / "review").mkdir()
        (analysis_dir / "README.md").write_text("# Standalone\n", encoding="utf-8")
        (analysis_dir / "validation_report.json").write_text(
            '{"status": "passed"}\n', encoding="utf-8"
        )
        self.identity_root = self.root / "data" / "identity"
        self.identity_root.mkdir(parents=True)
        (self.identity_root / "troops.csv").write_text(
            "troop_id,name\nravens_teeth,Ravens' Teeth\n", encoding="utf-8"
        )

    def tearDown(self):
        self.temp.cleanup()

    def make_source(
        self,
        batch_id,
        cohort,
        battle_ids,
        kills,
        *,
        track="realm_of_thrones",
        schema_version="2.0.0",
        include_boundary_flags=True,
        validation_overrides=None,
        slug="ravens_teeth",
    ):
        display_name = (
            "Ravens' Teeth"
            if slug == "ravens_teeth"
            else slug.replace("_", " ").title()
        )
        batch_path = self.root / "data" / batch_id
        bundle = batch_path / "bundle"
        bundle.mkdir(parents=True)
        archive_name = f"{batch_id}.tar.xz"
        archive_root = f"normalized-{batch_id}"
        files = {
            "normalization_summary.json": json.dumps(
                {
                    "batch_id": batch_id,
                    "schema_version": schema_version,
                    "game_track": track,
                    "game_version": "1.4.x",
                },
                sort_keys=True,
            )
            + "\n",
            "battles.jsonl": "".join(
                json.dumps(
                    {
                        "battle_id": battle_id,
                        "battle_context": "field",
                        "game_track": track,
                        "game_version": "1.4.x",
                        "player_side": "attacker",
                    },
                    sort_keys=True,
                )
                + "\n"
                for battle_id in battle_ids
            ),
            "troop_battle_consolidated.jsonl": "".join(
                json.dumps(
                    {
                        "battle_id": battle_id,
                        "battle_context": "field",
                        "display_name_normalized": slug,
                        "display_names_raw": [f"{display_name} [T6]"],
                        "game_track": track,
                        "deployed": 5,
                        "survivors": 5,
                        "kills": kill_count,
                        "deaths": 0,
                        "wounded": 0,
                        "routed": 0,
                        "needs_review": False,
                    },
                    sort_keys=True,
                )
                + "\n"
                for battle_id, kill_count in zip(battle_ids, kills, strict=True)
            ),
        }
        validation = {
            "schema_version": schema_version,
            "status": "passed",
            "validation_errors": [],
        }
        if include_boundary_flags:
            validation.update(
                {
                    "context_boundaries_preserved": True,
                    "heroes_in_primary": False,
                    "offscreen_rows_inferred": False,
                    "sides_pooled": False,
                }
            )
        validation.update(validation_overrides or {})
        files["validation_report.json"] = json.dumps(validation, sort_keys=True) + "\n"
        manifest = io.StringIO()
        writer = csv.DictWriter(
            manifest, fieldnames=("file", "sha256", "size_bytes"), lineterminator="\n"
        )
        writer.writeheader()
        for name, text in sorted(files.items()):
            encoded = text.encode()
            writer.writerow(
                {
                    "file": name,
                    "sha256": hashlib.sha256(encoded).hexdigest(),
                    "size_bytes": len(encoded),
                }
            )
        files["artifact_hashes.csv"] = manifest.getvalue()

        archive_path = bundle / archive_name
        with tarfile.open(archive_path, "w:xz") as archive:
            directory = tarfile.TarInfo(archive_root)
            directory.type = tarfile.DIRTYPE
            archive.addfile(directory)
            for name, text in sorted(files.items()):
                encoded = text.encode()
                info = tarfile.TarInfo(f"{archive_root}/{name}")
                info.size = len(encoded)
                archive.addfile(info, io.BytesIO(encoded))
        archive_hash = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        part = bundle / f"{archive_name}.base64.part-00"
        part.write_bytes(base64.b64encode(archive_path.read_bytes()))
        archive_path.unlink()
        return {
            "archive_name": archive_name,
            "batch_id": batch_id,
            "batch_path": str(batch_path.relative_to(self.root)),
            "battles_path": f"{archive_root}/battles.jsonl",
            "cohort": cohort,
            "consolidated_path": f"{archive_root}/troop_battle_consolidated.jsonl",
            "expected_archive_sha256": archive_hash,
            "manifest_base_path": archive_root,
            "manifest_path": f"{archive_root}/artifact_hashes.csv",
            "normalization_commit": "a" * 40,
            "schema_version": schema_version,
            "summary_path": f"{archive_root}/normalization_summary.json",
            "validation_path": f"{archive_root}/validation_report.json",
        }

    def write_config(self, sources):
        config = {
            "analysis_id": "test-compatible-field",
            "bootstrap_repetitions": 200,
            "focus_slug": "ravens_teeth",
            "focus_label": "Ravens' Teeth",
            "game_version": "1.4.x",
            "minimum_battles": 5,
            "minimum_deployed": 20,
            "sources": sources,
            "track": "realm_of_thrones",
        }
        path = self.batch_dir / "analysis" / "compatible_field_sources.json"
        path.write_text(json.dumps(config), encoding="utf-8")
        return path

    def test_real_archives_are_verified_joined_and_gated(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b1", "b2", "b3"],
            [5, 10, 15],
            schema_version="1.1.0",
            include_boundary_flags=False,
        )
        current = self.make_source("current", "current", ["b4", "b5"], [20, 25])
        config_path = self.write_config([baseline, current])

        result = module.run_analysis(
            config_path, self.root, self.batch_dir, self.identity_root
        )

        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["independent_battles"], 5)
        self.assertEqual(result["reliable_rows"], 1)
        ranking = module.base.read_csv(
            self.batch_dir / "analysis" / "combined_ranking_reliable.csv"
        )
        self.assertEqual(ranking[0]["canonical_troop_id"], "ravens_teeth")
        self.assertEqual(ranking[0]["kills_per_deployed"], "3.000000")
        comparison = module.base.read_csv(
            self.batch_dir / "analysis" / "ravens_teeth_comparison.csv"
        )
        self.assertEqual(comparison[1]["reliability_status"], "insufficient_evidence")
        self.assertEqual(comparison[2]["reliability_status"], "reliable")
        decision = json.loads(
            (self.batch_dir / "analysis" / "compatibility_decision.json").read_text()
        )
        self.assertTrue(decision["checks"]["artifact_manifests_verified"])
        baseline_verification = next(
            source for source in decision["sources"] if source["batch_id"] == "baseline"
        )
        self.assertEqual(
            baseline_verification["unverified_normalization_boundary_flags"],
            [
                "sides_pooled",
                "offscreen_rows_inferred",
                "heroes_in_primary",
                "context_boundaries_preserved",
            ],
        )
        self.assertNotIn("player_and_enemy_not_pooled", decision["checks"])
        self.assertNotIn("count_projection_semantics_match", decision["checks"])
        self.assertEqual(decision["compatibility_basis"]["status"], "analysis_decision")

    def test_duplicate_battle_ids_are_rejected_as_non_independent(self):
        baseline = self.make_source("baseline", "baseline", ["same"], [5])
        current = self.make_source("current", "current", ["same"], [10])
        config_path = self.write_config([baseline, current])

        with self.assertRaisesRegex(ValueError, "battle ID collision"):
            module.run_analysis(
                config_path, self.root, self.batch_dir, self.identity_root
            )

    def test_archive_name_cannot_escape_bundle_directory(self):
        source = self.make_source("baseline", "baseline", ["b1"], [5])
        source["archive_name"] = "../evidence.tar.xz"

        with self.assertRaisesRegex(
            ValueError, "invalid compatible source archive_name"
        ):
            module.SourceSpec.from_dict(source)

    def test_explicit_normalization_boundary_violation_is_rejected(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b1"],
            [5],
            validation_overrides={"sides_pooled": True},
        )
        current = self.make_source("current", "current", ["b2"], [10])
        config_path = self.write_config([baseline, current])

        with self.assertRaisesRegex(ValueError, "sides_pooled"):
            module.run_analysis(
                config_path, self.root, self.batch_dir, self.identity_root
            )

    def test_legacy_errors_are_rejected_when_validation_errors_are_empty(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b1"],
            [5],
            validation_overrides={"errors": ["legacy failure"]},
        )
        current = self.make_source("current", "current", ["b2"], [10])
        config_path = self.write_config([baseline, current])

        with self.assertRaisesRegex(ValueError, "normalization validation has errors"):
            module.run_analysis(
                config_path, self.root, self.batch_dir, self.identity_root
            )

    def test_tampered_archive_is_rejected_before_analysis(self):
        baseline = self.make_source("baseline", "baseline", ["b1"], [5])
        current = self.make_source("current", "current", ["b2"], [10])
        part = next(
            (self.root / current["batch_path"] / "bundle").glob("*.base64.part-*")
        )
        archive = bytearray(base64.b64decode(part.read_bytes()))
        archive[-1] ^= 1
        part.write_bytes(base64.b64encode(archive))
        config_path = self.write_config([baseline, current])

        with self.assertRaisesRegex(ValueError, "archive SHA-256 mismatch"):
            module.run_analysis(
                config_path, self.root, self.batch_dir, self.identity_root
            )

    def test_bootstrap_outputs_are_independent_of_source_config_order(self):
        baseline = self.make_source(
            "baseline", "baseline", ["b1", "b2", "b3"], [1, 8, 20]
        )
        current = self.make_source(
            "current", "current", ["b4", "b5", "b6"], [2, 15, 25]
        )
        config_path = self.write_config([baseline, current])
        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)
        first_ranking = (
            self.batch_dir / "analysis" / "combined_ranking_complete.csv"
        ).read_bytes()
        first_comparison = (
            self.batch_dir / "analysis" / "ravens_teeth_comparison.csv"
        ).read_bytes()
        first_delta = (
            self.batch_dir / "analysis" / "ravens_teeth_delta_uncertainty.json"
        ).read_bytes()

        self.write_config([current, baseline])
        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        self.assertEqual(
            first_ranking,
            (
                self.batch_dir / "analysis" / "combined_ranking_complete.csv"
            ).read_bytes(),
        )
        self.assertEqual(
            first_comparison,
            (self.batch_dir / "analysis" / "ravens_teeth_comparison.csv").read_bytes(),
        )
        self.assertEqual(
            first_delta,
            (
                self.batch_dir / "analysis" / "ravens_teeth_delta_uncertainty.json"
            ).read_bytes(),
        )

    def test_focus_slug_must_be_a_safe_output_stem(self):
        baseline = self.make_source("baseline", "baseline", ["b1"], [5])
        current = self.make_source("current", "current", ["b2"], [10])
        config_path = self.write_config([baseline, current])
        config = json.loads(config_path.read_text())
        config["focus_slug"] = "../ravens_teeth"
        config_path.write_text(json.dumps(config), encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "invalid focus_slug"):
            module.run_analysis(
                config_path, self.root, self.batch_dir, self.identity_root
            )

    def test_focus_output_filenames_follow_the_configured_slug(self):
        baseline = self.make_source(
            "baseline", "baseline", ["b1", "b2", "b3"], [5, 10, 15], slug="wolf_guard"
        )
        current = self.make_source(
            "current", "current", ["b4", "b5"], [20, 25], slug="wolf_guard"
        )
        config_path = self.write_config([baseline, current])
        config = json.loads(config_path.read_text())
        config["focus_slug"] = "wolf_guard"
        config["focus_label"] = "Wolf Guard"
        config_path.write_text(json.dumps(config), encoding="utf-8")

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        analysis_dir = self.batch_dir / "analysis"
        self.assertTrue((analysis_dir / "wolf_guard_comparison.csv").is_file())
        self.assertTrue((analysis_dir / "wolf_guard_battle_rates.csv").is_file())
        self.assertTrue((analysis_dir / "wolf_guard_delta_uncertainty.json").is_file())

    def test_report_gate_statement_uses_the_current_battle_count(self):
        baseline = self.make_source("baseline", "baseline", ["b0"], [5])
        current = self.make_source(
            "current",
            "current",
            ["b1", "b2", "b3", "b4", "b5"],
            [5, 10, 15, 20, 25],
        )
        config_path = self.write_config([baseline, current])

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        report = (self.batch_dir / "analysis" / "ANALYSIS_REPORT.md").read_text()
        self.assertIn("Per-label standalone eligibility", report)
        self.assertNotIn("none can clear", report)


if __name__ == "__main__":
    unittest.main()
