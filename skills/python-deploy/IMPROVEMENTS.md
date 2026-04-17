# Improvements roadmap

The templates already include the high-value, low-effort improvements from the original Thermal Inspector pipeline. This file tracks further enhancements — opt in per project as needs arise.

## Already baked in (see [SKILL.md](SKILL.md))

1. Sign inner `.exe` (not just installer)
2. SHA-256 in `version.json`, verified in updater
3. Git tag per release (`v1.2.3`)
4. Conditional push (skipped when nothing was signed + deployed)
5. Updater tempdir cleanup on failure/cancel
6. Auto release notes from `git log <last-tag>..HEAD --oneline`
7. Non-interactive `--yes` mode
8. Pre-build smoke import test

## Opt-in enhancements

### Rollback command (medium value)
Add `release.py --rollback` that restores the previous `version.json` from `version.json.prev` on the network share. Every successful deploy saves the previous copy before overwriting. Useful when a bad release ships.

**Implementation:** 20 lines in `release.py`. Needs a `save_previous_version_json()` step before overwriting, and a `do_rollback()` branch parallel to `do_deploy()`.

### `build_info.json` alongside installer (low value)
Capture `git rev-parse HEAD`, `python --version`, `pip freeze` hash, build timestamp. Helps answer "which build is this user on?" when debugging. Write next to the installer on the share.

### Channels: stable / beta (medium value, defer)
Two `version.json` files on the share: `version.json` (stable) and `version-beta.json`. App has a setting to opt into beta. Useful once you have >10 users and want to dogfood before full rollout.

**Implementation:** 50 lines — new `--channel stable|beta` flag in `release.py`, new `channel` setting in the app, second URL in `updater.py`.

### Prune old installers on share (low value)
Share grows unbounded. Keep last N versions, archive older. Low priority until the share has 20+ versioned installers.

### Retained build artifacts (low value)
`dist/installer/` gets clobbered every build. For audit, copy `<App>_Setup_X.Y.Z.exe` to `dist/archive/` too. Cheap, and you can always re-sign/re-deploy from archive.

### Parallel signing via session PIN cache (defer — may break HSM policy)
SafeNet has a "single logon" option that caches the PIN for the session. Would cut 2 prompts to 1. May violate EV code-signing policy depending on CA — don't enable without confirming.

### Pin `pyinstaller` in requirements.txt (trivial, do this)
Lock the PyInstaller version so builds are reproducible across machines. Add to `requirements.txt`: `pyinstaller==<current-version>`.

### Generate `installer.iss` + `version_info.txt` from `version.py` (medium effort)
Currently updated via regex. Templates would be cleaner. Worth it once a cross-project bug bites — until then, regex works.

## Process improvements (no code change)

### `docs/DEPLOYMENTS.md` discipline
Keep entries short: version, date, key changes, signed/deployed status. The release script appends automatically. Don't hand-edit unless correcting an error.

### PR + release cadence
Land PRs to `main`, run release from `main`. Avoid releasing from feature branches — the git tag then points at a ref that may be rebased.

### Test on a non-dev machine
Install from the network share on a clean VM / fresh user before announcing the release. Catches "works on my box" issues.

## How to add a new improvement

1. Prototype in one project (usually Thermal Inspector — the reference implementation)
2. Verify across a release cycle
3. Port to the skill's templates
4. Add to the "Already baked in" section above
5. If it's non-trivial, add a short commit message in the template file explaining the rationale
