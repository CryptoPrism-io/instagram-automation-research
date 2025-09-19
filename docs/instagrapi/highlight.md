# Instagrapi Highlight Documentation

> **Source**: https://subzeroid.github.io/instagrapi/usage-guide/highlight.html

This document provides comprehensive information about Instagram Story Highlights operations using the instagrapi library for Instagram's Private API.

## ✨ Highlight Information Methods

### Basic Highlight Operations

#### Get Highlight Primary Key from URL
```python
from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)

# Extract highlight primary key from URL
highlight_url = "https://instagram.com/stories/highlights/17895485201104054/"
highlight_pk = cl.highlight_pk_from_url(highlight_url)
print(f"Highlight PK: {highlight_pk}")
```

#### Get Highlight Information
```python
# Get detailed highlight information
highlight_info = cl.highlight_info(highlight_pk)

print(f"Highlight ID: {highlight_info.pk}")
print(f"Title: {highlight_info.title}")
print(f"Cover Media: {highlight_info.cover_media.pk}")
print(f"Story Count: {len(highlight_info.items)}")
print(f"Created: {highlight_info.created_at}")

# Access stories in highlight
for story in highlight_info.items:
    print(f"Story: {story.pk} - {story.media_type}")
```

#### Get User's Highlights
```python
# Get all highlights for a user
user_id = 29817608135  # Example user ID
user_highlights = cl.user_highlights(user_id)

for highlight in user_highlights:
    print(f"Highlight: {highlight.title}")
    print(f"ID: {highlight.pk}")
    print(f"Cover: {highlight.cover_media.thumbnail_url}")
    print(f"Stories: {len(highlight.items)}")
    print("---")
```

## 📱 Highlight Management Operations

### Create Highlights

#### Create New Highlight
```python
# Create highlight from story IDs
story_ids = ["story_id_1", "story_id_2", "story_id_3"]
title = "Travel Adventures"

new_highlight = cl.highlight_create(title, story_ids)
print(f"Created highlight: {new_highlight.pk}")
print(f"Title: {new_highlight.title}")
```

#### Create Highlight with Advanced Options
```python
def create_branded_highlight(title, story_ids, cover_story_id=None):
    """Create highlight with specific cover"""
    # Create the highlight
    highlight = cl.highlight_create(title, story_ids)

    if cover_story_id and cover_story_id in story_ids:
        # Set specific story as cover
        try:
            # Get the story media for cover
            story_info = cl.story_info(cover_story_id)

            # Download story image to use as cover
            cover_path = cl.story_download(cover_story_id, folder="temp/")

            # Set as highlight cover
            success = cl.highlight_change_cover(highlight.pk, cover_path)
            if success:
                print(f"✅ Cover updated for highlight: {title}")

        except Exception as e:
            print(f"❌ Failed to set cover: {e}")

    return highlight
```

### Modify Existing Highlights

#### Change Highlight Title
```python
# Update highlight title
new_title = "Summer Vibes 2024"
success = cl.highlight_change_title(highlight_pk, new_title)
print(f"Title changed: {success}")
```

#### Change Highlight Cover
```python
# Change highlight cover image
cover_image_path = "path/to/new_cover.jpg"
success = cl.highlight_change_cover(highlight_pk, cover_image_path)
print(f"Cover changed: {success}")

# Alternative: Set cover from existing story in highlight
def set_cover_from_story(highlight_pk, story_pk):
    """Set highlight cover from a specific story"""
    try:
        # Download the story
        story_path = cl.story_download(story_pk, folder="temp/")

        # Set as cover
        success = cl.highlight_change_cover(highlight_pk, story_path)

        # Clean up temp file
        import os
        os.remove(story_path)

        return success
    except Exception as e:
        print(f"Error setting cover from story: {e}")
        return False
```

### Manage Highlight Content

#### Add Stories to Highlight
```python
# Add new stories to existing highlight
new_story_ids = ["new_story_1", "new_story_2"]
success = cl.highlight_add_stories(highlight_pk, new_story_ids)
print(f"Stories added: {success}")
```

