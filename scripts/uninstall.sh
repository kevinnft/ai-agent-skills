#!/bin/bash
set -uo pipefail

# AI Agent Skills - Uninstaller
# Reverses install.sh by deleting categories from the agent's skill directory.
# Defaults match install.sh: ~/.hermes/skills with --agent overrides.

VERSION="1.7.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
# Defined for symmetry with install.sh; not currently consulted by the
# uninstall path but kept so future per-skill awareness is easy to wire.
# shellcheck disable=SC2034
SKILLS_DIR="$REPO_ROOT/skills"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Defaults — kept in sync with install.sh
UNINSTALL_ALL=false
CATEGORY=""
PRESET=""
TARGET_DIR="$HOME/.hermes/skills"
TARGET_EXPLICIT=false
AGENT="hermes"
DRY_RUN=false
ASSUME_YES=false
BACKUP=true

# Same preset table as install.sh
PRESETS=(
    "developer:superpowers,software-development,addyosmani,mattpocock,github"
    "researcher:research,mlops,data-science,note-taking"
    "content-creator:creative,media,social-media,productivity"
    "devops:devops,github,mcp,autonomous-ai-agents"
    "agentic:superpowers,autonomous-ai-agents,mcp,red-teaming"
    "minimal:superpowers"
)

print_msg() {
    local color=$1
    shift
    echo -e "${color}$*${NC}"
}

usage() {
    cat << EOF
AI Agent Skills - Uninstaller v${VERSION}

Usage: $0 [OPTIONS]

Options:
    --all                Remove every installed category from TARGET_DIR
    --category NAME      Remove a single category
    --preset NAME        Remove the categories from a curated starter pack
                         (developer, researcher, content-creator, devops,
                         agentic, minimal)
    --target DIR         Skill directory to clean (default: ~/.hermes/skills)
    --agent NAME         Agent type: hermes, claude, cursor, custom
    --dry-run            Print what would be removed without deleting
    --no-backup          Skip the timestamped backup created before removal
    --yes                Skip the interactive confirmation prompt
    --help               Show this help message

Examples:
    $0 --preset minimal --agent claude
    $0 --all --dry-run
    $0 --category creative --no-backup
    $0 --preset developer --yes

By default a backup is created at:
    \$TARGET_DIR/../skills_backup_<timestamp>/<category>/

EOF
    exit 0
}

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

set_target_dir() {
    if [ "$TARGET_EXPLICIT" = true ]; then
        return 0
    fi

    case "$AGENT" in
        hermes) TARGET_DIR="$HOME/.hermes/skills" ;;
        claude) TARGET_DIR="$HOME/.claude/skills" ;;
        cursor) TARGET_DIR="$HOME/.cursor/skills" ;;
        custom) ;;
        *)
            print_msg "$RED" "✗ Unknown agent: $AGENT"
            exit 1
            ;;
    esac
}

confirm() {
    if [ "$ASSUME_YES" = true ]; then
        return 0
    fi
    local prompt=$1
    read -r -p "$prompt [y/N] " reply
    [[ $reply =~ ^[Yy]$ ]]
}

# Remove one category from TARGET_DIR.
remove_category() {
    local category=$1
    local target_cat_dir="$TARGET_DIR/$category"

    if [ ! -d "$target_cat_dir" ]; then
        print_msg "$YELLOW" "  ⚠  Not installed: $category"
        return 0
    fi

    local skill_count
    skill_count=$(find "$target_cat_dir" -name "SKILL.md" -type f 2>/dev/null | wc -l)

    if [ "$DRY_RUN" = true ]; then
        print_msg "$BLUE" "  ⓘ would remove: $category ($skill_count skills)"
        return 0
    fi

    if [ "$BACKUP" = true ]; then
        local stamp
        stamp=$(date +%Y%m%d_%H%M%S)
        local backup_root
        backup_root="$(dirname "$TARGET_DIR")/skills_backup_${stamp}"
        mkdir -p "$backup_root"
        cp -r "$target_cat_dir" "$backup_root/$category" 2>/dev/null || true
        print_msg "$BLUE" "  📦 backup → $backup_root/$category"
    fi

    rm -rf "$target_cat_dir"
    print_msg "$GREEN" "  ✓ removed: $category ($skill_count skills)"
}

remove_categories() {
    local cats_csv=$1
    IFS=',' read -ra cats <<< "$cats_csv"

    if [ "$DRY_RUN" = false ]; then
        local count=${#cats[@]}
        if ! confirm "Remove $count categor(y/ies) from $TARGET_DIR?"; then
            print_msg "$YELLOW" "Cancelled."
            exit 0
        fi
    fi

    for c in "${cats[@]}"; do
        remove_category "$c"
    done
}

remove_all() {
    if [ ! -d "$TARGET_DIR" ]; then
        print_msg "$YELLOW" "⚠  Target not present: $TARGET_DIR"
        exit 0
    fi

    local installed_cats=()
    while IFS= read -r d; do
        installed_cats+=("$(basename "$d")")
    done < <(find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)

    if [ ${#installed_cats[@]} -eq 0 ]; then
        print_msg "$YELLOW" "⚠  No installed categories at $TARGET_DIR"
        exit 0
    fi

    if [ "$DRY_RUN" = false ]; then
        if ! confirm "Remove ${#installed_cats[@]} categor(y/ies) from $TARGET_DIR?"; then
            print_msg "$YELLOW" "Cancelled."
            exit 0
        fi
    fi

    for c in "${installed_cats[@]}"; do
        remove_category "$c"
    done
}

main() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)            UNINSTALL_ALL=true; shift ;;
            --category)       CATEGORY="$2"; shift 2 ;;
            --preset)         PRESET="$2"; shift 2 ;;
            --target)         TARGET_DIR="$2"; TARGET_EXPLICIT=true; shift 2 ;;
            --agent)          AGENT="$2"; shift 2 ;;
            --dry-run)        DRY_RUN=true; shift ;;
            --no-backup)      BACKUP=false; shift ;;
            --yes|-y)         ASSUME_YES=true; shift ;;
            --help|-h)        usage ;;
            *)
                print_msg "$RED" "✗ Unknown option: $1"
                usage
                ;;
        esac
    done

    print_msg "$BLUE" "╔════════════════════════════════════════╗"
    print_msg "$BLUE" "║   AI Agent Skills - Uninstaller v${VERSION}║"
    print_msg "$BLUE" "╚════════════════════════════════════════╝"
    echo ""

    set_target_dir
    print_msg "$BLUE" "Target: $TARGET_DIR"
    [ "$DRY_RUN" = true ] && print_msg "$YELLOW" "Mode: dry-run (no files will be touched)"
    echo ""

    if [ -n "$PRESET" ]; then
        local cats
        if ! cats=$(resolve_preset "$PRESET"); then
            print_msg "$RED" "✗ Unknown preset: $PRESET"
            exit 1
        fi
        remove_categories "$cats"
    elif [ -n "$CATEGORY" ]; then
        remove_categories "$CATEGORY"
    elif [ "$UNINSTALL_ALL" = true ]; then
        remove_all
    else
        print_msg "$RED" "✗ Specify one of: --all, --category NAME, --preset NAME"
        usage
    fi

    echo ""
    if [ "$DRY_RUN" = true ]; then
        print_msg "$YELLOW" "ⓘ Dry run only. No files were removed."
    else
        print_msg "$GREEN" "✅ Uninstall complete."
    fi
}

main "$@"
