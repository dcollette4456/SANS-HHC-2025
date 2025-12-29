# Going in Reverse

**Difficulty**: ⭐⭐

---

**Difficulty:** ⭐⭐

# Challenge Overview

Help Kevin analyze a mysterious Commodore 64 BASIC program found on an
old 5.25" floppy disk. The program contains an encrypted password and
flag that need to be reverse engineered.

## Kevin

*Hello, I'm Kevin (though past friends have referred to me as 'Heavy
K')*

Kevin is a philosophy graduate with diverse interests including Amateur
Astronomy, Shortwave Radio, and retro-gaming. He's particularly
fascinated by vintage computing artifacts like the Commodore 64.

*"Finding an old Commodore 64 disk with a mysterious BASIC program on
it? That's like discovering a digital time capsule. The C64 was an
incredible machine for its time - 64KB of RAM seemed like an ocean of
possibility back then."*

# The BASIC Program

The challenge presents a Commodore 64 BASIC security program:

10 REM \*\*\* COMMODORE 64 SECURITY SYSTEM \*\*\*

20 ENC_PASS\$ = "D13URKBT"

30 ENC_FLAG\$ = "DSA\|auhts\*wkfi=dhjwubtthut+dhhkfis+hnkz"

40 INPUT "ENTER PASSWORD: "; PASS\$

50 IF LEN(PASS\$) \<\> LEN(ENC_PASS\$) THEN GOTO 90

60 FOR I = 1 TO LEN(PASS\$)

70 IF CHR\$(ASC(MID\$(PASS\$,I,1)) XOR 7) \<\> MID\$(ENC_PASS\$,I,1)
THEN GOTO 90

80 NEXT I

85 FLAG\$ = "" : FOR I = 1 TO LEN(ENC_FLAG\$) : FLAG\$ = FLAG\$ +
CHR\$(ASC(MID\$(ENC_FLAG\$,I,1)) XOR 7) : NEXT I : PRINT FLAG\$

90 PRINT "ACCESS DENIED"

100 END

# Reverse Engineering Analysis

## Step 1: Understanding the Encryption

The key to solving this challenge is understanding the XOR encryption
used in lines 70 and 85:

70 IF CHR\$(ASC(MID\$(PASS\$,I,1)) XOR 7) \<\> MID\$(ENC_PASS\$,I,1)

85 FLAG\$ = FLAG\$ + CHR\$(ASC(MID\$(ENC_FLAG\$,I,1)) XOR 7)

**How the encryption works:**

-   Each character is XORed with the value 7

-   XOR is reversible: A XOR B XOR B = A

-   To decrypt: encrypted_char XOR 7 = original_char

-   The same XOR 7 operation both encrypts AND decrypts

## Step 2: Decrypting the Password

Line 20 contains the encrypted password:

ENC_PASS\$ = "D13URKBT"

Applying XOR 7 to each character:

  -----------------------------------------------------------------------
  **Position**      **Encrypted**     **ASCII**         **Decrypted**
  ----------------- ----------------- ----------------- -----------------
  1                 D                 68 XOR 7 = 67     **C**

  2                 1                 49 XOR 7 = 54     **6**

  3                 3                 51 XOR 7 = 52     **4**

  \...              \...              \...              \...
  -----------------------------------------------------------------------

**✓ DECRYPTED PASSWORD: C64RULES**

## Step 3: Decrypting the Flag

Line 30 contains the encrypted flag:

ENC_FLAG\$ = "DSA\|auhts\*wkfi=dhjwubtthut+dhhkfis+hnkz"

Line 85 shows how the flag is decrypted once the correct password is
entered - using the same XOR 7 operation:

FLAG\$ = FLAG\$ + CHR\$(ASC(MID\$(ENC_FLAG\$,I,1)) XOR 7)

Applying XOR 7 to the first few characters as demonstration:

  ----------------------------------------------------------------------------
  **Position**   **Encrypted**   **ASCII**      **XOR 7**      **Decrypted**
  -------------- --------------- -------------- -------------- ---------------
  1              D               68             67             **C**

  2              S               83             84             **T**

  3              A               65             70             **F**

  4              \|              124            123            **{**

  \...           \...            \...           \...           \...
  ----------------------------------------------------------------------------

**✓ DECRYPTED FLAG: CTF{frost-plan:compressors,coolant,oil}**

# Python Solution Script

Here's the complete Python script used to reverse engineer the program:

#!/usr/bin/env python3

\# Encrypted values from the BASIC program

ENC_PASS = "D13URKBT"

ENC_FLAG = "DSA\|auhts\*wkfi=dhjwubtthut+dhhkfis+hnkz"

\# Decrypt password using XOR 7

password = ""

for char in ENC_PASS:

password += chr(ord(char) \^ 7)

print(f"Password: {password}")

\# Decrypt flag using XOR 7

flag = ""

for char in ENC_FLAG:

flag += chr(ord(char) \^ 7)

print(f"Flag: {flag}")

# Technical Concepts Learned

## XOR Encryption

-   XOR (Exclusive OR) is a bitwise operation

-   XOR is its own inverse: A XOR B XOR B = A

-   Simple XOR encryption is easily reversible if you know the key

-   In this case, the key is 7 (a single byte)

## BASIC String Functions

-   **MID\$(string, position, length)** - Extracts substring

-   **ASC(character)** - Returns ASCII value

-   **CHR\$(number)** - Converts ASCII value to character

-   **LEN(string)** - Returns string length

## Commodore 64 History

-   Released in 1982, one of the best-selling home computers

-   64KB of RAM (hence the name C64)

-   BASIC 2.0 was built into ROM

-   Programs were often stored on 5.25" floppy disks or cassette tapes

# Challenge Summary

  -----------------------------------------------------------------------
  **Challenge Type**      Reverse Engineering, Cryptography
  ----------------------- -----------------------------------------------
  **Encryption Method**   XOR cipher with key value 7

  **Password**            **C64RULES**

  **Flag**                **CTF{frost-plan:compressors,coolant,oil}**

  **Key Learning**        Understanding XOR encryption and reverse
                          engineering vintage BASIC programs
  -----------------------------------------------------------------------

**Challenge Status: ✅ Completed**
