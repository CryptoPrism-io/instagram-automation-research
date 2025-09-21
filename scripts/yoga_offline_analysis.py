#!/usr/bin/env python3
"""
Offline Analysis for @yoga_ss_ using existing DM data
Demonstrates data analysis capabilities without API connection
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter

def analyze_yoga_ss_from_dm_data():
    """Analyze @yoga_ss_ using existing DM conversation data"""

    print("📱 Offline Analysis: @yoga_ss_ (Yogesh Sahu)")
    print("Using existing DM conversation data")
    print("=" * 60)

    # Load existing DM data
    dm_file = Path("data/real_dm_data_20250920_235320.json")
    if not dm_file.exists():
        print("❌ No DM data file found")
        return None

    with open(dm_file, 'r') as f:
        dm_data = json.load(f)

    # Find conversation with yoga_ss_
    target_conversation = None
    for conv in dm_data['conversations']:
        for user in conv['users']:
            if user['username'] == 'yoga_ss_':
                target_conversation = conv
                break
        if target_conversation:
            break

    if not target_conversation:
        print("❌ No conversation found with @yoga_ss_")
        return None

    print("✅ Found DM conversation with @yoga_ss_")

    # Extract user data
    user_data = target_conversation['users'][0]

    # Analyze conversation
    analysis = {
        'profile': {
            'username': user_data['username'],
            'user_id': user_data['user_id'],
            'full_name': user_data['full_name'],
            'data_source': 'DM conversation'
        },
        'conversation': {
            'thread_id': target_conversation['thread_id'],
            'total_messages': target_conversation['message_count'],
            'last_activity': target_conversation['last_activity'],
            'message_breakdown': {
                'sent_by_me': 0,
                'received_from_friend': 0
            },
            'message_types': Counter()
        }
    }

    # Analyze messages
    for msg in target_conversation['messages']:
        if msg['is_sent_by_me']:
            analysis['conversation']['message_breakdown']['sent_by_me'] += 1
        else:
            analysis['conversation']['message_breakdown']['received_from_friend'] += 1

        analysis['conversation']['message_types'][msg['item_type']] += 1

    # Calculate last activity
    try:
        last_activity_timestamp = target_conversation['last_activity'] / 1000000
        last_activity_dt = datetime.fromtimestamp(last_activity_timestamp)
        analysis['conversation']['last_activity_formatted'] = last_activity_dt.strftime('%Y-%m-%d %H:%M:%S')
        analysis['conversation']['days_since_last_activity'] = (datetime.now() - last_activity_dt).days
    except:
        analysis['conversation']['last_activity_formatted'] = 'Unknown'
        analysis['conversation']['days_since_last_activity'] = None

    return analysis

def generate_yoga_report(analysis):
    """Generate analysis report for @yoga_ss_"""

    if not analysis:
        return "❌ No analysis data available"

    report = []
    report.append("# Offline Analysis: @yoga_ss_ (Yogesh Sahu)")
    report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Data Source**: Existing DM conversation data")
    report.append(f"**Analysis Type**: Offline data analysis")
    report.append("")

    # Profile Information
    profile = analysis['profile']
    report.append("## 👤 Profile Information")
    report.append(f"- **Username**: @{profile['username']}")
    report.append(f"- **Full Name**: {profile['full_name']}")
    report.append(f"- **User ID**: {profile['user_id']}")
    report.append(f"- **Data Source**: {profile['data_source']}")
    report.append("")

    # Conversation Analysis
    conv = analysis['conversation']
    report.append("## 💬 DM Conversation Analysis")
    report.append(f"- **Conversation Status**: ✅ Active")
    report.append(f"- **Thread ID**: {conv['thread_id']}")
    report.append(f"- **Total Messages**: {conv['total_messages']}")
    report.append(f"- **Messages from you**: {conv['message_breakdown']['sent_by_me']}")
    report.append(f"- **Messages from them**: {conv['message_breakdown']['received_from_friend']}")
    report.append(f"- **Last Activity**: {conv['last_activity_formatted']}")

    if conv['days_since_last_activity'] is not None:
        if conv['days_since_last_activity'] < 7:
            activity_status = "🔥 Very Recent"
        elif conv['days_since_last_activity'] < 30:
            activity_status = "📅 Recent"
        else:
            activity_status = "📆 Older"

        report.append(f"- **Activity Status**: {activity_status} ({conv['days_since_last_activity']} days ago)")

    # Message types
    if conv['message_types']:
        report.append("")
        report.append("### Message Types")
        for msg_type, count in conv['message_types'].most_common():
            report.append(f"- **{msg_type}**: {count} messages")

    report.append("")

    # Communication Analysis
    report.append("## 📊 Communication Analysis")

    total_messages = conv['message_breakdown']['sent_by_me'] + conv['message_breakdown']['received_from_friend']
    if total_messages > 0:
        sent_ratio = conv['message_breakdown']['sent_by_me'] / total_messages
        received_ratio = conv['message_breakdown']['received_from_friend'] / total_messages

        report.append(f"- **Communication Balance**:")
        report.append(f"  - You: {sent_ratio:.1%} ({conv['message_breakdown']['sent_by_me']} messages)")
        report.append(f"  - Them: {received_ratio:.1%} ({conv['message_breakdown']['received_from_friend']} messages)")

        if 0.4 <= sent_ratio <= 0.6:
            balance_status = "⚖️ Balanced"
        elif sent_ratio > 0.6:
            balance_status = "📤 You're more active"
        else:
            balance_status = "📥 They're more active"

        report.append(f"- **Balance Status**: {balance_status}")

    report.append("")

    # Key Insights
    report.append("## 💡 Key Insights")

    # Relationship evidence
    if total_messages > 0:
        if conv['message_breakdown']['sent_by_me'] > 0 and conv['message_breakdown']['received_from_friend'] > 0:
            report.append("- 🤝 **Mutual Communication**: Both parties actively participate in conversation")

        if conv['days_since_last_activity'] is not None:
            if conv['days_since_last_activity'] < 30:
                report.append("- 📱 **Recent Contact**: Active communication within the last month")

    # Message type insights
    most_common_type = conv['message_types'].most_common(1)
    if most_common_type:
        top_type, top_count = most_common_type[0]
        report.append(f"- 📝 **Primary Communication**: {top_type} messages ({top_count}/{total_messages})")

    report.append("")

    # Comparison with other contacts
    report.append("## 📈 Contact Ranking")
    report.append("Based on your DM analysis from earlier:")
    report.append("- **@rourkeheath**: 9 messages (Top contact)")
    report.append("- **@kanikaachaudhary**: 6 messages")
    report.append(f"- **@yoga_ss_**: {total_messages} messages")

    # Determine ranking
    if total_messages >= 9:
        rank_status = "🥇 Top contact"
    elif total_messages >= 6:
        rank_status = "🥈 High-priority contact"
    else:
        rank_status = "📱 Regular contact"

    report.append(f"- **Ranking**: {rank_status}")

    report.append("")
    report.append("## 🔒 Analysis Method")
    report.append("- **Data Source**: Previously extracted DM conversation data")
    report.append("- **Privacy Compliant**: No new API calls or data extraction")
    report.append("- **Scope**: Limited to conversation history and metadata")
    report.append("- **Advantage**: Works even when API access is restricted")

    report.append("")
    report.append("---")
    report.append("*Offline analysis using existing conversation data*")
    report.append("*Demonstrates data analysis capabilities without live API connection*")

    return '\n'.join(report)

def main():
    """Main function"""

    # Analyze yoga_ss_ data
    analysis = analyze_yoga_ss_from_dm_data()

    if not analysis:
        print("😞 Analysis failed - no data available")
        return

    # Generate report
    report = generate_yoga_report(analysis)

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Save analysis data
    data_file = Path(f"data/yoga_offline_analysis_{timestamp}.json")
    data_file.parent.mkdir(parents=True, exist_ok=True)
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, default=str)

    # Save report
    report_file = Path(f"data/yoga_offline_report_{timestamp}.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n✅ Offline analysis completed!")
    print(f"📊 Analysis data: {data_file}")
    print(f"📄 Report: {report_file}")

    # Display key findings
    conv = analysis['conversation']
    print(f"\n🔍 KEY FINDINGS - @yoga_ss_:")
    print("=" * 40)
    print(f"👤 Full Name: {analysis['profile']['full_name']}")
    print(f"🆔 User ID: {analysis['profile']['user_id']}")
    print(f"💬 Total Messages: {conv['total_messages']}")
    print(f"📤 Sent by you: {conv['message_breakdown']['sent_by_me']}")
    print(f"📥 Received: {conv['message_breakdown']['received_from_friend']}")
    print(f"📅 Last Activity: {conv['last_activity_formatted']}")

    if conv['days_since_last_activity'] is not None:
        print(f"⏰ Days ago: {conv['days_since_last_activity']}")

    # Most common message type
    if conv['message_types']:
        top_type = conv['message_types'].most_common(1)[0]
        print(f"📝 Main message type: {top_type[0]} ({top_type[1]} messages)")

if __name__ == "__main__":
    main()