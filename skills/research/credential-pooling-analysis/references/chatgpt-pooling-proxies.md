# ChatGPT Credential Pooling Proxies

Self-hosted proxy solutions for pooling multiple ChatGPT Plus accounts into a single 0penAI-compatible API endpoint.

## Use Case

User has multiple ChatGPT Plus accounts and wants:
- Single API key + base URL for all accounts
- Automatic rotation across accounts
- Unlimited usage (bypass per-account rate limits)
- 0penAI-compatible API for drop-in replacement

## Solutions

### 1. PandoraNext (Full-Featured)

**Best for**: Users who want web UI, monitoring, and enterprise features

**Specs**:
- Disk: ~200-300MB
- RAM: ~100-150MB
- Features: Web UI, token pooling, rate limiting, health checks
- Support: GPT-4, GPT-4 Turbo, o1, DALL-E

**Install (Docker)**:
```bash
docker run -d \
  --name pandoranext \
  -p 8080:8080 \
  -v ./data:/data \
  pengzhile/pandora-next:latest
```

**Config** (`data/config.json`):
```json
{
  "accounts": [
    {"username": "user1@gmail.com", "password": "pass1"},
    {"username": "user2@gmail.com", "password": "pass2"}
  ],
  "proxy_url": "http://0.0.0.0:8080",
  "api_keys": ["sk-your-custom-key-here"]
}
```

**Pros**:
- Full-featured dashboard
- Health monitoring
- Auto token refresh
- Fallback logic

**Cons**:
- Heavier resource usage
- More complex setup
- Overkill for simple use cases

**Resource Fit**:
- ✅ Windows host (plenty of resources)
- ⚠️ VPS (2GB RAM, 40GB disk) — acceptable but monitor usage
- ❌ Constrained VPS (<1GB RAM) — too heavy

---

### 2. ChatGPT-to-API (Lightweight)

**Best for**: Resource-constrained VPS, simple pooling needs

**Specs**:
- Disk: ~50-100MB
- RAM: ~50-100MB
- Features: Basic pooling, 0penAI-compatible API
- Support: GPT-4, GPT-4 Turbo, streaming

**Install**:
```bash
git clone https://github.com/acheong08/ChatGPT-to-API
cd ChatGPT-to-API
pip install -r requirements.txt
```

**Config** (`accounts.json`):
```json
[
  {"email": "user1@gmail.com", "password": "pass1"},
  {"email": "user2@gmail.com", "password": "pass2"}
]
```

**Run**:
```bash
python server.py --accounts accounts.json --port 8080
```

**Pros**:
- Minimal resource usage
- Simple setup
- Fast startup
- Easy to debug (Python)

**Cons**:
- No web UI
- Basic features only
- Manual monitoring

**Resource Fit**:
- ✅ VPS (2GB RAM, 40GB disk) — perfect fit
- ✅ Windows host — works but underutilizes resources
- ✅ Constrained VPS — ideal choice

---

### 3. Ninja (Commercial/Self-Host)

**Best for**: Enterprise deployments, high reliability needs

**Specs**:
- Disk: ~300-500MB
- RAM: ~200-300MB
- Features: Enterprise-grade pooling, SLA monitoring, auto-recovery
- Support: All ChatGPT models

**Note**: Primarily commercial SaaS, self-host version less documented

**Pros**:
- Production-ready
- High reliability
- Advanced features

**Cons**:
- Commercial focus (self-host not priority)
- Heavier than alternatives
- Less community support

**Resource Fit**:
- ✅ Windows host
- ⚠️ VPS (2GB RAM) — borderline, monitor closely
- ❌ Constrained VPS — too heavy

---

### 4. Extend Existing enowxai Proxy

**Best for**: Users already running enowxai proxy (Windows host)

**Concept**: Add ChatGPT provider to existing proxy config

**Pros**:
- Reuse existing infrastructure
- Single proxy for all services (Kiro, CodeBuddy, ChatGPT)
- Unified monitoring

**Cons**:
- Requires enowxai proxy source code access
- Custom development needed
- Depends on proxy's extensibility

**Feasibility**: Check if enowxai proxy supports custom providers

---

## Recommendation Matrix

| Scenario | Recommended Solution | Reason |
|----------|---------------------|--------|
| VPS (2GB RAM, 40GB disk) | **ChatGPT-to-API** | Lightweight, fits resource constraints |
| Windows host (plenty of resources) | **PandoraNext** | Full features, monitoring, no resource concerns |
| Already running enowxai proxy | **Extend existing** | Reuse infrastructure, unified management |
| Enterprise/production | **Ninja** | High reliability, SLA guarantees |

## Authentication Methods

All solutions support:
1. **Email + Password**: Direct login credentials
2. **Session Tokens**: Extract from browser cookies (longer-lived, more stable)

**Session token extraction**:
```javascript
// In browser console on chat.openai.com
console.log(document.cookie.match(/__Secure-next-auth.session-token=([^;]+)/)[1])
```

## Integration with Hermes

After proxy is running:

```bash
# Configure Hermes to use proxy
hermes config set providers.chatgpt.base_url http://PROXY_IP:8080/v1
hermes config set providers.chatgpt.api_key sk-your-custom-key
hermes config set providers.chatgpt.models '["gpt-4", "gpt-4-turbo", "gpt-4o"]'

# Test
hermes chat --provider chatgpt --model gpt-4 "test message"
```

**For WSL2 accessing Windows proxy**:
```bash
# Get Windows host IP from WSL
WINDOWS_IP=$(ip route show default | awk '{print $3}')

# Configure with gateway IP
hermes config set providers.chatgpt.base_url http://${WINDOWS_IP}:8080/v1
```

## Monitoring

**Check proxy health**:
```bash
# Test API endpoint
curl http://PROXY_IP:8080/v1/models

# Check account status (if proxy has status endpoint)
curl http://PROXY_IP:8080/status
```

**Monitor resource usage**:
```bash
# Docker (if using PandoraNext)
docker stats pandoranext

# Process (if using ChatGPT-to-API)
ps aux | grep "python server.py"
top -p $(pgrep -f "python server.py")
```

## Pitfalls

### 1. Account Ban Risk

**Problem**: ChatGPT detects pooling patterns, bans accounts

**Mitigation**:
- Rotate IPs (use proxy with residential IPs)
- Randomize request timing
- Limit requests per account per hour
- Use session tokens (more stable than password login)

### 2. Session Token Expiry

**Problem**: Session tokens expire, proxy stops working

**Mitigation**:
- Monitor token validity
- Auto-refresh tokens
- Fallback to password login
- Alert on token expiry

### 3. Rate Limiting

**Problem**: Even with pooling, hitting aggregate rate limits

**Mitigation**:
- Implement request queuing
- Add delays between requests
- Monitor per-account usage
- Scale account pool size

### 4. VPS Resource Exhaustion

**Problem**: Proxy consumes too much RAM/disk on constrained VPS

**Solution**:
- Use ChatGPT-to-API (lightest option)
- Monitor with `htop`, `df -h`
- Set memory limits (Docker: `--memory=200m`)
- Kill proxy if exceeds threshold

## Related

- `windows-local-ai-services` skill — Running AI services on Windows with WSL2 access
- `vps-cleanup` skill — Resource evaluation criteria for VPS deployments
- Main skill (`credential-pooling-analysis`) — Economics and sustainability analysis
