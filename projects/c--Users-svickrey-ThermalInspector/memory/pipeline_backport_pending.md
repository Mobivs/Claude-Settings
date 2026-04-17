---
name: Pipeline back-port pending test + commit
description: Thermal Inspector pipeline improvements (inner-exe sign, SHA-256, git tags, smoke test, auto notes, --yes) are in working tree uncommitted. Needs test + commit before next release. Target 2026-04-17.
type: project
originSessionId: c44629ec-e370-47cd-82dc-3ae01563e66a
---
**Status**: 8 pipeline improvements from the `python-deploy` skill have been back-ported to Thermal Inspector but are **uncommitted** in the working tree as of 2026-04-17. The user is actively developing on the app and wanted to defer the test + commit.

**Why:** Pipeline had known issues — unsigned inner .exe triggered SmartScreen post-install; no hash verification of downloaded installers; git history lacked release tags; interactive-only; no pre-build import sanity check. These were designed and scoped together in the skill build-out, then back-ported for consistency.

**How to apply (today — 2026-04-17):**

1. **Review diffs** — three files touched:
   - `build/release.py` — near-full rewrite, 12 steps instead of 10
   - `updater.py` — SHA-256 verify + tempdir cleanup (back-compat: `sha256` is optional in `version.json`, old releases still work)
   - `.claude/skills/deploy/SKILL.md` — updated docs
   `git diff build/release.py updater.py .claude/skills/deploy/SKILL.md`

2. **Syntax-checked, dry-run passes** — all 12 steps render correctly, conditional git-push skip triggers when nothing shipped. Not yet exercised with live SafeNet signing.

3. **Test before committing**: `python build/release.py --bump patch --skip-deploy` — exercises the two SafeNet PIN prompts (inner .exe, then installer). Verify both signatures with `signtool verify /pa` on the installer AND on the extracted inner .exe inside it. Bumps version to 1.1.14 but `--skip-deploy` keeps it off Z:.

4. **Commit pipeline changes separately from a deploy** — so the release tag points at production code, not pipeline rework. Suggested:
   ```
   git add build/release.py updater.py .claude/skills/deploy/SKILL.md
   git commit -m "feat: pipeline improvements - inner-exe signing, SHA-256 verify, git tags, smoke test"
   ```
   Then deploy normally after.

5. **If test fails**: `git checkout build/release.py updater.py .claude/skills/deploy/SKILL.md` reverts cleanly. Skill templates at `~/.claude/skills/python-deploy/` are unaffected.

**Watch out for:**
- The smoke-test step runs `python -c "import thermal_inspector_app"` after the version bump. If any import-time code is broken, version.py will already show the new number — either fix-and-continue or manually revert version.py.
- First release will have no prior `v*` tag, so auto-release-notes falls back to last 10 commits. Expected behavior.
- Two PIN prompts per release now. User needs to enter it twice.
