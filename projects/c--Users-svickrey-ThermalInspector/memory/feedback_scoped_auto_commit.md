---
name: Scope auto-commits, never git add -A
description: When automating commits, always stage specific paths — user learned this tradeoff after auto-sync swept files they had explicitly asked to leave for review
type: feedback
originSessionId: c44629ec-e370-47cd-82dc-3ae01563e66a
---
Automated git commits should stage explicit paths, never `git add -A`.

**Why:** During the sync system setup, the initial `sync.sh` used `git add -A` on Stop. It auto-committed `plugins/known_marketplaces.json` and `plugins/blocklist.json` even though I had explicitly told the user I'd leave those for their review. They accepted the outcome but immediately asked to redesign the scope rules so it wouldn't happen again.

**How to apply:**
- Automation that touches git should stage specific paths or globs, not everything
- Even when the user says "commit everything", double-check for untracked files they may not have seen
- When adding new automation: default to narrow scope and ask before widening
- The current `~/.claude/scripts/sync.sh` is the reference pattern — stages only `skills/ agents/ templates/ scripts/ projects/ .gitignore README.md`
