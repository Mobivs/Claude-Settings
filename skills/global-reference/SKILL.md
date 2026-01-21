---
name: global-reference
description: Master reference for all global Claude Code configuration, skills, agents, templates, and knowledge management. Use this to understand the global structure, find resources, or set up new components correctly.
allowed-tools: Read, Glob, Grep
---

# Global Reference Guide

This is the master reference for John Vickrey's global Claude Code setup. Use this to find resources, understand conventions, and maintain consistency across all projects.

---

## Directory Structure Overview

### Claude Code Configuration (`~/.claude/` = `C:\Users\John Vickrey\.claude\`)

```
~/.claude/
├── .credentials.json          # OAuth credentials (do not edit)
├── settings.local.json        # Global permission settings
│
├── agents/                    # Custom agents (available globally)
│   └── hypothesis-driven-researcher.md
│
├── skills/                    # Custom skills (available globally)
│   ├── global-reference/      # THIS SKILL - master reference
│   │   └── SKILL.md
│   ├── knowledge-base/        # Knowledge management skill
│   │   └── SKILL.md
│   └── meta-ads/              # Meta Marketing API reference
│       ├── SKILL.md           # Main entry point
│       ├── authentication.md
│       ├── campaign-structure.md
│       ├── campaigns.md
│       ├── adsets.md
│       ├── ads-creatives.md
│       ├── insights.md
│       ├── targeting.md
│       └── troubleshooting.md
│
├── templates/                 # Reusable file templates
│   └── research-notes-template.md
│
├── plugins/                   # Installed plugins
├── plans/                     # Saved plans
├── todos/                     # Todo state
├── debug/                     # Debug logs
├── downloads/                 # Downloaded files
├── file-history/              # File change history
├── shell-snapshots/           # Shell state snapshots
├── ide/                       # IDE integration state
├── statsig/                   # Feature flags
└── telemetry/                 # Usage telemetry
```

### Claude Code Main Config (`~/.claude.json`)

Location: `C:\Users\John Vickrey\.claude.json`

Contains:
- MCP server configurations
- Project trust settings
- User preferences
- Cached feature flags

**Current MCP Servers:**
- `hostinger-mcp` - Hostinger hosting management

---

### Knowledge Base (`~/Knowledge/` = `C:\Users\John Vickrey\Knowledge\`)

```
Knowledge/
├── logs/                      # Daily activity logs
│   └── YYYY-MM-DD.md         # One file per day
│
├── lessons/                   # Lessons learned by topic
│   ├── claude-code.md        # Claude Code tips & tricks
│   ├── tailwind-css.md       # Tailwind CSS lessons
│   ├── php.md                # PHP patterns
│   └── {topic}.md            # Add new topics as needed
│
├── projects/                  # Project registry
│   ├── _index.md             # Master index of all projects
│   └── {project-slug}.md     # Individual project files
│
└── references/                # Quick reference sheets
    ├── tech-stacks.md        # Preferred stacks & why we like them
    └── {topic}.md            # Command references, patterns
```

---

## Global Agents

Located in: `~/.claude/agents/`

### hypothesis-driven-researcher
**File**: `hypothesis-driven-researcher.md`
**Purpose**: Systematic research with competing hypotheses and confidence tracking
**Model**: Sonnet
**Color**: Green

**When to use**:
- Complex investigations with multiple possible explanations
- Root cause analysis
- Competitive analysis
- Technical deep-dives requiring systematic exploration

**Template**: Uses `~/.claude/templates/research-notes-template.md`

---

## Global Skills

Located in: `~/.claude/skills/`

### knowledge-base
**Folder**: `knowledge-base/`
**Purpose**: Track lessons learned, daily logs, and references across all projects

**Triggers**:
- "log this", "add to the log"
- "record what we learned", "add to lessons"
- "end of day", "wrap up"
- "what did we do on X date"
- "what do we know about X"

### global-reference (this skill)
**Folder**: `global-reference/`
**Purpose**: Master reference for all global configuration and resources

### meta-ads
**Folder**: `meta-ads/`
**Purpose**: Meta Marketing API reference for Facebook and Instagram advertising

**Triggers**:
- Working with Meta/Facebook/Instagram ads API
- Creating or managing ad campaigns programmatically
- Understanding campaign structure or hierarchy
- Targeting options for ads
- Pulling performance reports or insights
- Meta API errors or troubleshooting

**Structure** (layered - only load what you need):
| File | Purpose |
|------|---------|
| `SKILL.md` | Overview and navigation |
| `authentication.md` | Access tokens, permissions, app setup |
| `campaign-structure.md` | Object hierarchy (Account > Campaign > AdSet > Ad) |
| `campaigns.md` | Creating/managing campaigns, objectives |
| `adsets.md` | Budgets, schedules, bidding, optimization |
| `ads-creatives.md` | Ads, images, videos, creative specs |
| `targeting.md` | Audiences, demographics, interests, locations |
| `insights.md` | Performance metrics, reporting, breakdowns |
| `troubleshooting.md` | Error codes, rate limits, debugging |

