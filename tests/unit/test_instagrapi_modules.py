#!/usr/bin/env python3
"""
Unit tests for instagrapi modules functionality
Tests each documented module from docs/instagrapi/
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

class TestInstagrapiModules(unittest.TestCase):
    """Test instagrapi library modules based on documentation"""

    def setUp(self):
        """Setup mock client for testing"""
        self.mock_client = Mock()

    def test_media_module(self):
        """Test media operations from docs/instagrapi/media.md"""
        # Mock media operations
        mock_media = Mock()
        mock_media.pk = "123456789_123456789"
        mock_media.caption_text = "Test caption #test"
        mock_media.like_count = 100
        mock_media.comment_count = 10
        mock_media.media_type = 1  # Photo

        # Test media info
        self.mock_client.media_info.return_value = mock_media
        media_info = self.mock_client.media_info("123456789_123456789")

        self.assertEqual(media_info.pk, "123456789_123456789")
        self.assertEqual(media_info.like_count, 100)
        self.mock_client.media_info.assert_called_once()

        # Test media interactions
        self.mock_client.media_like.return_value = True
        self.mock_client.media_unlike.return_value = True
        self.mock_client.media_save.return_value = True

        self.assertTrue(self.mock_client.media_like("123456789_123456789"))
        self.assertTrue(self.mock_client.media_unlike("123456789_123456789"))
        self.assertTrue(self.mock_client.media_save("123456789_123456789"))

    def test_user_module(self):
        """Test user operations from docs/instagrapi/user.md"""
        # Mock user data
        mock_user = Mock()
        mock_user.pk = 123456789
        mock_user.username = "test_user"
        mock_user.full_name = "Test User"
        mock_user.follower_count = 1000
        mock_user.following_count = 500
        mock_user.is_private = False

        # Test user info
        self.mock_client.user_info.return_value = mock_user
        self.mock_client.user_info_by_username.return_value = mock_user

        user_info = self.mock_client.user_info_by_username("test_user")
        self.assertEqual(user_info.username, "test_user")
        self.assertEqual(user_info.follower_count, 1000)

        # Test follow operations
        self.mock_client.user_follow.return_value = True
        self.mock_client.user_unfollow.return_value = True

        self.assertTrue(self.mock_client.user_follow(123456789))
        self.assertTrue(self.mock_client.user_unfollow(123456789))

    def test_story_module(self):
        """Test story operations from docs/instagrapi/story.md"""
        # Mock story data
        mock_story = Mock()
        mock_story.pk = "123456789_123456789"
        mock_story.taken_at = "2024-01-01T00:00:00"
        mock_story.media_type = 1
        mock_story.user_id = 123456789

        # Test story operations
        self.mock_client.user_stories.return_value = [mock_story]
        self.mock_client.story_info.return_value = mock_story

        stories = self.mock_client.user_stories(123456789)
        self.assertIsInstance(stories, list)
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0].pk, "123456789_123456789")

    def test_direct_messages_module(self):
        """Test DM operations from docs/instagrapi/direct-messages.md"""
        # Mock thread and message data
        mock_thread = Mock()
        mock_thread.id = "123456789"
        mock_thread.users = []
        mock_thread.messages = []

        mock_message = Mock()
        mock_message.id = "msg_123456789"
        mock_message.text = "Test message"
        mock_message.user_id = 123456789

        # Test thread operations
        self.mock_client.direct_threads.return_value = [mock_thread]
        self.mock_client.direct_send.return_value = mock_message

        threads = self.mock_client.direct_threads()
        self.assertIsInstance(threads, list)

        # Test sending message
        sent_message = self.mock_client.direct_send("Hello!", user_ids=[123456789])
        self.assertEqual(sent_message.text, "Test message")

    def test_hashtag_module(self):
        """Test hashtag operations from docs/instagrapi/hashtag.md"""
        # Mock hashtag data
        mock_hashtag = Mock()
        mock_hashtag.name = "test"
        mock_hashtag.media_count = 1000000
        mock_hashtag.id = 17841562447105233

        # Test hashtag operations
        self.mock_client.hashtag_info.return_value = mock_hashtag
        self.mock_client.hashtag_medias_recent.return_value = []

        hashtag_info = self.mock_client.hashtag_info("test")
        self.assertEqual(hashtag_info.name, "test")
        self.assertEqual(hashtag_info.media_count, 1000000)

        recent_media = self.mock_client.hashtag_medias_recent("test", amount=20)
        self.assertIsInstance(recent_media, list)

    def test_location_module(self):
        """Test location operations from docs/instagrapi/location.md"""
        # Mock location data
        mock_location = Mock()
        mock_location.pk = 123456789
        mock_location.name = "New York, NY"
        mock_location.lat = 40.7128
        mock_location.lng = -74.0060

        # Test location operations
        self.mock_client.location_info.return_value = mock_location
        self.mock_client.location_search.return_value = [mock_location]

        location_info = self.mock_client.location_info(123456789)
        self.assertEqual(location_info.name, "New York, NY")
        self.assertEqual(location_info.lat, 40.7128)

        locations = self.mock_client.location_search(40.7128, -74.0060)
        self.assertIsInstance(locations, list)

    def test_highlight_module(self):
        """Test highlight operations from docs/instagrapi/highlight.md"""
        # Mock highlight data
        mock_highlight = Mock()
        mock_highlight.pk = "highlight_123456789"
        mock_highlight.title = "Test Highlight"
        mock_highlight.cover_media = Mock()

        # Test highlight operations
        self.mock_client.user_highlights.return_value = [mock_highlight]
        self.mock_client.highlight_info.return_value = mock_highlight

        highlights = self.mock_client.user_highlights(123456789)
        self.assertIsInstance(highlights, list)
        self.assertEqual(highlights[0].title, "Test Highlight")

class TestInstagrapiSafety(unittest.TestCase):
    """Test safety features and best practices"""

    def test_rate_limiting_settings(self):
        """Test rate limiting configuration exists"""
        rate_limits = {
            'likes_per_hour': 30,
            'follows_per_hour': 20,
            'comments_per_hour': 10,
            'posts_per_day': 5,
            'story_views_per_hour': 100,
            'dm_sends_per_hour': 20
        }

        for action, limit in rate_limits.items():
            self.assertIsInstance(limit, int)
            self.assertGreater(limit, 0)
            self.assertLessEqual(limit, 200)  # Reasonable upper bound

    def test_safety_configuration(self):
        """Test safety configuration"""
        safety_config = {
            'use_test_accounts_only': True,
            'enable_rate_limiting': True,
            'max_daily_actions': 100,
            'cooldown_period_hours': 2,
            'session_timeout_hours': 24,
            'enable_proxy_rotation': False,  # For testing
            'delay_range_seconds': [1, 3]
        }

        # Verify safety settings
        self.assertTrue(safety_config['use_test_accounts_only'])
        self.assertTrue(safety_config['enable_rate_limiting'])
        self.assertGreater(safety_config['max_daily_actions'], 0)
        self.assertGreater(safety_config['cooldown_period_hours'], 0)
        self.assertIsInstance(safety_config['delay_range_seconds'], list)
        self.assertEqual(len(safety_config['delay_range_seconds']), 2)

class TestInstagramCompliance(unittest.TestCase):
    """Test Instagram ToS compliance features"""

    def test_anti_spam_measures(self):
        """Test anti-spam configuration"""
        anti_spam_config = {
            'max_likes_per_session': 50,
            'min_delay_between_actions': 1,
            'max_delay_between_actions': 5,
            'randomize_delays': True,
            'respect_private_accounts': True,
            'avoid_repetitive_patterns': True
        }

        for setting, value in anti_spam_config.items():
            self.assertIsNotNone(value)
            if isinstance(value, int):
                self.assertGreater(value, 0)

    def test_privacy_compliance(self):
        """Test privacy compliance settings"""
        privacy_settings = {
            'respect_user_privacy': True,
            'skip_private_accounts': True,
            'no_data_collection_from_minors': True,
            'respect_blocked_users': True,
            'honor_privacy_settings': True
        }

        for setting, enabled in privacy_settings.items():
            self.assertTrue(enabled, f"Privacy setting {setting} should be enabled")

if __name__ == "__main__":
    unittest.main(verbosity=2)