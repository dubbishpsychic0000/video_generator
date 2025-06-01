import google.generativeai as genai
import config

def generate_script(topic: str) -> str:
    """Generate a video script using Gemini AI"""
    if not config.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Create a 45-50 second YouTube Shorts script about: {topic}
    
    Requirements:
    - Hook the viewer in the first 3 seconds
    - Make it educational and engaging
    - Use simple language
    - Include a surprising fact or statistic
    - End with a call-to-action (like/subscribe)
    - Keep it under 150 words
    - Write in a conversational tone
    
    Format: Just return the script text, no extra formatting.
    """
    
    try:
        response = model.generate_content(prompt)
        script = response.text.strip()
        
        if len(script) < 50:
            raise ValueError("Generated script is too short")
            
        return script
        
    except Exception as e:
        print(f"Error generating script: {e}")
        # Fallback script
        return f"Did you know that {topic.lower()} is more fascinating than you think? Let me explain why this matters in just 60 seconds. Like and subscribe for more amazing facts!"

if __name__ == "__main__":
    # Test script generation
    test_script = generate_script("Why bridges have expansion joints")
    print("Generated script:")
    print(test_script)
