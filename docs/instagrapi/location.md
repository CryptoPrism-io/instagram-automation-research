# Instagrapi Location Documentation

> **Source**: https://subzeroid.github.io/instagrapi/usage-guide/location.html

This document provides comprehensive information about location-related operations using the instagrapi library for Instagram's Private API.

## 📍 Location Information Methods

### Basic Location Operations

#### Search Locations by Coordinates
```python
from instagrapi import Client

cl = Client()
cl.login(USERNAME, PASSWORD)

# Search locations by latitude and longitude
latitude = 59.96  # Example: St. Petersburg
longitude = 30.29

locations = cl.location_search(latitude, longitude)

for location in locations:
    print(f"Location: {location.name}")
    print(f"Address: {location.address}")
    print(f"Location ID: {location.pk}")
    print(f"Coordinates: {location.lat}, {location.lng}")
    print("---")
```

#### Get Location Information
```python
# Get detailed information about a specific location
location_pk = 123456789  # Location primary key
location_info = cl.location_info(location_pk)

print(f"Name: {location_info.name}")
print(f"Address: {location_info.address}")
print(f"City: {location_info.city}")
print(f"Coordinates: {location_info.lat}, {location_info.lng}")
print(f"External ID: {location_info.external_id}")
print(f"External Source: {location_info.external_id_source}")
```

#### Complete Location Information
```python
# Fill in missing location details
incomplete_location = locations[0]
complete_location = cl.location_complete(incomplete_location)

print(f"Complete name: {complete_location.name}")
print(f"Complete address: {complete_location.address}")
```

### Advanced Location Search

#### Search Places via Facebook
```python
# Search places using Facebook Search (more comprehensive)
query = "Starbucks"
latitude = 40.7128  # New York City
longitude = -74.0060

places = cl.fbsearch_places(query, latitude, longitude)

for place in places:
    print(f"Place: {place.name}")
    print(f"Category: {place.category}")
    print(f"Distance: {place.distance} meters")
    print(f"Location ID: {place.location.pk}")
```

#### Search Locations by Name and Area
```python
def search_locations_by_area(city_name, search_radius=5000):
    """Search for locations within a city area"""
    # First, find the city coordinates (you'd need a geocoding service)
    city_coords = get_city_coordinates(city_name)  # Implement this function

    if not city_coords:
        return []

    lat, lng = city_coords
    locations = cl.location_search(lat, lng)

    # Filter by radius if needed
    nearby_locations = []
    for location in locations:
        if location.lat and location.lng:
            distance = calculate_distance(lat, lng, location.lat, location.lng)
            if distance <= search_radius:
                nearby_locations.append({
                    'location': location,
                    'distance': distance
                })

    return sorted(nearby_locations, key=lambda x: x['distance'])

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two coordinates in meters"""
    from math import radians, cos, sin, asin, sqrt

    # Convert to radians
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])

    # Haversine formula
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius of earth in meters
    return c * r

def get_city_coordinates(city_name):
    """Get coordinates for a city (implement with geocoding service)"""
    # You would implement this with a geocoding service like:
    # - Google Geocoding API
    # - OpenStreetMap Nominatim
    # - etc.
    city_coords = {
        'new york': (40.7128, -74.0060),
        'london': (51.5074, -0.1278),
        'paris': (48.8566, 2.3522),
        'tokyo': (35.6762, 139.6503)
    }
    return city_coords.get(city_name.lower())
```

## 📱 Location Media Operations

### Get Media from Locations

#### Get Top Media for Location
```python
# Get most popular posts from a location
location_pk = 123456789
top_medias = cl.location_medias_top(location_pk, amount=20)

for media in top_medias:
    print(f"Top Post: {media.code}")
    print(f"User: {media.user.username}")
    print(f"Likes: {media.like_count}")
    print(f"Caption: {media.caption_text[:100]}...")
```

#### Get Recent Media for Location
```python
# Get recent posts from a location
recent_medias = cl.location_medias_recent(location_pk, amount=50)

for media in recent_medias:
    print(f"Recent Post: {media.code}")
    print(f"Posted: {media.taken_at}")
    print(f"User: {media.user.username}")
```

