#!/usr/bin/env python3
"""
Like and Comment on @yoga_ss_'s First Picture
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

def like_and_comment_first_post():
    """Like and comment on yoga_ss_'s first/latest post"""

    print("❤️ Like & Comment on @yoga_ss_'s Post")
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

        # Get their posts
        print("\n📸 Getting @yoga_ss_'s posts...")
        try:
            posts = client.user_medias(yoga_user_id, amount=5)

            if not posts:
                print("❌ No posts found")
                return

            print(f"✅ Found {len(posts)} recent posts")

            # Get the first (most recent) post
            first_post = posts[0]
            post_id = first_post.pk

            print(f"\n📱 First post details:")
            print(f"   Post ID: {post_id}")
            print(f"   Caption: {first_post.caption_text[:100]}..." if first_post.caption_text else "   Caption: [No caption]")
            print(f"   Media type: {first_post.media_type}")
            print(f"   Likes: {first_post.like_count}")
            print(f"   Comments: {first_post.comment_count}")

            # Like the post
            print(f"\n❤️ Liking the post...")
            try:
                like_result = client.media_like(post_id)
                if like_result:
                    print("✅ Post liked successfully!")
                else:
                    print("⚠️ Like may have failed or already liked")
            except Exception as e:
                print(f"❌ Like failed: {e}")

            # Comment on the post
            print(f"\n💬 Adding comment...")

            # Thoughtful comment options
            comments = [
                "Great post! 👍",
                "Love this content! 🔥",
                "Awesome! 💯",
                "Nice one! 👌",
                "Keep it up! 🚀"
            ]

            # Use the first comment
            comment_text = comments[0]

            try:
                comment_result = client.media_comment(post_id, comment_text)
                if comment_result:
                    print(f"✅ Comment added: '{comment_text}'")
                else:
                    print("⚠️ Comment may have failed")
            except Exception as e:
                print(f"❌ Comment failed: {e}")

            print(f"\n🎉 Interaction completed!")
            print(f"   Post: {post_id}")
            print(f"   Actions: Like ❤️ + Comment 💬")

            # Get updated post stats
            try:
                updated_post = client.media_info(post_id)
                print(f"\n📊 Updated stats:")
                print(f"   Likes: {updated_post.like_count}")
                print(f"   Comments: {updated_post.comment_count}")
            except:
                pass

        except Exception as e:
            print(f"❌ Failed to get posts: {e}")

    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    like_and_comment_first_post()