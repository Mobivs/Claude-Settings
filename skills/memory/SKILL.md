---
name: memory
description: Personal journal and memory system. Log daily activities, capture ideas and inspirations, recall past work, and manage session continuity. Triggers: "log this", "capture this", "save this", "remember this", "what did we work on", "catch me up", "wrap up", "end of session", "any open threads".
---

# Memory Skill

Personal journal system backed by `~/Knowledge/`.

## Vault Structure

```
Knowledge/
├── logs/YYYY-MM-DD.md      # Daily journal — one file per day, append each session
├── notes/[slug].md         # Permanent notes — created when something earns it
└── projects/[name].md      # Per-project running doc with agent-maintained current state
```

---

## Vault Init (before any write operation)

Before writing for the first time in a session, silently ensure the vault directories exist:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\Knowledge\logs"
New-Item -ItemType Directory -Force "$env:USERPROFILE\Knowledge\notes"
New-Item -ItemType Directory -Force "$env:USERPROFILE\Knowledge\projects"
```

On Mac/Linux:
```bash
mkdir -p ~/Knowledge/{logs,notes,projects}
```

Never mention this to the user unless creation fails.

---

## Operations

### Direct Writes (handle inline — no subagent)

**LOG / CAPTURE** — user says "log this", "save this", "remember this", "capture this":
1. Determine which section of today's note it belongs to (see Daily Log Format below)
2. Append to `logs/YYYY-MM-DD.md` under the right section — create the file if it doesn't exist
3. Respond with one line: `Logged to YYYY-MM-DD.md`

**IDEA** — user shares an idea, inspiration, or exciting discovery mid-session:
- Append to `## ⚡ Ideas & Inspirations` in today's log
- Use their words, no editorializing, no friction
- Respond: `Idea captured.`

Never ask the user to categorize what they're saving. Just save it.

---

### Subagent Operations (use Agent tool — protect main context window)

**SESSION OPEN** — when user starts a session or asks "catch me up" / "what were we working on" / "any open threads":

Spawn an Agent with these instructions:
> Read the last 7 days of daily logs from `~/Knowledge/logs/`.
> Identify: (1) which projects were active, (2) any open threads or unresolved questions left in the logs, (3) any ideas flagged for follow-up.
> Return a compact brief — 5 to 8 bullet points maximum. Never dump raw file content. Be terse.

Return that brief directly to the user as the session opener.

**SESSION CLOSE** — user says "wrap up", "end of session", "signing off", "that's it for today", "I'm done":

1. Summarize the current session from conversation context: what was worked on, decisions made, ideas captured, anything left open
2. Write or update today's log at `logs/YYYY-MM-DD.md`
3. If a specific project was the focus, update `projects/[name].md` current state section
4. Respond with:
   ```
   Logged to YYYY-MM-DD.md
   Open threads:
   - [thread 1]
   - [thread 2]
   ```

**RECALL** — user asks about past work, a past idea, or what we know about a topic:

Spawn an Agent with these instructions:
> Search `~/Knowledge/` for [topic / date / project].
> Read the relevant sections. Return a compact summary — max 10 bullets. Never dump raw file content.

---

## Daily Log Format

```markdown
# YYYY-MM-DD

## Session: [project or context — e.g. "vibe9 auth refactor" or "brainstorming"]

### What We're Working On
- Where we picked up, what we're doing

### Progress & Wins
-

### ⚡ Ideas & Inspirations
-

### Discoveries & Learnings
-

### Open Threads
- Things to follow up on next session

### Personal Note
-
```

If a session section already exists for today, append a new `## Session: [context]` block rather than overwriting.

---

## Project Note Format

```markdown
# [Project Name]

## Current State
> Agent-maintained. Updated each session. Reflects where things stand RIGHT NOW.

Last updated: YYYY-MM-DD

[2-4 sentence summary of current status, active work, and next logical step]

---

## Session History

### YYYY-MM-DD
- Bullet summary of what happened this session
```

When updating a project note: rewrite the `## Current State` block with a fresh summary, then append a new entry to `## Session History`. Never delete history.

---

## Permanent Notes (`notes/`)

Create `notes/YYYY-MM-DD-[slug].md` when:
- An idea appears across multiple daily logs and deserves its own space
- A discovery fundamentally changes how we approach something
- The user says "make a proper note of this" or "I want to keep that idea somewhere solid"

Keep notes atomic — one clear insight or idea per file. Link back to the daily log it came from.

---

## Response Rules

- WRITE confirmations: one line only
- RECALL / SESSION_OPEN: bullets only, never raw file dumps, never more than 10 points
- SESSION_CLOSE: confirmation line + open threads list
- Never ask the user to categorize or organize — the agent decides
