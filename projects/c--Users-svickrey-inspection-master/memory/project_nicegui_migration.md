---
name: NiceGUI Migration
description: UI refactor from CustomTkinter to NiceGUI - all phases complete as of 2026-04-17
type: project
originSessionId: 13aefaec-0db0-4caa-80aa-2f286dd894b4
---
Full UI migration from CustomTkinter to NiceGUI. COMPLETE as of 2026-04-17.

**Why:** CustomTkinter cannot render markdown, rich tables, or modern formatting. The AI chat feature pushed us past the framework's limits.

**How to apply:** All UI work is in `src/ui_ng/`. The old `src/ui/` has been deleted. `python src/main.py` launches NiceGUI natively via PyWebView. Backend (`database/`, `violation/`, `ai/`, `reports/`, `photo/`) is untouched.

**Key patterns**: `await run.io_bound()` for DB/AI calls, Tailwind classes replace ComponentStyles, `ui.dialog()` replaces Toplevel modals, `photo_server.py` + `report_server.py` for secure file serving, global inspection context via `InspectionSelector` singleton in `ui_ng/inspection_context.py`.

## Phase Status (as of 2026-04-17)
- Phase 0 Foundation: COMPLETE
- Phase 1 App Shell + Chat: COMPLETE
- Phase 2 Inspection Panel: COMPLETE
- Phase 3 Violation Panel: COMPLETE
- Phase 4 Material Picker: COMPLETE
- Phase 5 Report Panel: COMPLETE
- Phase 6 Menus + Shortcuts + Backup: NOT STARTED (deferred post-deployment)
- Phase 7 Cleanup: COMPLETE (src/ui/ deleted, customtkinter removed, main.py simplified)

## Known open issues (carry into next session)
- Test suite broken: `tests/smoke/ui/` and `tests/integration/ui/` import deleted `src/ui/` - need rewrite or removal
- `--debug` flag in main.py is parsed but not wired through to NiceGUI
- `requirements.txt` pins are loose (`nicegui>=2.0.0`, `pywebview>=4.0.0`) - actual tested: nicegui 3.x, pywebview 6.2.1. Tighten before packaging
- `src/violation/templates.py` was deleted - confirm no remaining imports before deployment
- Phase 6 still open: no menu bar, no keyboard shortcuts (Ctrl+N, F11), no backup dialog
