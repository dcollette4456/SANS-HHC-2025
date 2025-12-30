# Going in Reverse - Commodore 64 BASIC Decryption

**Difficulty:** ⭐⭐ (2/5)

## Challenge Overview

Help Kevin analyze a mysterious Commodore 64 BASIC program found on an old 5.25" floppy disk. The program contains an encrypted password and flag that need to be reverse engineered.

**Objective:** Reverse engineer a vintage BASIC program to decrypt hidden messages.

---

## Character Introduction: Kevin

> *Hello, I'm Kevin (though past friends have referred to me as 'Heavy K')*

Kevin is a philosophy graduate with diverse interests including Amateur Astronomy, Shortwave Radio, and retro-gaming. He's particularly fascinated by vintage computing artifacts like the Commodore 64.

> *"Finding an old Commodore 64 disk with a mysterious BASIC program on it? That's like discovering a digital time capsule. The C64 was an incredible machine for its time - 64KB of RAM seemed like an ocean of possibility back then."*

---

## The BASIC Program

The challenge presents a Commodore 64 BASIC security program:

```basic
10 REM *** COMMODORE 64 SECURITY SYSTEM ***
20 ENC_PASS$ = "D13URKBT"
30 ENC_FLAG$ = "DSA|auhts*wkfi=dhjwubtthut+dhhkfis+hnkz"
40 INPUT "ENTER PASSWORD: "; PASS$
50 IF LEN(PASS$) <> LEN(ENC_PASS$) THEN GOTO 90
60 FOR I = 1 TO LEN(PASS$)
70 IF CHR$(ASC(MID$(PASS$,I,1)) XOR 7) <> MID$(ENC_PASS$,I,1) THEN GOTO 90
80 NEXT I
85 FLAG$ = "" : FOR I = 1 TO LEN(ENC_FLAG$) : FLAG$ = FLAG$ + CHR$(ASC(MID$(ENC_FLAG$,I,1)) XOR 7) : NEXT I : PRINT FLAG$
90 PRINT "ACCESS DENIED"
100 END
```

---

## Reverse Engineering Analysis

### Step 1: Understanding the Encryption

The key to solving this challenge is understanding the XOR encryption used in lines 70 and 85:

**Line 70:** Password verification
```basic
IF CHR$(ASC(MID$(PASS$,I,1)) XOR 7) <> MID$(ENC_PASS$,I,1) THEN GOTO 90
```

**Line 85:** Flag decryption
```basic
FLAG$ = FLAG$ + CHR$(ASC(MID$(ENC_FLAG$,I,1)) XOR 7)
```

#### How the Encryption Works

**XOR Properties:**
- Each character is XORed with the value `7`
- XOR is reversible: `A XOR B XOR B = A`
- To decrypt: `encrypted_char XOR 7 = original_char`
- The same XOR 7 operation both **encrypts AND decrypts**

**BASIC String Functions:**
- `MID$(string, position, length)` - Extracts substring
- `ASC(character)` - Returns ASCII value  
- `CHR$(number)` - Converts ASCII value to character
- `LEN(string)` - Returns string length

---

### Step 2: Decrypting the Password

**Line 20** contains the encrypted password:

```basic
ENC_PASS$ = "D13URKBT"
```

Applying XOR 7 to each character:

| **Position** | **Encrypted** | **ASCII** | **XOR 7** | **Decrypted** |
|-------------|--------------|----------|-----------|--------------|
| 1 | D | 68 | 68 XOR 7 = 67 | **C** |
| 2 | 1 | 49 | 49 XOR 7 = 54 | **6** |
| 3 | 3 | 51 | 51 XOR 7 = 52 | **4** |
| 4 | U | 85 | 85 XOR 7 = 82 | **R** |
| 5 | R | 82 | 82 XOR 7 = 85 | **U** |
| 6 | K | 75 | 75 XOR 7 = 76 | **L** |
| 7 | B | 66 | 66 XOR 7 = 69 | **E** |
| 8 | T | 84 | 84 XOR 7 = 83 | **S** |

