# Instagrapi Hashtag Documentation

> **Source**: https://subzeroid.github.io/instagrapi/usage-guide/hashtag.html

This document provides comprehensive information about hashtag-related operations using the instagrapi library for Instagram's Private API.

## 🏷️ Hashtag Information Methods

### Basic Hashtag Operations

#### Get Hashtag Information
```python
from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)

# Get hashtag information by name
hashtag_info = cl.hashtag_info("photography")

print(f"Hashtag ID: {hashtag_info.id}")
print(f"Name: {hashtag_info.name}")
print(f"Media Count: {hashtag_info.media_count}")
print(f"Profile Picture: {hashtag_info.profile_pic_url}")
```

#### Get Related Hashtags
```python
# Find hashtags related to a specific hashtag
related_hashtags = cl.hashtag_related_hashtags("photography")

for hashtag in related_hashtags:
    print(f"Related: #{hashtag.name} ({hashtag.media_count} posts)")
```

### Hashtag Media Retrieval

#### Get Top Media for Hashtag
```python
# Get top/most popular posts for a hashtag
top_medias = cl.hashtag_medias_top("photography", amount=20)

for media in top_medias:
    print(f"Top Post: {media.code}")
    print(f"Likes: {media.like_count}")
    print(f"Comments: {media.comment_count}")
    print(f"User: {media.user.username}")
```

#### Get Recent Media for Hashtag
```python
# Get most recent posts for a hashtag
recent_medias = cl.hashtag_medias_recent("photography", amount=50)

for media in recent_medias:
    print(f"Recent Post: {media.code}")
    print(f"Posted: {media.taken_at}")
    print(f"Caption: {media.caption_text[:100]}...")
```

## 📊 Advanced Hashtag Analysis

### Hashtag Performance Metrics
```python
def analyze_hashtag_performance(hashtag_name):
    """Comprehensive hashtag analysis"""
    # Get hashtag info
    hashtag_info = cl.hashtag_info(hashtag_name)

    # Get top and recent media
    top_medias = cl.hashtag_medias_top(hashtag_name, amount=20)
    recent_medias = cl.hashtag_medias_recent(hashtag_name, amount=50)

    # Calculate metrics
    top_engagement = sum(m.like_count + m.comment_count for m in top_medias)
    recent_engagement = sum(m.like_count + m.comment_count for m in recent_medias)

    return {
        'hashtag': hashtag_name,
        'total_posts': hashtag_info.media_count,
        'top_posts_engagement': top_engagement,
        'recent_posts_engagement': recent_engagement,
        'avg_top_engagement': top_engagement / len(top_medias) if top_medias else 0,
        'avg_recent_engagement': recent_engagement / len(recent_medias) if recent_medias else 0,
        'top_users': get_top_users_for_hashtag(top_medias),
        'related_hashtags': [h.name for h in cl.hashtag_related_hashtags(hashtag_name)]
    }

def get_top_users_for_hashtag(medias):
    """Get users with highest engagement for hashtag"""
    user_engagement = {}

    for media in medias:
        username = media.user.username
        engagement = media.like_count + media.comment_count

        if username not in user_engagement:
            user_engagement[username] = 0
        user_engagement[username] += engagement

    # Sort by engagement
    return sorted(user_engagement.items(), key=lambda x: x[1], reverse=True)[:10]
```

