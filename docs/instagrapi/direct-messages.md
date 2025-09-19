# Instagrapi Direct Messages Documentation

> **Source**: https://subzeroid.github.io/instagrapi/usage-guide/direct.html

This document provides comprehensive information about Instagram Direct Messaging operations using the instagrapi library for Instagram's Private API.

## 💬 Direct Message Core Methods

### Basic Thread Operations

#### Get Inbox Threads
```python
from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)

# Get inbox threads (conversations)
threads = cl.direct_threads()

# Get specific number of threads
threads = cl.direct_threads(amount=20)

# Process threads
for thread in threads:
    print(f"Thread ID: {thread.id}")
    print(f"Thread Type: {thread.thread_type}")
    print(f"Users: {[user.username for user in thread.users]}")
    print(f"Last Activity: {thread.last_activity_at}")
    print(f"Unread Count: {thread.read_state}")
```

#### Get Pending Inbox
```python
# Get pending message requests
pending_threads = cl.direct_pending_inbox()

for thread in pending_threads:
    print(f"Pending from: {thread.users[0].username}")
    print(f"Message: {thread.last_permanent_item.text}")
```

#### Get Specific Thread Details
```python
# Get detailed thread information
thread_details = cl.direct_thread(thread_id)

print(f"Thread Title: {thread_details.thread_title}")
print(f"Is Group: {thread_details.is_group}")
print(f"Member Count: {len(thread_details.users)}")
```

### Message Retrieval

#### Get Messages in Thread
```python
# Get messages from a specific thread
messages = cl.direct_messages(thread_id)

# Get specific number of messages
messages = cl.direct_messages(thread_id, amount=50)

# Process messages
for message in messages:
    print(f"From: {message.user_id}")
    print(f"Text: {message.text}")
    print(f"Timestamp: {message.timestamp}")
    print(f"Message Type: {message.item_type}")
```

#### Advanced Message Filtering
```python
def filter_messages(thread_id, filters=None):
    """Filter messages by various criteria"""
    messages = cl.direct_messages(thread_id, amount=100)

    if not filters:
        return messages

    filtered = []
    for message in messages:
        # Filter by user
        if filters.get('from_user') and message.user_id != filters['from_user']:
            continue

        # Filter by message type
        if filters.get('message_type') and message.item_type != filters['message_type']:
            continue

        # Filter by date range
        if filters.get('after_date') and message.timestamp < filters['after_date']:
            continue

        filtered.append(message)

    return filtered

# Usage
filters = {
    'from_user': user_id,
    'message_type': 'text',
    'after_date': datetime(2024, 1, 1)
}
filtered_messages = filter_messages(thread_id, filters)
```

## 📤 Sending Messages

### Basic Text Messages

#### Send Text Message
```python
# Send message to user by user ID
success = cl.direct_send(text="Hello!", user_ids=[user_id])
print(f"Message sent: {success}")

# Send message to existing thread
success = cl.direct_send(text="Hello!", thread_ids=[thread_id])

# Send message to multiple users
success = cl.direct_send(
    text="Group message!",
    user_ids=[user_id1, user_id2, user_id3]
)
```

#### Send to Thread by Username
```python
def send_message_by_username(username, message):
    """Send message to user by username"""
    user_id = cl.user_id_from_username(username)
    return cl.direct_send(text=message, user_ids=[user_id])

# Usage
success = send_message_by_username("friend_username", "Hey there!")
```

### Media Messages

#### Send Photo
```python
# Send photo from file
success = cl.direct_send_photo(
    path="path/to/photo.jpg",
    user_ids=[user_id]
)

# Send photo with caption
success = cl.direct_send_photo(
    path="path/to/photo.jpg",
    user_ids=[user_id],
    text="Check out this photo!"
)
```

#### Send Video
```python
# Send video file
success = cl.direct_send_video(
    path="path/to/video.mp4",
    user_ids=[user_id]
)

# Send video with thumbnail
success = cl.direct_send_video(
    path="path/to/video.mp4",
    user_ids=[user_id],
    thumbnail="path/to/thumbnail.jpg"
)
```

#### Send Voice Message
```python
# Send audio/voice message
success = cl.direct_send_audio(
    path="path/to/audio.mp3",
    user_ids=[user_id]
)
```

### Share Content

#### Share Media Posts
```python
# Share a media post to direct message
success = cl.direct_media_share(
    media_id=media_id,
    user_ids=[user_id],
    text="Check out this post!"
)
```

#### Share Stories
```python
# Share a story to direct message
success = cl.direct_story_share(
    story_id=story_id,
    user_ids=[user_id]
)
```

