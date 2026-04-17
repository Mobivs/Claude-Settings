<#
.SYNOPSIS
    Sync Claude Code global settings with remote repository.
.DESCRIPTION
    Auto-commits only scoped paths (skills, agents, templates, scripts, project memories,
    .gitignore, README). Everything else (settings.json, plugins/*, caches) requires
    manual `git add`. Keeps settings drift out of the shared repo.
.PARAMETER Pull   Pull only.
.PARAMETER Push   Commit + push scoped paths only.
#>
param([switch]$Pull, [switch]$Push)

$ErrorActionPreference = "Stop"
$ClaudeDir = "$env:USERPROFILE\.claude"

# Paths that auto-sync. Mirror of sync.sh SCOPED_PATHS.
$ScopedPaths = @(
    'skills/', 'agents/', 'templates/', 'scripts/', 'projects/',
    '.gitignore', 'README.md'
)

Push-Location $ClaudeDir
try {
    if (-not (Test-Path ".git")) { throw "Not a git repository." }

    # Default: do both
    if (-not $Pull -and -not $Push) { $Pull = $true; $Push = $true }

    if ($Pull) {
        $dirty = $false
        git diff --quiet 2>$null; if ($LASTEXITCODE -ne 0) { $dirty = $true }
        git diff --cached --quiet 2>$null; if ($LASTEXITCODE -ne 0) { $dirty = $true }
        if ($dirty) { git stash push -u -m "sync-pull-$(Get-Date -Format s)" | Out-Null }

        git pull --rebase origin main
        if ($LASTEXITCODE -ne 0) { throw "Pull failed." }

        if ($dirty) {
            git stash pop 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) { Write-Warning "stash pop conflicted - run 'git stash list'" }
        }
    }

    if ($Push) {
        git add -- $ScopedPaths 2>$null | Out-Null

        git diff --cached --quiet 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "sync: nothing to commit"
        } else {
            $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            git commit -m "auto-sync: $ts" | Out-Null
            git push origin main
            if ($LASTEXITCODE -ne 0) { throw "Push failed." }
            Write-Host "sync: pushed"
        }
    }
}
finally {
    Pop-Location
}
