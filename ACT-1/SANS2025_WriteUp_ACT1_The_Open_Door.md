# The Open Door

**Difficulty:** ⭐

**Location:** Hotel Parking Lot  
**Character:** Goose Lucas

---

## Challenge Overview

Help Goose Lucas audit the Dosis Neighborhood's Azure network security configuration. The HOA claims all production systems are properly protected from internet attacks, but we need to verify there are no overly permissive Network Security Group (NSG) rules that could expose critical services.

**Objective:** Find the dangerously misconfigured NSG rule allowing unrestricted internet access to sensitive ports.

---

## Character Introduction: Lucas

![Challenge Badge](../images/act1/01-challenge-badge.png)

*The Open Door - Help Goose Lucas find the dangerously misconfigured Network Security Group rule*

> *(Spanish mode)* Hi... welcome to the Dosis Neighborhood! Nice to meet you! Please make sure the town's Azure network is secured properly.

---

## Challenge Briefing

The Neighborhood HOA uses Azure for their IT infrastructure. We've been tasked to audit their network security configuration to ensure production systems aren't exposed to internet attacks. They claim all systems are properly protected, but we need to verify there are no overly permissive NSG rules.

**Key Requirements:**
- Audit all Network Security Groups (NSGs)
- Identify rules exposing management ports (SSH, RDP) to the internet
- Focus on production environments
- Report any critical misconfigurations

---

## Solution Walkthrough

### Step 1: Understanding the Environment

When we access the terminal, we're presented with a welcome message explaining output formats:

```bash
# Welcome to The Open Door Challenge!
# You're connected to a read-only Azure CLI session in "The Neighborhood" tenant.
# Your mission: Review their network configurations and find what doesn't belong.
```

![Challenge Welcome Screen](../images/act1/02-welcome-screen.png)

*The terminal welcome message explaining JSON and table output formats*

The challenge provides helpful guidance on Azure CLI output formats:
- **JSON format** (default): Shows detailed structured data
- **Table format** (`-o table`): Human-readable tabular output

### Step 2: List Resource Groups

First, let's identify what resource groups exist:

```bash
az group list -o table
```

**Result:**
```
Name                  Location    ProvisioningState
--------------------  ----------  -------------------
theneighborhood-rg1   eastus      Succeeded
theneighborhood-rg2   westus      Succeeded
```

![Resource Groups](../images/act1/03-resource-groups.png)

*Resource groups displayed in JSON format showing theneighborhood-rg1 and theneighborhood-rg2*

**Analysis:** We have two resource groups - one in East US and one in West US. Let's investigate what network security groups exist in these regions.

### Step 3: List All Network Security Groups

```bash
az network nsg list -o table
```

**Result:**
```
Location  Name                      ResourceGroup
--------  ------------------------  ---------------------
eastus    nsg-web-eastus           theneighborhood-rg1
eastus    nsg-db-eastus            theneighborhood-rg1
eastus    nsg-dev-eastus           theneighborhood-rg2
eastus    nsg-mgmt-eastus          theneighborhood-rg2
eastus    nsg-production-eastus    theneighborhood-rg1
```

**Identified NSGs:**
- `nsg-web-eastus` - Web servers (public-facing)
- `nsg-db-eastus` - Database servers (should be internal only)
- `nsg-dev-eastus` - Development environment
- `nsg-mgmt-eastus` - Management servers
- `nsg-production-eastus` - **Production environment** (critical!)

### Step 4: Inspect Web NSG (Baseline)

Let's start by examining the web NSG to understand what a properly configured public-facing service looks like:

```bash
az network nsg show --name nsg-web-eastus --resource-group theneighborhood-rg1 | less
```

**Key Security Rules Found:**

| Rule Name | Port | Source | Analysis |
|-----------|------|--------|----------|
| Allow-HTTP-Inbound | 80 | 0.0.0.0/0 | ✅ Normal for web servers |
| Allow-HTTPS-Inbound | 443 | 0.0.0.0/0 | ✅ Normal for web servers |
| Allow-Web-To-App | 8080, 8443 | VirtualNetwork | ✅ Internal traffic only |
| Deny-All-Inbound | * | * | ✅ Good default deny |

**Verdict:** Web NSG is properly configured - only HTTP/HTTPS exposed to internet, with a default deny rule.

### Step 5: Inspect Management NSG

