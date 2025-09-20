#!/usr/bin/env python3

from bs4 import BeautifulSoup
from config import *
from helper import get_username_patterns

def debug_sections(html_file):
    """Debug what sections we're finding"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all sections with class="_a6-g"
    all_sections = soup.find_all('section', class_='_a6-g')
    
    status_headers = []
    photo_headers = []
    
    # Get username patterns from config
    username_patterns = get_username_patterns()
    
    for i, section in enumerate(all_sections):
        # Get all header texts to determine post type
        headers = section.find_all('h2', class_=['_2ph_', '_a6-h', '_a6-i'])
        if headers:
            # Combine all header texts
            all_header_text = ' '.join([h.get_text() for h in headers])
            all_header_text_lower = all_header_text.lower()
            
            # Check for status updates
            for pattern in username_patterns['status_update']:
                if pattern in all_header_text_lower:
                    status_headers.append(all_header_text)
                    if len(status_headers) <= 10:  # Only show first 10
                        print(f"Status {len(status_headers)}: {all_header_text}")
                    break
            else:
                # Check for photo posts
                for pattern in username_patterns['photo_post']:
                    if pattern in all_header_text_lower and 'video' not in all_header_text_lower:
                        photo_headers.append(all_header_text)
                        if len(photo_headers) <= 10:  # Only show first 10
                            print(f"Photo {len(photo_headers)}: {all_header_text}")
                        break
    
    print(f"\nTotal status updates found: {len(status_headers)}")
    print(f"Total photo posts found: {len(photo_headers)}")

if __name__ == "__main__":
    debug_sections(INPUT_FILE)