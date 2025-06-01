import argparse
import os
import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import google.generativeai
    except ImportError:
        missing_deps.append('google-generativeai')
    
    try:
        import gtts
    except ImportError:
        missing_deps.append('gtts')
    
    try:
        import moviepy.editor
    except ImportError:
        missing_deps.append('moviepy')
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append('Pillow')
    
    try:
        import requests
    except ImportError:
        missing_deps.append('requests')
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main function with proper error handling"""
    print("🚀 Starting YouTube Shorts Bot Pipeline...")
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    # Now import our modules after dependency check
    try:
        from script_gen import generate_script
        from voice_gen import generate_voice
        from image_gen import get_background_image
        from video_gen import create_video
        from upload_youtube import upload_to_youtube
        from utils import clean_temp_files, setup_directories
        import config
    except ImportError as e:
        print(f"❌ Failed to import modules: {e}")
        sys.exit(1)
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="AI-Powered YouTube Shorts Bot")
    parser.add_argument("--topic", type=str, help="Topic for the video")
    args = parser.parse_args()
    
    # Run the pipeline
    run_full_pipeline(args.topic)

def run_full_pipeline(topic: str = None):
    """Run the complete YouTube Shorts creation pipeline"""
    # Import here to avoid import issues
    from script_gen import generate_script
    from voice_gen import generate_voice
    from image_gen import get_background_image
    from video_gen import create_video
    from upload_youtube import upload_to_youtube
    from utils import clean_temp_files, setup_directories
    import config
    
    # Setup directories
    setup_directories()
    
    # Use default topic if none provided
    if not topic:
        topic = config.DEFAULT_TOPIC
    
    try:
        # Step 1: Generate script
        print(f"📝 Generating script for topic: {topic}")
        script = generate_script(topic)
        if not script or len(script) < 20:
            raise ValueError("Generated script is too short or empty")
        print(f"✅ Script generated ({len(script.split())} words): {script[:100]}...")
        
        # Step 2: Generate voice narration
        print("🗣️ Converting script to voice...")
        audio_path = generate_voice(script, config.TEMP_AUDIO_PATH)
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not created at {audio_path}")
        print(f"✅ Voice generated: {audio_path}")
        
        # Step 3: Get background image
        print("🖼️ Fetching background image...")
        image_path = get_background_image(topic, config.TEMP_IMAGE_PATH)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not created at {image_path}")
        print(f"✅ Image ready: {image_path}")
        
        # Step 4: Create video
        print("🎬 Creating video...")
        video_path = create_video(image_path, audio_path, config.TEMP_VIDEO_PATH)
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not created at {video_path}")
        
        # Get video file size
        video_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        print(f"✅ Video created: {video_path} ({video_size:.1f} MB)")
        
        # Step 5: Upload to YouTube
        if config.UPLOAD_TO_YOUTUBE:
            print("📤 Uploading to YouTube...")
            title = f"{topic} - AI Generated Short"
            description = f"An AI-generated short video about {topic}\n\n#shorts #ai #automation"
            
            # Check if YouTube credentials exist
            if not os.path.exists('credentials/client_secrets.json'):
                print("⚠️ YouTube credentials not found. Skipping upload.")
                print("To enable uploads, add credentials/client_secrets.json")
            else:
                upload_to_youtube(video_path, title, description)
                print("✅ Video uploaded to YouTube!")
        else:
            print("⏭️ Skipping YouTube upload (disabled in config)")
        
        print("🎉 Pipeline completed successfully!")
        print(f"📁 Video saved at: {video_path}")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        
        # Print more detailed error for debugging
        import traceback
        print("\n🔍 Detailed error information:")
        traceback.print_exc()
        
        raise
    
    finally:
        # Clean up temporary files
        if hasattr(config, 'CLEAN_TEMP_FILES') and config.CLEAN_TEMP_FILES:
            print("🧹 Cleaning up temporary files...")
            clean_temp_files()

if __name__ == "__main__":
    main()
