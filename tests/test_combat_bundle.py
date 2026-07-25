from __future__ import annotations

import base64
import hashlib
import io
import json
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts.combat_observations.bundle import (
    REQUIRED_OUTPUTS,
    BundleError,
    build_forensic_report,
    inspect_tar,
    reconstruct_and_verify,
    validate_part_paths,
)


JSONL_COUNTS = {
    "screenshots.jsonl": 1,
    "battles.jsonl": 1,
    "troop_occurrences.jsonl": 1,
    "primary_troop_occurrences.jsonl": 1,
    "troop_battle_consolidated.jsonl": 1,
    "historical_troop_aggregates.jsonl": 1,
}


def valid_payloads() -> dict[str, bytes]:
    validation = {
        "counts": {
            "screenshots": 1,
            "battle_groups": 1,
            "all_rows": 1,
            "primary_troop_occurrences": 1,
            "battle_consolidated_rows": 1,
            "historical_aggregates": 1,
            "review_queue_rows": 1,
        }
    }
    payloads: dict[str, bytes] = {}
    for name in REQUIRED_OUTPUTS:
        if name.endswith(".jsonl"):
            payloads[name] = b'{"id":"one"}\n'
        elif name.endswith(".csv"):
            payloads[name] = b"id,value\none,1\n"
        elif name == "validation_report.json":
            payloads[name] = (json.dumps(validation) + "\n").encode()
        else:
            payloads[name] = b'{"schema_version":"fixture"}\n'
    return payloads


def build_tar(payloads: dict[str, bytes], *, unsafe_member: str | None = None) -> bytes:
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w:xz") as archive:
        for name, data in sorted(payloads.items()):
            info = tarfile.TarInfo(name)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
        if unsafe_member:
            data = b"unsafe"
            info = tarfile.TarInfo(unsafe_member)
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return output.getvalue()


def write_parts(directory: Path, archive: bytes) -> list[Path]:
    encoded = base64.b64encode(archive)
    boundaries = [round(len(encoded) * index / 11) for index in range(12)]
    paths = []
    for index in range(11):
        path = directory / f"bannerlord_normalized_v1.tar.xz.base64.part-{index:02d}"
        path.write_bytes(encoded[boundaries[index] : boundaries[index + 1]])
        paths.append(path)
    return paths


class BundleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def paths(self) -> tuple[Path, Path]:
        return self.root / "normalized.tar.xz", self.root / "reconstructed"

    def test_correct_reconstruction_and_parsing(self) -> None:
        archive = build_tar(valid_payloads())
        write_parts(self.root, archive)
        archive_path, extract_dir = self.paths()
        report = reconstruct_and_verify(
            self.root,
            archive_path,
            extract_dir,
            expected_sha256=hashlib.sha256(archive).hexdigest(),
        )
        self.assertEqual(report["status"], "verified")
        self.assertEqual(report["archive_sha256"], hashlib.sha256(archive).hexdigest())
        self.assertFalse(report["extracted_validation"]["count_discrepancies"])

    def test_missing_part(self) -> None:
        paths = write_parts(self.root, build_tar(valid_payloads()))
        paths[4].unlink()
        with self.assertRaisesRegex(BundleError, "missing"):
            reconstruct_and_verify(self.root, *self.paths(), expected_sha256="0" * 64)

    def test_duplicate_and_out_of_order_parts(self) -> None:
        paths = write_parts(self.root, build_tar(valid_payloads()))
        with self.assertRaisesRegex(BundleError, "duplicate"):
            validate_part_paths([paths[0], paths[0], *paths[2:]])
        reordered = paths.copy()
        reordered[2], reordered[3] = reordered[3], reordered[2]
        with self.assertRaisesRegex(BundleError, "out of order"):
            validate_part_paths(reordered)

    def test_malformed_base64(self) -> None:
        paths = write_parts(self.root, build_tar(valid_payloads()))
        paths[0].write_bytes(b"%" + paths[0].read_bytes()[1:])
        with self.assertRaisesRegex(BundleError, "malformed Base64"):
            reconstruct_and_verify(self.root, *self.paths(), expected_sha256="0" * 64)

    def test_intermediate_padding_corruption_is_rejected(self) -> None:
        paths = write_parts(self.root, build_tar(valid_payloads()))
        paths[3].write_bytes(paths[3].read_bytes() + b"==")
        with self.assertRaisesRegex(
            BundleError,
            "data follows padding|continues after padding|malformed Base64",
        ):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256="0" * 64,
            )

    def test_hash_mismatch_rejects_archive(self) -> None:
        write_parts(self.root, build_tar(valid_payloads()))
        archive_path, extract_dir = self.paths()
        with self.assertRaisesRegex(BundleError, "SHA-256 mismatch"):
            reconstruct_and_verify(self.root, archive_path, extract_dir, expected_sha256="0" * 64)
        self.assertFalse(archive_path.exists())

    def test_unsafe_tar_member(self) -> None:
        archive = build_tar(valid_payloads(), unsafe_member="../escape")
        write_parts(self.root, archive)
        with self.assertRaisesRegex(BundleError, "unsafe archive member"):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256=hashlib.sha256(archive).hexdigest(),
            )

    def test_missing_required_output(self) -> None:
        payloads = valid_payloads()
        del payloads["review_queue.csv"]
        archive = build_tar(payloads)
        write_parts(self.root, archive)
        with self.assertRaisesRegex(BundleError, "required reconstructed outputs are missing"):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256=hashlib.sha256(archive).hexdigest(),
            )

    def test_malformed_json(self) -> None:
        payloads = valid_payloads()
        payloads["validation_report.json"] = b"{"
        archive = build_tar(payloads)
        write_parts(self.root, archive)
        with self.assertRaisesRegex(BundleError, "malformed JSON"):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256=hashlib.sha256(archive).hexdigest(),
            )

    def test_malformed_jsonl_line(self) -> None:
        payloads = valid_payloads()
        payloads["battles.jsonl"] = b"{not-json}\n"
        archive = build_tar(payloads)
        write_parts(self.root, archive)
        with self.assertRaisesRegex(BundleError, "malformed JSONL"):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256=hashlib.sha256(archive).hexdigest(),
            )

    def test_malformed_csv_header(self) -> None:
        payloads = valid_payloads()
        payloads["review_queue.csv"] = b",\none,1\n"
        archive = build_tar(payloads)
        write_parts(self.root, archive)
        with self.assertRaisesRegex(BundleError, "malformed CSV header"):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256=hashlib.sha256(archive).hexdigest(),
            )

    def test_malformed_csv_row_is_rejected(self) -> None:
        payloads = valid_payloads()
        payloads["review_queue.csv"] = b"id,value\none\n"
        archive = build_tar(payloads)
        write_parts(self.root, archive)
        with self.assertRaisesRegex(BundleError, "malformed CSV row"):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256=hashlib.sha256(archive).hexdigest(),
            )

    def test_count_mismatch_is_rejected(self) -> None:
        payloads = valid_payloads()
        payloads["review_queue.csv"] = b"id,value\none,1\ntwo,2\n"
        archive = build_tar(payloads)
        write_parts(self.root, archive)
        with self.assertRaisesRegex(BundleError, "row counts do not match"):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256=hashlib.sha256(archive).hexdigest(),
            )

    def test_duplicate_tar_member_is_rejected(self) -> None:
        output = io.BytesIO()
        with tarfile.open(fileobj=output, mode="w:xz") as archive:
            for payload in (b"first", b"second"):
                info = tarfile.TarInfo("same.json")
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
        archive_path = self.root / "duplicate.tar.xz"
        archive_path.write_bytes(output.getvalue())
        with self.assertRaisesRegex(BundleError, "duplicate archive member"):
            inspect_tar(archive_path)

    def test_tar_size_limit_is_enforced(self) -> None:
        archive_path = self.root / "oversize.tar.xz"
        archive_path.write_bytes(build_tar(valid_payloads()))
        with self.assertRaisesRegex(BundleError, "uncompressed size exceeds limit"):
            inspect_tar(archive_path, max_uncompressed_bytes=1)

    def test_divergent_existing_extraction_is_rejected(self) -> None:
        archive = build_tar(valid_payloads())
        write_parts(self.root, archive)
        expected = hashlib.sha256(archive).hexdigest()
        reconstruct_and_verify(self.root, *self.paths(), expected_sha256=expected)
        (self.paths()[1] / "review_queue.csv").write_text(
            "id,value\nchanged,9\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(BundleError, "divergent extraction destination"):
            reconstruct_and_verify(self.root, *self.paths(), expected_sha256=expected)

    def test_non_standard_json_constant_is_rejected(self) -> None:
        payloads = valid_payloads()
        payloads["battles.jsonl"] = b'{"value":NaN}\n'
        archive = build_tar(payloads)
        write_parts(self.root, archive)
        with self.assertRaisesRegex(BundleError, "non-standard JSON constant"):
            reconstruct_and_verify(
                self.root,
                *self.paths(),
                expected_sha256=hashlib.sha256(archive).hexdigest(),
            )

    def test_deterministic_forensic_report(self) -> None:
        paths = write_parts(self.root, build_tar(valid_payloads()))
        paths[8].write_bytes(paths[8].read_bytes() + b"==")
        first = build_forensic_report(paths, exact_error="fixture failure")
        second = build_forensic_report(paths, exact_error="fixture failure")
        self.assertEqual(first, second)

    def test_idempotent_rerun(self) -> None:
        archive = build_tar(valid_payloads())
        write_parts(self.root, archive)
        expected = hashlib.sha256(archive).hexdigest()
        first = reconstruct_and_verify(self.root, *self.paths(), expected_sha256=expected)
        second = reconstruct_and_verify(self.root, *self.paths(), expected_sha256=expected)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
