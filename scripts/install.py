#!/usr/bin/env python3
"""
AI Agent Skills - Cross-Platform Installation Script

Replicates the functionality of install.sh for Windows, macOS, and Linux.
Uses only Python stdlib — no external dependencies required.

Usage:
    python install.py [OPTIONS]
    python install.py --help
"""

import argparse
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VERSION = "1.7.1"

# Skills that exist under multiple categories. The installer keeps a single
# copy per name based on --prefer (default: superpowers).
# Format: "skill-name:cat1,cat2,cat3"
DUPLICATE_SKILLS = [
    "test-driven-development:addyosmani,superpowers,software-development",
    "systematic-debugging:superpowers,software-development",
    "requesting-code-review:superpowers,software-development",
    "subagent-driven-development:superpowers,software-development",
    "writing-plans:superpowers,software-development",
]

# Curated starter packs. Each entry is "preset_name:cat1,cat2,cat3"; categories
# resolve against the directory names under skills/.
PRESETS = [
    "developer:superpowers,software-development,addyosmani,mattpocock,github",
    "researcher:research,mlops,data-science,note-taking",
    "content-creator:creative,media,social-media,productivity",
    "devops:devops,github,mcp,autonomous-ai-agents",
    "agentic:superpowers,autonomous-ai-agents,mcp,red-teaming",
    "minimal:superpowers",
]

# Default target directories per agent type
AGENT_TARGETS = {
    "hermes": ".hermes/skills",
    "claude": ".claude/skills",
    "cursor": ".cursor/skills",
}

# ---------------------------------------------------------------------------
# Color support
# ---------------------------------------------------------------------------

# Enable ANSI escape codes on Windows 10+ by calling os.system('')
# which triggers the Windows console to process virtual terminal sequences.
if platform.system() == "Windows":
    os.system("")


class Colors:
    """ANSI color codes with automatic disable on dumb terminals."""

    def __init__(self):
        # Disable colors if NO_COLOR env is set, or output is not a terminal
        use_color = (
            sys.stdout.isatty()
            and os.environ.get("NO_COLOR") is None
            and os.environ.get("TERM") != "dumb"
        )
        if use_color:
            self.RED = "\033[0;31m"
            self.GREEN = "\033[0;32m"
            self.YELLOW = "\033[1;33m"
            self.BLUE = "\033[0;34m"
            self.NC = "\033[0m"
        else:
            self.RED = ""
            self.GREEN = ""
            self.YELLOW = ""
            self.BLUE = ""
            self.NC = ""


C = Colors()


def print_msg(color: str, message: str):
    """Print a colored message to stdout."""
    print(f"{color}{message}{C.NC}")


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SKILLS_DIR = REPO_ROOT / "skills"


def get_home_dir() -> Path:
    """Return the user's home directory, cross-platform."""
    return Path.home()


def get_default_target(agent: str) -> Path:
    """Return the default target directory for a given agent type."""
    if agent in AGENT_TARGETS:
        return get_home_dir() / AGENT_TARGETS[agent]
    return get_home_dir() / ".hermes" / "skills"


# ---------------------------------------------------------------------------
# Skill discovery helpers
# ---------------------------------------------------------------------------

def find_skill_files(directory: Path) -> list:
    """
    Recursively find all SKILL.md files under a directory.
    Returns a sorted list of Path objects for deterministic output.
    """
    if not directory.is_dir():
        return []
    return sorted(directory.rglob("SKILL.md"))


