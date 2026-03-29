# Memory System — Cross-Machine Reference

This document is the authoritative guide for running the memory/journal system across multiple machines and Claude Code instances.

---

## Architecture: Two Synced Repos

The system has two parts that must **both** exist on every machine:

| Component | Location | Synced via |
|---|---|---|
| Memory skill + CLAUDE.md | `~/.claude/` | Git (`Mobivs/Claude-Settings`) |
| Knowledge vault (journal files) | `~/Knowledge/` | Git (`Mobivs/Knowledge` — private) + auto-sync every 5 min |

**The most common new-machine failure:** the skill syncs fine, but `~/Knowledge/` hasn't been cloned, so every write operation silently fails or errors.

---

## Vault Structure (must exist on every machine)

```
~/Knowledge/
├── logs/           # Daily journal — YYYY-MM-DD.md, one per day
├── notes/          # Permanent atomic notes (agent-created)
├── projects/       # Per-project running docs (agent-maintained)
└── sync.ps1        # Auto-sync script (commit + push every 5 min)
```

**Legacy folders** (exist on the primary machine, still readable):
```
├── lessons/        # Old topic files — readable but new captures go to logs/
├── references/     # Old quick refs — readable but superseded
```

---

## New Machine Setup Checklist

After cloning `~/.claude` on a new machine:

- [ ] Clone the Knowledge vault:
  ```powershell
  git clone https://github.com/Mobivs/Knowledge.git "$env:USERPROFILE\Knowledge"
  ```
  Or on Mac/Linux:
  ```bash
  git clone https://github.com/Mobivs/Knowledge.git ~/Knowledge
  ```
- [ ] Set up auto-sync (see Auto-Sync Setup below)
- [ ] Restart Claude Code
- [ ] Test with `/memory` — should respond without errors
- [ ] Test session open: ask "catch me up" — agent should read last 7 days

---

## Auto-Sync Setup

The vault auto-syncs to GitHub every 5 minutes via a scheduled task. This keeps all machines in sync — write on one, it appears on the others within minutes.

### Windows (Task Scheduler)

The sync script `sync.ps1` is included in the vault. Register it:

```powershell
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$env:USERPROFILE\Knowledge\sync.ps1`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName 'Knowledge Vault Sync' -Action $action -Trigger $trigger -Settings $settings -Description 'Auto-sync Knowledge vault to GitHub every 5 minutes' -Force
```

### Mac/Linux (cron)

```bash
# Add to crontab
(crontab -l 2>/dev/null; echo "*/5 * * * * cd ~/Knowledge && git pull --rebase --quiet && git add -A && git diff --cached --quiet || git commit -m 'auto-sync: $(hostname) @ $(date +\%Y-\%m-\%d\ \%H:\%M)' --quiet && git push --quiet") | crontab -
```

### How sync works

1. `git pull --rebase` — get changes from other machines first
2. `git add -A` — stage any local changes
3. `git commit` — only if there are changes, with machine name + timestamp
4. `git push` — send to GitHub

Runs silently in the background. No window, no interruption.

---

## Sync Flow Between Machines

### Settings (skills, CLAUDE.md, agents)
```powershell
# Pull latest on any machine
cd ~/.claude
git pull origin main

# Push changes after editing skills/agents/CLAUDE.md
cd ~/.claude
git add -A && git commit -m "description" && git push
```

### Knowledge vault
**Automatic** — the scheduled task handles pull/commit/push every 5 minutes. No manual sync needed.

To force an immediate sync:
```powershell
# Windows
powershell -File "$env:USERPROFILE\Knowledge\sync.ps1"
```
```bash
# Mac/Linux
cd ~/Knowledge && git pull --rebase && git add -A && git diff --cached --quiet || git commit -m "manual sync" && git push
```

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
- `~/Knowledge/` doesn't exist → clone it: `git clone https://github.com/Mobivs/Knowledge.git ~/Knowledge`
- Check the exact path: must be `%USERPROFILE%\Knowledge\` on Windows, `~/Knowledge/` on Mac/Linux

### "Session open returns nothing / errors"
- `~/Knowledge/logs/` is empty (new machine, no prior logs) — this is normal
- If auto-sync is running, logs from other machines should appear within 5 minutes

### "Sync conflicts"
- The sync script uses `git pull --rebase` which handles most cases
- If a real conflict occurs (rare — two machines editing the same file at the same time), resolve manually with `git rebase --continue`

### Vault Init (only if not cloning)
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\Knowledge\logs"
New-Item -ItemType Directory -Force "$env:USERPROFILE\Knowledge\notes"
New-Item -ItemType Directory -Force "$env:USERPROFILE\Knowledge\projects"
```

Or on Mac/Linux:
```bash
mkdir -p ~/Knowledge/{logs,notes,projects}
```

---

## Future Expansion

- **Obsidian vault**: open `~/Knowledge/` as an Obsidian vault for visual browsing and linking
- **Obsidian Local REST API + MCP**: richer queries without grep, better semantic search
- **Vector store**: semantic search layer — the memory skill interface stays the same, only the backend changes
