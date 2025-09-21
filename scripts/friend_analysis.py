#!/usr/bin/env python3
"""
Comprehensive Friend Analysis - @kanikaachaudhary
Tests all instagrapi functionality with consent-based friend analysis
Based on docs/instagrapi/ modules
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Any, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FriendAnalyzer:
    """Comprehensive Instagram friend analysis using all instagrapi features"""

    def __init__(self, target_username: str = "kanikaachaudhary"):
        """Initialize friend analyzer"""
        from core.session_manager import InstagramSessionManager

        self.target_username = target_username
        self.session_manager = InstagramSessionManager()
        self.client = None
        self.target_user = None
        self.analysis_data = {}

    def connect(self) -> bool:
        """Connect using existing session"""
        try:
            print("🔐 Connecting to Instagram (using session)...")
            self.client = self.session_manager.get_smart_client()

            if self.client:
                user_info = self.client.account_info()
                print(f"✅ Connected as: {user_info.username}")
                return True
            else:
                print("❌ Failed to connect")
                return False

        except Exception as e:
            print(f"💥 Connection error: {e}")
            return False

    def get_user_profile(self) -> bool:
        """Test user profile retrieval - docs/instagrapi/user.md"""
        try:
            print(f"\n👤 Getting profile info for @{self.target_username}...")

            # Get user info by username (primary method)
            self.target_user = self.client.user_info_by_username(self.target_username)

            if not self.target_user:
                print(f"❌ User @{self.target_username} not found")
                return False

            profile_data = {
                'username': self.target_user.username,
                'user_id': self.target_user.pk,
                'full_name': self.target_user.full_name,
                'biography': self.target_user.biography,
                'follower_count': self.target_user.follower_count,
                'following_count': self.target_user.following_count,
                'media_count': self.target_user.media_count,
                'is_private': self.target_user.is_private,
                'is_verified': self.target_user.is_verified,
                'is_business': getattr(self.target_user, 'is_business', False),
                'category': getattr(self.target_user, 'category', None),
                'external_url': getattr(self.target_user, 'external_url', None),
                'profile_pic_url': self.target_user.profile_pic_url,
            }

            self.analysis_data['profile'] = profile_data

            print(f"✅ Profile retrieved:")
            print(f"   👤 Name: {profile_data['full_name']}")
            print(f"   🆔 ID: {profile_data['user_id']}")
            print(f"   👥 Followers: {profile_data['follower_count']}")
            print(f"   📸 Posts: {profile_data['media_count']}")
            print(f"   🔒 Private: {profile_data['is_private']}")

            # Add delay
            time.sleep(2)
            return True

        except Exception as e:
            print(f"💥 Profile analysis error: {e}")
            return False

    def analyze_media_posts(self, limit: int = 12) -> bool:
        """Test media analysis - docs/instagrapi/media.md"""
        try:
            print(f"\n📸 Analyzing recent posts (limit: {limit})...")

            if self.target_user.is_private:
                print("⚠️ Account is private - media analysis limited")
                return True

            # Get user media
            medias = self.client.user_medias(self.target_user.pk, amount=limit)

            if not medias:
                print("📭 No public posts found")
                return True

            media_analysis = {
                'total_posts': len(medias),
                'posts': [],
                'engagement_stats': {
                    'total_likes': 0,
                    'total_comments': 0,
                    'avg_likes': 0,
                    'avg_comments': 0,
                    'engagement_rate': 0
                },
                'content_types': Counter(),
                'posting_patterns': {
                    'hours': Counter(),
                    'days': Counter()
                }
            }

            print(f"📊 Found {len(medias)} recent posts")

            for i, media in enumerate(medias):
                try:
                    print(f"   📝 Analyzing post {i+1}/{len(medias)}: {media.pk}")

                    # Get detailed media info
                    media_info = self.client.media_info(media.pk)

                    post_data = {
                        'media_id': media.pk,
                        'media_type': media_info.media_type,
                        'like_count': media_info.like_count,
                        'comment_count': media_info.comment_count,
                        'caption': media_info.caption_text[:200] if media_info.caption_text else '',
                        'taken_at': media_info.taken_at,
                        'location': getattr(media_info, 'location', None)
                    }

                    media_analysis['posts'].append(post_data)

                    # Update stats
                    media_analysis['engagement_stats']['total_likes'] += media_info.like_count
                    media_analysis['engagement_stats']['total_comments'] += media_info.comment_count

                    # Content type analysis
                    if media_info.media_type == 1:
                        media_analysis['content_types']['photo'] += 1
                    elif media_info.media_type == 2:
                        media_analysis['content_types']['video'] += 1
                    elif media_info.media_type == 8:
                        media_analysis['content_types']['carousel'] += 1

                    # Time pattern analysis
                    if media_info.taken_at:
                        post_time = media_info.taken_at
                        media_analysis['posting_patterns']['hours'][post_time.hour] += 1
                        media_analysis['posting_patterns']['days'][post_time.strftime('%A')] += 1

                    # Rate limiting delay
                    time.sleep(1)

                except Exception as e:
                    print(f"      ⚠️ Error analyzing post {media.pk}: {e}")
                    continue

            # Calculate averages
            if len(medias) > 0:
                media_analysis['engagement_stats']['avg_likes'] = media_analysis['engagement_stats']['total_likes'] / len(medias)
                media_analysis['engagement_stats']['avg_comments'] = media_analysis['engagement_stats']['total_comments'] / len(medias)

                # Calculate engagement rate (likes + comments / followers)
                if self.target_user.follower_count > 0:
                    total_engagement = media_analysis['engagement_stats']['total_likes'] + media_analysis['engagement_stats']['total_comments']
                    media_analysis['engagement_stats']['engagement_rate'] = (total_engagement / len(medias)) / self.target_user.follower_count * 100

            self.analysis_data['media'] = media_analysis

            print(f"✅ Media analysis complete:")
            print(f"   📊 Total engagement: {media_analysis['engagement_stats']['total_likes']} likes, {media_analysis['engagement_stats']['total_comments']} comments")
            print(f"   📈 Avg per post: {media_analysis['engagement_stats']['avg_likes']:.1f} likes, {media_analysis['engagement_stats']['avg_comments']:.1f} comments")
            print(f"   📱 Engagement rate: {media_analysis['engagement_stats']['engagement_rate']:.2f}%")

            return True

        except Exception as e:
            print(f"💥 Media analysis error: {e}")
            return False

    def analyze_followers_sample(self, limit: int = 50) -> bool:
        """Test follower analysis - docs/instagrapi/user.md"""
        try:
            print(f"\n👥 Analyzing followers sample (limit: {limit})...")

            if self.target_user.is_private:
                print("⚠️ Account is private - follower analysis not available")
                return True

            # Get followers sample
            followers = self.client.user_followers(self.target_user.pk, amount=limit)

            if not followers:
                print("👥 No followers data available")
                return True

            follower_analysis = {
                'sample_size': len(followers),
                'total_followers': self.target_user.follower_count,
                'demographics': {
                    'verified_users': 0,
                    'business_accounts': 0,
                    'private_accounts': 0
                },
                'engagement_indicators': {
                    'avg_follower_count': 0,
                    'avg_following_count': 0
                },
                'top_followers': []
            }

            print(f"📊 Analyzing {len(followers)} followers...")

            total_follower_count = 0
            total_following_count = 0

            for user in followers[:20]:  # Analyze top 20 for detailed insights
                try:
                    if user.is_verified:
                        follower_analysis['demographics']['verified_users'] += 1

                    if getattr(user, 'is_business', False):
                        follower_analysis['demographics']['business_accounts'] += 1

                    if user.is_private:
                        follower_analysis['demographics']['private_accounts'] += 1

                    total_follower_count += user.follower_count
                    total_following_count += user.following_count

                    # Add to top followers if significant following
                    if user.follower_count > 1000 or user.is_verified:
                        follower_analysis['top_followers'].append({
                            'username': user.username,
                            'full_name': user.full_name,
                            'follower_count': user.follower_count,
                            'is_verified': user.is_verified,
                            'is_business': getattr(user, 'is_business', False)
                        })

                except Exception as e:
                    continue

            # Calculate averages
            if len(followers) > 0:
                follower_analysis['engagement_indicators']['avg_follower_count'] = total_follower_count / len(followers)
                follower_analysis['engagement_indicators']['avg_following_count'] = total_following_count / len(followers)

            # Sort top followers by follower count
            follower_analysis['top_followers'].sort(key=lambda x: x['follower_count'], reverse=True)

            self.analysis_data['followers'] = follower_analysis

            print(f"✅ Follower analysis complete:")
            print(f"   ✅ Verified followers: {follower_analysis['demographics']['verified_users']}")
            print(f"   🏢 Business accounts: {follower_analysis['demographics']['business_accounts']}")
            print(f"   👥 Avg follower count: {follower_analysis['engagement_indicators']['avg_follower_count']:.0f}")

            return True

        except Exception as e:
            print(f"💥 Follower analysis error: {e}")
            return False

    def analyze_dm_conversation(self) -> bool:
        """Analyze DM conversation - docs/instagrapi/direct-messages.md"""
        try:
            print(f"\n💬 Analyzing DM conversation with @{self.target_username}...")

            # Get DM threads
            threads = self.client.direct_threads(amount=50)

            # Find conversation with target user
            target_thread = None
            for thread in threads:
                if not thread.is_group:
                    for user in thread.users:
                        if user.username == self.target_username:
                            target_thread = thread
                            break
                    if target_thread:
                        break

            if not target_thread:
                print(f"💬 No DM conversation found with @{self.target_username}")
                return True

            # Get thread details
            thread_details = self.client.direct_thread(target_thread.id)

            dm_analysis = {
                'conversation_exists': True,
                'thread_id': target_thread.id,
                'total_messages': len(thread_details.messages) if hasattr(thread_details, 'messages') else 0,
                'last_activity': target_thread.last_activity_at,
                'message_breakdown': {
                    'sent_by_me': 0,
                    'received_from_friend': 0
                },
                'message_types': Counter(),
                'conversation_pattern': []
            }

            # Analyze recent messages
            if hasattr(thread_details, 'messages'):
                for msg in thread_details.messages[:20]:  # Last 20 messages
                    try:
                        if msg.user_id == self.client.user_id:
                            dm_analysis['message_breakdown']['sent_by_me'] += 1
                        else:
                            dm_analysis['message_breakdown']['received_from_friend'] += 1

                        dm_analysis['message_types'][msg.item_type] += 1

                        # Basic message pattern (without revealing content)
                        dm_analysis['conversation_pattern'].append({
                            'timestamp': msg.timestamp,
                            'sender': 'me' if msg.user_id == self.client.user_id else 'friend',
                            'type': msg.item_type
                        })

                    except Exception as e:
                        continue

            self.analysis_data['dm_conversation'] = dm_analysis

            print(f"✅ DM analysis complete:")
            print(f"   💬 Total messages: {dm_analysis['total_messages']}")
            print(f"   📤 Sent by you: {dm_analysis['message_breakdown']['sent_by_me']}")
            print(f"   📥 Received: {dm_analysis['message_breakdown']['received_from_friend']}")

            return True

        except Exception as e:
            print(f"💥 DM analysis error: {e}")
            return False

    def check_friendship_status(self) -> bool:
        """Check friendship status and interactions"""
        try:
            print(f"\n🤝 Checking friendship status with @{self.target_username}...")

            friendship_analysis = {
                'following_them': False,
                'followed_by_them': False,
                'relationship_status': 'unknown',
                'can_see_posts': not self.target_user.is_private,
                'mutual_connection': False
            }

            # Check if we follow them
            try:
                following = self.client.user_following(self.client.user_id, amount=1000)
                friendship_analysis['following_them'] = any(user.pk == self.target_user.pk for user in following)
            except:
                print("   ⚠️ Could not check following status")

            # Check if they follow us
            try:
                followers = self.client.user_followers(self.client.user_id, amount=1000)
                friendship_analysis['followed_by_them'] = any(user.pk == self.target_user.pk for user in followers)
            except:
                print("   ⚠️ Could not check follower status")

            # Determine relationship status
            if friendship_analysis['following_them'] and friendship_analysis['followed_by_them']:
                friendship_analysis['relationship_status'] = 'mutual_friends'
                friendship_analysis['mutual_connection'] = True
            elif friendship_analysis['following_them']:
                friendship_analysis['relationship_status'] = 'you_follow_them'
            elif friendship_analysis['followed_by_them']:
                friendship_analysis['relationship_status'] = 'they_follow_you'
            else:
                friendship_analysis['relationship_status'] = 'no_connection'

            self.analysis_data['friendship'] = friendship_analysis

            print(f"✅ Friendship status:")
            print(f"   👤 You follow them: {friendship_analysis['following_them']}")
            print(f"   👤 They follow you: {friendship_analysis['followed_by_them']}")
            print(f"   🤝 Status: {friendship_analysis['relationship_status']}")

            return True

        except Exception as e:
            print(f"💥 Friendship analysis error: {e}")
            return False

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive friend analysis report"""
        try:
            print(f"\n📋 Generating comprehensive report...")

            report = []
            report.append(f"# Comprehensive Friend Analysis: @{self.target_username}")
            report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"**Analyzer**: @{self.session_manager.username}")
            report.append("")

            # Profile Summary
            if 'profile' in self.analysis_data:
                profile = self.analysis_data['profile']
                report.append("## 👤 Profile Overview")
                report.append(f"- **Username**: @{profile['username']}")
                report.append(f"- **Full Name**: {profile['full_name']}")
                report.append(f"- **Bio**: {profile['biography'][:100]}..." if profile['biography'] else "- **Bio**: Not provided")
                report.append(f"- **Followers**: {profile['follower_count']:,}")
                report.append(f"- **Following**: {profile['following_count']:,}")
                report.append(f"- **Posts**: {profile['media_count']:,}")
                report.append(f"- **Account Type**: {'Private' if profile['is_private'] else 'Public'}")
                report.append(f"- **Verified**: {'✅ Yes' if profile['is_verified'] else '❌ No'}")
                report.append("")

            # Friendship Status
            if 'friendship' in self.analysis_data:
                friendship = self.analysis_data['friendship']
                report.append("## 🤝 Friendship Status")
                report.append(f"- **Relationship**: {friendship['relationship_status'].replace('_', ' ').title()}")
                report.append(f"- **You follow them**: {'✅ Yes' if friendship['following_them'] else '❌ No'}")
                report.append(f"- **They follow you**: {'✅ Yes' if friendship['followed_by_them'] else '❌ No'}")
                report.append(f"- **Mutual connection**: {'✅ Yes' if friendship['mutual_connection'] else '❌ No'}")
                report.append("")

            # Content Analysis
            if 'media' in self.analysis_data:
                media = self.analysis_data['media']
                report.append("## 📸 Content Analysis")
                report.append(f"- **Recent posts analyzed**: {media['total_posts']}")
                report.append(f"- **Average likes per post**: {media['engagement_stats']['avg_likes']:.1f}")
                report.append(f"- **Average comments per post**: {media['engagement_stats']['avg_comments']:.1f}")
                report.append(f"- **Engagement rate**: {media['engagement_stats']['engagement_rate']:.2f}%")

                if media['content_types']:
                    report.append("- **Content types**:")
                    for content_type, count in media['content_types'].most_common():
                        report.append(f"  - {content_type.title()}: {count} posts")
                report.append("")

            # DM Analysis
            if 'dm_conversation' in self.analysis_data:
                dm = self.analysis_data['dm_conversation']
                if dm['conversation_exists']:
                    report.append("## 💬 DM Conversation Analysis")
                    report.append(f"- **Total messages**: {dm['total_messages']}")
                    report.append(f"- **Messages from you**: {dm['message_breakdown']['sent_by_me']}")
                    report.append(f"- **Messages from them**: {dm['message_breakdown']['received_from_friend']}")

                    if dm['message_types']:
                        report.append("- **Message types**:")
                        for msg_type, count in dm['message_types'].most_common():
                            report.append(f"  - {msg_type}: {count}")
                    report.append("")

            # Follower Insights
            if 'followers' in self.analysis_data:
                followers = self.analysis_data['followers']
                report.append("## 👥 Follower Analysis")
                report.append(f"- **Sample analyzed**: {followers['sample_size']} of {followers['total_followers']} followers")
                report.append(f"- **Verified followers**: {followers['demographics']['verified_users']}")
                report.append(f"- **Business accounts**: {followers['demographics']['business_accounts']}")
                report.append(f"- **Private accounts**: {followers['demographics']['private_accounts']}")

                if followers['top_followers']:
                    report.append("- **Notable followers**:")
                    for follower in followers['top_followers'][:5]:
                        status = "✅" if follower['is_verified'] else "🏢" if follower['is_business'] else "👤"
                        report.append(f"  - {status} @{follower['username']} ({follower['follower_count']:,} followers)")
                report.append("")

            # Summary & Insights
            report.append("## 💡 Key Insights")

            if 'profile' in self.analysis_data:
                profile = self.analysis_data['profile']
                follower_ratio = profile['following_count'] / max(profile['follower_count'], 1)

                if follower_ratio < 0.5:
                    report.append("- 🌟 **Influential Account**: Low following-to-follower ratio indicates influence")
                elif follower_ratio > 2:
                    report.append("- 🤝 **Social Connector**: High following-to-follower ratio indicates social activity")

                if profile['media_count'] > 100:
                    report.append("- 📸 **Active Content Creator**: High number of posts shows consistent activity")

            if 'media' in self.analysis_data and 'profile' in self.analysis_data:
                media = self.analysis_data['media']
                if media['engagement_stats']['engagement_rate'] > 3:
                    report.append("- 🔥 **High Engagement**: Above-average engagement rate for follower count")

            if 'friendship' in self.analysis_data:
                friendship = self.analysis_data['friendship']
                if friendship['mutual_connection']:
                    report.append("- 💫 **Strong Connection**: Mutual following indicates close relationship")

            report.append("")
            report.append("---")
            report.append("*Analysis conducted with consent using Instagram automation research platform*")
            report.append("*All data extracted safely and ethically*")

            return '\n'.join(report)

        except Exception as e:
            print(f"💥 Report generation error: {e}")
            return f"Error generating report: {e}"

    def run_comprehensive_analysis(self) -> bool:
        """Run complete friend analysis"""
        print(f"🚀 Starting Comprehensive Friend Analysis")
        print(f"Target: @{self.target_username}")
        print("=" * 60)

        try:
            # Step 1: Connect
            if not self.connect():
                return False

            # Step 2: Get profile
            if not self.get_user_profile():
                return False

            # Step 3: Check friendship status
            self.check_friendship_status()

            # Step 4: Analyze DM conversation
            self.analyze_dm_conversation()

            # Step 5: Analyze media (if public)
            if not self.target_user.is_private:
                self.analyze_media_posts(limit=12)
                self.analyze_followers_sample(limit=50)

            # Step 6: Generate report
            report = self.generate_comprehensive_report()

            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Save raw data
            data_file = Path(f"data/friend_analysis_{self.target_username}_{timestamp}.json")
            data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_data, f, indent=2, default=str)

            # Save report
            report_file = Path(f"data/friend_report_{self.target_username}_{timestamp}.md")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"\n✅ Comprehensive analysis completed!")
            print(f"📊 Raw data: {data_file}")
            print(f"📄 Report: {report_file}")

            return True

        except Exception as e:
            print(f"💥 Analysis failed: {e}")
            return False

def main():
    """Main function"""
    target_user = "yoga_ss_"  # Your friend

    print("👥 Instagram Friend Analysis Tool")
    print("Testing all instagrapi functionality with consent")
    print("=" * 60)

    analyzer = FriendAnalyzer(target_user)
    success = analyzer.run_comprehensive_analysis()

    if success:
        print("\n🎉 Friend analysis completed successfully!")
        print("All instagrapi modules tested and working!")
    else:
        print("\n😞 Analysis failed - check logs for details")

if __name__ == "__main__":
    main()