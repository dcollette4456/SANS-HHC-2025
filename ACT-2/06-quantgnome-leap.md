# Quantgnome Leap

**Difficulty**: ⭐⭐

---

Difficulty: ⭐⭐

## **Challenge Overview**

I just spotted a mysterious gnome - he winked and vanished, or maybe
he's still here? Things are getting strange, and I think we've
wandered into a quantum conundrum! If you help me unravel these riddles,
we might just outsmart future quantum computers.

![Challenge screenshot](media/image9.png){width="5.208333333333333in"
height="3.125in"}

## **Phase 1: Finding the PQC Key Generator**

The challenge begins with a cryptic message about quantum cryptography
and a hint that there's a PQC key generation program on the system.

![Challenge screenshot](media/image7.png){width="5.208333333333333in"
height="3.125in"}

### **Step 1: Locate the Program**

echo \$PATH

The PATH includes /opt/oqs-ssh/bin, suggesting this uses Open Quantum
Safe (OQS) SSH.

find /usr/local/bin -name "\*pqc\*" 2\>/dev/null

Result: /usr/local/bin/pqc-keygen

### **Step 2: Execute the Key Generator**

pqc-keygen

Output: --- Summary -\> Total algorithms = 28 \| ✔ Keys generated = 28

### **Step 3: View Key Characteristics**

pqc-keygen -t

This displays a table of all 28 generated cryptographic key pairs:

![Challenge screenshot](media/image2.png){width="6.25in"
height="3.75in"}

![Challenge screenshot](media/image11.png){width="4.114583333333333in"
height="1.3404407261592302in"}

![Challenge screenshot](media/image4.png){width="6.25in"
height="3.75in"}

## **Phase 2: Understanding the Challenge**

The table shows three types of keys:

• Classical: Traditional algorithms (RSA, Ed25519) - vulnerable to
quantum computers

• PQC: Pure Post-Quantum Cryptography (SPHINCS+, Falcon, ML-DSA, MAYO)

• Hybrid: Combines classical + PQC for 'quantum agility'

NIST Security Levels:

• 0: Not NIST-standardized

• 1: Security equivalent to AES-128

• 3: Security equivalent to AES-192

• 5: Security equivalent to AES-256 (strongest)

## **Phase 3: Finding the Server Keys**

Attempting to SSH with our generated keys fails - the server expects
specific pre-registered keys.

![Challenge screenshot](media/image3.png){width="3.6875in"
height="1.1156681977252842in"}

### **Discovering User Keys**

ls -la /opt/oqs-ssh/user-keys/

Found public keys for: gnome1, gnome2, gnome3, gnome4, and admin

![Challenge screenshot](media/image12.png){width="6.25in"
height="3.75in"}

Key types identified:

• gnome1: ssh-rsa (Classical RSA)

• gnome2: ssh-ed25519 (Classical Ed25519)

• gnome3: ssh-mayo2 (Pure PQC - MAYO)

• gnome4: ssh-ecdsa-nistp256-sphincssha2128fsimple (Hybrid PQC)

• admin: ssh-ecdsa-nistp521-mldsa-87 (Maximum security hybrid)

## **Phase 4: Authentication Chain**

### **Gnome1 - Classical RSA**

Using the RSA key from \~/.ssh/:

ssh -i \~/.ssh/id_rsa gnome1@pqc-server.com

SUCCESS! Authenticated with classical RSA.

![Challenge screenshot](media/image10.png){width="6.25in"
height="2.494792213473316in"}

The welcome message explains that RSA is vulnerable to Shor's algorithm
on quantum computers.

### **Gnome2 - Classical Ed25519**

Found Ed25519 key in gnome1's \~/.ssh/ directory:

ssh -i \~/.ssh/id_ed25519 gnome2@localhost

SUCCESS! Ed25519 is smaller than RSA but still vulnerable to quantum
attacks.

### **Gnome3 - Pure PQC (MAYO)**

Gnome2 has the MAYO2 key needed for gnome3:

ssh -i \~/.ssh/id_mayo2 gnome3@localhost

![Challenge screenshot](media/image6.png){width="6.25in"
height="2.390651793525809in"}

MAYO is a post-quantum algorithm designed for embedded systems, but not
yet NIST-standardized.

### **Gnome4 - Hybrid PQC (ECDSA + SPHINCS+)**

