# Snowcat Privilege Escalation - Not Complete

**Difficulty:** ⭐⭐⭐ (In Progress)

**SANS Holiday Hack Challenge 2025 - Act 3**

---

Snowcat Privilege Escalation Challenge

*SANS Holiday Hack Challenge 2025 - Act 3*

**Difficulty: ⭐⭐⭐ (In Progress)**

Challenge Overview

Exploit the Snowcat web server to gain elevated privileges and retrieve
an unauthorized API key. The challenge combines **Java deserialization
RCE** with **SUID binary privilege escalation**.

**Objective:** Find an API key that is NOT being used by the
Snowcat-hosted Neighborhood Weather Monitoring Station.

**Known API Key in Use:** 4b2f3c2d-1f88-4a09-8bd4-d3e5e52e19a6

Phase 1: Initial Reconnaissance

System Enumeration

Starting in the user home directory, we discovered several important
files:

user@weather:~\$ ls -la

-rwx------ 1 user user 1992 Sep 13 08:24 CVE-2025-24813.py -rw-rw-r-- 1
user user 1424 Sep 13 08:24 notes.md drwxrwxr-x 1 user user 4096 Sep 15
08:15 weather-jsps/ -rw-rw-r-- 1 user user 59525376 Sep 13 08:24
ysoserial.jar

Key Files Discovered

- CVE-2025-24813.py - Python exploit script for Snowcat RCE

- notes.md - Contains challenge hints and technical debt notes

- weather-jsps/ - JSP files revealing application logic and API key
  usage

- ysoserial.jar - Tool for generating Java deserialization payloads

Service Discovery

Checking listening ports revealed the Snowcat web server:

ss -tlnp

LISTEN 0 100 127.0.0.1:8005 0.0.0.0:\* LISTEN 0 100 0.0.0.0:80
0.0.0.0:\*

- **Port 80** - Snowcat web server (public interface)

- **Port 8005** - Internal service (localhost only)

Weather Binary Discovery

Found three SUID binaries in /usr/local/weather/:

1212858 -rwsr-sr-x 1 root weather 16984 humidity 1212865 -rwsr-sr-x 1
root weather 16984 pressure 1212867 -rwsr-sr-x 1 root weather 16992
temperature

**Critical Observation:** temperature is 8 bytes larger (16992 vs
16984) - potentially contains different code or vulnerability.

Phase 2: Remote Code Execution via CVE-2025-24813

Vulnerability Analysis

CVE-2025-24813 is a Java deserialization vulnerability in the Snowcat
web server. The vulnerability allows unauthenticated attackers to
execute arbitrary code by crafting malicious serialized Java objects and
sending them via HTTP PUT requests.

**Attack Vector:** Apache Commons Collections gadget chains enable code
execution during object deserialization.

Exploitation Steps

Step 1: Generate Payload

Using ysoserial to create a CommonsCollections7 gadget chain:

java -jar ysoserial.jar CommonsCollections7 'touch /tmp/rce_worked' \|
\\ base64 -w 0 \> payload_b64.txt

Step 2: Deliver Exploit

Using the provided Python script to send the malicious payload:

python3 CVE-2025-24813.py \\ --host localhost \\ --port 80 \\
--base64-payload "\$(cat payload_b64.txt)" \\ --session-id
unique-test-123

Step 3: Verify Code Execution

ls -la /tmp/rce_worked

-rw-r--r-- 1 snowcat snowcat 0 Dec 28 01:00 /tmp/rce_worked

**Success!** File created as snowcat user, confirming RCE.

Gadget Chain Testing Results

Tested multiple Commons Collections gadget chains:

- CommonsCollections5 - Failed (ClassCastException)

- CommonsCollections6 - Failed (ClassCastException)

- CommonsCollections7 - **Success!** (HTTP 200 OK)

RCE Limitations Discovered

**Critical Limitation:** Shell redirections (\>, \|, \<, \>\>, 2\>&1) do
not work in deserialization payloads.

Failed attempts to capture command output:

- File redirection: ls \> /tmp/output.txt

- Pipes: cat file \| grep pattern

- stderr redirect: command 2\>&1

- Python file writes: python -c 'open(...)'

Commands execute but output cannot be captured or redirected, severely
limiting information gathering capabilities.

Phase 3: Privilege Escalation Attempts

Target System Analysis

File Structure

/usr/local/weather/ ├── config (weather:snowcat, 35 bytes) ├── data/
(weather:snowcat, drwx------) │ ├── humidity │ ├── pressure │ └──
temperature ├── humidity (root:weather, -rwxr-xr-x) ├── keys/
(weather:weather, drwx------) │ └── authorized_keys (target file) ├──
logUsage (root:weather, -rwxr-x---) ├── logs/ (weather:weather,
drwx------) ├── pressure (root:weather, -rwsr-sr-x, SUID) └──
temperature (root:weather, -rwsr-sr-x, SUID)

