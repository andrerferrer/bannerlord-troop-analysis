#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path


SKILL_NAME = "analyze-bannerlord-combat-zip"


class InstallError(RuntimeError):
    pass


def tree_hash(root: Path) -> str:
    digest = hashlib.sha256()
    if root.is_symlink():
        root = root.resolve()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def target_roots(platform: str, scope: str, project_root: Path, user_root: Path) -> list[Path]:
    platforms = ("codex", "chatgpt", "claude", "cursor") if platform == "all" else (platform,)
    paths = []
    for item in platforms:
        if scope == "project":
            base = {
                "codex": project_root / ".agents/skills",
                "chatgpt": project_root / ".agents/skills",
                "claude": project_root / ".claude/skills",
                "cursor": project_root / ".cursor/skills",
            }[item]
        else:
            base = {
                "codex": user_root / ".agents/skills",
                "chatgpt": user_root / ".agents/skills",
                "claude": user_root / ".claude/skills",
                "cursor": user_root / ".cursor/skills",
            }[item]
        if base not in paths:
            paths.append(base)
    return paths


def install(source: Path, destination: Path, mode: str, dry_run: bool) -> str:
    target = destination / SKILL_NAME
    if target.resolve() == source.resolve():
        return f"already canonical: {target}"
    if target.exists() or target.is_symlink():
        try:
            same = tree_hash(target) == tree_hash(source)
        except (OSError, RuntimeError):
            same = False
        if same:
            return f"already current: {target}"
        raise InstallError(f"refusing to overwrite a different installed skill: {target}")
    action = f"{mode} {source} -> {target}"
    if dry_run:
        return f"dry-run: {action}"
    destination.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        target.symlink_to(source, target_is_directory=True)
    else:
        temporary = Path(tempfile.mkdtemp(prefix=f".{SKILL_NAME}.", dir=destination))
        shutil.rmtree(temporary)
        shutil.copytree(source, temporary)
        os.replace(temporary, target)
    return action


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--target", choices=("codex", "chatgpt", "claude", "cursor", "all"), required=True)
    value.add_argument("--scope", choices=("project", "user"), required=True)
    value.add_argument("--mode", choices=("symlink", "copy"), required=True)
    value.add_argument("--project-root", type=Path, default=Path.cwd())
    value.add_argument("--user-root", type=Path, default=Path.home())
    value.add_argument("--dry-run", action="store_true")
    return value


def main() -> int:
    args = parser().parse_args()
    source = Path(__file__).resolve().parents[1]
    if not (source / "SKILL.md").is_file():
        raise InstallError(f"canonical skill source is invalid: {source}")
    roots = target_roots(
        args.target,
        args.scope,
        args.project_root.resolve(),
        args.user_root.resolve(),
    )
    for root in roots:
        print(install(source, root, args.mode, args.dry_run))
    print("Rollback: remove only the exact adapter path printed above after verifying it targets this skill.")
    print("Reload: start a new host conversation if the skill does not appear automatically.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except InstallError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(2)
