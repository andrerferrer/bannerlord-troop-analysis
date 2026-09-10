from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "analysis"
    / "discover_analysis_tasks.py"
)
SPEC = importlib.util.spec_from_file_location("discover_analysis_tasks", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def valid_payload(**overrides):
    payload = {
        "protocol": "bannerlord-analysis-task",
        "version": 1,
        "task_id": "batch-1",
        "status": "pending",
        "branch": "agent/batch-1",
        "handoff_path": "data/batch-1/handoff/ANALYSIS_PROMPT.md",
        "normalization_commit": "a" * 40,
        "required_actions": ["verify_handoff_hashes", "validate_and_merge"],
        "completion": {"action": "merge", "merge_method": "squash"},
        "blockers": [],
    }
    payload.update(overrides)
    return payload


def valid_consolidation_payload(**overrides):
    payload = {
        "protocol": "bannerlord-consolidation-task",
        "version": 1,
        "task_id": "realm-paladin-consolidation",
        "status": "blocked",
        "branch": "data/consolidate-realm-paladin",
        "workflow": "historical_consolidation",
        "consolidation_path": (
            "data/combat_observations/consolidations/"
            "realm-paladin/CONSOLIDATION_TASK.md"
        ),
        "required_actions": [
            "verify_pinned_source",
            "audit_history",
            "validate_latest_head",
        ],
        "completion": {"action": "merge", "merge_method": "squash"},
        "blockers": ["Missing historical evidence has not been located."],
    }
    payload.update(overrides)
    return payload


def protocol_comment(
    payload,
    *,
    created_at="2026-07-27T18:00:00Z",
    updated_at=None,
    comment_id=1,
    author_association="OWNER",
    marker_protocol=None,
    marker_version=1,
):
    protocol = marker_protocol or payload["protocol"]
    return {
        "id": comment_id,
        "created_at": created_at,
        "updated_at": updated_at or created_at,
        "html_url": f"https://example.invalid/comments/{comment_id}",
        "author_association": author_association,
        "body": (
            f"<!-- {protocol}:v{marker_version} -->\n"
            "```json\n"
            f"{json.dumps(payload, indent=2)}\n"
            "```"
        ),
    }


class AnalysisTaskProtocolTests(unittest.TestCase):
    def test_parses_valid_pending_comment(self):
        parsed = MODULE.parse_protocol_comment(protocol_comment(valid_payload()))
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed.payload["task_id"], "batch-1")
        self.assertEqual(parsed.payload["status"], "pending")
        self.assertEqual(parsed.payload["protocol"], MODULE.ANALYSIS_PROTOCOL)

    def test_parses_valid_historical_consolidation_comment(self):
        parsed = MODULE.parse_protocol_comment(
            protocol_comment(valid_consolidation_payload())
        )
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(
            parsed.payload["protocol"],
            MODULE.CONSOLIDATION_PROTOCOL,
        )
        self.assertEqual(
            parsed.payload["workflow"],
            "historical_consolidation",
        )

    def test_consolidation_requires_consolidation_path(self):
        payload = valid_consolidation_payload()
        payload.pop("consolidation_path")
        with self.assertRaisesRegex(
            ValueError,
            "consolidation_path must be a non-empty string",
        ):
            MODULE.parse_protocol_comment(protocol_comment(payload))

    def test_consolidation_rejects_wrong_workflow(self):
        with self.assertRaisesRegex(
            ValueError,
            "historical_consolidation",
        ):
            MODULE.parse_protocol_comment(
                protocol_comment(
                    valid_consolidation_payload(workflow="new_evidence_batch")
                )
            )

    def test_rejects_protocol_comment_from_untrusted_author(self):
        for author_association in ("NONE", "CONTRIBUTOR"):
            with self.subTest(author_association=author_association):
                with self.assertRaisesRegex(
                    ValueError,
                    "untrusted author association",
                ):
                    MODULE.parse_protocol_comment(
                        protocol_comment(
                            valid_consolidation_payload(),
                            author_association=author_association,
                        )
                    )

    def test_accepts_protocol_comment_from_trusted_author(self):
        for author_association in ("OWNER", "MEMBER", "COLLABORATOR"):
            with self.subTest(author_association=author_association):
                parsed = MODULE.parse_protocol_comment(
                    protocol_comment(
                        valid_consolidation_payload(),
                        author_association=author_association,
                    )
                )
                self.assertIsNotNone(parsed)

    def test_rejects_repository_path_escape(self):
        unsafe_paths = (
            "../../outside.md",
            "/tmp/outside.md",
            "C:/outside.md",
            "data\\outside.md",
            "data//outside.md",
        )
        for unsafe_path in unsafe_paths:
            with self.subTest(unsafe_path=unsafe_path):
                with self.assertRaisesRegex(
                    ValueError,
                    "repository-relative path",
                ):
                    MODULE.parse_protocol_comment(
                        protocol_comment(
                            valid_consolidation_payload(
                                consolidation_path=unsafe_path
                            )
                        )
                    )

    def test_rejects_optional_repository_path_escape(self):
        with self.assertRaisesRegex(ValueError, "repository-relative path"):
            MODULE.parse_protocol_comment(
                protocol_comment(
                    valid_consolidation_payload(queue_path="/tmp/queue.json")
                )
            )

    def test_rejects_nested_repository_path_escape(self):
        payload = valid_consolidation_payload()
        payload["recovered_source_identity"] = {
            "path": "../../outside.csv",
        }
        with self.assertRaisesRegex(ValueError, "repository-relative path"):
            MODULE.parse_protocol_comment(protocol_comment(payload))

    def test_rejects_path_collection_and_file_key_escapes(self):
        unsafe_metadata = (
            {"source_paths": ["../../outside.csv"]},
            {"evidence_files": ["/tmp/secret"]},
            {"archive_parts": ["C:/secret.part"]},
            {"source_identity": {"file": "../outside.csv"}},
        )
        for metadata in unsafe_metadata:
            with self.subTest(metadata=metadata):
                payload = valid_consolidation_payload()
                payload.update(metadata)
                with self.assertRaisesRegex(ValueError, "repository-relative path"):
                    MODULE.parse_protocol_comment(protocol_comment(payload))

        payload = valid_consolidation_payload(archive_input_files=19)
        self.assertIsNotNone(
            MODULE.parse_protocol_comment(protocol_comment(payload))
        )

    def test_rejects_edited_protocol_comment(self):
        with self.assertRaisesRegex(ValueError, "edited protocol comments"):
            MODULE.parse_protocol_comment(
                protocol_comment(
                    valid_payload(),
                    created_at="2026-09-10T12:00:00Z",
                    updated_at="2026-09-10T12:05:00Z",
                )
            )

    def test_rejects_analysis_handoff_path_escape(self):
        with self.assertRaisesRegex(ValueError, "repository-relative path"):
            MODULE.parse_protocol_comment(
                protocol_comment(valid_payload(handoff_path="../handoff.md"))
            )

    def test_marker_protocol_must_match_payload_protocol(self):
        with self.assertRaisesRegex(ValueError, "protocol must equal"):
            MODULE.parse_protocol_comment(
                protocol_comment(
                    valid_consolidation_payload(),
                    marker_protocol=MODULE.ANALYSIS_PROTOCOL,
                )
            )

    def test_render_human_supports_consolidation_task(self):
        payload = valid_consolidation_payload()
        output = MODULE.render_human(
            [
                {
                    "pr_number": 95,
                    "pr_title": "Consolidate Realm Paladin",
                    "pr_url": "https://example.invalid/pull/95",
                    "branch_matches_pr": True,
                    "task_protocol": MODULE.CONSOLIDATION_PROTOCOL,
                    "task_kind": "historical_consolidation",
                    "task": payload,
                }
            ]
        )
        self.assertIn("bannerlord-consolidation-task", output)
        self.assertIn(payload["consolidation_path"], output)
        self.assertNotIn("Normalization commit", output)

    def test_discovers_consolidation_comment_from_open_pr(self):
        payload = valid_consolidation_payload(status="pending", blockers=[])
        comment = protocol_comment(payload, comment_id=95)
        original = MODULE.run_gh_json

        def fake_run_gh_json(arguments):
            if arguments[:2] == ["pr", "list"]:
                return [
                    {
                        "number": 95,
                        "title": "Consolidate Realm Paladin",
                        "url": "https://example.invalid/pull/95",
                        "headRefName": "data/consolidate-realm-paladin",
                        "isDraft": True,
                    }
                ]
            return [[comment]]

        MODULE.run_gh_json = fake_run_gh_json
        try:
            tasks, warnings = MODULE.discover_tasks(
                "andrerferrer/bannerlord-troop-analysis"
            )
        finally:
            MODULE.run_gh_json = original

        self.assertEqual(warnings, [])
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["task_kind"], "historical_consolidation")
        self.assertTrue(tasks[0]["branch_matches_pr"])
        self.assertEqual(tasks[0]["task"]["status"], "pending")

    def test_latest_same_second_transition_uses_highest_comment_id(self):
        pending = protocol_comment(
            valid_consolidation_payload(status="pending", blockers=[]),
            created_at="2026-09-10T11:59:59Z",
            comment_id=99,
        )
        older = protocol_comment(
            valid_consolidation_payload(status="in_progress", blockers=[]),
            created_at="2026-09-10T12:00:00Z",
            comment_id=100,
        )
        newer = protocol_comment(
            valid_consolidation_payload(status="complete", blockers=[]),
            created_at="2026-09-10T12:00:00Z",
            comment_id=101,
        )
        original = MODULE.run_gh_json

        for comments in ([pending, older, newer], [newer, pending, older]):
            with self.subTest(comment_ids=[comment["id"] for comment in comments]):
                def fake_run_gh_json(arguments):
                    if arguments[:2] == ["pr", "list"]:
                        return [
                            {
                                "number": 95,
                                "title": "Consolidate Realm Paladin",
                                "url": "https://example.invalid/pull/95",
                                "headRefName": "data/consolidate-realm-paladin",
                                "isDraft": True,
                            }
                        ]
                    return [comments]

                MODULE.run_gh_json = fake_run_gh_json
                try:
                    tasks, warnings = MODULE.discover_tasks(
                        "andrerferrer/bannerlord-troop-analysis"
                    )
                finally:
                    MODULE.run_gh_json = original

                self.assertEqual(warnings, [])
                self.assertEqual(tasks[0]["comment_id"], 101)
                self.assertEqual(tasks[0]["task"]["status"], "complete")

    def test_invalid_state_transitions_do_not_replace_last_valid_state(self):
        pending = protocol_comment(
            valid_consolidation_payload(status="pending", blockers=[]),
            created_at="2026-09-10T12:00:00Z",
            comment_id=100,
        )
        in_progress = protocol_comment(
            valid_consolidation_payload(status="in_progress", blockers=[]),
            created_at="2026-09-10T12:01:00Z",
            comment_id=101,
        )
        complete = protocol_comment(
            valid_consolidation_payload(status="complete", blockers=[]),
            created_at="2026-09-10T12:02:00Z",
            comment_id=102,
        )
        revived = protocol_comment(
            valid_consolidation_payload(status="pending", blockers=[]),
            created_at="2026-09-10T12:03:00Z",
            comment_id=103,
        )
        original = MODULE.run_gh_json

        def fake_run_gh_json(arguments):
            if arguments[:2] == ["pr", "list"]:
                return [
                    {
                        "number": 95,
                        "title": "Consolidate Realm Paladin",
                        "url": "https://example.invalid/pull/95",
                        "headRefName": "data/consolidate-realm-paladin",
                        "isDraft": True,
                    }
                ]
            return [[revived, complete, pending, in_progress]]

        MODULE.run_gh_json = fake_run_gh_json
        try:
            tasks, warnings = MODULE.discover_tasks(
                "andrerferrer/bannerlord-troop-analysis"
            )
        finally:
            MODULE.run_gh_json = original

        self.assertEqual(tasks[0]["comment_id"], 102)
        self.assertEqual(tasks[0]["task"]["status"], "complete")
        self.assertTrue(any("complete' -> 'pending" in warning for warning in warnings))

    def test_ignores_unmarked_comments(self):
        parsed = MODULE.parse_protocol_comment(
            {
                "id": 2,
                "created_at": "2026-07-27T18:01:00Z",
                "body": "ordinary comment",
            }
        )
        self.assertIsNone(parsed)

    def test_blocked_state_requires_blocker(self):
        with self.assertRaisesRegex(ValueError, "blocked tasks must include"):
            MODULE.parse_protocol_comment(
                protocol_comment(valid_payload(status="blocked"))
            )

    def test_marker_and_payload_versions_must_match(self):
        with self.assertRaisesRegex(ValueError, "version does not match"):
            MODULE.parse_protocol_comment(
                protocol_comment(valid_payload(version=2))
            )

    def test_flattens_paginated_comment_pages(self):
        flattened = MODULE.flatten_comment_pages([[{"id": 1}], [{"id": 2}]])
        self.assertEqual([item["id"] for item in flattened], [1, 2])


if __name__ == "__main__":
    unittest.main()
