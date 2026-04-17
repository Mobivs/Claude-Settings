---
name: Release script only commits version-bump files, not code
description: build/release.py git-adds only version.py + version_info.txt + installer.iss + DEPLOYMENTS.md — code changes must be committed first
type: project
originSessionId: e14add26-9713-4d62-b634-d157cfd7b8ee
---
`build/release.py` step 7 runs `git add version.py build/version_info.txt build/installer.iss docs/DEPLOYMENTS.md` and commits only those. Any other working-tree changes (actual feature/bug code) are NOT committed by the script — but PyInstaller still bundles them into the binary because it reads the working tree.

**Why:** This creates a footgun where the deployed `.exe` contains code that doesn't exist on `origin/main`. Future debugging via git history will be misleading.

**How to apply:** Before running the release script, check `git status` and commit/push any uncommitted code changes as their own commit. Then run the release script — its version-bump commit will land cleanly on top of the real code commit. The user confirmed this approach (commit code first, then release) on 2026-04-16.
