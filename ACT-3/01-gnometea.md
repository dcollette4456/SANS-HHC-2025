# GnomeTea - Firebase Security Misconfiguration

**Difficulty:** ⭐⭐⭐

**SANS Holiday Hack Challenge 2025 - Act 3**

---


# Challenge Overview

GnomeTea is a social network for gnomes featuring Firebase/Firestore
backend. The challenge requires exploiting security misconfigurations to
access a secret passphrase stored in a protected admin collection. This
write-up documents our complete investigation, successful data
extraction, and the authentication barrier we encountered.

<img src="../images/act3/image9.png"
style="width:5.20833in;height:4.16667in"
alt="Failed login attempt showing credentials no longer work" />

*Figure 1: Authentication failure - test credentials disabled*

# Phase 1: Initial Reconnaissance

## Challenge Entry Point

The challenge begins at the GnomeTea login page. Browser DevTools
network inspection immediately revealed the Firebase configuration
endpoint.

<img src="../images/act3/image8.png"
style="width:5.72917in;height:3.64583in"
alt="GnomeTea login interface" />

*Figure 2: GnomeTea login page - initial access point*

## Firebase Configuration Discovery

Opening Browser DevTools and examining network requests revealed
Firebase initialization:

GET https://gnometea.web.app/\_\_/firebase/init.json

<img src="../images/act3/image2.png"
style="width:5.20833in;height:2.60417in"
alt="Firebase configuration in network tab" />

*Figure 3: Firebase configuration exposed via init.json endpoint*

**Key Configuration:**

{ "apiKey": "AIzaSyDx0DEPz2rKo4bPEFFjXjIqERfJrCEGUiw", "authDomain":
"holidayhack2025.firebaseapp.com", "projectId": "holidayhack2025",
"storageBucket": "holidayhack2025.firebasestorage.app"}

## HTML Source Code Analysis

Examining the page source revealed commented-out test credentials and
security TODO items:

<img src="../images/act3/image1.png"
style="width:5.72917in;height:3.125in"
alt="Test credentials in HTML comments" />

*Figure 4: Test account credentials found in HTML comments*

\<!-- Test account: gnome@gnomemail.dosis --\>\<!-- TODO: lock down dms,
tea, gnomes collections --\>

**Critical Intelligence Gathered:**

- Test email: gnome@gnomemail.dosis

- Collections requiring lockdown: dms, tea, gnomes

- **Security misconfiguration confirmed**

# Phase 2: Firestore Database Exploitation

## Browser Console Access

Using the Firebase JavaScript SDK directly in the browser console, we
accessed unsecured Firestore collections:

<img src="../images/act3/image6.png"
style="width:5.72917in;height:2.08333in"
alt="Firebase SDK in browser console" />

*Figure 5: Direct Firestore access via browser console*

// Initialize Firebase (config from init.json)firebase.initializeApp({
apiKey: "AIzaSyDx0DEPz2rKo4bPEFFjXjIqERfJrCEGUiw", projectId:
"holidayhack2025"});const db = firebase.firestore();// Query unsecured
collectionsconst gnomes = await db.collection('gnomes').get();const dms
= await db.collection('dms').get();const tea = await
db.collection('tea').get();

<img src="../images/act3/image20.png"
style="width:5.72917in;height:4.16667in"
alt="Successfully retrieved Firestore documents" />

*Figure 6: Successfully retrieved all documents from unsecured
collections*

## Collections Successfully Accessed

| **Collection** | **Documents** | **Data Exposed**                       |
|----------------|---------------|----------------------------------------|
| gnomes         | 26            | User profiles, emails, locations, bios |
| dms            | 15            | Private conversations, password hints  |
| tea            | 38            | Social posts, public messages          |

## The Admin Collection Discovery

Analysis of the minified JavaScript revealed references to an 'admins'
collection containing the secret:

<img src="../images/act3/image12.png"
style="width:5.72917in;height:2.08333in"
alt="Admins collection in JavaScript" />

