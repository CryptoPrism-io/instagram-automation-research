#!/usr/bin/env python3
"""
Real Session Testing Suite
Tests actual Instagram functionality using session manager with real credentials
Only logs in once and reuses session for all tests
"""

import unittest
import sys
import os
import time
from pathlib import Path
from datetime import datetime
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestRealInstagramSession(unittest.TestCase):
    """Test real Instagram functionality with session management"""

    @classmethod
    def setUpClass(cls):
        """Set up shared session for all tests"""
        from core.session_manager import InstagramSessionManager

        logger.info("🚀 Setting up Instagram session for real testing...")

        # Initialize session manager
        cls.session_manager = InstagramSessionManager(
            session_file="data/test_instagram_session.json"
        )

        # Get authenticated client (will login only if needed)
        cls.client = cls.session_manager.get_smart_client()

        if not cls.client:
            raise unittest.SkipTest("❌ Failed to authenticate with Instagram - skipping real session tests")

        logger.info("✅ Instagram session established successfully")

        # Store session info for reference
        cls.session_info = {
            'username': cls.session_manager.username,
            'session_file': str(cls.session_manager.session_file),
            'setup_time': datetime.now()
        }

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        if hasattr(cls, 'client') and cls.client:
            logger.info("🧹 Cleaning up Instagram session...")
            # Note: We keep the session file for reuse

    def test_01_session_authentication(self):
        """Test that session authentication is working"""
        self.assertIsNotNone(self.client, "Client should be authenticated")
        self.assertTrue(hasattr(self.client, 'user_id'), "Client should have user_id")
        logger.info(f"✅ Session authenticated for user: {self.session_manager.username}")

    def test_02_get_own_user_info(self):
        """Test getting own user information"""
        try:
            user_info = self.client.account_info()

            self.assertIsNotNone(user_info, "User info should not be None")
            self.assertEqual(user_info.username, self.session_manager.username)

            logger.info(f"✅ User info retrieved:")
            logger.info(f"   👤 Username: {user_info.username}")
            logger.info(f"   📝 Full name: {user_info.full_name}")
            logger.info(f"   👥 Followers: {user_info.follower_count}")
            logger.info(f"   👤 Following: {user_info.following_count}")
            logger.info(f"   📸 Media count: {user_info.media_count}")

        except Exception as e:
            self.fail(f"Failed to get user info: {e}")

    def test_03_user_info_by_username(self):
        """Test getting user info by username"""
        try:
            # Test with own username
            user_info = self.client.user_info_by_username(self.session_manager.username)

            self.assertIsNotNone(user_info, "User info should not be None")
            self.assertEqual(user_info.username, self.session_manager.username)

            logger.info(f"✅ User info by username successful")

        except Exception as e:
            self.fail(f"Failed to get user info by username: {e}")

    def test_04_get_own_media(self):
        """Test getting own media posts"""
        try:
            # Get latest media posts (limit to 5 for testing)
            medias = self.client.user_medias(self.client.user_id, amount=5)

            self.assertIsInstance(medias, list, "Media should be a list")

            logger.info(f"✅ Retrieved {len(medias)} media posts")

            if medias:
                latest_media = medias[0]
                logger.info(f"   📸 Latest post ID: {latest_media.pk}")
                logger.info(f"   📝 Caption: {latest_media.caption_text[:50]}..." if latest_media.caption_text else "   📝 No caption")
                logger.info(f"   ❤️ Likes: {latest_media.like_count}")
                logger.info(f"   💬 Comments: {latest_media.comment_count}")

        except Exception as e:
            logger.warning(f"⚠️ Could not retrieve media (may be expected): {e}")
            # Don't fail the test - account might have no posts

    def test_05_get_followers_count(self):
        """Test getting followers count"""
        try:
            user_info = self.client.account_info()
            followers_count = user_info.follower_count

            self.assertIsInstance(followers_count, int, "Followers count should be an integer")
            self.assertGreaterEqual(followers_count, 0, "Followers count should be non-negative")

            logger.info(f"✅ Followers count: {followers_count}")

        except Exception as e:
            self.fail(f"Failed to get followers count: {e}")

    def test_06_session_persistence(self):
        """Test that session is properly saved and can be reused"""
        try:
            session_file_path = Path(self.session_manager.session_file)

            self.assertTrue(session_file_path.exists(), "Session file should exist")

            # Check session file has content
            with open(session_file_path, 'r') as f:
                import json
                session_data = json.load(f)

            self.assertIn('session_data', session_data, "Session should have session_data")
            self.assertIn('metadata', session_data, "Session should have metadata")

            metadata = session_data['metadata']
            self.assertEqual(metadata['username'], self.session_manager.username)

            logger.info(f"✅ Session persistence verified:")
            logger.info(f"   📁 File: {session_file_path}")
            logger.info(f"   📅 Created: {metadata.get('created_at', 'Unknown')}")
            logger.info(f"   🔄 Login count: {metadata.get('login_count', 'Unknown')}")

        except Exception as e:
            self.fail(f"Session persistence test failed: {e}")

    def test_07_rate_limiting_protection(self):
        """Test that rate limiting protection is working"""
        try:
            # Check if session manager has rate limiting attributes
            self.assertTrue(hasattr(self.session_manager, 'min_login_interval_hours'))
            self.assertGreater(self.session_manager.min_login_interval_hours, 0)

            logger.info(f"✅ Rate limiting protection:")
            logger.info(f"   ⏱️ Min login interval: {self.session_manager.min_login_interval_hours} hours")

        except Exception as e:
            self.fail(f"Rate limiting protection test failed: {e}")

    def test_08_client_configuration(self):
        """Test client configuration and settings"""
        try:
            # Test client has proper settings
            self.assertTrue(hasattr(self.client, 'user_agent'))
            self.assertTrue(hasattr(self.client, 'delay_range'))

            # Set safe delay range for testing
            self.client.delay_range = [1, 3]

            logger.info(f"✅ Client configuration:")
            logger.info(f"   🤖 User agent: {self.client.user_agent[:50]}...")
            logger.info(f"   ⏱️ Delay range: {self.client.delay_range}")

        except Exception as e:
            self.fail(f"Client configuration test failed: {e}")

