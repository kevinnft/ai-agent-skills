# Domain Registrars for Google Workspace (Indonesia Context)

When setting up Google Workspace for bulk OAuth account provisioning, you need a custom domain. This reference compares registrars accessible from Indonesia with pricing in IDR.

## Quick Comparison

| Registrar | Year 1 (.com) | Renewal | WHOIS Privacy | Total 3 Years |
|-----------|---------------|---------|---------------|---------------|
| **Hostinger** | Rp15k | Rp169k | Rp89k/year | Rp620k |
| **Domainesia** | Rp165k | Rp165k | FREE | Rp495k |
| **Porkbun** (USD) | $7.65 (~Rp122k) | $9.13 (~Rp146k) | FREE | ~Rp414k |
| **Cloudflare** (USD) | $9.15 (~Rp146k) | $9.15 (~Rp146k) | FREE | ~Rp438k |

Exchange rate: $1 = Rp16,000 (approximate, May 2026)

## Detailed Breakdown

### Hostinger (Indonesia)

**Pros:**
- Cheapest first year (Rp15k promo)
- Modern dashboard
- 24/7 support (live chat)
- Payment: e-wallet, QRIS, bank transfer

**Cons:**
- **Expensive renewal** (Rp169k/year)
- **WHOIS privacy costs extra** (Rp89k/year)
- Aggressive upselling (hosting, VPS)
- DNS propagation slow (6-12 hours)

**Total Cost (3 years with WHOIS privacy):**
- Year 1: Rp15k + Rp89k = Rp104k
- Year 2-3: (Rp169k + Rp89k) × 2 = Rp516k
- **Total: Rp620k**

**Best for**: 1-year test projects, tight initial budget

---

### Domainesia (Indonesia)

**Pros:**
- **Consistent pricing** (no surprise renewal)
- **WHOIS privacy included**
- Support in Bahasa Indonesia
- Registrar resmi PANDI
- Payment: bank transfer, e-wallet

**Cons:**
- Higher first-year cost vs Hostinger promo
- Interface dated (but functional)
- Support limited to business hours

**Total Cost (3 years):**
- Rp165k × 3 = **Rp495k**

**Best for**: Long-term projects, predictable budgeting, Indonesian support

---

### Porkbun (International, USD)

**Pros:**
- Low pricing, no markup
- **WHOIS privacy included**
- Free SSL
- No upselling
- Straightforward interface

**Cons:**
- Payment in USD (exchange rate risk)
- Support in English only
- Requires international payment method

**Total Cost (3 years):**
- Year 1: $7.65 (~Rp122k)
- Year 2-3: $9.13 × 2 (~Rp292k)
- **Total: ~Rp414k**

**Best for**: Lowest total cost, comfortable with USD/English

---

### Cloudflare Registrar (International, USD)

**Pros:**
- **At-cost pricing** (no markup, same renewal)
- **WHOIS privacy included**
- Free DDoS protection
- Instant DNS propagation (Cloudflare network)

