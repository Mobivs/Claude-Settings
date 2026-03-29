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
│   ├── hypothesis-driven-researcher.md
│   └── conversion-engineer.md
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
├── logs/                      # Daily journal — one file per day, one section per session
│   └── YYYY-MM-DD.md
│
├── notes/                     # Permanent atomic notes — agent creates when something earns it
│   └── YYYY-MM-DD-[slug].md
│
├── projects/                  # Per-project running docs with agent-maintained current state
│   ├── _index.md
│   └── {project-slug}.md
│
├── lessons/                   # Legacy topic files (still readable, new captures go to daily log)
└── references/                # Legacy quick references (still readable)
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

### ui-expert
**File**: `ui-expert.md`
**Purpose**: Professional UI design review of any web application — visual consistency, color systems, typography, spacing, layout, animations, responsive design, dark/light theme quality
**Model**: Sonnet
**Color**: Purple

**When to use**:
- Visual design review or audit of a web app
- Inconsistent styling, colors, or spacing across pages
- App looks unprofessional or unpolished
- Need to bring UI up to production quality
- Evaluating dark mode, glassmorphism, or theme implementation

**Key capability**: Uses WebFetch to view the running app as users see it, plus reads source code for CSS/HTML/component issues.

### ux-expert
**File**: `ux-expert.md`
**Purpose**: Professional UX review of any web application — navigation, user flows, accessibility (WCAG 2.2), error handling, loading states, data presentation, cognitive load, mobile experience
**Model**: Sonnet
**Color**: Blue

**When to use**:
- Usability review or audit of a web app
- Users report confusion or difficulty
- Accessibility audit needed (ARIA, keyboard, screen reader)
- Need to improve user flows, error handling, or feedback
- Evaluating data-heavy dashboards or security UIs

**Key capability**: Uses WebFetch to experience the app as a user would, plus reviews source code for interaction quality, a11y, and error handling.

### conversion-engineer
**File**: `conversion-engineer.md`
**Purpose**: Audit landing pages, diagnose unprofitable ads, design conversion funnels
**Model**: Sonnet
**Color**: Orange

**When to use**:
- Google/Meta/paid ads aren't converting profitably
- Landing page audit needed
- Designing post-click funnels
- Understanding why traffic bounces
- Fixing measurement/attribution issues
- Building checkout flows or email sequences

**Core Framework**: The 9 Conversion Factors (from 13K marketer study):
1. Funnels (59.9% of winners)
2. Multiple payment options (58.2%)
3. Email sequences for non-buyers (47.9%)
4. Multi-step checkouts (42.5%)
5. Persona-specific copy (35.6%)
6. Smart remarketing (33.4%)
7. Video on landing pages (26.8%)
8. Long descriptive pages (21.5%)
9. Influencer/testimonial content (17.7%)

**Key Insight**: Failed campaigns have 0-2 factors. Profitable campaigns have 5-7.

---

## Global Skills

Located in: `~/.claude/skills/`

### memory
**Folder**: `memory/`
**Purpose**: Personal journal and memory system — daily logs, ideas, discoveries, project state, session continuity

**Triggers**:
- "log this", "save this", "capture this", "remember this"
- "what did we work on", "catch me up", "any open threads"
- "wrap up", "end of session", "signing off"
- "what was that idea about X"

**Architecture**: Skill (user-facing) + subagent (for recall/search — protects main context window)

### knowledge-base *(legacy — superseded by memory skill)*
**Folder**: `knowledge-base/`
**Purpose**: Original knowledge tracking skill — use `/memory` instead for new work

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
| Permanent notes | `C:\Users\John Vickrey\Knowledge\notes\` |
| Projects | `C:\Users\John Vickrey\Knowledge\projects\` |
| Legacy lessons | `C:\Users\John Vickrey\Knowledge\lessons\` |
| Legacy references | `C:\Users\John Vickrey\Knowledge\references\` |

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
