# Usage Guide

Learn how to use AI Agent Skills effectively with examples and best practices.

---

## 🎯 Quick Start

Skills automatically trigger based on your intent. Just use your AI agent normally!

```bash
# Start Hermes
hermes chat

# Skills auto-trigger based on context
> "Let's build a new feature"
→ Automatically uses brainstorming skill

> "Add a component with tests"
→ Automatically uses TDD skill

> "Review my code"
→ Automatically uses code-review-and-quality skill
```

---

## 📚 Skill Categories

### 🏆 Engineering Skills

#### Code Review & Quality

**Skill:** `addyosmani/code-review-and-quality`

**When to use:** Before merging any code

**Example:**
```
User: Review the changes in src/components/Button.tsx

Agent: [Uses code-review-and-quality skill]
- Checks correctness, security, performance
- Validates against repo conventions
- Suggests improvements
```

---

#### Test-Driven Development

**Skill:** `mattpocock/tdd` or `superpowers/test-driven-development`

**When to use:** Implementing any feature or bugfix

**Example:**
```
User: Add a login form component

Agent: [Uses TDD skill]
1. Write failing test first
2. Implement minimal code to pass
3. Refactor while keeping tests green
```

---

#### Systematic Debugging

**Skill:** `mattpocock/diagnose` or `superpowers/systematic-debugging`

**When to use:** Encountering bugs or test failures

**Example:**
```
User: Tests are failing with "Cannot read property 'user' of undefined"

Agent: [Uses systematic-debugging skill]
1. Reproduce the issue
2. Minimize test case
3. Form hypothesis
4. Instrument code
5. Fix root cause
6. Add regression test
```

---

### 🎨 Creative Skills

#### Architecture Diagrams

**Skill:** `creative/architecture-diagram`

**When to use:** Visualizing system architecture

**Example:**
```
User: Create a diagram showing our microservices architecture

Agent: [Uses architecture-diagram skill]
- Generates dark-themed SVG diagram
- Shows services, databases, message queues
- Exports as HTML file
```

---

#### ASCII Art

**Skill:** `creative/ascii-art`

**When to use:** Creating terminal banners or visual elements

**Example:**
```
User: Create ASCII art banner for "AI Agent Skills"

Agent: [Uses ascii-art skill]
   _    ___      _                    _   
  /_\  |_ _|    /_\   __ _  ___ _ __ | |_ 
 //_\\  | |    //_\\ / _` |/ _ \ '_ \| __|
