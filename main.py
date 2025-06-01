import argparse
import os
from script_gen import generate_script
from voice_gen import generate_voice
from image_gen import get_background_image
from video_gen import create_video
from upload_youtube import upload_to_youtube
from utils import clean_temp_files, setup_directories
import config

def run_full_pipeline(topic: str = None):
    """Run the complete YouTube Shorts creation pipeline"""
    print("🚀 Starting YouTube Shorts Bot Pipeline...")
    
    # Setup directories
    setup_directories()
    
    # Use default topic if none provided
    if not topic:
        topic = config.DEFAULT_TOPIC
    
    try:
        # Step 1: Generate script
        print(f"📝 Generating script for topic: {topic}")
        script = generate_script(topic)
        print(f"✅ Script generated: {script[:100]}...")
        
        # Step 2: Generate voice narration
        print("🗣️ Converting script to voice...")
        audio_path = generate_voice(script, config.TEMP_AUDIO_PATH)
        print(f"✅ Voice generated: {audio_path}")
        
        # Step 3: Get background image
        print("🖼️ Fetching background image...")
        image_path = get_background_image(topic, config.TEMP_IMAGE_PATH)
        print(f"✅ Image ready: {image_path}")
        
        # Step 4: Create video
        print("🎬 Creating video...")
        video_path = create_video(image_path, audio_path, config.TEMP_VIDEO_PATH)
        print(f"✅ Video created: {video_path}")
        
        # Step 5: Upload to YouTube
        if config.UPLOAD_TO_YOUTUBE:
            print("📤 Uploading to YouTube...")
            title = f"{topic} - AI Generated Short"
            description = f"An AI-generated short video about {topic}\n\n#shorts #ai #automation"
            upload_to_youtube(video_path, title, description)
            print("✅ Video uploaded to YouTube!")
        else:
            print("⏭️ Skipping YouTube upload (disabled in config)")
        
        print("🎉 Pipeline completed successfully!")
        
    except Exception as e:
        print(f"❌ Pipeline failed: {str(e)}")
        raise
    
    finally:
        # Clean up temporary files
        if config.CLEAN_TEMP_FILES:
            clean_temp_files()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI-Powered YouTube Shorts Bot")
    parser.add_argument("--topic", type=str, help="Topic for the video")
    args = parser.parse_args()
    
    run_full_pipeline(args.topic)
