# GnomeTea Data Extractor - Instructions

## Challenge Background

The GnomeTea Firebase application has misconfigured Firestore security rules that allow 
unauthenticated access to the `gnomes`, `tea`, and `dms` collections. However, the 
`admins/secret_operations` document containing the passphrase is properly secured.

To get the passphrase, we need to:
1. Extract data from unsecured collections
2. Find credentials in the DM conversations
3. Authenticate and access the protected passphrase

## Requirements

```bash
pip install requests
```

## Usage

1. Run the extraction script:
```bash
python3 gnometea_extractor.py
```

2. The script will create a `gnometea_data/` directory with:
   - `json/` - Raw Firestore JSON data
   - `parsed/` - Clean, readable JSON  
   - `images/` - Downloaded images (if accessible)
   - `dm_conversations/` - Individual DM conversations as text files
   - `EXTRACTION_REPORT.txt` - Summary of findings

## Solution Steps

### Step 1: Analyze the DM Conversations

After extraction, examine the DM conversations in `dm_conversations/`:

Look for `Barnaby-Briefcase_and_Glitch-Mitnick.txt`:
```
Barnaby Briefcase: Hey Glitch, I keep forgetting my password. Can you help me reset it?
Glitch Mitnick: Sure thing! What's your current password so I can verify your account?
Barnaby Briefcase: Sorry, I can't give you my password but I can give you a hint. 
My password is actually the name of my hometown that I grew up in. I actually just 
visited there back when I signed up with my id to GnomeTea (I took my picture of 
my id there).
```

**Key Intel:**
- Barnaby's password = his hometown
- He took his driver's license photo there
- Email: barnabybriefcase@gnomemail.dosis

### Step 2: Find Barnaby's Driver's License

From the extracted gnomes data, Barnaby's driver's license URL is:
```
https://storage.googleapis.com/holidayhack2025.firebasestorage.app/gnome-documents/l7VS01K9GKV5ir5S8suDcwOFEpp2_drivers_license.jpeg
```

**Note:** The Firebase Storage bucket may also be protected. If the image download 
fails, you'll need to find another way to access it (check if someone else has 
extracted and shared the images).

### Step 3: Authenticate as Barnaby

Once you have his hometown from the license:

1. Go to https://gnometea.web.app/login
2. Login with:
   - Email: `barnabybriefcase@gnomemail.dosis`
   - Password: `[hometown from driver's license]`

### Step 4: Access the Secret Passphrase

After authentication, the dashboard will display:
- Secret operations data from `admins/secret_operations`
- The **Agent Recognition Protocol** section
- **The secret passphrase field!**

## What the Script Does

### Accessible Collections (No Auth Required):
- ✅ `gnomes` - User profiles with emails and driver's license URLs
- ✅ `tea` - Public posts/messages  
- ✅ `dms` - Direct messages (contains Barnaby's password hint!)

### Protected Collections (Requires Auth):
- ❌ `admins` - Contains `secret_operations` document with passphrase
- ❌ Firebase Storage - May require auth to download images

The script will extract everything it can access and clearly mark what's protected.

## Troubleshooting

### Network Errors
If you get proxy/connection errors:
- Run on your local machine (not a restricted environment)
- Ensure you can access: https://firestore.googleapis.com

### Images Won't Download
If driver's licenses fail to download (403 errors):
- The storage bucket is protected
- Look for the images in public GitHub repos or shared solutions
- Or find the hometown through other OSINT methods

### Can't Find Passphrase
The passphrase is NOT in the unsecured collections. You MUST:
1. Find Barnaby's credentials via DMs
2. Authenticate to the web app
3. View the authenticated dashboard

## Challenge Complete!

Once authenticated as Barnaby, the Operations Dashboard will display the 
**Agent Recognition Protocol** with the secret passphrase to submit!
