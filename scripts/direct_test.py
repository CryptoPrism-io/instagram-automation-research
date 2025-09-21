#!/usr/bin/env python3
"""
Direct Instagram Test - Attempt connection and story posting
"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_direct_connection():
    """Test direct Instagram connection"""
    try:
        from instagrapi import Client

        username = os.getenv('INSTAGRAM_USERNAME')
        password = os.getenv('INSTAGRAM_PASSWORD')

        print(f"🔐 Attempting direct login for: {username}")

        # Create client
        client = Client()
        client.delay_range = [1, 3]

        # Attempt login
        success = client.login(username, password)

        if success:
            print("✅ Login successful!")

            # Get account info
            user_info = client.account_info()
            print(f"👤 Logged in as: {user_info.username}")
            print(f"👥 Followers: {getattr(user_info, 'follower_count', 'N/A')}")
            print(f"📧 Email: {getattr(user_info, 'email', 'N/A')}")
            print(f"🆔 User ID: {client.user_id}")

            # Save session
            session_file = "data/instagram_session.json"
            client.dump_settings(session_file)
            print(f"💾 Session saved to: {session_file}")

            return client

        else:
            print("❌ Login failed")
            return None

    except Exception as e:
        print(f"💥 Error: {e}")
        return None

def post_test_story(client):
    """Post a test story"""
    try:
        print("\n📱 Preparing to post test story...")

        # Create a simple test image (we'll use a basic color image)
        from PIL import Image
        import tempfile

        # Create a simple test image
        img = Image.new('RGB', (1080, 1920), color='#1DA1F2')  # Twitter blue

        # Add some text-like appearance (basic)
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(img)

        # Try to use a basic font
        try:
            font = ImageFont.truetype("arial.ttf", 72)
        except:
            font = ImageFont.load_default()

        # Add text
        text = "Test Story\nCryptoPrism.io\nLive Test"
        draw.multiline_text((540, 960), text, fill='white', font=font, anchor="mm")

        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            img.save(f.name, 'JPEG', quality=95)
            temp_image = f.name

        print(f"📸 Test image created: {temp_image}")

        # Upload story
        story = client.photo_upload_to_story(temp_image)

        print(f"✅ Story posted successfully!")
        print(f"📱 Story ID: {story.pk}")

        # Clean up
        os.unlink(temp_image)

        return True

    except Exception as e:
        print(f"💥 Story posting error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Direct Instagram Test")
    print("=" * 40)

    # Test connection
    client = test_direct_connection()

    if client:
        # Test story posting
        post_test_story(client)

        print("\n✅ Test completed successfully!")
    else:
        print("\n❌ Test failed - could not establish connection")

if __name__ == "__main__":
    main()