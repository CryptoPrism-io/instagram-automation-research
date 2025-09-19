# Instagrapi Best Practices

> **Source**: https://subzeroid.github.io/instagrapi/usage-guide/best-practices.html

This document outlines the essential best practices for using the instagrapi library to interact with Instagram's Private API while avoiding rate limits, account restrictions, and suspicious behavior detection.

## 🚨 Critical Best Practices Overview

### 1. Use a Proxy 🌐

**Why It's Essential:**
- Prevents rate limiting and suspicious login attempts
- Protects against IP-based account restrictions
- Allows for proper scaling with multiple accounts

**Safe Limits:**
- ✅ **10 accounts per IP address** (maximum)
- ✅ **4-16 posts per account per day**
- ✅ **24-48 stories per account per day**

**Recommended Proxy Setup:**
```python
from instagrapi import Client

cl = Client()
# Replace with your actual proxy credentials
cl.set_proxy("http://<api_key>:wifi;ca;;;toronto@proxy.soax.com:9137")
```

**Recommended Proxy Services:**
- **SOAX** (specifically mentioned in documentation)
- Rotating residential proxies
- High-quality datacenter proxies

### 2. Add Delays ⏰

**Purpose:**
- Mimic real human user behavior
- Prevent API rate limiting
- Avoid triggering Instagram's bot detection

**Implementation:**
```python
cl = Client()
# Set random delay between 1-3 seconds for all requests
cl.delay_range = [1, 3]
```

**Advanced Delay Strategies:**
```python
import random
import time

# Custom delay function for critical operations
def smart_delay():
    delay = random.uniform(2, 5)  # 2-5 second random delay
    time.sleep(delay)

# Use between sensitive operations
cl.media_like(media_id)
smart_delay()
cl.user_follow(user_id)
```

### 3. Use Sessions 💾

**Critical Importance:**
- Avoid logging in repeatedly with username/password
- Prevent suspicious login patterns
- Maintain account safety and longevity

**Session Management Best Practices:**
```python
import json
from pathlib import Path

def login_user():
    cl = Client()
    session_file = Path("session.json")

    # Try to load existing session first
    if session_file.exists():
        try:
            cl.load_settings(str(session_file))
            # Test if session is still valid
            cl.get_timeline_feed()
            print("✅ Session loaded successfully")
            return cl
        except Exception as e:
            print(f"⚠️ Session invalid: {e}")

    # Fallback to username/password login
    cl.login(USERNAME, PASSWORD)

    # Save session for future use
    cl.dump_settings(str(session_file))
    print("✅ New session created and saved")

    return cl
```

**Session Lifecycle Management:**
```python
class SessionManager:
    def __init__(self, session_file="session.json"):
        self.session_file = Path(session_file)
        self.client = Client()

    def smart_login(self, username, password):
        # Load existing session
        if self._load_session():
            if self._validate_session():
                return True

        # Fresh login if session invalid
        return self._fresh_login(username, password)

    def _load_session(self):
        if not self.session_file.exists():
            return False

        try:
            self.client.load_settings(str(self.session_file))
            return True
        except:
            return False

    def _validate_session(self):
        try:
            # Lightweight API call to test session
            self.client.user_info_by_username(self.client.username)
            return True
        except:
            return False

    def _fresh_login(self, username, password):
        try:
            self.client.login(username, password)
            self.client.dump_settings(str(self.session_file))
            return True
        except:
            return False
```

## 🛡️ Additional Safety Measures

### 4. Consistent IP Address
- Use the same IP address for the same account
- Avoid frequent IP changes which trigger security checks
- Consider dedicated IP addresses for important accounts

### 5. Random, Human-like Timing
- Vary the timing of your actions
- Don't post at exactly the same time every day
- Add randomness to your automation schedules

```python
import random
from datetime import datetime, timedelta

def get_random_post_time():
    # Random time between 9 AM and 6 PM
    base_hour = random.randint(9, 18)
    random_minutes = random.randint(0, 59)
    return f"{base_hour:02d}:{random_minutes:02d}"
```

