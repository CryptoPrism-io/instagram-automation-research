#!/usr/bin/env python3
"""
Automation Base - Core automation framework for Instagram research
Provides base classes and utilities for safe Instagram automation
"""

import time
import random
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from .session_manager import InstagramSessionManager

logger = logging.getLogger(__name__)

@dataclass
class AutomationConfig:
    """Configuration for automation tasks"""
    rate_limits: Dict[str, int]
    delays: Dict[str, tuple]
    safety_settings: Dict[str, Any]
    session_config: Dict[str, Any]

class AutomationBase(ABC):
    """
    Base class for all Instagram automation tasks
    Provides common functionality for safe automation
    """

    def __init__(self, config: Optional[AutomationConfig] = None):
        """
        Initialize automation base

        Args:
            config: Automation configuration settings
        """
        self.config = config or self._get_default_config()
        self.session_manager = None
        self.client = None
        self.action_tracker = ActionTracker()
        self.last_action_time = datetime.now()

    def _get_default_config(self) -> AutomationConfig:
        """Get default safe configuration"""
        return AutomationConfig(
            rate_limits={
                'likes_per_hour': 30,
                'follows_per_hour': 20,
                'comments_per_hour': 10,
                'posts_per_day': 5,
                'dm_per_hour': 15
            },
            delays={
                'action_delay': (2, 5),
                'request_delay': (1, 3),
                'error_delay': (10, 30)
            },
            safety_settings={
                'use_test_accounts_only': True,
                'enable_rate_limiting': True,
                'max_daily_actions': 100,
                'cooldown_period_hours': 2
            },
            session_config={
                'session_max_age_days': 30,
                'min_login_interval_hours': 24
            }
        )

    def initialize_session(self, username: Optional[str] = None,
                          password: Optional[str] = None) -> bool:
        """
        Initialize Instagram session safely

        Args:
            username: Instagram username (optional, will use env var)
            password: Instagram password (optional, will use env var)

        Returns:
            True if session initialized successfully
        """
        try:
            logger.info("🔄 Initializing Instagram session...")

            self.session_manager = InstagramSessionManager(
                session_file="data/sessions/automation_session.json",
                username=username,
                password=password,
                session_max_age_days=self.config.session_config['session_max_age_days']
            )

            self.client = self.session_manager.get_smart_client()

            if self.client:
                logger.info("✅ Instagram session initialized successfully")
                self._setup_client_safety()
                return True
            else:
                logger.error("❌ Failed to initialize Instagram session")
                return False

        except Exception as e:
            logger.error(f"❌ Error initializing session: {e}")
            return False

    def _setup_client_safety(self):
        """Setup safety features for the client"""
        if self.client:
            # Set delay ranges for natural behavior
            delay_range = self.config.delays['request_delay']
            self.client.delay_range = list(delay_range)

            logger.info(f"🛡️ Safety settings applied - delays: {delay_range}")

    def safe_action(self, action_type: str, action_func, *args, **kwargs):
        """
        Execute an action safely with rate limiting and error handling

        Args:
            action_type: Type of action for tracking
            action_func: Function to execute
            *args: Arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            Result of the action or None if failed/rate limited
        """
        try:
            # Check rate limits
            if not self._check_rate_limit(action_type):
                logger.warning(f"⏳ Rate limit reached for {action_type}")
                return None

            # Check minimum delay since last action
            self._ensure_action_delay()

            # Execute action
            logger.debug(f"🔄 Executing {action_type} action")
            result = action_func(*args, **kwargs)

            # Track successful action
            self.action_tracker.record_action(action_type, success=True)
            self.last_action_time = datetime.now()

            # Add post-action delay
            self._add_random_delay(self.config.delays['action_delay'])

            logger.debug(f"✅ {action_type} action completed successfully")
            return result

        except Exception as e:
            logger.error(f"❌ Error executing {action_type}: {e}")
            self.action_tracker.record_action(action_type, success=False, error=str(e))

            # Add error delay
            self._add_random_delay(self.config.delays['error_delay'])
            return None

    def _check_rate_limit(self, action_type: str) -> bool:
        """
        Check if action is within rate limits

        Args:
            action_type: Type of action to check

        Returns:
            True if action is allowed, False if rate limited
        """
        if not self.config.safety_settings['enable_rate_limiting']:
            return True

        # Map action types to rate limit keys
        rate_limit_key = self._get_rate_limit_key(action_type)

        if rate_limit_key in self.config.rate_limits:
            limit = self.config.rate_limits[rate_limit_key]
            current_count = self.action_tracker.get_hourly_count(action_type)

            if current_count >= limit:
                return False

        return True

    def _get_rate_limit_key(self, action_type: str) -> str:
        """Map action type to rate limit configuration key"""
        mapping = {
            'like': 'likes_per_hour',
            'follow': 'follows_per_hour',
            'comment': 'comments_per_hour',
            'post': 'posts_per_day',
            'dm': 'dm_per_hour'
        }
        return mapping.get(action_type, 'default')

    def _ensure_action_delay(self):
        """Ensure minimum delay between actions"""
        min_delay = self.config.delays['action_delay'][0]
        time_since_last = (datetime.now() - self.last_action_time).total_seconds()

        if time_since_last < min_delay:
            sleep_time = min_delay - time_since_last
            logger.debug(f"⏳ Waiting {sleep_time:.1f}s for action delay")
            time.sleep(sleep_time)

    def _add_random_delay(self, delay_range: tuple):
        """Add random delay within specified range"""
        delay = random.uniform(delay_range[0], delay_range[1])
        logger.debug(f"⏳ Random delay: {delay:.1f}s")
        time.sleep(delay)

    def get_session_info(self) -> Dict[str, Any]:
        """Get current session information"""
        if self.session_manager:
            return self.session_manager.get_session_info()
        return {"error": "No session manager initialized"}

    def get_action_stats(self) -> Dict[str, Any]:
        """Get action statistics"""
        return self.action_tracker.get_stats()

    @abstractmethod
    def run(self) -> Dict[str, Any]:
        """Main automation logic - must be implemented by subclasses"""
        pass

