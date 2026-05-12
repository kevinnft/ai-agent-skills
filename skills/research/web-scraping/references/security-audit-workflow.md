# Security Audit Workflow

End-to-end workflow for conducting security audits and responsible disclosure (tested May 2026 on rpow2swap.com).

## When to Use

- User asks to "find bugs" or "test security"
- Responsible disclosure to site owner
- Vulnerability assessment for bug bounty
- Pre-launch security review

## Workflow

### 1. Reconnaissance

**API endpoint discovery:**
```bash
# Trial-error common paths
for path in /api/listings /api/users /api/orders /api/admin /api/config /api/env; do
  timeout 3 curl -s -m 3 -o /dev/null -w "HTTP %{http_code} | Size: %{size_download}\\n" \
    "https://target.com$path"
done
```

**Response analysis:**
- 200 + large size → public endpoint (check if should be protected)
- 200 + small size → SPA HTML fallback
- 401/403 → protected (good)
- 404 → not found
- 500 → server error (potential DoS vector)
- Timeout → slow query or rate limiting

### 2. Automated Testing

**Test categories:**
1. **Authentication bypass** (SQL injection in auth, missing auth checks)
2. **Rate limiting** (DoS vulnerability)
3. **CORS misconfiguration** (permissive `Access-Control-Allow-Origin`)
4. **Input validation** (negative values, SQL injection, XSS)
5. **IDOR** (Insecure Direct Object Reference)
6. **Path traversal** (`/api/../../../etc/passwd`)
7. **Data integrity** (anomalies in public data)

**Example script:**
```python
#!/usr/bin/env python3
import requests

API_BASE = "https://target.com"

def test_rate_limiting():
    """Test rate limiting by sending rapid requests"""
    for i in range(50):
        r = requests.get(f"{API_BASE}/api/listings", timeout=2)
        if r.status_code == 429:
            return {"status": "RATE_LIMITED", "note": "Rate limiting detected"}
    return {"status": "NO_RATE_LIMIT", "note": "⚠️ No rate limiting - DoS vulnerability"}

def test_cors():
    """Test CORS configuration"""
    r = requests.options(f"{API_BASE}/api/listings", headers={
        "Origin": "https://evil.com",
        "Access-Control-Request-Method": "POST"
    })
    
    allow_origin = r.headers.get("Access-Control-Allow-Origin")
    
    return {
        "allow_origin": allow_origin,
        "note": "⚠️ Permissive CORS" if allow_origin == "*" else "OK"
    }

def test_input_validation():
    """Test input validation with malicious payloads"""
    payloads = [
        {"amount": -1000, "price": 1},  # Negative values
        {"amount": "'; DROP TABLE items; --", "price": 1},  # SQL injection
        {"amount": "<script>alert('xss')</script>", "price": 1},  # XSS
    ]
    
    results = []
    for payload in payloads:
        r = requests.post(f"{API_BASE}/api/listings", json=payload)
        if r.status_code in [200, 201]:
            results.append({
                "payload": payload,
                "note": "⚠️ Invalid input accepted"
            })
    
    return results
```

### 3. Report Generation

**Structure:**
```markdown
# Security Audit Report

**Date:** YYYY-MM-DD
**Target:** https://target.com
**Purpose:** Responsible Disclosure

## Executive Summary

Brief overview of findings.

## Critical Findings

### 1. 🚨 CRITICAL: [Vulnerability Name]
**Severity:** Critical
**Impact:** [Description]

[Details]

**Recommendation:** [Fix]

### 2. ⚠️ MEDIUM: [Vulnerability Name]
...

## Positive Findings

✅ [Good security practices observed]

## Recommendations

- 🚨 **CRITICAL:** [Action]
- ⚠️ **MEDIUM:** [Action]

## Contact for Disclosure

Report will be sent to: [email]
```

### 4. Responsible Disclosure

**Email template:**
```
Subject: [Security Disclosure] [Site Name] Vulnerability Report

Dear [Site Name] Team,

I am writing to responsibly disclose several security vulnerabilities 
discovered during a security audit of [site]. This report is provided 
in good faith to help improve the security of your platform.

## Critical Findings

[Summary of critical vulnerabilities]

## Disclosure Timeline

- Discovery Date: [date]
- Disclosure Date: [date]
- Requested Response: Within 7 days
- Public Disclosure: 30 days after fix confirmation

## Contact

For questions or clarifications, please contact:
- Email: [your email]

Attached: Full technical report

Best regards,
Security Researcher
```

**Attachment:** Full markdown report with technical details.

## Pitfalls

- **Don't exploit production systems:** Read-only testing only, no data modification
- **Verify testnet vs mainnet:** Check wallet addresses, transaction history
- **Rate limiting:** Don't DoS the site during testing (use reasonable intervals)
- **False positives:** Timeouts may be network issues, not vulnerabilities
- **Scope creep:** Focus on high-impact vulnerabilities, not minor issues
- **Legal concerns:** Ensure testing is authorized or within bug bounty scope

## User Preference (May 2026)

**"Tampilkan disini dulu jngn langsung kirim ke email web"**

Before sending disclosure email:
1. Generate full report
2. Display in chat for user review
3. Wait for user approval
4. Then send to site owner

**Workflow:**
```python
# Generate report
report = generate_report(results)

# Save to file
with open("/tmp/security_audit.md", "w") as f:
    f.write(report)

# Display in chat (via send_message or print)
print(report)

# Wait for user confirmation before sending email
```

## Example: rpow2swap.com (May 2026)

**Findings:**
1. 🚨 **CRITICAL:** No rate limiting (DoS vulnerability)
2. ⚠️ **MEDIUM:** Permissive CORS (`Access-Control-Allow-Origin: *`)
3. ⚠️ **MEDIUM:** Multiple endpoint timeouts (possible DoS vector)
4. ℹ️ **LOW:** Suspicious listings (price anomalies)

**Good practices:**
- ✅ POST endpoints protected (401 auth)
- ✅ SQL injection attempts blocked
- ✅ Path traversal handled properly

**Contact:** rpow2swap@protonmail.com (found in minified JS)

**Files:**
- `/tmp/rpow2_security_audit.md` — Full report
- `/tmp/disclosure_email.txt` — Email draft
- `/tmp/rpow2_security_audit.py` — Audit script

## Verification

**Test script manually:**
```bash
python3 /tmp/security_audit.py
```

**Review report:**
```bash
cat /tmp/security_audit.md
```

**Send disclosure:**
```bash
# Manual: Copy email draft and send via email client
# Automated: Use Himalaya CLI (requires SMTP config)
```

## Legal & Ethical Considerations

**DO:**
- ✅ Test read-only operations
- ✅ Report vulnerabilities responsibly
- ✅ Give site owner time to fix (30 days standard)
- ✅ Use test accounts when possible

**DON'T:**
- ❌ Exploit vulnerabilities for personal gain
- ❌ Modify/delete production data
- ❌ Access other users' accounts
- ❌ Public disclosure before fix
- ❌ Test without authorization (unless bug bounty)

**Gray areas:**
- Automated scanning (may trigger rate limits)
- Testing authentication bypass (may violate ToS)
- Accessing admin endpoints (even if unprotected)

**When in doubt:** Ask for permission or stick to public endpoints only.
