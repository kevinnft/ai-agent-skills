# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

We take the security of AI Agent Skills seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do Not** Open a Public Issue

Please do not report security vulnerabilities through public GitHub issues.

### 2. Report Privately

Instead, please report security vulnerabilities by emailing:

**Email:** [Create a private security advisory on GitHub](https://github.com/kevinnft/ai-agent-skills/security/advisories/new)

Or open a private security advisory directly on GitHub.

### 3. Include Details

Please include the following information:

- **Type of vulnerability** (e.g., code injection, XSS, path traversal)
- **Full paths** of source file(s) related to the vulnerability
- **Location** of the affected source code (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact** of the vulnerability (what an attacker could do)

### 4. Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next release cycle

---

## Security Best Practices

### For Users

When using AI Agent Skills:

1. **Review Skills Before Use**
   - Read skill content before installation
   - Check for suspicious commands or patterns
   - Verify source attribution

2. **Keep Updated**
   - Use `./scripts/update.sh` regularly
   - Check for security advisories
   - Follow release notes

3. **Validate Installation**
   - Run `./scripts/validate.sh` after installation
   - Check for unexpected files
   - Verify checksums if provided

4. **Sandbox Testing**
   - Test new skills in isolated environments first
   - Use containers or VMs for untrusted skills
   - Monitor system behavior

### For Contributors

When contributing skills:

1. **No Secrets**
   - Never include API keys, tokens, or passwords
   - Use environment variables for sensitive data
   - Check commits for accidental leaks

2. **Input Validation**
   - Validate all user inputs
   - Sanitize file paths
   - Escape shell commands

3. **Safe Defaults**
   - Fail securely by default
   - Require explicit confirmation for destructive actions
   - Use least privilege principle

4. **Dependencies**
   - Minimize external dependencies
   - Pin dependency versions
   - Audit dependencies regularly

---

## Known Security Considerations

### Skill Execution

Skills are markdown files with instructions for AI agents. They do not execute code directly, but:

- **AI agents may execute commands** based on skill instructions
- **Users should review** what skills instruct agents to do
- **Malicious skills** could instruct agents to perform harmful actions

### Mitigation

1. **Review Before Use:** Always read skill content
2. **Trusted Sources:** Skills curated from reputable sources (186K+ stars)
3. **Validation:** Use validation script to check skill integrity
4. **Agent Safeguards:** Modern AI agents have built-in safety checks

---

## Security Updates

Security updates are released as:

- **Patch versions** (e.g., 1.1.1) for security fixes
- **GitHub Security Advisories** for critical issues
- **CHANGELOG.md** entries marked with `[SECURITY]`

Subscribe to:
- [GitHub Security Advisories](https://github.com/kevinnft/ai-agent-skills/security/advisories)
- [Release notifications](https://github.com/kevinnft/ai-agent-skills/releases)

---

## Scope

### In Scope

- Skill content that could lead to code execution vulnerabilities
- Installation scripts (install.sh, update.sh, validate.sh)
- Documentation that could mislead users into unsafe practices
- Dependencies with known vulnerabilities

### Out of Scope

- AI agent behavior (report to agent maintainers)
- Third-party tools referenced in skills
- User misconfiguration
- Social engineering attacks

---

## Attribution

We believe in responsible disclosure and will credit security researchers who report vulnerabilities (unless they prefer to remain anonymous).

---

## Questions?

For security questions that are not vulnerabilities, please open a regular GitHub issue or discussion.

---

**Thank you for helping keep AI Agent Skills secure!** 🔒
