from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.combat_observations.domain import write_jsonl


REPO = Path(__file__).resolve().parents[1]
NORMALIZER_SKILL = REPO / ".agents/skills/normalize-bannerlord-combat-batch"
ANALYZER_SKILL = REPO / ".agents/skills/analyze-bannerlord-combat-zip"
INVOKE = NORMALIZER_SKILL / "scripts/invoke_pipeline.py"
INSTALL = NORMALIZER_SKILL / "scripts/install_adapters.py"
ANALYZER_INSTALL = ANALYZER_SKILL / "scripts/install_adapters.py"
PNG_FIXTURE = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + (1).to_bytes(4, "big") + (1).to_bytes(4, "big") + b"\x00" * 16


class PortableSkillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_script(self, script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *arguments],
            cwd=REPO,
            text=True,
            capture_output=True,
        )

    def test_trigger_and_non_trigger_contract(self) -> None:
        cases = json.loads((REPO / "tests/fixtures/skill_trigger_cases.json").read_text(encoding="utf-8"))

        def normalizer_contract(prompt: str) -> bool:
            text = prompt.casefold()
            return "bannerlord" in text and (
                any(token in text for token in ("raw", "screenshot", "unpublished"))
                and any(token in text for token in ("normalize", "process", "publish", "draft pr", "phase 1"))
            )

        def analyzer_contract(prompt: str) -> bool:
            text = prompt.casefold()
            raw_request = any(token in text for token in ("raw", "screenshot", "unpublished"))
            phase2_request = "fecha as análises" in text or any(
                token in text for token in ("normalized", "handoff", "analysis-task", "canonical empirical rankings")
            )
            return not raw_request and phase2_request and (
                "bannerlord" in text or "fecha as análises" in text
            )

        self.assertTrue(all(normalizer_contract(prompt) for prompt in cases["normalizer"]["trigger"]))
        self.assertTrue(all(not normalizer_contract(prompt) for prompt in cases["normalizer"]["non_trigger"]))
        self.assertTrue(all(analyzer_contract(prompt) for prompt in cases["analyzer"]["trigger"]))
        self.assertTrue(all(not analyzer_contract(prompt) for prompt in cases["analyzer"]["non_trigger"]))
        for prompt in cases["mixed"]:
            self.assertTrue(normalizer_contract(prompt))
            self.assertFalse(analyzer_contract(prompt))
        for prompt in cases["neither"]:
            self.assertFalse(normalizer_contract(prompt))
            self.assertFalse(analyzer_contract(prompt))

        normalizer_text = (NORMALIZER_SKILL / "SKILL.md").read_text(encoding="utf-8")
        analyzer_text = (ANALYZER_SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Never continue into Phase 2 in the same agent run", normalizer_text)
        self.assertIn("Reject raw screenshots and raw screenshot ZIPs", analyzer_text)
        self.assertLess(len(normalizer_text.splitlines()), 500)
        self.assertLess(len(analyzer_text.splitlines()), 500)

    def test_adapter_dry_run_and_temporary_copy(self) -> None:
        project = self.root / "project"
        project.mkdir()
        preview = self.run_script(
            INSTALL,
            "--target", "all",
            "--scope", "project",
            "--mode", "symlink",
            "--project-root", str(project),
            "--dry-run",
        )
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertIn("dry-run:", preview.stdout)
        self.assertFalse((project / ".claude/skills/normalize-bannerlord-combat-batch").exists())

        user_preview = self.run_script(
            INSTALL,
            "--target", "all",
            "--scope", "user",
            "--mode", "copy",
            "--user-root", str(self.root / "user"),
            "--dry-run",
        )
        self.assertEqual(user_preview.returncode, 0, user_preview.stderr)
        self.assertIn(".claude/skills", user_preview.stdout)
        self.assertIn(".cursor/skills", user_preview.stdout)
        self.assertFalse(
            (self.root / "user/.claude/skills/normalize-bannerlord-combat-batch").exists()
        )

        applied = self.run_script(
            INSTALL,
            "--target", "claude",
            "--scope", "project",
            "--mode", "copy",
            "--project-root", str(project),
        )
        self.assertEqual(applied.returncode, 0, applied.stderr)
        installed = project / ".claude/skills/normalize-bannerlord-combat-batch"
        self.assertTrue((installed / "SKILL.md").is_file())
        again = self.run_script(
            INSTALL,
            "--target", "claude",
            "--scope", "project",
            "--mode", "copy",
            "--project-root", str(project),
        )
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn("already current", again.stdout)

        analyzer_preview = self.run_script(
            ANALYZER_INSTALL,
            "--target", "claude",
            "--scope", "project",
            "--mode", "copy",
            "--project-root", str(project),
            "--dry-run",
        )
        self.assertEqual(analyzer_preview.returncode, 0, analyzer_preview.stderr)
        self.assertIn("analyze-bannerlord-combat-zip", analyzer_preview.stdout)

    def test_screenshot_directory_preflight_and_resume(self) -> None:
        images = self.root / "images"
        images.mkdir()
        (images / "battle.png").write_bytes(PNG_FIXTURE)
        output = self.root / "output"
        arguments = (
            "--input", str(images),
            "--output", str(output),
            "--mode", "host-vision",
            "--repo", str(REPO),
        )
        first = self.run_script(INVOKE, *arguments)
        self.assertEqual(first.returncode, 0, first.stderr)
        first_state = (output / "batch_state.json").read_bytes()
        state = json.loads(first_state)
        self.assertEqual(state["pending_images"], 1)
        self.assertEqual(state["phase_statuses"]["preflight"], "complete")
        self.assertEqual(state["phase_statuses"]["extraction"], "pending")
        self.assertTrue((output / "extraction/extraction_queue.jsonl").is_file())

        second = self.run_script(INVOKE, *arguments)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first_state, (output / "batch_state.json").read_bytes())
        (images / "different.png").write_bytes(PNG_FIXTURE + b"different")
        incompatible = self.run_script(INVOKE, *arguments)
        self.assertEqual(incompatible.returncode, 2)
        self.assertIn("refusing incompatible resume", incompatible.stderr)

    def test_offline_mode_and_nested_output_are_rejected_for_screenshots(self) -> None:
        images = self.root / "images-offline"
        images.mkdir()
        (images / "battle.png").write_bytes(PNG_FIXTURE)
        offline = self.run_script(
            INVOKE,
            "--input", str(images),
            "--output", str(self.root / "offline-output"),
            "--mode", "offline-existing",
            "--repo", str(REPO),
        )
        self.assertEqual(offline.returncode, 2)
        self.assertIn("requires a normalized input", offline.stderr)

        nested = self.run_script(
            INVOKE,
            "--input", str(images),
            "--output", str(images / "generated"),
            "--mode", "host-vision",
            "--repo", str(REPO),
        )
        self.assertEqual(nested.returncode, 2)
        self.assertIn("must not be the input directory", nested.stderr)

    def test_screenshot_zip_preflight_through_skill(self) -> None:
        screenshot_zip = self.root / "screenshots.zip"
        with zipfile.ZipFile(screenshot_zip, "w") as archive:
            archive.writestr("battle.png", PNG_FIXTURE)
            archive.writestr("notes.txt", b"retained but never executed")
        output = self.root / "zip-preflight"
        result = self.run_script(
            INVOKE,
            "--input", str(screenshot_zip),
            "--output", str(output),
            "--mode", "host-vision",
            "--repo", str(REPO),
            "--config", str(REPO / "config/combat_observations.default.json"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads((output / "batch_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["input_name"], "screenshots.zip")
        self.assertEqual(state["counts"]["images_queued"], 1)
        self.assertIn("resume_command", state)
        manifest = next((output / "manifest").glob("*.csv"))
        self.assertIn("source_timestamp", manifest.read_text(encoding="utf-8"))

    def test_unreadable_normalized_zip_remains_partial(self) -> None:
        normalized_zip = self.root / "unreadable-normalized.zip"
        record = {
            "schema_version": "1.0.0-first-pass",
            "observation_id": "obs-unreadable",
            "battle_id": "battle-1",
            "battle_context": "field",
            "classification_source": "raw_extraction",
            "side": "attacker",
            "parent_group": "party",
            "row_type": "troop",
            "display_name_raw": "Imperial Naute",
            "canonical_troop_id": None,
            "relationship_to_player": "player_party",
            "source": {"image_file": "battle.png", "image_sha256": "1" * 64},
            "survivors": 8,
            "kills": None,
            "upgrade_ready": 0,
            "deaths": 1,
            "wounded": 1,
            "routed": 0,
            "analysis_status": "raw",
            "game": {"version": "1.4.x", "track": "vanilla_war_sails_1.4.x", "active_modules": []},
            "provenance": {"extractor_model": "fixture"},
        }
        with zipfile.ZipFile(normalized_zip, "w") as archive:
            archive.writestr(
                "troop_occurrences.jsonl",
                json.dumps(record, sort_keys=True) + "\n",
            )
        output = self.root / "unreadable-output"
        result = self.run_script(
            INVOKE,
            "--input", str(normalized_zip),
            "--output", str(output),
            "--mode", "offline-existing",
            "--repo", str(REPO),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        state = json.loads((output / "batch_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["status"], "partial")
        self.assertEqual(state["phase_statuses"]["phase1_packaging"], "pending")
        self.assertEqual(state["phase_statuses"]["canonical"], "not_permitted_in_phase1")
        self.assertIn("validate_phase1_handoff.py", state["next_action"])
        self.assertFalse((output / "canonical").exists())

    def test_existing_normalized_stops_before_phase2(self) -> None:
        normalized = self.root / "normalized"
        normalized.mkdir()
        write_jsonl(
            normalized / "troop_occurrences.jsonl",
            [
                {
                    "schema_version": "1.0.0-first-pass",
                    "observation_id": "obs-1",
                    "battle_id": "battle-1",
                    "battle_context": "field",
                    "classification_source": "raw_extraction",
                    "side": "attacker",
                    "parent_group": "party",
                    "row_type": "troop",
                    "display_name_raw": "Imperial Naute",
                    "canonical_troop_id": None,
                    "relationship_to_player": "player_party",
                    "source": {"image_file": "battle.png", "image_sha256": "1" * 64},
                    "survivors": 8,
                    "kills": 5,
                    "upgrade_ready": 0,
                    "deaths": 1,
                    "wounded": 1,
                    "routed": 0,
                    "analysis_status": "raw",
                    "game": {"version": "1.4.x", "track": "vanilla_war_sails_1.4.x", "active_modules": []},
                    "provenance": {"extractor_model": "fixture"}
                }
            ],
        )
        output = self.root / "phase1-output"
        completed = self.run_script(
            INVOKE,
            "--input", str(normalized),
            "--output", str(output),
            "--mode", "offline-existing",
            "--repo", str(REPO),
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        state = json.loads((output / "batch_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["phase_statuses"]["raw_verification"], "complete")
        self.assertEqual(state["phase_statuses"]["phase1_packaging"], "pending")
        self.assertEqual(state["phase_statuses"]["canonical"], "not_permitted_in_phase1")
        self.assertIn("validate_phase1_handoff.py", state["next_action"])
        self.assertFalse((output / "canonical").exists())

        normalized_zip = self.root / "normalized.zip"
        with zipfile.ZipFile(normalized_zip, "w") as archive:
            archive.write(normalized / "troop_occurrences.jsonl", "payload/troop_occurrences.jsonl")
        zip_output = self.root / "zip-output"
        zipped = self.run_script(
            INVOKE,
            "--input", str(normalized_zip),
            "--output", str(zip_output),
            "--mode", "offline-existing",
            "--repo", str(REPO),
        )
        self.assertEqual(zipped.returncode, 0, zipped.stderr)
        self.assertTrue((zip_output / "reports/normalized_zip_preflight.json").is_file())
        zipped_state = json.loads((zip_output / "batch_state.json").read_text(encoding="utf-8"))
        self.assertEqual(zipped_state["phase_statuses"]["canonical"], "not_permitted_in_phase1")
        self.assertFalse((zip_output / "canonical").exists())


if __name__ == "__main__":
    unittest.main()
