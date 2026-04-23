---
name: shared.env Tier 2 ACL Hardening
description: Open task — request AD group from IT to fully restrict read access on shared.env. Tier 1 (write-restrict) already done.
type: project
originSessionId: b6cb14a8-329e-4e4b-80ec-fb8450453c64
---
`Z:\01_LYTHIX\02_PUBLIC\04_ TOOLS\01_SOFTWARE\NEC INSPECTION\shared.env`
holds team-wide secrets (Postgres password, OpenAI key, Perplexity key)
for the NEC Inspection App. Read at startup as a baseline; users can
override per-machine via `%LOCALAPPDATA%\NEC Inspection App\.env`.

**Tier 1 done (2026-04-24):** Disabled inheritance, dropped
`LYTHIX\Domain Users` from `FullControl` to `Read, Synchronize`. Random
Lythix accounts can still read but can no longer overwrite the file and
break every NEC App on the network.

**Tier 2 open — needs IT involvement:**

- Open a ticket asking IT to create an AD group, e.g.
  `LYTHIX\NEC-Inspection-Users`, with members = everyone who runs the
  NEC Inspection App.
- Once the group exists: move `shared.env` into a folder where only
  that group has Read and only Scott + Admins have Write. Drop
  `Domain Users` from the ACL entirely.
- Update [src/ui_ng/main.py](src/ui_ng/main.py)'s shared.env loader path
  if the file location changes.

**Why:** Tier 1 prevents tampering. Tier 2 also prevents read access
from non-team Lythix employees, which is the right default for DB
credentials and API keys (even shared ones).

**How to apply:** When closing this task, verify the new folder ACL
with `(Get-Acl <path>).Access`, then confirm the app still reads creds
on a fresh-install test.
