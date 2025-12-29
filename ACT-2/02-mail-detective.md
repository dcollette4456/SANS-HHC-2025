# Mail Detective

**Difficulty**: ⭐⭐

---

Mail Detective

Difficulty: ⭐⭐

Challenge Overview

Help Mo from the Air Force investigate malicious JavaScript-enabled
emails sent by gnomes to the Dosis Neighborhood. All email clients have
been shut down for security, and the only safe way to access the IMAP
server is through curl.

![Mail Detective
Challenge](media/9b1060507ce9ee37e0c2f5d6ab2829aa49afe290.png "Challenge Screen"){width="5.958333333333333in"
height="3.9166666666666665in"}

Objective

Use curl to connect to the IMAP server and find the malicious email that
attempts to exfiltrate data to a pastebin service. Submit the URL of the
pastebin service.

Server Information

-   **IMAP Server:** localhost (127.0.0.1)

-   **Port:** 143 (IMAP)

-   **Username:** dosismail

-   **Password:** holidaymagic

Solution Walkthrough

Step 1: Initial Connection Test

First, let's test connectivity to the IMAP server:

curl -v imap://127.0.0.1:143

**Result:**

\* OK \[CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE
LITERAL+\...\]

Dovecot (Ubuntu) ready.

**Analysis:** Server is up and running Dovecot IMAP. The connection
works but we need to authenticate.

Step 2: Authenticate and List Mailboxes

Now let's login and see what mailboxes are available:

curl -v \--user dosismail:holidaymagic imap://127.0.0.1:143

**Result:**

![Available
mailboxes](media/ca1ad83cc6981d82b67bb3b4594f5e515158fa95.png "Mailbox Listing"){width="4.229166666666667in"
height="2.5729166666666665in"}

**Available Mailboxes:**

-   INBOX

-   Spam (suspicious - check here first!)

-   Sent

-   Archives

-   Drafts

Step 3: Check INBOX for Messages

curl \--user dosismail:holidaymagic imap://127.0.0.1:143 -X 'SELECT
INBOX'

**Result:**

![7 messages in
INBOX](media/1be03c11a08e9f4fd16f8078cff47a832ed48609.png "INBOX Messages"){width="1.1354166666666667in"
height="0.3645833333333333in"}

The INBOX has 7 messages. Let's search all folders to see where
messages are:

for folder in INBOX Spam Sent Archives Drafts; do

echo "=== Checking \$folder ==="

curl \--user dosismail:holidaymagic imap://127.0.0.1:143/\$folder -X
'SEARCH ALL'

echo ""

done

**Result:**

![Message counts in all
folders](media/d081a5c80a3f21bda2ba6156946385a30d0985d9.png "Folder Search"){width="2.3125in"
height="2.4270833333333335in"}

Step 4: Scan for Malicious Content

Let's scan the Spam folder (3 messages) for JavaScript and pastebin
references:

for i in {1..3}; do

echo "=== Spam Message \$i ==="

curl -s \--user dosismail:holidaymagic
"imap://127.0.0.1:143/Spam;MAILINDEX=\$i" \| grep -iE
"pastebin\|paste.ee\|dpaste\|javascript\|\<script"

echo ""

done

**Result:**

![Grep results showing pastebin
URL](media/c231a83043530391eaa20abcc6e8891d8eb5d8c7.png "Malicious Email Found"){width="6.3125in"
height="2.125in"}

**🎯 FOUND IT!** Spam Message 2 contains the malicious pastebin
exfiltration!

Step 5: View Complete Malicious Email

curl \--user dosismail:holidaymagic
'imap://127.0.0.1:143/Spam;MAILINDEX=2'

The Malicious Email

Email Headers

-   **From:** "Frozen Network Bot"
    \<frozen.network@mysterymastermind.mail\>

-   **To:** "Dosis Neighborhood Residents"
    \<dosis.residents@dosisneighborhood.mail\>

-   **Cc:** "Jessica and Joshua" \<siblings@dosisneighborhood.mail\>,
    "CHI Team" \<chi.team@counterhack.com\>

-   **Subject:** Frost Protocol: Dosis Neighborhood Freezing Initiative

-   **Date:** Mon, 16 Sep 2025 12:10:00 +0000

-   **Message-ID:** \<gnome-js-3@mysterymastermind.mail\>

Malicious JavaScript Analysis

