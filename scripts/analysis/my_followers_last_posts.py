#!/usr/bin/env python3
"""
Simple Follower Last Post Check
Get your followers and check when they posted last
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

def check_my_followers_last_posts():
    """Get your followers and check when they last posted"""

    print("👥 Your Followers' Last Posts")
    print("Getting your followers and checking when they posted last")
    print("=" * 60)

    try:
        # Get session - should be logged in as cryptoprism.io
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ No session available - need to login first")
            return

        # Get your user ID (the logged-in account)
        my_user_id = client.user_id
        print(f"✅ Logged in as user ID: {my_user_id}")

        # Try to get account info
        try:
            account = client.account_info()
            print(f"✅ Account: @{account.username}")
        except:
            print("ℹ️ Using session without account verification")

        # Get YOUR followers (top 10)
        print(f"\n👥 Getting your followers...")
        try:
            params = {
                "count": 10,  # Just get 10 followers
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            response = client.private_request(f"friendships/{my_user_id}/followers/", params=params)

            if 'users' not in response:
                print("❌ No followers data received")
                return

            followers = response['users']
            print(f"✅ Found {len(followers)} followers")

        except Exception as e:
            print(f"❌ Failed to get followers: {e}")
            return

        # Check each follower's last post
        results = []

        print(f"\n🔍 Checking when each follower posted last...")
        print("=" * 60)

        for i, follower in enumerate(followers, 1):
            username = follower.get('username')
            user_id = follower.get('pk')
            full_name = follower.get('full_name', '')
            is_private = follower.get('is_private', False)

            print(f"\n{i:2d}. @{username}")
            if full_name:
                print(f"    {full_name}")

            if is_private:
                print(f"    🔒 Private account - can't check posts")
                results.append({
                    'username': username,
                    'user_id': str(user_id),
                    'full_name': full_name,
                    'is_private': True,
                    'last_post': 'Private account'
                })
                continue

            # Get their most recent post
            try:
                print(f"    📸 Checking most recent post...")

                params = {"count": 1, "exclude_comment": True}
                post_response = client.private_request(f"feed/user/{user_id}/", params=params)

                if 'items' in post_response and post_response['items']:
                    latest_post = post_response['items'][0]

                    # Get when it was posted
                    taken_at = latest_post.get('taken_at', 0)
                    if taken_at:
                        post_date = datetime.fromtimestamp(taken_at)
                        days_ago = (datetime.now() - post_date).days

                        # Simple time description
                        if days_ago == 0:
                            time_desc = "Today"
                        elif days_ago == 1:
                            time_desc = "Yesterday"
                        elif days_ago <= 7:
                            time_desc = f"{days_ago} days ago"
                        elif days_ago <= 30:
                            time_desc = f"{days_ago} days ago"
                        else:
                            time_desc = f"{days_ago} days ago"

                        print(f"    ✅ Last posted: {time_desc} ({post_date.strftime('%Y-%m-%d')})")

                        results.append({
                            'username': username,
                            'user_id': str(user_id),
                            'full_name': full_name,
                            'is_private': False,
                            'last_post': {
                                'date': post_date.strftime('%Y-%m-%d %H:%M'),
                                'days_ago': days_ago,
                                'time_description': time_desc
                            }
                        })

                    else:
                        print(f"    ❌ Post found but no timestamp")
                        results.append({
                            'username': username,
                            'user_id': str(user_id),
                            'full_name': full_name,
                            'is_private': False,
                            'last_post': 'No timestamp available'
                        })

                else:
                    print(f"    ❌ No posts found")
                    results.append({
                        'username': username,
                        'user_id': str(user_id),
                        'full_name': full_name,
                        'is_private': False,
                        'last_post': 'No posts found'
                    })

            except Exception as e:
                error_msg = str(e)
                if "wait a few minutes" in error_msg:
                    print(f"    ⏳ Rate limited - slowing down")
                    time.sleep(3)
                else:
                    print(f"    ⚠️ Error: {error_msg}")

                results.append({
                    'username': username,
                    'user_id': str(user_id),
                    'full_name': full_name,
                    'is_private': False,
                    'last_post': f'Error: {error_msg}'
                })

            # Be nice to Instagram
            time.sleep(1)

        # Summary report
        print(f"\n📊 SUMMARY: When Your Followers Posted Last")
        print("=" * 60)

        active_followers = [r for r in results if isinstance(r['last_post'], dict)]

        if active_followers:
            # Sort by most recent
            active_followers.sort(key=lambda x: x['last_post']['days_ago'])

            print(f"📱 Active Followers ({len(active_followers)}):")
            for follower in active_followers:
                username = follower['username']
                time_desc = follower['last_post']['time_description']
                print(f"   @{username} - {time_desc}")

        private_count = len([r for r in results if r.get('is_private')])
        no_posts_count = len([r for r in results if r['last_post'] == 'No posts found'])

        print(f"\n📊 Overview:")
        print(f"   Total followers checked: {len(results)}")
        print(f"   With recent posts: {len(active_followers)}")
        print(f"   Private accounts: {private_count}")
        print(f"   No posts found: {no_posts_count}")

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = Path(f"../data/my_followers_last_posts_{timestamp}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_date': datetime.now().isoformat(),
                'total_followers_checked': len(results),
                'followers': results
            }, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Detailed results saved to: {output_file}")

    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    check_my_followers_last_posts()