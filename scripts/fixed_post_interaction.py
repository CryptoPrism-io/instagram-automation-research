#!/usr/bin/env python3
"""
Fixed Post Interaction - Correct API usage
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

def fixed_post_interaction():
    """Fixed API interaction with posts"""

    print("🎯 Fixed Post Interaction: @yoga_ss_")
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

        # Get posts via direct API
        print("\n📱 Getting posts...")
        try:
            params = {
                "count": 12,
                "exclude_comment": True
            }

            response = client.private_request(f"feed/user/{yoga_user_id}/", params=params)

            if 'items' in response and response['items']:
                posts = response['items']
                print(f"✅ Found {len(posts)} posts")

                # Get the first post
                first_post = posts[0]
                post_id = first_post['id']
                media_id = first_post['pk']

                print(f"\n📸 @yoga_ss_'s latest post:")
                print(f"   Post ID: {post_id}")
                print(f"   Media ID: {media_id}")

                caption = ""
                if 'caption' in first_post and first_post['caption']:
                    caption = first_post['caption'].get('text', '')

                print(f"   Caption: {caption[:100]}..." if caption else "   Caption: [No caption]")
                print(f"   Likes: {first_post.get('like_count', 0)}")
                print(f"   Comments: {first_post.get('comment_count', 0)}")

                # Method 1: Try using instagrapi's built-in methods
                print(f"\n❤️ Method 1: Using instagrapi like method...")
                try:
                    like_result = client.media_like(media_id)
                    print(f"✅ Like result: {like_result}")
                except Exception as e:
                    print(f"❌ Method 1 failed: {e}")

                # Method 2: Direct POST request
                print(f"\n❤️ Method 2: Direct POST request...")
                try:
                    # Correct way to make POST requests with instagrapi
                    like_data = {"media_id": str(media_id)}
                    like_response = client.private_request(
                        f"media/{media_id}/like/",
                        data=like_data
                    )
                    print(f"✅ Like response: {like_response.get('status', 'unknown')}")

                except Exception as e:
                    print(f"❌ Method 2 failed: {e}")

                # Comment using instagrapi method
                print(f"\n💬 Adding comment...")
                try:
                    comment_text = "Great post! 👍"
                    comment_result = client.media_comment(media_id, comment_text)
                    print(f"✅ Comment result: {comment_result}")

                except Exception as e:
                    print(f"❌ Comment failed: {e}")

                print(f"\n🎉 Interaction attempted!")
                print(f"   Target: @yoga_ss_")
                print(f"   Post: {media_id}")
                print(f"   Caption preview: {caption[:50]}...")

                # Try to get updated stats
                print(f"\n📊 Checking if interactions worked...")
                try:
                    updated_response = client.private_request(f"feed/user/{yoga_user_id}/", params={"count": 1})
                    if 'items' in updated_response and updated_response['items']:
                        updated_post = updated_response['items'][0]
                        if updated_post['pk'] == media_id:
                            print(f"   Updated likes: {updated_post.get('like_count', 0)}")
                            print(f"   Updated comments: {updated_post.get('comment_count', 0)}")
                except:
                    pass

            else:
                print("❌ No posts found")

        except Exception as e:
            print(f"❌ Failed to get posts: {e}")

    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    fixed_post_interaction()