> [!NOTE]
> **HISTORICAL — Resolved in v1.2.0 (2026-05-12).**
> This document is preserved for transparency and post-mortem reference. The bugs described here are fixed in the current code on `main`.
> See [`CHANGELOG.md`](../../../CHANGELOG.md) for the resolution.

---

# CRITICAL BUGS FOUND — FRESH ANALYSIS v2 🐛

**Date:** 2026-05-12  
**Analysis:** Deep validation from fresh clone  
**Status:** ❌ **CRITICAL BUGS CONFIRMED**

---

## 🔴 CRITICAL BUGS (6 duplicates)

### **BUG #1: Duplicate Skill Names — CRITICAL**

**Severity:** CRITICAL  
**Impact:** Skills will overwrite each other during installation

**Problem:**
When installing skills to `~/.hermes/skills/`, duplicate names cause file conflicts. The last copied skill overwrites previous ones.

**Duplicates Found:**

#### **1. test-driven-development** (3x) ❌❌❌
```
Locations:
  - addyosmani/test-driven-development
  - software-development/test-driven-development
  - superpowers/test-driven-development

Impact: Only 1 of 3 will survive installation
```

#### **2. systematic-debugging** (2x) ❌❌
```
Locations:
  - software-development/systematic-debugging
  - superpowers/systematic-debugging

Impact: One will overwrite the other
```

#### **3. requesting-code-review** (2x) ❌❌
```
Locations:
  - software-development/requesting-code-review
  - superpowers/requesting-code-review

Impact: One will overwrite the other
```

#### **4. writing-plans** (2x) ❌❌
```
Locations:
  - software-development/writing-plans
  - superpowers/writing-plans

Impact: One will overwrite the other
```

#### **5. subagent-driven-development** (2x) ❌❌
```
Locations:
  - software-development/subagent-driven-development
  - superpowers/subagent-driven-development

Impact: One will overwrite the other
```

#### **6. CI** (2x) ❌❌
```
Locations:
  - addyosmani/ci-cd-and-automation
  - github/public-repo-creation

Impact: One will overwrite the other
```

**Total Duplicates:** 6 skill names, 13 files affected

---

## 🟡 MEDIUM BUGS (7 mismatches)

### **BUG #2: Name/Directory Mismatch**

**Severity:** MEDIUM  
**Impact:** Confusing for users, inconsistent naming

**Problem:**
Skill `name:` in frontmatter doesn't match directory name. This creates confusion and inconsistency.

**Mismatches Found:**

#### **1. vllm**
```
Directory: vllm
name: serving-llms-vllm
Mismatch: ⚠️
```

#### **2. trl-fine-tuning**
```
Directory: trl-fine-tuning
name: fine-tuning-with-trl
Mismatch: ⚠️
```

#### **3. segment-anything**
```
Directory: segment-anything
name: segment-anything-model
Mismatch: ⚠️
```

#### **4. audiocraft**
```
Directory: audiocraft
name: audiocraft-audio-generation
Mismatch: ⚠️
```

#### **5. lm-evaluation-harness**
```
Directory: lm-evaluation-harness
name: evaluating-llms-harness
Mismatch: ⚠️
```

#### **6. creative-ideation**
```
Directory: creative-ideation
name: ideation
Mismatch: ⚠️
```

#### **7. software-copyright**
```
Directory: software-copyright
name: software-copyright-materials
Mismatch: ⚠️
```

**Total Mismatches:** 7 skills

---

## 🟢 MINOR BUGS (4 files)

### **BUG #3: SKILL.md Without Headings**

**Severity:** MINOR  
**Impact:** Poor documentation structure

**Problem:**
Some SKILL.md files have no markdown headings, making them hard to read.

**Files Without Headings:**

```
1. skills/mattpocock/personal/edit-article/SKILL.md
2. skills/mattpocock/engineering/zoom-out/SKILL.md
3. skills/mattpocock/productivity/handoff/SKILL.md
4. skills/mattpocock/productivity/grill-me/SKILL.md
```

