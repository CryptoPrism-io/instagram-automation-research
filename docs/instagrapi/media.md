# Instagrapi Media Documentation

> **Source**: https://subzeroid.github.io/instagrapi/usage-guide/media.html

This document provides comprehensive information about media-related operations using the instagrapi library for Instagram's Private API.

## 📋 Media Identification Terms

Understanding Instagram's media identification system:

### Media ID Types
- **`media_id`**: String ID format (e.g., "2277033926878261772_1903424587")
- **`media_pk`**: Integer primary key format
- **`code`**: Short media code/slug used in URLs
- **`url`**: Full media publication URL

### Media Type Classifications
- **Photo**: `media_type=1`
- **Video**: `media_type=2, product_type=feed`
- **IGTV**: `media_type=2, product_type=igtv`
- **Reels**: `media_type=2, product_type=clips`
- **Album/Carousel**: `media_type=8`

## 🎯 Core Media Functionality

### 1. Media Information Retrieval

#### Basic Media Info
```python
from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)

# Get media information by ID
media_info = cl.media_info(media_id)

# Get media info by URL
media_url = "https://instagram.com/p/ABC123/"
media_info = cl.media_info_by_url(media_url)

# Media info structure
print(f"Media ID: {media_info.id}")
print(f"Media Type: {media_info.media_type}")
print(f"Caption: {media_info.caption_text}")
print(f"Like Count: {media_info.like_count}")
print(f"Comment Count: {media_info.comment_count}")
```

#### Advanced Media Properties
```python
# Access detailed media properties
def analyze_media(media_info):
    return {
        'id': media_info.id,
        'pk': media_info.pk,
        'code': media_info.code,
        'taken_at': media_info.taken_at,
        'media_type': media_info.media_type,
        'product_type': media_info.product_type,
        'thumbnail_url': media_info.thumbnail_url,
        'user': {
            'username': media_info.user.username,
            'full_name': media_info.user.full_name,
            'is_verified': media_info.user.is_verified
        },
        'location': media_info.location.name if media_info.location else None,
        'caption': media_info.caption_text,
        'like_count': media_info.like_count,
        'comment_count': media_info.comment_count,
        'view_count': media_info.view_count,  # For videos
        'play_count': media_info.play_count,  # For videos
    }
```

### 2. Media Download Operations

#### Download Photos
```python
# Download photo to local file
photo_path = cl.photo_download(media_pk, folder="downloads/")
print(f"Photo downloaded to: {photo_path}")

# Download with custom filename
photo_path = cl.photo_download(
    media_pk,
    folder="downloads/",
    filename="custom_name.jpg"
)
```

#### Download Videos
```python
# Download video
video_path = cl.video_download(media_pk, folder="downloads/")

# Download video by URL
video_url = "https://instagram.com/p/ABC123/"
video_path = cl.video_download_by_url(video_url, folder="downloads/")
```

#### Download Albums/Carousels
```python
# Download entire album
album_paths = cl.album_download(media_pk, folder="downloads/")
for path in album_paths:
    print(f"Downloaded: {path}")
```

#### Download IGTV
```python
# Download IGTV video
igtv_path = cl.igtv_download(media_pk, folder="downloads/")
```

### 3. Media Upload Operations

#### Photo Upload
```python
# Basic photo upload
media = cl.photo_upload(
    path="path/to/photo.jpg",
    caption="Your caption here #hashtag"
)
print(f"Uploaded media ID: {media.id}")

# Advanced photo upload with options
media = cl.photo_upload(
    path="path/to/photo.jpg",
    caption="Caption with location and tags",
    usertags=[
        {
            "user": {"pk": user_id},
            "position": [0.5, 0.5]  # x, y position (0-1 scale)
        }
    ],
    location=location_info,  # Location object from location search
    extra_data={
        "custom_accessibility_caption": "Alt text for accessibility",
        "disable_comments": False,
        "like_and_view_counts_disabled": False
    }
)
```

#### Video Upload
```python
# Basic video upload
media = cl.video_upload(
    path="path/to/video.mp4",
    caption="Video caption #video"
)

# Video with thumbnail
media = cl.video_upload(
    path="path/to/video.mp4",
    caption="Video with custom thumbnail",
    thumbnail="path/to/thumbnail.jpg"
)
```

#### Album/Carousel Upload
```python
# Upload multiple media as album
media_files = [
    {"type": "photo", "path": "photo1.jpg"},
    {"type": "video", "path": "video1.mp4"},
    {"type": "photo", "path": "photo2.jpg"}
]

album = cl.album_upload(
    media_files,
    caption="Album caption #carousel"
)
```

#### IGTV Upload
```python
# Upload IGTV video
igtv = cl.igtv_upload(
    path="path/to/long_video.mp4",
    title="IGTV Title",
    caption="IGTV description #igtv",
    thumbnail="path/to/cover.jpg"
)
```

#### Reels Upload
```python
# Upload Reels video
reel = cl.clip_upload(
    path="path/to/reel.mp4",
    caption="Reels caption #reels",
    extra_data={
        "audio_cluster_id": "audio_id",  # Optional background music
        "share_to_feed": True  # Also post to main feed
    }
)
```

### 4. Media Interaction Operations

#### Like/Unlike Media
```python
# Like a post
success = cl.media_like(media_id)
print(f"Like successful: {success}")

# Unlike a post
success = cl.media_unlike(media_id)
print(f"Unlike successful: {success}")

# Check if media is liked
is_liked = cl.media_info(media_id).has_liked
```

