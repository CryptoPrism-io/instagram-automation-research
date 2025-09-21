#!/usr/bin/env python3
"""
Full Follower Extraction for @kanikaachaudhary
Using the same successful method from yoga_ss_ extraction
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

def extract_all_followers_following(username, max_amount=500):
    """Extract all followers and following for a user"""

    print(f"👥 FULL Extraction: @{username}")
    print("=" * 60)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get Instagram client")
            return None

        print("✅ Session active")

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
                'is_private': user.is_private,
                'is_verified': getattr(user, 'is_verified', False)
            },
            'followers': [],
            'following': [],
            'extraction_stats': {},
            'extracted_at': datetime.now().isoformat()
        }

        # Extract ALL followers
        print(f"\n👥 Extracting ALL followers (target: {user.follower_count})...")
        try:
            # Use the same method that worked for yoga_ss_
            params = {
                "count": max_amount,
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            # Get followers via private API
            follower_response = client.private_request(f"friendships/{user_id}/followers/", params=params)

            if 'users' in follower_response:
                followers_raw = follower_response['users']
                print(f"✅ Retrieved {len(followers_raw)} followers")

                for follower_data in followers_raw:
                    result['followers'].append({
                        'username': follower_data.get('username'),
                        'full_name': follower_data.get('full_name'),
                        'user_id': str(follower_data.get('pk')),
                        'is_verified': follower_data.get('is_verified', False),
                        'is_private': follower_data.get('is_private', False),
                        'follower_count': follower_data.get('follower_count', 0),
                        'profile_pic_url': follower_data.get('profile_pic_url'),
                        'is_business': follower_data.get('is_business', False),
                        'category': follower_data.get('category')
                    })

                result['extraction_stats']['followers_extracted'] = len(result['followers'])
                result['extraction_stats']['followers_method'] = 'private_api_success'

            else:
                print("❌ No followers data in response")
                result['extraction_stats']['followers_method'] = 'failed'

        except Exception as e:
            print(f"❌ Followers extraction failed: {e}")
            result['extraction_stats']['followers_method'] = f'failed: {str(e)}'

        # Extract ALL following
        print(f"\n👤 Extracting ALL following (target: {user.following_count})...")
        try:
            params = {
                "count": max_amount,
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            # Get following via private API
            following_response = client.private_request(f"friendships/{user_id}/following/", params=params)

            if 'users' in following_response:
                following_raw = following_response['users']
                print(f"✅ Retrieved {len(following_raw)} following")

                for following_data in following_raw:
                    result['following'].append({
                        'username': following_data.get('username'),
                        'full_name': following_data.get('full_name'),
                        'user_id': str(following_data.get('pk')),
                        'is_verified': following_data.get('is_verified', False),
                        'is_private': following_data.get('is_private', False),
                        'follower_count': following_data.get('follower_count', 0),
                        'profile_pic_url': following_data.get('profile_pic_url'),
                        'is_business': following_data.get('is_business', False),
                        'category': following_data.get('category')
                    })

                result['extraction_stats']['following_extracted'] = len(result['following'])
                result['extraction_stats']['following_method'] = 'private_api_success'

            else:
                print("❌ No following data in response")
                result['extraction_stats']['following_method'] = 'failed'

        except Exception as e:
            print(f"❌ Following extraction failed: {e}")
            result['extraction_stats']['following_method'] = f'failed: {str(e)}'

        # Display top results
        if result['followers']:
            print(f"\n👥 TOP FOLLOWERS ({len(result['followers'])}):")
            print("=" * 50)
            for i, follower in enumerate(result['followers'][:10], 1):
                status = "✅" if follower.get('is_verified') else "🔒" if follower.get('is_private') else "👤"
                biz = "🏢" if follower.get('is_business') else ""
                print(f"{i:2d}. {status}{biz} @{follower['username']}")
                print(f"    {follower['full_name']}")
                if follower.get('follower_count', 0) > 0:
                    print(f"    {follower['follower_count']:,} followers")
                print()

        if result['following']:
            print(f"\n👤 TOP FOLLOWING ({len(result['following'])}):")
            print("=" * 50)
            for i, following in enumerate(result['following'][:10], 1):
                status = "✅" if following.get('is_verified') else "🔒" if following.get('is_private') else "👤"
                biz = "🏢" if following.get('is_business') else ""
                print(f"{i:2d}. {status}{biz} @{following['username']}")
                print(f"    {following['full_name']}")
                if following.get('follower_count', 0) > 0:
                    print(f"    {following['follower_count']:,} followers")
                print()

        # Save comprehensive results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = Path(f"data/full_extraction_{username}_{timestamp}.json")
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Complete data saved to: {output_file}")
        print(f"📊 EXTRACTION SUMMARY:")
        print(f"   Total Followers: {result['target_info']['total_followers']}")
        print(f"   Followers Extracted: {len(result['followers'])}")
        print(f"   Total Following: {result['target_info']['total_following']}")
        print(f"   Following Extracted: {len(result['following'])}")
        print(f"   Coverage: {len(result['followers'])/result['target_info']['total_followers']*100:.1f}% followers, {len(result['following'])/result['target_info']['total_following']*100:.1f}% following")

        return result

    except Exception as e:
        print(f"💥 Extraction failed: {e}")
        return None

def main():
    """Main function"""

    # Test session first
    print("🔐 Testing session status...")
    session_manager = InstagramSessionManager()
    client = session_manager.get_smart_client()

    if not client:
        print("❌ Session not active")
        return

    try:
        account = client.account_info()
        print(f"✅ Session LIVE - Logged in as: @{account.username}")
    except:
        print("❌ Session validation failed")
        return

    # Extract kanikaachaudhary's complete network
    result = extract_all_followers_following("kanikaachaudhary", max_amount=1000)

    if result and (result['followers'] or result['following']):
        print("\n🎉 SUCCESS! Full network extraction completed!")
    else:
        print("\n😞 Extraction failed")

if __name__ == "__main__":
    main()