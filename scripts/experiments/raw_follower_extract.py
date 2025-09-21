#!/usr/bin/env python3
"""
Raw Follower Extract - Direct API call inspection
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

def raw_follower_extraction():
    """Extract followers using raw API inspection"""

    print("🔍 Raw Follower Extraction - @yoga_ss_")
    print("=" * 50)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Could not get Instagram client")
            return

        print("✅ Session active")

        # Get yoga_ss_ user ID
        yoga_user_id = 143732789

        print(f"🎯 Target: @yoga_ss_ (ID: {yoga_user_id})")

        # Try the raw API call that we saw working in the logs
        print("\n🔧 Making direct API call for followers...")

        # Use the internal method to make the API call
        try:
            # This mirrors the successful API call we saw in logs
            url = f"https://i.instagram.com/api/v1/friendships/{yoga_user_id}/followers/"
            params = {
                "count": 20,
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            # Make the request
            response = client.private_request(url, params=params)

            if 'users' in response:
                users = response['users']
                print(f"✅ Raw API returned {len(users)} followers")

                print("\n👥 YOGA_SS_ FOLLOWERS:")
                print("=" * 40)

                for i, user in enumerate(users[:10], 1):
                    username = user.get('username', 'N/A')
                    full_name = user.get('full_name', 'N/A')
                    is_verified = user.get('is_verified', False)
                    is_private = user.get('is_private', False)
                    follower_count = user.get('follower_count', 0)

                    status = "✅" if is_verified else "🔒" if is_private else "👤"
                    print(f"{i:2d}. {status} @{username}")
                    print(f"    Name: {full_name}")
                    print(f"    Followers: {follower_count:,}")
                    print()

                # Save raw data
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = Path(f"data/yoga_raw_followers_{timestamp}.json")

                result = {
                    'target_user_id': yoga_user_id,
                    'target_username': 'yoga_ss_',
                    'followers_data': users,
                    'extracted_at': datetime.now().isoformat(),
                    'api_url': url
                }

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"💾 Raw data saved to: {output_file}")
                return users

            else:
                print("❌ No users data in API response")
                print(f"Response keys: {list(response.keys())}")

        except Exception as e:
            print(f"❌ Raw API call failed: {e}")

        # Try following as well
        print("\n🔧 Making direct API call for following...")
        try:
            url = f"https://i.instagram.com/api/v1/friendships/{yoga_user_id}/following/"
            params = {
                "count": 20,
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            response = client.private_request(url, params=params)

            if 'users' in response:
                users = response['users']
                print(f"✅ Raw API returned {len(users)} following")

                print("\n👤 YOGA_SS_ FOLLOWING:")
                print("=" * 40)

                for i, user in enumerate(users[:10], 1):
                    username = user.get('username', 'N/A')
                    full_name = user.get('full_name', 'N/A')
                    is_verified = user.get('is_verified', False)
                    is_private = user.get('is_private', False)
                    follower_count = user.get('follower_count', 0)

                    status = "✅" if is_verified else "🔒" if is_private else "👤"
                    print(f"{i:2d}. {status} @{username}")
                    print(f"    Name: {full_name}")
                    print(f"    Followers: {follower_count:,}")
                    print()

        except Exception as e:
            print(f"❌ Following API call failed: {e}")

    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    raw_follower_extraction()