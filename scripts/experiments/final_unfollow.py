#!/usr/bin/env python3
"""
Final Unfollow Script - Using correct user_unfollow method
Uses user IDs from backup file and the correct instagrapi method
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

def final_unfollow():
    """Unfollow everyone using the correct method and user IDs"""

    print("🚀 FINAL UNFOLLOW - CORRECT METHOD")
    print("=" * 60)

    # Load backup with user IDs
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

        # Check if we have user IDs in the backup
        has_user_ids = any('user_id' in user for user in following_users[:5])
        if not has_user_ids:
            print("⚠️ Backup doesn't contain user IDs - will need to get them")

    except Exception as e:
        print(f"❌ Error reading backup: {e}")
        return False

    # Get client using bypass method
    try:
        session_manager = InstagramSessionManager()
        client = session_manager.get_client_bypass_validation()

        if not client:
            print("❌ Could not get client")
            return False

        my_user_id = client.user_id
        print(f"✅ Session loaded - User ID: {my_user_id}")

    except Exception as e:
        print(f"❌ Session error: {e}")
        return False

    # Get current following list with user IDs
    print(f"\n👥 Getting current following list with user IDs...")
    try:
        params = {
            "count": 200,
            "rank_token": f"{client.user_id}_{client.uuid}",
            "search_surface": "follow_list_page"
        }

        response = client.private_request(f"friendships/{my_user_id}/following/", params=params)

        if 'users' not in response:
            print("❌ Could not get following list")
            return False

        current_following = response['users']
        current_total = len(current_following)

        print(f"✅ Currently following: {current_total} users")

        if current_total == 0:
            print("🎉 ALREADY FOLLOWING NO ONE!")
            return True

    except Exception as e:
        if "wait" in str(e).lower():
            print(f"⏳ Rate limited: {e}")
            print("⚠️ Proceeding with backup list...")
            current_following = following_users  # Use backup
        else:
            print(f"❌ Error getting current following: {e}")
            return False

    # Start unfollowing process
    print(f"\n🚀 Starting unfollow process...")
    print("=" * 60)

    unfollowed = []
    failed = []

    for i, user in enumerate(current_following, 1):
        username = user.get('username', 'unknown')
        user_id = user.get('pk') or user.get('user_id')  # Try both keys

        if not user_id:
            print(f"{i:3d}/{len(current_following)} @{username}... ❌ No user ID")
            failed.append(username)
            continue

        print(f"{i:3d}/{len(current_following)} @{username}...", end=" ")

        try:
            # Use the correct method with user ID
            result = client.user_unfollow(user_id)

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

        # Break if we've had too many failures
        if len(failed) > 20 and len(unfollowed) == 0:
            print("     ⚠️ Too many failures - stopping to investigate")
            break

    # Final summary
    print(f"\n🎯 UNFOLLOW COMPLETE")
    print("=" * 40)
    print(f"✅ Unfollowed: {len(unfollowed)}/{len(current_following)}")
    print(f"❌ Failed: {len(failed)}/{len(current_following)}")

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {
        'operation': 'final_unfollow',
        'total_before': len(current_following),
        'unfollowed_count': len(unfollowed),
        'failed_count': len(failed),
        'unfollowed_users': unfollowed,
        'failed_users': failed,
        'completed_at': datetime.now().isoformat()
    }

    results_file = Path(f"data/final_unfollow_results_{timestamp}.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved: {results_file}")

    # Show sample results
    if unfollowed:
        print(f"\n✅ SAMPLE UNFOLLOWED ({len(unfollowed)} total):")
        for username in unfollowed[:5]:
            print(f"   @{username}")
        if len(unfollowed) > 5:
            print(f"   ... and {len(unfollowed)-5} more")

    if failed:
        print(f"\n❌ SAMPLE FAILED ({len(failed)} total):")
        for username in failed[:5]:
            print(f"   @{username}")
        if len(failed) > 5:
            print(f"   ... and {len(failed)-5} more")

    # Final verification
    try:
        time.sleep(5)
        check_params = {"count": 10}
        check_response = client.private_request(f"friendships/{my_user_id}/following/", params=check_params)
        remaining = len(check_response.get('users', []))
        print(f"\n📊 Final check: Still following {remaining} users")

        if remaining == 0:
            print("🎉 SUCCESS: Following NO ONE!")
        elif remaining < len(current_following):
            print(f"🎯 Progress made: Reduced from {len(current_following)} to {remaining}")

    except Exception as e:
        print(f"⚠️ Could not verify final count: {e}")

    success_rate = len(unfollowed) / len(current_following) if current_following else 0
    return success_rate > 0.5  # Success if > 50% unfollowed

if __name__ == "__main__":
    print("🔥 FINAL UNFOLLOW - Starting in 3 seconds...")
    print("Using correct user_unfollow method with user IDs")
    print("Press Ctrl+C to cancel...")

    for i in range(3, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)

    print("Starting final unfollow process...      ")
    success = final_unfollow()

    if success:
        print("\n🎉 OPERATION SUCCESSFUL!")
    else:
        print("\n⚠️ Operation had issues - check results")