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

    def test_routed_is_not_added_to_deployed_arithmetic(self):
        spec = module.SourceSpec(
            batch_id="batch",
            cohort="current",
            batch_path="data/batch",
            normalization_commit="a" * 40,
            archive_name="batch.tar.xz",
            expected_archive_sha256="b" * 64,
            manifest_path="artifact_hashes.csv",
            manifest_base_path=".",
            summary_path="normalization_summary.json",
            validation_path="validation_report.json",
            battles_path="battles.jsonl",
            consolidated_path="troop_battle_consolidated.jsonl",
            schema_version="2.0.0",
        )
        battles = [
            {
                "battle_id": "b1",
                "battle_context": "field",
                "game_track": "realm_of_thrones",
                "game_version": "1.4.x",
                "player_side": "attacker",
            }
        ]
        rows = [
            {
                "battle_id": "b1",
                "battle_context": "field",
                "display_name_normalized": "troop",
                "display_names_raw": ["Troop [T1]"],
                "game_track": "realm_of_thrones",
                "deployed": 5,
                "survivors": 5,
                "kills": 1,
                "deaths": 0,
                "wounded": 0,
                "routed": 2,
                "needs_review": False,
            }
        ]

        validated_battles, validated_rows = module.validate_field_projection(
            spec,
            battles,
            rows,
            "realm_of_thrones",
            "1.4.x",
        )

        self.assertEqual(validated_battles, battles)
        self.assertEqual(validated_rows, rows)

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
        battle_context="field",
        results=None,
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
                        "battle_context": battle_context,
                        "game_track": track,
                        "game_version": "1.4.x",
                        "player_side": "attacker",
                        "result": result,
                    },
                    sort_keys=True,
                )
                + "\n"
                for battle_id, result in zip(
                    battle_ids,
                    results or ["Victory"] * len(battle_ids),
                    strict=True,
                )
            ),
            "troop_battle_consolidated.jsonl": "".join(
                json.dumps(
                    {
                        "battle_id": battle_id,
                        "battle_context": battle_context,
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

    def write_config(self, sources, battle_context="field"):
        config = {
            "analysis_id": "test-compatible-field",
            "bootstrap_repetitions": 200,
            "context": battle_context,
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

    def test_configured_siege_attack_context_is_joined_and_gated(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["s1", "s2", "s3"],
            [5, 10, 15],
            battle_context="siege_attack",
        )
        current = self.make_source(
            "current",
            "current",
            ["s4", "s5"],
            [20, 25],
            battle_context="siege_attack",
        )
        config_path = self.write_config([baseline, current], "siege_attack")
        analysis_dir = self.batch_dir / "analysis"
        (analysis_dir / "context_coverage.csv").write_text(
            "context,independent_battles,observed_labels,deployed,reliable_labels,"
            "insufficient_labels,minimum_battles,minimum_deployed\n"
            "field,1,2,158,0,2,5,20\n"
            "siege_attack,2,1,10,0,1,5,20\n",
            encoding="utf-8",
        )
        (analysis_dir / "focus_troop_contexts.csv").write_text(
            "context,provisional_slug,independent_battles,deployed,reliability_status\n"
            "field,ravens_teeth,0,0,not_observed\n"
            "field,other_troop,1,158,insufficient_evidence\n"
            "siege_attack,ravens_teeth,2,10,insufficient_evidence\n",
            encoding="utf-8",
        )
        (analysis_dir / "validation_report.json").write_text(
            '{"review": {"decisions": 11}, "status": "passed"}\n',
            encoding="utf-8",
        )

        result = module.run_analysis(
            config_path, self.root, self.batch_dir, self.identity_root
        )

        self.assertEqual(result["reliable_rows"], 1)
        decision = json.loads(
            (
                self.batch_dir / "analysis" / "compatibility_decision_siege_attack.json"
            ).read_text()
        )
        self.assertEqual(decision["context"], "siege_attack")
        self.assertEqual(
            decision["decision"],
            "compatible_on_common_player_siege_attack_count_projection",
        )
        report = (analysis_dir / "ANALYSIS_REPORT_siege_attack.md").read_text()
        self.assertIn("current-batch siege attack display gate", report)
        self.assertNotIn("current-batch field", report)
        self.assertIn("Ravens' Teeth was not observed in `field`", report)
        self.assertNotIn("158 deployed", report)
        self.assertNotIn("Ravens' Teeth in `siege_attack`", report)
        self.assertIn("`combined_battle_provenance_siege_attack.csv`", report)
        self.assertIn("11 batch-level review decisions", report)
        self.assertNotIn("field-level review decisions", report)

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
        report = (self.batch_dir / "analysis" / "ANALYSIS_REPORT.md").read_text()
        self.assertIn(
            "Every observed label resolves to exactly one canonical ID", report
        )
        self.assertNotIn("remain provisional: .", report)

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

    def test_contradictory_normalization_boundary_alias_is_rejected(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b1"],
            [5],
            validation_overrides={"contexts_pooled": True},
        )
        current = self.make_source("current", "current", ["b2"], [10])
        config_path = self.write_config([baseline, current])

        with self.assertRaisesRegex(ValueError, "contexts_pooled"):
            module.run_analysis(
                config_path, self.root, self.batch_dir, self.identity_root
            )

    def test_compatible_normalization_boundary_aliases_are_recorded(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b1"],
            [5],
            validation_overrides={"contexts_pooled": False},
        )
        current = self.make_source("current", "current", ["b2"], [10])
        config_path = self.write_config([baseline, current])

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        decision = json.loads(
            (self.batch_dir / "analysis" / "compatibility_decision.json").read_text()
        )
        baseline_evidence = next(
            source for source in decision["sources"] if source["batch_id"] == "baseline"
        )["normalization_boundary_evidence"]["context_boundaries_preserved"]
        self.assertEqual(
            baseline_evidence,
            {
                "status": "verified",
                "reported_fields": [
                    {
                        "source_field": "context_boundaries_preserved",
                        "reported_value": True,
                        "expected_reported_value": True,
                    },
                    {
                        "source_field": "contexts_pooled",
                        "reported_value": False,
                        "expected_reported_value": False,
                    },
                ],
                "canonical_value": True,
            },
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
            "baseline", "baseline", ["b1", "b3", "b5"], [1, 8, 20]
        )
        current = self.make_source(
            "current", "current", ["b2", "b4", "b6"], [2, 15, 25]
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
        ranking = next(
            row
            for row in module.base.read_csv(
                self.batch_dir / "analysis" / "combined_ranking_complete.csv"
            )
            if row["provisional_slug"] == "ravens_teeth"
        )
        comparison = next(
            row
            for row in module.base.read_csv(
                self.batch_dir / "analysis" / "ravens_teeth_comparison.csv"
            )
            if row["cohort"] == "combined"
        )
        self.assertEqual(comparison["ci95_low"], ranking["ci95_low"])
        self.assertEqual(comparison["ci95_high"], ranking["ci95_high"])

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

    def test_focus_outputs_and_report_follow_the_configured_focus(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b1", "b2", "b3"],
            [5, 10, 15],
            slug="wolf_guard",
            track="other_track",
        )
        current = self.make_source(
            "current",
            "current",
            ["b4", "b5"],
            [20, 25],
            slug="wolf_guard",
            track="other_track",
        )
        config_path = self.write_config([baseline, current])
        config = json.loads(config_path.read_text())
        config["focus_slug"] = "wolf_guard"
        config["focus_label"] = "Wolf Guard"
        config["track"] = "other_track"
        config_path.write_text(json.dumps(config), encoding="utf-8")

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        analysis_dir = self.batch_dir / "analysis"
        self.assertTrue((analysis_dir / "wolf_guard_comparison.csv").is_file())
        self.assertTrue((analysis_dir / "wolf_guard_battle_rates.csv").is_file())
        self.assertTrue((analysis_dir / "wolf_guard_delta_uncertainty.json").is_file())
        report = (analysis_dir / "ANALYSIS_REPORT.md").read_text()
        self.assertIn("## Wolf Guard focus", report)
        self.assertNotIn("## Ravens' Teeth focus", report)
        self.assertIn("The 2.0.0 normalized schemas are joined", report)
        self.assertIn("The schema join across 2.0.0 is deliberately narrow", report)
        self.assertNotIn("1.1.0, 2.0.0", report)
        self.assertIn("`wolf_guard` (provisional)", report)
        self.assertIn("versioned audit for track `other_track`", report)
        self.assertNotIn("Realm of Thrones audit", report)

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

    def test_report_preserves_standalone_context_boundaries(self):
        baseline = self.make_source(
            "baseline", "baseline", ["b0", "b1", "b2", "b3", "b4"], [5] * 5
        )
        current = self.make_source(
            "current", "current", ["b5", "b6", "b7", "b8", "b9"], [10] * 5
        )
        config_path = self.write_config([baseline, current])
        analysis_dir = self.batch_dir / "analysis"
        (analysis_dir / "context_coverage.csv").write_text(
            "context,independent_battles,observed_labels,deployed,reliable_labels,"
            "insufficient_labels,minimum_battles,minimum_deployed\n"
            "field,5,2,40,1,1,5,20\n"
            "siege_attack,1,3,30,0,3,5,20\n"
            "siege_defense,0,0,0,0,0,5,20\n",
            encoding="utf-8",
        )
        (analysis_dir / "focus_troop_contexts.csv").write_text(
            "context,independent_battles,deployed,reliability_status\n"
            "field,5,25,reliable\n"
            "siege_attack,1,20,insufficient_evidence\n",
            encoding="utf-8",
        )

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        report = (analysis_dir / "ANALYSIS_REPORT.md").read_text()
        self.assertIn("## Current batch context coverage", report)
        self.assertIn("| `siege_attack` | 1 | 3 | 30 | 0 | 3 |", report)
        self.assertIn("| `siege_defense` | 0 | 0 | 0 | 0 | 0 |\n\n-", report)
        self.assertIn(
            "Ravens' Teeth in `siege_attack` remains below the display gate with "
            "1 battle and 20 deployed",
            report,
        )
        self.assertIn("No field and siege observations are pooled", report)

    def test_report_distinguishes_not_observed_context(self):
        baseline = self.make_source(
            "baseline", "baseline", ["b0", "b1", "b2", "b3", "b4"], [5] * 5
        )
        current = self.make_source(
            "current", "current", ["b5", "b6", "b7", "b8", "b9"], [10] * 5
        )
        config_path = self.write_config([baseline, current])
        analysis_dir = self.batch_dir / "analysis"
        (analysis_dir / "context_coverage.csv").write_text(
            "context,independent_battles,observed_labels,deployed,reliable_labels,"
            "insufficient_labels,minimum_battles,minimum_deployed\n"
            "field,5,1,25,1,0,5,20\n"
            "siege_defense,1,2,30,0,2,5,20\n",
            encoding="utf-8",
        )
        (analysis_dir / "focus_troop_contexts.csv").write_text(
            "context,independent_battles,deployed,reliability_status\n"
            "field,5,25,reliable\n"
            "siege_defense,0,0,not_observed\n",
            encoding="utf-8",
        )

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        report = (analysis_dir / "ANALYSIS_REPORT.md").read_text()
        self.assertIn(
            "Ravens' Teeth was not observed in `siege_defense`; no rate from another "
            "context is substituted",
            report,
        )
        self.assertNotIn("`siege_defense` remains below", report)

    def test_standalone_context_gate_must_match_combined_config(self):
        baseline = self.make_source("baseline", "baseline", ["b0"], [5])
        current = self.make_source("current", "current", ["b1"], [10])
        config_path = self.write_config([baseline, current])
        analysis_dir = self.batch_dir / "analysis"
        (analysis_dir / "context_coverage.csv").write_text(
            "context,independent_battles,observed_labels,deployed,reliable_labels,"
            "insufficient_labels,minimum_battles,minimum_deployed\n"
            "field,1,1,5,0,1,3,20\n",
            encoding="utf-8",
        )

        with self.assertRaisesRegex(ValueError, "standalone context gate mismatch"):
            module.run_analysis(
                config_path, self.root, self.batch_dir, self.identity_root
            )

    def test_outcome_composition_is_preserved_and_disclosed(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b0", "b1", "b2", "b3", "b4"],
            [5] * 5,
        )
        current = self.make_source(
            "current",
            "current",
            ["b5", "b6", "b7", "b8", "b9"],
            [10] * 5,
            results=["Victory", "Victory", "Victory", "Victory", "Defeat"],
        )
        config_path = self.write_config([baseline, current])

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        analysis_dir = self.batch_dir / "analysis"
        provenance = module.base.read_csv(
            analysis_dir / "combined_battle_provenance.csv"
        )
        self.assertEqual(
            [row["result"] for row in provenance if row["cohort"] == "current"],
            ["Victory", "Victory", "Victory", "Victory", "Defeat"],
        )
        report = (analysis_dir / "ANALYSIS_REPORT.md").read_text()
        self.assertIn(
            "baseline 5 Victory; current 4 Victory, 1 Defeat; combined 9 Victory, 1 Defeat",
            report,
        )
        self.assertIn("cohort contrast is outcome-confounded", report)
        self.assertNotIn("victory-only", report)

    def test_single_source_current_interval_matches_standalone_seed(self):
        baseline = self.make_source(
            "baseline", "baseline", ["b0", "b1", "b2", "b3", "b4"], [5] * 5
        )
        current = self.make_source(
            "current", "current", ["b5", "b6", "b7", "b8", "b9"], [1, 3, 5, 7, 9]
        )
        config_path = self.write_config([baseline, current])

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        comparison = next(
            row
            for row in module.base.read_csv(
                self.batch_dir / "analysis" / "ravens_teeth_comparison.csv"
            )
            if row["cohort"] == "current"
        )
        expected_low, expected_high = module.base.bootstrap_interval(
            [
                {"battle_id": battle_id, "deployed": 5, "kills": kills}
                for battle_id, kills in zip(
                    ["b5", "b6", "b7", "b8", "b9"],
                    [1, 3, 5, 7, 9],
                    strict=True,
                )
            ],
            "current",
            "field",
            "ravens_teeth",
            200,
        )
        self.assertEqual(comparison["ci95_low"], f"{expected_low:.6f}")
        self.assertEqual(comparison["ci95_high"], f"{expected_high:.6f}")

    def test_bootstrap_interval_is_row_order_independent(self):
        rows = [
            {"battle_id": battle_id, "deployed": 5, "kills": kills}
            for battle_id, kills in zip(
                ["b5", "b6", "b7", "b8", "b9"],
                [1, 3, 5, 7, 9],
                strict=True,
            )
        ]

        forward = module.base.bootstrap_interval(
            rows, "current", "field", "ravens_teeth", 200
        )
        reversed_order = module.base.bootstrap_interval(
            list(reversed(rows)), "current", "field", "ravens_teeth", 200
        )

        self.assertEqual(forward, reversed_order)

    def test_delta_names_the_actual_below_gate_cohort(self):
        baseline = self.make_source("baseline", "baseline", ["b0"], [5])
        current = self.make_source(
            "current",
            "current",
            ["b1", "b2", "b3", "b4", "b5"],
            [5, 10, 15, 20, 25],
        )
        config_path = self.write_config([baseline, current])

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        delta = json.loads(
            (
                self.batch_dir / "analysis" / "ravens_teeth_delta_uncertainty.json"
            ).read_text()
        )
        self.assertEqual(delta["evidence_status"], "diagnostic_only_below_display_gate")
        self.assertEqual(delta["below_display_gate"], ["baseline"])
        self.assertFalse(delta["report_displayed"])
        report = (self.batch_dir / "analysis" / "ANALYSIS_REPORT.md").read_text()
        self.assertIn("below-gate cohorts: baseline", report)
        self.assertIn("No increase or decline is claimed", report)

    def test_reliable_delta_is_displayed_with_its_interval(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b1", "b2", "b3", "b4", "b5"],
            [5, 5, 5, 5, 5],
        )
        current = self.make_source(
            "current",
            "current",
            ["b6", "b7", "b8", "b9", "b10"],
            [10, 10, 10, 10, 10],
        )
        config_path = self.write_config([baseline, current])

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        delta = json.loads(
            (
                self.batch_dir / "analysis" / "ravens_teeth_delta_uncertainty.json"
            ).read_text()
        )
        self.assertEqual(delta["evidence_status"], "reliable")
        self.assertEqual(delta["below_display_gate"], [])
        self.assertTrue(delta["report_displayed"])
        report = (self.batch_dir / "analysis" / "ANALYSIS_REPORT.md").read_text()
        self.assertIn("Current minus baseline: 1.000 kills/deployed", report)
        self.assertIn("95% battle bootstrap 1.000–1.000", report)
        self.assertIn("interval excludes zero on the increase side", report)
        self.assertNotIn("No increase or decline is claimed", report)

    def test_reliable_delta_crossing_zero_does_not_establish_direction(self):
        baseline = self.make_source(
            "baseline",
            "baseline",
            ["b1", "b2", "b3", "b4", "b5"],
            [1, 1, 1, 1, 10],
        )
        current = self.make_source(
            "current",
            "current",
            ["b6", "b7", "b8", "b9", "b10"],
            [1, 1, 1, 1, 9],
        )
        config_path = self.write_config([baseline, current])

        module.run_analysis(config_path, self.root, self.batch_dir, self.identity_root)

        delta = json.loads(
            (
                self.batch_dir / "analysis" / "ravens_teeth_delta_uncertainty.json"
            ).read_text()
        )
        self.assertLessEqual(delta["ci95_low"], 0)
        self.assertGreaterEqual(delta["ci95_high"], 0)
        report = (self.batch_dir / "analysis" / "ANALYSIS_REPORT.md").read_text()
        self.assertIn(
            "The interval crosses zero, so no increase or decline is established",
            report,
        )


if __name__ == "__main__":
    unittest.main()
