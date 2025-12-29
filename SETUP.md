# 🚀 GitHub Setup Instructions

## Quick Setup (5 minutes)

### Step 1: Create Your GitHub Repository

1. Go to https://github.com/new
2. **Repository name**: `SANS-HHC-2025` (or your preferred name)
3. **Description**: "Complete write-ups for SANS Holiday Hack Challenge 2025"
4. **Visibility**: Public (recommended for CTF write-ups) or Private
5. ✅ Check "Add a README file" - NO! (we have our own)
6. Click **"Create repository"**

### Step 2: Upload the Files

**Option A: Via Web Interface (Easiest)**

1. On your new repo page, click "uploading an existing file"
2. Drag and drop the entire `SANS-HHC-2025` folder contents
3. Or upload files one by one:
   - `README.md` (main file)
   - `ACT-1/` folder (10 markdown files)
   - `images/` folder (60 images)
4. Scroll down and click "Commit changes"

**Option B: Via Git Command Line**

```bash
# Navigate to the SANS-HHC-2025 folder
cd SANS-HHC-2025

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Act 1 write-ups"

# Connect to your GitHub repo (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/SANS-HHC-2025.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Images Display

1. Navigate to any challenge, e.g., `ACT-1/01-defang.md`
2. Scroll down and check if images display properly
3. If not, images might need to be in the right folder structure

---

## 📁 File Structure Overview

```
SANS-HHC-2025/
├── README.md                           # Main landing page
├── SETUP.md                            # This file
├── ACT-1/
│   ├── 01-defang.md
│   ├── 02-neighborhood-watch-bypass.md
│   ├── 03-santas-gift-tracker.md
│   ├── 04-visual-networking.md
│   ├── 05-visual-firewall.md
│   ├── 06-intro-to-nmap.md
│   ├── 07-blob-storage.md
│   ├── 08-spare-key.md
│   ├── 09-the-open-door.md
│   └── 10-owner.md
└── images/
    └── act1/
        ├── 10000000000001A4000000B6DBA7333F.png
        ├── 10000000000001B7000000A1F14C70B6.png
        └── ... (60 total images)
```

---

## ✨ Features Your Repo Will Have

✅ **Professional README** with table of contents  
✅ **All 10 Act 1 challenges** in markdown format  
✅ **60+ embedded images** showing solutions  
✅ **Proper formatting** for GitHub display  
✅ **Searchable content** via GitHub search  
✅ **Version history** of your write-ups  
✅ **Easy sharing** via URL  

---

## 🎨 Make It Look Even Better

### Add a Nice Banner (Optional)

Create a banner image and add to README.md:

```markdown
![SANS Holiday Hack Challenge 2025](images/banner.png)
```

### Enable GitHub Pages (Optional)

1. Go to your repo **Settings**
2. Scroll to **Pages**
3. Source: Deploy from branch → `main`
4. Your write-ups will be at: `https://YOUR_USERNAME.github.io/SANS-HHC-2025/`

### Add Topics/Tags

In your repo, click the ⚙️ gear next to "About":
- Add topics: `ctf`, `sans`, `holiday-hack-challenge`, `writeup`, `cybersecurity`, `azure`, `penetration-testing`

---

## 📝 Adding Act 2 Later

When you complete Act 2 challenges:

1. Create new markdown files in `ACT-2/` folder
2. Add images to `images/act2/`
3. Update README.md table of contents
4. Commit and push:

```bash
git add .
git commit -m "Added Act 2 write-ups"
git push
```

---

## 🔗 Sharing Your Write-Ups

Once published, share via:

- **Direct link**: `https://github.com/YOUR_USERNAME/SANS-HHC-2025`
- **Specific challenge**: `https://github.com/YOUR_USERNAME/SANS-HHC-2025/blob/main/ACT-1/02-neighborhood-watch-bypass.md`
- **LinkedIn**: Post about your achievements with repo link
- **Twitter/X**: Share with #HolidayHackChallenge #SANS
- **CTF Discord/Forums**: Help others learn!

---

## 🆘 Troubleshooting

**Images not showing?**
- Make sure `images/act1/` folder structure is correct
- Check image paths in markdown files start with `../images/act1/`
- GitHub is case-sensitive with filenames

**Can't push to GitHub?**
- Check you have write access to the repo
- Verify your Git credentials are set up
- Try the web interface upload instead

**Formatting looks weird?**
- GitHub uses GitHub Flavored Markdown (GFM)
- Preview files before committing
- Check for special characters that need escaping

---

## ✅ You're All Set!

Your write-ups are ready to share with the world! 🎉

Questions? Issues? Create an issue in your repo or DM me!

**Good luck and happy hacking! 🎄🔐**
