# Retro Recovery

**Difficulty**: ⭐⭐

---

##  Retro Recovery

*Difficulty: *\*\***

Never forget to remove RIFA caps from vintage computer power supplies
when restoring a system. I love vintage computing, its the very core of
where and when it all began. Sometimes it is the people no one can
imagine anything of who do the things no one can imagine. - Alan Turing.
You never forget your first 8-bit system.

This FAT12 floppy disk image must have been under an arcade machine here
in the Retro Store.

When I was a kid we shared warez by hiding things as deleted files.

I remember writing programs in BASIC. So much fun! My favorite was Star
Trek.

The beauty of file systems is that 'deleted' doesn't always mean gone
forever.

Ready to dive into some digital archaeology and see what secrets this
old disk is hiding?

Download the floppy disk image, and see what you can find!

![](Pictures/10000000000002F800000242F264498F.png){width="6.6929in"
height="5.0902in"}

I downloaded the "floppy.img" file.

![](Pictures/1000000000000212000000993CEE6359.png){width="5.5201in"
height="1.5929in"}

Also ran: file floppy.img

floppy.img: DOS/MBR boot sector, code offset 0x3c+2, OEM-ID
"mkfs.fat", root entries 224, sectors 2880 (volumes \<=32 MB),
sectors/FAT 9, sectors/track 18, reserved 0x1, serial number 0x9c01e8ae,
unlabeled, FAT (12 bit), followed by FAT

We got a serial number: 0x9c01e8ae

ok, so I'm going to put Sleuth Kit on my new Linux Mint install with:
sudo apt install sleuthkit\
\
this will give me access to the "fls" command: File List (from The
Sleuth Kit)

Using *fls* from The Sleuth Kit, I listed all files including deleted
ones with the *-r* (recursive) flag. This revealed a deleted BASIC
program file marked with an asterisk\...

![](Pictures/100000000000031300000114212C415A.png){width="8.1965in"
height="2.8744in"}

Looks like we have 2 deleted files indicated by an asterisk "\*"
all_i-want_for_christmas.bas inode 6 and .all_i-want_f inode 10. The
inode is just a unique ID for the file. We can see the contents of the
file using icat and pointing to the inode number:

icat floppy.img 6 \> all_i-want_for_christmas.bas

now I just: "more all_i-want_for_christmas.bas" and we get:

![](Pictures/100000000000034C000001D180F58A16.png){width="8.7902in"
height="4.8429in"}

line 211 looks like base64 encoded text:

bWVycnkgY2hyaXN0bWFzIHRvIGFsbCBhbmQgdG8gYWxsIGEgZ29vZCBuaWdodAo=

So, lets decode: echo
"bWVycnkgY2hyaXN0bWFzIHRvIGFsbCBhbmQgdG8gYWxsIGEgZ29vZCBuaWdodAo=" \|
base64 -d

![](Pictures/100000000000045A00000034228DF4EA.png){width="10.6256in"
height="0.4957in"}

Looks like the answer to me.

### Answer

**merry christmas to all and to all a good night**

### Tools Used

-   *fls* - List files in filesystem images (The Sleuth Kit)
-   *icat* - Extract files by inode number
-   *base64* - Decode Base64 strings

### Key Concepts

-   Deleted files remain recoverable until overwritten
-   FAT12 filesystem structure
-   "Warez scene" technique of hiding data in deleted files
-   Base64 encoding
