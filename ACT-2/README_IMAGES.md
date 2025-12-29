# 📸 Act 2 Images

The Act 2 write-ups reference images that need to be extracted from the original DOCX files.

## How to Add Images

1. **Download your DOCX files** from Google Drive
2. **Extract images** using one of these methods:

### Method 1: Unzip the DOCX (Easiest)
```bash
# DOCX files are ZIP archives
unzip SANS2025_WriteUP_ACT_2_-_Dosis_Network_Down.docx -d temp/
cp temp/word/media/* ../images/act2/
```

### Method 2: Use pandoc
```bash
pandoc your_file.docx -t markdown --extract-media=./media
cp media/media/* ../images/act2/
```

3. **Fix image references** in markdown files:
   - Change `media/image1.png` to `../images/act2/image1.png`

## Images Needed

Based on the write-ups, you'll need images from:

- **Dosis Network Down**: image1.png, image2.png, image3.png
- **IDORable Bistro**: Multiple screenshots
- **Quantgnome Leap**: image2.png through image12.png
- **Mail Detective**: Screenshots
- **Going in Reverse**: Screenshots
- **Rogue Gnome**: Screenshots

## Quick Fix Script

Run this after adding images to `images/act2/`:

```bash
cd ACT-2
sed -i 's|media/|../images/act2/|g' *.md
```

---

**Note**: The write-ups are complete and functional without images, but images greatly enhance understanding!
