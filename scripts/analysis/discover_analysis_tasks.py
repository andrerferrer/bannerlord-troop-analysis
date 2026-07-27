#!/usr/bin/env python3
"""Discover actionable analysis tasks from versioned GitHub PR comments.

Requires an authenticated GitHub CLI (`gh`). The script scans open pull requests,
parses append-only `bannerlord-analysis-task:v1` comments, and reports the latest
valid state for each task_id.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Iterable

MARKER_RE = re.compile(
    r"<!--\s*bannerlord-analysis-task:v(?P<version>\d+)\s*-->", re.IGNORECASE
)
JSON_FENCE_RE = re.compile(r"```json\s*(?P<payload>\{.*?\})\s*```", re.IGNORECASE | re.DOTALL)
PROTOCOL = "bannerlord-analysis-task"
SUPPORTED_VERSION = 1
ALLOWED_STATUSES = {"pending", "in_progress", "blocked", "complete", "cancelled"}
ACTIONABLE_STATUSES = {"pending", "in_progress", "blocked"}


class DiscoveryError(RuntimeError):
    """Raised when GitHub task discovery cannot continue safely."""


@dataclass(frozen=True)
class ParsedTask:
    payload: dict[str, Any]
    created_at: str
    comment_url: str
    comment_id: int | None


def run_gh_json(arguments: list[str]) -> Any:
    command = ["gh", *arguments]
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError as exc:
        raise DiscoveryError("GitHub CLI `gh` was not found in PATH.") from exc

    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "unknown gh error"
        raise DiscoveryError(f"Command failed: {' '.join(command)}\n{stderr}")

    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise DiscoveryError(
            f"Command returned invalid JSON: {' '.join(command)}"
        ) from exc


def detect_repository() -> str:
    payload = run_gh_json(["repo", "view", "--json", "nameWithOwner"])
    repository = payload.get("nameWithOwner") if isinstance(payload, dict) else None
    if not isinstance(repository, str) or "/" not in repository:
        raise DiscoveryError("Could not determine the current GitHub repository.")
    return repository


def flatten_comment_pages(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, list):
        raise DiscoveryError("GitHub comments response was not a list.")

    if not payload:
        return []

    if all(isinstance(item, dict) for item in payload):
        return list(payload)

    comments: list[dict[str, Any]] = []
    for page in payload:
        if not isinstance(page, list):
            raise DiscoveryError("GitHub paginated comments response was malformed.")
        for item in page:
            if isinstance(item, dict):
                comments.append(item)
    return comments


def validate_payload(payload: Any, marker_version: int) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("protocol payload must be a JSON object")
    if payload.get("protocol") != PROTOCOL:
        raise ValueError(f"protocol must equal {PROTOCOL!r}")
    if payload.get("version") != marker_version:
        raise ValueError("payload version does not match marker version")
    if marker_version != SUPPORTED_VERSION:
        raise ValueError(f"unsupported protocol version: {marker_version}")

    required_string_fields = [
        "task_id",
        "status",
        "branch",
        "handoff_path",
        "normalization_commit",
    ]
    for field in required_string_fields:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")

    if payload["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"unsupported status: {payload['status']!r}")

    required_actions = payload.get("required_actions")
    if not isinstance(required_actions, list) or not all(
        isinstance(action, str) and action.strip() for action in required_actions
    ):
        raise ValueError("required_actions must be a list of non-empty strings")

    completion = payload.get("completion")
    if not isinstance(completion, dict):
        raise ValueError("completion must be an object")
    if completion.get("action") not in {"merge", "close", "none"}:
        raise ValueError("completion.action must be merge, close, or none")
    if completion.get("action") == "merge" and completion.get("merge_method") not in {
        "squash",
        "merge",
        "rebase",
    }:
        raise ValueError("completion.merge_method must be squash, merge, or rebase")

    blockers = payload.get("blockers")
    if not isinstance(blockers, list) or not all(isinstance(item, str) for item in blockers):
        raise ValueError("blockers must be a list of strings")
    if payload["status"] == "blocked" and not blockers:
        raise ValueError("blocked tasks must include at least one blocker")

    return payload


def parse_protocol_comment(comment: dict[str, Any]) -> ParsedTask | None:
    body = comment.get("body")
    if not isinstance(body, str):
        return None

    marker = MARKER_RE.search(body)
    if marker is None:
        return None

    marker_version = int(marker.group("version"))
    fence = JSON_FENCE_RE.search(body, marker.end())
    if fence is None:
        raise ValueError("marker is not followed by a fenced JSON payload")

    try:
        raw_payload = json.loads(fence.group("payload"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON payload: {exc.msg}") from exc

    payload = validate_payload(raw_payload, marker_version)
    created_at = comment.get("created_at")
    if not isinstance(created_at, str) or not created_at:
        raise ValueError("comment is missing created_at")

    comment_url = comment.get("html_url")
    if not isinstance(comment_url, str):
        comment_url = ""

    comment_id = comment.get("id")
    if not isinstance(comment_id, int):
        comment_id = None

    return ParsedTask(
        payload=payload,
        created_at=created_at,
        comment_url=comment_url,
        comment_id=comment_id,
    )


def discover_tasks(repository: str) -> tuple[list[dict[str, Any]], list[str]]:
    prs = run_gh_json(
        [
            "pr",
            "list",
            "--repo",
            repository,
            "--state",
            "open",
            "--limit",
            "500",
            "--json",
            "number,title,url,headRefName,isDraft",
        ]
    )
    if not isinstance(prs, list):
        raise DiscoveryError("GitHub PR response was not a list.")

    discovered: list[dict[str, Any]] = []
    warnings: list[str] = []

    for pr in prs:
        if not isinstance(pr, dict) or not isinstance(pr.get("number"), int):
            continue

        pr_number = pr["number"]
        pages = run_gh_json(
            [
                "api",
                "--paginate",
                "--slurp",
                f"repos/{repository}/issues/{pr_number}/comments",
            ]
        )
        comments = flatten_comment_pages(pages)
        latest_by_task: dict[str, ParsedTask] = {}

        for comment in comments:
            try:
                parsed = parse_protocol_comment(comment)
            except ValueError as exc:
                comment_url = comment.get("html_url", "unknown comment")
                warnings.append(f"PR #{pr_number}: ignored invalid protocol comment {comment_url}: {exc}")
                continue

            if parsed is None:
                continue

            task_id = parsed.payload["task_id"]
            previous = latest_by_task.get(task_id)
            if previous is None or parsed.created_at > previous.created_at:
                latest_by_task[task_id] = parsed

        for parsed in latest_by_task.values():
            payload = parsed.payload
            branch_matches = payload["branch"] == pr.get("headRefName")
            if not branch_matches:
                warnings.append(
                    f"PR #{pr_number} task {payload['task_id']}: comment branch "
                    f"{payload['branch']!r} differs from PR head {pr.get('headRefName')!r}."
                )

            discovered.append(
                {
                    "repository": repository,
                    "pr_number": pr_number,
                    "pr_title": pr.get("title", ""),
                    "pr_url": pr.get("url", ""),
                    "pr_is_draft": bool(pr.get("isDraft")),
                    "pr_head_branch": pr.get("headRefName", ""),
                    "branch_matches_pr": branch_matches,
                    "comment_created_at": parsed.created_at,
                    "comment_url": parsed.comment_url,
                    "comment_id": parsed.comment_id,
                    "task": payload,
                }
            )

    discovered.sort(key=lambda item: (item["pr_number"], item["task"]["task_id"]))
    return discovered, warnings


def render_human(tasks: Iterable[dict[str, Any]]) -> str:
    lines: list[str] = []
    for item in tasks:
        task = item["task"]
        blockers = task.get("blockers") or []
        lines.extend(
            [
                f"PR #{item['pr_number']} [{task['status']}] {item['pr_title']}",
                f"  URL: {item['pr_url']}",
                f"  Task: {task['task_id']}",
                f"  Branch: {task['branch']}",
                f"  Handoff: {task['handoff_path']}",
                f"  Normalization commit: {task['normalization_commit']}",
                f"  Branch matches PR: {'yes' if item['branch_matches_pr'] else 'NO'}",
            ]
        )
        if blockers:
            lines.append("  Blockers:")
            lines.extend(f"    - {blocker}" for blocker in blockers)
        lines.append("")

    if not lines:
        return "No actionable analysis tasks found."
    return "\n".join(lines).rstrip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover versioned analysis tasks in open GitHub PR comments."
    )
    parser.add_argument(
        "--repo",
        help="Repository in owner/name form. Defaults to the current gh repository.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON instead of a human summary.",
    )
    parser.add_argument(
        "--all-statuses",
        action="store_true",
        help="Include complete and cancelled tasks in addition to actionable states.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    try:
        repository = args.repo or detect_repository()
        tasks, warnings = discover_tasks(repository)
    except DiscoveryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)

    selected = tasks
    if not args.all_statuses:
        selected = [task for task in tasks if task["task"]["status"] in ACTIONABLE_STATUSES]

    if args.json:
        print(
            json.dumps(
                {
                    "protocol": PROTOCOL,
                    "supported_version": SUPPORTED_VERSION,
                    "repository": repository,
                    "actionable_count": sum(
                        task["task"]["status"] in ACTIONABLE_STATUSES for task in tasks
                    ),
                    "tasks": selected,
                    "warnings": warnings,
                },
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    else:
        print(render_human(selected))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
