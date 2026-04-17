# Building & Releasing {{APP_NAME}}

## Quick release

```bash
python build/release.py --bump patch
```

One command → version bump → smoke test → build → sign (2 PIN prompts) → installer → SHA-256'd `version.json` → network share → deployment log → git commit + tag + push.

## Release flags

| Flag | Purpose |
|------|---------|
| `--bump {major,minor,patch}` | Required. Semver bump type. |
| `--release-notes "..."` | Optional. Auto-generated from git log since last tag otherwise. |
| `--dry-run` | Print each step without executing. |
| `--yes` | Non-interactive — auto-yes to all prompts (CI). |
| `--skip-sign` | Skip code signing. **Deploy is also skipped** because AV quarantines unsigned EXEs on network shares. |
| `--skip-deploy` | Build + sign but don't push to the share. Useful for local testing. |

## Prerequisites

1. **Python 3.10+**
2. **PyInstaller** (`pip install pyinstaller`)
3. **Inno Setup 6** — [jrsoftware.org](https://jrsoftware.org/isdl.php)
4. **Windows SDK** — for `signtool.exe`
5. **SafeNet Authentication Client** + **Sectigo EV certificate** on USB token

## What gets signed

**Both** the inner `.exe` (inside the installer) and the installer `.exe` itself. Two PIN prompts per release — one for each. This ensures users don't hit SmartScreen warnings when they launch the app post-install.

## Signtool via PowerShell (important)

Git Bash eats forward-slash signtool flags (`/tr`, `/fd`, `/a` get misinterpreted as paths). The pipeline wraps signtool calls in `powershell.exe -Command "& signtool ..."` automatically.

## File layout

```
build/
├── release.py              # Full pipeline (use this)
├── build.py                # Lower-level: version bump, PyInstaller, Inno Setup
├── {{APP_SLUG_LOWER}}.spec # PyInstaller configuration
├── installer.iss           # Inno Setup script
├── version_info.txt        # Windows EXE version resource
└── README.md               # This file

dist/                       # Output (git-ignored)
├── {{APP_SLUG}}/           # PyInstaller output (inner .exe lives here)
└── installer/              # Signed installer + version.json
```

## Troubleshooting

### Signtool "SignTool Error: No certificates were found..."
- SafeNet USB token not plugged in, OR
- SafeNet Authentication Client not running, OR
- Token locked (too many PIN failures) — contact Sectigo support

### PyInstaller "No module named X" at runtime
Add `X` to `hiddenimports` in `{{APP_SLUG_LOWER}}.spec`. The smoke-test step (step 2) catches most of these before the full build.

### Inno Setup "file in use" error
The `OutputDir=..\dist\installer` means Inno writes locally — not to the share. If it still errors, close Explorer windows showing `dist/installer/` and retry.

### SHA-256 mismatch in updater
Usually means network copy got corrupted or the installer on the share was replaced between `version.json` write and the user's download. Re-run the release to regenerate both.

### `docs/DEPLOYMENTS.md` out of order
The release script inserts new entries at the top (after the `---` header). If the file is missing or malformed, the release will recreate it with a fresh header.