#### Share User Profiles
```python
# Share a user profile
success = cl.direct_profile_share(
    profile_user_id=target_user_id,
    user_ids=[recipient_user_id],
    text="Check out this profile"
)
```

#### Share External Links
```python
# Share URL with preview
success = cl.direct_send_link(
    link="https://example.com",
    user_ids=[user_id],
    text="Interesting article!"
)
```

## 🔍 Thread Management

### Search Threads
```python
# Search threads by query
search_results = cl.direct_search(query="keyword")

for result in search_results:
    if result.thread:
        print(f"Found thread: {result.thread.thread_title}")
    if result.user:
        print(f"Found user: {result.user.username}")
```

### Thread Actions

#### Hide Thread
```python
# Hide a thread from inbox
success = cl.direct_thread_hide(thread_id)
print(f"Thread hidden: {success}")
```

#### Mark as Unread
```python
# Mark thread as unread
success = cl.direct_thread_mark_unread(thread_id)
print(f"Marked as unread: {success}")
```

#### Mute/Unmute Thread
```python
# Mute thread notifications
success = cl.direct_thread_mute(thread_id)

# Unmute thread notifications
success = cl.direct_thread_unmute(thread_id)
```

#### Mute Video Calls
```python
# Mute video call notifications for thread
success = cl.direct_thread_mute_video_call(thread_id)

# Unmute video call notifications
success = cl.direct_thread_unmute_video_call(thread_id)
```

### Message Actions

#### Delete Messages
```python
# Delete a specific message
success = cl.direct_message_delete(thread_id, message_id)
print(f"Message deleted: {success}")

# Delete multiple messages
message_ids = [msg_id1, msg_id2, msg_id3]
for msg_id in message_ids:
    cl.direct_message_delete(thread_id, msg_id)
```

#### Like/Unlike Messages
```python
# Like a message (heart reaction)
success = cl.direct_message_like(thread_id, message_id)

# Unlike a message
success = cl.direct_message_unlike(thread_id, message_id)
```

## 👥 Group Chat Management

### Create Group Chat
```python
# Create group chat with multiple users
group = cl.direct_create_group(
    user_ids=[user_id1, user_id2, user_id3],
    title="My Group Chat"
)
print(f"Group created: {group.thread_id}")
```

### Manage Group Members

#### Add Users to Group
```python
# Add users to existing group
success = cl.direct_add_users(
    thread_id=group_thread_id,
    user_ids=[new_user_id1, new_user_id2]
)
```

#### Remove Users from Group
```python
# Remove users from group
success = cl.direct_remove_users(
    thread_id=group_thread_id,
    user_ids=[user_to_remove_id]
)
```

#### Leave Group
```python
# Leave a group chat
success = cl.direct_leave_group(thread_id)
```

### Group Settings

#### Change Group Title
```python
# Update group chat title
success = cl.direct_thread_set_title(
    thread_id=group_thread_id,
    title="New Group Name"
)
```

#### Change Group Photo
```python
# Set group chat photo
success = cl.direct_thread_set_photo(
    thread_id=group_thread_id,
    photo_path="path/to/group_photo.jpg"
)
```

## 📊 Message Analytics & Monitoring

### Track Message Statistics
```python
def analyze_thread_activity(thread_id, days=30):
    """Analyze thread activity over time"""
    messages = cl.direct_messages(thread_id, amount=1000)

    # Filter messages from last X days
    cutoff_date = datetime.now() - timedelta(days=days)
    recent_messages = [
        msg for msg in messages
        if msg.timestamp > cutoff_date
    ]

    # Analyze by user
    user_stats = {}
    for message in recent_messages:
        user_id = message.user_id
        if user_id not in user_stats:
            user_stats[user_id] = {
                'message_count': 0,
                'message_types': {},
                'most_active_hour': None
            }

        user_stats[user_id]['message_count'] += 1

        # Track message types
        msg_type = message.item_type
        user_stats[user_id]['message_types'][msg_type] = \
            user_stats[user_id]['message_types'].get(msg_type, 0) + 1

    return {
        'total_messages': len(recent_messages),
        'active_users': len(user_stats),
        'user_breakdown': user_stats,
        'busiest_day': get_busiest_day(recent_messages)
    }

def get_busiest_day(messages):
    """Find the day with most messages"""
    day_counts = {}
    for message in messages:
        day = message.timestamp.date()
        day_counts[day] = day_counts.get(day, 0) + 1

    return max(day_counts.items(), key=lambda x: x[1]) if day_counts else None
```

