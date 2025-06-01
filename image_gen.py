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
