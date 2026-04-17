---
name: python-deploy skill
description: Reusable global skill at ~/.claude/skills/python-deploy/ — packages the Thermal Inspector deployment pipeline as templates for new Python apps
type: reference
originSessionId: c44629ec-e370-47cd-82dc-3ae01563e66a
---
Global skill `python-deploy` at `~/.claude/skills/python-deploy/` contains reusable templates for porting the PyInstaller + Inno Setup + Sectigo EV + network-share-auto-update pipeline to new Python desktop apps.

**Use for**: scaffolding deployment into a new Python app (e.g. inspection-master, yellow-pine), running existing releases, or proposing pipeline improvements.

**Entry**: `SKILL.md` — describes when to invoke + 12-step pipeline.
**Porting guide**: `ADAPT.md` — required variables, file copying, common mistakes.
**Roadmap**: `IMPROVEMENTS.md` — opt-in enhancements beyond what's baked in.
**Variants**: `variants/customtkinter.md`, `variants/fastapi-browser.md`.
**Templates**: `templates/` — `version.py`, `updater.py`, `build/release.py`, `build/build.py`, `build/app.spec`, `build/installer.iss`, `build/version_info.txt`, `build/README.md`, `docs/DEPLOYMENTS.md`.

**Baked-in improvements over the original Thermal Inspector pipeline**:
1. Inner `.exe` signed before Inno Setup packages it (two PIN prompts per release)
2. SHA-256 in `version.json`, verified by updater before install
3. Git tag per release (`v1.2.3`)
4. Conditional git push (skipped when nothing was signed + deployed)
5. Updater tempdir cleanup on failure/cancel
6. Auto-generated release notes from `git log <last-tag>..HEAD --oneline`
7. Non-interactive `--yes` mode
8. Pre-build smoke import test

**Known candidates for this skill**: inspection-master (needs UI refactor first), yellow-pine (FastAPI/browser-UI variant).

**When Thermal Inspector's pipeline materially changes, refresh the templates here** — the skill is a reference impl, not a live fork.
