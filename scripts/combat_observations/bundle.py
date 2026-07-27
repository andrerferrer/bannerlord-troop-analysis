from __future__ import annotations

import base64
import binascii
import csv
import hashlib
import io
import json
import lzma
import os
import re
import shutil
import tarfile
import tempfile
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence


PART_PATTERN = re.compile(r"^bannerlord_normalized_v1\.tar\.xz\.base64\.part-(\d{2})$")
EXPECTED_PART_INDICES = tuple(range(11))
EXPECTED_ARCHIVE_SHA256 = "10446ce7afb01ec35211c06468812bf2fa3d53e6091f128a7ec67ca605dea2aa"
MAX_TAR_MEMBERS = 10_000
MAX_TAR_UNCOMPRESSED_BYTES = 1_000_000_000

REQUIRED_OUTPUTS = (
    "screenshots_manifest.csv",
    "screenshots.jsonl",
    "battles.jsonl",
    "troop_occurrences.jsonl",
    "primary_troop_occurrences.jsonl",
    "troop_battle_consolidated.jsonl",
    "historical_troop_aggregates.jsonl",
    "ranking_complete.csv",
    "ranking_reliable.csv",
    "review_queue.csv",
    "validation_report.json",
    "combat_troop_occurrence.schema.json",
)

COUNT_KEYS = {
    "screenshots.jsonl": "screenshots",
    "battles.jsonl": "battle_groups",
    "troop_occurrences.jsonl": "all_rows",
    "primary_troop_occurrences.jsonl": "primary_troop_occurrences",
    "troop_battle_consolidated.jsonl": "battle_consolidated_rows",
    "historical_troop_aggregates.jsonl": "historical_aggregates",
    "review_queue.csv": "review_queue_rows",
}


class BundleError(RuntimeError):
    """Raised when the normalized bundle fails an integrity or safety gate."""


@dataclass(frozen=True)
class PartInfo:
    index: int
    name: str
    size: int
    sha256: str
    padding_count: int
    padding_positions: tuple[int, ...]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def directory_trees_equal(left: Path, right: Path) -> bool:
    if (
        not left.is_dir()
        or not right.is_dir()
        or left.is_symlink()
        or right.is_symlink()
    ):
        return False

    def snapshot(root: Path) -> list[tuple[str, int, str]]:
        return [
            (path.relative_to(root).as_posix(), path.stat().st_size, sha256_file(path))
            for path in sorted(item for item in root.rglob("*") if item.is_file())
        ]

    return snapshot(left) == snapshot(right)


def atomic_write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ) + "\n"
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def validate_part_paths(paths: Sequence[Path], *, require_order: bool = True) -> list[Path]:
    indexed: list[tuple[int, Path]] = []
    seen: set[int] = set()
    for path in paths:
        match = PART_PATTERN.fullmatch(path.name)
        if not match:
            raise BundleError(f"unexpected bundle part name: {path.name}")
        index = int(match.group(1))
        if index in seen:
            raise BundleError(f"duplicate bundle part index: {index:02d}")
        seen.add(index)
        indexed.append((index, path))

    actual = tuple(index for index, _ in indexed)
    if require_order and actual != tuple(sorted(actual)):
        raise BundleError(f"bundle parts are out of order: {actual}")
    missing = sorted(set(EXPECTED_PART_INDICES) - seen)
    extra = sorted(seen - set(EXPECTED_PART_INDICES))
    if missing or extra:
        raise BundleError(f"invalid bundle sequence; missing={missing}, extra={extra}")
    if len(indexed) != len(EXPECTED_PART_INDICES):
        raise BundleError(f"expected 11 bundle parts, found {len(indexed)}")
    return [path for _, path in sorted(indexed)]


def discover_parts(bundle_dir: Path) -> list[Path]:
    candidates = list(bundle_dir.glob("bannerlord_normalized_v1.tar.xz.base64.part-*"))
    return validate_part_paths(sorted(candidates), require_order=True)


def inspect_parts(parts: Sequence[Path]) -> list[PartInfo]:
    result = []
    for index, path in enumerate(parts):
        data = path.read_bytes()
        result.append(
            PartInfo(
                index=index,
                name=path.name,
                size=len(data),
                sha256=hashlib.sha256(data).hexdigest(),
                padding_count=data.count(b"="),
                padding_positions=tuple(pos for pos, byte in enumerate(data) if byte == ord("=")),
            )
        )
    return result


