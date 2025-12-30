# Retro Recovery

**Difficulty:** ⭐⭐

---

## Challenge Overview

This challenge involves digital forensics on a FAT12 floppy disk image to recover a deleted BASIC program file. The scenario demonstrates classic file recovery techniques and how "deleted" files persist on storage media until overwritten.

**Objective:** Recover and decode the hidden message from a deleted BASIC program on the floppy disk image.

---

## Challenge Description

![Challenge Briefing](../images/act2/retro-recovery-02.png)

*The Retro Recovery challenge briefing*

The challenge presents a FAT12 floppy disk image allegedly found under an arcade machine in the Retro Store. The briefing references the historical "warez scene" practice of hiding files by marking them as deleted in the file system directory structure while leaving the actual data intact.

**Key Challenge Hints:**
- FAT12 floppy disk filesystem
- Files hidden as deleted entries
- BASIC programming language involvement
- "Deleted doesn't always mean gone forever"

---

## Initial Analysis

### File Identification

First, I attempted to identify the file type using standard tools:
```bash
exiftool floppy.img
file floppy.img
```

![ExifTool Output](../images/act2/retro-recovery-01.png)

*ExifTool initially reports "Unknown file type" but provides filesystem metadata*

**ExifTool Results:**
- **File Name:** floppy.img
- **File Size:** 1475 KB (1.44 MB - standard floppy size)
- **Modification Date:** 2025-12-27 10:46:03
- **Directory:** Current working directory

The `file` command provides more detailed filesystem information:
```
floppy.img: DOS/MBR boot sector, code offset 0x3c+2, OEM-ID "mkfs.fat", 
root entries 224, sectors 2880 (volumes <=32 MB), sectors/FAT 9, 
sectors/track 18, reserved 0x1, serial number 0x9c01e8ae, unlabeled, 
FAT (12 bit), followed by FAT
```

**Filesystem Analysis:**
- **Type:** FAT12 (12-bit File Allocation Table)
- **Total Sectors:** 2880 (1.44 MB standard capacity)
- **Root Directory Entries:** 224 maximum
- **Serial Number:** 0x9c01e8ae
- **Creator:** mkfs.fat (Linux FAT filesystem creator)

This confirms a standard 1.44MB floppy disk image using FAT12 filesystem.

---

## Digital Forensics Analysis

### Tool Selection: The Sleuth Kit

For forensic analysis of the disk image, I used **The Sleuth Kit (TSK)**, an industry-standard open-source digital forensics toolkit.

**Installation:**
```bash
sudo apt install sleuthkit
```

**Key TSK Tools for This Challenge:**
- `fls` - Lists files and directories, including deleted entries
- `icat` - Extracts file content by inode number

### File System Enumeration

Using `fls` with the recursive (`-r`) flag to enumerate all files, including deleted entries:
```bash
fls -r floppy.img
```

![File Listing with Deleted Entries](../images/act2/retro-recovery-03.png)

*The fls command reveals deleted files marked with asterisks*

**Results:**
```
r/r 4:        system_info.txt
r/r 5:        readme.txt
r/r * 6:      all_i-want_for_christmas.bas
r/r 7:        game_scores.txt
r/r * 10:     .all_i-want_f
```

**Analysis:**
- Entries prefixed with `*` indicate **deleted files**
- **Inode 6:** `all_i-want_for_christmas.bas` - Deleted BASIC program (primary target)
- **Inode 10:** `.all_i-want_f` - Truncated filename or fragment
- Active files: system_info.txt, readme.txt, game_scores.txt

**FAT12 Deletion Mechanism:**
When files are deleted in FAT12:
1. First byte of directory entry filename changed to 0xE5
2. Cluster allocation marked as "free" in FAT
3. **Data content remains on disk until overwritten**
4. File can be recovered if clusters haven't been reused

### File Recovery

Extracting the deleted BASIC program using `icat`:
```bash
icat floppy.img 6 > all_i-want_for_christmas.bas
```

**Command Breakdown:**
- `icat` - Tool to extract file by inode
- `floppy.img` - Source disk image
- `6` - Inode number of target file
- `> all_i-want_for_christmas.bas` - Output redirection

---

## Code Analysis

### BASIC Program Examination

Viewing the recovered file content:
```bash
cat all_i-want_for_christmas.bas
```

![BASIC Program Contents](../images/act2/retro-recovery-04.png)

*The recovered BASIC program - a Star Trek game from the 1970s*

**Program Analysis:**

The recovered file is a classic BASIC program:
- **Lines 1-10:** Program metadata and version history
- **Lines 30-210:** REM (remark) statements with program documentation
- **Line 211:** Contains suspicious data statement

