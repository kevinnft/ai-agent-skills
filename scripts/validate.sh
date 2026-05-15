#!/bin/bash
# Use a defensive mode that still lets the validator continue past
# individual skill failures so we can report all issues in one pass.
set -uo pipefail

# AI Agent Skills - Validation Script
# Validates all skills for correctness

VERSION="1.2.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$REPO_ROOT/skills"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
TOTAL_SKILLS=0
VALID_SKILLS=0
INVALID_SKILLS=0
WARNINGS=0

# Print colored message
print_msg() {
    local color=$1
    shift
    echo -e "${color}$*${NC}"
}

# Validate YAML frontmatter
validate_frontmatter() {
    local file=$1
    local errors=0
    
    # Check frontmatter exists
    if ! grep -q "^---$" "$file"; then
        print_msg "$RED" "    ✗ Missing YAML frontmatter"
        return 1
    fi
    
    # Extract the first YAML frontmatter block only. Do not scan later markdown
    # examples or horizontal rules, because many skills contain sample `name:`
    # fields inside code blocks.
    local frontmatter
    frontmatter=$(awk '
        NR == 1 && $0 == "---" { in_frontmatter = 1; next }
        in_frontmatter && $0 == "---" { exit }
        in_frontmatter { print }
    ' "$file")
    
    # Check required fields
    if ! echo "$frontmatter" | grep -q "^name:"; then
        print_msg "$RED" "    ✗ Missing 'name' field"
        ((errors++))
    fi
    
    if ! echo "$frontmatter" | grep -q "^description:"; then
        print_msg "$RED" "    ✗ Missing 'description' field"
        ((errors++))
    fi
    
    # Check name format (lowercase, hyphens/underscores only)
    local name
    name=$(echo "$frontmatter" | grep "^name:" | sed 's/name: *//' | tr -d '"' | tr -d "'")
    if [[ ! "$name" =~ ^[a-z0-9_-]+$ ]]; then
        print_msg "$YELLOW" "    ⚠  Name should be lowercase with hyphens/underscores: $name"
        ((WARNINGS++))
    fi
    
    return $errors
}

# Validate markdown structure
validate_markdown() {
    local file=$1
    local errors=0
    
    # Check file is not empty
    if [ ! -s "$file" ]; then
        print_msg "$RED" "    ✗ File is empty"
        return 1
    fi
    
    # Check has content after frontmatter
    local content_lines
    content_lines=$(sed -n '/^---$/,/^---$/!p' "$file" | grep -v "^$" | wc -l)
    if [ $content_lines -lt 5 ]; then
        print_msg "$YELLOW" "    ⚠  Very short content ($content_lines lines)"
        ((WARNINGS++))
    fi
    
    # Check has at least one heading
    if ! grep -q "^#" "$file"; then
        print_msg "$YELLOW" "    ⚠  No markdown headings found"
        ((WARNINGS++))
    fi
    
    return 0
}

# Validate skill file
validate_skill() {
    local skill_file=$1
    local skill_name
    skill_name=$(basename "$(dirname "$skill_file")")
    
    print_msg "$BLUE" "  Validating: $skill_name"
    
    # Check file exists
    if [ ! -f "$skill_file" ]; then
        print_msg "$RED" "    ✗ File not found"
        return 1
    fi
    
    # Validate frontmatter
    if ! validate_frontmatter "$skill_file"; then
        return 1
    fi
    
    # Validate markdown
    if ! validate_markdown "$skill_file"; then
        return 1
    fi
    
    print_msg "$GREEN" "    ✓ Valid"
    return 0
}

# Validate category
validate_category() {
    local category=$1
    local category_dir="$SKILLS_DIR/$category"
    
    print_msg "$BLUE" "📂 Category: $category"
    
    if [ ! -d "$category_dir" ]; then
        print_msg "$RED" "  ✗ Directory not found"
        return 1
    fi
    
    local skill_count=0
    local valid_count=0
    local invalid_count=0
    
    # Find all SKILL.md files
    while IFS= read -r skill_file; do
        ((skill_count++))
        ((TOTAL_SKILLS++))
        
        if validate_skill "$skill_file"; then
            ((valid_count++))
            ((VALID_SKILLS++))
        else
            ((invalid_count++))
            ((INVALID_SKILLS++))
        fi
    done < <(find "$category_dir" -name "SKILL.md" -type f)
    
    if [ $skill_count -eq 0 ]; then
        if [ -f "$category_dir/DESCRIPTION.md" ]; then
            print_msg "$GREEN" "  Info: descriptor-only category (no skills yet)"
        else
            print_msg "$YELLOW" "  ⚠  No skills found"
            ((WARNINGS++))
        fi
    else
        print_msg "$GREEN" "  Summary: $valid_count valid, $invalid_count invalid"
    fi
    
    echo ""
    return 0
}

# Main validation
main() {
    print_msg "$BLUE" "╔════════════════════════════════════════╗"
    print_msg "$BLUE" "║   AI Agent Skills - Validator v${VERSION}  ║"
    print_msg "$BLUE" "╚════════════════════════════════════════╝"
    echo ""
    
    # Check skills directory exists
    if [ ! -d "$SKILLS_DIR" ]; then
        print_msg "$RED" "✗ Skills directory not found: $SKILLS_DIR"
        exit 1
    fi
    
    print_msg "$BLUE" "🔍 Validating all skills..."
    echo ""
    
    # Validate each category
    for dir in "$SKILLS_DIR"/*; do
        if [ -d "$dir" ]; then
            local cat_name
            cat_name=$(basename "$dir")
            validate_category "$cat_name"
        fi
    done
    
    # Print summary
    print_msg "$BLUE" "╔════════════════════════════════════════╗"
    print_msg "$BLUE" "║            VALIDATION SUMMARY          ║"
    print_msg "$BLUE" "╚════════════════════════════════════════╝"
    echo ""
    echo "  Total Skills:   $TOTAL_SKILLS"
    print_msg "$GREEN" "  Valid:          $VALID_SKILLS"
    
    if [ $INVALID_SKILLS -gt 0 ]; then
        print_msg "$RED" "  Invalid:        $INVALID_SKILLS"
    else
        echo "  Invalid:        $INVALID_SKILLS"
    fi
    
    if [ $WARNINGS -gt 0 ]; then
        print_msg "$YELLOW" "  Warnings:       $WARNINGS"
    else
        echo "  Warnings:       $WARNINGS"
    fi
    
    echo ""
    
    # Exit code
    if [ $INVALID_SKILLS -gt 0 ]; then
        print_msg "$RED" "❌ Validation failed!"
        exit 1
    elif [ $WARNINGS -gt 0 ]; then
        print_msg "$YELLOW" "⚠️  Validation passed with warnings"
        exit 0
    else
        print_msg "$GREEN" "✅ All skills valid!"
        exit 0
    fi
}

# Run main
main "$@"