```bash
az network nsg rule list --nsg-name nsg-mgmt-eastus --resource-group theneighborhood-rg2 -o table
```

![Management NSG Rules](../images/act1/04-mgmt-nsg-rules.png)

*Management NSG showing secure Azure Bastion configuration*

**Key Findings:**

| Priority | Name | Source | Destination Port | Analysis |
|----------|------|--------|-----------------|----------|
| 100 | Allow-AzureBastion | AzureBastion | 22, 3389 | ✅ Excellent - Using Azure Bastion for secure access |
| 110 | Allow-AzureMonitor | AzureMonitor | * | ✅ Monitoring traffic |
| 120 | Allow-DNS-VirtualNetwork | VirtualNetwork | 53 | ✅ Internal DNS only |

**Verdict:** Management NSG follows security best practices:
- ✅ Uses Azure Bastion instead of exposing RDP/SSH
- ✅ No direct internet access to management ports
- ✅ All access is controlled and logged

### Step 6: Examine Remaining NSGs

Let's check the database, development, and production NSGs:

```bash
# Database NSG
az network nsg rule list --nsg-name nsg-db-eastus --resource-group theneighborhood-rg1 -o table

# Development NSG  
az network nsg rule list --nsg-name nsg-dev-eastus --resource-group theneighborhood-rg2 -o table

# Production NSG
az network nsg rule list --nsg-name nsg-production-eastus --resource-group theneighborhood-rg1 -o table
```

![All NSG Rules Comparison](../images/act1/05-all-nsg-rules.png)

*Comparison of database, development, and production NSG rules showing the critical vulnerability*

**Database NSG (nsg-db-eastus):**
- ✅ Only allows traffic from VirtualNetwork
- ✅ No internet exposure
- ✅ Properly secured

**Development NSG (nsg-dev-eastus):**
- Rule: Allow-Jumpbox-Remote-Access (ports 3389, 22)
- Source: `10.2.0.0/24` (private subnet)
- ✅ Acceptable - restricted to internal jumpbox subnet

**Production NSG (nsg-production-eastus):**
- 🚨 **CRITICAL FINDING:**
  - Rule Name: `Allow-RDP-From-Internet`
  - Port: **3389** (Remote Desktop Protocol)
  - Source: **0.0.0.0/0** (entire internet!)
  - Priority: 120

### Step 7: Investigate the Vulnerability

Let's get detailed information about this suspicious rule:

```bash
az network nsg rule show \
  --nsg-name nsg-production-eastus \
  --resource-group theneighborhood-rg1 \
  --name Allow-RDP-From-Internet
```

**Output:**
```json
{
  "name": "Allow-RDP-From-Internet",
  "properties": {
    "access": "Allow",
    "destinationPortRange": "3389",
    "direction": "Inbound",
    "priority": 120,
    "protocol": "Tcp",
    "sourceAddressPrefix": "0.0.0.0/0"
  }
}
```

![RDP Rule Details](../images/act1/06-rdp-rule-details.png)

*Detailed view of the Allow-RDP-From-Internet rule showing port 3389 open to 0.0.0.0/0*

---

## Security Analysis

### The Critical Misconfiguration

**What was found:** The production NSG (`nsg-production-eastus`) has a rule allowing RDP (port 3389) from the entire internet (0.0.0.0/0).

### Why This Is Extremely Dangerous

1. **Remote Desktop Protocol (RDP)** - Port 3389:
   - Allows remote GUI access to Windows servers
   - Full administrative capabilities when authenticated
   - Target #1 for brute force attacks

2. **Source: 0.0.0.0/0** - Open to the entire internet:
   - Anyone, anywhere can attempt to connect
   - No geographic or network restrictions
   - Exposed to global bot networks

3. **Production Environment:**
   - Contains live business systems
   - Likely has sensitive customer data
   - Compromise could lead to data breach
   - Potential regulatory violations (PCI, HIPAA, GDPR)

### Real-World Attack Scenarios

**Brute Force Attacks:**
- Attackers constantly scan for open RDP ports
- Automated tools try common username/password combinations
- Weak passwords can be cracked in minutes/hours

**Vulnerability Exploitation:**
- RDP has had critical CVEs (BlueKeep, DejaBlue)
- Unpatched systems are remotely exploitable
- Can lead to ransomware deployment

