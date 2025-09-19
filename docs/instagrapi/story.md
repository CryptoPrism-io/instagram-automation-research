# Instagrapi Story Documentation

> **Source**: https://subzeroid.github.io/instagrapi/usage-guide/story.html

This document provides comprehensive information about Instagram Stories operations using the instagrapi library for Instagram's Private API.

## 📱 Story Information & Retrieval

### Basic Story Operations

#### Get User Stories
```python
from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)

# Get stories for a specific user
user_stories = cl.user_stories(user_id)

# Process stories
for story in user_stories:
    print(f"Story ID: {story.pk}")
    print(f"Media Type: {story.media_type}")  # 1=photo, 2=video
    print(f"Taken At: {story.taken_at}")
    print(f"Expires At: {story.expiring_at}")
```

#### Get Story Information
```python
# Get detailed story information
story_info = cl.story_info(story_pk)

# Story properties
def analyze_story(story):
    return {
        'id': story.pk,
        'code': story.code,
        'media_type': story.media_type,
        'user': {
            'username': story.user.username,
            'full_name': story.user.full_name
        },
        'taken_at': story.taken_at,
        'expiring_at': story.expiring_at,
        'thumbnail_url': story.thumbnail_url,
        'video_url': story.video_url if story.media_type == 2 else None,
        'view_count': story.view_count,
        'has_audio': story.has_audio if story.media_type == 2 else None
    }
```

### Story Download Operations

#### Download Story Media
```python
# Download story (photo or video)
story_path = cl.story_download(story_pk, folder="downloads/stories/")
print(f"Story downloaded to: {story_path}")

# Download story by URL
story_url = "https://instagram.com/stories/username/story_id/"
story_pk = cl.story_pk_from_url(story_url)
story_path = cl.story_download(story_pk)
```

#### Bulk Story Download
```python
def download_user_stories(username, folder="downloads/"):
    """Download all current stories from a user"""
    user_id = cl.user_id_from_username(username)
    stories = cl.user_stories(user_id)

    downloaded_files = []
    for story in stories:
        try:
            file_path = cl.story_download(story.pk, folder=folder)
            downloaded_files.append(file_path)
            print(f"Downloaded: {story.pk}")
        except Exception as e:
            print(f"Failed to download story {story.pk}: {e}")

    return downloaded_files
```

## 📤 Story Upload Operations

### Photo Story Upload

#### Basic Photo Story
```python
# Upload photo story
story = cl.photo_upload_to_story(
    path="path/to/photo.jpg",
    caption="Story caption"
)
print(f"Story uploaded: {story.pk}")
```

#### Photo Story with Advanced Options
```python
from instagrapi.types import StoryMention, StoryLink, StoryLocation

# Upload photo story with mentions, links, and location
story = cl.photo_upload_to_story(
    path="path/to/photo.jpg",
    caption="Check out this amazing place! @friend",
    mentions=[
        StoryMention(
            user=cl.user_info_by_username("friend"),
            x=0.5,  # Position x (0-1)
            y=0.3   # Position y (0-1)
        )
    ],
    links=[
        StoryLink(
            webUri="https://example.com",
            x=0.5,
            y=0.8
        )
    ],
    locations=[
        StoryLocation(
            location=location_info,  # From location search
            x=0.5,
            y=0.9
        )
    ]
)
```

### Video Story Upload

#### Basic Video Story
```python
# Upload video story
story = cl.video_upload_to_story(
    path="path/to/video.mp4",
    caption="Video story caption"
)
```

#### Video Story with Thumbnail
```python
# Upload video story with custom thumbnail
story = cl.video_upload_to_story(
    path="path/to/video.mp4",
    caption="Video with custom thumbnail",
    thumbnail="path/to/thumbnail.jpg"
)
```

### Advanced Story Upload Features

#### Story with Hashtags
```python
from instagrapi.types import StoryHashtag

story = cl.photo_upload_to_story(
    path="path/to/photo.jpg",
    caption="Story with hashtags",
    hashtags=[
        StoryHashtag(
            hashtag="#photography",
            x=0.5,
            y=0.2
        ),
        StoryHashtag(
            hashtag="#travel",
            x=0.5,
            y=0.7
        )
    ]
)
```

#### Story with Stickers
```python
from instagrapi.types import StorySticker

story = cl.photo_upload_to_story(
    path="path/to/photo.jpg",
    stickers=[
        StorySticker(
            type="time",  # time, location, mention, etc.
            x=0.5,
            y=0.1
        )
    ]
)
```

#### Close Friends Story
```python
# Upload story visible only to close friends
story = cl.photo_upload_to_story(
    path="path/to/photo.jpg",
    caption="Close friends only!",
    extra_data={
        "audience": "besties"  # Close friends only
    }
)
```

## 📊 Story Analytics & Interactions

