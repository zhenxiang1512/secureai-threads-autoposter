#!/usr/bin/env python3
"""
Threads Auto Poster CLI
Simple command-line interface for managing automated Threads posts
"""

import argparse
import sys
from threads_autoposter import ThreadsAutoPoster

def main():
    parser = argparse.ArgumentParser(description='Automated Threads Poster for Secure LLM content')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Post single command
    post_parser = subparsers.add_parser('post', help='Post a single message')
    post_parser.add_argument('--id', type=int, help='Post ID to publish (optional)')
    
    # Schedule command
    schedule_parser = subparsers.add_parser('schedule', help='Start automated scheduling')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test API connection')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all available posts')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    poster = ThreadsAutoPoster()
    
    if args.command == 'post':
        if args.id:
            success = poster.post_single(args.id)
        else:
            success = poster.post_single()
        
        if success:
            print("✅ Post published successfully!")
        else:
            print("❌ Failed to publish post")
            sys.exit(1)
    
    elif args.command == 'schedule':
        print("🕐 Starting automated scheduler...")
        poster.run_scheduler()
    
    elif args.command == 'test':
        user_id = poster.get_user_id()
        if user_id:
            print(f"✅ API connection successful! User ID: {user_id}")
        else:
            print("❌ API connection failed")
            sys.exit(1)
    
    elif args.command == 'list':
        print("\n📋 Available Posts:")
        print("-" * 50)
        for post in poster.posts:
            print(f"ID: {post['id']} | Category: {post['category']}")
            print(f"Content: {post['content'][:80]}...")
            print(f"Hashtags: {', '.join(post['hashtags'][:3])}...")
            print("-" * 50)

if __name__ == "__main__":
    main()