<#
.SYNOPSIS
    Install git hooks for Claude Code settings repository.

.DESCRIPTION
    Copies hook scripts from the scripts/hooks directory to .git/hooks
    and makes them executable. Run this after cloning to a new machine.
#>

$ClaudeDir = "$env:USERPROFILE\.claude"
$HooksDir = "$ClaudeDir\.git\hooks"

Write-Host "Installing git hooks..." -ForegroundColor Cyan

# Ensure hooks directory exists
if (-not (Test-Path $HooksDir)) {
    New-Item -ItemType Directory -Path $HooksDir -Force | Out-Null
}

# Pre-commit hook content
$PreCommitHook = @'
#!/bin/bash
#
# Pre-commit hook for Claude Code global settings repository
# Validates JSON files and skill frontmatter before allowing commits
#

echo "Running pre-commit validation..."

ERRORS=0

# Validate JSON files
for file in settings.json plugins/installed_plugins.json plugins/known_marketplaces.json; do
    if [ -f "$file" ]; then
        if git diff --cached --name-only | grep -q "^$file$"; then
            if ! python -m json.tool "$file" > /dev/null 2>&1; then
                echo "ERROR: Invalid JSON in $file"
                ERRORS=$((ERRORS + 1))
            else
                echo "  OK: $file"
            fi
        fi
    fi
done

# Validate skill frontmatter
for skill in skills/*/SKILL.md; do
    if [ -f "$skill" ]; then
        if git diff --cached --name-only | grep -q "^$skill$"; then
            if ! head -1 "$skill" | grep -q "^---"; then
                echo "ERROR: Missing frontmatter in $skill"
                ERRORS=$((ERRORS + 1))
            else
                echo "  OK: $skill"
            fi
        fi
    fi
done

# Validate agent frontmatter
for agent in agents/*.md; do
    if [ -f "$agent" ]; then
        if git diff --cached --name-only | grep -q "^$agent$"; then
            if ! head -1 "$agent" | grep -q "^---"; then
                echo "ERROR: Missing frontmatter in $agent"
                ERRORS=$((ERRORS + 1))
            else
                echo "  OK: $agent"
            fi
        fi
    fi
done

# Check for credentials
if git diff --cached --name-only | grep -qE "\.credentials\.json|\.vibe9-token|\.secret|\.key|\.pem"; then
    echo "ERROR: Attempting to commit sensitive files!"
    ERRORS=$((ERRORS + 1))
fi

if [ $ERRORS -gt 0 ]; then
    echo "Pre-commit validation failed with $ERRORS error(s)."
    exit 1
fi

echo "Pre-commit validation passed!"
exit 0
'@

# Write pre-commit hook
$PreCommitPath = "$HooksDir\pre-commit"
$PreCommitHook | Out-File -FilePath $PreCommitPath -Encoding utf8 -NoNewline

Write-Host "  Installed: pre-commit" -ForegroundColor Green

Write-Host "`nGit hooks installed successfully!" -ForegroundColor Green
Write-Host "The pre-commit hook will validate your files before each commit." -ForegroundColor Cyan
