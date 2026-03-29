---
name: knowledge-base
description: Personal knowledge base for tracking lessons learned, daily activity logs, and references across all projects. Use when the user wants to log activities, record lessons, or reference past learnings.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(dir:*)
---

# Knowledge Base Skill

A global knowledge management system that spans all your projects. Track what you learn, log daily activities, and build a searchable reference library.

## Directory Structure

All files are stored in `~/Knowledge/`:

```
Knowledge/
├── logs/           # Daily activity logs
│   └── 2025-12-24.md
├── lessons/        # Things learned (organized by topic)
│   ├── php.md
│   ├── docker.md
│   ├── claude-code.md
│   └── ...
└── references/     # Quick reference sheets
    ├── api-patterns.md
    ├── git-commands.md
    └── ...
```

## When to Use This Skill

Use this skill when the user:
- Says "log this" or "add to the log"
- Wants to "record what we learned"
- Asks to "save this for later"
- Says "add to lessons learned"
- Wants to "check the logs" or "what did we do on X date"
- Asks "what do we know about X"
- Says "end of day" or "wrap up"

---

## Activity Logging

### Log Today's Activities

Create or append to today's log file:

```
~/Knowledge/logs\YYYY-MM-DD.md
```

Format:
```markdown
# Activity Log - YYYY-MM-DD

## Projects Worked On
- [Project Name]: Brief description of work done

## Key Accomplishments
- Accomplishment 1
- Accomplishment 2

## Issues Encountered
- Issue and how it was resolved

## Tomorrow / Next Steps
- Planned follow-up items
```

### End of Day Summary

When the user says "end of day" or "wrap up":
1. Read today's log if it exists
2. Summarize key activities from the session
3. Append or create the log entry
4. List any pending items for next time

---

## Lessons Learned

### Add a Lesson

When something important is learned, add it to the appropriate topic file:

```
~/Knowledge/lessons\{topic}.md
```

Format:
```markdown
## Topic Title

### Lesson: [Brief title]
**Date**: YYYY-MM-DD
**Project**: [Project name]
**Context**: What we were doing

**The Lesson**:
- Key insight or solution

**Example**:
```code or command```

---
```

### Common Topics
- `php.md` - PHP patterns, gotchas, solutions
- `docker.md` - Docker and container tips
- `claude-code.md` - Claude Code usage, skills, settings
- `git.md` - Git workflows and commands
- `deployment.md` - Hosting, deployment patterns
- `api.md` - API design patterns

---

## Quick References

### Add a Reference

For frequently-needed commands or patterns:

```
~/Knowledge/references\{topic}.md
```

Format:
```markdown
# {Topic} Quick Reference

## Section

### Command/Pattern Name
```command or code```
Brief explanation

---
```

---

## Searching Knowledge

### Find Lessons About a Topic
```bash
grep -r "search term" "~/Knowledge/lessons\"
```

### Find in Logs
```bash
grep -r "search term" "~/Knowledge/logs\"
```

### List All Lessons Files
```bash
dir "~/Knowledge/lessons\"
```

---

## Common Workflows

### "Log what we did today"
1. Get current date
2. Read existing log if present
3. Append new activities
4. Write updated log

### "What did we learn about X?"
1. Search lessons folder for topic
2. Read relevant files
3. Summarize findings

### "Save this for later"
1. Determine if it's a lesson, reference, or log entry
2. Write to appropriate file
3. Confirm saved

### "End of day wrap up"
1. Summarize session activities
2. Note any lessons learned
3. Update today's log
4. List items for next session
