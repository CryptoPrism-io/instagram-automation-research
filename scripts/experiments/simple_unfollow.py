#!/usr/bin/env python3
"""
Simple Unfollow Script - Final attempt
Uses simple approach to unfollow everyone
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

def simple_unfollow():
    """Simple unfollow using backup list"""

    print("🚀 SIMPLE UNFOLLOW - FINAL ATTEMPT")
    print("=" * 60)

    # Load backup with proper encoding
    backup_file = Path("data/BACKUP_following_list_before_unfollow.json")
    if not backup_file.exists():
        print("❌ Backup file not found")
        return False

    try:
        with open(backup_file, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        following_users = backup_data['following_users']
        total = len(following_users)

        print(f"📋 Found {total} users to unfollow from backup")

        # Show who we're about to unfollow
        print(f"\n👥 USERS TO UNFOLLOW:")
        for i, user in enumerate(following_users[:10], 1):  # Show first 10
            username = user.get('username', 'unknown')
            print(f"  {i:2d}. @{username}")

        if total > 10:
            print(f"     ... and {total-10} more users")

    except Exception as e:
        print(f"❌ Error reading backup file: {e}")
        return False

    # Try using session manager one more time
    try:
        from core.session_manager import InstagramSessionManager

        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()  # Use existing method

        if client:
            print(f"✅ Got client instance")

            # Try to get current following list to verify session
            try:
                my_user_id = client.user_id
                print(f"✅ User ID: {my_user_id}")

                # Try a simple API call
                params = {"count": 5}
                response = client.private_request(f"friendships/{my_user_id}/following/", params=params)
                current_following = response.get('users', [])

                print(f"✅ Currently following {len(current_following)} users (from quick check)")

                if len(current_following) == 0:
                    print("🎉 ALREADY FOLLOWING NO ONE!")
                    return True

                # Start unfollowing process
                unfollowed = []
                failed = []

                print(f"\n🚀 Starting unfollow process...")
                print("=" * 40)

                for i, user in enumerate(following_users, 1):
                    username = user.get('username')

                    print(f"{i:3d}/{total} @{username}...", end=" ")

                    try:
                        # Try to unfollow by username
                        result = client.user_unfollow_by_username(username)

                        if result:
                            print("✅")
                            unfollowed.append(username)
                        else:
                            print("❌")
                            failed.append(username)

                    except Exception as e:
                        print(f"❌")
                        failed.append(username)

                    # Rate limit
                    time.sleep(1.5)

                    # Progress every 10
                    if i % 10 == 0:
                        print(f"     📊 {len(unfollowed)} done, {len(failed)} failed")

                # Final summary
                print(f"\n🎯 SUMMARY")
                print("=" * 30)
                print(f"✅ Unfollowed: {len(unfollowed)}")
                print(f"❌ Failed: {len(failed)}")

                # Save minimal results
                results = {
                    'unfollowed_count': len(unfollowed),
                    'failed_count': len(failed),
                    'unfollowed_users': unfollowed,
                    'failed_users': failed,
                    'completed_at': datetime.now().isoformat()
                }

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                results_file = Path(f"data/simple_unfollow_{timestamp}.json")
                results_file.parent.mkdir(parents=True, exist_ok=True)

                with open(results_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2)

                print(f"💾 Results: {results_file}")

                return len(failed) == 0

            except Exception as e:
                print(f"❌ API call failed: {e}")
                return False

        else:
            print("❌ Could not get client")
            return False

    except Exception as e:
        print(f"❌ Session error: {e}")
        return False

if __name__ == "__main__":
    success = simple_unfollow()

    if success:
        print("\n🎉 SUCCESS!")
    else:
        print("\n⚠️ Some issues occurred")