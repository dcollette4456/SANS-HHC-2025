#!/usr/bin/env python3
"""
GnomeTea Data Analyzer
Analyzes extracted Firestore data to find credential hints
"""

import json
import os
from pathlib import Path

def analyze_dms_for_passwords(dms_file):
    """Search DM conversations for password hints."""
    print("\n" + "="*80)
    print("ANALYZING DM CONVERSATIONS FOR PASSWORD HINTS")
    print("="*80 + "\n")
    
    if not os.path.exists(dms_file):
        print(f"[!] DMs file not found: {dms_file}")
        return
    
    with open(dms_file, 'r', encoding='utf-8') as f:
        dms = json.load(f)
    
    keywords = ['password', 'hometown', 'license', 'id', 'reset', 'forgot']
    found_hints = []
    
    for dm in dms:
        participant_names = dm.get('participantNames', [])
        messages = dm.get('messages', [])
        
        if len(participant_names) != 2:
            continue
        
        # Check each message for keywords
        for msg in messages:
            content = msg.get('content', '').lower()
            
            if any(keyword in content for keyword in keywords):
                found_hints.append({
                    'participants': participant_names,
                    'sender': msg.get('senderName'),
                    'message': msg.get('content')
                })
    
    if found_hints:
        print(f"[+] Found {len(found_hints)} messages containing password-related keywords:\n")
        
        for i, hint in enumerate(found_hints, 1):
            print(f"--- Message {i} ---")
            print(f"Conversation: {' and '.join(hint['participants'])}")
            print(f"From: {hint['sender']}")
            print(f"Message: {hint['message']}")
            print()
    else:
        print("[!] No password hints found in DMs")

def find_gnome_by_name(gnomes_file, name):
    """Find a specific gnome's data."""
    if not os.path.exists(gnomes_file):
        print(f"[!] Gnomes file not found: {gnomes_file}")
        return None
    
    with open(gnomes_file, 'r', encoding='utf-8') as f:
        gnomes = json.load(f)
    
    for gnome in gnomes:
        if gnome.get('name', '').lower() == name.lower():
            return gnome
    
    return None

def main():
    print("="*80)
    print("GNOMETEA DATA ANALYZER")
    print("="*80)
    
    # Check if data directory exists
    data_dir = Path("gnometea_data/parsed")
    if not data_dir.exists():
        print("\n[!] Data directory not found!")
        print("Please run gnometea_extractor.py first")
        return
    
    # Analyze DMs
    dms_file = data_dir / "dms_parsed.json"
    analyze_dms_for_passwords(dms_file)
    
    # Find Barnaby's info
    print("\n" + "="*80)
    print("BARNABY BRIEFCASE PROFILE")
    print("="*80 + "\n")
    
    gnomes_file = data_dir / "gnomes_parsed.json"
    barnaby = find_gnome_by_name(gnomes_file, "Barnaby Briefcase")
    
    if barnaby:
        print("[+] Found Barnaby's profile:\n")
        print(f"Name: {barnaby.get('name')}")
        print(f"Email: {barnaby.get('email')}")
        print(f"Home Location: {barnaby.get('homeLocation')}")
        print(f"Driver's License URL: {barnaby.get('driversLicenseUrl')}")
        print(f"\nBio: {barnaby.get('bio')}")
        
        print("\n" + "-"*80)
        print("CREDENTIALS TO TRY:")
        print("-"*80)
        print(f"Email: {barnaby.get('email')}")
        print(f"Password: [hometown from driver's license image]")
        print("\nTo get the password:")
        print(f"1. Download or view: {barnaby.get('driversLicenseUrl')}")
        print(f"2. Look for the city/hometown on the license")
        print(f"3. That's the password!")
    else:
        print("[!] Barnaby Briefcase not found in gnomes data")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
