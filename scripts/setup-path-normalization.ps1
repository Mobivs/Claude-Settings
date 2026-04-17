<#
.SYNOPSIS
    Create junctions from C:\dev\<project> to your user-profile project folders
    so memory paths match across machines with different usernames.

.DESCRIPTION
    Claude Code stores project memories under ~/.claude/projects/<sanitized-cwd>/memory/.
    The <sanitized-cwd> is derived from the absolute working-directory path — so opening
    the same project from C:\Users\svickrey\Foo vs C:\Users\John Vickrey\Foo creates
    two different memory folders that never share.

    This script creates a canonical junction path (default: C:\dev\) pointing at your
    user-profile projects. Open projects from C:\dev\<project> on every machine and
    memory folders collapse to a single shared name: c--dev-<project>.

    Junctions are created with `mklink /J` — persistent, no admin needed, reversible
    with `rmdir C:\dev\<project>` (only removes the junction, not the target).

.PARAMETER Root
    Canonical directory to create (default: C:\dev).

.PARAMETER Projects
    Optional list of project folder names to junction. If omitted, the script lists
    immediate subdirectories of your user profile and prompts for each.

.EXAMPLE
    .\setup-path-normalization.ps1
    Interactive — scans ~/ for candidate projects.

.EXAMPLE
    .\setup-path-normalization.ps1 -Projects ThermalInspector,inspection-master,yellow-pine
    Non-interactive — creates the three listed junctions.
#>
param(
    [string]$Root = "C:\dev",
    [string[]]$Projects
)

$ErrorActionPreference = "Stop"
$UserProfile = $env:USERPROFILE

Write-Host "`n=== Claude project path normalization ===" -ForegroundColor Cyan
Write-Host "User profile: $UserProfile"
Write-Host "Canonical root: $Root"
Write-Host ""

if (-not (Test-Path $Root)) {
    New-Item -ItemType Directory -Path $Root -Force | Out-Null
    Write-Host "Created $Root" -ForegroundColor Green
}

# Discover candidates if not provided
if (-not $Projects) {
    $candidates = Get-ChildItem -Path $UserProfile -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -notmatch '^\.|^AppData$|^OneDrive|^Documents$|^Downloads$|^Desktop$|^Pictures$|^Videos$|^Music$|^Favorites$|^Links$|^Searches$|^Saved Games$|^Contacts$|^source$|^scoop$' } |
        Select-Object -ExpandProperty Name
    if ($candidates.Count -eq 0) {
        Write-Host "No candidate folders found in $UserProfile" -ForegroundColor Yellow
        return
    }
    Write-Host "Candidate project folders:" -ForegroundColor Cyan
    $Projects = @()
    foreach ($c in $candidates) {
        $answer = Read-Host "  Junction $Root\$c -> $UserProfile\$c ? [y/N]"
        if ($answer -match '^[Yy]') { $Projects += $c }
    }
}

foreach ($p in $Projects) {
    $src = Join-Path $Root $p
    $dst = Join-Path $UserProfile $p

    if (-not (Test-Path $dst)) {
        Write-Host "SKIP $p - target $dst does not exist" -ForegroundColor Yellow
        continue
    }

    if (Test-Path $src) {
        # Already there - check if it's our junction
        $item = Get-Item $src -Force
        if ($item.Attributes.ToString() -match 'ReparsePoint') {
            Write-Host "EXISTS $src (junction) - skipping" -ForegroundColor DarkGray
        } else {
            Write-Host "EXISTS $src (regular dir, NOT a junction) - skipping to avoid overwrite" -ForegroundColor Yellow
        }
        continue
    }

    cmd /c mklink /J "`"$src`"" "`"$dst`"" | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "LINKED $src -> $dst" -ForegroundColor Green
    } else {
        Write-Host "FAILED to link $src" -ForegroundColor Red
    }
}

Write-Host "`nDone. Open projects from $Root\<project> going forward."
Write-Host "Example: code $Root\ThermalInspector"
Write-Host ""
Write-Host "Memory folders on every machine will normalize to:" -ForegroundColor Cyan
Write-Host "  ~/.claude/projects/c--dev-<project>/memory/"
Write-Host ""
Write-Host "Existing memory folders under the old user-profile path (e.g."
Write-Host "c--Users-$env:USERNAME-<project>) remain until you move them."
Write-Host "Move with: mv ~/.claude/projects/c--Users-*-<project> ~/.claude/projects/c--dev-<project>"
