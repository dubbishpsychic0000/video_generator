from moviepy.editor import *
import config
import os

def create_video(image_path: str, audio_path: str, output_path: str) -> str:
    """Create a video from image and audio"""
    try:
        # Load audio to get duration
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration
        
        # Load and prepare image
        image = ImageClip(image_path, duration=audio_duration)
        
        # Resize image to fit video dimensions while maintaining aspect ratio
        image = image.resize(height=config.VIDEO_HEIGHT)
        
        # If image is wider than video width, crop it
        if image.w > config.VIDEO_WIDTH:
            image = image.crop(
                x_center=image.w/2,
                width=config.VIDEO_WIDTH
            )
        
        # Center the image if it's narrower than video width
        if image.w < config.VIDEO_WIDTH:
            image = image.on_color(
                size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                color=(0, 0, 0),
                pos='center'
            )
        
        # Set video properties
        image = image.set_fps(config.VIDEO_FPS)
        
        # Add fade in/out effects
        image = image.fadein(0.5).fadeout(0.5)
        audio = audio.fadein(0.2).fadeout(0.2)
        
        # Combine image and audio
        final_video = image.set_audio(audio)
        
        # Write video file
        final_video.write_videofile(
            output_path,
            fps=config.VIDEO_FPS,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None  # Suppress moviepy logs
        )
        
        # Clean up
        audio.close()
        image.close()
        final_video.close()
        
        print(f"Video created successfully: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"Error creating video: {e}")
        raise

def add_text_overlay(video_clip, text: str, fontsize: int = 50):
    """Add text overlay to video (optional enhancement)"""
    try:
        # Create text clip
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            color='white',
            font='Arial-Bold',
            stroke_color='black',
            stroke_width=2
        ).set_position(('center', 'bottom')).set_duration(video_clip.duration)
        
        # Composite video with text
        final_video = CompositeVideoClip([video_clip, txt_clip])
        return final_video
        
    except Exception as e:
        print(f"Error adding text overlay: {e}")
        return video_clip

def create_video_with_effects(image_path: str, audio_path: str, output_path: str, 
                            add_zoom: bool = True, add_text: str = None) -> str:
    """Create video with additional effects"""
    try:
        # Load audio
        audio = AudioFileClip(audio_path)
        audio_duration = audio.duration
        
        # Load image
        image = ImageClip(image_path, duration=audio_duration)
        
        # Resize and fit image
        image = image.resize(height=config.VIDEO_HEIGHT)
        if image.w > config.VIDEO_WIDTH:
            image = image.crop(x_center=image.w/2, width=config.VIDEO_WIDTH)
        elif image.w < config.VIDEO_WIDTH:
            image = image.on_color(
                size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                color=(0, 0, 0),
                pos='center'
            )
        
        # Add zoom effect if requested
        if add_zoom and audio_duration > 5:
            # Subtle zoom in effect
            image = image.resize(lambda t: 1 + 0.02 * t / audio_duration)
        
        # Set FPS
        image = image.set_fps(config.VIDEO_FPS)
        
        # Add fade effects
        image = image.fadein(0.5).fadeout(0.5)
        audio = audio.fadein(0.2).fadeout(0.2)
        
        # Add text overlay if provided
        if add_text:
            image = add_text_overlay(image, add_text)
        
        # Combine video and audio
        final_video = image.set_audio(audio)
        
        # Write video
        final_video.write_videofile(
            output_path,
            fps=config.VIDEO_FPS,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None
        )
        
        # Cleanup
        audio.close()
        image.close()
        final_video.close()
        
        return output_path
        
    except Exception as e:
        print(f"Error creating enhanced video: {e}")
        # Fall back to basic video creation
        return create_video(image_path, audio_path, output_path)

if __name__ == "__main__":
    # Test video creation
    if os.path.exists("test_image.jpg") and os.path.exists("test_voice.mp3"):
        test_video = create_video("test_image.jpg", "test_voice.mp3", "test_output.mp4")
        print(f"Test video created: {test_video}")
    else:
        print("Test files not found. Create test_image.jpg and test_voice.mp3 first.")
