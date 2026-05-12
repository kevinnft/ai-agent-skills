# NFT Analysis When OpenSea Blocks Direct Access

## Problem

OpenSea (and many NFT platforms) use Cloudflare protection that blocks:
- Direct HTTP requests (403 Forbidden)
- Standard web scraping tools
- Automated data collection

This makes it impossible to get real-time metrics (floor price, volume, holders) programmatically.

## Workflow

### Step 1: Try Direct Scraping

```bash
# Always try simplest approach first
curl -s "https://opensea.io/collection/xyz/overview" \
  -H "User-Agent: Mozilla/5.0"
```

**Expected result:** 403 Forbidden (Cloudflare block)

### Step 2: Try Cloud Browser (Browserbase)

```python
# Create session
session = create_browserbase_session()

# Attempt automation
# Problem: Requires Playwright/Selenium SDK
# VPS constraint: pip install blocked on Ubuntu 24.04
```

**Expected result:** Session created but can't automate without SDK

### Step 3: Delegate Research to Subagent

When automation blocked, delegate to subagent with web search:

```python
delegate_task(
    context=f"User wants analysis of '{collection_name}' NFT collection on OpenSea. URL: {url}. OpenSea blocks direct HTTP (403 Cloudflare). Browserbase session created but can't automate without Playwright SDK. Need alternative approach: web search + research to gather data.",
    goal=f"""Research and analyze '{collection_name}' NFT collection.
    
    Tasks:
    1. Web search for '{collection_name} NFT OpenSea' to find info
    2. Search for floor price, volume, sales data
    3. Find collection description, artist info
    4. Check Twitter/social media for community
    5. Analyze if it's active or dead project
    6. Provide buy/sell recommendation
    
    Create comprehensive analysis report with all findings.""",
    toolsets=["web", "terminal"]
)
```

### Step 4: Analyze Subagent Report

Subagent will:
- ✅ Find collection existence (OpenSea URL, Twitter, NFT Calendar)
- ✅ Identify available information sources
- ❌ Cannot access critical metrics (floor price, volume, holders)
- ✅ Provide conservative recommendation based on limited data

### Step 5: Conservative Recommendation

**When data is insufficient:**

```
Recommendation: DO NOT BUY

Reasoning:
1. Insufficient Data — Cannot verify floor price, volume, activity
2. Lack of Transparency — Difficulty accessing basic info = RED FLAG
3. Unknown Risk — Cannot assess liquidity or demand
4. Market Context — NFT market declined since 2022 peak
5. Due Diligence Incomplete — Cannot verify project legitimacy

Risk Level: UNKNOWN (Assume HIGH)
```

**Key principle:** When you can't verify data, assume high risk and recommend avoiding.

## Example: Anita Onink NFT

**Session:** 2026-05-03

**What we found:**
- ✅ Collection exists on OpenSea
- ✅ Has Twitter account (@ANITAONINKCTO)
- ✅ Listed on NFT Calendar
- ❌ Cannot verify floor price
- ❌ Cannot verify volume
- ❌ Cannot verify holders
- ❌ Cannot verify activity

**Recommendation:** DO NOT BUY (insufficient data)

**Report generated:** `/tmp/anita_onink_nft_analysis.md` (5.8KB)

**Key sections:**
1. Collection overview
2. Data collection challenges (technical limitations)
3. Available information sources (but inaccessible)
4. What we know vs. cannot verify
5. Preliminary assessment (insufficient data)
6. How to proceed (manual research required)
7. General NFT investment advice (2026 market context)

## Manual Research Checklist

If user insists on researching despite blocked access:

**1. Visit OpenSea directly in browser**
- Check floor price (current minimum)
- Check 24h volume (trading activity)
- Review recent sales (last 10-20)
- Examine holder distribution
- Note listed % (sell pressure indicator)

**2. Social media investigation**
- Twitter: follower count, tweet frequency, engagement
- Discord: member count, activity level, team presence
- Telegram: community size, discussion quality
- Look for announcements, roadmap updates

**3. Red flags to watch**
- Zero or very low volume (< 1 ETH/day)
- High listed % (> 50% = weak demand)
- Inactive social media (no posts in weeks)
- Anonymous team (no doxxed members)
- No utility or roadmap
- Suspicious holder distribution (few wallets hold most)

**4. Community sentiment**
- Search Twitter for mentions
- Check NFT Discord servers for discussions
- Look for reviews from NFT influencers
- Gauge overall sentiment (bullish/bearish/dead)

## Response Template

When OpenSea blocks access:

```markdown
# [COLLECTION NAME] NFT — ANALISA LENGKAP

## 🎯 JAWABAN SINGKAT

# ❌ JANGAN BELI — INSUFFICIENT DATA!

**Reason:** Gak bisa verify data penting (floor price, volume, activity)

---

## 📊 WHAT WE FOUND

### Collection Info:
- Name: [name]
- Platform: OpenSea
- URL: [url]
- Twitter: [handle]

### What We KNOW:
✅ Collection exists
✅ Has social media presence
✅ Listed on tracking platforms

### What We CANNOT Verify:
❌ Floor price (unknown)
❌ Volume (unknown)
❌ Holders (unknown)
❌ Activity (unknown)

---

## 🚧 TECHNICAL CHALLENGES

**Why we couldn't get full data:**

1. OpenSea Cloudflare Protection 🔴
   - Direct HTTP: ❌ 403 Forbidden
   - Automation: ❌ Need SDK (VPS restrictions)

2. Anti-Bot Measures 🔴
   - Web scraping: ❌ Blocked
   - API access: ❌ Requires authentication

---

## 🎯 RECOMMENDATION

# ❌ DO NOT BUY

**Reasoning:**

1. **Insufficient Data** 🔴
   - Cannot verify critical metrics
   - Decision impossible without data

2. **Lack of Transparency** 🔴
   - Difficulty accessing info = RED FLAG
   - Healthy projects have transparent data

3. **Unknown Risk** 🔴
   - Cannot assess liquidity, demand, legitimacy
   - Risk Level: UNKNOWN (Assume HIGH)

---

## 💡 IF YOU STILL WANT TO RESEARCH

**Manual steps required:**
1. Visit OpenSea directly (check floor, volume, sales)
2. Investigate social media (Twitter, Discord, Telegram)
3. Watch for red flags (low volume, inactive community, anonymous team)

**Better strategy:** Find NFT projects with:
- ✅ Transparent metrics (easy to find data)
- ✅ Active community (Discord 10k+)
- ✅ Clear utility (real use case)
- ✅ Proven track record (delivered roadmap)
```

## Lessons Learned

1. **Always try escalation ladder** — web_fetch → browser → cloud browser → delegate
2. **Conservative when data missing** — insufficient data = recommend avoiding
3. **Explain technical limitations** — user understands why we can't get data
4. **Provide manual research path** — if user insists, give them checklist
5. **Close cloud sessions immediately** — save credits, avoid rate limits
6. **Generate comprehensive report** — save to file for user reference

## Related Skills

- `cloud-browser-automation` — Browserbase usage patterns
- `web-scraping` — General web scraping techniques
- `crypto-token-analysis` — Similar analysis framework for tokens
