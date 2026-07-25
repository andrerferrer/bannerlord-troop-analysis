# Platform adapters

- **Accessed:** 2026-07-24
- **Portable standard:** https://agentskills.io/specification
- **OpenAI/Codex:** https://learn.chatgpt.com/docs/build-skills
- **Claude Code:** https://code.claude.com/docs/en/skills
- **Cursor:** https://cursor.com/docs/skills

## Compatibility matrix

| Platform | Verified local version | Discovery paths | Explicit invocation | Attachment/local-path behavior | Scripts | Reload | Validation |
|---|---|---|---|---|---|---|---|
| Codex CLI/IDE | `codex-cli 0.145.0` installed | Project `.agents/skills/`; user `~/.agents/skills/` | `$analyze-bannerlord-combat-zip`; `/skills` lists/selects | Local paths; attachments only when exposed to the workspace | Yes | Auto-detect; restart if absent | Canonical path; static + CLI present |
| ChatGPT desktop Work/Codex | Host not invoked in tests | Supported local project `.agents/skills/`; user `~/.agents/skills/` | `@` skill selector | Use the host-exposed local attachment path; otherwise save locally first | Yes on supported local desktop surfaces | New conversation/restart if absent | OpenAI docs static validation |
| ChatGPT Work web | Not runtime-tested | Standalone local folder is not the install unit | `@` after plugin installation | Web upload behavior is plugin/surface-dependent | Plugin-dependent | New conversation | Adapter required: package as plugin for distribution |
| Claude Code | `2.1.219` installed | Project `.claude/skills/`; user `~/.claude/skills/` | `/analyze-bannerlord-combat-zip` | Local paths; attachments require a local path visible to the session | Yes | Live change detection; restart only when creating a previously absent top-level skills directory | Native adapter dry-run + CLI present |
| Cursor IDE/CLI | IDE `3.12.30`; agent CLI `2026.07.23-e383d2b` installed | Project/user `.agents/skills/` or `.cursor/skills/` | `/analyze-bannerlord-combat-zip` | Local workspace paths; save unsupported attachments locally first | Yes | Normally automatic; reopen if discovery is stale | Native `.cursor` adapter dry-run + CLIs present |

The open Agent Skills specification defines skill contents, not discovery paths. Each host owns its paths and invocation UI.

## Installer

Always preview first:

```bash
python3 scripts/install_adapters.py \
  --target all \
  --scope project \
  --mode symlink \
  --project-root "/path/to/project" \
  --dry-run
```

Apply only with explicit authorization by removing `--dry-run`. The installer refuses to overwrite a different skill and deduplicates Codex/ChatGPT’s shared `.agents/skills` target.

Use `copy` when symlinks are unsuitable. A copy can drift; compare hashes before updating. For Cursor, prefer the native `.cursor/skills` adapter when runtime discovery from `.agents/skills` is inconsistent in a particular release.

No global installation was performed by repository validation.
