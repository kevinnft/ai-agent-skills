#!/bin/bash
set +e

# AI Agent Skills - Installation Script
# Installs skills to Hermes Agent or other AI agents

VERSION="1.7.0"
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
PRESET=""
VALIDATE=false
DRY_RUN=false
TARGET_DIR="$HOME/.hermes/skills"
TARGET_EXPLICIT=false
AGENT="hermes"
PREFER="superpowers"

# Skills that exist under multiple categories. The installer keeps a single
# copy per name based on $PREFER (default: superpowers).
# Format: "skill-name:cat1,cat2,cat3"
DUPLICATE_SKILLS=(
    "test-driven-development:addyosmani,superpowers,software-development"
    "systematic-debugging:superpowers,software-development"
    "requesting-code-review:superpowers,software-development"
    "subagent-driven-development:superpowers,software-development"
    "writing-plans:superpowers,software-development"
)

# Curated starter packs. Each entry is "preset_name:cat1,cat2,cat3"; categories
# resolve against the directory names under skills/. Listed in usage() too.
PRESETS=(
    "developer:superpowers,software-development,addyosmani,mattpocock,github"
    "researcher:research,mlops,data-science,note-taking"
    "content-creator:creative,media,social-media,productivity"
    "devops:devops,github,mcp,autonomous-ai-agents"
    "agentic:superpowers,autonomous-ai-agents,mcp,red-teaming"
    "minimal:superpowers"
)

# Print colored message
print_msg() {
    local color=$1
    shift
    echo -e "${color}$*${NC}"
}

# Print usage
usage() {
    cat << EOF
AI Agent Skills - Installation Script v${VERSION}

Usage: $0 [OPTIONS]

Options:
    --all                Install all skills (default)
    --category NAME      Install specific category
    --preset NAME        Install a curated starter pack (see below)
    --list               List available categories
    --list-presets       List curated starter packs
    --validate           Validate skills before install
    --dry-run            Print what would be installed without copying
    --target DIR         Target directory (default: ~/.hermes/skills)
    --agent NAME         Agent type: hermes, claude, cursor, custom
    --prefer NAME        For duplicate skill names, keep the copy from
                         this category (default: superpowers)
    --help               Show this help message

Curated presets:
    developer            Engineering-focused: superpowers, software-development,
                         addyosmani, mattpocock, github (~92 skills)
    researcher           Research workflows: research, mlops, data-science,
                         note-taking (~28 skills)
    content-creator      Visual + media: creative, media, social-media,
                         productivity (~37 skills)
    devops               Infra + ops: devops, github, mcp,
                         autonomous-ai-agents (~24 skills)
    agentic              Agent patterns: superpowers, autonomous-ai-agents,
                         mcp, red-teaming (~20 skills)
    minimal              Just the superpowers core (14 skills)

Examples:
    $0 --preset developer --agent claude
    $0 --preset minimal --dry-run
    $0 --category addyosmani
    $0 --category mattpocock --validate
    $0 --agent claude --target ~/.claude/skills
    $0 --list
    $0 --list-presets

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
            local cat_name
            cat_name=$(basename "$dir")
            local skill_count
            skill_count=$(find "$dir" -name "SKILL.md" -type f | wc -l)
            printf "  %-30s %3d skills\n" "$cat_name" "$skill_count"
            count=$((count + 1))
        fi
    done

    echo ""
    print_msg "$GREEN" "Total: $count categories"
    exit 0
}

# List presets
list_presets() {
    print_msg "$BLUE" "📦 Curated Starter Packs:"
    echo ""
    for entry in "${PRESETS[@]}"; do
        local name="${entry%%:*}"
        local cats_csv="${entry#*:}"
        local total=0
        IFS=',' read -ra cats <<< "$cats_csv"
        for c in "${cats[@]}"; do
            local n
            n=$(find "$SKILLS_DIR/$c" -name "SKILL.md" -type f 2>/dev/null | wc -l)
            total=$((total + n))
        done
        printf "  %-18s %3d skills    %s\n" "$name" "$total" "$cats_csv"
    done
    echo ""
    print_msg "$GREEN" "Use: $0 --preset NAME"
    exit 0
}

