# Contributing to AI Agent Skills

Thank you for your interest in contributing! This document provides guidelines for contributing to the AI Agent Skills repository.

## 🎯 What We Accept

Two kinds of contributions, with different rules:

### ✅ Original skills (authored for this repo)
- Author your own `SKILL.md` from scratch
- **Required frontmatter:** `name`, `description`, `author` (your handle)
- Clear documentation with concrete examples
- No external dependencies (pure markdown + linked scripts)
- Tested by you in at least one real session — describe how in the PR

### ✅ Aggregated skills (pulled from another public repo)
- **Required frontmatter:** `name`, `description`, `source_repo`, `source_url`, `source_license`
- Upstream license must permit redistribution (MIT/Apache-2.0/BSD/CC-BY/etc.)
- Do not modify upstream skill content beyond frontmatter additions
- If you make substantive edits, mark with `derived_from:` instead of `source_url:`
- Link directly to the upstream commit hash if the upstream repo is fast-moving

### ✅ Improvements
- Bug fixes in existing skills
- Better examples and documentation
- Performance improvements
- Typo fixes
- Adding missing source attribution to existing aggregated skills

### ✅ Translations
- Translate skills to other languages
- Maintain same structure and quality
- Add `translation_of:` frontmatter pointing to the original

### ❌ What we don't accept
- Skills with external runtime dependencies that aren't documented
- Pure theoretical skills with no runnable example
- Duplicate skills (check existing categories first — `find skills -name SKILL.md | xargs grep -l "your-keyword"`)
- Skills without proper documentation
- **Aggregated content without `source_url:` attribution**
- Skills that misrepresent authorship of upstream work

## 📝 Skill Format

Every skill must follow this structure:

```markdown
---
name: skill-name
description: One-line description of when to use this skill
tags: [tag1, tag2, tag3]
---

# Skill Title

Brief description of what the skill does.

## When to Use

- Clear trigger conditions
- Specific use cases

## How It Works

Step-by-step explanation

## Examples

Concrete examples with code

## Best Practices

Tips and recommendations

## References

Links to documentation
```

### Required fields (original skills)

- `name`: lowercase, hyphens/underscores only
- `description`: one-line, clear trigger phrases
- `author`: your GitHub handle (or other contact)
- `tags`: relevant keywords

### Required fields (aggregated skills)

- `name`, `description`, `tags` (as above)
- `source_repo`: e.g. `"addyosmani/agent-skills"`
- `source_url`: the upstream URL (repo or specific path)
- `source_license`: SPDX identifier (`MIT`, `Apache-2.0`, etc.)

### Optional fields

- `version`: skill version
- `requires`: dependencies (if any) — be specific about what
- `derived_from`: if you substantively edited an upstream skill
- `translation_of`: for translations

## 🔧 Development Workflow

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/ai-agent-skills.git
cd ai-agent-skills
```

### 2. Create Branch

```bash
git checkout -b feature/my-new-skill
```

### 3. Add Your Skill

```bash
# Create skill directory
mkdir -p skills/category-name/skill-name

# Create SKILL.md
cat > skills/category-name/skill-name/SKILL.md << 'EOF'
---
name: skill-name
description: Description here
tags: [tag1, tag2]
---

# Skill Content
EOF
```

### 4. Validate

```bash
# Validate your skill
./scripts/validate.sh

# Test installation
./scripts/install.sh --category category-name --validate
```

### 5. Commit & Push

```bash
git add skills/category-name/skill-name/
git commit -m "feat: add skill-name skill"
git push origin feature/my-new-skill
```

### 6. Create Pull Request

- Go to GitHub and create a PR
- Fill in the PR template
- Wait for review

## ✅ Quality Checklist

Before submitting, ensure:

- [ ] Skill has valid YAML frontmatter
- [ ] Name is lowercase with hyphens/underscores
- [ ] Description is clear and concise
- [ ] Has "When to Use" section
- [ ] Has concrete examples
- [ ] Has proper markdown formatting
- [ ] No broken links
- [ ] Passes validation script
- [ ] **For original skills:** `author:` field set, tested in at least one real session
- [ ] **For aggregated skills:** `source_repo:`, `source_url:`, `source_license:` fields set; upstream license permits redistribution

## 📚 Skill Categories

Place your skill in the appropriate category:

- **engineering**: Code quality, testing, debugging
- **creative**: Visual content, diagrams, design
- **mlops**: ML/AI operations, training, inference
- **devops**: Infrastructure, deployment, operations
- **github**: GitHub workflows, repo management
- **research**: Analysis, data extraction, papers
- **productivity**: Tools, integrations, automation
- **software-development**: Development workflows

If your skill doesn't fit existing categories, propose a new one in your PR.

## 🎨 Style Guide

### Markdown

- Use ATX-style headers (`#` not `===`)
- Use fenced code blocks with language tags
- Use bullet lists for items
- Use numbered lists for steps
- Keep lines under 120 characters

### Code Examples

- Include language tags: ` ```python `, ` ```bash `
- Show complete, working examples
- Add comments for clarity
- Use realistic variable names

### Tone

- Be clear and concise
- Use active voice
- Avoid jargon (or explain it)
- Write for developers

## 🐛 Reporting Issues

Found a bug? Please report it!

### Bug Report Template

```markdown
**Skill Name**: skill-name
**Category**: category-name

**Description**:
Clear description of the issue

**Expected Behavior**:
What should happen

**Actual Behavior**:
What actually happens

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Step 3

**Environment**:
- Agent: Hermes/Claude/Cursor
- OS: Linux/macOS/Windows
- Version: x.x.x
```

## 💡 Feature Requests

Have an idea? Open an issue with:

- Clear description of the feature
- Use cases and benefits
- Example usage (if applicable)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the Golden Rule

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

All contributors will be recognized in:
- README.md contributors section
- CHANGELOG.md for each release
- GitHub contributors page

## 📞 Questions?

- Open an issue for questions
- Join our Discord community
- Check existing issues first

---

**Thank you for contributing!** 🎉

Your contributions help make AI agents more powerful and accessible to everyone.