/  _  \ | |   /  _  \ (_| |  __/ | | | |_ 
\_/ \_/|___| \_/ \_/\__, |\___|_| |_|\__|
                    |___/                 
```

---

### 🤖 MLOps Skills

#### LLM Inference

**Skill:** `mlops/llama-cpp`

**When to use:** Running local LLM inference

**Example:**
```
User: Run Llama 3.1 8B locally with GGUF

Agent: [Uses llama-cpp skill]
1. Download model from HuggingFace
2. Convert to GGUF if needed
3. Run with llama.cpp
4. Configure context size, temperature
```

---

#### Fine-Tuning

**Skill:** `mlops/axolotl`

**When to use:** Fine-tuning LLMs with custom data

**Example:**
```
User: Fine-tune Llama 3.1 on my dataset

Agent: [Uses axolotl skill]
1. Prepare dataset in correct format
2. Create axolotl config YAML
3. Run training with LoRA
4. Merge and export model
```

---

### 🔧 DevOps Skills

#### Docker Compose

**Skill:** `devops/docker-compose`

**When to use:** Multi-container applications

**Example:**
```
User: Set up PostgreSQL + Redis + API server

Agent: [Uses docker-compose skill]
1. Create docker-compose.yml
2. Define services with networks
3. Configure volumes for persistence
4. Add health checks
5. Document startup commands
```

---

#### VPS Security

**Skill:** `devops/vps-security-hardening`

**When to use:** Securing a new VPS

**Example:**
```
User: Harden security on my Ubuntu VPS

Agent: [Uses vps-security-hardening skill]
1. Configure fail2ban
2. Harden SSH (disable root, key-only)
3. Setup UFW firewall
4. Enable automatic security updates
5. Configure audit logging
```

---

### 🐙 GitHub Skills

#### PR Workflow

**Skill:** `github/github-pr-workflow`

**When to use:** Creating pull requests

**Example:**
```
User: Create a PR for the new feature

Agent: [Uses github-pr-workflow skill]
1. Create feature branch
2. Commit changes with conventional commits
3. Push to remote
4. Create PR with gh CLI
5. Add description and reviewers
```

---

#### Code Review

**Skill:** `github/github-code-review`

**When to use:** Reviewing pull requests

**Example:**
```
User: Review PR #42

Agent: [Uses github-code-review skill]
1. Fetch PR diff
2. Review changes file by file
3. Add inline comments
4. Suggest improvements
5. Approve or request changes
```

---

### 🔬 Research Skills

#### Web Scraping

**Skill:** `research/web-scraping`

**When to use:** Extracting data from websites

**Example:**
```
User: Scrape product prices from example.com

Agent: [Uses web-scraping skill]
1. Inspect page structure
2. Write scraper with requests/BeautifulSoup
3. Handle pagination
4. Export to CSV/JSON
5. Add error handling
```

---

#### arXiv Papers

**Skill:** `research/arxiv`

**When to use:** Finding research papers

**Example:**
```
User: Find recent papers on transformer architectures

Agent: [Uses arxiv skill]
1. Search arXiv API
2. Filter by date, category
3. Download PDFs
4. Summarize abstracts
```

---

## 🎯 Best Practices

### 1. Let Skills Auto-Trigger

**Don't:**
```
User: Use the TDD skill to add a login form
```

**Do:**
```
User: Add a login form with tests
```

Skills trigger automatically based on intent. No need to explicitly name them.

---

### 2. Provide Context

**Don't:**
```
User: Fix the bug
```

**Do:**
```
User: Fix the bug in src/auth.ts where login fails with "Invalid token"
```

More context = better skill selection and execution.

---

### 3. Use Brainstorming First

**For any creative work:**
```
User: Let's build a new dashboard feature

Agent: [Automatically uses brainstorming skill]
- Explores requirements
- Discusses design options
- Plans implementation
- THEN starts coding
```

The `superpowers/brainstorming` skill is marked as **MUST USE** before creative work.

---

### 4. Verify Before Completion

**Always verify:**
```
User: Is the feature complete?

Agent: [Uses verification-before-completion skill]
- Runs tests
- Checks build
- Verifies functionality
- Provides evidence
```

Never claim work is done without verification.

---

### 5. Follow TDD

**For any implementation:**
```
1. Write failing test
2. Make it pass (minimal code)
3. Refactor
4. Repeat
```

The `tdd` skill enforces red-green-refactor loop.

---

## 🔄 Common Workflows

### Workflow 1: New Feature

```
1. Brainstorming
   → Explore requirements and design

2. Planning
   → Break into tasks with writing-plans skill

3. TDD Implementation
   → Write tests first, then code

4. Code Review
   → Review with code-review-and-quality skill

5. Verification
   → Verify all tests pass

6. PR Creation
   → Create PR with github-pr-workflow skill
```

---

### Workflow 2: Bug Fix

```
1. Systematic Debugging
   → Reproduce, minimize, diagnose

2. TDD Fix
   → Write regression test first
   → Fix bug
   → Verify test passes

3. Code Review
   → Review changes

4. PR Creation
   → Create PR with fix
```

---

### Workflow 3: Research Task

```
1. Web Scraping / arXiv Search
   → Gather data or papers

2. Analysis
   → Process and analyze data

3. Documentation
   → Document findings

4. Visualization
   → Create diagrams if needed
```

---

## 💡 Tips & Tricks

### Tip 1: Combine Skills

Skills can work together:

```
User: Build a microservices architecture with monitoring

Agent:
1. Uses architecture-diagram → Create visual design
2. Uses docker-compose → Setup containers
3. Uses api-testing → Test endpoints
4. Uses github-pr-workflow → Create PR
```

---

### Tip 2: Use Validation

Before installing or using skills:

```bash
# Validate all skills
./scripts/validate.sh

# Ensures:
# - Proper YAML frontmatter
# - Required fields present
# - Valid markdown structure
```

---

### Tip 3: Explore Categories

```bash
# List all categories
./scripts/install.sh --list

# Install category you need
./scripts/install.sh --category creative
```

---

### Tip 4: Read Skill Content

Skills contain:
- When to use
- How it works
- Examples
- Best practices
- References

Read `SKILL.md` files for details.

---

## 🐛 Troubleshooting

### Skill Not Triggering

**Problem:** Expected skill doesn't activate

**Solution:**
1. Be more explicit in your request
2. Mention the task type (e.g., "with tests", "review", "debug")
3. Check skill is installed: `find ~/.hermes/skills -name "SKILL.md" | grep skill-name`

---

### Wrong Skill Triggered

**Problem:** Different skill than expected activates

**Solution:**
1. Provide more context
2. Explicitly mention the approach (e.g., "using TDD")
3. Skills trigger based on intent matching

---

### Skill Errors

**Problem:** Skill execution fails

**Solution:**
1. Check skill requirements (some need external tools)
2. Verify dependencies installed
3. Report issue on GitHub

---

## 📚 Further Reading

- [Installation Guide](./installation.md)
- [Categories Overview](./categories.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Changelog](../CHANGELOG.md)

---

## 🤝 Getting Help

- [GitHub Issues](https://github.com/kevinnft/ai-agent-skills/issues)
- [Discussions](https://github.com/kevinnft/ai-agent-skills/discussions)

---

**Happy coding with AI Agent Skills!** 🚀