# Resolve preset name to comma-separated categories. Echoes "" if no match.
resolve_preset() {
    local name=$1
    for entry in "${PRESETS[@]}"; do
        if [ "${entry%%:*}" = "$name" ]; then
            echo "${entry#*:}"
            return 0
        fi
    done
    return 1
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

# Should this duplicate copy be skipped?
# Returns 0 (skip) if the skill is in DUPLICATE_SKILLS, lists this category,
# AND $PREFER lists it differently. Returns 1 otherwise.
should_skip_duplicate() {
    local skill_name=$1
    local current_category=$2

    for entry in "${DUPLICATE_SKILLS[@]}"; do
        local name="${entry%%:*}"
        local cats_csv="${entry#*:}"
        if [ "$name" != "$skill_name" ]; then
            continue
        fi

        # If $PREFER is itself one of the candidate categories AND the
        # current copy comes from a different category, skip this copy.
        if [[ ",${cats_csv}," == *",${PREFER},"* ]] && [ "$current_category" != "$PREFER" ]; then
            return 0
        fi
        # If $PREFER isn't one of the candidate categories, fall through
        # to a stable order: keep the first listed category.
        if [[ ",${cats_csv}," != *",${PREFER},"* ]]; then
            local first_cat="${cats_csv%%,*}"
            if [ "$current_category" != "$first_cat" ]; then
                return 0
            fi
        fi
        return 1
    done
    return 1
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

    # In dry-run mode just enumerate and bail out.
    if [ "$DRY_RUN" = true ]; then
        local skill_count
        skill_count=$(find "$source_dir" -name "SKILL.md" -type f | wc -l)
        local would_skip=0
        while IFS= read -r skill_file; do
            local skill_name
            skill_name=$(basename "$(dirname "$skill_file")")
            if should_skip_duplicate "$skill_name" "$category"; then
                would_skip=$((would_skip + 1))
                print_msg "$YELLOW" "  ⤳ would skip: $skill_name (kept from --prefer=$PREFER)"
            fi
        done < <(find "$source_dir" -name "SKILL.md" -type f)
        print_msg "$GREEN" "  ⓘ would install $((skill_count - would_skip)) skills (would skip $would_skip)"
        return 0
    fi

    # Create target directory
    mkdir -p "$target_cat_dir"
    
    # Count skills
    local skill_count
    skill_count=$(find "$source_dir" -name "SKILL.md" -type f | wc -l)
    
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
    
    # Copy skills, but skip duplicates that lose the --prefer tiebreak.
    local skipped=0
    while IFS= read -r skill_file; do
        local skill_dir
        skill_dir=$(dirname "$skill_file")
        local skill_name
        skill_name=$(basename "$skill_dir")
        local rel
        rel=${skill_dir#"$source_dir/"}

        if should_skip_duplicate "$skill_name" "$category"; then
            skipped=$((skipped + 1))
            print_msg "$YELLOW" "  ⤳ skip duplicate: $skill_name (kept from --prefer=$PREFER)"
            continue
        fi

        mkdir -p "$target_cat_dir/$rel"
        cp -r "$skill_dir"/. "$target_cat_dir/$rel/" 2>/dev/null || true
    done < <(find "$source_dir" -name "SKILL.md" -type f)

    # Copy non-skill files at the category root (DESCRIPTION.md, README, etc.).
    find "$source_dir" -maxdepth 1 -type f -exec cp {} "$target_cat_dir/" \; 2>/dev/null || true

    if [ "$skipped" -gt 0 ]; then
        print_msg "$GREEN" "  ✓ Installed $((skill_count - skipped)) skills (skipped $skipped duplicate(s))"
    else
        print_msg "$GREEN" "  ✓ Installed $skill_count skills"
    fi
    return 0
}

# Install a list of categories specified by name (used by --preset).
install_preset_categories() {
    local cats_csv=$1
    print_msg "$BLUE" "📦 Installing preset: $PRESET ($cats_csv)"
    echo ""

    IFS=',' read -ra cats <<< "$cats_csv"
    local installed=0
    local failed=0
    for c in "${cats[@]}"; do
        if install_category "$c"; then
            installed=$((installed + 1))
        else
            failed=$((failed + 1))
        fi
        echo ""
    done

    if [ "$DRY_RUN" = true ]; then
        print_msg "$YELLOW" "ⓘ Dry run complete. Re-run without --dry-run to apply."
    else
        print_msg "$GREEN" "✅ Preset '$PRESET' installation complete!"
    fi
    echo "  Categories installed: $installed"
    echo "  Failed: $failed"
    echo "  Target: $TARGET_DIR"
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
            local cat_name
            cat_name=$(basename "$dir")

            if install_category "$cat_name"; then
                local skill_count
                skill_count=$(find "$dir" -name "SKILL.md" -type f | wc -l)
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
    # Honor an explicit --target even if --agent was also passed.
    if [ "$TARGET_EXPLICIT" = true ]; then
        return 0
    fi

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
            --preset)
                INSTALL_ALL=false
                PRESET="$2"
                shift 2
                ;;
            --list)
                list_categories
                ;;
            --list-presets)
                list_presets
                ;;
            --validate)
                VALIDATE=true
                shift
                ;;
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --target)
                TARGET_DIR="$2"
                TARGET_EXPLICIT=true
                shift 2
                ;;
            --agent)
                AGENT="$2"
                shift 2
                ;;
            --prefer)
                PREFER="$2"
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
    
    # Create target directory (skipped in dry-run to keep filesystem untouched).
    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$TARGET_DIR"
    fi

    # Install
    if [ -n "$PRESET" ]; then
        local preset_cats
        if ! preset_cats=$(resolve_preset "$PRESET"); then
            print_msg "$RED" "✗ Unknown preset: $PRESET"
            print_msg "$YELLOW" "  Run --list-presets to see available bundles."
            exit 1
        fi
        install_preset_categories "$preset_cats"
    elif [ "$INSTALL_ALL" = true ]; then
        install_all
    else
        if [ -z "$CATEGORY" ]; then
            print_msg "$RED" "✗ Category name required with --category"
            usage
        fi
        install_category "$CATEGORY"
    fi

    if [ "$DRY_RUN" = true ]; then
        echo ""
        print_msg "$YELLOW" "ⓘ Dry run only. No files were copied."
        return 0
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