**Lateral Movement:**
- Once inside via RDP, attackers pivot to other systems
- Domain credentials can be harvested
- Entire network can be compromised

### Comparison: Good vs Bad Configurations

| NSG | Management Ports | Source | Security |
|-----|-----------------|--------|----------|
| **nsg-mgmt-eastus** | 22, 3389 | Azure Bastion | ✅ Secure |
| **nsg-dev-eastus** | 22, 3389 | 10.2.0.0/24 (internal) | ✅ Acceptable |
| **nsg-production-eastus** | **3389** | **0.0.0.0/0 (internet)** | 🚨 **CRITICAL** |

---

## The Answer

**Misconfigured NSG:** `nsg-production-eastus`  
**Vulnerable Rule:** `Allow-RDP-From-Internet`  
**Exposed Port:** **3389** (RDP)  
**Source:** **0.0.0.0/0** (entire internet)

When submitting the answer, the challenge confirms:

![Challenge Complete](../images/act1/07-challenge-complete.png)

*Challenge completion screen with achievement notification*

> Great, you found the NSG misconfiguration allowing RDP (port 3389) from the public internet!
>
> Port 3389 is used by Remote Desktop Protocol — exposing it broadly allows attackers to brute-force credentials, exploit RDP vulnerabilities, and pivot within the network.

---

## Technical Concepts Learned

### Network Security Groups (NSGs)

**What are NSGs?**
- Azure's virtual firewall for controlling network traffic
- Contain security rules that allow or deny traffic
- Can be associated with subnets or network interfaces
- Stateful firewall (return traffic automatically allowed)

**NSG Rule Components:**
- **Priority** - Lower number = evaluated first (100-4096)
- **Name** - Descriptive identifier
- **Source** - Source IP/CIDR or service tag
- **Destination** - Destination IP/CIDR
- **Port** - Destination port or range
- **Protocol** - TCP, UDP, ICMP, or Any
- **Action** - Allow or Deny
- **Direction** - Inbound or Outbound

**Rule Processing:**
1. Rules evaluated in priority order (lowest to highest)
2. First matching rule is applied
3. If no match, default deny applies
4. Explicit deny rules override allow rules

### Azure Service Tags

**Common Service Tags Seen:**
- `AzureBastion` - Azure Bastion service IP ranges
- `AzureMonitor` - Azure Monitor service
- `VirtualNetwork` - All IPs in the virtual network
- `Internet` - Public internet IP addresses

**Why use service tags?**
- Automatically updated by Microsoft
- No need to track IP ranges manually
- Cleaner, more maintainable rules

### Secure Remote Access Methods

**❌ BAD: Direct RDP/SSH Exposure**
```
Internet (0.0.0.0/0) → Port 3389 → Production Server
```
- No additional security layers
- Direct attack surface
- Difficult to monitor/audit

**✅ GOOD: Azure Bastion**
```
User → Azure Portal → Azure Bastion → Private IP → Server
```
- No public IP on server
- Encrypted in-browser RDP/SSH
- Full session logging
- MFA integration

**✅ GOOD: VPN or Private Link**
```
User → VPN/ExpressRoute → Private Network → Server
```
- Network-level encryption
- Corporate network controls
- Identity-based access

**✅ GOOD: Jump Box with Restricted Access**
```
Internet → NSG (Whitelisted IPs) → Jump Box → Internal Servers
```
- Single hardened entry point
- Restricted source IPs
- Additional logging layer

### Common NSG Misconfigurations

1. **Management Ports to Internet (CRITICAL)**
   - RDP (3389), SSH (22) from 0.0.0.0/0
   - **Fix:** Use Azure Bastion or restrict to known IPs

2. **Database Ports Exposed**
   - MySQL (3306), PostgreSQL (5432), MSSQL (1433)
   - **Fix:** Only allow from application tier subnet

3. **Overly Broad Wildcard Rules**
   - Source: Any (*), Destination: Any (*), Port: Any (*)
   - **Fix:** Implement least privilege - only needed ports/sources

4. **Missing Default Deny**
   - No catch-all deny rule at bottom
   - **Fix:** Add low-priority deny-all rule

5. **Service Tags Misuse**
   - Using `Internet` tag when specific IPs should be used
   - **Fix:** Be specific with source addresses

---

## Azure CLI Command Reference

