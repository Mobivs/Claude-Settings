<#
.SYNOPSIS
    Sync Claude Code global settings with remote repository.

.DESCRIPTION
    Pulls latest changes, commits any local modifications, and pushes to remote.
    Designed to be run manually or via Task Scheduler.

.PARAMETER Pull
    Only pull changes, don't commit/push local changes.

.PARAMETER Push
    Only commit and push local changes, don't pull.

.EXAMPLE
    .\sync.ps1
    Full sync (pull, commit, push)

.EXAMPLE
    .\sync.ps1 -Pull
    Only pull latest changes

.EXAMPLE
    .\sync.ps1 -Push
    Only commit and push local changes
#>

param(
    [switch]$Pull,
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$ClaudeDir = "$env:USERPROFILE\.claude"

# Colors for output
function Write-Success { param($msg) Write-Host $msg -ForegroundColor Green }
function Write-Info { param($msg) Write-Host $msg -ForegroundColor Cyan }
function Write-Warn { param($msg) Write-Host $msg -ForegroundColor Yellow }

# Change to .claude directory
Push-Location $ClaudeDir

try {
    # Check if this is a git repository
    if (-not (Test-Path ".git")) {
        Write-Error "Not a git repository. Initialize with 'git init' first."
        exit 1
    }

    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    # Pull changes (unless -Push only)
    if (-not $Push) {
        Write-Info "[$timestamp] Pulling latest changes..."

        # Stash any uncommitted changes
        $stashOutput = git stash 2>&1
        $hasStash = $stashOutput -notmatch "No local changes"

        # Pull with rebase
        git pull --rebase origin main 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Warn "Pull failed. You may need to resolve conflicts manually."
            if ($hasStash) {
                git stash pop 2>&1
            }
            exit 1
        }

        # Restore stashed changes
        if ($hasStash) {
            git stash pop 2>&1
        }

        Write-Success "Pull complete."
    }

    # Push changes (unless -Pull only)
    if (-not $Pull) {
        Write-Info "[$timestamp] Checking for local changes..."

        # Stage all changes
        git add -A

        # Check if there are changes to commit
        $status = git status --porcelain
        if ($status) {
            Write-Info "Changes detected:"
            git status --short

            # Create commit message
            $commitMsg = "Auto-sync: $timestamp"

            # Check what changed for a better commit message
            $diffStat = git diff --cached --stat
            if ($diffStat -match "skills/") {
                $commitMsg = "Update skills - $timestamp"
            }
            elseif ($diffStat -match "agents/") {
                $commitMsg = "Update agents - $timestamp"
            }
            elseif ($diffStat -match "templates/") {
                $commitMsg = "Update templates - $timestamp"
            }
            elseif ($diffStat -match "settings") {
                $commitMsg = "Update settings - $timestamp"
            }

            # Commit
            git commit -m $commitMsg 2>&1
            Write-Success "Committed: $commitMsg"

            # Push
            Write-Info "Pushing to remote..."
            git push origin main 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Warn "Push failed. You may need to push manually."
                exit 1
            }
            Write-Success "Push complete."
        }
        else {
            Write-Info "No local changes to commit."
        }
    }

    Write-Success "`n[OK] Claude settings sync complete!"

}
catch {
    Write-Error "Sync failed: $_"
    exit 1
}
finally {
    Pop-Location
}
