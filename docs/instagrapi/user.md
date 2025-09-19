# Instagrapi User Documentation

> **Source**: https://subzeroid.github.io/instagrapi/usage-guide/user.html

This document provides comprehensive information about user-related operations using the instagrapi library for Instagram's Private API.

## 👤 User Information Methods

### Basic User Information Retrieval

#### Get User Info by ID
```python
from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)

# Get user information by user ID
user_info = cl.user_info(user_id)

# Access user properties
print(f"Username: {user_info.username}")
print(f"Full Name: {user_info.full_name}")
print(f"Bio: {user_info.biography}")
print(f"Followers: {user_info.follower_count}")
print(f"Following: {user_info.following_count}")
print(f"Posts: {user_info.media_count}")
print(f"Is Verified: {user_info.is_verified}")
print(f"Is Private: {user_info.is_private}")
```

#### Get User Info by Username
```python
# Get user information by username
user_info = cl.user_info_by_username("target_username")

# User info structure
def display_user_info(user):
    return {
        'user_id': user.pk,
        'username': user.username,
        'full_name': user.full_name,
        'biography': user.biography,
        'follower_count': user.follower_count,
        'following_count': user.following_count,
        'media_count': user.media_count,
        'is_verified': user.is_verified,
        'is_private': user.is_private,
        'is_business': user.is_business,
        'category': user.category,
        'external_url': user.external_url,
        'profile_pic_url': user.profile_pic_url,
        'has_anonymous_profile_picture': user.has_anonymous_profile_picture
    }
```

### ID/Username Conversion Methods

#### Convert Username to User ID
```python
# Get user ID from username
user_id = cl.user_id_from_username("target_username")
print(f"User ID: {user_id}")
```

#### Convert User ID to Username
```python
# Get username from user ID
username = cl.username_from_user_id(user_id)
print(f"Username: {username}")
```

## 👥 Follower/Following Operations

### Retrieve Followers and Following

#### Get User's Followers
```python
# Get all followers (limited by Instagram API)
followers = cl.user_followers(user_id)

# Get specific amount of followers
followers = cl.user_followers(user_id, amount=100)

# Process followers
for user_id, user_info in followers.items():
    print(f"Follower: {user_info.username} - {user_info.full_name}")
```

#### Get User's Following List
```python
# Get users that the target user is following
following = cl.user_following(user_id)

# Get specific amount
following = cl.user_following(user_id, amount=50)

# Process following list
for user_id, user_info in following.items():
    print(f"Following: {user_info.username}")
```

### Advanced Follower Operations

#### Search Followers
```python
# Search within a user's followers
search_results = cl.search_followers(user_id, query="john")

for user in search_results:
    print(f"Found follower: {user.username}")
```

#### Get Mutual Followers
```python
def get_mutual_followers(user1_id, user2_id):
    """Find mutual followers between two users"""
    followers1 = set(cl.user_followers(user1_id).keys())
    followers2 = set(cl.user_followers(user2_id).keys())

    mutual = followers1.intersection(followers2)
    return [cl.user_info(uid) for uid in mutual]
```

### Follow/Unfollow Operations

#### Follow a User
```python
# Follow a user
success = cl.user_follow(user_id)
print(f"Follow successful: {success}")

# Check follow status
user_info = cl.user_info(user_id)
is_following = user_info.friendship_status.following
print(f"Currently following: {is_following}")
```

#### Unfollow a User
```python
# Unfollow a user
success = cl.user_unfollow(user_id)
print(f"Unfollow successful: {success}")
```

#### Bulk Follow/Unfollow Operations
```python
def bulk_follow_users(usernames, delay_range=(1, 3)):
    """Follow multiple users with delays"""
    followed_count = 0

    for username in usernames:
        try:
            user_id = cl.user_id_from_username(username)
            success = cl.user_follow(user_id)

            if success:
                followed_count += 1
                print(f"✅ Followed {username}")
            else:
                print(f"❌ Failed to follow {username}")

            # Add delay between follows
            delay = random.uniform(*delay_range)
            time.sleep(delay)

        except Exception as e:
            print(f"❌ Error following {username}: {e}")

    return followed_count

# Usage
usernames_to_follow = ["user1", "user2", "user3"]
followed = bulk_follow_users(usernames_to_follow)
```

#### Smart Unfollow System
```python
def smart_unfollow_non_followers():
    """Unfollow users who don't follow back"""
    # Get your following list
    following = cl.user_following(cl.user_id)

    # Get your followers
    followers = cl.user_followers(cl.user_id)
    follower_ids = set(followers.keys())

    unfollowed_count = 0

    for user_id, user_info in following.items():
        # Skip if they follow you back
        if user_id in follower_ids:
            continue

        # Unfollow non-followers
        success = cl.user_unfollow(user_id)
        if success:
            unfollowed_count += 1
            print(f"Unfollowed {user_info.username}")

        # Rate limiting delay
        time.sleep(random.uniform(2, 5))

    return unfollowed_count
```

