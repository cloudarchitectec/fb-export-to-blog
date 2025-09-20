"""
Helper functions for Facebook Export to Blog Converter

This file contains utility functions that use the configuration variables.
"""

from config import *

def get_username_patterns():
    """
    Generate username patterns for post type identification.
    Returns patterns with the configured username inserted.
    """
    patterns = {}
    for post_type, pattern_list in POST_TYPE_PATTERNS.items():
        patterns[post_type] = [
            pattern.format(username=FACEBOOK_USERNAME.lower())
            for pattern in pattern_list
        ]
    return patterns

def get_output_filename():
    """
    Generate the output filename based on configuration.
    """
    from datetime import datetime
    
    if INCLUDE_TIMESTAMP:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"{OUTPUT_DIR}/{OUTPUT_PREFIX}-{timestamp}.html"
    else:
        return f"{OUTPUT_DIR}/{OUTPUT_PREFIX}.html"

def get_media_path_prefix():
    """
    Get the media path prefix for fixing image/video sources.
    """
    return RELATIVE_MEDIA_PATH

def validate_config():
    """
    Validate configuration settings and warn about potential issues.
    """
    warnings = []
    if not FACEBOOK_USERNAME:
        warnings.append(
            "⚠️  FACEBOOK_USERNAME is not set. "
        )
    else:
        print(f"Your Facebook username is: {FACEBOOK_USERNAME}")
    
    if not any([INCLUDE_PHOTOS, INCLUDE_VIDEOS, INCLUDE_STATUS_UPDATES]):
        warnings.append(
            "⚠️  All post types are disabled. No posts will be included in output."
        )
    
    return warnings