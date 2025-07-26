import os
import sys
import json
import time
import re

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from tqdm import tqdm

# 🔐 OAuth 2.0 scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# 🔑 OAuth credentials file from Google Cloud Console
CLIENT_SECRET_FILE = "client_secret_66416017636-vl49b9am6792t1k9g02rasr9ng9t0omj.apps.googleusercontent.com.json"

# ✅ Authenticate and return YouTube API client
def authenticate_youtube():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)

# ✅ Upload one video
def upload_video(youtube, video_path, title, description, language, tags, category_id="20", privacy_status="public"):
    def attempt_upload(current_title):
        print(f"🚀 Uploading: {video_path} as '{current_title}'")
        if not os.path.exists(video_path):
            print(f"❌ File not found: {video_path}")
            return False

        try:
            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": current_title,
                        "description": description,
                        "tags": tags,
                        "categoryId": category_id,
                        "defaultLanguage": language,
                        "defaultAudioLanguage": language
                    },
                    "status": {"privacyStatus": privacy_status}
                },
                media_body=MediaFileUpload(video_path, resumable=True),
            )

            progress = tqdm(total=100, desc=f"Uploading {current_title}", bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}%", leave=False)
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress.update(int(status.progress() * 100) - progress.n)

            progress.close()

            if "id" in response:
                print(f"✅ Uploaded successfully → https://youtu.be/{response['id']}")
                return True
            else:
                print(f"❌ Upload failed for {current_title}")
                return False

        except Exception as e:
            print(f"❌ Upload error: {e}")
            return False

    return attempt_upload(title)

# ✅ Upload all videos using metadata.json
def bulk_upload_with_metadata(folder, metadata_path):
    youtube = authenticate_youtube()

    with open(metadata_path, "r", encoding="utf-8") as f:
        videos = json.load(f)

    for video in videos:
        video_path = os.path.join(folder, video["file"])
        title = video["title"]
        description = f"{video['description']}\n\n{video['hashtags']}"
        tags = [tag.strip() for tag in video["tags"].split(",")]
        lang = video["language"]

        upload_video(
            youtube,
            video_path,
            title=title,
            description=description,
            tags=tags,
            language=lang,
            category_id="20",
            privacy_status="public"
        )

        time.sleep(10)

    print("✅ All videos uploaded using metadata.")

# ✅ Entry point
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("❌ Usage: python youtube_uploader.py <video_folder> <metadata.json>")
        sys.exit(1)

    VIDEO_FOLDER = sys.argv[1]
    metadata_file = sys.argv[2]
    bulk_upload_with_metadata(VIDEO_FOLDER, metadata_file)