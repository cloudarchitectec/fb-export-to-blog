#!/usr/bin/env python3

import re
from bs4 import BeautifulSoup
from datetime import datetime
import html

def parse_facebook_date(date_str):
    """Convert Facebook date format to YYYY-MM-DD"""
    try:
        # Facebook dates are like "Aug 09, 2025 9:48:19 am"
        # First, clean up the string
        date_str = date_str.strip()
        
        # Parse the date
        dt = datetime.strptime(date_str, "%b %d, %Y %I:%M:%S %p")
        return dt.strftime("%Y-%m-%d"), dt
    except ValueError:
        try:
            # Try alternative format
            dt = datetime.strptime(date_str, "%b %d, %Y %I:%M:%S %p")
            return dt.strftime("%Y-%m-%d"), dt
        except ValueError:
            print(f"Could not parse date: {date_str}")
            return "unknown-date", None

def clean_facebook_content(section):
    """Clean Facebook content by removing unwanted header text"""
    # Clone the section to avoid modifying the original
    section_copy = BeautifulSoup(str(section), 'html.parser')
    
    # Find and clean the header
    header = section_copy.find('h2', class_=['_2ph_', '_a6-h', '_a6-i'])
    if header:
        # Remove text like "Ellie Ellie added a new photo."
        header_text = header.get_text()
        if any(phrase in header_text for phrase in ['added', 'shared', 'updated', 'posted']):
            header.decompose()  # Remove the entire header
    
    # Find and remove redundant photo type labels
    for div in section_copy.find_all('div'):
        text = div.get_text().strip()
        if text in ['Timeline photos', 'Mobile uploads', 'Profile pictures', 'Cover photos']:
            # Check if this div only contains the unwanted text
            if len(div.get_text().strip()) == len(text):
                div.decompose()
    
    return section_copy

def extract_first_sentence(text):
    """Extract first sentence from text, limit to 50 chars"""
    if not text:
        return ""
    
    # Remove HTML tags and decode entities
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    text = text.strip()
    
    if not text:
        return ""
    
    # Find first sentence (end with ., !, ?, or line break)
    sentences = re.split(r'[.!?]|\n', text)
    first_sentence = sentences[0].strip() if sentences else text
    
    # Limit to 50 characters
    if len(first_sentence) > 50:
        return first_sentence[:47] + "..."
    
    return first_sentence

def clean_title(title):
    """Clean up title by removing unwanted prefixes"""
    # Remove common Facebook post type prefixes
    prefixes_to_remove = [
        "Timeline-photos", "Timeline photos", 
        "Mobile-uploads", "Mobile uploads",
        "Profile-pictures", "Profile pictures",
        "Cover-photos", "Cover photos"
    ]
    
    for prefix in prefixes_to_remove:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
            # Remove leading dash or space
            if title.startswith('-') or title.startswith(' '):
                title = title[1:].strip()
            break
    
    return title

