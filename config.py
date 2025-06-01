import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY')
YOUTUBE_CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
YOUTUBE_CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')

# Video Settings
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # 9:16 aspect ratio for Shorts
VIDEO_FPS = 30
VIDEO_DURATION = 60  # Maximum duration in seconds

# Audio Settings
VOICE_LANGUAGE = 'en'
AUDIO_BITRATE = '128k'

# File Paths
TEMP_DIR = 'temp'
TEMP_AUDIO_PATH = os.path.join(TEMP_DIR, 'audio.mp3')
TEMP_IMAGE_PATH = os.path.join(TEMP_DIR, 'background.jpg')
TEMP_VIDEO_PATH = os.path.join(TEMP_DIR, 'output_video.mp4')

# Default Settings
DEFAULT_TOPIC = "Amazing engineering facts"
UPLOAD_TO_YOUTUBE = False  # Set to True when ready to upload
CLEAN_TEMP_FILES = True

# YouTube Settings
YOUTUBE_CATEGORY_ID = '27'  # Education
YOUTUBE_PRIVACY_STATUS = 'public'  # 'public', 'private', or 'unlisted'
YOUTUBE_TAGS = ['shorts', 'ai', 'automation', 'educational', 'facts']

# Script Generation Settings
MAX_SCRIPT_LENGTH = 150  # words
TARGET_VIDEO_LENGTH = 50  # seconds
WORDS_PER_MINUTE = 150

# Image Settings
IMAGE_SEARCH_ORIENTATION = 'portrait'
IMAGE_QUALITY = 'large'
