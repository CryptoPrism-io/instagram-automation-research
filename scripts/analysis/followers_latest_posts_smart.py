#!/usr/bin/env python3
"""
Smart Follower Latest Posts Check
Gets top 6 posts for each follower and finds the actual latest post date
(Handles pinned posts correctly)
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

def get_actual_latest_post(client, user_id, username):
    """Get the actual latest post date by checking top 6 posts (handles pinned posts)"""
    try:
        print(f"    📸 Getting top 6 posts to find latest...")

        # Get top 6 posts to handle pinned posts
        params = {"count": 6, "exclude_comment": True}
        response = client.private_request(f"feed/user/{user_id}/", params=params)

        if 'items' in response and response['items']:
            posts = response['items']
            print(f"    ✅ Found {len(posts)} posts")

            # Extract all post dates and find the latest
            post_dates = []
            for post in posts:
                taken_at = post.get('taken_at', 0)
                if taken_at:
                    post_date = datetime.fromtimestamp(taken_at)
                    post_dates.append({
                        'date': post_date,
                        'timestamp': taken_at,
                        'likes': post.get('like_count', 0),
                        'comments': post.get('comment_count', 0)
                    })

            if post_dates:
                # Sort by date (newest first) to get actual latest
                post_dates.sort(key=lambda x: x['timestamp'], reverse=True)
                latest_post = post_dates[0]

                days_ago = (datetime.now() - latest_post['date']).days

                # Time description
                if days_ago == 0:
                    time_desc = "Today"
                elif days_ago == 1:
                    time_desc = "Yesterday"
                elif days_ago <= 7:
                    time_desc = f"{days_ago} days ago"
                else:
                    time_desc = f"{days_ago} days ago"

                return {
                    'success': True,
                    'latest_date': latest_post['date'],
                    'days_ago': days_ago,
                    'time_description': time_desc,
                    'likes': latest_post['likes'],
                    'comments': latest_post['comments'],
                    'total_posts_checked': len(posts),
                    'total_posts_with_dates': len(post_dates)
                }
            else:
                return {'success': False, 'error': 'No posts with valid dates'}
        else:
            return {'success': False, 'error': 'No posts found'}

    except Exception as e:
        return {'success': False, 'error': str(e)}

def check_followers_smart():
    """Smart check of followers' latest posts (handles pinned posts)"""

    print("👥 Smart Followers' Latest Posts Check")
    print("Gets top 6 posts per follower to handle pinned posts correctly")
    print("=" * 70)

    try:
        # Get session from root directory
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
            print("ℹ️ Session working without account verification")

        # Get your followers (top 10)
        print(f"\n👥 Getting your top 10 followers...")
        try:
            params = {
                "count": 10,
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            response = client.private_request(f"friendships/{my_user_id}/followers/", params=params)

            if 'users' not in response:
                print("❌ No followers data")
                return

            followers = response['users']
            print(f"✅ Found {len(followers)} followers to analyze")

        except Exception as e:
            print(f"❌ Failed to get followers: {e}")
            return

        # Analyze each follower's actual latest post
        results = []

        print(f"\n🔍 Smart analysis of latest posts (checking 6 posts each)...")
        print("=" * 70)

        for i, follower in enumerate(followers, 1):
            username = follower.get('username')
            user_id = follower.get('pk')
            full_name = follower.get('full_name', '')
            is_private = follower.get('is_private', False)
            is_verified = follower.get('is_verified', False)

            print(f"\n{i:2d}. @{username}")
            if full_name:
                print(f"    {full_name}")

            follower_data = {
                'rank': i,
                'username': username,
                'user_id': str(user_id),
                'full_name': full_name,
                'is_private': is_private,
                'is_verified': is_verified
            }

            if is_private:
                print(f"    🔒 Private account - skipping")
                follower_data['latest_post'] = 'Private account'
            else:
                # Get actual latest post (handling pinned posts)
                latest_result = get_actual_latest_post(client, user_id, username)

                if latest_result['success']:
                    latest_date = latest_result['latest_date']
                    time_desc = latest_result['time_description']
                    likes = latest_result['likes']
                    comments = latest_result['comments']

                    print(f"    ✅ Latest post: {time_desc}")
                    print(f"    📅 Date: {latest_date.strftime('%Y-%m-%d %H:%M')}")
                    print(f"    💙 {likes} likes, 💬 {comments} comments")
                    print(f"    📊 Checked {latest_result['total_posts_checked']} posts")

                    follower_data['latest_post'] = {
                        'date': latest_date.strftime('%Y-%m-%d %H:%M'),
                        'days_ago': latest_result['days_ago'],
                        'time_description': time_desc,
                        'likes': likes,
                        'comments': comments,
                        'posts_checked': latest_result['total_posts_checked']
                    }
                else:
                    error = latest_result['error']
                    print(f"    ❌ {error}")
                    follower_data['latest_post'] = f'Error: {error}'

            results.append(follower_data)

            # Be respectful with API calls
            if i < len(followers):
                time.sleep(1.5)

        # Generate smart summary
        print(f"\n📊 SMART SUMMARY: Your Followers' Latest Posts")
        print("=" * 60)

        active_followers = [r for r in results if isinstance(r['latest_post'], dict)]

        if active_followers:
            # Sort by most recent
            active_followers.sort(key=lambda x: x['latest_post']['days_ago'])

            print(f"📱 Active Followers ({len(active_followers)}):")
            for follower in active_followers:
                username = follower['username']
                time_desc = follower['latest_post']['time_description']
                likes = follower['latest_post']['likes']
                verified = "✅" if follower.get('is_verified') else ""

                print(f"   {verified} @{username} - {time_desc} ({likes} likes)")

        # Activity breakdown
        private_count = len([r for r in results if r['latest_post'] == 'Private account'])
        error_count = len([r for r in results if isinstance(r['latest_post'], str) and 'Error:' in r['latest_post']])

        recent_this_week = len([r for r in active_followers if r['latest_post']['days_ago'] <= 7])
        recent_this_month = len([r for r in active_followers if r['latest_post']['days_ago'] <= 30])

        print(f"\n📈 Activity Breakdown:")
        print(f"   Total followers: {len(results)}")
        print(f"   With latest posts: {len(active_followers)}")
        print(f"   Posted this week: {recent_this_week}")
        print(f"   Posted this month: {recent_this_month}")
        print(f"   Private accounts: {private_count}")
        print(f"   Errors/No posts: {error_count}")

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = Path(f"data/smart_followers_latest_{timestamp}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'analysis_type': 'smart_latest_posts',
                'description': 'Handles pinned posts by checking top 6 posts per user',
                'analysis_date': datetime.now().isoformat(),
                'total_followers_checked': len(results),
                'method': 'top_6_posts_check',
                'followers': results
            }, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Smart analysis saved to: {output_file}")
        print(f"🧠 Method: Checked top 6 posts per user to handle pinned posts")

    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    check_followers_smart()