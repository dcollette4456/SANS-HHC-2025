# SANS Holiday Hack Challenge 2025 - Complete Write-Up

> **Author**: SFC David P. Collette  
> **Organization**: United States Army - Regional Cyber Center - Korea (RCC-K)  
> **Role**: Senior Executive in Defensive Cyber Operations | Penetration Testing Instructor

---

## 📋 Table of Contents

### Act 1: The Gnome Invasion
1. [Its All About Defang](ACT-1/SANS2025_WriteUp_ACT1_Its_All_About_Defang.md) - ⭐ - IOC extraction, regex, defanging, SOC workflows
2. [Neighborhood Watch Bypass](ACT-1/SANS2025_WriteUp_ACT1_Neighborhood_Watch_Bypass.md) ⭐⭐ - Linux privilege escalation via PATH hijacking
3. [Santa's Gift-Tracking Service Port Mystery](ACT-1/SANS2025_WriteUp_ACT1_Santas_Gift_Tracker.md) ⭐ - Network port discovery with `ss`
4. [Visual Networking Thinger](ACT-1/SANS2025_WriteUp_ACT1_Visual_Networking.md) ⭐ - Interactive networking fundamentals
5. [Visual Firewall Thinger](ACT-1/SANS2025_WriteUp_ACT1_Visual_Firewall.md) ⭐ - Firewall rules and network segmentation
6. [Intro to Nmap](ACT-1/SANS2025_WriteUp_ACT1_Intro_to_Nmap.md) ⭐ - Port scanning and service detection
7. [Blob Storage Challenge](ACT-1/SANS2025_WriteUp_ACT1_Blob_Storage.md) ⭐⭐ - Azure storage security and public access misconfiguration
8. [Spare Key](ACT-1/SANS2025_WriteUp_ACT1_Spare_Key.md) ⭐⭐ - Azure Storage, Infrastructure as Code Security
9. [The Open Door](ACT-1/09-the-open-door.md) ⭐
10. [Owner](ACT-1/10-owner.md) ⭐⭐

### Act 2: Advanced Challenges
1. [Retro Recovery](ACT-2/01-retro-recovery.md) ⭐⭐
2. [Mail Detective](ACT-2/02-mail-detective.md) ⭐⭐
3. [IDORable Bistro](ACT-2/03-idorable-bistro.md) ⭐⭐
4. [Dosis Network Down](ACT-2/04-dosis-network-down.md) ⭐⭐
5. [Going in Reverse](ACT-2/05-going-in-reverse.md) ⭐⭐
6. [Quantgnome Leap](ACT-2/06-quantgnome-leap.md) ⭐⭐
7. [Rogue Gnome Identity Provider](ACT-2/07-rogue-gnome-identity-provider.md) ⭐⭐⭐⭐⭐

### Act 3: Expert Challenges
1. [GnomeTea - Firebase Security Misconfiguration](ACT-3/01-gnometea.md) ⭐⭐⭐ (In Progress)
2. [Snowcat Privilege Escalation](ACT-3/02-snowcat-privilege-escalation.md) ⭐⭐⭐ (In Progress)

---

## 🎯 Challenge Summary

### Act 1
| Challenge | Difficulty | Category | Skills Demonstrated |
|-----------|------------|----------|---------------------|
| Its All About Defang | ⭐ | IOC Analysis | Regex, Defanging, SOC Operations |
| Neighborhood Watch Bypass | ⭐⭐ | Privilege Escalation | PATH Hijacking, sudo exploitation |
| Santa's Gift Tracker | ⭐ | Network Enumeration | ss command, port discovery |
| Visual Networking | ⭐ | Network Fundamentals | DNS, TCP, HTTP, TLS protocols |
| Visual Firewall | ⭐ | Firewall Config | Zone-based security, rule creation |
| Intro to Nmap | ⭐ | Port Scanning | Nmap flags, version detection, banner grabbing |
| Blob Storage | ⭐ | Azure Security | Storage misconfiguration, public blob access |
| Spare Key | ⭐⭐ | Azure Security | SAS token leak, IaC security |
| The Open Door | ⭐ | Azure NSG | Network Security Groups, RDP exposure |
| Owner | ⭐⭐ | Azure RBAC | Role auditing, PIM, nested groups |

### Act 2
| Challenge | Difficulty | Category | Skills Demonstrated |
|-----------|------------|----------|---------------------|
| Retro Recovery | ⭐⭐ | Digital Forensics | FAT12, Sleuth Kit, deleted file recovery |
| Mail Detective | ⭐⭐ | Email Security | IMAP, curl, malicious JavaScript analysis |
| IDORable Bistro | ⭐⭐ | Web Security | IDOR vulnerabilities, API exploitation |
| Dosis Network Down | ⭐⭐ | Router Exploitation | CVE-2023-1389, command injection |
| Going in Reverse | ⭐⭐ | Reverse Engineering | BASIC, XOR cipher, Base64 decoding |
| Quantgnome Leap | ⭐⭐ | Post-Quantum Crypto | PQC, ML-DSA, SSH authentication |
| Rogue Gnome Identity Provider | ⭐⭐⭐⭐⭐ | Authentication | JWT forgery, JKU injection, privilege escalation |

### Act 3
| Challenge | Difficulty | Category | Skills Demonstrated |
|-----------|------------|----------|---------------------|
| GnomeTea | ⭐⭐⭐ | Firebase/NoSQL | Firestore exploitation, security rules bypass, OSINT |
| Snowcat Privilege Escalation | ⭐⭐⭐ | Binary Exploitation | Java deserialization (CVE-2025-24813), SUID binaries |

---

## 🛠️ Tools & Technologies

**Cloud Platform**:
- Azure CLI
- Azure Storage
- Azure RBAC & PIM
- Network Security Groups (NSG)

**Linux**:
- sudo privilege escalation
- PATH hijacking
- ss (socket statistics)
- privilege enumeration

**Network Tools**:
- Nmap
- curl
- ncat
- telnet

**Security Concepts**:
- IOC defanging
- Regex patterns
- Phishing analysis
- Infrastructure as Code (IaC) security

---

## 📊 Statistics

- **Total Challenges Completed**: 17/19 (Acts 1 & 2 complete, Act 3 in progress)
- **Act 1**: 10/10 challenges ✅
- **Act 2**: 7/7 challenges ✅
- **Act 3**: 2/2 challenges documented (both in progress ⚠️)
- **Difficulty Range**: ⭐ to ⭐⭐⭐⭐⭐
- **Primary Domains**: Cloud Security, Linux Privilege Escalation, Network Analysis, Web Security, Cryptography, Binary Exploitation
- **Images**: 80+ screenshots (60 Act 1, 20 Act 3; Act 2 pending extraction)
- **Python Scripts**: 3 GnomeTea extraction/analysis tools included
- **Detailed Walkthroughs**: Complete step-by-step solutions with commands and outputs

---

## 💡 Key Learnings

### Azure Security (Act 1)
- RBAC audit techniques and PIM enforcement
- NSG misconfiguration identification
- SAS token security and expiration policies
- Public blob access risks
- Nested group permission inheritance

### Linux Privilege Escalation (Act 1)
- PATH hijacking via sudo with preserved environment
- env_keep+=PATH vulnerability
- Exploiting scripts with relative command paths
- Enumeration methodology (sudo -l, SUID binaries)

### Network & SOC Operations (Act 1)
- IOC extraction with regex
- Proper defanging standards
- Port scanning methodologies
- Network protocol fundamentals
- Firewall zone configuration

### Web Security & Authentication (Act 2)
- JWT forgery and JKU injection attacks
- IDOR (Insecure Direct Object Reference) exploitation
- API enumeration and testing
- Router exploitation (CVE-2023-1389)
- Command injection vulnerabilities

### Cryptography & Forensics (Act 2)
- Post-Quantum Cryptography (PQC) concepts
- ML-DSA and hybrid cryptographic schemes
- FAT12 filesystem analysis
- Deleted file recovery with Sleuth Kit
- XOR cipher and Base64 encoding

### Email & Protocol Security (Act 2)
- IMAP protocol analysis with curl
- Malicious JavaScript detection in emails
- Data exfiltration techniques
- Reverse engineering BASIC programs

### Firebase & NoSQL Security (Act 3)
- Firebase/Firestore security rule misconfigurations
- Direct database access via browser console JavaScript
- Client-side configuration exposure risks
- NoSQL injection and unauthorized data extraction
- OSINT for credential discovery

### Binary Exploitation & Privilege Escalation (Act 3)
- Java deserialization attacks (ysoserial, CommonsCollections gadget chains)
- CVE exploitation methodology
- SUID/SGID binary analysis and exploitation attempts
- RCE limitations in restricted environments
- String analysis for reverse engineering

---

## 🎓 About RCC-K

The Regional Cyber Center - Korea (RCC-K) provides defensive cyber operations support, penetration testing, and cybersecurity training for U.S. Army forces in the Korean theater. These write-ups demonstrate real-world skills applied in:

- **Incident Response**: IOC analysis and threat intelligence sharing
- **Security Auditing**: Cloud configuration reviews and RBAC auditing
- **Penetration Testing**: Privilege escalation and exploitation techniques
- **Training & Education**: Creating educational materials for cybersecurity awareness

---

## 📝 Write-Up Format

Each challenge write-up includes:

1. **Challenge Overview**: Difficulty, category, and objectives
2. **Initial Reconnaissance**: Enumeration and discovery phase
3. **Solution Walkthrough**: Step-by-step exploitation with commands
4. **Technical Analysis**: Deep dive into vulnerabilities and concepts
5. **Key Takeaways**: Lessons learned and real-world applications
6. **Screenshots**: Embedded images showing key steps and results

---

## 🤝 Contributing

Found a better solution or alternate approach? Feel free to open an issue or submit a pull request!

---

## 📜 License

This repository is for educational purposes. All content is related to the SANS Holiday Hack Challenge 2025.

---

## 🔗 Links

- [SANS Holiday Hack Challenge](https://holidayhackchallenge.com/)
- [Counter Hack](https://www.counterhack.com/)
- [SANS Institute](https://www.sans.org/)

---

**⭐ Star this repo if you found these write-ups helpful!**
