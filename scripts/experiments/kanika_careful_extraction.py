#!/usr/bin/env python3
"""
Careful Extraction for @kanikaachaudhary
Using small batches to avoid 400 errors
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

def careful_follower_extraction(username):
    """Careful extraction with small batches"""

    print(f"🔍 Careful Extraction: @{username}")
    print("=" * 50)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get Instagram client")
            return None

        print("✅ Session is LIVE")

        # Get user info
        print(f"🔍 Looking up @{username}...")
        try:
            user = client.user_info_by_username(username)
            user_id = user.pk
            print(f"✅ Found: @{user.username} (ID: {user_id})")
            print(f"   Full Name: {user.full_name}")
            print(f"   Total Followers: {user.follower_count}")
            print(f"   Total Following: {user.following_count}")
            print(f"   Is Private: {user.is_private}")
        except Exception as e:
            print(f"❌ Could not find user: {e}")
            return None

        result = {
            'target_username': username,
            'target_user_id': str(user_id),
            'target_info': {
                'full_name': user.full_name,
                'total_followers': user.follower_count,
                'total_following': user.following_count,
                'is_private': user.is_private
            },
            'followers': [],
            'following': [],
            'extraction_method': 'careful_small_batches',
            'extracted_at': datetime.now().isoformat()
        }

        # Method 1: Try small batch followers
        print(f"\n👥 Extracting followers (small batches)...")
        try:
            batch_size = 50  # Start small
            max_id = ""

            for batch in range(5):  # Try up to 5 batches
                print(f"   Batch {batch + 1}: Getting {batch_size} followers...")

                params = {
                    "count": batch_size,
                    "rank_token": f"{client.user_id}_{client.uuid}",
                    "search_surface": "follow_list_page"
                }

                if max_id:
                    params["max_id"] = max_id

                follower_response = client.private_request(f"friendships/{user_id}/followers/", params=params)

                if 'users' in follower_response:
                    batch_followers = follower_response['users']
                    print(f"   ✅ Got {len(batch_followers)} followers in batch {batch + 1}")

                    for follower_data in batch_followers:
                        result['followers'].append({
                            'username': follower_data.get('username'),
                            'full_name': follower_data.get('full_name'),
                            'user_id': str(follower_data.get('pk')),
                            'is_verified': follower_data.get('is_verified', False),
                            'is_private': follower_data.get('is_private', False),
                            'follower_count': follower_data.get('follower_count', 0),
                            'profile_pic_url': follower_data.get('profile_pic_url')
                        })

                    # Check if there's more data
                    if 'next_max_id' in follower_response and follower_response['next_max_id']:
                        max_id = follower_response['next_max_id']
                        print(f"   📄 More data available, continuing...")
                        time.sleep(2)  # Be respectful
                    else:
                        print(f"   🏁 No more followers data")
                        break

                else:
                    print(f"   ⚠️ No users in batch {batch + 1}")
                    break

            print(f"✅ Followers extraction completed: {len(result['followers'])} total")

        except Exception as e:
            print(f"❌ Followers extraction failed: {e}")

        # Method 2: Try small batch following
        print(f"\n👤 Extracting following (small batches)...")
        try:
            batch_size = 50
            max_id = ""

            for batch in range(5):  # Try up to 5 batches
                print(f"   Batch {batch + 1}: Getting {batch_size} following...")

                params = {
                    "count": batch_size,
                    "rank_token": f"{client.user_id}_{client.uuid}",
                    "search_surface": "follow_list_page"
                }

                if max_id:
                    params["max_id"] = max_id

                following_response = client.private_request(f"friendships/{user_id}/following/", params=params)

                if 'users' in following_response:
                    batch_following = following_response['users']
                    print(f"   ✅ Got {len(batch_following)} following in batch {batch + 1}")

                    for following_data in batch_following:
                        result['following'].append({
                            'username': following_data.get('username'),
                            'full_name': following_data.get('full_name'),
                            'user_id': str(following_data.get('pk')),
                            'is_verified': following_data.get('is_verified', False),
                            'is_private': following_data.get('is_private', False),
                            'follower_count': following_data.get('follower_count', 0),
                            'profile_pic_url': following_data.get('profile_pic_url')
                        })

                    # Check if there's more data
                    if 'next_max_id' in following_response and following_response['next_max_id']:
                        max_id = following_response['next_max_id']
                        print(f"   📄 More data available, continuing...")
                        time.sleep(2)  # Be respectful
                    else:
                        print(f"   🏁 No more following data")
                        break

                else:
                    print(f"   ⚠️ No users in batch {batch + 1}")
                    break

            print(f"✅ Following extraction completed: {len(result['following'])} total")

        except Exception as e:
            print(f"❌ Following extraction failed: {e}")

        # Display results
        if result['followers']:
            print(f"\n👥 @{username}'S FOLLOWERS ({len(result['followers'])}):")
            print("=" * 50)
            for i, follower in enumerate(result['followers'][:15], 1):
                status = "✅" if follower.get('is_verified') else "🔒" if follower.get('is_private') else "👤"
                print(f"{i:2d}. {status} @{follower['username']}")
                print(f"    {follower['full_name']}")
                if follower.get('follower_count', 0) > 0:
                    print(f"    {follower['follower_count']:,} followers")
                print()

        if result['following']:
            print(f"\n👤 @{username}'S FOLLOWING ({len(result['following'])}):")
            print("=" * 50)
            for i, following in enumerate(result['following'][:15], 1):
                status = "✅" if following.get('is_verified') else "🔒" if following.get('is_private') else "👤"
                print(f"{i:2d}. {status} @{following['username']}")
                print(f"    {following['full_name']}")
                if following.get('follower_count', 0) > 0:
                    print(f"    {following['follower_count']:,} followers")
                print()

        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = Path(f"data/careful_extraction_{username}_{timestamp}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Results saved to: {output_file}")
        print(f"📊 EXTRACTION SUMMARY for @{username}:")
        print(f"   Account Followers: {result['target_info']['total_followers']}")
        print(f"   Extracted Followers: {len(result['followers'])}")
        print(f"   Account Following: {result['target_info']['total_following']}")
        print(f"   Extracted Following: {len(result['following'])}")

        if result['target_info']['total_followers'] > 0:
            follower_pct = len(result['followers'])/result['target_info']['total_followers']*100
            print(f"   Follower Coverage: {follower_pct:.1f}%")

        if result['target_info']['total_following'] > 0:
            following_pct = len(result['following'])/result['target_info']['total_following']*100
            print(f"   Following Coverage: {following_pct:.1f}%")

        return result

    except Exception as e:
        print(f"💥 Extraction failed: {e}")
        return None

def main():
    """Main function"""

    # Extract kanikaachaudhary's network carefully
    result = careful_follower_extraction("kanikaachaudhary")

    if result and (result['followers'] or result['following']):
        print("\n🎉 SUCCESS! Careful extraction completed!")
        print("Using the same session that worked for yoga_ss_ yesterday")
    else:
        print("\n😞 Extraction failed")

if __name__ == "__main__":
    main()