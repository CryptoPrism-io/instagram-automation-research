#!/usr/bin/env python3
"""
Quick Unfollow Test - Test with first 5 users only
"""

import sys
import os
from pathlib import Path
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.session_manager import InstagramSessionManager

def quick_unfollow_test():
    """Test unfollow with first 5 users only"""

    print("🧪 QUICK UNFOLLOW TEST - 5 USERS")
    print("=" * 40)

    # Load backup
    backup_file = Path("data/BACKUP_following_list_before_unfollow.json")
    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        test_users = backup_data['following_users'][:5]  # First 5 only
        print(f"📋 Testing with {len(test_users)} users")

    except Exception as e:
        print(f"❌ Error reading backup: {e}")
        return False

    # Get client
    try:
        session_manager = InstagramSessionManager()
        client = session_manager.get_client_bypass_validation()

        if not client:
            print("❌ No client")
            return False

        print(f"✅ Client ready - User ID: {client.user_id}")

    except Exception as e:
        print(f"❌ Client error: {e}")
        return False

    # Test unfollow
    unfollowed = []
    failed = []

    for i, user in enumerate(test_users, 1):
        username = user.get('username')

        print(f"{i}/5 @{username}...", end=" ")

        try:
            result = client.user_unfollow_by_username(username)

            if result:
                print("✅")
                unfollowed.append(username)
            else:
                print("❌")
                failed.append(username)

        except Exception as e:
            print(f"❌ {str(e)[:30]}")
            failed.append(username)

        time.sleep(3)  # Longer delay for safety

    # Results
    print(f"\n📊 TEST RESULTS")
    print(f"✅ Unfollowed: {len(unfollowed)}")
    print(f"❌ Failed: {len(failed)}")

    if unfollowed:
        print("✅ Unfollowed users:")
        for user in unfollowed:
            print(f"   @{user}")

    if failed:
        print("❌ Failed users:")
        for user in failed:
            print(f"   @{user}")

    return len(unfollowed) > 0

if __name__ == "__main__":
    success = quick_unfollow_test()

    if success:
        print("\n🎉 TEST SUCCESSFUL - Method working!")
    else:
        print("\n⚠️ Test had issues")