### Hashtag Trend Analysis
```python
import time
from datetime import datetime, timedelta

def track_hashtag_trends(hashtags, days=7):
    """Track hashtag popularity over time"""
    trend_data = {}

    for hashtag in hashtags:
        print(f"Analyzing #{hashtag}...")

        # Get recent posts
        recent_medias = cl.hashtag_medias_recent(hashtag, amount=100)

        # Group by day
        daily_posts = {}
        daily_engagement = {}

        for media in recent_medias:
            post_date = media.taken_at.date()

            # Count posts per day
            daily_posts[post_date] = daily_posts.get(post_date, 0) + 1

            # Sum engagement per day
            engagement = media.like_count + media.comment_count
            daily_engagement[post_date] = daily_engagement.get(post_date, 0) + engagement

        trend_data[hashtag] = {
            'daily_posts': daily_posts,
            'daily_engagement': daily_engagement,
            'total_recent_posts': len(recent_medias),
            'avg_daily_posts': len(recent_medias) / days,
            'trend_score': calculate_trend_score(daily_posts, days)
        }

    return trend_data

def calculate_trend_score(daily_posts, days):
    """Calculate if hashtag is trending up or down"""
    if len(daily_posts) < 2:
        return 0

    dates = sorted(daily_posts.keys())
    recent_half = dates[len(dates)//2:]
    early_half = dates[:len(dates)//2]

    recent_avg = sum(daily_posts[d] for d in recent_half) / len(recent_half)
    early_avg = sum(daily_posts[d] for d in early_half) / len(early_half)

    return (recent_avg - early_avg) / early_avg if early_avg > 0 else 0
```

## 🔍 Hashtag Discovery & Research

### Find Optimal Hashtags
```python
def find_optimal_hashtags(base_hashtag, target_engagement_range=(1000, 100000)):
    """Find hashtags with optimal engagement levels"""
    related_hashtags = cl.hashtag_related_hashtags(base_hashtag)
    optimal_hashtags = []

    for hashtag in related_hashtags:
        # Get sample of recent posts
        recent_medias = cl.hashtag_medias_recent(hashtag.name, amount=10)

        if not recent_medias:
            continue

        # Calculate average engagement
        avg_engagement = sum(
            m.like_count + m.comment_count for m in recent_medias
        ) / len(recent_medias)

        # Check if within target range
        min_engagement, max_engagement = target_engagement_range
        if min_engagement <= avg_engagement <= max_engagement:
            optimal_hashtags.append({
                'hashtag': hashtag.name,
                'media_count': hashtag.media_count,
                'avg_engagement': avg_engagement,
                'competition_score': calculate_competition_score(hashtag.media_count, avg_engagement)
            })

    # Sort by competition score (lower is better)
    return sorted(optimal_hashtags, key=lambda x: x['competition_score'])

def calculate_competition_score(media_count, avg_engagement):
    """Calculate competition score (media count vs engagement)"""
    if avg_engagement == 0:
        return float('inf')
    return media_count / avg_engagement
```

### Hashtag Research Tools
```python
def research_hashtag_set(hashtags):
    """Research a set of hashtags for content strategy"""
    research_data = {}

    for hashtag in hashtags:
        print(f"Researching #{hashtag}...")

        try:
            # Basic info
            hashtag_info = cl.hashtag_info(hashtag)

            # Sample recent posts for analysis
            recent_medias = cl.hashtag_medias_recent(hashtag, amount=30)
            top_medias = cl.hashtag_medias_top(hashtag, amount=9)

            # Analyze posting patterns
            posting_hours = analyze_posting_times(recent_medias)
            top_content_types = analyze_content_types(top_medias)

            research_data[hashtag] = {
                'total_posts': hashtag_info.media_count,
                'difficulty': categorize_hashtag_difficulty(hashtag_info.media_count),
                'best_posting_hours': posting_hours,
                'top_content_types': top_content_types,
                'avg_recent_engagement': calculate_avg_engagement(recent_medias),
                'avg_top_engagement': calculate_avg_engagement(top_medias),
                'recommendation': get_hashtag_recommendation(hashtag_info, recent_medias)
            }

        except Exception as e:
            research_data[hashtag] = {'error': str(e)}

    return research_data

def analyze_posting_times(medias):
    """Analyze best times to post for hashtag"""
    hour_counts = {}

    for media in medias:
        hour = media.taken_at.hour
        hour_counts[hour] = hour_counts.get(hour, 0) + 1

    # Return top 3 hours
    return sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:3]

def analyze_content_types(medias):
    """Analyze what content performs best"""
    type_engagement = {'photo': [], 'video': [], 'carousel': []}

    for media in medias:
        engagement = media.like_count + media.comment_count

        if media.media_type == 1:  # Photo
            type_engagement['photo'].append(engagement)
        elif media.media_type == 2:  # Video
            type_engagement['video'].append(engagement)
        elif media.media_type == 8:  # Carousel
            type_engagement['carousel'].append(engagement)

    # Calculate averages
    return {
        content_type: sum(engagements) / len(engagements) if engagements else 0
        for content_type, engagements in type_engagement.items()
    }

def categorize_hashtag_difficulty(media_count):
    """Categorize hashtag difficulty based on post count"""
    if media_count < 100000:
        return "Easy"
    elif media_count < 1000000:
        return "Medium"
    elif media_count < 10000000:
        return "Hard"
    else:
        return "Very Hard"

def get_hashtag_recommendation(hashtag_info, recent_medias):
    """Get recommendation for hashtag usage"""
    media_count = hashtag_info.media_count
    avg_engagement = calculate_avg_engagement(recent_medias)

    if media_count < 50000 and avg_engagement > 100:
        return "Great niche hashtag - high engagement, low competition"
    elif media_count > 10000000:
        return "High competition - use sparingly or with niche hashtags"
    elif avg_engagement < 50:
        return "Low engagement - consider alternatives"
    else:
        return "Good hashtag for balanced reach and engagement"

def calculate_avg_engagement(medias):
    """Calculate average engagement for media list"""
    if not medias:
        return 0
    return sum(m.like_count + m.comment_count for m in medias) / len(medias)
```