#### Advanced Location Media Analysis
```python
def analyze_location_content(location_pk, days=30):
    """Analyze content posted at a location"""
    from datetime import datetime, timedelta

    # Get recent media
    recent_medias = cl.location_medias_recent(location_pk, amount=200)

    # Filter by date range
    cutoff_date = datetime.now() - timedelta(days=days)
    filtered_medias = [
        media for media in recent_medias
        if media.taken_at > cutoff_date
    ]

    if not filtered_medias:
        return {"error": "No recent media found"}

    # Analyze content
    analysis = {
        'total_posts': len(filtered_medias),
        'unique_users': len(set(media.user.pk for media in filtered_medias)),
        'total_engagement': sum(m.like_count + m.comment_count for m in filtered_medias),
        'media_types': analyze_media_types(filtered_medias),
        'posting_times': analyze_posting_times(filtered_medias),
        'top_users': get_top_users_at_location(filtered_medias),
        'engagement_stats': calculate_engagement_stats(filtered_medias)
    }

    return analysis

def analyze_media_types(medias):
    """Analyze distribution of media types"""
    types = {'photo': 0, 'video': 0, 'carousel': 0}

    for media in medias:
        if media.media_type == 1:
            types['photo'] += 1
        elif media.media_type == 2:
            types['video'] += 1
        elif media.media_type == 8:
            types['carousel'] += 1

    total = len(medias)
    return {
        media_type: {'count': count, 'percentage': (count / total) * 100}
        for media_type, count in types.items()
    }

def analyze_posting_times(medias):
    """Analyze best posting times for location"""
    hour_counts = {}
    day_counts = {}

    for media in medias:
        hour = media.taken_at.hour
        day = media.taken_at.strftime('%A')

        hour_counts[hour] = hour_counts.get(hour, 0) + 1
        day_counts[day] = day_counts.get(day, 0) + 1

    return {
        'best_hours': sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:5],
        'best_days': sorted(day_counts.items(), key=lambda x: x[1], reverse=True)
    }

def get_top_users_at_location(medias):
    """Get users who post most frequently at location"""
    user_stats = {}

    for media in medias:
        user_id = media.user.pk
        username = media.user.username

        if user_id not in user_stats:
            user_stats[user_id] = {
                'username': username,
                'post_count': 0,
                'total_engagement': 0
            }

        user_stats[user_id]['post_count'] += 1
        user_stats[user_id]['total_engagement'] += media.like_count + media.comment_count

    # Sort by post count
    return sorted(
        user_stats.values(),
        key=lambda x: x['post_count'],
        reverse=True
    )[:10]

def calculate_engagement_stats(medias):
    """Calculate engagement statistics"""
    if not medias:
        return {}

    engagements = [m.like_count + m.comment_count for m in medias]
    likes = [m.like_count for m in medias]
    comments = [m.comment_count for m in medias]

    return {
        'avg_engagement': sum(engagements) / len(engagements),
        'max_engagement': max(engagements),
        'min_engagement': min(engagements),
        'avg_likes': sum(likes) / len(likes),
        'avg_comments': sum(comments) / len(comments),
        'engagement_rate_distribution': calculate_engagement_distribution(engagements)
    }

def calculate_engagement_distribution(engagements):
    """Calculate engagement distribution ranges"""
    if not engagements:
        return {}

    ranges = {
        '0-100': 0,
        '100-500': 0,
        '500-1000': 0,
        '1000-5000': 0,
        '5000+': 0
    }

    for engagement in engagements:
        if engagement <= 100:
            ranges['0-100'] += 1
        elif engagement <= 500:
            ranges['100-500'] += 1
        elif engagement <= 1000:
            ranges['500-1000'] += 1
        elif engagement <= 5000:
            ranges['1000-5000'] += 1
        else:
            ranges['5000+'] += 1

    total = len(engagements)
    return {
        range_name: {'count': count, 'percentage': (count / total) * 100}
        for range_name, count in ranges.items()
    }
```

## 🗺️ Location Discovery & Research

