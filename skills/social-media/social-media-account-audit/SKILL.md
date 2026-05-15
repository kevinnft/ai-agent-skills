---
name: social-media-account-audit
description: "Audit social media accounts (TikTok, IG, etc.): scrape profiles, calculate engagement metrics, diagnose performance drops, interpret analytics screenshots."
tags: [tiktok, instagram, analytics, audit, engagement, live-streaming, social-commerce]
related_skills: [social-media-slideshow-video, xurl]
origin: unknown
source_license: see upstream
language: en
---

# Social Media Account Audit

## When to Use

- User shares analytics screenshots (LIVE stats, dashboard data, engagement metrics)
- User asks "why is my account/LIVE performing badly?"
- User shares a TikTok/Instagram profile link for review
- User wants to compare past vs current performance
- User asks for growth strategy based on data

## Workflow Overview

```
1. Scrape profile data (if link provided)
2. Extract metrics from screenshots (if provided)
3. Calculate health ratios
4. Diagnose root causes
5. Deliver actionable recommendations
```

## Step 1: Scrape TikTok Profile Data

### Fetch HTML
```bash
curl -s -L -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://www.tiktok.com/@USERNAME" -o /tmp/tiktok_profile.html
```

### Extract Basic Stats (grep approach — fast)
```bash
grep -oP '"uniqueId":"[^"]*"|"nickname":"[^"]*"|"signature":"[^"]*"|"followerCount":\d+|"followingCount":\d+|"heartCount":\d+|"videoCount":\d+|"verified":[a-z]+' /tmp/tiktok_profile.html
```

### Extract Full Profile (Python — comprehensive)
```python
import json, re
from datetime import datetime

with open('/tmp/tiktok_profile.html') as f:
    html = f.read()

match = re.search(
    r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>',
    html, re.DOTALL
)
data = json.loads(match.group(1))
scope = data['__DEFAULT_SCOPE__']
user_info = scope['webapp.user-detail']['userInfo']
user = user_info['user']
stats = user_info['stats']

# Key fields
print(f"Username: @{user['uniqueId']}")
print(f"Bio: {user['signature']}")
print(f"Created: {datetime.fromtimestamp(int(user['createTime']))}")
print(f"Category: {user.get('commerceUserInfo', {}).get('category', 'N/A')}")
print(f"Commerce User: {user.get('commerceUserInfo', {}).get('commerceUser', False)}")
print(f"TT Seller: {user.get('ttSeller', False)}")
print(f"Verified: {user['verified']}")
print(f"Followers: {stats['followerCount']:,}")
print(f"Following: {stats['followingCount']:,}")
print(f"Likes: {stats['heartCount']:,}")
print(f"Videos: {stats['videoCount']}")
```

### Additional Metadata to Extract
```bash
# Commerce info, seller status, room ID, account settings
grep -oP '"commerceUserInfo":\{[^}]*\}|"category":"[^"]*"|"ttSeller":[a-z]+|"roomId":"[^"]*"|"privateAccount":[a-z]+|"nickNameModifyTime":\d+|"openFavorite":[a-z]+' /tmp/tiktok_profile.html
```

### Get secUid (needed for API calls)
```bash
grep -oP '"secUid":"[^"]*"' /tmp/tiktok_profile.html | head -1
```

## Step 2: Calculate Health Metrics

| Metric | Formula | Healthy Range | Warning |
|--------|---------|---------------|---------|
| **Engagement Rate** | (avg_likes / followers) × 100 | 4-8% | <3% is low |
| **Likes-to-Follower Ratio** | total_likes / followers | 10-20+ | <5 = ghost followers |
| **Follower:Following Ratio** | followers / following | 50:1+ for brands | <10:1 = follow-for-follow |
| **Video Output** | videos / account_age_months | 30-90/month (1-3/day) | <10/month is too low |
| **LIVE Retention Rate** | avg_viewers / total_viewers × 100 | 5-15% | <1% = bounce problem |
| **LIVE PCU Ratio** | PCU / avg_viewers | 2-4x | >10x = spike then crash |

## Step 3: Interpret LIVE Analytics Screenshots

### Key Metrics to Look For (TikTok LIVE)
- **Rata-Rata Penonton** = Average concurrent viewers
- **PCU** = Peak Concurrent Users
- **Penonton** = Total unique viewers
- **GMV** = Gross Merchandise Value (sales)
- **CTR LIVE** = Click-through rate on products
- **Barang terjual** = Items sold

