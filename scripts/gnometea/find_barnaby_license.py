#!/usr/bin/env python3
"""
Find and download Barnaby Briefcase's driver's license
"""

import json
import requests
import os

def find_barnaby_license():
    """Find Barnaby's license URL from gnomes data"""
    
    # Read the gnomes data
    gnomes_file = '/mnt/user-data/uploads/gnomes.json'
    
    if not os.path.exists(gnomes_file):
        print(f"❌ Error: {gnomes_file} not found!")
        return None
    
    with open(gnomes_file, 'r') as f:
        data = json.load(f)
    
    # Find Barnaby - handle Firestore format
    for gnome in data:
        fields = gnome.get('fields', {})
        
        # Extract email from Firestore format
        email_obj = fields.get('email', {})
        email = email_obj.get('stringValue', '')
        
        # Extract UID from Firestore format
        uid_obj = fields.get('uid', {})
        uid = uid_obj.get('stringValue', '')
        
        # Check if this is Barnaby
        if email == 'barnabybriefcase@gnomemail.dosis' or uid == 'l7VS01K9GKV5ir5S8suDcwOFEpp2':
            print("✅ Found Barnaby Briefcase!")
            
            name = fields.get('name', {}).get('stringValue', 'N/A')
            home_location = fields.get('homeLocation', {}).get('stringValue', 'N/A')
            license_url_obj = fields.get('driversLicenseUrl', {})
            license_url = license_url_obj.get('stringValue')
            
            print(f"\nName: {name}")
            print(f"Email: {email}")
            print(f"UID: {uid}")
            print(f"Home Location: {home_location}")
            
            if license_url:
                print(f"\nDriver's License URL:")
                print(f"{license_url}")
                return license_url
            else:
                print("❌ No driversLicenseUrl field found!")
                return None
    
    print("❌ Barnaby not found in the data!")
    return None

def download_license(url):
    """Try to download the driver's license image"""
    
    if not url:
        return False
    
    output_dir = '/mnt/user-data/outputs'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'barnaby_drivers_license.jpeg')
    
    print(f"\n🔄 Attempting to download license...")
    print(f"URL: {url}")
    
    try:
        # Try direct download (might fail due to permissions)
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"✅ SUCCESS! License saved to: {output_file}")
            return True
        else:
            print(f"❌ HTTP {response.status_code}: {response.reason}")
            if response.status_code == 403:
                print("\n⚠️  Access Forbidden - Firebase Storage bucket is protected!")
                print("The license URL exists but requires authentication.")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading: {e}")
        return False

def main():
    print("=" * 70)
    print("🔍 Barnaby Briefcase Driver's License Finder")
    print("=" * 70)
    
    # Find the license URL
    license_url = find_barnaby_license()
    
    if license_url:
        # Try to download it
        success = download_license(license_url)
        
        if not success:
            print("\n" + "=" * 70)
            print("💡 ALTERNATIVE METHODS:")
            print("=" * 70)
            print("\n1. Open browser while logged into GnomeTea app")
            print("2. Paste this URL into address bar:")
            print(f"\n   {license_url}")
            print("\n3. If you have Firebase auth cookies, you might see the image!")
            print("\n4. Or check the GitHub repo for extracted images:")
            print("   https://github.com/gmanctf/2025-HHC/tree/main/Gnome%20Tea")
    else:
        print("\n❌ Could not find Barnaby's license URL in the data!")

if __name__ == '__main__':
    main()
