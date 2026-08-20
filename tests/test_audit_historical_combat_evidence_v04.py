from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[1]
    / "scripts"
    / "analysis"
    / "audit_historical_combat_evidence_v04.py"
)
SPEC = importlib.util.spec_from_file_location("audit_historical_combat_evidence_v04", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def ranking(
    rank: int,
    slug: str,
    deployed: int,
    kills: int,
) -> dict[str, str]:
    return {
        "context": "field",
        "rank": str(rank),
        "display_name": slug.title(),
        "provisional_slug": slug,
        "canonical_troop_id": slug,
        "identity_status": "confirmed_id",
        "independent_battles": "1",
        "deployed": str(deployed),
        "kills": str(kills),
        "kills_per_deployed": f"{kills / deployed:.6f}",
        "reliability_status": "insufficient_evidence",
    }


def consolidated(
    battle_id: str,
    slug: str,
    deployed: int,
    kills: int,
) -> dict[str, object]:
    return {
        "battle_id": battle_id,
        "battle_context": "field",
        "display_name_normalized": slug,
        "deployed": deployed,
        "kills": kills,
    }


class HistoricalEvidenceAuditTests(unittest.TestCase):
    def test_impact_rank_uses_efficiency_and_kill_share(self) -> None:
        rows = MODULE.augment_rankings(
            "batch",
            "realm_of_thrones",
            [
                ranking(1, "burst", 5, 20),
                ranking(2, "majority", 9, 18),
            ],
            [
                consolidated("b2", "burst", 5, 20),
                consolidated("b1", "majority", 9, 18),
            ],
            {
                ("b1", "field"): {
                    "kills": 20,
                    "provenance": "battle_metadata_direct",
                },
                ("b2", "field"): {
                    "kills": 80,
                    "provenance": "battle_metadata_direct",
                },
            },
            "verified",
        )
        by_slug = {row["provisional_slug"]: row for row in rows}

        self.assertEqual(by_slug["majority"]["player_side_kill_share"], "0.900000")
        self.assertEqual(by_slug["majority"]["share_adjusted_impact"], "1.800000")
        self.assertEqual(by_slug["majority"]["impact_rank"], 1)
        self.assertEqual(by_slug["burst"]["player_side_kill_share"], "0.250000")
        self.assertEqual(by_slug["burst"]["share_adjusted_impact"], "1.000000")
        self.assertEqual(by_slug["burst"]["impact_rank"], 2)

    def test_cross_batch_hash_is_skipped_as_already_normalized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for batch_name in ("2026-01-01", "2026-01-02"):
                batch = root / batch_name
                batch.mkdir()
                with (batch / "screenshots_manifest.csv").open(
                    "w", encoding="utf-8", newline=""
                ) as handle:
                    writer = csv.DictWriter(
                        handle,
                        fieldnames=(
                            "screenshot_id",
                            "image_file",
                            "image_sha256",
                            "captured_at",
                            "battle_id",
                            "screen_status",
                            "included_in_primary",
                        ),
                    )
                    writer.writeheader()
                    writer.writerow(
                        {
                            "screenshot_id": batch_name,
                            "image_file": "score.png",
                            "image_sha256": "a" * 64,
                            "captured_at": "2026-01-01T00:00:00-03:00",
                            "battle_id": batch_name,
                            "screen_status": "final_result",
                            "included_in_primary": "True",
                        }
                    )

            rows = MODULE.screenshot_audit_rows(root)

        self.assertEqual(rows[0]["decision"], "keep_existing_representative")
        self.assertEqual(rows[1]["decision"], "skip_already_normalized")
        self.assertEqual(
            rows[1]["representative_or_prior"],
            "2026-01-01:2026-01-01",
        )


if __name__ == "__main__":
    unittest.main()
