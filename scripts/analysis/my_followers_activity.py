#!/usr/bin/env python3
"""
Analyze Your Own Followers' Activity
Check last posts and activity for your followers
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

def analyze_my_followers_activity():
    """Analyze activity for your own followers"""

    print("👥 Your Followers' Activity Analysis")
    print("=" * 50)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get Instagram client")
            return

        print("✅ Session active")

        # Get your own user info
        my_user_id = client.user_id
        print(f"🎯 Analyzing followers for your account (ID: {my_user_id})")

        # Get your followers
        print(f"\n👥 Getting your followers...")
        try:
            params = {
                "count": 20,  # Start with smaller number to avoid rate limits
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            follower_response = client.private_request(f"friendships/{my_user_id}/followers/", params=params)

            if 'users' not in follower_response:
                print("❌ No followers data received")
                return

            followers = follower_response['users']
            print(f"✅ Got {len(followers)} followers for analysis")

        except Exception as e:
            print(f"❌ Failed to get followers: {e}")
            return

        # Analyze each follower's last post
        results = []

        print(f"\n🔍 Analyzing last posts for {len(followers)} followers...")
        print("=" * 60)

        for i, follower in enumerate(followers, 1):
            follower_username = follower.get('username')
            follower_id = follower.get('pk')
            is_private = follower.get('is_private', False)
            is_verified = follower.get('is_verified', False)

            print(f"\n{i:2d}. @{follower_username}", end="")
            if is_verified:
                print(" ✅", end="")
            if is_private:
                print(" 🔒", end="")
            print()

            follower_data = {
                'username': follower_username,
                'user_id': str(follower_id),
                'full_name': follower.get('full_name', ''),
                'is_private': is_private,
                'is_verified': is_verified,
                'follower_count': follower.get('follower_count', 0),
                'last_post': None
            }

            if is_private:
                print(f"   🔒 Private account - skipping post analysis")
                follower_data['last_post'] = {'error': 'Private account'}
            else:
                try:
                    print(f"   📸 Checking last post...")

                    params = {"count": 1, "exclude_comment": True}
                    post_response = client.private_request(f"feed/user/{follower_id}/", params=params)

                    if 'items' in post_response and post_response['items']:
                        last_post = post_response['items'][0]

                        # Extract post details
                        taken_at = last_post.get('taken_at', 0)
                        if taken_at:
                            post_date = datetime.fromtimestamp(taken_at)
                            days_ago = (datetime.now() - post_date).days

                            media_type_map = {1: "Photo", 2: "Video", 8: "Carousel"}
                            media_type = media_type_map.get(last_post.get('media_type', 1), "Unknown")

                            caption = last_post.get('caption', {})
                            caption_text = caption.get('text', '') if caption else ''

                            post_info = {
                                'has_post': True,
                                'date': post_date.strftime('%Y-%m-%d'),
                                'days_ago': days_ago,
                                'type': media_type,
                                'likes': last_post.get('like_count', 0),
                                'comments': last_post.get('comment_count', 0),
                                'caption_preview': caption_text[:50] + ('...' if len(caption_text) > 50 else '')
                            }

                            follower_data['last_post'] = post_info

                            # Display summary
                            if days_ago == 0:
                                print(f"   ✅ Posted today! ({post_info['likes']} likes)")
                            elif days_ago <= 7:
                                print(f"   ✅ Posted {days_ago} days ago ({post_info['likes']} likes)")
                            elif days_ago <= 30:
                                print(f"   📅 Posted {days_ago} days ago")
                            else:
                                print(f"   😴 Inactive - {days_ago} days ago")

                    else:
                        print(f"   ❌ No posts found")
                        follower_data['last_post'] = {'has_post': False, 'message': 'No posts found'}

                except Exception as e:
                    error_msg = str(e)
                    if "wait a few minutes" in error_msg:
                        print(f"   ⏳ Rate limited - slowing down")
                        time.sleep(3)
                    else:
                        print(f"   ⚠️ Error: {error_msg}")

                    follower_data['last_post'] = {'error': error_msg}

            results.append(follower_data)

            # Be respectful with API calls
            if i < len(followers):
                time.sleep(1)

        # Generate summary report
        print(f"\n📊 ACTIVITY SUMMARY FOR YOUR FOLLOWERS")
        print("=" * 50)

        total = len(results)
        private_accounts = len([r for r in results if r['is_private']])
        public_accounts = total - private_accounts

        # Post activity analysis
        with_posts = [r for r in results if r['last_post'] and r['last_post'].get('has_post')]
        recent_posts = [r for r in with_posts if r['last_post'].get('days_ago', 999) <= 7]
        this_month = [r for r in with_posts if r['last_post'].get('days_ago', 999) <= 30]
        inactive = [r for r in with_posts if r['last_post'].get('days_ago', 999) > 90]

        print(f"📊 Account Types:")
        print(f"   Public accounts: {public_accounts}/{total} ({public_accounts/total*100:.1f}%)")
        print(f"   Private accounts: {private_accounts}/{total} ({private_accounts/total*100:.1f}%)")

        print(f"\n📸 Post Activity (Public accounts only):")
        print(f"   Have posts: {len(with_posts)}/{public_accounts}")
        print(f"   Posted this week: {len(recent_posts)}/{public_accounts} ({len(recent_posts)/public_accounts*100:.1f}%)")
        print(f"   Posted this month: {len(this_month)}/{public_accounts} ({len(this_month)/public_accounts*100:.1f}%)")
        print(f"   Inactive (90+ days): {len(inactive)}/{public_accounts}")

        # Most active followers
        if recent_posts:
            print(f"\n🔥 MOST ACTIVE FOLLOWERS (This Week):")
            recent_sorted = sorted(recent_posts, key=lambda x: x['last_post']['days_ago'])
            for follower in recent_sorted[:5]:
                username = follower['username']
                days = follower['last_post']['days_ago']
                likes = follower['last_post']['likes']
                verified = "✅" if follower['is_verified'] else ""

                if days == 0:
                    time_desc = "today"
                else:
                    time_desc = f"{days} days ago"

                print(f"   {verified} @{username} - {time_desc} ({likes} likes)")

        # Save detailed results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = Path(f"../data/my_followers_activity_{timestamp}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        summary_data = {
            'analysis_date': datetime.now().isoformat(),
            'total_followers_analyzed': total,
            'public_accounts': public_accounts,
            'private_accounts': private_accounts,
            'activity_summary': {
                'with_posts': len(with_posts),
                'posted_this_week': len(recent_posts),
                'posted_this_month': len(this_month),
                'inactive_90_plus_days': len(inactive)
            },
            'followers': results
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Detailed results saved to: {output_file}")
        print(f"\n🎉 Analysis completed for {total} followers!")

    except Exception as e:
        print(f"💥 Analysis failed: {e}")

if __name__ == "__main__":
    analyze_my_followers_activity()