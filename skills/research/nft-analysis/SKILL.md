---
name: nft-analysis
description: Analyze NFT projects for investment decisions — evaluate fundamentals, identify red flags, assess risk, and provide buy/hold/avoid recommendations
triggers:
  - analyze NFT project
  - should I buy this NFT
  - NFT investment analysis
  - is this NFT a good investment
  - NFT project evaluation
  - NFT due diligence
origin: unknown
source_license: see upstream
language: en
---

# NFT Project Analysis

Comprehensive framework for evaluating NFT projects and providing investment recommendations. Focuses on fundamentals, red flags, and risk assessment rather than speculation.

## When to Use

- User asks to analyze an NFT collection
- User asks "should I buy this NFT?"
- User wants to evaluate NFT project health
- User asks about NFT price trends or investment potential

## Analysis Framework

### 1. Data Collection

**Primary sources:**
- OpenSea (floor price, volume, holders, sales)
- Blur, LooksRare, Rarible (alternative marketplaces)
- Twitter (community size, engagement, updates)
- Discord/Telegram (community activity, team presence)
- Etherscan/blockchain explorer (contract, holder distribution)
- Project website (roadmap, team, utility)

**Key metrics:**
- Floor price (current + historical)
- Trading volume (24h, 7d, 30d)
- Total volume (all-time)
- Unique holders
- Total supply
- Recent sales activity
- **Listed count** (how many NFTs are listed for sale)
- **Marketplace presence** (which platforms list the collection)
- Social media followers
- Community engagement

**CRITICAL: Check marketplace liquidity FIRST**
- Verify NFT is actually listed on marketplaces (OpenSea, Blur, etc.)
- Check on-chain holders count (0 holders = NFTs stuck in contract)
- Verify contract is verified on block explorer
- If zero marketplace presence + zero holders = DEAD MARKET (instant avoid)

### 2. Chart Pattern Recognition

**Healthy patterns:**
- Gradual uptrend with consolidation zones
- Higher lows, higher highs
- Multiple horizontal support levels
- Steady volume growth
- Low volatility

**Death patterns:**
- Pump & dump (sharp spike → crash)
- Death spiral (continuous decline, no support)
- Extreme volatility (0 → peak → 0 → peak → 0)
- Declining volume
- No consolidation zones

**Example death chart:**
```
Launch:  0.1 ETH  (accumulation)
Month 2: 0.5 ETH  (PUMP — 5x in days)
Month 3: 0.0 ETH  (CRASH — rug pull)
Month 4: 0.4 ETH  (dead cat bounce)
Month 5: 0.003 ETH (death spiral)

Pattern: TEXTBOOK RUG PULL
```

### 3. Red Flags Checklist