## 🔔 Notification Controls

### Post Notifications
```python
# Enable notifications for user's posts
success = cl.enable_user_notifications(user_id)

# Disable notifications for user's posts
success = cl.disable_user_notifications(user_id)
```

### Story Notifications
```python
# Enable story notifications
success = cl.enable_user_story_notifications(user_id)

# Disable story notifications
success = cl.disable_user_story_notifications(user_id)
```

### Video Notifications
```python
# Enable video notifications
success = cl.enable_user_video_notifications(user_id)

# Disable video notifications
success = cl.disable_user_video_notifications(user_id)
```

### Reels Notifications
```python
# Enable reels notifications
success = cl.enable_user_reels_notifications(user_id)

# Disable reels notifications
success = cl.disable_user_reels_notifications(user_id)
```

## 👨‍👩‍👧‍👦 Close Friends Management

### Add to Close Friends
```python
# Add user to close friends list
success = cl.close_friend_add(user_id)
print(f"Added to close friends: {success}")
```

### Remove from Close Friends
```python
# Remove user from close friends list
success = cl.close_friend_remove(user_id)
print(f"Removed from close friends: {success}")
```

### Manage Close Friends List
```python
def manage_close_friends():
    """View and manage close friends list"""
    # Get current close friends (if available)
    # Note: This might require specific API access

    close_friends = []  # Instagram API limitation

    # Add multiple users to close friends
    users_to_add = ["friend1", "friend2", "friend3"]
    for username in users_to_add:
        user_id = cl.user_id_from_username(username)
        success = cl.close_friend_add(user_id)
        if success:
            close_friends.append(username)

    return close_friends
```

## 🔍 User Search Operations

### Search Users by Query
```python
# Search for users
search_results = cl.search_users("query_string")

for user in search_results:
    print(f"Found: {user.username} - {user.full_name}")
```

### Advanced User Search
```python
def advanced_user_search(query, filters=None):
    """Enhanced user search with filtering"""
    results = cl.search_users(query)

    if not filters:
        return results

    filtered_results = []
    for user in results:
        # Apply filters
        if filters.get('verified_only') and not user.is_verified:
            continue
        if filters.get('min_followers') and user.follower_count < filters['min_followers']:
            continue
        if filters.get('exclude_private') and user.is_private:
            continue

        filtered_results.append(user)

    return filtered_results

# Usage with filters
filters = {
    'verified_only': True,
    'min_followers': 1000,
    'exclude_private': True
}
results = advanced_user_search("photographer", filters)
```

## 📊 User Analytics & Insights

### Analyze User Profile
```python
def analyze_user_profile(username):
    """Comprehensive user profile analysis"""
    user = cl.user_info_by_username(username)

    # Calculate engagement metrics
    recent_media = cl.user_medias(user.pk, amount=12)
    total_likes = sum(media.like_count for media in recent_media)
    total_comments = sum(media.comment_count for media in recent_media)

    engagement_rate = (total_likes + total_comments) / (user.follower_count * len(recent_media)) * 100

    return {
        'username': user.username,
        'followers': user.follower_count,
        'following': user.following_count,
        'posts': user.media_count,
        'follower_following_ratio': user.follower_count / max(user.following_count, 1),
        'avg_likes': total_likes / len(recent_media) if recent_media else 0,
        'avg_comments': total_comments / len(recent_media) if recent_media else 0,
        'engagement_rate': engagement_rate,
        'is_business': user.is_business,
        'is_verified': user.is_verified,
        'profile_strength': calculate_profile_strength(user)
    }

def calculate_profile_strength(user):
    """Calculate profile completeness score"""
    score = 0
    score += 20 if user.full_name else 0
    score += 20 if user.biography else 0
    score += 20 if user.external_url else 0
    score += 20 if not user.has_anonymous_profile_picture else 0
    score += 20 if user.media_count > 0 else 0
    return score
```

### Track User Growth
```python
import json
from datetime import datetime

def track_user_growth(username, log_file="user_growth.json"):
    """Track user follower growth over time"""
    user = cl.user_info_by_username(username)

    # Load existing data
    try:
        with open(log_file, 'r') as f:
            growth_data = json.load(f)
    except FileNotFoundError:
        growth_data = {}

    # Add current data point
    today = datetime.now().isoformat()
    if username not in growth_data:
        growth_data[username] = []

    growth_data[username].append({
        'date': today,
        'followers': user.follower_count,
        'following': user.following_count,
        'posts': user.media_count
    })

    # Save updated data
    with open(log_file, 'w') as f:
        json.dump(growth_data, f, indent=2)

    return growth_data[username]
```

## 🛡️ Privacy & Safety Features

