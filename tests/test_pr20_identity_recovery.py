from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]
RECOVERY_ROOT = REPO_ROOT / "data" / "canonical_identity_recovery" / "pr20"
RESOLVER_PATH = REPO_ROOT / "scripts" / "analysis" / "build_canonical_identity_audit.py"

spec = importlib.util.spec_from_file_location("canonical_recovery_resolver", RESOLVER_PATH)
assert spec and spec.loader
resolver = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = resolver
spec.loader.exec_module(resolver)


def source_identity_pairs() -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    in_table = False
    source = (RECOVERY_ROOT / "SOURCE_PR_BODY.md").read_text(encoding="utf-8")
    for line in source.splitlines():
        if line == "| Observed label | Track | `troop_id` |":
            in_table = True
            continue
        if not in_table or line == "|---|---|---|":
            continue
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        name = re.sub(r" \[T\d+\]$", "", cells[0])
        troop_id = cells[2].split("`")[1]
        pairs.add((resolver.normalize_display_name(name), troop_id))
    return pairs


class Pr20IdentityRecoveryTests(unittest.TestCase):
    def test_manifest_hashes_and_row_counts_match(self):
        manifest = json.loads((RECOVERY_ROOT / "manifest.json").read_text(encoding="utf-8"))
        source_path = RECOVERY_ROOT / manifest["source"]["path"]
        self.assertEqual(source_path.stat().st_size, manifest["source"]["body_bytes_utf8"])
        self.assertEqual(
            hashlib.sha256(source_path.read_bytes()).hexdigest(),
            manifest["source"]["body_sha256_utf8"],
        )
        recovered_pairs: set[tuple[str, str]] = set()
        for artifact in manifest["artifacts"]:
            artifact_path = RECOVERY_ROOT / artifact["path"]
            self.assertEqual(
                hashlib.sha256(artifact_path.read_bytes()).hexdigest(),
                artifact["sha256"],
            )
            with artifact_path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), artifact["rows"])
            self.assertTrue(all(row["troop_id"] and row["name"] for row in rows))
            self.assertTrue(
                all(
                    row["evidence_kind"] == artifact["evidence_kind"]
                    == resolver.HISTORICAL_REPORTED_EXACT
                    and row["coverage_scope"] == artifact["coverage_scope"]
                    == "sparse_published_exact_matches"
                    and int(row["reported_full_audit_rows"])
                    == artifact["reported_full_audit_rows"]
                    for row in rows
                )
            )
            self.assertEqual(
                len({(row["troop_id"], resolver.normalize_display_name(row["name"])) for row in rows}),
                len(rows),
            )
            recovered_pairs.update(
                (resolver.normalize_display_name(row["name"]), row["troop_id"])
                for row in rows
            )
        self.assertEqual(recovered_pairs, source_identity_pairs())

    def test_recovered_exact_matches_resolve_seventeen_baseline_labels(self):
        manifest = json.loads((RECOVERY_ROOT / "manifest.json").read_text(encoding="utf-8"))
        track_specs = [
            (artifact["track"], RECOVERY_ROOT / artifact["path"])
            for artifact in manifest["artifacts"]
        ]
        candidates = resolver.load_candidates(track_specs)
        baseline = resolver.read_rows(
            REPO_ROOT / "analysis" / "empirical" / "2026-07-23" / "baseline_strict_player_side.csv"
        )
        resolved = {
            row["canonical_name_slug"]: resolver.resolve_row(row, None, candidates)
            for row in baseline
        }
        confirmed = sum(row["match_status"] == resolver.CONFIRMED for row in resolved.values())
        self.assertEqual(confirmed, manifest["expected_resolution"]["confirmed_ids"])
        self.assertEqual(
            len(resolved) - confirmed,
            manifest["expected_resolution"]["unresolved"],
        )
        self.assertTrue(
            all(
                row["resolution_method"].startswith("historical_pr_reported_exact")
                for row in resolved.values()
                if row["match_status"] == resolver.CONFIRMED
            )
        )
        self.assertEqual(
            {
                slug
                for slug, row in resolved.items()
                if row["match_status"] != resolver.CONFIRMED
            },
            {
                "rhoynar_bahriyyah_t5",
                "rhodok_admiral_sharpshooter",
                "rhodok_sharpshooter",
                "rhodok_river_guard",
                "rhodok_sarge",
                "rhodok_river_hunter",
                "reaver_t4",
            },
        )


if __name__ == "__main__":
    unittest.main()
