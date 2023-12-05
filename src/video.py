import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_info: str) -> None:
        self.video_info = video_info
        self.video = self.youtube.videos().list(id=self.video_info, part='snippet,statistics').execute()
        self.video_id = self.video['items'][0]['id']
        self.title = self.video['items'][0]['snippet']['title']
        self.video_url = self.video['items'][0]['snippet']['thumbnails']['default']['url']
        self.video_number_views = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