#### Remove Stories from Highlight
```python
# Remove specific stories from highlight
stories_to_remove = ["story_id_to_remove"]
success = cl.highlight_remove_stories(highlight_pk, stories_to_remove)
print(f"Stories removed: {success}")
```

#### Reorganize Highlight Stories
```python
def reorganize_highlight_stories(highlight_pk, new_story_order):
    """Reorganize stories in highlight by removing and re-adding"""
    try:
        # Get current highlight info
        highlight_info = cl.highlight_info(highlight_pk)
        current_stories = [story.pk for story in highlight_info.items]

        # Remove all stories
        cl.highlight_remove_stories(highlight_pk, current_stories)

        # Add stories in new order
        cl.highlight_add_stories(highlight_pk, new_story_order)

        return True
    except Exception as e:
        print(f"Error reorganizing highlight: {e}")
        return False

# Usage
new_order = ["story_3", "story_1", "story_2"]  # Desired order
reorganize_highlight_stories(highlight_pk, new_order)
```

### Delete Highlights

#### Delete Highlight
```python
# Delete a highlight completely
success = cl.highlight_delete(highlight_pk)
print(f"Highlight deleted: {success}")
```

## 📊 Highlight Analytics & Management

### Analyze Highlight Performance
```python
def analyze_highlight_performance(user_id):
    """Analyze performance of all user highlights"""
    highlights = cl.user_highlights(user_id)
    performance_data = []

    for highlight in highlights:
        try:
            # Get detailed info
            detail_info = cl.highlight_info(highlight.pk)

            # Analyze stories in highlight
            story_count = len(detail_info.items)
            story_types = analyze_story_types(detail_info.items)

            # Estimate age of highlight
            creation_date = detail_info.created_at
            age_days = (datetime.now() - creation_date).days

            performance_data.append({
                'title': highlight.title,
                'pk': highlight.pk,
                'story_count': story_count,
                'story_types': story_types,
                'age_days': age_days,
                'has_custom_cover': has_custom_cover(highlight),
                'estimated_views': estimate_highlight_views(detail_info)
            })

        except Exception as e:
            print(f"Error analyzing highlight {highlight.title}: {e}")
            continue

    return performance_data

def analyze_story_types(stories):
    """Analyze types of stories in highlight"""
    types = {'photo': 0, 'video': 0}

    for story in stories:
        if story.media_type == 1:
            types['photo'] += 1
        elif story.media_type == 2:
            types['video'] += 1

    return types

def has_custom_cover(highlight):
    """Check if highlight has custom cover"""
    # This is an estimation based on cover media properties
    return highlight.cover_media is not None

def estimate_highlight_views(highlight_info):
    """Estimate highlight views (Instagram doesn't provide this directly)"""
    # This is an estimation based on story age and account metrics
    # In practice, you'd need additional data or different methods
    story_count = len(highlight_info.items)
    age_days = (datetime.now() - highlight_info.created_at).days

    # Simple estimation formula (adjust based on your needs)
    base_views = story_count * 100  # Base estimation
    age_factor = max(0.1, 1 - (age_days / 365))  # Decay over time

    return int(base_views * age_factor)
```

