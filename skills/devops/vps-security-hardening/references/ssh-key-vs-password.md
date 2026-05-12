# SSH Key vs Password Authentication — Decision Framework

## Quick Comparison

| Aspect | Password + fail2ban | SSH Key |
|--------|-------------------|---------|
| **Security** | 99% (excellent) | 99.9% (maximum) |
| **Brute-force** | Blocked by fail2ban | Impossible |
| **Password leak** | Risk: attacker can login | Risk: zero (password useless) |
| **Convenience** | Easy (just type) | Need key file |
| **Portability** | Login from anywhere | Need key file on device |
| **Setup** | Already done | 5-10 minutes |
| **Emergency access** | Type password anywhere | Need key file or console |

## When to Keep Password

✅ User comfortable with current setup
✅ Strong password (12+ chars, mixed)
✅ Don't login from many devices
✅ Don't need automation (scripts)
✅ Want portability (login from anywhere)
✅ Don't want key file management

**Security level:** 99% with fail2ban — **good enough for most use cases**

## When to Upgrade to SSH Key

⚠️ Handle sensitive data (payment, personal info)
⚠️ Worried about password leak
⚠️ Login frequently (10+ times/day)
⚠️ Need automation (backup scripts, CI/CD)
⚠️ Multiple devices (want granular control)
⚠️ Want maximum security

**Security level:** 99.9% — **best for production/sensitive data**

## Hybrid Approach (Best of Both)

Setup SSH key as primary, keep password as backup:

```bash
# 1. Setup SSH key (primary)
ssh-keygen -t ed25519
ssh-copy-id user@host

# 2. Keep PasswordAuthentication yes (backup)

# 3. Use key by default
ssh user@host  # Uses key automatically

# 4. Use password if needed (emergency)
ssh -o PubkeyAuthentication=no user@host
```

**Benefits:**
- Daily use: SSH key (fast, secure)
- Emergency: Password (if lose key file)
- Best of both worlds

## User Communication Pattern

### Present Options Once

```
"Mau gue setup SSH key sekarang? Atau keep password (sudah aman)?"

Options:
1. Keep password — Sudah aman, gak perlu apa-apa ✅
2. Setup SSH key — Maximum security 🔑
3. Hybrid — SSH key + keep password (best of both) 🎯
```

### User Decides

User says: "Keep password aja" or "tanpa ssh key"

### Accept and Move On

```
"Perfect! Keep password — sudah aman dan praktis. ✅

Security Level: 99% SECURE (excellent with fail2ban)
Status: OPTIMAL untuk current use case"
```

### DO NOT

❌ "Tapi SSH key lebih aman..."
❌ "Yakin gak mau SSH key?"
❌ "Nanti kalau password leaked..."
❌ Keep suggesting alternatives

### DO

✅ Accept decision immediately
✅ Confirm security is already good
✅ Provide monitoring commands
✅ Move on to next topic

## Password Strength Guidelines

**Weak (❌ NOT SAFE):**
- 123456, password, ubuntu123, qwerty, admin

**Medium (🟡 OKAY):**
- MyPassword123, Ubuntu2026, Server@123

**Strong (✅ SAFE):**
- X9$mK2#pL7@nQ4
- Tr0ub4dor&3-Correct-Horse-Battery
- aB3$dE6#gH9@jK2

With fail2ban, even medium passwords are reasonably safe (attacker only gets 5 attempts before ban).

## Real-World Scenarios

### Scenario 1: Personal Dev Server
- **Use case:** Learning, testing, personal projects
- **Recommendation:** Password + fail2ban ✅
- **Reason:** Convenience > maximum security

### Scenario 2: Production Server
- **Use case:** Customer data, payment processing
- **Recommendation:** SSH key (disable password) 🔑
- **Reason:** Maximum security required

### Scenario 3: Shared Team Server
- **Use case:** Multiple developers, CI/CD
- **Recommendation:** SSH keys (one per person) 🔑
- **Reason:** Granular access control, revocable

### Scenario 4: Emergency-Only Access
- **Use case:** Rarely login, might need from anywhere
- **Recommendation:** Hybrid (key + password backup) 🎯
- **Reason:** Convenience + emergency fallback