### Story Viewers
```python
# Get list of users who viewed the story
viewers = cl.story_viewers(story_pk)

for viewer in viewers:
    print(f"Viewer: {viewer.username} - {viewer.full_name}")

# Get viewer count
viewer_count = len(viewers)
print(f"Total viewers: {viewer_count}")
```

### Story Interactions

#### Like/Unlike Stories
```python
# Like a story
success = cl.story_like(story_pk)
print(f"Story liked: {success}")

# Unlike a story
success = cl.story_unlike(story_pk)
print(f"Story unliked: {success}")
```

#### Story Reactions
```python
# React to story with emoji
success = cl.story_reaction(story_pk, emoji="❤️")
print(f"Story reaction sent: {success}")
```

## 🛠️ Story Builder & Formatting

### Story Builder for Advanced Creation
```python
from instagrapi.story import StoryBuilder

# Create story with multiple elements
builder = StoryBuilder()

# Add background
builder.add_background("path/to/background.jpg")

# Add text overlay
builder.add_text(
    text="Hello World!",
    x=0.5,
    y=0.3,
    font_size=24,
    color="#FFFFFF"
)

# Add mention
builder.add_mention(
    username="friend",
    x=0.5,
    y=0.7
)

# Build and upload story
story_media = builder.build()
story = cl.story_upload(story_media)
```

### Story Templates
```python
def create_branded_story(image_path, title, subtitle):
    """Create a branded story template"""
    builder = StoryBuilder()

    # Add main image
    builder.add_background(image_path)

    # Add brand overlay
    builder.add_text(
        text=title,
        x=0.5,
        y=0.2,
        font_size=32,
        color="#000000",
        background_color="#FFFFFF",
        background_opacity=0.8
    )

    builder.add_text(
        text=subtitle,
        x=0.5,
        y=0.8,
        font_size=16,
        color="#666666"
    )

    return builder.build()
```

## 📺 Story Highlights

### View Story Highlights
```python
# Get user's story highlights
highlights = cl.user_highlights(user_id)

for highlight in highlights:
    print(f"Highlight: {highlight.title}")
    print(f"Cover URL: {highlight.cover_media.thumbnail_url}")

    # Get stories in highlight
    highlight_stories = cl.highlight_info(highlight.pk).items
    for story in highlight_stories:
        print(f"  Story: {story.pk}")
```

### Create Story Highlight
```python
# Create new highlight from story IDs
highlight = cl.highlight_create(
    title="Travel Adventures",
    story_ids=[story_pk1, story_pk2, story_pk3]
)
print(f"Highlight created: {highlight.pk}")
```

### Manage Existing Highlights
```python
# Add stories to existing highlight
success = cl.highlight_add_stories(highlight_pk, [new_story_pk])

# Remove stories from highlight
success = cl.highlight_remove_stories(highlight_pk, [story_pk_to_remove])

# Change highlight title
success = cl.highlight_change_title(highlight_pk, "New Title")

# Change highlight cover
success = cl.highlight_change_cover(highlight_pk, "path/to/cover.jpg")

# Delete highlight
success = cl.highlight_delete(highlight_pk)
```

## 🔍 Story Discovery & Search

### Find Stories by Hashtag
```python
def find_stories_by_hashtag(hashtag, max_stories=10):
    """Find recent stories containing a hashtag"""
    # Get recent media with hashtag
    media_list = cl.hashtag_medias_recent(hashtag, amount=100)

    story_users = set()
    for media in media_list:
        user_stories = cl.user_stories(media.user.pk)
        if user_stories:
            story_users.add(media.user.pk)
            if len(story_users) >= max_stories:
                break

    return list(story_users)
```

### Story Archive Access
```python
# Note: Story archives are typically private
# This would depend on account permissions
def get_story_archive():
    """Access story archive (if available)"""
    try:
        # This method may not be available in all cases
        archived_stories = cl.story_archive()
        return archived_stories
    except Exception as e:
        print(f"Story archive not accessible: {e}")
        return []
```

## 📱 Story Optimization

### Optimal Story Specifications
```python
STORY_SPECS = {
    'resolution': {
        'width': 720,
        'height': 1280,
        'aspect_ratio': '9:16'
    },
    'formats': {
        'photo': ['JPG', 'PNG'],
        'video': ['MP4', 'MOV'],
        'max_video_duration': 15  # seconds
    },
    'file_size': {
        'photo_max': '5MB',
        'video_max': '50MB'
    }
}
```

### Story Resizing Function
```python
from PIL import Image

def resize_for_story(image_path, output_path):
    """Resize image for optimal story display"""
    with Image.open(image_path) as img:
        # Calculate new dimensions maintaining aspect ratio
        target_width = 720
        target_height = 1280

        # Resize to fit story dimensions
        img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # Save optimized image
        img_resized.save(output_path, 'JPEG', quality=95)

    return output_path
```