### Highlight Organization System
```python
class HighlightManager:
    def __init__(self, client):
        self.cl = client

    def organize_highlights_by_category(self, categories):
        """Organize highlights into categories"""
        user_highlights = self.cl.user_highlights(self.cl.user_id)
        categorized = {category: [] for category in categories}
        categorized['uncategorized'] = []

        for highlight in user_highlights:
            category_found = False

            for category in categories:
                if category.lower() in highlight.title.lower():
                    categorized[category].append(highlight)
                    category_found = True
                    break

            if not category_found:
                categorized['uncategorized'].append(highlight)

        return categorized

    def suggest_highlight_optimization(self, highlight_pk):
        """Suggest optimizations for highlight"""
        try:
            highlight_info = self.cl.highlight_info(highlight_pk)
            suggestions = []

            # Check story count
            story_count = len(highlight_info.items)
            if story_count < 3:
                suggestions.append("Add more stories for better engagement")
            elif story_count > 20:
                suggestions.append("Consider splitting into multiple highlights")

            # Check title
            if len(highlight_info.title) < 3:
                suggestions.append("Use a more descriptive title")

            # Check story types
            story_types = analyze_story_types(highlight_info.items)
            if story_types['video'] == 0:
                suggestions.append("Add video content for variety")

            # Check age
            age_days = (datetime.now() - highlight_info.created_at).days
            if age_days > 180:
                suggestions.append("Consider refreshing with newer content")

            return suggestions

        except Exception as e:
            return [f"Error analyzing highlight: {e}"]

    def create_highlight_from_hashtag(self, hashtag, title, max_stories=15):
        """Create highlight from stories containing specific hashtag"""
        try:
            # Get your recent stories
            user_stories = self.cl.user_stories(self.cl.user_id)

            # Filter stories containing hashtag
            matching_stories = []
            for story in user_stories:
                # Check if story contains hashtag (in stickers, text, etc.)
                if self.story_contains_hashtag(story, hashtag):
                    matching_stories.append(story.pk)

                    if len(matching_stories) >= max_stories:
                        break

            if matching_stories:
                return self.cl.highlight_create(title, matching_stories)
            else:
                print(f"No stories found with hashtag #{hashtag}")
                return None

        except Exception as e:
            print(f"Error creating highlight from hashtag: {e}")
            return None

    def story_contains_hashtag(self, story, hashtag):
        """Check if story contains specific hashtag"""
        # This would require analyzing story content, stickers, etc.
        # For now, this is a simplified check
        try:
            # You could analyze story stickers, captions, etc.
            # This is a placeholder implementation
            return False  # Implement based on your needs
        except:
            return False

# Usage
manager = HighlightManager(cl)
categories = ["Travel", "Food", "Work", "Fitness"]
organized = manager.organize_highlights_by_category(categories)
```

## 🎨 Highlight Content Strategy

### Content Planning for Highlights
```python
def plan_highlight_content_strategy():
    """Plan comprehensive highlight strategy"""
    strategy = {
        'essential_highlights': [
            {
                'title': 'About Me',
                'purpose': 'Introduction to your brand/personality',
                'content_types': ['Introduction video', 'Behind the scenes', 'Values'],
                'update_frequency': 'Quarterly'
            },
            {
                'title': 'Products/Services',
                'purpose': 'Showcase main offerings',
                'content_types': ['Product demos', 'Features', 'Benefits'],
                'update_frequency': 'Monthly'
            },
            {
                'title': 'Testimonials',
                'purpose': 'Social proof and reviews',
                'content_types': ['Customer reviews', 'Success stories', 'Case studies'],
                'update_frequency': 'Bi-weekly'
            },
            {
                'title': 'FAQ',
                'purpose': 'Answer common questions',
                'content_types': ['Q&A sessions', 'How-to guides', 'Tips'],
                'update_frequency': 'Monthly'
            }
        ],
        'content_highlights': [
            {
                'title': 'Recent Projects',
                'purpose': 'Showcase latest work',
                'update_frequency': 'Weekly'
            },
            {
                'title': 'Events',
                'purpose': 'Document events and milestones',
                'update_frequency': 'As needed'
            }
        ]
    }

    return strategy

def create_highlight_content_calendar(highlights_strategy):
    """Create content calendar for highlights"""
    import calendar
    from datetime import datetime, timedelta

    calendar_data = {}
    current_date = datetime.now()

    for month in range(12):
        month_date = current_date + timedelta(days=30 * month)
        month_name = calendar.month_name[month_date.month]

        calendar_data[month_name] = {
            'updates_needed': [],
            'new_highlights': [],
            'maintenance_tasks': []
        }

        # Schedule updates based on frequency
        for highlight in highlights_strategy['essential_highlights']:
            frequency = highlight['update_frequency']

            if frequency == 'Monthly' or (frequency == 'Quarterly' and month % 3 == 0):
                calendar_data[month_name]['updates_needed'].append({
                    'highlight': highlight['title'],
                    'task': f"Update {highlight['title']} highlight",
                    'content_needed': highlight['content_types']
                })

    return calendar_data
```

