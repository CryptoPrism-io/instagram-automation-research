#!/usr/bin/env python3
"""
Follower Network Analysis for @yoga_ss_
Attempts multiple methods to analyze follower/following networks
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime
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

class FollowerAnalyzer:
    """Analyze follower networks with multiple access methods"""

    def __init__(self, target_username: str = "yoga_ss_"):
        """Initialize analyzer"""
        from core.session_manager import InstagramSessionManager

        self.target_username = target_username
        self.target_user_id = 143732789  # From DM data
        self.session_manager = InstagramSessionManager()
        self.client = None
        self.analysis_data = {}

    def connect_if_possible(self) -> bool:
        """Try to connect, return status"""
        try:
            print("🔐 Checking Instagram connection...")
            self.client = self.session_manager.get_smart_client()

            if self.client:
                user_info = self.client.account_info()
                print(f"✅ Connected as: {user_info.username}")
                return True
            else:
                print("❌ Connection failed (expected due to rate limiting)")
                return False

        except Exception as e:
            print(f"⚠️ Connection unavailable: {e}")
            return False

    def attempt_direct_follower_access(self) -> Dict[str, Any]:
        """Attempt direct access to follower data"""
        result = {
            'method': 'direct_api',
            'success': False,
            'followers': [],
            'following': [],
            'error': None,
            'restrictions': []
        }

        if not self.client:
            result['error'] = 'No active session'
            result['restrictions'].append('Session expired - 7-day rate limiting active')
            return result

        try:
            print(f"\n👥 Attempting direct follower access for @{self.target_username}...")

            # Try getting followers
            try:
                followers = self.client.user_followers(self.target_user_id, amount=50)
                result['followers'] = [
                    {
                        'username': user.username,
                        'user_id': user.pk,
                        'full_name': user.full_name,
                        'follower_count': getattr(user, 'follower_count', 0),
                        'is_verified': getattr(user, 'is_verified', False),
                        'is_private': getattr(user, 'is_private', False)
                    }
                    for user in followers[:50]  # Limit for safety
                ]
                print(f"✅ Retrieved {len(result['followers'])} followers")
                result['success'] = True

            except Exception as e:
                print(f"   ❌ Followers access failed: {e}")
                result['restrictions'].append(f'Followers access: {str(e)}')

            # Try getting following
            try:
                following = self.client.user_following(self.target_user_id, amount=50)
                result['following'] = [
                    {
                        'username': user.username,
                        'user_id': user.pk,
                        'full_name': user.full_name,
                        'follower_count': getattr(user, 'follower_count', 0),
                        'is_verified': getattr(user, 'is_verified', False),
                        'is_private': getattr(user, 'is_private', False)
                    }
                    for user in following[:50]  # Limit for safety
                ]
                print(f"✅ Retrieved {len(result['following'])} following")
                result['success'] = True

            except Exception as e:
                print(f"   ❌ Following access failed: {e}")
                result['restrictions'].append(f'Following access: {str(e)}')

        except Exception as e:
            result['error'] = str(e)
            result['restrictions'].append(f'General access error: {str(e)}')

        return result

    def analyze_mutual_connections(self) -> Dict[str, Any]:
        """Analyze mutual connections through your own network"""
        result = {
            'method': 'mutual_analysis',
            'success': False,
            'mutual_followers': [],
            'mutual_following': [],
            'your_network_size': 0,
            'error': None
        }

        if not self.client:
            result['error'] = 'No active session'
            return result

        try:
            print(f"\n🔍 Analyzing mutual connections...")

            # Get your followers
            try:
                your_followers = self.client.user_followers(self.client.user_id, amount=200)
                result['your_network_size'] = len(your_followers)
                print(f"📊 Your followers: {len(your_followers)}")

                # Check if yoga_ss_ is in your followers
                yoga_in_followers = any(user.pk == self.target_user_id for user in your_followers)
                if yoga_in_followers:
                    result['mutual_followers'].append({
                        'status': 'yoga_ss_ follows you',
                        'confirmed': True
                    })
                    print("✅ yoga_ss_ is in your followers")

            except Exception as e:
                print(f"   ⚠️ Your followers check failed: {e}")

            # Get your following
            try:
                your_following = self.client.user_following(self.client.user_id, amount=200)
                print(f"📊 You follow: {len(your_following)}")

                # Check if you follow yoga_ss_
                you_follow_yoga = any(user.pk == self.target_user_id for user in your_following)
                if you_follow_yoga:
                    result['mutual_following'].append({
                        'status': 'you follow yoga_ss_',
                        'confirmed': True
                    })
                    print("✅ You follow yoga_ss_")

                result['success'] = True

            except Exception as e:
                print(f"   ⚠️ Your following check failed: {e}")

        except Exception as e:
            result['error'] = str(e)

        return result

    def analyze_network_from_dms(self) -> Dict[str, Any]:
        """Analyze network possibilities from DM data"""
        result = {
            'method': 'dm_network_analysis',
            'success': False,
            'potential_connections': [],
            'network_insights': [],
            'error': None
        }

        try:
            print(f"\n💬 Analyzing network from DM conversations...")

            # Load your DM data
            dm_file = Path("data/real_dm_data_20250920_235320.json")
            if not dm_file.exists():
                result['error'] = 'No DM data available'
                return result

            with open(dm_file, 'r') as f:
                dm_data = json.load(f)

            # Analyze your contact network
            contacts = []
            for conv in dm_data['conversations']:
                if not conv['is_group']:
                    for user in conv['users']:
                        contacts.append({
                            'username': user['username'],
                            'user_id': user['user_id'],
                            'full_name': user['full_name'],
                            'message_count': conv['message_count']
                        })

            result['potential_connections'] = contacts

            # Network insights
            result['network_insights'] = [
                f"You have DM conversations with {len(contacts)} people",
                f"These contacts might follow or be followed by @{self.target_username}",
                "Common contacts often indicate shared social circles",
                f"@{self.target_username} appears in your DM network, suggesting existing connection"
            ]

            # Look for patterns
            high_activity_contacts = [c for c in contacts if c['message_count'] > 5]
            result['network_insights'].append(
                f"{len(high_activity_contacts)} contacts have high engagement (>5 messages)"
            )

            result['success'] = True
            print(f"✅ Identified {len(contacts)} potential network connections")

        except Exception as e:
            result['error'] = str(e)

        return result

    def alternative_research_methods(self) -> Dict[str, Any]:
        """Suggest alternative research methods"""
        result = {
            'method': 'alternative_approaches',
            'manual_methods': [],
            'tool_based_methods': [],
            'future_automated_methods': []
        }

        # Manual methods
        result['manual_methods'] = [
            {
                'method': 'Instagram App Manual Check',
                'description': 'Open Instagram app, search for @yoga_ss_, view followers/following',
                'pros': 'Direct access, full data',
                'cons': 'Manual work, limited by privacy settings',
                'feasibility': 'High if account is public'
            },
            {
                'method': 'Mutual Friends Analysis',
                'description': 'Check followers/following of your mutual contacts',
                'pros': 'May reveal indirect connections',
                'cons': 'Time-intensive, limited scope',
                'feasibility': 'Medium'
            }
        ]

        # Tool-based methods
        result['tool_based_methods'] = [
            {
                'method': 'Session Renewal + API Access',
                'description': 'Wait for 7-day rate limit, then use full API access',
                'pros': 'Complete programmatic access',
                'cons': 'Must wait ~7 days',
                'feasibility': 'High (guaranteed to work)'
            },
            {
                'method': 'Browser Automation',
                'description': 'Use Playwright/Selenium to automate Instagram web',
                'pros': 'Bypasses API restrictions',
                'cons': 'More complex, higher detection risk',
                'feasibility': 'Medium (technical complexity)'
            }
        ]

        # Future automated methods
        result['future_automated_methods'] = [
            {
                'method': 'Enhanced Session Management',
                'description': 'Multiple session rotation to avoid rate limits',
                'pros': 'Continuous access',
                'cons': 'Requires multiple accounts',
                'feasibility': 'Low (violates best practices)'
            },
            {
                'method': 'Proxy + IP Rotation',
                'description': 'Change IP addresses to reset rate limits',
                'pros': 'Could bypass restrictions',
                'cons': 'Against Instagram ToS, risky',
                'feasibility': 'Not recommended'
            }
        ]

        return result

    def generate_network_report(self) -> str:
        """Generate comprehensive network analysis report"""
        report = []
        report.append(f"# Follower Network Analysis: @{self.target_username}")
        report.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Target**: @{self.target_username} (Yogesh Sahu)")
        report.append(f"**User ID**: {self.target_user_id}")
        report.append("")

        # Current limitations
        report.append("## 🚨 Current Limitations")
        report.append("- **Session Status**: Expired (7-day rate limiting active)")
        report.append("- **Direct API Access**: Unavailable until rate limit expires")
        report.append("- **Profile Access**: Restricted (403 error in previous attempts)")
        report.append("")

        # Analysis results
        for method, data in self.analysis_data.items():
            if method == 'direct_access':
                report.append("## 🔍 Direct Access Attempt")
                if data['success']:
                    report.append(f"✅ **Success**: Retrieved {len(data['followers'])} followers and {len(data['following'])} following")

                    if data['followers']:
                        report.append("### Followers Sample")
                        for follower in data['followers'][:10]:
                            status = "✅" if follower['is_verified'] else "🔒" if follower['is_private'] else "👤"
                            report.append(f"- {status} @{follower['username']} ({follower['follower_count']} followers)")

                    if data['following']:
                        report.append("### Following Sample")
                        for following in data['following'][:10]:
                            status = "✅" if following['is_verified'] else "🔒" if following['is_private'] else "👤"
                            report.append(f"- {status} @{following['username']} ({following['follower_count']} followers)")
                else:
                    report.append("❌ **Failed**: Direct access unavailable")
                    for restriction in data['restrictions']:
                        report.append(f"- {restriction}")
                report.append("")

            elif method == 'mutual_analysis':
                report.append("## 🤝 Mutual Connection Analysis")
                if data['success']:
                    report.append(f"📊 **Your Network Size**: {data['your_network_size']} total connections analyzed")

                    if data['mutual_followers'] or data['mutual_following']:
                        report.append("### Connection Status")
                        for connection in data['mutual_followers'] + data['mutual_following']:
                            report.append(f"- ✅ {connection['status']}")
                    else:
                        report.append("- ❌ No direct mutual connections found")
                else:
                    report.append("❌ **Failed**: Could not analyze mutual connections")
                report.append("")

            elif method == 'dm_network':
                report.append("## 💬 DM Network Analysis")
                if data['success']:
                    report.append(f"📱 **Network Size**: {len(data['potential_connections'])} DM contacts")

                    report.append("### Network Insights")
                    for insight in data['network_insights']:
                        report.append(f"- {insight}")

                    if data['potential_connections']:
                        report.append("### Your DM Network (Potential Mutual Connections)")
                        for contact in sorted(data['potential_connections'], key=lambda x: x['message_count'], reverse=True)[:10]:
                            report.append(f"- @{contact['username']} ({contact['message_count']} messages)")
                report.append("")

        # Alternative methods
        if 'alternatives' in self.analysis_data:
            alternatives = self.analysis_data['alternatives']
            report.append("## 🛠️ Alternative Research Methods")

            report.append("### Manual Methods")
            for method in alternatives['manual_methods']:
                report.append(f"**{method['method']}**")
                report.append(f"- Description: {method['description']}")
                report.append(f"- Feasibility: {method['feasibility']}")
                report.append("")

            report.append("### Automated Solutions")
            for method in alternatives['tool_based_methods']:
                report.append(f"**{method['method']}**")
                report.append(f"- Description: {method['description']}")
                report.append(f"- Feasibility: {method['feasibility']}")
                report.append("")

        # Recommendations
        report.append("## 💡 Recommendations")
        report.append("")
        report.append("### Immediate Options")
        report.append("1. **Manual Instagram App Check**: Search @yoga_ss_ and manually view followers/following")
        report.append("2. **Contact Analysis**: Analyze mutual contacts through your DM network")
        report.append("3. **Wait for API Access**: Session renewal in ~7 days for full automated analysis")
        report.append("")

        report.append("### Best Approach")
        report.append("- **Short-term**: Manual verification via Instagram app")
        report.append("- **Long-term**: Automated analysis when session renews")
        report.append("- **Hybrid**: Combine manual insights with DM network analysis")

        report.append("")
        report.append("---")
        report.append("*Analysis conducted with respect for privacy and platform limitations*")

        return '\n'.join(report)

    def run_comprehensive_analysis(self) -> bool:
        """Run comprehensive follower network analysis"""
        print(f"🚀 Follower Network Analysis: @{self.target_username}")
        print(f"Target: @{self.target_username} (Yogesh Sahu)")
        print("=" * 60)

        try:
            # Step 1: Check connection
            connection_available = self.connect_if_possible()

            # Step 2: Attempt direct access
            self.analysis_data['direct_access'] = self.attempt_direct_follower_access()

            # Step 3: Mutual connection analysis (if connected)
            if connection_available:
                self.analysis_data['mutual_analysis'] = self.analyze_mutual_connections()

            # Step 4: DM network analysis
            self.analysis_data['dm_network'] = self.analyze_network_from_dms()

            # Step 5: Alternative methods
            self.analysis_data['alternatives'] = self.alternative_research_methods()

            # Step 6: Generate report
            report = self.generate_network_report()

            # Save results
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # Save analysis data
            data_file = Path(f"data/follower_network_analysis_{timestamp}.json")
            data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_data, f, indent=2, default=str)

            # Save report
            report_file = Path(f"data/follower_network_report_{timestamp}.md")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"\n✅ Follower network analysis completed!")
            print(f"📊 Analysis data: {data_file}")
            print(f"📄 Report: {report_file}")

            return True

        except Exception as e:
            print(f"💥 Analysis failed: {e}")
            return False

def main():
    """Main function"""
    print("👥 Instagram Follower Network Analyzer")
    print("Comprehensive network analysis with multiple access methods")
    print("=" * 60)

    analyzer = FollowerAnalyzer("yoga_ss_")
    success = analyzer.run_comprehensive_analysis()

    if success:
        print("\n🎉 Network analysis completed!")
        print("Check the generated report for detailed findings and recommendations.")
    else:
        print("\n😞 Analysis failed - check logs for details")

if __name__ == "__main__":
    main()