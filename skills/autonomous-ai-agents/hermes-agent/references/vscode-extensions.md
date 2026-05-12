# VSCode Extensions for Custom AI Providers

When users want to use custom AI providers (like enowxai proxy) in VSCode, recommend these extensions:

## Top 3 Extensions

### 1. Continue ⭐ MOST POPULAR
- **Name:** Continue
- **Publisher:** Continue
- **Downloads:** 1M+
- **Features:** Chat, inline edit, tab autocomplete, slash commands
- **Setup difficulty:** Easy (5 minutes)
- **Config location:** `~/.continue/config.json` (Windows: `C:\Users\USERNAME\.continue\config.json`)

**Config example:**
```json
{
  "models": [{
    "title": "Custom Provider",
    "provider": "openai",
    "model": "model-name",
    "apiKey": "DUMMY_KEY",
    "apiBase": "http://custom-endpoint/v1"
  }]
}
```

### 2. Cline (formerly CL4ude Dev) ⭐ MOST POWERFUL
- **Name:** Cline
- **Publisher:** Cline
- **Downloads:** 500K+
- **Features:** Autonomous agent, file operations, terminal access, browser automation
- **Setup difficulty:** Medium
- **Best for:** Complex autonomous tasks

### 3. Twinny ⭐ MOST LIGHTWEIGHT
- **Name:** Twinny
- **Publisher:** Twinny
- **Downloads:** 100K+
- **Features:** Chat, code completion, lightweight
- **Setup difficulty:** Easy
- **Best for:** Low resource usage, privacy-focused

## Extensions That DON'T Support Custom Providers

- ❌ GitHub Copilot (requires GitHub subscription)
- ❌ Codex (0penAI official, requires 0penAI key)
- ❌ Tabnine (enterprise only for custom providers)
- ❌ Cody (limited custom provider support)

## Recommendation Priority

1. **For general coding:** Continue (most popular, easy setup)
2. **For autonomous tasks:** Cline (most powerful)
3. **For lightweight:** Twinny (low resource usage)

## Common Issues

### WSL2 + Windows Setup
- Gateway IP from WSL: Use `ip route show default | awk '{print $3}'` (typically 172.17.16.1)
- localhost does NOT work cross-OS
- Firewall must allow the port
- Service must listen on 0.0.0.0, not 127.0.0.1

### Config File Locations
- **Continue:** `~/.continue/config.json`
- **Cline:** VSCode settings (JSON)
- **Twinny:** VSCode settings (JSON)

From WSL, copy to Windows:
```bash
cp config.json /mnt/c/Users/USERNAME/.continue/config.json
```
