#!/bin/bash
#
# Sync Claude Code global settings with remote repository.
# Pulls latest changes, commits any local modifications, and pushes to remote.
#
# Usage:
#   ./sync.sh           Full sync (pull, commit, push)
#   ./sync.sh --pull    Only pull latest changes
#   ./sync.sh --push    Only commit and push local changes
#

set -e

CLAUDE_DIR="$HOME/.claude"
PULL_ONLY=false
PUSH_ONLY=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --pull|-p)
            PULL_ONLY=true
            shift
            ;;
        --push|-P)
            PUSH_ONLY=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--pull | --push]"
            exit 1
            ;;
    esac
done

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

info() { echo -e "${CYAN}$1${NC}"; }
success() { echo -e "${GREEN}$1${NC}"; }
warn() { echo -e "${YELLOW}$1${NC}"; }

cd "$CLAUDE_DIR"

# Check if git repo
if [ ! -d ".git" ]; then
    echo "Error: Not a git repository. Initialize with 'git init' first."
    exit 1
fi

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Pull changes (unless --push only)
if [ "$PUSH_ONLY" = false ]; then
    info "[$TIMESTAMP] Pulling latest changes..."

    # Stash any uncommitted changes
    STASH_OUTPUT=$(git stash 2>&1)
    HAS_STASH=false
    if [[ ! "$STASH_OUTPUT" =~ "No local changes" ]]; then
        HAS_STASH=true
    fi

    # Pull with rebase
    if ! git pull --rebase origin main 2>&1; then
        warn "Pull failed. You may need to resolve conflicts manually."
        if [ "$HAS_STASH" = true ]; then
            git stash pop 2>&1 || true
        fi
        exit 1
    fi

    # Restore stashed changes
    if [ "$HAS_STASH" = true ]; then
        git stash pop 2>&1 || true
    fi

    success "Pull complete."
fi

# Push changes (unless --pull only)
if [ "$PULL_ONLY" = false ]; then
    info "[$TIMESTAMP] Checking for local changes..."

    # Stage all changes
    git add -A

    # Check if there are changes to commit
    if ! git diff --cached --quiet; then
        info "Changes detected:"
        git status --short

        # Create commit message based on what changed
        DIFF_STAT=$(git diff --cached --stat)
        COMMIT_MSG="Auto-sync: $TIMESTAMP"

        if echo "$DIFF_STAT" | grep -q "skills/"; then
            COMMIT_MSG="Update skills - $TIMESTAMP"
        elif echo "$DIFF_STAT" | grep -q "agents/"; then
            COMMIT_MSG="Update agents - $TIMESTAMP"
        elif echo "$DIFF_STAT" | grep -q "templates/"; then
            COMMIT_MSG="Update templates - $TIMESTAMP"
        elif echo "$DIFF_STAT" | grep -q "settings"; then
            COMMIT_MSG="Update settings - $TIMESTAMP"
        fi

        # Commit
        git commit -m "$COMMIT_MSG"
        success "Committed: $COMMIT_MSG"

        # Push
        info "Pushing to remote..."
        if ! git push origin main 2>&1; then
            warn "Push failed. You may need to push manually."
            exit 1
        fi
        success "Push complete."
    else
        info "No local changes to commit."
    fi
fi

success ""
success "[OK] Claude settings sync complete!"
