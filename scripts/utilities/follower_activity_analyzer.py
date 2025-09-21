#!/usr/bin/env python3
"""
Follower Activity Analyzer
Analyze followers' last posts, stories, and activity timestamps
"""

import sys
import os
from pathlib import Path
import json
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.session_manager import InstagramSessionManager

class FollowerActivityAnalyzer:
    """Analyze follower activity patterns"""

    def __init__(self):
        self.session_manager = InstagramSessionManager()
        self.client = None

    def get_client(self):
        """Get authenticated client"""
        if not self.client:
            self.client = self.session_manager.get_smart_client()
        return self.client

    def get_last_post_info(self, user_id):
        """Get last post information for a user"""
        try:
            # Get user's recent posts
            params = {"count": 1, "exclude_comment": True}
            response = self.client.private_request(f"feed/user/{user_id}/", params=params)

            if 'items' in response and response['items']:
                last_post = response['items'][0]

                # Extract post timestamp
                taken_at = last_post.get('taken_at', 0)
                if taken_at:
                    post_date = datetime.fromtimestamp(taken_at)
                    days_ago = (datetime.now() - post_date).days
                else:
                    post_date = None
                    days_ago = None

                return {
                    'has_posts': True,
                    'last_post_id': last_post.get('pk'),
                    'last_post_date': post_date.isoformat() if post_date else None,
                    'days_since_last_post': days_ago,
                    'last_post_type': last_post.get('media_type', 1),  # 1=photo, 2=video, 8=carousel
                    'like_count': last_post.get('like_count', 0),
                    'comment_count': last_post.get('comment_count', 0),
                    'caption_preview': (last_post.get('caption', {}).get('text', '') or '')[:100]
                }
            else:
                return {
                    'has_posts': False,
                    'last_post_id': None,
                    'last_post_date': None,
                    'days_since_last_post': None,
                    'last_post_type': None,
                    'like_count': 0,
                    'comment_count': 0,
                    'caption_preview': ''
                }

        except Exception as e:
            return {
                'has_posts': None,
                'error': str(e),
                'last_post_date': None,
                'days_since_last_post': None
            }

    def get_story_activity(self, user_id):
        """Check if user has active stories"""
        try:
            # Get user's story highlights and recent stories
            story_response = self.client.private_request(f"feed/user/{user_id}/story/")

            if 'reel' in story_response and story_response['reel']:
                reel = story_response['reel']
                if 'items' in reel and reel['items']:
                    # Get most recent story
                    latest_story = reel['items'][0]
                    story_timestamp = latest_story.get('taken_at', 0)

                    if story_timestamp:
                        story_date = datetime.fromtimestamp(story_timestamp)
                        hours_ago = (datetime.now() - story_date).total_seconds() / 3600

                        return {
                            'has_active_stories': hours_ago < 24,  # Stories expire after 24h
                            'story_count': len(reel['items']),
                            'latest_story_date': story_date.isoformat(),
                            'hours_since_story': round(hours_ago, 1)
                        }

            return {
                'has_active_stories': False,
                'story_count': 0,
                'latest_story_date': None,
                'hours_since_story': None
            }

        except Exception as e:
            return {
                'has_active_stories': None,
                'error': str(e),
                'story_count': 0
            }

    def get_user_activity_status(self, user_id):
        """Get user's last seen/activity status"""
        try:
            # Get user info which sometimes includes activity status
            user_response = self.client.private_request(f"users/{user_id}/info/")

            if 'user' in user_response:
                user_data = user_response['user']

                # Check for activity indicators
                is_active = user_data.get('is_active', False)
                last_seen = user_data.get('last_seen_at', 0)

                activity_info = {
                    'is_currently_active': is_active
                }

                if last_seen:
                    last_seen_date = datetime.fromtimestamp(last_seen)
                    hours_since_active = (datetime.now() - last_seen_date).total_seconds() / 3600

                    activity_info.update({
                        'last_seen_date': last_seen_date.isoformat(),
                        'hours_since_active': round(hours_since_active, 1)
                    })

                return activity_info

            return {'is_currently_active': None, 'last_seen_date': None}

        except Exception as e:
            return {'error': str(e), 'is_currently_active': None}

    def analyze_followers_activity(self, username, max_followers=50):
        """Analyze activity for a user's followers"""

        print(f"👥 Follower Activity Analysis: @{username}")
        print("=" * 60)

        try:
            client = self.get_client()
            if not client:
                print("❌ Could not get Instagram client")
                return None

            print("✅ Session active")

            # Get target user info
            print(f"🔍 Looking up @{username}...")
            try:
                user = client.user_info_by_username(username)
                user_id = user.pk
                print(f"✅ Found: @{user.username} (ID: {user_id})")
                print(f"   Total Followers: {user.follower_count}")
            except Exception as e:
                print(f"❌ Could not find user: {e}")
                return None

            # Get followers list
            print(f"\n👥 Getting followers list...")
            try:
                params = {
                    "count": min(max_followers, 50),
                    "rank_token": f"{client.user_id}_{client.uuid}",
                    "search_surface": "follow_list_page"
                }

                follower_response = client.private_request(f"friendships/{user_id}/followers/", params=params)

                if 'users' not in follower_response:
                    print("❌ No followers data received")
                    return None

                followers = follower_response['users']
                print(f"✅ Got {len(followers)} followers for analysis")

            except Exception as e:
                print(f"❌ Failed to get followers: {e}")
                return None

            # Analyze each follower's activity
            results = {
                'target_username': username,
                'target_user_id': str(user_id),
                'analysis_date': datetime.now().isoformat(),
                'followers_analyzed': len(followers),
                'follower_activities': []
            }

            print(f"\n🔍 Analyzing activity for {len(followers)} followers...")
            print("=" * 60)

            for i, follower in enumerate(followers, 1):
                follower_username = follower.get('username')
                follower_id = follower.get('pk')

                print(f"\n{i:2d}. Analyzing @{follower_username}...")

                # Get follower activity data
                follower_activity = {
                    'username': follower_username,
                    'user_id': str(follower_id),
                    'full_name': follower.get('full_name', ''),
                    'is_private': follower.get('is_private', False),
                    'is_verified': follower.get('is_verified', False),
                    'follower_count': follower.get('follower_count', 0)
                }

                # Get last post info
                print(f"   📸 Checking last post...")
                post_info = self.get_last_post_info(follower_id)
                follower_activity['last_post'] = post_info

                # Get story activity
                print(f"   📱 Checking story activity...")
                story_info = self.get_story_activity(follower_id)
                follower_activity['story_activity'] = story_info

                # Get general activity status
                print(f"   ⏰ Checking activity status...")
                activity_status = self.get_user_activity_status(follower_id)
                follower_activity['activity_status'] = activity_status

                results['follower_activities'].append(follower_activity)

                # Display summary
                if post_info.get('has_posts'):
                    days_ago = post_info.get('days_since_last_post', 'Unknown')
                    print(f"   ✅ Last post: {days_ago} days ago")
                else:
                    print(f"   ❌ No posts found")

                if story_info.get('has_active_stories'):
                    hours_ago = story_info.get('hours_since_story', 'Unknown')
                    print(f"   📱 Active story: {hours_ago}h ago")
                else:
                    print(f"   📱 No active stories")

                # Be respectful with requests
                if i < len(followers):
                    time.sleep(1)

            # Generate summary report
            self.generate_activity_report(results)

            # Save detailed results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = Path(f"data/follower_activity_{username}_{timestamp}.json")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"\n💾 Detailed results saved to: {output_file}")

            return results

        except Exception as e:
            print(f"💥 Analysis failed: {e}")
            return None

    def generate_activity_report(self, results):
        """Generate a summary report of follower activity"""

        print(f"\n📊 ACTIVITY SUMMARY for @{results['target_username']}")
        print("=" * 60)

        activities = results['follower_activities']
        total = len(activities)

        if total == 0:
            print("No followers analyzed")
            return

        # Post activity analysis
        active_posters = [a for a in activities if a['last_post'].get('has_posts') and a['last_post'].get('days_since_last_post') is not None]
        recent_posters = [a for a in active_posters if a['last_post']['days_since_last_post'] <= 7]
        inactive_posters = [a for a in active_posters if a['last_post']['days_since_last_post'] > 30]

        print(f"📸 POST ACTIVITY:")
        print(f"   Active posters: {len(active_posters)}/{total} ({len(active_posters)/total*100:.1f}%)")
        print(f"   Posted this week: {len(recent_posters)}/{total} ({len(recent_posters)/total*100:.1f}%)")
        print(f"   Inactive (30+ days): {len(inactive_posters)}/{total} ({len(inactive_posters)/total*100:.1f}%)")

        # Story activity analysis
        story_active = [a for a in activities if a['story_activity'].get('has_active_stories')]

        print(f"\n📱 STORY ACTIVITY:")
        print(f"   Active stories: {len(story_active)}/{total} ({len(story_active)/total*100:.1f}%)")

        # Most active followers
        print(f"\n🔥 MOST ACTIVE FOLLOWERS:")
        active_sorted = sorted(
            [a for a in active_posters if a['last_post']['days_since_last_post'] is not None],
            key=lambda x: x['last_post']['days_since_last_post']
        )

        for i, follower in enumerate(active_sorted[:5], 1):
            username = follower['username']
            days = follower['last_post']['days_since_last_post']
            likes = follower['last_post']['like_count']
            story = "📱" if follower['story_activity'].get('has_active_stories') else ""
            verified = "✅" if follower['is_verified'] else ""
            private = "🔒" if follower['is_private'] else ""

            print(f"   {i}. {verified}{private}{story} @{username} - {days} days ago ({likes} likes)")

        # Least active followers
        print(f"\n😴 LEAST ACTIVE FOLLOWERS:")
        inactive_sorted = sorted(
            active_posters,
            key=lambda x: x['last_post']['days_since_last_post'],
            reverse=True
        )

        for i, follower in enumerate(inactive_sorted[:5], 1):
            username = follower['username']
            days = follower['last_post']['days_since_last_post']
            private = "🔒" if follower['is_private'] else ""

            print(f"   {i}. {private} @{username} - {days} days ago")

def main():
    """Main function"""

    print("👥 Instagram Follower Activity Analyzer")
    print("Analyzes last posts, stories, and activity for followers")
    print("=" * 60)

    # You can change this to analyze any user's followers
    target_username = input("Enter username to analyze followers for (default: yoga_ss_): ").strip()
    if not target_username:
        target_username = "yoga_ss_"

    max_followers = input("Max followers to analyze (default: 25): ").strip()
    if not max_followers:
        max_followers = 25
    else:
        max_followers = int(max_followers)

    analyzer = FollowerActivityAnalyzer()
    result = analyzer.analyze_followers_activity(target_username, max_followers)

    if result:
        print("\n🎉 Activity analysis completed!")
        print("Check the generated JSON file for detailed results.")
    else:
        print("\n😞 Analysis failed")

if __name__ == "__main__":
    main()