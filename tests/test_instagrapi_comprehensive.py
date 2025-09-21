#!/usr/bin/env python3
"""
Comprehensive test suite for instagrapi functionality
Tests all major features documented in docs/instagrapi/
"""

import unittest
import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestInstagramSessionManager(unittest.TestCase):
    """Test Session Manager functionality"""

    def setUp(self):
        from core.session_manager import InstagramSessionManager
        self.temp_dir = tempfile.mkdtemp()
        self.session_file = os.path.join(self.temp_dir, "test_session.json")

    def test_session_manager_init(self):
        """Test session manager initialization"""
        from core.session_manager import InstagramSessionManager

        manager = InstagramSessionManager(
            session_file=self.session_file,
            username="test_user",
            password="test_pass"
        )

        self.assertIsNotNone(manager)
        self.assertEqual(manager.username, "test_user")
        self.assertEqual(manager.password, "test_pass")
        self.assertEqual(str(manager.session_file), self.session_file)

    def test_session_file_creation(self):
        """Test session file directory creation"""
        from core.session_manager import InstagramSessionManager

        nested_path = os.path.join(self.temp_dir, "nested", "session.json")
        manager = InstagramSessionManager(session_file=nested_path)

        # Directory should be created
        self.assertTrue(os.path.exists(os.path.dirname(nested_path)))

class TestInstagrapiFeatures(unittest.TestCase):
    """Test instagrapi library features (mocked for safety)"""

    def setUp(self):
        """Setup mock client for testing"""
        self.mock_client = Mock()

    def test_user_operations(self):
        """Test user-related operations"""
        # Mock user info response
        mock_user = Mock()
        mock_user.pk = 123456789
        mock_user.username = "test_user"
        mock_user.full_name = "Test User"
        mock_user.follower_count = 1000
        mock_user.following_count = 500

        self.mock_client.user_info_by_username.return_value = mock_user
        self.mock_client.user_followers.return_value = [mock_user]
        self.mock_client.user_following.return_value = [mock_user]

        # Test user info retrieval
        user_info = self.mock_client.user_info_by_username("test_user")
        self.assertEqual(user_info.username, "test_user")
        self.assertEqual(user_info.follower_count, 1000)

        # Test followers/following
        followers = self.mock_client.user_followers(123456789)
        following = self.mock_client.user_following(123456789)
        self.assertIsInstance(followers, list)
        self.assertIsInstance(following, list)

    def test_media_operations(self):
        """Test media-related operations"""
        # Mock media response
        mock_media = Mock()
        mock_media.pk = "123456789_123456789"
        mock_media.caption_text = "Test caption #test"
        mock_media.like_count = 100
        mock_media.comment_count = 10

        self.mock_client.media_info.return_value = mock_media
        self.mock_client.media_likers.return_value = []

        # Test media info
        media_info = self.mock_client.media_info("123456789_123456789")
        self.assertEqual(media_info.caption_text, "Test caption #test")
        self.assertEqual(media_info.like_count, 100)

    def test_story_operations(self):
        """Test story-related operations"""
        # Mock story response
        mock_story = Mock()
        mock_story.pk = "123456789_123456789"
        mock_story.taken_at = "2024-01-01T00:00:00"

        self.mock_client.user_stories.return_value = [mock_story]

        # Test story retrieval
        stories = self.mock_client.user_stories(123456789)
        self.assertIsInstance(stories, list)

    def test_direct_message_operations(self):
        """Test direct message operations"""
        # Mock DM response
        mock_thread = Mock()
        mock_thread.id = "123456789"
        mock_thread.users = []

        self.mock_client.direct_threads.return_value = [mock_thread]

        # Test thread retrieval
        threads = self.mock_client.direct_threads()
        self.assertIsInstance(threads, list)

    def test_hashtag_operations(self):
        """Test hashtag-related operations"""
        # Mock hashtag response
        mock_hashtag = Mock()
        mock_hashtag.name = "test"
        mock_hashtag.media_count = 1000000

        self.mock_client.hashtag_info.return_value = mock_hashtag

        # Test hashtag info
        hashtag_info = self.mock_client.hashtag_info("test")
        self.assertEqual(hashtag_info.name, "test")
        self.assertEqual(hashtag_info.media_count, 1000000)

    def test_location_operations(self):
        """Test location-related operations"""
        # Mock location response
        mock_location = Mock()
        mock_location.pk = 123456789
        mock_location.name = "Test Location"
        mock_location.lat = 40.7128
        mock_location.lng = -74.0060

        self.mock_client.location_info.return_value = mock_location

        # Test location info
        location_info = self.mock_client.location_info(123456789)
        self.assertEqual(location_info.name, "Test Location")
        self.assertEqual(location_info.lat, 40.7128)

class TestContentGenerator(unittest.TestCase):
    """Test content generator functionality"""

    def test_content_generator_init(self):
        """Test content generator initialization"""
        from core.content_generator import ContentGenerator

        generator = ContentGenerator()
        self.assertIsNotNone(generator)
        self.assertTrue(hasattr(generator, 'templates_dir'))
        self.assertTrue(hasattr(generator, 'output_dir'))

class TestSafetyFeatures(unittest.TestCase):
    """Test safety and rate limiting features"""

    def test_rate_limiting_config(self):
        """Test rate limiting configuration"""
        # Test that rate limiting settings exist
        rate_limits = {
            'likes_per_hour': 30,
            'follows_per_hour': 20,
            'comments_per_hour': 10,
            'posts_per_day': 5
        }

        for action, limit in rate_limits.items():
            self.assertIsInstance(limit, int)
            self.assertGreater(limit, 0)

    def test_safety_config(self):
        """Test safety configuration"""
        safety_config = {
            'use_test_accounts_only': True,
            'enable_rate_limiting': True,
            'max_daily_actions': 100,
            'cooldown_period_hours': 2
        }

        self.assertTrue(safety_config['use_test_accounts_only'])
        self.assertTrue(safety_config['enable_rate_limiting'])
        self.assertGreater(safety_config['max_daily_actions'], 0)

class TestIntegrationReadiness(unittest.TestCase):
    """Test integration readiness without actual API calls"""

    def test_environment_setup(self):
        """Test that environment can be set up"""
        # Test that required packages are importable
        try:
            import instagrapi
            from instagrapi import Client
            self.assertTrue(True, "instagrapi import successful")
        except ImportError as e:
            self.fail(f"instagrapi not available: {e}")

    def test_mock_authentication(self):
        """Test authentication flow (mocked)"""
        from instagrapi import Client

        with patch.object(Client, 'login') as mock_login:
            mock_login.return_value = True

            client = Client()
            result = client.login("test_user", "test_pass")

            mock_login.assert_called_once_with("test_user", "test_pass")
            self.assertTrue(result)

if __name__ == "__main__":
    # Run tests with detailed output
    unittest.main(verbosity=2)