### Find Trending Locations
```python
def find_trending_locations_in_area(center_lat, center_lng, radius=10000):
    """Find trending locations in an area"""
    locations = cl.location_search(center_lat, center_lng)
    trending_data = []

    for location in locations:
        try:
            # Get recent activity
            recent_medias = cl.location_medias_recent(location.pk, amount=50)

            if len(recent_medias) < 10:  # Skip locations with low activity
                continue

            # Calculate trend score
            trend_score = calculate_location_trend_score(recent_medias)

            trending_data.append({
                'location': location,
                'recent_posts': len(recent_medias),
                'trend_score': trend_score,
                'avg_engagement': sum(m.like_count + m.comment_count for m in recent_medias) / len(recent_medias)
            })

        except Exception as e:
            print(f"Error analyzing location {location.name}: {e}")
            continue

    # Sort by trend score
    return sorted(trending_data, key=lambda x: x['trend_score'], reverse=True)

def calculate_location_trend_score(medias):
    """Calculate trending score based on recent activity"""
    from datetime import datetime, timedelta

    if not medias:
        return 0

    now = datetime.now()
    recent_24h = [m for m in medias if (now - m.taken_at).total_seconds() < 86400]
    recent_7d = [m for m in medias if (now - m.taken_at).total_seconds() < 604800]

    # Score based on recent activity density
    score = len(recent_24h) * 10 + len(recent_7d) * 2

    # Boost score for high engagement
    if recent_24h:
        avg_engagement = sum(m.like_count + m.comment_count for m in recent_24h) / len(recent_24h)
        score += avg_engagement / 100

    return score
```

### Location Competitor Analysis
```python
def analyze_competitor_locations(competitor_usernames):
    """Analyze locations where competitors post"""
    competitor_locations = {}

    for username in competitor_usernames:
        try:
            user_id = cl.user_id_from_username(username)
            user_medias = cl.user_medias(user_id, amount=50)

            locations = []
            for media in user_medias:
                if media.location:
                    locations.append({
                        'location': media.location,
                        'engagement': media.like_count + media.comment_count,
                        'media_id': media.id
                    })

            competitor_locations[username] = locations

        except Exception as e:
            print(f"Error analyzing {username}: {e}")

    return analyze_location_overlap(competitor_locations)

def analyze_location_overlap(competitor_locations):
    """Find locations used by multiple competitors"""
    location_usage = {}

    for username, locations in competitor_locations.items():
        for loc_data in locations:
            location_pk = loc_data['location'].pk
            location_name = loc_data['location'].name

            if location_pk not in location_usage:
                location_usage[location_pk] = {
                    'name': location_name,
                    'users': [],
                    'total_posts': 0,
                    'avg_engagement': 0,
                    'engagements': []
                }

            location_usage[location_pk]['users'].append(username)
            location_usage[location_pk]['total_posts'] += 1
            location_usage[location_pk]['engagements'].append(loc_data['engagement'])

    # Calculate averages and popularity
    for location_pk, data in location_usage.items():
        data['user_count'] = len(set(data['users']))
        data['avg_engagement'] = sum(data['engagements']) / len(data['engagements'])
        data['popularity_score'] = data['user_count'] * data['total_posts']

    # Sort by popularity
    return sorted(
        location_usage.values(),
        key=lambda x: x['popularity_score'],
        reverse=True
    )
```

## 📍 Location-Based Content Strategy

### Optimal Location Selection
```python
def find_optimal_locations_for_niche(niche_hashtags, target_audience_location):
    """Find best locations for a specific niche"""
    # Get center coordinates for target audience
    center_coords = get_city_coordinates(target_audience_location)
    if not center_coords:
        return []

    lat, lng = center_coords
    locations = cl.location_search(lat, lng)

    location_scores = []

    for location in locations:
        try:
            # Get recent media from location
            recent_medias = cl.location_medias_recent(location.pk, amount=30)

            if not recent_medias:
                continue

            # Calculate niche relevance
            niche_score = calculate_niche_relevance(recent_medias, niche_hashtags)

            # Calculate engagement potential
            avg_engagement = sum(m.like_count + m.comment_count for m in recent_medias) / len(recent_medias)

            # Calculate competition level
            unique_users = len(set(m.user.pk for m in recent_medias))
            competition_score = len(recent_medias) / unique_users if unique_users > 0 else 0

            overall_score = (niche_score * 0.4) + (avg_engagement * 0.4) + ((1 / competition_score) * 0.2)

            location_scores.append({
                'location': location,
                'niche_relevance': niche_score,
                'avg_engagement': avg_engagement,
                'competition_level': competition_score,
                'overall_score': overall_score,
                'recent_posts': len(recent_medias)
            })

        except Exception as e:
            continue

    return sorted(location_scores, key=lambda x: x['overall_score'], reverse=True)

def calculate_niche_relevance(medias, niche_hashtags):
    """Calculate how relevant location is to niche"""
    relevant_posts = 0

    for media in medias:
        if media.caption_text:
            caption_lower = media.caption_text.lower()
            for hashtag in niche_hashtags:
                if f"#{hashtag.lower()}" in caption_lower:
                    relevant_posts += 1
                    break

    return relevant_posts / len(medias) if medias else 0
```