## 🎯 Hashtag Strategy Tools

### Hashtag Mix Generator
```python
def generate_hashtag_mix(niche, follower_count=10000):
    """Generate optimal hashtag mix based on account size"""
    # Define hashtag categories based on follower count
    if follower_count < 1000:
        # Small accounts: focus on niche hashtags
        mix = {
            'big_hashtags': 1,      # 1M+ posts
            'medium_hashtags': 4,   # 100K-1M posts
            'small_hashtags': 15,   # 10K-100K posts
            'micro_hashtags': 10    # <10K posts
        }
    elif follower_count < 10000:
        # Growing accounts: balanced approach
        mix = {
            'big_hashtags': 3,
            'medium_hashtags': 7,
            'small_hashtags': 12,
            'micro_hashtags': 8
        }
    else:
        # Larger accounts: can compete in bigger hashtags
        mix = {
            'big_hashtags': 8,
            'medium_hashtags': 10,
            'small_hashtags': 8,
            'micro_hashtags': 4
        }

    return generate_hashtags_by_category(niche, mix)

def generate_hashtags_by_category(niche, mix):
    """Generate hashtags for each category"""
    # Get base hashtags for niche
    base_hashtags = get_niche_hashtags(niche)
    categorized_hashtags = categorize_hashtags_by_size(base_hashtags)

    selected_hashtags = []

    for category, count in mix.items():
        available = categorized_hashtags.get(category, [])
        selected = available[:count]
        selected_hashtags.extend(selected)

    return selected_hashtags[:30]  # Instagram limit

def get_niche_hashtags(niche):
    """Get hashtags related to a niche"""
    # Start with main niche hashtag
    try:
        related = cl.hashtag_related_hashtags(niche)
        return [h.name for h in related] + [niche]
    except:
        return [niche]

def categorize_hashtags_by_size(hashtags):
    """Categorize hashtags by their post count"""
    categories = {
        'big_hashtags': [],
        'medium_hashtags': [],
        'small_hashtags': [],
        'micro_hashtags': []
    }

    for hashtag in hashtags:
        try:
            info = cl.hashtag_info(hashtag)
            count = info.media_count

            if count >= 1000000:
                categories['big_hashtags'].append(hashtag)
            elif count >= 100000:
                categories['medium_hashtags'].append(hashtag)
            elif count >= 10000:
                categories['small_hashtags'].append(hashtag)
            else:
                categories['micro_hashtags'].append(hashtag)

        except:
            continue

    return categories
```

