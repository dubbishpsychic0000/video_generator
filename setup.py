#!/usr/bin/env python3
"""
Setup script for YouTube Shorts Bot
This script helps you set up the bot with all necessary API keys and configurations.
"""

import os
import shutil
import sys
from getpass import getpass

def print_header():
    print("=" * 60)
    print("🎬 YOUTUBE SHORTS BOT SETUP")
    print("=" * 60)
    print()

def check_dependencies():
    """Check if all required packages are installed"""
    print("📦 Checking dependencies...")
    
    try:
        import google.generativeai
        import gtts
        import moviepy
        from PIL import Image
        import requests
        from dotenv import load_dotenv
        print("✅ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_directories():
    """Create necessary directories"""
    print("📁 Setting up directories...")
    
    dirs = ['temp', 'credentials', 'output']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✅ Created directory: {dir_name}")

def setup_env_file():
    """Setup environment variables"""
    print("\n🔑 Setting up API keys...")
    print("You'll need to get these API keys:")
    print("1. Gemini AI API Key: https://makersuite.google.com/app/apikey")
    print("2. Pexels API Key (optional): https://www.pexels.com/api/")
    print("3. YouTube API credentials: https://console.cloud.google.com/")
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("❓ .env file already exists. Overwrite? (y/n): ").lower()
        if overwrite != 'y':
            print("⏭️ Skipping .env setup")
            return
    
    # Get API keys
    gemini_key = getpass("Enter your Gemini API Key (required): ").strip()
    if not gemini_key:
        print("❌ Gemini API Key is required!")
        return False
    
    pexels_key = input("Enter your Pexels API Key (optional, press Enter to skip): ").strip()
    youtube_client_id = input("Enter YouTube Client ID (optional, press Enter to skip): ").strip()
    youtube_client_secret = getpass("Enter YouTube Client Secret (optional): ").strip()
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(f"# API Keys for YouTube Shorts Bot\n")
        f.write(f"GEMINI_API_KEY={gemini_key}\n")
        f.write(f"PEXELS_API_KEY={pexels_key}\n")
        f.write(f"YOUTUBE_CLIENT_ID={youtube_client_id}\n")
        f.write(f"YOUTUBE_CLIENT_SECRET={youtube_client_secret}\n")
    
    print("✅ .env file created successfully!")
    return True

def test_setup():
    """Test the setup by generating a sample script"""
    print("\n🧪 Testing setup...")
    
    try:
        from script_gen import generate_script
        
        test_script = generate_script("testing the AI setup")
        if test_script and len(test_script) > 20:
            print("✅ Script generation test passed!")
            print(f"Sample script: {test_script[:100]}...")
            return True
        else:
            print("❌ Script generation test failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def setup_youtube_credentials():
    """Guide user through YouTube API setup"""
    print("\n📺 YouTube API Setup Guide:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Create a new project or select an existing one")
    print("3. Enable the YouTube Data API v3")
    print("4. Create credentials (OAuth 2.0 client ID)")
    print("5. Download the JSON file and save it as 'credentials/client_secrets.json'")
    print()
    
    if input("Have you completed the YouTube API setup? (y/n): ").lower() == 'y':
        client_secrets_path = 'credentials/client_secrets.json'
        if os.path.exists(client_secrets_path):
            print("✅ YouTube credentials found!")
            return True
        else:
            print("❌ client_secrets.json not found in credentials/")
            print("Please download it from Google Cloud Console")
            return False
    else:
        print("⏭️ YouTube API setup skipped - you can do this later")
        return False

def show_usage_guide():
    """Show how to use the bot"""
    print("\n" + "=" * 60)
    print("🚀 SETUP COMPLETE! Here's how to use your bot:")
    print("=" * 60)
    print()
    print("📝 Generate a single video:")
    print("   python main.py --topic 'your topic here'")
    print()
    print("🔄 Run with default topic:")
    print("   python main.py")
    print()
    print("⏰ Run scheduler for daily uploads:")
    print("   python scheduler.py")
    print()
    print("🧪 Test individual components:")
    print("   python script_gen.py")
    print("   python voice_gen.py")
    print("   python image_gen.py")
    print()
    print("⚠️  Important Notes:")
    print("   - Set UPLOAD_TO_YOUTUBE=True in config.py when ready to upload")
    print("   - Complete YouTube API setup for automatic uploads")
    print("   - First YouTube upload will require browser authentication")
    print()

def main():
    print_header()
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        sys.exit(1)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Setup directories
    setup_directories()
    
    # Step 3: Setup environment variables
    if not setup_env_file():
        sys.exit(1)
    
    # Step 4: Test basic functionality
    if not test_setup():
        print("⚠️  Basic test failed, but you can still proceed")
    
    # Step 5: YouTube setup (optional)
    setup_youtube_credentials()
    
    # Step 6: Show usage guide
    show_usage_guide()
    
    print("🎉 Setup completed successfully!")
    print("Happy creating! 🎬✨")

if __name__ == "__main__":
    main()
