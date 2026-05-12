# Skill Writing Reference

Complete reference for writing high-quality agent skills.

---

## Skill Structure

### Required Components

1. **YAML Frontmatter**
   ```yaml
   ---
   name: skill-name
   description: Brief description (one sentence)
   ---
   ```

2. **Main Heading**
   ```markdown
   # Skill Name
   ```

3. **Core Sections**
   - When to Use
   - How It Works
   - Examples

---

## YAML Frontmatter Fields

### Required Fields

- **name**: Lowercase, hyphens/underscores, max 64 chars
- **description**: One-sentence summary, under 200 chars

### Optional Fields

- **tags**: Array of keywords for discovery
- **category**: Skill category (e.g., 'devops', 'creative')
- **version**: Semantic version (e.g., '1.0.0')
- **author**: Author name or GitHub username
- **disable-model-invocation**: Set to `true` for prompt-only skills

---

## Content Guidelines

### When to Use Section

Describe trigger conditions:
- User intent patterns
- Keywords that should activate the skill
- Specific scenarios

**Example:**
```markdown
## When to Use

- User mentions "code review" or "review my code"
- Before merging any pull request
- When implementing critical features
```

### How It Works Section

Explain the process:
- Step-by-step workflow
- What the agent will do
- Expected outcomes

**Example:**
```markdown
## How It Works

1. Read the changed files
2. Check for common issues
3. Provide actionable feedback
4. Suggest improvements
```

### Examples Section

Provide concrete examples:
- Real-world use cases
- Sample inputs/outputs
- Code snippets

**Example:**
```markdown
## Examples

### Basic Usage

User: "Review my changes"

Agent: [Reads files, analyzes code, provides feedback]
```

---

## Best Practices

### Writing Style

- **Be concise**: One skill, one purpose
- **Be specific**: Clear trigger conditions
- **Be actionable**: Concrete steps, not vague advice
- **Be complete**: Include all necessary context

### Skill Naming

- Use lowercase with hyphens: `code-review-and-quality`
- Be descriptive: Name should indicate purpose
- Avoid abbreviations unless widely known
- Keep under 64 characters

### Description Writing

- One sentence, under 200 characters
- Start with action verb: "Automates...", "Guides...", "Validates..."
- Include trigger hint: "Use when..."
- Be specific about what it does

---

## Common Patterns

### Workflow Skills

For multi-step processes:

```markdown
## Process

1. **Step 1**: Description
   - Sub-step A
   - Sub-step B

2. **Step 2**: Description
   - Sub-step A
   - Sub-step B
```

### Validation Skills

For checking/validating:

```markdown
## Validation Checklist

- [ ] Check A
- [ ] Check B
- [ ] Check C

## What to Look For

- Issue 1: How to detect, how to fix
- Issue 2: How to detect, how to fix
```

### Template Skills

For generating content:

```markdown
## Template

\`\`\`
[Template content here]
\`\`\`

## Customization

- Field 1: Description
- Field 2: Description
```

---

## File Organization

### Single-File Skills

Simple skills in one SKILL.md:

```
skill-name/
└── SKILL.md
```

### Multi-File Skills

Complex skills with supporting files:

```
skill-name/
├── SKILL.md
├── references/
│   ├── api-docs.md
│   └── examples.md
├── templates/
│   └── config.yaml
└── scripts/
    └── helper.sh
```

---

## Testing Your Skill

### Validation Checklist

- [ ] YAML frontmatter is valid
- [ ] Name is lowercase with hyphens
- [ ] Description is under 200 chars
- [ ] Has main heading
- [ ] Has "When to Use" section
- [ ] Has clear examples
- [ ] No broken links
- [ ] No typos

### Manual Testing

1. Install the skill
2. Trigger it with test input
3. Verify expected behavior
4. Check edge cases

---

## Examples of Great Skills

### Minimal Skill

```markdown
---
name: zoom-out
description: Request broader context or higher-level perspective
---

# Zoom Out

## When to Use

When you're unfamiliar with code and need the big picture.

## Request

I don't know this area well. Go up a layer of abstraction. 
Give me a map of relevant modules and callers.
```

### Complete Skill

```markdown
---
name: code-review-and-quality
description: Conduct multi-axis code review before merging
tags: [code-review, quality, testing]
---

# Code Review and Quality

## When to Use

- Before merging any pull request
- When implementing critical features
- After major refactoring

## Review Checklist

### Correctness
- [ ] Logic is sound
- [ ] Edge cases handled
- [ ] No obvious bugs

### Quality
- [ ] Code is readable
- [ ] Names are clear
- [ ] No duplication

### Testing
- [ ] Tests exist
- [ ] Tests pass
- [ ] Coverage adequate

## Process

1. Read all changed files
2. Check each item in checklist
3. Provide specific feedback
4. Suggest improvements

## Examples

[Concrete examples here]
```

---

## Common Mistakes

### ❌ Avoid

- Vague descriptions: "Helps with code"
- Missing trigger conditions
- No examples
- Overly complex single skills
- Broken internal links

### ✅ Do

- Specific descriptions: "Validates API responses against schema"
- Clear trigger patterns
- Concrete examples
- One focused purpose per skill
- Test all links

---

## Resources

- [Hermes Agent Docs](https://hermes-agent.nousresearch.com/docs)
- [Skill Examples](../../)
- [YAML Validator](https://www.yamllint.com/)

---

**Questions?** Open an issue or discussion in the repository.
