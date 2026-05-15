#!/usr/bin/env python3
"""
Release Automation Script for ai-agent-skills

Features:
- Auto-generate changelog from commits
- Semantic versioning (major.minor.patch)
- Auto-create GitHub release
- Update CHANGELOG.md
- Send Telegram notification (optional)
- Validate before release
- Zero bugs, production-ready

Usage:
    ./scripts/release.py --patch              # 1.2.2 → 1.2.3
    ./scripts/release.py --minor              # 1.2.2 → 1.3.0
    ./scripts/release.py --major              # 1.2.2 → 2.0.0
    ./scripts/release.py --version 1.5.0      # Custom version
    ./scripts/release.py --dry-run            # Preview only
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    """Print colored header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ️  {text}{Colors.ENDC}")

def run_command(cmd: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
    """Run shell command and return exit code, stdout, stderr"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=False
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def get_current_version() -> Optional[str]:
    """Get current version from latest git tag"""
    code, stdout, _ = run_command(['git', 'describe', '--tags', '--abbrev=0'])
    if code == 0 and stdout:
        # Remove 'v' prefix if present
        return stdout.lstrip('v')
    return None

def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse version string into (major, minor, patch)"""
    match = re.match(r'(\d+)\.(\d+)\.(\d+)', version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))

def bump_version(current: str, bump_type: str) -> str:
    """Bump version based on type (major, minor, patch)"""
    major, minor, patch = parse_version(current)
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

def get_commits_since_last_tag() -> List[Dict[str, str]]:
    """Get all commits since last tag"""
    # Get last tag
    code, last_tag, _ = run_command(['git', 'describe', '--tags', '--abbrev=0'])
    
    if code != 0:
        # No tags yet, get all commits
        cmd = ['git', 'log', '--pretty=format:%H|%s|%an|%ae|%ad', '--date=short']
    else:
        # Get commits since last tag
        cmd = ['git', 'log', f'{last_tag}..HEAD', '--pretty=format:%H|%s|%an|%ae|%ad', '--date=short']
    
    code, stdout, _ = run_command(cmd)
    
    if code != 0 or not stdout:
        return []
    
    commits = []
    for line in stdout.split('\n'):
        if not line:
            continue
        parts = line.split('|')
        if len(parts) >= 5:
            commits.append({
                'hash': parts[0][:7],
                'message': parts[1],
                'author': parts[2],
                'email': parts[3],
                'date': parts[4]
            })
    
    return commits

_CONVENTIONAL_PREFIX = re.compile(
    r'^(?P<type>feat|feature|fix|docs?|refactor|test|chore|perf|build|ci|style|revert)'
    r'(?:\([^)]*\))?!?:\s*',
    re.IGNORECASE
)

_TYPE_TO_CATEGORY = {
    'feat': 'features',
    'feature': 'features',
    'fix': 'fixes',
    'doc': 'docs',
    'docs': 'docs',
    'refactor': 'refactor',
    'test': 'tests',
    'chore': 'chore',
    'perf': 'features',
    'build': 'chore',
    'ci': 'chore',
    'style': 'chore',
    'revert': 'other',
}


def _capitalize(text: str) -> str:
    """Capitalize first character if present, otherwise return as-is."""
    return text[:1].upper() + text[1:] if text else text


