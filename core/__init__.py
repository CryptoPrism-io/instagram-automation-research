"""
Core automation components for Instagram research platform
"""

from .session_manager import InstagramSessionManager
from .content_generator import ContentGenerator
from .automation_base import AutomationBase, AutomationConfig

__all__ = [
    'InstagramSessionManager',
    'ContentGenerator',
    'AutomationBase',
    'AutomationConfig'
]