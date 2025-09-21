#!/usr/bin/env python3
"""
Quick Follower Activity Check
Analyze last posts and activity for specific followers
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.session_manager import InstagramSessionManager

def get_user_last_post(client, user_id, username):
    """Get last post info for a specific user"""
    try:
        print(f"   📸 Checking @{username}'s last post...")

        params = {"count": 1, "exclude_comment": True}
        response = client.private_request(f"feed/user/{user_id}/", params=params)

        if 'items' in response and response['items']:
            last_post = response['items'][0]

            # Extract post details
            taken_at = last_post.get('taken_at', 0)
            if taken_at:
                post_date = datetime.fromtimestamp(taken_at)
                days_ago = (datetime.now() - post_date).days

                media_type_map = {1: "Photo", 2: "Video", 8: "Carousel"}
                media_type = media_type_map.get(last_post.get('media_type', 1), "Unknown")

                caption = last_post.get('caption', {})
                caption_text = caption.get('text', '') if caption else ''

                return {
                    'has_post': True,
                    'date': post_date.strftime('%Y-%m-%d %H:%M'),
                    'days_ago': days_ago,
                    'type': media_type,
                    'likes': last_post.get('like_count', 0),
                    'comments': last_post.get('comment_count', 0),
                    'caption_preview': caption_text[:50] + ('...' if len(caption_text) > 50 else '')
                }

        return {'has_post': False, 'message': 'No posts found'}

    except Exception as e:
        return {'has_post': None, 'error': str(e)}

def quick_activity_check():
    """Quick activity check for specific users"""

    print("🔍 Quick Follower Activity Check")
    print("=" * 50)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get Instagram client")
            return

        print("✅ Session active")

        # Users to check (from our previous extractions)
        target_users = [
            {"username": "yoga_ss_", "id": "143732789"},
            {"username": "saberikathak", "id": "3708395460"},
            {"username": "seeking_sagar", "id": "71644131282"},
            {"username": "finding_solitude", "id": "71469867829"},
            {"username": "kanikaachaudhary", "id": "4033185620"}
        ]

        results = []

        print(f"\n📊 Checking activity for {len(target_users)} users...")
        print("=" * 50)

        for i, user in enumerate(target_users, 1):
            username = user['username']
            user_id = user['id']

            print(f"\n{i}. @{username}")

            # Get last post info
            post_info = get_user_last_post(client, user_id, username)

            user_result = {
                'username': username,
                'user_id': user_id,
                'last_post': post_info,
                'checked_at': datetime.now().isoformat()
            }

            # Display results
            if post_info.get('has_post'):
                print(f"   ✅ Last post: {post_info['days_ago']} days ago ({post_info['date']})")
                print(f"   📱 Type: {post_info['type']}")
                print(f"   ❤️ Engagement: {post_info['likes']} likes, {post_info['comments']} comments")
                if post_info['caption_preview']:
                    print(f"   💬 Caption: {post_info['caption_preview']}")
            elif post_info.get('has_post') is False:
                print(f"   ❌ No posts found")
            else:
                print(f"   ⚠️ Error: {post_info.get('error', 'Unknown error')}")

            results.append(user_result)

        # Generate summary
        print(f"\n📈 ACTIVITY SUMMARY")
        print("=" * 30)

        active_users = [r for r in results if r['last_post'].get('has_post')]
        recent_users = [r for r in active_users if r['last_post'].get('days_ago', 999) <= 7]

        print(f"Users with posts: {len(active_users)}/{len(target_users)}")
        print(f"Posted this week: {len(recent_users)}/{len(target_users)}")

        if recent_users:
            print(f"\n🔥 MOST RECENT POSTS:")
            recent_sorted = sorted(recent_users, key=lambda x: x['last_post']['days_ago'])
            for user in recent_sorted:
                username = user['username']
                days = user['last_post']['days_ago']
                likes = user['last_post']['likes']
                print(f"   @{username}: {days} days ago ({likes} likes)")

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = Path(f"../data/quick_activity_check_{timestamp}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Results saved to: {output_file}")

    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    quick_activity_check()