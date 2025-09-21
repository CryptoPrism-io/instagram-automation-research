#!/usr/bin/env python3
"""
Test Follower Activity Analysis
Direct test without user input
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import the analyzer
from follower_activity_analyzer import FollowerActivityAnalyzer

def test_yoga_followers_activity():
    """Test activity analysis for yoga_ss_ followers"""

    print("🧪 Testing Follower Activity Analysis")
    print("Target: @yoga_ss_")
    print("Max followers: 10")
    print("=" * 50)

    analyzer = FollowerActivityAnalyzer()
    result = analyzer.analyze_followers_activity("yoga_ss_", max_followers=10)

    if result:
        print("\n✅ Test completed successfully!")
        return True
    else:
        print("\n❌ Test failed")
        return False

if __name__ == "__main__":
    test_yoga_followers_activity()