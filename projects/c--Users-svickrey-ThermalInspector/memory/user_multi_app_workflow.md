---
name: Multi-app Windows Python desktop workflow
description: User develops several Windows Python desktop apps sharing a common PyInstaller + Inno Setup + Sectigo EV + network-share pipeline. Moving from customtkinter to FastAPI+browser-UI for newer apps.
type: user
originSessionId: c44629ec-e370-47cd-82dc-3ae01563e66a
---
User develops multiple Windows Python desktop applications that share a common deployment pattern.

**Active apps** (as of 2026-04-17):
- **ThermalInspector** (`C:\Users\svickrey\ThermalInspector`) — customtkinter GUI, mature, v1.1.13, reference implementation for the shared deployment pipeline
- **inspection-master** (`C:\Users\svickrey\inspection-master`) — customtkinter GUI, NEC/electrical inspection, undergoing UI refactor before first deployment via shared pipeline
- **yellow-pine** (`C:\Users\svickrey\yellow-pine`) — FastAPI/uvicorn + browser UI for power-line defect detection training. This is the new pattern for future desktop apps.

**Architectural direction:** Moving from customtkinter to FastAPI-served browser UIs "for more control of the graphics" on newer apps. ThermalInspector + inspection-master stay customtkinter; yellow-pine and beyond use the browser-UI pattern.

**Shared deployment pipeline:** PyInstaller → Inno Setup → Sectigo EV sign (SafeNet USB token) → SHA-256'd `version.json` → network-share (`Z:\...`) → git tag + push. Global skill `python-deploy` at `~/.claude/skills/python-deploy/` has the templates + `variants/customtkinter.md` and `variants/fastapi-browser.md` for the two UI shapes.

**How to apply:** When discussing deployment, UI patterns, or architecture across these apps, note which pattern applies. When porting between apps, use the python-deploy skill rather than re-solving from scratch.
