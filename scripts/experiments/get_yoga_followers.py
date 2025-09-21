#!/usr/bin/env python3
"""
Get yoga_ss_ Followers - Extract actual follower data
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

def get_yoga_followers_and_following():
    """Get followers and following for yoga_ss_"""

    print("👥 @yoga_ss_ Followers & Following Extraction")
    print("=" * 60)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get Instagram client")
            return

        print("✅ Session active")

        # Get yoga_ss_ user info
        print("🔍 Looking up @yoga_ss_...")
        yoga_user = client.user_info_by_username("yoga_ss_")
        print(f"✅ Found: @{yoga_user.username}")
        print(f"   User ID: {yoga_user.pk}")
        print(f"   Full Name: {yoga_user.full_name}")
        print(f"   Followers: {yoga_user.follower_count}")
        print(f"   Following: {yoga_user.following_count}")

        result = {
            'target_user': {
                'username': yoga_user.username,
                'user_id': str(yoga_user.pk),
                'full_name': yoga_user.full_name,
                'follower_count': yoga_user.follower_count,
                'following_count': yoga_user.following_count,
                'is_private': yoga_user.is_private
            },
            'followers': [],
            'following': [],
            'extracted_at': datetime.now().isoformat()
        }

        # Get followers
        print(f"\n👥 Getting followers (showing first 20 of {yoga_user.follower_count})...")
        try:
            followers = client.user_followers(yoga_user.pk, amount=20)
            print(f"✅ Retrieved {len(followers)} followers:")

            for i, follower in enumerate(followers, 1):
                follower_data = {
                    'rank': i,
                    'username': follower.username,
                    'user_id': str(follower.pk),
                    'full_name': follower.full_name,
                    'is_verified': getattr(follower, 'is_verified', False),
                    'is_private': getattr(follower, 'is_private', False),
                    'follower_count': getattr(follower, 'follower_count', 0)
                }
                result['followers'].append(follower_data)

                status = "✅" if follower_data['is_verified'] else "🔒" if follower_data['is_private'] else "👤"
                print(f"   {i:2d}. {status} @{follower.username} ({follower.full_name})")

        except Exception as e:
            print(f"❌ Followers access failed: {e}")

        # Get following
        print(f"\n👤 Getting following (showing first 20 of {yoga_user.following_count})...")
        try:
            following = client.user_following(yoga_user.pk, amount=20)
            print(f"✅ Retrieved {len(following)} following:")

            for i, follow in enumerate(following, 1):
                following_data = {
                    'rank': i,
                    'username': follow.username,
                    'user_id': str(follow.pk),
                    'full_name': follow.full_name,
                    'is_verified': getattr(follow, 'is_verified', False),
                    'is_private': getattr(follow, 'is_private', False),
                    'follower_count': getattr(follow, 'follower_count', 0)
                }
                result['following'].append(following_data)

                status = "✅" if following_data['is_verified'] else "🔒" if following_data['is_private'] else "👤"
                print(f"   {i:2d}. {status} @{follow.username} ({follow.full_name})")

        except Exception as e:
            print(f"❌ Following access failed: {e}")

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = Path(f"data/yoga_followers_following_{timestamp}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Data saved to: {output_file}")

        # Summary
        print(f"\n📊 SUMMARY - @yoga_ss_:")
        print(f"   Followers retrieved: {len(result['followers'])}")
        print(f"   Following retrieved: {len(result['following'])}")
        print(f"   Total followers: {yoga_user.follower_count}")
        print(f"   Total following: {yoga_user.following_count}")

        return result

    except Exception as e:
        print(f"💥 Error: {e}")
        return None

if __name__ == "__main__":
    get_yoga_followers_and_following()