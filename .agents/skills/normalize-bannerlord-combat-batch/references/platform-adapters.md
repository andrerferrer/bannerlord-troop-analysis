# Phase 1 platform boundary

Repository publication requires a local checkout capable of running `validate_phase1_handoff.py` plus authenticated GitHub write access.

- Codex, Claude Code, and Cursor may normalize and publish when the checkout and validator are available.
- A connector-only ChatGPT host may help extract or prepare artifacts, but it must not publish a `pending` analysis task without confirmed executable repository validation.
- A host without GitHub write access may leave a validated local branch/commit and report the exact blocked write step.

Explicit invocations are `$normalize-bannerlord-combat-batch`, `/normalize-bannerlord-combat-batch`, or the host's skill selector.

Preview project adapter installation with:

```bash
python3 scripts/install_adapters.py \
  --target all \
  --scope project \
  --mode symlink \
  --project-root "/path/to/project" \
  --dry-run
```

Remove `--dry-run` only with authorization for the target directories.
