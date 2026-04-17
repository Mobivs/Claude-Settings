---
name: Claude settings sync topology
description: ~/.claude is git-synced at Mobivs/Claude-Settings with SessionStart/Stop hooks auto-running sync.sh; scope is 7 paths; C:\dev junctions normalize project paths across machines
type: reference
originSessionId: c44629ec-e370-47cd-82dc-3ae01563e66a
---
**Repo**: `~/.claude/` ↔ `github.com/Mobivs/Claude-Settings` (branch `main`).

**Auto-sync hooks** (in `~/.claude/settings.json`, global):
- `SessionStart` → `bash $HOME/.claude/scripts/sync.sh --pull`
- `Stop` → `bash $HOME/.claude/scripts/sync.sh` (full pull+commit+push)

**sync.sh scope** (simplified 2026-04-17):
Stages ONLY these paths: `skills/ agents/ templates/ scripts/ projects/ .gitignore README.md`. Everything else (settings.json, plugins/*, caches, session transcripts) requires manual `git add`.

**Memory folder naming**: `~/.claude/projects/<sanitized-cwd>/memory/`. `<sanitized-cwd>` replaces `\` with `-`, so `C:\Users\svickrey\ThermalInspector` → `c--Users-svickrey-ThermalInspector`.

**Cross-machine memory sharing** requires identical CWD paths. Convention: use `C:\dev\<project>` junctions via `scripts/setup-path-normalization.ps1`. The first-run CMD one-liner is at the top of `~/.claude/README.md` under "⚡ First Run On This Machine".

**Does NOT sync**: `settings.json` (permissions drift per machine), `plugins/cache/`, `backups/`, `sessions/`, `mcp-needs-auth-cache.json`, session transcripts (`.jsonl` + UUID dirs under `projects/`), `settings.local.json`.

**`~/Knowledge/`** is a separate private repo (`Mobivs/Knowledge`) with its own 5-min scheduled-task auto-sync, set up by `scripts/setup-new-machine.ps1`.
