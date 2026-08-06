from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from typing import Callable


REPO = Path(__file__).resolve().parents[1]
VALIDATOR = (
    REPO
    / ".agents/skills/normalize-bannerlord-combat-batch/scripts/validate_phase1_handoff.py"
)
REQUIRED_ACTIONS = [
    "verify_handoff_hashes",
    "preserve_normalized_inputs",
    "complete_review_layer",
    "resolve_canonical_identities",
    "generate_analysis_outputs",
    "confirm_frozen_models_unchanged",
    "validate_and_merge",
]


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def jsonl_bytes(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def occurrence_record(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "observation_id": "obs-1",
        "battle_id": "battle-1",
        "battle_context": "field",
        "side": "attacker",
        "row_type": "troop",
        "analysis_status": "included_primary",
        "display_name_normalized": "test_troop",
        "needs_review": False,
        "source_image_sha256": "b" * 64,
        "deployed": 10,
        "survivors": 8,
        "kills": 5,
        "deaths": 1,
        "wounded": 1,
        "routed": 0,
    }
    value.update(overrides)
    return value


def consolidated_record(**overrides: object) -> dict[str, object]:
    source = occurrence_record()
    value: dict[str, object] = {
        "battle_id": source["battle_id"],
        "battle_context": source["battle_context"],
        "display_name_normalized": source["display_name_normalized"],
        "needs_review": False,
        **{field: source[field] for field in ("deployed", "survivors", "kills", "deaths", "wounded", "routed")},
    }
    value.update(overrides)
    return value


class Phase1HandoffValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        self.branch = "agent/test-phase1"
        self.batch_relative = "data/combat_observations/2026-08-02-test"
        self.batch = self.repo / self.batch_relative
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test Agent")
        self.git("config", "user.email", "test@example.com")
        (self.repo / "AGENTS.md").write_text("# Test repository\n", encoding="utf-8")
        self.git("add", "AGENTS.md")
        self.git("commit", "-m", "initial")
        self.git("switch", "-c", self.branch)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def git(self, *arguments: str) -> str:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=self.repo,
            text=True,
            capture_output=True,
            check=True,
        )
        return completed.stdout.strip()

    def make_archive(self, files: dict[str, bytes], *, mtime: int = 0) -> bytes:
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:xz", format=tarfile.PAX_FORMAT) as archive:
            for relative, contents in sorted(files.items()):
                info = tarfile.TarInfo(f"normalized-test/{relative}")
                info.size = len(contents)
                info.mtime = mtime
                info.mode = 0o644
                archive.addfile(info, io.BytesIO(contents))
        return buffer.getvalue()

    def write_fixture(
        self,
        mutate_task: Callable[[dict[str, object]], None] | None = None,
        *,
        extra_archive_files: dict[str, bytes] | None = None,
        declared_observations: int = 1,
        base64_newline: bool = False,
        documented_archive_hash: str | None = None,
        generic_source_identity: bool = False,
        declared_review_queue: int = 0,
    ) -> tuple[str, dict[str, object]]:
        source_hash = "a" * 64
        summary = {
            ("source_sha256" if generic_source_identity else "source_zip_sha256"): source_hash,
            "game_track": "realm_of_thrones",
            "game_version": "1.4.x",
            "screenshots": 1,
            "battles": 1,
            "observations": declared_observations,
            "primary_troop_occurrences": 1,
            "review_queue": declared_review_queue,
        }
        report = {
            "status": "passed",
            "validation_errors": [],
            ("source_sha256" if generic_source_identity else "source_zip_sha256"): source_hash,
            ("source_size_bytes" if generic_source_identity else "source_zip_size_bytes"): 123,
            "image_count": 1,
            "battle_count": 1,
            "observation_count": declared_observations,
            "primary_troop_occurrences": 1,
            "review_queue_count": declared_review_queue,
        }
        files = {
            "README.md": b"# Normalized test batch\n",
            "screenshots_manifest.csv": b"image_file,image_sha256\nbattle.png," + b"b" * 64 + b"\n",
            "battles.jsonl": jsonl_bytes({
                "battle_id": "battle-1", "battle_context": "field", "player_side": "attacker",
                "game_track": "realm_of_thrones", "game_version": "1.4.x",
            }),
            "troop_occurrences.jsonl": jsonl_bytes(occurrence_record()),
            "primary_troop_occurrences.jsonl": jsonl_bytes(occurrence_record()),
            "troop_battle_consolidated.jsonl": jsonl_bytes(consolidated_record()),
            "review_queue.csv": b"observation_id,reason\n",
            "normalization_summary.json": json_bytes(summary),
            "validation_report.json": json_bytes(report),
        }
        files.update(extra_archive_files or {})
        manifest = io.StringIO()
        writer = csv.DictWriter(manifest, fieldnames=["file", "sha256", "size_bytes"], lineterminator="\n")
        writer.writeheader()
        for relative, contents in sorted(files.items()):
            writer.writerow({"file": relative, "sha256": sha256(contents), "size_bytes": len(contents)})
        files["artifact_hashes.csv"] = manifest.getvalue().encode("utf-8")
        archive = self.make_archive(files)

        for relative in (
            "README.md",
            "screenshots_manifest.csv",
            "normalization_summary.json",
            "review_queue.csv",
            "validation_report.json",
            "artifact_hashes.csv",
        ):
            path = self.batch / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(files[relative])
        (self.batch / "source").mkdir(parents=True)
        (self.batch / "source/README.md").write_text(
            f"source_zip_sha256: {source_hash}\n", encoding="utf-8"
        )
        (self.batch / "bundle").mkdir(parents=True)
        (self.batch / "bundle/README.md").write_text(
            f"archive_sha256: {documented_archive_hash or sha256(archive)}\n",
            encoding="utf-8",
        )
        encoded_archive = base64.b64encode(archive) + (b"\n" if base64_newline else b"")
        (self.batch / "bundle/normalized-test.tar.xz.base64.part-00").write_bytes(
            encoded_archive
        )
        (self.batch / "handoff").mkdir(parents=True)
        (self.batch / "handoff/ANALYSIS_PROMPT.md").write_text(
            "# Phase 2 handoff\n", encoding="utf-8"
        )

        self.git("add", self.batch_relative)
        self.git("commit", "-m", "normalize: create deterministic handoff")
        normalization_commit = self.git("rev-parse", "HEAD")

        task: dict[str, object] = {
            "protocol": "bannerlord-analysis-task",
            "version": 1,
            "task_id": "2026-08-02-test",
            "status": "pending",
            "branch": self.branch,
            "handoff_path": f"{self.batch_relative}/handoff/ANALYSIS_PROMPT.md",
            "normalization_commit": normalization_commit,
            "source_sha256": source_hash,
            "normalized_archive_sha256": sha256(archive),
            "required_actions": list(REQUIRED_ACTIONS),
            "completion": {"action": "merge", "merge_method": "squash"},
            "blockers": [],
        }
        if mutate_task:
            mutate_task(task)
        (self.batch / "handoff/ANALYSIS_TASK_V1.json").write_bytes(json_bytes(task))
        self.git("add", f"{self.batch_relative}/handoff/ANALYSIS_TASK_V1.json")
        self.git("commit", "-m", "normalize: publish pending task mirror")
        return normalization_commit, task

    def validate(self, normalization_commit: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--repo-root",
                str(self.repo),
                "--batch-dir",
                str(self.batch),
                "--branch",
                self.branch,
                "--normalization-commit",
                normalization_commit,
            ],
            cwd=self.repo,
            text=True,
            capture_output=True,
        )

    def test_accepts_complete_pending_phase1_handoff(self) -> None:
        normalization_commit, task = self.write_fixture()

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["task_id"], task["task_id"])
        self.assertEqual(result["manifest_entries"], 9)

    def test_accepts_established_analysis_action_alias_and_base64_whitespace(self) -> None:
        def use_established_action(task: dict[str, object]) -> None:
            actions = list(task["required_actions"])
            actions.remove("generate_analysis_outputs")
            actions.append("generate_reliable_and_complete_rankings")
            task["required_actions"] = actions

        normalization_commit, _ = self.write_fixture(
            use_established_action,
            base64_newline=True,
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_accepts_generic_source_identity_for_screenshot_directory(self) -> None:
        normalization_commit, _ = self.write_fixture(generic_source_identity=True)

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_rejects_missing_core_required_action(self) -> None:
        def omit_action(task: dict[str, object]) -> None:
            task["required_actions"] = REQUIRED_ACTIONS[:-1]

        normalization_commit, _ = self.write_fixture(omit_action)

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("omits required actions", completed.stderr)

    def test_rejects_archive_hash_mismatch(self) -> None:
        def corrupt_hash(task: dict[str, object]) -> None:
            task["normalized_archive_sha256"] = "0" * 64

        normalization_commit, _ = self.write_fixture(corrupt_hash)

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("normalized archive hash is incorrect", completed.stderr)

    def test_rejects_documented_archive_hash_mismatch(self) -> None:
        normalization_commit, _ = self.write_fixture(documented_archive_hash="0" * 64)

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("expected archive hash is incorrect", completed.stderr)

    def test_rejects_source_identity_mismatch(self) -> None:
        def corrupt_source(task: dict[str, object]) -> None:
            task["source_sha256"] = "0" * 64

        normalization_commit, _ = self.write_fixture(corrupt_source)

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("source_sha256 differs", completed.stderr)

    def test_rejects_phase2_output_in_phase1_batch(self) -> None:
        normalization_commit, _ = self.write_fixture()
        (self.batch / "analysis").mkdir()
        (self.batch / "analysis/README.md").write_text("too early\n", encoding="utf-8")
        self.git("add", f"{self.batch_relative}/analysis/README.md")
        self.git("commit", "-m", "analysis: violate phase boundary")

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("non-Phase-1 files are forbidden", completed.stderr)

    def test_rejects_phase2_output_inside_normalized_archive(self) -> None:
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={"analysis/ranking_complete.csv": b"troop_id,score\nfoo,1\n"}
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("Phase 2 artifacts are forbidden", completed.stderr)

    def test_rejects_declared_counts_that_do_not_match_records(self) -> None:
        normalization_commit, _ = self.write_fixture(declared_observations=2)

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("declared count differs from archive records", completed.stderr)

    def test_rejects_player_enemy_boundary_violation(self) -> None:
        invalid_primary = jsonl_bytes(occurrence_record(side="defender"))
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={
                "troop_occurrences.jsonl": invalid_primary,
                "primary_troop_occurrences.jsonl": invalid_primary,
            }
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("player/enemy side boundary violation", completed.stderr)

    def test_rejects_primary_value_tampering(self) -> None:
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={
                "primary_troop_occurrences.jsonl": jsonl_bytes(occurrence_record(kills=999))
            }
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("primary row differs from source occurrence", completed.stderr)

    def test_rejects_consolidated_context_tampering(self) -> None:
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={
                "troop_battle_consolidated.jsonl": jsonl_bytes(
                    consolidated_record(battle_context="siege_attack")
                )
            }
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("consolidated context mismatch", completed.stderr)

    def test_rejects_consolidated_value_tampering(self) -> None:
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={
                "troop_battle_consolidated.jsonl": jsonl_bytes(
                    consolidated_record(kills=999)
                )
            }
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("consolidated kills differs from primary rows", completed.stderr)

    def test_rejects_unknown_battle_context(self) -> None:
        invalid_battle = jsonl_bytes({
            "battle_id": "battle-1", "battle_context": "naval", "player_side": "attacker",
            "game_track": "realm_of_thrones", "game_version": "1.4.x",
        })
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={"battles.jsonl": invalid_battle}
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("unknown battle context", completed.stderr)

    def test_rejects_mixed_game_track(self) -> None:
        invalid_battle = jsonl_bytes({
            "battle_id": "battle-1", "battle_context": "field", "player_side": "attacker",
            "game_track": "nightmare_sails", "game_version": "1.4.x",
        })
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={"battles.jsonl": invalid_battle}
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("mixed or missing game track", completed.stderr)

    def test_rejects_occurrence_track_contradiction(self) -> None:
        contradictory = jsonl_bytes(occurrence_record(game_track="nightmare_sails"))
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={
                "troop_occurrences.jsonl": contradictory,
                "primary_troop_occurrences.jsonl": contradictory,
            }
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("occurrence game track mismatch", completed.stderr)

    def test_rejects_unqueued_uncertain_occurrence(self) -> None:
        uncertain = occurrence_record(
            observation_id="obs-2",
            analysis_status="unresolved",
            needs_review=True,
            uncertain_fields=["kills"],
        )
        all_occurrences = jsonl_bytes(occurrence_record()) + jsonl_bytes(uncertain)
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={"troop_occurrences.jsonl": all_occurrences},
            declared_observations=2,
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("review-needed occurrences are absent", completed.stderr)

    def test_rejects_review_item_without_review_reason(self) -> None:
        non_primary = occurrence_record(
            observation_id="obs-2",
            analysis_status="supporting_only",
        )
        all_occurrences = jsonl_bytes(occurrence_record()) + jsonl_bytes(non_primary)
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={
                "troop_occurrences.jsonl": all_occurrences,
                "review_queue.csv": b"observation_id,reason\nobs-2,none\n",
            },
            declared_observations=2,
            declared_review_queue=1,
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("review item has no review reason", completed.stderr)

    def test_accepts_routed_as_separate_from_deployed_arithmetic(self) -> None:
        occurrence = occurrence_record(routed=2)
        normalization_commit, _ = self.write_fixture(
            extra_archive_files={
                "troop_occurrences.jsonl": jsonl_bytes(occurrence),
                "primary_troop_occurrences.jsonl": jsonl_bytes(occurrence),
                "troop_battle_consolidated.jsonl": jsonl_bytes(consolidated_record(routed=2)),
            }
        )

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_rejects_root_phase2_artifacts(self) -> None:
        normalization_commit, _ = self.write_fixture()
        (self.batch / "reports").mkdir()
        (self.batch / "reports/empirical_residual_rankings.csv").write_text(
            "troop,score\nfoo,1\n", encoding="utf-8"
        )
        self.git("add", f"{self.batch_relative}/reports")
        self.git("commit", "-m", "analysis: hide output in phase1 root")

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("non-Phase-1 files are forbidden", completed.stderr)

    def test_rejects_archive_replacement_after_normalization_commit(self) -> None:
        normalization_commit, _ = self.write_fixture()
        part = self.batch / "bundle/normalized-test.tar.xz.base64.part-00"
        original_archive = base64.b64decode(part.read_bytes(), validate=True)
        files: dict[str, bytes] = {}
        with tarfile.open(fileobj=io.BytesIO(original_archive), mode="r:xz") as archive:
            for member in archive:
                if member.isfile():
                    extracted = archive.extractfile(member)
                    self.assertIsNotNone(extracted)
                    files["/".join(member.name.split("/")[1:])] = extracted.read()
        replacement = self.make_archive(files, mtime=1)
        self.assertNotEqual(sha256(original_archive), sha256(replacement))
        part.write_bytes(base64.b64encode(replacement))
        (self.batch / "bundle/README.md").write_text(
            f"archive_sha256: {sha256(replacement)}\n", encoding="utf-8"
        )
        task_path = self.batch / "handoff/ANALYSIS_TASK_V1.json"
        task = json.loads(task_path.read_text(encoding="utf-8"))
        task["normalized_archive_sha256"] = sha256(replacement)
        task_path.write_bytes(json_bytes(task))
        self.git("add", self.batch_relative)
        self.git("commit", "-m", "normalize: replace archive after handoff")

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("immutable Phase 1 files changed", completed.stderr)

    def test_rejects_frozen_model_change_anywhere_on_batch_branch(self) -> None:
        model = self.repo / "analysis/model_versions/forbidden.json"
        model.parent.mkdir(parents=True)
        model.write_text("{}\n", encoding="utf-8")
        self.git("add", "analysis/model_versions/forbidden.json")
        self.git("commit", "-m", "model: forbidden batch-branch change")
        normalization_commit, _ = self.write_fixture()

        completed = self.validate(normalization_commit)

        self.assertEqual(completed.returncode, 2)
        self.assertIn("frozen model files changed", completed.stderr)


if __name__ == "__main__":
    unittest.main()
