#!/usr/bin/env python3
"""
Wait and Unfollow - Wait for rate limits then execute
Waits and retries until rate limits clear
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

def wait_and_unfollow():
    """Wait for rate limits to clear then execute unfollow"""

    print("⏳ WAIT AND UNFOLLOW - PERSISTENT RETRY")
    print("=" * 50)

    # Get session
    session_manager = InstagramSessionManager()
    client = session_manager.get_client_bypass_validation()

    if not client:
        print("❌ No session")
        return False

    print(f"✅ Session ready - User ID: {client.user_id}")

    # Wait for rate limits to clear
    max_attempts = 10
    for attempt in range(1, max_attempts + 1):
        print(f"\n🔄 Attempt {attempt}/{max_attempts} - Testing rate limits...")

        try:
            test_params = {"count": 1}
            test_response = client.private_request(f"friendships/{client.user_id}/following/", params=test_params)

            if 'users' in test_response:
                print("✅ Rate limits cleared! Starting unfollow...")
                break
            else:
                print("❌ Unexpected response")
                return False

        except Exception as e:
            if "wait" in str(e).lower():
                wait_time = min(30 + (attempt * 10), 120)  # Progressive wait: 40s, 50s, 60s... max 120s
                print(f"⏳ Still rate limited - waiting {wait_time}s before retry {attempt+1}")
                time.sleep(wait_time)
                continue
            else:
                print(f"❌ Error: {e}")
                return False
    else:
        print("❌ Max attempts reached - still rate limited")
        return False

    # Rate limits cleared - proceed with unfollow
    try:
        params = {"count": 200, "rank_token": f"{client.user_id}_{client.uuid}"}
        response = client.private_request(f"friendships/{client.user_id}/following/", params=params)

        following_users = response.get('users', [])
        total = len(following_users)

        print(f"\n👥 Found {total} users to unfollow")

        if total == 0:
            print("🎉 Already following no one!")
            return True

    except Exception as e:
        print(f"❌ Error getting following list: {e}")
        return False

    # Execute unfollow operation
    print(f"\n🚀 Starting unfollow operation...")
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
            print(f"❌")
            failed.append(username)

            if "wait" in str(e).lower():
                print(f"\n     ⏳ Hit rate limit during operation - sleeping 30s")
                time.sleep(30)

        # Rate limiting between requests
        time.sleep(2)

        # Progress update
        if i % 10 == 0:
            success_rate = (len(unfollowed) / i) * 100
            print(f"\n     📊 Progress: {len(unfollowed)}/{i} ({success_rate:.0f}% success)")

    # Final results
    print(f"\n🎯 UNFOLLOW OPERATION COMPLETE")
    print("=" * 40)
    print(f"✅ Successfully unfollowed: {len(unfollowed)}/{total}")
    print(f"❌ Failed to unfollow: {len(failed)}/{total}")

    if len(unfollowed) > 0:
        success_percentage = (len(unfollowed) / total) * 100
        print(f"📊 Success rate: {success_percentage:.1f}%")

    # Save detailed results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = Path(f"data/wait_unfollow_results_{timestamp}.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)

    results = {
        'operation': 'wait_and_unfollow',
        'total_users_before': total,
        'unfollowed_count': len(unfollowed),
        'failed_count': len(failed),
        'success_rate_percent': (len(unfollowed) / total * 100) if total > 0 else 0,
        'unfollowed_users': unfollowed,
        'failed_users': failed,
        'completed_at': datetime.now().isoformat()
    }

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved: {results_file}")

    # Show sample of unfollowed users
    if unfollowed:
        print(f"\n✅ SAMPLE UNFOLLOWED USERS:")
        for username in unfollowed[:10]:
            print(f"   @{username}")
        if len(unfollowed) > 10:
            print(f"   ... and {len(unfollowed)-10} more")

    # Final verification
    try:
        print(f"\n🔍 Final verification...")
        time.sleep(3)
        verify_response = client.private_request(f"friendships/{client.user_id}/following/", params={"count": 10})
        remaining = len(verify_response.get('users', []))

        print(f"📊 Still following: {remaining} users")

        if remaining == 0:
            print("🎉 SUCCESS: Following NO ONE!")
        elif remaining < total:
            reduction = total - remaining
            print(f"🎯 Good progress: Reduced from {total} to {remaining} (-{reduction} users)")

    except Exception as e:
        print(f"⚠️ Could not verify final count: {e}")

    return len(unfollowed) > 0

if __name__ == "__main__":
    print("Starting persistent unfollow operation...")
    print("Will wait for rate limits to clear automatically")

    success = wait_and_unfollow()

    if success:
        print("\n🎉 UNFOLLOW OPERATION SUCCESSFUL!")
        print("Check the results file for detailed information")
    else:
        print("\n⚠️ Operation encountered issues")
        print("Session is still working - can retry later")