**Line 211 (Critical Finding):**
```basic
211 REM bWVycnkgY2hyaXN0bWFzIHRvIGFsbCBhbmQgdG8gYWxsIGEgZ29vZCBuaWdodAo=
```

**Encoding Identification:**

The string exhibits characteristics of **Base64 encoding**:
- Character set: A-Z, a-z, 0-9, +, /
- Padding character: `=` at the end
- Length divisible by 4
- No whitespace or special characters

Base64 is commonly used to encode binary data in ASCII-safe format, often embedded in configuration files, emails, or in this case, legacy BASIC programs.

---

## Decoding Process

### Base64 Decryption

Decoding the Base64 string:
```bash
echo "bWVycnkgY2hyaXN0bWFzIHRvIGFsbCBhbmQgdG8gYWxsIGEgZ29vZCBuaWdodAo=" | base64 -d
```

![Decoded Message](../images/act2/retro-recovery-05.png)

*Base64 decoding reveals the hidden message*

**Output:**
```
merry christmas to all and to all a good night
```

### Answer Verification

The decoded message is a famous line from Clement Clarke Moore's 1823 poem "A Visit from St. Nicholas" (commonly known as "The Night Before Christmas"). This confirms successful recovery and decoding.

---

## Technical Summary

### Attack Chain

1. **File Identification** → Identified FAT12 floppy disk image
2. **Forensic Enumeration** → Used TSK `fls` to list deleted files
3. **File Recovery** → Extracted deleted file with `icat` by inode
4. **Content Analysis** → Examined BASIC program structure
5. **Encoding Detection** → Identified Base64 encoding pattern
6. **Decoding** → Decoded Base64 to retrieve plaintext message

### Key Technical Concepts

**FAT12 Filesystem:**
- 12-bit cluster addressing (max 4,084 clusters)
- Used on 1.44MB floppy disks
- File deletion marks directory entry, not data
- Deleted files recoverable until overwrite

**File Recovery Methodology:**
- Deleted files retain inode references
- Directory entry marked with 0xE5 marker
- Data clusters persist until reallocation
- Forensic tools can access "deleted" data directly

**Base64 Encoding:**
- Binary-to-text encoding scheme
- 3 bytes → 4 ASCII characters
- Padding with `=` for alignment
- Reversible (encoding, not encryption)
- No key required for decoding

---

## Answer

**Hidden Message:** `merry christmas to all and to all a good night`

---

## Tools Used

| Tool | Purpose | Command |
|------|---------|---------|
| `file` | File type identification | `file floppy.img` |
| `exiftool` | Metadata extraction | `exiftool floppy.img` |
| `fls` | Filesystem enumeration (TSK) | `fls -r floppy.img` |
| `icat` | File extraction by inode (TSK) | `icat floppy.img 6` |
| `base64` | Base64 decoding | `base64 -d` |

---

## Lessons Learned

### Digital Forensics Best Practices

1. **File Deletion ≠ Data Destruction**
   - Operating systems mark files as deleted without erasing data
   - Forensic recovery possible until disk space reused
   - Secure deletion requires overwriting (e.g., `shred`, DBAN)

2. **Filesystem Understanding Critical**
   - FAT12/16/32 directory structure preservation
   - Inode/cluster relationship
   - Metadata vs. actual data storage

3. **Tool Selection Matters**
   - Industry-standard tools (Sleuth Kit, Autopsy, FTK)
   - Open-source alternatives equally effective
   - Multiple tool verification recommended

4. **Encoding vs. Encryption**
   - Base64 is **encoding** (no security, easily reversible)
   - Encryption requires key (AES, RSA, etc.)
   - Never confuse obfuscation with protection

### Real-World Applications

**Incident Response:**
- Recovering attacker-deleted logs
- Finding evidence in deleted files
- Timeline reconstruction from filesystem metadata

**E-Discovery:**
- Legal hold and document recovery
- Email investigation from deleted items
- Compliance audit support

**Data Recovery:**
- Accidental deletion recovery
- Corrupted filesystem repair
- Lost file restoration

---

## References

- [The Sleuth Kit Documentation](http://www.sleuthkit.org/sleuthkit/docs.php)
- [FAT File System Specification](https://en.wikipedia.org/wiki/File_Allocation_Table)
- [Digital Forensics Framework - NIST](https://www.nist.gov/digital-forensics)
- [Base64 Encoding (RFC 4648)](https://tools.ietf.org/html/rfc4648)

---

**Challenge Status:** ✅ Completed

**Difficulty Rating:** ⭐⭐ (Intermediate - Requires forensic tool knowledge and encoding awareness)

---

*Writeup by SFC David P. Collette*  
*Regional Cyber Center - Korea (RCC-K)*  
*SANS Holiday Hack Challenge 2025*
