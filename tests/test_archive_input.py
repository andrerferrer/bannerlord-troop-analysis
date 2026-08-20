from __future__ import annotations

import stat
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

from scripts.combat_observations.archive_input import capture_identity, inspect_zip, prepare_input
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
        self.assertEqual(first["pending_images"], 1)
        self.assertEqual(first["counts"]["skipped_exact_duplicates"], 1)
        manifest = (output / first["generated_artifacts"][0]).read_text(encoding="utf-8")
        self.assertIn("nested/two.png", manifest)
        self.assertIn("one.png", manifest)
        self.assertIn("notes.txt", manifest)
        self.assertIn("exact_duplicate_of", manifest)

    def test_capture_identity_handles_bannerlord_and_armoury_names(self) -> None:
        bannerlord = (
            "Mount and Blade II Bannerlord PID_ 10 - Modules_ 19_08_2026 21_03_23.png"
        )
        armoury = "Armoury Crate SE 17_08_2026 23_18_42.png"
        self.assertEqual(capture_identity(bannerlord)[0], "2026-08-19T21:03:23")
        self.assertEqual(capture_identity(armoury)[0], "2026-08-17T23:18:42")

    def test_reencoded_historical_capture_is_skipped_by_identity(self) -> None:
        history = self.root / "history" / "prior-batch"
        history.mkdir(parents=True)
        filename = "Armoury Crate SE 17_08_2026 23_18_42.png"
        (history / "screenshots_manifest.csv").write_text(
            "image_file,image_sha256,battle_id\n"
            f"{filename},{'a' * 64},battle-prior\n",
            encoding="utf-8",
        )
        archive = self.make_zip("repeat.zip", [(filename, PNG_FIXTURE + b"reencoded")])
        output = self.root / "historical-output"
        state = prepare_input(archive, output, history_root=self.root / "history")
        self.assertEqual(state["pending_images"], 0)
        self.assertEqual(state["counts"]["skipped_already_normalized"], 1)
        manifest = (output / state["generated_artifacts"][0]).read_text(encoding="utf-8")
        self.assertIn("capture_identity_and_filename", manifest)
        self.assertIn("skip_already_normalized", manifest)

    def test_close_captures_require_visual_review_instead_of_auto_skip(self) -> None:
        archive = self.make_zip(
            "near.zip",
            [
                ("Bannerlord PID_ 1_19_08_2026 21_02_50.png", PNG_FIXTURE + b"first"),
                ("Bannerlord PID_ 1_19_08_2026 21_03_23.png", PNG_FIXTURE + b"second"),
            ],
        )
        output = self.root / "near-output"
        state = prepare_input(archive, output)
        self.assertEqual(state["pending_images"], 2)
        self.assertEqual(state["counts"]["visual_deduplication_review"], 1)
        manifest = (output / state["generated_artifacts"][0]).read_text(encoding="utf-8")
        self.assertIn("needs_visual_review", manifest)

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
