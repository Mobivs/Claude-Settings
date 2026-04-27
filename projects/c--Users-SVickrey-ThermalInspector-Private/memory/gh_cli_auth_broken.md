---
name: gh CLI auth fails to persist on this dev box
description: gh auth login completes the OAuth flow with GitHub but the token never lands in Windows Credential Manager — likely corporate policy on this box
type: project
originSessionId: e14add26-9713-4d62-b634-d157cfd7b8ee
---
`gh auth login` on this dev box (`c:\Users\SVickrey\ThermalInspector-Private`) completes the device flow with GitHub successfully (browser shows "Congratulations, you're all set!") but the OAuth token never gets written to Windows Credential Manager, so `gh auth status` keeps reporting not logged in. Verified 2026-04-17: only one `gh.exe` exists (`C:\Program Files\GitHub CLI\gh.exe`, v2.91.0), no `hosts.yml` anywhere, no `gh:github.com` entry in `cmdkey /list` (only the GCM `git:https://github.com` entry from regular git push). Likely cause: corporate group policy blocking gh's WCM write.

**Why:** Without persisted auth, `gh issue create`, `gh pr create`, etc. don't work — every CLI invocation fails with "not logged in." Don't waste a session looping on `gh auth login` thinking the user botched the flow.

**How to apply:** When the user asks to file an issue / open a PR / interact with GitHub from this box, skip `gh auth login` entirely. Two working alternatives:
1. **Save the draft to a file** under `docs/known-issues/` (issues) or as a PR description doc, and have the user paste into GitHub web UI later. This is what we did 2026-04-17 for the "Reports only filter" bug.
2. **Try `gh auth login --insecure-storage`** — bypasses WCM and writes plaintext to `%APPDATA%\GitHub CLI\hosts.yml`. Untested as of 2026-04-17 (user opted to skip).

If the user wants the GitHub-CLI workflow long term, suggest option 2 as a one-time fix. Otherwise, the file-draft workflow is fine.
