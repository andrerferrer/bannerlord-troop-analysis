from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.combat_observations.gate_status import (
    GateStatusError,
    build_report,
    main,
)

RANKING_FIELDS = [
    "context",
    "display_name",
    "provisional_slug",
    "canonical_troop_id",
    "identity_status",
    "independent_battles",
    "deployed",
]


def write_batch(
    root: Path,
    name: str,
    *,
    track: str,
    context_battle_counts: dict[str, int],
    rows: list[dict[str, object]],
) -> Path:
    """Write a minimal synthetic batch directory shaped like a real
    committed combat_observations batch: normalization_summary.json plus
    analysis/ranking_complete.csv."""

    batch_dir = root / name
    (batch_dir / "analysis").mkdir(parents=True)

    (batch_dir / "normalization_summary.json").write_text(
        json.dumps(
            {
                "game_track": track,
                "battles": sum(context_battle_counts.values()),
                "battle_context_counts": context_battle_counts,
            }
        ),
        encoding="utf-8",
    )

    ranking_path = batch_dir / "analysis" / "ranking_complete.csv"
    with ranking_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RANKING_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            full_row = {field: row.get(field, "") for field in RANKING_FIELDS}
            writer.writerow(full_row)

    return batch_dir


def row(
    *,
    context: str,
    display_name: str,
    slug: str,
    battles: int,
    deployed: int,
    canonical_troop_id: str = "",
    identity_status: str = "unresolved",
) -> dict[str, object]:
    return {
        "context": context,
        "display_name": display_name,
        "provisional_slug": slug,
        "canonical_troop_id": canonical_troop_id,
        "identity_status": identity_status,
        "independent_battles": battles,
        "deployed": deployed,
    }


class GateStatusBelowGateTests(unittest.TestCase):
    def test_single_batch_below_gate_on_both_axes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            write_batch(
                data_root,
                "batch-a",
                track="realm_of_thrones",
                context_battle_counts={"field": 2},
                rows=[
                    row(
                        context="field",
                        display_name="Ravens' Teeth",
                        slug="ravens_teeth",
                        battles=2,
                        deployed=9,
                        canonical_troop_id="ravens_teeth",
                        identity_status="confirmed_id",
                    )
                ],
            )

            report = build_report(data_root, ["realm_of_thrones"])

            self.assertFalse(report["overall_gate_met"])
            track_report = report["tracks"]["realm_of_thrones"]
            self.assertFalse(track_report["gate_met"])
            field_report = track_report["contexts"]["field"]
            self.assertEqual(field_report["independent_battles_captured"], 2)
            self.assertFalse(field_report["gate_met"])
            troop = field_report["relationships"]["player_party"]["troops"][0]
            self.assertFalse(troop["gate_met"])
            self.assertEqual(troop["battles_needed"], 3)
            self.assertEqual(troop["deployed_needed"], 11)

    def test_exit_code_is_nonzero_below_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            write_batch(
                data_root,
                "batch-a",
                track="realm_of_thrones",
                context_battle_counts={"field": 1},
                rows=[row(context="field", display_name="X", slug="x", battles=1, deployed=1)],
            )
            exit_code = main(["--data-root", str(data_root), "--track", "realm_of_thrones"])
            self.assertEqual(exit_code, 1)