### Hashtag Performance Tracker
```python
import json
from datetime import datetime

class HashtagTracker:
    def __init__(self, client):
        self.cl = client
        self.tracking_file = "hashtag_performance.json"

    def track_post_performance(self, media_id, hashtags_used):
        """Track how hashtags perform for your posts"""
        try:
            media = self.cl.media_info(media_id)

            performance_data = {
                'media_id': media_id,
                'hashtags': hashtags_used,
                'initial_metrics': {
                    'likes': media.like_count,
                    'comments': media.comment_count,
                    'timestamp': datetime.now().isoformat()
                }
            }

            self._save_performance_data(performance_data)
            return performance_data

        except Exception as e:
            print(f"Error tracking post: {e}")
            return None

    def update_performance(self, media_id):
        """Update performance metrics for tracked post"""
        try:
            media = self.cl.media_info(media_id)

            # Load existing data
            data = self._load_performance_data()

            for post in data:
                if post['media_id'] == media_id:
                    post['updated_metrics'] = {
                        'likes': media.like_count,
                        'comments': media.comment_count,
                        'timestamp': datetime.now().isoformat()
                    }
                    break

            self._save_performance_data(data)

        except Exception as e:
            print(f"Error updating performance: {e}")

    def analyze_hashtag_effectiveness(self):
        """Analyze which hashtags perform best"""
        data = self._load_performance_data()
        hashtag_performance = {}

        for post in data:
            if 'updated_metrics' not in post:
                continue

            initial = post['initial_metrics']
            updated = post['updated_metrics']

            # Calculate growth
            like_growth = updated['likes'] - initial['likes']
            comment_growth = updated['comments'] - initial['comments']
            total_growth = like_growth + comment_growth

            for hashtag in post['hashtags']:
                if hashtag not in hashtag_performance:
                    hashtag_performance[hashtag] = {
                        'total_growth': 0,
                        'post_count': 0,
                        'avg_growth': 0
                    }

                hashtag_performance[hashtag]['total_growth'] += total_growth
                hashtag_performance[hashtag]['post_count'] += 1

        # Calculate averages
        for hashtag, stats in hashtag_performance.items():
            if stats['post_count'] > 0:
                stats['avg_growth'] = stats['total_growth'] / stats['post_count']

        # Sort by average growth
        return sorted(
            hashtag_performance.items(),
            key=lambda x: x[1]['avg_growth'],
            reverse=True
        )

    def _load_performance_data(self):
        """Load performance data from file"""
        try:
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_performance_data(self, data):
        """Save performance data to file"""
        existing_data = self._load_performance_data()

        if isinstance(data, list):
            with open(self.tracking_file, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            existing_data.append(data)
            with open(self.tracking_file, 'w') as f:
                json.dump(existing_data, f, indent=2)

# Usage
tracker = HashtagTracker(cl)

# Track a new post
hashtags = ["photography", "portrait", "canon", "photooftheday"]
tracker.track_post_performance(media_id, hashtags)

# Update performance after some time
tracker.update_performance(media_id)

# Analyze which hashtags work best
best_hashtags = tracker.analyze_hashtag_effectiveness()
```

## 🚀 Hashtag Automation Tools

### Auto-Hashtag Generator
```python
def auto_generate_hashtags(image_path, caption_text, max_hashtags=30):
    """Auto-generate hashtags based on image and caption"""
    hashtags = set()

    # Extract hashtags from caption
    caption_hashtags = extract_hashtags_from_text(caption_text)
    hashtags.update(caption_hashtags)

    # Add related hashtags for each found hashtag
    for hashtag in caption_hashtags[:3]:  # Limit to avoid API limits
        try:
            related = cl.hashtag_related_hashtags(hashtag)
            related_names = [h.name for h in related[:5]]
            hashtags.update(related_names)
        except:
            continue

    # Add general popular hashtags if needed
    if len(hashtags) < max_hashtags:
        general_hashtags = get_general_popular_hashtags()
        hashtags.update(general_hashtags)

    return list(hashtags)[:max_hashtags]

def extract_hashtags_from_text(text):
    """Extract existing hashtags from text"""
    import re
    if not text:
        return []

    hashtag_pattern = r'#(\w+)'
    matches = re.findall(hashtag_pattern, text.lower())
    return matches

def get_general_popular_hashtags():
    """Get list of generally popular hashtags"""
    return [
        'photooftheday', 'instagood', 'love', 'beautiful', 'happy',
        'follow', 'picoftheday', 'art', 'photography', 'nature'
    ]
```

