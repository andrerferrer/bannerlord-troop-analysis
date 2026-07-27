from __future__ import annotations

import csv
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.combat_observations.bundle import BundleError
from scripts.combat_observations.model_assisted import (
    NonRetryableModelError,
    RetryableModelError,
    prepare_extraction_queue,
    run_with_retries,
    validate_model_response,
)


class ModelAssistedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.manifest = self.root / "manifest.csv"
        with self.manifest.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["source_filename", "source_sha256", "supported_image"])
            writer.writeheader()
            writer.writerow({"source_filename": "one.png", "source_sha256": "a" * 64, "supported_image": "True"})

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_host_vision_queue_uses_unknown_provenance(self) -> None:
        report = prepare_extraction_queue(self.manifest, self.root / "output", mode="host-vision")
        self.assertEqual(report["status"], "ready_for_host_vision")
        queue = (self.root / "output/extraction_queue.jsonl").read_text(encoding="utf-8")
        self.assertIn('"extractor_model":"unknown"', queue)
        self.assertEqual(report["files_that_would_leave_machine"], [])

    def test_api_batch_requires_models_and_authorization(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(BundleError, "requires VISION_EXTRACTOR_MODEL"):
                prepare_extraction_queue(self.manifest, self.root / "missing-models", mode="api-batch")
        with patch.dict(
            os.environ,
            {"VISION_EXTRACTOR_MODEL": "configured-extractor", "VISION_REVIEWER_MODEL": "configured-reviewer"},
            clear=True,
        ):
            with self.assertRaisesRegex(BundleError, "explicit --authorize-paid-api"):
                prepare_extraction_queue(
                    self.manifest,
                    self.root / "not-authorized",
                    mode="api-batch",
                    estimated_cost_per_image=0.01,
                )

    def test_offline_manifest_and_negative_cost_are_rejected(self) -> None:
        with self.assertRaisesRegex(BundleError, "consumes normalized records"):
            prepare_extraction_queue(
                self.manifest,
                self.root / "offline",
                mode="offline-existing",
            )
        with self.assertRaisesRegex(BundleError, "cost per image"):
            prepare_extraction_queue(
                self.manifest,
                self.root / "negative-cost",
                mode="host-vision",
                estimated_cost_per_image=-1,
            )

    def test_retryable_and_non_retryable_failures(self) -> None:
        attempts = 0

        def transient():
            nonlocal attempts
            attempts += 1
            if attempts < 3:
                raise RetryableModelError("transient")
            return {"ok": True}

        result, retries = run_with_retries(transient, max_retries=2)
        self.assertEqual(result, {"ok": True})
        self.assertEqual(retries, 2)
        with self.assertRaises(NonRetryableModelError):
            run_with_retries(lambda: (_ for _ in ()).throw(NonRetryableModelError("bad")), max_retries=2)

    def test_malformed_and_semantically_invalid_model_response(self) -> None:
        self.assertTrue(validate_model_response("not an object"))
        errors = validate_model_response(
            {
                "screen_type": "result",
                "rows": [{"display_name_raw": "Troop", "kills": -1}],
            }
        )
        self.assertIn("rows[0].kills must be a non-negative integer or null", errors)
        self.assertFalse(
            validate_model_response(
                {
                    "screen_type": "result",
                    "rows": [
                        {
                            "display_name_raw": "Troop",
                            "survivors": 1,
                            "kills": 1,
                            "upgrade_ready": 0,
                            "deaths": 0,
                            "wounded": 0,
                            "routed": 0,
                        }
                    ],
                }
            )
        )


if __name__ == "__main__":
    unittest.main()