### Monitor New Messages
```python
class MessageMonitor:
    def __init__(self, client):
        self.cl = client
        self.last_check = {}

    def check_new_messages(self):
        """Check for new messages across all threads"""
        threads = self.cl.direct_threads(amount=50)
        new_messages = []

        for thread in threads:
            thread_id = thread.id
            latest_message = thread.last_permanent_item

            if thread_id not in self.last_check:
                self.last_check[thread_id] = latest_message.id
                continue

            if latest_message.id != self.last_check[thread_id]:
                # New message found
                messages = self.cl.direct_messages(thread_id, amount=10)
                for msg in messages:
                    if msg.id == self.last_check[thread_id]:
                        break
                    new_messages.append({
                        'thread_id': thread_id,
                        'message': msg,
                        'from_user': msg.user_id
                    })

                self.last_check[thread_id] = latest_message.id

        return new_messages

# Usage
monitor = MessageMonitor(cl)
new_msgs = monitor.check_new_messages()
for msg_info in new_msgs:
    print(f"New message in thread {msg_info['thread_id']}: {msg_info['message'].text}")
```

## 🤖 Automated Response System

### Auto-Reply Bot
```python
class AutoReplyBot:
    def __init__(self, client):
        self.cl = client
        self.auto_responses = {}
        self.enabled = True

    def add_auto_response(self, keyword, response):
        """Add keyword-based auto response"""
        self.auto_responses[keyword.lower()] = response

    def process_new_messages(self):
        """Process new messages and send auto replies"""
        if not self.enabled:
            return

        threads = self.cl.direct_threads(amount=20)

        for thread in threads:
            messages = self.cl.direct_messages(thread.id, amount=5)

            for message in messages:
                # Skip your own messages
                if message.user_id == self.cl.user_id:
                    continue

                # Check if already replied to this message
                if self.already_replied(thread.id, message.id):
                    continue

                # Check for keywords
                response = self.get_auto_response(message.text)
                if response:
                    self.cl.direct_send(
                        text=response,
                        thread_ids=[thread.id]
                    )
                    self.mark_as_replied(thread.id, message.id)

    def get_auto_response(self, text):
        """Get auto response for message text"""
        if not text:
            return None

        text_lower = text.lower()
        for keyword, response in self.auto_responses.items():
            if keyword in text_lower:
                return response

        return None

    def already_replied(self, thread_id, message_id):
        """Check if already replied to message"""
        # Implement your tracking logic here
        return False

    def mark_as_replied(self, thread_id, message_id):
        """Mark message as replied to"""
        # Implement your tracking logic here
        pass

# Usage
bot = AutoReplyBot(cl)
bot.add_auto_response("hello", "Hi there! Thanks for your message.")
bot.add_auto_response("price", "Please check our website for current pricing.")
bot.add_auto_response("support", "I'll connect you with our support team.")

# Run periodically
bot.process_new_messages()
```

### Smart Message Filtering
```python
def filter_spam_messages(thread_id):
    """Filter and handle spam messages"""
    messages = cl.direct_messages(thread_id, amount=50)

    spam_indicators = [
        "click here",
        "free money",
        "winner",
        "congratulations",
        "verify account"
    ]

    spam_messages = []
    for message in messages:
        if message.text:
            text_lower = message.text.lower()
            if any(indicator in text_lower for indicator in spam_indicators):
                spam_messages.append(message)

    return spam_messages

def auto_delete_spam(thread_id):
    """Automatically delete spam messages"""
    spam_messages = filter_spam_messages(thread_id)

    for spam_msg in spam_messages:
        try:
            cl.direct_message_delete(thread_id, spam_msg.id)
            print(f"Deleted spam message: {spam_msg.text[:50]}...")
        except Exception as e:
            print(f"Failed to delete spam message: {e}")

    return len(spam_messages)
```

## 📱 Direct Message Best Practices