### Location Content Calendar
```python
class LocationContentCalendar:
    def __init__(self, client):
        self.cl = client
        self.location_schedule = {}

    def create_location_rotation(self, locations, content_types):
        """Create a rotating schedule of locations"""
        import itertools

        # Create rotation pattern
        location_cycle = itertools.cycle(locations)
        content_cycle = itertools.cycle(content_types)

        calendar = {}
        for day in range(30):  # 30-day calendar
            location = next(location_cycle)
            content_type = next(content_cycle)

            calendar[day] = {
                'location': location,
                'content_type': content_type,
                'best_time': self.get_optimal_posting_time(location),
                'suggested_hashtags': self.get_location_hashtags(location)
            }

        return calendar

    def get_optimal_posting_time(self, location):
        """Get optimal posting time for location"""
        try:
            recent_medias = self.cl.location_medias_recent(location.pk, amount=50)
            posting_times = analyze_posting_times(recent_medias)
            return posting_times['best_hours'][0][0] if posting_times['best_hours'] else 12
        except:
            return 12  # Default to noon

    def get_location_hashtags(self, location):
        """Get popular hashtags for location"""
        try:
            recent_medias = self.cl.location_medias_recent(location.pk, amount=20)
            hashtags = set()

            for media in recent_medias:
                if media.caption_text:
                    # Extract hashtags from captions
                    import re
                    found_hashtags = re.findall(r'#(\w+)', media.caption_text.lower())
                    hashtags.update(found_hashtags[:5])  # Limit per post

            return list(hashtags)[:15]  # Return top 15

        except:
            return []

# Usage
calendar = LocationContentCalendar(cl)
locations = [location1, location2, location3]  # Your location objects
content_types = ['photo', 'video', 'carousel']
schedule = calendar.create_location_rotation(locations, content_types)
```

## 🎯 Location Marketing Tools

### Local Influencer Discovery
```python
def find_local_influencers(location_pk, min_followers=1000, max_followers=100000):
    """Find local influencers who post at specific locations"""
    # Get recent media from location
    recent_medias = cl.location_medias_recent(location_pk, amount=100)

    influencers = {}

    for media in recent_medias:
        user_id = media.user.pk
        username = media.user.username

        if user_id not in influencers:
            try:
                user_info = cl.user_info(user_id)

                # Filter by follower count
                if min_followers <= user_info.follower_count <= max_followers:
                    engagement_rate = calculate_user_engagement_rate(user_id)

                    influencers[user_id] = {
                        'username': username,
                        'followers': user_info.follower_count,
                        'engagement_rate': engagement_rate,
                        'posts_at_location': 1,
                        'avg_likes': media.like_count,
                        'is_business': user_info.is_business,
                        'is_verified': user_info.is_verified
                    }

            except Exception as e:
                continue
        else:
            # Update existing influencer data
            influencers[user_id]['posts_at_location'] += 1
            influencers[user_id]['avg_likes'] = (
                influencers[user_id]['avg_likes'] + media.like_count
            ) / 2

    # Sort by engagement rate and follower count
    return sorted(
        influencers.values(),
        key=lambda x: (x['engagement_rate'], x['followers']),
        reverse=True
    )

def calculate_user_engagement_rate(user_id):
    """Calculate user's average engagement rate"""
    try:
        user_medias = cl.user_medias(user_id, amount=12)
        user_info = cl.user_info(user_id)

        if not user_medias or user_info.follower_count == 0:
            return 0

        total_engagement = sum(m.like_count + m.comment_count for m in user_medias)
        avg_engagement = total_engagement / len(user_medias)

        return (avg_engagement / user_info.follower_count) * 100

    except:
        return 0
```

