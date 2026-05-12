# IDX High Dividend Stock Analysis Workflow

**Context:** Indonesian stock market (IDX) dividend analysis when real-time APIs fail.

## Problem

All public APIs for Indonesian stock data are blocked or rate-limited:
- Yahoo Finance: 429 Too Many Requests after 1-2 calls
- Google Finance: Cloudflare blocking
- IDX.co.id: Cloudflare blocking
- Stockbit API: Requires authentication
- RTI, IPOT: No public API

## Solution: User-Provided Data First

**Best approach:**
1. Ask user for screenshot from their broker app (Stockbit, IPOT, etc.)
2. Use vision tools to extract prices from screenshot
3. Analyze based on real data

**Example:**
```
User sends Stockbit screenshot showing:
- BBCA: Rp 5,850 (-2.09%)
- BBRI: Rp 2,990 (-2.61%)
- BBNI: Rp 3,720 (-2.11%)

→ Immediately recognize market crash (banks down 34-44% from normal)
→ Analyze implications (dividend yield higher, but dividend cut risk)
```

## Fallback: Curated Data from Financial Reports

If user explicitly requests analysis without providing real-time data:

1. **Clearly label as estimates:**
   - "Data estimasi dari laporan keuangan Q4 2025 / Q1 2026"
   - "⚠️ BUKAN real-time — verifikasi dengan broker"

2. **Use conservative estimates:**
   - Price ranges from recent quarterly reports
   - Dividend yield from last 3-5 years average
   - Payout ratio from latest annual report

3. **Focus on fundamentals over price:**
   - ROE, debt/equity, payout ratio trends
   - Sector analysis (banking, mining, telco)
   - Dividend sustainability (free cash flow, earnings growth)

## Analysis Framework for Dividend Stocks

### Key Metrics (Priority Order)

1. **Dividend Yield** (target ≥5%)
   ```
   yield = (annual_dividend / current_price) * 100
   ```

2. **Payout Ratio** (healthy: 30-80%)
   ```
   payout = (dividend_per_share / earnings_per_share) * 100
   
   Red flags:
   - >90%: Unsustainable (dividend trap risk)
   - >100%: Paying from debt/reserves (critical)
   ```

3. **ROE** (target ≥15%)
   ```
   roe = (net_income / shareholder_equity) * 100
   
   Benchmarks:
   - >20%: Excellent
   - 15-20%: Strong
   - 10-15%: Acceptable
   - <10%: Weak
   ```

4. **Debt/Equity** (exclude banks)
   ```
   Healthy: <1.0x
   Moderate: 1.0-1.5x
   High: >1.5x (risk)
   
   Note: Banks naturally have high D/E (5-6x is normal)
   ```

5. **Free Cash Flow**
   ```
   Positive FCF = dividend sustainable
   Negative FCF = dividend at risk
   ```

### Sector-Specific Analysis

**Banking (BBRI, BBCA, BMRI, BBNI):**
- Check NPL (Non-Performing Loan) ratio: <3% healthy, >5% red flag
- CAR (Capital Adequacy Ratio): >15% safe, <12% risk
- NIM (Net Interest Margin): 5-7% typical for Indonesia
- Defensive sector, but cyclical (affected by economic growth)

**Coal Mining (PTBA, ADRO, ITMG):**
- Highest dividend yields (7-12%)
- Cyclical: depends on coal prices (Newcastle benchmark)
- Unlock risk: check if high payout ratio (>70%)
- ESG risk: coal phase-out long-term (10-20 years)

**Telco (TLKM):**
- Defensive, stable dividends
- Lower yield (5-6%) but consistent
- BUMN backing (government support)
- Growth limited (mature market)

**Tobacco (HMSP, GGRM):**
- High yield but sunset industry
- Regulatory risk (cukai/excise tax increases)
- Demand declining long-term
- Often dividend traps (high payout ratio >80%)

### Dividend Trap Detection

**Red flags:**
1. Payout ratio >90% (unsustainable)
2. Earnings declining while dividend stays high
3. Free cash flow negative
4. Debt increasing significantly
5. Sunset industry (tobacco, coal long-term)
6. High yield due to price crash (not strong fundamentals)

