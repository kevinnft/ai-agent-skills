# Race Condition Bug Patterns in Order Matching Systems

Common bug patterns when orders "reappear" after being filled, based on rpow2swap.com analysis (May 2026).

## Symptom

User reports:
- Order visible in listing
- Someone buys the order
- Same order appears again in listing

## Root Cause Analysis Framework

### 1. Database Race Condition (Most Common)

**Pattern:**
```
T0: Order A in DB (status: OPEN)
T1: User B starts purchase transaction
T2: User C fetches listings → gets Order A (still OPEN)
T3: User B commits → Order A status = FILLED
T4: User C sees Order A in UI (stale data)
```

**Verification:**
```sql
-- Check if order is actually FILLED in database
SELECT id, status, filled_at, remaining_amount, version
FROM orders 
WHERE id = '<order_id>';
```

**If status = FILLED but still visible → frontend/cache bug**  
**If status = OPEN → database transaction bug**

**Fix:**
```sql
-- Add optimistic locking
UPDATE orders 
SET status = 'FILLED', version = version + 1
WHERE id = ? AND status = 'OPEN' AND version = ?;

-- Check affected rows
-- If 0 rows affected → order already filled (race prevented)
```

**Alternative: Use database-level locks**
```sql
-- PostgreSQL
SELECT * FROM orders WHERE id = ? FOR UPDATE;
UPDATE orders SET status = 'FILLED' WHERE id = ?;

-- MySQL
SELECT * FROM orders WHERE id = ? FOR UPDATE;
UPDATE orders SET status = 'FILLED' WHERE id = ?;
```

### 2. Cache Invalidation Failure

**Pattern:**
```
T0: Redis/CDN caches GET /api/listings (TTL: 60s)
T1: Order filled at T=30s
T2: Cache still serves stale data for 30s
T3: User sees filled order in listing
```

**Verification:**
```bash
# Check if API returns filled order
curl -s "https://example.com/api/listings" | jq '.[] | select(.id == "ORDER_ID")'

# If order present in API response → backend bug
# If order absent → frontend cache bug
```

**Fix:**
```python
# Invalidate cache on order fill
def fill_order(order_id):
    # Fill order in database
    db.execute("UPDATE orders SET status='FILLED' WHERE id=?", order_id)
    
    # Invalidate cache
    cache.delete('listings')
    cache.delete(f'order:{order_id}')
    
    # Broadcast to websocket clients
    ws.broadcast({'type': 'orderFilled', 'orderId': order_id})
```

**Alternative: Reduce TTL**
```python
# For order listings, use short TTL (5-10 seconds max)
cache.set('listings', data, ttl=5)
```

### 3. Frontend State Management Bug

**Pattern:**
```javascript
// Bug: Websocket event received but state not updated
const [orders, setOrders] = useState([]);

socket.on('orderFilled', (orderId) => {
  console.log('Order filled:', orderId);
  // BUG: No state update → order still visible
});
```

**Verification:**
```javascript
// In browser console
const ws = new WebSocket('wss://example.com/ws');
ws.onmessage = (e) => console.log('WS:', e.data);

// Buy an order → check if websocket message received
// If no message → websocket not implemented
// If message received but UI not updated → handler bug
```

**Fix:**
```javascript
socket.on('orderFilled', (orderId) => {
  setOrders(prev => prev.filter(o => o.id !== orderId));
});

// Or refetch listings
socket.on('orderFilled', () => {
  fetchListings();
});
```

### 4. Partial Fill Logic Error

**Pattern:**
```
Order: Sell 100 tokens
Fill 1: Buy 30 tokens → remaining = 70 (status: OPEN)
Fill 2: Buy 70 tokens → remaining = 0 (status: FILLED)

Bug: Frontend shows order with original amount (100)
```

**Verification:**
```sql
SELECT id, amount, filled_amount, remaining_amount, status
FROM orders
WHERE id = '<order_id>';
```

**Fix:**
```javascript
// Update remaining amount on partial fill
socket.on('partialFill', ({orderId, filledAmount, remainingAmount}) => {
  setOrders(prev => prev.map(o => 
    o.id === orderId 
      ? {...o, filledAmount, remainingAmount}
      : o
  ).filter(o => o.remainingAmount > 0));
});
```

### 5. Database Replication Lag

**Pattern:**
```
Master DB: Order filled → status = FILLED
Replica DB: Lag 1-2 seconds → status = OPEN
Frontend: Queries replica → gets stale data
```

**Verification:**
```sql
-- Check replication lag
-- PostgreSQL
SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;

-- MySQL
SHOW SLAVE STATUS\G
-- Look at: Seconds_Behind_Master
```

**Fix:**
```python
# Read from master for critical queries
def get_order_status(order_id):
    # Force read from master
    return db.execute(
        "SELECT status FROM orders WHERE id = ?",
        order_id,
        read_preference='primary'  # MongoDB
        # or use master connection pool for SQL
    )
```

