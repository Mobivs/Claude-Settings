# Memory System — Cross-Machine Reference

This document is the authoritative guide for running the memory/journal system across multiple machines and Claude Code instances.

---

## Architecture: Two Separate Pieces

The system has two parts that must **both** exist on every machine:

| Component | Location | Synced via |
|---|---|---|
| Memory skill + CLAUDE.md | `~/.claude/` | Git (`Mobivs/Claude-Settings`) |
| Knowledge vault (journal files) | `~/Knowledge/` | **Not synced — local only** |

**The most common new-machine failure:** the skill syncs fine, but `~/Knowledge/` doesn't exist, so every write operation silently fails or errors.

---

## Vault Structure (must exist on every machine)

```
C:\Users\John Vickrey\Knowledge\
├── logs\           # Daily journal — YYYY-MM-DD.md, one per day
├── notes\          # Permanent atomic notes (agent-created)
└── projects\       # Per-project running docs (agent-maintained)
```

**Legacy folders** (exist on the primary machine, still readable):
```
├── lessons\        # Old topic files — readable but new captures go to logs/
├── references\     # Old quick refs — readable but superseded
```

---

## New Machine Setup Checklist

After cloning `~/.claude` on a new machine:

- [ ] Run `setup-new-machine.ps1` (or `setup-new-machine.sh` on Mac/Linux)
- [ ] Confirm `~/Knowledge/` was created with `logs/`, `notes/`, `projects/` subfolders
- [ ] Restart Claude Code
- [ ] Test with `/memory` — should respond without errors
- [ ] Test session open: ask "catch me up" — agent should read last 7 days (or report no logs yet if vault is empty)

---

## Sync Flow Between Machines

### Settings (skills, CLAUDE.md, agents)
```powershell
# Pull latest on any machine
cd ~/.claude
git pull origin main

# Push changes after editing skills/agents/CLAUDE.md
cd ~/.claude
./scripts/sync.ps1
```

### Journal logs (Knowledge vault)
The vault is **intentionally local** — each machine keeps its own log. This is by design: you work on one machine at a time, and the agent reads whichever logs exist locally.

If you want cross-machine journal history, the simplest option is to sync `~/Knowledge/` via OneDrive, Dropbox, or a separate git repo. This is not currently set up — it's a future option.

---

## Memory Skill Operations

| Operation | Trigger | Handled by |
|---|---|---|
| LOG / CAPTURE | "log this", "save this", "remember this" | Direct write (no subagent) |
| IDEA | Exciting idea shared mid-session | Direct write (no subagent) |
| SESSION OPEN | "catch me up", "what were we working on" | Subagent reads last 7 days |
| SESSION CLOSE | "wrap up", "end of session", "signing off" | Direct write from conversation summary |
| RECALL | "what did we work on on X", "what do we know about Y" | Subagent searches vault |

---

## Troubleshooting

### "Memory skill not responding / skill not found"
- Did you restart Claude Code after pulling?
- Check `~/.claude/skills/memory/SKILL.md` exists
- Run `/global-reference` and look under Global Skills

### "Skill runs but writes fail"
- `~/Knowledge/` doesn't exist → run the vault init (see below)
- Check the exact path: must be `C:\Users\John Vickrey\Knowledge\` on Windows

### "Session open returns nothing / errors"
- `~/Knowledge/logs/` is empty (new machine, no prior logs) — this is normal
- Agent will say no recent logs found

### Vault Init (run manually if missing)
```powershell
New-Item -ItemType Directory -Force "C:\Users\John Vickrey\Knowledge\logs"
New-Item -ItemType Directory -Force "C:\Users\John Vickrey\Knowledge\notes"
New-Item -ItemType Directory -Force "C:\Users\John Vickrey\Knowledge\projects"
```

Or on Mac/Linux:
```bash
mkdir -p ~/Knowledge/{logs,notes,projects}
```

---

## Future Expansion (not yet built)

- **Obsidian vault**: open `~/Knowledge/` as an Obsidian vault for visual browsing and linking
- **Obsidian Local REST API + MCP**: richer queries without grep, better semantic search
- **Cross-machine log sync**: sync `~/Knowledge/` via OneDrive or a separate git repo
- **Vector store**: semantic search layer — the memory skill interface stays the same, only the backend changes