def create_blog_posts(input_file, output_file):
    """Transform Facebook posts into blog format"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all sections (posts)
    sections = soup.find_all('section', class_='_a6-g')
    
    posts = []
    photo_only_count = 0
    
    for section in sections:
        # Extract date from footer
        footer = section.find('footer')
        if not footer:
            continue
            
        date_div = footer.find('div', class_='_a72d')
        if not date_div:
            continue
            
        date_str = date_div.get_text().strip()
        formatted_date, dt_obj = parse_facebook_date(date_str)
        
        if not dt_obj:
            continue
        
        # Extract post content
        content_div = section.find('div', class_='_2pin')
        post_text = ""
        
        if content_div:
            # Look for text content
            text_divs = content_div.find_all('div', recursive=False)
            for div in text_divs:
                text = div.get_text().strip()
                if text and not text.startswith('Updated '):
                    post_text = text
                    break
        
        # Extract header (post type)
        header = section.find('h2', class_=['_2ph_', '_a6-h', '_a6-i'])
        header_text = header.get_text() if header else ""
        
        # Determine title
        if post_text:
            title = extract_first_sentence(post_text)
        else:
            # This is a photo-only post
            photo_only_count += 1
            title = "photos"
        
        # Clean up title
        title = clean_title(title)
        
        # Clean up title for filename safety
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title)
        
        blog_title = f"{formatted_date}-{safe_title}" if safe_title else formatted_date
        
        posts.append({
            'date': formatted_date,
            'datetime': dt_obj,
            'title': title,
            'blog_title': blog_title,
            'content': post_text,
            'header': header_text,
            'html': str(clean_facebook_content(section))
        })
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x['datetime'], reverse=True)
    
    # Generate blog HTML
    blog_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ellie's Blog Posts - Organized from Facebook</title>
    <style>
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 16px;
            line-height: 1.6;
            background-color: #f5f5f5;
            color: #1c1e21;
        }}
        
        .blog-header {{
            text-align: center;
            margin-bottom: 32px;
            padding: 24px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        }}
        
        .blog-header h1 {{
            font-size: 2.5rem;
            margin: 0 0 12px 0;
            color: #1c1e21;
            font-weight: 700;
        }}
        
        .blog-header p {{
            font-size: 1.1rem;
            color: #65676b;
            margin: 0;
        }}
        
        .blog-post {{
            background: white;
            margin-bottom: 24px;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            transition: box-shadow 0.2s ease;
        }}
        
        .blog-post:hover {{
            box-shadow: 0 4px 20px rgba(0,0,0,0.12);
        }}
        
        .post-header {{
            background: linear-gradient(135deg, #4267b2 0%, #5b7bd5 100%);
            color: white;
            padding: 20px 24px;
        }}
        
        .post-title {{
            font-size: 1.3rem;
            font-weight: 600;
            margin: 0;
            line-height: 1.4;
            word-break: break-word;
        }}
        
        .post-content {{
            padding: 24px;
        }}
        
        .stats {{
            background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 100%);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 32px;
            border-left: 4px solid #4267b2;
        }}
        
        .stats strong {{
            font-size: 1.1rem;
            color: #1c1e21;
        }}
        
        .facebook-content {{
            border: 1px solid #e4e6ea;
            border-radius: 8px;
            overflow: hidden;
            background: #fafbfc;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            body {{
                padding: 12px;
            }}
            
            .blog-header {{
                padding: 20px 16px;
                margin-bottom: 24px;
            }}
            
            .blog-header h1 {{
                font-size: 2rem;
            }}
            
            .blog-header p {{
                font-size: 1rem;
            }}
            
            .post-header {{
                padding: 16px 20px;
            }}
            
            .post-title {{
                font-size: 1.1rem;
            }}
            
            .post-content {{
                padding: 20px;
            }}
            
            .stats {{
                padding: 16px;
                margin-bottom: 24px;
            }}
            
            .blog-post {{
                margin-bottom: 20px;
            }}
        }}
        
        @media (max-width: 480px) {{
            body {{
                padding: 8px;
            }}
            
            .blog-header {{
                padding: 16px 12px;
            }}
            
            .blog-header h1 {{
                font-size: 1.75rem;
            }}
            
            .post-header {{
                padding: 14px 16px;
            }}
            
            .post-title {{
                font-size: 1rem;
            }}
            
            .post-content {{
                padding: 16px;
            }}
            
            .stats {{
                padding: 14px;
            }}
        }}
        
        /* Improve Facebook content display */
        .facebook-content img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }}
        
        .facebook-content ._a6-g {{
            background: transparent;
            border-radius: 0;
        }}
        
        /* Include original Facebook styles */
        {extract_original_css(content)}
    </style>
</head>
<body>
    <div class="blog-header">
        <h1>Ellie's Facebook Posts</h1>
        <p>Organized blog-style from Facebook export • {len(posts)} posts total</p>
    </div>
    
    <div class="stats">
        <strong>Statistics:</strong><br>
        📝 Total posts: {len(posts)}<br>
        📷 Photo-only posts (no text): {photo_only_count}<br>
        💬 Posts with text: {len(posts) - photo_only_count}<br>
        📅 Date range: {posts[-1]['date'] if posts else 'N/A'} to {posts[0]['date'] if posts else 'N/A'}
    </div>
"""
    
    # Add each post
    for post in posts:
        blog_html += f"""
    <article class="blog-post">
        <div class="post-header">
            <h2 class="post-title">{html.escape(post['blog_title'])}</h2>
        </div>
        <div class="post-content">
            <div class="facebook-content">
                {post['html']}
            </div>
        </div>
    </article>
"""
    
    blog_html += """
</body>
</html>"""
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(blog_html)
    
    print(f"Created blog with {len(posts)} posts")
    print(f"Photo-only posts: {photo_only_count}")
    print(f"Posts with text: {len(posts) - photo_only_count}")
    print(f"Saved as: {output_file}")

def extract_original_css(content):
    """Extract CSS from original Facebook export"""
    css_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if css_match:
        return css_match.group(1)
    return ""

if __name__ == "__main__":
    create_blog_posts('second_cut.html', 'third_cut.html')