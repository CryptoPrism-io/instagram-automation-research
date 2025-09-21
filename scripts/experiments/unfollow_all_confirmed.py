#!/usr/bin/env python3
"""
Unfollow All - Direct Execution
Unfollows everyone immediately (confirmation already given)
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

def unfollow_all_confirmed():
    """Unfollow everyone - direct execution"""

    print("🚀 UNFOLLOWING EVERYONE - DIRECT EXECUTION")
    print("=" * 60)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ No session available")
            return

        my_user_id = client.user_id
        print(f"✅ Session active - User ID: {my_user_id}")

        # Get following list
        print(f"\n👥 Getting following list...")
        params = {
            "count": 200,
            "rank_token": f"{client.user_id}_{client.uuid}",
            "search_surface": "follow_list_page"
        }

        response = client.private_request(f"friendships/{my_user_id}/following/", params=params)
        following_users = response.get('users', [])
        total = len(following_users)

        print(f"✅ Found {total} users to unfollow")

        if total == 0:
            print("ℹ️ Not following anyone!")
            return

        # Start unfollowing
        unfollowed = []
        failed = []

        print(f"\n🚀 Starting unfollow process for {total} users...")
        print("=" * 60)

        for i, user in enumerate(following_users, 1):
            username = user.get('username')
            user_id = user.get('pk')

            print(f"{i:3d}/{total} Unfollowing @{username}...", end=" ")

            try:
                result = client.user_unfollow(user_id)

                if result:
                    print("✅")
                    unfollowed.append(username)
                else:
                    print("❌")
                    failed.append(username)

            except Exception as e:
                print(f"❌ {str(e)[:50]}")
                failed.append(username)

                if "wait" in str(e).lower():
                    print("     ⏳ Rate limited - sleeping 30s...")
                    time.sleep(30)

            # Rate limiting
            time.sleep(1.5)

        # Summary
        print(f"\n🎯 UNFOLLOW COMPLETE")
        print("=" * 40)
        print(f"✅ Unfollowed: {len(unfollowed)}/{total}")
        print(f"❌ Failed: {len(failed)}/{total}")

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {
            'total_before': total,
            'unfollowed_count': len(unfollowed),
            'failed_count': len(failed),
            'unfollowed_users': unfollowed,
            'failed_users': failed,
            'completed_at': datetime.now().isoformat()
        }

        results_file = Path(f"data/unfollow_results_{timestamp}.json")
        results_file.parent.mkdir(parents=True, exist_ok=True)

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved: {results_file}")

        # Final check
        try:
            check_response = client.private_request(f"friendships/{my_user_id}/following/", params={"count": 10})
            remaining = len(check_response.get('users', []))
            print(f"📊 Still following: {remaining} users")

            if remaining == 0:
                print("🎉 SUCCESS: Following NO ONE!")

        except:
            pass

    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    print("⚠️  This will unfollow ALL 95 users you are following")
    print("Press Ctrl+C within 5 seconds to cancel...")

    for i in range(5, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)

    print("Starting unfollow process...    ")
    unfollow_all_confirmed()