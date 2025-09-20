#!/usr/bin/env python3

from bs4 import BeautifulSoup
from config import *

def count_unique_sections(html_file):
    """Count unique sections with specific headers"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all sections with class="_a6-g"
    all_sections = soup.find_all('section', class_='_a6-g')
    
    status_sections = 0
    photo_sections = 0
    
    for section in all_sections:
        # Get all header texts to determine post type
        headers = section.find_all('h2', class_=['_2ph_', '_a6-h', '_a6-i'])
        if headers:
            # Combine all header texts
            all_header_text = ' '.join([h.get_text() for h in headers]).lower()
            
            # Check if this SECTION contains these patterns (only count once per section)
            if 'updated her status' in all_header_text:
                status_sections += 1
            elif ('added a new photo' in all_header_text or 
                  ('added' in all_header_text and 'photos' in all_header_text and 'video' not in all_header_text)):
                photo_sections += 1
    
    print(f"Unique sections with status updates: {status_sections}")
    print(f"Unique sections with photo posts: {photo_sections}")
    print(f"Total sections: {len(all_sections)}")

if __name__ == "__main__":
    count_unique_sections('first_cut.html')