#!/usr/bin/env python3

from bs4 import BeautifulSoup

def analyze_file(html_file):
    """Analyze the HTML file structure"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all sections with class="_a6-g"
    all_sections = soup.find_all('section', class_='_a6-g')
    print(f"BeautifulSoup found {len(all_sections)} sections")
    
    # Check first few sections
    for i, section in enumerate(all_sections[:5]):
        headers = section.find_all('h2', class_=['_2ph_', '_a6-h', '_a6-i'])
        if headers:
            print(f"Section {i+1}: {len(headers)} headers")
            for j, header in enumerate(headers):
                print(f"  Header {j+1}: {header.get_text()}")
        else:
            print(f"Section {i+1}: No headers found")
        print("---")

if __name__ == "__main__":
    analyze_file('first_cut.html')