from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import stat
import struct
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Iterable

from . import PIPELINE_VERSION
from .bundle import BundleError, atomic_write_json, directory_trees_equal, sha256_file
from .domain import stable_id, stable_json, write_csv


SUPPORTED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
CAPTURE_STAMP = re.compile(
    r"(?<!\d)(\d{2})[_-](\d{2})[_-](\d{4})[ _T-]+(\d{2})[_-](\d{2})[_-](\d{2})(?!\d)"
)


def capture_identity(filename: str) -> tuple[str, str]:
    """Return a stable capture timestamp and the recorder/process prefix."""
    name = Path(filename).name
    match = CAPTURE_STAMP.search(name)
    if match is None:
        return "", ""
    day, month, year, hour, minute, second = match.groups()
    try:
        captured_at = datetime(
            int(year), int(month), int(day), int(hour), int(minute), int(second)
        )
    except ValueError:
        return "", ""
    stamp = captured_at.isoformat(timespec="seconds")
    prefix = name[: match.start()].strip(" _-").casefold()
    return stamp, prefix


def _history_records(history_root: Path | None) -> list[dict[str, str]]:
    if history_root is None or not history_root.is_dir():
        return []
    records: list[dict[str, str]] = []
    manifests = sorted(history_root.rglob("screenshots_manifest.csv"))
    inventories = sorted(history_root.rglob("source_inventory.csv"))
    for path in [*manifests, *inventories]:
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                filename = str(row.get("image_file") or row.get("source_filename") or "")
                digest = str(row.get("image_sha256") or row.get("source_sha256") or "")
                if not filename or len(digest) != 64:
                    continue
                stamp, _ = capture_identity(filename)
                records.append(
                    {
                        "filename": filename,
                        "basename": Path(filename).name.casefold(),
                        "sha256": digest,
                        "capture_identity": stamp,
                        "reference": f"{path.relative_to(history_root).as_posix()}::{filename}",
                    }
                )
    return records


