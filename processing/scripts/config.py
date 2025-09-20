"""
This file contains all configurable parameters for the Facebook post conversion scripts.
Modify these values to customisze the behavior for your specific Facebook export data.
"""

# ============================================================================
# USER CONFIGURATION
# ============================================================================

# Your Facebook display name (case-insensitive matching)
# This is used to identify your posts vs. other people's posts/interactions
FACEBOOK_USERNAME = "Ellie Ellie"
BLOG_TITLE = "The Ellie Edition"
BLOG_DESCRIPTION = "A curated archive of everyday thoughts and snapshots beyond Facebook."

# Input files from Facebook export

INPUT_FILE = "processing/input/your_posts__check_ins__photos_and_videos_1.html" # The main posts HTML file from your Facebook data download
MEDIA_DIR = "processing/input/media" # Media directory path (where Facebook photos/videos are stored)

# Output directory and file settings
OUTPUT_DIR = "processing/output"
INCLUDE_TIMESTAMP = True    # Whether to add timestamp to output filename
OUTPUT_PREFIX = "fb-posts"  # Output will be: fb-posts-YYYYMMDD-HHMMSS.html

# Processing options
SKIP_EMPTY_POSTS = True         # Skip posts with no meaningful content
REVERSE_CHRONOLOGICAL = True    # Show newest posts first (True) or oldest first (False)
INCLUDE_PHOTOS = True           # Include photo posts in output
INCLUDE_VIDEOS = True           # Include video posts in output
INCLUDE_STATUS_UPDATES = False  # Include text-only status updates
MAX_TITLE_LENGTH = 40           # Maximum title length for generated post titles

# Image and video processing
FIX_MEDIA_PATHS = True         # Automatically fix broken image/video paths
RELATIVE_MEDIA_PATH = "../input/media"  # Relative path from output to media directory

# ============================================================================
# CONTENT FILTERING CONFIGURATION
# ============================================================================

# Facebook clutter terms to remove from post titles and content
# These are common Facebook-generated labels that add no meaningful content
FACEBOOK_CLUTTER_TERMS = [
    "Timeline photos", "Timeline-photos",
    "Profile pictures", "Profile-pictures", 
    "Cover photos", "Cover-photos",
    "Mobile uploads", "Mobile-uploads",
    "Timeline", "Cover"
]

# Post type identification patterns
# These patterns help categorize different types of Facebook posts
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