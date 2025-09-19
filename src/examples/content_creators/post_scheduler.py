#!/usr/bin/env python3
"""
Content Creator Example 1: Automated Post Scheduling
Schedule Instagram posts with optimal timing based on audience analytics
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import schedule
import time
import json
from typing import Dict, List, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.automation_base import AutomationBase, AutomationConfig
from core.content_generator import ContentGenerator
import logging

logger = logging.getLogger(__name__)

class PostScheduler(AutomationBase):
    """
    Automated post scheduling system for content creators
    Features:
    - Optimal timing based on audience activity
    - Content queue management
    - Performance tracking
    - Template-based content generation
    """

    def __init__(self, config: AutomationConfig = None):
        super().__init__(config)
        self.content_generator = ContentGenerator()
        self.content_queue = []
        self.scheduling_data = self._load_scheduling_data()

    def _load_scheduling_data(self) -> Dict[str, Any]:
        """Load or create scheduling configuration"""
        config_file = Path("data/scheduling_config.json")

        default_config = {
            "optimal_times": {
                "monday": ["09:00", "13:00", "18:00"],
                "tuesday": ["09:00", "13:00", "18:00"],
                "wednesday": ["09:00", "13:00", "18:00"],
                "thursday": ["09:00", "13:00", "18:00"],
                "friday": ["09:00", "13:00", "17:00"],
                "saturday": ["10:00", "14:00", "19:00"],
                "sunday": ["10:00", "15:00", "19:00"]
            },
            "content_types": {
                "educational": {"frequency": "daily", "best_times": ["09:00", "13:00"]},
                "promotional": {"frequency": "twice_weekly", "best_times": ["18:00", "19:00"]},
                "behind_scenes": {"frequency": "weekly", "best_times": ["15:00", "19:00"]},
                "user_generated": {"frequency": "twice_weekly", "best_times": ["13:00", "18:00"]}
            },
            "hashtag_sets": {
                "educational": ["#education", "#learning", "#tips", "#knowledge", "#growth"],
                "promotional": ["#product", "#announcement", "#special", "#offer", "#new"],
                "behind_scenes": ["#behindthescenes", "#process", "#team", "#workspace"],
                "user_generated": ["#community", "#usergenerated", "#showcase", "#featured"]
            }
        }

        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        # Save default config
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)

        return default_config

    def add_content_to_queue(self, content_data: Dict[str, Any]) -> bool:
        """
        Add content to the scheduling queue

        Args:
            content_data: Content information including type, template, data

        Returns:
            True if added successfully
        """
        try:
            # Validate content data
            required_fields = ['type', 'template', 'data']
            if not all(field in content_data for field in required_fields):
                logger.error("Missing required fields in content data")
                return False

            # Add metadata
            content_data.update({
                'id': f"content_{int(time.time())}",
                'created_at': datetime.now().isoformat(),
                'status': 'queued',
                'scheduled_time': None
            })

            self.content_queue.append(content_data)
            logger.info(f"✅ Added content to queue: {content_data['id']}")
            return True

        except Exception as e:
            logger.error(f"❌ Error adding content to queue: {e}")
            return False

    def schedule_content(self, days_ahead: int = 7) -> List[Dict[str, Any]]:
        """
        Schedule content from queue for the next X days

        Args:
            days_ahead: Number of days to schedule ahead

        Returns:
            List of scheduled posts
        """
        try:
            scheduled_posts = []
            current_date = datetime.now().date()

            for day_offset in range(days_ahead):
                target_date = current_date + timedelta(days=day_offset)
                day_name = target_date.strftime('%A').lower()

                # Get optimal times for this day
                optimal_times = self.scheduling_data['optimal_times'].get(day_name, ["12:00"])

                # Schedule content based on type and frequency
                daily_posts = self._plan_daily_content(target_date, optimal_times)
                scheduled_posts.extend(daily_posts)

            # Update queue status
            self._update_queue_status(scheduled_posts)

            logger.info(f"✅ Scheduled {len(scheduled_posts)} posts for {days_ahead} days")
            return scheduled_posts

        except Exception as e:
            logger.error(f"❌ Error scheduling content: {e}")
            return []

    def _plan_daily_content(self, target_date: datetime.date,
                           optimal_times: List[str]) -> List[Dict[str, Any]]:
        """Plan content for a specific day"""
        daily_posts = []

        # Determine content types for this day
        content_plan = self._get_content_plan_for_date(target_date)

        for i, (content_type, time_slot) in enumerate(zip(content_plan, optimal_times)):
            # Find suitable content from queue
            content = self._find_content_by_type(content_type)

            if content:
                scheduled_time = datetime.combine(target_date, datetime.strptime(time_slot, '%H:%M').time())

                scheduled_post = {
                    'content_id': content['id'],
                    'content_type': content_type,
                    'scheduled_time': scheduled_time.isoformat(),
                    'template': content['template'],
                    'data': content['data'],
                    'hashtags': self._get_hashtags_for_type(content_type),
                    'status': 'scheduled'
                }

                daily_posts.append(scheduled_post)

        return daily_posts

    def _get_content_plan_for_date(self, target_date: datetime.date) -> List[str]:
        """Get content types to post on a specific date"""
        day_of_week = target_date.weekday()  # 0 = Monday

        # Example content planning logic
        if day_of_week == 0:  # Monday
            return ['educational']
        elif day_of_week == 2:  # Wednesday
            return ['educational', 'promotional']
        elif day_of_week == 4:  # Friday
            return ['behind_scenes']
        elif day_of_week == 6:  # Sunday
            return ['user_generated']
        else:
            return ['educational']

    def _find_content_by_type(self, content_type: str) -> Dict[str, Any]:
        """Find queued content by type"""
        for content in self.content_queue:
            if content['type'] == content_type and content['status'] == 'queued':
                return content
        return None

    def _get_hashtags_for_type(self, content_type: str) -> str:
        """Get hashtags for content type"""
        hashtags = self.scheduling_data['hashtag_sets'].get(content_type, [])
        return ' '.join([f"#{tag}" for tag in hashtags])

    def _update_queue_status(self, scheduled_posts: List[Dict[str, Any]]):
        """Update status of scheduled content in queue"""
        scheduled_ids = {post['content_id'] for post in scheduled_posts}

        for content in self.content_queue:
            if content['id'] in scheduled_ids:
                content['status'] = 'scheduled'

    def execute_scheduled_posts(self) -> Dict[str, Any]:
        """Execute posts that are scheduled for now"""
        results = {
            'executed': 0,
            'failed': 0,
            'posts': []
        }

        try:
            if not self.initialize_session():
                return {'error': 'Session initialization failed'}

            # Load scheduled posts
            scheduled_posts = self._load_scheduled_posts()
            current_time = datetime.now()

            for post in scheduled_posts:
                scheduled_time = datetime.fromisoformat(post['scheduled_time'])

                # Check if it's time to post (within 5 minutes)
                if abs((current_time - scheduled_time).total_seconds()) <= 300:
                    result = self._execute_single_post(post)
                    results['posts'].append(result)

                    if result['success']:
                        results['executed'] += 1
                    else:
                        results['failed'] += 1

            return results

        except Exception as e:
            logger.error(f"❌ Error executing scheduled posts: {e}")
            return {'error': str(e)}

    def _execute_single_post(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single scheduled post"""
        try:
            # Generate content image
            image_path = self.content_generator.create_post_image(
                template=post['template'],
                data=post['data']
            )

            # Create caption
            caption = self._create_caption(post)

            # Upload to Instagram
            media = self.safe_action(
                'post',
                self.client.photo_upload,
                image_path,
                caption
            )

            if media:
                return {
                    'content_id': post['content_id'],
                    'media_id': media.pk,
                    'success': True,
                    'posted_at': datetime.now().isoformat()
                }
            else:
                return {
                    'content_id': post['content_id'],
                    'success': False,
                    'error': 'Upload failed'
                }

        except Exception as e:
            return {
                'content_id': post['content_id'],
                'success': False,
                'error': str(e)
            }

    def _create_caption(self, post: Dict[str, Any]) -> str:
        """Create Instagram caption from post data"""
        data = post['data']
        hashtags = post['hashtags']

        caption_parts = []

        if 'title' in data:
            caption_parts.append(data['title'])

        if 'description' in data:
            caption_parts.append(data['description'])

        caption_parts.append(hashtags)

        return '\n\n'.join(caption_parts)

    def _load_scheduled_posts(self) -> List[Dict[str, Any]]:
        """Load scheduled posts from storage"""
        posts_file = Path("data/scheduled_posts.json")

        if posts_file.exists():
            try:
                with open(posts_file, 'r') as f:
                    return json.load(f)
            except:
                pass

        return []

    def analyze_optimal_times(self) -> Dict[str, Any]:
        """Analyze follower activity to determine optimal posting times"""
        try:
            if not self.initialize_session():
                return {'error': 'Session initialization failed'}

            # Get account insights (simplified analysis)
            user_info = self.client.user_info_by_username(self.client.username)

            # Analyze recent posts performance by time
            recent_posts = self.client.user_medias(user_info.pk, amount=20)
            time_analysis = {}

            for post in recent_posts:
                hour = post.taken_at.hour
                engagement = post.like_count + post.comment_count

                if hour not in time_analysis:
                    time_analysis[hour] = {'total_engagement': 0, 'post_count': 0}

                time_analysis[hour]['total_engagement'] += engagement
                time_analysis[hour]['post_count'] += 1

            # Calculate average engagement by hour
            optimal_analysis = {}
            for hour, data in time_analysis.items():
                avg_engagement = data['total_engagement'] / data['post_count']
                optimal_analysis[hour] = avg_engagement

            # Sort by engagement
            sorted_hours = sorted(optimal_analysis.items(), key=lambda x: x[1], reverse=True)

            return {
                'optimal_hours': sorted_hours[:5],
                'analysis_data': time_analysis,
                'recommendations': self._generate_timing_recommendations(sorted_hours)
            }

        except Exception as e:
            logger.error(f"❌ Error analyzing optimal times: {e}")
            return {'error': str(e)}

    def _generate_timing_recommendations(self, sorted_hours: List) -> List[str]:
        """Generate timing recommendations based on analysis"""
        recommendations = []

        if sorted_hours:
            best_hour = sorted_hours[0][0]
            recommendations.append(f"Best performing hour: {best_hour}:00")

            # Group by time periods
            morning_hours = [h for h, _ in sorted_hours if 6 <= h <= 11]
            afternoon_hours = [h for h, _ in sorted_hours if 12 <= h <= 17]
            evening_hours = [h for h, _ in sorted_hours if 18 <= h <= 23]

            if morning_hours:
                recommendations.append(f"Best morning time: {morning_hours[0]}:00")
            if afternoon_hours:
                recommendations.append(f"Best afternoon time: {afternoon_hours[0]}:00")
            if evening_hours:
                recommendations.append(f"Best evening time: {evening_hours[0]}:00")

        return recommendations

    def run(self) -> Dict[str, Any]:
        """Main automation workflow"""
        logger.info("🚀 Starting Post Scheduler automation")

        results = {
            'status': 'completed',
            'actions': []
        }

        try:
            # Execute any scheduled posts
            execution_results = self.execute_scheduled_posts()
            results['actions'].append({
                'action': 'execute_scheduled_posts',
                'results': execution_results
            })

            # Analyze optimal times
            timing_analysis = self.analyze_optimal_times()
            results['actions'].append({
                'action': 'analyze_optimal_times',
                'results': timing_analysis
            })

            # Get action statistics
            results['action_stats'] = self.get_action_stats()

            logger.info("✅ Post Scheduler automation completed")
            return results

        except Exception as e:
            logger.error(f"❌ Post Scheduler automation failed: {e}")
            return {'status': 'failed', 'error': str(e)}

# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize scheduler
    scheduler = PostScheduler()

    # Add example content to queue
    example_content = [
        {
            'type': 'educational',
            'template': 'basic_post',
            'data': {
                'title': 'Instagram Growth Tips',
                'subtitle': 'Boost Your Engagement',
                'description': 'Learn proven strategies to grow your Instagram following organically',
                'metric1_value': '500%',
                'metric1_label': 'Growth',
                'metric2_value': '10K',
                'metric2_label': 'Followers',
                'metric3_value': '85%',
                'metric3_label': 'Engagement',
                'hashtags': '#instagramgrowth #socialmedia #contentcreator'
            }
        },
        {
            'type': 'promotional',
            'template': 'basic_post',
            'data': {
                'title': 'New Course Launch',
                'subtitle': 'Instagram Mastery 2024',
                'description': 'Everything you need to know about Instagram success',
                'metric1_value': '50%',
                'metric1_label': 'Discount',
                'metric2_value': '24H',
                'metric2_label': 'Only',
                'metric3_value': '100+',
                'metric3_label': 'Students',
                'hashtags': '#course #instagram #marketing #launch'
            }
        }
    ]

    # Add content to queue
    for content in example_content:
        scheduler.add_content_to_queue(content)

    # Schedule content
    scheduled = scheduler.schedule_content(days_ahead=3)
    print(f"📅 Scheduled {len(scheduled)} posts")

    # Run analysis
    results = scheduler.run()
    print(f"📊 Automation Results: {results['status']}")