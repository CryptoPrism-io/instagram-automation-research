#!/usr/bin/env python3
"""
Direct Post Interaction - Like and comment using raw API
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.session_manager import InstagramSessionManager

def direct_post_interaction():
    """Direct API interaction with posts"""

    print("🎯 Direct Post Interaction: @yoga_ss_")
    print("=" * 50)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get Instagram client")
            return

        print("✅ Session active")

        # Get yoga_ss_ user info
        yoga_user_id = 143732789
        print(f"🎯 Target: @yoga_ss_ (ID: {yoga_user_id})")

        # Method 1: Try direct API call to get user feed
        print("\n📱 Getting posts via direct API...")
        try:
            # Use private API endpoint for user feed
            params = {
                "count": 12,
                "exclude_comment": True
            }

            response = client.private_request(f"feed/user/{yoga_user_id}/", params=params)

            if 'items' in response and response['items']:
                posts = response['items']
                print(f"✅ Found {len(posts)} posts via direct API")

                # Get the first post
                first_post = posts[0]
                post_id = first_post['id']
                media_id = first_post['pk']

                print(f"\n📸 First post details:")
                print(f"   Post ID: {post_id}")
                print(f"   Media ID: {media_id}")

                caption = ""
                if 'caption' in first_post and first_post['caption']:
                    caption = first_post['caption'].get('text', '')

                print(f"   Caption: {caption[:100]}..." if caption else "   Caption: [No caption]")
                print(f"   Like count: {first_post.get('like_count', 0)}")
                print(f"   Comment count: {first_post.get('comment_count', 0)}")

                # Like the post using direct API
                print(f"\n❤️ Liking post {media_id}...")
                try:
                    like_response = client.private_request(f"media/{media_id}/like/", method="POST")

                    if like_response.get('status') == 'ok':
                        print("✅ Post liked successfully!")
                    else:
                        print(f"⚠️ Like response: {like_response}")

                except Exception as e:
                    print(f"❌ Like failed: {e}")

                # Comment on the post using direct API
                print(f"\n💬 Adding comment...")
                try:
                    comment_text = "Great post! 👍"

                    comment_data = {
                        "comment_text": comment_text,
                        "replied_to_comment_id": ""
                    }

                    comment_response = client.private_request(
                        f"media/{media_id}/comment/",
                        data=comment_data,
                        method="POST"
                    )

                    if comment_response.get('status') == 'ok':
                        print(f"✅ Comment added: '{comment_text}'")
                        if 'comment' in comment_response:
                            print(f"   Comment ID: {comment_response['comment'].get('pk')}")
                    else:
                        print(f"⚠️ Comment response: {comment_response}")

                except Exception as e:
                    print(f"❌ Comment failed: {e}")

                print(f"\n🎉 Post interaction completed!")
                print(f"   Target: @yoga_ss_")
                print(f"   Post ID: {media_id}")
                print(f"   Actions: Like ❤️ + Comment 💬")

            else:
                print("❌ No posts found in API response")
                print(f"Response keys: {list(response.keys()) if response else 'None'}")

        except Exception as e:
            print(f"❌ Direct API failed: {e}")

            # Fallback: try basic like/comment with known post
            print("\n🔄 Trying fallback approach...")

            # You can manually provide a post ID if known
            print("💡 For manual interaction:")
            print("   1. Open Instagram app")
            print("   2. Go to @yoga_ss_ profile")
            print("   3. Like and comment on the first post")
            print("   4. This ensures the interaction happens")

    except Exception as e:
        print(f"💥 Error: {e}")

def test_basic_like_functionality():
    """Test if basic like functionality works"""

    print("\n🧪 Testing Basic Like Functionality")
    print("-" * 40)

    try:
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ No client")
            return

        # Test liking our own latest post (should be safe)
        print("🔍 Testing like on your own posts...")

        try:
            # Get your own user ID
            my_user_id = client.user_id
            print(f"Your user ID: {my_user_id}")

            # Try to get your own posts
            params = {"count": 1}
            response = client.private_request(f"feed/user/{my_user_id}/", params=params)

            if 'items' in response and response['items']:
                my_post = response['items'][0]
                my_post_id = my_post['pk']
                print(f"Found your post: {my_post_id}")

                # Test like (safe to like your own post)
                like_response = client.private_request(f"media/{my_post_id}/like/", method="POST")
                print(f"Like test result: {like_response.get('status', 'unknown')}")

            else:
                print("No posts found in your feed")

        except Exception as e:
            print(f"Basic test failed: {e}")

    except Exception as e:
        print(f"Test setup failed: {e}")

if __name__ == "__main__":
    direct_post_interaction()
    test_basic_like_functionality()