#!/usr/bin/env python3
"""
Check 200 Response - Test if session gives proper HTTP responses
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

def check_200_response():
    """Check if we're getting proper 200 responses"""

    print("🔍 CHECKING 200 RESPONSE STATUS")
    print("=" * 40)

    try:
        # Get session
        session_manager = InstagramSessionManager()
        client = session_manager.get_client_bypass_validation()

        if not client:
            print("❌ No client")
            return False

        print(f"✅ Session loaded - User ID: {client.user_id}")

        # Test simple API call
        print(f"\n🧪 Testing API response...")

        try:
            # Try a simple request and check response
            my_user_id = client.user_id
            params = {"count": 1}

            print(f"📡 Making request to following endpoint...")
            response = client.private_request(f"friendships/{my_user_id}/following/", params=params)

            # Check response
            print(f"✅ Response received!")
            print(f"📊 Response type: {type(response)}")
            print(f"📋 Response keys: {list(response.keys()) if isinstance(response, dict) else 'Not a dict'}")

            if 'users' in response:
                users = response['users']
                print(f"👥 Users found: {len(users)}")
                print(f"🎯 GETTING PROPER 200 RESPONSE!")
                return True
            else:
                print(f"⚠️ No 'users' in response")
                print(f"📄 Full response: {response}")
                return False

        except Exception as e:
            error_msg = str(e)
            print(f"❌ API Error: {error_msg}")

            if "wait" in error_msg.lower():
                print("⏳ Rate limited (but session working)")
                return "rate_limited"
            else:
                print("💥 Other error")
                return False

    except Exception as e:
        print(f"❌ Session error: {e}")
        return False

if __name__ == "__main__":
    result = check_200_response()

    if result == True:
        print("\n🎉 SUCCESS: Getting proper 200 responses!")
    elif result == "rate_limited":
        print("\n⏳ RATE LIMITED: Session working, just need to wait")
    else:
        print("\n❌ ISSUES: Not getting proper responses")