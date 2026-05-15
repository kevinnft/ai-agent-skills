---
name: api-monitoring-bots
description: Build monitoring bots that poll APIs and send notifications on state changes (new listings, price alerts, status updates)
tags: [monitoring, cron, notifications, polling, alerts]
related_skills: [web-scraping, hermes-agent]
triggers:
  - monitor API for changes
  - notify when new listing
  - alert on price change
  - track API state
  - polling bot
  - watchdog script
origin: unknown
source_license: see upstream
language: en
---

# API Monitoring Bots

Build lightweight monitoring bots that poll REST APIs and send notifications when state changes (new items, price alerts, status updates).

## When to Use

- User wants notifications for new listings/posts/items
- Need to track price changes or threshold alerts
- Monitor API for specific conditions
- Watchdog for service status changes

## Architecture Pattern

**Stateful polling bot:**
1. Fetch current state from API
2. Compare with last known state (stored in file)
3. Detect changes (new IDs, price deltas, status transitions)
4. Format and send notifications
5. Update state file

**Key principle:** Silent when no changes (watchdog pattern, no spam).

## Implementation

### 1. Core Script Structure

```python
#!/usr/bin/env python3
import requests
import json
from pathlib import Path
from datetime import datetime

API_URL = "https://api.example.com/items"
STATE_FILE = Path.home() / ".hermes" / "monitor_state.json"

def load_state():
    """Load last seen state"""
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen_ids": [], "last_check": None}

def save_state(state):
    """Save current state"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def fetch_items():
    """Fetch current items from API"""
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return None

def check_new_items():
    """Check for new items and return notifications"""
    state = load_state()
    items = fetch_items()
    
    if not items:
        return []
    
    seen_ids = set(state["seen_ids"])
    new_items = []
    
    for item in items:
        if item["id"] not in seen_ids:
            new_items.append(item)
            seen_ids.add(item["id"])
    
    # Update state (keep last 1000 IDs to prevent bloat)
    state["seen_ids"] = list(seen_ids)[-1000:]
    state["last_check"] = datetime.now().isoformat()
    save_state(state)
    
    return new_items

# Initialize state on first run (don't notify)
state = load_state()
if not state["seen_ids"]:
    items = fetch_items()
    if items:
        state["seen_ids"] = [item["id"] for item in items]
        state["last_check"] = datetime.now().isoformat()
        save_state(state)
        print(f"Initialized with {len(state['seen_ids'])} existing items")

# Check for new items
new_items = check_new_items()

if new_items:
    for item in new_items:
        print(format_notification(item))
# Silent when no new items (watchdog pattern)
```

### 2. Hermes Cron Integration

**Create cron job:**
```bash
hermes cron create \
  --name "api-monitor" \
  --schedule "every 1m" \
  --script "monitor.py" \
  --no-agent \
  --deliver "telegram:Username"
```

**Key flags:**
- `--no-agent`: Pure script execution, no LLM cost
- `--deliver "telegram:Username"`: Send to specific Telegram user/group (use `send_message list` to see targets)
- `--schedule "every 1m"`: Run every minute (adjust as needed)

**⚠️ CRITICAL:** `--deliver origin` does NOT work for cron jobs — it doesn't know the chat ID. Always use explicit target like `telegram:Username` or `telegram:GroupName`.

**Delivery target patterns:**
- `telegram:Username` — DM to specific user (use `send_message list` to see available names)
- `telegram:GroupName` — Group chat (must be in available targets list)
- `telegram:-1001234567890` — Chat ID (numeric, for channels/groups not in target list)
- ❌ `telegram:https://t.me/channelname` — **DOES NOT WORK** (causes `invalid literal for int()` error)

**Getting chat ID for channels:**
1. Forward a message from the channel to @userinfobot
2. Bot replies with chat ID (format: `-100xxxxxxxxxx`)
3. Use that numeric ID: `--deliver "telegram:-1003963927119"`

