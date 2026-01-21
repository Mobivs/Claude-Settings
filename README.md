# Claude Code Global Settings Repository

A version-controlled repository for managing Claude Code global configuration across multiple machines. Push changes from any machine, pull to synchronize all others.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [What's Tracked vs Ignored](#whats-tracked-vs-ignored)
- [Setting Up a New Machine](#setting-up-a-new-machine)
- [Daily Workflow](#daily-workflow)
- [Configuration Reference](#configuration-reference)
  - [settings.json](#settingsjson)
  - [settings.local.json](#settingslocaljson)
  - [Skills](#skills)
  - [Agents](#agents)
  - [Templates](#templates)
  - [Plugins](#plugins)
- [Automation Options](#automation-options)
- [Troubleshooting](#troubleshooting)

---

## Quick Start

### First-Time Setup (Origin Machine)

```bash
cd ~/.claude
git init
git remote add origin https://github.com/YOUR_USERNAME/claude-global-settings.git
git add .
git commit -m "Initial commit: global Claude Code settings"
git push -u origin main
```

### Clone to New Machine

```bash
# Backup existing .claude directory if it exists
mv ~/.claude ~/.claude-backup

# Clone the repository
git clone https://github.com/YOUR_USERNAME/claude-global-settings.git ~/.claude

# Copy machine-specific files from backup
cp ~/.claude-backup/.credentials.json ~/.claude/
cp ~/.claude-backup/settings.local.json ~/.claude/

# Restart Claude Code
```

---

## Repository Structure

```
~/.claude/
├── .git/                      # Git repository
├── .gitignore                 # Excludes sensitive/machine-specific files
├── README.md                  # This file
│
├── settings.json              # SHARED global settings
├── settings.local.json        # IGNORED - machine-specific permissions
│
├── agents/                    # SHARED - custom agent definitions
│   └── hypothesis-driven-researcher.md
│
├── skills/                    # SHARED - custom skills
│   ├── global-reference/
│   │   └── SKILL.md
│   ├── knowledge-base/
│   │   └── SKILL.md
│   ├── meta-ads/
│   │   └── SKILL.md (+ sub-docs)
│   └── vibe9-publish/
│       └── SKILL.md
│
├── templates/                 # SHARED - reusable file templates
│   ├── project-template.md
│   └── research-notes-template.md
│
├── plugins/                   # PARTIALLY SHARED
│   ├── installed_plugins.json # tracked
│   ├── known_marketplaces.json# tracked
│   └── cache/                 # ignored
│
├── .credentials.json          # IGNORED - OAuth credentials
├── cache/                     # IGNORED - temporary cache
├── debug/                     # IGNORED - debug logs
├── downloads/                 # IGNORED - downloaded files
├── file-history/              # IGNORED - change history
├── ide/                       # IGNORED - IDE state
├── plans/                     # IGNORED - session plans
├── projects/                  # IGNORED - project-specific data
├── shell-snapshots/           # IGNORED - shell state
├── statsig/                   # IGNORED - feature flags
├── telemetry/                 # IGNORED - usage telemetry
└── todos/                     # IGNORED - todo state
```

---

## What's Tracked vs Ignored

### Tracked (Shared Across Machines)

| Item | Purpose |
|------|---------|
| `settings.json` | Global permissions and plugin enablement |
| `agents/` | Custom agent definitions |
| `skills/` | Custom skill definitions |
| `templates/` | Reusable file templates |
| `plugins/installed_plugins.json` | List of installed plugins |
| `plugins/known_marketplaces.json` | Plugin marketplace registry |
| `README.md` | This documentation |
| `.gitignore` | Repository configuration |

### Ignored (Machine-Specific)

| Item | Reason |
|------|--------|
| `.credentials.json` | OAuth tokens - machine/account specific |
| `.vibe9-token` | API token - sensitive |
| `settings.local.json` | Machine-specific permissions & paths |
| `cache/`, `debug/`, `ide/` | Temporary/session data |
| `projects/` | Machine-specific project paths |
| `plans/`, `todos/` | Session state |
| `telemetry/`, `statsig/` | Analytics data |
| `file-history/`, `shell-snapshots/` | Local history |

---

## Setting Up a New Machine

### Prerequisites

1. Claude Code CLI installed
2. Git installed and configured
3. GitHub SSH key or HTTPS credentials set up

### Step-by-Step Setup

#### 1. Run Claude Code Once (Creates Default Structure)

```bash
claude
# Exit immediately with Ctrl+C
```

#### 2. Backup Auto-Generated Files

```bash
cd ~
mv .claude .claude-original
```

#### 3. Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/claude-global-settings.git ~/.claude
```

#### 4. Restore Machine-Specific Files

```bash
# Copy credentials (required for authentication)
cp ~/.claude-original/.credentials.json ~/.claude/

# Create machine-specific settings
# Copy from original or create new:
cp ~/.claude-original/settings.local.json ~/.claude/
```

#### 5. Create settings.local.json (If New)

If you don't have a `settings.local.json`, create one:

```json
{
  "permissions": {
    "allow": []
  }
}
```

Add machine-specific permissions as needed (see [settings.local.json](#settingslocaljson)).

#### 6. Restart Claude Code

```bash
claude
```

Verify everything loads correctly with:
- Check skills: `/global-reference`
- Check agents: Use Task tool with `hypothesis-driven-researcher`
- Check MCP: `/mcp` (requires `~/.claude.json` setup separately)

---

## Daily Workflow

### Pull Latest Changes

```bash
cd ~/.claude
git pull
```

Then restart Claude Code to pick up changes.

### Push Your Changes

After modifying settings, skills, agents, or templates:

```bash
cd ~/.claude
git add .
git commit -m "Add new skill for X"
git push
```

### Sync Script (Recommended)

Create `~/.claude/scripts/sync.sh` (or `.ps1` for Windows):

**Bash (Mac/Linux):**
```bash
#!/bin/bash
cd ~/.claude
git pull --rebase
git add .
if ! git diff --cached --quiet; then
    git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M')"
    git push
fi
echo "Claude settings synced!"
```

**PowerShell (Windows):**
```powershell
Set-Location $env:USERPROFILE\.claude
git pull --rebase
git add .
$changes = git diff --cached --quiet; $LASTEXITCODE
if ($LASTEXITCODE -ne 0) {
    $date = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "Auto-sync: $date"
    git push
}
Write-Host "Claude settings synced!"
```

---

## Configuration Reference

### settings.json

Global settings shared across all machines.

```json
{
  "permissions": {
    "allow": [
      "Skill(global-reference)",
      "Skill(global-reference:*)"
    ],
    "additionalDirectories": [
      "C:\\Users\\John Vickrey\\.claude\\skills"
    ]
  },
  "enabledPlugins": {
    "php-lsp@claude-plugins-official": true
  }
}
```

**Key Fields:**
- `permissions.allow` - Pre-approved tools/skills (won't prompt)
- `permissions.additionalDirectories` - Extra directories Claude can access
- `enabledPlugins` - Plugins to load automatically

**Note:** Paths in `additionalDirectories` may need adjustment per machine. Consider using `settings.local.json` for machine-specific paths.

### settings.local.json

Machine-specific settings. **Not tracked in git.**

```json
{
  "permissions": {
    "allow": [
      "Bash(powershell.exe:*)",
      "Bash(mkdir:*)",
      "WebSearch"
    ]
  }
}
```

Use this for:
- Machine-specific command permissions
- Local tool authorizations
- Paths specific to this machine

### Skills

Located in `skills/{skill-name}/SKILL.md`

#### Skill File Format

```markdown
---
name: skill-name
description: What this skill does (shown in tool list)
allowed-tools: Read, Glob, Grep, WebFetch
---

# Skill Instructions

Your skill prompt content here...
```

**Frontmatter Fields:**
- `name` (required) - Skill identifier
- `description` (required) - Shown in help/tool descriptions
- `allowed-tools` - Comma-separated list of tools the skill can use

#### Creating a New Skill

```bash
mkdir -p ~/.claude/skills/my-new-skill
touch ~/.claude/skills/my-new-skill/SKILL.md
```

Edit the `SKILL.md` file with the format above.

#### Current Skills

| Skill | Purpose |
|-------|---------|
| `global-reference` | Master reference for all configuration |
| `knowledge-base` | Personal knowledge management (logs, lessons) |
| `meta-ads` | Meta Marketing API reference |
| `vibe9-publish` | Vibe9 community site integration |

### Agents

Located in `agents/{agent-name}.md`

#### Agent File Format

```markdown
---
name: agent-name
description: When to use this agent (shown in Task tool)
model: sonnet
color: green
---

# Agent System Prompt

Your agent instructions here...
```

**Frontmatter Fields:**
- `name` (required) - Agent identifier
- `description` (required) - When/why to use this agent
- `model` - `sonnet`, `opus`, or `haiku`
- `color` - Display color in UI

#### Current Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| `hypothesis-driven-researcher` | sonnet | Systematic research with hypothesis tracking |

### Templates

Located in `templates/{name}-template.md`

Templates are reference files that agents/skills can copy from.

#### Current Templates

| Template | Used By |
|----------|---------|
| `research-notes-template.md` | hypothesis-driven-researcher agent |
| `project-template.md` | Project documentation |

### Plugins

Plugin installation is managed through Claude Code's plugin system.

**Tracked files:**
- `plugins/installed_plugins.json` - Which plugins are installed
- `plugins/known_marketplaces.json` - Plugin sources

**Ignored files:**
- `plugins/cache/` - Downloaded plugin files
- `plugins/install-counts-cache.json` - Usage stats

After pulling, plugins may need to be reinstalled if they're not cached locally.

---

## Automation Options

### Git Hooks

#### Auto-Pull on Claude Start

Add to your shell profile (`.bashrc`, `.zshrc`, or PowerShell profile):

```bash
# Bash/Zsh
alias claude='cd ~/.claude && git pull --quiet && cd - && claude'
```

```powershell
# PowerShell
function Start-Claude {
    Push-Location $env:USERPROFILE\.claude
    git pull --quiet
    Pop-Location
    claude
}
Set-Alias claude Start-Claude
```

#### Pre-Commit Hook for Validation

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Validate JSON files
for f in settings.json plugins/installed_plugins.json plugins/known_marketplaces.json; do
    if [ -f "$f" ]; then
        python -m json.tool "$f" > /dev/null 2>&1 || {
            echo "Invalid JSON: $f"
            exit 1
        }
    fi
done
```

### Scheduled Sync

#### Windows Task Scheduler

1. Create `sync-claude.ps1` in the scripts folder
2. Open Task Scheduler
3. Create Basic Task → Trigger: At log on / Daily
4. Action: Start a program
5. Program: `powershell.exe`
6. Arguments: `-File "C:\Users\John Vickrey\.claude\scripts\sync-claude.ps1"`

#### Mac/Linux Cron

```bash
# Edit crontab
crontab -e

# Add line (sync every hour)
0 * * * * cd ~/.claude && git pull --rebase --quiet
```

### GitHub Actions (Optional)

For automated testing of configuration:

```yaml
# .github/workflows/validate.yml
name: Validate Config

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate JSON files
        run: |
          for f in settings.json plugins/*.json; do
            if [ -f "$f" ]; then
              python -m json.tool "$f" > /dev/null
            fi
          done

      - name: Check skill frontmatter
        run: |
          for f in skills/*/SKILL.md; do
            head -1 "$f" | grep -q "^---" || echo "Missing frontmatter: $f"
          done
```

---

## Troubleshooting

### Changes Not Taking Effect

**Solution:** Restart Claude Code after any changes to:
- `settings.json`
- Skills (`skills/*/SKILL.md`)
- Agents (`agents/*.md`)
- MCP configuration (`~/.claude.json`)

### Merge Conflicts

If you get merge conflicts after pulling:

```bash
cd ~/.claude
git status  # See conflicted files
# Edit files to resolve conflicts
git add .
git commit -m "Resolve merge conflicts"
```

### Permission Denied on New Machine

If Claude can't access skills:

1. Check `settings.json` has correct `additionalDirectories` path
2. Ensure the path uses correct format for OS:
   - Windows: `C:\\Users\\Username\\.claude\\skills`
   - Mac/Linux: `/Users/username/.claude/skills`

### Skills Not Loading

1. Verify skill folder structure: `skills/{name}/SKILL.md`
2. Check SKILL.md has valid frontmatter (starts with `---`)
3. Restart Claude Code
4. Try invoking with full path: `Skill(global-reference)`

### Credentials Invalid After Clone

The `.credentials.json` file is machine-specific. You must:

1. Run Claude Code once on the new machine to authenticate
2. Or copy `.credentials.json` from a working machine (same account only)

### Git Pull Fails

If local changes conflict with remote:

```bash
# Option 1: Stash local changes
git stash
git pull
git stash pop

# Option 2: Force reset to remote (loses local changes!)
git fetch origin
git reset --hard origin/main
```

---

## Related Files Outside This Repository

These files are related but stored elsewhere:

| File | Location | Purpose |
|------|----------|---------|
| `~/.claude.json` | Home directory | MCP servers, project trust |
| `~/Knowledge/` | Knowledge folder | Personal knowledge base |
| `{project}/.claude/` | Per-project | Project-specific Claude config |

Consider creating separate repositories for:
- **Knowledge base**: `~/Knowledge/` - lessons, logs, references
- **MCP configuration**: `~/.claude.json` - if you want to sync MCP servers

---

## Contributing

When adding new skills/agents/templates:

1. Follow existing naming conventions
2. Include complete frontmatter
3. Test locally before pushing
4. Update this README if adding new categories
5. Commit with descriptive messages

---

*Last updated: 2025-01-20*
