---
# Project Metadata
name: "Project Name"
slug: "project-slug"
status: "active"  # active | maintenance | archived | planned
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"

# Tech Stack
languages:
  - PHP
frameworks:
  - Tailwind CSS
database: MySQL
build_tools: none
package_managers:
  - composer

# Hosting & Deployment
hosting:
  provider: Hostinger
  type: "Shared PHP"  # Shared PHP | VPS | Serverless | Static | Docker
  plan: "Premium Web Hosting"
domains:
  production: "example.com"
  staging: ""
deployment:
  method: "FTP"  # FTP | Git Push | CI/CD | Manual Upload
  branch: "main"

# Repository
git:
  remote: "https://github.com/user/repo"
  branch_strategy: "main only"  # main only | feature branches | gitflow

# Contacts
contacts:
  - name: "John Vickrey"
    role: "Owner/Developer"
    email: ""
---

# Project Name

Brief description of what this project does and its purpose.

---

## Development Environment

### Local Setup
- **Path**: `C:\Users\John Vickrey\{project-folder}`
- **IDE**: VS Code / Cursor
- **Dev Server**: `localhost:8000` or Docker

### Prerequisites
```bash
# Commands to set up local dev environment
composer install
```

### Running Locally
```bash
# Command to start local development
php -S localhost:8000
```

---

## Server Details

### Production
- **PHP Version**: 8.x
- **MySQL Version**: 8.x
- **Document Root**: `/public_html/`
- **SSH Access**: Yes/No

### Environment Variables
Location: `.env` or server config

Key variables (names only):
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `API_KEY`

---

## Credentials & Secrets

**DO NOT store actual credentials here!**

| Secret | Location | Notes |
|--------|----------|-------|
| Database credentials | Hostinger hPanel | MySQL settings |
| API keys | `.env` file (not in git) | |
| FTP credentials | Hostinger hPanel | |
| SSH keys | `~/.ssh/` | |

---

## Integrations & APIs

### External Services
- **Service Name**: What it's used for

### MCP Connections
- `hostinger-mcp` - Deployment and domain management

---

## Project-Specific Claude Config

### Skills
- `.claude/skills/{skill-name}/` - Description

### Agents
- `.claude/agents/{agent-name}.md` - Description

---

## Backup Strategy

### Code
- **Method**: Git repository
- **Location**: GitHub
- **Frequency**: On every push

### Database
- **Method**: Manual export / Automated
- **Location**: Local backups folder / Cloud
- **Frequency**: Weekly

### Files/Uploads
- **Method**: FTP download / Hostinger backup
- **Location**:
- **Frequency**:

---

## Deployment Checklist

- [ ] Run tests locally
- [ ] Build assets if needed
- [ ] Commit and push to git
- [ ] Upload via FTP / trigger deploy
- [ ] Verify on production
- [ ] Check error logs

---

## Known Issues

- Issue 1: Description and workaround

---

## Future Plans / Roadmap

- [ ] Planned feature 1
- [ ] Planned feature 2

---

## Notes

Any additional notes, quirks, or important information about this project.

---

*Last updated: YYYY-MM-DD*
