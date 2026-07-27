from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "analysis" / "discover_analysis_tasks.py"
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


def protocol_comment(payload, *, created_at="2026-07-27T18:00:00Z", comment_id=1):
    return {
        "id": comment_id,
        "created_at": created_at,
        "html_url": f"https://example.invalid/comments/{comment_id}",
        "body": (
            "<!-- bannerlord-analysis-task:v1 -->\n"
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

    def test_ignores_unmarked_comments(self):
        parsed = MODULE.parse_protocol_comment(
            {"id": 2, "created_at": "2026-07-27T18:01:00Z", "body": "ordinary comment"}
        )
        self.assertIsNone(parsed)

    def test_blocked_state_requires_blocker(self):
        with self.assertRaisesRegex(ValueError, "blocked tasks must include"):
            MODULE.parse_protocol_comment(protocol_comment(valid_payload(status="blocked")))

    def test_marker_and_payload_versions_must_match(self):
        with self.assertRaisesRegex(ValueError, "version does not match"):
            MODULE.parse_protocol_comment(protocol_comment(valid_payload(version=2)))

    def test_flattens_paginated_comment_pages(self):
        flattened = MODULE.flatten_comment_pages([[{"id": 1}], [{"id": 2}]])
        self.assertEqual([item["id"] for item in flattened], [1, 2])


if __name__ == "__main__":
    unittest.main()