*Figure 7: JavaScript bundle reveals admins/secret_operations document*

const \$ = Yf(er,"admins","secret_operations"),H = await
ap(\$);H.exists() && ( l(H.data()), console.log("🔓 Secret data
loaded:", H.data()))

**Critical Finding:** The passphrase is NOT in the gnomes collection -
it's in **admins/secret_operations**!

## Security Rules - The Authentication Barrier

Attempting to access the admins collection directly:

<img src="../images/act3/image17.png"
style="width:5.72917in;height:2.08333in"
alt="Firestore permission error" />

*Figure 8: Permission denied when accessing admin collection*

const admin = await db.collection('admins')
.doc('secret_operations').get();// Error: Missing or insufficient
permissions

# Phase 3: Credential Discovery via DMs

## DM Data Extraction

Analyzing the DM conversations revealed password security discussions:

<img src="../images/act3/image3.png"
style="width:5.72917in;height:4.16667in"
alt="Direct messages extracted" />

*Figure 9: DM conversations containing credential hints*

## The Critical Password Hint

Found in conversation between Barnaby Briefcase and Glitch Mitnick:

<img src="../images/act3/image19.png"
style="width:5.72917in;height:3.125in"
alt="Barnaby reveals password hint" />

*Figure 10: Barnaby Briefcase reveals his password is his hometown*

\[2025-09-30\] Barnaby Briefcase:"My password is actually the name of my
hometown that I grew up in. I actually just visited there back when I
signed up with my id to GnomeTea (I took my picture of my id
there)."\[2025-09-30\] Glitch Mitnick:"Barnaby... we need to talk about
password security. 😅"

**Credentials Identified:**

- **Email: barnabybriefcase@gnomemail.dosis**

- **Password: \[childhood hometown name\]**

- Location visible on driver's license photo

## Barnaby's Profile Analysis

<img src="../images/act3/image13.png"
style="width:5.72917in;height:2.22473in"
alt="Barnaby&#39;s gnome profile" />

*Figure 11: Barnaby Briefcase's profile with driver's license URL*

{ "uid": "l7VS01K9GKV5ir5S8suDcwOFEpp2", "name": "Barnaby Briefcase",
"email": "barnabybriefcase@gnomemail.dosis", "homeLocation": "Gnomewood
Grove, Dosis Neighborhood", "driversLicenseUrl":
"https://storage.googleapis.com/
holidayhack2025.firebasestorage.app/gnome-documents/
l7VS01K9GKV5ir5S8suDcwOFEpp2_drivers_license.jpeg"}

**Important:** homeLocation shows his <u>current</u> address, NOT his
childhood hometown (which is the password)!

# Phase 4: The Firebase Storage Barrier

## Storage Access Attempt

Attempting to access Barnaby's driver's license image:

<img src="../images/act3/image15.png"
style="width:3.98393in;height:3.07244in"
alt="Access denied to driver&#39;s license" />

*Figure 12: HTTP 403 Forbidden - Firebase Storage properly secured*

curl https://storage.googleapis.com/holidayhack2025.firebasestorage.app/
gnome-documents/l7VS01K9GKV5ir5S8suDcwOFEpp2_drivers_license.jpegHTTP/1.1
403 ForbiddenContent-Type: application/xml\<Error\>
\<Code\>AccessDenied\</Code\> \<Message\>Access
denied.\</Message\>\</Error\>

## Other Gnomes' Licenses - Comparison

Some gnomes' licenses were accessible (different permission levels):

<img src="../images/act3/image10.png"
style="width:5.72917in;height:4.16667in"
alt="Example accessible driver&#39;s license" />

*Figure 13: Titus Toadstool's license showing current address format*

**Observation:** Other licenses show **current address**, not
birthplace/hometown. This suggests Barnaby's license may have been
specifically protected because it contained his password.

# Phase 5: Automated Data Extraction

## Python Extraction Scripts

Created comprehensive scripts to automate data extraction:

<img src="../images/act3/image4.png"
style="width:5.72917in;height:2.60417in"
alt="Python data extraction script" />

*Figure 14: Python script for comprehensive Firebase data extraction*

### Script Features

- Dumps all accessible Firestore collections via REST API

- Tests protected collections (admins, secret, config)

- Downloads images from discovered URLs

- Parses Firestore's nested field format

- Creates individual conversation text files

- Searches for password-related keywords

<img src="../images/act3/image16.png"
style="width:5.72917in;height:2.08333in"
alt="Extraction script results" />

*Figure 15: Script successfully extracted all accessible data*

# Phase 6: Attempted Workarounds

## Approach 1: Test Account Authentication

Attempted to use test credentials to gain authenticated access:

<img src="../images/act3/image11.png"
style="width:5.72917in;height:4.16667in"
alt="Failed login with test credentials" />

*Figure 16: Test credentials disabled - authentication failed*

**Result:** Firebase returned 'auth/invalid-credential' - test account
has been disabled.

## Approach 2: GitHub Repository Search

Searched the challenge GitHub repository for extracted images:

<img src="../images/act3/image14.png"
style="width:5.72917in;height:3.64583in"
alt="Searching GitHub repository" />

*Figure 17: GitHub repository search for image files*

**Result:** Found other licenses but Barnaby's specific license was not
included in the repository.

## Approach 3: Password Guessing

Compiled list of gnome-themed town names based on game world:

<img src="../images/act3/image7.png"
style="width:5.72917in;height:3.64583in"
alt="Potential password candidates" />

*Figure 18: Compiled list of potential hometown names*

**Candidate Passwords:**

- Toadstoolton (from Titus's area)

- Mushroomshire, Sporesbury, Capville

- Gnomewood, Gnomeville, Gnometon

- Briefcaseton (surname-based)

- Corporateville (personality-based)

**Result:** Too many possibilities without additional context.
Systematic guessing impractical.

# Vulnerability Analysis

## Root Cause: Firestore Security Rules Misconfiguration

<img src="../images/act3/image5.png"
style="width:4in;height:2.00521in" alt="Firestore security rules" />

*Figure 19: Comparison of vulnerable vs. secure Firestore rules*

The vulnerability stems from overly permissive Firestore Security Rules:

// VULNERABLE CONFIGURATIONrules_version = '2';service cloud.firestore {
match /databases/{database}/documents { // ❌ INSECURE - Allows
unauthenticated read match /gnomes/{document} { allow read: if true; }
match /dms/{document} { allow read: if true; } match /tea/{document} {
allow read: if true; } // ✅ SECURE - Requires authentication match
/admins/{document} { allow read: if request.auth != null; } }}

## Attack Vector Diagram

**Attack Flow:**

1.  Firebase API key discovered via /\_\_/firebase/init.json

2.  Project ID identified (holidayhack2025)

3.  **No authentication required for sensitive collections**

4.  Direct database queries via Firebase SDK

5.  Credential hints discovered in DMs

6.  Password format identified (hometown name)

7.  **BLOCKED: Storage properly secured**

## Security Impact Assessment

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Data Exposed</strong></th>
<th><strong>Data Protected</strong></th>
</tr>
<tr class="odd">
<th><ul>
<li><blockquote>
<p>User profiles (26 gnomes)</p>
</blockquote></li>
<li><blockquote>
<p>Email addresses</p>
</blockquote></li>
<li><blockquote>
<p>Private DMs (15 conversations)</p>
</blockquote></li>
<li><blockquote>
<p>Password hints</p>
</blockquote></li>
<li><blockquote>
<p>Social posts (38 messages)</p>
</blockquote></li>
</ul></th>
<th><ul>
<li><blockquote>
<p>Admin collection data</p>
</blockquote></li>
<li><blockquote>
<p>Secret passphrase</p>
</blockquote></li>
<li><blockquote>
<p>Driver's license images</p>
</blockquote></li>
<li><blockquote>
<p>Authenticated Storage files</p>
</blockquote></li>
</ul></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# Current Status and Blockers

<img src="../images/act3/image18.png"
style="width:5.72917in;height:3.125in"
alt="Challenge progress summary" />

*Figure 20: Current progress - stuck at authentication barrier*

## What We Successfully Accomplished

- ✓ Discovered Firebase configuration

- ✓ Exploited unsecured Firestore collections

- ✓ Extracted 26 user profiles, 15 DM conversations, 38 posts

- ✓ Identified passphrase location: admins/secret_operations

- ✓ Found credential hint in Barnaby's DMs

- ✓ Determined password format (hometown name)

- ✓ Located driver's license URL

## What We're Missing

- **✗ Cannot view Barnaby's driver's license (403 Forbidden)**

- **✗ License would show hometown = password**

- ✗ Firebase Storage properly secured (requires auth)

- ✗ Test credentials disabled

- ✗ No birthplace field in database

## The Authentication Catch-22

We encountered a circular dependency:

8.  Need Barnaby's password → to authenticate → to access admin data

9.  Password is his hometown name

10. Hometown shown on driver's license

11. **Cannot access license without authentication**

# Lessons Learned

## Technical Skills Demonstrated

- Firebase/Firestore security rule analysis

- Client-side NoSQL database exploitation

- REST API enumeration and data extraction

- OSINT through social engineering (DM analysis)

- Python scripting for automated reconnaissance

- Understanding defense-in-depth security

## Security Best Practices Learned

- **Never use 'allow read: if true' in production**

- Implement authentication for all sensitive collections

- Use defense-in-depth (multiple security layers)

- Don't share password hints in unsecured messages

- Regularly audit and remove test accounts

- Store sensitive documents with proper access controls

# Conclusion

This challenge effectively demonstrates a realistic Firebase security
misconfiguration scenario. We successfully exploited overly permissive
Firestore rules to access user data and identify the authentication
pathway. The investigation revealed:

12. **The primary vulnerability:** Firestore collections lacking
    > authentication requirements

13. **The exploitation path:** Direct database access via Firebase SDK

14. **The intelligence gathered:** Valid credentials and password format

15. **The barrier encountered:** Well-designed Storage security
    > preventing document access

While incomplete, this investigation demonstrates the importance of:

- Proper Firestore Security Rules configuration

- Defense-in-depth security architecture

- Secure credential management practices

- Thorough security audits and testing

**CHALLENGE STATUS: INCOMPLETE**

*Unable to access Barnaby Briefcase's driver's license image*

*Additional information required to determine password*

# Appendix: Technical Resources

## Key URLs and Endpoints

- **Challenge URL:** https://gnometea.web.app/login

- **Firebase Config:** https://gnometea.web.app/\_\_/firebase/init.json

- **Project ID:** holidayhack2025

- **Storage Bucket:** holidayhack2025.firebasestorage.app

- **GitHub Repo:** https://github.com/gmanctf/2025-HHC

## Created Analysis Scripts

16. **gnometea_complete_extractor.py** - Comprehensive data extraction
    > from all accessible collections

17. **analyze_data.py** - DM analysis and credential discovery tool

18. **find_barnaby_license.py** - License URL locator and access tester

## Extracted Data Summary

| **Data Type**    | **Quantity** | **Format**           |
|------------------|--------------|----------------------|
| Gnome Profiles   | 26           | JSON (gnomes.json)   |
| DM Conversations | 15           | JSON + TXT files     |
| Social Posts     | 38           | JSON (tea.json)      |
| Avatar Images    | 12           | PNG/JPG files        |
| License Images   | 3            | JPG (partial access) |

*--- End of Write-Up ---*

*Total Pages: 20+ \| Total Screenshots: 20 \| Challenge Status:
INCOMPLETE*