#### Save/Unsave Media
```python
# Save media to saved collection
success = cl.media_save(media_id)

# Unsave media
success = cl.media_unsave(media_id)

# Add to specific collection
success = cl.media_save_to_collection(media_id, collection_id)
```

#### Archive/Unarchive Media
```python
# Archive your own post
success = cl.media_archive(media_id)

# Unarchive post
success = cl.media_unarchive(media_id)
```

#### Delete Media
```python
# Delete your own media
success = cl.media_delete(media_id)
print(f"Deletion successful: {success}")
```

### 5. Media Editing Operations

#### Edit Caption
```python
# Edit post caption
success = cl.media_edit(
    media_id=media_id,
    caption="New caption #updated"
)
```

#### Edit User Tags
```python
# Update user tags on media
success = cl.media_edit_usertags(
    media_id=media_id,
    usertags=[
        {
            "user": {"pk": user_id},
            "position": [0.3, 0.7]
        }
    ]
)
```

## 📊 Media Analytics & Insights

### View Media Statistics
```python
def get_media_stats(media_id):
    media = cl.media_info(media_id)

    return {
        'engagement_rate': (media.like_count + media.comment_count) /
                          cl.user_info(media.user.pk).follower_count * 100,
        'likes': media.like_count,
        'comments': media.comment_count,
        'views': media.view_count if media.media_type == 2 else None,
        'saves': media.save_count if hasattr(media, 'save_count') else None,
        'shares': media.share_count if hasattr(media, 'share_count') else None
    }
```

### Media Likers and Comments
```python
# Get users who liked the media
likers = cl.media_likers(media_id)
for user in likers:
    print(f"{user.username} - {user.full_name}")

# Get comments on media
comments = cl.media_comments(media_id)
for comment in comments:
    print(f"{comment.user.username}: {comment.text}")
```

## 🔍 Media Search & Discovery

### Search Media by User
```python
# Get user's media
user_medias = cl.user_medias(user_id, amount=20)
for media in user_medias:
    print(f"Media: {media.code} - {media.caption_text[:50]}...")
```

### Search Media by Hashtag
```python
# Get recent media for hashtag
hashtag_medias = cl.hashtag_medias_recent("python", amount=10)
for media in hashtag_medias:
    print(f"Found: {media.code}")
```

### Search Media by Location
```python
# Get media from specific location
location_medias = cl.location_medias_recent(location_pk, amount=10)
```

## 🛠️ Advanced Media Operations

### Media URL Conversion
```python
# Convert between different ID formats
def convert_media_ids(media_input):
    if media_input.startswith('http'):
        # URL to media_id
        media_id = cl.media_id_from_url(media_input)
    else:
        # Assume it's already an ID
        media_id = media_input

    # Get media info
    media = cl.media_info(media_id)

    return {
        'media_id': media.id,
        'media_pk': media.pk,
        'code': media.code,
        'url': f"https://instagram.com/p/{media.code}/"
    }
```

### Bulk Media Operations
```python
def bulk_like_user_posts(username, max_likes=10):
    """Like recent posts from a user"""
    user_id = cl.user_id_from_username(username)
    medias = cl.user_medias(user_id, amount=max_likes)

    liked_count = 0
    for media in medias:
        if not media.has_liked:
            success = cl.media_like(media.id)
            if success:
                liked_count += 1
                time.sleep(random.randint(1, 3))  # Random delay

    return liked_count
```

### Media Quality Optimization
```python
def optimize_upload_settings():
    """Configure optimal upload settings"""
    cl.set_upload_quality(95)  # JPEG quality (1-100)
    cl.set_video_max_duration(60)  # Max video duration in seconds
    cl.set_photo_max_size(1080)  # Max photo resolution
```

## 🔐 Privacy & Safety

### Respect Privacy Settings
```python
def safe_media_access(media_id):
    """Safely access media with error handling"""
    try:
        media = cl.media_info(media_id)
        if media.user.is_private and not media.user.friendship_status.following:
            print("Cannot access private user's media")
            return None
        return media
    except Exception as e:
        print(f"Error accessing media: {e}")
        return None
```

### Rate Limiting for Media Operations
```python
import time
import random

def rate_limited_media_operation(operation, *args, **kwargs):
    """Execute media operation with rate limiting"""
    result = operation(*args, **kwargs)

    # Add random delay after each operation
    delay = random.uniform(1, 3)
    time.sleep(delay)

    return result

# Usage
# rate_limited_media_operation(cl.media_like, media_id)
```

## 📝 Best Practices for Media Operations

### 1. **Upload Best Practices**
```python
# Optimal image specifications
OPTIMAL_SPECS = {
    'photo': {
        'width': 1080,
        'height': 1080,  # or 1350 for portrait
        'format': 'JPEG',
        'quality': 95
    },
    'video': {
        'width': 1080,
        'height': 1920,  # for stories/reels
        'format': 'MP4',
        'codec': 'H.264',
        'max_duration': 60,  # seconds
        'fps': 30
    }
}
```

### 2. **Error Handling**
```python
from instagrapi.exceptions import MediaError, ClientError

def robust_media_upload(path, caption):
    """Upload with comprehensive error handling"""
    try:
        media = cl.photo_upload(path, caption)
        return media
    except MediaError as e:
        print(f"Media error: {e}")
        return None
    except ClientError as e:
        print(f"Client error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

### 3. **Content Guidelines**
- Ensure content complies with Instagram's community guidelines
- Use appropriate hashtags and captions
- Respect copyright and intellectual property
- Include accessibility descriptions when possible

This comprehensive media documentation covers all aspects of working with Instagram media through the instagrapi library.