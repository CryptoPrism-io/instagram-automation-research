#!/usr/bin/env python3
"""
Simple Instagram DM Analysis - Real Data Extraction
Extracts and analyzes your actual Instagram DMs safely
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def extract_real_dm_data():
    """Extract real DM data safely"""
    try:
        from core.session_manager import InstagramSessionManager

        print("🔐 Connecting to Instagram...")
        session_manager = InstagramSessionManager()
        client = session_manager.get_smart_client()

        if not client:
            print("❌ Failed to connect")
            return None

        user_info = client.account_info()
        print(f"✅ Connected as: {user_info.username}")

        print("\n📥 Extracting DM threads...")

        # Get basic thread info without detailed messages to avoid parsing issues
        try:
            # Get inbox threads
            response = client.private_request("direct_v2/inbox/", params={
                "visual_message_return_type": "unseen",
                "thread_message_limit": 5,  # Reduced to avoid parsing issues
                "persistentBadging": "true",
                "limit": 20,
                "is_prefetching": "false"
            })

            if 'inbox' not in response:
                print("❌ No inbox data found")
                return None

            inbox = response['inbox']
            threads = inbox.get('threads', [])

            print(f"📊 Found {len(threads)} conversation threads")

            conversations = []
            total_messages = 0

            for i, thread in enumerate(threads):
                print(f"   📝 Processing thread {i+1}/{len(threads)}")

                try:
                    # Extract basic thread info
                    thread_data = {
                        'thread_id': thread.get('thread_id', ''),
                        'thread_type': thread.get('thread_type', ''),
                        'is_group': thread.get('thread_type') == 'group',
                        'user_count': len(thread.get('users', [])),
                        'users': [],
                        'message_count': len(thread.get('items', [])),
                        'last_activity': thread.get('last_activity_at', 0),
                        'unread_count': thread.get('read_state', 0),
                        'messages': []
                    }

                    # Extract user info
                    for user in thread.get('users', []):
                        thread_data['users'].append({
                            'username': user.get('username', 'unknown'),
                            'user_id': user.get('pk', 0),
                            'full_name': user.get('full_name', '')
                        })

                    # Extract recent messages (basic info only)
                    for item in thread.get('items', [])[:10]:  # Limit to recent messages
                        try:
                            message = {
                                'user_id': item.get('user_id', 0),
                                'timestamp': item.get('timestamp', 0),
                                'item_type': item.get('item_type', 'unknown'),
                                'is_sent_by_me': item.get('user_id') == client.user_id,
                                'text': ''
                            }

                            # Extract text safely
                            if item.get('item_type') == 'text' and 'text' in item:
                                message['text'] = item['text'][:100]  # Truncate long messages

                            thread_data['messages'].append(message)

                        except Exception as e:
                            print(f"      ⚠️ Error processing message: {e}")
                            continue

                    conversations.append(thread_data)
                    total_messages += thread_data['message_count']

                    # Add delay between threads
                    time.sleep(0.5)

                except Exception as e:
                    print(f"   ⚠️ Error processing thread: {e}")
                    continue

            print(f"✅ Extracted {len(conversations)} conversations with {total_messages} total messages")

            return {
                'account': user_info.username,
                'user_id': client.user_id,
                'conversations': conversations,
                'extraction_time': datetime.now().isoformat(),
                'total_threads': len(conversations),
                'total_messages': total_messages
            }

        except Exception as e:
            print(f"💥 Error extracting threads: {e}")
            return None

    except Exception as e:
        print(f"💥 Connection error: {e}")
        return None

def analyze_dm_data(data):
    """Analyze extracted DM data"""
    if not data:
        return None

    print("\n🔍 Analyzing conversation patterns...")

    analysis = {
        'account_info': {
            'username': data['account'],
            'user_id': data['user_id'],
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        'overview': {
            'total_conversations': data['total_threads'],
            'total_messages': data['total_messages'],
            'individual_chats': 0,
            'group_chats': 0,
            'avg_messages_per_conversation': 0
        },
        'engagement': {
            'messages_sent': 0,
            'messages_received': 0,
            'response_ratio': 0
        },
        'activity_patterns': {
            'recent_conversations': 0,
            'active_conversations': 0
        },
        'top_contacts': [],
        'conversation_types': Counter(),
        'message_types': Counter()
    }

    # Analyze conversations
    contact_stats = defaultdict(lambda: {'sent': 0, 'received': 0, 'total': 0, 'name': ''})
    recent_cutoff = datetime.now() - timedelta(days=7)

    for conv in data['conversations']:
        # Count conversation types
        if conv['is_group']:
            analysis['overview']['group_chats'] += 1
        else:
            analysis['overview']['individual_chats'] += 1

        # Recent activity
        try:
            if conv['last_activity']:
                last_activity = datetime.fromtimestamp(conv['last_activity'] / 1000000)
                if last_activity > recent_cutoff:
                    analysis['activity_patterns']['recent_conversations'] += 1
        except:
            pass

        # Active conversations (have messages)
        if conv['message_count'] > 0:
            analysis['activity_patterns']['active_conversations'] += 1

        # Message analysis
        for msg in conv['messages']:
            analysis['message_types'][msg['item_type']] += 1

            if msg['is_sent_by_me']:
                analysis['engagement']['messages_sent'] += 1
            else:
                analysis['engagement']['messages_received'] += 1

            # Contact stats (for individual chats)
            if not conv['is_group'] and conv['users']:
                contact = conv['users'][0]
                username = contact['username']
                contact_stats[username]['name'] = contact.get('full_name', username)

                if msg['is_sent_by_me']:
                    contact_stats[username]['sent'] += 1
                else:
                    contact_stats[username]['received'] += 1
                contact_stats[username]['total'] += 1

    # Calculate metrics
    if data['total_threads'] > 0:
        analysis['overview']['avg_messages_per_conversation'] = data['total_messages'] / data['total_threads']

    if analysis['engagement']['messages_received'] > 0:
        analysis['engagement']['response_ratio'] = analysis['engagement']['messages_sent'] / analysis['engagement']['messages_received']

    # Top contacts
    top_contacts = sorted(contact_stats.items(), key=lambda x: x[1]['total'], reverse=True)[:10]
    analysis['top_contacts'] = [
        {
            'username': username,
            'name': stats['name'],
            'total_messages': stats['total'],
            'sent': stats['sent'],
            'received': stats['received'],
            'engagement_ratio': stats['sent'] / max(stats['received'], 1)
        }
        for username, stats in top_contacts if stats['total'] > 0
    ]

    return analysis

def generate_report(analysis):
    """Generate analysis report"""
    if not analysis:
        return "❌ No analysis data available"

    report = []
    report.append("# Real Instagram DM Analysis Report")
    report.append(f"**Account**: @{analysis['account_info']['username']}")
    report.append(f"**Generated**: {analysis['account_info']['analysis_date']}")
    report.append(f"**User ID**: {analysis['account_info']['user_id']}")
    report.append("")

    # Overview
    report.append("## 📊 Overview")
    report.append(f"- **Total Conversations**: {analysis['overview']['total_conversations']}")
    report.append(f"- **Individual Chats**: {analysis['overview']['individual_chats']}")
    report.append(f"- **Group Chats**: {analysis['overview']['group_chats']}")
    report.append(f"- **Total Messages**: {analysis['overview']['total_messages']}")
    report.append(f"- **Recent Activity** (7 days): {analysis['activity_patterns']['recent_conversations']} conversations")
    report.append("")

    # Engagement
    report.append("## 💬 Engagement Analysis")
    report.append(f"- **Messages Sent**: {analysis['engagement']['messages_sent']}")
    report.append(f"- **Messages Received**: {analysis['engagement']['messages_received']}")
    report.append(f"- **Response Ratio**: {analysis['engagement']['response_ratio']:.2f}")
    report.append(f"- **Avg Messages/Conversation**: {analysis['overview']['avg_messages_per_conversation']:.1f}")
    report.append("")

    # Message Types
    if analysis['message_types']:
        report.append("## 📝 Message Types")
        for msg_type, count in analysis['message_types'].most_common(5):
            report.append(f"- **{msg_type}**: {count} messages")
        report.append("")

    # Top Contacts
    if analysis['top_contacts']:
        report.append("## 👥 Top Contacts")
        report.append("| Contact | Name | Total | Sent | Received | Ratio |")
        report.append("|---------|------|-------|------|----------|-------|")
        for contact in analysis['top_contacts'][:10]:
            name = contact['name'][:20] if contact['name'] else contact['username']
            report.append(f"| @{contact['username']} | {name} | {contact['total_messages']} | {contact['sent']} | {contact['received']} | {contact['engagement_ratio']:.2f} |")
        report.append("")

    # Insights
    report.append("## 💡 Key Insights")

    if analysis['engagement']['response_ratio'] > 1:
        report.append("- ✅ **Proactive Communicator**: You send more messages than you receive")
    elif analysis['engagement']['response_ratio'] < 0.5:
        report.append("- 📥 **Popular Recipient**: You receive significantly more messages than you send")
    else:
        report.append("- ⚖️ **Balanced Communication**: Good balance between sending and receiving")

    group_ratio = analysis['overview']['group_chats'] / max(analysis['overview']['total_conversations'], 1)
    if group_ratio > 0.3:
        report.append("- 👥 **Group Chat Active**: You participate in many group conversations")
    else:
        report.append("- 🤝 **One-on-One Focused**: You prefer individual conversations")

    report.append("")
    report.append("---")
    report.append("*Analysis of real Instagram conversation data*")
    report.append("*Generated safely using your own account access*")

    return '\n'.join(report)

def main():
    """Main function"""
    print("📱 Real Instagram DM Analysis")
    print("=" * 50)

    # Extract real data
    data = extract_real_dm_data()

    if not data:
        print("😞 Failed to extract DM data")
        return

    # Analyze data
    analysis = analyze_dm_data(data)

    if not analysis:
        print("😞 Failed to analyze data")
        return

    # Generate report
    report = generate_report(analysis)

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save raw data
    data_file = Path(f"data/real_dm_data_{timestamp}.json")
    data_file.parent.mkdir(parents=True, exist_ok=True)
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)

    # Save analysis
    analysis_file = Path(f"data/real_dm_analysis_{timestamp}.json")
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, default=str)

    # Save report
    report_file = Path(f"data/real_dm_report_{timestamp}.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Analysis completed!")
    print(f"📊 Raw data: {data_file}")
    print(f"📈 Analysis: {analysis_file}")
    print(f"📄 Report: {report_file}")

    # Display summary
    print(f"\n🔍 REAL DM INSIGHTS:")
    print("=" * 30)
    print(f"👤 Account: @{analysis['account_info']['username']}")
    print(f"💬 Total Conversations: {analysis['overview']['total_conversations']}")
    print(f"📨 Messages Sent: {analysis['engagement']['messages_sent']}")
    print(f"📥 Messages Received: {analysis['engagement']['messages_received']}")
    print(f"🔄 Response Ratio: {analysis['engagement']['response_ratio']:.2f}")
    print(f"🔥 Recent Activity: {analysis['activity_patterns']['recent_conversations']} conversations")

    if analysis['top_contacts']:
        top_contact = analysis['top_contacts'][0]
        print(f"👥 Top Contact: @{top_contact['username']} ({top_contact['total_messages']} messages)")

    print(f"\n📋 Check {report_file} for detailed insights!")

if __name__ == "__main__":
    main()