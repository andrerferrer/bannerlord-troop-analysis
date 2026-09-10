#!/usr/bin/env python3
"""Discover actionable Bannerlord repository tasks from versioned PR comments.

Requires an authenticated GitHub CLI (`gh`). The script scans open pull requests,
parses append-only analysis and historical-consolidation task comments, and
reports the latest valid state for each protocol/task_id pair.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Iterable

ANALYSIS_PROTOCOL = "bannerlord-analysis-task"
CONSOLIDATION_PROTOCOL = "bannerlord-consolidation-task"
PROTOCOL = ANALYSIS_PROTOCOL  # Backward-compatible exported constant.
SUPPORTED_VERSION = 1
SUPPORTED_PROTOCOLS = {
    ANALYSIS_PROTOCOL: SUPPORTED_VERSION,
    CONSOLIDATION_PROTOCOL: SUPPORTED_VERSION,
}
MARKER_RE = re.compile(
    r"<!--\s*(?P<protocol>bannerlord-(?:analysis|consolidation)-task):"
    r"v(?P<version>\d+)\s*-->",
    re.IGNORECASE,
)
JSON_FENCE_RE = re.compile(
    r"```json\s*(?P<payload>\{.*?\})\s*```",
    re.IGNORECASE | re.DOTALL,
)
ALLOWED_STATUSES = {"pending", "in_progress", "blocked", "complete", "cancelled"}
ACTIONABLE_STATUSES = {"pending", "in_progress", "blocked"}
TRUSTED_AUTHOR_ASSOCIATIONS = frozenset({"OWNER", "MEMBER", "COLLABORATOR"})
PATH_FIELD_TOKENS = frozenset(
    {
        "artifact",
        "artifacts",
        "dir",
        "dirs",
        "directory",
        "directories",
        "file",
        "files",
        "part",
        "parts",
        "path",
        "paths",
    }
)
ALLOWED_TRANSITIONS = {
    "pending": frozenset({"in_progress", "blocked", "cancelled"}),
    "in_progress": frozenset({"complete", "blocked", "cancelled"}),
    "blocked": frozenset({"in_progress", "cancelled"}),
    "complete": frozenset(),
    "cancelled": frozenset(),
}


class DiscoveryError(RuntimeError):
    """Raised when GitHub task discovery cannot continue safely."""


@dataclass(frozen=True)
class ParsedTask:
    payload: dict[str, Any]
    created_at: str
    comment_url: str
    comment_id: int


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


def _require_non_empty_strings(payload: dict[str, Any], fields: list[str]) -> None:
    for field in fields:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")


def _require_repository_relative_path(value: Any, field: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty repository-relative path")

    path = PurePosixPath(value)
    has_windows_drive = len(value) >= 2 and value[0].isalpha() and value[1] == ":"
    has_unsafe_component = any(part in {"", ".", ".."} for part in value.split("/"))
    has_control_character = any(
        ord(character) < 32 or ord(character) == 127
        for character in value
    )
    if (
        path.is_absolute()
        or value.startswith("~")
        or value != value.strip()
        or has_windows_drive
        or "\\" in value
        or has_unsafe_component
        or has_control_character
        or path.as_posix() != value
    ):
        raise ValueError(f"{field} must be a normalized repository-relative path")


def _validate_repository_paths(payload: dict[str, Any], primary_field: str) -> None:
    _require_repository_relative_path(payload.get(primary_field), primary_field)

    def is_path_field(key: str) -> bool:
        return re.split(r"[_-]+", key.casefold())[-1] in PATH_FIELD_TOKENS

    def validate_path_value(value: Any, field: str) -> None:
        if isinstance(value, str):
            _require_repository_relative_path(value, field)
        elif isinstance(value, list):
            for index, nested_value in enumerate(value):
                nested_field = f"{field}[{index}]"
                if isinstance(nested_value, (str, list, dict)):
                    validate_path_value(nested_value, nested_field)
        elif isinstance(value, dict):
            for key, nested_value in value.items():
                nested_field = f"{field}.{key}"
                _require_repository_relative_path(key, f"{field}.<key>")
                if isinstance(nested_value, (str, list, dict)):
                    validate_path_value(nested_value, nested_field)
        else:
            raise ValueError(f"{field} must contain repository-relative paths")

    def visit(value: Any, field: str) -> None:
        if isinstance(value, dict):
            for key, nested_value in value.items():
                nested_field = f"{field}.{key}" if field else key
                if is_path_field(key) and isinstance(
                    nested_value,
                    (str, list, dict),
                ):
                    validate_path_value(nested_value, nested_field)
                else:
                    visit(nested_value, nested_field)
        elif isinstance(value, list):
            for index, nested_value in enumerate(value):
                visit(nested_value, f"{field}[{index}]")

    visit(payload, "")


def validate_payload(
    payload: Any,
    marker_version: int,
    marker_protocol: str = ANALYSIS_PROTOCOL,
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("protocol payload must be a JSON object")

    normalized_protocol = marker_protocol.casefold()
    supported_version = SUPPORTED_PROTOCOLS.get(normalized_protocol)
    if supported_version is None:
        raise ValueError(f"unsupported protocol marker: {marker_protocol!r}")
    if payload.get("protocol") != normalized_protocol:
        raise ValueError(f"protocol must equal {normalized_protocol!r}")
    if payload.get("version") != marker_version:
        raise ValueError("payload version does not match marker version")
    if marker_version != supported_version:
        raise ValueError(
            f"unsupported {normalized_protocol} version: {marker_version}"
        )

    _require_non_empty_strings(payload, ["task_id", "status", "branch"])
    if payload["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"unsupported status: {payload['status']!r}")

    if normalized_protocol == ANALYSIS_PROTOCOL:
        _require_non_empty_strings(
            payload,
            ["handoff_path", "normalization_commit"],
        )
        _validate_repository_paths(payload, "handoff_path")
    else:
        _require_non_empty_strings(
            payload,
            ["workflow", "consolidation_path"],
        )
        _validate_repository_paths(payload, "consolidation_path")
        if payload["workflow"] != "historical_consolidation":
            raise ValueError(
                "consolidation workflow must equal 'historical_consolidation'"
            )

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
    if not isinstance(blockers, list) or not all(
        isinstance(item, str) for item in blockers
    ):
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

    author_association = comment.get("author_association")
    if (
        not isinstance(author_association, str)
        or author_association.upper() not in TRUSTED_AUTHOR_ASSOCIATIONS
    ):
        raise ValueError(
            f"untrusted author association: {author_association!r}"
        )

    marker_protocol = marker.group("protocol").casefold()
    marker_version = int(marker.group("version"))
    fence = JSON_FENCE_RE.search(body, marker.end())
    if fence is None:
        raise ValueError("marker is not followed by a fenced JSON payload")

    try:
        raw_payload = json.loads(fence.group("payload"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON payload: {exc.msg}") from exc

    payload = validate_payload(
        raw_payload,
        marker_version,
        marker_protocol=marker_protocol,
    )
    created_at = comment.get("created_at")
    if not isinstance(created_at, str) or not created_at:
        raise ValueError("comment is missing created_at")

    updated_at = comment.get("updated_at")
    if not isinstance(updated_at, str) or not updated_at:
        raise ValueError("comment is missing updated_at")
    if updated_at != created_at:
        raise ValueError("edited protocol comments are not authoritative")

    comment_url = comment.get("html_url")
    if not isinstance(comment_url, str):
        comment_url = ""

    comment_id = comment.get("id")
    if type(comment_id) is not int:
        raise ValueError("comment is missing integer id")

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
        transitions_by_task: dict[tuple[str, str], list[ParsedTask]] = {}

        for comment in comments:
            try:
                parsed = parse_protocol_comment(comment)
            except ValueError as exc:
                comment_url = comment.get("html_url", "unknown comment")
                warnings.append(
                    f"PR #{pr_number}: ignored invalid protocol comment "
                    f"{comment_url}: {exc}"
                )
                continue

            if parsed is None:
                continue

            task_key = (
                parsed.payload["protocol"],
                parsed.payload["task_id"],
            )
            transitions_by_task.setdefault(task_key, []).append(parsed)

        latest_by_task: dict[tuple[str, str], ParsedTask] = {}
        for task_key, transitions in transitions_by_task.items():
            previous: ParsedTask | None = None
            for parsed in sorted(
                transitions,
                key=lambda item: (item.created_at, item.comment_id),
            ):
                status = parsed.payload["status"]
                if previous is None:
                    if status != "pending":
                        warnings.append(
                            f"PR #{pr_number} task {task_key[1]}: ignored invalid "
                            f"initial status {status!r} in {parsed.comment_url}; "
                            "expected 'pending'."
                        )
                        continue
                else:
                    previous_status = previous.payload["status"]
                    if status not in ALLOWED_TRANSITIONS[previous_status]:
                        warnings.append(
                            f"PR #{pr_number} task {task_key[1]}: ignored invalid "
                            f"state transition {previous_status!r} -> {status!r} "
                            f"in {parsed.comment_url}."
                        )
                        continue

                previous = parsed

            if previous is not None:
                latest_by_task[task_key] = previous

        for parsed in latest_by_task.values():
            payload = parsed.payload
            branch_matches = payload["branch"] == pr.get("headRefName")
            if not branch_matches:
                warnings.append(
                    f"PR #{pr_number} task {payload['task_id']}: comment branch "
                    f"{payload['branch']!r} differs from PR head "
                    f"{pr.get('headRefName')!r}."
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
                    "task_protocol": payload["protocol"],
                    "task_kind": (
                        "analysis"
                        if payload["protocol"] == ANALYSIS_PROTOCOL
                        else "historical_consolidation"
                    ),
                    "task": payload,
                }
            )

    discovered.sort(
        key=lambda item: (
            item["pr_number"],
            item["task_protocol"],
            item["task"]["task_id"],
        )
    )
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
                f"  Protocol: {item['task_protocol']}",
                f"  Task: {task['task_id']}",
                f"  Branch: {task['branch']}",
                f"  Branch matches PR: {'yes' if item['branch_matches_pr'] else 'NO'}",
            ]
        )
        if item["task_kind"] == "analysis":
            lines.extend(
                [
                    f"  Handoff: {task['handoff_path']}",
                    f"  Normalization commit: {task['normalization_commit']}",
                ]
            )
        else:
            lines.extend(
                [
                    f"  Workflow: {task['workflow']}",
                    f"  Consolidation: {task['consolidation_path']}",
                ]
            )
        if blockers:
            lines.append("  Blockers:")
            lines.extend(f"    - {blocker}" for blocker in blockers)
        lines.append("")

    if not lines:
        return "No actionable Bannerlord tasks found."
    return "\n".join(lines).rstrip()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Discover versioned analysis and historical-consolidation tasks "
            "in open GitHub PR comments."
        )
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
        selected = [
            task
            for task in tasks
            if task["task"]["status"] in ACTIONABLE_STATUSES
        ]

    if args.json:
        print(
            json.dumps(
                {
                    "protocol": PROTOCOL,
                    "supported_version": SUPPORTED_VERSION,
                    "supported_protocols": SUPPORTED_PROTOCOLS,
                    "repository": repository,
                    "actionable_count": sum(
                        task["task"]["status"] in ACTIONABLE_STATUSES
                        for task in tasks
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
