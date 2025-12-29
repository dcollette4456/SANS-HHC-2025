# IDORable Bistro

**Difficulty**: ⭐⭐

---

**SANS Holiday Hack Challenge 2025**

**Act 2: IDORable Bistro**

*Challenge Write-up*

Challenge Overview

**Difficulty:** ⭐⭐ (2/5)

The IDORable Bistro challenge introduces players to IDOR (Insecure
Direct Object Reference) vulnerabilities through a restaurant receipt
verification system. A gnome disguised as a human visited Sasabune
restaurant and ordered frozen sushi. Our task is to exploit the IDOR
vulnerability to unmask the gnome's true identity.

![](media/bf49b35428b9a8629d2aaa97dea588397b0debe3.undefined){width="5.208333333333333in"
height="3.6458333333333335in"}

Figure 1: Challenge briefing page

Challenge Description

*From the challenge briefing:*

> *"A gnome came through Sasabune today, poorly disguising itself as
> human - apparently asking for frozen sushi, which is almost as
> terrible as that fusion disaster I had to endure that one time. Based
> on my previous work finding IDOR bugs in restaurant payment systems, I
> suspect we can exploit a similar vulnerability here."*

Initial Reconnaissance

Examining the Web Interface

Upon accessing the challenge URL, we discovered a receipt verification
system for Sasabune restaurant. The main page displayed a QR code
scanner interface instructing users to scan receipt QR codes to view
order details.

![](media/5cbc482f8c831d6bab7e6d67e4424eb2fe142902.undefined){width="4.6875in"
height="4.166666666666667in"}

Figure 2: Sasabune receipt verification system main page

Key findings from the HTML source code revealed a commented-out testing
section:

\<!\-- For testing purposes only \--\>

\<li\>\<a href="/receipt/a1b2c3d4"\>Sample Receipt\</a\>\</li\>

This revealed the URL structure for accessing receipts:
/receipt/\[8-character-code\]

API Endpoint Discovery

Accessing the sample receipt (/receipt/a1b2c3d4) revealed receipt #101
for Duke Dosis:

![](media/2b29f29642f12df33dda45e628926d468c8a682c.undefined){width="5.208333333333333in"
height="4.166666666666667in"}

Figure 3: Receipt #101 - Duke Dosis

Examining the page source revealed JavaScript code showing the internal
API structure:

![](media/01b18e1d8d2d0b428c986e34bff34e3034a4ba63.undefined){width="5.729166666666667in"
height="3.125in"}

Figure 4: Browser DevTools showing the JavaScript API calls

let receiptId = '101';