### Hashtag Scheduler
```python
class HashtagScheduler:
    def __init__(self, client):
        self.cl = client
        self.hashtag_rotation = {}

    def create_hashtag_rotation(self, base_hashtags, rotation_days=7):
        """Create rotating hashtag sets"""
        all_related = set(base_hashtags)

        # Get related hashtags for each base hashtag
        for hashtag in base_hashtags:
            try:
                related = cl.hashtag_related_hashtags(hashtag)
                related_names = [h.name for h in related]
                all_related.update(related_names)
            except:
                continue

        # Create daily sets
        hashtag_list = list(all_related)
        for day in range(rotation_days):
            start_idx = (day * 20) % len(hashtag_list)
            daily_set = hashtag_list[start_idx:start_idx + 30]

            # Fill remaining slots if needed
            if len(daily_set) < 30:
                daily_set.extend(hashtag_list[:30 - len(daily_set)])

            self.hashtag_rotation[day] = daily_set[:30]

        return self.hashtag_rotation

    def get_daily_hashtags(self, day_of_week=None):
        """Get hashtags for specific day"""
        if day_of_week is None:
            day_of_week = datetime.now().weekday()

        return self.hashtag_rotation.get(day_of_week % 7, [])

# Usage
scheduler = HashtagScheduler(cl)
base_tags = ["photography", "portrait", "art"]
rotation = scheduler.create_hashtag_rotation(base_tags)
today_hashtags = scheduler.get_daily_hashtags()
```

## ⚠️ Best Practices for Hashtags

### Hashtag Usage Guidelines
```python
HASHTAG_BEST_PRACTICES = {
    'limits': {
        'max_per_post': 30,
        'recommended_count': '5-15',
        'stories_max': 10
    },
    'strategy': {
        'mix_sizes': 'Use mix of popular and niche hashtags',
        'relevance': 'Keep hashtags relevant to content',
        'avoid_banned': 'Check for shadowbanned hashtags',
        'rotate': 'Rotate hashtags across posts'
    },
    'timing': {
        'research_timing': 'Post when your hashtag audience is active',
        'trend_watch': 'Monitor trending hashtags in your niche',
        'seasonal': 'Use seasonal and event-based hashtags'
    }
}
```

### Shadowban Detection
```python
def check_hashtag_shadowban(hashtag):
    """Check if hashtag might be shadowbanned"""
    try:
        # Get recent posts
        recent_posts = cl.hashtag_medias_recent(hashtag, amount=50)

        if not recent_posts:
            return {"status": "possible_shadowban", "reason": "No recent posts found"}

        # Check posting frequency
        post_times = [post.taken_at for post in recent_posts]
        time_gaps = []

        for i in range(1, len(post_times)):
            gap = (post_times[i-1] - post_times[i]).total_seconds() / 60  # minutes
            time_gaps.append(gap)

        avg_gap = sum(time_gaps) / len(time_gaps) if time_gaps else 0

        # Very large gaps might indicate issues
        if avg_gap > 120:  # More than 2 hours between posts
            return {"status": "possible_shadowban", "reason": "Large gaps between posts"}

        return {"status": "healthy", "avg_posting_gap_minutes": avg_gap}

    except Exception as e:
        return {"status": "error", "error": str(e)}

def validate_hashtag_set(hashtags):
    """Validate a set of hashtags for potential issues"""
    results = {}

    for hashtag in hashtags:
        try:
            # Check if hashtag exists and has content
            info = cl.hashtag_info(hashtag)
            shadowban_check = check_hashtag_shadowban(hashtag)

            results[hashtag] = {
                'exists': True,
                'media_count': info.media_count,
                'shadowban_check': shadowban_check,
                'recommendation': 'safe' if shadowban_check['status'] == 'healthy' else 'caution'
            }

        except Exception as e:
            results[hashtag] = {
                'exists': False,
                'error': str(e),
                'recommendation': 'avoid'
            }

    return results
```

This comprehensive hashtag documentation covers all aspects of working with Instagram hashtags through the instagrapi library, including research, analysis, strategy, automation, and best practices for optimal hashtag usage.