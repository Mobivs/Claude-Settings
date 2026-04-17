# ThermalInspector Project Memory

## Deployment Pipeline
- See [deployment.md](deployment.md) for detailed build/deploy notes
- **Global skill `python-deploy`** at `~/.claude/skills/python-deploy/` — templates to port this pipeline to new apps (inspection-master, yellow-pine). See [python_deploy_skill.md](python_deploy_skill.md)
- **PENDING (target 2026-04-17)**: Pipeline back-port uncommitted in working tree — see [pipeline_backport_pending.md](pipeline_backport_pending.md)
- Current version: 1.1.13 (as of 2026-04-17)
- Use `/deploy` skill for automated deployments
- `build/release.py` automates full pipeline (requires interactive terminal, not Claude's Bash)
- Pipeline builds entirely on C: drive (~2 min), no H: drive needed

## Key Architecture
- Python + customtkinter (dark mode GUI), PostgreSQL backend
- PyInstaller for packaging, Inno Setup 6 for installer
- Sectigo EV code signing via SafeNet USB token
- Auto-updater checks Z: drive `version.json`

## Critical Lessons
- **signtool in bash**: Forward-slash flags get eaten. MUST use PowerShell wrapper.
- **version.json must point to .exe**: All users are on 1.1.4+. Using `.exe` directly avoids the zip file-lock bug (WinError 32: `os.remove` inside `with zipfile.ZipFile` context). No more .zip in the pipeline.
- **Cynet quarantine**: Only affects unsigned EXEs on network shares (Z:). C: drive is safe. Signed EXEs are safe everywhere.
- **Inno Setup on network drives**: Gets "file in use" errors. Always output locally to dist\installer\.