**Delivery target patterns:**
- `telegram:Username` — DM to specific user (use `send_message list` to see available names)
- `telegram:GroupName` — Group chat (must be in available targets list)
- `telegram:-1001234567890` — Chat ID (numeric, for channels/groups not in target list)
- ❌ `telegram:https://t.me/channelname` — **DOES NOT WORK** (causes `invalid literal for int()` error)

**Getting chat ID for channels:**
1. Forward a message from the channel to @userinfobot
2. Bot replies with chat ID (format: `-100xxxxxxxxxx`)
3. Use that numeric ID: `--deliver "telegram:-1003963927119"`

**Management:**
```bash
# List jobs
hermes cron list

# Pause monitoring
hermes cron pause <job_id>

# Resume monitoring
hermes cron resume <job_id>

# Check logs
cat ~/.hermes/cron/logs/<job_id>.log
```

### 3. Notification Formatting

**Markdown for Telegram:**
```python
def format_notification(item):
    # Detect anomalies
    alert = ""
    if item["price"] < threshold:
        alert = "🚨 ALERT! "
    
    return f"""
{alert}**New Item Detected**

💰 **Price:** {item['price']}
📊 **Quantity:** {item['quantity']}
🆔 **ID:** `{item['id'][:8]}...`
⏰ **Created:** {item['created_at']}

🔗 https://example.com/item/{item['id']}
""".strip()
```

**Alert levels:**
- 🚨 Critical (price anomaly, urgent action)
- ⚠️ Warning (notable but not urgent)
- ℹ️ Info (normal notification)
- (no emoji) Standard update

### 4. State Management

**State file structure:**
```json
{
  "seen_ids": ["id1", "id2", "..."],
  "last_check": "2026-05-10T13:00:00",
  "last_price": 0.5,
  "alert_count": 3
}
```

**Best practices:**
- Keep last 1000 IDs max (prevent unbounded growth)
- Store timestamp for debugging
- Include metadata for threshold tracking
- Use `.hermes/` directory for state files

**State file location:**
```python
STATE_FILE = Path.home() / ".hermes" / f"{bot_name}_state.json"
```

## Patterns

### Pattern 1: New Item Detection (rpow2swap.com case study)

**Use case:** Notify on every new token listing.

**API:** `https://rpow2swap.com/api/listings`

**Response:**
```json
[
  {
    "id": "uuid",
    "type": "sell",
    "amount": 10000,
    "sol_price": 10,
    "status": "active",
    "created_at": "2026-05-10 02:43:08",
    "solana_wallet_address": "..."
  }
]
```

**Detection logic:**
```python
def check_new_listings():
    state = load_state()
    listings = fetch_listings()
    
    seen_ids = set(state["seen_ids"])
    new_listings = []
    
    for listing in listings:
        if listing["status"] == "active" and listing["id"] not in seen_ids:
            new_listings.append(listing)
            seen_ids.add(listing["id"])
    
    state["seen_ids"] = list(seen_ids)[-1000:]
    save_state(state)
    
    return new_listings
```

**Notification:**
```python
def format_listing(listing):
    price_per_token = listing["sol_price"] / listing["amount"]
    
    alert = ""
    if price_per_token < 0.0001:
        alert = "🚨 SANGAT MURAH! "
    elif price_per_token < 0.0005:
        alert = "⚠️ Harga Menarik! "
    
    return f"""
{alert}**Token Listing Baru**

💰 Amount: {listing['amount']:,} RPOW2
📊 Total: {listing['sol_price']:.4f} SOL
💵 Price/Token: {price_per_token:.6f} SOL
🆔 ID: `{listing['id'][:8]}...`
👤 Wallet: `{listing['solana_wallet_address'][:8]}...`
⏰ {listing['created_at']}

🔗 https://rpow2swap.com/
"""
```

**Cron setup:**
```bash
hermes cron create \
  --name "rpow2swap-monitor" \
  --schedule "every 1m" \
  --script "rpow2_monitor.py" \
  --no-agent \
  --deliver "telegram:Aboy"  # Use explicit target, NOT "origin"
```

**Files:**
- Script: `~/.hermes/scripts/rpow2_monitor.py`
- State: `~/.hermes/rpow2_monitor_state.json`

