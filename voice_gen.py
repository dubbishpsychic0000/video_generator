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

def generate_voice_pyttsx3(text: str, output_path: str) -> str:
    """Alternative TTS using pyttsx3 (offline)"""
    import pyttsx3
    
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1.0)  # Volume level
    
    # Save to file
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    
    return output_path

if __name__ == "__main__":
    # Test voice generation
    test_text = "This is a test of the text to speech system."
    output = generate_voice(test_text, "test_voice.mp3")
    print(f"Voice generated: {output}")

