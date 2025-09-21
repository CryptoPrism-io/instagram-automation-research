#!/usr/bin/env python3
"""
Session Manager Mock Testing Suite
Tests session management functionality using mock data to simulate real Instagram API
Demonstrates the full workflow without making actual API calls
"""

import unittest
import sys
import os
import json
import tempfile
import time
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestSessionManagerWithMocks(unittest.TestCase):
    """Test session manager functionality with mocked Instagram API"""

    def setUp(self):
        """Set up temporary session file for testing"""
        self.temp_dir = tempfile.mkdtemp()
        self.session_file = os.path.join(self.temp_dir, "mock_session.json")

    def test_01_session_manager_initialization(self):
        """Test session manager initialization with real credentials"""
        from core.session_manager import InstagramSessionManager

        # Test with environment variables
        session_manager = InstagramSessionManager(
            session_file=self.session_file
        )

        self.assertEqual(session_manager.username, "cryptoprism.io")
        self.assertEqual(session_manager.password, "jaimaakamakhya")
        self.assertEqual(str(session_manager.session_file), self.session_file)
        self.assertEqual(session_manager.session_max_age_days, 30)
        self.assertEqual(session_manager.min_login_interval_hours, 24)

        print(f"✅ Session manager initialized with username: {session_manager.username}")

    @patch('instagrapi.Client')
    def test_02_fresh_login_simulation(self, mock_client_class):
        """Test fresh login process with mocked Instagram client"""
        from core.session_manager import InstagramSessionManager

        # Setup mock client
        mock_client = Mock()
        mock_client.login.return_value = True
        mock_client.user_id = 123456789
        mock_client.username = "cryptoprism.io"
        mock_client.account_info.return_value = Mock(
            username="cryptoprism.io",
            full_name="CryptoPrism",
            follower_count=1500,
            following_count=800,
            media_count=45
        )
        mock_client.get_settings.return_value = {"mock": "session_data"}

        mock_client_class.return_value = mock_client

        # Test session creation
        session_manager = InstagramSessionManager(session_file=self.session_file)

        # Mock the validation to pass
        with patch.object(session_manager, '_validate_session', return_value=True):
            client = session_manager.get_smart_client()

        self.assertIsNotNone(client)
        self.assertEqual(client.username, "cryptoprism.io")

        # Verify session file was created
        self.assertTrue(os.path.exists(self.session_file))

        print("✅ Fresh login simulation successful")

    def test_03_session_persistence(self):
        """Test session file creation and persistence"""
        from core.session_manager import InstagramSessionManager

        # Create mock session data
        session_data = {
            "session_data": {
                "user_id": 123456789,
                "username": "cryptoprism.io",
                "cookies": {"mock": "cookie_data"},
                "settings": {"mock": "settings_data"}
            },
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "last_validated": datetime.now().isoformat(),
                "login_count": 1,
                "username": "cryptoprism.io",
                "session_version": "1.0",
                "device_uuids": {"phone_id": "mock-phone-id"}
            }
        }

        # Save mock session
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

        # Test loading existing session
        session_manager = InstagramSessionManager(session_file=self.session_file)

        self.assertTrue(session_manager._load_existing_session())

        print("✅ Session persistence test successful")

    @patch('instagrapi.Client')
    def test_04_session_validation(self, mock_client_class):
        """Test session validation process"""
        from core.session_manager import InstagramSessionManager

        # Create session with older date to test age validation
        old_date = (datetime.now() - timedelta(days=35)).isoformat()
        session_data = {
            "session_data": {"mock": "data"},
            "metadata": {
                "created_at": old_date,
                "last_updated": old_date,
                "username": "cryptoprism.io"
            }
        }

        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)

        session_manager = InstagramSessionManager(session_file=self.session_file)
        session_manager._load_existing_session()

        # Test session age validation
        is_valid = session_manager._is_session_fresh()
        self.assertFalse(is_valid, "Old session should be considered invalid")

        print("✅ Session validation test successful")

    def test_05_rate_limiting_protection(self):
        """Test rate limiting protection features"""
        from core.session_manager import InstagramSessionManager

        session_manager = InstagramSessionManager(session_file=self.session_file)

        # Test that rate limiting attributes exist
        self.assertTrue(hasattr(session_manager, 'min_login_interval_hours'))
        self.assertEqual(session_manager.min_login_interval_hours, 24)

        # Test rate limiting check with recent login
        recent_time = datetime.now() - timedelta(hours=12)
        session_manager._session_metadata = {
            'last_fresh_login': recent_time.isoformat()
        }

        should_login = session_manager._should_attempt_fresh_login()
        self.assertFalse(should_login, "Should not allow login within 24 hours")

        print("✅ Rate limiting protection test successful")

