---
name: credential-pooling-analysis
description: Analyze credential pooling operations and API reseller business models — economics, risks, detection patterns, and sustainability
tags: [business-analysis, api-reseller, credential-pooling, arbitrage, economics]
related_skills: [web-scraping, cloud-browser-automation]
origin: unknown
source_license: see upstream
language: en
---

# Credential Pooling Analysis

Framework for analyzing API reseller operations that use credential pooling (bulk account creation → free tier exploitation → resell access at markup).

## What is Credential Pooling?

**Definition**: Acquiring many free/trial accounts from a service, pooling their credits/quotas, and reselling access to end-users at a markup.

**Common pattern**:
```
User → Reseller API → Credential Pool (100s of accounts) → Official API (Claude/GPT/etc)
```

**Economics**:
- Input: Bulk accounts (e.g., 100 Google accounts = $1-2)
- Multiplier: Each account gets $5-10 free credits
- Output: $500-1000 total credits
- Markup: Sell at 50-70% of official API price
- ROI: 50-100x return on account cost

## Analysis Framework

### 1. Identify the Operation

**Signals that indicate credential pooling**:

✅ **Pricing signals**:
- Significantly cheaper than official API (30-70% discount)
- Credit-based, not subscription
- "No subscription, just credits" messaging
- Prices that don't match any official tier

✅ **Technical signals**:
- Unified API for multiple providers (Claude + GPT + Gemini in one endpoint)
- OpenAI-compatible API (drop-in replacement)
- Frequent "maintenance" or "rate limit" messages
- Inconsistent response times

✅ **Business signals**:
- New/small operation (not official partner)
- Located in regions with cheap bulk accounts (Indonesia, India, etc)
- Telegram/Discord-only support (no official business presence)
- Vague about "how we get access"

### 2. Scrape and Extract Data

**Target pages**:
- Homepage (tagline, value prop)
- Pricing page (model list, credit costs)
- Docs (API endpoints, authentication)
- About/Contact (location, team, legitimacy signals)

**Use escalation ladder** (see `cloud-browser-automation` skill):
1. Try `web_fetch` first
2. Try direct curl with headers
3. Try Hermes browser
4. Use Browserbase if Cloudflare-protected

**Key data to extract**:
```python
{
  "site": "example.com",
  "tagline": "...",
  "models": ["claude-opus-4", "gpt-5", ...],
  "pricing": {"claude-opus-4": "$X per 1M tokens"},
  "features": ["streaming", "openai-compatible", ...],
  "contact": {"email": "...", "discord": "...", "telegram": "..."},
  "location": "...",
  "legal_docs": ["terms", "privacy", ...]
}
```

### 3. Economic Analysis

**Calculate unit economics**:

```python
# Input costs
accounts_cost = 100 * 0.02  # $2 for 100 Google accounts
credits_per_account = 7.5   # $7.50 average free credits
total_credits = 100 * credits_per_account  # $750

# Output revenue
markup = 0.5  # 50% of official price
official_price = 1.0
reseller_price = official_price * markup
revenue = total_credits / reseller_price  # How much they can sell

# Profit
profit = revenue - accounts_cost
roi = profit / accounts_cost
```

**Key metrics**:
- **ROI**: Return on investment (target: 20-100x)
- **Burn rate**: How fast credits deplete
- **Ban rate**: % of accounts that get banned
- **Sustainability**: Can they maintain supply?

### 4. Risk Assessment

**Operational risks**:

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| High ban rate | Service disruption | High (30-60%) | Diversify providers |
| Provider closes loophole | Business death | Medium | Have backup sources |
| Legal action | Shutdown | Low (hard to enforce) | Offshore entity |
| Detection patterns | Account bans | High | Rotate IPs, randomize usage |
| Credit exhaustion | Revenue loss | High | Continuous account creation |

