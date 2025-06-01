from gtts import gTTS
import os
import config

def generate_voice(text: str, output_path: str) -> str:
    """Convert text to speech using Google TTS"""
    try:
        # Create TTS object
        tts = gTTS(
            text=text,
            lang=config.VOICE_LANGUAGE,
            slow=False
        )
        
        # Save audio file
        tts.save(output_path)
        
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Failed to create audio file at {output_path}")
            
        return output_path
        
    except Exception as e:
        print(f"Error generating voice: {e}")
        raise
