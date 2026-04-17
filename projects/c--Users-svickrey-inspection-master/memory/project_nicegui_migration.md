---
name: NiceGUI Migration
description: Major UI refactor from CustomTkinter to NiceGUI - 8-phase plan tracked in docs/plan-nicegui-migration.md
type: project
originSessionId: 13aefaec-0db0-4caa-80aa-2f286dd894b4
---
Full UI migration from CustomTkinter to NiceGUI, decided 2026-04-16.

**Why:** CustomTkinter cannot render markdown, rich tables, or modern formatting. The AI chat feature pushed us past the framework's limits.

**How to apply:** All new UI work goes in `src/ui_ng/`. The plan with checkboxes lives at `docs/plan-nicegui-migration.md`. Each phase must have a code review and testing pass before moving to the next. The backend (`database/`, `violation/`, `ai/`, `reports/`, `photo/`) is untouched.

**Spike**: `spike_nicegui_chat.py` proves the pattern (chat with Claude tool-calling, markdown, async IO).

**Current phase**: Phase 0 (Foundation) - NOT STARTED

**Key patterns**: `await run.io_bound()` for DB/AI calls, Tailwind classes replace ComponentStyles, `ui.dialog()` replaces Toplevel modals, `photo_server.py` for secure photo serving.
