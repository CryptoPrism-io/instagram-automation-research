#!/usr/bin/env python3
"""
Unfollow Everyone Script
Unfollows all users you are currently following
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

def unfollow_everyone():
    """Unfollow all users you are currently following"""

    print("⚠️  UNFOLLOW EVERYONE")
    print("This will unfollow ALL users you are currently following")
    print("=" * 60)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ No session available")
            return

        # Get your user ID
        my_user_id = client.user_id
        print(f"✅ Session active - User ID: {my_user_id}")

        try:
            account = client.account_info()
            print(f"✅ Logged in as: @{account.username}")
        except:
            print("ℹ️ Session working")

        # Get list of users you're following
        print(f"\n👥 Getting list of users you're following...")
        try:
            params = {
                "count": 200,  # Get up to 200 users you're following
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            response = client.private_request(f"friendships/{my_user_id}/following/", params=params)

            if 'users' not in response:
                print("❌ No following data received")
                return

            following_users = response['users']
            total_following = len(following_users)
            print(f"✅ Found {total_following} users you are following")

            if total_following == 0:
                print("ℹ️ You're not following anyone!")
                return

        except Exception as e:
            print(f"❌ Failed to get following list: {e}")
            return

        # Display the list before unfollowing
        print(f"\n📋 USERS YOU ARE FOLLOWING ({total_following}):")
        print("-" * 50)
        for i, user in enumerate(following_users, 1):
            username = user.get('username')
            full_name = user.get('full_name', '')
            is_verified = user.get('is_verified', False)

            status = "✅" if is_verified else "👤"
            print(f"{i:3d}. {status} @{username}")
            if full_name:
                print(f"      {full_name}")

        # Confirmation prompt
        print(f"\n⚠️  CONFIRMATION REQUIRED")
        print(f"You are about to unfollow {total_following} users.")
        print(f"This action cannot be easily undone.")

        confirm = input(f"\nType 'UNFOLLOW ALL' to confirm: ").strip()

        if confirm != "UNFOLLOW ALL":
            print("❌ Operation cancelled")
            return

        # Start unfollowing process
        print(f"\n🚀 Starting unfollow process...")
        print("=" * 60)

        unfollowed = []
        failed = []

        for i, user in enumerate(following_users, 1):
            username = user.get('username')
            user_id = user.get('pk')

            print(f"\n{i:3d}/{total_following} Unfollowing @{username}...")

            try:
                # Unfollow the user
                result = client.user_unfollow(user_id)

                if result:
                    print(f"     ✅ Successfully unfollowed @{username}")
                    unfollowed.append({
                        'username': username,
                        'user_id': str(user_id),
                        'full_name': user.get('full_name', ''),
                        'unfollowed_at': datetime.now().isoformat()
                    })
                else:
                    print(f"     ❌ Failed to unfollow @{username}")
                    failed.append({
                        'username': username,
                        'user_id': str(user_id),
                        'error': 'Unfollow returned False'
                    })

            except Exception as e:
                error_msg = str(e)
                print(f"     ❌ Error unfollowing @{username}: {error_msg}")
                failed.append({
                    'username': username,
                    'user_id': str(user_id),
                    'error': error_msg
                })

                # If we hit rate limits, slow down
                if "wait" in error_msg.lower() or "limit" in error_msg.lower():
                    print(f"     ⏳ Rate limited - sleeping for 30 seconds...")
                    time.sleep(30)

            # Rate limiting - be respectful
            if i < total_following:
                sleep_time = 2  # 2 seconds between unfollows
                print(f"     ⏳ Waiting {sleep_time}s before next unfollow...")
                time.sleep(sleep_time)

        # Final summary
        print(f"\n🎯 UNFOLLOW OPERATION COMPLETE")
        print("=" * 50)
        print(f"✅ Successfully unfollowed: {len(unfollowed)}/{total_following}")
        print(f"❌ Failed to unfollow: {len(failed)}/{total_following}")

        if unfollowed:
            print(f"\n✅ SUCCESSFULLY UNFOLLOWED ({len(unfollowed)}):")
            for user in unfollowed:
                print(f"   @{user['username']}")

        if failed:
            print(f"\n❌ FAILED TO UNFOLLOW ({len(failed)}):")
            for user in failed:
                print(f"   @{user['username']} - {user['error']}")

        # Save detailed results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = Path(f"data/unfollow_results_{timestamp}.json")
        results_file.parent.mkdir(parents=True, exist_ok=True)

        results = {
            'operation': 'unfollow_everyone',
            'operation_date': datetime.now().isoformat(),
            'total_following_before': total_following,
            'successfully_unfollowed': len(unfollowed),
            'failed_to_unfollow': len(failed),
            'unfollowed_users': unfollowed,
            'failed_users': failed
        }

        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Detailed results saved to: {results_file}")

        # Final verification
        print(f"\n🔍 Verifying unfollow operation...")
        try:
            verify_response = client.private_request(f"friendships/{my_user_id}/following/", params={"count": 10})
            remaining_following = len(verify_response.get('users', []))
            print(f"📊 You are now following: {remaining_following} users")

            if remaining_following == 0:
                print("🎉 SUCCESS: You are now following NO ONE!")
            else:
                print(f"ℹ️ Still following {remaining_following} users (may be due to failed unfollows)")

        except Exception as e:
            print(f"⚠️ Could not verify final count: {e}")

    except Exception as e:
        print(f"💥 Operation failed: {e}")

if __name__ == "__main__":
    unfollow_everyone()