import json
import requests
import os
import time
import schedule
import logging
from datetime import datetime
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

class ThreadsAutoPoster:
    def __init__(self):
        self.app_id = os.getenv('THREADS_APP_ID')
        self.app_secret = os.getenv('THREADS_APP_SECRET')
        self.user_id = os.getenv('THREADS_USER_ID')
        self.access_token = os.getenv('THREADS_LONG_LIVED_TOKEN')
        self.base_url = "https://graph.threads.net"
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('threads_poster.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load posts content
        self.load_posts_content()
        self.current_post_index = 0
        
    def load_posts_content(self):
        """Load posts from JSON file"""
        try:
            with open('posts_content.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.posts = data['posts']
                self.settings = data['settings']
                self.schedule_config = data['posting_schedule']
                self.logger.info(f"Loaded {len(self.posts)} posts from JSON file")
        except FileNotFoundError:
            self.logger.error("posts_content.json file not found")
            self.posts = []
        except json.JSONDecodeError:
            self.logger.error("Invalid JSON format in posts_content.json")
            self.posts = []
    
    def get_user_id(self):
        """Get user ID if not set in environment"""
        if not self.user_id:
            url = f"{self.base_url}/v1.0/me"
            params = {
                'fields': 'id,username',
                'access_token': self.access_token
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                user_data = response.json()
                self.user_id = user_data['id']
                self.logger.info(f"Retrieved user ID: {self.user_id}")
                return self.user_id
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Error getting user ID: {e}")
                return None
        return self.user_id
    
    def create_media_container(self, text_content):
        """Create a media container for the post"""
        if not self.user_id:
            self.user_id = self.get_user_id()
            if not self.user_id:
                return None
        
        url = f"{self.base_url}/v1.0/{self.user_id}/threads"
        
        payload = {
            'media_type': 'TEXT',
            'text': text_content,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            result = response.json()
            return result.get('id')
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error creating media container: {e}")
            if hasattr(e, 'response') and e.response:
                self.logger.error(f"Response: {e.response.text}")
            return None
    
    def publish_container(self, creation_id):
        """Publish the media container"""
        if not self.user_id:
            return None
            
        url = f"{self.base_url}/v1.0/{self.user_id}/threads_publish"
        
        payload = {
            'creation_id': creation_id,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            result = response.json()
            return result.get('id')
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error publishing container: {e}")
            if hasattr(e, 'response') and e.response:
                self.logger.error(f"Response: {e.response.text}")
            return None
    
    def post_to_threads(self, content):
        """Post content to Threads"""
        self.logger.info(f"Attempting to post: {content[:50]}...")
        
        # Create media container
        creation_id = self.create_media_container(content)
        if not creation_id:
            self.logger.error("Failed to create media container")
            return False
        
        self.logger.info(f"Created media container: {creation_id}")
        
        # Wait a moment before publishing
        time.sleep(2)
        
        # Publish the container
        post_id = self.publish_container(creation_id)
        if post_id:
            self.logger.info(f"Successfully published post: {post_id}")
            return True
        else:
            self.logger.error("Failed to publish post")
            return False
    
    def get_next_post(self):
        """Get the next post to publish"""
        if not self.posts:
            self.logger.error("No posts available")
            return None
        
        if self.settings.get('randomize_order', False):
            post = random.choice(self.posts)
        else:
            post = self.posts[self.current_post_index % len(self.posts)]
            self.current_post_index += 1
        
        return post
    
    def schedule_posts(self):
        """Schedule posts based on configuration"""
        posting_time = self.schedule_config.get('time', '09:00')
        frequency = self.schedule_config.get('frequency', 'daily')
        
        if frequency == 'daily':
            schedule.every().day.at(posting_time).do(self.post_scheduled_content)
        elif frequency == 'hourly':
            schedule.every().hour.do(self.post_scheduled_content)
        elif frequency == 'weekly':
            schedule.every().week.do(self.post_scheduled_content)
        
        self.logger.info(f"Scheduled posts to run {frequency} at {posting_time}")
    
    def post_scheduled_content(self):
        """Post the next scheduled content"""
        post = self.get_next_post()
        if post:
            content = post['content']
            if self.post_to_threads(content):
                self.logger.info(f"Successfully posted: {post['category']} - {post['id']}")
            else:
                self.logger.error(f"Failed to post: {post['category']} - {post['id']}")
    
    def post_single(self, post_id=None):
        """Post a single post by ID or get next post"""
        if post_id:
            post = next((p for p in self.posts if p['id'] == post_id), None)
            if not post:
                self.logger.error(f"Post with ID {post_id} not found")
                return False
        else:
            post = self.get_next_post()
        
        if post:
            content = post['content']
            return self.post_to_threads(content)
        return False
    
    def run_scheduler(self):
        """Run the scheduler"""
        self.schedule_posts()
        self.logger.info("Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")

if __name__ == "__main__":
    poster = ThreadsAutoPoster()
    
    # Example usage:
    # Post a single post
    # poster.post_single(1)  # Post by ID
    # poster.post_single()   # Post next in sequence
    
    # Run scheduler for automated posting
    poster.run_scheduler()