### Highlight Automation Tools
```python
class HighlightAutomation:
    def __init__(self, client):
        self.cl = client

    def auto_update_highlights_from_stories(self, highlight_mapping):
        """Automatically update highlights with new relevant stories"""
        user_stories = self.cl.user_stories(self.cl.user_id)

        for story in user_stories:
            # Analyze story content to determine which highlight it belongs to
            suggested_highlight = self.suggest_highlight_for_story(story, highlight_mapping)

            if suggested_highlight:
                try:
                    self.cl.highlight_add_stories(suggested_highlight, [story.pk])
                    print(f"Added story {story.pk} to highlight {suggested_highlight}")
                except Exception as e:
                    print(f"Failed to add story to highlight: {e}")

    def suggest_highlight_for_story(self, story, highlight_mapping):
        """Suggest which highlight a story should be added to"""
        # This would analyze story content, hashtags, location, etc.
        # For now, this is a simplified implementation

        # Example mapping: story characteristics -> highlight
        # You would implement more sophisticated logic here

        return None  # Placeholder

    def cleanup_old_highlights(self, max_age_days=365):
        """Remove stories from highlights that are too old"""
        user_highlights = self.cl.user_highlights(self.cl.user_id)

        for highlight in user_highlights:
            try:
                highlight_info = self.cl.highlight_info(highlight.pk)
                old_stories = []

                for story in highlight_info.items:
                    # Check story age
                    story_age = (datetime.now() - story.taken_at).days
                    if story_age > max_age_days:
                        old_stories.append(story.pk)

                if old_stories:
                    self.cl.highlight_remove_stories(highlight.pk, old_stories)
                    print(f"Removed {len(old_stories)} old stories from {highlight.title}")

            except Exception as e:
                print(f"Error cleaning up highlight {highlight.title}: {e}")

    def backup_highlights(self, backup_folder="highlight_backups"):
        """Backup all highlights by downloading their content"""
        import os
        from pathlib import Path

        backup_path = Path(backup_folder)
        backup_path.mkdir(exist_ok=True)

        user_highlights = self.cl.user_highlights(self.cl.user_id)

        for highlight in user_highlights:
            try:
                highlight_info = self.cl.highlight_info(highlight.pk)

                # Create folder for this highlight
                highlight_folder = backup_path / f"{highlight.title}_{highlight.pk}"
                highlight_folder.mkdir(exist_ok=True)

                # Download all stories in highlight
                for i, story in enumerate(highlight_info.items):
                    try:
                        story_path = self.cl.story_download(
                            story.pk,
                            folder=str(highlight_folder)
                        )
                        print(f"Backed up story {i+1}/{len(highlight_info.items)} from {highlight.title}")
                    except Exception as e:
                        print(f"Failed to backup story {story.pk}: {e}")

                # Save highlight metadata
                metadata = {
                    'title': highlight.title,
                    'pk': highlight.pk,
                    'created_at': highlight_info.created_at.isoformat(),
                    'story_count': len(highlight_info.items),
                    'backup_date': datetime.now().isoformat()
                }

                import json
                with open(highlight_folder / "metadata.json", 'w') as f:
                    json.dump(metadata, f, indent=2)

            except Exception as e:
                print(f"Error backing up highlight {highlight.title}: {e}")

# Usage
automation = HighlightAutomation(cl)
automation.cleanup_old_highlights(max_age_days=180)
automation.backup_highlights()
```

## ⚠️ Best Practices for Highlights

