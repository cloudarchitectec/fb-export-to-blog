#!/usr/bin/env python3
"""
Facebook Export to Blog Converter

This script processes a Facebook HTML export file and converts it into a clean,
responsive blog-style HTML file containing only status updates and photo posts.

Input: input/your_posts__check_ins__photos_and_videos_1.html (Facebook export)
Output: output/fb-posts.html (Clean blog format)

Features:
- Filters only status updates and photo posts
- Removes Facebook clutter (Timeline-photos, Mobile-uploads, etc.)
- Creates responsive design for mobile/tablet/desktop
- Organizes posts chronologically (newest first)
- Fixes image paths to work with local files
- Generates clean YYYY-MM-DD-{title} format
"""

import re
from bs4 import BeautifulSoup
from datetime import datetime
import html
import os

def parse_facebook_date(date_str):
    """Convert Facebook date format to YYYY-MM-DD"""
    try:
        # Facebook dates are like "Aug 09, 2025 9:48:19 am"
        date_str = date_str.strip()
        dt = datetime.strptime(date_str, "%b %d, %Y %I:%M:%S %p")
        return dt.strftime("%Y-%m-%d"), dt
    except ValueError:
        try:
            # Try alternative format without seconds
            dt = datetime.strptime(date_str, "%b %d, %Y %I:%M %p")
            return dt.strftime("%Y-%m-%d"), dt
        except ValueError:
            print(f"Could not parse date: {date_str}")
            return "unknown-date", None

def extract_first_sentence(text):
    """Extract first sentence from text, limit to 40 chars"""
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
    
    # Limit to 40 characters
    if len(first_sentence) > 40:
        return first_sentence[:37] + "..."
    
    return first_sentence

def clean_title(title):
    """Clean up title by removing unwanted prefixes and cleaning formatting"""
    if not title:
        return title
    
    # Remove "Mobile-uploads" or "Mobile uploads" from anywhere in the title
    title = re.sub(r'Mobile[-\s]*uploads?', '', title, flags=re.IGNORECASE)
    
    # Remove common Facebook post type prefixes
    prefixes_to_remove = [
        "Timeline-photos", "Timeline photos", 
        "Profile-pictures", "Profile pictures",
        "Cover-photos", "Cover photos",
        "Timeline", "Cover"
    ]
    
    for prefix in prefixes_to_remove:
        if title.lower().startswith(prefix.lower()):
            title = title[len(prefix):].strip()
            # Remove leading dash, space, or other punctuation
            while title and title[0] in '-_ ':
                title = title[1:].strip()
            break
    
    # Clean up multiple Mobile-uploads patterns
    title = re.sub(r'(Mobile[-\s]*uploads?\s*)+', '', title, flags=re.IGNORECASE)
    
    # Clean up any remaining leading/trailing dashes or spaces
    title = re.sub(r'^[-\s_]+|[-\s_]+$', '', title)
    
    # Clean up multiple consecutive dashes or spaces
    title = re.sub(r'[-\s_]{2,}', '-', title)
    
    return title

def clean_facebook_content(section):
    """Clean up Facebook content by removing UI elements and labels"""
    # Remove "Mobile uploads", "Timeline photos" labels from photo galleries
    for div in section.find_all('div'):
        div_text = div.get_text().strip()
        if div_text in ['Mobile uploads', 'Timeline photos', 'Profile pictures', 'Cover photos']:
            # Replace the text with empty string but keep the div structure
            div.string = ''
    
    return section

def fix_image_paths(section):
    """Fix image and video paths to point to the correct location"""
    # Fix img src attributes
    for img in section.find_all('img'):
        src = img.get('src', '')
        if src and not src.startswith('http'):
            # Handle Facebook media paths
            if 'your_facebook_activity/posts/media' in src:
                # Extract the path after "media/"
                media_path = src.split('your_facebook_activity/posts/media/')[-1]
                img['src'] = f"../input/media/{media_path}"
            elif not src.startswith('../input/media/'):
                img['src'] = f"../input/media/{src.split('/')[-1]}" if '/' in src else f"../input/media/{src}"
    
    # Fix video src attributes
    for video in section.find_all('video'):
        src = video.get('src', '')
        if src and not src.startswith('http'):
            # Handle Facebook media paths
            if 'your_facebook_activity/posts/media' in src:
                # Extract the path after "media/"
                media_path = src.split('your_facebook_activity/posts/media/')[-1]
                video['src'] = f"../input/media/{media_path}"
            elif not src.startswith('../input/media/'):
                video['src'] = f"../input/media/{src.split('/')[-1]}" if '/' in src else f"../input/media/{src}"
    
    # Fix href attributes in links
    for link in section.find_all('a'):
        href = link.get('href', '')
        if href and not href.startswith('http'):
            # Handle Facebook media paths
            if 'your_facebook_activity/posts/media' in href:
                # Extract the path after "media/"
                media_path = href.split('your_facebook_activity/posts/media/')[-1]
                link['href'] = f"../input/media/{media_path}"
            elif not href.startswith('../input/media/'):
                link['href'] = f"../input/media/{href.split('/')[-1]}" if '/' in href else f"../input/media/{href}"
    
    return section

def extract_css(content):
    """Extract CSS from original Facebook export"""
    css_match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if css_match:
        return css_match.group(1)
    return ""

