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


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class Phase1HandoffValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repo = Path(self.temporary.name)
        self.branch = "agent/test-phase1"
        self.batch_relative = "data/combat_observations/2026-08-02-test"
        self.batch = self.repo / self.batch_relative
        self.git("init", "-b", self.branch)
        self.git("config", "user.name", "Test Agent")
        self.git("config", "user.email", "test@example.com")
        (self.repo / "AGENTS.md").write_text("# Test repository\n", encoding="utf-8")
        self.git("add", "AGENTS.md")
        self.git("commit", "-m", "initial")

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

    def make_archive(self, files: dict[str, bytes]) -> bytes:
        buffer = io.BytesIO()
        with tarfile.open(fileobj=buffer, mode="w:xz", format=tarfile.PAX_FORMAT) as archive:
            for relative, contents in sorted(files.items()):
                info = tarfile.TarInfo(f"normalized-test/{relative}")
                info.size = len(contents)
                info.mtime = 0
                info.mode = 0o644
                archive.addfile(info, io.BytesIO(contents))
        return buffer.getvalue()

    def write_fixture(
        self,
        mutate_task: Callable[[dict[str, object]], None] | None = None,
    ) -> tuple[str, dict[str, object]]:
        source_hash = "a" * 64
        summary = {
            "source_zip_sha256": source_hash,
            "screenshots": 1,
            "battles": 1,
            "observations": 1,
            "primary_troop_occurrences": 1,
            "review_queue": 0,
        }
        report = {
            "status": "passed",
            "validation_errors": [],
            "source_zip_sha256": source_hash,
            "source_zip_size_bytes": 123,
            "image_count": 1,
            "battle_count": 1,
            "observation_count": 1,
            "primary_troop_occurrences": 1,
            "review_queue_count": 0,
        }
        files = {
            "README.md": b"# Normalized test batch\n",
            "screenshots_manifest.csv": b"image_file,image_sha256\nbattle.png," + b"b" * 64 + b"\n",
            "battles.jsonl": b'{"battle_id":"battle-1"}\n',
            "troop_occurrences.jsonl": b'{"observation_id":"obs-1"}\n',
            "primary_troop_occurrences.jsonl": b'{"observation_id":"obs-1"}\n',
            "troop_battle_consolidated.jsonl": b'{"battle_id":"battle-1"}\n',
            "review_queue.csv": b"observation_id,reason\n",
            "normalization_summary.json": json_bytes(summary),
            "validation_report.json": json_bytes(report),
        }
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
            f"archive_sha256: {sha256(archive)}\n", encoding="utf-8"
        )
        (self.batch / "bundle/normalized-test.tar.xz.base64.part-00").write_bytes(
            base64.b64encode(archive)
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
        self.assertIn("Phase 2 directory is forbidden", completed.stderr)


if __name__ == "__main__":
    unittest.main()
