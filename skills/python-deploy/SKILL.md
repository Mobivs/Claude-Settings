---
name: python-deploy
description: Build, sign, and deploy Windows Python apps (customtkinter GUI or FastAPI browser-UI). Handles PyInstaller packaging, Inno Setup installer, Sectigo EV code signing, network-share auto-update, and git tag/push. Use when setting up a new app's deployment pipeline, running a release, troubleshooting sign/install issues, or porting the pipeline between projects (e.g. ThermalInspector → inspection-master → yellow-pine).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# python-deploy

Opinionated deployment pipeline for Windows Python apps. Extracted from Thermal Inspector, generalized for reuse.

## When to invoke

- **Scaffold** a deployment pipeline into a new Python project — see [ADAPT.md](ADAPT.md)
- **Run a release** on a project that already uses this pipeline — `python build/release.py --bump patch`
- **Troubleshoot** signing, install, or auto-update failures — see [variants/](variants/) and [IMPROVEMENTS.md](IMPROVEMENTS.md)
- **Upgrade** a project's pipeline — see [IMPROVEMENTS.md](IMPROVEMENTS.md) for the opt-in menu

## Assumptions

- Windows-only target
- Python app packaged with **PyInstaller** (folder mode, not onefile)
- **Inno Setup 6** for installer creation
- **Sectigo EV Code Signing** certificate on a **SafeNet USB token** (PIN prompt per signing operation)
- Delivery via a **network share** that users have mapped (e.g. `Z:\...`)
- Git repo; main branch is `main` (adjust per project)

## The pipeline — 12 steps

`release.py` orchestrates these. Each is skippable for partial/recovery runs.

| # | Step | Notes |
|---|------|-------|
| 0 | Pre-flight | git clean, tools present, drives mounted, SafeNet ready |
| 1 | Version bump | Updates `version.py`, `installer.iss`, `version_info.txt` |
| 2 | Smoke import test | `python -c "import <entry_module>"` — catches missing hidden imports before the 2 min build |
| 3 | PyInstaller build | → `dist/<App>/<App>.exe` |
| 4 | Sign inner `.exe` | So users launching post-install don't hit SmartScreen (1st PIN prompt) |
| 5 | Inno Setup installer | → `dist/installer/<App>_Setup_X.Y.Z.exe` |
| 6 | Sign installer | 2nd PIN prompt |
| 7 | Create `version.json` | Includes SHA-256 of installer for integrity check |
| 8 | Deploy to network share | Blocked if unsigned |
| 9 | Append to `docs/DEPLOYMENTS.md` | Release log |
| 10 | Git commit + **tag** + push | `v<version>` tag for clean rollback points |
| 11 | Summary | Prints artifact paths and status |

## Baked-in improvements vs. Thermal Inspector's original

This skill's templates include these enhancements over the Thermal Inspector source:

1. **Inner `.exe` signed** before Inno Setup packages it
2. **SHA-256 verification** — hash in `version.json`; updater verifies before launch
3. **Git tag per release** (`v1.2.3`)
4. **Conditional push** — skipped when both `--skip-sign` and `--skip-deploy` are set
5. **Updater tempdir cleanup** on failure/cancel
6. **Auto release notes** from `git log <last-tag>..HEAD --oneline` if `--release-notes` not provided
7. **Non-interactive `--yes`** mode for automation/CI
8. **Pre-build smoke import test** to fail fast

Further opt-in improvements (rollback, channels, build_info.json, etc.) are in [IMPROVEMENTS.md](IMPROVEMENTS.md).

## Variants

Different app shapes need minor template tweaks. See:
- [variants/customtkinter.md](variants/customtkinter.md) — GUI desktop apps (Thermal Inspector, inspection-master)
- [variants/fastapi-browser.md](variants/fastapi-browser.md) — Browser-UI apps served on `127.0.0.1` (yellow-pine)

## Layout this skill creates in a target project

```
<project_root>/
├── version.py                     # Single source of truth for version + update path
├── updater.py                     # In-app auto-update client with SHA-256 verify
├── build/
│   ├── release.py                 # 12-step release orchestrator
│   ├── build.py                   # Version-bump + lower-level build helpers
│   ├── <app>.spec                 # PyInstaller spec
│   ├── installer.iss              # Inno Setup script
│   ├── version_info.txt           # Windows EXE version resource
│   └── README.md                  # Build docs
└── docs/DEPLOYMENTS.md            # Append-only release log
```

## Running a release (once scaffolded)

```bash
# Most common
python build/release.py --bump patch

# With explicit release notes
python build/release.py --bump minor --release-notes "New annotation tool"

# Preview without executing
python build/release.py --bump patch --dry-run

# Automation — no prompts
python build/release.py --bump patch --yes --release-notes "CI build"

# Partial — skip signing (won't deploy either)
python build/release.py --bump patch --skip-sign

# Build and sign but don't push to network share
python build/release.py --bump patch --skip-deploy
```

The script prompts for the SafeNet PIN twice during signing (inner `.exe`, then installer). Let the user know when those steps are reached.

## Critical gotchas

1. **signtool from bash** — forward-slash flags (`/tr`, `/fd`) get eaten. ALWAYS wrap in `powershell.exe -Command "& signtool ..."`.
2. **Inno Setup on network shares** — "file in use" errors. Always `OutputDir=..\dist\installer` (local), then copy to the share.
3. **PyInstaller `unittest` exclude** — don't. `pyparsing.testing` imports it at module level.
4. **`AppId` GUID in `installer.iss`** — must be **unique per product** and **fixed for the product's lifetime**. Regenerating breaks upgrades.
5. **Unsigned EXEs on network shares** — corporate AV (Cynet) quarantines them. The pipeline blocks deploy if unsigned.
6. **Version.json points to `.exe` directly** — not `.zip`. Older ThermalInspector versions used `.zip`; a `os.remove` inside `with zipfile.ZipFile` context caused a Windows file-lock bug (WinError 32).

## Next steps when invoked

1. **Scaffolding a new app** → read [ADAPT.md](ADAPT.md), collect required variables from the user, copy templates with substitutions.
2. **Running a release** → read the target project's `version.py`, run `python build/release.py --bump <type>`, monitor output, alert on SafeNet prompts.
3. **Improving an existing pipeline** → read [IMPROVEMENTS.md](IMPROVEMENTS.md), propose a ranked shortlist, implement the agreed items.
