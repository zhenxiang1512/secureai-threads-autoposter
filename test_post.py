#!/usr/bin/env python3
"""
Test Script for Threads Auto Poster
Simple script to test posting a single message safely
"""

from threads_autoposter import ThreadsAutoPoster
import sys

def test_single_post():
    """Test posting a single message"""
    print("🧪 Testing Threads Auto Poster...")
    print("=" * 50)
    
    # Initialize the poster
    try:
        poster = ThreadsAutoPoster()
        print(f"✅ Successfully loaded {len(poster.posts)} posts from JSON")
    except Exception as e:
        print(f"❌ Failed to initialize poster: {e}")
        return False
    
    # Test API connection
    print("\n🔗 Testing API connection...")
    user_id = poster.get_user_id()
    if not user_id:
        print("❌ API connection failed")
        return False
    else:
        print(f"✅ API connection successful! User ID: {user_id}")
    
    # Show available posts
    print(f"\n📋 Available posts (showing first 3):")
    for i, post in enumerate(poster.posts[:3]):
        print(f"  {post['id']}: {post['category']} - {post['content'][:60]}...")
    
    # Ask user which post to test
    print(f"\n🎯 Choose a post to test:")
    print("1. Post ID 1 (Introduction)")
    print("2. Post ID 3 (Benefits/Stats)")
    print("3. Post ID 7 (Success Story)")
    print("4. Custom test message")
    print("0. Exit without posting")
    
    try:
        choice = input("\nEnter your choice (0-4): ").strip()
        
        if choice == "0":
            print("👍 Exiting without posting")
            return True
        elif choice == "1":
            post_id = 1
        elif choice == "2":
            post_id = 3
        elif choice == "3":
            post_id = 7
        elif choice == "4":
            # Custom test message
            print("\n📝 Testing with a simple message...")
            custom_content = "🧪 Test post from SecureAI Threads Auto Poster - Testing API integration for Malaysian business content! #TestPost #SecureAI #Malaysia"
            
            success = poster.post_to_threads(custom_content)
            if success:
                print("✅ Test post successful!")
                return True
            else:
                print("❌ Test post failed")
                return False
        else:
            print("❌ Invalid choice")
            return False
            
        # Post the selected message
        print(f"\n📤 Posting message with ID {post_id}...")
        success = poster.post_single(post_id)
        
        if success:
            print("✅ Test post successful!")
            print("💡 Check your Threads profile to see the posted message")
            return True
        else:
            print("❌ Test post failed")
            print("💡 Check threads_poster.log for detailed error information")
            return False
            
    except KeyboardInterrupt:
        print("\n\n👋 Test cancelled by user")
        return True
    except Exception as e:
        print(f"❌ Error during test: {e}")
        return False

def main():
    print("🚀 Threads Auto Poster - Test Script")
    print("This script will help you safely test posting to Threads")
    print("=" * 60)
    
    # Confirm before proceeding
    confirm = input("\n⚠️  This will post to your actual Threads account. Continue? (y/N): ").strip().lower()
    
    if confirm not in ['y', 'yes']:
        print("👍 Test cancelled - no posts will be made")
        sys.exit(0)
    
    success = test_single_post()
    
    if success:
        print(f"\n🎉 Test completed successfully!")
        print("💡 Your automated posting system is ready to use")
        print("💡 Run 'python cli.py schedule' to start automated posting")
    else:
        print(f"\n⚠️  Test had issues - check the logs")
        print("💡 Review threads_poster.log for detailed error information")
        sys.exit(1)

if __name__ == "__main__":
    main()