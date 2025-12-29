# Act 3 Challenges - SANS Holiday Hack Challenge 2025

**Status:** 2/2 Documented (both in progress)

Act 3 features advanced challenges combining web security, privilege escalation, and data exfiltration techniques.

## Challenges

### 1. [GnomeTea - Firebase Security Misconfiguration](01-gnometea.md)

**Difficulty:** ⭐⭐⭐  
**Status:** ⚠️ In Progress

Exploit Firebase/Firestore security misconfigurations to access a secret passphrase stored in a protected admin collection.

**Key Techniques:**
- Firebase configuration analysis
- Firestore security rule exploitation
- Browser console JavaScript manipulation
- Direct database queries without authentication
- Credential discovery via DM analysis
- OSINT for driver's license information

**Python Scripts Available:**
- `scripts/gnometea/gnometea_complete_extractor.py` - Full Firestore data extraction
- `scripts/gnometea/analyze_data.py` - Analyze extracted data for credentials
- `scripts/gnometea/find_barnaby_license.py` - Locate and download driver's license

See: [scripts/gnometea/README.md](../scripts/gnometea/README.md) for usage instructions.

---

### 2. [Snowcat Privilege Escalation](02-snowcat-privilege-escalation.md)

**Difficulty:** ⭐⭐⭐  
**Status:** ⚠️ In Progress - RCE Achieved, Privilege Escalation Incomplete

Exploit a Java deserialization vulnerability (CVE-2025-24813) to gain RCE, then escalate privileges via SUID binary exploitation to retrieve an unauthorized API key.

**Key Techniques:**
- Java deserialization exploitation (ysoserial)
- CommonsCollections gadget chains
- SUID/SGID binary analysis
- Privilege escalation techniques:
  - PATH hijacking attempts
  - LD_PRELOAD injection attempts
  - Command injection testing
  - Symbolic link attacks
  - Buffer overflow testing
- String analysis for binary reverse engineering

**Current Status:**
- ✅ RCE as `snowcat` user achieved via CVE-2025-24813
- ✅ Complete /usr/local/weather/ file structure mapped
- ✅ SUID binaries analyzed (pressure, temperature, humidity)
- ⚠️ Privilege escalation to `weather` group incomplete
- ⚠️ API key retrieval pending

**Limitations Discovered:**
- Shell redirections (>, |, 2>&1) don't work in deserialization payloads
- Output cannot be captured from RCE commands
- Standard privilege escalation vectors blocked by SUID protections

---

## Summary

| Challenge | Difficulty | Topics | Status |
|-----------|-----------|--------|---------|
| GnomeTea | ⭐⭐⭐ | Firebase, Firestore, NoSQL, OSINT | ✅ Complete |
| Snowcat | ⭐⭐⭐ | Java Deserialization, SUID, Privilege Escalation | ⚠️ In Progress |

## Key Learnings

### Web Application Security
- **Firebase Misconfigurations:** Firestore security rules often leave collections unsecured
- **Client-Side Secrets:** Sensitive configuration in JavaScript accessible via DevTools
- **Comment-Based OSINT:** HTML comments can leak test credentials and TODOs

### Binary Exploitation
- **Java Deserialization:** Different gadget chains work against different targets
- **SUID Security:** Modern SUID binaries have strong protections (LD_PRELOAD blocked, PATH sanitized)
- **Reverse Engineering:** `strings` command reveals valuable binary behavior insights

### Attack Methodology
- **Reconnaissance First:** Map all accessible resources before exploitation
- **Document Limitations:** RCE without output capture requires creative approaches
- **Persistence Matters:** Complex challenges require methodical testing of multiple vectors

## Scripts & Tools

All Python scripts for GnomeTea are in the `scripts/gnometea/` directory with full documentation.

## Images

All screenshots for Act 3 challenges are in `images/act3/` (20 images total).

---

**Author:** SFC David P. Collette  
**Organization:** Regional Cyber Center - Korea (RCC-K)  
**Role:** Senior Executive in Defensive Cyber Operations
