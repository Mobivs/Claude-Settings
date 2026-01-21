<#
.SYNOPSIS
    Set up Claude Code global settings on a new Windows machine.

.DESCRIPTION
    Clones the Claude global settings repository and configures the new machine.
    Run this script AFTER running Claude Code once to generate initial files.

.PARAMETER RepoUrl
    The Git repository URL for your Claude settings.
    Default: Prompts for input.

.EXAMPLE
    .\setup-new-machine.ps1
    Interactive setup

.EXAMPLE
    .\setup-new-machine.ps1 -RepoUrl "https://github.com/user/claude-settings.git"
    Non-interactive setup with provided URL
#>

param(
    [string]$RepoUrl
)

$ErrorActionPreference = "Stop"
$ClaudeDir = "$env:USERPROFILE\.claude"
$BackupDir = "$env:USERPROFILE\.claude-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

function Write-Success { param($msg) Write-Host $msg -ForegroundColor Green }
function Write-Info { param($msg) Write-Host $msg -ForegroundColor Cyan }
function Write-Warn { param($msg) Write-Host $msg -ForegroundColor Yellow }
function Write-Step { param($num, $msg) Write-Host "`n[$num] $msg" -ForegroundColor Magenta }

Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║         Claude Code Global Settings - New Machine Setup           ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Check prerequisites
Write-Step 1 "Checking prerequisites..."

# Check for Git
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "Git is not installed. Please install Git first."
    exit 1
}
Write-Success "  Git: OK"

# Check if Claude has been run (has .claude directory)
if (-not (Test-Path $ClaudeDir)) {
    Write-Warn @"

  The .claude directory doesn't exist yet.
  Please run 'claude' once to generate initial configuration, then run this script again.

"@
    exit 1
}
Write-Success "  .claude directory: OK"

# Check for credentials
$CredentialsFile = "$ClaudeDir\.credentials.json"
if (-not (Test-Path $CredentialsFile)) {
    Write-Warn @"

  No credentials found. Please authenticate Claude Code first:
  1. Run 'claude'
  2. Complete the authentication flow
  3. Run this script again

"@
    exit 1
}
Write-Success "  Credentials: OK"

# Get repository URL
Write-Step 2 "Repository configuration..."

if (-not $RepoUrl) {
    $RepoUrl = Read-Host "Enter your Claude settings Git repository URL"
}

if (-not $RepoUrl) {
    Write-Error "Repository URL is required."
    exit 1
}

# Backup existing directory
Write-Step 3 "Backing up existing configuration..."

Write-Info "  Moving $ClaudeDir to $BackupDir"
Move-Item -Path $ClaudeDir -Destination $BackupDir -Force
Write-Success "  Backup created: $BackupDir"

# Clone repository
Write-Step 4 "Cloning settings repository..."

try {
    git clone $RepoUrl $ClaudeDir 2>&1
    Write-Success "  Repository cloned successfully"
}
catch {
    Write-Warn "  Clone failed. Restoring backup..."
    Move-Item -Path $BackupDir -Destination $ClaudeDir -Force
    Write-Error "Failed to clone repository: $_"
    exit 1
}

# Restore machine-specific files
Write-Step 5 "Restoring machine-specific files..."

# Credentials (required)
$CredBackup = "$BackupDir\.credentials.json"
if (Test-Path $CredBackup) {
    Copy-Item -Path $CredBackup -Destination "$ClaudeDir\.credentials.json" -Force
    Write-Success "  Restored: .credentials.json"
}
else {
    Write-Warn "  Warning: No credentials backup found. You may need to re-authenticate."
}

# Local settings (if exists)
$LocalSettingsBackup = "$BackupDir\settings.local.json"
if (Test-Path $LocalSettingsBackup) {
    Copy-Item -Path $LocalSettingsBackup -Destination "$ClaudeDir\settings.local.json" -Force
    Write-Success "  Restored: settings.local.json"
}
else {
    Write-Info "  Creating default settings.local.json..."
    @'
{
  "permissions": {
    "allow": []
  }
}
'@ | Out-File -FilePath "$ClaudeDir\settings.local.json" -Encoding utf8
    Write-Success "  Created: settings.local.json (empty permissions)"
}

# Vibe9 token (if exists)
$Vibe9Backup = "$BackupDir\.vibe9-token"
if (Test-Path $Vibe9Backup) {
    Copy-Item -Path $Vibe9Backup -Destination "$ClaudeDir\.vibe9-token" -Force
    Write-Success "  Restored: .vibe9-token"
}

# Create necessary directories that are gitignored
Write-Step 6 "Creating local directories..."

$LocalDirs = @(
    "cache",
    "debug",
    "downloads",
    "file-history",
    "ide",
    "plans",
    "projects",
    "shell-snapshots",
    "statsig",
    "telemetry",
    "todos"
)

foreach ($dir in $LocalDirs) {
    $dirPath = "$ClaudeDir\$dir"
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
}
Write-Success "  Local directories created"

# Summary
Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                        Setup Complete!                            ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green

Write-Info "Next steps:"
Write-Host "  1. Restart Claude Code to load the new configuration"
Write-Host "  2. Verify skills are working: /global-reference"
Write-Host "  3. Check MCP servers: /mcp"
Write-Host ""
Write-Info "Your backup is at: $BackupDir"
Write-Host "  You can delete it once you've verified everything works."
Write-Host ""
Write-Info "To sync settings in the future, run:"
Write-Host "  cd ~/.claude && ./scripts/sync.ps1"
Write-Host ""
