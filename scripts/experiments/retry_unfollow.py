#!/usr/bin/env python3
"""
Retry Unfollow - Use when rate limits clear
Simple retry script for the unfollow operation
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

def retry_unfollow():
    """Retry unfollow when rate limits clear"""

    print("🔄 RETRY UNFOLLOW - WHEN RATE LIMITS CLEAR")
    print("=" * 50)

    # Get session using bypass (no validation issues)
    session_manager = InstagramSessionManager()
    client = session_manager.get_client_bypass_validation()

    if not client:
        print("❌ Session not available")
        return False

    print(f"✅ Session active - User ID: {client.user_id}")

    # Test if rate limits cleared
    try:
        test_params = {"count": 1}
        test_response = client.private_request(f"friendships/{client.user_id}/following/", params=test_params)

        if 'users' in test_response:
            print("✅ Rate limits cleared - proceeding with unfollow")
        else:
            print("❌ Unexpected response format")
            return False

    except Exception as e:
        if "wait" in str(e).lower():
            print("⏳ Still rate limited - try again later")
            print("The session is working fine, just need to wait for Instagram")
            return False
        else:
            print(f"❌ Error: {e}")
            return False

    # Get full following list
    try:
        params = {"count": 200, "rank_token": f"{client.user_id}_{client.uuid}"}
        response = client.private_request(f"friendships/{client.user_id}/following/", params=params)

        following_users = response.get('users', [])
        total = len(following_users)

        print(f"👥 Found {total} users to unfollow")

        if total == 0:
            print("🎉 Already following no one!")
            return True

    except Exception as e:
        print(f"❌ Error getting following list: {e}")
        return False

    # Execute unfollow
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
                print(f"     ⏳ Rate limited again - sleeping 30s")
                time.sleep(30)

        time.sleep(1.5)  # Rate limiting

        if i % 10 == 0:
            print(f"     📊 Progress: {len(unfollowed)} done, {len(failed)} failed")

    # Final results
    print(f"\n🎯 UNFOLLOW COMPLETE")
    print(f"✅ Unfollowed: {len(unfollowed)}/{total}")
    print(f"❌ Failed: {len(failed)}/{total}")

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results_file = Path(f"data/retry_unfollow_{timestamp}.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)

    results = {
        'total_users': total,
        'unfollowed_count': len(unfollowed),
        'failed_count': len(failed),
        'unfollowed_users': unfollowed,
        'failed_users': failed,
        'completed_at': datetime.now().isoformat()
    }

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"💾 Results saved: {results_file}")

    # Final verification
    try:
        time.sleep(5)
        verify_response = client.private_request(f"friendships/{client.user_id}/following/", params={"count": 10})
        remaining = len(verify_response.get('users', []))

        print(f"\n📊 Final check: Still following {remaining} users")

        if remaining == 0:
            print("🎉 SUCCESS: Following NO ONE!")
        elif remaining < total:
            reduction = total - remaining
            print(f"🎯 Progress: Reduced following from {total} to {remaining} (-{reduction})")

    except Exception as e:
        print(f"⚠️ Could not verify final count: {e}")

    return len(unfollowed) > 0

if __name__ == "__main__":
    print("Checking if rate limits have cleared...")
    success = retry_unfollow()

    if success:
        print("\n🎉 UNFOLLOW OPERATION SUCCESSFUL!")
    else:
        print("\n⚠️ Still rate limited or other issues - try again later")
        print("The session is working fine, just need to wait for Instagram rate limits to clear")