✅ **DECRYPTED PASSWORD:** `C64RULES`

---

### Step 3: Decrypting the Flag

**Line 30** contains the encrypted flag:

```basic
ENC_FLAG$ = "DSA|auhts*wkfi=dhjwubtthut+dhhkfis+hnkz"
```

**Line 85** shows how the flag is decrypted once the correct password is entered - using the same XOR 7 operation:

```basic
FLAG$ = FLAG$ + CHR$(ASC(MID$(ENC_FLAG$,I,1)) XOR 7)
```

Applying XOR 7 to the first few characters as demonstration:

| **Position** | **Encrypted** | **ASCII** | **XOR 7** | **Decrypted** |
|-------------|--------------|----------|-----------|--------------|
| 1 | D | 68 | 67 | **C** |
| 2 | S | 83 | 84 | **T** |
| 3 | A | 65 | 70 | **F** |
| 4 | \| | 124 | 123 | **{** |
| 5 | a | 97 | 102 | **f** |
| 6 | u | 117 | 114 | **r** |
| 7 | h | 104 | 111 | **o** |
| 8 | t | 116 | 115 | **s** |
| 9 | s | 115 | 116 | **t** |
| ... | ... | ... | ... | ... |

✅ **DECRYPTED FLAG:** `CTF{frost-plan:compressors,coolant,oil}`

---

## Python Solution Script

Here's the complete Python script used to reverse engineer the program:

```python
#!/usr/bin/env python3

# Encrypted values from the BASIC program
ENC_PASS = "D13URKBT"
ENC_FLAG = "DSA|auhts*wkfi=dhjwubtthut+dhhkfis+hnkz"

# Decrypt password using XOR 7
password = ""
for char in ENC_PASS:
    password += chr(ord(char) ^ 7)

print(f"Password: {password}")

# Decrypt flag using XOR 7
flag = ""
for char in ENC_FLAG:
    flag += chr(ord(char) ^ 7)

print(f"Flag: {flag}")
```

**Output:**

```
Password: C64RULES
Flag: CTF{frost-plan:compressors,coolant,oil}
```

---

## Technical Concepts Learned

### XOR Encryption

**What is XOR?**
- XOR (Exclusive OR) is a bitwise operation
- Returns 1 if bits are different, 0 if same
- Truth table:

| A | B | A XOR B |
|---|---|---------|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

**Why XOR is Special:**
- **Self-Inverse:** `A XOR B XOR B = A`
- **Commutative:** `A XOR B = B XOR A`
- **Associative:** `(A XOR B) XOR C = A XOR (B XOR C)`

**Example with ASCII:**

```
Character 'D':
ASCII: 68 (decimal) = 01000100 (binary)
Key: 7 (decimal) = 00000111 (binary)

XOR Operation:
  01000100  (D = 68)
⊕ 00000111  (7)
-----------
  01000011  (C = 67)
```

### Security Analysis

**Why Simple XOR is Weak:**

1. **Known-Plaintext Attack**
   - If attacker knows any plaintext-ciphertext pair
   - Can recover the key: `key = plaintext XOR ciphertext`
   - In this case: single-byte key is trivial to brute force

2. **Key Reuse**
   - Same key (7) used for all characters
   - No key derivation or randomization
   - Patterns in plaintext visible in ciphertext

3. **Small Keyspace**
   - Only 256 possible keys (0-255)
   - Can brute force in milliseconds
   - No computational security

**Modern Encryption:**
- Uses complex algorithms (AES, ChaCha20)
- Large key sizes (128, 256 bits)
- Key derivation functions
- Authentication (HMAC, GCM)

---

## Commodore 64 History & Context

### The C64 Legacy

| **Attribute** | **Details** |
|--------------|-------------|
| **Released** | 1982 |
| **Manufacturer** | Commodore International |
| **CPU** | MOS Technology 6510 @ 1.023 MHz |
| **RAM** | 64 KB (hence the name!) |
| **ROM** | 20 KB (BASIC 2.0, KERNAL) |
| **Sales** | ~17 million units (best-selling single computer model) |

### BASIC 2.0 Features

The Commodore 64 came with **BASIC 2.0** built into ROM:

- **Line-numbered programming** - Programs organized by line numbers (10, 20, 30...)
- **Immediate mode** - Execute commands without line numbers
- **String handling** - Built-in string manipulation functions
- **File I/O** - Read/write to cassette tapes and floppy disks
- **Graphics & Sound** - POKE commands to control hardware

### Storage Media

**5.25" Floppy Disks:**
- Capacity: ~170 KB
- Speed: Very slow (minutes to load programs)
- Fragile: Magnetic media, easily damaged
- **"Don't copy that floppy!"** - 1980s anti-piracy campaign

**Cassette Tapes:**
- Even slower than floppies
- Used audio encoding
- Very unreliable

### Warez Scene

The challenge references the "warez scene" - underground software piracy culture:

- **BBS (Bulletin Board Systems)** - Dial-up networks for file sharing
- **Cracking groups** - Removed copy protection from software
- **Demo scene** - Created impressive graphics/music demos
- **Hidden files** - Deleted files could still be recovered (like this challenge!)

---

## The Flag's Meaning

**Flag:** `CTF{frost-plan:compressors,coolant,oil}`

This relates to the gnomes' plot to freeze the neighborhood:

- **Compressors** - HVAC components for cooling
- **Coolant** - Refrigerant chemicals
- **Oil** - Lubricant for compressor systems

The gnomes are targeting the neighborhood's heating/cooling infrastructure to create a perpetual winter! 🥶

---

## Key Concepts Summary

### Programming Concepts

1. **String Manipulation**
   - Character-by-character processing
   - ASCII conversion and manipulation
   - Loop-based string building

2. **Control Flow**
   - Conditional logic (IF/THEN)
   - Loops (FOR/NEXT)
   - Program flow control (GOTO)

3. **Input Validation**
   - Length checking
   - Character comparison
   - Access control logic

### Cryptography Concepts

1. **Symmetric Encryption**
   - Same key for encryption and decryption
   - XOR as simplest symmetric cipher

2. **Reversibility**
   - XOR's self-inverse property
   - Importance of key secrecy

3. **Cryptanalysis**
   - Reverse engineering algorithms
   - Known-plaintext attacks
   - Brute force key search

---

## Tools & Resources

### Reverse Engineering Tools

- **Python** - Modern scripting for analysis
- **CyberChef** - Web-based crypto analysis tool
- **Hex Editors** - View raw binary data
- **Disassemblers** - For more complex reverse engineering

### Commodore 64 Emulators

- **VICE** - Versatile Commodore Emulator
- **CCS64** - High compatibility emulator
- **Frodo** - Fast, portable emulator

### Learning Resources

- [Commodore 64 Wiki](https://www.c64-wiki.com/)
- [BASIC 2.0 Reference](https://www.c64-wiki.com/wiki/BASIC)
- [XOR Cipher Tutorial](https://en.wikipedia.org/wiki/XOR_cipher)

---

## Challenge Complete! 🎉

**Status:** ✅ Completed

**Password:** `C64RULES`

**Flag:** `CTF{frost-plan:compressors,coolant,oil}`

**Encryption Method:** XOR cipher with key value 7

**Technique:** Reverse engineering vintage BASIC program + XOR decryption

**Historical Context:** Warez scene technique of hiding data in old computers

---

*Challenge writeup by SFC David P. Collette*  
*Regional Cyber Center - Korea (RCC-K)*  
*SANS Holiday Hack Challenge 2025*