SUID Binary Analysis

Using strings to analyze the SUID binaries revealed their execution
flow:

- Read /usr/local/weather/config for username/groupname

- Check /usr/local/weather/keys/authorized_keys for valid API keys

- Use setuid/setgid to drop privileges to weather user

- Execute /usr/local/weather/logUsage with parameters

- Read sensor data from /usr/local/weather/data/

**Key Finding:** Binaries temporarily gain weather group privileges via
SUID/SGID bits, then call logUsage script.

Failed Exploitation Techniques

The following privilege escalation vectors were tested and failed:

1\. PATH Hijacking

**Attempt:** Create malicious logUsage in controlled directory and
manipulate PATH.

**Result:** Failed - Binaries use absolute path
/usr/local/weather/logUsage

2\. LD_PRELOAD Injection

**Attempt:** Preload malicious shared library via LD_PRELOAD environment
variable.

**Result:** Failed - SUID binaries ignore LD_PRELOAD for security

3\. Command Injection in API Key

**Attempt:** Inject shell metacharacters in API key parameter:
\$(whoami), \`id\`, ;ls

**Result:** Failed - API key validated against authorized_keys before
use

4\. Symbolic Link Attack

**Attempt:** Create symlinks to target files in accessible locations.

**Result:** Failed - Permissions checked on target file, not symlink

5\. Buffer Overflow

**Attempt:** Send 1000+ character API key to overflow buffers.

**Result:** Failed - Returns "Unauthorized" without crash

6\. Format String Vulnerability

**Attempt:** Use format specifiers: %s%s%s%s

**Result:** Failed - Returns "Unauthorized" without exploitable behavior

7\. File Copying via RCE

**Attempt:** Use RCE to copy files to accessible locations.

**Result:** Failed - Commands execute but snowcat user lacks read
permissions

8\. Process Memory Inspection

**Attempt:** Dump process memory using gdb or gcore

**Result:** Failed - Binaries execute too quickly to attach debugger

Current Status & Next Steps

Challenge Status

**Status: IN PROGRESS** - RCE achieved, privilege escalation incomplete

What We've Accomplished

- **✓** Successfully exploited CVE-2025-24813 for RCE as snowcat user

- **✓** Mapped complete /usr/local/weather/ file structure

- **✓** Analyzed SUID binary behavior via strings command

- **✓** Identified temperature binary as 8 bytes larger than others

- **✓** Tested 8+ privilege escalation vectors

Unexplored Avenues

The following areas have not yet been thoroughly investigated:

- logUsage script contents - Analyze the script called by SUID binaries

- /usr/local/weather/logs/ - Check if log files are readable or contain
  API keys

- data/ files - Examine sensor data files for clues

- TOCTOU (Time-of-check/time-of-use) race conditions

- Core dump analysis

- Stderr output from binaries when run with invalid keys

Technical Concepts Learned

Java Deserialization Attacks

Java deserialization vulnerabilities occur when applications deserialize
untrusted data without proper validation. Attackers craft malicious
serialized objects (gadget chains) that execute arbitrary code during
the deserialization process.

**Key Tool:** ysoserial - Generates payloads exploiting gadget chains in
common Java libraries like Apache Commons Collections.

SUID/SGID Binaries

SUID (Set User ID) and SGID (Set Group ID) are special permissions that
allow executables to run with the privileges of their owner/group rather
than the user executing them.

- **SUID:** Runs with file owner's permissions (often root)

- **SGID:** Runs with file group's permissions

- **Security:** SUID binaries ignore LD_PRELOAD and sanitize environment
  variables

Common Privilege Escalation Techniques

- **PATH Hijacking:** Manipulate search path to execute malicious
  binaries

- **LD_PRELOAD:** Preload malicious shared libraries (blocked by SUID)

- **Command Injection:** Inject shell commands via user-controlled input

- **Race Conditions:** Exploit timing gaps in privilege checks (TOCTOU)

- **Buffer Overflows:** Overflow buffers to overwrite return addresses

Key Takeaways

- Deserialization vulnerabilities require specific gadget chains - not
  all work against all targets

- RCE limitations (no redirects) can severely hamper information
  gathering

- SUID binaries have strong security protections against common
  exploitation techniques

- File size differences in similar binaries may indicate different code
  paths or vulnerabilities

- The strings command reveals valuable insights into binary behavior

- Privilege escalation often requires creative thinking and persistence

**Challenge Status: IN PROGRESS**

*RCE ✓ \| Privilege Escalation ⚠️ \| Flag Retrieval ✗*

**SFC David P. Collette**

*Regional Cyber Center - Korea (RCC-K)*
