#!/bin/bash
set +e

# AI Agent Skills - Installation Script
# Installs skills to Hermes Agent or other AI agents

VERSION="1.2.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$REPO_ROOT/skills"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
INSTALL_ALL=true
CATEGORY=""
VALIDATE=false
TARGET_DIR="$HOME/.hermes/skills"
AGENT="hermes"

# Print colored message
print_msg() {
    local color=$1
    shift
    echo -e "${color}$@${NC}"
}

# Print usage
usage() {
    cat << EOF
AI Agent Skills - Installation Script v${VERSION}

Usage: $0 [OPTIONS]

Options:
    --all                Install all skills (default)
    --category NAME      Install specific category
    --list               List available categories
    --validate           Validate skills before install
    --target DIR         Target directory (default: ~/.hermes/skills)
    --agent NAME         Agent type: hermes, claude, cursor, custom
    --help               Show this help message

Examples:
    $0 --all
    $0 --category addyosmani
    $0 --category mattpocock --validate
    $0 --agent claude --target ~/.claude/skills
    $0 --list

EOF
    exit 0
}

# List categories
list_categories() {
    print_msg "$BLUE" "📋 Available Categories:"
    echo ""
    
    local count=0
    for dir in "$SKILLS_DIR"/*; do
        if [ -d "$dir" ]; then
            local cat_name=$(basename "$dir")
            local skill_count=$(find "$dir" -name "SKILL.md" -type f | wc -l)
            printf "  %-30s %3d skills\n" "$cat_name" "$skill_count"
            count=$((count + 1))
        fi
    done
    
    echo ""
    print_msg "$GREEN" "Total: $count categories"
    exit 0
}

# Validate skill
validate_skill() {
    local skill_file=$1
    local errors=0
    
    # Check file exists
    if [ ! -f "$skill_file" ]; then
        print_msg "$RED" "  ✗ File not found: $skill_file"
        return 1
    fi
    
    # Check YAML frontmatter
    if ! grep -q "^---$" "$skill_file"; then
        print_msg "$RED" "  ✗ Missing YAML frontmatter"
        ((errors++))
    fi
    
    # Check required fields
    if ! grep -q "^name:" "$skill_file"; then
        print_msg "$RED" "  ✗ Missing 'name' field"
        ((errors++))
    fi
    
    if ! grep -q "^description:" "$skill_file"; then
        print_msg "$RED" "  ✗ Missing 'description' field"
        ((errors++))
    fi
    
    if [ $errors -eq 0 ]; then
        print_msg "$GREEN" "  ✓ Valid"
        return 0
    else
        return 1
    fi
}

# Install category
install_category() {
    local category=$1
    local source_dir="$SKILLS_DIR/$category"
    local target_cat_dir="$TARGET_DIR/$category"
    
    if [ ! -d "$source_dir" ]; then
        print_msg "$RED" "✗ Category not found: $category"
        return 1
    fi
    
    print_msg "$BLUE" "📦 Installing category: $category"
    
    # Create target directory
    mkdir -p "$target_cat_dir"
    
    # Count skills
    local skill_count=$(find "$source_dir" -name "SKILL.md" -type f | wc -l)
    
    if [ $skill_count -eq 0 ]; then
        print_msg "$YELLOW" "  ⚠  No skills found in category"
        return 0
    fi
    
    # Validate if requested
    if [ "$VALIDATE" = true ]; then
        print_msg "$BLUE" "  Validating skills..."
        local valid=0
        local invalid=0
        
        while IFS= read -r skill_file; do
            if validate_skill "$skill_file"; then
                ((valid++))
            else
                ((invalid++))
            fi
        done < <(find "$source_dir" -name "SKILL.md" -type f)
        
        if [ $invalid -gt 0 ]; then
            print_msg "$RED" "  ✗ Validation failed: $invalid invalid skills"
            return 1
        fi
        
        print_msg "$GREEN" "  ✓ All skills valid ($valid skills)"
    fi
    
    # Copy skills
    cp -r "$source_dir"/* "$target_cat_dir/" 2>/dev/null || true
    
    print_msg "$GREEN" "  ✓ Installed $skill_count skills"
    return 0
}

# Install all categories
install_all() {
    print_msg "$BLUE" "📦 Installing all skills..."
    echo ""
    
    local total_skills=0
    local total_categories=0
    local failed_categories=0
    
    for dir in "$SKILLS_DIR"/*; do
        if [ -d "$dir" ]; then
            local cat_name=$(basename "$dir")
            
            if install_category "$cat_name"; then
                local skill_count=$(find "$dir" -name "SKILL.md" -type f | wc -l)
                ((total_skills += skill_count))
                ((total_categories++))
            else
                ((failed_categories++))
            fi
            
            echo ""
        fi
    done
    
    print_msg "$GREEN" "✅ Installation complete!"
    echo ""
    echo "Summary:"
    echo "  Categories: $total_categories"
    echo "  Skills: $total_skills"
    echo "  Failed: $failed_categories"
    echo "  Target: $TARGET_DIR"
}

# Set target directory based on agent
set_target_dir() {
    case "$AGENT" in
        hermes)
            TARGET_DIR="$HOME/.hermes/skills"
            ;;
        claude)
            TARGET_DIR="$HOME/.claude/skills"
            ;;
        cursor)
            TARGET_DIR="$HOME/.cursor/skills"
            ;;
        custom)
            # TARGET_DIR already set via --target
            ;;
        *)
            print_msg "$RED" "✗ Unknown agent: $AGENT"
            exit 1
            ;;
    esac
}

# Main
main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                INSTALL_ALL=true
                shift
                ;;
            --category)
                INSTALL_ALL=false
                CATEGORY="$2"
                shift 2
                ;;
            --list)
                list_categories
                ;;
            --validate)
                VALIDATE=true
                shift
                ;;
            --target)
                TARGET_DIR="$2"
                AGENT="custom"
                shift 2
                ;;
            --agent)
                AGENT="$2"
                shift 2
                ;;
            --help)
                usage
                ;;
            *)
                print_msg "$RED" "✗ Unknown option: $1"
                usage
                ;;
        esac
    done
    
    # Print header
    print_msg "$BLUE" "╔════════════════════════════════════════╗"
    print_msg "$BLUE" "║   AI Agent Skills - Installer v${VERSION}   ║"
    print_msg "$BLUE" "╚════════════════════════════════════════╝"
    echo ""
    
    # Set target directory
    set_target_dir
    
    # Check skills directory exists
    if [ ! -d "$SKILLS_DIR" ]; then
        print_msg "$RED" "✗ Skills directory not found: $SKILLS_DIR"
        exit 1
    fi
    
    # Create target directory
    mkdir -p "$TARGET_DIR"
    
    # Install
    if [ "$INSTALL_ALL" = true ]; then
        install_all
    else
        if [ -z "$CATEGORY" ]; then
            print_msg "$RED" "✗ Category name required with --category"
            usage
        fi
        install_category "$CATEGORY"
    fi
    
    echo ""
    print_msg "$GREEN" "🎉 Done! Skills installed to: $TARGET_DIR"
    
    # Agent-specific instructions
    case "$AGENT" in
        hermes)
            echo ""
            print_msg "$BLUE" "Next steps:"
            echo "  1. Restart Hermes Agent (if running)"
            echo "  2. Skills will auto-load on next session"
            echo "  3. Use 'hermes skills list' to verify"
            ;;
        claude)
            echo ""
            print_msg "$BLUE" "Next steps:"
            echo "  1. Restart Claude Code"
            echo "  2. Skills will auto-load on next session"
            ;;
        cursor)
            echo ""
            print_msg "$BLUE" "Next steps:"
            echo "  1. Restart Cursor"
            echo "  2. Skills will auto-load on next session"
            ;;
    esac
}

# Run main
main "$@"