def categorize_commits(commits: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    """Categorize commits by Conventional Commit type with verb-keyword fallback."""
    categories = {
        'features': [],
        'fixes': [],
        'docs': [],
        'refactor': [],
        'tests': [],
        'chore': [],
        'other': []
    }

    for commit in commits:
        msg = commit.get('message', '').strip()
        category = None

        match = _CONVENTIONAL_PREFIX.match(msg)
        if match:
            category = _TYPE_TO_CATEGORY.get(match.group('type').lower())
        else:
            # Word-boundary fallback so "address" doesn't match "add" and
            # "fix add bug" gets classified as a fix, not a feature.
            head = msg.lower()[:40]
            if re.search(r'\bfix(?:es|ed|ing)?\b', head):
                category = 'fixes'
            elif re.search(r'\b(?:add|adds|added|adding)\b', head):
                category = 'features'
            elif re.search(r'\bdocs?\b', head):
                category = 'docs'
            elif re.search(r'\brefactor(?:s|ed|ing)?\b', head):
                category = 'refactor'
            elif re.search(r'\btests?\b', head):
                category = 'tests'
            elif re.search(r'\bchore\b', head):
                category = 'chore'

        categories[category or 'other'].append(commit)

    return categories

def generate_changelog(version: str, commits: List[Dict[str, str]]) -> str:
    """Generate changelog from commits"""
    categories = categorize_commits(commits)

    changelog = f"## [{version}] - {datetime.now().strftime('%Y-%m-%d')}\n\n"

    # Features
    if categories['features']:
        changelog += "### ✨ New Features\n\n"
        for commit in categories['features']:
            msg = _CONVENTIONAL_PREFIX.sub('', commit['message']).strip()
            msg = _capitalize(msg)
            changelog += f"- {msg} ({commit['hash']})\n"
        changelog += "\n"

    # Fixes
    if categories['fixes']:
        changelog += "### 🐛 Bug Fixes\n\n"
        for commit in categories['fixes']:
            msg = _CONVENTIONAL_PREFIX.sub('', commit['message']).strip()
            msg = _capitalize(msg)
            changelog += f"- {msg} ({commit['hash']})\n"
        changelog += "\n"

    # Documentation
    if categories['docs']:
        changelog += "### 📚 Documentation\n\n"
        for commit in categories['docs']:
            msg = _CONVENTIONAL_PREFIX.sub('', commit['message']).strip()
            msg = _capitalize(msg)
            changelog += f"- {msg} ({commit['hash']})\n"
        changelog += "\n"

    # Refactoring
    if categories['refactor']:
        changelog += "### ♻️ Refactoring\n\n"
        for commit in categories['refactor']:
            msg = _CONVENTIONAL_PREFIX.sub('', commit['message']).strip()
            msg = _capitalize(msg)
            changelog += f"- {msg} ({commit['hash']})\n"
        changelog += "\n"

    # Tests
    if categories['tests']:
        changelog += "### 🧪 Tests\n\n"
        for commit in categories['tests']:
            msg = _CONVENTIONAL_PREFIX.sub('', commit['message']).strip()
            msg = _capitalize(msg)
            changelog += f"- {msg} ({commit['hash']})\n"
        changelog += "\n"

    # Other
    if categories['other']:
        changelog += "### 🔧 Other Changes\n\n"
        for commit in categories['other']:
            msg = commit['message'].strip()
            msg = _capitalize(msg)
            changelog += f"- {msg} ({commit['hash']})\n"
        changelog += "\n"

    return changelog

def update_changelog_file(new_content: str, changelog_path: Path):
    """Update CHANGELOG.md with new content"""
    if not changelog_path.exists():
        print_error(f"CHANGELOG.md not found at {changelog_path}")
        return False
    
    # Read existing changelog
    with open(changelog_path, 'r') as f:
        existing = f.read()
    
    # Find where to insert new content (after header)
    lines = existing.split('\n')
    header_end = 0
    for i, line in enumerate(lines):
        if line.startswith('## ['):
            header_end = i
            break
    
    if header_end == 0:
        # No existing releases, append after header
        for i, line in enumerate(lines):
            if line.strip() == '':
                header_end = i + 1
                break
    
    # Insert new content
    new_lines = lines[:header_end] + new_content.split('\n') + lines[header_end:]
    
    # Write back
    with open(changelog_path, 'w') as f:
        f.write('\n'.join(new_lines))
    
    return True

def validate_repo_state() -> bool:
    """Validate repository state before release"""
    print_info("Validating repository state...")
    
    # Check if git repo
    code, _, _ = run_command(['git', 'rev-parse', '--git-dir'])
    if code != 0:
        print_error("Not a git repository")
        return False
    
    # Check for uncommitted changes
    code, stdout, _ = run_command(['git', 'status', '--porcelain'])
    if stdout:
        print_error("Uncommitted changes detected. Commit or stash them first.")
        print(stdout)
        return False
    
    # Check if on main branch
    code, branch, _ = run_command(['git', 'branch', '--show-current'])
    if branch != 'main':
        print_warning(f"Not on main branch (current: {branch})")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return False
    
    # Check if remote exists
    code, _, _ = run_command(['git', 'remote', 'get-url', 'origin'])
    if code != 0:
        print_error("No remote 'origin' configured")
        return False
    
    print_success("Repository state validated")
    return True

def create_github_release(version: str, changelog: str, dry_run: bool = False) -> bool:
    """Create GitHub release using gh CLI"""
    if dry_run:
        print_info("DRY RUN: Would create GitHub release")
        return True
    
    print_info(f"Creating GitHub release v{version}...")
    
    # Create release using gh CLI
    cmd = [
        'gh', 'release', 'create', f'v{version}',
        '--title', f'v{version}',
        '--notes', changelog
    ]
    
    code, stdout, stderr = run_command(cmd)
    
    if code != 0:
        print_error(f"Failed to create GitHub release: {stderr}")
        return False
    
    print_success(f"GitHub release created: {stdout}")
    return True

def send_telegram_notification(version: str, changelog: str):
    """Send Telegram notification (optional)"""
    # Check if Telegram bot token and chat ID are configured
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print_info("Telegram notification skipped (not configured)")
        return
    
    message = f"🚀 *New Release: v{version}*\n\n{changelog}"
    
    try:
        import requests
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print_success("Telegram notification sent")
        else:
            print_warning(f"Telegram notification failed: {response.text}")
    except Exception as e:
        print_warning(f"Telegram notification failed: {e}")

def main():
    parser = argparse.ArgumentParser(
        description='Release Automation Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--patch', action='store_true', help='Bump patch version (1.2.2 → 1.2.3)')
    group.add_argument('--minor', action='store_true', help='Bump minor version (1.2.2 → 1.3.0)')
    group.add_argument('--major', action='store_true', help='Bump major version (1.2.2 → 2.0.0)')
    group.add_argument('--version', type=str, help='Custom version (e.g., 1.5.0)')
    
    parser.add_argument('--dry-run', action='store_true', help='Preview only, do not create release')
    parser.add_argument('--no-telegram', action='store_true', help='Skip Telegram notification')
    
    args = parser.parse_args()
    
    print_header("🚀 RELEASE AUTOMATION")
    
    # Validate repository state
    if not validate_repo_state():
        sys.exit(1)
    
    # Get current version
    current_version = get_current_version()
    if not current_version:
        print_warning("No existing tags found, starting from 1.0.0")
        current_version = "0.0.0"
    
    print_info(f"Current version: {current_version}")
    
    # Determine new version
    if args.version:
        new_version = args.version.lstrip('v')
    elif args.major:
        new_version = bump_version(current_version, 'major')
    elif args.minor:
        new_version = bump_version(current_version, 'minor')
    else:  # patch
        new_version = bump_version(current_version, 'patch')
    
    print_success(f"New version: {new_version}")
    
    # Get commits since last tag
    print_info("Analyzing commits...")
    commits = get_commits_since_last_tag()
    
    if not commits:
        print_warning("No new commits since last release")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(0)
    else:
        print_success(f"Found {len(commits)} commits")
    
    # Generate changelog
    print_info("Generating changelog...")
    changelog = generate_changelog(new_version, commits)
    
    print("\n" + "="*60)
    print("CHANGELOG PREVIEW:")
    print("="*60)
    print(changelog)
    print("="*60 + "\n")
    
    if args.dry_run:
        print_warning("DRY RUN MODE - No changes will be made")
        sys.exit(0)
    
    # Confirm
    response = input(f"\nCreate release v{new_version}? (y/N): ")
    if response.lower() != 'y':
        print_info("Release cancelled")
        sys.exit(0)
    
    # Update CHANGELOG.md
    print_info("Updating CHANGELOG.md...")
    changelog_path = Path.cwd() / 'CHANGELOG.md'
    if update_changelog_file(changelog, changelog_path):
        print_success("CHANGELOG.md updated")
    else:
        print_error("Failed to update CHANGELOG.md")
        sys.exit(1)
    
    # Commit CHANGELOG.md
    print_info("Committing CHANGELOG.md...")
    run_command(['git', 'add', 'CHANGELOG.md'])
    run_command(['git', 'commit', '-m', f'chore: Update CHANGELOG for v{new_version}'])
    
    # Create git tag
    print_info(f"Creating git tag v{new_version}...")
    code, _, stderr = run_command(['git', 'tag', '-a', f'v{new_version}', '-m', f'Release v{new_version}'])
    if code != 0:
        print_error(f"Failed to create tag: {stderr}")
        sys.exit(1)
    print_success(f"Tag v{new_version} created")
    
    # Push changes
    print_info("Pushing to remote...")
    code, _, stderr = run_command(['git', 'push', 'origin', 'main'])
    if code != 0:
        print_error(f"Failed to push: {stderr}")
        sys.exit(1)
    
    code, _, stderr = run_command(['git', 'push', 'origin', f'v{new_version}'])
    if code != 0:
        print_error(f"Failed to push tag: {stderr}")
        sys.exit(1)
    print_success("Pushed to remote")
    
    # Create GitHub release
    if not create_github_release(new_version, changelog):
        print_error("Failed to create GitHub release")
        sys.exit(1)
    
    # Send Telegram notification
    if not args.no_telegram:
        send_telegram_notification(new_version, changelog)
    
    print_header(f"✅ RELEASE v{new_version} COMPLETE!")
    print_success(f"Version: {current_version} → {new_version}")
    print_success(f"Commits: {len(commits)}")
    print_success(f"URL: https://github.com/kevinnft/ai-agent-skills/releases/tag/v{new_version}")
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Verify release on GitHub")
    print("2. Test installation: bash scripts/install.sh")
    print("3. Announce release to community")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print_warning("Release cancelled by user")
        print("="*60)
        sys.exit(1)
    except Exception as e:
        print("\n\n" + "="*60)
        print_error(f"Unexpected error: {e}")
        print("="*60)
        import traceback
        traceback.print_exc()
        sys.exit(1)
