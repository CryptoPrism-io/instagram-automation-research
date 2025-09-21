#!/usr/bin/env python3
"""
Unfollow Script Using Session Bypass
Uses the bypass method to avoid false session expiration errors
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

def unfollow_with_bypass():
    """Unfollow everyone using the session bypass method"""

    print("🚀 UNFOLLOW WITH SESSION BYPASS")
    print("=" * 60)

    # Load backup to know who to unfollow
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

    except Exception as e:
        print(f"❌ Error reading backup: {e}")
        return False

    # Get client using bypass method
    try:
        session_manager = InstagramSessionManager()
        client = session_manager.get_client_bypass_validation()

        if not client:
            print("❌ Could not get client with bypass method")
            return False

        my_user_id = client.user_id
        print(f"✅ Session loaded - User ID: {my_user_id}")

    except Exception as e:
        print(f"❌ Session bypass failed: {e}")
        return False

    # Try to get current following list first
    try:
        params = {"count": 10}
        response = client.private_request(f"friendships/{my_user_id}/following/", params=params)

        if 'users' in response:
            current_following = len(response['users'])
            print(f"📊 Currently following: {current_following} users (quick check)")

            if current_following == 0:
                print("🎉 ALREADY FOLLOWING NO ONE!")
                return True

        else:
            print("⚠️ Could not verify current following count")

    except Exception as e:
        if "wait" in str(e).lower():
            print(f"⏳ Rate limited on check: {e}")
            print("⚠️ Proceeding with unfollow from backup list...")
        else:
            print(f"❌ Error checking current following: {e}")
            return False

    # Start unfollowing process
    print(f"\n🚀 Starting unfollow process for {total} users...")
    print("=" * 60)

    unfollowed = []
    failed = []

    for i, user in enumerate(following_users, 1):
        username = user.get('username')

        print(f"{i:3d}/{total} @{username}...", end=" ")

        try:
            # Try unfollow by username
            result = client.user_unfollow_by_username(username)

            if result:
                print("✅")
                unfollowed.append(username)
            else:
                print("❌")
                failed.append(username)

        except Exception as e:
            error_msg = str(e)
            print(f"❌ {error_msg[:30]}")
            failed.append(username)

            # Handle rate limits
            if "wait" in error_msg.lower() or "limit" in error_msg.lower():
                print("     ⏳ Rate limited - sleeping 30s...")
                time.sleep(30)

        # Rate limiting between requests
        time.sleep(2)

        # Progress update every 10 users
        if i % 10 == 0:
            print(f"     📊 Progress: {len(unfollowed)} ✅ | {len(failed)} ❌")

        # If we hit too many failures in a row, pause longer
        if len(failed) > len(unfollowed) and i > 10:
            print("     ⏳ Many failures - extending delay...")
            time.sleep(10)

    # Final summary
    print(f"\n🎯 UNFOLLOW COMPLETE")
    print("=" * 40)
    print(f"✅ Unfollowed: {len(unfollowed)}/{total}")
    print(f"❌ Failed: {len(failed)}/{total}")

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {
        'operation': 'unfollow_with_bypass',
        'total_before': total,
        'unfollowed_count': len(unfollowed),
        'failed_count': len(failed),
        'unfollowed_users': unfollowed,
        'failed_users': failed,
        'completed_at': datetime.now().isoformat()
    }

    results_file = Path(f"data/unfollow_bypass_results_{timestamp}.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved: {results_file}")

    # Show results summary
    if unfollowed:
        print(f"\n✅ SUCCESSFULLY UNFOLLOWED ({len(unfollowed)}):")
        for username in unfollowed[:10]:  # Show first 10
            print(f"   @{username}")
        if len(unfollowed) > 10:
            print(f"   ... and {len(unfollowed)-10} more")

    if failed:
        print(f"\n❌ FAILED TO UNFOLLOW ({len(failed)}):")
        for username in failed[:5]:  # Show first 5
            print(f"   @{username}")
        if len(failed) > 5:
            print(f"   ... and {len(failed)-5} more")

    # Final verification attempt
    try:
        time.sleep(5)  # Wait a bit before final check
        check_params = {"count": 5}
        check_response = client.private_request(f"friendships/{my_user_id}/following/", params=check_params)
        remaining = len(check_response.get('users', []))
        print(f"\n📊 Final check: Still following {remaining} users")

        if remaining == 0:
            print("🎉 SUCCESS: Following NO ONE!")
        elif remaining < 10:
            print(f"🎯 Almost done: Only {remaining} users remaining")

    except Exception as e:
        print(f"⚠️ Could not verify final count: {e}")

    return len(failed) < total  # Success if not all failed

if __name__ == "__main__":
    print("🔥 UNFOLLOW WITH BYPASS - Starting in 3 seconds...")
    print("Press Ctrl+C to cancel...")

    for i in range(3, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)

    print("Starting unfollow process...      ")
    success = unfollow_with_bypass()

    if success:
        print("\n🎉 OPERATION COMPLETED!")
    else:
        print("\n⚠️ Operation had issues - check results file")