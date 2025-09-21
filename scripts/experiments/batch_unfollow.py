#!/usr/bin/env python3
"""
Batch Unfollow Script - Robust Implementation
Unfollows users in small batches to avoid timeouts
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

def batch_unfollow_all():
    """Unfollow all users in small batches"""

    print("🚀 BATCH UNFOLLOW - ROBUST IMPLEMENTATION")
    print("=" * 60)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ No session available")
            return False

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
            return True

        # Process in batches of 10
        batch_size = 10
        unfollowed = []
        failed = []

        print(f"\n🚀 Processing {total} users in batches of {batch_size}...")
        print("=" * 60)

        for batch_start in range(0, total, batch_size):
            batch_end = min(batch_start + batch_size, total)
            batch_users = following_users[batch_start:batch_end]

            print(f"\n📦 BATCH {batch_start//batch_size + 1}: Users {batch_start+1}-{batch_end}")
            print("-" * 50)

            for i, user in enumerate(batch_users):
                username = user.get('username')
                user_id = user.get('pk')
                global_index = batch_start + i + 1

                print(f"{global_index:3d}/{total} @{username}...", end=" ")

                try:
                    result = client.user_unfollow(user_id)

                    if result:
                        print("✅")
                        unfollowed.append(username)
                    else:
                        print("❌")
                        failed.append(username)

                except Exception as e:
                    print(f"❌ {str(e)[:30]}")
                    failed.append(username)

                    if "wait" in str(e).lower():
                        print(f"     ⏳ Rate limited - sleeping 30s...")
                        time.sleep(30)

                # Small delay between each unfollow
                time.sleep(1.2)

            # Longer delay between batches
            if batch_end < total:
                print(f"     ⏳ Batch complete. Sleeping 10s before next batch...")
                time.sleep(10)

        # Summary
        print(f"\n🎯 UNFOLLOW COMPLETE")
        print("=" * 40)
        print(f"✅ Unfollowed: {len(unfollowed)}/{total}")
        print(f"❌ Failed: {len(failed)}/{total}")

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results = {
            'operation': 'batch_unfollow_all',
            'total_before': total,
            'unfollowed_count': len(unfollowed),
            'failed_count': len(failed),
            'unfollowed_users': unfollowed,
            'failed_users': failed,
            'completed_at': datetime.now().isoformat(),
            'batch_size': batch_size
        }

        results_file = Path(f"data/batch_unfollow_results_{timestamp}.json")
        results_file.parent.mkdir(parents=True, exist_ok=True)

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"\n💾 Results saved: {results_file}")

        # Final verification
        try:
            check_response = client.private_request(f"friendships/{my_user_id}/following/", params={"count": 10})
            remaining = len(check_response.get('users', []))
            print(f"📊 Still following: {remaining} users")

            if remaining == 0:
                print("🎉 SUCCESS: Following NO ONE!")
            else:
                print(f"ℹ️ {remaining} users remaining (may be due to failures)")

        except Exception as e:
            print(f"⚠️ Could not verify: {e}")

        return len(failed) == 0

    except Exception as e:
        print(f"💥 Error: {e}")
        return False

if __name__ == "__main__":
    print("🔥 BATCH UNFOLLOW - Starting in 3 seconds...")
    print("Press Ctrl+C to cancel...")

    for i in range(3, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)

    print("Starting batch unfollow process...     ")
    success = batch_unfollow_all()

    if success:
        print("\n🎉 OPERATION COMPLETED SUCCESSFULLY!")
    else:
        print("\n⚠️ Operation completed with some issues.")