#!/usr/bin/env python3
"""
Direct Unfollow Script - Using existing session directly
Bypasses session manager to use existing session file
"""

import sys
import os
from pathlib import Path
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from instagrapi import Client

def load_session_directly():
    """Load session directly from file"""
    try:
        session_file = Path("instagram_session.json")
        if not session_file.exists():
            print("❌ Session file not found")
            return None

        with open(session_file, 'r') as f:
            session_data = json.load(f)

        client = Client()

        # Load session data directly
        if 'session_data' in session_data:
            session = session_data['session_data']

            # Set basic client properties
            client.user_id = session['authorization_data']['ds_user_id']
            client.username = session_data['metadata']['username']

            # Set device info
            client.set_device(session['device_settings'])

            # Set session cookies/headers
            client.authorization_data = session['authorization_data']

            print(f"✅ Session loaded for @{client.username}")
            return client

    except Exception as e:
        print(f"❌ Failed to load session: {e}")
        return None

    return None

def direct_unfollow_all():
    """Direct unfollow using session file"""

    print("🚀 DIRECT UNFOLLOW - USING EXISTING SESSION")
    print("=" * 60)

    # Load the backup list to see who we need to unfollow
    backup_file = Path("data/BACKUP_following_list_before_unfollow.json")
    if not backup_file.exists():
        print("❌ Backup file not found")
        return False

    with open(backup_file, 'r') as f:
        backup_data = json.load(f)

    following_users = backup_data['following_users']
    total = len(following_users)

    print(f"📋 Found {total} users to unfollow from backup")

    # Try to get a working client
    client = load_session_directly()
    if not client:
        print("❌ Could not establish session")
        return False

    print(f"✅ Session active - User: @{client.username}")

    # Start unfollowing process
    unfollowed = []
    failed = []

    print(f"\n🚀 Starting unfollow process...")
    print("=" * 60)

    for i, user in enumerate(following_users, 1):
        username = user.get('username')

        print(f"{i:3d}/{total} Unfollowing @{username}...", end=" ")

        try:
            # Try to unfollow by username
            result = client.user_unfollow_by_username(username)

            if result:
                print("✅")
                unfollowed.append(username)
            else:
                print("❌")
                failed.append(username)

        except Exception as e:
            print(f"❌ {str(e)[:50]}")
            failed.append(username)

            if "wait" in str(e).lower() or "limit" in str(e).lower():
                print("     ⏳ Rate limited - sleeping 30s...")
                time.sleep(30)

        # Rate limiting between requests
        time.sleep(2)

        # Progress update every 10 users
        if i % 10 == 0:
            print(f"     📊 Progress: {len(unfollowed)} unfollowed, {len(failed)} failed")

    # Summary
    print(f"\n🎯 UNFOLLOW COMPLETE")
    print("=" * 40)
    print(f"✅ Unfollowed: {len(unfollowed)}/{total}")
    print(f"❌ Failed: {len(failed)}/{total}")

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    results = {
        'operation': 'direct_unfollow_all',
        'total_before': total,
        'unfollowed_count': len(unfollowed),
        'failed_count': len(failed),
        'unfollowed_users': unfollowed,
        'failed_users': failed,
        'completed_at': datetime.now().isoformat()
    }

    results_file = Path(f"data/direct_unfollow_results_{timestamp}.json")
    results_file.parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Results saved: {results_file}")

    if len(unfollowed) > 0:
        print(f"\n✅ SUCCESSFULLY UNFOLLOWED ({len(unfollowed)}):")
        for username in unfollowed:
            print(f"   @{username}")

    if len(failed) > 0:
        print(f"\n❌ FAILED TO UNFOLLOW ({len(failed)}):")
        for username in failed:
            print(f"   @{username}")

    return len(failed) == 0

if __name__ == "__main__":
    print("🔥 DIRECT UNFOLLOW - Starting in 3 seconds...")
    print("Press Ctrl+C to cancel...")

    for i in range(3, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)

    print("Starting direct unfollow process...     ")
    success = direct_unfollow_all()

    if success:
        print("\n🎉 OPERATION COMPLETED SUCCESSFULLY!")
    else:
        print("\n⚠️ Operation completed with some issues.")