### Trend Graph Interpretation
- **Menonton (red)** = Currently watching — should stay stable or rise
- **Masuk (blue)** = Entering — inflow rate
- **Keluar (green)** = Leaving — outflow rate
- **Healthy pattern**: Masuk > Keluar, Menonton rises over time
- **Unhealthy pattern**: Keluar > Masuk early, Menonton drops and flatlines

### Traffic Sources (Sumber Penonton)
- **Feed Untuk Anda (FYP)** — Algorithmic reach (usually 60-90%)
- **Tombol LIVE** — Followers clicking LIVE notification
- **Tab Shop** — Discovery via TikTok Shop tab
- **Lainnya** — Other sources (search, profile visits, shares)

### Buyer Profile (Profil Pembeli)
- **Jenis kelamin** = Gender split
- **Usia** = Age demographics
- **Pengikut** = Follower vs non-follower buyers

## Step 4: Common Diagnoses

### Pattern: High Total Viewers, Low Average (Bounce Problem)
- **Cause**: Hook is weak — viewers enter and leave within seconds
- **Evidence**: Keluar line tracks Masuk line closely; Menonton stays flat/low
- **Fix**: Stronger first-3-second hook, engaging title, immediate interaction

### Pattern: FYP Traffic High % but Low Absolute Numbers
- **Cause**: Algorithm has "cooled" the account — still sending FYP traffic but to fewer people
- **Evidence**: FYP % similar to before but total viewers way down
- **Fix**: Rebuild algorithm trust via consistent posting + high-retention content

### Pattern: Performance Cliff (Was Good, Now Bad)
- **Causes** (check in order):
  1. Posting frequency dropped → algorithm deprioritized
  2. Content/niche changed → audience mismatch
  3. Community guidelines violation/warning → shadow restriction
  4. Ghost followers accumulated → engagement rate tanked
  5. Increased competition in niche

### Pattern: Commerce User but Not TT Seller
- **Impact**: Doesn't get seller-tier algorithm priority for LIVE shopping
- **Fix**: Register as official TikTok Shop seller if eligible

## Step 5: Recommendation Framework

### Bio Optimization Template
```
[Emoji] [What you sell — specific]
[Emoji] LIVE [Schedule — day + time]
[Emoji] [Value prop / price hook]
```
Example:
```
👗 Fashion Wanita Murah & Berkualitas
🔴 LIVE Setiap Hari Jam 19:00-21:00
💰 Harga Mulai 25rb!
```

### Recovery Timeline
| Phase | Duration | Focus |
|-------|----------|-------|
| Foundation | Week 1-2 | Fix bio, clean following list, post 2-3 videos/day |
| Warm-up | Week 3-4 | Daily LIVE at consistent time, video teasers before LIVE |
| Scale | Month 2+ | TikTok Promote, collaborations, flash sales during LIVE |

### LIVE Retention Tactics
- Giveaway/games every 15-20 minutes
- Greet every viewer by name
- "Surprise coming in 5 minutes" hooks
- Flash sales with countdown timers
- Pin products and mention them regularly

## Pitfalls

1. **TikTok anti-bot detection**: curl fetches may return empty `itemList` (videos). The profile metadata still comes through in `__UNIVERSAL_DATA_FOR_REHYDRATION__`. Video-level data requires a real browser or authenticated API.
2. **Bot classification**: TikTok sets `"botType": "others"` and `"needFix": true` on bot-detected requests. Profile stats are still accurate; video lists are withheld.
3. **API endpoints blocked**: Direct API calls like `/api/post/item_list/` return empty responses without proper cookies/tokens. Don't waste time on these.
4. **Indonesian language**: TikTok Shop analytics in Indonesia use Bahasa. Key terms: Penonton=Viewers, Keterlibatan=Engagement, Jangkauan=Reach, Konversi=Conversion, Barang terjual=Items sold, Pesanan=Orders.
5. **Timestamp conversion**: `createTime` and `nickNameModifyTime` are Unix timestamps. Use `datetime.fromtimestamp()`.
6. **Screenshot analysis**: When user sends analytics screenshots, the image description provides structured data. Cross-reference multiple screenshots to build the full picture.

## Output Format

Present audit results as:
1. **Data table** — Profile stats with health indicators (✅/⚠️/🔴)
2. **Ratio analysis** — Calculated metrics vs benchmarks
3. **Root cause chain** — Visual cause→effect flow showing why performance dropped
4. **Prioritized action plan** — Phased recommendations (Foundation → Warm-up → Scale)

## References
- `references/tiktok-profile-fields.md` — All extractable fields from TikTok profile HTML
- `references/tiktok-analytics-terms-id.md` — Indonesian↔English analytics terminology
