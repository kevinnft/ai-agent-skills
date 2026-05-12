#!/bin/bash
set -e

# AI Agent Skills - Update Script
# Updates skills to latest version

VERSION="1.0.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$HOME/.hermes/skills"
BACKUP_DIR="$HOME/.hermes/skills_backup_$(date +%Y%m%d_%H%M%S)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Print colored message
print_msg() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Print header
print_header() {
    print_msg "$BLUE" "╔════════════════════════════════════════╗"
    print_msg "$BLUE" "║   AI Agent Skills - Updater v${VERSION}    ║"
    print_msg "$BLUE" "╚════════════════════════════════════════╝"
    echo ""
}

# Backup existing skills
backup_skills() {
    if [ ! -d "$TARGET_DIR" ]; then
        print_msg "$YELLOW" "⚠  No existing skills to backup"
        return 0
    fi
    
    print_msg "$BLUE" "📦 Backing up existing skills..."
    
    mkdir -p "$BACKUP_DIR"
    cp -r "$TARGET_DIR"/* "$BACKUP_DIR/" 2>/dev/null || true
    
    local backup_size=$(du -sh "$BACKUP_DIR" | awk '{print $1}')
    print_msg "$GREEN" "  ✓ Backup created: $BACKUP_DIR ($backup_size)"
}

# Pull latest changes
pull_latest() {
    print_msg "$BLUE" "🔄 Pulling latest changes..."
    
    cd "$REPO_ROOT"
    
    # Check if git repo
    if [ ! -d ".git" ]; then
        print_msg "$RED" "  ✗ Not a git repository"
        return 1
    fi
    
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        print_msg "$YELLOW" "  ⚠  Uncommitted changes detected"
        print_msg "$YELLOW" "  Stashing changes..."
        git stash push -m "Auto-stash before update $(date +%Y%m%d_%H%M%S)"
    fi
    
    # Pull latest
    local current_commit=$(git rev-parse --short HEAD)
    git pull origin main 2>&1 | tail -3
    local new_commit=$(git rev-parse --short HEAD)
    
    if [ "$current_commit" = "$new_commit" ]; then
        print_msg "$GREEN" "  ✓ Already up to date ($current_commit)"
    else
        print_msg "$GREEN" "  ✓ Updated: $current_commit → $new_commit"
    fi
}

# Show changelog
show_changelog() {
    print_msg "$BLUE" "📋 Recent changes:"
    echo ""
    
    cd "$REPO_ROOT"
    
    # Show last 5 commits
    git log --oneline --decorate -5 | sed 's/^/  /'
    
    echo ""
}

# Reinstall skills
reinstall_skills() {
    print_msg "$BLUE" "📦 Reinstalling skills..."
    
    cd "$REPO_ROOT"
    
    if [ ! -f "scripts/install.sh" ]; then
        print_msg "$RED" "  ✗ Install script not found"
        return 1
    fi
    
    # Run install script
    ./scripts/install.sh --all
}

# Verify installation
verify_installation() {
    print_msg "$BLUE" "✅ Verifying installation..."
    
    local skill_count=$(find "$TARGET_DIR" -name "SKILL.md" -type f 2>/dev/null | wc -l)
    
    if [ $skill_count -eq 0 ]; then
        print_msg "$RED" "  ✗ No skills found after update"
        return 1
    fi
    
    print_msg "$GREEN" "  ✓ $skill_count skills installed"
}

# Cleanup old backups
cleanup_backups() {
    local backup_parent=$(dirname "$BACKUP_DIR")
    local backup_count=$(find "$backup_parent" -maxdepth 1 -type d -name "skills_backup_*" 2>/dev/null | wc -l)
    
    if [ $backup_count -gt 5 ]; then
        print_msg "$BLUE" "🧹 Cleaning up old backups..."
        
        # Keep only 5 most recent backups
        find "$backup_parent" -maxdepth 1 -type d -name "skills_backup_*" -printf '%T@ %p\n' | \
            sort -rn | \
            tail -n +6 | \
            cut -d' ' -f2- | \
            while read dir; do
                rm -rf "$dir"
                print_msg "$GREEN" "  ✓ Removed old backup: $(basename $dir)"
            done
    fi
}

# Main
main() {
    print_header
    
    # Check if in repo directory
    if [ ! -f "$REPO_ROOT/README.md" ]; then
        print_msg "$RED" "✗ Must run from ai-agent-skills repository"
        exit 1
    fi
    
    # Backup
    backup_skills
    echo ""
    
    # Pull latest
    pull_latest
    echo ""
    
    # Show changelog
    show_changelog
    
    # Reinstall
    reinstall_skills
    echo ""
    
    # Verify
    verify_installation
    echo ""
    
    # Cleanup
    cleanup_backups
    echo ""
    
    # Summary
    print_msg "$GREEN" "✅ Update complete!"
    echo ""
    echo "Summary:"
    echo "  Backup: $BACKUP_DIR"
    echo "  Skills: $TARGET_DIR"
    echo "  Status: Up to date"
    echo ""
    print_msg "$BLUE" "Next steps:"
    echo "  1. Restart your AI agent"
    echo "  2. Skills will auto-load on next session"
    echo "  3. Check changelog for new features"
}

# Run main
main "$@"
