#!/usr/bin/env python3
"""
Force Fresh Instagram Login - Create New Session
Bypasses rate limiting to create a fresh session
"""

import sys
import os
from pathlib import Path
from datetime import datetime
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

def force_fresh_login():
    """Force a fresh login and create new session"""

    print("🔄 Instagram Fresh Login - Creating New Session")
    print("=" * 60)

    try:
        # Initialize session manager
        session_manager = InstagramSessionManager()

        print("📱 Current session status:")
        session_info = session_manager.get_session_info()

        print(f"   Session file exists: {session_info['session_file_exists']}")
        print(f"   Client authenticated: {session_info['client_authenticated']}")

        if session_info.get('session_age_hours'):
            print(f"   Session age: {session_info['session_age_hours']:.1f} hours")

        print("\n🚀 Forcing fresh login (bypassing rate limits)...")

        # Force fresh login
        client = session_manager.force_refresh_session()

        if client:
            print("✅ Fresh login successful!")

            # Test the connection
            print("\n🔍 Testing new session...")
            user_info = client.account_info()
            print(f"✅ Authenticated as: @{user_info.username}")
            print(f"   User ID: {user_info.pk}")
            print(f"   Followers: {user_info.follower_count}")
            print(f"   Following: {user_info.following_count}")

            # Get session info again
            new_session_info = session_manager.get_session_info()
            print(f"\n📊 New session created:")
            print(f"   Username: {new_session_info['metadata'].get('username')}")
            print(f"   Created: {new_session_info['metadata'].get('created_at')}")
            print(f"   Session file: {session_manager.session_file}")

            return True

        else:
            print("❌ Fresh login failed!")
            return False

    except Exception as e:
        print(f"💥 Error during fresh login: {e}")
        return False

def test_session_functionality(session_manager):
    """Test basic session functionality"""

    print("\n🧪 Testing Session Functionality")
    print("-" * 40)

    try:
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get client")
            return False

        # Test 1: Account info
        print("🔍 Test 1: Account info...")
        account = client.account_info()
        print(f"   ✅ Username: @{account.username}")

        # Test 2: User lookup
        print("🔍 Test 2: User lookup...")
        yoga_user = client.user_info_by_username("yoga_ss_")
        print(f"   ✅ Found: @{yoga_user.username} (ID: {yoga_user.pk})")

        # Test 3: Try getting followers (might fail due to privacy)
        print("🔍 Test 3: Follower access test...")
        try:
            followers = client.user_followers(yoga_user.pk, amount=5)
            print(f"   ✅ Followers accessible: {len(followers)} retrieved")
        except Exception as e:
            print(f"   ⚠️ Followers restricted: {e}")

        return True

    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Instagram Session Manager - Fresh Login")
    print("This will create a new session bypassing rate limits")

    success = force_fresh_login()

    if success:
        print("\n🎉 New session created successfully!")
        print("You can now use the session for follower analysis.")

        # Test functionality
        session_manager = InstagramSessionManager()
        test_session_functionality(session_manager)

    else:
        print("\n😞 Failed to create new session")