import os
from typing import List
from dotenv import load_dotenv
from utils import get_playlist_id
from dataclasses import dataclass, field
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi


load_dotenv()


@dataclass
class GoogleApiClientDiscovery:
    service_name: str = "youtube"
    version: str = "V3"
    youtube_api_key: str = os.environ.get("YOUTUBE_API_KEY")
    channel_id: str = os.environ.get("YOUTUBE_CHANNEL_ID_HUBERMAN")
    channel_part: str = "contentDetails"
    playlist_part: List[str] = field(default_factory=lambda: ["id", "snippet"])
    videos_part: str = "contentDetails"


class YoutubeApi:

    def __init__(self) -> None:
        self.youtube_discovery = GoogleApiClientDiscovery()
        self.youtube = self._initialize()

    def _initialize(self):
        return build(
            serviceName=self.youtube_discovery.service_name,
            version=self.youtube_discovery.version,
            developerKey=self.youtube_discovery.youtube_api_key
        )

    def send_request_for_channel_videos(self):
        return self.youtube.channels().list(
            part=self.youtube_discovery.channel_part,
            id=self.youtube_discovery.channel_id).execute()

    def send_request_for_playlist_videos(self, next_page_token=None):
        return self.youtube.playlistItems().list(
            part=self.youtube_discovery.playlist_part,
            playlistId=self.get_playlist_id(),
            maxResults=50,
            pageToken=next_page_token).execute()

    def send_request_for_videos(self, video_id):
        return self.youtube.videos().list(part=self.youtube_discovery.videos_part,
                                          id=video_id).execute()

    def get_playlist_id(self):
        response = self.send_request_for_channel_videos()
        return get_playlist_id(response)

    def get_transcripts(self, video_id: str):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, languages=["en"])
            return transcript
        except Exception as e:
            print(
                f"Could not retrieve transcript for video {video_id}: {str(e)}")
            return None
