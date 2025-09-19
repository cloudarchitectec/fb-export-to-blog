#!/usr/bin/env python3

import re

def fix_image_paths(input_file, output_file):
    """Fix image paths to point to the correct relative location"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace src="your_facebook_activity/ with src="../original/your_facebook_activity/
    updated_content = re.sub(
        r'src="your_facebook_activity/',
        r'src="../original/your_facebook_activity/',
        content
    )
    
    # Also fix href links to media
    updated_content = re.sub(
        r'href="your_facebook_activity/',
        r'href="../original/your_facebook_activity/',
        updated_content
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"Fixed image paths in {input_file}")
    print(f"Updated file saved as {output_file}")

if __name__ == "__main__":
    fix_image_paths('second_cut.html', 'second_cut_fixed.html')