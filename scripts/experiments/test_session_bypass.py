#!/usr/bin/env python3
"""
Test Session Bypass - Verify the bypass method works
Tests the new get_client_bypass_validation method
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

def test_session_bypass():
    """Test the session bypass method"""

    print("🧪 TESTING SESSION BYPASS METHOD")
    print("=" * 50)

    try:
        # Test the bypass method
        session_manager = InstagramSessionManager()
        client = session_manager.get_client_bypass_validation()

        if client:
            print("✅ Bypass method successful!")
            print(f"✅ User ID: {client.user_id}")

            # Test a simple API call that should work
            try:
                # Try to get current following count
                my_user_id = client.user_id
                params = {"count": 5}
                response = client.private_request(f"friendships/{my_user_id}/following/", params=params)

                if 'users' in response:
                    following_count = len(response['users'])
                    print(f"✅ API test successful - Found {following_count} users in following list")

                    # Show a few users to verify it's working
                    users = response['users']
                    if users:
                        print("👥 Sample following users:")
                        for i, user in enumerate(users[:3], 1):
                            username = user.get('username', 'unknown')
                            print(f"  {i}. @{username}")

                    print(f"\n🎯 SESSION IS WORKING! Ready for unfollow operation.")
                    return True
                else:
                    print("❌ API response missing 'users' field")
                    return False

            except Exception as e:
                print(f"❌ API test failed: {e}")
                return False

        else:
            print("❌ Bypass method failed - no client returned")
            return False

    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_session_bypass()

    if success:
        print("\n🎉 TEST PASSED - Session bypass working!")
        print("Ready to proceed with unfollow operation.")
    else:
        print("\n⚠️ TEST FAILED - Need to investigate further.")