---

## Global Templates

Located in: `~/.claude/templates/`

### research-notes-template.md
**Purpose**: Structured template for hypothesis-driven research
**Used by**: hypothesis-driven-researcher agent

**Sections**:
- Problem Decomposition
- Hypothesis Tree (H1, H2, H3)
- Confidence Tracker
- Evidence Log
- Self-Critique Checkpoints
- Current Conclusions

### project-template.md
**Purpose**: Template for documenting projects in the registry
**Location**: `~/Knowledge/projects/{project-slug}.md`

**Includes**:
- YAML frontmatter with structured metadata
- Tech stack details
- Hosting & deployment info
- Development environment setup
- Credentials locations (not values!)
- Backup strategy
- Contacts/team
- Known issues and roadmap

---

## Project Registry

Located in: `~/Knowledge/projects/`

### Structure
- `_index.md` - Master index with quick reference table
- `{project-slug}.md` - Individual project files

### Project File Format
Uses YAML frontmatter + Markdown:
- **Frontmatter**: Structured metadata (status, tech stack, hosting, contacts)
- **Body**: Detailed documentation, setup instructions, notes

### Adding a New Project
1. Copy template: `~/.claude/templates/project-template.md`
2. Save as: `~/Knowledge/projects/{project-slug}.md`
3. Fill in frontmatter and sections
4. Add entry to `_index.md`

---

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Daily logs | `YYYY-MM-DD.md` | `2025-12-26.md` |
| Lessons | `{topic}.md` (lowercase, hyphens) | `claude-code.md` |
| Projects | `{project-slug}.md` | `vibe9.md` |
| Agents | `{descriptive-name}.md` | `hypothesis-driven-researcher.md` |
| Skills | `{skill-name}/SKILL.md` | `knowledge-base/SKILL.md` |
| Templates | `{name}-template.md` | `research-notes-template.md` |
| Research notes | `research-notes-{topic}.md` | `research-notes-auth-bug.md` |

---

## Adding New Components

### Add a New Global Agent
1. Create: `~/.claude/agents/{agent-name}.md`
2. Include frontmatter: `name`, `description`, `model`, `color`
3. Restart Claude Code

### Add a New Global Skill
1. Create folder: `~/.claude/skills/{skill-name}/`
2. Create: `~/.claude/skills/{skill-name}/SKILL.md`
3. Include frontmatter: `name`, `description`, `allowed-tools`
4. Restart Claude Code

### Add a New Template
1. Create: `~/.claude/templates/{name}-template.md`
2. Reference in agents/skills that use it

### Add a New Lessons Topic
1. Create: `~/Knowledge/lessons/{topic}.md`
2. Use consistent format (see existing files)

### Add a New MCP Server
1. Edit: `~/.claude.json`
2. Add to `mcpServers` object
3. Windows: Use `cmd /c npx` wrapper
4. Restart Claude Code

---

## MCP Server Configuration

### Current Servers

**hostinger-mcp**
```json
{
  "type": "stdio",
  "command": "cmd",
  "args": ["/c", "npx", "hostinger-api-mcp@latest"],
  "env": {
    "API_TOKEN": "YOUR_API_KEY"
  }
}
```

### Windows vs Mac/Linux

**Windows** (must use cmd wrapper):
```json
"command": "cmd",
"args": ["/c", "npx", "package-name"]
```

**Mac/Linux**:
```json
"command": "npx",
"args": ["package-name"]
```

---

## Quick Reference Paths

| Resource | Path |
|----------|------|
| Main config | `C:\Users\John Vickrey\.claude.json` |
| Permissions | `C:\Users\John Vickrey\.claude\settings.local.json` |
| Agents | `C:\Users\John Vickrey\.claude\agents\` |
| Skills | `C:\Users\John Vickrey\.claude\skills\` |
| Templates | `C:\Users\John Vickrey\.claude\templates\` |
| Daily logs | `C:\Users\John Vickrey\Knowledge\logs\` |
| Lessons | `C:\Users\John Vickrey\Knowledge\lessons\` |
| Projects | `C:\Users\John Vickrey\Knowledge\projects\` |
| References | `C:\Users\John Vickrey\Knowledge\references\` |

---

## Common Tasks

### Find what agents/skills exist
```bash
ls ~/.claude/agents/
ls ~/.claude/skills/
```

### Check MCP server status
Use `/mcp` command in Claude Code

### Search knowledge base
```bash
grep -r "search term" ~/Knowledge/
```

### View today's log
```bash
cat ~/Knowledge/logs/$(date +%Y-%m-%d).md
```

### Check global permissions
```bash
cat ~/.claude/settings.local.json
```

---

## Maintenance

### After changes to agents/skills
- Restart Claude Code for changes to take effect

### After changes to MCP config
- Restart Claude Code
- Verify with `/mcp` command

### Regular cleanup
- Review and archive old logs monthly
- Consolidate lessons when topics grow large
- Remove unused templates
