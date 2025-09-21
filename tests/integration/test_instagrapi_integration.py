#!/usr/bin/env python3
"""
Integration tests for instagrapi functionality
Tests actual library imports and basic functionality without API calls
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

class TestInstagrapiIntegration(unittest.TestCase):
    """Test instagrapi library integration"""

    def test_instagrapi_import(self):
        """Test that instagrapi can be imported"""
        try:
            import instagrapi
            from instagrapi import Client
            from instagrapi.exceptions import LoginRequired, ClientError
            self.assertTrue(True, "All instagrapi imports successful")
        except ImportError as e:
            self.fail(f"Failed to import instagrapi: {e}")

    def test_client_initialization(self):
        """Test Client initialization without authentication"""
        from instagrapi import Client

        client = Client()
        self.assertIsNotNone(client)
        self.assertTrue(hasattr(client, 'login'))
        self.assertTrue(hasattr(client, 'user_info'))
        self.assertTrue(hasattr(client, 'media_info'))

    def test_client_settings(self):
        """Test client configuration without authentication"""
        from instagrapi import Client

        client = Client()

        # Test delay configuration
        client.delay_range = [1, 3]
        self.assertEqual(client.delay_range, [1, 3])

        # Test user agent setting
        original_user_agent = client.user_agent
        client.set_user_agent("test-agent")
        self.assertNotEqual(client.user_agent, original_user_agent)

    @patch('instagrapi.Client.login')
    def test_mock_authentication(self):
        """Test authentication flow with mocking"""
        from instagrapi import Client

        mock_login = Mock(return_value=True)

        with patch.object(Client, 'login', mock_login):
            client = Client()
            result = client.login("test_user", "test_pass")

            mock_login.assert_called_once_with("test_user", "test_pass")
            self.assertTrue(result)

    def test_session_management_structure(self):
        """Test session management without actual session"""
        from instagrapi import Client
        import tempfile
        import os

        client = Client()

        # Test settings methods exist
        self.assertTrue(hasattr(client, 'dump_settings'))
        self.assertTrue(hasattr(client, 'load_settings'))
        self.assertTrue(hasattr(client, 'get_settings'))

        # Test settings structure (mock)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            settings_file = f.name

        try:
            # Test that methods can be called (will create empty or default settings)
            settings = client.get_settings()
            self.assertIsInstance(settings, dict)
        finally:
            if os.path.exists(settings_file):
                os.unlink(settings_file)

class TestCoreIntegration(unittest.TestCase):
    """Test integration with our core modules"""

    def test_session_manager_integration(self):
        """Test session manager integrates with instagrapi"""
        from core.session_manager import InstagramSessionManager

        # Test that session manager can be initialized
        with patch.dict('os.environ', {'INSTAGRAM_USERNAME': 'test', 'INSTAGRAM_PASSWORD': 'test'}):
            manager = InstagramSessionManager()
            self.assertIsNotNone(manager)
            self.assertTrue(hasattr(manager, 'client'))

    def test_content_generator_integration(self):
        """Test content generator integration"""
        from core.content_generator import ContentGenerator

        generator = ContentGenerator()
        self.assertIsNotNone(generator)
        self.assertTrue(hasattr(generator, 'templates_dir'))

    def test_automation_base_integration(self):
        """Test automation base integration"""
        from core.automation_base import AutomationBase, AutomationConfig

        # Test that classes can be imported and have expected structure
        self.assertTrue(hasattr(AutomationBase, '__init__'))
        self.assertTrue(hasattr(AutomationConfig, '__init__'))

class TestDocumentationCoverage(unittest.TestCase):
    """Test that documented features have corresponding functionality"""

    def test_media_documentation_coverage(self):
        """Test media module documentation coverage"""
        from instagrapi import Client

        client = Client()

        # Check methods mentioned in docs/instagrapi/media.md exist
        media_methods = [
            'media_info', 'media_like', 'media_unlike', 'media_save',
            'media_unsave', 'media_comment', 'media_likers',
            'photo_upload', 'video_upload', 'album_upload'
        ]

        for method in media_methods:
            self.assertTrue(hasattr(client, method),
                          f"Client missing documented method: {method}")

    def test_user_documentation_coverage(self):
        """Test user module documentation coverage"""
        from instagrapi import Client

        client = Client()

        # Check methods mentioned in docs/instagrapi/user.md exist
        user_methods = [
            'user_info', 'user_info_by_username', 'user_followers',
            'user_following', 'user_follow', 'user_unfollow',
            'user_medias', 'user_stories'
        ]

        for method in user_methods:
            self.assertTrue(hasattr(client, method),
                          f"Client missing documented method: {method}")

    def test_story_documentation_coverage(self):
        """Test story module documentation coverage"""
        from instagrapi import Client

        client = Client()

        # Check methods mentioned in docs/instagrapi/story.md exist
        story_methods = [
            'user_stories', 'story_info', 'story_download',
            'photo_upload_to_story', 'video_upload_to_story'
        ]

        for method in story_methods:
            self.assertTrue(hasattr(client, method),
                          f"Client missing documented method: {method}")

    def test_hashtag_documentation_coverage(self):
        """Test hashtag module documentation coverage"""
        from instagrapi import Client

        client = Client()

        # Check methods mentioned in docs/instagrapi/hashtag.md exist
        hashtag_methods = [
            'hashtag_info', 'hashtag_medias_recent', 'hashtag_medias_top'
        ]

        for method in hashtag_methods:
            self.assertTrue(hasattr(client, method),
                          f"Client missing documented method: {method}")

if __name__ == "__main__":
    unittest.main(verbosity=2)