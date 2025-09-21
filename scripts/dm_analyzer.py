#!/usr/bin/env python3
"""
Instagram DM Analyzer
Analyzes your own Instagram direct messages for patterns, engagement, and insights
Safe analysis of personal conversation data
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

class InstagramDMAnalyzer:
    """Analyzes Instagram Direct Messages for insights and patterns"""

    def __init__(self):
        """Initialize DM analyzer"""
        from core.session_manager import InstagramSessionManager

        self.session_manager = InstagramSessionManager()
        self.client = None
        self.analysis_data = {}
        self.conversations = []

    def connect(self) -> bool:
        """Connect to Instagram using session manager"""
        try:
            print("🔐 Connecting to Instagram...")
            self.client = self.session_manager.get_smart_client()

            if self.client:
                user_info = self.client.account_info()
                print(f"✅ Connected as: {user_info.username}")
                print(f"🆔 User ID: {self.client.user_id}")
                return True
            else:
                print("❌ Failed to connect to Instagram")
                return False

        except Exception as e:
            print(f"💥 Connection error: {e}")
            return False

    def extract_dm_data(self, limit: int = 50) -> bool:
        """Extract DM data for analysis"""
        try:
            print(f"\n📥 Extracting DM data (limit: {limit} threads)...")

            # Get inbox threads
            threads = self.client.direct_threads(amount=limit)
            print(f"📊 Found {len(threads)} conversation threads")

            self.conversations = []

            for i, thread in enumerate(threads):
                print(f"   📝 Processing thread {i+1}/{len(threads)}: {thread.id}")

                try:
                    # Get thread details
                    thread_details = self.client.direct_thread(thread.id)

                    # Extract conversation data
                    conversation = {
                        'thread_id': thread.id,
                        'thread_type': thread.thread_type,
                        'is_group': thread.is_group,
                        'user_count': len(thread.users),
                        'users': [{'username': user.username, 'user_id': user.pk} for user in thread.users],
                        'last_activity': thread.last_activity_at,
                        'unread_count': getattr(thread, 'read_state', 0),
                        'message_count': len(thread_details.messages) if hasattr(thread_details, 'messages') else 0,
                        'messages': []
                    }

                    # Extract recent messages (limit to 20 per thread for analysis)
                    if hasattr(thread_details, 'messages'):
                        for msg in thread_details.messages[:20]:
                            message_data = {
                                'message_id': msg.id,
                                'user_id': msg.user_id,
                                'timestamp': msg.timestamp,
                                'message_type': msg.item_type,
                                'text': getattr(msg, 'text', '') if hasattr(msg, 'text') else '',
                                'is_sent_by_me': msg.user_id == self.client.user_id
                            }
                            conversation['messages'].append(message_data)

                    self.conversations.append(conversation)

                    # Add delay to be respectful
                    time.sleep(1)

                except Exception as e:
                    print(f"   ⚠️ Error processing thread {thread.id}: {e}")
                    continue

            print(f"✅ Successfully extracted data from {len(self.conversations)} conversations")
            return True

        except Exception as e:
            print(f"💥 Error extracting DM data: {e}")
            return False

    def analyze_conversation_patterns(self) -> Dict[str, Any]:
        """Analyze conversation patterns and engagement"""
        print("\n🔍 Analyzing conversation patterns...")

        analysis = {
            'total_conversations': len(self.conversations),
            'conversation_types': {
                'individual': 0,
                'group': 0
            },
            'activity_patterns': {
                'most_active_conversations': [],
                'recent_activity': 0,
                'total_messages_analyzed': 0
            },
            'engagement_metrics': {
                'messages_sent': 0,
                'messages_received': 0,
                'response_rate': 0,
                'avg_messages_per_conversation': 0
            },
            'message_types': Counter(),
            'time_patterns': {
                'messages_by_hour': defaultdict(int),
                'messages_by_day': defaultdict(int)
            },
            'top_contacts': []
        }

        total_messages = 0
        messages_sent = 0
        messages_received = 0
        contact_stats = defaultdict(lambda: {'sent': 0, 'received': 0, 'total': 0})

        for conv in self.conversations:
            # Conversation type analysis
            if conv['is_group']:
                analysis['conversation_types']['group'] += 1
            else:
                analysis['conversation_types']['individual'] += 1

            # Message analysis
            total_messages += conv['message_count']

            for msg in conv['messages']:
                # Count message types
                analysis['message_types'][msg['message_type']] += 1

                # Time pattern analysis
                if msg['timestamp']:
                    try:
                        msg_time = datetime.fromisoformat(msg['timestamp'].replace('Z', '+00:00'))
                        analysis['time_patterns']['messages_by_hour'][msg_time.hour] += 1
                        analysis['time_patterns']['messages_by_day'][msg_time.strftime('%A')] += 1
                    except:
                        pass

                # Engagement analysis
                if msg['is_sent_by_me']:
                    messages_sent += 1
                else:
                    messages_received += 1

                # Contact stats (for individual conversations)
                if not conv['is_group'] and conv['users']:
                    other_user = conv['users'][0]['username']
                    if msg['is_sent_by_me']:
                        contact_stats[other_user]['sent'] += 1
                    else:
                        contact_stats[other_user]['received'] += 1
                    contact_stats[other_user]['total'] += 1

        # Calculate metrics
        analysis['activity_patterns']['total_messages_analyzed'] = total_messages
        analysis['engagement_metrics']['messages_sent'] = messages_sent
        analysis['engagement_metrics']['messages_received'] = messages_received

        if total_messages > 0:
            analysis['engagement_metrics']['avg_messages_per_conversation'] = total_messages / len(self.conversations)

        if messages_received > 0:
            analysis['engagement_metrics']['response_rate'] = (messages_sent / messages_received) * 100

        # Recent activity (last 7 days)
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent_activity = sum(1 for conv in self.conversations
                            if conv['last_activity'] and
                            datetime.fromisoformat(conv['last_activity'].replace('Z', '+00:00')) > recent_cutoff)
        analysis['activity_patterns']['recent_activity'] = recent_activity

        # Most active conversations
        active_convs = sorted(self.conversations, key=lambda x: x['message_count'], reverse=True)[:5]
        analysis['activity_patterns']['most_active_conversations'] = [
            {
                'users': conv['users'],
                'message_count': conv['message_count'],
                'is_group': conv['is_group']
            }
            for conv in active_convs
        ]

        # Top contacts
        top_contacts = sorted(contact_stats.items(), key=lambda x: x[1]['total'], reverse=True)[:10]
        analysis['top_contacts'] = [
            {
                'username': username,
                'total_messages': stats['total'],
                'sent': stats['sent'],
                'received': stats['received'],
                'engagement_ratio': stats['sent'] / max(stats['received'], 1)
            }
            for username, stats in top_contacts
        ]

        self.analysis_data = analysis
        return analysis

    def generate_insights_report(self) -> str:
        """Generate comprehensive insights report"""
        print("\n📋 Generating insights report...")

        report = []
        data = self.analysis_data

        report.append("# Instagram DM Analysis Report")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Account**: {self.session_manager.username}")
        report.append("")

        # Overview
        report.append("## 📊 Overview")
        report.append(f"- **Total Conversations**: {data['total_conversations']}")
        report.append(f"- **Individual Chats**: {data['conversation_types']['individual']}")
        report.append(f"- **Group Chats**: {data['conversation_types']['group']}")
        report.append(f"- **Recent Activity** (7 days): {data['activity_patterns']['recent_activity']} conversations")
        report.append("")

        # Engagement Metrics
        report.append("## 💬 Engagement Metrics")
        report.append(f"- **Messages Sent**: {data['engagement_metrics']['messages_sent']}")
        report.append(f"- **Messages Received**: {data['engagement_metrics']['messages_received']}")
        report.append(f"- **Response Rate**: {data['engagement_metrics']['response_rate']:.1f}%")
        report.append(f"- **Avg Messages per Conversation**: {data['engagement_metrics']['avg_messages_per_conversation']:.1f}")
        report.append("")

        # Message Types
        report.append("## 📝 Message Types")
        for msg_type, count in data['message_types'].most_common(5):
            report.append(f"- **{msg_type}**: {count} messages")
        report.append("")

        # Time Patterns
        report.append("## ⏰ Activity Patterns")
        report.append("### Most Active Hours")
        hour_stats = data['time_patterns']['messages_by_hour']
        if hour_stats:
            sorted_hours = sorted(hour_stats.items(), key=lambda x: x[1], reverse=True)[:5]
            for hour, count in sorted_hours:
                report.append(f"- **{hour:02d}:00**: {count} messages")

        report.append("\n### Most Active Days")
        day_stats = data['time_patterns']['messages_by_day']
        if day_stats:
            sorted_days = sorted(day_stats.items(), key=lambda x: x[1], reverse=True)
            for day, count in sorted_days:
                report.append(f"- **{day}**: {count} messages")
        report.append("")

        # Top Contacts
        report.append("## 👥 Top Contacts")
        if data['top_contacts']:
            report.append("| Contact | Total Messages | Sent | Received | Engagement Ratio |")
            report.append("|---------|----------------|------|----------|------------------|")
            for contact in data['top_contacts'][:10]:
                report.append(f"| {contact['username']} | {contact['total_messages']} | {contact['sent']} | {contact['received']} | {contact['engagement_ratio']:.2f} |")
        report.append("")

        # Most Active Conversations
        report.append("## 🔥 Most Active Conversations")
        for i, conv in enumerate(data['activity_patterns']['most_active_conversations'][:5], 1):
            conv_type = "Group" if conv['is_group'] else "Individual"
            users = ', '.join([user['username'] for user in conv['users'][:3]])
            if len(conv['users']) > 3:
                users += f" (+{len(conv['users'])-3} more)"
            report.append(f"{i}. **{conv_type}**: {users} ({conv['message_count']} messages)")
        report.append("")

        # Insights and Recommendations
        report.append("## 💡 Insights & Recommendations")

        # Response rate insights
        response_rate = data['engagement_metrics']['response_rate']
        if response_rate > 80:
            report.append("- ✅ **High Engagement**: You're very responsive to messages")
        elif response_rate < 50:
            report.append("- ⚠️ **Low Response Rate**: Consider being more responsive to build better relationships")

        # Activity insights
        recent_activity = data['activity_patterns']['recent_activity']
        total_convs = data['total_conversations']
        if recent_activity / total_convs > 0.3:
            report.append("- 🔥 **High Activity**: You're actively engaging in conversations")

        # Group vs individual preference
        group_ratio = data['conversation_types']['group'] / total_convs
        if group_ratio > 0.3:
            report.append("- 👥 **Group Chat Active**: You participate in many group conversations")
        else:
            report.append("- 🤝 **One-on-One Focused**: You prefer individual conversations")

        report.append("")
        report.append("---")
        report.append("*Analysis completed safely using your own conversation data*")

        return '\n'.join(report)

    def save_analysis(self, filename: str = None) -> str:
        """Save analysis to file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/dm_analysis_{timestamp}.md"

        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        report = self.generate_insights_report()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)

        return str(filepath)

    def run_full_analysis(self, thread_limit: int = 50) -> bool:
        """Run complete DM analysis"""
        print("🚀 Starting Instagram DM Analysis")
        print("=" * 50)

        # Step 1: Connect
        if not self.connect():
            return False

        # Step 2: Extract data
        if not self.extract_dm_data(limit=thread_limit):
            return False

        # Step 3: Analyze patterns
        self.analyze_conversation_patterns()

        # Step 4: Generate and save report
        report_file = self.save_analysis()
        print(f"\n📄 Analysis report saved to: {report_file}")

        # Step 5: Display summary
        print("\n📊 ANALYSIS SUMMARY")
        print("=" * 30)
        data = self.analysis_data
        print(f"Total Conversations: {data['total_conversations']}")
        print(f"Messages Analyzed: {data['activity_patterns']['total_messages_analyzed']}")
        print(f"Response Rate: {data['engagement_metrics']['response_rate']:.1f}%")
        print(f"Recent Activity: {data['activity_patterns']['recent_activity']} conversations")

        if data['top_contacts']:
            print(f"Top Contact: {data['top_contacts'][0]['username']} ({data['top_contacts'][0]['total_messages']} messages)")

        return True

def main():
    """Main function"""
    analyzer = InstagramDMAnalyzer()

    print("📱 Instagram DM Analyzer")
    print("Analyzes your own Instagram conversations for insights")
    print("=" * 60)

    # Set default preferences for automation
    thread_limit = 20  # Reduced for initial testing

    # Run analysis
    success = analyzer.run_full_analysis(thread_limit=thread_limit)

    if success:
        print("\n🎉 Analysis completed successfully!")
        print("Check the generated report for detailed insights.")
    else:
        print("\n😞 Analysis failed. Please check your connection and try again.")

if __name__ == "__main__":
    main()