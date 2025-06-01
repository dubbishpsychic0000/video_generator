import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import config

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_authenticated_service():
    """Get authenticated YouTube service"""
    credentials = None
    
    # Load existing credentials
    if os.path.exists('credentials/token.pickle'):
        with open('credentials/token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/client_secrets.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save credentials for next run
        os.makedirs('credentials', exist_ok=True)
        with open('credentials/token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    
    return build('youtube', 'v3', credentials=credentials)

def upload_to_youtube(video_path: str, title: str, description: str):
    """Upload video to YouTube"""
    try:
        youtube = get_authenticated_service()
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['shorts', 'ai', 'automation', 'educational'],
                'categoryId': '27'  # Education category
            },
            'status': {
                'privacyStatus': 'public'  # or 'private' for testing
            }
        }
        
        # Create media upload
        media = MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        # Execute upload
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = request.execute()
        
        print(f"Video uploaded successfully!")
        print(f"Video ID: {response['id']}")
        print(f"Video URL: https://www.youtube.com/watch?v={response['id']}")
        
        return response
        
    except Exception as e:
        print(f"Error uploading to YouTube: {e}")
        raise

if __name__ == "__main__":
    # Test upload (requires valid video file and credentials)
    print("Testing YouTube upload...")
    # upload_to_youtube("test_video.mp4", "Test Video", "Test description")
