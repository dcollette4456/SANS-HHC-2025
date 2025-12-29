#!/usr/bin/env python3
"""
Convert ODT-extracted markdown to GitHub-ready format
"""

import re
import os
from pathlib import Path

def fix_image_paths(content, image_dir="../images/act1"):
    """Fix image paths to point to GitHub structure"""
    # Pattern: ![alt](Pictures/XXXXX.png){width="..." height="..."}
    # Replace with: ![alt](../images/act1/XXXXX.png)
    
    pattern = r'!\[(.*?)\]\(Pictures/([^)]+\.png)\)(?:\{[^}]+\})?'
    replacement = r'![\1](' + image_dir + r'/\2)'
    
    content = re.sub(pattern, replacement, content)
    
    # Also handle cases without alt text
    pattern2 = r'!\[\]\(Pictures/([^)]+\.png)\)(?:\{[^}]+\})?'
    replacement2 = r'![](' + image_dir + r'/\1)'
    
    content = re.sub(pattern2, replacement2, content)
    
    return content

def add_header(title, difficulty, content):
    """Add proper header to markdown file"""
    header = f"""# {title}

**Difficulty**: {difficulty}

---

"""
    return header + content

def clean_markdown(content):
    """Clean up markdown formatting issues"""
    # Remove escaped backslashes
    content = content.replace('\\\\', '')
    
    # Fix escaped quotes
    content = content.replace("\\'", "'")
    content = content.replace('\\"', '"')
    
    # Remove extra backslashes before newlines
    content = content.replace('\\\n', '\n')
    
    return content

# Mapping of files
challenges = [
    {
        'input': '/tmp/Its_All_About_Defang.md',
        'output': 'ACT-1/01-defang.md',
        'title': 'Its All About Defang',
        'difficulty': '⭐'
    },
    {
        'input': '/tmp/Neighborhood_Watch_Bypass.md',
        'output': 'ACT-1/02-neighborhood-watch-bypass.md',
        'title': 'Neighborhood Watch Bypass',
        'difficulty': '⭐⭐'
    },
    {
        'input': '/tmp/Santas_Gift-Tracking_Service_Port_Mystery.md',
        'output': 'ACT-1/03-santas-gift-tracker.md',
        'title': "Santa's Gift-Tracking Service Port Mystery",
        'difficulty': '⭐'
    },
    {
        'input': '/tmp/Visual_Networking_Thinger_.md',
        'output': 'ACT-1/04-visual-networking.md',
        'title': 'Visual Networking Thinger',
        'difficulty': '⭐'
    },
    {
        'input': '/tmp/Visual_Firewall_Thinger.md',
        'output': 'ACT-1/05-visual-firewall.md',
        'title': 'Visual Firewall Thinger',
        'difficulty': '⭐'
    },
    {
        'input': '/tmp/Intro_to_Nmap.md',
        'output': 'ACT-1/06-intro-to-nmap.md',
        'title': 'Intro to Nmap',
        'difficulty': '⭐'
    },
    {
        'input': '/tmp/Blob_Storage_Challenge_in_the_Neighborhood.md',
        'output': 'ACT-1/07-blob-storage.md',
        'title': 'Blob Storage Challenge in the Neighborhood',
        'difficulty': '⭐'
    },
    {
        'input': '/tmp/Spare_Key.md',
        'output': 'ACT-1/08-spare-key.md',
        'title': 'Spare Key',
        'difficulty': '⭐⭐'
    },
    {
        'input': '/tmp/The_Open_Door.md',
        'output': 'ACT-1/09-the-open-door.md',
        'title': 'The Open Door',
        'difficulty': '⭐'
    },
    {
        'input': '/tmp/Owner.md',
        'output': 'ACT-1/10-owner.md',
        'title': 'Owner',
        'difficulty': '⭐⭐'
    }
]

# Process each challenge
for challenge in challenges:
    input_file = challenge['input']
    output_file = challenge['output']
    
    if not os.path.exists(input_file):
        print(f"❌ Missing: {input_file}")
        continue
    
    # Read content
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process content
    content = clean_markdown(content)
    content = fix_image_paths(content)
    content = add_header(challenge['title'], challenge['difficulty'], content)
    
    # Write output
    output_path = Path('/home/claude/SANS-HHC-2025') / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Created: {output_file}")

print("\n🎉 All challenges converted!")
