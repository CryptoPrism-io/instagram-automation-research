#!/usr/bin/env python3
"""
Direct Follower Test - Test follower access with new session
"""

import sys
import os
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.session_manager import InstagramSessionManager

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_yoga_follower_access():
    """Test direct follower access for yoga_ss_"""

    print("🧪 Direct Follower Access Test")
    print("=" * 50)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get Instagram client")
            return

        print("✅ Session active")

        # Get yoga_ss_ user info
        print("🔍 Looking up @yoga_ss_...")
        yoga_user = client.user_info_by_username("yoga_ss_")
        print(f"✅ Found: @{yoga_user.username}")
        print(f"   User ID: {yoga_user.pk}")
        print(f"   Full Name: {yoga_user.full_name}")
        print(f"   Followers: {yoga_user.follower_count}")
        print(f"   Following: {yoga_user.following_count}")
        print(f"   Is Private: {yoga_user.is_private}")

        # Try to get followers
        print("\n👥 Attempting to get followers...")
        try:
            followers = client.user_followers(yoga_user.pk, amount=10)
            print(f"✅ SUCCESS! Retrieved {len(followers)} followers:")

            for i, follower in enumerate(followers[:5], 1):
                print(f"   {i}. @{follower.username} ({follower.full_name})")

        except Exception as e:
            print(f"❌ Followers access failed: {e}")

        # Try to get following
        print("\n👤 Attempting to get following...")
        try:
            following = client.user_following(yoga_user.pk, amount=10)
            print(f"✅ SUCCESS! Retrieved {len(following)} following:")

            for i, follow in enumerate(following[:5], 1):
                print(f"   {i}. @{follow.username} ({follow.full_name})")

        except Exception as e:
            print(f"❌ Following access failed: {e}")

        # Check if you follow each other
        print("\n🤝 Checking mutual connection...")
        try:
            friendship = client.user_friendship(yoga_user.pk)
            print(f"   You follow @yoga_ss_: {friendship.following}")
            print(f"   @yoga_ss_ follows you: {friendship.followed_by}")
        except Exception as e:
            print(f"❌ Friendship check failed: {e}")

    except Exception as e:
        print(f"💥 Test failed: {e}")

if __name__ == "__main__":
    test_yoga_follower_access()