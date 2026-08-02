# Phase 2 platform boundary

Use this skill only on a host that can access the repository checkout, run its validation commands, and update the existing analysis-task pull request.

- Codex, Claude Code, and Cursor may run the local analysis queue from the repository checkout.
- A connector-only host without local repository execution cannot complete Phase 2 validation; publish no completion claim from that host.
- Raw screenshot attachments belong to `$normalize-bannerlord-combat-batch`, not this skill.

Project discovery paths follow the Agent Skills standard (`.agents/skills/` and host-specific adapters). The explicit invocations are `$analyze-bannerlord-combat-zip`, `/analyze-bannerlord-combat-zip`, or the host's skill selector.

Preview project adapter installation with `python3 scripts/install_adapters.py --target all --scope project --mode symlink --project-root /path/to/project --dry-run`. Remove `--dry-run` only with authorization for the target directories.
