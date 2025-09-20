# Facebook Export to Blog Converter

*[This is a vibe coding project with limited verification - use at your own risk.🤖]*

Convert Facebook HTML export into a clean, responsive blog-style website. Filters meaningful posts (status updates and photos) and presents them chronologically with modern design.

##### Example Output

![Example Blog Output](processing/output/example.png)

## Features

- Filters only status updates and photo posts (excludes likes, shares, etc.)
- Removes Facebook clutter ("Timeline photos", "Mobile uploads", etc.)
- Configurable username filtering
- Creates responsive design (mobile/tablet/desktop)
- Organizes posts chronologically (newest first)
- Generates clean YYYY-MM-DD-{title} format
- Fixes image paths automatically
- Generates clean, SEO-friendly titles
- Includes original Facebook CSS for proper rendering

## Quick Start

### Prerequisites
- Code editor (VS Code recommended)
- Python 3 and pip installed

### Setup

1. **Download Facebook data:**
   - Go to Facebook → Settings → Your Facebook Information → Download Your Information
   - Select "Posts" and download HTML format
   - Extract the files

2. **Prepare files:**
   - Copy `your_posts__check_ins__photos_and_videos_1.html` to the `processing/input/` directory
   - Copy the `media/` folder from the export to `processing/input/media/`
   
3. **Configure for your username:**
   - Open `processing/scripts/config.py`
   - (REQUIRED) Update **`FACEBOOK_USERNAME`** with your actual Facebook display name. 
   - Optional settings:
      - **`INPUT_FILE`** - Path to your Facebook posts HTML file
      - **`OUTPUT_DIR`** - Where to save the generated blog
      - **`BLOG_TITLE`** - Title for your blog page
      - **`INCLUDE_PHOTOS`** - Include photo posts (True/False)
      - **`INCLUDE_VIDEOS`** - Include video posts (True/False)  
      - **`INCLUDE_STATUS_UPDATES`** - Include text status updates (True/False)
      - **`SKIP_EMPTY_POSTS`** - Skip posts with no meaningful content (True/False)
      - **`REVERSE_CHRONOLOGICAL`** - Show newest posts first (True/False)
      - **`INCLUDE_TIMESTAMP`** - Add timestamp to output filename (True/False)
      - **`FACEBOOK_CLUTTER_TERMS`** - List of Facebook labels to remove

4. **Install and run:**
   ```bash
   pip3 install -r requirements.txt
   python3 processing/scripts/create_fb_posts.py
   ```

5. **View results:**
   - Open `processing/output/fb-posts-YYYYMMDD-HHMMSS.html` in your browser

## File Structure

```
fb_posts/
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── original/                 # Facebook export archive
│   └── your_facebook_activity/
├── processing/
│   ├── input/                # Your Facebook files go here
│   │   ├── your_posts__*.html
│   │   └── media/
│   ├── output/               # Generated blog
│   │   └── fb-posts-YYYYMMDD-HHMMSS.html
│   └── scripts/              # Converter tools
│       ├── config.py             # ⚙️ Configuration file  
│       ├── create_fb_posts.py    # 🌟 Main converter
│       ├── analyze_file.py       # Analyze content
│       ├── count_unique.py       # Post statistics
│       ├── debug_extract.py      # Debug tool
│       ├── extract_final.py      # Filter posts
│       ├── extract_posts.py      # Basic extraction
│       └── fix_image_paths.py    # Fix image links
```

## Scripts Overview
- `config.py` - Settings and customization
- `create_fb_posts.py` - Complete Facebook-to-blog converter (main script)
- `analyze_file.py` - Categorize and analyze post types
- `count_unique.py` - Generate post statistics
- `debug_extract.py` - Debug HTML structure issues
- `extract_final.py` - Filter meaningful posts only
- `extract_posts.py` - Basic post extraction
- `fix_image_paths.py` - Repair broken image links

## Results

The tool filters ~40% of Facebook content, keeping only meaningful posts while preserving all your actual content and media.