**Provider-specific ban rates** (from user's data):
- **Kiro**: 58% ban rate (AWS actively blocks third-party harness)
- **CodeBuddy**: 0% ban rate (Tencent detection weak)
- **Cursor**: Unknown (not tested)

**Detection signals providers look for**:
- Same IP for many accounts
- Identical usage patterns
- Rapid sequential requests
- Unusual geographic distribution
- API key sharing patterns

### 5. Sustainability Analysis

**Short-term (0-6 months)**:
- ✅ Highly profitable (ROI 50-100x)
- ✅ Easy to scale (bulk accounts cheap)
- ⚠️ High churn (ban rate 30-60%)

**Medium-term (6-18 months)**:
- ⚠️ Provider detection improves
- ⚠️ Free tiers get restricted
- ⚠️ Competition increases (price war)

**Long-term (18+ months)**:
- ❌ Unsustainable (providers close loopholes)
- ❌ Legal risk increases
- ❌ Need to pivot to legitimate model

### 6. Competitive Analysis

**Compare multiple operations**:

```markdown
| Operator | Models | Pricing | Location | Stage | Risk Level |
|----------|--------|---------|----------|-------|------------|
| adye.dev | 7 models | 50% off | Unknown | Operational | High |
| enowxlabs.com | Unknown | Unknown | Indonesia | Beta | Medium |
```

**Differentiation strategies**:
- **Price**: Race to bottom (unsustainable)
- **Reliability**: Better uptime (requires more accounts)
- **Features**: Better API, docs, support
- **Niche**: Specific models or use cases

## Common Patterns

### Pattern 1: Pure API Reseller (adye.dev style)

**Characteristics**:
- Direct API proxy
- Multiple models in one endpoint
- Credit-based pricing
- Minimal branding

**Pros**:
- Simple to build
- Fast to market
- High margins

**Cons**:
- Commodity (easy to copy)
- High ban risk
- No moat

### Pattern 2: Software Marketplace (enowxlabs.com style)

**Characteristics**:
- Platform for developer tools
- Built-in licensing system
- API access as backend
- More legitimate appearance

**Pros**:
- Better optics (not just reseller)
- Multiple revenue streams
- Harder to shut down

**Cons**:
- More complex to build
- Slower to market
- Still relies on pooling

### Pattern 3: Hybrid Model

**Characteristics**:
- Tools + API access
- Subscription + credits
- White-label options

**Pros**:
- Diversified risk
- Higher LTV
- Stickier customers

**Cons**:
- Complex operations
- Higher overhead

## Recommendations

### For Operators (User Perspective)

**Optimization**:
1. **Focus on low-ban providers** (CodeBuddy 0% vs Kiro 58%)
2. **Automate rotation** (smart load balancer)
3. **Monitor ban rate** (track and adjust)
4. **Diversify sources** (don't rely on one provider)

**Risk mitigation**:
1. **Legal entity** (proper business structure)
2. **ToS compliance** (find providers that allow reselling)
3. **Backup plan** (alternative sources ready)
4. **Geographic distribution** (avoid single jurisdiction)

**Scaling strategy**:
1. Start with one provider (test economics)
2. Automate account creation and rotation
3. Add more providers (diversify)
4. Build legitimate features (moat)
5. Transition to official partnerships (long-term)

### For Analysts (Research Perspective)

**Red flags**:
- Prices too good to be true (70%+ discount)
- No official partnership claims
- Vague about infrastructure
- Frequent downtime
- New operation with many models

**Green flags**:
- Official partner badges
- Transparent pricing
- SLA guarantees
- Enterprise contracts
- Long track record

## Verification

After analysis, verify findings:

```bash
# Check if site is operational
curl -I https://example.com

# Test API endpoint (if public)
curl -X POST https://api.example.com/v1/chat/completions \
  -H "Authorization: Bearer test-key" \
  -H "Content-Type: application/json" \
  -d '{"model": "claude-opus-4", "messages": [{"role": "user", "content": "test"}]}'

# Check DNS/hosting
whois example.com
dig example.com

# Check social presence
# Discord, Telegram, GitHub, Twitter
```

## Output Format

**Executive summary**:
```markdown
## Executive Summary

[Site] is a [type] operation using [method] to provide [service].

**Economics**: ROI [X]x, [sustainability assessment]
**Risk**: [High/Medium/Low] — [key risks]
**Recommendation**: [Action for user]
```

**Full report structure**:
1. Identity (name, tagline, location, contact)
2. Business model (what they sell, how they position)
3. Technical analysis (API structure, features)
4. Economic analysis (unit economics, ROI)
5. Risk assessment (ban rates, sustainability)
6. Competitive analysis (vs similar operations)
7. Recommendations (optimize, mitigate, scale)

## Pitfalls

### 1. Assuming All Cheap APIs Are Pooling

**Problem**: Some legitimate providers have lower costs (different infrastructure, regions, partnerships)

**Solution**: Look for multiple signals, not just price

### 2. Overestimating Sustainability

**Problem**: High ROI looks attractive but ignores ban rate and provider countermeasures

**Solution**: Model worst-case scenarios (50%+ ban rate, free tier closure)

### 3. Ignoring Legal Risk

**Problem**: "Hard to enforce" ≠ "no risk"

**Solution**: Assess jurisdiction, provider aggressiveness, scale of operation

### 4. Missing the Moat

**Problem**: Pure reselling is commodity — easy to copy, race to bottom

**Solution**: Look for differentiation (features, reliability, niche, legitimacy)

## References

- `references/chatgpt-pooling-proxies.md` — Self-hosted ChatGPT pooling proxy solutions (PandoraNext, ChatGPT-to-API, Ninja)
- `references/case-study-enowxlabs-adye.md` — Case studies of existing operations
- User's credential pool data (Kiro 58% ban, CodeBuddy 0% ban)
- Bulk account pricing (100 Google accounts = Rp20k ≈ $1.25)
- Example operations: adye.dev (pure reseller), enowxlabs.com (marketplace)
