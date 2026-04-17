---
name: Releases must be done from the signing machine
description: Thermal Inspector releases require SafeNet + signtool, which only live on a separate machine — not this dev box
type: project
originSessionId: e14add26-9713-4d62-b634-d157cfd7b8ee
---
Thermal Inspector releases (`python build/release.py`) cannot be completed on this dev box (`c:\Users\SVickrey\ThermalInspector-Private`). The Windows SDK signtool is not installed here (Windows Kits 10 has no `bin/` directory at all), and the SafeNet hardware key is plugged into a different machine.

**Why:** Cynet quarantines unsigned binaries deployed to `Z:\01_LYTHIX\02_PUBLIC\04_ TOOLS\01_SOFTWARE\POWERLINE INSPECTION` immediately, so a build without signing is useless for distribution. The release script's `--skip-sign` mode auto-skips the Z: deploy for that reason.

**How to apply:** When the user asks to deploy/release from this dev box, do the source side here (commit + push code changes), then explicitly remind them they need to run the release script on their signing machine. The user has self-reported "I keep forgetting" — proactive flag is welcome.