**Critical red flags (avoid immediately):**
- ❌ **Zero marketplace listings** (not on OpenSea/Blur/any platform)
- ❌ **Zero holders on-chain** (NFTs stuck in minting contract)
- ❌ **Unverified contract** (can't verify legitimacy)
- ❌ Floor price < $10 (death territory)
- ❌ No Discord/Telegram (dead community)
- ❌ Zero market cap
- ❌ No development updates in 3+ months
- ❌ Wash trading (high sale count, tiny values)
- ❌ No utility (pure collectible)
- ❌ Team anonymous + no roadmap
- ❌ Pump & dump chart pattern
- ❌ 90%+ decline from peak
- ❌ No recovery catalysts

**Warning signs (proceed with caution):**
- ⚠️ Small community (< 5k Discord members)
- ⚠️ Low liquidity (< 10 ETH daily volume)
- ⚠️ High holder concentration (top 10 hold > 50%)
- ⚠️ Declining social engagement
- ⚠️ Delayed roadmap milestones
- ⚠️ No partnerships or integrations

**Positive signals:**
- ✅ Active Discord (10k+ members, daily activity)
- ✅ Regular development updates
- ✅ Real utility (gaming, metaverse, membership)
- ✅ Partnerships with established projects
- ✅ Doxxed team with track record
- ✅ Healthy chart (uptrend, support levels)
- ✅ Growing community
- ✅ Blue-chip status (BAYC, Azuki, Pudgy Penguins)

### 4. Risk Assessment

**Calculate probability-weighted expected value:**

```
Scenarios:
1. Best case (5-10%): 3-10x gain
2. Most likely (70-80%): -50% to +50%
3. Worst case (10-20%): -90% to -100%

Expected value = (P1 × Gain1) + (P2 × Gain2) + (P3 × Loss3)

If EV < 0: AVOID
If EV > 0 but high risk: CAUTION
If EV > 0 and low risk: CONSIDER
```

**Risk levels:**
- **EXTREME (10/10):** Death spiral, abandoned project, rug pull signs
- **HIGH (7-9/10):** Declining metrics, weak community, no utility
- **MEDIUM (4-6/10):** Mixed signals, execution risk, market dependent
- **LOW (1-3/10):** Blue-chip, strong fundamentals, active development

### 5. Comparison with Similar Projects

**Compare against:**
- Blue-chip NFTs (BAYC, Azuki, Doodles)
- Same category (PFP, gaming, metaverse)
- Similar launch date
- Similar supply size

**Metrics to compare:**
- Floor price trajectory
- Volume trends
- Community size
- Development activity
- Utility/roadmap execution

## Recommendation Framework

### BUY (Serok)
**Criteria:**
- ✅ All fundamentals strong
- ✅ Active community (10k+ Discord)
- ✅ Regular development updates
- ✅ Real utility or roadmap
- ✅ Healthy chart (uptrend, support)
- ✅ Expected value > 0
- ✅ Risk level: LOW to MEDIUM

**Example:** Blue-chip NFT during temporary dip

### HOLD
**Criteria:**
- 🟡 Mixed signals
- 🟡 Some red flags but not critical
- 🟡 Execution risk
- 🟡 Expected value ≈ 0
- 🟡 Risk level: MEDIUM

**Example:** Established project with delayed roadmap

### AVOID (Jangan Serok)
**Criteria:**
- ❌ Multiple critical red flags
- ❌ Death spiral chart pattern
- ❌ Dead community
- ❌ No development
- ❌ Expected value < 0
- ❌ Risk level: HIGH to EXTREME

**Example:** Project with $8 floor, no Discord, 95% down from peak

## Response Format

**Structure:**
1. Executive summary (BUY/HOLD/AVOID + one-line reason)
2. Current metrics (floor, volume, holders)
3. Chart analysis (pattern recognition)
4. Red flags and positive signals
5. Risk assessment (probability-weighted)
6. Comparison with similar projects
7. Final recommendation with reasoning

**Tone:**
- Direct and honest (don't sugarcoat bad projects)
- Data-driven (cite specific metrics)
- Risk-aware (acknowledge uncertainty)
- Actionable (clear buy/hold/avoid)
- **Lead with risk assessment** — users want to know "is this high risk?" upfront, not buried in analysis
- **Label risk level prominently** — use visual markers (🔴 EXTREME, 🟡 MEDIUM, 🟢 LOW) early in response

**For Indonesian users:**
- Use "serok" for "buy the dip"
- Use "jangan serok" for "don't buy"
- Keep technical terms in English (floor price, volume, etc.)
- Explain reasoning clearly
- When user says "mantep ini untuk high risk" — they appreciate direct risk labeling and want it upfront, not buried

## Pitfalls

- **Don't rely on hype** — community excitement ≠ good investment
- **Don't ignore red flags** — one critical red flag can sink a project
- **Don't assume recovery** — death spirals rarely reverse
- **Don't compare apples to oranges** — compare within same category
- **Don't forget opportunity cost** — even if project survives, better options may exist

## Verification

- Cross-reference data from multiple sources (OpenSea + Twitter + Discord)
- Check contract on Etherscan for holder distribution
- Look for wash trading (same wallets trading back and forth)
- Verify team claims (partnerships, roadmap milestones)

## Example Analysis

See `references/numismatis-nft-analysis.md` for full example of death spiral project analysis.

See `references/ardinals-dead-market.md` for agent-only NFT with zero marketplace liquidity (dead market despite active minting).

See `references/cloudflare-blocked-workflow.md` for workflow when OpenSea blocks direct access (Cloudflare protection).