### Check User Relationship Status
```python
def check_relationship(username):
    """Check relationship status with a user"""
    user = cl.user_info_by_username(username)

    relationship = {
        'following': user.friendship_status.following,
        'followed_by': user.friendship_status.followed_by,
        'blocking': user.friendship_status.blocking,
        'blocked_by': user.friendship_status.blocked_by,
        'is_private': user.is_private,
        'is_muting_reel': user.friendship_status.muting_reel,
        'outgoing_request': user.friendship_status.outgoing_request
    }

    return relationship
```

### Block/Unblock Users
```python
# Block a user
success = cl.user_block(user_id)
print(f"Block successful: {success}")

# Unblock a user
success = cl.user_unblock(user_id)
print(f"Unblock successful: {success}")
```

### Mute/Unmute Users
```python
# Mute user's posts
success = cl.user_mute(user_id)

# Unmute user's posts
success = cl.user_unmute(user_id)

# Mute user's stories
success = cl.user_mute_stories(user_id)

# Unmute user's stories
success = cl.user_unmute_stories(user_id)
```

## 🎯 Practical Examples

### Complete User Management Example
```python
import time
import random

class UserManager:
    def __init__(self, client):
        self.cl = client

    def follow_users_by_hashtag(self, hashtag, max_follows=10):
        """Follow users who recently posted with a hashtag"""
        # Get recent media for hashtag
        media_list = self.cl.hashtag_medias_recent(hashtag, amount=50)

        followed_users = []
        follow_count = 0

        for media in media_list:
            if follow_count >= max_follows:
                break

            user_id = media.user.pk

            # Skip if already following
            user_info = self.cl.user_info(user_id)
            if user_info.friendship_status.following:
                continue

            # Follow user
            success = self.cl.user_follow(user_id)
            if success:
                followed_users.append(media.user.username)
                follow_count += 1
                print(f"✅ Followed {media.user.username}")

                # Delay between follows
                time.sleep(random.uniform(2, 5))

        return followed_users

    def cleanup_following(self, days_since_follow=7):
        """Unfollow users who haven't followed back after X days"""
        # This would require tracking follow dates
        # Implementation depends on your tracking system
        pass

# Usage
user_manager = UserManager(cl)
followed = user_manager.follow_users_by_hashtag("photography", max_follows=5)
```

### User Engagement Analysis
```python
def analyze_user_engagement(username, competitor_usernames):
    """Analyze user engagement compared to competitors"""
    target_user = cl.user_info_by_username(username)
    target_media = cl.user_medias(target_user.pk, amount=12)

    # Calculate target user metrics
    target_metrics = calculate_engagement_metrics(target_media, target_user.follower_count)

    # Analyze competitors
    competitor_metrics = {}
    for comp_username in competitor_usernames:
        comp_user = cl.user_info_by_username(comp_username)
        comp_media = cl.user_medias(comp_user.pk, amount=12)
        competitor_metrics[comp_username] = calculate_engagement_metrics(comp_media, comp_user.follower_count)

    return {
        'target': target_metrics,
        'competitors': competitor_metrics,
        'ranking': rank_engagement(target_metrics, competitor_metrics)
    }

def calculate_engagement_metrics(media_list, follower_count):
    """Calculate detailed engagement metrics"""
    if not media_list:
        return {}

    total_likes = sum(m.like_count for m in media_list)
    total_comments = sum(m.comment_count for m in media_list)
    post_count = len(media_list)

    return {
        'avg_likes': total_likes / post_count,
        'avg_comments': total_comments / post_count,
        'engagement_rate': (total_likes + total_comments) / (follower_count * post_count) * 100,
        'likes_per_follower': total_likes / follower_count,
        'comments_per_follower': total_comments / follower_count
    }
```

## ⚠️ Best Practices & Rate Limiting

### Safe Follow/Unfollow Practices
```python
# Daily limits to avoid Instagram restrictions
DAILY_LIMITS = {
    'follows': 200,
    'unfollows': 200,
    'user_searches': 500
}

def safe_follow_operation(user_id, action='follow'):
    """Execute follow operations with safety checks"""
    try:
        if action == 'follow':
            success = cl.user_follow(user_id)
        else:
            success = cl.user_unfollow(user_id)

        # Add mandatory delay
        time.sleep(random.uniform(2, 5))
        return success

    except Exception as e:
        print(f"Error in {action} operation: {e}")
        return False
```

### Error Handling for User Operations
```python
from instagrapi.exceptions import UserNotFound, PrivateError

def robust_user_info(username):
    """Get user info with comprehensive error handling"""
    try:
        return cl.user_info_by_username(username)
    except UserNotFound:
        print(f"User {username} not found")
        return None
    except PrivateError:
        print(f"User {username} is private")
        return None
    except Exception as e:
        print(f"Error getting user info: {e}")
        return None
```

This comprehensive user documentation covers all aspects of working with Instagram users through the instagrapi library, including information retrieval, relationship management, analytics, and safety considerations.