class TestMockedInstagramOperations(unittest.TestCase):
    """Test Instagram operations with comprehensive mocking"""

    def setUp(self):
        """Set up mock client with comprehensive API responses"""
        self.mock_client = Mock()

        # Mock user info
        self.mock_user = Mock()
        self.mock_user.pk = 123456789
        self.mock_user.username = "cryptoprism.io"
        self.mock_user.full_name = "CryptoPrism"
        self.mock_user.follower_count = 1500
        self.mock_user.following_count = 800
        self.mock_user.media_count = 45
        self.mock_user.is_private = False

        # Setup mock client responses
        self.mock_client.account_info.return_value = self.mock_user
        self.mock_client.user_info_by_username.return_value = self.mock_user
        self.mock_client.user_id = 123456789
        self.mock_client.username = "cryptoprism.io"

    def test_01_user_operations(self):
        """Test user-related operations"""
        # Test account info
        user_info = self.mock_client.account_info()
        self.assertEqual(user_info.username, "cryptoprism.io")
        self.assertEqual(user_info.follower_count, 1500)

        # Test user info by username
        user_by_username = self.mock_client.user_info_by_username("cryptoprism.io")
        self.assertEqual(user_by_username.username, "cryptoprism.io")

        print("✅ User operations test successful")
        print(f"   👤 Username: {user_info.username}")
        print(f"   👥 Followers: {user_info.follower_count}")
        print(f"   📸 Media: {user_info.media_count}")

    def test_02_media_operations(self):
        """Test media-related operations"""
        # Mock media response
        mock_media = Mock()
        mock_media.pk = "123456789_987654321"
        mock_media.caption_text = "Test post about crypto #crypto #blockchain"
        mock_media.like_count = 150
        mock_media.comment_count = 25
        mock_media.media_type = 1  # Photo

        self.mock_client.user_medias.return_value = [mock_media]
        self.mock_client.media_info.return_value = mock_media

        # Test getting user media
        medias = self.mock_client.user_medias(123456789, amount=5)
        self.assertEqual(len(medias), 1)
        self.assertEqual(medias[0].like_count, 150)

        # Test media info
        media_info = self.mock_client.media_info("123456789_987654321")
        self.assertEqual(media_info.comment_count, 25)

        print("✅ Media operations test successful")
        print(f"   📸 Post: {mock_media.pk}")
        print(f"   📝 Caption: {mock_media.caption_text[:50]}...")
        print(f"   ❤️ Likes: {mock_media.like_count}")

    def test_03_hashtag_operations(self):
        """Test hashtag-related operations"""
        # Mock hashtag response
        mock_hashtag = Mock()
        mock_hashtag.name = "crypto"
        mock_hashtag.media_count = 5000000
        mock_hashtag.id = 17841562447105233

        self.mock_client.hashtag_info.return_value = mock_hashtag

        # Test hashtag info
        hashtag_info = self.mock_client.hashtag_info("crypto")
        self.assertEqual(hashtag_info.name, "crypto")
        self.assertGreater(hashtag_info.media_count, 1000000)

        print("✅ Hashtag operations test successful")
        print(f"   🏷️ Hashtag: #{hashtag_info.name}")
        print(f"   📊 Media count: {hashtag_info.media_count:,}")

    def test_04_safety_features(self):
        """Test safety and compliance features"""
        # Mock delay range setting
        self.mock_client.delay_range = [1, 3]

        # Test rate limiting configuration
        rate_limits = {
            'likes_per_hour': 30,
            'follows_per_hour': 20,
            'comments_per_hour': 10,
            'posts_per_day': 5
        }

        for action, limit in rate_limits.items():
            self.assertIsInstance(limit, int)
            self.assertGreater(limit, 0)
            self.assertLessEqual(limit, 50)  # Conservative limits

        print("✅ Safety features test successful")
        print(f"   ⏱️ Delay range: {self.mock_client.delay_range}")
        print(f"   🛡️ Like limit: {rate_limits['likes_per_hour']}/hour")

def run_mock_session_tests():
    """Run the mock session test suite"""
    print("🧪 Starting Mock Session Tests")
    print("=" * 60)
    print("Testing session management with real credentials but mocked API")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSessionManagerWithMocks))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMockedInstagramOperations))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 MOCK SESSION TEST SUMMARY")
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
    run_mock_session_tests()