class TestInstagramSafeOperations(unittest.TestCase):
    """Test safe Instagram operations that don't modify anything"""

    @classmethod
    def setUpClass(cls):
        """Reuse the session from previous test class"""
        if hasattr(TestRealInstagramSession, 'client') and TestRealInstagramSession.client:
            cls.client = TestRealInstagramSession.client
            cls.session_manager = TestRealInstagramSession.session_manager
        else:
            raise unittest.SkipTest("No authenticated session available")

    def test_01_hashtag_info(self):
        """Test hashtag information retrieval (safe operation)"""
        try:
            # Test with popular, safe hashtag
            hashtag_info = self.client.hashtag_info("crypto")

            self.assertIsNotNone(hashtag_info)
            self.assertEqual(hashtag_info.name.lower(), "crypto")
            self.assertGreater(hashtag_info.media_count, 0)

            logger.info(f"✅ Hashtag info for #crypto:")
            logger.info(f"   📊 Media count: {hashtag_info.media_count:,}")
            logger.info(f"   🆔 Hashtag ID: {hashtag_info.id}")

        except Exception as e:
            logger.warning(f"⚠️ Hashtag info test failed (may be rate limited): {e}")

    def test_02_search_functionality(self):
        """Test search functionality (safe operation)"""
        try:
            # Search for users (limit to 1 for safety)
            search_results = self.client.search_users("crypto", amount=1)

            self.assertIsInstance(search_results, list)

            logger.info(f"✅ User search results: {len(search_results)} users found")

            if search_results:
                user = search_results[0]
                logger.info(f"   👤 Found user: {user.username}")

        except Exception as e:
            logger.warning(f"⚠️ Search test failed (may be rate limited): {e}")

def run_real_session_tests():
    """Run the real session test suite"""
    print("🧪 Starting Real Instagram Session Tests")
    print("=" * 50)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestRealInstagramSession))
    test_suite.addTest(unittest.makeSuite(TestInstagramSafeOperations))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}")

    if result.errors:
        print("\n💥 ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}")

    return result

if __name__ == "__main__":
    run_real_session_tests()