See `references/rpow2swap-monitor.md` for full implementation.

### Pattern 2: Price Threshold Alert

**Use case:** Alert when price drops below threshold.

```python
def check_price_alert():
    state = load_state()
    data = fetch_price()
    
    if not data:
        return None
    
    current_price = data["price"]
    last_price = state.get("last_price", current_price)
    
    # Alert on 10% drop
    if current_price < last_price * 0.9:
        alert = f"🚨 Price dropped {((last_price - current_price) / last_price * 100):.1f}%"
        state["last_price"] = current_price
        save_state(state)
        return alert
    
    # Update price silently
    state["last_price"] = current_price
    save_state(state)
    return None
```

### Pattern 3: Status Change Detection

**Use case:** Monitor service status, alert on downtime.

```python
def check_status():
    state = load_state()
    
    try:
        r = requests.get(API_URL, timeout=5)
        current_status = "up" if r.status_code == 200 else "down"
    except:
        current_status = "down"
    
    last_status = state.get("last_status", "up")
    
    if current_status != last_status:
        state["last_status"] = current_status
        state["status_changed_at"] = datetime.now().isoformat()
        save_state(state)
        
        if current_status == "down":
            return "🚨 Service is DOWN!"
        else:
            return "✅ Service is back UP"
    
    return None  # Silent when no change
```

## Pitfalls

- **First run spam:** Initialize state without notifying on first run
- **State file bloat:** Limit stored IDs to last 1000
- **API rate limits:** Don't poll too frequently (1-5 min intervals recommended)
- **Timeout handling:** Always use timeouts on API calls (10s recommended)
- **Silent failures:** Log errors but don't spam user with connection failures
- **Duplicate notifications:** Ensure ID-based deduplication, not timestamp-based
- **State file corruption:** Use `try/except` when loading state, fallback to empty state
- **Telegram delivery target format:** NEVER use `telegram:https://t.me/...` — causes `invalid literal for int()` error. Use `telegram:Username`, `telegram:GroupName`, or numeric chat ID `telegram:-1001234567890`. Get chat ID by forwarding message to @userinfobot

## Verification

**Test script manually:**
```bash
python3 ~/.hermes/scripts/monitor.py
```

**Simulate new items (reset state):**
```bash
rm ~/.hermes/monitor_state.json
python3 ~/.hermes/scripts/monitor.py
```

**Check cron job status:**
```bash
hermes cron list
cat ~/.hermes/cron/logs/<job_id>.log
```

**Verify state file:**
```bash
cat ~/.hermes/monitor_state.json | jq '.'
```

## Real-Time Monitoring (<1 Minute Intervals)

**Problem:** Hermes cron minimum interval is 1 minute. For near-instant notifications (1-10 second checks), you need a different approach.

### ⚠️ CRITICAL: Hermes send_message Doesn't Work from Background Processes

**DO NOT** try to call Hermes `send_message` tool or CLI from a background Python script — it will fail silently or with subprocess errors. The Hermes messaging system requires the agent context that only exists during interactive sessions or cron jobs.

**Failed approaches:**
```python
# ❌ DOES NOT WORK
subprocess.run(["hermes", "send", "-t", chat_id, "-m", message])
subprocess.run(["hermes", "msg", "send", "-c", chat_id, "-f", file])

# ❌ DOES NOT WORK
# File-based queue that Hermes "picks up" — no such mechanism exists
```

### ✅ Solution: Standalone Bot with Telegram Bot API

For sub-minute monitoring, use a **standalone Python script** that calls Telegram Bot API directly (not via Hermes).

**Architecture:**
```
[Python Script] --poll every 3s--> [API]
       |
       +--detect change--> [Telegram Bot API] --> [Channel/Group]
```

**Full implementation:**

