#!/usr/bin/env python3
"""
Unfollow Now - Use the working session immediately
No delays, just execute the unfollow operation
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

def unfollow_now():
    """Execute unfollow immediately with working session"""

    print("🚀 UNFOLLOW NOW - USING WORKING SESSION")
    print("=" * 60)

    # Get working client
    try:
        session_manager = InstagramSessionManager()
        client = session_manager.get_client_bypass_validation()

        if not client:
            print("❌ No client")
            return False

        my_user_id = client.user_id
        print(f"✅ Session ready - User ID: {my_user_id}")

    except Exception as e:
        print(f"❌ Session error: {e}")
        return False

    # Get current following list
    print(f"\n👥 Getting following list...")
    try:
        params = {
            "count": 200,
            "rank_token": f"{client.user_id}_{client.uuid}"
        }

        response = client.private_request(f"friendships/{my_user_id}/following/", params=params)

        if 'users' not in response:
            print("❌ No users in response")
            return False

        following_users = response['users']
        total = len(following_users)

        print(f"✅ Found {total} users to unfollow")

        if total == 0:
            print("🎉 ALREADY FOLLOWING NO ONE!")
            return True

    except Exception as e:
        print(f"❌ Error getting following: {e}")
        return False

    # Start unfollowing
    print(f"\n🚀 Unfollowing {total} users...")
    print("=" * 40)

    unfollowed = []
    failed = []

    for i, user in enumerate(following_users, 1):
        username = user.get('username', 'unknown')
        user_id = user.get('pk')

        print(f"{i:3d}/{total} @{username}...", end=" ")

        try:
            result = client.user_unfollow(user_id)

            if result:
                print("✅")
                unfollowed.append(username)
            else:
                print("❌")
                failed.append(username)

        except Exception as e:
            print(f"❌ {str(e)[:20]}")
            failed.append(username)

            if "wait" in str(e).lower():
                print("     ⏳ Rate limited - sleeping 15s...")
                time.sleep(15)

        # Quick delay
        time.sleep(1)

        if i % 20 == 0:
            print(f"     📊 {len(unfollowed)} ✅ | {len(failed)} ❌")

    # Results
    print(f"\n🎯 COMPLETE")
    print(f"✅ Unfollowed: {len(unfollowed)}")
    print(f"❌ Failed: {len(failed)}")

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {
        'unfollowed_count': len(unfollowed),
        'failed_count': len(failed),
        'unfollowed_users': unfollowed,
        'failed_users': failed,
        'completed_at': datetime.now().isoformat()
    }

    results_file = Path(f"data/unfollow_now_{timestamp}.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"💾 Results: {results_file}")

    # Final check
    try:
        check_response = client.private_request(f"friendships/{my_user_id}/following/", params={"count": 5})
        remaining = len(check_response.get('users', []))
        print(f"📊 Still following: {remaining}")

        if remaining == 0:
            print("🎉 SUCCESS: Following NO ONE!")

    except:
        pass

    return len(unfollowed) > 0

if __name__ == "__main__":
    success = unfollow_now()

    if success:
        print("\n🎉 DONE!")
    else:
        print("\n⚠️ Issues occurred")