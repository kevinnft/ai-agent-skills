# Web Application Security Audit Pattern

Structured approach for security auditing web applications for responsible disclosure.

## Use Case

User wants to find vulnerabilities in a web application to report to the owner (responsible disclosure, bug bounty, security research).

## Audit Structure

### 1. API Endpoint Discovery & Testing

Test common endpoints for:
- **Exposure:** Admin/config/env endpoints accessible without auth
- **SQL Injection:** `?id=1' OR '1'='1`
- **Path Traversal:** `/api/../../../etc/passwd`
- **IDOR:** `/api/user/1`, `/api/order/1` (access other users' data)
- **Authentication bypass:** POST without auth token

**Pattern:**
```python
endpoints = [
    # Public endpoints (should work)
    ("/api/listings", "GET", None),
    
    # Admin/sensitive (should be protected)
    ("/api/admin", "GET", None),
    ("/api/config", "GET", None),
    ("/api/env", "GET", None),
    
    # SQL injection tests
    ("/api/listings?id=1' OR '1'='1", "GET", None),
    
    # Path traversal
    ("/api/../../../etc/passwd", "GET", None),
    
    # IDOR
    ("/api/user/1", "GET", None),
    
    # Auth bypass
    ("/api/listings", "POST", {"data": "test"}),
]

for path, method, data in endpoints:
    try:
        url = f"{BASE_URL}{path}"
        if method == "GET":
            r = requests.get(url, timeout=5)
        elif method == "POST":
            r = requests.post(url, json=data, timeout=5)
        
        results.append({
            "endpoint": path,
            "status": r.status_code,
            "size": len(r.content),
            "note": classify_response(r)
        })
    except requests.exceptions.Timeout:
        results.append({
            "endpoint": path,
            "status": "TIMEOUT",
            "note": "Possible DoS vector"
        })
```

### 2. Authentication Testing

Test if endpoints require authentication:
```python
tests = [
    ("No auth header", {}),
    ("Invalid token", {"Authorization": "Bearer invalid"}),
    ("SQL injection in token", {"Authorization": "Bearer ' OR '1'='1"}),
    ("Empty token", {"Authorization": "Bearer "}),
]

for test_name, headers in tests:
    r = requests.get(f"{BASE_URL}/api/listings", headers=headers)
    authenticated = r.status_code != 401
```

### 3. Rate Limiting Test

Send rapid requests to detect rate limiting:
```python
for i in range(50):
    r = requests.get(f"{BASE_URL}/api/listings", timeout=2)
    if r.status_code == 429:
        print(f"Rate limited after {i+1} requests")
        break
else:
    print("⚠️ No rate limiting detected - DoS vulnerability")
```

### 4. CORS Configuration

Check for permissive CORS:
```python
r = requests.options(f"{BASE_URL}/api/listings", headers={
    "Origin": "https://evil.com",
    "Access-Control-Request-Method": "POST"
})

if r.headers.get("Access-Control-Allow-Origin") == "*":
    print("⚠️ Permissive CORS - allows any origin")
```

### 5. Input Validation

Test with malicious payloads:
```python
payloads = [
    {"amount": -1000, "price": 1},  # Negative values
    {"amount": 999999999999, "price": 0.000001},  # Overflow
    {"amount": "'; DROP TABLE listings; --", "price": 1},  # SQL injection
    {"amount": "<script>alert('xss')</script>", "price": 1},  # XSS
]

for payload in payloads:
    r = requests.post(f"{BASE_URL}/api/listings", json=payload)
    if r.status_code in [200, 201]:
        print(f"⚠️ Invalid input accepted: {payload}")
```

### 6. Data Analysis

Analyze existing data for anomalies:
```python
listings = requests.get(f"{BASE_URL}/api/listings").json()

for listing in listings:
    # Check for negative values (should be impossible)
    if listing.get("amount", 0) < 0 or listing.get("price", 0) < 0:
        print(f"🚨 CRITICAL: Negative values in listing {listing['id']}")
    
    # Check for price manipulation
    if listing["amount"] > 0:
        price_per_unit = listing["price"] / listing["amount"]
        if price_per_unit < 0.00001:
            print(f"⚠️ Suspiciously low price: {listing['id']}")
        if price_per_unit > 100:
            print(f"⚠️ Suspiciously high price: {listing['id']}")
```

## Report Structure

### Executive Summary
- Date, target, purpose
- Number of vulnerabilities found
- Severity breakdown

### Findings by Category
1. **API Endpoint Testing**
   - Status codes, response sizes
   - Classify: ✅ OK, ⚠️ WARNING, 🚨 ERROR
   
2. **Authentication**
   - Which endpoints require auth
   - Bypass attempts
   
3. **Rate Limiting**
   - Presence/absence
   - Threshold if detected
   
4. **CORS**
   - Configuration
   - Permissiveness level
   
5. **Input Validation**
   - Accepted/rejected payloads
   - Sanitization effectiveness
   
6. **Data Integrity**
   - Anomalies in existing data
   - Business logic flaws

### Recommendations
Prioritized by severity:
- 🚨 **CRITICAL:** Immediate action required (DoS, data breach risk)
- ⚠️ **MEDIUM:** Should fix soon (CORS, missing validation)
- ℹ️ **LOW:** Nice to have (data quality, UX issues)

### Positive Findings
List what's done right (builds trust with recipient).

### Disclosure Timeline
- Discovery date
- Disclosure date
- Requested response time (7 days)
- Public disclosure timeline (30 days after fix)

## Case Study: rpow2swap.com (May 2026)

**Findings:**
1. 🚨 **CRITICAL:** No rate limiting (50+ requests without throttling)
2. ⚠️ **MEDIUM:** Permissive CORS (`Access-Control-Allow-Origin: *`)
3. ⚠️ **MEDIUM:** Multiple endpoint timeouts (possible DoS vector)
4. ℹ️ **LOW:** 2 suspicious listings with abnormally high prices

**Positive:**
- ✅ POST endpoints protected (401 auth)
- ✅ SQL injection attempts blocked
- ✅ Path traversal handled properly

**Contact:** rpow2swap@protonmail.com (found in minified JS)

**Files:**
- `/tmp/rpow2_security_audit.py` — Automated audit script
- `/tmp/rpow2_security_audit.md` — Full report
- `/tmp/disclosure_email.txt` — Email template

## Ethical Guidelines

**DO:**
- Test read-only operations
- Use test accounts when possible
- Report findings responsibly
- Give reasonable response time (7-30 days)
- Offer to help with remediation

**DON'T:**
- Exploit vulnerabilities for personal gain
- Access/modify other users' data
- Perform destructive tests on production
- Publicly disclose before fix (unless critical + unresponsive)
- Demand payment (unless bug bounty program)

## Pitfalls

- **Mainnet vs Testnet:** Always verify you're testing the right environment. Check wallet addresses on blockchain explorers.
- **False positives:** Timeouts may be network issues, not vulnerabilities.
- **Legal risk:** Ensure you have permission or are within legal safe harbor (responsible disclosure laws vary by country).
- **Scope creep:** Focus on security issues, not feature requests or UX complaints.
- **Tone:** Keep report professional and constructive, not accusatory.

## Tools

- `requests` — HTTP client
- `jq` — JSON parsing
- Browser DevTools — Network inspection
- Burp Suite / OWASP ZAP — Advanced testing (optional)

## References

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- HackerOne Disclosure Guidelines: https://www.hackerone.com/disclosure-guidelines
- Bug Bounty Platforms: HackerOne, Bugcrowd, Intigriti
