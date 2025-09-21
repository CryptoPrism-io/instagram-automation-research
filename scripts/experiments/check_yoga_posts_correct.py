#!/usr/bin/env python3
"""
Correct Yoga_ss_ Post Check
Get the correct latest post date without fresh login
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

def check_yoga_posts_correctly():
    """Check yoga_ss_ posts correctly using existing session"""

    print("🔍 Correct Post Check for @yoga_ss_")
    print("=" * 50)

    try:
        # Get session manager but don't force new login
        session_manager = InstagramSessionManager()

        # Try to get existing session
        print("📱 Checking existing session...")
        client = session_manager.get_smart_client()

        if not client:
            print("❌ No active session available")
            return

        print("✅ Using existing session")

        # Check current user (should be yoga_ss_)
        try:
            account_info = client.account_info()
            print(f"🎯 Authenticated as: @{account_info.username}")

            if account_info.username != "cryptoprism.io":
                print(f"⚠️ Expected @yoga_ss_ but got @{account_info.username}")
        except Exception as e:
            print(f"⚠️ Could not get account info: {e}")

        # Get yoga_ss_ user ID (this is the target user, not necessarily the logged-in user)
        yoga_user_id = 143732789

        print(f"\n📸 Getting posts for yoga_ss_ (ID: {yoga_user_id})...")

        try:
            # Get recent posts
            params = {"count": 5, "exclude_comment": True}
            response = client.private_request(f"feed/user/{yoga_user_id}/", params=params)

            if 'items' in response and response['items']:
                posts = response['items']
                print(f"✅ Found {len(posts)} recent posts")

                print(f"\n📱 Recent Posts for @yoga_ss_:")
                print("=" * 40)

                for i, post in enumerate(posts, 1):
                    taken_at = post.get('taken_at', 0)
                    if taken_at:
                        post_date = datetime.fromtimestamp(taken_at)
                        days_ago = (datetime.now() - post_date).days

                        media_type_map = {1: "Photo", 2: "Video", 8: "Carousel"}
                        media_type = media_type_map.get(post.get('media_type', 1), "Unknown")

                        likes = post.get('like_count', 0)
                        comments = post.get('comment_count', 0)

                        caption = post.get('caption', {})
                        caption_text = caption.get('text', '') if caption else ''
                        caption_preview = caption_text[:100] + ('...' if len(caption_text) > 100 else '')

                        print(f"{i}. {media_type} - {post_date.strftime('%Y-%m-%d %H:%M')}")
                        print(f"   📅 {days_ago} days ago")
                        print(f"   ❤️ {likes} likes, 💬 {comments} comments")
                        if caption_preview:
                            print(f"   💭 {caption_preview}")
                        print()

                # Save corrected data
                latest_post = posts[0]
                taken_at = latest_post.get('taken_at', 0)
                latest_date = datetime.fromtimestamp(taken_at) if taken_at else None
                days_ago = (datetime.now() - latest_date).days if latest_date else None

                result = {
                    'username': 'yoga_ss_',
                    'user_id': str(yoga_user_id),
                    'latest_post': {
                        'date': latest_date.isoformat() if latest_date else None,
                        'days_ago': days_ago,
                        'likes': latest_post.get('like_count', 0),
                        'comments': latest_post.get('comment_count', 0),
                        'type': media_type_map.get(latest_post.get('media_type', 1), "Unknown")
                    },
                    'total_recent_posts': len(posts),
                    'checked_at': datetime.now().isoformat()
                }

                # Save corrected data
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = Path(f"../data/yoga_posts_corrected_{timestamp}.json")
                output_file.parent.mkdir(parents=True, exist_ok=True)

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"💾 Corrected data saved to: {output_file}")

                # Summary
                print(f"🎯 CORRECTED SUMMARY for @yoga_ss_:")
                print(f"   Latest post: {days_ago} days ago ({latest_date.strftime('%Y-%m-%d')})")
                print(f"   Engagement: {latest_post.get('like_count', 0)} likes, {latest_post.get('comment_count', 0)} comments")

            else:
                print("❌ No posts found in response")
                print(f"Response keys: {list(response.keys()) if response else 'None'}")

        except Exception as e:
            print(f"❌ Failed to get posts: {e}")

            # If we can't get posts, maybe we're rate limited or the session expired
            if "wait a few minutes" in str(e).lower():
                print("⏳ Rate limited - API is working but we need to slow down")
            elif "login" in str(e).lower():
                print("🔐 Session may have expired")

    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    check_yoga_posts_correctly()