# Facebook Export to Blog Converter

This project converts Facebook HTML export files into a clean, responsive blog-style website. It filters only meaningful posts (status updates and photos) and presents them in chronological order with a modern design.

## Overview

The tool processes Facebook's "Your information" export, specifically the posts data, and transforms it into a readable blog format while:
- Filtering out low-value content (likes, shares, comments, etc.)
- Removing Facebook UI clutter 
- Creating responsive design for all devices
- Organizing posts chronologically (newest first)
- Fixing image paths to work locally
- Generating clean, SEO-friendly titles

## Quick Start

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Prepare your Facebook export:**
   - Go to Facebook Settings > Your Facebook Information > Download Your Information
   - Select "Posts" in the data categories
   - Download and extract the HTML export
   - Copy `your_posts__check_ins__photos_and_videos_1.html` to the `processing/input/` directory
   - Copy the `media/` folder from the export to `processing/input/media/`

3. **Run the converter:**
   ```bash
   python3 processing/scripts/create_fb_posts.py
   ```

4. **View your blog:**
   - Open `processing/output/fb-posts.html` in any web browser
   - All images will work if your `input/media/` folder structure is maintained

## File Structure

```
fb_posts/
├── requirements.txt                    # Python dependencies
├── README.md                          # This file
├── original/                          # Facebook export files (archived)
│   ├── your_facebook_activity/
│   │   └── posts/
│   │       └── media/                 # Photos and videos
│   └── files/                         # Profile pics, etc.
└── processing/                        # Working directory
    ├── input/                         # Input files
    │   ├── your_posts__check_ins__photos_and_videos_1.html  # Input file
    │   └── media/                     # Photos and videos
    ├── output/                        # Generated files
    │   └── fb-posts.html              # Final blog output
    └── scripts/                       # Utility scripts
        ├── create_fb_posts.py         # Main script (recommended)
        ├── analyze_file.py            # Analyze post content
        ├── count_unique.py            # Count post statistics  
        ├── debug_extract.py           # Debug extraction issues
        ├── extract_final.py           # Extract specific posts
        ├── extract_posts.py           # Basic post extraction
        └── fix_image_paths.py         # Fix image references
```

## Main Script: create_fb_posts.py

**Purpose:** One-stop solution to convert Facebook export to blog format

**Input:** `input/your_posts__check_ins__photos_and_videos_1.html` (Facebook export)
**Output:** `output/fb-posts.html` (Responsive blog)

**Features:**
- Filters only status updates and photo posts (excludes likes, shares, etc.)
- Removes Facebook clutter ("Timeline photos", "Ellie Ellie added...", etc.)
- Creates responsive design (mobile/tablet/desktop)
- Organizes posts chronologically (newest first)
- Generates clean YYYY-MM-DD-{title} format
- Fixes image paths automatically
- Includes original Facebook CSS for proper rendering


## Utility Scripts

- `analyze_file.py`: Analyzes post content and categorizes different types of posts.
- `count_unique.py`: Counts unique posts and provides statistics breakdown.
- `debug_extract.py`: Debug tool to examine Facebook HTML structure and section classification.
- `extract_final.py`: Extracts only status updates and photo posts to a filtered HTML file.
- `extract_posts.py`: Basic post extraction utility for initial data processing.
- `fix_image_paths.py`: Fixes image paths in existing HTML files to point to correct locations.


## Output Features

**Responsive Design:**
- Desktop: Full-width layout (up to 1200px)
- Tablet: Optimized for 768px and below
- Mobile: Touch-friendly design for 480px and below

**Post Organization:**
- Chronological order (newest posts first)
- Clean titles with date prefix (YYYY-MM-DD-{content})
- Statistics dashboard showing totals and breakdowns
- Working image galleries with local file support

**Clean Content:**
- Removes Facebook-generated headers ("Ellie Ellie added...")
- Strips redundant labels ("Timeline photos", "Mobile uploads")
- Preserves original post content and formatting
- Maintains Facebook's original CSS for proper display

## Troubleshooting

**Missing images:**
- Ensure the `input/media/` directory structure is maintained
- Images should be in `processing/input/media/`
- The script automatically fixes relative paths

**No posts found:**
- Verify the input file name matches exactly
- Check that the file contains Facebook post data
- Run `analyze_file.py` to debug content structure

**Performance issues:**
- The script processes 1500+ posts, expect 30-60 seconds runtime
- Large image collections may take longer
- Use `extract_final.py` first if you need intermediate debugging

**Wrong post filtering:**
- Modify the filtering logic in `filter_facebook_posts()` if needed
- Use `debug_extract.py` to examine post structure

## Output Statistics

Typical results from a complete Facebook export:
- **Total sections processed:** ~3,000
- **Filtered posts:** ~1,840 (status updates + photos + videos)
- **Status updates:** ~543 (text-only posts)
- **Photo posts:** ~1,022 (posts with images)
- **Video posts:** ~275 (posts with videos)
- **Photo-only posts:** ~25 (posts with media but no text)
- **Text posts:** ~1,815 (posts with meaningful content)
- **Date range:** 2009-2025 (varies by user)
- **Output file size:** ~7MB (responsive HTML with all media)

The tool successfully filters out roughly 40% of the original content, keeping only the most meaningful posts while maintaining full fidelity of your actual content and media.