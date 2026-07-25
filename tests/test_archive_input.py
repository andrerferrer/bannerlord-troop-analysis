from __future__ import annotations

import stat
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

from scripts.combat_observations.archive_input import inspect_zip, prepare_input
from scripts.combat_observations.bundle import BundleError


PNG_FIXTURE = b"\x89PNG\r\n\x1a\n" + b"\x00" * 8 + (1).to_bytes(4, "big") + (1).to_bytes(4, "big") + b"\x00" * 16


class ArchiveInputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def make_zip(self, name: str, members: list[tuple[object, bytes]], *, compression=zipfile.ZIP_DEFLATED) -> Path:
        path = self.root / name
        with zipfile.ZipFile(path, "w", compression=compression) as archive:
            for member, payload in members:
                archive.writestr(member, payload)
        return path

    def test_valid_zip_manifest_duplicates_and_resume(self) -> None:
        archive = self.make_zip(
            "valid.zip",
            [("one.png", PNG_FIXTURE), ("nested/two.png", PNG_FIXTURE), ("notes.txt", b"not an image")],
        )
        output = self.root / "output"
        first = prepare_input(archive, output)
        second = prepare_input(archive, output)
        self.assertEqual(first, second)
        self.assertEqual(first["pending_images"], 2)
        manifest = (output / first["generated_artifacts"][0]).read_text(encoding="utf-8")
        self.assertIn("nested/two.png", manifest)
        self.assertIn("one.png", manifest)
        self.assertIn("notes.txt", manifest)
        self.assertIn("exact_duplicate_of", manifest)

    def test_corrupt_zip_is_not_empty_batch(self) -> None:
        path = self.root / "corrupt.zip"
        path.write_bytes(b"not a zip")
        with self.assertRaisesRegex(BundleError, "not a valid ZIP"):
            prepare_input(path, self.root / "output")

    def test_path_traversal_is_rejected(self) -> None:
        archive = self.make_zip("traversal.zip", [("../escape.png", PNG_FIXTURE)])
        with self.assertRaisesRegex(BundleError, "unsafe ZIP member path"):
            inspect_zip(archive)

    def test_symlink_is_rejected(self) -> None:
        info = zipfile.ZipInfo("link.png")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive = self.make_zip("symlink.zip", [(info, b"target")], compression=zipfile.ZIP_STORED)
        with self.assertRaisesRegex(BundleError, "symlinks are not allowed"):
            inspect_zip(archive)

    def test_duplicate_member_name_is_rejected(self) -> None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            archive = self.make_zip(
                "duplicate.zip",
                [("same.png", PNG_FIXTURE), ("same.png", PNG_FIXTURE)],
            )
        with self.assertRaisesRegex(BundleError, "duplicate ZIP member name"):
            inspect_zip(archive)

    def test_suspicious_compression_ratio_is_rejected(self) -> None:
        archive = self.make_zip("ratio.zip", [("bomb.png", b"\0" * 100_000)])
        with self.assertRaisesRegex(BundleError, "suspicious ZIP compression ratio"):
            inspect_zip(archive, max_compression_ratio=10)

    def test_unrelated_files_are_rejected_without_execution(self) -> None:
        archive = self.make_zip("unrelated.zip", [("run.py", b"raise SystemExit('must not run')")])
        with self.assertRaisesRegex(BundleError, "no supported screenshot images"):
            prepare_input(archive, self.root / "output")

    def test_directory_output_cannot_modify_input_tree(self) -> None:
        images = self.root / "images"
        images.mkdir()
        (images / "one.png").write_bytes(PNG_FIXTURE)
        with self.assertRaisesRegex(BundleError, "must not be the input directory"):
            prepare_input(images, images / "generated")

    def test_directory_symlink_is_rejected(self) -> None:
        images = self.root / "symlink-images"
        images.mkdir()
        target = self.root / "outside.png"
        target.write_bytes(PNG_FIXTURE)
        (images / "linked.png").symlink_to(target)
        with self.assertRaisesRegex(BundleError, "must not contain symlinks"):
            prepare_input(images, self.root / "symlink-output")

    def test_divergent_existing_zip_staging_is_rejected(self) -> None:
        archive = self.make_zip("valid.zip", [("one.png", PNG_FIXTURE)])
        output = self.root / "output"
        state = prepare_input(archive, output)
        staged = output / "staging" / state["batch_id"] / "one.png"
        staged.write_bytes(PNG_FIXTURE + b"changed")
        with self.assertRaisesRegex(BundleError, "divergent extraction destination"):
            prepare_input(archive, output)


if __name__ == "__main__":
    unittest.main()