**Cons:**
- Must use Cloudflare DNS (not a real con, it's excellent)
- Cannot buy directly — must transfer from another registrar
- 60-day wait after initial registration before transfer

**Total Cost (3 years):**
- $9.15 × 3 = **$27.45 (~Rp438k)**

**Best for**: Best long-term value, but requires initial purchase elsewhere + 60-day wait

---

## Alternative TLDs (Cheaper First Year, Expensive Renewal)

**Warning**: These have aggressive first-year discounts but expensive renewals. Only use for 1-year disposable projects.

| TLD | Year 1 | Renewal | 3-Year Total |
|-----|--------|---------|--------------|
| **.site** | Rp17k (Hostinger) | Rp645k | Rp1.3M |
| **.xyz** | $1.99 (Porkbun) | $13/year | ~Rp450k |
| **.tech** | $4.99 (Porkbun) | $49/year | ~Rp1.6M |

**Recommendation**: Stick with **.com** for Google Workspace. The renewal prices for alternative TLDs are not worth the first-year savings.

---

## Recommended Strategy

### For Long-Term Use (3+ years):

**Option A: Lowest Total Cost**
1. Buy .com at **Porkbun** ($7.65 first year)
2. Renew at Porkbun ($9.13/year)
3. **Total 3 years: ~Rp414k**

**Option B: Predictable, Local Support**
1. Buy .com at **Domainesia** (Rp165k/year)
2. Consistent pricing, Indonesian support
3. **Total 3 years: Rp495k**

**Option C: Absolute Lowest (with effort)**
1. Buy .com at **Hostinger** (Rp15k first year, skip WHOIS privacy)
2. Wait 60 days
3. Transfer to **Cloudflare** ($9.15, includes +1 year extension)
4. Renew at Cloudflare ($9.15/year)
5. **Total 2 years: Rp161k** (Rp15k + $9.15 = ~Rp161k)

### For 1-Year Test:

**Hostinger** (Rp15k) — cheapest entry, acceptable if not renewing.

---

## DNS Setup for Google Workspace

After purchasing domain, configure these DNS records:

### 1. Verification (TXT Record)
```
Type: TXT
Name: @ (or root)
Value: google-site-verification=XXXXXX (provided by Google)
TTL: 3600
```

### 2. MX Records (Email Routing)
```
Priority 1:  ASPMX.L.GOOGLE.COM
Priority 5:  ALT1.ASPMX.L.GOOGLE.COM
Priority 5:  ALT2.ASPMX.L.GOOGLE.COM
Priority 10: ALT3.ASPMX.L.GOOGLE.COM
Priority 10: ALT4.ASPMX.L.GOOGLE.COM
```

### 3. SPF Record (Anti-Spam, Recommended)
```
Type: TXT
Name: @
Value: v=spf1 include:_spf.google.com ~all
```

### 4. DKIM Record (Email Authentication, Optional)
Google provides this after setup:
```
Type: TXT
Name: google._domainkey
Value: v=DKIM1; k=rsa; p=XXXXXXX...
```

---

## Google Workspace Pricing (May 2026)

For bulk OAuth account provisioning:

| Plan | Per User/Month | 10 Users/Month | 10 Users/Year |
|------|----------------|----------------|---------------|
| **Starter** | $4.20 (annual) | $42 | $504 (~Rp8M) |
| **Starter** | $5 (monthly) | $50 | $600 (~Rp9.6M) |
| Standard | $9.80 (annual) | $98 | $1,176 (~Rp18.8M) |
| Plus | $22 (annual) | $220 | $2,640 (~Rp42M) |

**Recommendation**: **Business Starter** ($4.20/user/month with annual commitment) is sufficient for OAuth-only use cases. You don't need the storage/features of higher tiers.

### Flexible Plan Alternative

Google Workspace Flexible Plan: **$0.14/user/day** (pay only for active days)
- 10 users × 30 days = $42/month (same as monthly Starter)
- Can disable users when not needed
- Good for variable usage patterns

---

## Total Cost Example (10 OAuth Accounts, 1 Year)

### Domainesia + Google Workspace Starter:
- Domain: Rp165k
- Google Workspace: $504 (~Rp8M)
- **Total Year 1: ~Rp8.2M**

### Hostinger → Cloudflare + Google Workspace Starter:
- Domain: Rp15k (Hostinger) + $9.15 (Cloudflare transfer after 60 days) = ~Rp161k
- Google Workspace: $504 (~Rp8M)
- **Total Year 1: ~Rp8.2M**

**vs Buying Bulk Google Accounts:**
- 100 accounts = Rp20k
- Kiro ban rate: 58% (waste Rp11.6k)
- Must rebuy monthly
- **Annual cost: ~Rp240k** (but high effort, constant account churn)

**ROI**: Google Workspace is 34× more expensive but provides:
- Admin control (no bans)
- Unlimited user provisioning
- Professional email
- Stable, long-term accounts

For production use or high-value projects, Google Workspace is worth it. For experimentation or low-budget projects, bulk accounts are acceptable with the understanding that 58% will be banned.

---

## Quick Decision Tree

**Budget < Rp200k/year, experimental project:**
→ Buy bulk Google accounts (Rp20k/100 accounts)

**Budget Rp200k-500k/year, 1-year project:**
→ Hostinger .com (Rp15k) + don't renew

**Budget Rp500k+/year, long-term, need stability:**
→ Domainesia .com (Rp165k/year) + Google Workspace Starter

**Budget flexible, want lowest total cost:**
→ Porkbun .com ($7.65 first year, $9.13 renewal)

**Budget flexible, want best infrastructure:**
→ Hostinger → Cloudflare transfer + Google Workspace Starter
