#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
from config import *
from helper import get_username_patterns

def extract_sections(html_file, output_file):
    """Extract specific sections from Facebook HTML export"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all sections with class="_a6-g"
    all_sections = soup.find_all('section', class_='_a6-g')
    
    # Categories we want to extract
    target_sections = []
    status_count = 0
    photo_count = 0
    
    # Get username patterns from config
    username_patterns = get_username_patterns()
    
    for section in all_sections:
        # Get all header texts to determine post type
        headers = section.find_all('h2', class_=['_2ph_', '_a6-h', '_a6-i'])
        if headers:
            # Combine all header texts
            all_header_text = ' '.join([h.get_text() for h in headers]).lower()
            
            # Check for status updates
            for pattern in username_patterns['status_update']:
                if pattern in all_header_text:
                    target_sections.append(section)
                    status_count += 1
                    break
            else:
                # Check for photo posts (only if not already matched as status)
                for pattern in username_patterns['photo_post']:
                    if pattern in all_header_text and 'video' not in all_header_text:
                        target_sections.append(section)
                        photo_count += 1
                        break
    
    # Create the output HTML
    html_structure = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Real Posts and Photos - Facebook Export</title>
    <style>
        {extract_css(content)}
    </style>
</head>
<body>
    <div class="_a705">
        <main>
"""
    
    # Add each target section
    for section in target_sections:
        html_structure += str(section) + '\n'
    
    html_structure += """
        </main>
    </div>
</body>
</html>"""
    
    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_structure)
    
    print(f"Extracted {len(target_sections)} sections to {output_file}")
    print(f"  - Status updates: {status_count}")
    print(f"  - Photo posts: {photo_count}")
    return len(target_sections)

def extract_css(content):
    """Extract CSS from the original file"""
    # Find the CSS style block
    css_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if css_match:
        return css_match.group(1)
    return ""

if __name__ == "__main__":
    # Use config file for input path
    extract_sections(INPUT_FILE, 'second_cut.html')