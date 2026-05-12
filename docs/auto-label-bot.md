# Auto-Label Bot

Automatic labeling system for Pull Requests and Issues using GitHub Actions.

## 🎯 What It Does

The Auto-Label Bot automatically applies relevant labels to PRs and Issues based on:
- Files changed
- Programming languages
- Folder structure
- Keywords in title/description
- PR size (lines changed)

## 🏷️ Label Categories

### Type Labels
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `maintenance` - Maintenance and updates
- `cleanup` - Code cleanup and refactoring
- `refactor` - Code refactoring
- `security` - Security related
- `performance` - Performance improvements
- `tests` - Testing related
- `question` - Further information is requested

### Component Labels
- `documentation` - Documentation improvements
- `skills` - Related to skills
- `scripts` - Related to scripts
- `github-actions` - GitHub Actions workflows
- `config` - Configuration files

### Language Labels
- `python` - Python code
- `javascript` - JavaScript/TypeScript code
- `bash` - Bash/Shell scripts

### Category Labels
- `research` - Research category
- `devops` - DevOps category
- `creative` - Creative category
- `development` - Development category
- `mlops` - MLOps category
- `github` - GitHub category
- `productivity` - Productivity category
- `ai-agents` - AI Agents category

### Special Labels
- `new-skill` - New skill addition
- `installation` - Installation related
- `validation` - Validation related
- `help-wanted` - Extra attention is needed
- `good-first-issue` - Good for newcomers
- `priority: high` - High priority

### Size Labels
- `size/XS` - Extra small changes (<10 lines)
- `size/S` - Small changes (10-50 lines)
- `size/M` - Medium changes (50-200 lines)
- `size/L` - Large changes (200-500 lines)
- `size/XL` - Extra large changes (>500 lines)

## 🔧 How It Works

### For Pull Requests

The bot analyzes:
1. **Files changed** - Detects folders (docs/, skills/, scripts/)
2. **File extensions** - Detects languages (.py, .js, .sh, .md)
3. **Skill categories** - Detects category from path (skills/research/, skills/devops/)
4. **File status** - Detects if files are added, modified, or removed
5. **PR title** - Detects keywords (fix, bug, add, new, update, refactor)
6. **PR size** - Calculates total lines changed

### For Issues

The bot analyzes:
1. **Title keywords** - Detects type (bug, feature, question, docs)
2. **Body content** - Detects components (install.sh, skills, readme)
3. **Priority keywords** - Detects urgency (critical, urgent)
4. **Help keywords** - Detects if help is needed

## 📋 Examples

### Example 1: New Skill PR
```
PR: "Add web scraping skill for Python"
Files: skills/research/web-scraping/SKILL.md
       skills/research/web-scraping/scripts/scraper.py

Auto-applied labels:
🏷️ skills
🏷️ research
🏷️ python
🏷️ enhancement
🏷️ new-skill
🏷️ size/M
```

### Example 2: Bug Fix PR
```
PR: "Fix broken links in README"
Files: README.md

Auto-applied labels:
🏷️ documentation
🏷️ bug
🏷️ size/XS
```

### Example 3: Script Update PR
```
PR: "Improve install.sh error handling"
Files: scripts/install.sh

Auto-applied labels:
🏷️ scripts
🏷️ bash
🏷️ maintenance
🏷️ size/S
```

### Example 4: Bug Report Issue
```
Issue: "Bug: install.sh fails on Ubuntu 22.04"

Auto-applied labels:
🏷️ bug
🏷️ scripts
🏷️ installation
```

## 🚀 Setup

### Prerequisites
- GitHub repository with Actions enabled
- Permissions: `issues: write`, `pull-requests: write`

### Installation

1. **Create labels** (one-time setup):
```bash
bash scripts/create-labels.sh
```

2. **Workflow is already set up** at `.github/workflows/auto-label.yml`

3. **Test it**:
   - Create a test PR
   - Bot will automatically apply labels within seconds

## 🔄 Workflow Triggers

The bot runs automatically on:
- `pull_request` events: opened, edited, synchronize, reopened
- `issues` events: opened, edited

## 📊 Benefits

- ✅ **Save time**: 0 seconds vs 2-3 minutes manual labeling
- ✅ **Consistency**: 100% consistent labeling
- ✅ **Organization**: Better PR/issue tracking
- ✅ **Professional**: Automated workflow
- ✅ **Zero cost**: Free GitHub Actions
- ✅ **Zero maintenance**: Runs automatically

## 🛠️ Customization

To customize label rules, edit `.github/workflows/auto-label.yml`:

```yaml
# Add custom folder detection
if (filename.includes('custom-folder/')) {
  labels.add('custom-label');
}

# Add custom keyword detection
if (title.includes('custom-keyword')) {
  labels.add('custom-label');
}
```

## 📝 Notes

- Labels are applied **in addition** to existing labels (not replaced)
- Bot runs on every PR/issue update
- Bot requires `GITHUB_TOKEN` (automatically provided by GitHub Actions)
- All 35 labels are created by `scripts/create-labels.sh`

## 🐛 Troubleshooting

### Bot not running?
- Check Actions tab in GitHub
- Verify workflow file exists at `.github/workflows/auto-label.yml`
- Check repository permissions

### Labels not applied?
- Check Actions logs for errors
- Verify labels exist in repository
- Run `scripts/create-labels.sh` to create missing labels

### Wrong labels applied?
- Review workflow logic in `.github/workflows/auto-label.yml`
- Customize rules as needed
- Test with a draft PR

## 📚 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Script Action](https://github.com/actions/github-script)
- [GitHub REST API - Labels](https://docs.github.com/en/rest/issues/labels)

## 🎉 Success!

The Auto-Label Bot is now active and will automatically label all new PRs and Issues!

**Total labels:** 35  
**Setup time:** 30 minutes  
**Maintenance:** Zero  
**Cost:** $0 (Free GitHub Actions)  
**ROI:** ⭐⭐⭐⭐⭐
