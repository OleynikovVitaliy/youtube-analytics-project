import datetime
import os

import isodate
from googleapiclient.discovery import build
from isodate import parse_duration


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = self.build_youtube_service()
        self.playlist_info = self.get_playlist_info()
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def build_youtube_service(self):
        return build('youtube', 'v3', developerKey=self.api_key)

    def get_playlist_info(self):
        request = self.youtube.playlists().list(part="snippet", id=self.playlist_id)
        response = request.execute()
        return response['items'][0]['snippet']

    @property
    def title(self):
        return self.playlist_info['title']

    @property
    def total_duration(self):
        """возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста"""
        videos = self.youtube.playlistItems().list(part="contentDetails",
                                                   playlistId=self.playlist_id).execute()['items']
        total_duration = datetime.timedelta()
        for video in videos:
            video_id = video["contentDetails"]["videoId"]
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails,topicDetails',
                id=video_id).execute()
            content_details = video_response['items'][0]['contentDetails']
            duration = content_details.get('duration', '')
            if duration:
                parsed_duration = parse_duration(duration)
                total_duration += parsed_duration
        return total_duration

    def get_video_ids(self):
        videos = self.youtube.playlistItems().list(part="contentDetails",
                                                   playlistId=self.playlist_id).execute()['items']
        return [video["contentDetails"]["videoId"] for video in videos]

    @property
    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails', maxResults=50).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()

        video_like_count = 0
        video_url = ''

        for video in video_response['items']:
            like_count = int(video['statistics']['likeCount'])

            if like_count > video_like_count:
                video_like_count = like_count
                video_url = f"https://youtu.be/{video['id']}"

        return video_url
