# GitHub Token for Permanent Access

When user wants autonomous GitHub operations (create/delete repos, push, etc.) without repeated auth prompts, generate a permanent token with full scopes.

## Token Generation

**URL with pre-selected scopes:**
```
https://github.com/settings/tokens/new?scopes=repo,delete_repo,admin:org,workflow,gist&description=Hermes%20Full%20Access
```

**Scopes needed:**
- `repo` — Create, read, update repos
- `delete_repo` — Delete repos (separate from `repo`)
- `admin:org` — Manage organizations
- `workflow` — Manage GitHub Actions
- `gist` — Manage gists

**Expiration:** Select "No expiration" for permanent access

## Storage Strategy

**Dual storage for reliability:**

1. **Mnemosyne (fast recall):**
```python
mnemosyne_remember(
  content="GitHub permanent token for USERNAME: ghp_xxxx... (full access: repo, delete_repo, admin:org, workflow, gist, no expiration)",
  importance=0.9,
  source="credential"
)
```

2. **~/.bashrc (auto-load every session):**
```bash
echo "export GH_TOKEN='ghp_xxxx...'" >> ~/.bashrc
```

**Result:** Token available in all future sessions without re-auth.

## Usage

**With GitHub CLI:**
```bash
export GH_TOKEN='ghp_xxxx...'
gh repo create my-repo --public
gh repo delete username/my-repo --yes
```

**With Git:**
```bash
git clone https://USERNAME:TOKEN@github.com/username/repo.git
git push https://USERNAME:TOKEN@github.com/username/repo.git
```

## Security Considerations

**Risks:**
- Token grants full access to GitHub account
- If leaked, attacker can delete all repos
- No expiration = permanent risk

**Mitigations:**
- Store only in Mnemosyne + ~/.bashrc (not in code/repos)
- Use for automation only (not for manual operations)
- Revoke immediately if compromised: https://github.com/settings/tokens
- Consider scoped tokens for specific tasks (e.g., only `repo` for read/write)

## User Preference Signal

**"kerjain semuannya sendiri jngn kbanyakan nanya"** — User wants autonomous execution with minimal prompts. Permanent token enables this for GitHub operations.

**When to use:**
- User explicitly requests autonomous GitHub access
- Repeated GitHub operations in session (create/delete multiple repos)
- User frustrated with auth prompts

**When NOT to use:**
- One-time operations (use temporary token)
- Shared/public systems (security risk)
- User hasn't explicitly granted permission
