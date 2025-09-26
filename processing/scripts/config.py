"""
Edit the settings below to control how your Facebook posts are turned into a blog.
Just change the values in quotes ("...") or True/False as needed.
"""

# ============================================================================
# BASIC SETTINGS - CHANGE THESE!
# ============================================================================

# Your Facebook display name (how your name appears on Facebook)
# This helps the tool find your posts (not your friends')
FACEBOOK_USERNAME = "Ellie Ellie"

# The title and description for your blog page
BLOG_TITLE = "The Ellie Edition"
BLOG_DESCRIPTION = "A curated archive of everyday thoughts and snapshots beyond Facebook."

# ============================================================================
# FILE LOCATIONS - USUALLY DON'T NEED TO CHANGE
# ============================================================================

# The main Facebook HTML file you downloaded (should be in processing/input/)
INPUT_FILE = "processing/input/your_posts__check_ins__photos_and_videos_1.html"

# The folder with your Facebook photos and videos (should be in processing/input/media)
MEDIA_DIR = "processing/input/media"

# Where to save your blog (the output folder)
OUTPUT_DIR = "processing/output"

# Add date and time to the blog filename? (True = yes, False = no)
INCLUDE_TIMESTAMP = True

# The start of the blog filename (don't change unless you want)
OUTPUT_PREFIX = "fb-posts"  # Example: fb-posts-YYYYMMDD-HHMMSS.html

# ============================================================================
# WHAT TO INCLUDE? (True = yes, False = no)
# ============================================================================

# Skip posts that are empty or have no real content
SKIP_EMPTY_POSTS = True

# Show newest posts first? (True = newest first, False = oldest first)
REVERSE_CHRONOLOGICAL = True

# Include photo posts?
INCLUDE_PHOTOS = True

# Include video posts?
INCLUDE_VIDEOS = True

# Include text-only status updates?
INCLUDE_STATUS_UPDATES = False

# Shorten long blog post titles (number of letters)
MAX_TITLE_LENGTH = 40

# ============================================================================
# IMAGE AND VIDEO SETTINGS
# ============================================================================

# Try to fix broken image/video links automatically?
FIX_MEDIA_PATHS = True

# Where the blog should look for your photos (usually don't change)
RELATIVE_MEDIA_PATH = "../input/media"

# ============================================================================
# ADVANCED: FILTERING FACEBOOK CLUTTER (EXTRA)
# ============================================================================

# Words Facebook adds to your posts that you probably don't want in your blog titles
FACEBOOK_CLUTTER_TERMS = [
    "Timeline photos", "Timeline-photos",
    "Profile pictures", "Profile-pictures", 
    "Cover photos", "Cover-photos",
    "Mobile uploads", "Mobile-uploads",
    "Timeline", "Cover"
]

# How the tool recognizes different types of posts (don't change unless you know what you're doing)
POST_TYPE_PATTERNS = {
    "status_update": [
        "{username} updated her status",
        "{username} updated his status", 
        "{username} updated their status"
    ],
    "photo_post": [
        "{username} added a new photo",
        "{username} added new photos",
        "{username} added",  # Generic "added" with photo context
    ],
    "video_post": [
        "{username} added a new video",
        "{username} added new videos"
    ]
}