The email contains embedded JavaScript with multiple malicious
functions:

1\. Crypto Mining Function

function initCryptoMiner() {

var worker = {

start: function() {

console.log("Frost's crypto miner started - mining FrostCoin\...");

}

};

}

**Purpose:** Mine cryptocurrency ("FrostCoin") using victim's
computer resources for the "perpetual winter fund".

2\. Data Exfiltration Function (CRITICAL)

function exfiltrateData() {

var sensitiveData = {

hvacSystems: "Located " + Math.floor(Math.random() \* 50) + " cooling
units",

thermostatData: "Temperature ranges: " + Math.floor(Math.random() \*
30 + 60) + "°F",

refrigerationUnits: "Found " + Math.floor(Math.random() \* 20) + "
commercial freezers"

};

var encodedData = btoa(JSON.stringify(sensitiveData));

// pastebin exfiltration

var pastebinUrl = "https://frostbin.atnas.mail/api/paste";

var exfilPayload = {

title: "HVAC_Survey\_" + Date.now(),

content: encodedData,

expiration: "1W",

private: "1",

format: "json"

};

}

**Purpose:** Steal HVAC system data, thermostat readings, and
refrigeration unit information, then exfiltrate via POST to pastebin
service.

**Target Data:**

-   HVAC cooling unit locations

-   Thermostat temperature data

-   Commercial freezer inventory

3\. Persistence Mechanism

function establishPersistence() {

if ('serviceWorker' in navigator) {

console.log("Attempting to register Frost's persistent service
worker\...");

}

localStorage.setItem("frost_persistence", JSON.stringify({

installDate: new Date().toISOString(),

version: "gnome_v2.0",

mission: "perpetual_winter_protocol"

}));

}

**Purpose:** Maintain persistent access through service workers and
localStorage to continue operations after initial infection.

The Answer

**Pastebin Exfiltration URL:**

**https://frostbin.atnas.mail/api/paste**

Easter Eggs Discovered

-   **"atnas.mail":** This is "Santa" spelled backwards! 🎅

-   **"FrostBin":** Holiday-themed play on "Pastebin"

-   **"FrostCoin":** Cryptocurrency for the "perpetual winter fund"

-   **Mission:** "perpetual_winter_protocol" - the gnomes are trying
    to keep the neighborhood frozen forever!

Technical Concepts Learned

IMAP Protocol

-   IMAP (Internet Message Access Protocol) keeps emails on the server

-   Port 143 is standard IMAP (unencrypted)

-   Port 993 is IMAPS (encrypted with SSL/TLS)

-   Dovecot is a popular open-source IMAP server

Curl with IMAP

-   Curl supports multiple protocols beyond HTTP (IMAP, FTP, SMTP, etc.)

-   Authentication: \--user username:password

-   URL format: imap://server:port/mailbox;MAILINDEX=N

-   Commands sent with -X flag

Email Security Threats

-   **JavaScript in emails:** Can execute malicious code when email
    client renders HTML

-   **Data exfiltration:** Stealing sensitive information and sending to
    attacker-controlled servers

-   **Pastebin services:** Often used for data exfiltration because
    they're public, free, and blend in with normal traffic

-   **Crypto mining:** Hijacking victim's computer resources to mine
    cryptocurrency

-   **Persistence:** Using service workers and localStorage to maintain
    access

Key Commands Reference

Essential Curl IMAP Commands

\# Connect and authenticate

curl \--user username:password imap://server:143

\# List mailboxes

curl \--user user:pass imap://server:143 -X 'LIST "" "\*"'

\# Search for all messages in folder

curl \--user user:pass imap://server:143/INBOX -X 'SEARCH ALL'

\# View specific message

curl \--user user:pass 'imap://server:143/INBOX;MAILINDEX=1'

\# Scan all messages for pattern

for i in {1..7}; do

curl -s \--user user:pass "imap://server/folder;MAILINDEX=\$i" \| grep
-i pattern

done

Challenge Complete! 🎄

**Status:** ✅ Completed

**Malicious Email Found:** Spam Message 2

**Pastebin URL:** https://frostbin.atnas.mail/api/paste

**Attack Type:** Data exfiltration, crypto mining, persistence

**Threat Actor:** Frost's Gnome Network (perpetual winter protocol)

*Thanks to Mo from the Air Force for the challenge! The neighborhood's
email is now secure! 🎖️*
