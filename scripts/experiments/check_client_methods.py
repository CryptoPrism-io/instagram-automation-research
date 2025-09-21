#!/usr/bin/env python3
"""
Check Client Methods - See what unfollow methods are available
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.session_manager import InstagramSessionManager

def check_client_methods():
    """Check what methods are available on the client"""

    print("🔍 CHECKING CLIENT METHODS")
    print("=" * 40)

    try:
        session_manager = InstagramSessionManager()
        client = session_manager.get_client_bypass_validation()

        if client:
            print("✅ Client loaded successfully")

            # Look for unfollow methods
            methods = [method for method in dir(client) if 'unfollow' in method.lower()]
            print(f"\n📋 UNFOLLOW METHODS ({len(methods)}):")
            for method in methods:
                print(f"  - {method}")

            # Look for user methods
            user_methods = [method for method in dir(client) if method.startswith('user_') and 'unfollow' in method.lower()]
            print(f"\n👤 USER UNFOLLOW METHODS ({len(user_methods)}):")
            for method in user_methods:
                print(f"  - {method}")

            # Check if specific methods exist
            test_methods = [
                'user_unfollow',
                'user_unfollow_by_username',
                'unfollow',
                'friendship_destroy'
            ]

            print(f"\n🧪 TESTING SPECIFIC METHODS:")
            for method in test_methods:
                exists = hasattr(client, method)
                print(f"  {method}: {'✅' if exists else '❌'}")

        else:
            print("❌ No client available")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_client_methods()