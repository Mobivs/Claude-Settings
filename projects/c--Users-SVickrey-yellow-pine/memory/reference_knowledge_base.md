---
name: Knowledge base and daily logging setup
description: Memory system uses /memory skill, vault at ~/Knowledge/ synced via GitHub (Mobivs/Knowledge) with auto-sync every 5 min
type: reference
---

The memory system has two synced repos:
- **`Mobivs/Claude-Settings`** — skills, agents, CLAUDE.md (the instructions)
- **`Mobivs/Knowledge`** (private) — daily logs, notes, project state (the data)

Vault lives at `~/Knowledge/` on every machine. Auto-syncs to GitHub every 5 minutes via Windows Task Scheduler running `sync.ps1`.

The `/memory` skill is the current system. The old `/knowledge-base` skill is legacy — superseded.

Daily logs go to `~/Knowledge/logs/YYYY-MM-DD.md`. Project state goes to `~/Knowledge/projects/[name].md`. Permanent notes go to `~/Knowledge/notes/`.

Paths use `~/` (not hardcoded user paths) for multi-machine support. PowerShell scripts use `$env:USERPROFILE`. Fixed from `John Vickrey` hardcoded paths on 2026-03-28.