**Example:**
```
HMSP (HM Sampoerna):
- Yield: 8% (attractive)
- Payout: 95% (CRITICAL)
- ROE: 30% (excellent)
- Sector: Tobacco (sunset)

Verdict: AVOID — payout unsustainable, one bad quarter = dividend cut
```

### Market Crash Context

When market crashes (e.g., BBCA down 40%):

1. **Recalculate yields:**
   ```
   Old: BBRI @ Rp 4,800 with Rp 216 dividend = 4.5% yield
   New: BBRI @ Rp 2,990 with Rp 216 dividend = 7.2% yield
   
   BUT: Dividend likely to be cut if earnings down
   ```

2. **Assess crash severity:**
   - Check IHSG (composite index) level
   - Compare sector performance (banks vs mining vs telco)
   - Look for systemic issues (banking crisis, recession)

3. **Adjust recommendations:**
   - WAIT for stabilization (IHSG sideways 3-5 days)
   - Don't catch falling knife
   - Focus on defensive sectors (less affected)
   - DCA (Dollar Cost Averaging) instead of lump sum

### Portfolio Construction

**Conservative (6-7% yield):**
- 50% Banking/Telco (defensive)
- 30% Mining Services (UNTR)
- 20% Coal (ADRO)

**Moderate (7-8% yield):**
- 35% Mining Services (UNTR)
- 30% Coal (PTBA)
- 20% Coal (ADRO)
- 15% Banking (BMRI)

**Aggressive (8-9% yield):**
- 40% Coal (PTBA)
- 30% Mining Services (UNTR)
- 20% Energy (INDY)
- 10% Oil & Gas (MEDC)

**Risk management:**
- Max 30-40% per stock
- Diversify across 3-5 stocks
- Mix defensive (50%) + cyclical (50%)
- Set stop loss at -15% from entry
- Rebalance quarterly

## Output Format (Indonesian)

When analyzing for Indonesian user:

```markdown
# ANALISA SAHAM DIVIDEN: [TICKER]

## DATA KRITIS
- Harga: Rp X,XXX
- Dividend Yield: X.X%
- Payout Ratio: XX%
- ROE: XX%
- D/E: X.XXx

## STATUS: [LAYAK BELI / WATCHLIST / HINDARI]

## STRENGTHS
✅ [Strength 1]
✅ [Strength 2]

## RISKS
⚠️ [Risk 1]
⚠️ [Risk 2]

## VERDICT
[2-3 sentences with reasoning]

Entry point: < Rp X,XXX
```

## Tools & Commands

**Python script for batch analysis:**
```python
# See ~/idx_dividend_analysis/final_analysis.py
# Analyzes 10+ stocks with scoring system
# Outputs ranking, sector breakdown, portfolio suggestions
```

**Manual data sources:**
- Quarterly reports: idx.co.id (if accessible)
- Company IR websites
- Financial news: Kontan, Bisnis Indonesia
- Broker research reports

## Key Lessons

1. **Never guess prices** — admit limitation and ask user
2. **User's broker screenshot > all APIs** — fastest path to real data
3. **Label estimates clearly** — "estimasi, bukan real-time"
4. **Focus on fundamentals** when real-time data unavailable
5. **Adjust for market context** — crash changes everything
6. **Dividend trap awareness** — high yield ≠ good investment

## Session Example

User: "Cek saham dividen bank di Indonesia"

❌ Wrong approach:
- Try 5+ APIs, all fail
- Provide outdated estimates (BBCA Rp 9,000)
- User corrects: "BBCA aja 5900 ambil data terbaru lah"

✅ Right approach:
- Try Yahoo Finance (1-2 attempts)
- If fails: "Gua gak bisa akses data real-time karena API kena rate limit. Lu bisa screenshot dari Stockbit/IPOT?"
- User sends screenshot
- Analyze: "BBCA @ Rp 5,850 = crash 44%, ini bukan koreksi biasa..."
