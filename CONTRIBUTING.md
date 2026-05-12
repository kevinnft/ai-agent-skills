# Contributing to AI Agent Skills

Thank you for your interest in contributing! This document provides guidelines for contributing to the AI Agent Skills repository.

## 🎯 What We Accept

### ✅ New Skills
- Production-tested skills with real-world use cases
- Clear documentation with examples
- Proper YAML frontmatter
- No external dependencies (pure markdown)

### ✅ Improvements
- Bug fixes in existing skills
- Better examples and documentation
- Performance improvements
- Typo fixes

### ✅ Translations
- Translate skills to other languages
- Maintain same structure and quality

### ❌ What We Don't Accept
- Skills with external dependencies
- Untested or theoretical skills
- Duplicate skills (check existing first)
- Skills without proper documentation

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

### Required Fields

- `name`: lowercase, hyphens/underscores only
- `description`: one-line, clear trigger phrases
- `tags`: relevant keywords

### Optional Fields

- `author`: skill author
- `version`: skill version
- `requires`: dependencies (if any)

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
- [ ] Tested in real use case

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