```python
#!/usr/bin/env python3
"""
Real-time API Monitor - Standalone
Polls API every 1-5 seconds, sends to Telegram directly
"""
import requests
import json
import time
from datetime import datetime
from pathlib import Path

# Configuration
TELEGRAM_BOT_TOKEN = "123456789:ABCdefGHIjklMNOpqrsTUVwxyz"  # From @BotFather
TELEGRAM_CHAT_ID = "-1001234567890"  # Channel/group chat ID
CHECK_INTERVAL = 3  # seconds
API_URL = "https://api.example.com/items"
STATE_FILE = Path.home() / ".monitor_state.json"

def send_telegram(message):
    """Send message via Telegram Bot API"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False

def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen_ids": [], "last_check": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def fetch_items():
    try:
        r = requests.get(API_URL, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return None

def check_new_items():
    state = load_state()
    items = fetch_items()
    
    if not items:
        return []
    
    seen_ids = set(state["seen_ids"])
    new_items = []
    
    for item in items:
        if item["id"] not in seen_ids:
            new_items.append(item)
            seen_ids.add(item["id"])
    
    state["seen_ids"] = list(seen_ids)[-1000:]
    state["last_check"] = datetime.now().isoformat()
    save_state(state)
    
    return new_items

# Initialize state (don't notify on first run)
state = load_state()
if not state["seen_ids"]:
    items = fetch_items()
    if items:
        state["seen_ids"] = [item["id"] for item in items]
        save_state(state)
        print(f"Initialized with {len(state['seen_ids'])} items")

print(f"Monitoring {API_URL} every {CHECK_INTERVAL}s...")

# Main loop
check_count = 0
while True:
    try:
        new_items = check_new_items()
        check_count += 1
        
        if new_items:
            print(f"\n🔥 {len(new_items)} new item(s)!")
            for item in new_items:
                msg = format_notification(item)
                if send_telegram(msg):
                    print("✅ Sent")
                else:
                    print("❌ Failed")
        else:
            now = datetime.now().strftime("%H:%M:%S")
            print(f"[{now}] Check #{check_count} - No new items", end="\r")
        
        time.sleep(CHECK_INTERVAL)
        
    except KeyboardInterrupt:
        print("\n\nStopped")
        break
    except Exception as e:
        print(f"\nError: {e}")
        time.sleep(CHECK_INTERVAL)
```

### Setup Steps

**1. Create Telegram Bot**
```
1. Open Telegram, search @BotFather
2. Send: /newbot
3. Follow instructions (name, username)
4. Copy token: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

**2. Add Bot to Channel/Group**
```
1. Open target channel/group
2. Add bot as administrator
3. Grant "Post Messages" permission
```

**3. Get Chat ID**
```
1. Forward message from channel to @userinfobot
2. Bot replies with chat ID: -1001234567890
3. Use this numeric ID in script
```

**4. Configure Script**
```python
TELEGRAM_BOT_TOKEN = "paste_token_here"
TELEGRAM_CHAT_ID = "-1001234567890"
CHECK_INTERVAL = 3  # 1-5 seconds recommended
```

### Deployment Options

**Option A: tmux (Recommended for development)**
```bash
# Start session
tmux new -s monitor

# Run bot
python3 monitor_realtime.py

# Detach: Ctrl+B, then D
# Reattach: tmux attach -t monitor
# Kill: tmux kill-session -t monitor
```

**Option B: systemd (Recommended for production)**
```bash
# Create service file
sudo nano /etc/systemd/system/api-monitor.service
```

```ini
[Unit]
Description=API Real-time Monitor
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu
ExecStart=/usr/bin/python3 /home/ubuntu/.hermes/scripts/monitor_realtime.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable api-monitor
sudo systemctl start api-monitor

# Check status
sudo systemctl status api-monitor

# View logs
sudo journalctl -u api-monitor -f

# Stop
sudo systemctl stop api-monitor
```

**Option C: nohup (Simple but less robust)**
```bash
# Start
nohup python3 monitor_realtime.py > ~/monitor.log 2>&1 &

# Check
ps aux | grep monitor_realtime
tail -f ~/monitor.log

