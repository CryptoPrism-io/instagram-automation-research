#!/usr/bin/env python3
"""
Basic tests for Instagram Automation Research platform
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestBasicFunctionality(unittest.TestCase):
    """Test basic platform functionality"""

    def test_import_core_modules(self):
        """Test that core modules can be imported"""
        try:
            from core.session_manager import InstagramSessionManager
            from core.content_generator import ContentGenerator
            from core.automation_base import AutomationBase
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import core modules: {e}")

    def test_content_generator_init(self):
        """Test content generator initialization"""
        from core.content_generator import ContentGenerator

        generator = ContentGenerator()
        self.assertIsNotNone(generator)
        self.assertTrue(hasattr(generator, 'templates_dir'))
        self.assertTrue(hasattr(generator, 'output_dir'))

    def test_session_manager_init(self):
        """Test session manager initialization"""
        from core.session_manager import InstagramSessionManager

        # Test without credentials (should not fail)
        try:
            session_manager = InstagramSessionManager(
                session_file="test_session.json",
                username="test",
                password="test"
            )
            self.assertIsNotNone(session_manager)
        except Exception as e:
            # Expected to fail without real credentials
            self.assertIn("Instagram", str(e))

if __name__ == "__main__":
    unittest.main()