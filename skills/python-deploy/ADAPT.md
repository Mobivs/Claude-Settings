# Porting the pipeline to a new app

Step-by-step for adding `python-deploy` to an existing Python project.

## 1. Collect required variables

Ask the user (or infer from the project) for these. Every template file uses `{{DOUBLE_BRACE}}` tokens that must be replaced.

| Token | Description | Example (Thermal Inspector) |
|-------|-------------|----------------------------|
| `{{APP_NAME}}` | Human-readable name | `Thermal Inspector` |
| `{{APP_SLUG}}` | No-space identifier (used in paths, exe name) | `ThermalInspector` |
| `{{APP_EXE}}` | Executable filename | `ThermalInspector.exe` |
| `{{APP_ID_GUID}}` | **Unique** GUID for this product (Inno Setup AppId) — generate once, never change | `B8A9D7E2-3F4C-4A5B-9E1D-6C8F2A7B3E4D` |
| `{{APP_PUBLISHER}}` | Company / publisher | `Lythix` |
| `{{APP_URL}}` | Homepage URL | `https://lythix.com` |
| `{{APP_DESC}}` | One-line description | `Professional thermal inspection software` |
| `{{ENTRY_SCRIPT}}` | Path to main Python entry point | `thermal_inspector_app.py` |
| `{{ENTRY_MODULE}}` | Python module name for smoke-test import | `thermal_inspector_app` |
| `{{UPDATE_PATH_RAW}}` | Windows path to network share (raw string) | `r"Z:\01_LYTHIX\02_PUBLIC\04_ TOOLS\01_SOFTWARE\POWERLINE INSPECTION"` |
| `{{GIT_BRANCH}}` | Main branch name | `main` |
| `{{GIT_TAG_PREFIX}}` | Prefix for release tags | `v` |
| `{{SIGNTOOL_PATH_RAW}}` | Path to signtool.exe | `r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe"` |
| `{{TIMESTAMP_URL}}` | RFC 3161 timestamp server | `http://timestamp.sectigo.com` |
| `{{MIN_WINDOWS_VERSION}}` | `MinVersion=` in installer | `10.0` |

### Generating a new GUID (required)

```powershell
powershell -Command "[guid]::NewGuid().ToString().ToUpper()"
```

Copy to `{{APP_ID_GUID}}`. **Do not reuse** Thermal Inspector's GUID for a different product — upgrades will break.

## 2. Copy template files

Copy from `~/.claude/skills/python-deploy/templates/` into the project root:

```
version.py                       → <project>/version.py
updater.py                       → <project>/updater.py
build/release.py                 → <project>/build/release.py
build/build.py                   → <project>/build/build.py
build/app.spec                   → <project>/build/{{APP_SLUG_LOWER}}.spec
build/installer.iss              → <project>/build/installer.iss
build/version_info.txt           → <project>/build/version_info.txt
build/README.md                  → <project>/build/README.md
docs/DEPLOYMENTS.md              → <project>/docs/DEPLOYMENTS.md (create if missing)
```

Do substitutions on every file before writing.

## 3. Configure PyInstaller spec

After copying `app.spec`, tailor it to the target app:

1. **`datas_list`** — add bundled assets (templates, static files, SDK binaries)
2. **`hiddenimports`** — add modules that PyInstaller can't trace (DB drivers, keyring backends, own app modules imported dynamically)
3. **`excludes`** — remove unnecessary bloat, but **never exclude `unittest`** (pyparsing needs it)
4. **`console`** — `False` for GUI apps, `True` for headless/server apps (yellow-pine keeps console to show server logs)

### Variant-specific tweaks
- **customtkinter GUI**: see [variants/customtkinter.md](variants/customtkinter.md)
- **FastAPI + static browser UI**: see [variants/fastapi-browser.md](variants/fastapi-browser.md)

## 4. Initial version bump

Pick a starting version (usually `1.0.0`) and set it in the three files. Or just set `version.py` and run:

```bash
python build/build.py --bump patch
```

This syncs `version_info.txt` and `installer.iss` via regex.

## 5. First build (without signing/deploy)

```bash
python build/release.py --bump patch --skip-sign --skip-deploy --dry-run
```

Review output. Then a real build:

```bash
python build/release.py --bump patch --skip-sign --skip-deploy
```

Inspect `dist/installer/<App>_Setup_X.Y.Z.exe`. Install it on a test machine.

## 6. Network share setup

On the delivery share:

```
{{UPDATE_PATH_RAW}}\
├── version.json
└── <App>_Setup_X.Y.Z.exe
```

Make sure client machines have the share mapped and read access. The updater fails silently if the path isn't accessible — that's by design (users without the share still run the app fine).

## 7. First real release

```bash
python build/release.py --bump patch --release-notes "Initial release"
```

Plug in the SafeNet token. Enter the PIN twice (inner `.exe`, then installer). Verify:

1. `dist/installer/<App>_Setup_X.Y.Z.exe` exists and is signed (`signtool verify /pa <path>`)
2. Signed installer + `version.json` copied to the network share
3. `docs/DEPLOYMENTS.md` has a new entry
4. Git commit made, tag `v1.0.0` created and pushed to remote

## 8. Add the in-app update check

In the app's startup code:

```python
from updater import check_for_updates_on_startup
# ... after main window is created ...
check_for_updates_on_startup(main_window)
```

For FastAPI apps the pattern is slightly different — see [variants/fastapi-browser.md](variants/fastapi-browser.md).

## 9. Wire the `/deploy` project skill (optional but recommended)

In the project's `.claude/skills/deploy/SKILL.md`, add a thin wrapper that calls this global skill with project-specific defaults. See Thermal Inspector's `.claude/skills/deploy/SKILL.md` for an example.

## Common porting mistakes

1. **Forgot to regenerate `AppId` GUID** — installer will try to upgrade over an unrelated product. Always `New-Guid`.
2. **Left `{{APP_NAME}}` placeholders in** — run a grep after substitution: `grep -r "{{" <project>/`.
3. **Wrong `ENTRY_MODULE`** — smoke test fails. It's the importable module name, not the filename (`app` not `app.py`).
4. **Forgot to add app modules to `hiddenimports`** — builds fine, crashes on launch with `ModuleNotFoundError`. The smoke test catches *most* of these.
5. **Used the same `UPDATE_PATH_RAW` as another product** — their users start getting updates for yours. Use a product-specific subfolder.
