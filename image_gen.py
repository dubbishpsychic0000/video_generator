import requests
import os
import config
from PIL import Image

def get_background_image(topic: str, output_path: str) -> str:
    """Get background image from Pexels API"""
    if config.PEXELS_API_KEY:
        return fetch_pexels_image(topic, output_path)
    else:
        return create_default_image(topic, output_path)

def fetch_pexels_image(topic: str, output_path: str) -> str:
    """Fetch image from Pexels API"""
    headers = {
        'Authorization': config.PEXELS_API_KEY
    }
    
    # Search for images
    search_url = f"https://api.pexels.com/v1/search"
    params = {
        'query': topic,
        'per_page': 1,
        'orientation': 'portrait'  # Better for vertical video
    }
    
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data['photos']:
            image_url = data['photos'][0]['src']['large']
            
            # Download image
            img_response = requests.get(image_url)
            img_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(img_response.content)
                
            # Resize to video dimensions
            resize_image_for_video(output_path)
            return output_path
        else:
            print("No images found, using default")
            return create_default_image(topic, output_path)
            
    except Exception as e:
        print(f"Error fetching Pexels image: {e}")
        return create_default_image(topic, output_path)

def create_default_image(topic: str, output_path: str) -> str:
    """Create a simple default background image"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Create image with video dimensions
    img = Image.new('RGB', (config.VIDEO_WIDTH, config.VIDEO_HEIGHT), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a better font
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
    
    # Add topic text
    text = topic.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (config.VIDEO_WIDTH - text_width) // 2
    y = (config.VIDEO_HEIGHT - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    img.save(output_path)
    return output_path

def resize_image_for_video(image_path: str):
    """Resize image to fit video dimensions"""
    with Image.open(image_path) as img:
        # Resize to video dimensions while maintaining aspect ratio
        img = img.resize((config.VIDEO_WIDTH, config.VIDEO_HEIGHT), Image.Resampling.LANCZOS)
        img.save(image_path)

if __name__ == "__main__":
    # Test image generation
    test_image = get_background_image("engineering", "test_image.jpg")
    print(f"Image created: {test_image}")