def _clean_base64_chunk(data: bytes, source: str) -> bytes:
    compact = b"".join(data.split())
    allowed = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    invalid = sorted(set(compact) - set(allowed))
    if invalid:
        rendered = ", ".join(f"0x{byte:02x}" for byte in invalid)
        raise BundleError(f"malformed Base64 in {source}: invalid bytes {rendered}")
    return compact


def decode_parts_streaming(parts: Sequence[Path], output_path: Path) -> str:
    """Decode ordered parts strictly without retaining the whole archive in memory."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256()
    carry = b""
    padding_seen = False
    try:
        with output_path.open("wb") as output:
            for part in parts:
                with part.open("rb") as handle:
                    while True:
                        raw = handle.read(64 * 1024)
                        if not raw:
                            break
                        compact = _clean_base64_chunk(raw, part.name)
                        if padding_seen and compact:
                            raise BundleError(f"Base64 data continues after padding before {part.name}")
                        combined = carry + compact
                        complete_length = len(combined) - (len(combined) % 4)
                        block = combined[:complete_length]
                        carry = combined[complete_length:]
                        if b"=" in block:
                            first_padding = block.index(b"=")
                            if any(byte != ord("=") for byte in block[first_padding:]):
                                raise BundleError(f"non-padding Base64 data follows padding in {part.name}")
                            padding_seen = True
                        if block:
                            try:
                                decoded = base64.b64decode(block, validate=True)
                            except binascii.Error as error:
                                raise BundleError(f"malformed Base64 in {part.name}: {error}") from error
                            output.write(decoded)
                            digest.update(decoded)
            if carry:
                if padding_seen:
                    raise BundleError("trailing Base64 data follows an earlier padded segment")
                try:
                    decoded = base64.b64decode(carry, validate=True)
                except binascii.Error as error:
                    raise BundleError(f"malformed trailing Base64: {error}") from error
                output.write(decoded)
                digest.update(decoded)
    except Exception:
        output_path.unlink(missing_ok=True)
        raise
    return digest.hexdigest()


def _safe_member_path(root: Path, member_name: str) -> Path:
    logical = PurePosixPath(member_name)
    if logical.is_absolute() or ".." in logical.parts or not logical.parts:
        raise BundleError(f"unsafe archive member path: {member_name}")
    destination = root.joinpath(*logical.parts)
    try:
        destination.resolve().relative_to(root.resolve())
    except ValueError as error:
        raise BundleError(f"archive member escapes extraction root: {member_name}") from error
    return destination


def inspect_tar(
    archive_path: Path,
    *,
    max_members: int = MAX_TAR_MEMBERS,
    max_uncompressed_bytes: int = MAX_TAR_UNCOMPRESSED_BYTES,
) -> list[dict[str, object]]:
    members: list[dict[str, object]] = []
    try:
        with tarfile.open(archive_path, mode="r:xz") as archive:
            seen: dict[str, str] = {}
            total_uncompressed = 0
            for member_count, member in enumerate(archive, start=1):
                if member_count > max_members:
                    raise BundleError(
                        f"tar member count exceeds limit: {member_count} > {max_members}"
                    )
                _safe_member_path(Path("/safe-root"), member.name)
                normalized = PurePosixPath(member.name).as_posix()
                collision_key = unicodedata.normalize("NFC", normalized).casefold()
                if collision_key in seen:
                    raise BundleError(f"duplicate archive member name: {normalized}")
                if member.issym() or member.islnk():
                    raise BundleError(f"archive links are not allowed: {member.name}")
                if not (member.isfile() or member.isdir()):
                    raise BundleError(f"unsupported archive member type: {member.name}")
                kind = "file" if member.isfile() else "directory"
                ancestors = list(PurePosixPath(collision_key).parents)[:-1]
                if any(seen.get(parent.as_posix()) == "file" for parent in ancestors):
                    raise BundleError(f"archive member is nested beneath a file: {normalized}")
                if kind == "file" and any(
                    existing.startswith(collision_key + "/") for existing in seen
                ):
                    raise BundleError(f"archive file collides with a directory: {normalized}")
                seen[collision_key] = kind
                if member.isfile():
                    total_uncompressed += member.size
                    if total_uncompressed > max_uncompressed_bytes:
                        raise BundleError(
                            "tar declared uncompressed size exceeds limit: "
                            f"{total_uncompressed} > {max_uncompressed_bytes}"
                        )
                members.append({"name": member.name, "size": member.size, "type": kind})
    except (tarfile.TarError, lzma.LZMAError, EOFError) as error:
        raise BundleError(f"invalid tar.xz archive: {error}") from error
    return members


def safe_extract_tar(archive_path: Path, destination: Path) -> None:
    members = inspect_tar(archive_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    try:
        with tarfile.open(archive_path, mode="r:xz") as archive:
            by_name = {member.name: member for member in archive.getmembers()}
            for description in members:
                member = by_name[str(description["name"])]
                target = _safe_member_path(temporary, member.name)
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    raise BundleError(f"could not read archive member: {member.name}")
                with source, target.open("xb") as output:
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


def _locate_payload_root(extracted_root: Path) -> Path:
    if all((extracted_root / name).exists() for name in REQUIRED_OUTPUTS):
        return extracted_root
    directories = [path for path in extracted_root.iterdir() if path.is_dir()]
    if len(directories) == 1 and all((directories[0] / name).exists() for name in REQUIRED_OUTPUTS):
        return directories[0]
    return extracted_root


def _parse_json(path: Path) -> tuple[int, object]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(
                handle,
                parse_constant=lambda constant: (_ for _ in ()).throw(
                    ValueError(f"non-standard JSON constant {constant}")
                ),
            )
    except (OSError, UnicodeError, ValueError) as error:
        raise BundleError(f"malformed JSON {path.name}: {error}") from error
    return 1, value


def _parse_jsonl(path: Path) -> tuple[int, None]:
    count = 0
    try:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                value = json.loads(
                    line,
                    parse_constant=lambda constant: (_ for _ in ()).throw(
                        ValueError(f"non-standard JSON constant {constant}")
                    ),
                )
                if not isinstance(value, dict):
                    raise BundleError(f"JSONL record is not an object in {path.name}:{line_number}")
                count += 1
    except (OSError, UnicodeError, ValueError) as error:
        raise BundleError(f"malformed JSONL {path.name}: {error}") from error
    return count, None


def _parse_csv(path: Path) -> tuple[int, tuple[str, ...]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if (
                not reader.fieldnames
                or any(not name.strip() for name in reader.fieldnames)
                or len(set(reader.fieldnames)) != len(reader.fieldnames)
            ):
                raise BundleError(f"malformed CSV header in {path.name}")
            count = 0
            for line_number, row in enumerate(reader, 2):
                if None in row or any(value is None for value in row.values()):
                    raise BundleError(f"malformed CSV row in {path.name}:{line_number}")
                count += 1
    except (OSError, UnicodeError, csv.Error) as error:
        raise BundleError(f"malformed CSV {path.name}: {error}") from error
    return count, tuple(reader.fieldnames)


def validate_extracted_outputs(extracted_root: Path) -> dict[str, object]:
    payload_root = _locate_payload_root(extracted_root)
    missing = [name for name in REQUIRED_OUTPUTS if not (payload_root / name).is_file()]
    if missing:
        raise BundleError(f"required reconstructed outputs are missing: {missing}")

    observed: dict[str, int] = {}
    headers: dict[str, list[str]] = {}
    parsed_json: dict[str, object] = {}
    for name in REQUIRED_OUTPUTS:
        path = payload_root / name
        if name.endswith(".jsonl"):
            observed[name], _ = _parse_jsonl(path)
        elif name.endswith(".csv"):
            observed[name], csv_headers = _parse_csv(path)
            headers[name] = list(csv_headers)
        elif name.endswith(".json"):
            observed[name], parsed_json[name] = _parse_json(path)

    validation_report = parsed_json.get("validation_report.json")
    if not isinstance(validation_report, dict) or not isinstance(validation_report.get("counts"), dict):
        raise BundleError("validation_report.json has no counts object")
    recorded_counts = validation_report["counts"]
    discrepancies = []
    for filename, count_key in COUNT_KEYS.items():
        recorded = recorded_counts.get(count_key)
        actual = observed.get(filename)
        if recorded is not None and actual != recorded:
            discrepancies.append(
                {"file": filename, "count_key": count_key, "recorded": recorded, "observed": actual}
            )
    if discrepancies:
        raise BundleError(f"reconstructed row counts do not match validation report: {discrepancies}")
    return {
        "payload_root": str(payload_root.relative_to(extracted_root)) if payload_root != extracted_root else ".",
        "observed_rows": dict(sorted(observed.items())),
        "csv_headers": dict(sorted(headers.items())),
        "recorded_counts": dict(sorted(recorded_counts.items())),
        "count_discrepancies": discrepancies,
    }


def _containment_relationships(parts: Sequence[Path]) -> list[dict[str, object]]:
    payloads = [(part.name, _clean_base64_chunk(part.read_bytes(), part.name)) for part in parts]
    relationships = []
    for outer_name, outer in payloads:
        for inner_name, inner in payloads:
            if outer_name == inner_name or len(inner) > len(outer):
                continue
            position = outer.find(inner)
            if position >= 0:
                relationships.append({"container": outer_name, "contained": inner_name, "offset": position})
    return sorted(relationships, key=lambda item: (str(item["container"]), str(item["contained"])))


def build_forensic_report(
    parts: Sequence[Path],
    *,
    expected_sha256: str = EXPECTED_ARCHIVE_SHA256,
    exact_error: str | None = None,
) -> dict[str, object]:
    infos = inspect_parts(parts)
    compact_parts = [_clean_base64_chunk(part.read_bytes(), part.name) for part in parts]
    combined = b"".join(compact_parts)
    padding_positions = [position for position, byte in enumerate(combined) if byte == ord("=")]
    repair: dict[str, object] = {"method": "strip_all_padding_then_restore_terminal_padding"}
    repaired = combined.replace(b"=", b"")
    repaired += b"=" * ((-len(repaired)) % 4)
    try:
        decoded = base64.b64decode(repaired, validate=True)
        repair["decoded_size"] = len(decoded)
        repair["sha256"] = hashlib.sha256(decoded).hexdigest()
        repair["matches_expected_sha256"] = repair["sha256"] == expected_sha256
        try:
            with lzma.open(io.BytesIO(decoded), "rb") as stream:
                while stream.read(1024 * 1024):
                    pass
            repair["xz_status"] = "valid"
        except (lzma.LZMAError, EOFError) as error:
            repair["xz_status"] = "invalid"
            repair["xz_error"] = str(error)
    except binascii.Error as error:
        repair["decode_error"] = str(error)

    return {
        "schema_version": "1.0.0",
        "status": "corrupt_unverified",
        "expected_archive_sha256": expected_sha256,
        "parts": [asdict(info) for info in infos],
        "combined_base64_size": len(combined),
        "combined_base64_modulo_4": len(combined) % 4,
        "combined_padding_positions": padding_positions,
        "containment_relationships": _containment_relationships(parts),
        "exact_reconstruction_error": exact_error,
        "attempted_repairs": [repair],
    }


def reconstruct_and_verify(
    bundle_dir: Path,
    archive_path: Path,
    extract_dir: Path,
    *,
    expected_sha256: str = EXPECTED_ARCHIVE_SHA256,
) -> dict[str, object]:
    parts = discover_parts(bundle_dir)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive_path.with_name(f".{archive_path.name}.partial")
    temporary.unlink(missing_ok=True)
    actual_sha256 = decode_parts_streaming(parts, temporary)
    if actual_sha256 != expected_sha256:
        temporary.unlink(missing_ok=True)
        raise BundleError(
            f"archive SHA-256 mismatch: expected {expected_sha256}, observed {actual_sha256}"
        )
    inspect_tar(temporary)
    os.replace(temporary, archive_path)
    safe_extract_tar(archive_path, extract_dir)
    validation = validate_extracted_outputs(extract_dir)
    return {
        "schema_version": "1.0.0",
        "status": "verified",
        "archive_sha256": actual_sha256,
        "archive_size": archive_path.stat().st_size,
        "parts": [asdict(info) for info in inspect_parts(parts)],
        "extracted_validation": validation,
    }