# Stop
pkill -f monitor_realtime
```

### When to Use Standalone vs Cron

| Factor | Cron (1 min) | Standalone (1-10s) |
|--------|--------------|-------------------|
| **Latency** | 0-60 seconds | 1-10 seconds |
| **Setup** | Easy (one command) | Medium (bot token, deployment) |
| **Reliability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Resource** | Ephemeral (10-50MB during run) | Persistent (20-50MB always) |
| **API load** | 1 req/min | 20-60 req/min |
| **Restart** | Auto (cron) | Manual (tmux) or auto (systemd) |

**Decision framework:**
- ✅ **Use cron** for: Low-priority monitoring, APIs with rate limits, "check every few minutes" use cases
- ✅ **Use standalone** for: Trading bots, auction sniping, limited inventory alerts, user explicitly says "instant" or "real-time"

**Best practice:** Start with cron (1 min). Only escalate to standalone if user explicitly needs <1 min latency AND is willing to do the setup.

### Resource Usage

**Cron (1 min interval):**
- RAM: 10-50MB during execution (ephemeral)
- CPU: Minimal (1-2 seconds per minute)
- Network: 1 request/min
- Disk: 1-10KB state file

**Standalone (3 sec interval):**
- RAM: 20-50MB (persistent)
- CPU: Minimal (mostly sleeping)
- Network: 20 requests/min
- Disk: 1-10KB state file

### Troubleshooting

**Bot token invalid:**
```bash
# Test token
curl "https://api.telegram.org/bot<TOKEN>/getMe"
# Should return bot info
```

**Bot can't send to channel:**
- Ensure bot is admin in channel
- Check "Post Messages" permission enabled
- Verify chat ID is correct (numeric, starts with `-100`)

**Rate limit errors (429):**
- Increase `CHECK_INTERVAL` (3s → 5s)
- Add exponential backoff on API errors
- Check API provider's rate limit policy

**Process dies after SSH disconnect:**
- Use tmux/screen (detachable sessions)
- Or use systemd (runs as service)
- Don't use `&` alone (dies with terminal)

## Cost Optimization

**No LLM cost:**
- Use `--no-agent` flag (pure script execution)
- No AI processing, just API polling + formatting

**Resource usage:**
- Disk: ~1-10KB state file
- RAM: ~10-50MB Python process (ephemeral for cron, persistent for background)
- Network: 1 API call per interval

**Recommended intervals:**
- Real-time (background process): 1-10 seconds (only if user needs it)
- High-frequency (cron): 1-2 minutes
- Medium-frequency (cron): 5-10 minutes
- Low-frequency (cron): 15-30 minutes

## Troubleshooting

**No notifications received:**
1. Check cron job status: `hermes cron list`
2. Check `last_delivery_error` field — if it says `invalid literal for int()`, you used wrong delivery target format
3. Fix delivery target: `hermes cron update <job_id> --deliver "telegram:Username"` or use numeric chat ID
4. Check logs: `cat ~/.hermes/cron/logs/<job_id>.log`
5. Test manually: `python3 ~/.hermes/scripts/monitor.py`
6. Verify state file exists: `cat ~/.hermes/monitor_state.json`

**Too many notifications:**
1. Increase check interval: `hermes cron update <job_id> --schedule "every 5m"`
2. Add filtering logic (only alert on significant changes)
3. Implement cooldown period in script

**API timeout errors:**
1. Increase timeout: `requests.get(url, timeout=30)`
2. Add retry logic with exponential backoff
3. Check API status (may be rate-limited)

**State file corruption:**
```python
def load_state():
    try:
        if STATE_FILE.exists():
            with open(STATE_FILE) as f:
                return json.load(f)
    except json.JSONDecodeError:
        print("State file corrupted, resetting...")
    return {"seen_ids": [], "last_check": None}
```

## References

- Hermes cron documentation: `hermes cron --help`
- **rpow2swap.com case study:**
  - Cron monitor (1 min): `references/rpow2swap-monitor.md` (Hermes cron implementation)
  - Real-time bot (3s): `references/rpow2swap-realtime-bot.md` (standalone bot with Telegram Bot API, full setup guide)
  - Security audit: `references/rpow2swap-security-audit.md` (vulnerabilities found, responsible disclosure)
