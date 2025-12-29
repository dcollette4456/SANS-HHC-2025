#!/usr/bin/env python3
"""
Convert Act 2 DOCX files to GitHub-ready markdown
"""

import os
import re
import zipfile
import shutil
from pathlib import Path

# Challenge mapping
act2_challenges = [
    {
        'file': '/mnt/project/SANS2025_WriteUP_ACT_2_-_Retro_Recovery.odt',
        'output': 'ACT-2/01-retro-recovery.md',
        'title': 'Retro Recovery',
        'difficulty': '⭐⭐',
        'is_odt': True
    },
    {
        'file': '/mnt/project/SANS2025_WriteUP_ACT_2_-_Mail_Detective.docx',
        'output': 'ACT-2/02-mail-detective.md',
        'title': 'Mail Detective',
        'difficulty': '⭐⭐',
        'is_odt': False
    },
    {
        'file': '/mnt/project/SANS2025_WriteUP_ACT_2_-_IDORable_Bistro.docx',
        'output': 'ACT-2/03-idorable-bistro.md',
        'title': 'IDORable Bistro',
        'difficulty': '⭐⭐',
        'is_odt': False
    },
    {
        'file': '/mnt/project/SANS2025_WriteUP_ACT_2_-_Dosis_Network_Down.docx',
        'output': 'ACT-2/04-dosis-network-down.md',
        'title': 'Dosis Network Down',
        'difficulty': '⭐⭐',
        'is_odt': False
    },
    {
        'file': '/mnt/project/SANS2025_WriteUP_ACT_2_-_Going_in_Reverse.docx',
        'output': 'ACT-2/05-going-in-reverse.md',
        'title': 'Going in Reverse',
        'difficulty': '⭐⭐',
        'is_odt': False
    },
    {
        'file': '/mnt/project/SANS2025_WriteUP_ACT_2_-_Quantgnome_Leap.docx',
        'output': 'ACT-2/06-quantgnome-leap.md',
        'title': 'Quantgnome Leap',
        'difficulty': '⭐⭐',
        'is_odt': False
    },
    {
        'file': '/mnt/project/SANS2025_WriteUP_ACT2_-_Rogue_Gnome_Identity_Provider.docx',
        'output': 'ACT-2/07-rogue-gnome-identity-provider.md',
        'title': 'Rogue Gnome Identity Provider',
        'difficulty': '⭐⭐⭐⭐⭐',
        'is_odt': False
    }
]

def extract_images_from_docx(docx_path, output_dir):
    """Extract images from DOCX file"""
    images = []
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            # Find all image files
            image_files = [f for f in zip_ref.namelist() if f.startswith('word/media/')]
            
            for img_file in image_files:
                # Extract to output directory
                img_name = os.path.basename(img_file)
                target_path = os.path.join(output_dir, img_name)
                
                with zip_ref.open(img_file) as source:
                    with open(target_path, 'wb') as target:
                        target.write(source.read())
                
                images.append(img_name)
    except Exception as e:
        print(f"  ⚠️ Could not extract images: {e}")
    
    return images

def extract_images_from_odt(odt_path, output_dir):
    """Extract images from ODT file"""
    images = []
    try:
        with zipfile.ZipFile(odt_path, 'r') as zip_ref:
            # Find all image files in ODT (Pictures/ directory)
            image_files = [f for f in zip_ref.namelist() if f.startswith('Pictures/')]
            
            for img_file in image_files:
                # Extract to output directory
                img_name = os.path.basename(img_file)
                target_path = os.path.join(output_dir, img_name)
                
                with zip_ref.open(img_file) as source:
                    with open(target_path, 'wb') as target:
                        target.write(source.read())
                
                images.append(img_name)
    except Exception as e:
        print(f"  ⚠️ Could not extract images: {e}")
    
    return images

def read_docx_as_text(docx_path):
    """Read DOCX as plain text (view tool format)"""
    try:
        with open(docx_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except:
        return None

def convert_to_markdown(content, images, challenge_name):
    """Convert content to markdown with image references"""
    # Fix image references
    # Replace word/media/ references with ../images/act2/
    for img in images:
        # Try multiple patterns
        content = re.sub(
            r'!\[([^\]]*)\]\(word/media/' + re.escape(img) + r'\)',
            r'![\1](../images/act2/' + img + ')',
            content
        )
        content = re.sub(
            r'!\[([^\]]*)\]\(media/' + re.escape(img) + r'\)',
            r'![\1](../images/act2/' + img + ')',
            content
        )
        content = re.sub(
            r'!\[([^\]]*)\]\(Pictures/' + re.escape(img) + r'\)',
            r'![\1](../images/act2/' + img + ')',
            content
        )
    
    # Clean up formatting
    content = content.replace('\\\'', "'")
    content = content.replace('\\"', '"')
    content = content.replace('\\\\', '')
    
    return content

# Process each challenge
total_images = 0
for challenge in act2_challenges:
    print(f"\n🔄 Processing: {challenge['title']}")
    
    # Read content
    content = read_docx_as_text(challenge['file'])
    if not content:
        print(f"  ❌ Could not read file")
        continue
    
    # Extract images
    img_output_dir = '/home/claude/SANS-HHC-2025/images/act2'
    os.makedirs(img_output_dir, exist_ok=True)
    
    if challenge['is_odt']:
        images = extract_images_from_odt(challenge['file'], img_output_dir)
    else:
        images = extract_images_from_docx(challenge['file'], img_output_dir)
    
    print(f"  📸 Extracted {len(images)} images")
    total_images += len(images)
    
    # Convert to markdown
    markdown = convert_to_markdown(content, images, challenge['title'])
    
    # Add header
    header = f"""# {challenge['title']}

**Difficulty**: {challenge['difficulty']}

---

"""
    markdown = header + markdown
    
    # Write output
    output_path = Path('/home/claude/SANS-HHC-2025') / challenge['output']
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"  ✅ Created: {challenge['output']}")

print(f"\n🎉 All Act 2 challenges converted!")
print(f"📊 Total images extracted: {total_images}")
