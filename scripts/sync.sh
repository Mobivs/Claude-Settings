#!/bin/bash
#
# Sync Claude Code global settings with remote repository.
# Auto-commits only shared paths — leaves settings.json and other local
# state alone unless explicitly staged.
#
# Usage:
#   sync.sh           Full sync: pull, commit scoped paths, push
#   sync.sh --pull    Pull only (used by SessionStart hook)
#   sync.sh --push    Commit + push scoped paths (no pull)

set -e

cd "$HOME/.claude"

case "${1:-}" in
    --pull) PULL=1 ;;
    --push) PUSH=1 ;;
    "")     PULL=1; PUSH=1 ;;
    *)      echo "Usage: $0 [--pull | --push]"; exit 1 ;;
esac

# Paths that auto-sync. Everything else (settings.json, plugins/*, caches,
# session transcripts) requires manual `git add` by the user.
SCOPED_PATHS=(
    skills/
    agents/
    templates/
    scripts/
    projects/
    .gitignore
    README.md
)

if [ -n "${PULL:-}" ]; then
    # Stash dirty state so rebase can proceed. Include untracked so nothing is lost.
    DIRTY=0
    if ! git diff --quiet || ! git diff --cached --quiet; then DIRTY=1; fi
    [ "$DIRTY" = 1 ] && git stash push -u -m "sync-pull-$(date +%s)" >/dev/null
    git pull --rebase origin main
    if [ "$DIRTY" = 1 ]; then
        git stash pop >/dev/null 2>&1 || echo "WARNING: stash pop conflicted — run 'git stash list'"
    fi
fi

if [ -n "${PUSH:-}" ]; then
    # Only stage the scoped paths that we've decided should sync.
    # Paths that don't exist are silently skipped.
    git add -- "${SCOPED_PATHS[@]}" 2>/dev/null || true

    if git diff --cached --quiet; then
        echo "sync: nothing to commit"
    else
        git commit -m "auto-sync: $(date '+%Y-%m-%d %H:%M:%S')" >/dev/null
        git push origin main
        echo "sync: pushed"
    fi
fi
