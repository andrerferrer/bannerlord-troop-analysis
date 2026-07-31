"""xml_ssot_package: artifact_hashes must pin every track audit CSV."""

from __future__ import annotations

import csv
import hashlib
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EXPORT_ID = "export_20260731_150800"
PACKAGE_ROOT = REPO / "data" / "xml_exports" / EXPORT_ID
HASHES_PATH = PACKAGE_ROOT / "artifact_hashes.csv"
PACKAGE_JSON = PACKAGE_ROOT / "PACKAGE.json"
TRACKS = ("vanilla", "nightmare_sails", "realm_of_thrones", "taom")
SOURCE_ZIP_SHA256 = (
    "c3614f6e41ae629bf95d3a34adf2b730a9ad0453a20d9c1d3858e277f30ea962"
)


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_hash_rows() -> list[dict[str, str]]:
    with HASHES_PATH.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _expected_package_sha256(rows: list[dict[str, str]]) -> str:
    lines = [
        f"{row['path']},{row['bytes']},{row['sha256']}"
        for row in sorted(rows, key=lambda item: item["path"])
    ]
    payload = "\n".join(lines) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class XmlSsotPackageHashTests(unittest.TestCase):
    def test_package_json_declares_xml_ssot_kind(self) -> None:
        self.assertTrue(PACKAGE_JSON.is_file(), "PACKAGE.json missing")
        package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
        self.assertEqual(package["package_kind"], "xml_ssot_package")
        self.assertEqual(package["export_id"], EXPORT_ID)
        self.assertEqual(package["source_zip"]["sha256"], SOURCE_ZIP_SHA256)
        self.assertEqual(package["source_zip"]["retention"], "local_only")
        self.assertTrue(package["source_zip"]["lfs_declined"])
        self.assertTrue(package["source_zip"]["git_declined"])

    def test_artifact_hashes_cover_every_audit_csv(self) -> None:
        rows = _load_hash_rows()
        by_path = {row["path"]: row for row in rows}
        missing: list[str] = []
        mismatched: list[str] = []
        for track in TRACKS:
            audit_dir = REPO / "data" / track / "audit"
            self.assertTrue(audit_dir.is_dir(), f"missing audit dir {audit_dir}")
            for path in sorted(audit_dir.glob("*.csv")):
                rel = path.relative_to(REPO).as_posix()
                if rel not in by_path:
                    missing.append(rel)
                    continue
                actual = _sha256_file(path)
                if by_path[rel]["sha256"] != actual:
                    mismatched.append(rel)
                if int(by_path[rel]["bytes"]) != path.stat().st_size:
                    mismatched.append(f"{rel}:bytes")
        self.assertEqual(missing, [], f"audit CSVs missing from artifact_hashes: {missing}")
        self.assertEqual(mismatched, [], f"hash/size mismatch: {mismatched}")

    def test_artifact_hashes_exclude_self_and_match_package_digest(self) -> None:
        rows = _load_hash_rows()
        rel_hashes = HASHES_PATH.relative_to(REPO).as_posix()
        self.assertNotIn(rel_hashes, {row["path"] for row in rows})
        package = json.loads(PACKAGE_JSON.read_text(encoding="utf-8"))
        self.assertEqual(
            package["expected_package_sha256"],
            _expected_package_sha256(rows),
        )

    def test_no_xml_bodies_listed_in_hashes(self) -> None:
        for row in _load_hash_rows():
            self.assertFalse(
                row["path"].lower().endswith(".xml"),
                f"XML body must not be hash-pinned in package: {row['path']}",
            )


if __name__ == "__main__":
    unittest.main()