### Rate Limiting for DMs
```python
import time
import random

# Daily limits for direct messages
DM_LIMITS = {
    'messages_per_hour': 60,
    'new_conversations_per_day': 20,
    'bulk_messages_per_day': 100
}

def rate_limited_send(text, user_ids, delay_range=(1, 3)):
    """Send message with rate limiting"""
    success = cl.direct_send(text=text, user_ids=user_ids)

    # Add random delay
    delay = random.uniform(*delay_range)
    time.sleep(delay)

    return success

def bulk_message_send(message, usernames, max_per_batch=10):
    """Send message to multiple users safely"""
    user_ids = []
    for username in usernames:
        try:
            user_id = cl.user_id_from_username(username)
            user_ids.append(user_id)
        except Exception as e:
            print(f"Failed to get user ID for {username}: {e}")

    # Send in batches
    sent_count = 0
    for i in range(0, len(user_ids), max_per_batch):
        batch = user_ids[i:i + max_per_batch]

        try:
            success = cl.direct_send(text=message, user_ids=batch)
            if success:
                sent_count += len(batch)

            # Delay between batches
            time.sleep(random.uniform(30, 60))

        except Exception as e:
            print(f"Failed to send batch: {e}")

    return sent_count
```

### Error Handling for DMs
```python
from instagrapi.exceptions import DirectError, UserNotFound

def safe_direct_send(text, user_ids):
    """Send direct message with error handling"""
    try:
        return cl.direct_send(text=text, user_ids=user_ids)
    except DirectError as e:
        print(f"Direct message error: {e}")
        return False
    except UserNotFound as e:
        print(f"User not found: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def validate_recipients(user_ids):
    """Validate recipient user IDs before sending"""
    valid_ids = []

    for user_id in user_ids:
        try:
            user_info = cl.user_info(user_id)
            # Check if user accepts messages
            if not user_info.is_private or user_info.friendship_status.following:
                valid_ids.append(user_id)
        except Exception as e:
            print(f"Invalid user ID {user_id}: {e}")

    return valid_ids
```

### Message Templates
```python
class MessageTemplates:
    """Pre-defined message templates for common scenarios"""

    WELCOME = "Welcome! Thanks for reaching out. How can I help you today?"

    BUSINESS_INQUIRY = """Thanks for your interest in our services!

Here's what we offer:
• Service 1
• Service 2
• Service 3

Would you like to schedule a consultation?"""

    FOLLOW_UP = "Hi! Just following up on our previous conversation. Let me know if you have any questions!"

    SUPPORT = """I understand you need help. Here are some options:

1️⃣ Check our FAQ: [link]
2️⃣ Email support: support@example.com
3️⃣ Schedule a call: [calendar link]

What works best for you?"""

    @staticmethod
    def personalized_greeting(name):
        return f"Hi {name}! Thanks for connecting. Looking forward to chatting with you! 😊"

    @staticmethod
    def product_recommendation(product_name, price):
        return f"""I think you'd love our {product_name}!

✨ Key features: [list features]
💰 Price: ${price}
🚚 Free shipping included

Would you like more details?"""

# Usage
templates = MessageTemplates()
welcome_msg = templates.WELCOME
personalized = templates.personalized_greeting("John")
```

## 🔐 Privacy & Security

### Message Privacy Controls
```python
def check_message_permissions(user_id):
    """Check if user can receive direct messages"""
    try:
        user_info = cl.user_info(user_id)

        return {
            'can_message': not user_info.is_private or user_info.friendship_status.following,
            'is_private': user_info.is_private,
            'following_them': user_info.friendship_status.following,
            'followed_by_them': user_info.friendship_status.followed_by,
            'restricted': user_info.friendship_status.is_restricted
        }
    except Exception as e:
        return {'error': str(e), 'can_message': False}

def safe_message_send(user_id, message):
    """Send message only if user can receive it"""
    permissions = check_message_permissions(user_id)

    if permissions.get('can_message'):
        return cl.direct_send(text=message, user_ids=[user_id])
    else:
        print(f"Cannot send message to user {user_id}: {permissions}")
        return False
```

### Message Backup System
```python
import json
from datetime import datetime

def backup_conversations(backup_file="dm_backup.json"):
    """Backup all direct message conversations"""
    threads = cl.direct_threads(amount=100)
    backup_data = {
        'backup_date': datetime.now().isoformat(),
        'conversations': []
    }

    for thread in threads:
        thread_data = {
            'thread_id': thread.id,
            'title': thread.thread_title,
            'users': [user.username for user in thread.users],
            'is_group': thread.is_group,
            'messages': []
        }

        messages = cl.direct_messages(thread.id, amount=500)
        for message in messages:
            msg_data = {
                'id': message.id,
                'user_id': message.user_id,
                'text': message.text,
                'timestamp': message.timestamp.isoformat(),
                'item_type': message.item_type
            }
            thread_data['messages'].append(msg_data)

        backup_data['conversations'].append(thread_data)

    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)

    return backup_file
```

This comprehensive direct messages documentation covers all aspects of Instagram DM functionality through the instagrapi library, including sending, receiving, managing conversations, automation, and security considerations.