fetch(\`/api/receipt?id=\${id}\`)

This revealed a critical IDOR vulnerability: the API accepts any receipt
ID as a query parameter without authentication, allowing us to view any
customer's receipt.

Exploitation

Receipt Enumeration

We developed a Python script to enumerate receipts through the API
endpoint:

base_url = "https://its-idorable.holidayhackchallenge.com/api/receipt"

for receipt_id in range(100, 200):

response = requests.get(f"{base_url}?id={receipt_id}")

The enumeration script successfully retrieved receipts for IDs 100-152,
revealing various customer orders with detailed information including
customer names, items ordered, prices, and notes.

Identifying the Suspicious Receipt

Receipt #139 immediately stood out as suspicious:

![](media/cabcede0ec1dd071bea9775857d04678f5e41440.undefined){width="5.208333333333333in"
height="2.6041666666666665in"}

Figure 5: Receipt #139 JSON response from API

![](media/c040277400b11c9b751921971b42f39e201930f4.undefined){width="5.208333333333333in"
height="4.166666666666667in"}

Figure 6: Receipt #139 rendered in browser

  ----------------------------------- -----------------------------------
  **Field**                           **Value**

  Receipt ID                          139

  Customer                            **Bartholomew Quibblefrost**

  Date                                2025-12-20

  Table                               14

  Items                               Frozen Roll (waitress improvised:
                                      sorbet, a hint of dry ice)

  Total                               \$19.00

  Note                                Insisted on increasingly bizarre
                                      rolls and demanded one be served
                                      frozen. The waitress invented a
                                      'Frozen Roll' on the spot with
                                      sorbet and a puff of theatrical
                                      smoke. He nodded solemnly and asked
                                      if we could make these in bulk.
  ----------------------------------- -----------------------------------

The customer name "Bartholomew Quibblefrost" clearly sounds
gnome-like, and the order for "Frozen Roll" (frozen sushi) matches the
challenge description perfectly.

Technical Analysis

IDOR Vulnerability Explanation

**What is IDOR?**

IDOR (Insecure Direct Object Reference) is an access control
vulnerability where an application exposes references to internal
objects (such as database keys, filenames, or IDs) without proper
authorization checks.

**The Vulnerability in Sasabune:**

The restaurant's receipt system commits two critical security errors:

> **1. Predictable IDs:** Receipt IDs are sequential integers (101, 102,
> 103\...) making them easy to enumerate.
>
> **2. No Authorization Checks:** The API endpoint /api/receipt?id=X
> returns receipt data for ANY valid ID without verifying if the
> requester is authorized to view it.

**Real-World Impact:**

In a real restaurant system, this vulnerability would allow attackers
to:

> • View other customers' orders, names, and payment information
>
> • Gather business intelligence (sales data, popular items, customer
> demographics)
>
> • Potentially commit identity theft or fraud
>
> • Violate privacy regulations (GDPR, CCPA)

Alternative Approaches Explored

During the investigation, we explored several approaches before finding
the solution:

**1. QR Code Pattern Analysis:**

> We found QR codes on receipts in the game map. We discovered that
> receipt URLs used 8-character codes (like /receipt/a1b2c3d4):

![](media/62038f5cc640cbca8563874a6a8306889cac258e.undefined){width="3.125in"
height="4.6875in"}

Figure 7: Receipt with QR code found on the game map

> We attempted to reverse-engineer the pattern:
>
> • Receipt 101: a1b2c3d4
>
> • Receipt 103: i9j0k1l2
>
> We developed an algorithm to calculate that receipt 139 should be
> w3x4y5z6, but this URL returned a 404 error, suggesting the codes may
> not follow a purely mathematical pattern.

**2. Secret Note Investigation:**

> The JavaScript code referenced a secret_note field that would display
> if present, suggesting some receipts might contain hidden information.
> However, receipt 139 accessed via the API did not contain this field.

**3. Parameter Injection Testing:**

> We tested various query parameters (admin=true, debug=true,
> show_all=true, etc.) attempting to reveal hidden fields, but none
> successfully modified the API response.

Solution

The challenge objective was to identify the gnome's name. Through API
enumeration, we discovered receipt #139 belonged to a customer named
**Bartholomew Quibblefrost**, who ordered frozen sushi - exactly
matching the behavior described in the challenge.

**Answer: Bartholomew Quibblefrost**

Lessons Learned

**1. Read the Question Carefully:**

> We spent significant time exploring advanced attack vectors when the
> challenge simply asked for the customer's name. Always verify what
> information is actually required before diving deep into exploitation.

**2. API Endpoints Are Often Less Protected:**

> While the web interface required 8-character codes, the underlying API
> accepted simple numeric IDs. APIs are often less protected than web
> UIs, making them prime targets for IDOR exploitation.

**3. Enumeration is Powerful:**

> Sequential ID enumeration remains one of the most effective techniques
> for discovering IDOR vulnerabilities. Simple Python scripts can
> automate this process efficiently.

**4. Source Code Reveals Architecture:**

> Client-side JavaScript often reveals API endpoints, data structures,
> and application logic. Always examine page source and JavaScript files
> during reconnaissance.

Security Remediation Recommendations

To fix this vulnerability, Sasabune should implement:

**1. Authentication and Authorization:**

> Require users to authenticate and verify they own the receipt before
> returning data. Implement session-based access control that validates
> receipt ownership.

**2. Non-Sequential Identifiers:**

> Use UUIDs or cryptographically random identifiers instead of
> sequential integers. This makes enumeration impractical.

**3. Rate Limiting:**

> Implement rate limiting on API endpoints to prevent mass enumeration
> attacks. Detect and block suspicious patterns of sequential ID
> requests.

**4. Indirect References:**

> Map internal database IDs to session-specific temporary tokens. Users
> receive tokens that only work for their session, preventing direct
> database ID exposure.

Tools and Scripts Used

**1. Python with Requests Library:**

> Used for automated receipt enumeration and API testing

**2. Browser Developer Tools:**

> Used for examining JavaScript, network requests, and testing API calls
> directly from the console

**3. QR Code Scanner:**

> Used OpenCV and PIL in Python to decode QR codes from receipt images
> found on the game map

Conclusion

The IDORable Bistro challenge effectively demonstrated how IDOR
vulnerabilities arise from inadequate access control and predictable
resource identifiers. By exploiting the ability to enumerate receipt IDs
through an unprotected API endpoint, we successfully identified the
gnome customer Bartholomew Quibblefrost. This challenge reinforces the
importance of implementing proper authorization checks, using
non-sequential identifiers, and protecting all API endpoints - not just
user-facing web interfaces.

While we explored numerous advanced exploitation techniques during the
solve process, the actual solution was straightforward: enumerate the
API, find the suspicious customer. This serves as a valuable reminder to
always verify what the challenge is actually asking for before pursuing
complex attack vectors.
