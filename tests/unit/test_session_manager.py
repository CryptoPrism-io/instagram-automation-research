#!/usr/bin/env python3
"""
Unit tests for Instagram Session Manager
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

class TestSessionManager(unittest.TestCase):
    """Test Session Manager functionality"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.session_file = os.path.join(self.temp_dir, "test_session.json")

    @patch.dict(os.environ, {'INSTAGRAM_USERNAME': 'test_user', 'INSTAGRAM_PASSWORD': 'test_pass'})
    def test_session_manager_with_env_vars(self):
        """Test session manager with environment variables"""
        from core.session_manager import InstagramSessionManager

        manager = InstagramSessionManager(session_file=self.session_file)
        self.assertEqual(manager.username, "test_user")
        self.assertEqual(manager.password, "test_pass")

    @patch.dict(os.environ, {'INSTAGRAM_USERNAME': 'test_user', 'INSTAGRAM_PASSWORD': 'test_pass'})
    def test_session_file_creation(self):
        """Test session file directory creation"""
        from core.session_manager import InstagramSessionManager

        nested_path = os.path.join(self.temp_dir, "nested", "session.json")
        manager = InstagramSessionManager(session_file=nested_path)

        # Directory should be created
        self.assertTrue(os.path.exists(os.path.dirname(nested_path)))

    def test_session_manager_explicit_credentials(self):
        """Test session manager with explicit credentials"""
        from core.session_manager import InstagramSessionManager

        manager = InstagramSessionManager(
            session_file=self.session_file,
            username="explicit_user",
            password="explicit_pass"
        )

        self.assertEqual(manager.username, "explicit_user")
        self.assertEqual(manager.password, "explicit_pass")

if __name__ == "__main__":
    unittest.main(verbosity=2)