### Location Performance Tracking
```python
import json
from datetime import datetime

class LocationPerformanceTracker:
    def __init__(self, client):
        self.cl = client
        self.tracking_file = "location_performance.json"

    def track_post_at_location(self, media_id, location_pk):
        """Track performance of post at specific location"""
        try:
            media = self.cl.media_info(media_id)
            location = self.cl.location_info(location_pk)

            tracking_data = {
                'media_id': media_id,
                'location': {
                    'pk': location_pk,
                    'name': location.name,
                    'address': location.address
                },
                'initial_metrics': {
                    'likes': media.like_count,
                    'comments': media.comment_count,
                    'timestamp': datetime.now().isoformat()
                }
            }

            self._save_tracking_data(tracking_data)
            return tracking_data

        except Exception as e:
            print(f"Error tracking location post: {e}")
            return None

    def analyze_location_performance(self):
        """Analyze which locations perform best"""
        data = self._load_tracking_data()
        location_performance = {}

        for post in data:
            if 'updated_metrics' not in post:
                continue

            location_pk = post['location']['pk']
            location_name = post['location']['name']

            initial = post['initial_metrics']
            updated = post['updated_metrics']

            growth = (updated['likes'] + updated['comments']) - (initial['likes'] + initial['comments'])

            if location_pk not in location_performance:
                location_performance[location_pk] = {
                    'name': location_name,
                    'total_growth': 0,
                    'post_count': 0,
                    'avg_growth': 0
                }

            location_performance[location_pk]['total_growth'] += growth
            location_performance[location_pk]['post_count'] += 1

        # Calculate averages
        for location_data in location_performance.values():
            if location_data['post_count'] > 0:
                location_data['avg_growth'] = location_data['total_growth'] / location_data['post_count']

        return sorted(
            location_performance.values(),
            key=lambda x: x['avg_growth'],
            reverse=True
        )

    def _load_tracking_data(self):
        try:
            with open(self.tracking_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_tracking_data(self, data):
        existing_data = self._load_tracking_data()
        existing_data.append(data)

        with open(self.tracking_file, 'w') as f:
            json.dump(existing_data, f, indent=2)

# Usage
tracker = LocationPerformanceTracker(cl)
tracker.track_post_at_location(media_id, location_pk)
best_locations = tracker.analyze_location_performance()
```

## ⚠️ Best Practices for Location Usage

### Location Strategy Guidelines
```python
LOCATION_BEST_PRACTICES = {
    'selection': {
        'relevance': 'Choose locations relevant to your content',
        'audience': 'Consider where your target audience is located',
        'authenticity': 'Only tag locations where you actually are/were',
        'variety': 'Mix popular and niche locations'
    },
    'timing': {
        'peak_hours': 'Post when location audience is most active',
        'local_time': 'Consider local timezone of the location',
        'events': 'Leverage local events and happenings'
    },
    'engagement': {
        'local_hashtags': 'Use location-specific hashtags',
        'community': 'Engage with other local content',
        'stories': 'Use location stickers in Stories'
    }
}
```

### Location Safety & Privacy
```python
def safe_location_usage():
    """Guidelines for safe location usage"""
    return {
        'privacy_considerations': [
            'Avoid tagging exact home address',
            'Be mindful of personal safety',
            'Consider delayed posting for security',
            'Review location accuracy before posting'
        ],
        'fake_location_detection': [
            'Instagram can detect GPS spoofing',
            'Use only authentic locations',
            'Avoid suspicious location patterns'
        ],
        'business_considerations': [
            'Get permission for business locations',
            'Respect location owner policies',
            'Consider commercial usage rights'
        ]
    }

def validate_location_authenticity(location_pk, user_recent_locations):
    """Check if location fits user's travel pattern"""
    try:
        location = cl.location_info(location_pk)

        # Basic validation logic
        if not user_recent_locations:
            return True

        last_location = user_recent_locations[-1]
        distance = calculate_distance(
            last_location['lat'], last_location['lng'],
            location.lat, location.lng
        )

        # Flag if distance is suspiciously large for time period
        time_diff = (datetime.now() - last_location['timestamp']).total_seconds() / 3600  # hours
        max_reasonable_distance = time_diff * 800000  # ~800km/hour max reasonable travel

        return distance <= max_reasonable_distance

    except:
        return True  # Default to allow if validation fails
```

This comprehensive location documentation covers all aspects of working with Instagram locations through the instagrapi library, including search, analysis, content strategy, influencer discovery, and best practices for safe and effective location usage.