**Alternative: Use read concern**
```python
# MongoDB
db.orders.find({'_id': order_id}, read_concern={'level': 'majority'})

# PostgreSQL
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

## Security Implications

**Critical:** If exploitable, this is a **double-spend vulnerability**:

```
1. User A posts: Sell 100 tokens @ $1
2. User B starts buy (holds transaction)
3. User C starts buy (holds transaction)
4. Both commit → User A sells 200 tokens but only has 100
```

**Mitigation:**
```sql
-- Add database constraint
ALTER TABLE balances ADD CONSTRAINT balance_non_negative 
CHECK (amount >= 0);

-- Use atomic decrement
UPDATE balances 
SET amount = amount - ?
WHERE user_id = ? AND amount >= ?;

-- Check affected rows
-- If 0 rows → insufficient balance
```

**Transaction isolation:**
```sql
-- Use SERIALIZABLE for critical operations
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

BEGIN;
  SELECT amount FROM balances WHERE user_id = ? FOR UPDATE;
  -- Check balance
  UPDATE balances SET amount = amount - ? WHERE user_id = ?;
  INSERT INTO orders ...;
COMMIT;
```

## Testing Strategy

### Unit Test: Race Condition
```python
import threading

def test_concurrent_order_fill():
    order_id = create_test_order()
    
    results = []
    def fill_order_thread():
        result = fill_order(order_id)
        results.append(result)
    
    # Spawn 10 concurrent fill attempts
    threads = [threading.Thread(target=fill_order_thread) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    # Only 1 should succeed
    assert sum(1 for r in results if r.success) == 1
    
    # Order should be FILLED
    order = get_order(order_id)
    assert order.status == 'FILLED'
```

### Integration Test: Cache Invalidation
```python
def test_cache_invalidation_on_fill():
    order_id = create_test_order()
    
    # Cache listings
    listings = get_listings()  # Hits cache
    assert order_id in [o.id for o in listings]
    
    # Fill order
    fill_order(order_id)
    
    # Listings should be updated immediately
    listings = get_listings()
    assert order_id not in [o.id for o in listings]
```

### E2E Test: Frontend Update
```javascript
// Playwright/Cypress test
test('order disappears after fill', async () => {
  await page.goto('/listings');
  
  // Wait for listings to load
  await page.waitForSelector('.order-item');
  
  const orderCount = await page.$$eval('.order-item', els => els.length);
  
  // Fill order via API
  await fillOrder(orderId);
  
  // Wait for websocket update
  await page.waitForTimeout(1000);
  
  // Order should be removed from UI
  const newOrderCount = await page.$$eval('.order-item', els => els.length);
  expect(newOrderCount).toBe(orderCount - 1);
});
```

## Monitoring & Alerting

**Metrics to track:**
```python
# Order fill latency
metrics.histogram('order.fill.latency', duration_ms)

# Cache hit rate
metrics.gauge('cache.listings.hit_rate', hit_rate)

# Websocket message delivery
metrics.counter('websocket.orderFilled.sent')
metrics.counter('websocket.orderFilled.acked')

# Stale order detection
metrics.counter('order.stale_detected', tags={'order_id': order_id})
```

**Alert rules:**
```yaml
# Alert if order fill takes >5 seconds
- alert: SlowOrderFill
  expr: order_fill_latency_p95 > 5000
  
# Alert if cache hit rate drops below 80%
- alert: LowCacheHitRate
  expr: cache_listings_hit_rate < 0.8
  
# Alert if websocket delivery fails
- alert: WebsocketDeliveryFailure
  expr: rate(websocket_orderFilled_sent[5m]) > rate(websocket_orderFilled_acked[5m]) * 1.1
```

## Debugging Checklist

When user reports "order reappeared":

1. **Check database:**
   ```sql
   SELECT * FROM orders WHERE id = '<order_id>';
   ```
   - If status = FILLED → frontend/cache bug
   - If status = OPEN → database bug

2. **Check API response:**
   ```bash
   curl -s "https://example.com/api/listings" | jq '.[] | select(.id == "ORDER_ID")'
   ```
   - If present → backend bug
   - If absent → frontend bug

3. **Check websocket logs:**
   ```bash
   grep "orderFilled.*ORDER_ID" /var/log/websocket.log
   ```
   - If no log → websocket not sent
   - If logged → check client receipt

4. **Check cache:**
   ```bash
   redis-cli GET "listings"
   ```
   - If contains order → cache not invalidated
   - If absent → cache working correctly

5. **Check replication lag:**
   ```sql
   SHOW SLAVE STATUS\G
   ```
   - If lag >1s → replication issue
   - If lag <1s → not replication issue

## References

- PostgreSQL Locking: https://www.postgresql.org/docs/current/explicit-locking.html
- MySQL Transactions: https://dev.mysql.com/doc/refman/8.0/en/innodb-locking.html
- Redis Cache Invalidation: https://redis.io/docs/manual/patterns/cache-invalidation/
