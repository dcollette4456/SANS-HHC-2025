# SANS Holiday Hack Challenge 2025 - Complete Write-Up

> **Author**: SFC David P. Collette  
> **Organization**: United States Army - Regional Cyber Center - Korea (RCC-K)  
> **Role**: Senior Executive in Defensive Cyber Operations | Penetration Testing Instructor

---

## 📋 Table of Contents

### Act 1: The Gnome Invasion
1. [Its All About Defang](ACT-1/01-defang.md) ⭐
2. [Neighborhood Watch Bypass](ACT-1/02-neighborhood-watch-bypass.md) ⭐⭐
3. [Santa's Gift-Tracking Service Port Mystery](ACT-1/03-santas-gift-tracker.md) ⭐
4. [Visual Networking Thinger](ACT-1/04-visual-networking.md) ⭐
5. [Visual Firewall Thinger](ACT-1/05-visual-firewall.md) ⭐
6. [Intro to Nmap](ACT-1/06-intro-to-nmap.md) ⭐
7. [Blob Storage Challenge in the Neighborhood](ACT-1/07-blob-storage.md) ⭐
8. [Spare Key](ACT-1/08-spare-key.md) ⭐⭐
9. [The Open Door](ACT-1/09-the-open-door.md) ⭐
10. [Owner](ACT-1/10-owner.md) ⭐⭐

### Act 2: _Coming Soon_
- Retro Recovery
- Mail Detective
- IDORable Bistro
- Dosis Network Down
- Rogue Gnome Identity Provider
- Quantgnome Leap
- Going in Reverse

---

## 🎯 Challenge Summary

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

- **Total Challenges Completed**: 10/10 (Act 1)
- **Difficulty Range**: ⭐ to ⭐⭐
- **Primary Domains**: Cloud Security, Linux Privilege Escalation, Network Analysis
- **Images**: 60+ screenshots and diagrams
- **Detailed Walkthroughs**: Complete step-by-step solutions with commands and outputs

---

## 💡 Key Learnings

### Azure Security
- RBAC audit techniques and PIM enforcement
- NSG misconfiguration identification
- SAS token security and expiration policies
- Public blob access risks
- Nested group permission inheritance

### Linux Privilege Escalation
- PATH hijacking via sudo with preserved environment
- env_keep+=PATH vulnerability
- Exploiting scripts with relative command paths
- Enumeration methodology (sudo -l, SUID binaries)

### Network & SOC Operations
- IOC extraction with regex
- Proper defanging standards
- Port scanning methodologies
- Network protocol fundamentals
- Firewall zone configuration

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