### Highlight Strategy Guidelines
```python
HIGHLIGHT_BEST_PRACTICES = {
    'content_strategy': {
        'essential_highlights': [
            'About/Introduction',
            'Products/Services',
            'Testimonials/Reviews',
            'FAQ/Help'
        ],
        'content_highlights': [
            'Recent Work/Projects',
            'Behind the Scenes',
            'Events/Milestones',
            'Tips/Tutorials'
        ]
    },
    'design_guidelines': {
        'covers': 'Use consistent, branded cover designs',
        'titles': 'Keep titles short and descriptive',
        'order': 'Arrange highlights by importance',
        'quantity': 'Aim for 5-15 highlights maximum'
    },
    'content_guidelines': {
        'story_count': '5-20 stories per highlight',
        'freshness': 'Update regularly with new content',
        'relevance': 'Keep content relevant to highlight theme',
        'quality': 'Use high-quality, engaging stories'
    },
    'maintenance': {
        'regular_review': 'Review highlights monthly',
        'update_frequency': 'Add new content weekly',
        'remove_old': 'Remove outdated content quarterly',
        'analytics': 'Track which highlights get most views'
    }
}

def validate_highlight_strategy(user_highlights):
    """Validate highlight strategy against best practices"""
    issues = []
    recommendations = []

    # Check quantity
    if len(user_highlights) < 3:
        issues.append("Too few highlights - consider adding more categories")
    elif len(user_highlights) > 20:
        issues.append("Too many highlights - consider consolidating")

    # Check for essential highlights
    essential_titles = ['about', 'product', 'service', 'faq']
    existing_titles = [h.title.lower() for h in user_highlights]

    for essential in essential_titles:
        if not any(essential in title for title in existing_titles):
            recommendations.append(f"Consider adding '{essential}' highlight")

    # Check title lengths
    for highlight in user_highlights:
        if len(highlight.title) > 15:
            issues.append(f"Title too long: '{highlight.title}'")
        elif len(highlight.title) < 3:
            issues.append(f"Title too short: '{highlight.title}'")

    return {
        'issues': issues,
        'recommendations': recommendations,
        'score': calculate_highlight_score(user_highlights)
    }

def calculate_highlight_score(user_highlights):
    """Calculate overall highlight strategy score"""
    score = 0
    max_score = 100

    # Quantity score (20 points)
    quantity_score = min(20, len(user_highlights) * 2)
    score += quantity_score

    # Coverage score (40 points)
    essential_keywords = ['about', 'product', 'service', 'faq', 'work', 'testimonial']
    existing_titles = ' '.join([h.title.lower() for h in user_highlights])

    coverage_score = sum(10 for keyword in essential_keywords
                        if keyword in existing_titles)
    score += min(40, coverage_score)

    # Title quality score (20 points)
    good_titles = sum(1 for h in user_highlights
                     if 3 <= len(h.title) <= 15)
    title_score = (good_titles / len(user_highlights)) * 20 if user_highlights else 0
    score += title_score

    # Freshness score (20 points) - simplified
    # In practice, you'd check highlight update dates
    score += 15  # Placeholder

    return min(100, score)
```

### Error Handling for Highlights
```python
from instagrapi.exceptions import HighlightNotFound, ClientError

def safe_highlight_operation(operation, *args, **kwargs):
    """Safely execute highlight operations with error handling"""
    try:
        return operation(*args, **kwargs)
    except HighlightNotFound:
        print("Highlight not found or no longer exists")
        return None
    except ClientError as e:
        if "story not found" in str(e).lower():
            print("Story no longer available for highlight")
        else:
            print(f"Client error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage examples
def safe_highlight_create(title, story_ids):
    """Safely create highlight with error handling"""
    return safe_highlight_operation(cl.highlight_create, title, story_ids)

def safe_highlight_add_stories(highlight_pk, story_ids):
    """Safely add stories to highlight"""
    return safe_highlight_operation(cl.highlight_add_stories, highlight_pk, story_ids)
```

This comprehensive highlight documentation covers all aspects of working with Instagram Story Highlights through the instagrapi library, including creation, management, analytics, automation, and best practices for effective highlight strategy.