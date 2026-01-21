#!/bin/bash
#
# Set up Claude Code global settings on a new Mac/Linux machine.
# Run this script AFTER running Claude Code once to generate initial files.
#
# Usage:
#   ./setup-new-machine.sh
#   ./setup-new-machine.sh https://github.com/user/claude-settings.git
#

set -e

CLAUDE_DIR="$HOME/.claude"
BACKUP_DIR="$HOME/.claude-backup-$(date +%Y%m%d-%H%M%S)"
REPO_URL="$1"

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
MAGENTA='\033[0;35m'
NC='\033[0m'

info() { echo -e "${CYAN}$1${NC}"; }
success() { echo -e "${GREEN}$1${NC}"; }
warn() { echo -e "${YELLOW}$1${NC}"; }
step() { echo -e "\n${MAGENTA}[$1] $2${NC}"; }

echo -e "${CYAN}"
cat << 'EOF'

╔═══════════════════════════════════════════════════════════════════╗
║         Claude Code Global Settings - New Machine Setup           ║
╚═══════════════════════════════════════════════════════════════════╝

EOF
echo -e "${NC}"

# Check prerequisites
step 1 "Checking prerequisites..."

# Check for Git
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Please install Git first."
    exit 1
fi
success "  Git: OK"

# Check if Claude has been run
if [ ! -d "$CLAUDE_DIR" ]; then
    warn "
  The .claude directory doesn't exist yet.
  Please run 'claude' once to generate initial configuration, then run this script again.
"
    exit 1
fi
success "  .claude directory: OK"

# Check for credentials
CREDENTIALS_FILE="$CLAUDE_DIR/.credentials.json"
if [ ! -f "$CREDENTIALS_FILE" ]; then
    warn "
  No credentials found. Please authenticate Claude Code first:
  1. Run 'claude'
  2. Complete the authentication flow
  3. Run this script again
"
    exit 1
fi
success "  Credentials: OK"

# Get repository URL
step 2 "Repository configuration..."

if [ -z "$REPO_URL" ]; then
    read -p "Enter your Claude settings Git repository URL: " REPO_URL
fi

if [ -z "$REPO_URL" ]; then
    echo "Error: Repository URL is required."
    exit 1
fi

# Backup existing directory
step 3 "Backing up existing configuration..."

info "  Moving $CLAUDE_DIR to $BACKUP_DIR"
mv "$CLAUDE_DIR" "$BACKUP_DIR"
success "  Backup created: $BACKUP_DIR"

# Clone repository
step 4 "Cloning settings repository..."

if git clone "$REPO_URL" "$CLAUDE_DIR" 2>&1; then
    success "  Repository cloned successfully"
else
    warn "  Clone failed. Restoring backup..."
    mv "$BACKUP_DIR" "$CLAUDE_DIR"
    echo "Error: Failed to clone repository"
    exit 1
fi

# Restore machine-specific files
step 5 "Restoring machine-specific files..."

# Credentials (required)
CRED_BACKUP="$BACKUP_DIR/.credentials.json"
if [ -f "$CRED_BACKUP" ]; then
    cp "$CRED_BACKUP" "$CLAUDE_DIR/.credentials.json"
    success "  Restored: .credentials.json"
else
    warn "  Warning: No credentials backup found. You may need to re-authenticate."
fi

# Local settings
LOCAL_SETTINGS_BACKUP="$BACKUP_DIR/settings.local.json"
if [ -f "$LOCAL_SETTINGS_BACKUP" ]; then
    cp "$LOCAL_SETTINGS_BACKUP" "$CLAUDE_DIR/settings.local.json"
    success "  Restored: settings.local.json"
else
    info "  Creating default settings.local.json..."
    cat > "$CLAUDE_DIR/settings.local.json" << 'EOF'
{
  "permissions": {
    "allow": []
  }
}
EOF
    success "  Created: settings.local.json (empty permissions)"
fi

# Vibe9 token
VIBE9_BACKUP="$BACKUP_DIR/.vibe9-token"
if [ -f "$VIBE9_BACKUP" ]; then
    cp "$VIBE9_BACKUP" "$CLAUDE_DIR/.vibe9-token"
    success "  Restored: .vibe9-token"
fi

# Create necessary directories
step 6 "Creating local directories..."

LOCAL_DIRS=(
    "cache"
    "debug"
    "downloads"
    "file-history"
    "ide"
    "plans"
    "projects"
    "shell-snapshots"
    "statsig"
    "telemetry"
    "todos"
)

for dir in "${LOCAL_DIRS[@]}"; do
    mkdir -p "$CLAUDE_DIR/$dir"
done
success "  Local directories created"

# Summary
echo -e "${GREEN}"
cat << 'EOF'

╔═══════════════════════════════════════════════════════════════════╗
║                        Setup Complete!                            ║
╚═══════════════════════════════════════════════════════════════════╝

EOF
echo -e "${NC}"

info "Next steps:"
echo "  1. Restart Claude Code to load the new configuration"
echo "  2. Verify skills are working: /global-reference"
echo "  3. Check MCP servers: /mcp"
echo ""
info "Your backup is at: $BACKUP_DIR"
echo "  You can delete it once you've verified everything works."
echo ""
info "To sync settings in the future, run:"
echo "  cd ~/.claude && ./scripts/sync.sh"
echo ""
