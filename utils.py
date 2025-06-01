import os
import shutil
import config

def setup_directories():
    """Create necessary directories"""
    os.makedirs(config.TEMP_DIR, exist_ok=True)
    os.makedirs('credentials', exist_ok=True)

def clean_temp_files():
    """Clean up temporary files"""
    temp_files = [
        config.TEMP_AUDIO_PATH,
        config.TEMP_IMAGE_PATH,
        config.TEMP_VIDEO_PATH
    ]
    
    for file_path in temp_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up: {file_path}")
            except Exception as e:
                print(f"Error cleaning {file_path}: {e}")

def validate_config():
    """Validate configuration and API keys"""
    required_vars = ['GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not getattr(config, var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Warning: Missing required environment variables: {missing_vars}")
        return False
    
    return True

def estimate_video_length(text: str, words_per_minute: int = 150) -> float:
    """Estimate video length based on text"""
    word_count = len(text.split())
    minutes = word_count / words_per_minute
    return minutes * 60  # Convert to seconds
