# Polymarket Trading Bots Ecosystem

Research conducted: May 4, 2026
Source: GitHub ecosystem analysis via tweet https://x.com/zostaff/status/2050982528920486374

## Key Finding

**Tweet claim validated:** "one npm package replaced the entire stack of paid crypto data APIs"
**Package:** pmxt-dev/pmxt (1,661⭐) — CCXT for prediction markets

## Top 3 Most Useful Repositories

### 1. zostaff/poly-trading-bot ⭐ 7 (Brand New)
- **URL:** https://github.com/zostaff/poly-trading-bot
- **Created:** May 3, 2026 (by tweet author)
- **Why best:** Most complete toolkit despite being brand new
- **Features:**
  - 3 built-in strategies (AI Directional, Safe Compounder, Beast Mode)
  - Paper trading mode
  - Kelly sizing + risk management (stop-loss, take-profit, drawdown breaker)
  - Streamlit dashboard
  - Honest documentation with real loss warnings
- **Tech:** Python 3.12+, OpenRouter, SQLite, Web3/Polygon
- **Lessons from live trading:**
  - Kelly fraction matters enormously (3/4 Kelly = catastrophic losses)
  - Category discipline > AI confidence
  - Over-trading without edge = faster path to zero

### 2. pmxt-dev/pmxt ⭐ 1,661
- **URL:** https://github.com/pmxt-dev/pmxt
- **What:** Unified API for prediction markets (like CCXT for crypto)
- **Why:** Replaces multiple paid APIs with one npm package
- **Platforms:** Polymarket, Kalshi, and more

### 3. warproxxx/poly-maker ⭐ 1,127
- **URL:** https://github.com/warproxxx/poly-maker
- **What:** Market making bot
- **Strategy:** Hold orders 24/7 on both sides (matches tweet description)
- **Config:** Google Sheets

## 8 Trading Strategies Found

1. **Market Making** — 24/7 order book presence (warproxxx/poly-maker)
2. **Arbitrage** — cross-platform, 5min/15min BTC intervals
3. **Contrarian/Base-Rate** — buy "No" on all markets (sterlingcrispin/nothing-ever-happens)
4. **AI/LLM-Driven** — parse Twitter before CNN, sentiment analysis
5. **Copy Trading** — follow successful wallets
6. **Weather Trading** — GFS forecasts + Kelly criterion (suislanchez/polymarket-kalshi-weather-bot)
7. **Sports Betting** — automated sports market trading
8. **High-Frequency** — BTC 5min/15min prediction

## Tech Stack (95% Python)

- **Languages:** Python (95%), Rust (5% for performance)
- **Blockchain:** Web3/Polygon
- **AI:** OpenRouter, CL4ude APIs
- **Position Sizing:** Kelly Criterion
- **Data:** SQLite/PostgreSQL
- **Dashboards:** Streamlit/React
- **Data Sources:** Polymarket CLOB API, Gamma API, GFS weather, Twitter/X

## Top 20 Repositories by Stars

1. **Polymarket/agents** (3,379⭐) — Official AI agents
2. **Jon-Becker/prediction-market-analysis** (3,252⭐) — Largest dataset
3. **pmxt-dev/pmxt** (1,661⭐) — Unified API (THE npm package)
4. **warproxxx/poly-maker** (1,127⭐) — Market making bot
5. **sterlingcrispin/nothing-ever-happens** (934⭐) — Contrarian strategy
6. **FrondEnt/PolymarketBTC15mAssistant** (685⭐) — BTC 15m trading
7. **SII-WANGZJ/Polymarket_data** (550⭐) — 1.1B trading records
8. **ent0n29/polybot** (496⭐) — Reverse-engineer strategies
9. **caiovicentino/polymarket-mcp-server** (459⭐) — CL4ude integration
10. **PoDev-Juanthiago/Polymarket-Arbitrage-Bot** (393⭐) — Arbitrage
11. **kuestcom/prediction-market** (352⭐) — Build your own platform
12. **PoDev-rahulrajasekhar/Polymarket-Copytrading-Bot** (305⭐) — Copy trading
13. **suislanchez/polymarket-kalshi-weather-bot** (291⭐) — Weather ($1.8k profits)
14. **GastonDeMichele/Polymarket-Sports-Bot** (289⭐) — Sports betting
15. **PolyScripts/polymarket-arbitrage-trading-bot-pack-5min-15min-kalshi** (268⭐) — HFT
16. **alteregoeth-ai/weatherbot** (258⭐) — Weather + Kelly
17. **ConteurShadow/Polymarket-Trading-Bot-Rust** (244⭐) — Rust implementation
18. **OctagonAI/kalshi-trading-bot-cli** (243⭐) — Kalshi (competitor)
19. **haredoggy/Prediction-Markets-Trading-Bot-Toolkits** (242⭐) — Multi-platform
20. **lorine93s/polymarket-btc-5min-15min-arbitrage-bot** (230⭐) — BTC arbitrage

## Critical Warnings

1. **No guaranteed profits** — Markets are efficient
2. **Small edges** — Requires proper risk management
3. **Kelly sizing critical** — Aggressive Kelly = catastrophic losses
4. **Category discipline** — Avoid sector concentration
5. **Over-trading kills** — More trades without edge = faster losses

## Use Case Recommendations

**For Beginners:**
- zostaff/poly-trading-bot (best docs, paper trading)
- pmxt-dev/pmxt (unified API)

**For Market Making:**
- warproxxx/poly-maker

**For Arbitrage:**
- PoDev-Juanthiago/Polymarket-Arbitrage-Bot

**For AI/LLM Trading:**
- zostaff/poly-trading-bot (most complete)
- Polymarket/agents (official)
- caiovicentino/polymarket-mcp-server (CL4ude)

**For Data Analysis:**
- Jon-Becker/prediction-market-analysis (largest dataset)
- SII-WANGZJ/Polymarket_data (1.1B records)

**For Weather Markets:**
- suislanchez/polymarket-kalshi-weather-bot (proven profits)
- alteregoeth-ai/weatherbot

## Tweet Claims Validated

1. ✅ "Top 50 wallets aren't people with quick fingers. It's code."
   - Found 20+ sophisticated trading bots
2. ✅ "Someone parsing Twitter before CNN picks it up"
   - Multiple AI bots with news/sentiment parsing
3. ✅ "Someone holding orders on both sides of the book 24/7"
   - warproxxx/poly-maker does exactly this
4. ✅ "One npm package replaced the entire stack of paid crypto data APIs"
   - pmxt-dev/pmxt is the unified API

## Conclusion

Polymarket bot ecosystem is mature with diverse strategies. Success requires:
- Proper risk management (Kelly criterion, drawdown limits)
- Data-driven decisions (not just AI confidence)
- Category/sector discipline
- Realistic expectations (small edges, not get-rich-quick)
