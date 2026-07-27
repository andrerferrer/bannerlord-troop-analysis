from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
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


class Pr20IdentityRecoveryTests(unittest.TestCase):
    def test_manifest_hashes_and_row_counts_match(self):
        manifest = json.loads((RECOVERY_ROOT / "manifest.json").read_text(encoding="utf-8"))
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
            self.assertEqual(
                len({(row["troop_id"], resolver.normalize_display_name(row["name"])) for row in rows}),
                len(rows),
            )

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


if __name__ == "__main__":
    unittest.main()
