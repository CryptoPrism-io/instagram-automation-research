#!/usr/bin/env python3
"""
Create Instagram Session Script
Creates and validates Instagram session for testing
"""

import sys
import os
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_instagram_session():
    """Create and validate Instagram session"""
    try:
        from core.session_manager import InstagramSessionManager

        print("🚀 Creating Instagram session...")
        print("=" * 50)

        # Initialize session manager
        session_manager = InstagramSessionManager(
            session_file="data/instagram_session.json"
        )

        print(f"👤 Username: {session_manager.username}")
        print(f"📁 Session file: {session_manager.session_file}")

        # Attempt to get client (will create session if needed)
        print("\n🔐 Authenticating with Instagram...")
        client = session_manager.get_smart_client()

        if client:
            print("✅ Session created successfully!")

            # Test the session with basic info
            print("\n📋 Testing session...")
            try:
                user_info = client.account_info()
                print(f"   👤 Username: {user_info.username}")
                print(f"   📝 Full name: {user_info.full_name}")
                print(f"   👥 Followers: {user_info.follower_count}")
                print(f"   📸 Posts: {user_info.media_count}")

                print("\n✅ Session validation successful!")
                print(f"📁 Session saved to: {session_manager.session_file}")

                return True

            except Exception as e:
                print(f"⚠️ Session created but validation failed: {e}")
                return False

        else:
            print("❌ Failed to create session")
            print("Please check your credentials and try again")
            return False

    except Exception as e:
        print(f"💥 Error creating session: {e}")
        return False

def check_session_status():
    """Check current session status"""
    try:
        from core.session_manager import InstagramSessionManager

        print("🔍 Checking session status...")
        print("=" * 50)

        session_manager = InstagramSessionManager()
        session_file = Path(session_manager.session_file)

        if session_file.exists():
            print(f"✅ Session file exists: {session_file}")

            # Try to load and validate
            client = session_manager.get_smart_client()

            if client:
                print("✅ Session is valid and working")

                try:
                    user_info = client.account_info()
                    print(f"   👤 Authenticated as: {user_info.username}")
                    print(f"   👥 Followers: {user_info.follower_count}")
                except Exception as e:
                    print(f"⚠️ Session loaded but API test failed: {e}")

                return True
            else:
                print("❌ Session file exists but is invalid")
                return False
        else:
            print("❌ No session file found")
            return False

    except Exception as e:
        print(f"💥 Error checking session: {e}")
        return False

def main():
    """Main function"""
    print("📱 Instagram Session Manager")
    print("=" * 50)

    # Check if session already exists
    if check_session_status():
        print("\n🎉 Existing session is working!")
        print("No need to create a new session.")

        response = input("\nDo you want to create a new session anyway? (y/N): ")
        if response.lower() != 'y':
            print("👋 Keeping existing session. Goodbye!")
            return

    # Create new session
    print("\n🔨 Creating new session...")
    success = create_instagram_session()

    if success:
        print("\n🎉 Session setup complete!")
        print("You can now run tests with:")
        print("  python tests/test_real_session.py")
    else:
        print("\n😞 Session setup failed")
        print("Please check your credentials in .env file")

if __name__ == "__main__":
    main()