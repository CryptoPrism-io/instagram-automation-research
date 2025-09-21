#!/usr/bin/env python3
"""
Specialized Analysis for @yoga_ss_ (Yogesh Sahu)
Uses DM data and alternative methods when direct profile access is restricted
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

class YogaAnalyzer:
    """Specialized analyzer for @yoga_ss_ using available data"""

    def __init__(self):
        """Initialize analyzer"""
        from core.session_manager import InstagramSessionManager

        self.target_username = "yoga_ss_"
        self.target_user_id = 143732789  # From DM data
        self.target_full_name = "Yogesh Sahu"
        self.session_manager = InstagramSessionManager()
        self.client = None
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

    def analyze_from_dm_data(self) -> bool:
        """Analyze using existing DM conversation data"""
        try:
            print(f"\n💬 Analyzing DM conversation with @{self.target_username}...")

            # Load existing DM data
            dm_file = Path("data/real_dm_data_20250920_235320.json")
            if not dm_file.exists():
                print("❌ No DM data file found")
                return False

            with open(dm_file, 'r') as f:
                dm_data = json.load(f)

            # Find conversation with yoga_ss_
            target_conversation = None
            for conv in dm_data['conversations']:
                for user in conv['users']:
                    if user['username'] == self.target_username:
                        target_conversation = conv
                        break
                if target_conversation:
                    break

            if not target_conversation:
                print(f"❌ No conversation found with @{self.target_username}")
                return False

            # Analyze DM conversation
            dm_analysis = {
                'conversation_exists': True,
                'user_id': self.target_user_id,
                'full_name': self.target_full_name,
                'thread_id': target_conversation['thread_id'],
                'total_messages': target_conversation['message_count'],
                'last_activity': target_conversation['last_activity'],
                'message_breakdown': {
                    'sent_by_me': 0,
                    'received_from_friend': 0
                },
                'message_types': Counter(),
                'conversation_timeline': []
            }

            # Analyze messages
            for msg in target_conversation['messages']:
                if msg['is_sent_by_me']:
                    dm_analysis['message_breakdown']['sent_by_me'] += 1
                else:
                    dm_analysis['message_breakdown']['received_from_friend'] += 1

                dm_analysis['message_types'][msg['item_type']] += 1

                # Add to timeline
                dm_analysis['conversation_timeline'].append({
                    'timestamp': msg['timestamp'],
                    'sender': 'me' if msg['is_sent_by_me'] else 'yoga_ss_',
                    'type': msg['item_type']
                })

            # Calculate last activity
            if target_conversation['last_activity']:
                try:
                    last_activity_dt = datetime.fromtimestamp(target_conversation['last_activity'] / 1000000)
                    dm_analysis['last_activity_formatted'] = last_activity_dt.strftime('%Y-%m-%d %H:%M:%S')
                    dm_analysis['days_since_last_activity'] = (datetime.now() - last_activity_dt).days
                except:
                    dm_analysis['last_activity_formatted'] = 'Unknown'
                    dm_analysis['days_since_last_activity'] = None

            self.analysis_data['dm_conversation'] = dm_analysis

            print(f"✅ DM analysis complete:")
            print(f"   💬 Total messages: {dm_analysis['total_messages']}")
            print(f"   📤 Sent by you: {dm_analysis['message_breakdown']['sent_by_me']}")
            print(f"   📥 Received: {dm_analysis['message_breakdown']['received_from_friend']}")
            print(f"   📅 Last activity: {dm_analysis['last_activity_formatted']}")

            return True

        except Exception as e:
            print(f"💥 DM analysis error: {e}")
            return False

    def attempt_profile_access(self) -> bool:
        """Attempt different methods to access profile info"""
        try:
            print(f"\n👤 Attempting profile access for @{self.target_username}...")

            profile_data = {
                'username': self.target_username,
                'user_id': self.target_user_id,
                'full_name': self.target_full_name,
                'access_method': 'dm_data',
                'direct_access': False,
                'profile_accessible': False
            }

            # Try direct API access (might be restricted)
            try:
                user_info = self.client.user_info_by_username(self.target_username)
                if user_info:
                    profile_data.update({
                        'follower_count': user_info.follower_count,
                        'following_count': user_info.following_count,
                        'media_count': user_info.media_count,
                        'is_private': user_info.is_private,
                        'is_verified': user_info.is_verified,
                        'biography': user_info.biography,
                        'access_method': 'direct_api',
                        'direct_access': True,
                        'profile_accessible': True
                    })
                    print(f"✅ Direct profile access successful")
            except Exception as e:
                print(f"   ⚠️ Direct profile access failed: {e}")
                print(f"   📋 Using DM-based data instead")

            # Try alternative user ID lookup
            if not profile_data['direct_access']:
                try:
                    # Sometimes we can get basic info via user_id
                    user_info = self.client.user_info(self.target_user_id)
                    if user_info:
                        profile_data.update({
                            'follower_count': getattr(user_info, 'follower_count', 'Unknown'),
                            'following_count': getattr(user_info, 'following_count', 'Unknown'),
                            'media_count': getattr(user_info, 'media_count', 'Unknown'),
                            'is_private': getattr(user_info, 'is_private', 'Unknown'),
                            'access_method': 'user_id_lookup',
                            'profile_accessible': True
                        })
                        print(f"✅ User ID lookup successful")
                except Exception as e:
                    print(f"   ⚠️ User ID lookup also failed: {e}")

            self.analysis_data['profile'] = profile_data
            return True

        except Exception as e:
            print(f"💥 Profile access error: {e}")
            return False

    def check_friendship_status(self) -> bool:
        """Check friendship and connection status"""
        try:
            print(f"\n🤝 Checking friendship status with @{self.target_username}...")

            friendship_analysis = {
                'dm_conversation_exists': True,
                'user_found_in_dms': True,
                'user_id_known': True,
                'full_name_known': True,
                'profile_restrictions': 'Unknown',
                'relationship_evidence': []
            }

            # Evidence from DM data
            if 'dm_conversation' in self.analysis_data:
                dm = self.analysis_data['dm_conversation']
                if dm['total_messages'] > 0:
                    friendship_analysis['relationship_evidence'].append(
                        f"Active DM conversation with {dm['total_messages']} messages"
                    )

                if dm['message_breakdown']['sent_by_me'] > 0 and dm['message_breakdown']['received_from_friend'] > 0:
                    friendship_analysis['relationship_evidence'].append(
                        "Bidirectional communication (both send and receive messages)"
                    )

                if dm.get('days_since_last_activity') is not None and dm['days_since_last_activity'] < 30:
                    friendship_analysis['relationship_evidence'].append(
                        f"Recent activity ({dm['days_since_last_activity']} days ago)"
                    )

            # Try to check following status
            try:
                # This might fail due to API restrictions
                followers = self.client.user_followers(self.client.user_id, amount=100)
                friendship_analysis['following_them'] = any(user.pk == self.target_user_id for user in followers)
            except:
                friendship_analysis['following_them'] = 'Unable to check'

            try:
                following = self.client.user_following(self.client.user_id, amount=100)
                friendship_analysis['followed_by_them'] = any(user.pk == self.target_user_id for user in following)
            except:
                friendship_analysis['followed_by_them'] = 'Unable to check'

            self.analysis_data['friendship'] = friendship_analysis

            print(f"✅ Friendship analysis:")
            print(f"   💬 DM conversation: Active")
            print(f"   📋 Evidence count: {len(friendship_analysis['relationship_evidence'])}")

            return True

        except Exception as e:
            print(f"💥 Friendship analysis error: {e}")
            return False

    def generate_report(self) -> str:
        """Generate comprehensive report"""
        try:
            print(f"\n📋 Generating analysis report...")

            report = []
            report.append(f"# Specialized Analysis: @{self.target_username}")
            report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"**Analyzer**: @{self.session_manager.username}")
            report.append(f"**Analysis Type**: DM-based + Limited Profile Access")
            report.append("")

            # Profile Summary
            if 'profile' in self.analysis_data:
                profile = self.analysis_data['profile']
                report.append("## 👤 Profile Information")
                report.append(f"- **Username**: @{profile['username']}")
                report.append(f"- **Full Name**: {profile['full_name']}")
                report.append(f"- **User ID**: {profile['user_id']}")
                report.append(f"- **Direct Access**: {'✅ Yes' if profile['direct_access'] else '❌ No (Restricted)'}")
                report.append(f"- **Data Source**: {profile['access_method'].replace('_', ' ').title()}")

                if profile.get('follower_count'):
                    report.append(f"- **Followers**: {profile['follower_count']}")
                    report.append(f"- **Following**: {profile['following_count']}")
                    report.append(f"- **Posts**: {profile['media_count']}")
                    report.append(f"- **Private Account**: {'✅ Yes' if profile.get('is_private') else '❌ No'}")

                report.append("")

            # DM Analysis
            if 'dm_conversation' in self.analysis_data:
                dm = self.analysis_data['dm_conversation']
                report.append("## 💬 DM Conversation Analysis")
                report.append(f"- **Conversation Status**: ✅ Active")
                report.append(f"- **Total Messages**: {dm['total_messages']}")
                report.append(f"- **Messages from you**: {dm['message_breakdown']['sent_by_me']}")
                report.append(f"- **Messages from them**: {dm['message_breakdown']['received_from_friend']}")
                report.append(f"- **Last Activity**: {dm.get('last_activity_formatted', 'Unknown')}")

                if dm.get('days_since_last_activity') is not None:
                    if dm['days_since_last_activity'] < 7:
                        activity_status = "🔥 Very Recent"
                    elif dm['days_since_last_activity'] < 30:
                        activity_status = "📅 Recent"
                    elif dm['days_since_last_activity'] < 90:
                        activity_status = "📆 Moderate"
                    else:
                        activity_status = "📋 Older"

                    report.append(f"- **Activity Status**: {activity_status} ({dm['days_since_last_activity']} days ago)")

                if dm['message_types']:
                    report.append("- **Message Types**:")
                    for msg_type, count in dm['message_types'].most_common():
                        report.append(f"  - {msg_type}: {count}")

                report.append("")

            # Friendship Status
            if 'friendship' in self.analysis_data:
                friendship = self.analysis_data['friendship']
                report.append("## 🤝 Relationship Analysis")
                report.append(f"- **DM Connection**: ✅ Established")
                report.append(f"- **Known Identity**: ✅ Confirmed ({self.target_full_name})")

                if friendship['relationship_evidence']:
                    report.append("- **Relationship Evidence**:")
                    for evidence in friendship['relationship_evidence']:
                        report.append(f"  - {evidence}")

                report.append("")

            # Key Insights
            report.append("## 💡 Key Insights")

            if 'dm_conversation' in self.analysis_data:
                dm = self.analysis_data['dm_conversation']

                # Communication balance
                total_msgs = dm['message_breakdown']['sent_by_me'] + dm['message_breakdown']['received_from_friend']
                if total_msgs > 0:
                    balance_ratio = dm['message_breakdown']['sent_by_me'] / total_msgs
                    if 0.4 <= balance_ratio <= 0.6:
                        report.append("- 🤝 **Balanced Communication**: Equal participation in conversation")
                    elif balance_ratio > 0.6:
                        report.append("- 📤 **You're More Active**: You send more messages")
                    else:
                        report.append("- 📥 **They're More Active**: They send more messages")

                # Activity pattern
                if dm.get('days_since_last_activity') is not None:
                    if dm['days_since_last_activity'] < 7:
                        report.append("- 🔥 **Active Connection**: Very recent communication")
                    elif dm['days_since_last_activity'] < 30:
                        report.append("- 📱 **Regular Contact**: Recent communication")

            # Profile access status
            if 'profile' in self.analysis_data:
                profile = self.analysis_data['profile']
                if not profile['direct_access']:
                    report.append("- 🔒 **Profile Restrictions**: Limited public access (possibly private account)")
                    report.append("- 💬 **DM-Based Analysis**: Using conversation data for insights")

            report.append("")
            report.append("## 🔍 Analysis Limitations")
            report.append("- **Profile Access**: Limited due to privacy settings or restrictions")
            report.append("- **Data Source**: Primarily based on DM conversation history")
            report.append("- **Scope**: Cannot analyze posts, followers, or public activity")
            report.append("")

            report.append("---")
            report.append("*Analysis conducted with available data and consent*")
            report.append("*Respecting privacy settings and platform restrictions*")

            return '\n'.join(report)

        except Exception as e:
            print(f"💥 Report generation error: {e}")
            return f"Error generating report: {e}"

    def run_analysis(self) -> bool:
        """Run specialized analysis for @yoga_ss_"""
        print(f"🚀 Starting Specialized Analysis for @{self.target_username}")
        print(f"Target: @{self.target_username} (Yogesh Sahu)")
        print("=" * 60)

        try:
            # Step 1: Connect
            if not self.connect():
                return False

            # Step 2: Analyze from DM data
            if not self.analyze_from_dm_data():
                return False

            # Step 3: Attempt profile access
            self.attempt_profile_access()

            # Step 4: Check friendship status
            self.check_friendship_status()

            # Step 5: Generate report
            report = self.generate_report()

            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Save raw data
            data_file = Path(f"data/yoga_analysis_{timestamp}.json")
            data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_data, f, indent=2, default=str)

            # Save report
            report_file = Path(f"data/yoga_report_{timestamp}.md")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"\n✅ Specialized analysis completed!")
            print(f"📊 Raw data: {data_file}")
            print(f"📄 Report: {report_file}")

            # Display summary
            if 'dm_conversation' in self.analysis_data:
                dm = self.analysis_data['dm_conversation']
                print(f"\n🔍 YOGA_SS_ ANALYSIS SUMMARY:")
                print("=" * 40)
                print(f"👤 Full Name: {self.target_full_name}")
                print(f"💬 DM Messages: {dm['total_messages']}")
                print(f"📤 Sent by you: {dm['message_breakdown']['sent_by_me']}")
                print(f"📥 Received: {dm['message_breakdown']['received_from_friend']}")
                print(f"📅 Last activity: {dm.get('last_activity_formatted', 'Unknown')}")

            return True

        except Exception as e:
            print(f"💥 Analysis failed: {e}")
            return False

def main():
    """Main function"""
    print("👥 Specialized Instagram Analysis - @yoga_ss_")
    print("Using DM data and alternative access methods")
    print("=" * 60)

    analyzer = YogaAnalyzer()
    success = analyzer.run_analysis()

    if success:
        print("\n🎉 Specialized analysis completed successfully!")
        print("Despite profile restrictions, valuable insights were extracted!")
    else:
        print("\n😞 Analysis failed - check logs for details")

if __name__ == "__main__":
    main()