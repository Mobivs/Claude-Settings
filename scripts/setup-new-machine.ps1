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

# Clone Knowledge vault (synced via GitHub — Mobivs/Knowledge, private repo)
Write-Step 7 "Setting up Knowledge vault..."

$KnowledgeDir = "$env:USERPROFILE\Knowledge"
$KnowledgeRepo = "https://github.com/Mobivs/Knowledge.git"

if (Test-Path "$KnowledgeDir\.git") {
    Write-Info "  Knowledge vault already cloned. Pulling latest..."
    Push-Location $KnowledgeDir
    git pull --rebase --quiet 2>&1
    Pop-Location
    Write-Success "  Knowledge vault up to date"
} elseif (Test-Path $KnowledgeDir) {
    Write-Warn "  Knowledge folder exists but is not a git repo."
    Write-Warn "  Back it up and clone fresh: git clone $KnowledgeRepo `"$KnowledgeDir`""
} else {
    Write-Info "  Cloning Knowledge vault from GitHub..."
    git clone $KnowledgeRepo $KnowledgeDir 2>&1
    Write-Success "  Knowledge vault cloned to: $KnowledgeDir"
}

# Ensure vault directories exist
foreach ($dir in @("logs", "notes", "projects")) {
    $dirPath = "$KnowledgeDir\$dir"
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
}

# Set up auto-sync scheduled task
Write-Step 8 "Setting up Knowledge vault auto-sync..."
$syncScript = "$KnowledgeDir\sync.ps1"
if (Test-Path $syncScript) {
    $taskName = "Knowledge Vault Sync"
    $existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Info "  Scheduled task '$taskName' already exists"
    } else {
        $action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$syncScript`""
        $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Days 3650)
        $settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
        Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description 'Auto-sync Knowledge vault to GitHub every 5 minutes' -Force | Out-Null
        Write-Success "  Auto-sync scheduled: every 5 minutes"
    }
} else {
    Write-Warn "  sync.ps1 not found in vault — auto-sync not configured"
}
Write-Success "  Knowledge vault ready at: $KnowledgeDir"

# Summary
Write-Host @"

╔═══════════════════════════════════════════════════════════════════╗
║                        Setup Complete!                            ║
╚═══════════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Green

Write-Info "Next steps:"
Write-Host "  1. Restart Claude Code to load the new configuration"
Write-Host "  2. Verify skills are working: /global-reference"
Write-Host "  3. Test memory system: /memory"
Write-Host "  4. Check MCP servers: /mcp"
Write-Host ""
Write-Info "Your backup is at: $BackupDir"
Write-Host "  You can delete it once you've verified everything works."
Write-Host ""
Write-Info "Two repos keep everything in sync:"
Write-Host "  Settings: cd ~/.claude && git pull origin main"
Write-Host "  Knowledge: auto-syncs every 5 min (Task Scheduler)"
Write-Host ""
