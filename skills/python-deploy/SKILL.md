---
name: python-deploy
description: Build, sign, and deploy Windows Python apps (customtkinter GUI, FastAPI browser-UI, or NiceGUI + PyWebView). Handles PyInstaller packaging, Inno Setup installer, Sectigo EV code signing, network-share auto-update, and git tag/push. Use when setting up a new app's deployment pipeline, running a release, troubleshooting sign/install issues, or porting the pipeline between projects (e.g. ThermalInspector → inspection-master → yellow-pine).
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
9. **`UPDATE_PATH` single source of truth** — `release.py` imports from `version.py` instead of duplicating the path. Previously, editing one but not the other silently skipped the deploy step with "network share not accessible".
10. **`git add -f` in step 10** — avoids the exit-1 "paths are ignored" warning that git emits when tracked files (`build/installer.iss`, `build/version_info.txt`) live under a gitignored parent dir.

Further opt-in improvements (rollback, channels, build_info.json, etc.) are in [IMPROVEMENTS.md](IMPROVEMENTS.md).

## Variants

Different app shapes need minor template tweaks. See:
- [variants/customtkinter.md](variants/customtkinter.md) — GUI desktop apps (Thermal Inspector)
- [variants/fastapi-browser.md](variants/fastapi-browser.md) — Browser-UI apps served on `127.0.0.1` (yellow-pine)
- [variants/nicegui.md](variants/nicegui.md) — NiceGUI + PyWebView native window (inspection-master). **Read this if the variant applies** — it lists the full windowed-mode hardening checklist, the "ui.run(native=True) silently fails in a windowed build" workaround, the 3s page-handler budget, and the credential-dialog closure pitfall.

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
7. **`UPDATE_PATH` baked into the installer** — the value of `UPDATE_PATH` in `version.py` at build time is what the installed updater reads. Change the path → all previously-installed clients keep polling the old path and never see the new release. Only change `UPDATE_PATH` during the first deployment, or accept that existing installs need a manual reinstall.
8. **Group-policy-blocked Python installs** — on managed machines the python.org MSI can fail with exit 1625 (`ERROR_INSTALL_PACKAGE_REJECTED`). Use [uv](https://github.com/astral-sh/uv) to install Python user-scope: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"` then `uv python install 3.12` + `uv venv --python 3.12 venv`. If AV blocks uv's trampoline `.exe` writes during `uv pip install`, bootstrap stdlib pip into the venv with `venv/Scripts/python.exe -m ensurepip --upgrade` and use that instead.
9. **Installed builds write to `Program Files (x86)` by default** — read-only for non-admin users. `.env`, logs, caches, DBs must go under `%LOCALAPPDATA%\<AppName>` via a `get_user_data_root()` helper that checks `sys.frozen`. See [variants/nicegui.md](variants/nicegui.md) for the full windowed-mode hardening list — it applies to any windowed (`console=False`) build.
10. **`git add` exits 1 with a "paths are ignored" warning** when tracked files live under a gitignored parent (`build/installer.iss` under a `build/` gitignore entry). Git stages the files but exits non-zero. Template uses `git add -f` to bypass. If you see the pipeline fail at step 10, this is why.
11. **Silent exits in windowed builds** — native libs (pythonnet, pywebview, uvicorn C) can call `fprintf(stderr)` or `WriteFile(GetStdHandle)` on fd 1/2, which don't exist in `console=False` builds. The process exits with code 0, no crash dump, no Event Viewer entry. Redirect `sys.stdout`/`sys.stderr` AND `os.dup2` fd 1/2 to a log file, and call `faulthandler.enable()` early. Full recipe in [variants/nicegui.md](variants/nicegui.md).

## Next steps when invoked

1. **Scaffolding a new app** → read [ADAPT.md](ADAPT.md), collect required variables from the user, copy templates with substitutions.
2. **Running a release** → read the target project's `version.py`, run `python build/release.py --bump <type>`, monitor output, alert on SafeNet prompts.
3. **Improving an existing pipeline** → read [IMPROVEMENTS.md](IMPROVEMENTS.md), propose a ranked shortlist, implement the agreed items.
