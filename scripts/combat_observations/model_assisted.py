from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Protocol

from .bundle import BundleError, atomic_write_json
from .domain import read_csv, stable_id, write_jsonl


MODES = ("offline-existing", "host-vision", "api-batch")


class RetryableModelError(RuntimeError):
    pass


class NonRetryableModelError(RuntimeError):
    pass


class VisionAdapter(Protocol):
    def extract(self, image_path: Path, config: "ExtractionConfig") -> dict[str, object]:
        ...


@dataclass(frozen=True)
class ExtractionConfig:
    mode: str
    extractor_model: str | None
    reviewer_model: str | None
    prompt_version: str
    schema_version: str
    image_detail: str
    max_retries: int = 2

    @classmethod
    def from_environment(cls, mode: str) -> "ExtractionConfig":
        if mode not in MODES:
            raise BundleError(f"unsupported extraction mode: {mode}")
        try:
            max_retries = int(os.environ.get("VISION_MAX_RETRIES", "2"))
        except ValueError as error:
            raise BundleError("VISION_MAX_RETRIES must be a non-negative integer") from error
        if max_retries < 0:
            raise BundleError("VISION_MAX_RETRIES must be a non-negative integer")
        return cls(
            mode=mode,
            extractor_model=os.environ.get("VISION_EXTRACTOR_MODEL"),
            reviewer_model=os.environ.get("VISION_REVIEWER_MODEL"),
            prompt_version=os.environ.get("COMBAT_PROMPT_VERSION", "combat-v2"),
            schema_version="2.0.0",
            image_detail=os.environ.get("IMAGE_DETAIL", "high"),
            max_retries=max_retries,
        )


def run_with_retries(
    operation: Callable[[], dict[str, object]],
    *,
    max_retries: int,
) -> tuple[dict[str, object], int]:
    retries = 0
    while True:
        try:
            return operation(), retries
        except RetryableModelError:
            if retries >= max_retries:
                raise
            retries += 1
        except NonRetryableModelError:
            raise


def validate_model_response(response: object) -> list[str]:
    if not isinstance(response, dict):
        return ["response must be an object"]
    errors = []
    if not isinstance(response.get("screen_type"), str):
        errors.append("screen_type must be a string")
    rows = response.get("rows")
    if not isinstance(rows, list):
        errors.append("rows must be an array")
    else:
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"rows[{index}] must be an object")
                continue
            if "display_name_raw" not in row:
                errors.append(f"rows[{index}].display_name_raw is required")
            for field in ("survivors", "kills", "upgrade_ready", "deaths", "wounded", "routed"):
                value = row.get(field)
                if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
                    errors.append(f"rows[{index}].{field} must be a non-negative integer or null")
    return errors


def prepare_extraction_queue(
    manifest_csv: Path,
    output_dir: Path,
    *,
    mode: str,
    authorize_paid_api: bool = False,
    estimated_cost_per_image: float | None = None,
) -> dict[str, object]:
    config = ExtractionConfig.from_environment(mode)
    inventory = [
        row
        for row in read_csv(manifest_csv)
        if str(row.get("supported_image")).casefold() == "true"
    ]
    rows = [
        row
        for row in inventory
        if not row.get("exact_duplicate_of") and not row.get("historical_duplicate_of")
    ]
    if estimated_cost_per_image is not None and estimated_cost_per_image < 0:
        raise BundleError("estimated cost per image must be non-negative")
    if mode == "offline-existing":
        raise BundleError(
            "offline-existing consumes normalized records, not an image manifest"
        )
    if mode == "api-batch":
        if not config.extractor_model or not config.reviewer_model:
            raise BundleError(
                "api-batch requires VISION_EXTRACTOR_MODEL and VISION_REVIEWER_MODEL; "
                "model IDs are configuration, not schema values"
            )
        if not authorize_paid_api:
            cost = (
                f" estimated upper-bound cost={len(rows) * estimated_cost_per_image:.4f}"
                if estimated_cost_per_image is not None
                else ""
            )
            raise BundleError(
                "api-batch would upload screenshots and may incur paid usage; "
                f"explicit --authorize-paid-api is required.{cost}"
            )
    queue = [
        {
            "queue_id": stable_id("extract", row["source_sha256"], config.prompt_version, config.schema_version),
            "source_filename": row["source_filename"],
            "source_sha256": row["source_sha256"],
            "mode": mode,
            "status": "pending",
            "extractor_model": config.extractor_model if mode == "api-batch" else ("unknown" if mode == "host-vision" else None),
            "reviewer_model": config.reviewer_model if mode == "api-batch" else ("unknown" if mode == "host-vision" else None),
            "prompt_version": config.prompt_version,
            "schema_version": config.schema_version,
            "image_detail": config.image_detail,
            "uncertainty_policy": "unreadable values remain null and route to review",
        }
        for row in sorted(rows, key=lambda item: item["source_filename"])
    ]
    queue_path = output_dir / "extraction_queue.jsonl"
    write_jsonl(queue_path, queue)
    report = {
        "schema_version": "1.0.0",
        "mode": mode,
        "queue_size": len(queue),
        "skipped_exact_duplicates": sum(bool(row.get("exact_duplicate_of")) for row in inventory),
        "skipped_already_normalized": sum(
            bool(row.get("historical_duplicate_of")) and not bool(row.get("exact_duplicate_of"))
            for row in inventory
        ),
        "visual_deduplication_review": sum(
            row.get("deduplication_status") == "needs_visual_review" for row in inventory
        ),
        "status": (
            "nothing_to_extract"
            if not queue
            else "ready_for_host_vision" if mode == "host-vision" else "ready"
        ),
        "paid_api_authorized": authorize_paid_api,
        "files_that_would_leave_machine": [row["source_filename"] for row in queue] if mode == "api-batch" else [],
        "queue_path": "extraction_queue.jsonl",
        "note": (
            "This command prepares deterministic work only. Live model execution is intentionally "
            "not performed without a configured provider adapter."
        ),
    }
    atomic_write_json(output_dir / "extraction_plan.json", report)
    return report