### Resource Group Commands
```bash
# List all resource groups
az group list -o table

# Show specific resource group details
az group show --name <resource-group-name>
```

### Network Security Group Commands
```bash
# List all NSGs
az network nsg list -o table

# Show NSG details
az network nsg show --name <nsg-name> --resource-group <rg-name>

# List rules in an NSG
az network nsg rule list --nsg-name <nsg-name> --resource-group <rg-name> -o table

# Show specific rule details
az network nsg rule show \
  --nsg-name <nsg-name> \
  --resource-group <rg-name> \
  --name <rule-name>
```

### Useful Output Formats
```bash
# Table format (human-readable)
-o table

# JSON format (detailed, scriptable)
-o json

# YAML format (readable structured data)
-o yaml

# TSV format (tab-separated for parsing)
-o tsv

# Pipe to less for long output
| less
```

---

## Best Practices & Remediation

### How to Fix This Vulnerability

**Immediate Actions:**
1. **Delete the vulnerable rule:**
   ```bash
   az network nsg rule delete \
     --nsg-name nsg-production-eastus \
     --resource-group theneighborhood-rg1 \
     --name Allow-RDP-From-Internet
   ```

2. **Implement Azure Bastion:**
   - Deploy Azure Bastion to the virtual network
   - Access servers through Azure Portal
   - No public IPs required on VMs

3. **Alternative: IP Whitelisting** (if Bastion not available):
   ```bash
   az network nsg rule create \
     --nsg-name nsg-production-eastus \
     --resource-group theneighborhood-rg1 \
     --name Allow-RDP-From-Corporate \
     --priority 120 \
     --source-address-prefixes 203.0.113.0/24 \
     --destination-port-ranges 3389 \
     --access Allow
   ```

### Long-Term Security Improvements

**Network Segmentation:**
- Separate production, development, staging environments
- Use different virtual networks or subnets
- Implement network peering with proper routing

**Defense in Depth:**
- ✅ NSG rules (network layer)
- ✅ Windows Firewall (host layer)  
- ✅ Strong authentication (MFA)
- ✅ Regular patching
- ✅ Intrusion detection (Azure Sentinel)

**Monitoring and Alerting:**
- Enable NSG flow logs
- Configure alerts for rule changes
- Monitor failed RDP attempts
- Regular security reviews

**Infrastructure as Code:**
- Use ARM templates or Terraform
- Version control NSG configurations
- Automated security compliance checks
- Prevent manual misconfigurations

---

## Key Takeaways

1. **Never Expose Management Ports to Internet:**
   - RDP (3389) and SSH (22) should NEVER be 0.0.0.0/0
   - Use Azure Bastion, VPN, or private access methods
   - Even with strong passwords, it's a major risk

2. **Production Environments Need Extra Care:**
   - Apply strictest security controls
   - Regular audits and reviews
   - Principle of least privilege

3. **NSG Rules Are Critical Security Controls:**
   - Incorrect configuration = direct path to compromise
   - Priority and order matter
   - Always include default deny rules

4. **Azure Provides Secure Alternatives:**
   - Azure Bastion for secure RDP/SSH
   - Service tags for managed services
   - Just-in-Time (JIT) VM access

5. **Security Is About Layers:**
   - Don't rely on NSGs alone
   - Implement defense in depth
   - Multiple security controls reduce risk

---

## Challenge Complete! 🎉

**Status:** ✅ Completed  
**Critical Finding:** RDP port 3389 exposed to internet on production NSG  
**NSG:** nsg-production-eastus  
**Rule:** Allow-RDP-From-Internet  
**Severity:** **CRITICAL** - Immediate remediation required

### Lucas's Response

> Ha! 'Properly protected' they said. More like 'properly exposed to the entire internet'! Good catch, amigo.

---

## Additional Resources

- [Azure Network Security Groups Documentation](https://docs.microsoft.com/azure/virtual-network/network-security-groups-overview)
- [Azure Bastion Overview](https://docs.microsoft.com/azure/bastion/bastion-overview)
- [NSG Best Practices](https://docs.microsoft.com/azure/security/fundamentals/network-best-practices)
- [Azure Security Benchmark](https://docs.microsoft.com/security/benchmark/azure/)

---

*Challenge writeup by SFC David P. Collette*  
*Regional Cyber Center - Korea (RCC-K)*  
*SANS Holiday Hack Challenge 2025*
