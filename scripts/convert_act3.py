#!/usr/bin/env python3
"""
Convert Act 3 DOCX files to markdown with proper formatting
"""

import re
from pathlib import Path

def fix_markdown(md_file, output_file, challenge_num, title, difficulty):
    """Fix markdown formatting and image paths"""
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix image paths - convert media/imageN.png to ../images/act3/imageN.png
    content = re.sub(
        r'<img src="[^"]*media/image(\d+\.\w+)"',
        r'<img src="../images/act3/image\1"',
        content
    )
    
    # Also fix any ![...](media/imageN.png) style
    content = re.sub(
        r'!\[([^\]]*)\]\([^)]*media/image(\d+\.\w+)\)',
        r'![\1](../images/act3/image\2)',
        content
    )
    
    # Add proper header
    header = f"""# {title}

**Difficulty:** {difficulty}

**SANS Holiday Hack Challenge 2025 - Act 3**

---

"""
    
    # If content already has the title, remove it to avoid duplication
    content = re.sub(r'^#\s+' + re.escape(title) + r'\s*\n', '', content)
    content = re.sub(r'^SANS Holiday Hack Challenge.*?\n', '', content)
    content = re.sub(r'^Difficulty:.*?\n', '', content)
    content = re.sub(r'^Status:.*?\n', '', content)
    
    # Combine header + content
    final_content = header + content
    
    # Save
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"✅ Created: {output_file}")

def main():
    print("="*70)
    print("Act 3 Markdown Converter")
    print("="*70)
    
    # Convert GnomeTea
    fix_markdown(
        md_file='/tmp/act3_conversion/gnometea.md',
        output_file='/home/claude/SANS-HHC-2025/ACT-3/01-gnometea.md',
        challenge_num='01',
        title='GnomeTea - Firebase Security Misconfiguration',
        difficulty='⭐⭐⭐'
    )
    
    # Convert Snowcat
    fix_markdown(
        md_file='/tmp/act3_conversion/snowcat.md',
        output_file='/home/claude/SANS-HHC-2025/ACT-3/02-snowcat-privilege-escalation.md',
        challenge_num='02',
        title='Snowcat Privilege Escalation',
        difficulty='⭐⭐⭐ (In Progress)'
    )
    
    print("\n✅ Act 3 conversion complete!")

if __name__ == '__main__':
    main()
