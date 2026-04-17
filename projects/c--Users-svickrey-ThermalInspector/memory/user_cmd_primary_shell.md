---
name: Primary Windows shell is cmd.exe
description: User runs commands from cmd.exe rather than git bash or PowerShell — give CMD-compatible commands or explicit shell direction when suggesting one-liners
type: user
originSessionId: c44629ec-e370-47cd-82dc-3ae01563e66a
---
User's primary interactive shell on Windows is **cmd.exe**, not git bash or PowerShell.

**Evidence:** When given a PowerShell script path with `~/.claude/scripts/...`, they tried three variants from a `C:\Users\svickrey>` cmd prompt (all failed — `~` doesn't expand in cmd, `.ps1` doesn't auto-invoke PowerShell from cmd).

**How to apply:**
- When telling the user to run a command, default to a CMD-compatible form
- For `.ps1` scripts: `powershell -ExecutionPolicy Bypass -File "%USERPROFILE%\..."`
- For `.sh` scripts: either `bash "%USERPROFILE%\..."` from CMD, or tell them to open git bash
- Use `%USERPROFILE%` instead of `~` when writing for CMD
- When the command requires a specific shell, say so explicitly (e.g. "from PowerShell:" before the block)
- Claude's own Bash tool uses git bash on Windows — this is separate from what the user sees in their terminal