def get_categories() -> list:
    """Return sorted list of category directory names under skills/."""
    if not SKILLS_DIR.is_dir():
        return []
    return sorted(
        d.name for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


# ---------------------------------------------------------------------------
# Duplicate resolution
# ---------------------------------------------------------------------------

def parse_duplicate_entry(entry: str) -> tuple:
    """Parse 'skill-name:cat1,cat2,cat3' into (name, [cat1, cat2, cat3])."""
    name, cats_csv = entry.split(":", 1)
    return name, cats_csv.split(",")


def should_skip_duplicate(skill_name: str, current_category: str, prefer: str) -> bool:
    """
    Determine if a duplicate skill copy should be skipped.

    Returns True (skip) if the skill is in DUPLICATE_SKILLS, lists this
    category, AND --prefer resolves to a different category.
    """
    for entry in DUPLICATE_SKILLS:
        name, cats = parse_duplicate_entry(entry)
        if name != skill_name:
            continue

        # If prefer is one of the candidate categories AND the current copy
        # comes from a different category, skip this copy.
        if prefer in cats and current_category != prefer:
            return True

        # If prefer isn't one of the candidate categories, fall through to
        # stable order: keep the first listed category.
        if prefer not in cats:
            first_cat = cats[0]
            if current_category != first_cat:
                return True

        return False

    return False


# ---------------------------------------------------------------------------
# Preset resolution
# ---------------------------------------------------------------------------

def resolve_preset(name: str):
    """
    Resolve a preset name to its comma-separated category list.
    Returns the CSV string or None if not found.
    """
    for entry in PRESETS:
        preset_name, cats_csv = entry.split(":", 1)
        if preset_name == name:
            return cats_csv
    return None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_skill(skill_file: Path, verbose: bool = True) -> bool:
    """
    Validate a SKILL.md file has required YAML frontmatter fields.
    Returns True if valid, False otherwise.
    """
    errors = 0

    if not skill_file.is_file():
        if verbose:
            print_msg(C.RED, f"  \u2717 File not found: {skill_file}")
        return False

    try:
        content = skill_file.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        if verbose:
            print_msg(C.RED, f"  \u2717 Cannot read: {skill_file} ({e})")
        return False

    # Check YAML frontmatter delimiter
    if not re.search(r"^---$", content, re.MULTILINE):
        if verbose:
            print_msg(C.RED, "  \u2717 Missing YAML frontmatter")
        errors += 1

    # Check required fields (at start of line)
    if not re.search(r"^name:", content, re.MULTILINE):
        if verbose:
            print_msg(C.RED, "  \u2717 Missing 'name' field")
        errors += 1

    if not re.search(r"^description:", content, re.MULTILINE):
        if verbose:
            print_msg(C.RED, "  \u2717 Missing 'description' field")
        errors += 1

    if errors == 0:
        if verbose:
            print_msg(C.GREEN, "  \u2713 Valid")
        return True
    return False


def run_validate_only(category: str, preset: str):
    """
    Validate-only mode: lint frontmatter across the requested scope and exit.
    Honours --category and --preset. Default scope is every category.
    """
    print_msg(C.BLUE, "\U0001f50e Validating skills (no install)...")
    print()

    cats = []
    if preset:
        preset_cats = resolve_preset(preset)
        if preset_cats is None:
            print_msg(C.RED, f"\u2717 Unknown preset: {preset}")
            sys.exit(1)
        cats = preset_cats.split(",")
    elif category:
        cats = [category]
    else:
        cats = get_categories()

    total_valid = 0
    total_invalid = 0

    for c in cats:
        source_dir = SKILLS_DIR / c
        if not source_dir.is_dir():
            print_msg(C.RED, f"\u2717 Category not found: {c}")
            total_invalid += 1
            continue

        print_msg(C.BLUE, f"\U0001f4cb {c}")
        skill_files = find_skill_files(source_dir)
        for skill_file in skill_files:
            if validate_skill(skill_file):
                total_valid += 1
            else:
                print_msg(C.RED, f"    in: {skill_file}")
                total_invalid += 1

    print()
    if total_invalid > 0:
        print_msg(C.RED, f"\u2717 {total_invalid} invalid \u00b7 {total_valid} valid")
        sys.exit(1)
    print_msg(C.GREEN, f"\u2713 All {total_valid} skills valid (no files copied)")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Installation
# ---------------------------------------------------------------------------

def copy_skill_dir(src: Path, dst: Path):
    """
    Copy a skill directory (all files within) to the target.
    Creates the destination if it doesn't exist.
    Equivalent to: cp -r src/. dst/
    """
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        s = item
        d = dst / item.name
        if item.is_dir():
            shutil.copytree(str(s), str(d), dirs_exist_ok=True)
        else:
            shutil.copy2(str(s), str(d))


def install_category(
    category: str,
    target_dir: Path,
    prefer: str,
    dry_run: bool,
    validate: bool,
) -> bool:
    """
    Install a single category of skills.
    Returns True on success, False on failure.
    """
    source_dir = SKILLS_DIR / category
    target_cat_dir = target_dir / category

    if not source_dir.is_dir():
        print_msg(C.RED, f"\u2717 Category not found: {category}")
        return False

    print_msg(C.BLUE, f"\U0001f4e6 Installing category: {category}")

    skill_files = find_skill_files(source_dir)
    skill_count = len(skill_files)

    # Dry-run mode: enumerate and bail out
    if dry_run:
        would_skip = 0
        for skill_file in skill_files:
            skill_name = skill_file.parent.name
            if should_skip_duplicate(skill_name, category, prefer):
                would_skip += 1
                print_msg(
                    C.YELLOW,
                    f"  \u2934 would skip: {skill_name} (kept from --prefer={prefer})",
                )
        print_msg(
            C.GREEN,
            f"  \u24d8 would install {skill_count - would_skip} skills "
            f"(would skip {would_skip})",
        )
        return True

    # Create target directory
    target_cat_dir.mkdir(parents=True, exist_ok=True)

    if skill_count == 0:
        print_msg(C.YELLOW, "  \u26a0  No skills found in category")
        return True

    # Validate if requested
    if validate:
        print_msg(C.BLUE, "  Validating skills...")
        valid = 0
        invalid = 0
        for skill_file in skill_files:
            if validate_skill(skill_file):
                valid += 1
            else:
                invalid += 1

        if invalid > 0:
            print_msg(C.RED, f"  \u2717 Validation failed: {invalid} invalid skills")
            return False
        print_msg(C.GREEN, f"  \u2713 All skills valid ({valid} skills)")

    # Copy skills, skipping duplicates that lose the --prefer tiebreak
    skipped = 0
    for skill_file in skill_files:
        skill_dir = skill_file.parent
        skill_name = skill_dir.name

        # Compute relative path from source_dir to skill_dir
        rel = skill_dir.relative_to(source_dir)

        if should_skip_duplicate(skill_name, category, prefer):
            skipped += 1
            print_msg(
                C.YELLOW,
                f"  \u2934 skip duplicate: {skill_name} (kept from --prefer={prefer})",
            )
            continue

        dest = target_cat_dir / rel
        copy_skill_dir(skill_dir, dest)

    # Copy non-skill files at the category root (DESCRIPTION.md, README, etc.)
    for item in source_dir.iterdir():
        if item.is_file():
            try:
                shutil.copy2(str(item), str(target_cat_dir / item.name))
            except OSError:
                pass

    if skipped > 0:
        print_msg(
            C.GREEN,
            f"  \u2713 Installed {skill_count - skipped} skills "
            f"(skipped {skipped} duplicate(s))",
        )
    else:
        print_msg(C.GREEN, f"  \u2713 Installed {skill_count} skills")

    return True


def install_preset_categories(
    preset_name: str,
    cats_csv: str,
    target_dir: Path,
    prefer: str,
    dry_run: bool,
    validate: bool,
):
    """Install a list of categories specified by a preset."""
    print_msg(C.BLUE, f"\U0001f4e6 Installing preset: {preset_name} ({cats_csv})")
    print()

    cats = cats_csv.split(",")
    installed = 0
    failed = 0

    for c in cats:
        if install_category(c, target_dir, prefer, dry_run, validate):
            installed += 1
        else:
            failed += 1
        print()

    if dry_run:
        print_msg(C.YELLOW, "\u24d8 Dry run complete. Re-run without --dry-run to apply.")
    else:
        print_msg(C.GREEN, f"\u2705 Preset '{preset_name}' installation complete!")

    print(f"  Categories installed: {installed}")
    print(f"  Failed: {failed}")
    print(f"  Target: {target_dir}")


def install_all(
    target_dir: Path,
    prefer: str,
    dry_run: bool,
    validate: bool,
):
    """Install all categories."""
    print_msg(C.BLUE, "\U0001f4e6 Installing all skills...")
    print()

    total_skills = 0
    total_categories = 0
    failed_categories = 0

    for cat_name in get_categories():
        cat_dir = SKILLS_DIR / cat_name
        if install_category(cat_name, target_dir, prefer, dry_run, validate):
            skill_count = len(find_skill_files(cat_dir))
            total_skills += skill_count
            total_categories += 1
        else:
            failed_categories += 1
        print()

    print_msg(C.GREEN, "\u2705 Installation complete!")
    print()
    print("Summary:")
    print(f"  Categories: {total_categories}")
    print(f"  Skills: {total_skills}")
    print(f"  Failed: {failed_categories}")
    print(f"  Target: {target_dir}")


# ---------------------------------------------------------------------------
# Submodule detection
# ---------------------------------------------------------------------------

def check_submodules():
    """
    Detect missing submodule content (clone done without --recurse-submodules).
    Warns the user so they know their install may be incomplete.
    """
    gitmodules = REPO_ROOT / ".gitmodules"
    if not gitmodules.is_file():
        return

    # Check if git is available
    if shutil.which("git") is None:
        return

    try:
        result = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "config", "--file", ".gitmodules",
             "--get-regexp", "path"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return

        empty_subs = 0
        for line in result.stdout.strip().splitlines():
            parts = line.split(None, 1)
            if len(parts) < 2:
                continue
            path = parts[1]
            sub_dir = REPO_ROOT / path
            if sub_dir.is_dir() and not any(sub_dir.iterdir()):
                empty_subs += 1

        if empty_subs > 0:
            print_msg(
                C.YELLOW,
                f"\u26a0  {empty_subs} submodule(s) not initialized "
                "\u2014 6 skills will be missing.",
            )
            print_msg(
                C.YELLOW,
                "   Run: git submodule update --init --recursive",
            )
            print_msg(
                C.YELLOW,
                "   (or re-clone with: git clone --recurse-submodules)",
            )
            print()

    except (subprocess.TimeoutExpired, OSError):
        # Git not working or timed out — skip silently
        pass


# ---------------------------------------------------------------------------
# Listing commands
# ---------------------------------------------------------------------------

def list_categories():
    """List available categories with skill counts."""
    print_msg(C.BLUE, "\U0001f4cb Available Categories:")
    print()

    count = 0
    for cat_name in get_categories():
        cat_dir = SKILLS_DIR / cat_name
        skill_count = len(find_skill_files(cat_dir))
        print(f"  {cat_name:<30} {skill_count:3d} skills")
        count += 1

    print()
    print_msg(C.GREEN, f"Total: {count} categories")
    sys.exit(0)


def list_presets():
    """List curated starter packs with skill counts."""
    print_msg(C.BLUE, "\U0001f4e6 Curated Starter Packs:")
    print()

    for entry in PRESETS:
        name, cats_csv = entry.split(":", 1)
        cats = cats_csv.split(",")
        total = 0
        for c in cats:
            cat_dir = SKILLS_DIR / c
            total += len(find_skill_files(cat_dir))
        print(f"  {name:<18} {total:3d} skills    {cats_csv}")

    print()
    print_msg(C.GREEN, "Use: python install.py --preset NAME")
    sys.exit(0)


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser matching install.sh's interface."""
    parser = argparse.ArgumentParser(
        description=f"AI Agent Skills - Installation Script v{VERSION}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
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
    python install.py --preset developer --agent claude
    python install.py --preset minimal --dry-run
    python install.py --category addyosmani
    python install.py --category mattpocock --validate
    python install.py --agent claude --target ~/.claude/skills
    python install.py --list
    python install.py --list-presets
""",
    )

    parser.add_argument(
        "--all", action="store_true", default=False,
        help="Install all skills (default behavior when no --category/--preset given)",
    )
    parser.add_argument(
        "--category", metavar="NAME",
        help="Install specific category",
    )
    parser.add_argument(
        "--preset", metavar="NAME",
        help="Install a curated starter pack (see --list-presets)",
    )
    parser.add_argument(
        "--list", action="store_true", dest="list_cats",
        help="List available categories",
    )
    parser.add_argument(
        "--list-presets", action="store_true",
        help="List curated starter packs",
    )
    parser.add_argument(
        "--validate", action="store_true",
        help="Lint frontmatter before install (combine with install)",
    )
    parser.add_argument(
        "--validate-only", action="store_true",
        help="Lint frontmatter and exit (no files copied)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be installed without copying",
    )
    parser.add_argument(
        "--target", metavar="DIR",
        help="Target directory (default: ~/.hermes/skills)",
    )
    parser.add_argument(
        "--agent", metavar="NAME", default="hermes",
        choices=["hermes", "claude", "cursor", "custom"],
        help="Agent type: hermes, claude, cursor, custom (default: hermes)",
    )
    parser.add_argument(
        "--prefer", metavar="NAME", default="superpowers",
        help="For duplicate skill names, keep the copy from this category "
             "(default: superpowers)",
    )

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = build_parser()
    args = parser.parse_args()

    # Handle --list and --list-presets early (they exit immediately)
    if args.list_cats:
        list_categories()
    if args.list_presets:
        list_presets()

    # Determine target directory
    target_explicit = args.target is not None
    if target_explicit:
        target_dir = Path(args.target).expanduser().resolve()
    else:
        if args.agent == "custom":
            print_msg(C.RED, "\u2717 --agent custom requires --target DIR")
            sys.exit(1)
        target_dir = get_default_target(args.agent)

    # Determine install mode
    install_all_flag = True
    if args.category or args.preset:
        install_all_flag = False

    # Print header
    print_msg(C.BLUE, "\u2554\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2557")
    print_msg(C.BLUE, f"\u2551   AI Agent Skills - Installer v{VERSION}   \u2551")
    print_msg(C.BLUE, "\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u255d")
    print()

    # Check skills directory exists
    if not SKILLS_DIR.is_dir():
        print_msg(C.RED, f"\u2717 Skills directory not found: {SKILLS_DIR}")
        sys.exit(1)

    # Detect missing submodule content
    check_submodules()

    # --validate-only short-circuits: lint and exit, never touch the FS
    if args.validate_only:
        run_validate_only(args.category or "", args.preset or "")

    # Backward-compat guard: bare --validate without install flags
    if (
        args.validate
        and install_all_flag
        and not args.category
        and not args.preset
    ):
        print_msg(
            C.YELLOW,
            "\u26a0  --validate without --category/--preset/--all will install ALL",
        )
        print_msg(
            C.YELLOW,
            f"   skills to {target_dir} after linting.",
        )
        print_msg(
            C.YELLOW,
            "   If you only want to lint, use --validate-only instead.",
        )
        print()

    # Create target directory (skipped in dry-run to keep filesystem untouched)
    if not args.dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    # Install
    if args.preset:
        preset_cats = resolve_preset(args.preset)
        if preset_cats is None:
            print_msg(C.RED, f"\u2717 Unknown preset: {args.preset}")
            print_msg(C.YELLOW, "  Run --list-presets to see available bundles.")
            sys.exit(1)
        install_preset_categories(
            args.preset, preset_cats, target_dir,
            args.prefer, args.dry_run, args.validate,
        )
    elif install_all_flag:
        install_all(target_dir, args.prefer, args.dry_run, args.validate)
    else:
        if not args.category:
            print_msg(C.RED, "\u2717 Category name required with --category")
            parser.print_help()
            sys.exit(1)
        install_category(
            args.category, target_dir, args.prefer,
            args.dry_run, args.validate,
        )

    # Dry-run footer
    if args.dry_run:
        print()
        print_msg(C.YELLOW, "\u24d8 Dry run only. No files were copied.")
        return

    # Success footer
    print()
    print_msg(C.GREEN, f"\U0001f389 Done! Skills installed to: {target_dir}")

    # Agent-specific instructions
    if args.agent == "hermes":
        print()
        print_msg(C.BLUE, "Next steps:")
        print("  1. Restart Hermes Agent (if running)")
        print("  2. Skills will auto-load on next session")
        print("  3. Use 'hermes skills list' to verify")
    elif args.agent == "claude":
        print()
        print_msg(C.BLUE, "Next steps:")
        print("  1. Restart Claude Code")
        print("  2. Skills will auto-load on next session")
    elif args.agent == "cursor":
        print()
        print_msg(C.BLUE, "Next steps:")
        print("  1. Restart Cursor")
        print("  2. Skills will auto-load on next session")


if __name__ == "__main__":
    main()