## 🛡️ Story Privacy & Safety

### Privacy Controls
```python
def check_story_privacy(story_pk):
    """Check if story is accessible"""
    try:
        story = cl.story_info(story_pk)
        return {
            'accessible': True,
            'user_private': story.user.is_private,
            'close_friends_only': hasattr(story, 'audience') and story.audience == 'besties'
        }
    except Exception as e:
        return {
            'accessible': False,
            'error': str(e)
        }
```

### Safe Story Viewing
```python
def safe_story_download(username, max_retries=3):
    """Safely download user stories with error handling"""
    try:
        user_id = cl.user_id_from_username(username)
        user_info = cl.user_info(user_id)

        # Check if user is private and we're not following
        if user_info.is_private and not user_info.friendship_status.following:
            print(f"Cannot access stories from private user: {username}")
            return []

        stories = cl.user_stories(user_id)
        downloaded = []

        for story in stories:
            retry_count = 0
            while retry_count < max_retries:
                try:
                    file_path = cl.story_download(story.pk)
                    downloaded.append(file_path)
                    break
                except Exception as e:
                    retry_count += 1
                    if retry_count == max_retries:
                        print(f"Failed to download story after {max_retries} retries: {e}")

        return downloaded

    except Exception as e:
        print(f"Error downloading stories from {username}: {e}")
        return []
```

## 🎯 Practical Story Automation

### Story Scheduling System
```python
import schedule
import time
from datetime import datetime

class StoryScheduler:
    def __init__(self, client):
        self.cl = client
        self.scheduled_stories = []

    def schedule_story(self, media_path, caption, upload_time):
        """Schedule a story for future upload"""
        self.scheduled_stories.append({
            'media_path': media_path,
            'caption': caption,
            'upload_time': upload_time
        })

    def upload_scheduled_stories(self):
        """Upload stories that are scheduled for now"""
        current_time = datetime.now()
        uploaded = []

        for story_data in self.scheduled_stories[:]:
            if current_time >= story_data['upload_time']:
                try:
                    story = self.cl.photo_upload_to_story(
                        story_data['media_path'],
                        story_data['caption']
                    )
                    uploaded.append(story.pk)
                    self.scheduled_stories.remove(story_data)
                    print(f"✅ Uploaded scheduled story: {story.pk}")
                except Exception as e:
                    print(f"❌ Failed to upload scheduled story: {e}")

        return uploaded

# Usage
scheduler = StoryScheduler(cl)
scheduler.schedule_story(
    "path/to/image.jpg",
    "Good morning!",
    datetime(2024, 1, 15, 9, 0)  # Schedule for 9 AM
)

# Run periodically
schedule.every(1).minutes.do(scheduler.upload_scheduled_stories)
```

### Story Analytics Tracker
```python
def track_story_performance(story_pk, duration_hours=24):
    """Track story performance over time"""
    import time

    performance_data = []
    start_time = time.time()

    while time.time() - start_time < duration_hours * 3600:
        try:
            viewers = cl.story_viewers(story_pk)
            view_count = len(viewers)

            performance_data.append({
                'timestamp': datetime.now().isoformat(),
                'view_count': view_count,
                'viewers': [v.username for v in viewers]
            })

            # Check every 30 minutes
            time.sleep(1800)

        except Exception as e:
            print(f"Error tracking story performance: {e}")
            break

    return performance_data
```

## ⚠️ Best Practices for Stories

### Story Content Guidelines
```python
STORY_BEST_PRACTICES = {
    'posting_frequency': {
        'max_per_day': 10,
        'recommended': '3-5',
        'spacing': 'Every 2-4 hours'
    },
    'content_mix': {
        'behind_scenes': '40%',
        'product_showcase': '30%',
        'user_generated': '20%',
        'educational': '10%'
    },
    'engagement_tactics': [
        'Use polls and questions',
        'Add location tags',
        'Mention relevant users',
        'Use trending hashtags',
        'Create highlight categories'
    ]
}
```

### Error Handling for Story Operations
```python
from instagrapi.exceptions import StoryNotFound, PrivateError

def robust_story_upload(media_path, caption):
    """Upload story with comprehensive error handling"""
    try:
        # Validate media file
        if not Path(media_path).exists():
            raise FileNotFoundError(f"Media file not found: {media_path}")

        # Check file size and format
        file_size = Path(media_path).stat().st_size
        if file_size > 50 * 1024 * 1024:  # 50MB limit
            raise ValueError("File size too large for story upload")

        # Upload story
        story = cl.photo_upload_to_story(media_path, caption)
        return story

    except Exception as e:
        print(f"Story upload failed: {e}")
        return None
```

This comprehensive story documentation covers all aspects of working with Instagram Stories through the instagrapi library, including viewing, uploading, analytics, and automation features.