# Deployment Notes

## Pipeline (as of v1.1.6+)
All builds happen locally on C: drive. No H: drive needed.

**Automated**: `python build/release.py --bump patch` (interactive terminal only, not Claude's Bash — EOFError on `input()`).

1. Bump version (version.py, version_info.txt, installer.iss)
2. PyInstaller → dist/ThermalInspector/ (local, default output)
3. Inno Setup → dist/installer/ (reads from dist/ThermalInspector/)
4. Sign the .exe via PowerShell (bash eats signtool flags)
5. Create version.json (points to .exe, not .zip)
6. Copy signed .exe + version.json → Z: drive
7. Update docs/DEPLOYMENTS.md
8. Git commit + push

## Drive Paths
- **Z:\01_LYTHIX\02_PUBLIC\04_ TOOLS\01_SOFTWARE\POWERLINE INSPECTION** — Network share for auto-updates
- **Cynet**: Quarantines unsigned .exe files on Z: drive. Only deploy signed .exe there.
- **H:\BUILD** — No longer used (was staging area, eliminated in v1.1.3+)

## Key Changes from Old Pipeline
- No more H: drive (was slow external USB, 20 min COLLECT phase)
- No more .zip wrapping — version.json points to .exe directly
- The old zip path had a Windows file-lock bug: `os.remove()` inside `with zipfile.ZipFile()` caused WinError 32
- Updater code still handles both .exe and .zip, but we always deploy .exe to avoid the bug

## Build Gotchas
- **signtool via bash**: Forward-slash flags (`/fd`, `/tr`) get eaten by git bash. Use `powershell.exe -Command "& signtool ..."` instead.
- **unittest exclude**: Do NOT exclude `unittest` in PyInstaller spec — `pyparsing.testing` imports it.
- **Inno Setup "file in use"**: If output dir gets locked, use `/O` override to output elsewhere.

## Signing
- Tool: `C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe`
- Flags: `/tr http://timestamp.sectigo.com /td SHA256 /fd SHA256 /a`
- SafeNet USB token required, PIN dialog appears during signing
- Must sign BEFORE deploying to Z: drive

## Inno Setup Paths (search order)
1. C:\Users\SVickrey\AppData\Local\Programs\Inno Setup 6\ISCC.exe
2. C:\Program Files (x86)\Inno Setup 6\ISCC.exe
3. C:\Program Files\Inno Setup 6\ISCC.exe
