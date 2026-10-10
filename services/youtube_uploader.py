import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import YOUTUBE_CLIENT_SECRETS_FILE


class YouTubeUploader:
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    def __init__(self):
        self.client_secrets_file = YOUTUBE_CLIENT_SECRETS_FILE

    def get_service(self):
        if not os.path.exists(self.client_secrets_file):
            raise FileNotFoundError(
                f"Missing {self.client_secrets_file}. Download your OAuth client JSON from Google Cloud Console."
            )

        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    self.SCOPES,
                )
                creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token_file:
                    token_file.write(creds.to_json())

        return build("youtube", "v3", credentials=creds)

    def upload_video(self, video_path: str, title: str, description: str):
        youtube = self.get_service()

        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": ["AI", "YouTube Shorts", "automation", "content creation"],
                "categoryId": "22",
            },
            "status": {"privacyStatus": "private"},
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media,
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Upload progress: {int(status.progress() * 100)}%")

        return {
            "status": "uploaded",
            "video_id": response.get("id"),
            "title": title,
            "privacy": "private",
        }
