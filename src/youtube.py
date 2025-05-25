## responsible for uploading videos to youtube
#
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError, Error


def upload_video(video_file, title, description, category_id="22", privacy_status="public"):
    SCOPES = ["https://www.googleapis.com/auth/youtube"]

    # Authenticate and get credentials
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", SCOPES)
    
    credentials = flow.run_local_server(host='localhost',
        port=8080, 
        authorization_prompt_message='Please visit this URL: {url}', 
        success_message='The auth flow is complete; you may close this window.',
        open_browser=True)
    
    # Build the API client
    with googleapiclient.discovery.build("youtube", "v3", credentials=credentials) as youtube:
        request_body = {
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy_status
            }
        }

        # Attach the video file
        media_file = MediaFileUpload(video_file, resumable=True)

        # Upload
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        )
        
        try:
            response = request.execute()
        except HttpError as e:
            print('Error response status code : {0}, reason : {1}'.format(e.status_code, e.error_details))

        print(f"✅ Upload successful! Video URL: https://youtu.be/{response['id']}")
