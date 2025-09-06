import os, pickle, logging
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

class DriveClient:
    def __init__(self, credentials_path: str = "credentials.json", token_path: str = "token.pickle"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self._service = None

    def service(self):
        if self._service:
            return self._service

        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, "rb") as f:
                creds = pickle.load(f)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, "wb") as f:
                pickle.dump(creds, f)

        self._service = build("drive", "v3", credentials=creds)
        return self._service

    def upload_png(self, local_path: str, folder_id: Optional[str] = None) -> str:
        meta = {"name": os.path.basename(local_path)}
        if folder_id:
            meta["parents"] = [folder_id]

        media = MediaFileUpload(local_path, mimetype="image/png")
        file = (
            self.service()
            .files()
            .create(
                body=meta,
                media_body=media,
                fields="id, parents",
                supportsAllDrives=True, 
            )
            .execute()
        )
        file_id = file["id"]
        logger.info("Uploaded to Drive: %s -> fileId=%s", local_path, file_id)
        return file_id
