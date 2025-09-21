#!/usr/bin/env python3
"""
Advanced Follower Extractor - Multiple methods to extract follower data
Bypasses instagrapi parsing issues with direct API access
"""

import sys
import os
from pathlib import Path
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.session_manager import InstagramSessionManager

class AdvancedFollowerExtractor:
    """Advanced follower extraction with multiple fallback methods"""

    def __init__(self):
        self.session_manager = InstagramSessionManager()
        self.client = None

    def get_client(self):
        """Get authenticated client"""
        if not self.client:
            self.client = self.session_manager.get_smart_client()
        return self.client

    def method_1_direct_requests(self, user_id, endpoint_type="followers"):
        """Method 1: Direct requests using session cookies"""
        try:
            print(f"🔧 Method 1: Direct requests for {endpoint_type}...")

            client = self.get_client()
            if not client:
                return None

            # Extract session data
            session_id = client.authorization_data.get('sessionid', '')
            user_agent = client.user_agent

            # Prepare headers
            headers = {
                'User-Agent': user_agent,
                'Cookie': f'sessionid={session_id}',
                'X-IG-App-ID': '936619743392459',
                'X-ASBD-ID': '129477',
                'X-IG-WWW-Claim': '0',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            }

            # Try Instagram web GraphQL endpoint
            if endpoint_type == "followers":
                variables = {
                    "id": str(user_id),
                    "include_reel": True,
                    "fetch_mutual": False,
                    "first": 24
                }
                query_hash = "37479f2b8209594dde7facb0d904896a"  # followers query hash
            else:
                variables = {
                    "id": str(user_id),
                    "include_reel": True,
                    "fetch_mutual": False,
                    "first": 24
                }
                query_hash = "58712303d941c6855d4e888c5f0cd22f"  # following query hash

            url = f"https://www.instagram.com/graphql/query/"
            params = {
                'variables': json.dumps(variables),
                'query_hash': query_hash
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()

                if 'data' in data and 'user' in data['data']:
                    if endpoint_type == "followers":
                        edges = data['data']['user']['edge_followed_by']['edges']
                    else:
                        edges = data['data']['user']['edge_follow']['edges']

                    users = []
                    for edge in edges:
                        node = edge['node']
                        users.append({
                            'username': node.get('username'),
                            'full_name': node.get('full_name'),
                            'user_id': node.get('id'),
                            'is_verified': node.get('is_verified', False),
                            'is_private': node.get('is_private', False),
                            'profile_pic_url': node.get('profile_pic_url')
                        })

                    print(f"✅ Method 1: Retrieved {len(users)} {endpoint_type}")
                    return users
                else:
                    print(f"❌ Method 1: No user data in response")
                    return None
            else:
                print(f"❌ Method 1: HTTP {response.status_code}")
                return None

        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
            return None

    def method_2_private_api(self, user_id, endpoint_type="followers"):
        """Method 2: Use instagrapi private API with custom parsing"""
        try:
            print(f"🔧 Method 2: Private API for {endpoint_type}...")

            client = self.get_client()
            if not client:
                return None

            # Use the internal private request method
            if endpoint_type == "followers":
                endpoint = f"friendships/{user_id}/followers/"
            else:
                endpoint = f"friendships/{user_id}/following/"

            params = {
                "count": 50,
                "rank_token": f"{client.user_id}_{client.uuid}",
                "search_surface": "follow_list_page"
            }

            # Make direct private API call
            response = client.private_request(endpoint, params=params)

            if 'users' in response:
                users = []
                for user_data in response['users']:
                    users.append({
                        'username': user_data.get('username'),
                        'full_name': user_data.get('full_name'),
                        'user_id': str(user_data.get('pk')),
                        'is_verified': user_data.get('is_verified', False),
                        'is_private': user_data.get('is_private', False),
                        'follower_count': user_data.get('follower_count', 0),
                        'profile_pic_url': user_data.get('profile_pic_url')
                    })

                print(f"✅ Method 2: Retrieved {len(users)} {endpoint_type}")
                return users
            else:
                print(f"❌ Method 2: No users in response")
                return None

        except Exception as e:
            print(f"❌ Method 2 failed: {e}")
            return None

    def extract_followers_and_following(self, username):
        """Extract followers and following using multiple methods"""

        print(f"👥 Advanced Follower Extraction: @{username}")
        print("=" * 60)

        try:
            client = self.get_client()
            if not client:
                print("❌ Could not get client")
                return None

            # Get user info
            print(f"🔍 Looking up @{username}...")
            try:
                user = client.user_info_by_username(username)
                user_id = user.pk
                print(f"✅ Found: @{user.username} (ID: {user_id})")
                print(f"   Followers: {user.follower_count}")
                print(f"   Following: {user.following_count}")
            except:
                # Fallback if username lookup fails
                if username == "yoga_ss_":
                    user_id = 143732789
                    print(f"✅ Using known ID: {user_id}")
                else:
                    print(f"❌ Could not find user ID for @{username}")
                    return None

            result = {
                'target_username': username,
                'target_user_id': str(user_id),
                'followers': [],
                'following': [],
                'extraction_methods': [],
                'extracted_at': datetime.now().isoformat()
            }

            # Try Method 1: Direct web requests for followers
            followers_method1 = self.method_1_direct_requests(user_id, "followers")
            if followers_method1:
                result['followers'] = followers_method1
                result['extraction_methods'].append('method_1_graphql_followers')
            else:
                # Try Method 2: Private API for followers
                followers_method2 = self.method_2_private_api(user_id, "followers")
                if followers_method2:
                    result['followers'] = followers_method2
                    result['extraction_methods'].append('method_2_private_api_followers')

            # Try Method 1: Direct web requests for following
            following_method1 = self.method_1_direct_requests(user_id, "following")
            if following_method1:
                result['following'] = following_method1
                result['extraction_methods'].append('method_1_graphql_following')
            else:
                # Try Method 2: Private API for following
                following_method2 = self.method_2_private_api(user_id, "following")
                if following_method2:
                    result['following'] = following_method2
                    result['extraction_methods'].append('method_2_private_api_following')

            # Display results
            if result['followers']:
                print(f"\n👥 FOLLOWERS ({len(result['followers'])}):")
                print("=" * 40)
                for i, follower in enumerate(result['followers'][:10], 1):
                    status = "✅" if follower.get('is_verified') else "🔒" if follower.get('is_private') else "👤"
                    print(f"{i:2d}. {status} @{follower['username']}")
                    print(f"    {follower['full_name']}")
                    if follower.get('follower_count'):
                        print(f"    {follower['follower_count']:,} followers")
                    print()

            if result['following']:
                print(f"\n👤 FOLLOWING ({len(result['following'])}):")
                print("=" * 40)
                for i, following in enumerate(result['following'][:10], 1):
                    status = "✅" if following.get('is_verified') else "🔒" if following.get('is_private') else "👤"
                    print(f"{i:2d}. {status} @{following['username']}")
                    print(f"    {following['full_name']}")
                    if following.get('follower_count'):
                        print(f"    {following['follower_count']:,} followers")
                    print()

            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path(f"data/advanced_follower_extract_{username}_{timestamp}.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"\n💾 Results saved to: {output_file}")
            print(f"📊 Total followers extracted: {len(result['followers'])}")
            print(f"📊 Total following extracted: {len(result['following'])}")
            print(f"🔧 Methods used: {', '.join(result['extraction_methods'])}")

            return result

        except Exception as e:
            print(f"💥 Extraction failed: {e}")
            return None

def main():
    """Main function"""
    extractor = AdvancedFollowerExtractor()
    result = extractor.extract_followers_and_following("yoga_ss_")

    if result and (result['followers'] or result['following']):
        print("\n🎉 SUCCESS! Follower extraction completed with advanced methods!")
    else:
        print("\n😞 All extraction methods failed")

if __name__ == "__main__":
    main()