### 6. Device Consistency
```python
# Preserve device UUIDs across sessions
def preserve_device_info(cl, old_session_file):
    if Path(old_session_file).exists():
        with open(old_session_file, 'r') as f:
            old_settings = json.load(f)

        # Preserve important device identifiers
        if 'uuids' in old_settings:
            cl.set_uuids(old_settings['uuids'])
```

## 📊 Monitoring and Safety

### Rate Limiting Guidelines
```python
# Safe action limits per day
DAILY_LIMITS = {
    'likes': 500,
    'follows': 200,
    'unfollows': 200,
    'comments': 50,
    'direct_messages': 100
}

# Track daily actions
def track_action(action_type):
    # Implement action counting
    # Stop automation if limits reached
    pass
```

### Error Handling
```python
from instagrapi.exceptions import (
    LoginRequired,
    ChallengeRequired,
    FeedbackRequired,
    RateLimitError
)

def safe_api_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except LoginRequired:
        # Re-authenticate
        print("🔄 Re-authentication required")
        return None
    except ChallengeRequired:
        # Handle 2FA or verification
        print("🚨 Challenge required - manual intervention needed")
        return None
    except RateLimitError:
        # Back off and retry later
        print("⏳ Rate limited - waiting...")
        time.sleep(3600)  # Wait 1 hour
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None
```

## 🎯 Practical Implementation

### Complete Setup Example
```python
from instagrapi import Client
import time
import random
import json
from pathlib import Path

def setup_instagram_client(username, password, proxy=None):
    """
    Complete setup following all best practices
    """
    cl = Client()

    # 1. Set proxy
    if proxy:
        cl.set_proxy(proxy)

    # 2. Set delays
    cl.delay_range = [1, 3]

    # 3. Session management
    session_file = Path(f"session_{username}.json")

    # Load existing session
    if session_file.exists():
        try:
            cl.load_settings(str(session_file))
            # Validate session
            cl.user_info_by_username(username)
            print("✅ Session loaded and validated")
            return cl
        except:
            print("⚠️ Session invalid, creating new one")

    # Fresh login
    cl.login(username, password)
    cl.dump_settings(str(session_file))
    print("✅ New session created")

    return cl

# Usage
USERNAME = "your_username"
PASSWORD = "your_password"
PROXY = "http://your-proxy-details"

cl = setup_instagram_client(USERNAME, PASSWORD, PROXY)
```

## ⚠️ What NOT to Do

### ❌ Common Mistakes to Avoid:
1. **Frequent logins** with username/password
2. **No delays** between actions
3. **Ignoring rate limits**
4. **Using residential IP** for multiple accounts
5. **Posting at exact same times** daily
6. **Not handling exceptions** properly
7. **Deleting session files** unnecessarily

### ❌ Suspicious Patterns:
- Posting every day at exactly 9:00 AM
- Liking posts in rapid succession
- Following/unfollowing users immediately
- Using the same captions repeatedly
- Operating from multiple IPs with same account

## 🔧 Recommended Tools & Services

### Proxy Services:
- **SOAX** (mentioned in official docs)
- Smartproxy
- Bright Data (formerly Luminati)

### Monitoring Tools:
- Custom action counters
- Error logging systems
- Session health monitors

## 📈 Success Metrics

### Healthy Account Indicators:
- ✅ No login challenges for weeks
- ✅ Consistent engagement rates
- ✅ No action blocks or restrictions
- ✅ Sessions lasting multiple days
- ✅ Smooth API responses

### Warning Signs:
- ⚠️ Frequent login challenges
- ⚠️ Reduced reach/engagement
- ⚠️ Action blocks (likes, follows, etc.)
- ⚠️ Session expiring quickly
- ⚠️ 429 (Rate Limited) responses

Following these best practices will help ensure your Instagram automation runs smoothly and safely without triggering Instagram's anti-bot measures.