def filter_facebook_posts(input_file):
    """Filter Facebook export to extract only status updates, photo posts, and video posts"""
    
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find all sections with class="_a6-g"
    all_sections = soup.find_all('section', class_='_a6-g')
    
    target_sections = []
    status_count = 0
    photo_count = 0
    video_count = 0
    
    for section in all_sections:
        # Get all header texts to determine post type
        headers = section.find_all('h2', class_=['_2ph_', '_a6-h', '_a6-i'])
        if headers:
            # Combine all header texts
            all_header_text = ' '.join([h.get_text() for h in headers]).lower()
            
            # Very specific matching to avoid false positives
            if 'ellie ellie updated her status' in all_header_text:
                target_sections.append(section)
                status_count += 1
            elif ('ellie ellie added a new photo' in all_header_text or 
                  ('ellie ellie added' in all_header_text and 'photo' in all_header_text)):
                target_sections.append(section)
                if 'video' in all_header_text:
                    video_count += 1
                else:
                    photo_count += 1
            elif ('ellie ellie added' in all_header_text and 'video' in all_header_text):
                target_sections.append(section)
                video_count += 1
    
    print(f"Filtered {len(target_sections)} posts from {len(all_sections)} total sections")
    print(f"  - Status updates: {status_count}")
    print(f"  - Photo posts: {photo_count}")
    print(f"  - Video posts: {video_count}")
    
    return target_sections, content

def create_facebook_blog(input_file, output_file):
    """Convert Facebook posts into blog format"""
    
    # Filter posts
    sections, original_content = filter_facebook_posts(input_file)
    
    posts = []
    photo_only_count = 0
    
    for section in sections:
        # Clean Facebook content first (remove UI labels)
        section = clean_facebook_content(section)
        
        # Fix image paths
        section = fix_image_paths(section)
        
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
        meaningful_caption = ""
        
        if content_div:
            # Look for text content in the main content area
            text_divs = content_div.find_all('div', recursive=False)
            for div in text_divs:
                text = div.get_text().strip()
                if text and not text.startswith('Updated '):
                    post_text = text
                    break
        
        # If no main text content, look for meaningful photo captions
        if not post_text:
            # Look for captions in photo gallery areas (class _3-95 often contains captions)
            caption_divs = section.find_all('div', class_='_3-95')
            for div in caption_divs:
                caption_text = div.get_text().strip()
                # Filter out Facebook UI labels and unwanted text
                if (caption_text and 
                    len(caption_text) > 5 and  # Must be more than just a few characters
                    'Mobile uploads' not in caption_text and  # Exclude Mobile uploads
                    'Mobile-uploads' not in caption_text and  # Exclude Mobile-uploads
                    caption_text not in ['Timeline photos', 'Profile pictures', 'Cover photos'] and
                    not caption_text.startswith('Click for') and  # Skip video click prompts
                    not caption_text.startswith('Updated ') and  # Skip update timestamps
                    len(caption_text) < 100):  # Not too long to be main content
                    meaningful_caption = caption_text
                    break
        
        # Determine title
        if post_text:
            title = extract_first_sentence(post_text)
        elif meaningful_caption:
            title = meaningful_caption
        else:
            # This is a photo-only post with no meaningful captions
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
            'html': clean_facebook_content(section)
        })
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x['datetime'], reverse=True)
    
    # Generate blog HTML
    blog_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ellie's Facebook Posts - Blog Format</title>
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
            font-size: 18px;
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
            font-size: 3rem;
            margin: 0 0 12px 0;
            color: #1c1e21;
            font-weight: 700;
        }}
        
        .blog-header p {{
            font-size: 1.3rem;
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
            font-size: 1.6rem;
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
            font-size: 1.3rem;
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
                font-size: 16px;
            }}
            
            .blog-header {{
                padding: 20px 16px;
                margin-bottom: 24px;
            }}
            
            .blog-header h1 {{
                font-size: 2.2rem;
            }}
            
            .blog-header p {{
                font-size: 1.1rem;
            }}
            
            .post-header {{
                padding: 16px 20px;
            }}
            
            .post-title {{
                font-size: 1.3rem;
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
                font-size: 15px;
            }}
            
            .blog-header {{
                padding: 16px 12px;
            }}
            
            .blog-header h1 {{
                font-size: 1.9rem;
            }}
            
            .post-header {{
                padding: 14px 16px;
            }}
            
            .post-title {{
                font-size: 1.1rem;
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
        
        /* Increase font size for Facebook content text */
        .facebook-content {{
            font-size: 16px;
            line-height: 1.5;
        }}
        
        .facebook-content ._3-95 {{
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 8px;
        }}
        
        .facebook-content ._2pin {{
            font-size: 16px;
            line-height: 1.5;
        }}
        
        .facebook-content ._a6-p {{
            font-size: 16px;
            line-height: 1.5;
        }}
        
        /* Include original Facebook styles */
        {extract_css(original_content)}
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
    
    return len(posts)

if __name__ == "__main__":
    # Default file paths
    input_file = "processing/input/your_posts__check_ins__photos_and_videos_1.html"
    
    # Generate timestamp for unique output filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = f"processing/output/fb-posts-{timestamp}.html"
    
    try:
        create_facebook_blog(input_file, output_file)
        print("\n✅ Blog creation completed successfully!")
        print(f"📁 Input: {input_file}")
        print(f"📄 Output: {output_file}")
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print(f"Please ensure {input_file} exists in the current directory.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")