class GateStatusAtGateTests(unittest.TestCase):
    def test_single_batch_exactly_meets_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            write_batch(
                data_root,
                "batch-a",
                track="nightmare_sails",
                context_battle_counts={"field": 5},
                rows=[
                    row(
                        context="field",
                        display_name="Nord Huscarl",
                        slug="nord_huscarl",
                        battles=5,
                        deployed=20,
                        canonical_troop_id="nord_huscarl",
                        identity_status="confirmed_id",
                    )
                ],
            )

            report = build_report(data_root, ["nightmare_sails"])

            self.assertTrue(report["overall_gate_met"])
            track_report = report["tracks"]["nightmare_sails"]
            self.assertTrue(track_report["gate_met"])
            troop = track_report["contexts"]["field"]["relationships"]["player_party"]["troops"][0]
            self.assertTrue(troop["gate_met"])
            self.assertEqual(troop["battles_needed"], 0)
            self.assertEqual(troop["deployed_needed"], 0)

    def test_exit_code_zero_when_requested_track_meets_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            write_batch(
                data_root,
                "batch-a",
                track="nightmare_sails",
                context_battle_counts={"field": 5},
                rows=[
                    row(
                        context="field",
                        display_name="Nord Huscarl",
                        slug="nord_huscarl",
                        battles=5,
                        deployed=20,
                        canonical_troop_id="nord_huscarl",
                        identity_status="confirmed_id",
                    )
                ],
            )
            exit_code = main(["--data-root", str(data_root), "--track", "nightmare_sails"])
            self.assertEqual(exit_code, 0)

    def test_unrequested_below_gate_track_does_not_affect_requested_track(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            write_batch(
                data_root,
                "batch-a",
                track="nightmare_sails",
                context_battle_counts={"field": 5},
                rows=[
                    row(
                        context="field",
                        display_name="Nord Huscarl",
                        slug="nord_huscarl",
                        battles=5,
                        deployed=20,
                        canonical_troop_id="nord_huscarl",
                        identity_status="confirmed_id",
                    )
                ],
            )
            # realm_of_thrones has zero evidence at all, but was not requested.
            exit_code = main(["--data-root", str(data_root), "--track", "nightmare_sails"])
            self.assertEqual(exit_code, 0)

    def test_cross_batch_aggregation_reaches_gate_only_when_combined(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            write_batch(
                data_root,
                "batch-a",
                track="realm_of_thrones",
                context_battle_counts={"field": 3},
                rows=[
                    row(
                        context="field",
                        display_name="Ravens' Teeth",
                        slug="ravens_teeth",
                        battles=3,
                        deployed=12,
                        canonical_troop_id="ravens_teeth",
                        identity_status="confirmed_id",
                    )
                ],
            )
            write_batch(
                data_root,
                "batch-b",
                track="realm_of_thrones",
                context_battle_counts={"field": 2},
                rows=[
                    row(
                        context="field",
                        display_name="Ravens' Teeth",
                        slug="ravens_teeth",
                        battles=2,
                        deployed=10,
                        canonical_troop_id="ravens_teeth",
                        identity_status="confirmed_id",
                    )
                ],
            )

            report = build_report(data_root, ["realm_of_thrones"])

            field_report = report["tracks"]["realm_of_thrones"]["contexts"]["field"]
            self.assertEqual(field_report["independent_battles_captured"], 5)
            troop = field_report["relationships"]["player_party"]["troops"][0]
            self.assertEqual(troop["independent_battles"], 5)
            self.assertEqual(troop["deployed"], 22)
            self.assertTrue(troop["gate_met"])
            self.assertEqual(len(report["tracks"]["realm_of_thrones"]["batches"]), 2)

    def test_unresolved_identity_still_counts_toward_gate_but_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            write_batch(
                data_root,
                "batch-a",
                track="nightmare_sails",
                context_battle_counts={"field": 5},
                rows=[
                    row(
                        context="field",
                        display_name="Imperial Trained Infantryman",
                        slug="imperial_trained_infantryman",
                        battles=5,
                        deployed=41,
                        canonical_troop_id="",
                        identity_status="unresolved",
                    )
                ],
            )

            report = build_report(data_root, ["nightmare_sails"])

            troop = (
                report["tracks"]["nightmare_sails"]["contexts"]["field"]
                ["relationships"]["player_party"]["troops"][0]
            )
            self.assertTrue(troop["gate_met"])
            self.assertFalse(troop["identity_confirmed"])
            self.assertEqual(troop["canonical_troop_id"], "")


class GateStatusContextSeparationTests(unittest.TestCase):
    def test_field_and_siege_are_never_pooled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            # Same troop, same track: 3 field battles/15 deployed and 3
            # siege_attack battles/15 deployed. Combined that would be 6
            # battles / 30 deployed (over the gate), but AGENTS.md requires
            # field, siege attack, and siege defense to remain separate, so
            # neither context alone may cross the gate.
            write_batch(
                data_root,
                "batch-a",
                track="realm_of_thrones",
                context_battle_counts={"field": 3, "siege_attack": 3},
                rows=[
                    row(
                        context="field",
                        display_name="Ravens' Teeth",
                        slug="ravens_teeth",
                        battles=3,
                        deployed=15,
                        canonical_troop_id="ravens_teeth",
                        identity_status="confirmed_id",
                    ),
                    row(
                        context="siege_attack",
                        display_name="Ravens' Teeth",
                        slug="ravens_teeth",
                        battles=3,
                        deployed=15,
                        canonical_troop_id="ravens_teeth",
                        identity_status="confirmed_id",
                    ),
                ],
            )

            report = build_report(data_root, ["realm_of_thrones"])
            contexts = report["tracks"]["realm_of_thrones"]["contexts"]

            field_troop = contexts["field"]["relationships"]["player_party"]["troops"][0]
            siege_troop = contexts["siege_attack"]["relationships"]["player_party"]["troops"][0]

            self.assertFalse(field_troop["gate_met"])
            self.assertFalse(siege_troop["gate_met"])
            self.assertEqual(field_troop["independent_battles"], 3)
            self.assertEqual(siege_troop["independent_battles"], 3)
            self.assertFalse(report["tracks"]["realm_of_thrones"]["gate_met"])
            # siege_defense was never observed at all in this fixture.
            self.assertEqual(contexts["siege_defense"]["independent_battles_captured"], 0)
            self.assertEqual(contexts["siege_defense"]["relationships"], {})

    def test_siege_attack_alone_can_meet_gate_while_field_stays_below(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            write_batch(
                data_root,
                "batch-a",
                track="realm_of_thrones",
                context_battle_counts={"field": 2, "siege_attack": 5},
                rows=[
                    row(
                        context="field",
                        display_name="Ravens' Teeth",
                        slug="ravens_teeth",
                        battles=2,
                        deployed=9,
                        canonical_troop_id="ravens_teeth",
                        identity_status="confirmed_id",
                    ),
                    row(
                        context="siege_attack",
                        display_name="Ravens' Teeth",
                        slug="ravens_teeth",
                        battles=5,
                        deployed=88,
                        canonical_troop_id="ravens_teeth",
                        identity_status="confirmed_id",
                    ),
                ],
            )

            report = build_report(data_root, ["realm_of_thrones"])
            contexts = report["tracks"]["realm_of_thrones"]["contexts"]

            self.assertFalse(contexts["field"]["gate_met"])
            self.assertTrue(contexts["siege_attack"]["gate_met"])
            # The track as a whole is reported as gate-met because *some*
            # context/troop combination reached the display gate.
            self.assertTrue(report["tracks"]["realm_of_thrones"]["gate_met"])


class GateStatusPlannedScaffoldTests(unittest.TestCase):
    def test_scaffold_with_no_evidence_is_reported_as_planned_not_captured(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            scaffold_dir = data_root / "2026-07-31-rot-field-plan"
            scaffold_dir.mkdir(parents=True)
            (scaffold_dir / "README.md").write_text(
                "# Realm of Thrones field capture plan\n\n"
                "> **Status: NO DATA CAPTURED YET.**\n\n"
                "- Track: `realm_of_thrones`\n",
                encoding="utf-8",
            )

            report = build_report(data_root, ["realm_of_thrones"])

            track_report = report["tracks"]["realm_of_thrones"]
            self.assertFalse(track_report["gate_met"])
            self.assertEqual(track_report["batches"], [])
            self.assertEqual(len(track_report["planned_batches"]), 1)
            self.assertEqual(track_report["planned_batches"][0]["track"], "realm_of_thrones")


class GateStatusMalformedInputTests(unittest.TestCase):
    def test_missing_game_track_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            data_root = Path(tmp)
            batch_dir = data_root / "batch-a"
            (batch_dir / "analysis").mkdir(parents=True)
            (batch_dir / "normalization_summary.json").write_text(
                json.dumps({"battle_context_counts": {"field": 1}}), encoding="utf-8"
            )
            ranking_path = batch_dir / "analysis" / "ranking_complete.csv"
            with ranking_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=RANKING_FIELDS, lineterminator="\n")
                writer.writeheader()

            with self.assertRaises(GateStatusError):
                build_report(data_root, ["realm_of_thrones"])


if __name__ == "__main__":
    unittest.main()