class ActionTracker:
    """Track automation actions for rate limiting and analytics"""

    def __init__(self):
        self.actions = []

    def record_action(self, action_type: str, success: bool = True, error: str = None):
        """Record an action with timestamp and result"""
        self.actions.append({
            'type': action_type,
            'timestamp': datetime.now(),
            'success': success,
            'error': error
        })

    def get_hourly_count(self, action_type: str) -> int:
        """Get count of actions in the last hour"""
        cutoff = datetime.now() - timedelta(hours=1)
        return len([
            action for action in self.actions
            if action['type'] == action_type and action['timestamp'] > cutoff
        ])

    def get_daily_count(self, action_type: str) -> int:
        """Get count of actions in the last 24 hours"""
        cutoff = datetime.now() - timedelta(days=1)
        return len([
            action for action in self.actions
            if action['type'] == action_type and action['timestamp'] > cutoff
        ])

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive action statistics"""
        if not self.actions:
            return {"total_actions": 0, "success_rate": 0}

        total = len(self.actions)
        successful = len([a for a in self.actions if a['success']])

        # Group by action type
        type_stats = {}
        for action in self.actions:
            action_type = action['type']
            if action_type not in type_stats:
                type_stats[action_type] = {'total': 0, 'successful': 0}

            type_stats[action_type]['total'] += 1
            if action['success']:
                type_stats[action_type]['successful'] += 1

        # Calculate success rates
        for stats in type_stats.values():
            stats['success_rate'] = stats['successful'] / stats['total'] * 100

        return {
            'total_actions': total,
            'successful_actions': successful,
            'overall_success_rate': successful / total * 100,
            'by_type': type_stats,
            'last_action': max(self.actions, key=lambda x: x['timestamp'])['timestamp'].isoformat()
        }

class SafetyMonitor:
    """Monitor automation for safety compliance"""

    def __init__(self, config: AutomationConfig):
        self.config = config
        self.alerts = []

    def check_compliance(self, action_tracker: ActionTracker) -> List[str]:
        """Check automation compliance and return any alerts"""
        alerts = []
        stats = action_tracker.get_stats()

        # Check daily action limits
        if stats['total_actions'] > self.config.safety_settings['max_daily_actions']:
            alerts.append("Daily action limit exceeded")

        # Check success rate
        if stats['overall_success_rate'] < 80:
            alerts.append("Low success rate detected - possible rate limiting")

        # Check for error patterns
        recent_errors = [
            action for action in action_tracker.actions
            if not action['success'] and
            (datetime.now() - action['timestamp']).total_seconds() < 3600
        ]

        if len(recent_errors) > 5:
            alerts.append("High error rate in the last hour")

        self.alerts.extend(alerts)
        return alerts

    def get_safety_report(self) -> Dict[str, Any]:
        """Generate safety compliance report"""
        return {
            'timestamp': datetime.now().isoformat(),
            'alerts': self.alerts,
            'compliance_status': 'SAFE' if not self.alerts else 'WARNING',
            'recommendations': self._get_recommendations()
        }

    def _get_recommendations(self) -> List[str]:
        """Get safety recommendations based on current state"""
        recommendations = []

        if any('limit' in alert for alert in self.alerts):
            recommendations.append("Reduce automation frequency")

        if any('error' in alert for alert in self.alerts):
            recommendations.append("Check account status and API connectivity")

        if any('success rate' in alert for alert in self.alerts):
            recommendations.append("Implement longer delays between actions")

        return recommendations

# Example automation implementation
class TestAutomation(AutomationBase):
    """Example automation for testing purposes"""

    def run(self) -> Dict[str, Any]:
        """Run test automation workflow"""
        logger.info("🧪 Starting test automation workflow")

        if not self.initialize_session():
            return {"status": "failed", "error": "Session initialization failed"}

        results = {
            "status": "completed",
            "actions_performed": [],
            "session_info": self.get_session_info()
        }

        try:
            # Test basic API connectivity
            user_info = self.safe_action('api_test', self.client.user_info_by_username, self.client.username)

            if user_info:
                results["actions_performed"].append({
                    "action": "user_info_test",
                    "success": True,
                    "data": {"username": user_info.username, "followers": user_info.follower_count}
                })
            else:
                results["actions_performed"].append({
                    "action": "user_info_test",
                    "success": False
                })

            # Add action statistics
            results["action_stats"] = self.get_action_stats()

            logger.info("✅ Test automation completed successfully")
            return results

        except Exception as e:
            logger.error(f"❌ Test automation failed: {e}")
            return {"status": "failed", "error": str(e)}

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Run test automation
    test_automation = TestAutomation()
    results = test_automation.run()

    print("🧪 Test Automation Results:")
    print(f"Status: {results['status']}")
    print(f"Actions: {len(results.get('actions_performed', []))}")

    if 'action_stats' in results:
        stats = results['action_stats']
        print(f"Success Rate: {stats.get('overall_success_rate', 0):.1f}%")