def _history_index_sha256(records: list[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    for record in sorted(records, key=lambda item: (item["reference"], item["sha256"])):
        digest.update(stable_json(record).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def _mark_visual_duplicate_candidates(rows: list[dict[str, object]]) -> None:
    previous_by_prefix: dict[str, tuple[datetime, str]] = {}
    chronological = []
    for row in rows:
        stamp = str(row["capture_identity"])
        prefix = str(row.pop("_capture_prefix"))
        if bool(row["supported_image"]) and stamp and prefix:
            chronological.append((datetime.fromisoformat(stamp), prefix, row))
    for captured_at, prefix, row in sorted(chronological, key=lambda item: item[0]):
        previous = previous_by_prefix.get(prefix)
        if previous is not None:
            previous_at, previous_filename = previous
            if (captured_at - previous_at).total_seconds() <= 60:
                row["visual_duplicate_candidate_of"] = previous_filename
        previous_by_prefix[prefix] = (captured_at, str(row["source_filename"]))


def _apply_history(rows: list[dict[str, object]], records: list[dict[str, str]]) -> None:
    by_hash: dict[str, list[str]] = {}
    by_capture_filename: dict[tuple[str, str], list[str]] = {}
    by_capture: dict[str, list[str]] = {}
    for record in records:
        by_hash.setdefault(record["sha256"], []).append(record["reference"])
        if record["capture_identity"]:
            key = (record["capture_identity"], record["basename"])
            by_capture_filename.setdefault(key, []).append(record["reference"])
            by_capture.setdefault(record["capture_identity"], []).append(record["reference"])

    for row in rows:
        if not bool(row["supported_image"]):
            row["deduplication_status"] = "unsupported"
            continue
        digest_matches = by_hash.get(str(row["source_sha256"]), [])
        stamp = str(row["capture_identity"])
        filename_matches = by_capture_filename.get(
            (stamp, Path(str(row["source_filename"])).name.casefold()), []
        ) if stamp else []
        candidate_matches = by_capture.get(stamp, []) if stamp else []
        if digest_matches:
            row["historical_duplicate_of"] = "|".join(sorted(set(digest_matches)))
            row["historical_match_type"] = "sha256"
        elif filename_matches:
            row["historical_duplicate_of"] = "|".join(sorted(set(filename_matches)))
            row["historical_match_type"] = "capture_identity_and_filename"
        elif candidate_matches:
            row["historical_candidate_of"] = "|".join(sorted(set(candidate_matches)))
            row["historical_match_type"] = "capture_identity_candidate"

        if row["exact_duplicate_of"]:
            row["deduplication_status"] = "skip_exact_duplicate"
        elif row["historical_duplicate_of"]:
            row["deduplication_status"] = "skip_already_normalized"
        elif row["historical_candidate_of"] or row["visual_duplicate_candidate_of"]:
            row["deduplication_status"] = "needs_visual_review"
        else:
            row["deduplication_status"] = "pending"


def _safe_zip_member(name: str) -> PurePosixPath:
    logical = PurePosixPath(name)
    if logical.is_absolute() or ".." in logical.parts or not logical.parts:
        raise BundleError(f"unsafe ZIP member path: {name}")
    if logical.parts[0].endswith(":"):
        raise BundleError(f"absolute Windows ZIP member path: {name}")
    return logical


def _is_zip_symlink(info: zipfile.ZipInfo) -> bool:
    mode = (info.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def inspect_zip(
    zip_path: Path,
    *,
    max_members: int = 10_000,
    max_uncompressed_bytes: int = 1_000_000_000,
    max_compression_ratio: float = 1_000.0,
) -> dict[str, object]:
    try:
        archive = zipfile.ZipFile(zip_path)
    except (OSError, zipfile.BadZipFile) as error:
        raise BundleError(f"corrupt or unreadable ZIP: {error}") from error
    with archive:
        infos = archive.infolist()
        if len(infos) > max_members:
            raise BundleError(f"ZIP member count exceeds limit: {len(infos)} > {max_members}")
        seen: set[str] = set()
        seen_casefold: set[str] = set()
        total_compressed = 0
        total_uncompressed = 0
        members = []
        for info in infos:
            logical = _safe_zip_member(info.filename)
            normalized = logical.as_posix()
            if normalized in seen or normalized.casefold() in seen_casefold:
                raise BundleError(f"duplicate ZIP member name: {normalized}")
            seen.add(normalized)
            seen_casefold.add(normalized.casefold())
            if _is_zip_symlink(info):
                raise BundleError(f"ZIP symlinks are not allowed: {normalized}")
            total_compressed += info.compress_size
            total_uncompressed += info.file_size
            if total_uncompressed > max_uncompressed_bytes:
                raise BundleError(
                    f"ZIP declared uncompressed size exceeds limit: "
                    f"{total_uncompressed} > {max_uncompressed_bytes}"
                )
            ratio = info.file_size / max(info.compress_size, 1)
            if info.file_size and ratio > max_compression_ratio:
                raise BundleError(
                    f"suspicious ZIP compression ratio for {normalized}: {ratio:.2f}"
                )
            members.append(
                {
                    "name": normalized,
                    "compressed_size": info.compress_size,
                    "uncompressed_size": info.file_size,
                    "compression_ratio": f"{ratio:.6f}",
                    "is_directory": info.is_dir(),
                    "source_timestamp": (
                        f"{info.date_time[0]:04d}-{info.date_time[1]:02d}-"
                        f"{info.date_time[2]:02d}T{info.date_time[3]:02d}:"
                        f"{info.date_time[4]:02d}:{info.date_time[5]:02d}"
                    ),
                }
            )
        return {
            "member_count": len(infos),
            "compressed_size": total_compressed,
            "declared_uncompressed_size": total_uncompressed,
            "members": members,
        }


def safe_extract_zip(
    zip_path: Path,
    destination: Path,
    *,
    max_members: int = 10_000,
    max_uncompressed_bytes: int = 1_000_000_000,
    max_compression_ratio: float = 1_000.0,
) -> dict[str, object]:
    report = inspect_zip(
        zip_path,
        max_members=max_members,
        max_uncompressed_bytes=max_uncompressed_bytes,
        max_compression_ratio=max_compression_ratio,
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    try:
        with zipfile.ZipFile(zip_path) as archive:
            for info in archive.infolist():
                logical = _safe_zip_member(info.filename)
                target = temporary.joinpath(*logical.parts)
                try:
                    target.resolve().relative_to(temporary.resolve())
                except ValueError as error:
                    raise BundleError(f"ZIP member escapes staging directory: {info.filename}") from error
                if info.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(info) as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output, length=1024 * 1024)
        if destination.exists() or destination.is_symlink():
            if not directory_trees_equal(destination, temporary):
                raise BundleError(
                    f"refusing to reuse divergent extraction destination: {destination}"
                )
            shutil.rmtree(temporary)
        else:
            os.replace(temporary, destination)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return report


def image_dimensions(path: Path) -> tuple[int | None, int | None]:
    try:
        with path.open("rb") as handle:
            header = handle.read(32)
            if header.startswith(b"\x89PNG\r\n\x1a\n") and len(header) >= 24:
                return struct.unpack(">II", header[16:24])
            if header[:2] == b"\xff\xd8":
                handle.seek(2)
                while True:
                    marker_start = handle.read(1)
                    if not marker_start:
                        break
                    if marker_start != b"\xff":
                        continue
                    marker = handle.read(1)
                    while marker == b"\xff":
                        marker = handle.read(1)
                    if marker in {b"\xd8", b"\xd9"}:
                        continue
                    length_bytes = handle.read(2)
                    if len(length_bytes) != 2:
                        break
                    length = struct.unpack(">H", length_bytes)[0]
                    if marker and marker[0] in range(0xC0, 0xC4):
                        data = handle.read(5)
                        if len(data) == 5:
                            height, width = struct.unpack(">HH", data[1:5])
                            return width, height
                        break
                    handle.seek(max(length - 2, 0), 1)
    except OSError:
        pass
    return None, None


def inventory_directory(
    root: Path,
    *,
    source_timestamps: dict[str, str] | None = None,
) -> list[dict[str, object]]:
    rows = []
    first_by_hash: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        digest = sha256_file(path)
        extension = path.suffix.casefold()
        supported = extension in SUPPORTED_IMAGE_EXTENSIONS
        width, height = image_dimensions(path) if supported else (None, None)
        duplicate_of = first_by_hash.get(digest)
        if duplicate_of is None:
            first_by_hash[digest] = relative
        capture_stamp, capture_prefix = capture_identity(relative)
        rows.append(
            {
                "source_filename": relative,
                "source_sha256": digest,
                "size": path.stat().st_size,
                "extension": extension,
                "supported_image": supported,
                "width": width,
                "height": height,
                "capture_identity": capture_stamp,
                "_capture_prefix": capture_prefix,
                "exact_duplicate_of": duplicate_of or "",
                "visual_duplicate_candidate_of": "",
                "historical_duplicate_of": "",
                "historical_candidate_of": "",
                "historical_match_type": "",
                "deduplication_status": "pending" if supported else "unsupported",
                "source_timestamp": (
                    source_timestamps.get(relative)
                    if source_timestamps is not None
                    else str(path.stat().st_mtime_ns)
                ),
            }
        )
    _mark_visual_duplicate_candidates(rows)
    return rows


def prepare_input(
    input_path: Path,
    output_dir: Path,
    *,
    max_members: int = 10_000,
    max_uncompressed_bytes: int = 1_000_000_000,
    max_compression_ratio: float = 1_000.0,
    history_root: Path | None = None,
) -> dict[str, object]:
    input_path = input_path.resolve()
    output_dir = output_dir.resolve()
    if not input_path.exists():
        raise BundleError(f"input path does not exist: {input_path}")
    if input_path.is_dir() and (
        output_dir == input_path or output_dir.is_relative_to(input_path)
    ):
        raise BundleError(
            "output directory must not be the input directory or one of its descendants"
        )
    if input_path.is_file():
        if not zipfile.is_zipfile(input_path):
            raise BundleError(f"input file is not a valid ZIP: {input_path.name}")
        input_sha256 = sha256_file(input_path)
        batch_id = stable_id("batch", input_sha256)
        staging = output_dir / "staging" / batch_id
        zip_report = safe_extract_zip(
            input_path,
            staging,
            max_members=max_members,
            max_uncompressed_bytes=max_uncompressed_bytes,
            max_compression_ratio=max_compression_ratio,
        )
        input_kind = "zip"
    elif input_path.is_dir():
        symlinks = sorted(path for path in input_path.rglob("*") if path.is_symlink())
        if symlinks:
            raise BundleError(
                "screenshot directories must not contain symlinks: "
                f"{symlinks[0].relative_to(input_path).as_posix()}"
            )
        inventory_seed = [
            (path.relative_to(input_path).as_posix(), sha256_file(path))
            for path in sorted(item for item in input_path.rglob("*") if item.is_file())
        ]
        digest = hashlib.sha256()
        for relative, file_hash in inventory_seed:
            digest.update(relative.encode("utf-8"))
            digest.update(b"\0")
            digest.update(file_hash.encode("ascii"))
            digest.update(b"\n")
        input_sha256 = digest.hexdigest()
        batch_id = stable_id("batch", input_sha256)
        staging = input_path
        zip_report = None
        input_kind = "directory"
    else:
        raise BundleError(f"unsupported input path type: {input_path}")

    source_timestamps = (
        {
            str(member["name"]): str(member["source_timestamp"])
            for member in zip_report["members"]
            if not bool(member["is_directory"])
        }
        if zip_report is not None
        else None
    )
    inventory = inventory_directory(staging, source_timestamps=source_timestamps)
    history_records = _history_records(history_root.resolve() if history_root else None)
    _apply_history(inventory, history_records)
    supported_count = sum(bool(row["supported_image"]) for row in inventory)
    if supported_count == 0:
        raise BundleError("input contains no supported screenshot images")
    manifest_path = output_dir / "manifest" / f"{batch_id}.csv"
    write_csv(
        manifest_path,
        inventory,
        (
            "source_filename",
            "source_sha256",
            "size",
            "extension",
            "supported_image",
            "width",
            "height",
            "capture_identity",
            "exact_duplicate_of",
            "visual_duplicate_candidate_of",
            "historical_duplicate_of",
            "historical_candidate_of",
            "historical_match_type",
            "deduplication_status",
            "source_timestamp",
        ),
    )
    skipped_exact = sum(row["deduplication_status"] == "skip_exact_duplicate" for row in inventory)
    skipped_historical = sum(
        row["deduplication_status"] == "skip_already_normalized" for row in inventory
    )
    visual_review = sum(row["deduplication_status"] == "needs_visual_review" for row in inventory)
    pending_count = supported_count - skipped_exact - skipped_historical
    configuration = {
        "max_members": max_members,
        "max_uncompressed_bytes": max_uncompressed_bytes,
        "max_compression_ratio": f"{max_compression_ratio:.6f}",
        "history_index_sha256": _history_index_sha256(history_records),
    }
    configuration_hash = hashlib.sha256(stable_json(configuration).encode("utf-8")).hexdigest()
    state_path = output_dir / "execution" / f"{batch_id}.json"
    if state_path.exists():
        existing = json.loads(state_path.read_text(encoding="utf-8"))
        if (
            existing.get("input_sha256") != input_sha256
            or existing.get("pipeline_version") != PIPELINE_VERSION
            or existing.get("configuration_hash") != configuration_hash
        ):
            raise BundleError("existing batch state is incompatible with input, configuration, or pipeline version")
    state = {
        "schema_version": "1.0.0",
        "batch_id": batch_id,
        "input_name": input_path.name,
        "input_kind": input_kind,
        "input_sha256": input_sha256,
        "pipeline_version": PIPELINE_VERSION,
        "configuration_hash": configuration_hash,
        "schema_version_combat": "2.0.0",
        "mode": "preflight",
        "phase_statuses": {"preflight": "complete", "extraction": "pending", "canonical": "pending"},
        "processed_images": 0,
        "pending_images": pending_count,
        "counts": {
            "supported_images": supported_count,
            "skipped_exact_duplicates": skipped_exact,
            "skipped_already_normalized": skipped_historical,
            "visual_deduplication_review": visual_review,
        },
        "review_queue_size": 0,
        "failed_items": [],
        "retry_counts": {},
        "generated_artifacts": [f"manifest/{batch_id}.csv"],
        "next_action": "run extraction in offline-existing, host-vision, or api-batch mode",
        "zip_preflight": zip_report,
    }
    atomic_write_json(state_path, state)
    return state