**Total:** 4 files

---

## 📊 SUMMARY

### **Total Bugs:** 17

```
🔴 CRITICAL: 6 duplicate names (13 files affected)
🟡 MEDIUM:   7 name/dir mismatches
🟢 MINOR:    4 files without headings
```

### **Impact:**

#### **Critical (Duplicate Names):**
- ❌ Skills overwrite each other during installation
- ❌ Users lose skills without knowing
- ❌ Unpredictable behavior (which version survives?)
- ❌ Installation script doesn't warn about conflicts

#### **Medium (Name Mismatch):**
- ⚠️ Confusing for users
- ⚠️ Inconsistent naming convention
- ⚠️ Harder to find skills
- ⚠️ Documentation references may be wrong

#### **Minor (No Headings):**
- ⚠️ Poor readability
- ⚠️ Inconsistent structure
- ⚠️ Harder to navigate

---

## 🔧 FIX STRATEGY

### **Phase 1: Fix Critical (Duplicates)**

**Option A: Rename Duplicates**
```
Keep original in source category, rename copies:
  - superpowers/test-driven-development → tdd-superpowers
  - software-development/test-driven-development → tdd-basic
  - addyosmani/test-driven-development → tdd-production
```

**Option B: Merge Duplicates**
```
Combine into single best version:
  - Keep best implementation
  - Add references to sources
  - Delete duplicates
```

**Option C: Namespace by Category**
```
Prefix all skills with category:
  - superpowers/test-driven-development → superpowers-tdd
  - software-development/test-driven-development → dev-tdd
  - addyosmani/test-driven-development → addyosmani-tdd
```

**Recommended:** Option C (namespace by category)
- Clear ownership
- No conflicts
- Easy to identify source
- Scalable

---

### **Phase 2: Fix Medium (Mismatches)**

**Fix name/dir mismatches:**
```
Option 1: Rename directories to match name:
  vllm/ → serving-llms-vllm/

Option 2: Update name: to match directory:
  name: serving-llms-vllm → name: vllm

Recommended: Option 2 (update name:)
- Less file moves
- Shorter names
- Easier to type
```

---

### **Phase 3: Fix Minor (Headings)**

**Add headings to 4 files:**
```
Add proper markdown structure:
  # Skill Name
  
  Description...
  
  ## When to Use
  
  ## How It Works
```

---

## 🎯 PRIORITY

### **Must Fix Now:**
```
1. 🔴 Duplicate names (CRITICAL)
   - Breaks installation
   - Data loss risk
   - User confusion
```

### **Should Fix Soon:**
```
2. 🟡 Name/dir mismatches (MEDIUM)
   - Inconsistent
   - Confusing
   - Not urgent but important
```

### **Can Fix Later:**
```
3. 🟢 Missing headings (MINOR)
   - Cosmetic
   - Low impact
   - Easy fix
```

---

## ✅ VERIFICATION

### **Bugs Confirmed:**
```
✅ Duplicate names: CONFIRMED (6 duplicates, 13 files)
✅ Name mismatches: CONFIRMED (7 mismatches)
✅ Missing headings: CONFIRMED (4 files)
```

### **Testing:**
```
✅ Tested with find + grep
✅ Validated all duplicates
✅ Checked all mismatches
✅ Verified missing headings
```

---

## 🚨 RECOMMENDATION

### **IMMEDIATE ACTION REQUIRED**

**Critical bugs must be fixed before v1.2.0:**
1. Fix duplicate skill names (namespace by category)
2. Update installation script to detect conflicts
3. Add validation for duplicate names
4. Test installation with all skills

**Status:** ❌ **NOT PRODUCTION-READY** until duplicates fixed

---

**BUGS CONFIRMED — NEED IMMEDIATE FIX!** 🐛❌

**PRIORITY: CRITICAL — FIX DUPLICATES FIRST!** 🔴⚠️