Gnome3 has the hybrid ECDSA-SPHINCS key:

ssh -i \~/.ssh/id_ecdsa_nistp256_sphincssha2128fsimple gnome4@localhost

![Challenge screenshot](media/image5.png){width="6.25in"
height="3.1788199912510935in"}

This hybrid key combines:

• Classical: ECDSA on NIST P-256 curve

• PQC: SPHINCS+ (standardized as SLH-DSA)

• Security Level: 1 (equivalent to AES-128)

Both signatures must be valid for authentication to succeed, providing
protection against both classical and quantum attacks.

### **Admin - Maximum Security (ECDSA P-521 + ML-DSA-87)**

Gnome4 has the strongest hybrid key:

ssh -i \~/.ssh/id_ecdsa_nistp521_mldsa87 admin@localhost

![Challenge screenshot](media/image1.png){width="6.25in"
height="3.75in"}

This is the strongest available hybrid key, combining:

• Classical: ECDSA on NIST P-521 (equivalent to 15360-bit RSA)

• PQC: ML-DSA-87 (NIST-standardized, Security Level 5)

• Security: Equivalent to AES-256

ML-DSA (Module-Lattice-Based Digital Signature Algorithm) security
levels:

• ML-DSA-44: Level 2 (SHA-256 equivalent)

• ML-DSA-65: Level 3 (AES-192 equivalent)

• ML-DSA-87: Level 5 (AES-256 equivalent) ← Strongest!

## **Phase 5: Retrieving the Flag**

The admin account has access to /opt/oqs-ssh/flag/:

ls -la /opt/oqs-ssh/flag/

cat /opt/oqs-ssh/flag/\*

![Challenge screenshot](media/image8.png){width="6.25in"
height="1.5260422134733158in"}

**FLAG: HHC{L3aping_0v3r_Quantum_Crypt0}**

## **Key Concepts Learned**

### **1. Post-Quantum Cryptography (PQC)**

Why PQC?

• Shor's Algorithm: Quantum computers can break RSA and ECC efficiently

• Current systems: All classical cryptography is vulnerable

• Timeline: Large-scale quantum computers may exist within 10-20 years

PQC Approaches:

• Lattice-based: ML-DSA (CRYSTALS-Dilithium), Falcon

• Hash-based: SPHINCS+ (SLH-DSA)

• Emerging: MAYO (efficient but not yet standardized)

### **2. NIST PQC Standardization**

NIST Selected Algorithms (FIPS 204-205):

• ML-DSA (FIPS 204): Digital signatures, from CRYSTALS-Dilithium

• SLH-DSA (FIPS 205): Digital signatures, from SPHINCS+

• ML-KEM (FIPS 203): Key encapsulation, from CRYSTALS-Kyber

### **3. Hybrid Cryptography**

Why Hybrid?

• Combines classical (proven) + PQC (quantum-resistant)

• Both signatures must succeed for authentication

• Provides 'quantum agility' during transition

• Protected against failures in either component

### **4. Open Quantum Safe (OQS) Project**

This challenge uses the Linux Foundation's OQS initiative:

• liboqs: C library providing PQC algorithm implementations

• OQS-SSH: Modified OpenSSH with PQC support

• Website: https://openquantumsafe.org/

## **Authentication Chain Summary**

qgnome (local system)

↓ (Classical RSA key)

gnome1@pqc-server

↓ (Classical Ed25519 key)

gnome2@pqc-server

↓ (Pure PQC - MAYO2)

gnome3@pqc-server

↓ (Hybrid - ECDSA + SPHINCS+, Level 1)

gnome4@pqc-server

↓ (Hybrid - ECDSA P-521 + ML-DSA-87, Level 5)

admin@pqc-server

↓

FLAG: HHC{L3aping_0v3r_Quantum_Crypt0}

## **Key Takeaways**

1\. PQC Transition: The move to post-quantum cryptography is underway

2\. Multiple Algorithms: Different PQC algorithms for different use
cases

3\. Hybrid Approach: Best practice combines classical + PQC

4\. NIST Standards: Follow FIPS 204-205 for standardized algorithms

5\. 'Harvest Now, Decrypt Later': Adversaries are collecting encrypted
data today to decrypt with future quantum computers

## **Challenge Complete!**

**✓ Status: Completed**

*Category: Post-Quantum Cryptography, SSH Authentication*
